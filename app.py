import streamlit as st
import feedparser
from newspaper import Article
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

nltk.download('punkt')

# Summarization function
def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    result = ""
    for sentence in summary:
        result += "🔸 " + str(sentence) + "\n"
    return result

# Streamlit UI
st.set_page_config(page_title="News Summarizer", layout="centered")
st.title("📰 Real-Time News Summarizer")
st.markdown("Get latest news summaries using NLP!")

count = st.slider("Select number of news to summarize", min_value=1, max_value=5, value=3)

if st.button("🔁 Summarize Now"):
    with st.spinner("Fetching news and summarizing..."):
        rss_url = "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"
        feed = feedparser.parse(rss_url)

        for i in range(count):
            try:
                title = feed.entries[i].title
                link = feed.entries[i].link

                article = Article(link)
                article.download()
                article.parse()

                summary = summarize_text(article.text)

                st.subheader(f"🗞️ {title}")
                st.markdown(f"[🔗 Read Full Article]({link})")
                st.markdown(summary)
            except:
                st.warning(f"⚠️ Could not summarize: {feed.entries[i].title}")




