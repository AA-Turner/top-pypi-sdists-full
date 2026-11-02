"""Tests for the private read-token pool deadline signal."""

from __future__ import annotations

import json
from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.read_token_pool as read_token_pool
from agentic_devtools.cli.ci.read_token_pool_execution import ReadTokenPoolOperations

_FIRST = "NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_SECOND = "CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"


def test_deadline_exception_stops_loading_later_candidates() -> None:
    deadline_error = read_token_pool._ReadTokenPoolDeadlineExceeded("deadline expired")
    calls: list[tuple[str, str]] = []

    def request(endpoint: str, _token: str, identity: str) -> tuple[str, int | None]:
        calls.append((endpoint, identity))
        if identity == _SECOND:
            raise deadline_error
        return json.dumps({"login": "later-user"}), None

    with pytest.raises(read_token_pool._ReadTokenPoolDeadlineExceeded) as raised:
        read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token", _SECOND: "second-token"}),
            default_token="",
            default_identity=_DEFAULT,
            request=request,
            active_cooldowns=set(),
            on_rate_limit=Mock(),
        )

    assert raised.value is deadline_error
    assert calls == [("/user", _SECOND)]


def test_expired_candidate_revalidation_recovers_on_a_fresh_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    calls: list[tuple[str, str]] = []
    interrupted = [True]
    users = {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"}

    def request(endpoint: str, _token: str, identity: str) -> tuple[str, int | None]:
        calls.append((endpoint, identity))
        if endpoint == "/user" and identity == _FIRST and interrupted[0]:
            interrupted[0] = False
            raise read_token_pool._ReadTokenPoolDeadlineExceeded("deadline expired")
        return (json.dumps({"login": users[identity]}) if endpoint == "/user" else "{}"), None

    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token", _SECOND: "second-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        active_cooldowns={_FIRST: 100.0},
        on_rate_limit=Mock(),
    )
    assert pool.candidate_names == (_SECOND,)

    now[0] = 101.0
    with (
        ReadTokenPoolOperations.request_context(110.0, lambda: now[0]),
        pytest.raises(read_token_pool._ReadTokenPoolDeadlineExceeded),
    ):
        pool.candidate_names

    now[0] = 102.0
    with ReadTokenPoolOperations.request_context(120.0, lambda: now[0]):
        names = pool.candidate_names

    assert names == tuple(sorted((_FIRST, _SECOND)))
    assert calls.count(("/user", _FIRST)) == 2
    assert ("/repos/owner/repo", _FIRST) in calls
