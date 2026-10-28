"""Registry API-version compatibility check.

Reads the registry's ``X-Istari-Registry-Version`` response header and warns once
per session when it differs from this SDK's built-against registry API version by
a **major** version. Same major → silent (compatible by contract). Never blocks;
real ``404``/``410``/``422`` responses carry the precise, usage-scoped truth.

``SDK_API_VERSION`` is generated from the registry spec's ``info.version`` at
codegen (``_api_version.py``); the registry serves the matching value because it
is built from its version-stamped tag at release (release-orchestration design
§7c). A ``0.x`` version on either side (pre-release / unstamped) disables the
compare. This replaces the old per-tag hash handshake (``X-Istari-Compatibility``
+ ``X-Istari-*-Tags``).
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from typing import Optional

from istari_digital_client.sdk._compatibility._api_version import SDK_API_VERSION

logger = logging.getLogger("istari.compatibility")


def _major(version: str) -> str:
    """Leading integer of a semver string (``v12.3.1`` / ``12.3.1-rc2`` → ``12``)."""
    return version.lstrip("v").split(".", 1)[0]


@dataclass
class CompatibilityResult:
    """Structured result from a compatibility header check.

    ``incompatible_tags`` / ``deprecated_tags`` are retained for backward
    compatibility with the old per-tag handshake; the major-only check leaves
    them empty.
    """

    server_version: Optional[str] = None
    status: Optional[str] = None
    incompatible_tags: list[str] = field(default_factory=list)
    deprecated_tags: list[str] = field(default_factory=list)


class CompatibilityChecker:
    """Reads ``X-Istari-Registry-Version`` and warns once on a major mismatch."""

    def __init__(self) -> None:
        self._warned: bool = False
        self.last_result: Optional[CompatibilityResult] = None

    def process_response_headers(self, headers: dict) -> None:
        """Read the registry version from response headers and warn once on a major gap.

        Args:
            headers: Response headers dict (may be case-sensitive after conversion
                from HTTPHeaderDict).
        """
        # Normalize to lowercase keys — urllib3's HTTPHeaderDict loses
        # case-insensitivity when converted to a plain dict.
        server = {k.lower(): v for k, v in headers.items()}.get("x-istari-registry-version")
        if not server:
            return

        # A 0.x version on either side is pre-release / unstamped — no compatibility
        # contract yet, so record the server version but do not judge.
        if _major(server) == "0" or _major(SDK_API_VERSION) == "0":
            self.last_result = CompatibilityResult(server_version=server, status="unknown")
            return

        same_major = _major(server) == _major(SDK_API_VERSION)
        self.last_result = CompatibilityResult(
            server_version=server,
            status="compatible" if same_major else "major-mismatch",
        )

        if self._warned or same_major:
            return

        self._warned = True
        msg = (
            f"This SDK was built against Istari Registry API v{SDK_API_VERSION}, but the "
            f"server is API v{server} — they differ by a major version and some calls may "
            "fail. Update your SDK."
        )
        warnings.warn(msg, UserWarning, stacklevel=4)
        logger.warning(msg)
