"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    minimize_and_redact,
)


def test_minimize_and_redact_skips_absent_pattern() -> None:
    content, transformed = minimize_and_redact("hello world", redact_patterns=("not-present", "world"))
    assert transformed is True
    assert content == "hello [REDACTED]"
