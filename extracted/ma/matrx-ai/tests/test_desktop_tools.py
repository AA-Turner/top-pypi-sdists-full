"""Matrx 2 desktop tools: ``device_op`` and ``desktop_transcribe`` against a faithful aidream.

The fake answers exactly as aidream's local_proxy ``POST /op/{cap.op}`` does: the op's result on
200, ``{"detail": {code, message, retryable, reason?}}`` otherwise.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from matrx_connect.context.app_context import AppContext, set_app_context

from matrx_ai.tools import _sandbox_proxy as proxy
from matrx_ai.tools.implementations import desktop
from matrx_ai.tools.models import ToolContext

pytestmark = pytest.mark.asyncio

BASE = "https://aidream.invalid/api/local-proxy/5b0c3a9e-8a51-4c2c-9d0e-1f2a3b4c5d6e"
DESKTOP = proxy.SandboxBinding("mac-1", BASE, "user-jwt", "/Users/person", "local_machine")
CLOUD = proxy.SandboxBinding(
    "sbx-1", "https://orchestrator.invalid/sandboxes/sbx-1", "tok", "/home/agent", "sandbox"
)
RESULT = {
    "text": "The quick brown fox.",
    "language": "en",
    "language_probability": 0.98,
    "duration_s": 5.3,
    "model": "tiny",
    "segments": [{"start_s": 0.0, "end_s": 5.3, "text": "The quick brown fox."}],
    "elapsed_ms": 812,
}


def _aidream(monkeypatch: pytest.MonkeyPatch, status: int, body: Any) -> list[httpx.Request]:
    seen: list[httpx.Request] = []
    real = httpx.AsyncClient

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(status, json=body)

    monkeypatch.setattr(
        proxy.httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(handler), **kw)
    )
    return seen


def _bind(binding: proxy.SandboxBinding | None) -> None:
    metadata: dict[str, Any] = {}
    if binding is not None:
        metadata["active_sandbox"] = {
            "sandbox_id": binding.sandbox_id,
            "base_url": binding.base_url,
            "access_token": binding.access_token,
            "root_path": binding.root_path,
            "target_kind": binding.target_kind,
        }
    set_app_context(
        AppContext(
            emitter=None,
            user_id="u",
            request_id="run-1",
            token="t",
            is_authenticated=True,
            metadata=metadata,
        )  # type: ignore[arg-type]
    )


async def test_device_op_posts_the_op_with_its_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _aidream(monkeypatch, 200, RESULT)
    out = await proxy.device_op(
        DESKTOP, "models.transcribe", {"path": "/Users/person/a.wav"}, timeout_s=900
    )
    assert out == RESULT
    req = seen[0]
    assert req.method == "POST"
    assert str(req.url) == f"{BASE}/op/models.transcribe"
    assert json.loads(req.content) == {"path": "/Users/person/a.wav"}
    assert req.headers["x-matrx-op-timeout-s"] == "900"
    assert req.headers["x-sandbox-access-token"] == "user-jwt"


async def test_device_op_keeps_the_device_error_code(monkeypatch: pytest.MonkeyPatch) -> None:
    _aidream(
        monkeypatch,
        400,
        {
            "detail": {
                "code": "INVALID_PARAMS",
                "message": "Not audio or video",
                "retryable": False,
                "reason": "unsupported_media",
            }
        },
    )
    with pytest.raises(proxy.SandboxProxyError) as err:
        await proxy.device_op(DESKTOP, "models.transcribe", {"path": "/Users/person/notes.txt"})
    assert str(err.value) == "INVALID_PARAMS (unsupported_media): Not audio or video"
    assert err.value.error_type == "invalid_params"
    assert err.value.is_retryable is False


async def test_device_op_refuses_a_cloud_sandbox(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = _aidream(monkeypatch, 200, RESULT)
    with pytest.raises(proxy.SandboxProxyError):
        await proxy.device_op(CLOUD, "models.transcribe", {"path": "/home/agent/a.wav"})
    assert seen == []


@pytest.mark.parametrize("binding", [None, CLOUD])
async def test_without_a_computer_the_tool_says_so(
    monkeypatch: pytest.MonkeyPatch, binding: Any
) -> None:
    seen = _aidream(monkeypatch, 200, RESULT)
    _bind(binding)
    r = await desktop.desktop_transcribe(
        {"path": "a.wav"}, ToolContext(call_id="c1", tool_name="desktop_transcribe")
    )
    assert not r.success
    assert r.error is not None and r.error.error_type == "no_computer"
    assert seen == []


async def test_a_relative_path_is_the_computers_home_and_the_transcript_comes_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, RESULT)
    _bind(DESKTOP)
    r = await desktop.desktop_transcribe(
        {"path": "Downloads/memo.m4a", "model": "tiny"},
        ToolContext(call_id="c2", tool_name="desktop_transcribe"),
    )
    assert r.success, r.error
    assert json.loads(seen[0].content) == {
        "path": "/Users/person/Downloads/memo.m4a",
        "task": "transcribe",
        "model": "tiny",
    }
    assert r.output["text"] == "The quick brown fox."
    assert r.output["language"] == "en"
    assert r.output["segments_total"] == 1


async def test_a_device_error_reaches_the_model_with_its_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _aidream(
        monkeypatch,
        404,
        {"detail": {"code": "NOT_FOUND", "message": "No such file", "retryable": False}},
    )
    _bind(DESKTOP)
    r = await desktop.desktop_transcribe(
        {"path": "/Users/person/x.wav"}, ToolContext(call_id="c3", tool_name="desktop_transcribe")
    )
    assert not r.success
    assert r.error is not None and "NOT_FOUND" in r.error.message
