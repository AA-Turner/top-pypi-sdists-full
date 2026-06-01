"""FastAPI dependency for the auth passthrough delegate.

This file is scaffolded once and never overwritten.
"""

from typing import Annotated

from fastapi import Depends

from ..delegates.auth_delegate import AuthDelegate
from . import Settings


def auth_delegate_factory(settings: Settings) -> AuthDelegate:
    """Create an ``AuthDelegate`` bound to the configured auth service URL."""
    return AuthDelegate(settings.auth_service_url)


AuthDelegateDep = Annotated[AuthDelegate, Depends(auth_delegate_factory)]

__all__ = ("AuthDelegateDep", "auth_delegate_factory")
