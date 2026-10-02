"""Auth-deprecation response header reading and warning mechanism.

Reads the `X-Istari-Auth-Deprecation` header from server responses and emits
a one-time warning. The registry service sets this header on every response when
a request authenticates with a legacy personal access token (PAT) against an
Identity-Service-enabled registry, nudging the caller to migrate to key-pair
authentication (see `client.keys.exchange_pat()`).
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("istari_digital_client.auth_deprecation")

# Response header set by the registry service when authenticating with a legacy
# personal access token against an Identity-Service-enabled registry.
# (See `middleware/deprecated_auth.py` in the RS.)
AUTH_DEPRECATION_HEADER = "X-Istari-Auth-Deprecation"


@dataclass
class AuthDeprecationResult:
    """Structured result from an auth-deprecation header check."""

    detected: bool = False
    message: Optional[str] = None


class AuthDeprecationChecker:
    """Reads the auth-deprecation response header and warns once per session."""

    def __init__(self) -> None:
        self._warned: bool = False
        self.last_result: Optional[AuthDeprecationResult] = None

    def process_response_headers(self, headers: dict) -> None:
        """Check response headers for an auth-deprecation advisory.

        Args:
             headers: Response headers dict (may be case-sensitive after conversion
                 from HTTPHeaderDict).
        """
        # Normalize to lowercase keys — urllib3's HTTPHeaderDict loses
        # case-insensitivity when converted to a plain dict.
        h = {k.lower(): v for k, v in headers.items()}

        message = h.get(AUTH_DEPRECATION_HEADER.lower())
        if not message:
            return

        self.last_result = AuthDeprecationResult(detected=True, message=message)

        if self._warned:
            return

        self._warned = True
        full = (
            f"{message} You are authenticating with a personal access token against "
            "an Identity-Service-enabled registry. Migrate to key-pair authentication "
            "(see client.keys.exchange_pat())."
        )
        warnings.warn(full, DeprecationWarning, stacklevel=4)
        logger.warning(full)
