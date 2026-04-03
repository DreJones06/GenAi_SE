#streamlit_app.py
import streamlit as st

#st.write("✅ App Loaded Successfully")

from controller.task_controller import submit_task
from engine.groq_engine import run_groq_query, review_code
from engine.code_executor import check_syntax, run_code
from storage.file_store import save_result
from config.settings import DEFAULT_QUERY, RESULT_PATH

st.set_page_config(page_title="CodeBuddy AI", page_icon="🧑‍💻", layout="wide")

st.title("🧑‍💻 CodeBuddy AI")
st.caption("Your AI-powered code playground — Write, Run, Review & Learn")
st.caption("Your AI-powered search assistant — Ask anything, get instant answers")
tab1, tab2 = st.tabs(["💬 AI Query", "🧪 Code Lab"])

# ============ TAB 1: AI Query ============
with tab1:
    query = st.text_input("Enter Query", DEFAULT_QUERY, key="query_input")

    if st.button("Run Search", key="run_search_btn"):
        st.write("🔍 Running query via Groq...")
        try:
            result = run_groq_query(query)
            st.success("✅ Done")
            st.markdown(result)
        except Exception as e:
            st.error(f"Error: {e}")

# ============ TAB 2: Code Lab (Multi-Language) ============
with tab2:
    st.subheader("🧪 Code Lab — Learn & Test")
    st.caption("Write or paste code. Run it, check syntax, or get AI-powered suggestions.")

    # Language selector
    language = st.selectbox(
        "🌐 Select Language",
        ["Python", "Shell", "PL/SQL"],
        key="lang_select",
    )

    # Placeholder examples per language
    placeholders = {
        "Python": "# Example:\nfor i in range(5):\n    print(f'Hello {i}')",
        "Shell": "# Example:\necho 'Hello World'\nfor i in 1 2 3; do\n  echo \"Number: $i\"\ndone",
        "PL/SQL": "-- Example:\nDECLARE\n  v_name VARCHAR2(50) := 'Hello';\nBEGIN\n  DBMS_OUTPUT.PUT_LINE(v_name);\nEND;\n/",
    }

    code = st.text_area(
        f"Write your {language} code here:",
        height=250,
        placeholder=placeholders.get(language, ""),
        key="code_input",
    )

    col1, col2, col3 = st.columns(3)

    # --- Run Code ---
    with col1:
        run_label = "▶️ Run Code" if language != "PL/SQL" else "▶️ Run (N/A)"
        if st.button(run_label, key="run_code_btn"):
            if code.strip():
                result = run_code(code, language)
                if result["success"]:
                    st.success("✅ Executed successfully")
                    st.code(result["output"], language="text")
                else:
                    if language == "PL/SQL":
                        st.info(result["error"])
                    else:
                        st.error("❌ Execution failed")
                        st.code(result["error"], language="text")
            else:
                st.warning("Please enter some code first.")

    # --- Syntax Check ---
    with col2:
        if st.button("🔍 Check Syntax", key="syntax_btn"):
            if code.strip():
                result = check_syntax(code, language)
                if result["valid"]:
                    st.success(result["message"])
                else:
                    st.error(result["message"])
                    if "line" in result and language == "Python":
                        lines = code.split("\n")
                        if result["line"] and result["line"] <= len(lines):
                            st.code(
                                f"Line {result['line']}: {lines[result['line'] - 1]}",
                                language="python",
                            )
            else:
                st.warning("Please enter some code first.")

    # --- AI Review ---
    with col3:
        if st.button("🤖 AI Review & Suggestions", key="review_btn"):
            if code.strip():
                with st.spinner(f"AI is reviewing your {language} code..."):
                    try:
                        feedback = review_code(code, language)
                        st.markdown("### 📝 AI Review")
                        st.markdown(feedback)
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please enter some code first.")

    # --- Language Info ---
    with st.expander("ℹ️ Language Support Details"):
        st.markdown("""
        | Feature | Python | Shell | PL/SQL |
        |---------|--------|-------|--------|
        | ▶️ Run Code | ✅ Sandbox | ✅ PowerShell/Bash | ❌ Needs Oracle DB |
        | 🔍 Syntax Check | ✅ Full (`ast`) | ✅ Basic | ✅ Structural |
        | 🤖 AI Review | ✅ Groq AI | ✅ Groq AI | ✅ Groq AI |
        
        **Sandbox Safety:**
        - **Python:** Blocks `os`, `sys`, `subprocess`, `open()`, `eval()`, `exec()`
        - **Shell:** Blocks `rm -rf`, `shutdown`, `format`, destructive commands
        - **PL/SQL:** No execution — syntax check & AI review only
        """)