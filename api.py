from fastapi import FastAPI
import litellm
import os

app = FastAPI()

SYSTEM = "You are an expert options and swing trader AND a knowledgeable AI assistant. For trade ideas: give direction, key risks, and a yes/no recommendation. For general questions: answer helpfully and concisely."

def ask_ai(model, query):
    try:
        r = litellm.completion(
            model=model,
            max_tokens=500,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": query}
            ]
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/ask")
def ask(q: str):
    gemini = ask_ai("gemini/gemini-3.5-flash-lite", q)
    groq = ask_ai("groq/qwen/qwen3.8-27b", q)
    claude_prompt = f"Question: {q}\nGemini: {gemini}\nGroq: {groq}\nGive your final verdict in 3 sentences."
    claude = ask_ai("anthropic/claude-haiku-4-5", claude_prompt)
    return {"gemini": gemini, "groq": groq, "claude": claude}