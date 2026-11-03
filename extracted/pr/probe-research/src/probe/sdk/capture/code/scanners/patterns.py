"""PatternScanner: the shared rules (tap_core.secrets) with their decoding layer, read near each rule's keywords."""

from __future__ import annotations

from .....foundation.transcripts.credential_scan.credential_scan import Finding, scan
from .....foundation.transcripts.credential_scan.quick import _keyword_windows


class PatternScanner:
    """Full rules and decoding. Text of 4 KiB and more is read only next to the rules' keywords
    (`_keyword_windows`): the same findings as a whole read, found faster."""

    def scan(self, text: str) -> list[Finding]:
        return scan(text, _accel=_keyword_windows)
