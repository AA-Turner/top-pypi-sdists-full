"""Workflow contract tests for the AI PR Loop dispatcher."""

import re
from pathlib import Path
from typing import Any, cast

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = REPO_ROOT / ".github/workflows/ai-pr-loop-dispatcher.yml"
AI_PR_LOOP_WORKFLOW = REPO_ROOT / ".github/workflows/ai-pr-loop.yml"


def _dispatcher_steps() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return workflow, workflow["jobs"]["dispatch-monitor"]["steps"]


def _named_step(steps: list[dict[str, Any]], name: str) -> dict[str, Any]:
    return next(step for step in steps if step.get("name") == name)


def test_ai_pr_loop_dispatcher_uses_default_workflow_pat_for_throttle_and_dispatch() -> None:
    workflow, steps = _dispatcher_steps()

    throttle = _named_step(steps, "Throttle check")
    expected_throttle_env = {
        "GH_TOKEN": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "AGDT_GITHUB_SECRETS_JSON": "${{ toJSON(secrets) }}",
        "REPO_VARIABLE_WRITER_PAT": "${{ secrets.REPO_VARIABLE_WRITER_PAT }}",
        "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        "DEFAULT_BRANCH": "${{ github.event.repository.default_branch }}",
    }
    assert throttle["env"] == expected_throttle_env
    assert "gh api " not in throttle["run"]
    assert throttle["run"] == 'agdt-ai-pr-loop-dispatcher-wakeup --mode check --default-branch "$DEFAULT_BRANCH"'

    dispatch = _named_step(steps, "Dispatch AI PR Loop Throttler")
    assert dispatch["env"] == {
        "GH_TOKEN": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "AGDT_GITHUB_SECRETS_JSON": "${{ toJSON(secrets) }}",
        "REPO_VARIABLE_WRITER_PAT": "${{ secrets.REPO_VARIABLE_WRITER_PAT }}",
        "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        "DEFAULT_BRANCH": "${{ github.event.repository.default_branch }}",
    }
    assert dispatch["run"] == 'agdt-ai-pr-loop-dispatcher-wakeup --mode dispatch --default-branch "$DEFAULT_BRANCH"'
    assert dispatch["if"] == "github.event.action != 'synchronize' && steps.throttle.outputs.throttled != 'true'"
    assert workflow["permissions"] == {"actions": "write"}
    assert workflow["concurrency"]["cancel-in-progress"] is False
    workflow_on = workflow.get("on")
    if workflow_on is None:
        workflow_on = cast(dict[Any, Any], workflow)[True]
    assert workflow_on == {
        "pull_request_target": {
            "types": [
                "opened",
                "synchronize",
                "reopened",
                "labeled",
                "unlabeled",
                "ready_for_review",
                "review_requested",
                "closed",
            ]
        }
    }


def test_synchronize_concurrency_preserves_distinct_prs_and_coalesces_pending_heads() -> None:
    workflow, _ = _dispatcher_steps()
    concurrency = workflow["concurrency"]
    group = concurrency["group"]
    assert concurrency == {
        "group": (
            "${{ github.event_name == 'pull_request_target' && github.event.action == 'synchronize' "
            "&& format('ai-pr-loop-dispatcher-pr-{0}', github.event.pull_request.number) "
            "|| 'ai-pr-loop-dispatcher' }}"
        ),
        "cancel-in-progress": False,
    }
    assert "github.event.pull_request.number" in group
    assert "head" not in group
    assert "run_id" not in group
    match = re.fullmatch(
        r"\$\{\{ github.event_name == '([^']+)' && github.event.action == '([^']+)' "
        r"&& format\('([^']+)', github.event.pull_request.number\) \|\| '([^']+)' \}\}",
        group,
    )
    assert match is not None
    event_name, event_action, template, fallback = match.groups()

    def group_for(name: str, action: str, pr_number: int) -> str:
        return template.format(pr_number) if name == event_name and action == event_action else fallback

    pending: dict[str, str] = {}
    first_pr = group_for("pull_request_target", "synchronize", 101)
    second_pr = group_for("pull_request_target", "synchronize", 202)
    pending[first_pr] = "first-head"
    pending[second_pr] = "other-pr-head"
    assert pending == {
        "ai-pr-loop-dispatcher-pr-101": "first-head",
        "ai-pr-loop-dispatcher-pr-202": "other-pr-head",
    }
    pending[group_for("pull_request_target", "synchronize", 101)] = "newest-head"
    assert pending == {
        "ai-pr-loop-dispatcher-pr-101": "newest-head",
        "ai-pr-loop-dispatcher-pr-202": "other-pr-head",
    }
    for action in ("opened", "reopened", "labeled", "unlabeled", "ready_for_review", "review_requested", "closed"):
        for pr_number in (101, 202):
            assert group_for("pull_request_target", action, pr_number) == "ai-pr-loop-dispatcher"
    assert group_for("pull_request", "synchronize", 101) == "ai-pr-loop-dispatcher"


def test_throttle_policy_is_installed_and_invoked_through_the_cli() -> None:
    _, steps = _dispatcher_steps()
    names = [step.get("name") for step in steps]
    throttle_step = _named_step(steps, "Throttle check")
    install_step = _named_step(steps, "Install agentic-devtools")

    assert names.index("Install agentic-devtools") < names.index("Throttle check")
    assert "uv pip install --system ." in install_step["run"]
    assert "python -m pip install ." in install_step["run"]
    assert throttle_step["run"] == 'agdt-ai-pr-loop-dispatcher-wakeup --mode check --default-branch "$DEFAULT_BRANCH"'


def test_synchronize_dispatch_targets_event_pr_and_head() -> None:
    workflow, steps = _dispatcher_steps()
    synchronize = _named_step(steps, "Dispatch AI PR Loop for synchronize")
    names = [step.get("name") for step in steps]

    assert synchronize["if"] == ("github.event_name == 'pull_request_target' && github.event.action == 'synchronize'")
    assert synchronize["run"].strip() == (
        "gh workflow run ai-pr-loop.yml \\\n"
        '  --repo "$GITHUB_REPOSITORY" \\\n'
        '  --ref "${{ github.event.repository.default_branch }}" \\\n'
        '  -f pr_number="${{ github.event.pull_request.number }}" \\\n'
        '  -f head_sha="${{ github.event.pull_request.head.sha }}"'
    )
    assert synchronize["env"] == {
        "GH_TOKEN": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}",
        "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
    }
    assert names.index("Install agentic-devtools") < names.index(synchronize["name"])
    assert names.index(synchronize["name"]) < names.index("Throttle check")
    assert workflow["permissions"] == {"actions": "write"}


def test_synchronize_dispatch_bypasses_recent_global_throttle() -> None:
    _, steps = _dispatcher_steps()
    synchronize = _named_step(steps, "Dispatch AI PR Loop for synchronize")
    ordinary = _named_step(steps, "Dispatch AI PR Loop Throttler")

    assert synchronize["if"] == ("github.event_name == 'pull_request_target' && github.event.action == 'synchronize'")
    assert "steps.throttle.outputs" not in synchronize["if"]
    assert "github.event.pull_request.number" in synchronize["run"]
    assert "github.event.pull_request.head.sha" in synchronize["run"]
    assert ordinary["if"] == "github.event.action != 'synchronize' && steps.throttle.outputs.throttled != 'true'"

    for throttled in ("true", "false"):
        event_name = "pull_request_target"
        event_action = "synchronize"
        targeted_route_enabled = event_name == "pull_request_target" and event_action == "synchronize"
        ordinary_route_enabled = event_action != "synchronize" and throttled != "true"
        assert targeted_route_enabled
        assert not ordinary_route_enabled


@pytest.mark.parametrize(
    "event_action",
    ("opened", "reopened", "labeled", "unlabeled", "ready_for_review", "review_requested", "closed"),
)
@pytest.mark.parametrize("throttled", ("true", "false"))
def test_unrelated_event_remains_on_global_throttle_path(event_action: str, throttled: str) -> None:
    _, steps = _dispatcher_steps()
    synchronize = _named_step(steps, "Dispatch AI PR Loop for synchronize")
    ordinary = _named_step(steps, "Dispatch AI PR Loop Throttler")

    assert synchronize["if"] == ("github.event_name == 'pull_request_target' && github.event.action == 'synchronize'")
    assert ordinary["if"] == "github.event.action != 'synchronize' && steps.throttle.outputs.throttled != 'true'"
    assert event_action != "synchronize"
    targeted_route_enabled = event_action == "synchronize"
    ordinary_route_enabled = event_action != "synchronize" and throttled != "true"
    assert not targeted_route_enabled
    assert ordinary_route_enabled is (throttled == "false")
    assert ordinary["run"] == ('agdt-ai-pr-loop-dispatcher-wakeup --mode dispatch --default-branch "$DEFAULT_BRANCH"')


def test_targeted_dispatch_preserves_existing_consumer_guards() -> None:
    _, dispatcher_steps = _dispatcher_steps()
    synchronize = _named_step(dispatcher_steps, "Dispatch AI PR Loop for synchronize")
    consumer = yaml.safe_load(AI_PR_LOOP_WORKFLOW.read_text(encoding="utf-8"))
    consumer_on = consumer.get("on")
    if consumer_on is None:
        consumer_on = cast(dict[Any, Any], consumer)[True]
    inputs = consumer_on["workflow_dispatch"]["inputs"]

    assert inputs["pr_number"] == {"required": True, "type": "string"}
    assert inputs["head_sha"] == {"required": False, "type": "string"}
    assert {"trigger_reason", "operation_id"} <= inputs.keys()
    assert consumer["concurrency"] == {
        "group": "ai-pr-loop-${{ inputs.pr_number }}",
        "cancel-in-progress": False,
    }

    consumer_steps = consumer["jobs"]["ai-pr-loop"]["steps"]
    cooldown = _named_step(consumer_steps, "Check provider cooldown gate")
    run_loop = next(step for step in consumer_steps if step.get("id") == "run-loop")
    assert cooldown["id"] == "cooldown-gate"
    assert "cooldown-gate" in run_loop["if"]
    assert "cooldown_active != 'true'" in run_loop["if"]
    assert "dispatch-pr.outputs.pr_open == 'true'" in run_loop["if"]
    assert synchronize["run"].splitlines() == [
        "gh workflow run ai-pr-loop.yml \\",
        '  --repo "$GITHUB_REPOSITORY" \\',
        '  --ref "${{ github.event.repository.default_branch }}" \\',
        '  -f pr_number="${{ github.event.pull_request.number }}" \\',
        '  -f head_sha="${{ github.event.pull_request.head.sha }}"',
    ]
