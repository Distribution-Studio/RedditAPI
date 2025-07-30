import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import API_HOST, API_PORT
from app.database.connection import (
    create_supabase_client, 
    close_supabase_client, 
    create_tables
)
from app.api import health, user_config, matches, metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Reddit Listener API...")
    create_supabase_client()
    create_tables()
    logger.info("Application started successfully")
    
    yield
    
    logger.info("Shutting down Reddit Listener API...")
    close_supabase_client()
    logger.info("Application shutdown complete")


app = FastAPI(
    title="Reddit Listener API",
    description="Backend API for Reddit content monitoring and alerting",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(user_config.router)
app.include_router(matches.router)
app.include_router(metadata.router)


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(30)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT) 