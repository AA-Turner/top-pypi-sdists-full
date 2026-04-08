"""Tests for the agent-runs HTTP endpoint TaskResult integration (#1316)."""

from __future__ import annotations

from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.routers.agent_runs import router


def _make_app(detach_manager: MagicMock, db: MagicMock | None = None) -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.state.detach_manager = detach_manager
    app.state.db = db or MagicMock()
    return app


class TestGetAgentRunTaskResult:
    """GET /api/agent-runs/{run_id} returns TaskResult payload when available."""

    def test_returns_task_result_fields(self) -> None:
        mgr = MagicMock()
        mgr.get_run.return_value = {
            "id": "run-abc",
            "status": "completed",
            "title": "Summarize logs",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:01:00",
            "duration_ms": 60000,
            "parent_run_id": None,
            "metadata": {
                "task_result": {
                    "status": "completed",
                    "summary": "Found 3 errors in logs",
                    "exit_code": None,
                    "error": None,
                    "tool_calls": ["grep", "read_file"],
                    "output_pointer": "run-abc",
                    "truncated": False,
                    "duration_seconds": 59.5,
                }
            },
        }
        client = TestClient(_make_app(mgr))
        resp = client.get("/api/agent-runs/run-abc")
        assert resp.status_code == 200
        data = resp.json()
        # TaskResult fields present
        assert data["status"] == "completed"
        assert data["summary"] == "Found 3 errors in logs"
        assert data["tool_calls"] == ["grep", "read_file"]
        assert data["duration_seconds"] == 59.5
        assert data["truncated"] is False
        assert data["error"] is None
        # output_pointer stripped by to_llm_dict()
        assert "output_pointer" not in data
        # Envelope fields present
        assert data["run_id"] == "run-abc"
        assert data["title"] == "Summarize logs"
        assert data["started_at"] == "2026-04-05T10:00:00"
        assert data["duration_ms"] == 60000

    def test_legacy_fallback_without_task_result(self) -> None:
        mgr = MagicMock()
        mgr.get_run.return_value = {
            "id": "run-xyz",
            "status": "running",
            "title": "In progress",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": None,
            "duration_ms": None,
            "parent_run_id": None,
            "metadata": {},
        }
        client = TestClient(_make_app(mgr))
        resp = client.get("/api/agent-runs/run-xyz")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "running"
        assert data["run_id"] == "run-xyz"
        # Legacy shape has no TaskResult fields
        assert "summary" not in data
        assert "output_pointer" not in data

    def test_not_found(self) -> None:
        mgr = MagicMock()
        mgr.get_run.return_value = None
        client = TestClient(_make_app(mgr))
        resp = client.get("/api/agent-runs/run-missing")
        assert resp.status_code == 404

    def test_failed_task_result_with_error(self) -> None:
        mgr = MagicMock()
        mgr.get_run.return_value = {
            "id": "run-fail",
            "status": "completed",
            "title": "Broken task",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:00:30",
            "duration_ms": 30000,
            "parent_run_id": "run-parent",
            "metadata": {
                "task_result": {
                    "status": "failed",
                    "summary": "",
                    "exit_code": 1,
                    "error": "Command failed: segfault",
                    "tool_calls": [],
                    "output_pointer": "run-fail",
                    "truncated": False,
                    "duration_seconds": 29.8,
                }
            },
        }
        client = TestClient(_make_app(mgr))
        resp = client.get("/api/agent-runs/run-fail")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "failed"
        assert data["exit_code"] == 1
        assert data["error"] == "Command failed: segfault"
        assert data["parent_run_id"] == "run-parent"
        assert "output_pointer" not in data

    def test_tool_calls_truncated_at_20(self) -> None:
        """to_llm_dict() caps tool_calls at 20 entries."""
        many_tools = [f"tool_{i}" for i in range(30)]
        mgr = MagicMock()
        mgr.get_run.return_value = {
            "id": "run-big",
            "status": "completed",
            "title": "Busy agent",
            "started_at": "2026-04-05T10:00:00",
            "completed_at": "2026-04-05T10:05:00",
            "duration_ms": 300000,
            "parent_run_id": None,
            "metadata": {
                "task_result": {
                    "status": "completed",
                    "summary": "Did lots of work",
                    "exit_code": None,
                    "error": None,
                    "tool_calls": many_tools,
                    "output_pointer": "run-big",
                    "truncated": False,
                    "duration_seconds": 300.0,
                }
            },
        }
        client = TestClient(_make_app(mgr))
        resp = client.get("/api/agent-runs/run-big")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data["tool_calls"]) == 20
        assert data["tool_calls"][0] == "tool_0"
        assert data["tool_calls"][-1] == "tool_19"
        assert "output_pointer" not in data

    def test_invalid_run_id_rejected(self) -> None:
        mgr = MagicMock()
        client = TestClient(_make_app(mgr))
        # Slashes are consumed by routing (404), but special chars hit the regex guard
        resp = client.get("/api/agent-runs/run!@bad")
        assert resp.status_code == 400
