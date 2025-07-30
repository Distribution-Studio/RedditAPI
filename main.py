import uvicorn
from app.main import app
from app.config import API_HOST, API_PORT

if __name__ == "__main__":
    print(f"Server will run on http://{API_HOST}:{API_PORT}")
    
    uvicorn.run(
        app, 
        host=API_HOST, 
        port=API_PORT,
        log_level="info"
    ) 