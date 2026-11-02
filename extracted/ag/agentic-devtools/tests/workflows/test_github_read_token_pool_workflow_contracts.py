"""Workflow contracts for step-scoped GitHub read-token pool access."""

import importlib.util
import re
import shlex
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import Mock

import yaml

from agentic_devtools.cli.ci import dispatcher_wakeup, github_provider

WORKFLOW_DIR = Path(".github/workflows")
SECRETS_ENV = "${{ toJSON(secrets) }}"
FILTERED_SECRETS_ENV = "${{ steps.dispatch-pr.outputs.read_token_secrets }}"
THROTTLER_FILTERED_SECRETS_ENV = "${{ steps.schedule.outputs.read_token_secrets }}"
REQUIRED_PROVIDER_STEPS = {
    "ai-pr-loop.yml": {
        "Check provider cooldown gate",
        "Resolve PR head ref",
        "run-loop",
        "Dispatch AI PR Loop Redispatch",
    },
    "ai-pr-loop-dispatcher.yml": {"Throttle check", "Dispatch AI PR Loop Throttler"},
    "ai-pr-loop-redispatch.yml": {
        "Check stop conditions",
        "Wait until safe to dispatch",
        "Dispatch ai-pr-loop-throttler",
    },
    "ai-pr-loop-watchdog.yml": {"Restart stalled ai-pr-loop when eligible PRs exist"},
    "ai-pr-loop-throttler.yml": {"Select and dispatch next PR(s)"},
    "ai-pr-loop-trusted-events.yml": {"Run live reconciliation preflight"},
    "ai-pr-loop-supervisor.yml": {"Run read-only supervisor scan"},
    "speckit-phase-progression.yml": {
        "Cloud Agent In-Flight Guard",
        "Cascade Trigger (Final Phase Complete)",
        "Cascade Trigger (Final Phase Skipped)",
        "Dispatch Cloud Agent",
        "Pre-Push Draft Existing PR for Advisory Artifact Gate",
        "Create Pull Request",
        "Request Copilot Fix for Artifact Violations",
    },
}


def _steps(workflow: dict) -> list[dict]:
    return [step for job in workflow["jobs"].values() for step in job.get("steps", [])]


def test_provider_steps_receive_secrets_json_only_at_step_scope() -> None:
    for workflow_name, required_names in REQUIRED_PROVIDER_STEPS.items():
        workflow = yaml.safe_load((WORKFLOW_DIR / workflow_name).read_text(encoding="utf-8"))
        assert "AGDT_GITHUB_SECRETS_JSON" not in workflow.get("env", {})
        for job in workflow["jobs"].values():
            assert "AGDT_GITHUB_SECRETS_JSON" not in job.get("env", {})
        steps = _steps(workflow)
        by_name = {step.get("name", step.get("id")): step for step in steps}

        for step_name in required_names:
            assert step_name in by_name, f"{workflow_name} is missing provider step {step_name!r}"
            step = by_name[step_name]
            expected_secrets_env = (
                FILTERED_SECRETS_ENV
                if (workflow_name == "ai-pr-loop.yml" and step_name in {"run-loop", "Dispatch AI PR Loop Redispatch"})
                or (workflow_name == "ai-pr-loop-throttler.yml" and step_name == "Continue retry liveness polling")
                else SECRETS_ENV
            )
            assert step.get("env", {}).get("AGDT_GITHUB_SECRETS_JSON") == expected_secrets_env

        for step in steps:
            env = step.get("env", {})
            if "AGDT_GITHUB_SECRETS_JSON" in env:
                assert env["AGDT_GITHUB_SECRETS_JSON"] in {
                    SECRETS_ENV,
                    FILTERED_SECRETS_ENV,
                    THROTTLER_FILTERED_SECRETS_ENV,
                }
                assert env.get("REPO_VARIABLE_WRITER_PAT") == "${{ secrets.REPO_VARIABLE_WRITER_PAT }}"
                assert "run" in step
            run = step.get("run", "")
            if re.search(r"\bagdt-[a-z0-9-]+", run):
                assert env.get("AGDT_GITHUB_SECRETS_JSON") in {
                    SECRETS_ENV,
                    FILTERED_SECRETS_ENV,
                    THROTTLER_FILTERED_SECRETS_ENV,
                }, (
                    f"{workflow_name} step {step.get('name', step.get('id'))!r} "
                    "runs an agdt command without the scoped secrets JSON"
                )


def test_ai_pr_loop_keeps_pooled_credentials_out_of_pr_head_code() -> None:
    workflow = yaml.safe_load((WORKFLOW_DIR / "ai-pr-loop.yml").read_text(encoding="utf-8"))
    steps = _steps(workflow)
    dispatch_index = next(i for i, step in enumerate(steps) if step.get("id") == "dispatch-pr")
    workflow_checkout = next(step for step in steps if step.get("name") == "Checkout workflow sources")
    run_loop = next(step for step in steps if step.get("id") == "run-loop")
    redispatch = next(step for step in steps if step.get("name") == "Dispatch AI PR Loop Redispatch")
    dispatch = steps[dispatch_index]

    assert workflow_checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
    assert not any(
        step.get("uses") == "actions/checkout@v4"
        and step.get("with", {}).get("ref") == "${{ steps.dispatch-pr.outputs.head_ref }}"
        for step in steps
    )
    assert not any("-e ." in step.get("run", "") for step in steps)
    assert dispatch["env"]["AGDT_GITHUB_SECRETS_JSON"] == SECRETS_ENV
    assert 'endswith("_SWICA_CLASSIC_REPO_WORKFLOW_PAT")' in dispatch["run"]
    assert "read_token_secrets=${read_token_secrets}" in dispatch["run"]
    assert run_loop["env"]["AGDT_GITHUB_SECRETS_JSON"] == FILTERED_SECRETS_ENV
    assert run_loop["env"]["AGDT_GITHUB_SECRETS_JSON"] != SECRETS_ENV
    assert redispatch["env"]["AGDT_GITHUB_SECRETS_JSON"] == FILTERED_SECRETS_ENV
    assert redispatch["env"]["AGDT_GITHUB_SECRETS_JSON"] != SECRETS_ENV


def test_throttler_filters_pooled_secrets_before_liveness_polling() -> None:
    workflow = yaml.safe_load((WORKFLOW_DIR / "ai-pr-loop-throttler.yml").read_text(encoding="utf-8"))
    steps = _steps(workflow)
    schedule = next(step for step in steps if step.get("id") == "schedule")
    polling = next(step for step in steps if step.get("name") == "Continue retry liveness polling")

    assert schedule["env"]["AGDT_GITHUB_SECRETS_JSON"] == SECRETS_ENV
    assert 'endswith("_SWICA_CLASSIC_REPO_WORKFLOW_PAT")' in schedule["run"]
    assert "read_token_secrets=${read_token_secrets}" in schedule["run"]
    assert polling["env"]["AGDT_GITHUB_SECRETS_JSON"] == THROTTLER_FILTERED_SECRETS_ENV


def test_workflow_read_calls_do_not_inherit_a_single_gh_credential() -> None:
    direct_read = re.compile(r"\bgh\s+(?:api\b|pr\s+(?:list|view)\b)")
    for workflow_name in REQUIRED_PROVIDER_STEPS:
        workflow_text = (WORKFLOW_DIR / workflow_name).read_text(encoding="utf-8")
        assert direct_read.search(workflow_text) is None, workflow_name

    spec_pr_script = Path(".github/scripts/speckit-trigger/create-spec-pr.sh").read_text(encoding="utf-8")
    assert "gh pr list --" not in spec_pr_script
    assert 'gh pr view "$pr_selector"' not in spec_pr_script
    assert 'gh api "/repos/${REPO_SLUG}/labels"' not in spec_pr_script
    assert 'python "$SCRIPT_DIR/pr-read-session.py"' in spec_pr_script
    reader_script = Path(".github/scripts/speckit-trigger/pr-read-session.py").read_text(encoding="utf-8")
    assert "from agentic_devtools.cli.ci.github_provider import _gh_api" in reader_script


def test_speckit_pre_push_combines_pr_lookup_and_state_read() -> None:
    workflow = (WORKFLOW_DIR / "speckit-phase-progression.yml").read_text(encoding="utf-8")
    assert 'operation:"find-open-pr-state"' in workflow
    assert "python .github/scripts/speckit-trigger/pr-read-session.py" in workflow
    assert "from agentic_devtools.cli.ci.github_provider import _gh_api" not in workflow
    error_guard = """if jq -e 'type == "object" and has("error")' <<<"$PR_STATE_JSON" >/dev/null; then"""
    assert error_guard in workflow
    assert workflow.index(error_guard) < workflow.index('EXISTING_PR_NUMBER="$(jq -r')

    reader_path = Path(".github/scripts/speckit-trigger/pr-read-session.py")
    spec = importlib.util.spec_from_file_location("pr_read_session", reader_path)
    assert spec is not None and spec.loader is not None
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)

    requests: list[str] = []

    def fake_gh_api(path: str) -> str:
        requests.append(path)
        if "?" in path:
            return '[{"number":123,"html_url":"https://github.com/swai-factory/agentic-devtools/pull/123"}]'
        return '{"draft":false,"labels":[{"name":"ai-auto-merge-allowed"}]}'

    setattr(reader, "_gh_api", fake_gh_api)
    result = reader._handle_request(
        {"operation": "find-open-pr-state", "repo": "swai-factory/agentic-devtools", "branch": "spec/123"}
    )

    assert result == {
        "number": 123,
        "isDraft": False,
        "labels": [{"name": "ai-auto-merge-allowed"}],
    }
    assert len(requests) == 2

    requests.clear()

    def no_open_pr(path: str) -> str:
        requests.append(path)
        return "[]"

    setattr(reader, "_gh_api", no_open_pr)
    assert (
        reader._handle_request(
            {"operation": "find-open-pr-state", "repo": "swai-factory/agentic-devtools", "branch": "spec/456"}
        )
        is None
    )
    assert len(requests) == 1

    for malformed_response in ("{}", "null", "false", "0"):
        setattr(reader, "_gh_api", lambda _path, response=malformed_response: response)
        try:
            reader._handle_request(
                {
                    "operation": "find-open-pr-state",
                    "repo": "swai-factory/agentic-devtools",
                    "branch": "spec/789",
                }
            )
        except ValueError as exc:
            assert "array" in str(exc)
        else:
            raise AssertionError(f"Malformed pull-list response was accepted: {malformed_response}")


def test_previous_phase_lookup_uses_pooled_reader_operation() -> None:
    reader_path = Path(".github/scripts/speckit-trigger/pr-read-session.py")
    spec = importlib.util.spec_from_file_location("pr_read_session_previous_phase", reader_path)
    assert spec is not None and spec.loader is not None
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)

    requests: list[str] = []

    def fake_gh_api(path: str) -> str:
        requests.append(path)
        return '{"items":[{"html_url":"https://github.com/swai-factory/agentic-devtools/pull/99"}]}'

    setattr(reader, "_gh_api", fake_gh_api)
    result = reader._handle_request(
        {
            "operation": "previous-phase-pr",
            "repo": "swai-factory/agentic-devtools",
            "phase": "1",
            "issue": "42",
        }
    )

    assert result == {"url": "https://github.com/swai-factory/agentic-devtools/pull/99"}
    assert len(requests) == 1
    assert requests[0].startswith("/search/issues?")


def test_python_readonly_gh_calls_use_the_shared_pooled_runner() -> None:
    provider_paths = (
        "agentic_devtools/cli/ci/job_logs.py",
        "agentic_devtools/cli/ci/supervision_control_command.py",
        "agentic_devtools/cli/ci/agent_task_inventory.py",
        "agentic_devtools/cli/speckit/hierarchy_detector.py",
    )
    for source_path in provider_paths:
        source = Path(source_path).read_text(encoding="utf-8")
        assert "_run_readonly_gh_command" in source, source_path


def test_supervisor_reads_through_the_shared_github_provider() -> None:
    source = Path("agentic_devtools/cli/ci/supervisor_command.py").read_text(encoding="utf-8")
    assert "GitHubActionsProvider" in source
    assert "list_workflow_runs" in source


def test_write_operations_keep_the_default_fixed_token(monkeypatch) -> None:
    dispatcher = yaml.safe_load((WORKFLOW_DIR / "ai-pr-loop-dispatcher.yml").read_text(encoding="utf-8"))
    dispatch_step = next(
        step
        for step in dispatcher["jobs"]["dispatch-monitor"]["steps"]
        if step.get("name") == "Dispatch AI PR Loop Throttler"
    )
    assert dispatch_step["env"]["AGDT_GITHUB_SECRETS_JSON"] == SECRETS_ENV
    command = shlex.split(dispatch_step["run"].replace('"$DEFAULT_BRANCH"', '"main"'))
    assert command == ["agdt-ai-pr-loop-dispatcher-wakeup", "--mode", "dispatch", "--default-branch", "main"]
    assert dispatch_step["env"]["GH_TOKEN"] == "${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}"
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/repo")
    monkeypatch.setenv("GH_TOKEN", "default-test-token")
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-test-token")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT":"pooled-test-token"}')
    request = Mock(return_value=CompletedProcess([], 0, "", ""))
    pool = Mock(side_effect=AssertionError("Workflow dispatch must not use pooled credentials"))
    monkeypatch.setattr(github_provider, "run_safe", request)
    monkeypatch.setattr(github_provider, "_call_with_read_token_pool", pool)
    dispatcher_wakeup.main(command[1:])
    args, kwargs = request.call_args
    assert args[0] == [
        "gh",
        "api",
        "/repos/owner/repo/actions/workflows/ai-pr-loop-throttler.yml/dispatches",
        "--method",
        "POST",
        "--include",
        "--input",
        "-",
    ]
    assert kwargs["input"] == '{"ref": "main"}'
    assert kwargs["env"]["GH_TOKEN"] == "default-test-token"
    assert "AGDT_GITHUB_SECRETS_JSON" not in kwargs["env"]
    request.assert_called_once()
    pool.assert_not_called()

    speckit = (WORKFLOW_DIR / "speckit-phase-progression.yml").read_text(encoding="utf-8")
    assert 'GH_TOKEN="$GH_TOKEN" gh pr ready "$EXISTING_PR_NUMBER" --undo' in speckit
    assert 'GH_TOKEN="$LABEL_TOKEN" gh pr edit "$EXISTING_PR_NUMBER"' in speckit
    spec_pr_script = Path(".github/scripts/speckit-trigger/create-spec-pr.sh").read_text(encoding="utf-8")
    assert 'gh pr create "${GH_CREATE_ARGS[@]}"' in spec_pr_script
    assert 'GH_TOKEN="$LABEL_TOKEN" gh pr edit' in spec_pr_script
