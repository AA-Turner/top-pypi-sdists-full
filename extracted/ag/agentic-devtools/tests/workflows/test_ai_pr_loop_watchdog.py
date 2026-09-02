"""Tests for ai-pr-loop-watchdog.yml workflow structure."""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_PR_LOOP_WATCHDOG = REPO_ROOT / ".github" / "workflows" / "ai-pr-loop-watchdog.yml"


class TestAiPrLoopWatchdog:
    """Validates ai-pr-loop-watchdog workflow structure and requirements."""

    def test_workflow_file_exists(self) -> None:
        assert AI_PR_LOOP_WATCHDOG.exists()

    def test_has_schedule_and_workflow_dispatch_triggers(self) -> None:
        content = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content) or {}
        on_section = parsed.get(True) if isinstance(parsed, dict) else None
        if on_section is None and isinstance(parsed, dict):
            on_section = parsed.get("on")
        triggers = on_section if isinstance(on_section, dict) else {}
        assert "workflow_dispatch" in triggers
        assert "schedule" in triggers
        schedules = triggers["schedule"]
        assert isinstance(schedules, list)
        assert schedules[0]["cron"] == "*/20 * * * *"

    def test_has_required_permissions(self) -> None:
        content = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")
        assert "contents: read" in content
        assert "actions: write" in content
        assert "pull-requests: read" in content

    def test_has_concurrency_group(self) -> None:
        content = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")
        assert "group: ai-pr-loop-watchdog" in content
        assert "cancel-in-progress: false" in content

    def test_uses_speckit_pr_token(self) -> None:
        content = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")
        assert "SPECKIT_PR_TOKEN" in content
        assert "REPO_VARIABLE_WRITER_PAT" in content

    def test_delegates_to_watchdog_cli(self) -> None:
        content = AI_PR_LOOP_WATCHDOG.read_text(encoding="utf-8")
        assert "agdt-ai-pr-loop-watchdog" in content
        assert '--repo "${{ github.repository }}"' in content
