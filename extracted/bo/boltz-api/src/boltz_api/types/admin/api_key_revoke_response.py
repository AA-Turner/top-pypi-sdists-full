# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["APIKeyRevokeResponse"]


class APIKeyRevokeResponse(BaseModel):
    id: str
    """API key ID"""

    allowed_ips: List[str]
    """IP addresses allowed to use this key. An empty array means all IPs are allowed."""

    created_at: datetime

    expires_at: Optional[datetime] = None
    """When the key expires. Null if the key does not expire."""

    is_active: bool

    key_prefix: str
    """First 12 characters of the key"""

    key_type: Literal["admin", "workspace"]

    last_used_at: Optional[datetime] = None

    livemode: bool
    """Whether this is a live API key (false for test keys)."""

    name: str
    """API key name"""

    workspace_id: Optional[str] = None
    """Workspace ID if workspace-scoped"""
