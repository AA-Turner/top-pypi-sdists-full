"""An expected caller refusal through the ConsoleEmitter is a WARNING, never an ERROR app_log line.

2026-11-12: 73 agent-test judge calls held by a spend approval each filed two ERROR lines from this
emitter — the error event and the ``failed`` record update. The refusal carries
``details.caller_refusal`` (set by its producer); the record update is a notification, the failure
itself is reported once by ``send_error``.
"""

from __future__ import annotations

import logging

import pytest

from matrx_connect.context.events import RecordUpdatePayload
from matrx_connect.emitters.console_emitter import ConsoleEmitter

LOGGER = "matrx_connect.emitters.console_emitter"


@pytest.mark.asyncio
async def test_a_caller_refusal_is_a_warning(caplog: pytest.LogCaptureFixture) -> None:
    emitter = ConsoleEmitter(label="judge", accumulate=False)
    with caplog.at_level(logging.WARNING, logger=LOGGER):
        await emitter.send_error(
            error_type="run_approval_required",
            message="held",
            code="run_approval_required",
            details={"caller_refusal": True, "status_code": 403},
        )
        await emitter.send_record_update(
            RecordUpdatePayload(db_project="matrx", table="user_request", record_id="r1", status="failed",
                                metadata={"reason": "terminal_status"})
        )
    lines = [r for r in caplog.records if r.name == LOGGER]
    assert lines and all(r.levelno == logging.WARNING for r in lines), [(r.levelname, r.getMessage()) for r in lines]


@pytest.mark.asyncio
async def test_a_real_failure_is_still_an_error(caplog: pytest.LogCaptureFixture) -> None:
    emitter = ConsoleEmitter(label="judge", accumulate=False)
    with caplog.at_level(logging.WARNING, logger=LOGGER):
        await emitter.send_error(error_type="provider_error", message="boom")
    assert any(r.levelno == logging.ERROR for r in caplog.records if r.name == LOGGER)
