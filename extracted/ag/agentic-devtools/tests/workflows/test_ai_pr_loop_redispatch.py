"""Tests for ai-pr-loop-redispatch.yml workflow structure."""

import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP_REDISPATCH = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-redispatch.yml"


class TestAiPrLoopRedispatch:
    """Validates ai-pr-loop-redispatch workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP_REDISPATCH.exists()

    def test_valid_yaml(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert "jobs" in parsed
        assert "smart-redispatch" in parsed["jobs"]

    def test_has_only_workflow_dispatch_trigger(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        triggers = set(parsed[True].keys()) if isinstance(parsed[True], dict) else set()
        assert triggers == {"workflow_dispatch"}

    def test_has_required_permissions(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "actions: write" in content
        assert "pull-requests: read" in content
        assert "contents: read" in content

    def test_has_concurrency_group_with_cancel(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "group: ai-pr-loop-redispatch" in content
        assert "cancel-in-progress: false" in content

    def test_has_timeout_minutes_8(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "timeout-minutes: 8" in content

    def test_uses_stop_condition_default_workflow_token(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        check_step = content[
            content.index("- name: Check stop conditions") : content.index("- name: Wait until safe to dispatch")
        ]
        assert "GH_TOKEN: ${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}" in check_step
        assert "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT: ${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}" in check_step
        assert "select_pr_read_token" not in check_step

    def test_uses_default_workflow_pat(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT" in content

    def test_uses_default_workflow_pat_for_final_dispatch(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        dispatch_step = content[content.index("- name: Dispatch ai-pr-loop-throttler") :]
        assert "GH_TOKEN: ${{ secrets.DEFAULT_CLASSIC_REPO_WORKFLOW_PAT }}" in dispatch_step
        assert "FALLBACK_GH_TOKEN" not in dispatch_step

    def test_checks_for_eligible_open_prs(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-stop-conditions" in content

    def test_checks_24_hour_stale_merge_guard(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "24" in content
        assert "--default-branch" in content

    def test_delegates_cooldown_timing_to_watchdog(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-wait" in content
        assert 'while [ "$remaining" -gt 0 ]' not in content

    def test_sleeps_before_dispatch(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-wait" in content

    def test_wait_step_keeps_writer_pat_for_cooldown_variable_reads(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        timing_step = content[
            content.index("- name: Wait until safe to dispatch") : content.index(
                "- name: Dispatch ai-pr-loop-throttler"
            )
        ]
        assert "REPO_VARIABLE_WRITER_PAT: ${{ secrets.REPO_VARIABLE_WRITER_PAT }}" in timing_step

    def test_dispatches_ai_pr_loop_throttler(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "--mode redispatch-dispatch-throttler" in content
        assert "default_branch" in content

    def test_stop_conditions_are_guarded(self) -> None:
        """Stop condition steps only run when should_dispatch is true."""
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "steps.check.outputs.should_dispatch == 'true'" in content

    def test_exits_cleanly_on_no_eligible_prs(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "No eligible open PRs" in content

    def test_exits_cleanly_on_stale_main(self) -> None:
        content = AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8")
        assert "human intervention" in content

    def test_stop_conditions_run_before_cooldown_wait(self) -> None:
        """Stop conditions are checked before the cooldown wait to avoid wasting Actions time."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["smart-redispatch"]["steps"]
        step_ids = [s.get("id", "") for s in steps]
        check_idx = step_ids.index("check")
        timing_idx = step_ids.index("timing")
        assert check_idx < timing_idx, "stop-condition 'check' step must precede 'timing' wait step"

    def test_cooldown_wait_gated_on_stop_conditions(self) -> None:
        """Cooldown wait only runs when stop conditions allow dispatch."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["smart-redispatch"]["steps"]
        timing_step = next(s for s in steps if s.get("id") == "timing")
        assert "steps.check.outputs.should_dispatch == 'true'" in (timing_step.get("if") or "")

    def test_does_not_duplicate_a_shell_cooldown_gate(self) -> None:
        """Redispatch defers cooldown parsing to the watchdog wait command."""
        parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
        step_ids = [step.get("id", "") for step in parsed["jobs"]["smart-redispatch"]["steps"]]
        assert "cooldown-gate" not in step_ids

    def test_uses_default_token_for_inventory_queries(self, tmp_path: Path) -> None:
        """A capable default PAT is used for probe and inventory checks."""
        result, calls, output = _run_check_script(tmp_path, "success")

        assert result.returncode == 0
        assert calls == [("api", "default-token-value")] * 3
        assert output == "should_dispatch=true\n"

    def test_fails_closed_when_default_token_is_unauthorized(self, tmp_path: Path) -> None:
        """Authorization rejection for the default PAT does not trigger cross-role fallback."""
        result, calls, output = _run_check_script(tmp_path, "auth")

        assert result.returncode == 0
        assert calls == [("api", "default-token-value")]
        assert output == "should_dispatch=false\n"
        diagnostic = result.stdout + result.stderr
        assert "inventory probe failed for the default repository-workflow credential" in diagnostic
        assert "default-token-value" not in diagnostic

    def test_fails_closed_on_non_authorization_probe_failure(self, tmp_path: Path) -> None:
        """A non-authorization probe failure does not trigger fallback."""
        result, calls, output = _run_check_script(tmp_path, "error")

        assert result.returncode == 0
        assert calls == [("api", "default-token-value")]
        assert output == "should_dispatch=false\n"
        assert "inventory probe failed" in result.stdout

    def test_fails_closed_on_malformed_probe_response(self, tmp_path: Path) -> None:
        """A successful but malformed probe response cannot enable redispatch."""
        result, calls, output = _run_check_script(tmp_path, "malformed")

        assert result.returncode == 0
        assert calls == [("api", "default-token-value")]
        assert output == "should_dispatch=false\n"
        assert "malformed response" in result.stdout


def _run_check_script(
    tmp_path: Path,
    token_behavior: str,
) -> tuple[subprocess.CompletedProcess[str], list[tuple[str, str]], str]:
    """Execute the workflow check step against deterministic fake commands."""
    parsed = yaml.safe_load(AI_PR_LOOP_REDISPATCH.read_text(encoding="utf-8"))
    check_step = next(step for step in parsed["jobs"]["smart-redispatch"]["steps"] if step.get("id") == "check")
    script = check_step["run"].replace("${{ github.event.repository.default_branch }}", "main")
    recent_merge = (datetime.now(UTC) - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    fake_gh = tmp_path / "gh"
    fake_gh.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
printf '%s %s\\n' "$1" "${GH_TOKEN}" >> "$GH_CALL_LOG"
if [[ "$1" == "api" ]]; then
  if [[ "$*" == *"state=open&per_page=100"* ]]; then
    printf '%s\\n' \
      '[{"labels":[],"number":1,"base":{"repo":{"full_name":"owner/repo"}},"head":{"repo":{"full_name":"owner/repo"}}}]'
  elif [[ "$*" == *"state=open&per_page=1"* ]]; then
    case "DEFAULT_BEHAVIOR" in
      auth)
        printf 'HTTP/2.0 403 Forbidden\\n' >&2
        printf 'GraphQL: Resource not accessible by personal access token (repository.pullRequests)\\n' >&2
        exit 1
        ;;
      error)
        printf 'network retry delayed 403 seconds\\n' >&2
        exit 1
        ;;
      malformed)
        printf 'not-json\\n'
        exit 0
        ;;
    esac
    printf '[]\\n'
  elif [[ "$*" == *"state=closed"* ]]; then
    printf '[{"updated_at":"RECENT_MERGE","merged_at":"RECENT_MERGE"}]\\n'
  fi
fi
""".replace("RECENT_MERGE", recent_merge).replace("DEFAULT_BEHAVIOR", token_behavior),
        encoding="utf-8",
    )
    fake_gh.chmod(0o755)
    fake_watchdog = tmp_path / "agdt-ai-pr-loop-watchdog"
    fake_watchdog.write_text(
        """#!/usr/bin/env bash
set -euo pipefail
python -c '
import sys
from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command
sys.argv = ["watchdog", *sys.argv[1:]]
ai_pr_loop_watchdog_command()
' "$@"
""",
        encoding="utf-8",
    )
    fake_watchdog.chmod(0o755)
    output_path = tmp_path / "github-output"
    call_log = tmp_path / "gh-calls"
    env = {
        **os.environ,
        "PATH": f"{tmp_path}{os.pathsep}{os.environ['PATH']}",
        "GITHUB_OUTPUT": str(output_path),
        "GITHUB_REPOSITORY": "owner/repo",
        "GH_CALL_LOG": str(call_log),
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token-value",
        "GH_TOKEN": "default-token-value",
    }
    result = subprocess.run(
        ["bash", "-c", script],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    calls: list[tuple[str, str]] = []
    if call_log.exists():
        for line in call_log.read_text(encoding="utf-8").splitlines():
            parts = line.split(" ", 1)
            assert len(parts) == 2
            calls.append((parts[0], parts[1]))
    output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    return result, calls, output
