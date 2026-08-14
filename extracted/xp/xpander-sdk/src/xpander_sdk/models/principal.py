"""Typed caller principal. MIRROR of xpander_dev_utils/models/principal.py (the SDK cannot
import dev_utils) - keep the kinds, fields and validator identical in both repos."""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class PrincipalKind(str, Enum):
    """The door a caller came through: person, chat platform, api key, machine, or guest."""

    user = "user"
    slack = "slack"
    api_key = "api_key"
    system = "system"
    anonymous = "anonymous"


class Principal(BaseModel):
    """Typed caller identity: who invoked the run and through which door."""

    kind: PrincipalKind
    id: str
    email: Optional[str] = None
    display_name: Optional[str] = None

    @field_validator("id")
    @classmethod
    def _vault_safe_id(cls, v: str) -> str:
        """Reject ids unusable as a vault-key segment (':' is the delimiter; whitespace never canonical)."""
        v = (v or "").strip()
        if not v:
            raise ValueError("principal id cannot be empty")
        if ":" in v or any(ch.isspace() for ch in v):
            raise ValueError("principal id cannot contain ':' or whitespace")
        return v
