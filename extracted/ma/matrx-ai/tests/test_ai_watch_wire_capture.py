"""AI Watch: every streamed run carries its exact outbound request (2026-10-11).

Fails if the wire capture goes back to opt-in (snapshot=None silent), if an
explicit opt-out (snapshot=False) leaks, or if a huge default body streams whole.
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


def _run(snapshot, body: dict, monkeypatch) -> list:
    emitter = _Emitter()
    ctx = SimpleNamespace(snapshot=snapshot, emitter=emitter, conversation_id="c", request_id="r")
    monkeypatch.setattr(oc, "try_get_app_context", lambda: ctx)
    request = httpx.Request("POST", "https://api.example.test/v1/messages", content=json.dumps(body).encode())
    asyncio.run(oc._outbound_request_hook(request))
    return emitter.payloads


def test_default_run_streams_exact_request(monkeypatch: pytest.MonkeyPatch) -> None:
    body = {"model": "m", "system": "be brief", "messages": [{"role": "user", "content": "hi"}]}
    payloads = _run(None, body, monkeypatch)
    assert len(payloads) == 1
    assert payloads[0].body == body


def test_opt_out_streams_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _run(False, {"model": "m"}, monkeypatch) == []


def test_default_caps_huge_body_but_explicit_true_keeps_it(monkeypatch: pytest.MonkeyPatch) -> None:
    body = {"model": "m", "messages": [{"role": "user", "content": "x" * (oc.AI_WATCH_FULL_BODY_MAX_BYTES + 10)}]}
    capped = _run(None, body, monkeypatch)[0]
    assert capped.body is None
    assert capped.body_raw and len(capped.body_raw) <= oc.AI_WATCH_PREVIEW_BYTES
    assert capped.body_size_bytes > oc.AI_WATCH_FULL_BODY_MAX_BYTES
    full = _run(True, body, monkeypatch)[0]
    assert full.body == body
