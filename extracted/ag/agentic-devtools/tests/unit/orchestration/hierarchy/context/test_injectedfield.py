"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.hierarchy.context import (
    ContextProvenance,
    InjectedField,
)


def test_injected_field_requires_snapshot_or_locator() -> None:
    with pytest.raises(ValueError, match="snapshot_ref or a locator"):
        InjectedField(name="x", content="c", provenance=ContextProvenance.VERIFIED, locator=None, snapshot_ref=None)


def test_injected_field_rejects_non_sha256_snapshot_ref_for_verified_content() -> None:
    with pytest.raises(ValueError, match="sha256:<64 lowercase hex>"):
        InjectedField(
            name="x",
            content="c",
            provenance=ContextProvenance.VERIFIED,
            locator=None,
            snapshot_ref="sha256:xyz",
        )


def test_injected_field_rejects_snapshot_ref_not_matching_content() -> None:
    """snapshot_ref format is valid but does not match sha256(content)."""
    correct_hash = "sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"  # sha256("hello")
    with pytest.raises(ValueError, match="snapshot_ref must be content-addressed"):
        InjectedField(
            name="x",
            content="world",  # sha256 is different from correct_hash
            provenance=ContextProvenance.VERIFIED,
            locator=None,
            snapshot_ref=correct_hash,
        )


def test_injected_field_rejects_non_string_content() -> None:
    """InjectedField content must be a string."""
    valid_sha256 = "sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    with pytest.raises(ValueError, match="content must be a string"):
        InjectedField(
            name="x",
            content=123,  # type: ignore[arg-type]
            provenance=ContextProvenance.VERIFIED,
            locator=None,
            snapshot_ref=valid_sha256,
        )
