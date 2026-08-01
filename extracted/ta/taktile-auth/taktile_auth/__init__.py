"""
Taktile Auth
"""

from importlib.metadata import version

__version__ = version(__name__.split(".", maxsplit=1)[0])

from taktile_auth.client import AuthClient
from taktile_auth.constants import NULL_RESOURCE_ARG
from taktile_auth.counter import (
    DynamoDBSharedCounter,
    SharedCounter,
)
from taktile_auth.exceptions import (
    InsufficientRightsException,
    InvalidAuthException,
    LoopDetectedException,
    TaktileAuthException,
)
from taktile_auth.recursion import (
    RECURSION_CACHE_REALM,
    RecursionDecision,
    RecursionGate,
    RecursionMode,
    recursion_counter_key,
)
from taktile_auth.schemas.session import (
    SessionState,
    parse_session_prefix,
)
from taktile_auth.schemas.token import TaktileIdToken

__all__ = [
    "NULL_RESOURCE_ARG",
    "RECURSION_CACHE_REALM",
    "AuthClient",
    "DynamoDBSharedCounter",
    "InsufficientRightsException",
    "InvalidAuthException",
    "LoopDetectedException",
    "RecursionDecision",
    "RecursionGate",
    "RecursionMode",
    "SessionState",
    "SharedCounter",
    "TaktileAuthException",
    "TaktileIdToken",
    "parse_session_prefix",
    "recursion_counter_key",
]
