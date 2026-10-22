"""A tool call the model TYPED into its reply is removed, and the model is re-asked once.

THE DEFECT (2026-10-21, conversation 9b224bf5…, message 388). The lead's final
answer ended with ``</invoke></invoke></invoke><invoke name="task"><parameter
name="action">update</parameter>…`` — a tool call written as text. The provider
reported no tool call, no ``chat.tool_call`` row was written, nothing ran, and the
person read the raw markup as part of the answer.

What each test is FOR (the production change that turns it red):

* the markup leaves the stored text and the model gets ONE host-noticed re-ask —
  delete the "A TOOL CALL WRITTEN AS TEXT" block in ``execute_until_complete``;
* a second text call ends the run (no third provider call), markup removed and a
  visible note added — drop the ``text_tool_call_reasks`` one-shot or the note;
* the stream is TOLD (a ``tool_call_written_as_text`` warning) — drop the warning;
* markup inside a fenced code block is an example, never a call — loosen the
  fence handling in ``orchestrator/text_tool_calls.py``.

The provider is the in-repo mock (no network); each call returns the next text.
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    FakeEmitter,
    InMemoryStore,
    StaticCatalog,
)

# The shape stored on message 388 (trimmed), and a plain answer.
INCIDENT = (
    "| 11 | Repos left on old branches | Fixed by hand here | — | ✅ |\n"
    "</invoke>\n</invoke>\n</invoke>\n"
    '<invoke name="task">\n<parameter name="action">update</parameter>\n'
    '<parameter name="task_id">cf1ab9ab-ab38-45a1-9d81-2d30e9196e2c</parameter>\n'
    '<parameter name="description">BUILT, SWAP OFF.</parameter>\n</invoke>'
)
ANSWER = "All eleven items are recorded; the task list is updated."
FENCED = 'Here is what that markup looks like:\n\n```xml\n<invoke name="task"></invoke>\n```'


class WarningEmitter(FakeEmitter):
    def __init__(self) -> None:
        super().__init__()
        self.warnings: list[Any] = []

    async def send_warning(self, payload: Any) -> None:
        self.warnings.append(payload)


def _scripted_model(monkeypatch, texts: list[str]) -> list[int]:
    """Each provider call answers with the next text (no tool calls)."""
    from matrx_ai.providers.mock.mock_api import MockChat

    calls: list[int] = []

    def _raw_spec(unified_config):
        calls.append(1)
        text = texts[min(len(calls), len(texts)) - 1]
        return {"latency_ms": 1, "ttft_ms": 0, "chunks": 1, "mode": "text", "text": text, "tool_calls": []}

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    return calls


def _run_context() -> WarningEmitter:
    from matrx_connect.context.app_context import AppContext, set_app_context

    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )
    emitter = WarningEmitter()
    set_app_context(
        AppContext(
            emitter=emitter,
            user_id=str(uuid.uuid4()),
            request_id=str(uuid.uuid4()),
            conversation_id=str(uuid.uuid4()),
            store=True,
            source_app="client_host_tests",
            source_feature="test",
            metadata={},
        )
    )
    return emitter


def _config() -> Any:
    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage

    return UnifiedConfig(
        model="mock-model",
        messages=MessageList(
            _messages=[UnifiedMessage(role="user", content=[TextContent(text="wrap it up")])]
        ),
    )


def _text_of(message: Any) -> str:
    from matrx_ai.config import TextContent

    return "".join(c.text for c in (message.content or []) if isinstance(c, TextContent))


def _codes(emitter: WarningEmitter) -> list[str]:
    return [getattr(w, "code", None) for w in emitter.warnings]


@pytest.mark.asyncio
async def test_the_markup_is_removed_and_the_model_is_re_asked_once(monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    calls = _scripted_model(monkeypatch, [INCIDENT, ANSWER])
    emitter = _run_context()

    completed = await execute_ai_request(_config(), max_iterations=10)
    messages = list(completed.request.config.messages)

    assert len(calls) == 2, f"{len(calls)} provider calls; expected the turn + ONE re-ask"
    assistants = [m for m in messages if m.role == "assistant"]
    assert all("<invoke" not in _text_of(m) and "</invoke>" not in _text_of(m) for m in assistants)
    assert "Repos left on old branches" in _text_of(assistants[0]), "the prose was lost with the markup"
    assert _text_of(messages[-1]) == ANSWER
    # The re-ask is a HOST notice; the person's message is untouched.
    users = [m for m in messages if m.role == "user"]
    assert _text_of(users[0]) == "wrap it up"
    host = [m for m in users[1:] if (m.metadata or {}).get("authored_by") == "host"]
    assert [(m.metadata or {}).get("authored_reason") for m in host] == ["text_tool_call"]
    assert all(m.user_content == [] for m in host)
    assert _codes(emitter) == ["tool_call_written_as_text"]


@pytest.mark.asyncio
async def test_a_second_text_call_ends_with_the_markup_removed_and_a_note(monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request
    from matrx_ai.orchestrator.text_tool_calls import TEXT_TOOL_CALL_NOTE

    calls = _scripted_model(monkeypatch, [INCIDENT, INCIDENT, ANSWER])
    emitter = _run_context()

    completed = await execute_ai_request(_config(), max_iterations=10)
    final = _text_of(list(completed.request.config.messages)[-1])

    assert len(calls) == 2, f"{len(calls)} provider calls; a second text call must end the run"
    assert "<invoke" not in final and "<parameter" not in final
    assert final.endswith(TEXT_TOOL_CALL_NOTE)
    assert _codes(emitter) == ["tool_call_written_as_text", "tool_call_written_as_text"]
    assert [getattr(w, "recoverable", None) for w in emitter.warnings] == [True, False]


@pytest.mark.asyncio
async def test_markup_inside_a_code_fence_is_an_example_not_a_call(monkeypatch) -> None:
    from matrx_ai.orchestrator.executor import execute_ai_request

    calls = _scripted_model(monkeypatch, [FENCED])
    emitter = _run_context()

    completed = await execute_ai_request(_config(), max_iterations=10)

    assert len(calls) == 1
    assert _text_of(list(completed.request.config.messages)[-1]) == FENCED
    assert _codes(emitter) == []


@pytest.mark.parametrize(
    "leaked",
    [
        '<function_calls>\n<invoke name="sql">\n<parameter name="q">select 1</parameter>\n</invoke>\n</function_calls>',
        '<tool_call>{"name": "sql", "arguments": {"q": "select 1"}}</tool_call>',
        '<function=sql>{"q": "select 1"}</function>',
        '<invoke name="task">\n<parameter name="action">update',  # cut off mid-call
    ],
)
def test_every_leaked_shape_is_found_and_removed(leaked: str) -> None:
    from matrx_ai.orchestrator.text_tool_calls import has_text_tool_markup, strip_text_tool_markup

    text = f"Done.\n\n{leaked}"
    assert has_text_tool_markup(text)
    assert strip_text_tool_markup(text) == "Done."


def test_ordinary_prose_and_html_are_left_alone() -> None:
    from matrx_ai.orchestrator.text_tool_calls import has_text_tool_markup

    for text in ("Use <b>bold</b> here.", "a < b and c > d", "The parameter name is `limit`."):
        assert not has_text_tool_markup(text), text
