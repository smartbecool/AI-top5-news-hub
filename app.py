import streamlit as st
import requests
import feedparser
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from datetime import datetime


# ------------ CONFIG ------------
st.set_page_config(
    page_title="ai-Top 5 News Hub",
    page_icon="📰",
    layout="wide",
)



st.title("📰 Ai-Top 5 News Hub")
st.caption("Configurable daily top news across your favorite categories.")

st.write(
    """
First working version ✅  

- Pick categories on the left  
- Set your **primary interest**  
- Click **Refresh** to load the top 5 news for each
"""
)

# ------------ STATE ------------
if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = None


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
            source_title = ""
            if hasattr(entry, "source") and isinstance(entry.source, dict):
                source_title = entry.source.get("title", "")

            # Clean HTML from summary
            raw_summary = entry.get("summary", "") or ""
            if raw_summary:
                summary_text = BeautifulSoup(raw_summary, "html.parser").get_text(" ", strip=True)
            else:
                summary_text = ""

            items.append(
                {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source_title,
                    "summary": summary_text,
                }
            )

        return items
    except Exception as e:
        st.error(f"Error while fetching news for '{query}': {e}")
        return []


# ------------ SIDEBAR ------------
st.sidebar.header("⚙️ Configuration")

primary_interest = st.sidebar.selectbox(
    "Your primary focus (used to prioritize categories):",
    options=["None"] + list(CATEGORY_QUERIES.keys()),
    index=1,  # default to Tech / AI
)

selected_categories = st.sidebar.multiselect(
    "Pick categories to display:",
    options=list(CATEGORY_QUERIES.keys()),
    default=["Tech / AI", "EPL", "India"],
    help="Only the categories you select will be shown on the page.",
)

refresh_clicked = st.sidebar.button("🔁 Refresh news")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Roadmap: user login, daily refresh, bubble UI based on interactions, sentiment summary, etc."
)

# ------------ PERSONALIZATION BANNER ------------
if primary_interest != "None":
    st.info(
        f"✨ Personalized for your interest in **{primary_interest}**. "
        "That category will be shown first if selected."
    )

# Always show primary interest category (even if user didn't select it)
if primary_interest != "None":
    # Ensure primary category is included at the top
    ordered_categories = [primary_interest] + [
        c for c in selected_categories if c != primary_interest
    ]
else:
    ordered_categories = selected_categories

# ------------ MAIN CONTENT ------------

if not ordered_categories:
    st.info("👈 Pick at least one category from the sidebar to get started.")
else:
    if refresh_clicked:
        st.session_state["last_refresh"] = datetime.now()
        st.success("News refreshed! Scroll down to view the latest top 5 in each category.")

    # Show last refresh info if available
    if st.session_state["last_refresh"] is not None:
        ts = st.session_state["last_refresh"].strftime("%Y-%m-%d %H:%M")
        st.caption(f"🕒 Last refreshed: {ts}")

    for cat in ordered_categories:
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
            source = article["source"]
            summary = article["summary"]

            st.markdown(f"**{idx}. [{title}]({link})**")
            meta = []
            if source:
                meta.append(source)
            if published:
                meta.append(published)
            if meta:
                st.caption(" | ".join(meta))

           

        st.markdown("---")
