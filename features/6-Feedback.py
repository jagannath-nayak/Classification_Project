import streamlit as st
import pandas as pd
import os

# ✅ CSV File Path
FEEDBACK_FILE = "feedback_data.csv"

# ✅ Function to Save Feedback to CSV
def save_feedback(data):
    # Convert single dictionary data into a DataFrame
    new_data = pd.DataFrame([data])

    # Check if the CSV file exists
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)

        # ✅ Use `pd.concat()` Instead of `df.append()`
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data  # If no file exists, start with new data

    df.to_csv(FEEDBACK_FILE, index=False)

# ✅ Streamlit UI
st.header("📝 Feedback", divider='rainbow')

with st.form("feedback_form"):
    name = st.text_input("Full Name*", placeholder="John Doe")
    email = st.text_input("Email*", placeholder="johndoe@gmail.com")
    rating = st.slider("Rating*", min_value=1, max_value=5, value=3)
    easy_to_use = st.selectbox("Easy to Use*", options=["Yes", "No", "Somewhat"], help="Select if the application is easy to use")
    challenges = st.text_area("Challenges Faced*", help="Enter the challenges you faced", placeholder="Describe any challenges")
    general_feedback = st.text_area("Any other feedback", help="Enter any other feedback")

    st.markdown("**Required*")
    submit = st.form_submit_button("Submit")

if submit:
    if not name or not email or not challenges:
        st.error("Please fill all the required fields.")
    else:
        feedback_data = {
            "Name": name,
            "Email": email,
            "Rating": rating,
            "Easy to Use": easy_to_use,
            "Challenges": challenges,
            "General Feedback": general_feedback
        }

        save_feedback(feedback_data)  # ✅ Save to CSV
        st.success("✅ Thank you for your feedback! Your response has been saved.")
