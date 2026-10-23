"""A call is made to FIT every limit before it is sent — never refused for a size we could shrink.

THE DEFECT (2026-10-22, conversation 9b224bf5): a sandbox conversation on a 1,000,000-token model
reached ~270k input tokens. The window pre-flight passed, the cost-gated trim held, and the host's
200,000-token per-call budget refused the call — the conversation died. Nothing measured the call
against the LOWER limit before sending, and nothing shrank it.

Locked here:
1. A call over the host's budget is shrunk under it before the send (RED with no fit step).
2. The newest iteration's results are never cut — the model always sees what it just did.
3. Compaction (the summarization seam) runs FIRST at the RESOLVE stage; when it fits the call, no
   forced trim runs. At the LOOP stage it never runs: the list is the executor's ledger.
4. A call under every limit is untouched.
5. ``prepare_for_send`` runs the fit step between the trim and the pre-flight.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.config import (
    ToolCallContent,
    ToolResultContent,
    UnifiedMessage,
    context_preflight,
    input_fit,
)
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.send_boundary import (
    STAGE_LOOP,
    STAGE_RESOLVE,
    _forced_trim,
    prepare_for_send,
    reset_loop_state,
)

CONVERSATION_ID = "conv-input-fit"
REQUEST_ID = "req-input-fit"


def _result(i: int, chars: int) -> UnifiedMessage:
    return UnifiedMessage(
        role="tool",
        position=None,
        content=[
            ToolResultContent(
                tool_use_id=f"call-{i}",
                name="shell_execute",
                content="x" * chars,
                output_chars=chars,
            )
        ],
    )


def _call(i: int) -> UnifiedMessage:
    return UnifiedMessage(
        role="assistant",
        position=None,
        content=[
            ToolCallContent(
                id=f"call-{i}", name="shell_execute", arguments={"command": f"step {i}"}
            )
        ],
    )


def _long_tool_loop(iterations: int = 12, chars: int = 60_000) -> SimpleNamespace:
    messages: list[UnifiedMessage] = [UnifiedMessage(role="user", content=[])]
    for i in range(iterations):
        messages.append(_call(i))
        messages.append(_result(i, chars))
    return SimpleNamespace(
        model="claude-opus-5-5",
        matrx_model_name="claude-opus-5-5",
        messages=messages,
        system_instruction=None,
        tools=[],
        prompt_cache_key=None,
    )


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    context_preflight.configure_context_preflight(enabled=True, trip_fraction=1.0)
    # The model's window is huge (like Opus 5.5's 1M) — only the HOST budget binds.
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: 1_000_000)
    input_fit.set_compactor(None)
    yield
    input_fit.set_input_budget_resolver(None)
    input_fit.set_compactor(None)
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


def _budget(limit: int):
    input_fit.set_input_budget_resolver(
        lambda _ctx, config: (limit, estimate_prompt_tokens(config))
    )


@pytest.mark.asyncio
async def test_a_call_over_the_host_budget_is_shrunk_under_it_before_the_send() -> None:
    config = _long_tool_loop()
    before = estimate_prompt_tokens(config)
    limit = before // 3
    _budget(limit)

    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )

    after = estimate_prompt_tokens(config)
    assert record and record["fits"] is True, f"still {after:,} over a {limit:,} budget: {record}"
    assert after <= limit < before
    newest = config.messages[-1].content[0]
    assert newest.content == "x" * 60_000, (
        "the newest result was cut — the model must see what it just did"
    )


@pytest.mark.asyncio
async def test_compaction_runs_first_and_a_fitting_compaction_skips_the_forced_trim() -> None:
    config = _long_tool_loop()
    _budget(estimate_prompt_tokens(config) // 3)
    calls: list[dict] = []

    async def _compact(cfg, *, limit_tokens, estimated_tokens, ctx, conversation_id):
        assert conversation_id == CONVERSATION_ID
        calls.append({"limit": limit_tokens, "estimated": estimated_tokens})
        cfg.messages[:] = cfg.messages[:1] + cfg.messages[-2:]  # a summary would stand here
        return True

    input_fit.set_compactor(_compact)
    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_RESOLVE, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )

    assert len(calls) == 1 and record["fits"] is True
    assert [p["pass"] for p in record["passes"]] == ["compaction"]


@pytest.mark.asyncio
async def test_a_call_under_every_limit_is_untouched() -> None:
    config = _long_tool_loop(iterations=2, chars=1_000)
    _budget(10_000_000)

    def _bodies():
        return [repr(m.content) for m in config.messages]

    snapshot = _bodies()
    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )
    assert record["fits"] is True and "passes" not in record
    assert _bodies() == snapshot


@pytest.mark.asyncio
async def test_the_send_boundary_runs_the_fit_step() -> None:
    config = _long_tool_loop()
    limit = estimate_prompt_tokens(config) // 3
    _budget(limit)

    prep = await prepare_for_send(
        config, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, request_id=REQUEST_ID
    )

    assert "input_fit" in prep.steps
    assert prep.fit and prep.fit["fits"] is True
    assert estimate_prompt_tokens(config) <= limit


@pytest.mark.asyncio
async def test_a_compactor_that_raises_falls_through_to_the_forced_trim() -> None:
    config = _long_tool_loop()
    limit = estimate_prompt_tokens(config) // 3
    _budget(limit)

    async def _broken(cfg, **_kw):
        raise RuntimeError("summarizer down")

    input_fit.set_compactor(_broken)
    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_RESOLVE, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )
    assert record["passes"][0] == {"pass": "compaction", "changed": False}
    assert record["fits"] is True and estimate_prompt_tokens(config) <= limit


@pytest.mark.asyncio
async def test_a_call_that_cannot_fit_says_so_and_names_every_pass() -> None:
    config = _long_tool_loop(iterations=1)  # only the newest iteration — protected, nothing to trim
    _budget(1)
    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )
    assert record["fits"] is False
    assert [p["pass"] for p in record["passes"]] == ["forced_trim_4_8", "forced_trim_2_2"]
    assert record["after"][-1]["estimated_tokens"] > 1


@pytest.mark.asyncio
async def test_the_compactor_never_runs_at_the_loop_stage() -> None:
    """At the loop stage ``config.messages`` is the executor's ledger (its cursors are indexes);
    a compactor that splices it files ``persisted_history_shifted``. Only the forced trim runs."""
    config = _long_tool_loop()
    ledger = list(config.messages)
    limit = estimate_prompt_tokens(config) // 3
    _budget(limit)
    calls: list[int] = []

    async def _compact(cfg, **_kw):
        calls.append(1)
        cfg.messages[:] = cfg.messages[:1] + cfg.messages[-2:]
        return True

    input_fit.set_compactor(_compact)
    record = await input_fit.ensure_fits(
        config, policy=None, stage=STAGE_LOOP, conversation_id=CONVERSATION_ID, trim=_forced_trim
    )
    assert calls == []
    assert record["passes"][0] == {"pass": "compaction", "changed": False, "skipped": "loop_stage"}
    assert len(config.messages) == len(ledger)
    assert all(a is b for a, b in zip(config.messages, ledger, strict=True))
    assert record["fits"] is True and estimate_prompt_tokens(config) <= limit
