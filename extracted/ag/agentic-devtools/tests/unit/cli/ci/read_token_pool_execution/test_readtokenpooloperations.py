"""Tests for deadline-aware read-token pool operations."""

import json
from contextvars import ContextVar
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.read_token_pool import ReadCredential, ReadTokenPool, _ReadTokenPoolDeadlineExceeded
from agentic_devtools.cli.ci.read_token_pool_execution import ReadTokenPoolOperations, ReadTokenPoolRateLimits
from agentic_devtools.cli.ci.retry import ProviderRateLimitError, RetryableError


def test_deadline_helpers_preserve_legacy_timeout_and_floor_remaining_time() -> None:
    assert ReadTokenPoolOperations.remaining_seconds(None, None) is None
    assert ReadTokenPoolOperations.request_timeout(60, None, None) == 60
    assert ReadTokenPoolOperations.remaining_seconds(10.5, lambda: 0.0) == 10.5
    assert ReadTokenPoolOperations.request_timeout(60, 10.5, lambda: 0.0) == 10
    assert ReadTokenPoolOperations.request_timeout(3, 10.5, lambda: 0.0) == 3
    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.remaining_seconds(10, lambda: 10)
    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.request_timeout(60, 0.5, lambda: 0.0)


def test_run_request_preserves_nonexpired_retryable_error() -> None:
    assert ReadTokenPoolOperations.run_request(lambda: "success", deadline=None, monotonic=None) == "success"
    expected = RetryableError("temporary failure", is_rate_limit=False)

    with pytest.raises(RetryableError) as raised_without_deadline:
        ReadTokenPoolOperations.run_request(
            lambda: (_ for _ in ()).throw(expected),
            deadline=None,
            monotonic=None,
        )

    with pytest.raises(RetryableError) as raised:
        ReadTokenPoolOperations.run_request(
            lambda: (_ for _ in ()).throw(expected),
            deadline=10.0,
            monotonic=lambda: 0.0,
        )

    assert raised_without_deadline.value is expected
    assert raised.value is expected


def test_run_request_signals_retryable_error_after_deadline() -> None:
    expected = RetryableError("request timed out", is_rate_limit=False)

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.run_request(
            lambda: (_ for _ in ()).throw(expected),
            deadline=10.0,
            monotonic=lambda: 10.0,
        )


def test_run_uses_direct_operation_without_pool_and_returns_successful_credential() -> None:
    def identity(token: str | None) -> str:
        return "default" if token is None else token

    operation = Mock(return_value=("direct", None))
    assert ReadTokenPoolOperations.run("rest", operation, None, identity) == "direct"
    operation.assert_called_once_with(None, "default")

    credential = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    pool = Mock()
    pool.select.return_value = credential
    operation.reset_mock(return_value=True)
    operation.return_value = ("pooled", 5)
    assert ReadTokenPoolOperations.run("rest", operation, pool, identity) == "pooled"
    operation.assert_called_once_with("alternate-token", "TEAM_PAT")
    pool.record_remaining.assert_called_once_with("TEAM_PAT", "rest", 5)


def test_run_preserves_non_rate_limit_error_from_pool_credential() -> None:
    pool = Mock()
    pool.select.return_value = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    expected = RetryableError("temporary failure", is_rate_limit=False)

    with pytest.raises(RetryableError) as raised:
        ReadTokenPoolOperations.run("rest", lambda *_args: (_ for _ in ()).throw(expected), pool, str)

    assert raised.value is expected
    pool.mark_rate_limited.assert_not_called()


def test_run_reports_pool_exhaustion_without_default_token() -> None:
    credential = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    pool = Mock()
    pool.select.side_effect = [credential, None]
    pool.default_token = ""
    pool.default_identity = "DEFAULT"
    pool.default_is_active = False

    def operation(_token: str | None, identity: str) -> tuple[str, int | None]:
        raise RetryableError(
            "rate limited",
            credential_identity=identity,
            is_rate_limit=True,
        )

    with pytest.raises(ProviderRateLimitError):
        ReadTokenPoolOperations.run("rest", operation, pool, str)

    pool.mark_rate_limited.assert_called_once()
    pool.record_remaining.assert_called_once_with("TEAM_PAT", "rest", None)


def test_run_preserves_active_default_cooldown() -> None:
    pool = Mock()
    pool.select.return_value = None
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT"
    pool.default_is_active = True
    operation = Mock()

    with pytest.raises(ProviderRateLimitError):
        ReadTokenPoolOperations.run("rest", operation, pool, str)

    operation.assert_not_called()


def test_run_stops_default_expiry_revalidation_after_deadline() -> None:
    now = [0.0]
    wall = Mock(side_effect=[100.0, 111.0, 111.0])
    limited = RetryableError("rate limited", credential_identity="DEFAULT", is_rate_limit=True)

    def request(endpoint: str, token: str, identity: str) -> tuple[str, int | None]:
        assert (endpoint, token, identity) == ("/user", "default-token", "DEFAULT")
        assert wall.call_count == 2 and now[0] == 0.0
        now[0] = 11.0
        raise limited

    revalidation = Mock(side_effect=request)
    pool = ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({"TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT": "team-token"}),
        default_token="default-token",
        default_identity="DEFAULT",
        request=revalidation,
        active_cooldowns={"DEFAULT": 110.0, "TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT": 200.0},
        on_rate_limit=Mock(return_value=None),
    )
    operation = Mock()
    with patch("agentic_devtools.cli.ci.read_token_pool.time.time", wall):
        with pytest.raises(_ReadTokenPoolDeadlineExceeded) as raised:
            ReadTokenPoolOperations.run(
                "rest",
                operation,
                pool,
                str,
                deadline=10.0,
                monotonic=lambda: now[0],
            )
    assert not isinstance(raised.value, ProviderRateLimitError)
    revalidation.assert_called_once_with("/user", "default-token", "DEFAULT")
    operation.assert_not_called()


def test_run_falls_back_to_default_after_rate_limit() -> None:
    credential = ReadCredential("TEAM_PAT", "alternate-token", "team-user")
    pool = Mock()
    pool.select.side_effect = [credential, None]
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT"
    pool.default_is_active = False
    operation = Mock(
        side_effect=[
            RetryableError("rate limited", credential_identity="TEAM_PAT", is_rate_limit=True),
            ("default-result", 12),
        ]
    )

    assert ReadTokenPoolOperations.run("rest", operation, pool, str) == "default-result"
    assert [call.args for call in operation.call_args_list] == [
        ("alternate-token", "TEAM_PAT"),
        ("default-token", "DEFAULT"),
    ]
    pool.mark_rate_limited.assert_called_once()
    pool.record_remaining.assert_any_call("DEFAULT", "rest", 12)


def test_run_preserves_non_rate_limit_error_from_default_fallback() -> None:
    pool = Mock()
    pool.select.return_value = None
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT"
    pool.default_is_active = False
    expected = RetryableError("temporary failure", is_rate_limit=False)

    with pytest.raises(RetryableError) as raised:
        ReadTokenPoolOperations.run(
            "rest",
            lambda *_args: (_ for _ in ()).throw(expected),
            pool,
            str,
        )

    assert raised.value is expected
    pool.mark_rate_limited.assert_not_called()


def test_run_maps_rate_limit_from_default_fallback() -> None:
    pool = Mock()
    pool.select.return_value = None
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT"
    pool.default_is_active = False
    limited = RetryableError("rate limited", credential_identity="DEFAULT", is_rate_limit=True)

    with pytest.raises(ProviderRateLimitError):
        ReadTokenPoolOperations.run(
            "rest",
            lambda *_args: (_ for _ in ()).throw(limited),
            pool,
            str,
        )

    pool.mark_rate_limited.assert_called_once_with("DEFAULT", limited)


def test_run_allows_empty_pool_default_operation() -> None:
    pool = Mock()
    pool.select.return_value = None
    pool.default_token = ""
    pool.default_identity = "DEFAULT"
    pool.default_is_active = False

    assert ReadTokenPoolOperations.run("rest", lambda _token, identity: (identity, None), pool, str) == "DEFAULT"


def test_deadline_defers_remote_rate_limit_persistence_but_keeps_local_cooldown() -> None:
    identity = "TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
    provider = Mock()
    bypass = ContextVar("test_read_pool_bypass", default=False)

    def persist(identity: str, error: RetryableError) -> float | None:
        return ReadTokenPoolRateLimits.persist_rate_limit(provider, identity, error, bypass=bypass)

    requests = iter([('{"login":"team-user"}', None), ("{}", None)])
    pool = ReadTokenPool(
        repo="owner/repo",
        secrets_json=json.dumps({identity: "team-token"}),
        request=lambda *_args: next(requests),
        on_rate_limit=persist,
    )
    now = [0.0]
    limited = RetryableError("rate limited", credential_identity=identity, is_rate_limit=True)

    def operation(*_args: object) -> tuple[str, int | None]:
        now[0] = 10.0
        raise limited

    with ReadTokenPoolOperations.request_context(10.0, lambda: now[0]):
        deadline, monotonic = ReadTokenPoolOperations.current_request_context()
        assert deadline == 10.0
        assert monotonic is not None and monotonic() == 0.0
        assert ReadTokenPoolOperations.resolve_request_context(None, None) == (deadline, monotonic)

        def explicit_clock() -> float:
            return 1.0

        assert ReadTokenPoolOperations.resolve_request_context(5.0, explicit_clock) == (5.0, explicit_clock)
        with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
            ReadTokenPoolOperations.run(
                "rest",
                operation,
                pool,
                str,
                deadline=10.0,
                monotonic=lambda: now[0],
            )

    assert identity in pool._rate_limited
    with patch(
        "agentic_devtools.cli.ci.cooldown.persist_cooldown",
        return_value=("github:TEAM", CooldownRecord(resume_at=20.0)),
    ) as persist_cooldown:
        ReadTokenPoolRateLimits.flush_deferred_rate_limits()
    persist_cooldown.assert_called_once()
    assert not bypass.get()


def test_http_error_deadline_check_preserves_only_pool_rate_limit_bookkeeping() -> None:
    ReadTokenPoolOperations.check_http_error_deadline(
        10.0,
        lambda: 10.0,
        pool_managed=True,
        is_rate_limit=True,
    )

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.check_http_error_deadline(
            10.0,
            lambda: 10.0,
            pool_managed=True,
            is_rate_limit=False,
        )

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.check_http_error_deadline(
            10.0,
            lambda: 10.0,
            pool_managed=False,
            is_rate_limit=True,
        )


def test_run_translates_direct_retryable_error_after_deadline() -> None:
    now = [0.0]
    error = RetryableError("server error", is_rate_limit=False)

    def operation(*_args: object) -> tuple[str, int | None]:
        now[0] = 10.0
        raise error

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.run(
            "rest",
            operation,
            None,
            str,
            deadline=10.0,
            monotonic=lambda: now[0],
        )


def test_run_preserves_direct_retryable_error_before_deadline() -> None:
    error = RetryableError("temporary failure", is_rate_limit=False)

    with pytest.raises(RetryableError) as raised:
        ReadTokenPoolOperations.run(
            "rest",
            lambda *_args: (_ for _ in ()).throw(error),
            None,
            str,
            deadline=10.0,
            monotonic=lambda: 0.0,
        )

    assert raised.value is error


def test_run_stops_pool_retry_when_server_error_arrives_at_deadline() -> None:
    pool = Mock()
    pool.select.return_value = ReadCredential("TEAM_PAT", "team-token", "team-user")
    now = [0.0]
    error = RetryableError("server error", is_rate_limit=False)

    def operation(*_args: object) -> tuple[str, int | None]:
        now[0] = 10.0
        raise error

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.run(
            "rest",
            operation,
            pool,
            str,
            deadline=10.0,
            monotonic=lambda: now[0],
        )

    pool.select.assert_called_once()
    pool.mark_rate_limited.assert_not_called()


def test_run_stops_default_fallback_when_rate_limit_arrives_at_deadline() -> None:
    pool = Mock()
    pool.select.return_value = None
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT"
    now = [0.0]
    error = RetryableError("rate limited", credential_identity="DEFAULT", is_rate_limit=True)

    def operation(*_args: object) -> tuple[str, int | None]:
        now[0] = 10.0
        raise error

    with pytest.raises(ReadTokenPoolOperations.DeadlineExpired):
        ReadTokenPoolOperations.run(
            "rest",
            operation,
            pool,
            str,
            deadline=10.0,
            monotonic=lambda: now[0],
        )

    pool.mark_rate_limited.assert_called_once_with("DEFAULT", error)
    pool.select.assert_called_once()
