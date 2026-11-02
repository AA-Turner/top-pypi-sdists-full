"""Replay reuses advisory eligible-PR membership only while its snapshot is current."""

import json
import os
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock, call

from agentic_devtools.cli.ci import dispatcher_wake_replay as replay_module

REPOSITORY = "owner/repo"
HEAD = "a" * 40


def _entry(number: int) -> dict[str, Any]:
    return {
        "pr_number": number,
        "head_sha": HEAD,
        "event": "pull_request_target:synchronize",
        "resume_at": 100.0,
        "status": "pending",
    }


def _pr(number: int, *, state: str = "open", head: str = HEAD) -> dict[str, Any]:
    return {
        "number": number,
        "id": number * 10,
        "state": state,
        "head": {"sha": head, "ref": f"copilot/{number}"},
    }


def _replay_harness(monkeypatch, entries, inventories, live_prs):
    monkeypatch.setenv("GITHUB_RUN_ID", "0")
    monkeypatch.delenv("AGDT_ALLOW_PRIVILEGED_PATHS", raising=False)
    monkeypatch.setattr(replay_module.time, "time", lambda: 100.0)
    provider = Mock()
    inventory_values = iter(inventories)
    inventory_env: list[str | None] = []

    def list_eligible_prs():
        inventory_env.append(os.environ.get("AGDT_ALLOW_PRIVILEGED_PATHS"))
        return next(inventory_values)

    provider.list_eligible_prs.side_effect = list_eligible_prs
    store = Mock()
    snapshot = {f"wake-{entry['pr_number']}": entry.copy() for entry in entries}
    store.entries.side_effect = lambda: {key: value.copy() for key, value in snapshot.items()}
    store.acknowledge.return_value = True
    responses = {number: list(values) for number, values in live_prs.items()}
    api_calls: list[tuple[str, dict[str, Any]]] = []
    posted: list[dict[str, Any]] = []

    def gh_api(endpoint: str, **kwargs: Any) -> str:
        api_calls.append((endpoint, kwargs))
        if endpoint.endswith("/dispatches"):
            posted.append(kwargs)
            return ""
        number = int(endpoint.rsplit("/", 1)[1])
        return json.dumps(responses[number].pop(0))

    monkeypatch.setattr(replay_module, "_gh_api", gh_api)
    monkeypatch.setattr(replay_module, "require_default_repo_workflow_token", lambda *_args: "token")
    cooldown = Mock(return_value=None)
    monkeypatch.setattr(replay_module, "_provider_cooldown", cooldown)
    monkeypatch.setattr(
        replay_module,
        "_reconcile_due_probes_and_check_availability",
        lambda *_args: (0, True, "available"),
    )
    task_check = Mock(return_value=False)
    monkeypatch.setattr(replay_module, "is_copilot_session_active_via_agent_task", task_check)
    throttle = Mock()
    throttle.return_value._lookup_last_run.return_value = {}
    throttle.return_value._is_throttled.return_value = False
    monkeypatch.setattr(replay_module, "DispatcherThrottle", throttle)
    return (
        replay_module.DispatcherWakeReplay(provider, store),
        provider,
        store,
        task_check,
        throttle,
        cooldown,
        api_calls,
        posted,
        inventory_env,
    )


def test_empty_membership_is_reused_and_each_run_gets_fresh_inventory(monkeypatch) -> None:
    entries = [_entry(42), _entry(43)]
    current_prs = {number: [_pr(number)] * 4 for number in (42, 43)}
    harness = _replay_harness(
        monkeypatch,
        entries,
        [[], [SimpleNamespace(number=42)]],
        current_prs,
    )
    runner, provider, store, task_check, throttle, cooldown, api_calls, posted, inventory_env = harness

    assert runner.run(REPOSITORY, "main") is False

    provider.list_eligible_prs.assert_called_once_with()
    assert task_check.call_count == 2
    assert len([call for call in api_calls if "/pulls/" in call[0]]) == 2
    assert throttle.call_count == 2
    assert throttle.return_value._lookup_last_run.call_count == 2
    assert cooldown.call_count == 2
    assert store.entries.call_count == 1
    assert posted == []

    assert runner.run(REPOSITORY, "main") is True

    assert provider.list_eligible_prs.call_count == 2
    assert task_check.call_count == 3
    assert store.entries.call_count == 3
    assert len(posted) == 1
    assert posted[0] == {"method": "POST", "body": {"ref": "main"}, "token": "token"}
    assert inventory_env == ["1", "1"]
    assert "AGDT_ALLOW_PRIVILEGED_PATHS" not in os.environ


def test_changed_live_head_refreshes_membership_before_the_next_entry(monkeypatch) -> None:
    first = _entry(42)
    second = _entry(43)
    harness = _replay_harness(
        monkeypatch,
        [first, second],
        [[SimpleNamespace(number=42)], [SimpleNamespace(number=43)]],
        {
            42: [_pr(42), _pr(42, head="b" * 40)],
            43: [_pr(43), _pr(43)],
        },
    )
    runner, provider, store, task_check, throttle, cooldown, api_calls, posted, _ = harness

    assert runner.run(REPOSITORY, "main") is True

    assert provider.list_eligible_prs.call_count == 2
    assert task_check.call_count == 2
    assert [call.args[1] for call in task_check.call_args_list] == [42, 43]
    assert len([call for call in api_calls if "/pulls/" in call[0]]) == 4
    assert throttle.call_count == 2
    assert throttle.return_value._lookup_last_run.call_count == 3
    assert throttle.return_value._is_throttled.call_count == 3
    assert cooldown.call_count == 3
    assert store.entries.call_count == 3
    assert store.acknowledge.call_args_list == [
        call("wake-42", first),
        call("wake-43", second),
    ]
    assert len(posted) == 1
