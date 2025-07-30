-- Reddit Listener API Database Setup
-- Run this in your Supabase SQL editor

-- User configurations table
CREATE TABLE IF NOT EXISTS user_configs (
    id uuid primary key,
    subreddits text[] not null,
    keywords text[] not null
);

-- Matches table for Reddit posts
CREATE TABLE IF NOT EXISTS matches (
    id text primary key,
    reddit_id text not null,
    type text not null,
    subreddit text not null,
    title text not null,
    content text,
    url text,
    upvotes integer,
    num_comments integer,
    ratio float,
    intent_score float,
    matched_keywords text[],
    sentiment text,
    user_ids uuid[],
    timestamp timestamptz not null
);

-- Metadata table for sync tracking
CREATE TABLE IF NOT EXISTS metadata (
    id integer primary key,
    job_name text not null,
    synced timestamptz not null
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_matches_timestamp ON matches(timestamp);
CREATE INDEX IF NOT EXISTS idx_matches_reddit_id ON matches(reddit_id);

-- Optional: Add some sample data for testing
INSERT INTO metadata (id, job_name, synced) VALUES 
(1, 'reddit_sync', NOW())
ON CONFLICT (id) DO NOTHING;

-- Optional: Add a sample user config (replace with actual UUID)
-- INSERT INTO user_configs (id, subreddits, keywords) VALUES 
-- ('550e8400-e29b-41d4-a716-446655440000', ARRAY['programming', 'python'], ARRAY['fastapi', 'supabase'])
-- ON CONFLICT (id) DO NOTHING; 