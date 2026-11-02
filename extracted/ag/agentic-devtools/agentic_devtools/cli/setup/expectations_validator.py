"""Sync-gate validator for the setup expectations document.

Parses ``docs/setup-expectations/agdt-setup.md`` and validates it against
the canonical source of truth (``PHASES`` tuple and ``exit_codes`` module).
Used by both the thin CLI wrapper and the checks pipeline integration.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple

from .exit_codes import ALL_EXIT_CODES
from .phases import PHASES

_EXPECTATIONS_DOC_REL = Path("docs") / "setup-expectations" / "agdt-setup.md"


class ValidationResult(NamedTuple):
    """Outcome of expectations validation."""

    passed: bool
    errors: list[str]


def _find_repo_root() -> Path | None:
    """Walk up from CWD to find a directory containing .git."""
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def _parse_phases_from_doc(content: str) -> list[str]:
    """Extract phase names from the ordered list in the Phases section."""
    phases: list[str] = []
    in_phases_section = False
    for line in content.splitlines():
        if line.strip().startswith("## Phases"):
            in_phases_section = True
            continue
        if in_phases_section and line.strip().startswith("## "):
            break
        if in_phases_section:
            # Match lines like "1. `version_check`"
            m = re.match(r"\d+\.\s+`([^`]+)`", line.strip())
            if m:
                phases.append(m.group(1))
    return phases


def _parse_exit_codes_from_doc(content: str) -> dict[str, int]:
    """Extract exit codes from the table in the Exit Codes section."""
    codes: dict[str, int] = {}
    in_codes_section = False
    for line in content.splitlines():
        if line.strip().startswith("## Exit Codes"):
            in_codes_section = True
            continue
        if in_codes_section and line.strip().startswith("## "):
            break
        if in_codes_section:
            # Match table rows like "| 0 | SUCCESS | ... |"
            m = re.match(r"\|\s*(\d+)\s*\|\s*(\w+)\s*\|", line.strip())
            if m:
                codes[m.group(2)] = int(m.group(1))
    return codes


def _has_mermaid_block(content: str) -> bool:
    """Check if the document contains a mermaid fenced code block."""
    return "```mermaid" in content


def _has_schema_section(content: str) -> bool:
    """Check if the document contains a Report Schema section."""
    return "## Report Schema" in content


def validate_expectations(repo_root: Path | None = None) -> ValidationResult:
    """Validate that the expectations doc matches source code.

    Args:
        repo_root: Repository root path. If None, auto-detected from CWD.

    Returns:
        A ``ValidationResult`` with pass/fail status and error messages.
    """
    if repo_root is None:
        repo_root = _find_repo_root()
    if repo_root is None:
        return ValidationResult(False, ["Cannot find repository root (no .git directory found)."])

    doc_path = repo_root / _EXPECTATIONS_DOC_REL
    if not doc_path.exists():
        return ValidationResult(False, [f"Expectations document not found: {doc_path}"])

    content = doc_path.read_text(encoding="utf-8")
    errors: list[str] = []

    # ── Check required sections ───────────────────────────────────────────
    if "## Phases" not in content:
        errors.append("Missing required section: ## Phases")
    if "## Exit Codes" not in content:
        errors.append("Missing required section: ## Exit Codes")
    if not _has_schema_section(content):
        errors.append("Missing required section: ## Report Schema")
    if not _has_mermaid_block(content):
        errors.append("Missing required Mermaid diagram (```mermaid block)")

    # ── Validate phases ───────────────────────────────────────────────────
    doc_phases = _parse_phases_from_doc(content)
    source_phases = list(PHASES)

    if doc_phases != source_phases:
        if set(doc_phases) - set(source_phases):
            extra = set(doc_phases) - set(source_phases)
            errors.append(f"Doc lists phases not in source: {sorted(extra)}")
        if set(source_phases) - set(doc_phases):
            missing = set(source_phases) - set(doc_phases)
            errors.append(f"Source phases missing from doc: {sorted(missing)}")
        if set(doc_phases) == set(source_phases) and doc_phases != source_phases:
            errors.append(f"Phase order mismatch: doc={doc_phases}, source={source_phases}")

    # ── Validate exit codes ───────────────────────────────────────────────
    doc_codes = _parse_exit_codes_from_doc(content)
    source_codes = dict(ALL_EXIT_CODES)

    if doc_codes != source_codes:
        extra_in_doc = set(doc_codes.keys()) - set(source_codes.keys())
        missing_from_doc = set(source_codes.keys()) - set(doc_codes.keys())
        if extra_in_doc:
            errors.append(f"Doc lists exit codes not in source: {sorted(extra_in_doc)}")
        if missing_from_doc:
            errors.append(f"Source exit codes missing from doc: {sorted(missing_from_doc)}")
        # Check value mismatches for codes present in both
        for name in set(doc_codes.keys()) & set(source_codes.keys()):
            if doc_codes[name] != source_codes[name]:
                errors.append(
                    f"Exit code value mismatch for {name}: doc={doc_codes[name]}, source={source_codes[name]}"
                )

    return ValidationResult(passed=len(errors) == 0, errors=errors)
