"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.context import (
    ContentLocator,
    ContextProvenance,
    InjectedField,
)


def test_content_locator_rejects_invalid_locator_type() -> None:
    with pytest.raises(ValueError, match="Invalid locator_type"):
        ContentLocator(locator_type="not_a_type", locator_value="x")


def test_content_locator_requires_revision_for_artifact_path() -> None:
    with pytest.raises(ValueError, match="revision-pinned"):
        ContentLocator(locator_type="artifact_path", locator_value="specs/x/spec.md", revision=None)


def test_issue_url_locator_requires_snapshot_ref() -> None:
    locator = ContentLocator(locator_type="issue_url", locator_value="https://github.com/org/repo/issues/1")
    with pytest.raises(ValueError, match="issue_url locator"):
        InjectedField(name="x", content="c", provenance=ContextProvenance.VERIFIED, locator=locator, snapshot_ref=None)
