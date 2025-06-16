from fastapi import Depends, HTTPException
from app.database_hub import DatabaseHub
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.utils import SECRET_KEY, ALGORITHM

db_hub = DatabaseHub(sqlite_path="app/db/data.db", secret_key=SECRET_KEY)

async def get_db_hub():
    yield db_hub

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        await db_hub.connect_sqlite()
        async with db_hub.sqlite_conn.execute("SELECT email FROM users WHERE email = ?", (email,)) as cursor:
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            return {"email": user[0]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")