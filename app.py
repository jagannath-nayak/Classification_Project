import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem import WordNetLemmatizer

# Load the saved model and vectorizer
model = pickle.load(open('model.pkl', 'rb'))
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [word for word in text if word.isalnum()]
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]
    text = [lemmatizer.lemmatize(word) for word in text]
    return " ".join(text)

# Streamlit App UI
st.title("📩 SMS/Email Spam Classifier")

input_sms = st.text_area("Enter the message:")

if st.button("Predict"):
    # 1. Preprocess the input
    transformed_sms = transform_text(input_sms)
    # 2. Vectorize the input
    vector_input = tfidf.transform([transformed_sms]).toarray()
    # 3. Predict using the model
    result = model.predict(vector_input)[0]
    # 4. Display the result
    if result == 1:
        st.error("🚨 This message is Spam!")
    else:
        st.success("✅ This message is Not Spam.")
