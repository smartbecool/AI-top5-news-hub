import streamlit as st
import requests
import feedparser
from urllib.parse import quote_plus

# ------------ CONFIG ------------
st.set_page_config(
    page_title="AI-Top 5 News Hub",
    page_icon="📰",
    layout="wide",
)

st.title("📰 AI-Top 5 News Hub")
st.caption("Configurable daily top news across your favorite categories.")

st.write(
    """
This is a first working version of your app.  
Pick categories on the left, click **Refresh**, and see the top 5 headlines for each.
"""
)

# Predefined categories and their search queries for Google News
CATEGORY_QUERIES = {
    "Tech / AI": "artificial intelligence OR AI OR machine learning OR LLM OR GenAI",
    "Startups": "startup funding OR tech startup",
    "India": "India news",
    "USA": "United States news",
    "World": "world news",
    "EPL": "English Premier League football",
    "Champions League": "UEFA Champions League",
    "NFL": "NFL American football",
    "General Sports": "sports news",
    "Stocks": "latest stocks news"
}


def fetch_google_news(query: str, max_items: int = 5):
    """
    Fetch top news items from Google News RSS for a given query.
    """
    try:
        search = quote_plus(query)
        url = (
            f"https://news.google.com/rss/search?q={search}&hl=en-US&gl=US&ceid=US:en"
        )
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        feed = feedparser.parse(resp.text)

        items = []
        for entry in feed.entries[:max_items]:
            items.append(
                {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": getattr(entry, "source", {}).get("title", ""),
                }
            )
        return items
    except Exception as e:
        st.error(f"Error while fetching news for '{query}': {e}")
        return []


# ------------ SIDEBAR ------------
st.sidebar.header("⚙️ Configuration")

selected_categories = st.sidebar.multiselect(
    "Pick categories to display:",
    options=list(CATEGORY_QUERIES.keys()),
    default=["Tech / AI", "EPL", "India"],
    help="Only the categories you select will be shown on the page.",
)

refresh_clicked = st.sidebar.button("🔁 Refresh news")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Future roadmap: user login, personalization, bubble UI, sentiment summary, etc."
)

# ------------ MAIN CONTENT ------------

if not selected_categories:
    st.info("👈 Pick at least one category from the sidebar to get started.")
else:
    if refresh_clicked:
        st.success("News refreshed! Scroll down to view the latest top 5 in each category.")

    for cat in selected_categories:
        st.markdown(f"## 📂 {cat}")

        query = CATEGORY_QUERIES[cat]
        with st.spinner(f"Fetching top 5 news for **{cat}**..."):
            articles = fetch_google_news(query, max_items=5)

        if not articles:
            st.warning("No news found for this category right now.")
            continue

        for idx, article in enumerate(articles, start=1):
            title = article["title"]
            link = article["link"]
            published = article["published"]

            st.markdown(f"**{idx}. [{title}]({link})**")
            if published:
                st.caption(published)

        st.markdown("---")
