# engine/gemini_engine.py

import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def run_gemini_query(query):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(query)
    return response.text
