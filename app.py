import streamlit as st
import requests
import feedparser
from urllib.parse import quote_plus
from datetime import datetime

import pandas as pd
import plotly.express as px

# ------------ CONFIG ------------
st.set_page_config(
    page_title="Top 5 News Hub",
    page_icon="📰",
    layout="wide",
)

st.title("📰 Top 5 News Hub")
st.caption("Configurable daily top news across your favorite categories.")

st.write(
    """
First working version ✅  

- Use the **sidebar** to select categories  
- Set your **primary focus**  
- Bubbles give you a visual sense of which categories you view more  
- Click **Refresh** to load the top 5 news for each category
"""
)

# ------------ CATEGORY CONFIG ------------
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

ALL_CATEGORIES = list(CATEGORY_QUERIES.keys())

# ------------ STATE ------------
if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = None

if "category_engagement" not in st.session_state:
    # start with baseline engagement so bubbles are visible
    st.session_state["category_engagement"] = {c: 1 for c in ALL_CATEGORIES}

if "selected_categories" not in st.session_state:
    st.session_state["selected_categories"] = ["Tech / AI", "EPL", "India"]


# ------------ FUNCTIONS ------------

def fetch_google_news(query: str, max_items: int = 5):
    """Fetch top news items from Google News RSS for a given query."""
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

            items.append(
                {
                    "title": entry.get("title", "No title"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                    "source": source_title,
                }
            )
        return items
    except Exception as e:
        st.error(f"Error while fetching news for '{query}': {e}")
        return []


def show_bubble_chart(selected_categories, primary_interest: str):
    """
    Bubble chart that VISUALIZES categories.
    - All categories are shown as bubbles.
    - Size is based on engagement + whether it's selected + primary focus.
    """
    data = []
    for idx, cat in enumerate(ALL_CATEGORIES):
        engagement = st.session_state["category_engagement"].get(cat, 1)
        is_selected = cat in selected_categories
        is_primary = (cat == primary_interest)

        size = engagement
        if is_selected:
            size += 5
        if is_primary:
            size += 5

        data.append(
            {
                "Category": cat,
                "Size": size,
                "Engagement": engagement,
                "Selected": "Selected" if is_selected else "Not selected",
                "Primary": "Primary" if is_primary else "Regular",
                "x": idx,   # spread horizontally
                "y": 0,
            }
        )

    df = pd.DataFrame(data)

    fig = px.scatter(
        df,
        x="x",
        y="y",
        size="Size",
        color="Category",
        hover_name="Category",
        hover_data=["Engagement", "Selected", "Primary"],
        size_max=120,
    )

    fig.update_traces(
        mode="markers",
        marker=dict(
            opacity=0.9,
            line=dict(width=2, color="white"),
        ),
    )

    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(t=20, b=10, l=10, r=10),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    st.plotly_chart(fig, use_container_width=True)


# ------------ SIDEBAR ------------
st.sidebar.header("⚙️ Configuration")

primary_interest = st.sidebar.selectbox(
    "Your primary focus:",
    options=["None"] + ALL_CATEGORIES,
    index=1,  # default to Tech / AI
)

selected_categories = st.sidebar.multiselect(
    "Categories to show:",
    options=ALL_CATEGORIES,
    default=st.session_state["selected_categories"],
    help="These categories will be shown below and highlighted in the bubbles.",
)

# keep selection in state
st.session_state["selected_categories"] = selected_categories

refresh_clicked = st.sidebar.button("🔁 Refresh news")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Roadmap: bubble-based selection, user login, daily auto-refresh, sentiment summary, etc."
)

# ------------ MAIN CONTENT ------------

if refresh_clicked:
    st.session_state["last_refresh"] = datetime.now()
    st.success("News refreshed! Scroll down to view the latest top 5 in each category.")

# Last refresh info
if st.session_state["last_refresh"] is not None:
    ts = st.session_state["last_refresh"].strftime("%Y-%m-%d %H:%M")
    st.caption(f"🕒 Last refreshed: {ts}")

# Bubble chart
st.subheader("Category bubble view")
st.caption(
    "Bubble size ≈ how often you viewed that category, plus extra weight for those you selected "
    "and your primary focus."
)
show_bubble_chart(selected_categories, primary_interest)
st.markdown("---")

# Determine which categories to show news for (ensure primary first)
ordered_categories = selected_categories.copy()

# Always include primary interest even if not selected
if primary_interest != "None":
    if primary_interest in ordered_categories:
        ordered_categories = [primary_interest] + [
            c for c in ordered_categories if c != primary_interest
        ]
    else:
        ordered_categories = [primary_interest] + ordered_categories

if not ordered_categories:
    st.info("Select at least one category from the sidebar.")
else:
    for cat in ordered_categories:
        # update engagement counter whenever we show this category
        st.session_state["category_engagement"][cat] = (
            st.session_state["category_engagement"].get(cat, 0) + 1
        )

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

            st.markdown(f"**{idx}. [{title}]({link})**")
            meta = []
            if source:
                meta.append(source)
            if published:
                meta.append(published)
            if meta:
                st.caption(" | ".join(meta))

        st.markdown("---")
