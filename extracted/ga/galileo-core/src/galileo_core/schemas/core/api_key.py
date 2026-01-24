from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from galileo_core.schemas.core.collaboration_role import CollaboratorRole


class CreateApiKeyRequest(BaseModel):
    description: str
    expires_at: Optional[datetime] = None
    project_id: Optional[UUID4] = None
    project_role: Optional[CollaboratorRole] = None


class BaseApiKey(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    last_used: Optional[datetime] = None
    truncated: str


class ApiKeyResponse(BaseApiKey, CreateApiKeyRequest):
    truncated: str


class CreateApiKeyResponse(ApiKeyResponse):
    api_key: str
