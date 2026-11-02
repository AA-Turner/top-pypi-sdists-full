"""A deferred wake survives the producer, failed handoff, and scheduled restarts."""

import json
from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci import dispatcher_throttle, dispatcher_wake_replay, dispatcher_wakeup, github_provider
from agentic_devtools.cli.ci.cooldown import COOLDOWN_VARIABLE, CooldownRecord, merge_cooldown
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

REPO = "owner/repo"
SHA = "a" * 40


def _configure_event(tmp_path, monkeypatch):
    event = tmp_path / "event.json"
    event.write_text(
        json.dumps({"action": "synchronize", "pull_request": {"number": 42, "head": {"sha": SHA}}}), encoding="utf-8"
    )
    for name, value in {
        "GITHUB_REPOSITORY": REPO,
        "GITHUB_EVENT_NAME": "pull_request_target",
        "GITHUB_EVENT_PATH": str(event),
        "GITHUB_RUN_ID": "123456",
        "GH_TOKEN": "default-test-credential",
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-test-credential",
        "REPO_VARIABLE_WRITER_PAT": "independent-test-credential",
    }.items():
        monkeypatch.setenv(name, value)
    monkeypatch.delenv("AGDT_GITHUB_SECRETS_JSON", raising=False)


def _exercise_replay(clock, provider, posts, raw):
    saved = json.loads(raw[0])
    wake = next(iter(saved["dispatcher_wakes"]["entries"].values()))
    shared = saved["provider_cooldowns"].get("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", {})
    first_deadline = max(wake["resume_at"], shared.get("resume_at", 0))
    # A new store/replayer has no job-local handoff data.
    clock[0] = first_deadline - 1
    assert not dispatcher_wake_replay.DispatcherWakeReplay(provider).run(REPO, "main")
    assert not posts
    clock[0] = first_deadline + 1
    assert dispatcher_wake_replay.DispatcherWakeReplay(provider).run(REPO, "main")
    pending = DispatcherWakeStore(provider).entries()
    assert len(pending) == 1
    saved = json.loads(raw[0])
    shared = saved["provider_cooldowns"].get("github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", {})
    renewed = max(next(iter(pending.values()))["resume_at"], shared.get("resume_at", 0))
    assert renewed > clock[0]
    clock[0] = renewed - 1
    assert not dispatcher_wake_replay.DispatcherWakeReplay(provider).run(REPO, "main")
    assert len(posts) == 1
    clock[0] = renewed + 1
    assert dispatcher_wake_replay.DispatcherWakeReplay(provider).run(REPO, "main")
    assert len(posts) == 2
    assert not DispatcherWakeStore(provider).entries()
    assert not dispatcher_wake_replay.DispatcherWakeReplay(provider).run(REPO, "main")
    assert len(posts) == 2
    final = json.loads(raw[0])
    assert final["future_metadata"] == {"preserve": True}
    assert final["provider_cooldowns"]["github:OTHER"]["resume_at"] == 550


@pytest.mark.parametrize("lose_shared_write", [False, True])
def test_independent_persistence_survives_job_exit_failed_post_and_new_scheduled_process(
    tmp_path, monkeypatch, lose_shared_write
):
    _configure_event(tmp_path, monkeypatch)
    clock = [100.0]
    monkeypatch.setattr(dispatcher_wakeup.time, "time", lambda: clock[0])
    raw = [json.dumps({"future_metadata": {"preserve": True}, "provider_cooldowns": {}})]
    writes = []

    def variable_api(endpoint, *, method="GET", body=None, token=None, **kwargs):
        assert token == "independent-test-credential"
        assert endpoint == f"/repos/{REPO}/actions/variables/{COOLDOWN_VARIABLE}"
        if method == "GET":
            return json.dumps({"value": raw[0]})
        assert method == "PATCH"
        payload = json.loads(body["value"])
        writes.append(payload)
        cooldowns = payload.get("provider_cooldowns", {})
        if not lose_shared_write or "github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" not in cooldowns:
            raw[0] = body["value"]
        return ""

    with patch.object(github_provider, "_gh_api", side_effect=variable_api):
        exhausted = ProviderRateLimitError(reset_timestamp=600, remaining=0)
        with pytest.raises(ProviderRateLimitError):
            dispatcher_wakeup.DispatcherWakeup()._preserve(exhausted)
        saved = json.loads(raw[0])
        assert saved["future_metadata"] == {"preserve": True}
        assert len(saved["dispatcher_wakes"]["entries"]) == 1
        if lose_shared_write:
            assert "github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" not in saved["provider_cooldowns"]
        else:
            assert saved["provider_cooldowns"]["github:DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"]["resume_at"] > 600

        # Another process writes ordinary cooldown metadata without deleting the wake.
        raw[0] = merge_cooldown(
            raw[0], key="github:OTHER", record=CooldownRecord(resume_at=550, updated_at=101), now=101
        )
        provider = github_provider.GitHubActionsProvider(repo=REPO)
        posts = []

        def replay_api(endpoint, *, method="GET", body=None, token=None):
            assert token == "default-test-credential"
            if method == "POST":
                posts.append(endpoint)
                if len(posts) == 1:
                    raise RetryableError("rate limited", retry_after=300, is_rate_limit=True)
                return ""
            assert endpoint == f"/repos/{REPO}/pulls/42"
            return json.dumps(
                {"number": 42, "id": 123, "state": "open", "draft": False, "head": {"sha": SHA, "ref": "branch"}}
            )

        def throttle_api(*args, **kwargs):
            return CompletedProcess(
                args[0], 0, b"HTTP/2.0 200 OK\r\n\r\n" + json.dumps({"workflow_runs": []}).encode(), b""
            )

        with (
            patch.object(dispatcher_wake_replay, "_gh_api", side_effect=replay_api),
            patch.object(dispatcher_wake_replay, "is_copilot_session_active_via_agent_task", return_value=False),
            patch.object(
                dispatcher_wake_replay,
                "_reconcile_due_probes_and_check_availability",
                return_value=(0, True, "available"),
            ),
            patch.object(provider, "list_eligible_prs", return_value=[type("PR", (), {"number": 42})()]),
            patch.object(dispatcher_throttle, "run_safe", side_effect=throttle_api),
        ):
            _exercise_replay(clock, provider, posts, raw)
