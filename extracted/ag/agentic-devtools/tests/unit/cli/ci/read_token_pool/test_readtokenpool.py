"""Tests for per-run GitHub read-token discovery and selection."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.read_token_pool as read_token_pool
from agentic_devtools.cli.ci.retry import RetryableError

_DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
_FIRST = "NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_SECOND = "CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_SAME_IDENTITY = "AMARSNIK_SWICA_CLASSIC_REPO_WORKFLOW_PAT"


def _responses(
    users: dict[str, str],
    *,
    remaining: dict[tuple[str, str], int | None] | None = None,
    failures: dict[tuple[str, str], Exception] | None = None,
) -> tuple[Callable[[str, str, str], tuple[str, int | None]], list[tuple[str, str, str]]]:
    calls: list[tuple[str, str, str]] = []
    remaining = remaining or {}
    failures = failures or {}

    def request(endpoint: str, token: str, identity: str) -> tuple[str, int | None]:
        calls.append((endpoint, token, identity))
        failure = failures.get((endpoint, identity))
        if failure is not None:
            raise failure
        if endpoint == "/user":
            return json.dumps({"login": users[identity]}), remaining.get((identity, "rest"))
        return json.dumps({"full_name": "owner/repo"}), remaining.get((identity, "rest"))

    return request, calls


def _make_pool(
    users: dict[str, str],
    *,
    secrets: dict[str, str] | None = None,
    default_token: str = "default-token",
    active_cooldowns: set[str] | dict[str, float] | None = None,
    remaining: dict[tuple[str, str], int | None] | None = None,
    failures: dict[tuple[str, str], Exception] | None = None,
    on_rate_limit: Mock | None = None,
) -> tuple[read_token_pool.ReadTokenPool, list[tuple[str, str, str]], Mock]:
    request, calls = _responses(users, remaining=remaining, failures=failures)
    persist = on_rate_limit or Mock()
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps(secrets or {_FIRST: "first-token", _SECOND: "second-token"}),
        default_token=default_token,
        default_identity=_DEFAULT,
        request=request,
        active_cooldowns=active_cooldowns or set(),
        on_rate_limit=persist,
    )
    return pool, calls, persist


def test_discovers_validates_and_deduplicates_candidates_by_login() -> None:
    users = {
        _DEFAULT: "default-user",
        _FIRST: "pool-user",
        _SECOND: "POOL-USER",
        _SAME_IDENTITY: "DEFAULT-USER",
    }
    secrets = {
        _FIRST: "first-token",
        _SECOND: "second-token",
        _SAME_IDENTITY: "same-user-token",
        "NOT_A_POOL_SECRET": "ignored-token",
        "EMPTY_SWICA_CLASSIC_REPO_WORKFLOW_PAT": " ",
    }

    pool, calls, _ = _make_pool(users, secrets=secrets)

    assert pool.candidate_names == (_SECOND,)
    assert calls.count(("/user", "first-token", _FIRST)) == 1
    assert calls.count(("/user", "second-token", _SECOND)) == 1
    assert calls.count(("/user", "same-user-token", _SAME_IDENTITY)) == 1
    assert ("/repos/owner/repo", "second-token", _SECOND) in calls
    assert not any(endpoint == "/repos/owner/repo" and identity != _SECOND for endpoint, _, identity in calls)


@pytest.mark.parametrize("secrets_json", ["", "not-json", "[]", '{"x": 5}'])
def test_ignores_missing_or_malformed_secrets_json(secrets_json: str, caplog: pytest.LogCaptureFixture) -> None:
    request, calls = _responses({_DEFAULT: "default-user"})

    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=secrets_json,
            default_token="default-token",
            default_identity=_DEFAULT,
            request=request,
            active_cooldowns=set(),
            on_rate_limit=Mock(),
        )

    assert pool.candidate_names == ()
    assert not calls
    assert "default-token" not in caplog.text


def test_excludes_candidates_with_invalid_login_or_failed_validation(caplog: pytest.LogCaptureFixture) -> None:
    users = {_DEFAULT: "default-user", _FIRST: "pool-user", _SECOND: "pool-user-2"}
    request, calls = _responses(
        users,
        failures={
            ("/user", _FIRST): RuntimeError("HTTP 401"),
            ("/repos/owner/repo", _SECOND): RuntimeError("HTTP 404"),
        },
    )
    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token", _SECOND: "second-token"}),
            default_token="default-token",
            default_identity=_DEFAULT,
            request=request,
            active_cooldowns=set(),
            on_rate_limit=Mock(),
        )

    assert pool.candidate_names == ()
    assert "NOEKVIST_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT" in caplog.text
    assert "CTRUX_EXT_SWICA_CLASSIC_REPO_WORKFLOW_PAT" in caplog.text
    assert "first-token" not in caplog.text
    assert "second-token" not in caplog.text
    assert not any(endpoint == "/repos/owner/repo" and identity == _FIRST for endpoint, _, identity in calls)


def test_rate_limited_validation_persists_cooldown_without_logging_token(caplog: pytest.LogCaptureFixture) -> None:
    limited = RetryableError(
        "rate limited",
        provider="github",
        credential_identity=_FIRST,
        is_rate_limit=True,
    )
    request, _ = _responses(
        {_DEFAULT: "default-user", _FIRST: "pool-user"},
        failures={("/repos/owner/repo", _FIRST): limited},
    )
    persist = Mock()

    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token"}),
            default_token="default-token",
            default_identity=_DEFAULT,
            request=request,
            active_cooldowns=set(),
            on_rate_limit=persist,
        )

    persist.assert_called_once_with(_FIRST, limited)
    assert pool.candidate_names == ()
    assert "first-token" not in caplog.text


def test_rate_limited_repository_validation_reserves_duplicate_login() -> None:
    limited = RetryableError(
        "rate limited",
        provider="github",
        credential_identity=_SECOND,
        is_rate_limit=True,
    )
    request, calls = _responses(
        {_DEFAULT: "default-user", _SECOND: "shared-user", _FIRST: "SHARED-USER"},
        failures={("/repos/owner/repo", _SECOND): limited},
    )
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_SECOND: "first-token", _FIRST: "second-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        on_rate_limit=Mock(),
    )

    assert pool.candidate_names == ()
    assert ("/repos/owner/repo", "first-token", _SECOND) in calls
    assert not any(endpoint == "/repos/owner/repo" and identity == _FIRST for endpoint, _, identity in calls)


def test_non_rate_limited_repository_failure_allows_duplicate_login_retry() -> None:
    request, calls = _responses(
        {_DEFAULT: "default-user", _SECOND: "shared-user", _FIRST: "SHARED-USER"},
        failures={("/repos/owner/repo", _SECOND): RuntimeError("HTTP 404")},
    )
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_SECOND: "first-token", _FIRST: "second-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        on_rate_limit=Mock(),
    )

    assert pool.candidate_names == (_FIRST,)
    assert ("/repos/owner/repo", "first-token", _SECOND) in calls
    assert ("/repos/owner/repo", "second-token", _FIRST) in calls


@pytest.mark.parametrize("is_rate_limit", [True, False])
def test_rate_limited_identity_lookup_is_recorded_and_excluded(is_rate_limit: bool) -> None:
    limited = RetryableError(
        "identity lookup failed",
        provider="github",
        credential_identity=_FIRST,
        is_rate_limit=is_rate_limit,
    )
    request, calls = _responses(
        {_DEFAULT: "default-user"},
        failures={("/user", _FIRST): limited},
    )
    persist = Mock()

    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        active_cooldowns=set(),
        on_rate_limit=persist,
    )

    assert pool.candidate_names == ()
    assert not any(endpoint == "/repos/owner/repo" for endpoint, _, _ in calls)
    if is_rate_limit:
        persist.assert_called_once_with(_FIRST, limited)
    else:
        persist.assert_not_called()


def test_default_identity_rate_limit_blocks_unverified_pool_candidates() -> None:
    limited = RetryableError(
        "rate limited",
        provider="github",
        credential_identity=_DEFAULT,
        is_rate_limit=True,
    )
    request, calls = _responses(
        {_DEFAULT: "default-user", _FIRST: "pool-user"},
        failures={("/user", _DEFAULT): limited},
    )
    persist = Mock()

    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        on_rate_limit=persist,
    )

    assert pool.candidate_names == ()
    assert not any(endpoint == "/repos/owner/repo" and identity == _FIRST for endpoint, _, identity in calls)
    persist.assert_called_once_with(_DEFAULT, limited)


def test_missing_default_token_still_validates_pool_candidates() -> None:
    pool, calls, _ = _make_pool(
        {_FIRST: "pool-user"},
        default_token="",
        secrets={_FIRST: "first-token"},
    )

    assert pool.candidate_names == (_FIRST,)
    assert not any(identity == _DEFAULT for _, _, identity in calls)


def test_invalid_default_identity_is_warned_and_blocks_unverified_candidates(caplog) -> None:
    request, calls = _responses(
        {_DEFAULT: "default-user", _FIRST: "pool-user"},
        failures={("/user", _DEFAULT): RuntimeError("HTTP 401")},
    )

    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token"}),
            default_token="default-token",
            default_identity=_DEFAULT,
            request=request,
            active_cooldowns=set(),
            on_rate_limit=Mock(),
        )

    assert pool.candidate_names == ()
    assert not any(endpoint == "/repos/owner/repo" and identity == _FIRST for endpoint, _, identity in calls)
    assert "default-token" not in caplog.text
    assert _DEFAULT in caplog.text


def test_reuses_cached_login_when_default_and_candidate_share_token() -> None:
    pool, calls, _ = _make_pool(
        {_DEFAULT: "same-user", _FIRST: "same-user"},
        default_token="first-token",
        secrets={_FIRST: "first-token"},
    )

    assert pool.candidate_names == ()
    assert calls.count(("/user", "first-token", _DEFAULT)) == 1
    assert not any(endpoint == "/user" and identity == _FIRST for endpoint, _, identity in calls)


def test_selects_highest_resource_budget_and_rotates_ties_independently() -> None:
    users = {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"}
    pool, _, _ = _make_pool(users, remaining={(_FIRST, "rest"): 9, (_SECOND, "rest"): 9})

    first_rest = pool.select("rest")
    first_graphql = pool.select("graphql")
    second_rest = pool.select("rest")
    second_graphql = pool.select("graphql")
    third_graphql = pool.select("graphql")

    assert first_rest is not None and second_rest is not None
    assert first_graphql is not None and second_graphql is not None and third_graphql is not None
    assert (first_rest.secret_name, second_rest.secret_name) == (_SECOND, _FIRST)
    assert (first_graphql.secret_name, second_graphql.secret_name, third_graphql.secret_name) == (
        _SECOND,
        _FIRST,
        _SECOND,
    )

    pool.record_remaining(_FIRST, "graphql", 5)
    pool.record_remaining(_SECOND, "graphql", 2)
    pool.record_remaining(_SECOND, "rest", 1)
    pool.record_remaining(_FIRST, "rest", None)

    best_graphql = pool.select("graphql")
    best_rest = pool.select("rest")
    assert best_graphql is not None and best_rest is not None
    assert best_graphql.secret_name == _FIRST
    assert best_rest.secret_name == _FIRST


def test_samples_untried_graphql_budget_before_ranking_known_budgets() -> None:
    users = {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"}
    pool, _, _ = _make_pool(users)

    first = pool.select("graphql")
    assert first is not None
    pool.record_remaining(first.secret_name, "graphql", 10)

    second = pool.select("graphql")
    assert second is not None
    assert second.secret_name != first.secret_name

    highest = pool.select("graphql")
    assert highest is not None
    assert highest.secret_name == first.secret_name


def test_filters_active_cooldowns_and_returns_none_when_all_candidates_are_cooling() -> None:
    users = {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"}
    pool, _, _ = _make_pool(users, active_cooldowns={_FIRST})

    remaining = pool.select("rest")
    assert remaining is not None
    assert remaining.secret_name == _SECOND

    fully_cooled, _, _ = _make_pool(users, active_cooldowns={_FIRST, _SECOND})
    assert fully_cooled.select("rest") is None
    assert fully_cooled.blocking_cooldown_identities == ()
    assert pool.blocking_cooldown_identities == ()


def test_default_cooldown_blocks_scheduling_even_with_available_alternates() -> None:
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user"},
        active_cooldowns={_DEFAULT},
    )

    assert pool.has_available_credentials is False
    assert pool.blocking_cooldown_identities == (_DEFAULT,)
    assert not any(endpoint == "/user" and identity == _DEFAULT for endpoint, _, identity in calls)
    assert not any(identity == _FIRST for _, _, identity in calls)


def test_rejects_default_token_alias_without_discovery_even_during_default_cooldown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(read_token_pool.time, "time", lambda: 99.0)
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "default-user"},
        secrets={_FIRST: "default-token"},
        active_cooldowns={_DEFAULT: 100.0},
    )

    assert pool.candidate_names == ()
    assert calls == []


def test_ignores_invalid_cooldown_names_and_deadlines() -> None:
    request, calls = _responses({_DEFAULT: "default-user"})
    active_cooldowns = {None: 100.0, _FIRST: float("nan")}
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token"}),
        request=request,
        active_cooldowns=active_cooldowns,  # type: ignore[arg-type]
        on_rate_limit=Mock(),
    )

    assert pool.candidate_names == ()
    assert calls == []


def test_revalidates_pool_candidate_after_its_cooldown_expires(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"},
        active_cooldowns={_FIRST: 100.0},
    )

    assert pool.candidate_names == (_SECOND,)
    assert not any(identity == _FIRST for _, _, identity in calls)

    now[0] = 101.0
    assert pool.candidate_names == (_SECOND, _FIRST)
    assert ("/user", "first-token", _FIRST) in calls
    assert ("/repos/owner/repo", "first-token", _FIRST) in calls


def test_reuses_cached_login_when_two_secrets_share_a_token() -> None:
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "shared-user", _SECOND: "shared-user"},
        secrets={_FIRST: "shared-token", _SECOND: "shared-token"},
    )

    assert pool.candidate_names == (_SECOND,)
    assert calls.count(("/user", "shared-token", _SECOND)) == 1
    assert not any(endpoint == "/user" and identity == _FIRST for endpoint, _, identity in calls)


def test_resolves_default_and_discovers_candidates_after_default_cooldown_expires(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user"},
        active_cooldowns={_DEFAULT: 100.0},
    )

    assert pool.candidate_names == ()
    assert not calls
    assert pool.default_is_active is True

    now[0] = 101.0
    assert pool.candidate_names == (_FIRST,)
    assert pool.default_is_active is False
    assert ("/user", "default-token", _DEFAULT) in calls
    assert ("/repos/owner/repo", "first-token", _FIRST) in calls


def test_expires_a_current_run_rate_limit_using_persisted_deadline(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    persist = Mock(return_value=100.0)
    pool, _, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user"},
        on_rate_limit=persist,
    )
    error = RetryableError("limited", credential_identity=_FIRST, is_rate_limit=True)

    pool.mark_rate_limited(_FIRST, error)
    assert pool.select("rest") is None

    now[0] = 101.0
    selected = pool.select("rest")
    assert selected is not None and selected.secret_name == _FIRST


def test_tracks_current_run_cooldown_when_persistence_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(read_token_pool.time, "time", lambda: 1000.0)
    limited = RetryableError(
        "rate limited",
        retry_after=20,
        provider="github",
        credential_identity=_DEFAULT,
        source="retry-after",
        is_rate_limit=True,
    )
    request, _ = _responses(
        {},
        failures={("/user", _DEFAULT): limited},
    )
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        on_rate_limit=Mock(return_value=None),
    )

    assert pool.blocking_cooldown_identities == (_DEFAULT,)
    assert pool.active_cooldown_for((_DEFAULT,), now=1000.0) == (
        f"github:{_DEFAULT}",
        read_token_pool.CooldownRecord(resume_at=1030.0, source="retry-after", updated_at=1000.0),
    )


def test_reselects_expired_reader_after_clearing_its_cached_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    now = [99.0]
    monkeypatch.setattr(read_token_pool.time, "time", lambda: now[0])
    persist = Mock(return_value=100.0)
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"},
        remaining={(_FIRST, "rest"): 0, (_SECOND, "rest"): 100},
        on_rate_limit=persist,
    )
    initial_call_count = len(calls)
    error = RetryableError("limited", credential_identity=_FIRST, is_rate_limit=True)

    assert pool.candidate_names == tuple(sorted((_FIRST, _SECOND)))
    pool.mark_rate_limited(_FIRST, error)
    selected_while_cooling = pool.select("rest")
    assert selected_while_cooling is not None and selected_while_cooling.secret_name == _SECOND

    now[0] = 101.0
    selected = pool.select("rest")

    assert selected is not None and selected.secret_name == _FIRST
    assert len(calls) == initial_call_count


def test_skips_candidate_discovery_for_identities_already_cooling() -> None:
    pool, calls, _ = _make_pool(
        {_DEFAULT: "default-user", _FIRST: "first-user", _SECOND: "second-user"},
        active_cooldowns={_FIRST},
    )

    assert pool.candidate_names == (_SECOND,)
    assert not any(identity == _FIRST for _, _, identity in calls)


def test_cooling_pool_identities_block_when_default_token_is_unavailable() -> None:
    pool, calls, _ = _make_pool(
        {},
        default_token="",
        active_cooldowns={_FIRST, _SECOND},
    )

    assert pool.candidate_names == ()
    assert not calls
    assert pool.blocking_cooldown_identities == (_SECOND, _FIRST)


def test_available_pool_identity_prevents_cooldown_pause_without_default_token() -> None:
    pool, _, _ = _make_pool(
        {_FIRST: "first-user", _SECOND: "second-user"},
        default_token="",
        active_cooldowns={_FIRST},
    )

    assert pool.blocking_cooldown_identities == ()


def test_unvalidated_login_does_not_reserve_identity_against_later_candidate() -> None:
    request, calls = _responses(
        {_DEFAULT: "default-user", _FIRST: "shared-user", _SECOND: "shared-user"},
        failures={("/repos/owner/repo", _SECOND): RuntimeError("HTTP 404")},
    )
    pool = read_token_pool.ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({_FIRST: "first-token", _SECOND: "second-token"}),
        default_token="default-token",
        default_identity=_DEFAULT,
        request=request,
        active_cooldowns=set(),
        on_rate_limit=Mock(),
    )

    assert pool.candidate_names == (_FIRST,)
    assert ("/repos/owner/repo", "first-token", _FIRST) in calls


def test_rate_limit_marks_identity_unavailable_and_persists_it() -> None:
    pool, _, persist = _make_pool({_DEFAULT: "default-user", _FIRST: "first-user"})
    error = RetryableError("limited", provider="github", credential_identity=_FIRST, is_rate_limit=True)

    pool.mark_rate_limited(_FIRST, error)

    assert pool.select("rest") is None
    persist.assert_called_once_with(_FIRST, error)


def test_invalid_resources_are_rejected() -> None:
    pool, _, _ = _make_pool({_DEFAULT: "default-user", _FIRST: "first-user"})

    with pytest.raises(ValueError, match="resource"):
        pool.select("search")

    with pytest.raises(ValueError, match="resource"):
        pool.record_remaining(_FIRST, "search", 3)


@pytest.mark.parametrize(
    ("repo", "default_identity", "message"),
    [
        ("", _DEFAULT, "repo"),
        ("owner", _DEFAULT, "repo"),
        ("owner/", _DEFAULT, "repo"),
        ("owner/repo/extra", _DEFAULT, "repo"),
        ("owner/repo", "", "default_identity"),
    ],
)
def test_rejects_invalid_repository_or_default_identity(repo: str, default_identity: str, message: str) -> None:
    request, _ = _responses({})
    with pytest.raises(ValueError, match=message):
        read_token_pool.ReadTokenPool(
            repo=repo,
            secrets_json=None,
            default_identity=default_identity,
            request=request,
            on_rate_limit=Mock(),
        )


def test_recognizes_only_validated_alternate_tokens() -> None:
    pool, _, _ = _make_pool({_DEFAULT: "default-user", _FIRST: "first-user"})

    assert pool.recognizes_token("first-token") is True
    assert pool.recognizes_token("unknown-token") is False
    assert pool.recognizes_token(None) is False


@pytest.mark.parametrize("remaining", ["3", True, -1])
def test_ignores_invalid_remaining_counts(remaining: object) -> None:
    pool, _, _ = _make_pool({_DEFAULT: "default-user", _FIRST: "first-user"})

    pool.record_remaining(_FIRST, "rest", remaining)  # type: ignore[arg-type]

    assert pool.select("rest") is not None


@pytest.mark.parametrize(
    "response",
    ["not-json", "[]", '{"login": 123}', '{"login": "  "}'],
)
def test_excludes_candidates_with_invalid_identity_responses(response: str, caplog: pytest.LogCaptureFixture) -> None:
    def request(endpoint: str, _token: str, _identity: str) -> tuple[str, int | None]:
        return (response if endpoint == "/user" else "{}", None)

    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token"}),
            default_token="",
            default_identity=_DEFAULT,
            request=request,
            on_rate_limit=Mock(),
        )

    assert pool.candidate_names == ()
    assert _FIRST in caplog.text
    assert "first-token" not in caplog.text


@pytest.mark.parametrize("identity", [_DEFAULT, _FIRST])
def test_non_rate_retryable_validation_failure_warns_and_excludes_identity(
    identity: str,
    caplog: pytest.LogCaptureFixture,
) -> None:
    error = RetryableError("temporary failure", is_rate_limit=False)
    endpoint = "/user" if identity == _DEFAULT else "/repos/owner/repo"
    request, calls = _responses(
        {_DEFAULT: "default-user", _FIRST: "pool-user"},
        failures={(endpoint, identity): error},
    )

    with caplog.at_level(logging.WARNING):
        pool = read_token_pool.ReadTokenPool(
            repo="owner/repo",
            secrets_json=json.dumps({_FIRST: "first-token"}),
            default_token="default-token",
            default_identity=_DEFAULT,
            request=request,
            on_rate_limit=Mock(),
        )

    if identity == _DEFAULT:
        assert pool.candidate_names == ()
        assert not any(endpoint == "/repos/owner/repo" for endpoint, _, _ in calls)
    else:
        assert pool.candidate_names == ()
    assert identity in caplog.text


def test_next_tied_returns_first_entry_when_pool_order_has_no_match() -> None:
    pool, _, _ = _make_pool({_DEFAULT: "default-user"})
    expected = read_token_pool.ReadCredential(_FIRST, "first-token", "first-user")

    assert pool._next_tied("rest", [expected]) == expected
