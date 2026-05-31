"""S13 — run() finally drains buffered logs via final_flush (typed ABC method)."""

from pathlib import Path
from unittest.mock import MagicMock

import abstra_internals.controllers.execution.execution as execmod
from abstra_internals.controllers.execution.execution import ExecutionController
from abstra_internals.entities.execution_context import ScriptContext


def _make_controller(execution_logs):
    # MagicMock() WITHOUT spec; bind the real run() (project convention).
    controller = MagicMock()
    controller.run = ExecutionController.run.__get__(controller)
    controller.context = ScriptContext(task_id="t")
    controller.stage = MagicMock()
    controller.stage.id = "stage-1"
    controller.stage.file_path = Path("script.py")
    controller.user_jwt = None
    controller.client = MagicMock()
    controller._execute_code = MagicMock(return_value=("finished", None))
    controller.repositories = MagicMock()
    controller.repositories.execution_logs = execution_logs
    return controller


def _patch_runtime(monkeypatch):
    # SDKContext/send_execution_usage are runtime collaborators irrelevant here.
    monkeypatch.setattr(execmod, "SDKContext", MagicMock())
    monkeypatch.setattr(execmod, "send_execution_usage", MagicMock())


def test_run_calls_final_flush(monkeypatch):
    _patch_runtime(monkeypatch)
    logs_repo = MagicMock()
    controller = _make_controller(logs_repo)

    result = controller.run("exec-1", "worker-1")

    assert "execution" in result
    logs_repo.final_flush.assert_called_once()


def test_run_unaffected_when_final_flush_is_noop(monkeypatch):
    _patch_runtime(monkeypatch)

    # File/HTTP repos inherit the ABC's no-op final_flush; run() still returns.
    class _NoopLogs:
        def final_flush(self):
            pass

    controller = _make_controller(_NoopLogs())

    result = controller.run("exec-1", "worker-1")
    assert "execution" in result
