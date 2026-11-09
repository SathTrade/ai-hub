import streamlit as st
import litellm
import os
import time
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

SYSTEM = "You are an expert options and swing trader. Analyze the trade idea concisely — give direction, key risks, and a yes/no recommendation."

st.title("🤖 AI Consensus Hub")
query = st.text_area("Enter your question or trade idea:")

def ask_ai(model, query):
    for attempt in range(3):
        try:
            r = litellm.completion(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": query}
                ]
            )
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
            st.subheader("🟦 Gemini")
            st.write(ask_ai("gemini/gemini-3.5-flash-lite", query))
        with col2:
            st.subheader("🟩 Groq")
            st.write(ask_ai("groq/qwen/qwen3.8-27b", query))
        st.subheader("📊 Consensus")
        st.info("Compare both answers above, then confirm with Claude chat.")