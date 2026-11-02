"""Tests for GitHubVariableBackingStore."""

from __future__ import annotations

import base64
import json
from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci.reconciliation.models import QueueState
from agentic_devtools.cli.ci.reconciliation.queue_store import (
    ConcurrentModificationError,
    GitHubVariableBackingStore,
    QueueStoreError,
    StateDecodeError,
    StateTooLargeError,
)
from agentic_devtools.cli.ci.reconciliation.ref_head_writer import _write_ref_head
from agentic_devtools.state import serialize_queue_document


@pytest.fixture(autouse=True)
def _default_workflow_pat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")


@pytest.fixture(autouse=True)
def writer(monkeypatch: pytest.MonkeyPatch) -> Mock:
    mock = Mock(side_effect=lambda *_args, **kwargs: kwargs["prepare_content"]("head-sha"))
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.queue_store._write_ref_head", mock)
    return mock


def _make_state(*, revision: int) -> QueueState:
    return QueueState(
        repo="owner/repo",
        revision=revision,
        items={},
        records=[],
        quarantines=[],
        last_updated_at=datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
    )


def _variable_payload(state: QueueState) -> str:
    return json.dumps(
        {
            "content": base64.b64encode(serialize_queue_document(asdict(state))).decode("ascii"),
            "sha": f"sha-{state.revision}",
        }
    )


def test_load_entry_returns_none_when_variable_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_gh_api(endpoint: str, **_kwargs: Any) -> str:
        raise RuntimeError(f"GitHub API error: 404 Not Found ({endpoint})")

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    assert backing.load_entry(("owner/repo", "ai-pr-loop-state")) is None


def test_load_entry_reraises_non_404_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_gh_api(endpoint: str, **_kwargs: Any) -> str:
        raise RuntimeError(f"GitHub API error: 403 Forbidden ({endpoint})")

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(RuntimeError, match="403"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_load_entry_does_not_treat_1404_as_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_gh_api(endpoint: str, **_kwargs: Any) -> str:
        raise RuntimeError(f"GitHub API error: lookup id 1404 failed ({endpoint})")

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(RuntimeError, match="1404"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_load_entry_decodes_valid_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _make_state(revision=3)

    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        return _variable_payload(state)

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    assert backing.load_entry(("owner/repo", "ai-pr-loop-state")) == (3, state)


def test_load_entry_uses_default_workflow_token(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _make_state(revision=3)
    seen: dict[str, Any] = {}

    def _fake_gh_api(_endpoint: str, **kwargs: Any) -> str:
        seen.update(kwargs)
        return _variable_payload(state)

    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)

    GitHubVariableBackingStore(repo="owner/repo").load_entry(("owner/repo", "ai-pr-loop-state"))

    assert seen["token"] == "default-token"


def test_load_entry_requires_default_workflow_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", raising=False)
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", "REPO_VARIABLE_WRITER_PAT")
    monkeypatch.setenv("GH_TOKEN", "writer-token")

    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(RuntimeError, match="DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_load_entry_rejects_oversized_variable_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _make_state(revision=3)

    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        return _variable_payload(state)

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.queue_store.config.MAX_STATE_SIZE_BYTES", 8)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(StateTooLargeError, match="State size exceeds"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_load_entry_raises_state_decode_error_for_invalid_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        return json.dumps({"name": "AI_PR_LOOP_STATE", "value": "not-json"})

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(StateDecodeError, match="Failed to decode queue state"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_load_entry_raises_state_decode_error_without_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    state = _make_state(revision=3)

    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        payload = json.loads(_variable_payload(state))
        del payload["sha"]
        return json.dumps(payload)

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(StateDecodeError, match="blob SHA"):
        backing.load_entry(("owner/repo", "ai-pr-loop-state"))


def test_save_entry_updates_existing_variable(monkeypatch: pytest.MonkeyPatch, writer: Mock) -> None:
    backing = GitHubVariableBackingStore(repo="owner/repo")
    api = Mock(return_value=_variable_payload(_make_state(revision=1)))
    monkeypatch.setattr(backing, "_api", api)
    updated = _make_state(revision=2)
    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 1, updated)
    api.assert_called_once_with("/repos/owner/repo/contents/.agdt/ai-pr-loop-state.json?ref=head-sha")
    assert writer.call_args.args == ("owner/repo", "ai-pr-loop-state")
    assert writer.call_args.kwargs["api"] == backing._api
    assert writer.call_args.kwargs["bootstrap"] == backing._create_state_ref
    assert writer.call_args.kwargs["conflict_error"] is ConcurrentModificationError
    assert writer.call_args.kwargs["prepare_content"]("head-sha") == serialize_queue_document(asdict(updated))


def test_save_entry_rejects_oversized_existing_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    updated = _make_state(revision=2)

    def _fake_gh_api(_endpoint: str, *, method: str = "GET", **_kwargs: Any) -> str:
        if method == "GET":
            return _variable_payload(_make_state(revision=1))
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    monkeypatch.setattr("agentic_devtools.cli.ci.reconciliation.queue_store.config.MAX_STATE_SIZE_BYTES", 8)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(StateTooLargeError, match="State size exceeds"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 1, updated)


def test_recovery_replaces_corrupt_content_with_observed_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    updated = _make_state(revision=1)
    calls: list[tuple[str, str, dict[str, Any] | None]] = []

    def _fake_gh_api(endpoint: str, *, method: str = "GET", body: dict[str, Any] | None = None, **_kwargs: Any) -> str:
        calls.append((endpoint, method, body))
        if method == "GET":
            return json.dumps({"content": "not-valid-state", "sha": "corrupt-sha"})
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    token = backing.recovery_token(("owner/repo", "ai-pr-loop-state"))
    assert token == "corrupt-sha"
    backing.save_recovery_entry(("owner/repo", "ai-pr-loop-state"), token, updated)

    assert calls[1][2] is not None
    assert calls[1][2]["sha"] == "corrupt-sha"


@pytest.mark.parametrize("error", ["404 Not Found", "403 Forbidden"])
def test_recovery_token_handles_api_errors(monkeypatch: pytest.MonkeyPatch, error: str) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError(error)),
    )
    backing = GitHubVariableBackingStore(repo="owner/repo")

    if error.startswith("404"):
        assert backing.recovery_token(("owner/repo", "ai-pr-loop-state")) is None
    else:
        with pytest.raises(RuntimeError, match="403"):
            backing.recovery_token(("owner/repo", "ai-pr-loop-state"))


def test_recovery_token_requires_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        lambda *_args, **_kwargs: json.dumps({"content": "broken"}),
    )
    with pytest.raises(StateDecodeError, match="blob SHA"):
        GitHubVariableBackingStore(repo="owner/repo").recovery_token(("owner/repo", "ai-pr-loop-state"))


@pytest.mark.parametrize(
    ("error", "exception"),
    [
        ("409 Conflict", ConcurrentModificationError),
        ("upstream error code 1409 during write", RuntimeError),
        ("403 Forbidden", RuntimeError),
    ],
)
def test_save_recovery_maps_api_errors(
    monkeypatch: pytest.MonkeyPatch, error: str, exception: type[BaseException]
) -> None:
    monkeypatch.setattr(
        "agentic_devtools.cli.ci.github_provider._gh_api",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError(error)),
    )
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(exception):
        backing.save_recovery_entry(("owner/repo", "ai-pr-loop-state"), "sha-1", _make_state(revision=1))


def test_save_entry_creates_entry_after_get_404(monkeypatch: pytest.MonkeyPatch, writer: Mock) -> None:
    writer.side_effect = _write_ref_head
    backing = GitHubVariableBackingStore(repo="owner/repo")
    api = Mock(
        side_effect=[
            json.dumps({"object": {"sha": "H0"}}),
            RuntimeError("404 Not Found"),
            json.dumps({"tree": {"sha": "T0"}}),
            *[json.dumps({"sha": "new"})] * 3,
            "",
        ]
    )
    monkeypatch.setattr(backing, "_api", api)
    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))
    assert api.call_args_list[1].args[0].endswith("?ref=H0")
    assert api.call_args_list[-2].kwargs["body"]["parents"] == ["H0"]


def test_save_entry_creates_ref_when_initial_put_is_missing(monkeypatch: pytest.MonkeyPatch, writer: Mock) -> None:
    writer.side_effect = _write_ref_head
    backing = GitHubVariableBackingStore(repo="owner/repo")
    create_ref = Mock()
    api = Mock(
        side_effect=[
            RuntimeError("404 Not Found"),
            json.dumps({"object": {"sha": "created"}}),
            RuntimeError("404 Not Found"),
            json.dumps({"tree": {"sha": "T0"}}),
            *[json.dumps({"sha": "new"})] * 3,
            "",
        ]
    )
    monkeypatch.setattr(backing, "_api", api)
    monkeypatch.setattr(backing, "_create_state_ref", create_ref)
    events = Mock()
    events.attach_mock(api, "api")
    events.attach_mock(create_ref, "bootstrap")
    backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))
    create_ref.assert_called_once_with("owner/repo", "ai-pr-loop-state")
    assert [c[0] for c in events.mock_calls[:3]] == ["api", "bootstrap", "api"]
    assert api.call_args_list[2].args[0].endswith("?ref=created")
    assert api.call_args_list[-2].kwargs["body"]["parents"] == ["created"]


def test_save_entry_retry_put_raises_concurrent_modification_on_conflict(
    monkeypatch: pytest.MonkeyPatch,
    writer: Mock,
) -> None:
    writer.side_effect = _write_ref_head
    backing = GitHubVariableBackingStore(repo="owner/repo")
    bootstrap = Mock()
    api = Mock(
        side_effect=[
            RuntimeError("404 Not Found"),
            json.dumps({"object": {"sha": "created"}}),
            RuntimeError("404 Not Found"),
            json.dumps({"tree": {"sha": "T0"}}),
            *[json.dumps({"sha": "new"})] * 3,
            RuntimeError("409 Conflict"),
        ]
    )
    monkeypatch.setattr(backing, "_api", api)
    monkeypatch.setattr(backing, "_create_state_ref", bootstrap)
    with pytest.raises(ConcurrentModificationError, match="changed during save"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))
    bootstrap.assert_called_once_with("owner/repo", "ai-pr-loop-state")
    writer.assert_called_once()


def test_save_entry_retry_put_normalizes_non_conflict_error(writer: Mock) -> None:
    writer.side_effect = RuntimeError("500 Internal Server Error")
    backing = GitHubVariableBackingStore(repo="owner/repo")
    with pytest.raises(QueueStoreError, match="500"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))


@pytest.mark.parametrize(
    ("responses", "match"),
    [
        ([json.dumps({})], "default branch"),
        ([json.dumps({"default_branch": "main"}), json.dumps({})], "commit SHA"),
    ],
)
def test_create_state_ref_rejects_missing_repository_metadata(
    monkeypatch: pytest.MonkeyPatch, responses: list[str], match: str
) -> None:
    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", lambda *_args, **_kwargs: responses.pop(0))

    with pytest.raises(StateDecodeError, match=match):
        GitHubVariableBackingStore._create_state_ref("owner/repo", "ai-pr-loop-state")


def test_create_state_ref_ignores_already_exists_error(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = [
        json.dumps({"default_branch": "main"}),
        json.dumps({"object": {"sha": "default-sha"}}),
    ]

    def _fake_gh_api(_endpoint: str, *, method: str = "GET", **_kwargs: Any) -> str:
        if method == "POST":
            raise RuntimeError("GitHub API error: 422 already exists")
        return responses.pop(0)

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)

    GitHubVariableBackingStore._create_state_ref("owner/repo", "ai-pr-loop-state")


def test_create_state_ref_reraises_unexpected_error(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = [
        json.dumps({"default_branch": "main"}),
        json.dumps({"object": {"sha": "default-sha"}}),
    ]

    def _fake_gh_api(_endpoint: str, *, method: str = "GET", **_kwargs: Any) -> str:
        if method == "POST":
            raise RuntimeError("GitHub API error: 500")
        return responses.pop(0)

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)

    with pytest.raises(RuntimeError, match="500"):
        GitHubVariableBackingStore._create_state_ref("owner/repo", "ai-pr-loop-state")


def test_save_entry_raises_on_revision_conflict(monkeypatch: pytest.MonkeyPatch) -> None:
    current = _make_state(revision=2)
    updated = _make_state(revision=3)

    def _fake_gh_api(_endpoint: str, *, method: str = "GET", **_kwargs: Any) -> str:
        if method == "GET":
            return _variable_payload(current)
        raise AssertionError("save should not be attempted after a CAS conflict")

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(ConcurrentModificationError, match="expected 1, got 2"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 1, updated)


def test_save_entry_normalizes_non_404_put_errors(writer: Mock) -> None:
    writer.side_effect = RuntimeError("403 Forbidden")
    backing = GitHubVariableBackingStore(repo="owner/repo")
    with pytest.raises(QueueStoreError, match="403"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))


def test_save_entry_normalizes_non_404_get_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    updated = _make_state(revision=1)

    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        raise RuntimeError("GitHub API error: 403 Forbidden")

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(QueueStoreError, match="403"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, updated)


def test_save_entry_raises_state_decode_error_for_invalid_existing_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    updated = _make_state(revision=1)

    def _fake_gh_api(_endpoint: str, **_kwargs: Any) -> str:
        return json.dumps({"content": "not-base64", "sha": "sha-1"})

    monkeypatch.setattr("agentic_devtools.cli.ci.github_provider._gh_api", _fake_gh_api)
    backing = GitHubVariableBackingStore(repo="owner/repo")

    with pytest.raises(StateDecodeError, match="Failed to decode queue state"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, updated)


def test_save_entry_maps_put_conflict_to_concurrent_modification(writer: Mock) -> None:
    writer.side_effect = RuntimeError("409 Conflict")
    backing = GitHubVariableBackingStore(repo="owner/repo")
    with pytest.raises(ConcurrentModificationError, match="changed during save"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))


def test_save_entry_does_not_treat_1409_as_conflict(writer: Mock) -> None:
    writer.side_effect = RuntimeError("upstream id 1409 failed")
    backing = GitHubVariableBackingStore(repo="owner/repo")
    with pytest.raises(QueueStoreError, match="1409"):
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))


@pytest.mark.parametrize("error", ["422 Validation Failed", "403 Forbidden", "422 does not match"])
def test_save_entry_normalizes_non_conflict_ref_write_error(
    monkeypatch: pytest.MonkeyPatch,
    writer: Mock,
    error: str,
) -> None:
    writer.side_effect = _write_ref_head
    backing = GitHubVariableBackingStore("owner/repo")
    api = Mock(
        side_effect=[
            json.dumps({"object": {"sha": "H0"}}),
            RuntimeError("404 Not Found"),
            json.dumps({"tree": {"sha": "T0"}}),
            *[json.dumps({"sha": "new"})] * 3,
            RuntimeError(error),
        ]
    )
    monkeypatch.setattr(backing, "_api", api)
    with pytest.raises(QueueStoreError, match="Failed to persist") as caught:
        backing.save_entry(("owner/repo", "ai-pr-loop-state"), 0, _make_state(revision=1))
    assert type(caught.value) is QueueStoreError
