"""Normative Markdown serialization for Phase 0 review results."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Literal, get_args

from agentic_devtools.cli.phase0_review.config import PROCESSING_TIMEOUT_SECONDS

FindingSection = Literal["template", "content"]
_FINDING_SECTIONS = frozenset(get_args(FindingSection))
_SERIALIZED_FINDING = re.compile(r"^- \[(?P<state>[ x])\]\s*(?P<text>.*)$")


def json_literal(value: str) -> str:
    """Serialize text as the JSON string literal required by the report contract."""
    return json.dumps(value, ensure_ascii=False)


@dataclass(frozen=True)
class Finding:
    """One already-classified report check."""

    section: FindingSection
    text: str
    passed: bool = False

    def __post_init__(self) -> None:
        """Reject unsupported sections so every blocking finding remains visible."""
        if self.section not in _FINDING_SECTIONS:
            raise ValueError(f"unsupported finding section: {self.section!r}")

    def serialize(self) -> str:
        """Return the normative checklist representation."""
        return f"- [{'x' if self.passed else ' '}] {self.text}"


def parse_serialized_finding(line: str) -> tuple[bool, str] | None:
    """Parse one serialized finding line into its status flag and text."""
    match = _SERIALIZED_FINDING.fullmatch(line)
    if match is None:
        return None
    return match.group("state") == "x", match.group("text")


def discrepancy(field: str, expected: str, observed: str) -> Finding:
    """Create a content-fidelity discrepancy finding."""
    return Finding(
        "content",
        f"Field {json_literal(field)}: expected {json_literal(expected)}, found {json_literal(observed)}",
    )


def structural(expected: str, observed: str) -> Finding:
    """Create a template-compliance structural finding."""
    return Finding("template", f"{json_literal(expected)}: {json_literal(observed)}")


def missing_input(expected: str, observed: str) -> Finding:
    """Create a missing-input finding."""
    return Finding(
        "template",
        f"Missing input: {json_literal(expected)}: {json_literal(observed)}",
    )


def malformed_input(expected: str, observed: str) -> Finding:
    """Create a malformed-input finding."""
    return Finding(
        "template",
        f"Malformed input: {json_literal(expected)}: {json_literal(observed)}",
    )


def ambiguity(field: str, reason: str) -> Finding:
    """Create an ambiguous-source finding."""
    return Finding(
        "template",
        f"Ambiguous source field {json_literal(field)}: {json_literal(reason)}",
    )


def render_report(findings: list[Finding], *, timed_out: bool = False) -> str:
    """Render findings and the deterministic gate verdict."""
    template = [finding for finding in findings if finding.section == "template"]
    content = [finding for finding in findings if finding.section == "content"]
    if timed_out:
        template.append(
            Finding(
                "template",
                f"Operational timeout: review exceeded the {int(PROCESSING_TIMEOUT_SECONDS)}-second ceiling",
            )
        )
    if not template:
        template = [Finding("template", "No structural findings", passed=True)]
    if not content:
        content = [Finding("content", "No content-fidelity checks performed", passed=True)]

    blocking = timed_out or any(not finding.passed for finding in findings)
    lines = ["## Template Compliance"]
    lines.extend(finding.serialize() for finding in template)
    lines.extend(("", "## Content Fidelity"))
    lines.extend(finding.serialize() for finding in content)
    lines.extend(("", "## Verdict", "CHANGES REQUESTED" if blocking else "APPROVED"))
    if not blocking:
        lines.append("confidence: 100%")
    return "\n".join(lines)
