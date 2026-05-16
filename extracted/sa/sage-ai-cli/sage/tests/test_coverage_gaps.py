"""Tests for the previously-uncovered branches in new modules.

Each test targets a specific line range called out by `pytest --cov`.
The goal is to bring coverage on the new modules from 75-88% to >95%.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner


_runner = CliRunner()


# ── document_extractor coverage gaps ─────────────────────────────────────────


class TestDocumentExtractorEdgeCases:
    """Targets: DOCX branch (130-131), corrupt/odd files (43-44, 146, 150),
    DOCX extract path (167-171), text normalization (182-199)."""

    def test_normalize_whitespace_collapses_blank_lines(self):
        from sage.core.document_extractor import _normalize_whitespace

        text = "Line 1\n\n\n\n\nLine 2\n\nLine 3   "
        normalized = _normalize_whitespace(text)
        # 3+ blank lines → 2 blank lines (one paragraph break)
        assert "\n\n\n" not in normalized
        # Trailing whitespace per line trimmed
        assert "Line 3   " not in normalized

    def test_detect_format_with_zip_but_unknown_extension_raises(self, tmp_path):
        """A ZIP file with non-.docx extension should be rejected with a
        clear error rather than silently parsed as DOCX."""
        from sage.core.document_extractor import (
            DocumentExtractor,
            UnsupportedFormatError,
        )

        f = tmp_path / "archive.zip"
        f.write_bytes(b"PK\x03\x04zip-not-docx")
        with pytest.raises(UnsupportedFormatError, match="ZIP"):
            DocumentExtractor.detect_format(f)

    def test_docx_without_python_docx_raises_clear_error(self, tmp_path, monkeypatch):
        """When python-docx isn't installed, DOCX extraction tells the
        user how to enable it."""
        from sage.core import document_extractor as de_mod
        from sage.core.document_extractor import (
            DocumentExtractor,
            UnsupportedFormatError,
        )

        # Force the optional-dep flag to False
        monkeypatch.setattr(de_mod, "_HAS_DOCX", False)

        f = tmp_path / "report.docx"
        f.write_bytes(b"PK\x03\x04fake-docx")
        with pytest.raises(UnsupportedFormatError, match="python-docx"):
            DocumentExtractor().extract(f)

    def test_docx_extraction_pulls_paragraphs_and_tables(self, tmp_path):
        """Real DOCX path (130-131, 167-171). Skip if python-docx isn't
        installed; otherwise construct a minimal DOCX and verify."""
        docx = pytest.importorskip("docx")  # python-docx

        # Build a tiny DOCX with both a paragraph and a single-cell table
        doc = docx.Document()
        doc.add_paragraph("Hello world")
        table = doc.add_table(rows=1, cols=2)
        table.cell(0, 0).text = "key"
        table.cell(0, 1).text = "value"
        out = tmp_path / "test.docx"
        doc.save(str(out))

        from sage.core.document_extractor import DocumentExtractor
        result = DocumentExtractor().extract(out)
        assert "Hello world" in result.text
        # Table content extracted with " | " separator
        assert "key | value" in result.text or ("key" in result.text and "value" in result.text)


# ── new_commands.py coverage gaps ───────────────────────────────────────────


class TestNewCommandsCoverageGaps:
    """Targets the uncovered lines in sage/cli/new_commands.py:
    schedule pause/resume, integrate connect, daemon start, search json."""

    @pytest.fixture
    def app(self):
        from sage.cli.new_commands import app
        return app

    def test_schedule_pause_and_resume(self, app, tmp_path, monkeypatch):
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(tmp_path / "tasks.json"))
        add = _runner.invoke(app, ["schedule", "add", "x", "--every", "5m"])
        assert add.exit_code == 0
        task_id = add.stdout.strip().split()[-1].strip(":,.")

        pause = _runner.invoke(app, ["schedule", "pause", task_id])
        assert pause.exit_code == 0
        assert "Paused" in pause.stdout or "paused" in pause.stdout.lower()

        resume = _runner.invoke(app, ["schedule", "resume", task_id])
        assert resume.exit_code == 0
        assert "Resumed" in resume.stdout or "resumed" in resume.stdout.lower()

    def test_schedule_list_renders_table(self, app, tmp_path, monkeypatch):
        """Table-rendering path (truncate long prompts, etc.)."""
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(tmp_path / "tasks.json"))
        long_prompt = "x " * 50  # ~100 chars — triggers truncation
        _runner.invoke(app, ["schedule", "add", long_prompt, "--every", "5m"])
        result = _runner.invoke(app, ["schedule", "list"])
        assert result.exit_code == 0
        # Truncated form ends with "…"
        assert "…" in result.stdout

    def test_schedule_run_due_when_nothing_due(self, app, tmp_path, monkeypatch):
        """run-due with no overdue tasks should print the "(no tasks due)"
        message and exit 0."""
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(tmp_path / "tasks.json"))
        # Add a task that won't be due for 5m
        _runner.invoke(app, ["schedule", "add", "later", "--every", "5m"])
        result = _runner.invoke(app, ["schedule", "run-due"])
        assert result.exit_code == 0
        assert "(no tasks due)" in result.stdout

    def test_schedule_run_due_fires_due_tasks(self, app, tmp_path, monkeypatch):
        """Backdate a task's next_run_at so it's due, then verify run-due
        fires it and updates the registry."""
        from sage.core.task_scheduler import TaskScheduler
        from datetime import datetime, timedelta, timezone

        state = tmp_path / "tasks.json"
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(state))

        # Create a task, then backdate it via direct API
        sched = TaskScheduler(state_path=state)
        task = sched.add("due now", "5m")
        sched._tasks[task.id] = task.with_next_run_at(
            datetime.now(timezone.utc) - timedelta(minutes=1),
        )
        sched._save()

        result = _runner.invoke(app, ["schedule", "run-due"])
        assert result.exit_code == 0
        assert "due now" in result.stdout

    def test_integrate_connect_shows_setup_instructions(self, app):
        """Connect to a known service (github) without credentials —
        should print the setup instructions, not crash."""
        result = _runner.invoke(app, ["integrate", "connect", "github"])
        # Setup instructions exit code is 0 (informational, not error)
        assert "OAuth setup" in result.stdout or "credentials" in result.stdout.lower()

    def test_daemon_start_warns_about_credentials(self, app):
        """Starting with imessage enabled should mention the credentials
        warning, not crash."""
        result = _runner.invoke(app, ["daemon", "start"])
        # Default has --imessage=true, so this should run + warn
        assert result.exit_code == 0
        assert "credential" in result.stdout.lower() or "imessage" in result.stdout.lower()

    def test_daemon_stop_prints_pid_message(self, app):
        result = _runner.invoke(app, ["daemon", "stop"])
        assert result.exit_code == 0
        # Whatever message we use, exit code must be 0
        assert "kill" in result.stdout.lower() or "pid" in result.stdout.lower() or "daemon" in result.stdout.lower()

    def test_search_json_output_is_valid_json(self, app):
        """--json output path produces parseable JSON."""
        from sage.core.query_orchestrator import QueryResult

        fake = QueryResult(
            query="q", answer="a",
            sources=[{"uri": "https://x.com", "title": "X"}],
            models_used={"CLASSIFY": "m"}, total_tokens=10,
        )
        with patch("sage.cli.new_commands._run_query_pipeline", return_value=fake):
            result = _runner.invoke(app, ["search", "q", "--json"])
        assert result.exit_code == 0
        # Parses cleanly
        parsed = json.loads(result.stdout)
        assert parsed["query"] == "q"
        assert parsed["total_tokens"] == 10

    def test_image_invalid_aspect_ratio_clean_error(self, app, tmp_path):
        """Invalid aspect ratio → ImageGenerator raises ValueError →
        CLI surfaces it cleanly with exit code 2."""
        result = _runner.invoke(app, ["image", "anything", "--aspect", "42:7"])
        assert result.exit_code == 2
        assert "Traceback" not in result.stdout
        assert "Invalid" in result.stdout or "aspect" in result.stdout.lower()


# ── query_orchestrator coverage gaps ────────────────────────────────────────


class TestQueryOrchestratorEdgeCases:
    """Targets default-stage stubs that real production paths replace
    but the heuristic fallbacks need test coverage too."""

    def test_default_classify_detects_code_query(self):
        from sage.core.query_orchestrator import QueryOrchestrator, QueryType

        orch = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        cls = orch._default_classify("write a python function to parse JSON")
        assert cls.query_type == QueryType.CODE

    def test_default_classify_detects_reasoning(self):
        from sage.core.query_orchestrator import QueryOrchestrator, QueryType

        orch = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        cls = orch._default_classify("why does this refactor reduce coupling")
        assert cls.query_type == QueryType.REASONING

    def test_default_classify_detects_creative(self):
        from sage.core.query_orchestrator import QueryOrchestrator, QueryType

        orch = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        cls = orch._default_classify("write a poem about coffee")
        assert cls.query_type == QueryType.CREATIVE

    def test_default_classify_detects_conversational(self):
        from sage.core.query_orchestrator import QueryOrchestrator, QueryType

        orch = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        cls = orch._default_classify("hi how are you")
        assert cls.query_type == QueryType.CONVERSATIONAL

    def test_run_empty_query_raises(self):
        from sage.core.query_orchestrator import QueryOrchestrator

        orch = QueryOrchestrator(available_models=["cloud:llama-3-1-8b"])
        with pytest.raises(ValueError, match="empty"):
            orch.run("")


# ── service_integrations coverage gaps ──────────────────────────────────────


class TestServiceIntegrationsEdgeCases:
    def test_github_request_post_method(self):
        """The .request() method's POST branch."""
        from sage.core.service_integrations import (
            GitHubIntegration,
            ServiceIntegration,
        )

        class _FakeHttp:
            def __init__(self):
                self.last_post = None

            def post(self, url, **kwargs):
                self.last_post = {"url": url, **kwargs}
                return MagicMock(status_code=200)

            def get(self, url, **kwargs):
                return MagicMock(status_code=200)

        http = _FakeHttp()
        gh = GitHubIntegration(client_id="c", client_secret="s", http_client=http)
        si = ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="u",
        )
        gh.request(si, "POST", "/repos/owner/repo/issues")
        assert http.last_post is not None
        assert "issues" in http.last_post["url"]

    def test_github_request_unsupported_method_raises(self):
        from sage.core.service_integrations import (
            GitHubIntegration,
            ServiceIntegration,
        )

        gh = GitHubIntegration(client_id="c", client_secret="s", http_client=MagicMock())
        si = ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="u",
        )
        with pytest.raises(ValueError, match="DELETE"):
            gh.request(si, "DELETE", "/repos/owner/repo")


# ── remote_agent_daemon coverage gaps ───────────────────────────────────────


class TestRemoteAgentDaemonEdgeCases:
    def test_agent_exception_returns_user_facing_error(self):
        """When the agent raises, the daemon returns an error message
        to the user rather than crashing the bridge."""
        from sage.core.remote_agent_daemon import RemoteAgentDaemon
        from sage.core.messaging_bridges import BridgeMessage

        def failing_agent(msg):
            raise RuntimeError("model OOM")

        daemon = RemoteAgentDaemon(agent=failing_agent, bridges=[])
        msg = BridgeMessage(
            platform="t", chat_id="c", sender_id="u",
            sender_name="x", text="anything",
        )
        reply = daemon.handle_message(msg)
        assert "error" in reply.lower() or "oom" in reply.lower()

    def test_daemon_join_waits_for_bridges(self):
        """join() with no bridges returns immediately, doesn't hang."""
        from sage.core.remote_agent_daemon import RemoteAgentDaemon

        daemon = RemoteAgentDaemon(agent=lambda m: "reply", bridges=[])
        daemon.start()
        daemon.stop()
        # join() with no bridges shouldn't block; brief timeout is plenty
        daemon.join(timeout=1.0)

    def test_runner_start_is_idempotent(self):
        """Calling start() on an already-running bridge shouldn't spin
        up a duplicate thread."""
        from sage.core.remote_agent_daemon import BridgeRunner

        runner = BridgeRunner(name="t", poll_once=lambda: None, poll_interval=0.5)
        runner.start()
        first_thread = runner._thread
        runner.start()  # Should be a no-op
        assert runner._thread is first_thread
        runner.stop()
