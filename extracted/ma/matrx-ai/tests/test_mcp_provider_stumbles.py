"""A provider's MCP server that stumbles is asked again when that is safe, and a failure says whose it was.

Live, 2026-10-17: one Notion read timed out on page 49 of 480, its error said only "Failed to call MCP server:"
(a timeout's own text is empty), and a whole import ended. Every connected tool now goes through
``mcp_resilience`` inside ``ExternalMCPClient.call_tool``:
- a read (readOnlyHint / idempotentHint) that got no answer is asked again;
- a call that never reached the provider (connect error, 429/502/503/504) is asked again for any tool;
- a WRITE that got no answer is never sent twice — it is reported as unconfirmed;
- every failure names the provider, the cause in plain words, and that our side did its part.
"""

from __future__ import annotations

import httpx
import pytest

from matrx_ai.tools import mcp_resilience
from matrx_ai.tools.external_mcp import ExternalMCPClient
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolType

OK = {"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": "the page"}]}}


def _tool(*, read_only: bool) -> ToolDefinition:
    return ToolDefinition(name="notion:notion-fetch", description="", parameters={}, tool_type=ToolType.EXTERNAL_MCP,
                          mcp_server_url="https://mcp.notion.com/mcp",
                          annotations=[{"readOnlyHint": True}] if read_only else [{"readOnlyHint": False}])


def _ctx() -> ToolContext:
    return ToolContext(call_id="c1", user_id="u1", conversation_id="conv1")


@pytest.fixture(autouse=True)
def _no_waiting(monkeypatch):
    async def _now(_s):
        return None

    monkeypatch.setattr("matrx_ai.tools.external_mcp.asyncio.sleep", _now)


def _client(monkeypatch, answers: list) -> tuple[ExternalMCPClient, list]:
    sent: list = []
    client = ExternalMCPClient(timeout=120)

    async def send(url, payload, auth=None):
        sent.append(payload)
        answer = answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return answer

    monkeypatch.setattr(client, "_send", send)
    return client, sent


@pytest.mark.asyncio
async def test_a_read_that_timed_out_is_asked_again_and_answers(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [httpx.ReadTimeout(""), httpx.RemoteProtocolError(""), OK])
    result = await client.call_tool(_tool(read_only=True), {"id": "x"}, _ctx())
    assert result.success and result.output == "the page" and len(sent) == 3


@pytest.mark.asyncio
async def test_a_read_that_never_answers_says_the_provider_failed_not_us(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [httpx.ReadTimeout("")] * 3)
    result = await client.call_tool(_tool(read_only=True), {"id": "x"}, _ctx())
    assert not result.success and len(sent) == 3
    message = result.error.message
    assert result.error.error_type == "provider_unavailable" and result.error.is_retryable
    assert message.startswith("Notion did not answer “notion-fetch”") and "120 seconds" in message
    assert "asked 3 times" in message and "nothing failed on ours" in message and "Failed to call MCP server" not in message


@pytest.mark.asyncio
async def test_a_write_that_got_no_answer_is_never_sent_twice(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [httpx.ReadTimeout(""), OK])
    result = await client.call_tool(_tool(read_only=False), {"id": "x"}, _ctx())
    assert len(sent) == 1 and not result.success
    assert result.error.error_type == "provider_unconfirmed"
    assert "may already have been done" in result.error.message and "Check in Notion" in result.error.suggested_action


@pytest.mark.asyncio
async def test_a_write_the_provider_never_received_is_sent_again(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [httpx.ConnectError("refused"), OK])
    result = await client.call_tool(_tool(read_only=False), {"id": "x"}, _ctx())
    assert result.success and len(sent) == 2


@pytest.mark.asyncio
async def test_a_slow_down_reply_is_asked_again_and_a_real_refusal_is_not(monkeypatch) -> None:
    slow = {"jsonrpc": "2.0", "id": 1, "result": {"isError": True, "content": [{"type": "text", "text": "rate_limited: 429 Too Many Requests"}]}}
    client, sent = _client(monkeypatch, [slow, OK])
    assert (await client.call_tool(_tool(read_only=False), {}, _ctx())).success and len(sent) == 2

    wrong = {"jsonrpc": "2.0", "id": 1, "result": {"isError": True, "content": [{"type": "text", "text": "object_not_found"}]}}
    client, sent = _client(monkeypatch, [wrong, OK])
    result = await client.call_tool(_tool(read_only=True), {}, _ctx())
    assert not result.success and len(sent) == 1 and result.error.error_type == "mcp_remote"


@pytest.mark.asyncio
async def test_a_request_the_provider_refused_is_said_with_its_cause_and_not_repeated(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [RuntimeError("MCP error -32602: Invalid params: id is required")])
    result = await client.call_tool(_tool(read_only=True), {}, _ctx())
    assert len(sent) == 1 and not result.success and not result.error.is_retryable
    assert "Notion refused “notion-fetch”" in result.error.message and "Invalid params" in result.error.message


def test_the_provider_is_named_from_its_address() -> None:
    assert mcp_resilience.provider_name("https://mcp.notion.com/mcp") == "Notion"
    assert mcp_resilience.provider_name("https://mcp.linear.app/sse") == "Linear"
    assert mcp_resilience.provider_name(None, "gmail:search") == "Gmail"
    assert mcp_resilience.provider_name(None) == "The connected service"



def _status(code: int) -> httpx.HTTPStatusError:
    request = httpx.Request("POST", "https://mcp.notion.com/mcp")
    return httpx.HTTPStatusError(str(code), request=request, response=httpx.Response(code, request=request))


@pytest.mark.asyncio
@pytest.mark.parametrize("code", [502, 503, 504, 500])
async def test_a_gateway_that_gave_up_may_have_passed_a_write_on_so_it_is_not_resent(monkeypatch, code) -> None:
    client, sent = _client(monkeypatch, [_status(code), OK])
    result = await client.call_tool(_tool(read_only=False), {}, _ctx())
    assert len(sent) == 1 and result.error.error_type == "provider_unconfirmed"
    client, sent = _client(monkeypatch, [_status(code), OK])
    assert (await client.call_tool(_tool(read_only=True), {}, _ctx())).success and len(sent) == 2  # a read is asked again


@pytest.mark.asyncio
async def test_a_rate_limit_status_is_asked_again_even_for_a_write(monkeypatch) -> None:
    client, sent = _client(monkeypatch, [_status(429), OK])
    assert (await client.call_tool(_tool(read_only=False), {}, _ctx())).success and len(sent) == 2


@pytest.mark.asyncio
async def test_a_busy_reply_on_a_write_is_not_resent(monkeypatch) -> None:
    busy = {"jsonrpc": "2.0", "id": 1, "result": {"isError": True, "content": [{"type": "text", "text": "Service temporarily unavailable"}]}}
    client, sent = _client(monkeypatch, [busy, OK])
    result = await client.call_tool(_tool(read_only=False), {}, _ctx())
    assert len(sent) == 1 and not result.success


@pytest.mark.asyncio
async def test_the_failure_words_carry_no_secret_from_a_url(monkeypatch) -> None:
    client, _ = _client(monkeypatch, [RuntimeError("GET https://files.example/x.png?X-Amz-Signature=abc123&token=s3cr3t failed")])
    result = await client.call_tool(_tool(read_only=True), {}, _ctx())
    assert "s3cr3t" not in result.error.message and "abc123" not in result.error.message


def test_an_outer_loop_sees_that_the_connection_already_asked_again() -> None:
    message, _ = mcp_resilience.failure_words(provider="Linear", tool="list_issues", kind=mcp_resilience.NOT_REACHED,
                                              why="it answered 429", tries=3, repeatable=True)
    assert mcp_resilience.already_asked_again(message) and not mcp_resilience.already_asked_again("HTTP 429 Too Many Requests")


# ── a server run on the person's own computer (stdio) follows the same rule ──


def _stdio_tool(*, read_only: bool) -> ToolDefinition:
    return ToolDefinition(name="files:read_file", description="", parameters={}, tool_type=ToolType.EXTERNAL_MCP,
                          mcp_transport="stdio", mcp_command="/usr/local/bin/files-mcp",
                          annotations=[{"readOnlyHint": True}] if read_only else [{"readOnlyHint": False}])


def _stdio_client(monkeypatch, answers: list) -> tuple[ExternalMCPClient, list]:
    from matrx_ai.tools.models import ToolResult

    tried: list = []
    client = ExternalMCPClient(timeout=30)

    async def once(*_a, **_k):
        tried.append(1)
        answer = answers.pop(0)
        if isinstance(answer, BaseException):
            raise answer
        return ToolResult(success=True, output=answer)

    monkeypatch.setattr(client, "_stdio_once", once)
    return client, tried


@pytest.mark.asyncio
async def test_a_local_read_that_timed_out_is_asked_again(monkeypatch) -> None:
    client, tried = _stdio_client(monkeypatch, [TimeoutError(), "the file"])
    result = await client.call_tool(_stdio_tool(read_only=True), {}, _ctx())
    assert result.success and result.output == "the file" and len(tried) == 2


@pytest.mark.asyncio
async def test_a_local_write_that_timed_out_is_not_resent_and_says_so(monkeypatch) -> None:
    client, tried = _stdio_client(monkeypatch, [TimeoutError(), "done"])
    result = await client.call_tool(_stdio_tool(read_only=False), {}, _ctx())
    assert len(tried) == 1 and not result.success
    assert "files-mcp" in result.error.message and "did not confirm" in result.error.message


@pytest.mark.asyncio
async def test_a_local_tool_that_will_not_start_says_why(monkeypatch) -> None:
    client, tried = _stdio_client(monkeypatch, [FileNotFoundError("files-mcp")])
    result = await client.call_tool(_stdio_tool(read_only=True), {}, _ctx())
    assert len(tried) == 1 and "could not run “read_file”" in result.error.message and "FileNotFoundError" in result.error.message



# ── a provider that HANGS: the call answers in its own words inside the caller's deadline (adversarial review
#    2026-10-18: with the connection and the dispatch ceiling both at 120s, the ceiling fired first) ──


@pytest.mark.asyncio
async def test_a_hung_read_is_asked_again_and_answers_inside_the_budget(monkeypatch) -> None:
    import asyncio as aio
    import time as clock

    monkeypatch.setattr("matrx_ai.tools.mcp_resilience.wait_before", lambda attempt: 0.05)
    client = ExternalMCPClient(timeout=120, budget_seconds=4)
    sent: list = []

    async def hang(url, payload, auth=None):  # never answers (asyncio.sleep is stubbed by this file's fixture)
        sent.append(1)
        await aio.Event().wait()

    monkeypatch.setattr(client, "_send", hang)
    began = clock.monotonic()
    result = await client.call_tool(_tool(read_only=True), {}, _ctx())
    assert clock.monotonic() - began < 4 and len(sent) >= 2
    assert result.error.error_type == "provider_unavailable" and result.error.message.startswith("Notion did not answer")


@pytest.mark.asyncio
async def test_a_hung_write_is_sent_once_and_said_unconfirmed_inside_the_budget(monkeypatch) -> None:
    import asyncio as aio
    import time as clock

    monkeypatch.setattr("matrx_ai.tools.mcp_resilience.wait_before", lambda attempt: 0.05)
    client = ExternalMCPClient(timeout=120, budget_seconds=1.5)
    sent: list = []

    async def hang(url, payload, auth=None):  # never answers (asyncio.sleep is stubbed by this file's fixture)
        sent.append(1)
        await aio.Event().wait()

    monkeypatch.setattr(client, "_send", hang)
    began = clock.monotonic()
    result = await client.call_tool(_tool(read_only=False), {}, _ctx())
    assert clock.monotonic() - began < 1.5 and len(sent) == 1 and result.error.error_type == "provider_unconfirmed"


def test_the_dispatch_timeout_never_calls_a_write_safe_to_repeat() -> None:
    from matrx_ai.tools.executor import timeout_tool_error

    write = timeout_tool_error(tool_name="notion:update-page", dispatch_timeout=120, user_message="x", safe_to_repeat=False)
    read = timeout_tool_error(tool_name="notion:fetch", dispatch_timeout=120, user_message="x")
    assert "safe to repeat" not in write.suggested_action and "Do NOT simply repeat" in write.suggested_action and not write.is_retryable
    assert "safe to repeat" in read.suggested_action


def test_a_wait_always_fits_inside_the_tools_dispatch_ceiling() -> None:
    import pytest as _pytest

    _pytest.importorskip("aidream")
    from aidream.services.runtime.run_wait import wait_that_fits

    assert wait_that_fits("workflow_run", 240) < 120 and wait_that_fits("workflow_run", 30) == 30



@pytest.mark.parametrize("text", ["title must be at most 500 characters", "Invalid date: 2026-05-03",
                                  "field 'timeout' must be a number", "MCP error -32602: Invalid params: id"])
def test_a_refusal_of_the_request_never_blames_the_provider(text) -> None:
    """Adversarial review 2026-10-18: a bare "500" or "time out" anywhere in a refusal read as the provider failing."""
    assert mcp_resilience.classify_reply(text) is None and mcp_resilience.classify(RuntimeError(text)) is None


@pytest.mark.parametrize(("text", "kind"), [("HTTP 503 Service Unavailable", mcp_resilience.NO_ANSWER),
                                            ("502 Bad Gateway", mcp_resilience.NO_ANSWER),
                                            ("rate_limited: too many requests", mcp_resilience.NOT_REACHED),
                                            ("429 Too Many Requests", mcp_resilience.NOT_REACHED),
                                            ("MCP error -32603: Internal error", mcp_resilience.NO_ANSWER)])
def test_a_real_provider_failure_is_still_recognized(text, kind) -> None:
    assert mcp_resilience.classify(RuntimeError(text)) == kind


# ── adversarial re-review (2026-10-18) ──


def test_a_connected_tool_that_declares_nothing_is_never_called_safe_to_repeat() -> None:
    from matrx_ai.tools.executor import _timeout_safe_to_repeat

    bare = ToolDefinition(name="linear:create_issue", description="", parameters={}, tool_type=ToolType.EXTERNAL_MCP)
    assert _timeout_safe_to_repeat(bare) is False and _timeout_safe_to_repeat(_tool(read_only=True)) is True


def test_a_write_gets_the_whole_budget_and_a_read_two_thirds_first() -> None:
    write, read = mcp_resilience.Deadline(120, 3, repeatable=False), mcp_resilience.Deadline(120, 3, repeatable=True)
    assert write.for_attempt(1, 120) > 110 and 70 < read.for_attempt(1, 120) < 80


def test_the_budget_counts_from_the_dispatch_not_from_after_the_token_refresh() -> None:
    import time as clock

    token = mcp_resilience.DISPATCH_ENDS_AT.set(clock.monotonic() + 10)
    try:
        assert mcp_resilience.Deadline(120, 3, repeatable=False).for_attempt(1, 120) < 10
    finally:
        mcp_resilience.DISPATCH_ENDS_AT.reset(token)
    assert mcp_resilience.Deadline(120, 3, repeatable=False).for_attempt(1, 120) > 110  # reset: no stale deadline


@pytest.mark.parametrize("text", ["rate_limited: slow down", "Notion API timed out", "upstream connect error"])
def test_providers_own_words_for_slow_down_and_time_out_are_recognized(text) -> None:
    assert mcp_resilience.classify(RuntimeError(text)) is not None


@pytest.mark.asyncio
async def test_a_hung_local_tool_answers_inside_the_budget(monkeypatch) -> None:
    import asyncio as aio
    import time as clock

    monkeypatch.setattr("matrx_ai.tools.mcp_resilience.wait_before", lambda attempt: 0.05)
    client = ExternalMCPClient(timeout=120, budget_seconds=1.5)

    async def hang(*_a, **_k):
        await aio.Event().wait()

    monkeypatch.setattr(client, "_stdio_once", hang)
    began = clock.monotonic()
    result = await client.call_tool(_stdio_tool(read_only=False), {}, _ctx())
    assert clock.monotonic() - began < 1.5 and not result.success and "did not confirm" in result.error.message
