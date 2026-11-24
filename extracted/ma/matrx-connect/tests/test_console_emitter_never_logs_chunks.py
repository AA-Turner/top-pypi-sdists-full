"""CASA 6.5.1: server-side runs stream through ConsoleEmitter; model output never reaches a log."""

import asyncio
import logging

import pytest

from matrx_connect.emitters.console_emitter import ConsoleEmitter

SHORT = "my SSN is 123-45-6789"


@pytest.fixture
def _knob(monkeypatch):
    from matrx_utils.conf import settings

    def set_to(value):
        if value is None:
            monkeypatch.delenv("MATRX_LOG_CONTENT", raising=False)
        else:
            monkeypatch.setenv("MATRX_LOG_CONTENT", value)
        settings.reset_env_variables()

    yield set_to
    monkeypatch.undo()
    settings.reset_env_variables()


def _run(emitter):
    async def go():
        await emitter.send_chunk(SHORT)
        await emitter.send_reasoning_chunk(SHORT)

    asyncio.run(go())


def test_chunks_are_not_logged_in_production(_knob, caplog, capsys):
    _knob(None)
    emitter = ConsoleEmitter("t", accumulate=True)
    with caplog.at_level(logging.DEBUG):
        _run(emitter)
    seen = "\n".join(r.getMessage() for r in caplog.records) + capsys.readouterr().out
    assert "123-45-6789" not in seen
    assert emitter.get_turn_text() == SHORT  # the caller still receives the text


def test_local_knob_shows_chunks(_knob, caplog):
    _knob("1")
    with caplog.at_level(logging.DEBUG):
        _run(ConsoleEmitter("t", accumulate=False))
    assert SHORT in "\n".join(r.getMessage() for r in caplog.records)


def _send_data(emitter, payload):
    asyncio.run(emitter.send_data(payload))


def test_a_data_payload_is_one_line_in_production(_knob, capsys):
    # L-SPEED 6c: a background workflow lane printed every event whole (~28k lines per run).
    _knob(None)
    emitter = ConsoleEmitter("mandate:x", accumulate=True)
    payload = {"event": "node_started", "run_id": "r1", "step": 3, "node_id": "keys", "inputs": {"text": SHORT}}
    _send_data(emitter, payload)
    out = capsys.readouterr().out
    assert "123-45-6789" not in out
    assert "node_started" in out and "keys" in out
    assert len([line for line in out.splitlines() if line.strip()]) <= 2, out
    assert emitter._accumulated["data"] == [payload]  # the caller still receives the payload


def test_debug_or_the_local_knob_shows_the_whole_payload(_knob, capsys):
    _knob("1")
    _send_data(ConsoleEmitter("t", accumulate=False), {"event": "node_started", "inputs": {"text": SHORT}})
    assert "123-45-6789" in capsys.readouterr().out
