"""Tests for recovering read-token cooldowns after interrupted revalidation."""

from __future__ import annotations

import json
from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.read_token_pool as read_token_pool
from agentic_devtools.cli.ci.retry import RetryableError

_FIRST = "NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_SECOND = "CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"


def test_interrupted_revalidation_preserves_a_fresh_rate_limit_cooldown(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    limited = RetryableError(
        "rate limited",
        retry_after=60,
        credential_identity=_SECOND,
        is_rate_limit=True,
    )
    failures: dict[tuple[str, str], Exception] = {
        ("/repos/owner/repo", _SECOND): limited,
        ("/user", _FIRST): read_token_pool._ReadTokenPoolDeadlineExceeded("deadline expired"),
    }
    calls: list[tuple[str, str, str]] = []

    def request(endpoint: str, token: str, identity: str) -> tuple[str, int | None]:
        calls.append((endpoint, token, identity))
        error = failures.pop((endpoint, identity), None)
        if error is not None:
            raise error
        if endpoint == "/user":
            return json.dumps({"login": f"{identity}-user"}), None
        return json.dumps({"full_name": "owner/repo"}), None

    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token", _SECOND: "second-token"}),
        default_token="",
        request=request,
        active_cooldowns={_FIRST: 100.0, _SECOND: 100.0},
        on_rate_limit=Mock(),
    )

    now[0] = 101.0
    with pytest.raises(read_token_pool._ReadTokenPoolDeadlineExceeded):
        pool.candidate_names

    fresh_deadline = pool._cooldown_deadlines[_SECOND]
    assert fresh_deadline > now[0]
    assert pool._cooldown_deadlines[_FIRST] == 100.0
    assert calls.count(("/repos/owner/repo", "second-token", _SECOND)) == 1

    now[0] = 102.0
    assert pool.candidate_names == (_FIRST,)

    assert pool._cooldown_deadlines[_SECOND] == fresh_deadline
    assert calls.count(("/repos/owner/repo", "second-token", _SECOND)) == 1
    assert ("/user", "first-token", _FIRST) in calls
    assert ("/repos/owner/repo", "first-token", _FIRST) in calls
