"""Verify direct dispatch acknowledges only its captured pending wake."""

import json
from copy import deepcopy
from typing import Any

import pytest

from agentic_devtools.cli.ci import dispatcher_wake_replay, dispatcher_wakeup, github_provider
from agentic_devtools.cli.ci.cooldown import COOLDOWN_VARIABLE
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore

REPOSITORY = "owner/repo"
PR_NUMBER = 42
HEAD_SHA = "a" * 40
DISPATCH_ENDPOINT = f"/repos/{REPOSITORY}/actions/workflows/ai-pr-loop-throttler.yml/dispatches"


class _VariableAPI:
    def __init__(self) -> None:
        self.value = json.dumps({"provider_cooldowns": {}})

    def __call__(
        self, endpoint: str, *, method: str = "GET", body: dict[str, Any] | None = None, **_kwargs: Any
    ) -> str:
        assert endpoint == f"/repos/{REPOSITORY}/actions/variables/{COOLDOWN_VARIABLE}"
        if method == "GET":
            return json.dumps({"value": self.value})
        assert method == "PATCH"
        assert body is not None
        self.value = body["value"]
        return ""


class _DispatchAPI:
    def __init__(self) -> None:
        self.posts: list[tuple[str, dict[str, Any]]] = []
        self.hook: Any = None

    def __call__(self, endpoint: str, *, method: str = "GET", body: dict[str, Any] | None = None, **kwargs: Any) -> str:
        assert endpoint == DISPATCH_ENDPOINT
        assert method == "POST"
        assert body == {"ref": "main"}
        assert "return_run_details" not in kwargs
        self.posts.append((endpoint, deepcopy(body)))
        return self.hook() if self.hook is not None else ""


def _configure(monkeypatch: pytest.MonkeyPatch, tmp_path: Any, event_name: str = "pull_request_target"):
    event_path = tmp_path / "event.json"
    event_path.write_text(
        json.dumps({"action": "synchronize", "pull_request": {"number": PR_NUMBER, "head": {"sha": HEAD_SHA}}}),
        encoding="utf-8",
    )
    for name, value in {
        "GITHUB_REPOSITORY": REPOSITORY,
        "GITHUB_EVENT_NAME": event_name,
        "GITHUB_EVENT_PATH": str(event_path),
        "GITHUB_RUN_ID": "123",
        "GITHUB_RUN_ATTEMPT": "2",
        "REPO_VARIABLE_WRITER_PAT": "test-writer-token",
    }.items():
        monkeypatch.setenv(name, value)
    variable_api = _VariableAPI()
    dispatch_api = _DispatchAPI()
    monkeypatch.setattr(github_provider, "_gh_api", variable_api)
    monkeypatch.setattr(dispatcher_wakeup, "_gh_api", dispatch_api)
    monkeypatch.setattr(dispatcher_wakeup, "_provider_cooldown", lambda *_args: None)
    monkeypatch.setattr(dispatcher_wakeup.time, "time", lambda: 100.0)
    provider = github_provider.GitHubActionsProvider(repo=REPOSITORY)
    return provider, DispatcherWakeStore(provider), variable_api, dispatch_api


def _seed(
    store: DispatcherWakeStore, *, pr_number: int = PR_NUMBER, head_sha: str = HEAD_SHA, event: str | None = None
):
    event = event or "pull_request_target:synchronize:123"
    assert store.enqueue(pr_number, head_sha, event, resume_at=500.0, now=100.0)
    key = store._key(pr_number, head_sha, event)
    return key, store.entries(now=100.0)[key]


def test_same_run_rerun_acknowledges_snapshot_after_empty_success_and_skips_replay(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """A successful empty-body dispatch acknowledges the old same-run wake before replay."""
    provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    key, snapshot = _seed(store)

    def accepted_post() -> str:
        assert store.entries(now=100.0)[key] == snapshot
        return ""

    dispatch.hook = accepted_post
    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    delivered = json.loads(_variables.value)["dispatcher_wakes"]["entries"][key]
    assert delivered["status"] == "delivered"
    assert delivered["identity"] == snapshot["identity"]
    assert len(dispatch.posts) == 1
    assert dispatcher_wake_replay.DispatcherWakeReplay(provider, store).run(REPOSITORY, "main") is False
    assert len(dispatch.posts) == 1


@pytest.mark.parametrize(
    ("pr_number", "head_sha", "event"),
    [
        (PR_NUMBER, HEAD_SHA, "pull_request_target:synchronize:456"),
        (PR_NUMBER + 1, HEAD_SHA, "pull_request_target:synchronize:123"),
        (PR_NUMBER, "b" * 40, "pull_request_target:synchronize:123"),
        (PR_NUMBER, HEAD_SHA, "pull_request_target:opened:123"),
        (None, None, None),
    ],
)
def test_nonmatching_wake_is_not_acknowledged(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Any,
    pr_number: int | None,
    head_sha: str | None,
    event: str | None,
) -> None:
    """Different run, PR, head, action, or absent entries cannot be acknowledged."""
    _provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    if pr_number is None:
        _seed(store, event="pull_request_target:opened:456")
    else:
        _seed(store, pr_number=pr_number, head_sha=head_sha or HEAD_SHA, event=event)

    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    assert dispatch.posts
    assert all(entry["status"] == "pending" for entry in store.entries(now=100.0).values())


def test_entry_with_mismatched_identity_fields_is_not_acknowledged(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """Entry identity fields must match even when supplied under the expected key."""
    _provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    key, snapshot = _seed(store)
    acknowledgements: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def return_mismatched_entry(_store: DispatcherWakeStore, *_args: Any, **_kwargs: Any):
        return {key: dict(snapshot, event="pull_request_target:synchronize:456")}

    def record_acknowledgment(*args: Any, **kwargs: Any) -> bool:
        acknowledgements.append((args, kwargs))
        return True

    monkeypatch.setattr(
        DispatcherWakeStore,
        "entries",
        return_mismatched_entry,
    )
    monkeypatch.setattr(
        DispatcherWakeStore,
        "acknowledge",
        record_acknowledgment,
    )

    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    assert not acknowledgements
    assert len(dispatch.posts) == 1
    saved = json.loads(_variables.value)["dispatcher_wakes"]["entries"]
    assert saved[key]["status"] == "pending"


def test_non_target_event_posts_without_identity_or_store_lookup(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any
) -> None:
    """Non-target events retain the direct path and never inspect wake state."""
    _provider, _store, _variables, dispatch = _configure(monkeypatch, tmp_path, event_name="workflow_dispatch")
    dispatcher = dispatcher_wakeup.DispatcherWakeup()
    monkeypatch.setattr(dispatcher, "_current_wake_identity", lambda: pytest.fail("identity lookup attempted"))
    monkeypatch.setattr(DispatcherWakeStore, "entries", lambda *_args, **_kwargs: pytest.fail("store lookup attempted"))

    dispatcher._dispatch(REPOSITORY, "main")

    assert len(dispatch.posts) == 1


@pytest.mark.parametrize("failure", ["identity", "entries"])
def test_lookup_failure_warns_and_continues_post(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Any,
    capsys: pytest.CaptureFixture[str],
    failure: str,
) -> None:
    """Identity and provider read exceptions fail open with one warning and no acknowledgment."""
    _provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    _seed(store)
    if failure == "identity":
        dispatcher = dispatcher_wakeup.DispatcherWakeup()
        monkeypatch.setattr(
            dispatcher, "_current_wake_identity", lambda: (_ for _ in ()).throw(ValueError("bad event"))
        )
    else:
        monkeypatch.setattr(
            store.provider,
            "get_variable",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("variable unavailable")),
        )
        monkeypatch.setattr(dispatcher_wakeup, "DispatcherWakeStore", lambda _provider: store)
        dispatcher = dispatcher_wakeup.DispatcherWakeup()

    dispatcher._dispatch(REPOSITORY, "main")

    exception = "ValueError" if failure == "identity" else "OSError"
    assert f"::warning::Dispatcher wake snapshot lookup failed ({exception})." in capsys.readouterr().out
    assert len(dispatch.posts) == 1
    saved = json.loads(_variables.value)["dispatcher_wakes"]["entries"]
    assert all(entry["status"] == "pending" for entry in saved.values())


def test_decode_failure_is_only_reported_by_store(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Any,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """An undecodable variable returns no candidate without a duplicate annotation."""
    _provider, _store, variables, dispatch = _configure(monkeypatch, tmp_path)
    variables.value = "not-json"

    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    output = capsys.readouterr().out
    assert "Dispatcher wake snapshot lookup failed" not in output
    assert "Could not decode dispatcher wakes: JSONDecodeError" in caplog.text
    assert len(dispatch.posts) == 1


@pytest.mark.parametrize("error", [TimeoutError("request timed out"), RuntimeError("HTTP 422 rejected")])
def test_failed_post_leaves_wake_pending(monkeypatch: pytest.MonkeyPatch, tmp_path: Any, error: Exception) -> None:
    """Timeouts and API-reported failures do not acknowledge a pending wake."""
    _provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    _seed(store)
    dispatch.hook = lambda: (_ for _ in ()).throw(error)

    with pytest.raises(type(error), match=str(error)):
        dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    assert all(entry["status"] == "pending" for entry in store.entries(now=100.0).values())


def test_concurrent_replacement_wins_cas_and_warns(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any, capsys: pytest.CaptureFixture[str]
) -> None:
    """A newer pending snapshot survives the old snapshot's failed CAS."""
    _provider, store, variables, dispatch = _configure(monkeypatch, tmp_path)
    key, snapshot = _seed(store)

    def replace_during_post() -> str:
        payload = json.loads(variables.value)
        replacement = dict(snapshot, identity="newer-snapshot", resume_at=200.0)
        payload["dispatcher_wakes"]["entries"][key] = replacement
        variables.value = json.dumps(payload)
        return ""

    dispatch.hook = replace_during_post
    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    assert store.entries(now=100.0)[key]["identity"] == "newer-snapshot"
    assert "::warning::Dispatcher wake acknowledgement was not applied." in capsys.readouterr().out


def test_acknowledgement_exception_does_not_change_successful_dispatch(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Any, capsys: pytest.CaptureFixture[str]
) -> None:
    """An acknowledgment exception warns but preserves the accepted POST result."""
    _provider, store, _variables, dispatch = _configure(monkeypatch, tmp_path)
    _seed(store)
    monkeypatch.setattr(
        DispatcherWakeStore,
        "acknowledge",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("write unavailable")),
    )

    dispatcher_wakeup.DispatcherWakeup()._dispatch(REPOSITORY, "main")

    assert len(dispatch.posts) == 1
    assert all(entry["status"] == "pending" for entry in store.entries(now=100.0).values())
    assert "::warning::Dispatcher wake acknowledgement failed (OSError)." in capsys.readouterr().out
