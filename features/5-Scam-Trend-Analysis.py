import os
import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from collections import Counter
from wordcloud import WordCloud

# ✅ Load API Key from .env file
#load_dotenv()
#news_api_key = os.getenv("NEWS_API_KEY")
news_api_key = st.secrets["NEWS_API_KEY"]
if not news_api_key:
    st.error("❌ News API Key not found. Please check your .env file.")

# ✅ Function to Fetch Scam News from NewsAPI
def fetch_scam_news():
    try:
        API_URL = f"https://newsapi.org/v2/everything?q=scam OR fraud OR phishing OR cybercrime&language=en&apiKey={news_api_key}"
        response = requests.get(API_URL)

        if response.status_code != 200:
            return None, f"❌ API Error: {response.status_code}"

        news_data = response.json()
        return news_data["articles"], None

    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# ✅ Function to Extract Scam Keywords from News Headlines
def extract_trending_keywords(news_articles):
    scam_keywords = []
    for article in news_articles:
        title = article["title"].lower()
        scam_keywords.extend(title.split())

    # ✅ Count Keyword Frequency
    keyword_counts = Counter(scam_keywords)
    common_keywords = keyword_counts.most_common(10)
    return common_keywords

# ✅ Function to Generate Word Cloud
def generate_wordcloud(news_articles):
    text = " ".join(article["title"] for article in news_articles)
    wordcloud = WordCloud(width=800, height=400, background_color="black", colormap="Reds").generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("🔥 Trending Scam Keywords from News", fontsize=14)
    st.pyplot(plt)

# ✅ Streamlit UI
st.title("🔥 AI-Powered Scam Trend Analysis")

# ✅ Fetch News
news_articles, error = fetch_scam_news()

if error:
    st.error(error)
else:
    # ✅ Extract Trending Scam Keywords
    trending_keywords = extract_trending_keywords(news_articles)
    
    st.subheader("📊 Trending Scam Keywords")
    for keyword, count in trending_keywords:
        st.write(f"🔹 **{keyword.capitalize()}** - {count} mentions")

    # ✅ Show Scam News Articles
    st.subheader("📰 Latest Scam & Fraud News")
    for article in news_articles[:5]:
        st.markdown(f"🔹 [{article['title']}]({article['url']})")

    # ✅ Generate Scam Word Cloud
    generate_wordcloud(news_articles)
