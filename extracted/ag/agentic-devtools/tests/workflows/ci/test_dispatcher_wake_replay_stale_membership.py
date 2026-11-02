"""Replay membership admits a wake, but fresh scheduler eligibility authorizes work."""

import json
from copy import deepcopy
from subprocess import CompletedProcess
from typing import Any

import pytest

from agentic_devtools.cli.ci import dispatcher_throttle, dispatcher_wake_replay, github_provider
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.ci.reconciliation.models import QueueState
from agentic_devtools.cli.ci.reconciliation.queue_store import QueueStore
from agentic_devtools.cli.ci.scheduler import run_scheduler

REPOSITORY = "owner/repo"
PR_NUMBER = 42
HEAD_SHA = "a" * 40


def _isolate_runtime(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", REPOSITORY)
    monkeypatch.setenv("GITHUB_RUN_ID", "0")
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-workflow-token")
    monkeypatch.setenv("REPO_VARIABLE_WRITER_PAT", "test-variable-token")
    monkeypatch.delenv("AGDT_GITHUB_SECRETS_JSON", raising=False)
    monkeypatch.delenv("AGDT_ALLOW_PRIVILEGED_PATHS", raising=False)
    monkeypatch.delenv("AI_PR_LOOP_DISPATCH_BATCH_SIZE", raising=False)
    monkeypatch.delenv("AI_PR_LOOP_ELIGIBLE_PR_LIMIT", raising=False)
    monkeypatch.setattr(dispatcher_wake_replay.time, "time", lambda: 100.0)
    monkeypatch.setattr(
        QueueStore,
        "load",
        lambda _self: QueueState(repo=REPOSITORY, revision=0, items={}, records=[], quarantines=[]),
    )


class _GitHubAPI:
    """Offline transport shared by replay and the subsequently dispatched scheduler."""

    def __init__(self) -> None:
        self.node = {
            "number": PR_NUMBER,
            "databaseId": 420,
            "createdAt": "2026-01-01T00:00:00Z",
            "isCrossRepository": False,
            "headRefName": "feature/stable-head",
            "headRefOid": HEAD_SHA,
            "title": "Ready for review",
            "changedFiles": 1,
            "isDraft": False,
            "labels": {"nodes": []},
            "closingIssuesReferences": {"nodes": []},
        }
        self.live_pr = {
            "number": PR_NUMBER,
            "id": self.node["databaseId"],
            "state": "open",
            "head": {"sha": HEAD_SHA, "ref": self.node["headRefName"]},
        }
        self.approved = False
        self.variables = {"AI_PR_LOOP_LAST_DISPATCHED_PR": "1"}
        self.inventories: list[dict[str, Any]] = []
        self.review_states: list[bool] = []
        self.ci_reads: list[str] = []
        self.live_reads: list[dict[str, Any]] = []
        self.dispatches: list[tuple[str, dict[str, Any]]] = []

    def _inventory(self) -> dict[str, Any]:
        self.inventories.append(deepcopy(self.node))
        return {
            "data": {
                "repository": {
                    "pullRequests": {
                        "nodes": [self.node],
                        "pageInfo": {"hasNextPage": False},
                    }
                }
            }
        }

    def _current_pr(self) -> dict[str, Any]:
        self.live_reads.append(deepcopy(self.live_pr))
        return self.live_pr

    def _reviews(self) -> list[dict[str, Any]]:
        self.review_states.append(self.approved)
        return [{"id": 1, "user": {"login": "reviewer"}, "state": "APPROVED"}] if self.approved else []

    def __call__(self, endpoint: str, **kwargs: Any) -> str:
        method = kwargs.get("method", "GET")
        variable_prefix = f"/repos/{REPOSITORY}/actions/variables/"
        if endpoint.startswith(variable_prefix):
            name = endpoint.removeprefix(variable_prefix)
            if method == "PATCH":
                self.variables[name] = kwargs["body"]["value"]
                return ""
            assert method == "GET"
            return json.dumps({"value": self.variables.get(name)})
        if endpoint.endswith("/dispatches") and method == "POST":
            self.dispatches.append((endpoint, deepcopy(kwargs["body"])))
            if endpoint == f"/repos/{REPOSITORY}/actions/workflows/ai-pr-loop-throttler.yml/dispatches":
                # Replay's cached positive is only admission; the queued scheduler
                # will observe the human block through its own inventory read.
                assert self.review_states == [False]
                self.approved = True
            return ""
        dynamic = {
            "/graphql": self._inventory,
            f"/repos/{REPOSITORY}/pulls/{PR_NUMBER}": self._current_pr,
            f"/repos/{REPOSITORY}/pulls/{PR_NUMBER}/reviews": self._reviews,
        }
        if endpoint in dynamic:
            return json.dumps(dynamic[endpoint]())
        responses = {
            f"/repos/{REPOSITORY}/commits/{HEAD_SHA}/status": {"state": "success", "total_count": 1},
            f"/repos/{REPOSITORY}/commits/{HEAD_SHA}/check-runs": {
                "check_runs": [{"status": "completed", "conclusion": "success"}]
            },
            f"/repos/{REPOSITORY}/issues/{PR_NUMBER}/events": [],
            f"/agents/repos/{REPOSITORY}/tasks": {"tasks": []},
            f"/agents/repos/{REPOSITORY}/tasks?per_page=100&page=1": {"tasks": []},
            f"/repos/{REPOSITORY}/actions/variables?per_page=1": {"variables": []},
            f"/repos/{REPOSITORY}/actions/workflows?per_page=100&page=1": {
                "workflows": [{"id": 123, "path": "dynamic/copilot-swe-agent/copilot"}]
            },
            **{
                f"/repos/{REPOSITORY}/actions/workflows/123/runs"
                f"?status={status}&branch=feature%2Fstable-head&per_page=100&page=1": {"workflow_runs": []}
                for status in ("queued", "in_progress", "waiting", "pending", "requested")
            },
        }
        if method == "GET" and endpoint in responses:
            if endpoint.startswith(f"/repos/{REPOSITORY}/commits/"):
                self.ci_reads.append(endpoint)
            return json.dumps(responses[endpoint])
        pytest.fail(f"Unexpected external API call: {method} {endpoint}")


def _throttle_api(args: list[str], **_kwargs: Any) -> CompletedProcess:
    assert args == [
        "gh",
        "api",
        f"/repos/{REPOSITORY}/actions/workflows/ai-pr-loop-throttler.yml/runs?per_page=1&branch=main",
        "--include",
    ]
    return CompletedProcess(args, 0, b'HTTP/2 200 OK\r\n\r\n{"workflow_runs":[]}', b"")


def test_fresh_scheduler_excludes_human_blocked_stale_replay_candidate(monkeypatch: pytest.MonkeyPatch) -> None:
    """A human block after replay admission prevents scheduling with unchanged PR/head."""
    _isolate_runtime(monkeypatch)
    api = _GitHubAPI()
    monkeypatch.setattr(github_provider, "_gh_api", api)
    monkeypatch.setattr(dispatcher_wake_replay, "_gh_api", api)
    monkeypatch.setattr(dispatcher_throttle, "run_safe", _throttle_api)
    replay_provider = github_provider.GitHubActionsProvider(repo=REPOSITORY)
    store = DispatcherWakeStore(replay_provider)
    assert store.enqueue(PR_NUMBER, HEAD_SHA, "pull_request_target:synchronize", resume_at=100.0, now=90.0)

    replay = dispatcher_wake_replay.DispatcherWakeReplay(replay_provider, store)
    assert replay.run(REPOSITORY, "main") is True
    assert api.dispatches == [
        (f"/repos/{REPOSITORY}/actions/workflows/ai-pr-loop-throttler.yml/dispatches", {"ref": "main"})
    ]
    assert api.live_reads == [api.live_pr, api.live_pr]
    assert api.inventories == [api.node]
    assert api.approved is True
    assert not replay.dispatch_failed

    # A dispatched workflow has its own provider, not replay's inventory snapshot.
    scheduler_provider = github_provider.GitHubActionsProvider(repo=REPOSITORY)
    result = run_scheduler(scheduler_provider)

    assert api.inventories == [api.node, api.node]
    assert api.review_states == [False, True]
    assert api.ci_reads == [
        f"/repos/{REPOSITORY}/commits/{HEAD_SHA}/status",
        f"/repos/{REPOSITORY}/commits/{HEAD_SHA}/check-runs",
    ]
    assert result.status == "ok"
    assert result.run_mode == "live"
    assert result.eligible_count == 0
    assert result.dispatched_count == 0
    assert result.dispatched_prs == []
    assert not result.had_dispatch_error
    assert not any(endpoint.endswith("/ai-pr-loop.yml/dispatches") for endpoint, _body in api.dispatches)
