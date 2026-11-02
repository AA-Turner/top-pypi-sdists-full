from __future__ import annotations

import pytest
from matrx_connect.emitters.console_emitter import ConsoleEmitter


@pytest.mark.asyncio
async def test_console_emitter_accumulates_only_first_terminal_error(capsys) -> None:
    emitter = ConsoleEmitter(accumulate=True)

    await emitter.send_error("first_failure", "first")
    await emitter.send_error("duplicate_failure", "duplicate")

    assert [error["error_type"] for error in emitter._accumulated["errors"]] == [
        "first_failure"
    ]
    assert emitter._error_guard.duplicate_count == 1
    assert "DUPLICATE ERROR SUPPRESSED" in capsys.readouterr().err
