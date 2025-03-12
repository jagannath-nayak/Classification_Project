import re
import os
import streamlit as st
import requests
from textblob import TextBlob
from dotenv import load_dotenv

# ✅ Load API Key from .env file
load_dotenv()
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")

if not huggingface_api_key:
    st.error("❌ Hugging Face API Key not found. Please check your .env file.")

# ✅ High-Risk Scam Keywords (Higher Weight)
high_risk_keywords = [
    "win", "congratulations", "free", "prize", "lottery", "click here",
    "urgent", "reward", "selected", "jackpot", "claim now", "guaranteed",
    "you have been chosen", "act fast", "limited time offer"
]

# ✅ Medium-Risk Keywords (Moderate Weight)
medium_risk_keywords = [
    "exclusive", "investment", "instant loan", "zero cost", "millionaire",
    "crypto giveaway", "no fees", "rich", "special deal"
]

# ✅ Function to Detect Phishing URLs
def detect_phishing_urls(text):
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    urls = re.findall(url_pattern, text)
    return urls if urls else None

# ✅ Improved Scam Score Calculation
def calculate_scam_score(text):
    scam_score = 0
    detected_high_risk = [word for word in high_risk_keywords if word in text.lower()]
    detected_medium_risk = [word for word in medium_risk_keywords if word in text.lower()]

    # ✅ Increase Score for High-Risk & Medium-Risk Keywords
    scam_score += len(detected_high_risk) * 20  # High-risk words increase score faster
    scam_score += len(detected_medium_risk) * 10  # Medium-risk words increase score moderately

    # ✅ Increase Score for Phishing Links
    if detect_phishing_urls(text):
        scam_score += 50  # High weight for phishing links

    # ✅ Ensure Scam Score is Between 0-100%
    scam_score = min(scam_score, 100)
    
    return scam_score, detected_high_risk + detected_medium_risk

# ✅ Function to Categorize Messages (Hugging Face API)
def categorize_message(text):
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}

        labels = ["spam", "banking", "work", "personal", "promotional", "transaction"]
        response = requests.post(API_URL, headers=headers, json={"inputs": text, "parameters": {"candidate_labels": labels}})

        if response.status_code != 200:
            return "❌ API Error"

        result = response.json()
        categories = result.get("labels", [])
        scores = result.get("scores", [])

        if categories and scores:
            return categories[0].capitalize()
        return "Unknown"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Streamlit UI
st.title("🛡 AI-Powered Scam Insights")
message_input = st.text_area("📩 Enter the SMS or Email content:")

if st.button("Analyze"):
    if message_input:
        scam_score, detected_keywords = calculate_scam_score(message_input)
        phishing_urls = detect_phishing_urls(message_input)
        category = categorize_message(message_input)

        # ✅ Display Scam Score
        st.subheader("🔍 Scam Analysis:")
        st.write(f"📊 **Scam Alert Score:** {scam_score}%")
        
        # ✅ Display Detected Scam Keywords
        if detected_keywords:
            st.write(f"⚠️ **Detected Scam Keywords:** {', '.join(detected_keywords)}")
        
        # ✅ Display Phishing Links (If Found)
        if phishing_urls:
            st.write(f"🚨 **Phishing URLs Detected:** {', '.join(phishing_urls)}")
        
        # ✅ Show Message Category
        st.write(f"📂 **Category:** {category}")

        # ✅ Scam Alert Messages
        if scam_score >= 70:
            st.error("🚨 **High Scam Risk! This message is likely a scam.**")
        elif scam_score >= 40:
            st.warning("⚠️ **Moderate Scam Risk! Be cautious.**")
        else:
            st.success("✅ **Low Scam Risk. This message seems safe.**")

    else:
        st.warning("⚠️ Please enter a message for analysis.")
