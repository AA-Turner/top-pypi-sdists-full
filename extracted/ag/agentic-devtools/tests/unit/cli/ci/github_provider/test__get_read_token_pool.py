"""Tests for github_provider._get_read_token_pool()."""

from __future__ import annotations

import json
from collections import deque
from types import SimpleNamespace
from typing import Any
from unittest.mock import patch

import pytest

import agentic_devtools.cli.ci.credential_roles as credential_roles
import agentic_devtools.cli.ci.github_provider as github_provider
import agentic_devtools.cli.ci.read_token_pool as read_token_pool
import agentic_devtools.cli.ci.read_token_pool_execution as execution
from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError

_DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
_TEAM = "TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_OTHER = "OTHER_SWICA_CLASSIC_REPO_WORKFLOW_PAT"


@pytest.fixture(autouse=True)
def isolated_retained_cooldowns(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "AI_PR_LOOP_CREDENTIAL_IDENTITY",
        credential_roles.AI_PR_LOOP_BOOKKEEPING_TOKEN,
        credential_roles.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT,
        credential_roles.COPILOT_GITHUB_TOKEN,
        credential_roles.LEGACY_SPECKIT_PR_TOKEN,
        credential_roles.AGDT_PR_APPROVER_PAT,
        credential_roles.REPO_VARIABLE_WRITER_PAT,
        credential_roles.GH_TOKEN,
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(execution, "_RETAINED_RATE_LIMITS", {})
    monkeypatch.setattr(execution, "_DEFERRED_RATE_LIMIT_PERSISTENCE", deque())


@pytest.fixture
def interrupted_cold_build(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))
    monkeypatch.delenv(_DEFAULT, raising=False)
    now = [100.0]
    tick = [0.0]
    calls: list[tuple[str, str]] = []
    monkeypatch.setattr(execution.time, "time", lambda: now[0])
    monkeypatch.setattr("agentic_devtools.cli.ci.cooldown.read_cooldowns", lambda *_args, **_kwargs: {})

    def gh_api(endpoint: str, **kwargs: Any) -> str:
        identity = kwargs["credential_identity"]
        calls.append((endpoint, identity))
        if identity == _TEAM and now[0] == 100.0:
            tick[0] = 1.0
            raise RetryableError("rate limited", retry_after=30, is_rate_limit=True)
        return json.dumps({"login": identity}) if endpoint == "/user" else "{}"

    monkeypatch.setattr(github_provider, "_gh_api", gh_api)
    with pytest.raises(github_provider._InventoryDeadlineExceeded):
        github_provider._get_read_token_pool(deadline=1.0, monotonic=lambda: tick[0])
    assert github_provider._READ_TOKEN_POOL is None
    now[0] = 101.0
    tick[0] = 0.0
    calls.clear()
    return SimpleNamespace(now=now, calls=calls)


def test_interrupted_cold_build_retains_original_cooldown_until_expiry(
    monkeypatch: pytest.MonkeyPatch, interrupted_cold_build: SimpleNamespace, caplog: pytest.LogCaptureFixture
) -> None:
    state = interrupted_cold_build
    retained = execution._RETAINED_RATE_LIMITS
    assert retained == {("owner/repo", _TEAM): 140.0}
    pool = github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.candidate_names == ()
    assert state.calls == []
    assert retained[("owner/repo", _TEAM)] == 140.0

    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    with (
        patch(
            "agentic_devtools.cli.ci.cooldown.read_cooldowns",
            return_value={f"github:{_TEAM}": CooldownRecord(resume_at=160.0)},
        ),
        patch.object(github_provider, "ReadTokenPool", wraps=read_token_pool.ReadTokenPool) as build,
    ):
        github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert build.call_args.kwargs["active_cooldowns"][_TEAM] == 160.0
    assert retained[("owner/repo", _TEAM)] == 140.0

    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    state.now[0] = 140.0
    pool = github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.candidate_names == (_TEAM,)
    assert state.calls == [("/user", _TEAM), ("/repos/owner/repo", _TEAM)]
    assert retained == {}
    assert "team-token" not in caplog.text


def test_interrupted_cold_build_does_not_suppress_another_repository(
    monkeypatch: pytest.MonkeyPatch, interrupted_cold_build: SimpleNamespace
) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/other")
    pool = github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.candidate_names == (_TEAM,)
    assert interrupted_cold_build.calls == [("/user", _TEAM), ("/repos/owner/other", _TEAM)]
    assert execution._RETAINED_RATE_LIMITS == {("owner/repo", _TEAM): 140.0}


def test_interrupted_cold_build_does_not_suppress_another_credential(
    monkeypatch: pytest.MonkeyPatch, interrupted_cold_build: SimpleNamespace
) -> None:
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_OTHER: "other-token"}))
    pool = github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.candidate_names == (_OTHER,)
    assert interrupted_cold_build.calls == [("/user", _OTHER), ("/repos/owner/repo", _OTHER)]
    assert execution._RETAINED_RATE_LIMITS == {("owner/repo", _TEAM): 140.0}


def test_rate_limited_bootstrap_lookup_keeps_distinct_retained_identity(
    interrupted_cold_build: SimpleNamespace,
) -> None:
    limited = ProviderRateLimitError(
        provider="github", credential_identity=_OTHER, retry_after_seconds=30, is_rate_limit=True
    )
    with (
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", side_effect=limited),
        patch.object(github_provider, "ReadTokenPool", wraps=read_token_pool.ReadTokenPool) as build,
    ):
        pool = github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: 0.0)
    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert build.call_args.kwargs["active_cooldowns"][_TEAM] == 140.0
    assert pool.candidate_names == ()
    assert interrupted_cold_build.calls == []


@pytest.mark.parametrize(
    ("repo", "secrets_json"),
    [
        ("", '{"TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT":"team-token"}'),
        ("owner/repo", ""),
    ],
)
def test_returns_none_when_repository_or_secret_json_is_missing(
    monkeypatch: pytest.MonkeyPatch,
    repo: str,
    secrets_json: str,
) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", repo)
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", secrets_json)

    assert github_provider._get_read_token_pool() is None


def test_builds_caches_and_rebuilds_pool_while_persisting_cooldowns(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv(
        "AGDT_GITHUB_SECRETS_JSON",
        json.dumps({_TEAM: "team-token", _OTHER: "other-token"}),
    )
    monkeypatch.setenv(_DEFAULT, "default-token")
    monkeypatch.setenv(github_provider.REPO_VARIABLE_WRITER_PAT, "writer-token")

    def gh_api(endpoint: str, **kwargs: object) -> str:
        assert kwargs["read_pool"] is False
        metadata = kwargs["response_metadata"]
        assert isinstance(metadata, dict)
        token = kwargs["token"]
        if endpoint == "/user":
            assert isinstance(token, str)
            logins = {
                "default-token": "default-user",
                "team-token": "team-user",
                "other-token": "other-user",
            }
            metadata["remaining"] = 40
            return json.dumps({"login": logins[token]})
        metadata["remaining"] = "unknown" if token == "other-token" else 20
        return "{}"

    records = {
        f"github:{_TEAM}": CooldownRecord(resume_at=1_800_000_000),
        "azure:ignored": CooldownRecord(resume_at=1_800_000_000),
    }
    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=gh_api),
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", return_value=records) as read_cooldowns,
        patch("agentic_devtools.cli.ci.cooldown.persist_cooldown") as persist_cooldown,
    ):
        pool = github_provider._get_read_token_pool()

        assert isinstance(pool, read_token_pool.ReadTokenPool)
        assert pool.candidate_names == (_OTHER,)
        assert pool.has_available_credentials
        assert github_provider._get_read_token_pool() is pool
        read_cooldowns.assert_called_once()
        assert read_cooldowns.call_args.kwargs["use_writer_token"] is True

        error = RetryableError("rate limited", is_rate_limit=True)
        pool.mark_rate_limited(_OTHER, error)

        persisted = persist_cooldown.call_args.args[1]
        assert persisted.credential_identity == _OTHER
        assert persisted.provider == "github"
        assert github_provider._READ_POOL_BYPASS.get() is False

        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/other-repo")
        monkeypatch.delenv(github_provider.REPO_VARIABLE_WRITER_PAT)
        rebuilt = github_provider._get_read_token_pool()

    assert rebuilt is not pool
    assert read_cooldowns.call_count == 2
    assert read_cooldowns.call_args.kwargs["use_writer_token"] is False


def test_expired_pool_rebuild_keeps_the_previous_repository_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo-a")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))

    def gh_api(endpoint: str, **kwargs: object) -> str:
        if endpoint == "/user":
            return json.dumps({"login": "team-user"})
        return "{}"

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=gh_api),
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", return_value={}),
    ):
        cached = github_provider._get_read_token_pool()
        assert isinstance(cached, read_token_pool.ReadTokenPool)
        assert cached.repo == "owner/repo-a"

        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo-b")
        now = [0.0]

        class ExpireAfterBuild(read_token_pool.ReadTokenPool):
            def __init__(self, **kwargs: Any) -> None:
                super().__init__(**kwargs)
                now[0] = 1.0

        monkeypatch.setattr(github_provider, "ReadTokenPool", ExpireAfterBuild)
        with pytest.raises(github_provider._InventoryDeadlineExceeded):
            github_provider._get_read_token_pool(deadline=1.0, monotonic=lambda: now[0])

        assert github_provider._READ_TOKEN_POOL is cached
        assert github_provider._READ_TOKEN_POOL_REPO == "owner/repo-a"
        monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo-a")
        assert github_provider._get_read_token_pool(deadline=2.0, monotonic=lambda: now[0]) is cached
        assert cached.candidate_names == (_TEAM,)


def test_cooldown_bootstrap_rate_limit_persists_default_and_skips_unverified_alternates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    monkeypatch.delenv(github_provider.REPO_VARIABLE_WRITER_PAT, raising=False)
    limited = ProviderRateLimitError(
        provider="github",
        credential_identity=_DEFAULT,
        source="retry-after",
        is_rate_limit=True,
    )
    calls: list[tuple[str, str, str]] = []

    def gh_api(endpoint: str, **kwargs: object) -> str:
        token = kwargs["token"]
        identity = kwargs["credential_identity"]
        assert isinstance(token, str)
        assert isinstance(identity, str)
        calls.append((endpoint, token, identity))
        if endpoint == "/user":
            return json.dumps({"login": "team-user"})
        return "{}"

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=gh_api),
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", side_effect=limited) as read_cooldowns,
        patch("agentic_devtools.cli.ci.cooldown.persist_cooldown") as persist_cooldown,
    ):
        pool = github_provider._get_read_token_pool()

    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.default_is_active
    assert pool.candidate_names == ()
    assert not any(token == "default-token" for _, token, _ in calls)
    assert not any(identity == _TEAM for _, _, identity in calls)
    read_cooldowns.assert_called_once()
    assert read_cooldowns.call_args.kwargs["use_writer_token"] is False
    persist_cooldown.assert_called_once()


def test_non_rate_limit_cooldown_lookup_error_propagates(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    error = ProviderRateLimitError(provider="github", is_rate_limit=False)

    with (
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", side_effect=error),
        pytest.raises(ProviderRateLimitError) as raised,
    ):
        github_provider._get_read_token_pool()

    assert raised.value is error


def test_deadline_bounds_cold_pool_initialization(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token", _OTHER: "other-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    now = [0.0]
    result = SimpleNamespace(returncode=0, stdout='HTTP/1.1 200 OK\n\n{"login":"default-user"}', stderr="")

    def run_safe(*_args: object, **_kwargs: object) -> object:
        now[0] = 10.0
        return result

    with (
        patch("agentic_devtools.cli.ci.cooldown.read_cooldowns", return_value={}),
        patch("agentic_devtools.cli.ci.github_provider._gh_api", wraps=github_provider._gh_api) as gh_api,
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as runner,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        github_provider._get_read_token_pool(deadline=10.0, monotonic=lambda: now[0])

    runner.assert_called_once()
    assert [call.kwargs["credential_identity"] for call in gh_api.call_args_list] == [_DEFAULT, _OTHER]


def test_deadline_bounds_real_cooldown_lookup_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", "{}")
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", _DEFAULT)
    now = [0.0]
    result = SimpleNamespace(
        returncode=1,
        stdout="HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n",
        stderr="",
    )
    sleeps: list[float] = []

    def run_safe(*_args: object, **_kwargs: object) -> object:
        return result

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        now[0] += seconds

    with (
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as runner,
        patch("agentic_devtools.cli.ci.retry.time.sleep", side_effect=sleep),
    ):
        pool = github_provider._get_read_token_pool(deadline=1.0, monotonic=lambda: now[0])

    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert pool.default_is_active
    runner.assert_called_once()
    assert runner.call_args.kwargs["timeout"] == 1
    assert sleeps == []
    assert now[0] == 0.0


def test_deadline_free_cooldown_lookup_keeps_retry_behavior(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", "{}")
    limited = SimpleNamespace(
        returncode=1,
        stdout="HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n",
        stderr="",
    )
    success = SimpleNamespace(returncode=0, stdout='{"value":"{}"}', stderr="")
    with (
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=[limited, success]) as runner,
        patch("agentic_devtools.cli.ci.retry.time.sleep") as sleep,
        patch(
            "agentic_devtools.cli.ci.cooldown.persist_cooldown",
            return_value=("github:DEFAULT", CooldownRecord(resume_at=100.0)),
        ),
    ):
        pool = github_provider._get_read_token_pool()

    assert isinstance(pool, read_token_pool.ReadTokenPool)
    assert runner.call_count == 2
    sleep.assert_called_once_with(45)


def test_cached_candidate_revalidation_recovers_after_deadline_interruption(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token", _OTHER: "other-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    interrupted = [True]
    calls: list[tuple[str, str]] = []

    def gh_api(endpoint: str, **kwargs: object) -> str:
        identity = kwargs["credential_identity"]
        token = kwargs["token"]
        assert isinstance(identity, str)
        assert isinstance(token, str)
        calls.append((endpoint, identity))
        if endpoint == "/user" and identity == _TEAM and interrupted[0]:
            interrupted[0] = False
            raise github_provider._InventoryDeadlineExceeded("deadline expired")
        if endpoint == "/user":
            return json.dumps({"login": f"{identity}-user"})
        return "{}"

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=gh_api),
        patch(
            "agentic_devtools.cli.ci.cooldown.read_cooldowns",
            return_value={f"github:{_TEAM}": CooldownRecord(resume_at=100.0)},
        ),
    ):
        pool = github_provider._get_read_token_pool()
        assert isinstance(pool, read_token_pool.ReadTokenPool)
        assert pool.candidate_names == (_OTHER,)

        now[0] = 101.0
        with (
            execution.ReadTokenPoolOperations.request_context(200.0, lambda: now[0]),
            pytest.raises(github_provider._InventoryDeadlineExceeded),
        ):
            pool.candidate_names

        now[0] = 102.0
        with execution.ReadTokenPoolOperations.request_context(300.0, lambda: now[0]):
            names = pool.candidate_names

    assert names == tuple(sorted((_TEAM, _OTHER)))
    assert pool.recognizes_token("team-token")
    assert calls.count(("/user", _TEAM)) == 2
    assert ("/repos/owner/repo", _TEAM) in calls
