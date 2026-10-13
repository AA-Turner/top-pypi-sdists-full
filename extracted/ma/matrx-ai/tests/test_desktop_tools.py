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


async def test_desktop_web_saves_the_agents_pages_in_the_organization_the_conversation_carries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """scrape and browser_fetch name the conversation's organization as the op's ``land``: the
    page becomes a Source there, never in whichever organization the computer has active."""
    from matrx_ai.tools import organization_hold

    seen = _aidream(monkeypatch, 200, {"pages": [], "elapsed_ms": 1})
    _bind(DESKTOP)
    org = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"
    monkeypatch.setattr(organization_hold, "carried_organization_id", lambda _ctx: org)
    await desktop.desktop_web(
        {"action": "scrape", "urls": ["https://example.com"]},
        ToolContext(call_id="w5", tool_name="desktop_web"),
    )
    await desktop.desktop_web(
        {"action": "browser_fetch", "url": "https://example.com"},
        ToolContext(call_id="w6", tool_name="desktop_web"),
    )
    land = {"organization_id": org, "keep": False, "attach_to": []}
    assert json.loads(seen[0].content)["land"] == land
    assert json.loads(seen[1].content)["land"] == land
    # A plain fetch saves nothing, so it names no organization.
    await desktop.desktop_web(
        {"action": "fetch", "url": "https://example.com"},
        ToolContext(call_id="w7", tool_name="desktop_web"),
    )
    assert "land" not in json.loads(seen[2].content)


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


async def test_desktop_browser_runs_each_action_as_the_extensions_own_tool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(
        monkeypatch, 200, {"client_instance": "ext_a", "result": {"ok": True}, "duration_ms": 9}
    )
    _bind(DESKTOP)
    cases: list[tuple[dict[str, Any], str, dict[str, Any]]] = [
        ({"action": "tabs"}, "list_open_tabs", {}),
        ({"action": "read", "max_chars": 2000}, "get_page_text", {"max_chars": 2000}),
        ({"action": "screenshot"}, "take_screenshot", {"persist": False}),
        (
            {"action": "navigate", "url": "https://example.com"},
            "navigate_active_tab",
            {"url": "https://example.com"},
        ),
        ({"action": "click", "selector": "#go"}, "click_element", {"selector": "#go"}),
        (
            {"action": "type", "ref": "e12", "text": "hi"},
            "type_into_element",
            {"ref": "e12", "text": "hi"},
        ),
        ({"action": "close", "tab_ids": [4, 5]}, "close_tab", {"tab_ids": [4, 5]}),
        (
            {"action": "call", "tool": "find_text_on_page", "tool_args": {"text": "x"}},
            "find_text_on_page",
            {"text": "x"},
        ),
    ]
    for i, (args, tool, tool_args) in enumerate(cases):
        r = await desktop.desktop_browser(
            args, ToolContext(call_id=f"b{i}", tool_name="desktop_browser")
        )
        assert r.success, (args, r.error)
        assert seen[i].url.path.endswith("/op/browser.call")
        assert json.loads(seen[i].content) == {
            "tool": tool,
            "args": tool_args,
            "timeout_ms": 120_000,
        }
        # The core waits up to the person's budget; the device hop adds its headroom.
        assert seen[i].headers["x-matrx-op-timeout-s"] == "150"


async def test_desktop_browser_names_a_browser_and_lists_sessions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {"enabled": True, "owner_signed_in": True, "sessions": []})
    _bind(DESKTOP)
    r = await desktop.desktop_browser(
        {"action": "sessions"}, ToolContext(call_id="s", tool_name="desktop_browser")
    )
    assert r.success
    assert seen[0].url.path.endswith("/op/browser.sessions")
    assert json.loads(seen[0].content) == {}
    await desktop.desktop_browser(
        {"action": "tabs", "browser": "ext_b", "timeout_s": 30},
        ToolContext(call_id="t", tool_name="desktop_browser"),
    )
    assert json.loads(seen[1].content) == {
        "tool": "list_open_tabs",
        "args": {},
        "timeout_ms": 30_000,
        "client_instance": "ext_b",
    }


async def test_desktop_browser_refuses_a_call_its_arguments_cannot_make(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {})
    _bind(DESKTOP)
    for args in (
        {"action": "navigate"},
        {"action": "click"},
        {"action": "type", "selector": "#a"},
        {"action": "close"},
        {"action": "call"},
    ):
        r = await desktop.desktop_browser(
            args, ToolContext(call_id="x", tool_name="desktop_browser")
        )
        assert not r.success and r.error is not None and r.error.error_type == "invalid_argument", (
            args
        )
    assert seen == []


async def test_desktop_browser_a_tool_that_could_not_do_it_is_a_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _aidream(
        monkeypatch,
        200,
        {
            "client_instance": "ext_a",
            "result": {"ok": False, "reason": "No active tab"},
            "duration_ms": 3,
        },
    )
    _bind(DESKTOP)
    r = await desktop.desktop_browser(
        {"action": "read"}, ToolContext(call_id="r", tool_name="desktop_browser")
    )
    assert not r.success
    assert (
        r.error is not None
        and r.error.error_type == "browser_refused"
        and r.error.message == "No active tab"
    )


async def test_desktop_browser_a_declined_confirmation_reaches_the_model_in_its_words(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _aidream(
        monkeypatch,
        403,
        {
            "detail": {
                "code": "AUTH_FORBIDDEN",
                "message": "The person said no: User denied this action",
                "retryable": False,
            }
        },
    )
    _bind(DESKTOP)
    r = await desktop.desktop_browser(
        {"action": "navigate", "url": "https://example.com"},
        ToolContext(call_id="n", tool_name="desktop_browser"),
    )
    assert not r.success and r.error is not None
    assert "denied" in r.error.message


async def test_desktop_browser_screenshot_reaches_the_model_as_an_image(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _aidream(
        monkeypatch,
        200,
        {
            "client_instance": "ext_a",
            "result": {
                "ok": True,
                "image_base64": "aGVsbG8=",
                "media_type": "image/png",
                "width": 800,
                "height": 600,
            },
            "duration_ms": 40,
        },
    )
    _bind(DESKTOP)
    r = await desktop.desktop_browser(
        {"action": "screenshot"}, ToolContext(call_id="p", tool_name="desktop_browser")
    )
    assert r.success
    assert "image_base64" not in r.output["result"]
    assert r.provider_content is not None and r.provider_content[0].mime_type == "image/png"


# ── Matrx Local's remaining tools (desktop-protocol 1.37) ───────────────────────────────────────


def _sent(seen: list[httpx.Request]) -> list[tuple[str, dict[str, Any]]]:
    return [(str(r.url).removeprefix(f"{BASE}/op/"), json.loads(r.content)) for r in seen]


@pytest.mark.parametrize(
    ("tool", "args", "op", "params"),
    [
        ("desktop_net", {"action": "info"}, "net.info", {}),
        (
            "desktop_net",
            {"action": "scan", "host": "192.168.1.10", "ports": [22, 80]},
            "net.scan",
            {"host": "192.168.1.10", "ports": [22, 80]},
        ),
        (
            "desktop_net",
            {"action": "download", "url": "https://example.com/a.zip", "path": "Downloads"},
            "net.download",
            {"url": "https://example.com/a.zip", "path": "/Users/person/Downloads"},
        ),
        (
            "desktop_automation",
            {"language": "jxa", "script": "1+1"},
            "automation.script",
            {"language": "jxa", "script": "1+1", "timeout_s": 60},
        ),
        (
            "desktop_mail",
            {
                "action": "send",
                "to": ["a@b.co"],
                "subject": "Hi",
                "body": "Yo",
                "sender": "me@x.co",
                "send": False,
            },
            "mail.send",
            {"to": ["a@b.co"], "subject": "Hi", "body": "Yo", "from": "me@x.co", "send": False},
        ),
        ("desktop_messages", {"action": "chats", "limit": 5}, "messages.chats", {"limit": 5}),
        (
            "desktop_contacts",
            {"action": "search", "query": "Jane"},
            "contacts.search",
            {"query": "Jane"},
        ),
        (
            "desktop_calendar",
            {"action": "events", "start": "2026-10-12T00:00:00Z", "end": "2026-10-13"},
            "calendar.list",
            {"from_ms": 1_791_763_200_000, "to_ms": 1_791_849_600_000},
        ),
        (
            "desktop_calendar",
            {"action": "create_reminder", "title": "Call Jane", "due": "2026-10-12T09:00:00-07:00"},
            "reminders.create",
            {"title": "Call Jane", "due_ms": 1_791_820_800_000},
        ),
        (
            "desktop_photos",
            {"action": "get", "id": "ABC/L0/001", "export": True},
            "photos.get",
            {"id": "ABC/L0/001", "export": True},
        ),
        ("desktop_location", {}, "location.get", {"timeout_s": 15}),
        (
            "desktop_windows_admin",
            {"action": "service_control", "name": "Spooler", "service_action": "restart"},
            "windows.service_control",
            {"name": "Spooler", "action": "restart"},
        ),
        (
            "desktop_notes",
            {"action": "read", "path": "Work/Plan.md"},
            "notes.read",
            {"path": "Work/Plan.md"},
        ),
        (
            "desktop_documents",
            {"action": "pdf_text", "path": "Documents/report.pdf", "last_page": 3},
            "documents.pdf_text",
            {"path": "/Users/person/Documents/report.pdf", "last_page": 3},
        ),
        (
            "desktop_entities",
            {"action": "private_data", "text": "a@b.co", "redact": True},
            "entities.pii",
            {"text": "a@b.co", "redact": True},
        ),
    ],
)
async def test_each_matrx_local_successor_sends_its_op_with_the_ops_own_params(
    monkeypatch: pytest.MonkeyPatch,
    tool: str,
    args: dict[str, Any],
    op: str,
    params: dict[str, Any],
) -> None:
    seen = _aidream(monkeypatch, 200, {"ok": True})
    _bind(DESKTOP)
    r = await getattr(desktop, tool)(args, ToolContext(call_id="s1", tool_name=tool))
    assert r.success, r.error
    assert _sent(seen) == [(op, params)]


async def test_a_successor_says_what_its_action_lacks_and_sends_nothing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {})
    _bind(DESKTOP)
    r = await desktop.desktop_notes(
        {"action": "write", "label": "x"}, ToolContext(call_id="s2", tool_name="desktop_notes")
    )
    assert not r.success and r.error is not None
    assert r.error.message == "write needs content"
    r = await desktop.desktop_calendar(
        {"action": "events", "start": "next tuesday", "end": "2026-10-13"},
        ToolContext(call_id="s3", tool_name="desktop_calendar"),
    )
    assert r.error is not None and "ISO 8601" in r.error.message
    assert seen == []


async def test_desktop_schedule_puts_another_tools_action_on_an_interval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen = _aidream(monkeypatch, 200, {"task": {"id": "t1"}})
    _bind(DESKTOP)
    r = await desktop.desktop_schedule(
        {
            "action": "create",
            "name": "Morning net check",
            "tool": "desktop_net",
            "tool_args": {"action": "devices"},
            "interval_s": 3600,
            "run_now": True,
        },
        ToolContext(call_id="s4", tool_name="desktop_schedule"),
    )
    assert r.success, r.error
    assert _sent(seen) == [
        (
            "schedule.create",
            {
                "name": "Morning net check",
                "op": "net.devices",
                "params": {},
                "interval_s": 3600,
                "run_now": True,
            },
        )
    ]
    bad = await desktop.desktop_schedule(
        {
            "action": "create",
            "name": "x",
            "tool": "desktop_schedule",
            "tool_args": {},
            "interval_s": 60,
        },
        ToolContext(call_id="s5", tool_name="desktop_schedule"),
    )
    assert bad.error is not None and "cannot be scheduled" in bad.error.message
