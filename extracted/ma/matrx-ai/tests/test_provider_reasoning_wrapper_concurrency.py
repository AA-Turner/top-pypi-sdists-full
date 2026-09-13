"""REGRESSION GUARD: the inline reasoning wrapper is PER-STREAM, never shared.

Provider client objects are memoized PROCESS-WIDE
(``unified_client._provider_client_cache`` — "the shared cache keeps each
provider's pool alive for the process lifetime"), so ONE ``AnthropicChat`` /
``OpenAIChat`` instance serves every concurrent request in the server process.
Any per-stream state kept on ``self`` is therefore shared across simultaneous
user turns.

That is what produced the 2026-09-12 defect (handoff
``docs/handoffs/canonical-stream-and-surface-writeback.md`` § "Cross-cutting
defect"): the Anthropic parser tracked its ``<reasoning>`` wrapper in
``self._reasoning_open``, so with two turns in flight

  * the second turn's wrapper never OPENED (the flag was already True) and its
    ``</reasoning>`` printed as literal message content, and
  * the first turn's wrapper never CLOSED (the flag was already False), so the
    whole visible ANSWER kept streaming inside the collapsed "Thought process"
    block and the assistant message read as empty.

Both are the same bug. These tests interleave two streams through ONE instance
and demand that each emitter sees a balanced, self-contained wrapper.
"""

from __future__ import annotations

from types import SimpleNamespace as NS

import pytest

from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat
from matrx_ai.providers.openai.openai_api import OpenAIChat
from matrx_ai.providers.reasoning_stream_state import reset_reasoning_state


class _CaptureEmitter:
    def __init__(self) -> None:
        self.events: list[tuple[str, object]] = []

    async def send_chunk(self, text: str) -> None:
        self.events.append(("chunk", text))

    async def send_reasoning_state(self, state: str) -> None:
        self.events.append(("reasoning", state))

    async def send_info(self, payload) -> None:
        self.events.append(("info", None))

    def reset_turn_text(self) -> None: ...

    def get_turn_text(self) -> str:
        return ""

    @property
    def text(self) -> str:
        return "".join(v for k, v in self.events if k == "chunk")

    @property
    def reasoning_states(self) -> list[str]:
        return [v for k, v in self.events if k == "reasoning"]


def _assert_balanced(em: _CaptureEmitter, who: str) -> None:
    text = em.text
    opens = text.count("<reasoning>")
    closes = text.count("</reasoning>")
    assert opens == 1, (
        f"{who}: expected exactly ONE <reasoning> open, got {opens}. "
        f"A missing open means this stream's chain-of-thought streamed as "
        f"visible prose and its closing tag leaks as literal content. "
        f"Stream text: {text!r}"
    )
    assert closes == 1, (
        f"{who}: expected exactly ONE </reasoning> close, got {closes}. "
        f"A missing close leaves the client's thinking region open, so the "
        f"whole answer renders inside the collapsed 'Thought process' block. "
        f"Stream text: {text!r}"
    )
    assert text.index("<reasoning>") < text.index("</reasoning>"), (
        f"{who}: close precedes open — {text!r}"
    )
    assert em.reasoning_states == ["started", "stopped"], (
        f"{who}: reasoning lifecycle signal is not balanced: "
        f"{em.reasoning_states}"
    )


# ── Anthropic ───────────────────────────────────────────────────────────────


def _cb_start(block_type: str):
    return NS(type="content_block_start", content_block=NS(type=block_type, name=""))


def _cb_delta_thinking(text: str):
    return NS(type="content_block_delta", delta=NS(type="thinking_delta", thinking=text))


def _cb_delta_text(text: str):
    return NS(type="content_block_delta", delta=NS(type="text_delta", text=text))


def _cb_stop():
    return NS(type="content_block_stop")


@pytest.mark.asyncio
async def test_anthropic_interleaved_streams_keep_their_own_wrapper():
    """Two turns thinking at the same time on the ONE cached provider client."""
    api = AnthropicChat()  # SDK client tolerates a missing key at construction
    a, b = _CaptureEmitter(), _CaptureEmitter()

    # Interleaving exactly as two concurrent asyncio tasks would produce it.
    await api._handle_event(_cb_start("thinking"), a)
    await api._handle_event(_cb_delta_thinking("A is thinking"), a)
    await api._handle_event(_cb_start("thinking"), b)
    await api._handle_event(_cb_delta_thinking("B is thinking"), b)
    await api._handle_event(_cb_stop(), a)
    await api._handle_event(_cb_stop(), b)
    await api._handle_event(_cb_start("text"), a)
    await api._handle_event(_cb_delta_text("A's visible answer."), a)
    await api._handle_event(_cb_stop(), a)
    await api._handle_event(_cb_start("text"), b)
    await api._handle_event(_cb_delta_text("B's visible answer."), b)
    await api._handle_event(_cb_stop(), b)

    _assert_balanced(a, "anthropic stream A")
    _assert_balanced(b, "anthropic stream B")


@pytest.mark.asyncio
async def test_anthropic_new_stream_cannot_strand_an_open_wrapper():
    """A second turn STARTING mid-think must not steal the first's close.

    ``_execute_streaming`` resets the wrapper state at the top of every stream;
    on a shared instance that reset lands inside another turn's open wrapper.
    """
    api = AnthropicChat()
    a, b = _CaptureEmitter(), _CaptureEmitter()

    await api._handle_event(_cb_start("thinking"), a)
    await api._handle_event(_cb_delta_thinking("A is thinking"), a)
    # Stream B starts here — the per-stream reset used to run on `self`.
    reset_reasoning_state(b)
    await api._handle_event(_cb_start("text"), b)
    await api._handle_event(_cb_delta_text("B's answer."), b)
    await api._handle_event(_cb_stop(), b)
    # A finishes thinking and answers.
    await api._handle_event(_cb_stop(), a)
    await api._handle_event(_cb_start("text"), a)
    await api._handle_event(_cb_delta_text("A's visible answer."), a)
    await api._handle_event(_cb_stop(), a)

    _assert_balanced(a, "anthropic stream A")
    assert "<reasoning>" not in b.text and "</reasoning>" not in b.text, (
        f"stream B never thought, yet carries reasoning scaffolding: {b.text!r}"
    )


# ── OpenAI (Responses API) — the named sibling of the same pattern ──────────


def _oa_reasoning_added(item_id: str):
    return NS(type="response.output_item.added", item=NS(type="reasoning", id=item_id))


def _oa_reasoning_summary_delta(item_id: str, text: str):
    return NS(type="response.reasoning_summary_text.delta", item_id=item_id, delta=text)


def _oa_reasoning_done(item_id: str):
    return NS(type="response.output_item.done", item=NS(type="reasoning", id=item_id))


def _oa_text_delta(text: str):
    return NS(type="response.output_text.delta", delta=text)


@pytest.mark.asyncio
async def test_openai_interleaved_streams_keep_their_own_wrapper():
    api = object.__new__(OpenAIChat)
    api.debug = False
    api._event_samples = {}
    a, b = _CaptureEmitter(), _CaptureEmitter()

    await api._handle_event(_oa_reasoning_added("ra"), a)
    await api._handle_event(_oa_reasoning_summary_delta("ra", "A thinks"), a)
    await api._handle_event(_oa_reasoning_added("rb"), b)
    await api._handle_event(_oa_reasoning_summary_delta("rb", "B thinks"), b)
    await api._handle_event(_oa_reasoning_done("ra"), a)
    await api._handle_event(_oa_reasoning_done("rb"), b)
    await api._handle_event(_oa_text_delta("A's visible answer."), a)
    await api._handle_event(_oa_text_delta("B's visible answer."), b)

    _assert_balanced(a, "openai stream A")
    _assert_balanced(b, "openai stream B")


@pytest.mark.asyncio
async def test_openai_new_stream_cannot_strand_an_open_wrapper():
    """``_execute_streaming``'s per-stream clear must not reach another turn.

    It used to be ``self._reasoning_started = {}`` on the process-wide client:
    a turn starting while another was mid-reasoning wiped that turn's open item,
    so its ``</reasoning>`` never fired.
    """
    api = object.__new__(OpenAIChat)
    api.debug = False
    api._event_samples = {}
    a, b = _CaptureEmitter(), _CaptureEmitter()

    await api._handle_event(_oa_reasoning_added("ra"), a)
    await api._handle_event(_oa_reasoning_summary_delta("ra", "A thinks"), a)
    # Stream B begins here.
    reset_reasoning_state(b)
    await api._handle_event(_oa_text_delta("B's answer."), b)
    # A finishes reasoning and answers.
    await api._handle_event(_oa_reasoning_done("ra"), a)
    await api._handle_event(_oa_text_delta("A's visible answer."), a)

    _assert_balanced(a, "openai stream A")
