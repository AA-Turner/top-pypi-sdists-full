"""
Taktile Auth
"""

from importlib.metadata import version

__version__ = version(__name__.split(".", maxsplit=1)[0])

from taktile_auth.client import AuthClient  # noqa: 401
from taktile_auth.exceptions import (  # noqa: 401
    InsufficientRightsException,
    InvalidAuthException,
    TaktileAuthException,
)
from taktile_auth.schemas.session import SessionState  # noqa: 401
from taktile_auth.schemas.token import TaktileIdToken  # noqa: 401

__all__ = [
    "AuthClient",
    "InsufficientRightsException",
    "InvalidAuthException",
    "SessionState",
    "TaktileAuthException",
    "TaktileIdToken",
]
