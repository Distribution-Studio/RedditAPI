import logging
from typing import Optional
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    global supabase_client
    if supabase_client is None:
        raise RuntimeError("Supabase client not initialized")
    return supabase_client


def create_supabase_client():
    global supabase_client
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client created successfully")
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {e}")
        raise


def close_supabase_client():
    global supabase_client
    if supabase_client:
        # Supabase client doesn't need explicit closing
        supabase_client = None
        logger.info("Supabase client closed")


def create_tables():
    """Create tables in Supabase - this should be done via Supabase dashboard or migrations"""
    logger.info("Tables should be created via Supabase dashboard or migrations")
    logger.info("""
    Required tables:
    1. user_configs (id uuid primary key, subreddits text[], keywords text[])
    2. matches (id text primary key, reddit_id text, type text, subreddit text, 
       title text, content text, url text, upvotes integer, num_comments integer, 
       ratio float, intent_score float, matched_keywords text[], sentiment text, 
       user_ids uuid[], timestamp timestamptz)
    3. metadata (id integer primary key, job_name text, synced timestamptz)
    
    Required indexes:
    1. idx_matches_timestamp on matches(timestamp)
    2. idx_matches_reddit_id on matches(reddit_id)
    """) 