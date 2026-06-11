"""
Taktile Auth
"""

from importlib.metadata import version

__version__ = version(__name__.split(".", maxsplit=1)[0])

from taktile_auth.client import AuthClient  # noqa: 401
from taktile_auth.counter import (  # noqa: 401
    DynamoDBSharedCounter,
    SharedCounter,
)
from taktile_auth.exceptions import (  # noqa: 401
    InsufficientRightsException,
    InvalidAuthException,
    LoopDetectedException,
    TaktileAuthException,
)
from taktile_auth.recursion import (  # noqa: 401
    RECURSION_CACHE_REALM,
    RecursionDecision,
    RecursionGate,
    RecursionMode,
    recursion_counter_key,
)
from taktile_auth.schemas.session import (  # noqa: 401
    SessionState,
    parse_session_prefix,
)
from taktile_auth.schemas.token import TaktileIdToken  # noqa: 401

__all__ = [
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
