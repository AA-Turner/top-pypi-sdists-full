"""S12 — send_stdio gating: DB mode persists but skips the RabbitMQ broadcast."""

from typing import cast
from unittest.mock import MagicMock, patch

from abstra_internals.controllers.execution.execution_stdio import BroadcastController
from abstra_internals.entities.execution import Execution
from abstra_internals.entities.execution_context import ScriptContext

MODULE = "abstra_internals.controllers.execution.execution_stdio"


def _make_bc():
    main_controller = MagicMock()
    main_controller.execution_logs_repository = MagicMock()
    main_controller.execution_repository = MagicMock()
    return BroadcastController(
        main_controller=main_controller,
        sys_stdout_write=lambda x: len(x),
        sys_stderr_write=lambda x: len(x),
    )


def _make_execution():
    return Execution.create(
        id="exec-1",
        context=ScriptContext(task_id="t"),
        stage_id="stage-1",
        worker_id="w1",
    )


@patch(f"{MODULE}.web_editor_uses_db", return_value=True)
@patch(f"{MODULE}.WORKER_LOG_TO_QUEUE", True)
def test_db_mode_persists_but_skips_queue_broadcast(_uses_db):
    bc = _make_bc()
    bc._send_stdio_via_queue = MagicMock()
    bc.send_stdio(_make_execution(), "stdout", "hi")

    cast(
        MagicMock, bc.execution_logs_repository
    ).insert_stdio.assert_called_once()  # always persists
    bc._send_stdio_via_queue.assert_not_called()  # gated off on the DB path


@patch(f"{MODULE}.web_editor_uses_db", return_value=False)
@patch(f"{MODULE}.WORKER_LOG_TO_QUEUE", True)
def test_legacy_mode_still_broadcasts_via_queue(_uses_db):
    bc = _make_bc()
    bc._send_stdio_via_queue = MagicMock()
    bc.send_stdio(_make_execution(), "stdout", "hi")

    cast(MagicMock, bc.execution_logs_repository).insert_stdio.assert_called_once()
    bc._send_stdio_via_queue.assert_called_once()


@patch(f"{MODULE}.web_editor_uses_db", return_value=False)
@patch(f"{MODULE}.WORKER_LOG_TO_QUEUE", True)
def test_whitespace_only_writes_are_not_persisted_or_broadcast(_uses_db):
    # print()'s standalone "\n"/separator writes (and whitespace-only lines) must
    # not create junk rows — the frontend discards them anyway. Content is kept.
    bc = _make_bc()
    bc._send_stdio_via_queue = MagicMock()
    repo = cast(MagicMock, bc.execution_logs_repository)
    execution = _make_execution()

    for blank in ("\n", "   ", "   \n", "\t\n"):
        bc.send_stdio(execution, "stdout", blank)
    repo.insert_stdio.assert_not_called()
    bc._send_stdio_via_queue.assert_not_called()

    bc.send_stdio(execution, "stdout", "real content")
    repo.insert_stdio.assert_called_once()
    bc._send_stdio_via_queue.assert_called_once()
