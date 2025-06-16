from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/config", tags=["Configurations"])

class ConfigItem(BaseModel):
    key: str
    value: str

@router.post("/bulk")
async def bulk_add_or_update_config(
    items: List[ConfigItem],
    db_hub: DatabaseHub = Depends(get_db_hub),
):
    try:
        await db_hub.connect_sqlite()
        try:
            async with db_hub.sqlite_conn.execute("BEGIN"):
                for item in items:
                    encrypted_value = db_hub.fernet.encrypt(item.value.encode()).decode()
                    await db_hub.sqlite_conn.execute(
                        """
                        INSERT INTO config (key, value) VALUES (?, ?)
                        ON CONFLICT(key) DO UPDATE SET value = excluded.value
                        """,
                        (item.key, encrypted_value)
                    )
                await db_hub.sqlite_conn.commit()
        except Exception as e:
            await db_hub.sqlite_conn.execute("ROLLBACK")
            raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
        return {"message": f"{len(items)} config items saved or updated."}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.get("/")
async def get_config(db_hub: DatabaseHub = Depends(get_db_hub)):
    try:
        await db_hub.connect_sqlite()
        config = {}
        async with db_hub.sqlite_conn.execute("SELECT key, value FROM config") as cursor:
            async for key, encrypted_value in cursor:
                try:
                    decrypted_value = db_hub.fernet.decrypt(encrypted_value.encode()).decode()
                except Exception:
                    decrypted_value = None 
                config[key] = decrypted_value
        return config
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
