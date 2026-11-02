"""Tests for durable dispatcher wake production."""

import json
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_wakeup as subject
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError


@pytest.fixture
def wakeup(monkeypatch, tmp_path):
    event_path = tmp_path / "event.json"
    event_path.write_text(
        json.dumps({"action": "synchronize", "pull_request": {"number": 42, "head": {"sha": "a" * 40}}})
    )
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path / "output"))
    monkeypatch.setenv("GITHUB_EVENT_NAME", "pull_request_target")
    monkeypatch.setenv("GITHUB_RUN_ID", "12345")
    monkeypatch.setattr(subject.time, "time", lambda: 1000)
    monkeypatch.setattr(subject, "_provider_cooldown", Mock(return_value=None))
    monkeypatch.setattr(subject, "active_cooldown", Mock(return_value=None))
    monkeypatch.setattr(subject, "_get_read_token_pool", Mock(return_value=None))
    monkeypatch.setattr(
        subject,
        "persist_cooldown",
        Mock(return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=1_000_000.0))),
    )
    provider = Mock()
    store = Mock()
    store.enqueue.return_value = True
    monkeypatch.setattr(subject, "DispatcherWakeStore", Mock(return_value=store))
    monkeypatch.setattr(subject, "GitHubActionsProvider", Mock(return_value=provider))
    return subject.DispatcherWakeup(), store


@pytest.mark.parametrize("site", ["check", "dispatch", "preserve"])
def test_lost_wake_names_refusing_guard(monkeypatch, wakeup, site):
    producer, store = wakeup
    store.enqueue.return_value = False
    store.last_refusal = "entry-capacity"
    monkeypatch.setattr(subject, "_provider_cooldown", Mock(return_value=("github:default", Mock(resume_at=9000))))
    error = ProviderRateLimitError(retry_after_seconds=60)
    with pytest.raises(RuntimeError) as caught:
        if site == "preserve":
            producer._preserve(error)
        else:
            producer.run(mode=site, default_branch="main")
    assert str(caught.value) == (
        "Dispatcher wake was not preserved; the scheduler wake-up was not handled (reason: entry-capacity)"
    )
    if site == "preserve":
        assert caught.value.__cause__ is error


def test_dispatch_uses_default_credential_and_default_branch(monkeypatch, wakeup):
    producer, store = wakeup
    request = Mock()
    monkeypatch.setattr(subject, "_gh_api", request)
    producer.run(mode="dispatch", default_branch="main")
    request.assert_called_once_with(
        "/repos/owner/repo/actions/workflows/ai-pr-loop-throttler.yml/dispatches",
        method="POST",
        body={"ref": "main"},
        read_pool=False,
    )
    store.enqueue.assert_not_called()


def test_dispatch_without_pull_request_target_context_keeps_fixed_token_write(monkeypatch, wakeup):
    producer, store = wakeup
    monkeypatch.delenv("GITHUB_EVENT_NAME")
    monkeypatch.delenv("GITHUB_EVENT_PATH")
    monkeypatch.setattr(
        subject,
        "_provider_cooldown",
        Mock(side_effect=AssertionError("non-PR dispatch must not require event context")),
    )
    request = Mock()
    monkeypatch.setattr(subject, "_gh_api", request)

    producer.run(mode="dispatch", default_branch="main")

    request.assert_called_once_with(
        "/repos/owner/repo/actions/workflows/ai-pr-loop-throttler.yml/dispatches",
        method="POST",
        body={"ref": "main"},
        read_pool=False,
    )
    store.enqueue.assert_not_called()


def test_check_defers_for_persisted_wake_before_throttle_lookup(monkeypatch, wakeup):
    from agentic_devtools.cli.ci import watchdog_command

    _, store = wakeup
    monkeypatch.setattr(subject, "_provider_cooldown", watchdog_command._provider_cooldown)
    monkeypatch.setattr(watchdog_command, "_get_read_token_pool", Mock(return_value=None))
    monkeypatch.setattr(watchdog_command, "active_cooldown", Mock(return_value=None))
    persisted_wakes = Mock()
    persisted_wakes.entries.return_value = {"prior": {"resume_at": 9000.0}}
    monkeypatch.setattr(watchdog_command, "DispatcherWakeStore", Mock(return_value=persisted_wakes))
    throttle = Mock()
    monkeypatch.setattr(subject, "DispatcherThrottle", Mock(return_value=throttle))

    subject.DispatcherWakeup().run(mode="check", default_branch="main")

    throttle.check.assert_not_called()
    assert subject.Path(subject.os.environ["GITHUB_OUTPUT"]).read_text(encoding="utf-8") == "throttled=true\n"
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 9000.0, now=1000)


def test_check_fails_closed_when_cooldown_wake_cannot_be_preserved(monkeypatch, wakeup):
    from agentic_devtools.cli.ci import watchdog_command

    _, store = wakeup
    store.enqueue.return_value = False
    monkeypatch.setattr(subject, "_provider_cooldown", watchdog_command._provider_cooldown)
    monkeypatch.setattr(watchdog_command, "_get_read_token_pool", Mock(return_value=None))
    monkeypatch.setattr(watchdog_command, "active_cooldown", Mock(return_value=None))
    persisted_wakes = Mock()
    persisted_wakes.entries.return_value = {"prior": {"resume_at": 9000.0}}
    monkeypatch.setattr(watchdog_command, "DispatcherWakeStore", Mock(return_value=persisted_wakes))
    throttle = Mock()
    monkeypatch.setattr(subject, "DispatcherThrottle", Mock(return_value=throttle))

    with pytest.raises(RuntimeError, match="not preserved"):
        subject.DispatcherWakeup().run(mode="check", default_branch="main")

    throttle.check.assert_not_called()


def test_check_without_pull_request_context_keeps_throttle_lookup(monkeypatch, wakeup):
    producer, store = wakeup
    monkeypatch.delenv("GITHUB_EVENT_NAME")
    monkeypatch.delenv("GITHUB_EVENT_PATH")
    throttle = Mock()
    monkeypatch.setattr(subject, "DispatcherThrottle", Mock(return_value=throttle))

    producer.run(mode="check", default_branch="main")

    throttle.check.assert_called_once()
    subject._provider_cooldown.assert_not_called()
    store.enqueue.assert_not_called()


@pytest.mark.parametrize(
    ("shared_deadline", "wake_deadline"),
    [(8200.0, 9000.0), (9000.0, 8200.0)],
)
def test_dispatch_defers_for_default_cooldown_even_when_read_pool_is_healthy(
    monkeypatch, wakeup, shared_deadline, wake_deadline
):
    from agentic_devtools.cli.ci import watchdog_command
    from agentic_devtools.cli.ci.cooldown import CooldownRecord

    producer, store = wakeup
    monkeypatch.setattr(subject, "_provider_cooldown", watchdog_command._provider_cooldown)
    pool = Mock()
    pool.blocking_cooldown_identities = ("READ_TOKEN",)
    pool.active_cooldown_for.return_value = None
    watchdog_store = Mock()
    watchdog_store.entries.return_value = {
        "pending": {"resume_at": wake_deadline},
    }
    monkeypatch.setattr(watchdog_command, "_get_read_token_pool", Mock(return_value=pool))
    monkeypatch.setattr(
        watchdog_command,
        "active_cooldown",
        Mock(return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", CooldownRecord(shared_deadline))),
    )
    monkeypatch.setattr(watchdog_command, "DispatcherWakeStore", Mock(return_value=watchdog_store))
    request = Mock()
    monkeypatch.setattr(subject, "_gh_api", request)

    producer.run(mode="dispatch", default_branch="main")

    request.assert_not_called()
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 9000.0, now=1000)


def test_dispatch_fails_closed_when_cooldown_wake_cannot_be_preserved(monkeypatch, wakeup):
    producer, store = wakeup
    store.enqueue.return_value = False
    monkeypatch.setattr(subject, "_provider_cooldown", Mock(return_value=("github:default", Mock(resume_at=9000))))
    request = Mock()
    monkeypatch.setattr(subject, "_gh_api", request)

    with pytest.raises(RuntimeError, match="not preserved"):
        producer.run(mode="dispatch", default_branch="main")

    request.assert_not_called()


@pytest.mark.parametrize("kind", ["provider", "retryable"])
def test_dispatch_rate_limit_persists_then_fails_visible(monkeypatch, wakeup, kind):
    producer, store = wakeup
    error = (
        ProviderRateLimitError(retry_after_seconds=7200)
        if kind == "provider"
        else RetryableError("limited", retry_after=7200, is_rate_limit=True)
    )
    monkeypatch.setattr(subject, "_gh_api", Mock(side_effect=error))
    with pytest.raises(ProviderRateLimitError):
        producer.run(mode="dispatch", default_branch="main")
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 8200, now=1000)
    subject.persist_cooldown.assert_called_once()
    assert subject.persist_cooldown.call_args.args[0] is subject.GitHubActionsProvider.return_value
    persisted_error = subject.persist_cooldown.call_args.args[1]
    assert isinstance(persisted_error, ProviderRateLimitError)
    assert persisted_error.retry_after_seconds is None
    assert persisted_error.reset_timestamp == 8200
    assert persisted_error.remaining == 0
    assert subject.persist_cooldown.call_args.kwargs == {"now": 1000}


def test_resolved_deadline_is_persisted_before_failed_enqueue(monkeypatch, wakeup):
    producer, store = wakeup
    monkeypatch.setattr(subject.time, "time", lambda: 100)
    store.enqueue.return_value = False
    record = Mock(resume_at=900.0)
    persist = Mock(return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", record))
    monkeypatch.setattr(subject, "persist_cooldown", persist)
    calls = Mock()
    calls.attach_mock(persist, "persist")
    calls.attach_mock(store.enqueue, "enqueue")

    with pytest.raises(RuntimeError, match="not preserved"):
        producer._preserve(ProviderRateLimitError(60, reset_timestamp=900, remaining=0))

    persisted_error = persist.call_args.args[1]
    assert persisted_error.reset_timestamp == 900
    assert persisted_error.retry_after_seconds is None
    assert persist.call_args.kwargs["now"] == 100
    assert calls.mock_calls[0][0] == "persist"
    assert calls.mock_calls[1][0] == "enqueue"


def test_unconfirmed_shared_cooldown_keeps_per_wake_deadline_and_warns(monkeypatch, wakeup, capsys):
    producer, store = wakeup
    monkeypatch.setattr(
        subject,
        "persist_cooldown",
        Mock(return_value=("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", Mock(resume_at=170.0))),
    )
    monkeypatch.setattr(subject, "_gh_api", Mock(side_effect=ProviderRateLimitError(retry_after_seconds=120)))

    with pytest.raises(ProviderRateLimitError):
        producer.run(mode="dispatch", default_branch="main")

    assert store.enqueue.call_args.args == (42, "a" * 40, "pull_request_target:synchronize:12345", 1120)
    assert "Shared provider cooldown persistence is unconfirmed or shorter" in capsys.readouterr().out


def test_shared_deadline_write_exception_still_preserves_wake(monkeypatch, wakeup, capsys):
    producer, store = wakeup
    monkeypatch.setattr(subject, "persist_cooldown", Mock(side_effect=RuntimeError("writer unavailable")))

    with pytest.raises(ProviderRateLimitError):
        producer._preserve(ProviderRateLimitError(retry_after_seconds=60))

    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 1060, now=1000)
    assert "Shared provider cooldown persistence failed" in capsys.readouterr().out


@pytest.mark.parametrize("preserved", [False, True])
@pytest.mark.parametrize(
    ("headers", "body", "expected_deadline"),
    [
        (b"Retry-After: 7200", b'{"message":"Forbidden"}', 8200),
        (b"X-RateLimit-Reset: 8200", b'{"message":"API rate limit exceeded"}', 8200),
        (b"Retry-After: 172800", b'{"message":"Forbidden"}', 173800),
        (b"X-RateLimit-Reset: 173800", b'{"message":"API rate limit exceeded"}', 173800),
    ],
)
def test_check_callback_preserves_before_any_sleep(monkeypatch, wakeup, preserved, headers, body, expected_deadline):
    producer, store = wakeup
    store.enqueue.return_value = preserved
    from agentic_devtools.cli.ci import dispatcher_throttle

    monkeypatch.delenv("AGDT_GITHUB_SECRETS_JSON", raising=False)
    monkeypatch.setattr(
        dispatcher_throttle,
        "run_safe",
        Mock(
            return_value=Mock(
                returncode=1,
                stdout=b"HTTP/2.0 403 Forbidden\n" + headers + b"\n\n" + body,
                stderr=b"gh: Forbidden",
            )
        ),
    )
    sleep = Mock(side_effect=AssertionError("must preserve and stop before sleep"))
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleep)
    with pytest.raises(ProviderRateLimitError if preserved else RuntimeError):
        producer.run(mode="check", default_branch="main")
    store.enqueue.assert_called_once_with(
        42, "a" * 40, "pull_request_target:synchronize:12345", expected_deadline, now=1000
    )
    sleep.assert_not_called()


def test_pooled_lookup_limit_is_preserved_with_independent_cooldown(monkeypatch, wakeup):
    from agentic_devtools.cli.ci import github_provider

    producer, store = wakeup
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", "{}")
    error = ProviderRateLimitError(credential_identity="TEAM_PAT")
    monkeypatch.setattr(github_provider, "_run_readonly_gh_command", Mock(side_effect=error))
    monkeypatch.setattr(subject, "active_cooldown", Mock(return_value=("github:TEAM_PAT", Mock(resume_at=8200))))
    with pytest.raises(ProviderRateLimitError) as caught:
        producer.run(mode="check", default_branch="main")
    assert caught.value is error
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 8200, now=1000)


def test_lookup_permission_error_never_preserves_or_dispatches(monkeypatch, wakeup):
    from agentic_devtools.cli.ci import dispatcher_throttle

    producer, store = wakeup
    monkeypatch.delenv("AGDT_GITHUB_SECRETS_JSON", raising=False)
    monkeypatch.setattr(
        dispatcher_throttle,
        "run_safe",
        Mock(return_value=Mock(returncode=1, stdout=b"HTTP/2.0 403 Forbidden\n\n{}", stderr=b"gh: Forbidden")),
    )
    with pytest.raises(RuntimeError, match="Forbidden"):
        producer.run(mode="check", default_branch="main")
    store.enqueue.assert_not_called()


def test_failed_preservation_is_not_reported_as_delivered(monkeypatch, wakeup):
    producer, store = wakeup
    store.enqueue.return_value = False
    monkeypatch.setattr(subject, "_gh_api", Mock(side_effect=ProviderRateLimitError(60)))
    with pytest.raises(RuntimeError, match="not preserved"):
        producer.run(mode="dispatch", default_branch="main")


@pytest.mark.parametrize(
    "error",
    [RuntimeError("permission denied"), RetryableError("server error"), ProviderRateLimitError(is_rate_limit=False)],
)
def test_non_rate_limit_errors_never_enqueue(monkeypatch, wakeup, error):
    producer, store = wakeup
    monkeypatch.setattr(subject, "_gh_api", Mock(side_effect=error))
    with pytest.raises(type(error)):
        producer.run(mode="dispatch", default_branch="main")
    store.enqueue.assert_not_called()


@pytest.mark.parametrize(
    ("variable", "value", "mode", "branch", "message"),
    [
        ("GITHUB_REPOSITORY", "", "check", "main", "owner/repo"),
        ("GITHUB_REPOSITORY", "owner/repo/../../else", "dispatch", "main", "owner/repo"),
        ("GITHUB_OUTPUT", "", "check", "main", "GITHUB_OUTPUT"),
        ("GITHUB_REPOSITORY", "owner/repo", "check", "", "default_branch"),
        ("GITHUB_REPOSITORY", "owner/repo", "invalid", "main", "mode"),
    ],
)
def test_validates_step_inputs(monkeypatch, wakeup, variable, value, mode, branch, message):
    producer, store = wakeup
    monkeypatch.setenv(variable, value)
    with pytest.raises(ValueError, match=message):
        producer.run(mode=mode, default_branch=branch)
    store.enqueue.assert_not_called()


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"action": None, "pull_request": {}},
        {"action": "$(evil)", "pull_request": {}},
        {"action": "closed", "pull_request": []},
        {"action": "closed", "pull_request": {"number": True, "head": {}}},
        {"action": "closed", "pull_request": {"number": -1, "head": {}}},
        {"action": "closed", "pull_request": {"number": "42", "head": {}}},
        {"action": "closed", "pull_request": {"number": 42, "head": []}},
        {"action": "closed", "pull_request": {"number": 42, "head": {"sha": "a\nthrottled=false"}}},
    ],
)
def test_rejects_untrusted_event_fields(monkeypatch, tmp_path, wakeup, payload):
    producer, store = wakeup
    event_path = tmp_path / "untrusted.json"
    event_path.write_text(json.dumps(payload))
    monkeypatch.setenv("GITHUB_EVENT_PATH", str(event_path))
    with pytest.raises(ValueError, match="Invalid dispatcher"):
        producer._preserve(ProviderRateLimitError(60))
    store.enqueue.assert_not_called()


@pytest.mark.parametrize("variable", ["GITHUB_EVENT_PATH", "GITHUB_EVENT_NAME"])
def test_requires_the_expected_event_context(monkeypatch, wakeup, variable):
    producer, store = wakeup
    monkeypatch.delenv(variable)
    with pytest.raises(ValueError, match="pull_request_target"):
        producer._preserve(ProviderRateLimitError(60))
    store.enqueue.assert_not_called()


@pytest.mark.parametrize(
    ("local_deadline", "persisted_deadline", "expected"),
    [
        (None, None, 1060),
        (4000, None, 4000),
        (None, 8200, 8200),
        (4000, 8200, 8200),
    ],
)
def test_missing_pool_error_timing_uses_effective_cooldown(
    monkeypatch, wakeup, local_deadline, persisted_deadline, expected
):
    producer, store = wakeup
    if local_deadline is not None:
        pool = Mock()
        pool.active_cooldown_for.return_value = ("github:TEAM_PAT", Mock(resume_at=local_deadline))
        monkeypatch.setattr(subject, "_get_read_token_pool", Mock(return_value=pool))
    active = None if persisted_deadline is None else ("github:TEAM_PAT", Mock(resume_at=persisted_deadline))
    monkeypatch.setattr(subject, "active_cooldown", Mock(return_value=active))
    with pytest.raises(ProviderRateLimitError):
        producer._preserve(ProviderRateLimitError(credential_identity="TEAM_PAT"))
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", expected, now=1000)
    subject.active_cooldown.assert_called_once_with(
        subject.GitHubActionsProvider.return_value,
        credential_identity=("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "TEAM_PAT"),
        now=1000,
        use_writer_token=True,
    )


def test_missing_identity_uses_default_credential_cooldown(monkeypatch, wakeup):
    producer, _ = wakeup
    with pytest.raises(ProviderRateLimitError):
        producer._preserve(ProviderRateLimitError())
    assert subject.active_cooldown.call_args.kwargs["credential_identity"] == ("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",)


def test_primary_reset_deadline_is_preserved(wakeup):
    producer, store = wakeup
    with pytest.raises(ProviderRateLimitError):
        producer._preserve(ProviderRateLimitError(reset_timestamp=8200, remaining=0))
    store.enqueue.assert_called_once_with(42, "a" * 40, "pull_request_target:synchronize:12345", 8200, now=1000)


def test_successful_check_never_enqueues(monkeypatch, wakeup):
    producer, store = wakeup
    throttle = Mock()
    monkeypatch.setattr(subject, "DispatcherThrottle", Mock(return_value=throttle))
    producer.run(mode="check", default_branch="main")
    subject.DispatcherThrottle.assert_called_once_with(
        on_rate_limit=producer._preserve, max_attempts=1, retry_window_seconds=0
    )
    throttle.check.assert_called_once()
    store.enqueue.assert_not_called()


@pytest.mark.parametrize("run_id", [None, "", "0", "-1", "²", "1\nthrottled=false", "9" * 21])
def test_rate_limited_event_requires_a_safe_positive_run_identity(monkeypatch, wakeup, run_id):
    producer, store = wakeup
    if run_id is None:
        monkeypatch.delenv("GITHUB_RUN_ID")
    else:
        monkeypatch.setenv("GITHUB_RUN_ID", run_id)
    with pytest.raises(ValueError, match="GITHUB_RUN_ID"):
        producer._preserve(ProviderRateLimitError(60))
    store.enqueue.assert_not_called()


def test_retries_share_a_key_but_distinct_events_on_the_same_head_do_not(monkeypatch, wakeup):
    producer, store = wakeup
    for run_id, attempt in [("12345", "1"), ("12345", "2"), ("12346", "1")]:
        monkeypatch.setenv("GITHUB_RUN_ID", run_id)
        monkeypatch.setenv("GITHUB_RUN_ATTEMPT", attempt)
        with pytest.raises(ProviderRateLimitError):
            producer._preserve(ProviderRateLimitError(60))
    events = [call.args[2] for call in store.enqueue.call_args_list]
    assert events == [
        "pull_request_target:synchronize:12345",
        "pull_request_target:synchronize:12345",
        "pull_request_target:synchronize:12346",
    ]
