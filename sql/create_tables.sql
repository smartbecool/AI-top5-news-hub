-- Users of the Top 5 News Hub
CREATE TABLE IF NOT EXISTS users (
    user_id         SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    display_name    VARCHAR(255),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Categories available in the system (mirrors YAML but stored in DB for future)
CREATE TABLE IF NOT EXISTS categories (
    category_id     SERIAL PRIMARY KEY,
    name            VARCHAR(255) UNIQUE NOT NULL,
    query           TEXT NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE
);

-- User-specific category preferences
CREATE TABLE IF NOT EXISTS user_category_preferences (
    user_id         INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id     INT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    is_selected     BOOLEAN DEFAULT TRUE,
    is_primary      BOOLEAN DEFAULT FALSE,
    display_order   INT DEFAULT 0,
    PRIMARY KEY (user_id, category_id)
);

-- Bookmarked articles per user
CREATE TABLE IF NOT EXISTS bookmarks (
    bookmark_id     SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category_id     INT REFERENCES categories(category_id),
    article_title   TEXT NOT NULL,
    article_url     TEXT NOT NULL,
    source          VARCHAR(255),
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Track refreshes (for daily limit / analytics)
CREATE TABLE IF NOT EXISTS refresh_logs (
    refresh_id      SERIAL PRIMARY KEY,
    user_id         INT REFERENCES users(user_id) ON DELETE SET NULL,
    refreshed_at    TIMESTAMP DEFAULT NOW(),
    categories_used TEXT
);
