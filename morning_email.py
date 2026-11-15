import urllib.request, json, smtplib, os, time
from email.mime.text import MIMEText
from datetime import datetime
import pytz

et = pytz.timezone('America/Toronto')
date_str = datetime.now(et).strftime('%A %b %d, %Y')

RENDER_URL = "https://ai-hub-d0ji.onrender.com/ask?q=What+is+today%27s+market+outlook+for+SPY+QQQ+NVDA%3F+Any+key+catalysts+today%3F+Bullish+or+bearish%3F+Key+levels+to+watch."

def call_render(max_attempts=3, timeout=90):
    """Call Render API with retries — handles cold-start spin-up delay."""
    for attempt in range(max_attempts):
        try:
            with urllib.request.urlopen(RENDER_URL, timeout=timeout) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt < max_attempts - 1:
                wait = 30 * (attempt + 1)  # 30s, 60s
                print(f"Attempt {attempt+1} failed ({e}), retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise

try:
    data = call_render()
    gemini  = data.get("gemini", "No response")
    groq    = data.get("groq",   "No response")
    verdict = data.get("claude", "No response")
except Exception as e:
    gemini = groq = verdict = f"Error: {e}"

body = f"""SATH AI MORNING OUTLOOK - {date_str}
========================================

GEMINI:
{gemini}

----------------------------------------
GROQ:
{groq}

----------------------------------------
FINAL VERDICT (Claude):
{verdict}

========================================
"""
msg = MIMEText(body)
msg['Subject'] = f'[8AM ET] Sath AI Outlook - {date_str}'
msg['From']    = 'sathbotalerts@gmail.com'
msg['To']      = 'rajaguru1195@gmail.com'

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login('sathbotalerts@gmail.com', os.environ['EMAIL_PASSWORD'])
    s.send_message(msg)
print("Email sent!")
