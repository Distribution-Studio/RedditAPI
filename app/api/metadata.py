from fastapi import APIRouter, HTTPException
from app.models.schemas import Metadata
from app.database.connection import get_supabase_client

router = APIRouter()


@router.get("/api/metadata/sync-time")
async def get_sync_time():
    """Get the last time data was synced from Reddit"""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("metadata").select("*").order("synced", desc=True).limit(1).execute()
        
        if response.data:
            latest_metadata = response.data[0]
            return {
                "job_name": latest_metadata["job_name"],
                "synced": latest_metadata["synced"]
            }
        
        return {"job_name": None, "synced": None}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/api/metadata", response_model=list[Metadata])
async def get_all_metadata():
    """Get all metadata entries"""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("metadata").select("*").order("synced", desc=True).execute()
        
        metadata_list = []
        for row in response.data:
            metadata = Metadata(
                id=row["id"],
                job_name=row["job_name"],
                synced=row["synced"]
            )
            metadata_list.append(metadata)
        
        return metadata_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") 