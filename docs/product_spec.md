# Top 5 News Hub – Product Spec

## 1. Product Summary

Top 5 News Hub is a configurable, personalized news dashboard that shows the top 5 news items per category (Tech, AI, Sports, EPL, India, USA, etc.), with a visual bubble-based interface that reflects user engagement and priorities.

It is designed as a daily “decision-saving” layer: instead of scanning multiple sites or feeds, users get a curated, interest-aware snapshot on a single screen.

---

## 2. Target Users

### Primary Users
- **Knowledge workers in tech / AI**  
  - Want to stay up-to-date on AI, tools, funding, and ecosystem news.
  - Have limited time and high context switching.
- **Multi-domain news consumers**  
  - Follow multiple topics (Tech + Sports + Regional news).
  - Don’t want to maintain separate apps or tabs for each category.

### Secondary Users
- **Students / early-career professionals**  
  - Want a simple way to track news in their domain of interest.
- **PM / data / AI interview candidates**  
  - Can use this as a talking point or demo in interviews.

---

## 3. Problem Statement

Today, users face:

1. **Fragmented news experience**  
   - Tech on one site, AI announcements elsewhere, sports on another app.
2. **No concept of “my work-first news”**  
   - Most feeds treat all topics equally, even if Tech / AI is critical to the user’s job.
3. **Time waste in scanning**  
   - Scrolling through noise to pick out the few important updates.
4. **Lack of visual prioritization**  
   - No clear signal of which categories the user actually consumes more.

**Top 5 News Hub** aims to fix this by:
- surfacing only the “top 5” per category,
- prioritizing categories based on the user’s primary focus,
- visualizing category engagement via bubbles.

---

## 4. Goals & Non-Goals

### Goals
- Provide a **one-screen view** of top news across selected categories.
- Allow users to **prioritize one primary domain** (e.g., Tech / AI).
- Make the experience **visual and intuitive** via bubble-based categories.
- Enable **daily usage** with clear refresh feedback.

### Non-Goals (for current version)
- Full article reading inside the app.
- Opinionated ranking beyond basic RSS search.
- Real-time, high-frequency updates (MVP does daily-style usage).

---

## 5. User Journeys

### Journey A – Tech professional starting the day
1. Opens Top 5 News Hub in the morning.
2. Primary focus pre-set to **Tech / AI**.
3. Bubbles show AI, EPL, India, etc. – Tech / AI bubble is visually prominent.
4. User clicks **Refresh** once.
5. User scrolls: Tech / AI → EPL → India.
6. In <5 minutes, user has context on key updates before work.

### Journey B – Mixed-interest user (sports + regional)
1. Sets primary focus to **EPL** or **General Sports**.
2. Selects India, USA, World as secondary categories.
3. Bubble view shows sports-heavy behavior over time.
4. Top 5 news per category gives a quick global + sports overview.

---

## 6. Functional Requirements (MVP)

### 6.1 Categories & Primary Focus
- Users can:
  - Select one **primary focus** category.
  - Select multiple categories to display.
- System must:
  - Always show primary focus category if set.
  - Place primary focus category at the top of the news list.

### 6.2 News Fetching
- Source: Google News RSS (per category query).
- For each category:
  - Fetch top N (default 5) articles.
  - Show:
    - title,
    - source (if available),
    - published time.
  - Provide clickable link to original article.

### 6.3 Bubble View
- All categories are represented as bubbles.
- Bubble size is influenced by:
  - baseline engagement,
  - whether category is selected,
  - whether category is primary focus.
- Bubbles display the **category name inside**.

### 6.4 Refresh Logic
- User can click **Refresh** to pull latest news.
- System shows:
  - “News refreshed” success state.
  - “Last refreshed” timestamp.

---

## 7. Future Enhancements (Phase 2+)

### 7.1 Personalization & Accounts
- Login / signup (email or OAuth).
- Store:
  - favorite categories,
  - primary focus,
  - refresh history,
  - bookmarks.

### 7.2 AI Summaries & Sentiment
- Auto-summarize each article via LLM.
- Provide:
  - “Key takeaways” per category.
  - “Community reaction summary” (pull from X/Twitter, Reddit, etc.)
- Per-topic sentiment trends (e.g., AI tools perceived positive vs negative).

### 7.3 Advanced Bubble Behavior
- True circle packing layout.
- Click-to-select / deselect directly on bubbles.
- Drag-and-drop to reprioritize categories.

### 7.4 Distribution Channels
- Telegram / WhatsApp bot version.
- Email digest mode (“send me today’s Top 5 at 8am”).
- Lightweight mobile wrapper.

---

## 8. Success Metrics

### Product Metrics
- **DAU / WAU**: number of returning users using it as a daily habit.
- **Session time**: 1–5 minutes per session (short, focused consumption).
- **Category diversity**: number of categories used per user.

### Engagement Metrics
- % users who set a **primary focus**.
- % sessions that use **Refresh**.
- Most engaged category overall (bubble engagement counts).

### Future Metrics (post-login)
- Number of bookmarks per user.
- Number of personalized refresh digests sent.

---

## 9. Risks & Assumptions

### Risks
- Google News RSS may have rate limits or change behavior.
- Some categories may not always have strong coverage.
- Too many categories could make the bubble view noisy.

### Assumptions
- Users are comfortable with a curated “Top 5” instead of infinite scroll.
- Users know at least one domain they want to prioritize (e.g., Tech / AI).
- A simple, visual dashboard is enough for their daily news needs.

---

## 10. Open Questions / Future Decisions

- Should we allow user-defined categories and custom queries?
- What’s the best identity provider for login (email vs Google vs GitHub)?
- Do we integrate directly with Twitter/X API for reaction summaries or use web scraping + LLM inference?

---

*This spec is intentionally written to be shared in product interviews to demonstrate product thinking, prioritization, and roadmap design.*
