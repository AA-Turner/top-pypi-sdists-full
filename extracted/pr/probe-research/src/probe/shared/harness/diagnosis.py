"""HarnessDiagnosis facet of HarnessIntegration: the rows (and their ok/off/missing words), warnings and binary version probe doctor and session status show for one harness."""

from __future__ import annotations

_OK = "ok"
_OFF = "off"
_MISSING = "not installed"


def _row(label: str, value: str) -> str:
    return f"  {label:<24} {value}"
