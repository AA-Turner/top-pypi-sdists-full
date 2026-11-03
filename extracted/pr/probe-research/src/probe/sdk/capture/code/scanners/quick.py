"""QuickScanner: the shared rules near their keywords with no decoding layer (tap_core.secrets.scan_quick)."""

from __future__ import annotations

from .....foundation.transcripts.credential_scan.credential_scan import Finding
from .....foundation.transcripts.credential_scan.quick import scan_quick


class QuickScanner:
    """What a file past FULL_SCAN_MAX_BYTES, or one chunk of it, is scanned with: no base64 or escape decoding."""

    def scan(self, text: str) -> list[Finding]:
        return scan_quick(text)
