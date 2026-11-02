"""Tests for snapshot-bound queue-state ref writes."""

import base64
import json
from typing import Any
from unittest.mock import Mock, call

import pytest

from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.reconciliation.queue_store import ConcurrentModificationError
from agentic_devtools.cli.ci.reconciliation.ref_head_writer import _write_ref_head

_ROOT = "/repos/owner/repo/git"
_REF = f"{_ROOT}/ref/heads/custom-state"
_UPDATE = f"{_ROOT}/refs/heads/custom-state"


@pytest.fixture
def api() -> Mock:
    return Mock(
        side_effect=[
            json.dumps({"object": {"sha": "H0"}}),
            json.dumps({"tree": {"sha": "T0"}}),
            json.dumps({"sha": "B1"}),
            json.dumps({"sha": "T1"}),
            json.dumps({"sha": "H1"}),
            "",
        ]
    )


@pytest.mark.parametrize("expected_head", [None, "H0"])
def test_ref_head_cas_creates_child_commit_and_advances_ref(api: Mock, expected_head: str | None) -> None:
    if expected_head is not None:
        api.side_effect = list(api.side_effect)[1:]
    prepare = Mock(return_value=b'{"revision":2}')
    bootstrap = Mock()
    _write_ref_head(
        "owner/repo",
        "custom-state",
        api=api,
        bootstrap=bootstrap,
        prepare_content=prepare,
        conflict_error=ConcurrentModificationError,
        expected_head=expected_head,
    )
    prepare.assert_called_once_with("H0")
    bootstrap.assert_not_called()
    calls = [
        call(f"{_ROOT}/commits/H0"),
        call(
            f"{_ROOT}/blobs",
            method="POST",
            body={
                "content": base64.b64encode(b'{"revision":2}').decode("ascii"),
                "encoding": "base64",
            },
        ),
        call(
            f"{_ROOT}/trees",
            method="POST",
            body={
                "base_tree": "T0",
                "tree": [{"path": ".agdt/ai-pr-loop-state.json", "mode": "100644", "type": "blob", "sha": "B1"}],
            },
        ),
        call(
            f"{_ROOT}/commits",
            method="POST",
            body={
                "message": "chore: update ai-pr-loop reconciliation state",
                "tree": "T1",
                "parents": ["H0"],
            },
        ),
        call(_UPDATE, method="PATCH", body={"sha": "H1", "force": False}),
    ]
    assert api.call_args_list == ([call(_REF)] if expected_head is None else []) + calls


@pytest.mark.parametrize(
    "error",
    [
        "409 Conflict",
        'GitHub API error: 422 {"message":"Update is not a fast forward"}',
        'GitHub API error: 422 {"errors":[{"code":"non_fast_forward"}]}',
    ],
)
def test_ref_update_conflict_preserves_newer_queue(error: str) -> None:
    ref: dict[str, Any] = {"head": "H0", "queue": {"revision": 1}}
    observed = []
    parents = []

    def prepare(head: str) -> bytes:
        assert head == ref["head"] == "H0"
        observed.append(ref["queue"]["revision"])
        ref.update(head="WINNER", queue={"revision": 2, "winner": True})
        return b'{"revision":2,"loser":true}'

    def request(endpoint: str, *, method: str = "GET", body=None) -> str:
        if endpoint == _REF:
            return json.dumps({"object": {"sha": ref["head"]}})
        if endpoint == f"{_ROOT}/commits/H0":
            return json.dumps({"tree": {"sha": "T0"}})
        if endpoint == f"{_ROOT}/commits":
            parents.extend(body["parents"])
        if method == "PATCH":
            assert parents == ["H0"] and ref["head"] == "WINNER"
            assert body == {"sha": "LOSER", "force": False}
            raise RuntimeError(error)
        return json.dumps({"sha": "LOSER"})

    api = Mock(side_effect=request)
    with pytest.raises(ConcurrentModificationError, match="changed during save"):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=prepare,
            conflict_error=ConcurrentModificationError,
        )
    assert observed == [1]
    assert ref == {"head": "WINNER", "queue": {"revision": 2, "winner": True}}
    assert api.call_args_list.count(call(_REF)) == 1
    assert sum(c.kwargs.get("method") == "PATCH" for c in api.call_args_list) == 1


def test_missing_state_file_uses_existing_ref_head(api: Mock) -> None:
    bootstrap = Mock()
    events = Mock()
    events.attach_mock(api, "api")
    prepare = Mock(return_value=b'{"revision":1}')
    events.attach_mock(prepare, "prepare")
    _write_ref_head(
        "owner/repo",
        "custom-state",
        api=api,
        bootstrap=bootstrap,
        prepare_content=prepare,
        conflict_error=ConcurrentModificationError,
    )
    assert events.mock_calls[:3] == [
        call.api(_REF),
        call.prepare("H0"),
        call.api(f"{_ROOT}/commits/H0"),
    ]
    bootstrap.assert_not_called()
    assert api.call_args_list[-2].kwargs["body"]["parents"] == ["H0"]


def test_missing_ref_bootstrap_reads_back_created_head(api: Mock) -> None:
    api.side_effect = [RuntimeError("404 Not Found"), *list(api.side_effect)]
    bootstrap = Mock()
    prepare = Mock(return_value=b"new queue")
    events = Mock()
    events.attach_mock(api, "api")
    events.attach_mock(bootstrap, "bootstrap")
    events.attach_mock(prepare, "prepare")
    _write_ref_head(
        "owner/repo",
        "custom-state",
        api=api,
        bootstrap=bootstrap,
        prepare_content=prepare,
        conflict_error=ConcurrentModificationError,
    )
    assert events.mock_calls[:5] == [
        call.api(_REF),
        call.bootstrap("owner/repo", "custom-state"),
        call.api(_REF),
        call.prepare("H0"),
        call.api(f"{_ROOT}/commits/H0"),
    ]
    assert api.call_args_list[-2].kwargs["body"]["parents"] == ["H0"]


@pytest.mark.parametrize("error", ["403 Forbidden", "1404 lookup failed"])
def test_ref_lookup_failure_does_not_bootstrap(error: str) -> None:
    api, bootstrap, prepare = Mock(side_effect=RuntimeError(error)), Mock(), Mock()
    with pytest.raises(RuntimeError, match=error):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=bootstrap,
            prepare_content=prepare,
            conflict_error=ConcurrentModificationError,
        )
    bootstrap.assert_not_called()
    prepare.assert_not_called()


@pytest.mark.parametrize(
    "response", ["invalid-json", "[]", "{}", '{"object":[]}', '{"object":{"sha":""}}', '{"object":{"sha":42}}']
)
def test_rejects_invalid_ref_metadata(response: str) -> None:
    api, prepare = Mock(return_value=response), Mock()
    with pytest.raises(RuntimeError, match="Invalid GitHub"):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=prepare,
            conflict_error=ConcurrentModificationError,
        )
    prepare.assert_not_called()


@pytest.mark.parametrize(
    "error",
    [
        "422 Validation Failed",
        "1422 non-fast-forward",
        "403 Forbidden",
        "422 does not match",
    ],
)
def test_generic_ref_update_error_is_not_a_conflict(api: Mock, error: str) -> None:
    api.side_effect = [*list(api.side_effect)[:-1], RuntimeError(error)]
    with pytest.raises(RuntimeError, match=error) as caught:
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(return_value=b"state"),
            conflict_error=ConcurrentModificationError,
        )
    assert type(caught.value) is RuntimeError


def test_sanitized_422_with_newer_ref_is_a_conflict_without_retrying_patch(api: Mock) -> None:
    error = GitHubApiError(422)
    api.side_effect = [*list(api.side_effect)[:-1], error, json.dumps({"object": {"sha": "H2"}})]

    with pytest.raises(ConcurrentModificationError, match="changed during save"):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(return_value=b"state"),
            conflict_error=ConcurrentModificationError,
        )

    assert api.call_args_list.count(call(_REF)) == 2
    assert sum(c.kwargs.get("method") == "PATCH" for c in api.call_args_list) == 1


def test_sanitized_422_with_same_ref_reraises_original_error(api: Mock) -> None:
    error = GitHubApiError(422)
    api.side_effect = [*list(api.side_effect)[:-1], error, json.dumps({"object": {"sha": "H0"}})]

    with pytest.raises(GitHubApiError) as caught:
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(return_value=b"state"),
            conflict_error=ConcurrentModificationError,
        )

    assert caught.value is error
    assert api.call_args_list.count(call(_REF)) == 2


def test_sanitized_422_ref_read_failure_reraises_original_error(api: Mock) -> None:
    error = GitHubApiError(422)
    api.side_effect = [*list(api.side_effect)[:-1], error, RuntimeError("GET failed")]

    with pytest.raises(GitHubApiError) as caught:
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(return_value=b"state"),
            conflict_error=ConcurrentModificationError,
        )

    assert caught.value is error
    assert api.call_args_list.count(call(_REF)) == 2


def test_sanitized_409_is_a_conflict(api: Mock) -> None:
    api.side_effect = [*list(api.side_effect)[:-1], GitHubApiError(409)]

    with pytest.raises(ConcurrentModificationError, match="changed during save"):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(return_value=b"state"),
            conflict_error=ConcurrentModificationError,
        )

    assert api.call_args_list.count(call(_REF)) == 1
    assert sum(c.kwargs.get("method") == "PATCH" for c in api.call_args_list) == 1


def test_callback_failure_does_not_write(api: Mock) -> None:
    with pytest.raises(ConcurrentModificationError, match="revision mismatch"):
        _write_ref_head(
            "owner/repo",
            "custom-state",
            api=api,
            bootstrap=Mock(),
            prepare_content=Mock(side_effect=ConcurrentModificationError("revision mismatch")),
            conflict_error=ConcurrentModificationError,
        )
    assert api.call_args_list == [call(_REF)]
