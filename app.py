import streamlit as st
import litellm
import os
import time
from dotenv import load_dotenv

load_dotenv()
for key in ["GEMINI_API_KEY", "GROQ_API_KEY", "ANTHROPIC_API_KEY"]:
    val = os.getenv(key) or st.secrets.get(key, "")
    if val:
        os.environ[key] = val
SYSTEM = "You are an expert options and swing trader AND a knowledgeable AI assistant. For trade ideas: give direction, key risks, and a yes/no recommendation. For general questions: answer helpfully and concisely."

st.title("AI Consensus Hub")
query = st.text_area("Enter your question or trade idea:")

def ask_ai(model, query):
    for attempt in range(3):
        try:
            r = litellm.completion(model=model, max_tokens=500, messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": query}])
            return r.choices[0].message.content
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                return f"Error: {str(e)}"

if st.button("Ask All AIs"):
    with st.spinner("Consulting AIs..."):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gemini")
            gemini_response = ask_ai("gemini/gemini-3.5-flash-lite", query)
            st.write(gemini_response)
        with col2:
            st.subheader("Groq")
            groq_response = ask_ai("groq/qwen/qwen3.8-27b", query)
            st.write(groq_response)
        st.subheader("Claude - Final Verdict")
        claude_prompt = f"Trade: {query}\nGemini: {gemini_response}\nGroq: {groq_response}\nChallenge both. Give YES or NO verdict in 3 sentences."
        st.write(ask_ai("anthropic/claude-haiku-4-5", claude_prompt))
        st.subheader("Consensus")
        st.info("2 out of 3 AIs must agree to confirm the trade.")
