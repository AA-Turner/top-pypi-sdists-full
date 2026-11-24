"""Content-IR rule 31 — NO BLANK KINDS. A ``__kind`` whose value is ``""`` is ALWAYS a defect.

Every detector that meets one calls ``report_blank_kind`` and then carries on
exactly as before: this REPORTS, it never changes control flow or a result.
Deduplicated per ``where`` + value shape (capped) so a stream does not spam.
Dependency-free on purpose (matrx-graph must not import aidream; matrx-ai
imports this helper).
"""

from __future__ import annotations

import logging
from typing import Any

_logger = logging.getLogger(__name__)

_MAX_REPORTED = 200
_reported: set[str] = set()


def _emit(where: str, shape: str) -> None:
    key = f"{where}|{shape}"
    if key in _reported or len(_reported) >= _MAX_REPORTED:
        return
    _reported.add(key)
    _logger.error(
        'BLANK KIND ("__kind": "") at %s — a kind is NAMED or the key is ABSENT, never "". content-ir rule 31.',
        where,
    )


def report_blank_kind(where: str, value: Any) -> bool:
    """Log at ERROR when ``value`` is a mapping whose ``__kind`` key is exactly ``""``."""
    if not isinstance(value, dict) or value.get("__kind") != "" or "__kind" not in value:
        return False
    _emit(where, ",".join(sorted(str(k) for k in value)))
    return True


def report_blank_kind_string(where: str, kind: Any) -> bool:
    """Same report for a caller holding only the extracted kind string."""
    if not isinstance(kind, str) or kind != "":
        return False
    _emit(where, "")
    return True


def reset_blank_kind_reports() -> None:
    """Test seam: forget what was reported."""
    _reported.clear()
