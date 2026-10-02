"""Compatibility response header reading and warning mechanism.

Reads X-Istari-Compatibility, X-Istari-Incompatible-Tags, and
X-Istari-Deprecated-Tags headers from server responses and emits
warnings on first occurrence.
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("istari.compatibility")


@dataclass
class CompatibilityResult:
    """Structured result from a compatibility header check."""

    server_version: Optional[str] = None
    status: Optional[str] = None
    incompatible_tags: list[str] = field(default_factory=list)
    deprecated_tags: list[str] = field(default_factory=list)


class CompatibilityChecker:
    """Reads compatibility response headers and emits warnings once per session."""

    def __init__(self) -> None:
        self._warned: bool = False
        self.last_result: Optional[CompatibilityResult] = None

    def process_response_headers(self, headers: dict) -> None:
        """Check response headers for compatibility information.

        Args:
            headers: Response headers dict (may be case-sensitive after conversion from HTTPHeaderDict).
        """
        # Normalize to lowercase keys — urllib3's HTTPHeaderDict loses
        # case-insensitivity when converted to a plain dict.
        h = {k.lower(): v for k, v in headers.items()}

        version = h.get("x-istari-registry-version")
        status = h.get("x-istari-compatibility")

        if version is None and status is None:
            return

        result = CompatibilityResult(server_version=version, status=status)

        incompatible = h.get("x-istari-incompatible-tags", "")
        if incompatible:
            result.incompatible_tags = [t.strip() for t in incompatible.split(",") if t.strip()]

        deprecated = h.get("x-istari-deprecated-tags", "")
        if deprecated:
            result.deprecated_tags = [t.strip() for t in deprecated.split(",") if t.strip()]

        self.last_result = result

        if self._warned:
            return

        v = f"v{version}" if version else "unknown version"

        if status == "compatible":
            logger.info("Connected to Istari Registry %s — SDK is up to date.", v)
            self._warned = True
            return

        if status == "incompatible":
            self._warned = True
            msg = (
                f"SDK is incompatible with Istari Registry {v} "
                f"(affected APIs: {', '.join(result.incompatible_tags)}). "
                "Please update your SDK to match the server version."
            )
            warnings.warn(msg, UserWarning, stacklevel=4)
            logger.warning(msg)

        elif status == "revision-mismatch":
            self._warned = True
            msg = (
                f"SDK has a minor version difference with Istari Registry {v} "
                f"(affected APIs: {', '.join(result.incompatible_tags)}). "
                "Some newer API features may not be available."
            )
            warnings.warn(msg, UserWarning, stacklevel=4)
            logger.warning(msg)

        elif status == "deprecation-warning":
            self._warned = True
            msg = (
                f"SDK uses deprecated APIs on Istari Registry {v} "
                f"(affected APIs: {', '.join(result.deprecated_tags)}). "
                "Consider updating your SDK to avoid future incompatibility."
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=4)
            logger.warning(msg)
