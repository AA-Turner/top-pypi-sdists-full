"""Token service dependency for the auth service.

This file is scaffolded once and never overwritten.
"""

from typing import Annotated

from fastapi import Depends

from ..services.token_service import TokenService
from . import Settings
from .db import KeyRing


def _token_service_factory(key_ring: KeyRing, settings: Settings) -> TokenService:
    """Create a ``TokenService`` with the key ring and settings."""
    return TokenService(key_ring, settings)


TokenSvc = Annotated[TokenService, Depends(_token_service_factory)]

__all__ = ("TokenSvc",)
