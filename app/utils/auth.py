import jwt
import httpx
import logging
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import JWT_SECRET, JWT_ALGORITHM, BETTER_AUTH_URL
from app.models.schemas import User

logger = logging.getLogger(__name__)

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials) -> User:
    try:
        token = credentials.credentials
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            email = payload.get("email")
            name = payload.get("name")
            
            if not user_id or not email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            return User(id=user_id, email=email, name=name)
            
        except jwt.InvalidTokenError:   
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{BETTER_AUTH_URL}/verify-token",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    if response.status_code != 200:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid or expired token"
                        )
                    
                    user_data = response.json()
                    return User(
                        id=user_data["id"],
                        email=user_data["email"],
                        name=user_data.get("name")
                    )
                    
            except Exception as e:
                logger.error(f"External auth verification failed: {e}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        ) 