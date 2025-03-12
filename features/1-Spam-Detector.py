import os
import pickle
import streamlit as st
import numpy as np

# ✅ Load trained model & vectorizer
MODEL_PATH = "models/model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

# Load model
with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

# Load vectorizer
with open(VECTORIZER_PATH, "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# ✅ Function to classify messages (Fix: Convert Sparse to Dense)
def classify_message(text):
    text_vectorized = vectorizer.transform([text])
    text_dense = text_vectorized.toarray()  # ✅ Convert sparse to dense

    prediction = model.predict(text_dense)[0]
    probability = model.predict_proba(text_dense)[0][1]  # Probability of spam

    return "🚨 Spam Detected!" if prediction == 1 else "✅ Not Spam", probability

# ✅ Streamlit UI
st.title("📩 AI-Powered SMS & Email Spam Detection (Custom Model)")
message_type = st.radio("Select Message Type:", ["SMS", "Email"])
message_input = st.text_area("Enter the message or email content:")

if st.button("Analyze"):
    if message_input:
        result, score = classify_message(message_input)
        st.subheader(result)
        st.write(f"🔍 **Spam Probability Score:** {score:.2f}")
    else:
        st.warning("⚠️ Please enter a message or email content.")
