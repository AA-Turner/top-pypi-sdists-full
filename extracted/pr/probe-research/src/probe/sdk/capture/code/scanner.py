"""SecretScanner: how the code snapshot asks which credential rules fire in a text (rule names, never values).
Picked once by scan depth; moves to sdk/redaction/ with redaction.py (a sync source the server vendors by path)."""

from __future__ import annotations

from typing import Protocol

from ....foundation.compat.compat import StrEnum
from ....foundation.transcripts.credential_scan.credential_scan import Finding
from .scanners.patterns import PatternScanner
from .scanners.quick import QuickScanner


class SecretScanner(Protocol):
    """Finds credentials in text: each finding names a rule and a span, never the matched value."""

    def scan(self, text: str) -> list[Finding]:
        """Every credential-shaped span in `text`, in order."""
        ...


class ScanDepth(StrEnum):
    """How much of the shared rule set a scan runs."""

    FULL = "full"  # every rule, with the decoding layer (base64, %xx, \uXXXX)
    QUICK = "quick"  # every rule near its keywords, no decoding: for text past FULL_SCAN_MAX_BYTES


_SCANNERS: dict[ScanDepth, SecretScanner] = {ScanDepth.FULL: PatternScanner(), ScanDepth.QUICK: QuickScanner()}


def get_scanner(depth: ScanDepth) -> SecretScanner:
    """The one scanner for `depth`."""
    return _SCANNERS[depth]
