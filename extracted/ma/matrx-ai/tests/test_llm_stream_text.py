"""``llm_stream_text`` — the streaming free-text funnel primitive.

The contract that matters (and the bugs it exists to prevent):

1. Every answer token reaches ``on_delta`` so the caller can emit its OWN typed
   event (e.g. a per-claim verify verdict).
2. Those tokens do NOT also reach the wrapped emitter as raw ``chunk`` events.
   Forwarding them would double-emit on a user-facing stream and — worse — leak
   an INTERNAL call's raw output (a grounding judge's JSON) into the user's chat.
3. Everything that is not a chunk (``send_data``, ``send_end``, …) still passes
   through to the real emitter, so cost/error/disconnect paths are untouched.
4. Reasoning deltas are not answer text: they go to the emitter's reasoning
   channel, never into ``on_delta`` or the returned string.
5. The AppContext emitter is restored afterwards, even when the call raises.
"""

from __future__ import annotations

import pytest

from matrx_ai.graph_nodes import _strict_json
from matrx_ai.graph_nodes._strict_json import _DeltaEmitter, llm_stream_text


class _RecordingEmitter:
    """Stands in for the real StreamEmitter on the AppContext."""

    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.reasoning: list[str] = []
        self.data: list[object] = []
        self.ended = False

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_reasoning_chunk(self, text: str) -> None:
        self.reasoning.append(text)

    async def send_data(self, payload: object) -> None:
        self.data.append(payload)

    async def send_end(self) -> None:
        self.ended = True


async def test_deltas_reach_callback_and_never_leak_to_the_emitter(monkeypatch):
    """The whole point: caller gets the tokens, the wire does not."""
    base = _RecordingEmitter()
    seen: list[str] = []

    async def _fake_run_completion(messages, system_text, **kwargs):
        # Stand in for the provider: push tokens the way every provider does —
        # through whatever emitter is on the AppContext at call time.
        from matrx_connect.context.app_context import get_app_context

        emitter = get_app_context().emitter
        for piece in ("Hello", " ", "world"):
            await emitter.send_chunk(piece)
        await emitter.send_reasoning_chunk("<thinking>")
        await emitter.send_data({"kind": "passthrough"})
        return "Hello world", "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _fake_run_completion)

    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:
        seen.append(text)

    answer = await llm_stream_text(
        model="m", system="s", user="u", on_delta=_on_delta, temperature=0.0
    )

    assert answer == "Hello world"
    assert seen == ["Hello", " ", "world"]  # 1. caller saw every token
    assert base.chunks == []  # 2. NOTHING leaked onto the wire
    assert base.data == [{"kind": "passthrough"}]  # 3. non-chunk events passed through
    assert base.reasoning == ["<thinking>"]  # 4. reasoning went to its own channel
    assert "<thinking>" not in answer  # 4. and never into the answer text

    # 5. the real emitter is back on the context
    from matrx_connect.context.app_context import get_app_context

    assert get_app_context().emitter is base


async def test_context_restored_even_when_the_call_raises(monkeypatch):
    base = _RecordingEmitter()

    async def _boom(messages, system_text, **kwargs):
        raise RuntimeError("provider exploded")

    monkeypatch.setattr(_strict_json, "_run_completion", _boom)
    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:  # pragma: no cover - never called
        raise AssertionError("should not fire")

    with pytest.raises(RuntimeError, match="provider exploded"):
        await llm_stream_text(model="m", system="s", user="u", on_delta=_on_delta)

    from matrx_connect.context.app_context import get_app_context

    assert get_app_context().emitter is base


async def test_falls_back_to_accumulated_tokens_when_final_text_is_empty(monkeypatch):
    """Some provider/emitter combos leave final_text empty; the wrapper holds the
    tokens, and the `_base`-peel in _run_completion must drain THIS wrapper."""
    base = _RecordingEmitter()

    async def _empty_final(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        emitter = get_app_context().emitter
        await emitter.send_chunk("recovered")
        return "", "stop"  # provider reported no final text

    monkeypatch.setattr(_strict_json, "_run_completion", _empty_final)
    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:
        pass

    assert await llm_stream_text(model="m", system="s", user="u", on_delta=_on_delta) == "recovered"


async def test_reasoning_is_split_out_of_the_answer(monkeypatch):
    """A thinking model streams its chain-of-thought on the SAME send_chunk
    channel, fenced by <reasoning>…</reasoning> (Anthropic does NOT use
    send_reasoning_chunk for it). Reasoning must never reach on_delta, never land
    in the returned answer, and never corrupt a caller's incremental parser."""
    base = _RecordingEmitter()
    seen: list[str] = []

    async def _thinking_provider(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        e = get_app_context().emitter
        await e.send_chunk("\n<reasoning>\n")
        await e.send_chunk("Let me think... {\"not\": \"json\"}")
        await e.send_chunk("\n</reasoning>\n")
        await e.send_chunk("The real answer.")
        return "", "stop"  # force the drain fallback so we test the RETURNED text

    monkeypatch.setattr(_strict_json, "_run_completion", _thinking_provider)
    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:
        seen.append(text)

    answer = await llm_stream_text(model="m", system="s", user="u", on_delta=_on_delta)

    assert "reasoning" not in answer.lower()
    assert "Let me think" not in answer
    assert answer.strip() == "The real answer."
    assert not any("Let me think" in s for s in seen)  # parser never saw the CoT
    assert any("Let me think" in r for r in base.reasoning)  # it went to the reasoning channel


async def test_on_delta_none_suppresses_the_stream(monkeypatch):
    """An INTERNAL call (grounding judge, vision caption) must not spray the
    model's raw output into the user's chat."""
    base = _RecordingEmitter()

    async def _run(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        await get_app_context().emitter.send_chunk("secret judge JSON")
        return "secret judge JSON", "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _run)
    _install_ctx(monkeypatch, base)

    out = await llm_stream_text(model="m", system="s", user="u", on_delta=None)

    assert out == "secret judge JSON"  # caller still gets it
    assert base.chunks == []  # the USER never saw a token


async def test_restore_preserves_context_written_during_the_call(monkeypatch):
    """execute_ai_request writes a resolved conversation_id back onto the
    ContextVar mid-call. Restoring our stale pre-call snapshot would silently
    revert it, so the next funnel call re-mints a different conversation."""
    base = _RecordingEmitter()

    async def _writes_ctx(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context, set_app_context

        ctx = get_app_context()
        set_app_context(ctx.with_overrides(conversation_id="conv-123"))
        return "ok", "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _writes_ctx)
    _install_ctx(monkeypatch, base)

    await llm_stream_text(model="m", system="s", user="u", on_delta=None)

    from matrx_connect.context.app_context import get_app_context

    ctx = get_app_context()
    assert ctx.conversation_id == "conv-123"  # the mid-call write SURVIVED
    assert ctx.emitter is base  # ...and the emitter was still restored


def test_base_peel_cannot_escape_the_wrapper():
    """_run_completion's empty-text fallback does `getattr(emitter, "_base", emitter)`.
    The wrapper holds its inner emitter as `_inner` precisely so that peel finds
    nothing and drains the wrapper (which has the tokens) — not the inner emitter
    (which never saw them)."""
    wrapper = _DeltaEmitter(_RecordingEmitter(), None)
    assert getattr(wrapper, "_base", wrapper) is wrapper


def _install_ctx(monkeypatch, emitter):
    """Put a minimal AppContext carrying `emitter` on the ContextVar."""
    from matrx_connect.context.app_context import get_app_context, set_app_context

    try:
        ctx = get_app_context().with_overrides(emitter=emitter)
    except Exception:
        from matrx_connect.context.app_context import AppContext

        ctx = AppContext(user_id="u", emitter=emitter)  # type: ignore[call-arg]
    set_app_context(ctx)
    return ctx
