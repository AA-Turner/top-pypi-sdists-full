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


async def test_desktop_git_sends_each_action_as_its_op_with_the_folder_on_the_computer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(
        monkeypatch, 200, {"sha": "a" * 40, "output": "1 file changed", "truncated": False}
    )
    _bind(DESKTOP)
    r = await desktop.desktop_git(
        {"action": "commit", "cwd": "code/app", "message": 'Fix "quotes" and $HOME'},
        ToolContext(call_id="g1", tool_name="desktop_git"),
    )
    assert r.success, r.error
    assert seen[0].url.path.endswith("/op/git.commit")
    assert json.loads(seen[0].content) == {
        "cwd": "/Users/person/code/app",
        "message": 'Fix "quotes" and $HOME',
        "amend": False,
    }
    assert r.output["sha"] == "a" * 40

    seen.clear()
    await desktop.desktop_git(
        {"action": "clone", "url": "https://github.com/o/r.git", "dest": "code/r", "depth": 1},
        ToolContext(call_id="g2", tool_name="desktop_git"),
    )
    assert seen[0].url.path.endswith("/op/git.clone")
    assert json.loads(seen[0].content) == {
        "url": "https://github.com/o/r.git",
        "dest": "/Users/person/code/r",
        "depth": 1,
    }


async def test_desktop_git_refuses_a_call_its_arguments_cannot_make_without_reaching_the_computer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {})
    _bind(DESKTOP)
    r = await desktop.desktop_git(
        {"action": "branch", "cwd": "/Users/person/code/app", "branch_action": "delete"},
        ToolContext(call_id="g3", tool_name="desktop_git"),
    )
    assert not r.success
    assert r.error is not None and "needs the name" in r.error.message
    assert seen == []


async def test_desktop_web_runs_fetch_scrape_and_browser_fetch_on_the_computer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {"pages": [], "elapsed_ms": 1})
    _bind(DESKTOP)
    r = await desktop.desktop_web(
        {"action": "fetch", "url": "https://example.com", "headers": {"x-a": "1"}, "body": "hi"},
        ToolContext(call_id="w1", tool_name="desktop_web"),
    )
    assert r.success, r.error
    assert seen[0].url.path.endswith("/op/web.fetch")
    assert json.loads(seen[0].content) == {
        "url": "https://example.com",
        "method": "GET",
        "headers": [{"name": "x-a", "value": "1"}],
        "timeout_s": 30,
        "body": "hi",
    }
    await desktop.desktop_web(
        {"action": "scrape", "urls": ["https://example.com"], "get_links": True},
        ToolContext(call_id="w2", tool_name="desktop_web"),
    )
    assert seen[1].url.path.endswith("/op/web.scrape")
    assert json.loads(seen[1].content) == {
        "urls": ["https://example.com"],
        "use_cache": True,
        "get_links": True,
    }
    await desktop.desktop_web(
        {"action": "browser_fetch", "url": "https://example.com", "wait_for": "#app"},
        ToolContext(call_id="w3", tool_name="desktop_web"),
    )
    assert seen[2].url.path.endswith("/op/web.fetch_with_browser")
    assert json.loads(seen[2].content) == {
        "url": "https://example.com",
        "extract_text": True,
        "wait_for": "#app",
    }


async def test_desktop_web_search_runs_on_the_server_never_on_the_computer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai.tools.implementations import web
    from matrx_ai.tools.models import ToolResult

    seen = _aidream(monkeypatch, 200, {})
    _bind(DESKTOP)
    asked: list[dict[str, object]] = []

    async def server_search(args: dict[str, object], ctx: ToolContext) -> ToolResult:
        asked.append(args)
        return ToolResult(
            success=True, output="1. Example", tool_name="web_search", call_id=ctx.call_id
        )

    monkeypatch.setattr(web, "web_search", server_search)
    r = await desktop.desktop_web(
        {"action": "search", "queries": ["matrx"], "count": 3, "freshness": "pw"},
        ToolContext(call_id="w4", tool_name="desktop_web"),
    )
    assert r.success, r.error
    assert r.tool_name == "desktop_web"
    assert asked == [{"queries": ["matrx"], "max_results_per_query": 3, "freshness": "pw"}]
    assert seen == []
