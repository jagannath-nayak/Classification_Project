import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import json  # ✅ Ensure proper JSON parsing

# ✅ Load API Key from .env file
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("❌ Google API Key not found. Please check your .env file.")

# ✅ Configure Google Gemini API
genai.configure(api_key=google_api_key)

# ✅ Function to generate AI-powered reply suggestions
def generate_smart_replies(message):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # ✅ Using Gemini 1.5 Flash (Fast & Cheap)
        
        # ✅ Force Gemini to return proper JSON using `json.dumps()`
        prompt = f"""
        You are an AI assistant. Generate 3 quick and professional reply suggestions based on the following message.
        - If it's a normal message, suggest natural responses.
        - If it's spam or scam, suggest a safe reply or a warning response.

        **Return the response as a valid JSON using Python's `json.dumps()` function.**  
        **DO NOT return extra text, only JSON output!**  

        Example JSON output:
        ```json
        {{
          "reply_1": "Sure, I can do that!",
          "reply_2": "Let me check and get back to you.",
          "reply_3": "Can we reschedule for tomorrow?"
        }}
        ```

        Message: "{message}"
        """

        response = model.generate_content(prompt)

        # ✅ Check if response is valid
        if not response or not response.text:
            return ["❌ Error: No response from AI. Try again."]

        # ✅ Extract JSON from AI response (Ignore markdown ```json formatting)
        json_start = response.text.find("{")
        json_end = response.text.rfind("}") + 1
        json_text = response.text[json_start:json_end]

        # ✅ Parse JSON response safely
        try:
            replies = json.loads(json_text)  # Load extracted JSON
            return [
                replies.get("reply_1", "No reply found"),
                replies.get("reply_2", "No reply found"),
                replies.get("reply_3", "No reply found"),
            ]
        except json.JSONDecodeError:
            return ["❌ Error: AI response was not in valid JSON format. Try again."]

    except Exception as e:
        return [f"❌ Error: {str(e)}"]

# ✅ Streamlit UI
st.title("💬 AI-Powered Smart Reply Suggestions")
message_input = st.text_area("📩 Enter the message or email content:")

if st.button("Generate Replies"):
    if message_input:
        st.subheader("🤖 AI-Suggested Replies:")
        replies = generate_smart_replies(message_input)
        for i, reply in enumerate(replies, 1):
            st.write(f"✅ **Option {i}:** {reply}")
    else:
        st.warning("⚠️ Please enter a message to generate replies.")
