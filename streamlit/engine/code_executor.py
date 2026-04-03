# engine/code_executor.py

import ast
import sys
import io
import re
import subprocess
import traceback


# ============ PYTHON ============

def check_syntax(code, language="Python"):
    """Route syntax check to the correct language handler."""
    if language == "Python":
        return _check_python_syntax(code)
    elif language == "Shell":
        return _check_shell_syntax(code)
    elif language == "PL/SQL":
        return _check_plsql_syntax(code)
    return {"valid": False, "message": "❌ Unknown language."}


def _check_python_syntax(code):
    """Check Python syntax using ast.parse."""
    try:
        ast.parse(code)
        return {"valid": True, "message": "✅ Python syntax is correct."}
    except SyntaxError as e:
        return {
            "valid": False,
            "message": f"❌ Syntax Error at line {e.lineno}: {e.msg}",
            "line": e.lineno,
            "offset": e.offset,
        }


# Blocked keywords for Python sandbox safety
_BLOCKED_KEYWORDS = {"import os", "import sys", "import subprocess", "import shutil",
                     "__import__", "eval(", "exec(", "compile(", "open(",
                     "os.system", "os.popen", "subprocess.run", "subprocess.call"}


def _is_safe_python(code):
    code_lower = code.lower()
    for keyword in _BLOCKED_KEYWORDS:
        if keyword.lower() in code_lower:
            return False, f"🚫 Blocked: `{keyword}` is not allowed in sandbox mode."
    return True, ""


def run_code(code, language="Python"):
    """Execute code based on language selection."""
    if language == "Python":
        return _run_python(code)
    elif language == "Shell":
        return _run_shell(code)
    elif language == "PL/SQL":
        return {
            "output": "",
            "error": "ℹ️ PL/SQL cannot be executed locally (needs an Oracle database).\nUse **Check Syntax** or **AI Review** instead.",
            "success": False,
        }
    return {"output": "", "error": "Unknown language.", "success": False}


def _run_python(code):
    """Execute Python code in a restricted environment."""
    syntax = _check_python_syntax(code)
    if not syntax["valid"]:
        return {"output": "", "error": syntax["message"], "success": False}

    safe, reason = _is_safe_python(code)
    if not safe:
        return {"output": "", "error": reason, "success": False}

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = captured_out = io.StringIO()
    sys.stderr = captured_err = io.StringIO()

    try:
        exec(code, {"__builtins__": __builtins__}, {})
        output = captured_out.getvalue()
        error = captured_err.getvalue()
        return {
            "output": output if output else "(No output)",
            "error": error if error else "",
            "success": True,
        }
    except Exception:
        return {
            "output": captured_out.getvalue(),
            "error": traceback.format_exc(),
            "success": False,
        }
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


# ============ SHELL / BASH ============

# Blocked shell commands for safety
_BLOCKED_SHELL = {"rm -rf", "mkfs", "dd if=", ":(){", "fork bomb",
                  "shutdown", "reboot", "halt", "poweroff",
                  "format c:", "del /f /s /q", "rd /s /q"}


def _is_safe_shell(code):
    code_lower = code.lower()
    for keyword in _BLOCKED_SHELL:
        if keyword in code_lower:
            return False, f"🚫 Blocked: `{keyword}` is not allowed in sandbox mode."
    return True, ""


def _check_shell_syntax(code):
    """Check shell/PowerShell syntax by writing to a temp file and parsing it."""
    import tempfile, os
    if sys.platform == "win32":
        try:
            # Write code to a temp .ps1 file and use PowerShell's parser
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
                f.write(code)
                tmp_path = f.name
            try:
                ps_cmd = (
                    f"$errors = $null; "
                    f"[System.Management.Automation.Language.Parser]::ParseFile('{tmp_path}', [ref]$null, [ref]$errors); "
                    f"if ($errors.Count -gt 0) {{ foreach ($e in $errors) {{ Write-Error $e.Message }}; exit 1 }} "
                    f"else {{ Write-Output 'OK' }}"
                )
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", ps_cmd],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0:
                    return {"valid": True, "message": "✅ Shell/PowerShell syntax is correct."}
                else:
                    err = result.stderr.strip()
                    return {"valid": False, "message": f"❌ Shell Syntax Error:\n{err}"}
            finally:
                os.unlink(tmp_path)
        except Exception as e:
            return {"valid": False, "message": f"⚠️ Syntax check failed: {e}"}
    else:
        try:
            result = subprocess.run(
                ["bash", "-n", "-c", code],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return {"valid": True, "message": "✅ Shell syntax is correct."}
            else:
                return {"valid": False, "message": f"❌ Shell Syntax Error:\n{result.stderr.strip()}"}
        except FileNotFoundError:
            return {"valid": False, "message": "❌ Bash not found. Install Git Bash or WSL on Windows."}


def _run_shell(code):
    """Execute shell commands in a sandboxed subprocess."""
    safe, reason = _is_safe_shell(code)
    if not safe:
        return {"output": "", "error": reason, "success": False}

    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", code],
                capture_output=True, text=True, timeout=15
            )
        else:
            result = subprocess.run(
                ["bash", "-c", code],
                capture_output=True, text=True, timeout=15
            )
        output = result.stdout.strip()
        error = result.stderr.strip()
        return {
            "output": output if output else "(No output)",
            "error": error if error else "",
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"output": "", "error": "⏰ Timeout: command took too long (15s limit).", "success": False}
    except Exception:
        return {"output": "", "error": traceback.format_exc(), "success": False}


# ============ PL/SQL ============

_PLSQL_KEYWORDS = {
    "blocks": ["BEGIN", "END", "DECLARE", "EXCEPTION"],
    "dml": ["SELECT", "INSERT", "UPDATE", "DELETE", "MERGE"],
    "ddl": ["CREATE", "ALTER", "DROP", "TRUNCATE"],
    "plsql": ["PROCEDURE", "FUNCTION", "PACKAGE", "TRIGGER", "CURSOR", "LOOP", "IF", "ELSIF", "ELSE", "WHILE", "FOR"],
}


def _check_plsql_syntax(code):
    """PL/SQL syntax validation with structural and common error checks."""
    code_upper = code.upper().strip()
    errors = []

    # Strip comments for analysis
    lines_raw = code.strip().split('\n')
    lines = []
    line_map = []  # maps cleaned line index → original line number
    in_block_comment = False
    for i, line in enumerate(lines_raw):
        stripped = line.strip()
        # Handle block comments
        if '/*' in stripped:
            in_block_comment = True
        if '*/' in stripped:
            in_block_comment = False
            continue
        if in_block_comment or stripped.startswith('--') or stripped == '' or stripped == '/':
            continue
        lines.append(stripped)
        line_map.append(i + 1)

    if not lines:
        return {"valid": False, "message": "❌ No PL/SQL code found (only comments or empty lines)."}

    # 1. Check matching BEGIN/END
    begin_count = len(re.findall(r'\bBEGIN\b', code_upper))
    end_count = len(re.findall(r'\bEND\s*;', code_upper))
    if begin_count > end_count:
        errors.append(f"❌ Missing END; — found {begin_count} BEGIN but only {end_count} END;")
    elif end_count > begin_count:
        errors.append(f"❌ Extra END; — found {end_count} END; but only {begin_count} BEGIN")

    # 2. Check matching IF/END IF
    if_count = len(re.findall(r'\bIF\b', code_upper)) - len(re.findall(r'\bELSIF\b', code_upper))
    end_if_count = len(re.findall(r'\bEND\s+IF\b', code_upper))
    if if_count > end_if_count:
        errors.append(f"❌ Missing END IF; — found {if_count} IF but only {end_if_count} END IF")

    # 3. Check matching LOOP/END LOOP
    loop_count = len(re.findall(r'\bLOOP\b', code_upper)) - len(re.findall(r'\bEND\s+LOOP\b', code_upper))
    end_loop_count = len(re.findall(r'\bEND\s+LOOP\b', code_upper))
    if loop_count > end_loop_count:
        errors.append(f"❌ Missing END LOOP; — found unmatched LOOP blocks")

    # 4. Check parentheses balance
    open_parens = code.count('(')
    close_parens = code.count(')')
    if open_parens != close_parens:
        errors.append(f"❌ Mismatched parentheses: {open_parens} opening '(' vs {close_parens} closing ')'")

    # 5. Check each line for missing semicolons
    skip_start = {"BEGIN", "DECLARE", "EXCEPTION", "ELSE", "ELSIF", "IF", "LOOP",
                  "FOR", "WHILE", "THEN", "CREATE", "AS", "IS", "OR", "AND", "/*", "--"}
    skip_end = {"END;", "END", "/", "BEGIN", "THEN", "LOOP", "ELSE", "IS", "AS", "DECLARE", "EXCEPTION"}

    for idx, line in enumerate(lines):
        lu = line.upper().rstrip(';').strip()
        # Skip structural keywords and block boundaries
        if any(lu.startswith(k) for k in skip_start):
            continue
        if lu in skip_end:
            continue
        # Lines with executable content should end with semicolon
        if line.rstrip() and not line.rstrip().endswith(';') and not line.rstrip().endswith(','):
            # Check if it's a statement-like line
            if any(lu.startswith(k) for k in ["SELECT", "INSERT", "UPDATE", "DELETE",
                                                "DBMS_", "RETURN", "RAISE", "NULL",
                                                "V_", "L_", "P_", "COMMIT", "ROLLBACK",
                                                "OPEN", "CLOSE", "FETCH", "EXIT"]):
                errors.append(f"⚠️ Line {line_map[idx]}: missing semicolon → `{line}`")

    # 6. Check DECLARE has BEGIN
    if 'DECLARE' in code_upper and 'BEGIN' not in code_upper:
        errors.append("❌ DECLARE block found but no BEGIN — did you forget BEGIN?")

    # 7. Check for common typos
    common_typos = {
        r'\bDBMS_OUTUT\b': 'DBMS_OUTPUT',
        r'\bVARCHR2\b': 'VARCHAR2',
        r'\bINTEGR\b': 'INTEGER',
        r'\bEXCEPTON\b': 'EXCEPTION',
        r'\bPROCEDURE\s+\w+\s*\(.*\)\s*BEGIN\b': 'Missing IS/AS before BEGIN',
    }
    for pattern, fix in common_typos.items():
        if re.search(pattern, code_upper):
            errors.append(f"⚠️ Possible typo: did you mean `{fix}`?")

    if errors:
        return {"valid": False, "message": "\n".join(errors)}

    return {"valid": True, "message": "✅ PL/SQL structure looks correct. (Full validation needs Oracle DB)"}
