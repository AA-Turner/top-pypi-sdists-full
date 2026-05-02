# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["Credential"]


class Credential(BaseModel):
    id: str

    created_at: datetime

    created_by_identity_type: str

    created_by_user_id: str

    credential_metadata: Dict[str, object]

    description: str

    name: str

    type: str

    updated_at: datetime

    object: Optional[str] = None
