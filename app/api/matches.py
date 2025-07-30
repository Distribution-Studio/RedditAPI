import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.schemas import Match, User
from app.utils.auth import verify_token
from app.database.connection import get_supabase_client

router = APIRouter()


@router.get("/api/matches", response_model=List[Match])
async def get_matches(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(verify_token)
):
    """Get Reddit posts that match user's criteria"""
    supabase = get_supabase_client()
    
    try:
        # Get user's configuration
        config_response = supabase.table("user_configs").select("*").eq("id", current_user.id).execute()
        
        if not config_response.data:
            return []
        
        user_config = config_response.data[0]
        user_subreddits = user_config.get("subreddits", [])
        user_keywords = user_config.get("keywords", [])
        
        # If no criteria set, return empty list
        if not user_subreddits and not user_keywords:
            return []
        
        # Build query to find matches
        query = supabase.table("matches").select("*")
        
        # Apply filters
        if user_subreddits:
            query = query.in_("subreddit", user_subreddits)
        
        if user_keywords:
            # For keywords, we need to check if any of the user's keywords are in matched_keywords
            # This is a simplified approach - in production you might want more sophisticated matching
            for keyword in user_keywords:
                query = query.contains("matched_keywords", [keyword])
        
        # Add user to user_ids if not already there
        query = query.or_(f"user_ids.cs.{{{current_user.id}}}", "user_ids.is.null")
        
        # Order by timestamp and limit
        query = query.order("timestamp", desc=True).range(offset, offset + limit - 1)
        
        response = query.execute()
        
        matches = []
        for row in response.data:
            match = Match(
                id=row["id"],
                reddit_id=row["reddit_id"],
                type=row["type"],
                subreddit=row["subreddit"],
                title=row["title"],
                content=row.get("content"),
                url=row.get("url"),
                upvotes=row.get("upvotes"),
                num_comments=row.get("num_comments"),
                ratio=row.get("ratio"),
                intent_score=row.get("intent_score"),
                matched_keywords=row.get("matched_keywords", []),
                sentiment=row.get("sentiment"),
                user_ids=row.get("user_ids", []),
                timestamp=row["timestamp"]
            )
            matches.append(match)
        
        return matches
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/api/matches/{match_id}", response_model=Match)
async def get_match(
    match_id: str,
    current_user: User = Depends(verify_token)
):
    """Get a specific match by ID"""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("matches").select("*").eq("id", match_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Match not found")
        
        row = response.data[0]
        return Match(
            id=row["id"],
            reddit_id=row["reddit_id"],
            type=row["type"],
            subreddit=row["subreddit"],
            title=row["title"],
            content=row.get("content"),
            url=row.get("url"),
            upvotes=row.get("upvotes"),
            num_comments=row.get("num_comments"),
            ratio=row.get("ratio"),
            intent_score=row.get("intent_score"),
            matched_keywords=row.get("matched_keywords", []),
            sentiment=row.get("sentiment"),
            user_ids=row.get("user_ids", []),
            timestamp=row["timestamp"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 