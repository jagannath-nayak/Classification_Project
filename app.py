import streamlit as st
st.set_page_config(page_title="SpamDefender.AI", page_icon="🤖🛡️", layout="wide", initial_sidebar_state="expanded")

from features.auth import authentication
from features.functions import load_lottie_file
import streamlit_lottie as st_lottie

# Initialize session state variables
if 'register' not in st.session_state:
    st.session_state['register'] = False
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

def intro():
    st.header("SpamDefender.AI :  Smart spam detection for SMS & emails 🤖🛡️", divider='rainbow')
    
    with st.container(border=True):
        left_col, right_col = st.columns(2)
        with left_col:
                st.subheader("About SpamDefender.AI", divider='rainbow')
                intro = '''
                📩 SpamDefender AI is an AI-powered spam detection system designed to protect your inbox from unwanted and malicious messages. 
                Whether it's SMS or email, our intelligent classifier accurately detects spam, phishing attempts, and 
                scam messages to keep your communication safe.
                '''
                st.markdown(intro)

        with right_col:
                robot_assist = load_lottie_file("animations/banner.json")
                st_lottie.st_lottie(robot_assist, loop=True, width=500, height=500)
                
    with st.container(border=True):
            left_col, right_col = st.columns(2)
            with right_col:
                st.subheader("Features of SpamDefender.AI ℹ️", divider='rainbow')
                features = [
                    "**Spam_Detector** Uses Machine Learning models to classify messages as spam or not spam.",
                    "**Smart_Reply:** Smart Reply feature suggests intelligent responses to incoming messages.",
                    "**Sentiment_categorization:** AI-powered sentiment analysis and message categorization.",
                    "**Scam_Insights:** Detects and provides insights on potential scam messages.",
                    "**Scam_Trend_Analysis:** Analyzes the trend of scam messages over time.",
                    "**Feedback:** Feedback feature allows users to share their experience and suggestions for improvement."
                ]
                for feature in features:
                    st.markdown(f"🔹 {feature}")
                st.write("*Explore the features from the sidebar navigation.*")

            with left_col:
                feature_animation = load_lottie_file("animations/loading.json")
                st_lottie.st_lottie(feature_animation, loop=True, width=500, height=400)

    with st.container(border=True):
            st.subheader("Why SpamDefender.AI? 🚀", divider='rainbow')
            left_col, right_col = st.columns(2)
            with left_col:
                benefits = [
                    "AI-Powered Accuracy - Uses advanced machine learning models to accurately detect spam, scams, and phishing emails.",
                    "Dual Protection (SMS & Email) - Unlike most spam filters that focus only on emails, SpamDefender AI protects both text messages and emails.",
                    "Feedback Loop - Allows users to provide feedback on the accuracy of the spam detection system.",
                    "AI-Powered Smart Replies - Suggests intelligent responses to incoming messages, making communication faster and safer.",
                    "Secure & Private - Your messages are analyzed securely, and no data is stored or shared externally."
                ]
                for benefit in benefits:
                    st.markdown(f"🔹 {benefit}")

            with right_col:
                benefits_animation = load_lottie_file("animations/success.json")
                st_lottie.st_lottie(benefits_animation, loop=True, width=500, height=300)

    with st.container(border=True):
            st.subheader("FAQs❓", divider='rainbow')
            # FAQ 1
            with st.expander("What is SpamDefender.AI?"):
                st.write("SpamDefender AI is an AI-powered spam detection system that helps identify and filter out spam, phishing, and scam messages from both SMS and emails.")
            # FAQ 2
            with st.expander("How does SpamDefender.AI detect spam?"):
                st.write("Our system uses machine learning models, NLP (Natural Language Processing), and Google AI to analyze the content, subject lines, sender details, and links in messages to classify them as spam or not spam.")
            #FAQ 3
            with st.expander("How does the AI-powered Smart Reply feature work?"):
                st.write("When a message is flagged as spam, SpamDefender AI suggests intelligent responses such as Block Sender, Report as Scam, or Ignore to help you take action quickly.")
            # FAQ 4
            with st.expander("Is my data safe with SpamDefender AI?"):
                st.write("Yes! We do not store or share your messages. SpamDefender AI analyzes text in real-time and ensures complete privacy.")

# Run authentication system
authentication()

if st.session_state["authentication_status"]:
    pg = st.navigation([
    st.Page(intro, title="Home", icon="🏠"),
    st.Page("features/spam_detector.py", title="Spam Detector", icon="🛡️"),
    st.Page("features/smart_reply.py", title="Smart Reply", icon="📧"),
    st.Page("features/sentiment_categorization.py" , title = "Sentiment_Categorization", icon = "💡"),
    st.Page("features/scam_insights.py", title="Scam Insights", icon="🔍"),
    st.Page("features/scam_trend_analysis.py", title="Scam Trend Analysis", icon="📈"),
    st.Page("features/feedback.py", title="Feedback", icon="💬")
      ])
    pg.run()
