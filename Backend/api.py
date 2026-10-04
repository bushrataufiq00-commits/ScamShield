from email import message

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main import check_message, check_url

from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
def analyze_with_ai(message):

    try:

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"""
Analyze the following message for scam or phishing indicators.

Message:
{message}

Identify:
1. Whether the message appears suspicious.
2. The main scam tactics used.
3. What the user should be careful about.

Give a short and simple explanation.
"""
        )

        return response.text

    except Exception as e:

        print("Gemini AI error:", e)

        return "AI analysis is temporarily unavailable. The result shown above is based on ScamShield's rule-based detection."


app = FastAPI(title="ScamShield AI")


# Allow the frontend to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "ScamShield AI API is running"
    }

@app.post("/analyze/message")
def analyze_message(message: str):

    # Run our existing rule-based detection
    score, result, reasons = check_message(message)

   # Use Gemini only when the rule-based result is uncertain
    if 20 <= score < 60:
         ai_analysis = analyze_with_ai(message)
    else:
         ai_analysis = "AI analysis was not required. The result was determined using ScamShield's rule-based detection."

    return {
    "risk_score": score,
    "result": result,
    "reasons": reasons,
    "ai_analysis": ai_analysis
}

@app.post("/analyze/url")
def analyze_url(url: str):

    score, result, reasons = check_url(url)

    return {
        "risk_score": score,
        "result": result,
        "reasons": reasons
    }