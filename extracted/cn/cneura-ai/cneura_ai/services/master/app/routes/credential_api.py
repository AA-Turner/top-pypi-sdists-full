from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from app.dependencies import get_db_hub, DatabaseHub
from cneura_ai.credential import CredentialManager, CredentialNotFound

router = APIRouter(prefix="/credentials", tags=["Credentials"])


class CredentialInput(BaseModel):
    name: str
    description: Optional[str] = None
    value: str 

class BulkCredentialInput(BaseModel):
    credentials: List[CredentialInput]



class CredentialResponse(BaseModel):
    credential_id: str
    name: str
    description: Optional[str] = None



async def get_credential_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> CredentialManager:
    await db_hub.load_config()
    mongo_uri = db_hub.config.get("MONGO_URI")
    secret_key = db_hub.config.get("SECRET_KEY")
    db_name = db_hub.config.get("CREDENTIAL_DB", "credential_db")
    collection_name = db_hub.config.get("CREDENTIAL_COLLECTION", "credentials")

    if not mongo_uri or not secret_key:
        raise HTTPException(status_code=500, detail="Mongo URI or Secret Key not found in config")

    return CredentialManager(
        secret_key=secret_key,
        mongo_uri=mongo_uri,
        db_name=db_name,
        collection_name=collection_name
    )



@router.post("/register", response_model=CredentialResponse, status_code=status.HTTP_201_CREATED)
async def register_credential(payload: CredentialInput, manager: CredentialManager = Depends(get_credential_manager)):
    try:
        credential_id = str(uuid4())
        manager.register(credential_id, {
            "name": payload.name,
            "description": payload.description,
            "value": payload.value
        })
        return {
            "credential_id": credential_id,
            "name": payload.name,
            "description": payload.description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register/bulk", response_model=List[CredentialResponse], status_code=status.HTTP_201_CREATED)
async def bulk_register_credentials(payload: BulkCredentialInput, manager: CredentialManager = Depends(get_credential_manager)):
    try:
        results = []
        for item in payload.credentials:
            credential_id = str(uuid4())
            manager.register(credential_id, {
                "name": item.name,
                "description": item.description,
                "value": item.value
            })
            results.append({
                "credential_id": credential_id,
                "name": item.name,
                "description": item.description
            })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/credential/{credential_id}", response_model=dict)
async def get_credential(credential_id: str, manager: CredentialManager = Depends(get_credential_manager)):
    try:
        return manager.get_credentials(credential_id)
    except CredentialNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/credential/{credential_id}")
async def delete_credential(credential_id: str, manager: CredentialManager = Depends(get_credential_manager)):
    try:
        manager.delete(credential_id)
        return {"message": "Credential deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[str])
async def list_credential_ids(manager: CredentialManager = Depends(get_credential_manager)):
    try:
        return manager.list_credentials()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
