"""Integration tests: /spec REPL command rendering.

Drives the extracted _handle_spec_command() with captured Rich Console
output, following the test_repl_config.py pattern. Verifies the actual
text a user sees in the terminal for each /spec subcommand.
"""

from __future__ import annotations

import io
import re
from pathlib import Path
from typing import Any

import pytest

from anteroom.cli import renderer
from anteroom.cli.repl import _handle_spec_command

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""

VALID_BUGFIX_YAML = """\
mode: bugfix
requirements: |
  ## Current Behavior
  Widget crashes on empty input.
design: |
  ## Root Cause
  Missing null check.
tasks:
  - id: t1
    summary: Add null check
"""

UPDATED_SPEC_YAML = """\
requirements: |
  Must support widgets AND gadgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
  - id: t2
    summary: Add validation layer
    depends_on: [t1]
"""

FQN = "@ns/spec/feat"


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def spec(db: Any) -> dict[str, Any]:
    from anteroom.services.spec_service import create_spec

    return create_spec(db, "ns", "feat", VALID_SPEC_YAML)


@pytest.fixture()
def bugfix_spec(db: Any) -> dict[str, Any]:
    from anteroom.services.spec_service import create_spec

    return create_spec(db, "ns", "bugfix1", VALID_BUGFIX_YAML)


def _capture(user_input: str, *, cmd: str = "/spec", db: Any) -> str:
    """Run _handle_spec_command and capture Rich Console output, stripped of ANSI."""
    import asyncio

    buf = io.StringIO()
    console = __import__("rich.console", fromlist=["Console"]).Console(
        file=buf, width=120, force_terminal=True, color_system="truecolor"
    )
    original = renderer.console
    renderer.console = console
    try:
        asyncio.run(_handle_spec_command(user_input, cmd=cmd, db=db))
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


# ---------------------------------------------------------------------------
# /spec list and /specs
# ---------------------------------------------------------------------------


class TestSpecList:
    def test_list_empty(self, db: Any) -> None:
        output = _capture("/spec list", db=db)
        assert "No specs found" in output

    def test_list_shows_specs(self, db: Any, spec: dict) -> None:
        output = _capture("/spec list", db=db)
        assert "@ns/spec/feat" in output
        assert "requirements:draft" in output
        assert "design:draft" in output
        assert "tasks:draft" in output

    def test_specs_alias(self, db: Any, spec: dict) -> None:
        output = _capture("/specs", cmd="/specs", db=db)
        assert "@ns/spec/feat" in output

    def test_list_shows_approved_status(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, FQN, "requirements", "troy")
        output = _capture("/spec list", db=db)
        assert "requirements:approved" in output
        assert "design:draft" in output


# ---------------------------------------------------------------------------
# /spec show
# ---------------------------------------------------------------------------


class TestSpecShow:
    def test_show_displays_content(self, db: Any, spec: dict) -> None:
        output = _capture(f"/spec show {FQN}", db=db)
        assert "@ns/spec/feat" in output
        assert "Must support widgets" in output
        assert "widget parser pattern" in output
        assert "t1" in output
        assert "Implement widget parser" in output

    def test_show_displays_phases(self, db: Any, spec: dict) -> None:
        output = _capture(f"/spec show {FQN}", db=db)
        assert "requirements:" in output
        assert "draft" in output

    def test_show_displays_depends_on(self, db: Any, spec: dict) -> None:
        output = _capture(f"/spec show {FQN}", db=db)
        assert "depends: t1" in output

    def test_show_not_found(self, db: Any) -> None:
        output = _capture("/spec show @ns/spec/nope", db=db)
        assert "not found" in output.lower()

    def test_show_missing_fqn(self, db: Any) -> None:
        output = _capture("/spec show", db=db)
        assert "Usage" in output


# ---------------------------------------------------------------------------
# /spec approve
# ---------------------------------------------------------------------------


class TestSpecApprove:
    def test_approve_shows_success(self, db: Any, spec: dict) -> None:
        output = _capture(f"/spec approve {FQN} design", db=db)
        assert "Approved" in output
        assert "design" in output

    def test_approve_not_found(self, db: Any) -> None:
        output = _capture("/spec approve @ns/spec/nope design", db=db)
        assert "not found" in output.lower()

    def test_approve_missing_args(self, db: Any) -> None:
        output = _capture("/spec approve", db=db)
        assert "Usage" in output


# ---------------------------------------------------------------------------
# /spec unapprove
# ---------------------------------------------------------------------------


class TestSpecUnapprove:
    def test_unapprove_shows_success(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, FQN, "design", "troy")
        output = _capture(f"/spec unapprove {FQN} design", db=db)
        assert "Reset to draft" in output

    def test_unapprove_missing_args(self, db: Any) -> None:
        output = _capture("/spec unapprove", db=db)
        assert "Usage" in output


# ---------------------------------------------------------------------------
# /spec diff
# ---------------------------------------------------------------------------


class TestSpecDiff:
    def test_diff_shows_changes(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import update_spec_content

        update_spec_content(db, FQN, UPDATED_SPEC_YAML)
        output = _capture(f"/spec diff {FQN}", db=db)
        assert "Diff" in output
        assert "v1" in output
        assert "v2" in output
        assert "requirements" in output.lower()

    def test_diff_single_version(self, db: Any, spec: dict) -> None:
        output = _capture(f"/spec diff {FQN}", db=db)
        assert "nothing to diff" in output.lower()

    def test_diff_not_found(self, db: Any) -> None:
        output = _capture("/spec diff @ns/spec/nope", db=db)
        assert "not found" in output.lower()

    def test_diff_missing_fqn(self, db: Any) -> None:
        output = _capture("/spec diff", db=db)
        assert "Usage" in output


# ---------------------------------------------------------------------------
# /spec (unknown subcommand)
# ---------------------------------------------------------------------------


class TestSpecUsage:
    def test_unknown_subcommand(self, db: Any) -> None:
        output = _capture("/spec bogus", db=db)
        assert "Usage" in output
        assert "list" in output
        assert "show" in output

    def test_bare_spec_shows_list_when_empty(self, db: Any) -> None:
        output = _capture("/spec", db=db)
        assert "No specs found" in output


# ---------------------------------------------------------------------------
# Bugfix mode badges
# ---------------------------------------------------------------------------


class TestSpecBugfixBadges:
    def test_spec_show_bugfix_badge(self, db: Any, bugfix_spec: dict) -> None:
        output = _capture("/spec show @ns/spec/bugfix1", db=db)
        assert "[bugfix]" in output

    def test_spec_list_bugfix_badge(self, db: Any, bugfix_spec: dict) -> None:
        output = _capture("/spec list", db=db)
        assert "[bugfix]" in output

    def test_spec_list_feature_no_badge(self, db: Any, spec: dict) -> None:
        output = _capture("/spec list", db=db)
        assert "[bugfix]" not in output

    def test_spec_show_bugfix_phases_same(self, db: Any, bugfix_spec: dict) -> None:
        output = _capture("/spec show @ns/spec/bugfix1", db=db)
        assert "requirements:" in output
        assert "design:" in output
        assert "tasks:" in output
        assert "draft" in output

    def test_spec_create_bugfix_usage(self, db: Any) -> None:
        output = _capture("/spec create", db=db)
        assert "--bugfix" in output


# ---------------------------------------------------------------------------
# /spec queue
# ---------------------------------------------------------------------------


class TestSpecQueue:
    def test_queue_empty(self, db: Any) -> None:
        output = _capture("/spec queue", db=db)
        assert "up to date" in output.lower()

    def test_queue_shows_draft_spec(self, db: Any, spec: dict) -> None:
        output = _capture("/spec queue", db=db)
        assert "@ns/spec/feat" in output
        assert "draft" in output.lower()


# ---------------------------------------------------------------------------
# /spec links
# ---------------------------------------------------------------------------


class TestSpecLinks:
    def test_links_empty(self, db: Any, spec: dict) -> None:
        output = _capture("/spec links @ns/spec/feat", db=db)
        assert "no links" in output.lower()

    def test_links_no_fqn(self, db: Any) -> None:
        output = _capture("/spec links", db=db)
        assert "usage" in output.lower()


# ---------------------------------------------------------------------------
# /spec conformance
# ---------------------------------------------------------------------------


class TestSpecConformance:
    def test_conformance_no_runs(self, db: Any, spec: dict) -> None:
        output = _capture("/spec conformance @ns/spec/feat", db=db)
        assert "not conformant" in output.lower() or "task coverage" in output.lower()

    def test_conformance_no_fqn(self, db: Any) -> None:
        output = _capture("/spec conformance", db=db)
        assert "usage" in output.lower()

    def test_conformance_not_found(self, db: Any) -> None:
        output = _capture("/spec conformance @ns/spec/nope", db=db)
        assert "not found" in output.lower()


# ---------------------------------------------------------------------------
# /spec dashboard
# ---------------------------------------------------------------------------


class TestSpecDashboard:
    def test_dashboard_empty(self, db: Any) -> None:
        output = _capture("/spec dashboard", db=db)
        assert "No specs found" in output

    def test_dashboard_shows_spec(self, db: Any, spec: dict) -> None:
        output = _capture("/spec dashboard", db=db)
        assert "@ns/spec/feat" in output
        assert "draft" in output

    def test_dashboard_shows_approved_status(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, FQN, "requirements", "troy")
        approve_phase(db, FQN, "design", "troy")
        approve_phase(db, FQN, "tasks", "troy")
        output = _capture("/spec dashboard", db=db)
        assert "all_approved" in output

    def test_dashboard_filter_by_status(self, db: Any, spec: dict) -> None:
        output = _capture("/spec dashboard --status stale", db=db)
        assert "No specs found" in output

    def test_dashboard_filter_by_status_match(self, db: Any, spec: dict) -> None:
        output = _capture("/spec dashboard --status draft", db=db)
        assert "@ns/spec/feat" in output

    def test_dashboard_filter_by_phase(self, db: Any, spec: dict) -> None:
        from anteroom.services.spec_service import approve_phase

        approve_phase(db, FQN, "requirements", "troy")
        output = _capture("/spec dashboard --phase requirements --phase-status approved", db=db)
        assert "@ns/spec/feat" in output

    def test_dashboard_shows_totals(self, db: Any, spec: dict) -> None:
        output = _capture("/spec dashboard", db=db)
        assert "1 specs" in output or "1 spec" in output


# ---------------------------------------------------------------------------
# /spec create --prompt / --from-issue (#1165)
# ---------------------------------------------------------------------------


def _capture_with_config(
    user_input: str,
    *,
    cmd: str = "/spec",
    db: Any,
    config: Any = None,
) -> str:
    """Run _handle_spec_command with config and capture output."""
    import asyncio

    buf = io.StringIO()
    console = __import__("rich.console", fromlist=["Console"]).Console(
        file=buf, width=120, force_terminal=True, color_system="truecolor"
    )
    original = renderer.console
    renderer.console = console
    try:
        asyncio.run(_handle_spec_command(user_input, cmd=cmd, db=db, config=config))
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


class TestSpecCreatePrompt:
    def test_prompt_missing_args(self, db: Any) -> None:
        output = _capture("/spec create --prompt", db=db)
        assert "Usage" in output

    def test_prompt_missing_name(self, db: Any) -> None:
        output = _capture("/spec create --prompt text ns", db=db)
        assert "Usage" in output

    def test_prompt_no_config(self, db: Any) -> None:
        output = _capture_with_config("/spec create --prompt text ns feat", db=db, config=None)
        assert "config not available" in output.lower() or "AI config" in output

    def test_from_issue_missing_args(self, db: Any) -> None:
        output = _capture("/spec create --from-issue", db=db)
        assert "Usage" in output

    def test_from_issue_missing_name(self, db: Any) -> None:
        output = _capture("/spec create --from-issue 42 ns", db=db)
        assert "Usage" in output

    def test_prompt_happy_path_generate_save(self, db: Any) -> None:
        """Full generate-review-save flow: AI generates, editor is a no-op, spec is created."""
        import asyncio
        import json
        from unittest.mock import AsyncMock, MagicMock, patch

        ai_response = json.dumps(
            {
                "requirements": "Must add retry logic.",
                "design": "Use exponential backoff.",
                "tasks": [{"id": "t1", "summary": "Implement retry"}],
            }
        )
        mock_config = MagicMock()
        mock_ai = MagicMock()
        mock_ai.complete = AsyncMock(return_value=ai_response)

        buf = io.StringIO()
        console = __import__("rich.console", fromlist=["Console"]).Console(
            file=buf, width=120, force_terminal=True, color_system="truecolor"
        )
        original = renderer.console
        renderer.console = console
        try:
            with (
                patch("anteroom.services.ai_service.create_ai_service", return_value=mock_ai),
                patch("subprocess.run"),  # editor no-op
            ):
                asyncio.run(
                    _handle_spec_command(
                        "/spec create --prompt add-retry ns genfeat",
                        cmd="/spec",
                        db=db,
                        config=mock_config,
                    )
                )
        finally:
            renderer.console = original
        output = _ANSI_RE.sub("", buf.getvalue())
        assert "Generated spec" in output
        assert "Created" in output or "genfeat" in output

    def test_from_issue_happy_path_generate_save(self, db: Any) -> None:
        """Full from-issue flow: fetches issue, AI generates, editor no-op, spec saved."""
        import asyncio
        import json
        from unittest.mock import AsyncMock, MagicMock, patch

        issue_json = json.dumps(
            {
                "title": "Add retry logic",
                "body": "We need retry on API calls.",
                "labels": [{"name": "enhancement"}],
            }
        )
        ai_response = json.dumps(
            {
                "requirements": "Must add retry logic.",
                "design": "Use exponential backoff.",
                "tasks": [{"id": "t1", "summary": "Implement retry"}],
            }
        )
        mock_config = MagicMock()
        mock_ai = MagicMock()
        mock_ai.complete = AsyncMock(return_value=ai_response)

        mock_gh_proc = MagicMock()
        mock_gh_proc.returncode = 0
        mock_gh_proc.stdout = issue_json

        def _selective_run(cmd: Any, **kwargs: Any) -> Any:
            """Route gh calls to mock, editor calls to no-op."""
            if isinstance(cmd, list) and cmd[0] == "gh":
                return mock_gh_proc
            # Editor call — return success
            return MagicMock(returncode=0)

        buf = io.StringIO()
        console = __import__("rich.console", fromlist=["Console"]).Console(
            file=buf, width=120, force_terminal=True, color_system="truecolor"
        )
        original = renderer.console
        renderer.console = console
        try:
            with (
                patch("anteroom.services.ai_service.create_ai_service", return_value=mock_ai),
                patch("anteroom.services.spec_generator.subprocess.run", side_effect=_selective_run),
                patch("subprocess.run", side_effect=_selective_run),
            ):
                asyncio.run(
                    _handle_spec_command(
                        "/spec create --from-issue 42 ns issuefeat",
                        cmd="/spec",
                        db=db,
                        config=mock_config,
                    )
                )
        finally:
            renderer.console = original
        output = _ANSI_RE.sub("", buf.getvalue())
        assert "Generated spec" in output
        assert "Created" in output or "issuefeat" in output

    def test_prompt_ai_failure_shows_error(self, db: Any) -> None:
        """AI service raises — error is displayed, no spec created."""
        import asyncio
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_config = MagicMock()
        mock_ai = MagicMock()
        mock_ai.complete = AsyncMock(side_effect=RuntimeError("LLM unavailable"))

        buf = io.StringIO()
        console = __import__("rich.console", fromlist=["Console"]).Console(
            file=buf, width=120, force_terminal=True, color_system="truecolor"
        )
        original = renderer.console
        renderer.console = console
        try:
            with patch("anteroom.services.ai_service.create_ai_service", return_value=mock_ai):
                asyncio.run(
                    _handle_spec_command(
                        "/spec create --prompt fail-test ns errfeat",
                        cmd="/spec",
                        db=db,
                        config=mock_config,
                    )
                )
        finally:
            renderer.console = original
        output = _ANSI_RE.sub("", buf.getvalue())
        assert "LLM unavailable" in output or "error" in output.lower()
