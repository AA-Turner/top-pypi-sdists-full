"""Pooled HTTP-date throttling survives persisted dispatcher wake replay."""

import json
from collections import deque
from copy import deepcopy
from datetime import UTC, datetime
from email.utils import format_datetime
from subprocess import CompletedProcess
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_throttle, dispatcher_wake_replay, github_provider
from agentic_devtools.cli.ci import read_token_pool_execution as execution
from agentic_devtools.cli.ci.cooldown import COOLDOWN_VARIABLE
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.ci.reconciliation.models import QueueState
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore
from agentic_devtools.cli.shared.retry import ProviderRateLimitError

REPO = "owner/repo"
SHA = "a" * 40
DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
TEAM = "TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
THROTTLE = f"/repos/{REPO}/actions/workflows/ai-pr-loop-throttler.yml"


class _Transport:
    """Keep unrelated APIs offline while the pooled throttle request parses raw HTTP."""

    def __init__(self, now: list[float]) -> None:
        self.now = now
        self.retry_at = now[0] + 900
        self.variables: dict[str, str] = {}
        self.events: list[str] = []
        self.posts: list[dict[str, Any]] = []
        self.limited = True
        self.active_run = False
        self.live_head = SHA
        self.original_api = github_provider._gh_api

    def api(self, endpoint: str, **kwargs: Any) -> str:
        method = kwargs.get("method", "GET")
        prefix = f"/repos/{REPO}/actions/variables/"
        if endpoint.startswith(prefix):
            name = endpoint.removeprefix(prefix)
            self.events.append(f"variable:{method}")
            if method == "PATCH":
                self.variables[name] = kwargs["body"]["value"]
                return ""
            assert method == "GET"
            return json.dumps({"value": self.variables.get(name)})
        if endpoint == f"/repos/{REPO}/pulls/42":
            self.events.append("live-head")
            assert kwargs["token"] == "default-dummy-token"
            return json.dumps(
                {"number": 42, "id": 420, "state": "open", "head": {"sha": self.live_head, "ref": "feature/replay"}}
            )
        if endpoint == f"{THROTTLE}/dispatches":
            assert method == "POST"
            assert kwargs["token"] == "default-dummy-token"
            self.events.append("POST")
            self.posts.append(deepcopy(kwargs["body"]))
            return ""
        if endpoint.startswith(f"/agents/repos/{REPO}/tasks"):
            self.events.append("tasks")
            return '{"tasks":[]}'
        if endpoint == f"/repos/{REPO}/actions/workflows?per_page=100&page=1":
            self.events.append("task-workflows")
            return '{"workflows":[{"id":123,"path":"dynamic/copilot-swe-agent/copilot"}]}'
        if endpoint.startswith(f"/repos/{REPO}/actions/workflows/123/runs?"):
            self.events.append("task-runs")
            return '{"workflow_runs":[]}'
        responses = {
            f"/repos/{REPO}/issues/42/events": "[]",
            f"/repos/{REPO}/actions/variables?per_page=1": '{"variables":[]}',
        }
        if endpoint in responses:
            return responses[endpoint]
        if endpoint in {"/user", f"/repos/{REPO}"}:
            return self.original_api(endpoint, **kwargs)
        pytest.fail(f"Unexpected API call: {method} {endpoint}")

    def run(self, args: list[str], **kwargs: Any) -> CompletedProcess:
        assert args[:2] == ["gh", "api"]
        assert kwargs["shell"] is False
        assert kwargs["text"] is True
        endpoint = args[2]
        body: dict[str, Any]
        token = kwargs["env"]["GH_TOKEN"]
        assert "AGDT_GITHUB_SECRETS_JSON" not in kwargs["env"]
        if endpoint == "/user":
            body = {"login": f"{token}-user"}
        elif endpoint == f"/repos/{REPO}":
            body = {"permissions": {"pull": True}}
        else:
            assert endpoint == f"{THROTTLE}/runs?per_page=1&branch=main"
            assert "--include" in args
            assert token in {"default-dummy-token", "team-dummy-token"}
            self.events.append(f"throttle:{token}")
            if self.limited:
                retry_date = format_datetime(datetime.fromtimestamp(self.retry_at, UTC), usegmt=True)
                return CompletedProcess(
                    args,
                    1,
                    f"HTTP/2 403 Forbidden\r\nRetry-After: {retry_date}\r\n"
                    'X-RateLimit-Remaining: 4999\r\n\r\n{"message":"You have exceeded a secondary rate limit."}',
                    "gh: You have exceeded a secondary rate limit. (HTTP 403)",
                )
            body = {"workflow_runs": [{"status": "in_progress"}]} if self.active_run else {"workflow_runs": []}
        return CompletedProcess(args, 0, f"HTTP/2 200 OK\r\nX-RateLimit-Remaining: 4999\r\n\r\n{json.dumps(body)}", "")


@pytest.fixture
def pooled_replay(monkeypatch: pytest.MonkeyPatch):
    """Isolate credentials, pool caches, clocks, and external API traffic."""
    now = [datetime(2026, 1, 1, tzinfo=UTC).timestamp()]
    monkeypatch.setenv("GITHUB_REPOSITORY", REPO)
    monkeypatch.setenv("GITHUB_RUN_ID", "0")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({TEAM: "team-dummy-token"}))
    monkeypatch.setenv(DEFAULT, "default-dummy-token")
    monkeypatch.setenv("GH_TOKEN", "default-dummy-token")
    monkeypatch.setenv("REPO_VARIABLE_WRITER_PAT", "writer-dummy-token")
    monkeypatch.delenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", raising=False)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setattr(execution, "_RETAINED_RATE_LIMITS", {})
    monkeypatch.setattr(execution, "_DEFERRED_RATE_LIMIT_PERSISTENCE", deque())
    monkeypatch.setattr(dispatcher_wake_replay.time, "time", lambda: now[0])

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls.fromtimestamp(now[0], tz)

    monkeypatch.setattr(github_provider, "datetime", FrozenDateTime)
    transport = _Transport(now)
    monkeypatch.setattr(github_provider, "_gh_api", transport.api)
    monkeypatch.setattr(dispatcher_wake_replay, "_gh_api", transport.api)
    monkeypatch.setattr(github_provider, "run_safe", transport.run)
    monkeypatch.setattr(dispatcher_throttle, "run_safe", transport.run)
    notify = Mock(wraps=dispatcher_throttle._notify_rate_limit)
    monkeypatch.setattr(dispatcher_throttle, "_notify_rate_limit", notify)
    monkeypatch.setattr(
        QueueStore,
        "load",
        lambda _self: QueueState(repo=REPO, revision=0, items={}, records=[], quarantines=[]),
    )
    provider = github_provider.GitHubActionsProvider(repo=REPO)

    def inventory():
        transport.events.append("inventory")
        return [SimpleNamespace(number=42)]

    monkeypatch.setattr(provider, "list_eligible_prs", inventory)
    store = DispatcherWakeStore(provider)
    assert store.enqueue(42, SHA, "pull_request_target:synchronize", now[0], now=now[0])
    key, original = next(iter(store.entries().items()))
    replay = dispatcher_wake_replay.DispatcherWakeReplay(provider, store)
    transport.events.clear()
    return SimpleNamespace(
        now=now,
        transport=transport,
        provider=provider,
        store=store,
        key=key,
        original=original,
        replay=replay,
        notify=notify,
    )


def _assert_http_date_persisted(harness: SimpleNamespace) -> dict[str, Any]:
    assert harness.replay.run(REPO, "main") is False
    assert harness.notify.call_count == 1
    error = harness.notify.call_args.args[0]
    assert isinstance(error, ProviderRateLimitError)
    assert error.is_rate_limit
    assert error.retry_after_seconds == 900
    assert error.reset_timestamp is None
    assert error.credential_identity in {DEFAULT, TEAM}
    pool = github_provider._get_read_token_pool()
    assert pool is not None
    assert pool.recognizes_token("team-dummy-token")
    transport = harness.transport
    assert "throttle:team-dummy-token" in transport.events
    assert "throttle:default-dummy-token" in transport.events
    postponed = harness.store.entries()[harness.key]
    assert postponed["status"] == "pending"
    assert postponed["identity"] == harness.original["identity"]
    assert postponed["resume_at"] >= transport.retry_at
    assert postponed["resume_at"] > harness.now[0] + 60
    persisted = json.loads(transport.variables[COOLDOWN_VARIABLE])
    assert persisted["dispatcher_wakes"]["entries"][harness.key] == postponed
    assert not harness.replay.persistence_unconfirmed
    assert transport.posts == []
    return postponed


def _assert_due_replay_guards(harness: SimpleNamespace, postponed: dict[str, Any]) -> None:
    now, transport, replay, store, key = harness.now, harness.transport, harness.replay, harness.store, harness.key
    now[0] = postponed["resume_at"] + 1
    transport.limited = False
    transport.events.clear()
    assert replay.run(REPO, "main") is False
    assert "live-head" not in transport.events
    assert transport.posts == []
    postponed = store.entries()[key]
    assert postponed["resume_at"] > now[0]
    now[0] = postponed["resume_at"] + 1
    transport.active_run = True
    transport.events.clear()
    assert replay.run(REPO, "main") is False
    assert "live-head" in transport.events
    assert any(event.startswith("throttle:") for event in transport.events)
    assert "inventory" not in transport.events
    assert store.entries()[key] == postponed
    assert transport.posts == []

    transport.active_run = False
    transport.events.clear()
    assert replay.run(REPO, "main") is True
    events = transport.events[: transport.events.index("POST")]
    assert events.count("live-head") == 2
    throttle_indices = [i for i, event in enumerate(events) if event.startswith("throttle:")]
    assert len(throttle_indices) == 2
    assert events.index("live-head") < throttle_indices[0] < events.index("tasks")
    assert events.index("tasks") < events.index("inventory") < throttle_indices[1]
    assert "variable:GET" in events[events.index("inventory") : throttle_indices[1]]
    assert "variable:GET" in events[throttle_indices[1] + 1 :]
    assert transport.posts == [{"ref": "main"}]
    assert store.entries() == {}
    delivered = json.loads(transport.variables[COOLDOWN_VARIABLE])["dispatcher_wakes"]["entries"][key]
    assert delivered["status"] == "delivered"


def test_pooled_http_date_postpones_wake_and_rechecks_live_guards(pooled_replay: SimpleNamespace) -> None:
    """A secondary limit defers durable intent; only a fresh guarded due replay may POST."""
    harness = pooled_replay
    postponed = _assert_http_date_persisted(harness)
    now, transport, store, key = harness.now, harness.transport, harness.store, harness.key
    now[0] = postponed["resume_at"] - 1
    transport.events.clear()
    assert dispatcher_wake_replay.DispatcherWakeReplay(harness.provider).run(REPO, "main") is False
    assert store.entries()[key] == postponed
    assert not any(event == "live-head" or event.startswith("throttle:") for event in transport.events)
    assert transport.posts == []

    _assert_due_replay_guards(harness, postponed)
