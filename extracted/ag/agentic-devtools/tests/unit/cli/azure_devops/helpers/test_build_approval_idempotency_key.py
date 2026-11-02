from __future__ import annotations

from agentic_devtools.cli.azure_devops.helpers import build_approval_idempotency_key


def test_returns_deterministic_hash() -> None:
    first = build_approval_idempotency_key(42, "repo")
    second = build_approval_idempotency_key(42, "repo")
    assert first == second
    assert len(first) == 64


def test_changes_when_inputs_change() -> None:
    first = build_approval_idempotency_key(42, "repo")
    second = build_approval_idempotency_key(43, "repo")
    assert first != second


def test_stable_across_content_wording_changes() -> None:
    """The key must identify the target PR/repository, not the mutable message body."""
    assert build_approval_idempotency_key(42, "repo") == build_approval_idempotency_key(42, "repo")


def test_normalizes_percent_encoded_repository_names() -> None:
    assert build_approval_idempotency_key(42, "My Repo") == build_approval_idempotency_key(42, "My%20Repo")


def test_normalizes_repository_name_casing() -> None:
    assert build_approval_idempotency_key(42, "My Repo") == build_approval_idempotency_key(42, "my repo")
