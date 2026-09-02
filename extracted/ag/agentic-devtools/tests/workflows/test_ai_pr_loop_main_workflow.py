"""Tests for ai-pr-loop.yml workflow structure."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop.yml"


class TestAiPrLoopMainWorkflow:
    """Validates ai-pr-loop.yml workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP.exists()

    def test_valid_yaml(self) -> None:
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        assert parsed is not None
        assert "jobs" in parsed
        assert "ai-pr-loop" in parsed["jobs"]

    def test_has_cooldown_gate_step(self) -> None:
        """An early provider-cooldown gate runs before PR-token provider calls."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        gate_idx = next(i for i, step in enumerate(steps) if step.get("id") == "cooldown-gate")
        dispatch_idx = next(i for i, step in enumerate(steps) if step.get("id") == "dispatch-pr")
        assert gate_idx < dispatch_idx, "cooldown-gate must run before PR-token provider work"

    def test_cooldown_gate_uses_writer_token(self) -> None:
        """Gate reads cooldown variable with the writer PAT, not the PR token."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "REPO_VARIABLE_WRITER_PAT" in content
        assert "--mode" in content
        assert "cooldown-gate" in content

    def test_cooldown_gate_checks_all_loop_credentials(self) -> None:
        """Any active loop-credential cooldown must block provider work."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "AI_PR_LOOP_CREDENTIAL_IDENTITY: SPECKIT_PR_TOKEN" in content

    def test_cooldown_gate_uses_python_command(self) -> None:
        """The workflow delegates cooldown parsing to the Python watchdog command."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "python -m pip install --disable-pip-version-check -q jinja2" in content
        assert "from agentic_devtools.cli.ci.watchdog_command import ai_pr_loop_watchdog_command" in content
        assert '"cooldown-gate"' in content

    def test_provider_steps_gated_on_cooldown(self) -> None:
        """Resolve PR ref and checkout are skipped while a cooldown is active."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        gate_condition = "steps.cooldown-gate.outputs.cooldown_active != 'true'"
        gated_ids = {s.get("id") or s.get("name", "") for s in steps if gate_condition in (s.get("if") or "")}
        assert "dispatch-pr" in gated_ids, "Resolve PR head ref step must be gated on cooldown-gate"
        assert "run-loop" in gated_ids, "Run AI PR loop orchestrator step must be gated on cooldown-gate"

    def test_redispatch_step_always_runs(self) -> None:
        """Redispatch fires even when the cooldown gate blocks provider work."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        steps = parsed["jobs"]["ai-pr-loop"]["steps"]
        dispatch_step = next(
            (s for s in steps if "Dispatch AI PR Loop Redispatch" in s.get("name", "")),
            None,
        )
        assert dispatch_step is not None
        assert (dispatch_step.get("if") or "").strip() == "always()"

    def test_redispatch_uses_writer_pat_after_gate_or_rate_limit_pause(self) -> None:
        """Redispatch falls back to the writer PAT when the PR token should not be reused."""
        content = AI_PR_LOOP.read_text(encoding="utf-8")
        assert "COOLDOWN_ACTIVE: ${{ steps.cooldown-gate.outputs.cooldown_active }}" in content
        assert "LOOP_EXIT_CODE: ${{ steps.run-loop.outputs.exit_code }}" in content
        assert 'export GH_TOKEN="${REPO_VARIABLE_WRITER_PAT}"' in content

    def test_loop_concurrency_is_scoped_to_the_selected_pr(self) -> None:
        """A loop run for one PR must not replace a pending run for another PR."""
        parsed = yaml.safe_load(AI_PR_LOOP.read_text(encoding="utf-8"))
        assert parsed["concurrency"]["group"] == "ai-pr-loop-${{ inputs.pr_number }}"
