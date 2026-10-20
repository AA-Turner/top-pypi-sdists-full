"""AI Watch gate on the exact outbound request (provision leak fix, 2026-10-19).

The wire body carries every provision value the model received, and provision values never reach
the browser outside AI Watch (provision audit 2026-10-18). So ``context_analysis`` streams ONLY on
a run whose context the host marked ``ai_watch=True`` — never by default (the 2026-10-11 behaviour
this replaces), and never because a request body said ``snapshot=True``.

Fails if the capture goes back to on-by-default, if ``snapshot=True`` alone arms it, if a watched
run's explicit opt-out (``snapshot=False``) leaks, if a huge default body streams whole, or if the
non-httpx emit path (``emit_explicit_context_analysis``) skips the gate.
"""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace

import httpx
import pytest

from matrx_ai.providers import outbound_capture as oc


class _Emitter:
    def __init__(self) -> None:
        self.payloads: list = []

    async def send_context_analysis(self, payload) -> None:
        self.payloads.append(payload)


def _ctx(snapshot, ai_watch: bool, emitter: _Emitter) -> SimpleNamespace:
    return SimpleNamespace(
        snapshot=snapshot, ai_watch=ai_watch, emitter=emitter, conversation_id="c", request_id="r"
    )


def _run(snapshot, body: dict, monkeypatch, *, ai_watch: bool) -> list:
    emitter = _Emitter()
    ctx = _ctx(snapshot, ai_watch, emitter)
    monkeypatch.setattr(oc, "try_get_app_context", lambda: ctx)
    request = httpx.Request("POST", "https://api.example.test/v1/messages", content=json.dumps(body).encode())
    asyncio.run(oc._outbound_request_hook(request))
    return emitter.payloads


BODY = {"model": "m", "system": "brand voice: <provision value>", "messages": [{"role": "user", "content": "hi"}]}


def test_an_unwatched_run_streams_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _run(None, BODY, monkeypatch, ai_watch=False) == []


def test_snapshot_true_from_a_body_does_not_arm_the_capture(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _run(True, BODY, monkeypatch, ai_watch=False) == []


def test_a_watched_run_streams_the_exact_request(monkeypatch: pytest.MonkeyPatch) -> None:
    payloads = _run(None, BODY, monkeypatch, ai_watch=True)
    assert len(payloads) == 1
    assert payloads[0].body == BODY


def test_a_watched_run_can_still_opt_out(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _run(False, BODY, monkeypatch, ai_watch=True) == []


def test_watched_default_caps_huge_body_but_explicit_true_keeps_it(monkeypatch: pytest.MonkeyPatch) -> None:
    body = {"model": "m", "messages": [{"role": "user", "content": "x" * (oc.AI_WATCH_FULL_BODY_MAX_BYTES + 10)}]}
    capped = _run(None, body, monkeypatch, ai_watch=True)[0]
    assert capped.body is None
    assert capped.body_raw and len(capped.body_raw) <= oc.AI_WATCH_PREVIEW_BYTES
    assert capped.body_size_bytes > oc.AI_WATCH_FULL_BODY_MAX_BYTES
    full = _run(True, body, monkeypatch, ai_watch=True)[0]
    assert full.body == body


@pytest.mark.parametrize(("ai_watch", "expected"), [(False, 0), (True, 1)])
def test_the_non_httpx_emit_path_obeys_the_same_gate(
    monkeypatch: pytest.MonkeyPatch, ai_watch: bool, expected: int
) -> None:
    emitter = _Emitter()
    ctx = _ctx(None, ai_watch, emitter)
    monkeypatch.setattr(oc, "try_get_app_context", lambda: ctx)
    asyncio.run(
        oc.emit_explicit_context_analysis(
            provider="elevenlabs", method="POST", url="https://api.example.test/tts", body={"text": "x"}
        )
    )
    assert len(emitter.payloads) == expected
