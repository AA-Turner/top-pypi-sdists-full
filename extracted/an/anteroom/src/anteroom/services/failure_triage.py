"""Failure triage extraction for workflow repair targeting."""

from __future__ import annotations

import hashlib
import re
from typing import Any


def extract_failure_triage(
    summary: str,
    findings: list[dict[str, Any]],
    artifacts: dict[str, Any],
) -> dict[str, Any] | None:
    """Extract normalized failure-triage fields from failed step output.

    Searches summary first, then findings content if summary is sparse.
    Returns None if no structured signal is found (graceful degradation).
    """
    texts = [summary] if summary else []
    for f in findings:
        content = f.get("content", "")
        if content:
            texts.append(content)

    combined = "\n".join(texts)
    if not combined.strip():
        return None

    triage: dict[str, Any] = {}

    # Exit code from artifacts
    exit_code = artifacts.get("exit_code")
    if exit_code is not None:
        triage["exit_code"] = exit_code

    # First FAILED test (pytest format)
    failed_match = re.search(
        r"FAILED\s+([\w/\-\.]+\.py::[:\w]+)(?:\s+-\s+(.+))?",
        combined,
    )
    if failed_match:
        triage["first_failing_test"] = failed_match.group(1)
        if failed_match.group(2):
            triage["first_assertion"] = failed_match.group(2).strip()

    # Assertion line (E   AssertionError: ...)
    if "first_assertion" not in triage:
        assertion_match = re.search(r"^E\s+(.+)$", combined, re.MULTILINE)
        if assertion_match:
            triage["first_assertion"] = assertion_match.group(1).strip()

    # First traceback frame (repo file, not stdlib)
    tb_match = re.search(
        r"([\w/\-\.]+\.py):(\d+):\s+in\s+(\w+)",
        combined,
    )
    if tb_match:
        triage["first_traceback_file"] = tb_match.group(1)
        triage["first_traceback_line"] = int(tb_match.group(2))

    # Ruff error
    if not triage.get("first_failing_test"):
        ruff_match = re.search(
            r"^([\w/\-\.]+\.py:\d+:\d+):\s+([A-Z]\d+)\s+(.+)",
            combined,
            re.MULTILINE,
        )
        if ruff_match:
            triage["first_failing_test"] = ruff_match.group(1)
            triage["first_assertion"] = f"{ruff_match.group(2)} {ruff_match.group(3)}"

    # Failure count
    count_match = re.search(r"(\d+)\s+failed", combined)
    if not count_match:
        count_match = re.search(r"Found\s+(\d+)\s+errors?", combined)
    if count_match:
        triage["failure_count"] = int(count_match.group(1))

    if not triage:
        return None

    # Compute stable failure signature
    triage["failure_signature"] = compute_failure_signature(triage)

    return triage


def compute_failure_signature(triage: dict[str, Any]) -> str:
    """Compute a stable SHA-256 signature from key triage fields."""
    parts = [
        triage.get("first_failing_test", ""),
        triage.get("first_assertion", ""),
        triage.get("first_traceback_file", ""),
        str(triage.get("first_traceback_line", "")),
    ]
    # Fallback: if no test/assertion, use exit code
    if not any(parts[:2]):
        parts.append(str(triage.get("exit_code", "")))

    content = "|".join(parts)
    return hashlib.sha256(content.encode()).hexdigest()[:16]
