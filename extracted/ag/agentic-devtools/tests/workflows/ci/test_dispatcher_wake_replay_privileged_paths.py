"""Replay inventory keeps privileged-path opt-in scoped to the provider call."""

import json
import os
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
import yaml

import agentic_devtools.cli.ci.pipeline.session_detector as session_detector
from agentic_devtools.cli.ci import dispatcher_wake_replay, github_provider
from agentic_devtools.cli.ci.pipeline.session_detector import SessionOutcome, SessionState

ENV_KEY = "AGDT_ALLOW_PRIVILEGED_PATHS"
PR_NUMBER = 42
HEAD_SHA = "a" * 40
PR: dict[str, Any] = {
    "number": PR_NUMBER,
    "id": 123,
    "state": "open",
    "head": {"sha": HEAD_SHA, "ref": "copilot/finished"},
}
ENTRY = {"pr_number": PR_NUMBER, "head_sha": HEAD_SHA}
PRIVILEGED_PATH = ".github/workflows/ai-pr-loop.yml"
REPO_ROOT = Path(__file__).resolve().parents[3]


def _provider_with_wip(monkeypatch: pytest.MonkeyPatch, error: Exception | None = None):
    provider = github_provider.GitHubActionsProvider(repo="owner/repo")
    observations: list[tuple[str, str | None]] = []
    graph = {
        "data": {
            "repository": {
                "pullRequests": {
                    "nodes": [
                        {
                            "number": PR_NUMBER,
                            "databaseId": PR["id"],
                            "createdAt": "2026-01-01T00:00:00Z",
                            "isCrossRepository": False,
                            "headRefName": PR["head"]["ref"],
                            "headRefOid": HEAD_SHA,
                            "title": "[WIP] finished privileged-path change",
                            "changedFiles": 1,
                            "isDraft": True,
                            "labels": {"nodes": [{"name": "ai-auto-merge-allowed"}]},
                        }
                    ],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                }
            }
        }
    }

    def fake_api(endpoint: str, **_kwargs: object) -> str:
        observations.append((endpoint, os.environ.get(ENV_KEY)))
        if endpoint == "/graphql":
            if error is not None:
                raise error
            return json.dumps(graph)
        if endpoint == f"/repos/owner/repo/pulls/{PR_NUMBER}/files":
            return json.dumps([{"filename": PRIVILEGED_PATH}])
        raise AssertionError(f"Unexpected provider API endpoint: {endpoint}")

    monkeypatch.setattr(github_provider, "_gh_api", fake_api)
    monkeypatch.setattr(provider, "_list_agent_task_inventory", lambda _repo: [])
    monkeypatch.setattr(
        session_detector,
        "get_latest_session_state",
        lambda *_args, **_kwargs: SessionState(SessionOutcome.FINISHED),
    )
    return provider, observations


def _set_initial_env(monkeypatch: pytest.MonkeyPatch, value: str | None) -> None:
    if value is None:
        monkeypatch.delenv(ENV_KEY, raising=False)
    else:
        monkeypatch.setenv(ENV_KEY, value)


def _assert_env_restored(value: str | None) -> None:
    if value is None:
        assert ENV_KEY not in os.environ
    else:
        assert os.environ[ENV_KEY] == value


@pytest.mark.parametrize("active_state", [True, None])
def test_active_or_unknown_task_short_circuits_inventory(
    monkeypatch: pytest.MonkeyPatch, active_state: bool | None
) -> None:
    monkeypatch.setenv(ENV_KEY, "preserve-me")
    provider, observations = _provider_with_wip(monkeypatch)
    replay = dispatcher_wake_replay.DispatcherWakeReplay(provider)
    inventory = Mock(side_effect=RuntimeError("inventory unavailable"))
    monkeypatch.setattr(provider, "list_eligible_prs", inventory)

    def task_is_active(*_args: object, **_kwargs: object) -> bool | None:
        return active_state

    monkeypatch.setattr(dispatcher_wake_replay, "is_copilot_session_active_via_agent_task", task_is_active)
    assert not replay._eligible(ENTRY, PR, "owner/repo")

    inventory.assert_not_called()
    assert observations == []
    assert os.environ[ENV_KEY] == "preserve-me"


@pytest.mark.parametrize("initial_value", [None, "", "not-enabled"])
def test_replay_scopes_opt_in_around_real_provider_inventory(
    monkeypatch: pytest.MonkeyPatch, initial_value: str | None
) -> None:
    _set_initial_env(monkeypatch, initial_value)
    provider, observations = _provider_with_wip(monkeypatch)
    store = Mock()
    replay = dispatcher_wake_replay.DispatcherWakeReplay(provider, store)
    task_lookup_env: list[str | None] = []

    def no_active_task(*_args: object, **_kwargs: object) -> bool:
        task_lookup_env.append(os.environ.get(ENV_KEY))
        return False

    monkeypatch.setattr(dispatcher_wake_replay, "is_copilot_session_active_via_agent_task", no_active_task)

    inventory_start = len(observations)
    assert provider.list_eligible_prs() == []
    unprivileged_calls = observations[inventory_start:]
    assert ("/graphql", initial_value) in unprivileged_calls
    assert (f"/repos/owner/repo/pulls/{PR_NUMBER}/files", initial_value) in unprivileged_calls

    inventory_start = len(observations)
    assert replay._eligible(ENTRY, PR, "owner/repo")

    replay_calls = observations[inventory_start:]
    assert replay_calls
    assert ("/graphql", "1") in replay_calls
    assert all(value == "1" for _, value in replay_calls)
    assert task_lookup_env == [initial_value]
    _assert_env_restored(initial_value)
    store.acknowledge.assert_not_called()


@pytest.mark.parametrize("initial_value", [None, "", "not-enabled"])
def test_inventory_exception_restores_environment_and_propagates(
    monkeypatch: pytest.MonkeyPatch, initial_value: str | None
) -> None:
    _set_initial_env(monkeypatch, initial_value)
    error = RuntimeError("inventory unavailable")
    provider, observations = _provider_with_wip(monkeypatch, error)
    replay = dispatcher_wake_replay.DispatcherWakeReplay(provider)
    monkeypatch.setattr(
        dispatcher_wake_replay,
        "is_copilot_session_active_via_agent_task",
        lambda *_args, **_kwargs: False,
    )

    with pytest.raises(RuntimeError) as raised:
        replay._eligible(ENTRY, PR, "owner/repo")

    assert raised.value is error
    assert observations == [("/graphql", "1")]
    _assert_env_restored(initial_value)


def test_throttler_scheduler_job_keeps_privileged_path_opt_in() -> None:
    workflow = yaml.safe_load((REPO_ROOT / ".github/workflows/ai-pr-loop-throttler.yml").read_text(encoding="utf-8"))
    scheduler_step = next(
        step for step in workflow["jobs"]["schedule-next-pr"]["steps"] if step.get("id") == "schedule"
    )

    assert scheduler_step["env"][ENV_KEY] == "1"
