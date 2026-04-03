# engine/groq_engine.py

from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL


def run_groq_query(query):
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content


def review_code(code, language="Python"):
    """Ask AI to review code: check for bugs, suggest improvements, explain."""
    client = Groq(api_key=GROQ_API_KEY)

    lang_hints = {
        "Python": "python",
        "Shell": "bash/PowerShell",
        "PL/SQL": "Oracle PL/SQL",
    }
    lang = lang_hints.get(language, language)

    prompt = f"""You are a {lang} tutor helping a beginner. Review the following code and provide:
1. **Syntax & Bug Check** — any errors or bugs? Point to exact lines.
2. **Suggestions** — how to improve it (readability, performance, best practices)
3. **Explanation** — a brief explanation of what the code does (for learning)
4. **Corrected Code** — if there are bugs, show the fixed version

Keep it concise and beginner-friendly. Use simple language.

```{language.lower()}
{code}
```"""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
