"""Tests for ai-pr-loop-throttler.yml workflow structure (PR Scheduler)."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP_THROTTLER = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-throttler.yml"


class TestAiPrLoopThrottler:
    """Validates ai-pr-loop-throttler workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP_THROTTLER.exists()

    def test_has_workflow_dispatch_trigger(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "workflow_dispatch:" in content

    def test_has_no_schedule_trigger(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "schedule:" not in content

    def test_has_required_permissions(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "contents: read" in content
        assert "actions: read" in content

    def test_has_timeout_minutes_6(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "timeout-minutes: 6" in content

    def test_has_concurrency_group(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "group: ai-pr-loop-throttler" in content
        assert "cancel-in-progress: false" in content

    def test_uses_speckit_pr_token(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "SPECKIT_PR_TOKEN" in content

    def test_invokes_scheduler_command(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "agdt-ai-pr-loop-scheduler" in content

    def test_passes_repo_variable_writer_pat(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "REPO_VARIABLE_WRITER_PAT" in content

    def test_has_dry_run_support(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "DRY_RUN" in content

    def test_has_step_summary_output(self) -> None:
        """The scheduler command writes GITHUB_STEP_SUMMARY internally."""
        # The workflow invokes agdt-ai-pr-loop-scheduler which handles summary
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "agdt-ai-pr-loop-scheduler" in content

    def test_only_has_workflow_dispatch_trigger(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        # YAML parses 'on' as True, so use True as key
        triggers = set(parsed[True].keys()) if isinstance(parsed[True], dict) else set()
        assert triggers == {"workflow_dispatch"}

    def test_valid_yaml(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert "jobs" in parsed
        assert "schedule-next-pr" in parsed["jobs"]

    def test_workflow_is_at_most_60_lines(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        assert line_count <= 60, f"Workflow has {line_count} lines, expected ≤60"

    def test_installs_agentic_devtools(self) -> None:
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "uv pip install --system ." in content
        assert "python -m pip install ." in content

    def test_caches_dependency_installs(self) -> None:
        """Both install paths (uv and pip) must be cached to keep run duration low."""
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        assert "cache: 'pip'" in content
        assert "enable-cache: true" in content
        assert "cache-dependency-glob: 'pyproject.toml'" in content

    def test_no_inline_bash_logic(self) -> None:
        """Workflow should delegate to Python — no complex bash."""
        content = AI_PR_LOOP_THROTTLER.read_text(encoding="utf-8")
        # Should NOT contain bash constructs from the old implementation
        assert "while IFS=" not in content
        assert "gh api graphql" not in content
        assert "DISPATCHES=" not in content
