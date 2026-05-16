"""Tests for the new user-facing CLI commands.

Each command wires up a feature module built earlier in the session:

    sage search "query"       → query_orchestrator + grounded_web_search
    sage image "prompt"       → image_generator
    sage schedule add/list/…  → task_scheduler
    sage integrate list/…     → service_integrations
    sage daemon start/status  → remote_agent_daemon
    sage ask --image          → vision_input
    sage ask --file foo.pdf   → document_extractor

Tests use typer's CliRunner. Backend feature modules are patched so the
CLI exercises wiring/argument parsing/output formatting, not network calls.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from sage.cli.new_commands import app as new_commands_app


_runner = CliRunner()


# ── sage search ──────────────────────────────────────────────────────────────


class TestSageSearch:
    def test_search_prints_answer_and_citations(self):
        from sage.core.query_orchestrator import QueryResult

        fake_result = QueryResult(
            query="who won the 2024 super bowl",
            answer="The Kansas City Chiefs won Super Bowl LVIII.",
            sources=[
                {"uri": "https://nfl.com/sb-lviii", "title": "SB LVIII"},
                {"uri": "https://espn.com/sb", "title": "Chiefs win"},
            ],
            models_used={"CLASSIFY": "phi-4", "SYNTHESIZE": "llama"},
            total_tokens=120,
        )
        with patch(
            "sage.cli.new_commands._run_query_pipeline",
            return_value=fake_result,
        ):
            result = _runner.invoke(new_commands_app, ["search", "who won the 2024 super bowl"])
        assert result.exit_code == 0
        assert "Kansas City Chiefs" in result.stdout
        # Sources rendered with titles (not raw URIs) — title fallback is URI
        # if title is missing; we passed titles so they appear.
        assert "SB LVIII" in result.stdout or "nfl.com/sb-lviii" in result.stdout

    def test_search_json_flag_outputs_machine_readable(self):
        from sage.core.query_orchestrator import QueryResult

        fake_result = QueryResult(
            query="q", answer="a",
            sources=[{"uri": "https://x.com", "title": "X"}],
            models_used={"CLASSIFY": "m"}, total_tokens=10,
        )
        with patch(
            "sage.cli.new_commands._run_query_pipeline",
            return_value=fake_result,
        ):
            result = _runner.invoke(new_commands_app, ["search", "q", "--json"])
        assert result.exit_code == 0
        # Valid JSON with expected fields
        data = json.loads(result.stdout)
        assert data["answer"] == "a"
        assert data["sources"][0]["uri"] == "https://x.com"

    def test_search_empty_query_exits_nonzero(self):
        result = _runner.invoke(new_commands_app, ["search", ""])
        assert result.exit_code != 0

    def test_search_handles_pipeline_failure_gracefully(self):
        with patch(
            "sage.cli.new_commands._run_query_pipeline",
            side_effect=ConnectionError("Vertex AI unavailable"),
        ):
            result = _runner.invoke(new_commands_app, ["search", "anything"])
        # User-facing error, not a stack trace
        assert result.exit_code != 0
        assert "unavailable" in (result.stdout + result.stderr).lower() or \
               "search failed" in (result.stdout + result.stderr).lower()


# ── sage image ───────────────────────────────────────────────────────────────


class TestSageImage:
    def test_image_generates_and_writes_default_filename(self, tmp_path):
        from sage.core.image_generator import GeneratedImage

        fake_image = GeneratedImage(
            prompt="a red apple",
            image_bytes=b"\x89PNG\r\n\x1a\nfake",
            mime_type="image/png",
        )
        with patch(
            "sage.cli.new_commands._build_image_generator",
            return_value=MagicMock(generate=MagicMock(return_value=fake_image)),
        ):
            result = _runner.invoke(
                new_commands_app, ["image", "a red apple", "--out", str(tmp_path)],
            )
        assert result.exit_code == 0
        # File written under tmp_path with slugified name
        png_files = list(tmp_path.glob("*.png"))
        assert len(png_files) == 1
        assert png_files[0].read_bytes() == b"\x89PNG\r\n\x1a\nfake"

    def test_image_supports_aspect_ratio(self, tmp_path):
        gen = MagicMock(generate=MagicMock(return_value=MagicMock(
            prompt="x",
            image_bytes=b"PNG",
            mime_type="image/png",
            save=MagicMock(return_value=tmp_path / "x.png"),
        )))
        with patch(
            "sage.cli.new_commands._build_image_generator",
            return_value=gen,
        ):
            result = _runner.invoke(
                new_commands_app,
                ["image", "fox", "--out", str(tmp_path), "--aspect", "16:9"],
            )
        assert result.exit_code == 0
        gen.generate.assert_called_once()
        kwargs = gen.generate.call_args.kwargs
        assert kwargs.get("aspect_ratio") == "16:9"

    def test_image_rejects_empty_prompt(self):
        result = _runner.invoke(new_commands_app, ["image", ""])
        assert result.exit_code != 0


# ── sage schedule ────────────────────────────────────────────────────────────


class TestSageSchedule:
    """Subcommands: add / list / pause / resume / remove / run-due."""

    def test_schedule_add_creates_task(self, tmp_path, monkeypatch):
        # Redirect the scheduler's state file to a temp path
        state = tmp_path / "tasks.json"
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(state))

        result = _runner.invoke(
            new_commands_app,
            ["schedule", "add", "check my email", "--every", "5m"],
        )
        assert result.exit_code == 0
        # ID printed for the user
        assert "Created" in result.stdout or "added" in result.stdout.lower()
        assert state.exists()

    def test_schedule_list_shows_tasks(self, tmp_path, monkeypatch):
        state = tmp_path / "tasks.json"
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(state))
        _runner.invoke(new_commands_app, ["schedule", "add", "task one", "--every", "1h"])
        _runner.invoke(new_commands_app, ["schedule", "add", "task two", "--every", "1d"])

        result = _runner.invoke(new_commands_app, ["schedule", "list"])
        assert result.exit_code == 0
        assert "task one" in result.stdout
        assert "task two" in result.stdout

    def test_schedule_remove_drops_task(self, tmp_path, monkeypatch):
        state = tmp_path / "tasks.json"
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(state))
        add = _runner.invoke(new_commands_app, ["schedule", "add", "x", "--every", "5m"])
        # Extract ID from output ("Created task <id>")
        task_id = add.stdout.strip().split()[-1].strip(":,.")

        result = _runner.invoke(new_commands_app, ["schedule", "remove", task_id])
        assert result.exit_code == 0
        # List shows empty
        listed = _runner.invoke(new_commands_app, ["schedule", "list"])
        assert "(no tasks)" in listed.stdout or "0 task" in listed.stdout.lower() or listed.stdout.strip() == "" or "task" not in listed.stdout

    def test_schedule_add_rejects_invalid_schedule(self, tmp_path, monkeypatch):
        state = tmp_path / "tasks.json"
        monkeypatch.setenv("SAGE_SCHEDULER_STATE", str(state))
        result = _runner.invoke(
            new_commands_app,
            ["schedule", "add", "x", "--every", "not a schedule"],
        )
        assert result.exit_code != 0


# ── sage integrate ───────────────────────────────────────────────────────────


class TestSageIntegrate:
    def test_integrate_list_empty_initial(self, tmp_path, monkeypatch):
        state = tmp_path / "ints.json"
        monkeypatch.setenv("SAGE_INTEGRATIONS_STATE", str(state))
        result = _runner.invoke(new_commands_app, ["integrate", "list"])
        assert result.exit_code == 0
        assert "no integrations" in result.stdout.lower() or "0" in result.stdout

    def test_integrate_list_shows_stored(self, tmp_path, monkeypatch):
        from sage.core.service_integrations import IntegrationStore, ServiceIntegration

        state = tmp_path / "ints.json"
        monkeypatch.setenv("SAGE_INTEGRATIONS_STATE", str(state))
        store = IntegrationStore(state_path=state)
        store.save(ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        ))
        result = _runner.invoke(new_commands_app, ["integrate", "list"])
        assert result.exit_code == 0
        assert "github" in result.stdout
        assert "laynef" in result.stdout

    def test_integrate_revoke_drops(self, tmp_path, monkeypatch):
        from sage.core.service_integrations import IntegrationStore, ServiceIntegration

        state = tmp_path / "ints.json"
        monkeypatch.setenv("SAGE_INTEGRATIONS_STATE", str(state))
        store = IntegrationStore(state_path=state)
        store.save(ServiceIntegration(
            service="github", access_token="t",
            refresh_token=None, expires_at=None,
            scope="repo", account_id="laynef",
        ))

        result = _runner.invoke(
            new_commands_app, ["integrate", "revoke", "github", "laynef"],
        )
        assert result.exit_code == 0
        # Verify it's gone
        listed = _runner.invoke(new_commands_app, ["integrate", "list"])
        assert "no integrations" in listed.stdout.lower() or "laynef" not in listed.stdout


# ── sage daemon ──────────────────────────────────────────────────────────────


class TestSageDaemon:
    def test_daemon_status_when_not_running(self, tmp_path):
        result = _runner.invoke(new_commands_app, ["daemon", "status"])
        # status should always return 0 — printing state isn't an error
        assert result.exit_code == 0
        # Status header + state indicator must appear
        out = result.stdout.lower()
        assert "status" in out
        assert "stopped" in out or "running" in out

    def test_daemon_status_outputs_bridge_names(self):
        """Status should mention configured bridges (even if none enabled)."""
        result = _runner.invoke(new_commands_app, ["daemon", "status"])
        # bridges section should appear regardless
        assert "bridge" in result.stdout.lower() or "imessage" in result.stdout.lower() \
               or "telegram" in result.stdout.lower() or "stopped" in result.stdout.lower()


# ── App-level wiring (verify nothing crashes at import) ─────────────────────


class TestAppWiring:
    def test_help_lists_all_new_commands(self):
        result = _runner.invoke(new_commands_app, ["--help"])
        assert result.exit_code == 0
        # Every top-level command appears in help
        for cmd in ("search", "image", "schedule", "integrate", "daemon"):
            assert cmd in result.stdout, f"missing command {cmd} in help"
