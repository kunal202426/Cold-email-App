import os
import re
import json
import time
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """ABSOLUTE LIMIT: The email body must be 80-120 words. 
Count before outputting. If it exceeds 120 words, CUT IT. 
Do not explain, do not add caveats, just cut.

You write cold emails for Kunal Mathur.

KUNAL'S BACKGROUND:
Final-year CSE (Blockchain) @ VIT Vellore. Interning at YES Bank 
building production features for a high-throughput trading platform 
(React, Node.js, FastAPI). Shipped ML pipelines, distributed systems, 
and blockchain projects end-to-end. Available for full-time SWE roles 
from July 2026.
Portfolio: https://portfolio-kunal26.vercel.app
LinkedIn: https://linkedin.com/in/kunal-mathur-612108267

KUNAL'S PROJECTS (pick ONE most relevant per email):
1. Distributed Systems Design Simulator — ReactFlow, FastAPI, 
   WebSockets, chaos engineering, metrics dashboard.
2. Hybrid Stock Price Prediction System — LSTM, LightGBM, FinBERT, 
   ETL pipelines, real-time forecasting.
3. CityFlow: 3D City Simulation & Analytics — Three.js, React, 
   real-time logistics analytics.
4. Real Time Eye Tracking Inference System — Python, CV, 
   Deep Learning, gaze estimation.
5. Fertilizer Subsidy Platform — Blockchain/Web3, Solidity, 
   Ethereum DApp.
6. Multi Source Job Aggregator — ETL, Scraper, 
   scoring model for ranking opportunities.

SUBJECT LINE:
Format: "Application at [Company Name]"
Example: "Application at HDFC"
Nothing else. No work mentioned. No hooks. No questions.

STRUCTURE (3 short paragraphs, flowing prose):
Paragraph 1 — HOOK + BRIDGE:
  Open with a factual observation about what the company is known for 
  technically — stated as fact, not as "I noticed" or "I've been following." 
  Write it like you're telling someone else about the company, not performing 
  interest to the recipient. Connect it to Kunal's work in one direct sentence.
  BANNED openers: "I've been following", "I noticed your work on", "I came across", 
  "I've been impressed by", "I admire"

Paragraph 2 — PROOF:
  One project from the list. One sentence. One hard detail. 
  No hedging words like "I believe", "could benefit", "highly relevant."

Paragraph 3 — ASK + CLOSE:
  Anchor to their technical domain.
  ASK paragraph must include exactly: "looking for full-time roles from July 2026"

HARD RULES:
- 80-120 words body MAX
- COMPANY NAME: The company's name must appear at least once in the email body, naturally in a sentence. Never write an email where the company is unidentifiable.
- PARAGRAPH BREAKS (STRICT): The body must have exactly 3 paragraphs. After every paragraph, add a blank line (\\n\\n in JSON). Never merge hook, proof, and ask into one block. 
  Example structure in JSON:
  "body": "Hook sentence. Bridge sentence.\\n\\nProof sentence.\\n\\nAsk sentence. Happy to share more if it's relevant — links below."
- STOP AI PATTERNS - NEVER USE: "aligns directly", "I believe", "mutually beneficial", "explore opportunities", "quick learner", "team player", "directly relates to", "honed my skills", "resilient and observable", "I believe my background could be valuable", "given your focus on"
- INDUSTRY AWARENESS: match the problem space to their actual domain. Never default to fintech unless they are a finance company.

SIGNAL FORMAT (exact order, no changes):
Happy to share more if it's relevant — links below.

Check my work at:
https://portfolio-kunal26.vercel.app
https://linkedin.com/in/kunal-mathur-612108267

— Kunal Mathur | +91 7597209058
"""

# Using 'gemini-2.5-flash-lite' as confirmed available in current tier
model = genai.GenerativeModel(
    "gemini-2.5-flash-lite",
    system_instruction=SYSTEM_PROMPT,
    generation_config=genai.GenerationConfig(
        temperature=0.4,
        max_output_tokens=500,
    )
)


def count_words(body: str) -> int:
    return len(body.split())


def generate_email(lead: dict) -> dict:
    prompt = f"""Generate the email for:
Company: {lead['company']}
HR/Recipient name: {lead.get('hr_name', 'Hiring Manager')}
One specific thing I noticed about them: {lead.get('notes', '')}
Most relevant project: Pick the best fit from the project list.

Return ONLY valid JSON, no markdown, no explanation:
{{"subject": "<5-7 word subject>", "body": "<email body>"}}
"""
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            # Handle potential markdown response
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                if "subject" in result and "body" in result:
                    word_count = count_words(result["body"])
                    if word_count > 130:
                        # Silently retry if too long
                        continue
                    return result
            raise ValueError(f"Bad response format: {text[:200]}")
        except ValueError as e:
            if attempt == 2:
                raise Exception(f"Failed after 3 retries: {str(e)}")
            time.sleep(3)
        except Exception as e:
            if "429" in str(e):
                time.sleep(60 * (attempt + 1))
            elif attempt == 2:
                raise Exception(f"Gemini error after 3 retries: {str(e)}")
            else:
                time.sleep(5)
    raise Exception("Generation failed after 3 retries")
