# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Credential"]


class Credential(BaseModel):
    id: str

    created_at: datetime

    created_by_identity_type: Optional[str] = None

    created_by_user_id: Optional[str] = None

    credential_metadata: Optional[Dict[str, object]] = None

    description: Optional[str] = None

    name: str

    type: str

    updated_at: datetime

    object: Optional[str] = None
