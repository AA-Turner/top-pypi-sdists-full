# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ConnectionGetByTagResponse", "LastSyncRun"]


class LastSyncRun(BaseModel):
    status: str

    completed_at: Optional[str] = FieldInfo(alias="completedAt", default=None)

    error: Optional[str] = None

    started_at: Optional[str] = FieldInfo(alias="startedAt", default=None)


class ConnectionGetByTagResponse(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    provider: str

    container_tags: Optional[List[str]] = FieldInfo(alias="containerTags", default=None)

    document_limit: Optional[float] = FieldInfo(alias="documentLimit", default=None)

    email: Optional[str] = None

    expires_at: Optional[str] = FieldInfo(alias="expiresAt", default=None)

    last_sync_run: Optional[LastSyncRun] = FieldInfo(alias="lastSyncRun", default=None)

    metadata: Optional[Dict[str, object]] = None
