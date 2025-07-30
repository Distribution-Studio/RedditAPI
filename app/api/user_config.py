from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserConfig, UserConfigUpdate, User
from app.utils.auth import verify_token
from app.database.connection import get_supabase_client

router = APIRouter()


@router.get("/api/user/config", response_model=UserConfig)
async def get_user_config(current_user: User = Depends(verify_token)):
    supabase = get_supabase_client()
    
    try:
        # Get user config from Supabase
        response = supabase.table("user_configs").select("*").eq("id", current_user.id).execute()
        
        if not response.data:
            # Create default config if not exists
            default_config = {
                "id": current_user.id,
                "subreddits": [],
                "keywords": []
            }
            supabase.table("user_configs").insert(default_config).execute()
            return UserConfig(**default_config)
        
        config_data = response.data[0]
        return UserConfig(
            id=config_data["id"],
            subreddits=config_data["subreddits"] or [],
            keywords=config_data["keywords"] or []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/api/user/config", response_model=UserConfig)
async def update_user_config(
    config_update: UserConfigUpdate,
    current_user: User = Depends(verify_token)
):
    supabase = get_supabase_client()
    
    try:
        # Get current config
        response = supabase.table("user_configs").select("*").eq("id", current_user.id).execute()
        
        if not response.data:
            # Create new config
            new_config = {
                "id": current_user.id,
                "subreddits": config_update.subreddits or [],
                "keywords": config_update.keywords or []
            }
            supabase.table("user_configs").insert(new_config).execute()
            return UserConfig(**new_config)
        
        # Update existing config
        current_config = response.data[0]
        update_data = {}
        
        if config_update.subreddits is not None:
            update_data["subreddits"] = config_update.subreddits
        if config_update.keywords is not None:
            update_data["keywords"] = config_update.keywords
        
        supabase.table("user_configs").update(update_data).eq("id", current_user.id).execute()
        
        # Get updated config
        updated_response = supabase.table("user_configs").select("*").eq("id", current_user.id).execute()
        updated_config = updated_response.data[0]
        
        return UserConfig(
            id=updated_config["id"],
            subreddits=updated_config["subreddits"] or [],
            keywords=updated_config["keywords"] or []
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 