"""matrx-ai running as a CLIENT gets a mandate runner (runner plan 25 step 6).

Package code reaches a mandate only through ``get_mandate_runner()`` — the conversation labeler, observational
memory, the judges, the summarize/research tools. A server host (aidream) installs its ONE runner; a CLIENT host
(matrx-local) has no aidream, so ``configure(server_url=..., get_jwt=...)`` installs ``ServerMandateRunner``:
held calls resolve over the API and send on the client, a typed NamedAgent run goes to the server's mandate door.
With no runner at all, those features refuse at CALL time in words — ``import matrx_ai`` never needs one.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from pydantic import BaseModel

import matrx_ai
from matrx_ai import mandates
from matrx_ai.client_host.mandate_runner import CLIENT_SYSTEM, MandateDoorError, ServerMandateRunner

ORG = "11111111-2222-4333-8444-555555555555"


@pytest.fixture
def no_runner(monkeypatch: pytest.MonkeyPatch, client_host_sandbox) -> None:
    monkeypatch.setattr(mandates, "_MANDATE_RUNNER", None)
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)


def test_a_client_configure_installs_the_client_runner_and_resolver(no_runner) -> None:
    matrx_ai.configure(server_url="https://server.example.com/", get_jwt=lambda: "jwt")
    runner = mandates.get_mandate_runner()
    assert isinstance(runner, ServerMandateRunner)
    assert runner.door_url("tools.summarize_content") == "https://server.example.com/ai/mandates/tools.summarize_content"
    assert mandates.get_mandate_resolver() is not None, "held calls resolve through the HTTP resolver"
    # a client's system job claims no platform identity
    assert mandates.system_principal() == CLIENT_SYSTEM


def test_a_host_runner_is_never_overwritten(no_runner, monkeypatch) -> None:
    from matrx_ai.testing.holders import HolderBackedRunner

    mine = HolderBackedRunner()
    monkeypatch.setattr(mandates, "_MANDATE_RUNNER", mine)
    matrx_ai.configure(server_url="https://server.example.com", get_jwt=lambda: "jwt")
    assert mandates.get_mandate_runner() is mine


@pytest.mark.asyncio
async def test_with_no_runner_the_labeler_refuses_in_words_never_crashes(no_runner) -> None:
    from matrx_ai.agent_runners.conversation_labeler import label_chat_conversation

    with pytest.raises(mandates.MandateRunnerUnavailable, match="No mandate runner is installed"):
        mandates.get_mandate_runner()
    result = await label_chat_conversation("User: hi", "")
    assert result.success is False
    assert "No mandate runner is installed" in (result.error or "")


class _Held:
    model = "client-model"

    def __init__(self) -> None:
        self.finished: list[tuple[str, dict[str, Any]]] = []

    async def send(self, **_kw: Any) -> Any:
        return type("Done", (), {"final_text": '{"label": "Greeting"}'})()

    async def finish(self, output: str, **kw: Any) -> None:
        self.finished.append((output, kw))


@pytest.mark.asyncio
async def test_the_labeler_prepares_and_sends_through_the_client_runner(no_runner, monkeypatch) -> None:
    from matrx_ai.agent_runners.conversation_labeler import label_chat_conversation

    seen: list[dict[str, Any]] = []
    held = _Held()

    async def hold(key: str, **kwargs: Any) -> _Held:
        seen.append({"key": key, **kwargs})
        return held

    monkeypatch.setattr(mandates, "hold_code_call", hold)
    monkeypatch.setattr(mandates, "_MANDATE_RUNNER", ServerMandateRunner("https://server.example.com", lambda: "jwt"))
    result = await label_chat_conversation("User: hi", "Earlier chat")
    assert result.success, result.error
    assert result.output == '{"label": "Greeting"}'
    assert seen[0]["key"] == "conversation.label_chat"
    # a client has no compute-rule pipeline: the held call receives plain values, never Offered wrappers
    assert seen[0]["variables"]["recent_titles"] == "Earlier chat"
    assert not any(isinstance(v, mandates.Offered) for v in seen[0]["variables"].values())


@pytest.mark.asyncio
async def test_finish_hands_the_completion_the_parsed_answer(no_runner, monkeypatch) -> None:
    held = _Held()

    async def hold(key: str, **_kwargs: Any) -> _Held:
        return held

    monkeypatch.setattr(mandates, "hold_code_call", hold)
    runner = ServerMandateRunner("https://server.example.com", lambda: "jwt")
    opts = mandates.RunOptions(door="package_code_call", consumer="tests.client")
    prepared = await runner.prepare("tests.client", mandates.Offer.given_values({"a": 1}), who=CLIENT_SYSTEM, opts=opts)
    done = await runner.finish(prepared, {"verdict": "better"})
    assert done.success and done.parsed == {"verdict": "better"}
    assert held.finished == [('{"verdict": "better"}', {"parsed": {"verdict": "better"}})]
    failed = await runner.finish(prepared, RuntimeError("provider down"))
    assert failed.success is False and "provider down" in (failed.error or "")


class _Out(BaseModel):
    summary: str


class _Agent:
    mandate_key = "tests.summarize"
    Output = _Out


def _door(monkeypatch: pytest.MonkeyPatch, lines: list[dict[str, Any]], status: int = 200) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["headers"] = dict(request.headers)
        captured["body"] = json.loads(request.content)
        return httpx.Response(status, content="\n".join(json.dumps(x) for x in lines).encode())

    real = httpx.AsyncClient
    monkeypatch.setattr(httpx, "AsyncClient", lambda **kw: real(transport=httpx.MockTransport(handler), **kw))
    return captured


def _named_offer() -> mandates.Offer:
    named = mandates.NamedCall(agent_cls=_Agent, kwargs={"inputs": {"text": "long"}, "user_input": "Summarize"})  # type: ignore[arg-type]
    return mandates.Offer({"text": mandates.given("long")}, named=named)


@pytest.mark.asyncio
async def test_a_named_run_goes_to_the_servers_mandate_door(monkeypatch) -> None:
    captured = _door(monkeypatch, [
        {"event": "phase", "data": {"phase": "processing"}},
        {"e": "c", "t": '{"summary": '},
        {"e": "c", "t": '"short"}'},
        {"event": "end", "data": {}},
    ])
    runner = ServerMandateRunner("https://server.example.com", lambda: "jwt")
    who = mandates.Principal(user_id="u-1", org_id=ORG)
    done = await runner.run("tests.summarize", _named_offer(), who=who, opts=mandates.RunOptions(door="named_agent"))
    assert captured["url"] == "https://server.example.com/ai/mandates/tests.summarize"
    assert captured["headers"]["authorization"] == "Bearer jwt"
    assert captured["headers"]["x-organization-id"] == ORG
    assert captured["body"] == {"variables": {"text": "long"}, "stream": True, "user_input": "Summarize"}
    assert done.success and done.raw.output == '{"summary": "short"}'
    assert done.raw.parsed == _Out(summary="short")


@pytest.mark.asyncio
async def test_a_door_error_is_a_failed_run_in_the_servers_words(monkeypatch) -> None:
    _door(monkeypatch, [{"event": "error", "data": {"message": "AI usage limit reached"}}, {"event": "end", "data": {}}])
    runner = ServerMandateRunner("https://server.example.com", lambda: "jwt")
    done = await runner.run("tests.summarize", _named_offer(), who=CLIENT_SYSTEM, opts=mandates.RunOptions(door="named_agent"))
    assert done.success is False and done.raw.error == "AI usage limit reached"


@pytest.mark.asyncio
async def test_a_refused_door_and_a_missing_token_are_said(monkeypatch) -> None:
    _door(monkeypatch, [{"detail": "mandate_unresolved"}], status=422)
    runner = ServerMandateRunner("https://server.example.com", lambda: "jwt")
    with pytest.raises(MandateDoorError, match="HTTP 422"):
        await runner.run("tests.summarize", _named_offer(), who=CLIENT_SYSTEM, opts=mandates.RunOptions(door="named_agent"))
    anonymous = ServerMandateRunner("https://server.example.com", lambda: None)
    with pytest.raises(MandateDoorError, match="anonymously"):
        await anonymous.run("tests.summarize", _named_offer(), who=CLIENT_SYSTEM, opts=mandates.RunOptions(door="named_agent"))
