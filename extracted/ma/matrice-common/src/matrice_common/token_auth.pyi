"""Auto-generated stub for module: token_auth."""
from typing import Any

from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log
from .utils import process_error_log

# Constants
logger: Any

# Classes
class AuthToken:
    # Implements a custom authentication scheme.

    def __init__(self: Any, access_key: Any, secret_key: Any, refresh_token: Any) -> None: ...

    def is_expired(self: Any, buffer_seconds: int = 300) -> bool:
        """
        Check if token is expired or will expire within buffer_seconds.
        
                Args:
                    buffer_seconds: Number of seconds before actual expiry to consider token expired.
                                  Default is 300 (5 minutes) to allow proactive refresh.
        
                Returns:
                    True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        ...

    def reset_and_refresh(self: Any) -> Any:
        """
        Reset token state and attempt to refresh.
        
                This method is used for in-place token updates to avoid
                creating new token objects that would leave concurrent threads
                with stale references.
        """
        ...

    def set_bearer_token(self: Any) -> None:
        """
        Obtain an authentication bearer token using the provided refresh token.
        
                Thread-safe: Uses a lock to prevent concurrent refresh attempts.
                On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        ...

class RefreshToken:
    # Implements a custom authentication scheme.

    def __init__(self: Any, access_key: str, secret_key: str) -> None: ...

    def is_expired(self: Any, buffer_seconds: int = 300) -> bool:
        """
        Check if token is expired or will expire within buffer_seconds.
        
                Args:
                    buffer_seconds: Number of seconds before actual expiry to consider token expired.
                                  Default is 300 (5 minutes) to allow proactive refresh.
        
                Returns:
                    True if token is None, has no expiry, or will expire within buffer_seconds.
        """
        ...

    def reset_and_refresh(self: Any) -> Any:
        """
        Reset token state and attempt to refresh.
        
                This method is used for in-place token updates to avoid
                creating new token objects that would leave concurrent threads
                with stale references.
        """
        ...

    def set_bearer_token(self: Any) -> None:
        """
        Obtain a bearer token using the provided access key and secret key.
        
                Thread-safe: Uses a lock to prevent concurrent refresh attempts.
                On failure, resets bearer_token to None to ensure stale tokens aren't used.
        """
        ...

