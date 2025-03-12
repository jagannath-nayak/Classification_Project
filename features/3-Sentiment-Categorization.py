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

# ✅ Hugging Face Model for Auto-Categorization
CATEGORY_MODEL = "facebook/bart-large-mnli"

# ✅ Function to analyze sentiment using TextBlob (No API Needed!)
def analyze_sentiment_textblob(text):
    try:
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity  # Range: -1 (Negative) to +1 (Positive)

        if sentiment_score >= 0.05:
            return f"Positive 😊 ({sentiment_score:.2f})"
        elif sentiment_score <= -0.05:
            return f"Negative 😠 ({sentiment_score:.2f})"
        else:
            return f"Neutral 😐 ({sentiment_score:.2f})"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Function to categorize messages using Hugging Face API
def categorize_message(text):
    try:
        API_URL = f"https://api-inference.huggingface.co/models/{CATEGORY_MODEL}"
        headers = {"Authorization": f"Bearer {huggingface_api_key}"}

        labels = ["spam", "banking", "work", "personal", "promotional", "transaction"]
        response = requests.post(API_URL, headers=headers, json={"inputs": text, "parameters": {"candidate_labels": labels}})

        if response.status_code != 200:
            return "❌ API Error"

        result = response.json()
        categories = result.get("labels", [])
        scores = result.get("scores", [])

        if categories and scores:
            # ✅ Only classify as spam if the confidence score is above 0.6
            if categories[0] == "spam" and scores[0] < 0.6:
                return "Not Spam"
            return categories[0].capitalize()
        return "Unknown"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Streamlit UI
st.title("📩 AI-Powered Sentiment & Message Categorization")
message_input = st.text_area("📩 Enter the SMS or Email content:")

if st.button("Analyze"):
    if message_input:
        sentiment = analyze_sentiment_textblob(message_input)  # ✅ Uses TextBlob (No API Needed)
        category = categorize_message(message_input)  # ✅ Uses Hugging Face API
        
        st.subheader("🔍 Analysis Results:")
        st.write(f"📊 **Sentiment:** {sentiment}")
        st.write(f"📂 **Category:** {category}")
    else:
        st.warning("⚠️ Please enter a message for analysis.")
