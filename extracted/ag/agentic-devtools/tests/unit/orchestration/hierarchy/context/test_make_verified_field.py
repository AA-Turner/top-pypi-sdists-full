"""Unit tests for ContextProvenance and verified/unavailable/inferred field construction."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.orchestration.hierarchy.context import (
    ContextProvenance,
    make_verified_field,
    sha256_hex,
)
from agentic_devtools.orchestration.hierarchy.protected_storage import ProtectedStorage, derive_caller_identity


def test_make_verified_field_uses_locator_when_untransformed() -> None:
    field = make_verified_field("spec_md", "# Spec\ncontent", artifact_path="specs/x/spec.md", revision="abc123")
    assert field.provenance == ContextProvenance.VERIFIED
    assert field.locator is not None
    assert field.locator.locator_type == "artifact_path"
    assert field.snapshot_ref is None
    assert field.content_sha256 == sha256_hex("# Spec\ncontent")


def test_make_verified_field_requires_snapshot_when_redacted() -> None:
    with pytest.raises(ValueError, match="durable snapshot_ref is required"):
        make_verified_field(
            "spec_md",
            "secret-token content",
            artifact_path="specs/x/spec.md",
            revision="abc123",
            redact_patterns=("secret-token",),
        )


def test_make_verified_field_with_redaction_and_snapshot_ref() -> None:
    redacted_content = "[REDACTED] content"
    field = make_verified_field(
        "spec_md",
        "secret-token content",
        artifact_path="specs/x/spec.md",
        revision="abc123",
        redact_patterns=("secret-token",),
        snapshot_ref=f"sha256:{sha256_hex(redacted_content)}",
    )
    assert field.content == redacted_content
    assert field.locator is None
    assert field.snapshot_ref == f"sha256:{sha256_hex(redacted_content)}"


def test_make_verified_field_rejects_mismatched_transformed_snapshot_ref() -> None:
    with pytest.raises(ValueError, match="content-addressed and match"):
        make_verified_field(
            "spec_md",
            "secret-token content",
            artifact_path="specs/x/spec.md",
            revision="abc123",
            redact_patterns=("secret-token",),
            snapshot_ref="sha256:deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
        )


def test_make_verified_field_persists_transformed_content_when_storage_is_available(
    tmp_path: Path,
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson",
        master_key=b"unit-test-master-key-material-32b",
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    field = make_verified_field(
        "spec_md",
        "secret-token content",
        artifact_path="specs/x/spec.md",
        revision="abc123",
        redact_patterns=("secret-token",),
        protected_storage=storage,
    )
    assert field.snapshot_ref == f"sha256:{sha256_hex('[REDACTED] content')}"
    assert storage.read_all() == [b"[REDACTED] content"]


def test_make_verified_field_rejects_mismatched_explicit_snapshot_ref_when_storage_persists_content(
    tmp_path: Path,
) -> None:
    storage = ProtectedStorage(
        tmp_path / "snapshots.ndjson",
        master_key=b"unit-test-master-key-material-32b",
        authorized_principals=frozenset({derive_caller_identity()}),
    )
    with pytest.raises(ValueError, match="retained transformed content"):
        make_verified_field(
            "spec_md",
            "secret-token content",
            artifact_path="specs/x/spec.md",
            revision="abc123",
            redact_patterns=("secret-token",),
            snapshot_ref="sha256:" + ("a" * 64),
            protected_storage=storage,
        )
