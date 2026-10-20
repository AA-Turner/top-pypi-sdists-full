"""The agent's open task list is restated at the END of every loop send.

2026-10-14 (chat.conversation 3787dd66): an agent approved a six-step plan at
iteration 13, then made 66 more model calls and ~170 tool calls without ever
touching it — the plan sat once at message 27 of 135. These tests fail the day
the plan block goes missing from a loop send, moves into the system prompt, or
lands before Anthropic's rolling cache breakpoint.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.live_plan import (
    LIVE_PLAN_SLOT,
    LivePlanSettings,
    LivePlanSnapshot,
    PlanTask,
    render_live_plan,
    set_live_plan_source,
    tool_calls_since_plan_update,
)
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send
from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.instructions.core import SystemInstruction
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.providers.openai.translator import OpenAITranslator
from matrx_ai.testing.profile_factory import make_profile

TASKS = [
    PlanTask(id="t1", title="Inventory the Notion workspace", status="done"),
    PlanTask(id="t2", title="Create the matching notes", status="in_progress"),
    PlanTask(id="t3", title="Verify nothing was lost", status="pending"),
]


def _loop_messages(*, extra_calls: int = 0, plan_touch: bool = True) -> list[UnifiedMessage]:
    messages = [
        UnifiedMessage(role="user", content=[TextContent(text="Move my Notion workspace over.")]),
    ]
    if plan_touch:
        messages += [
            UnifiedMessage(
                role="assistant",
                content=[
                    ToolCallContent(
                        id="p1", name="tasks", arguments={"action": "set_status", "id": "t1", "status": "done"}
                    )
                ],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id="p1", call_id="p1", name="tasks", content="ok")],
            ),
        ]
    for i in range(extra_calls):
        cid = f"c{i}"
        messages += [
            UnifiedMessage(
                role="assistant",
                content=[ToolCallContent(id=cid, name="notes", arguments={"action": "create"})],
            ),
            UnifiedMessage(
                role="tool",
                content=[ToolResultContent(tool_use_id=cid, call_id=cid, name="notes", content="created")],
            ),
        ]
    return messages


def _config(messages: list[UnifiedMessage], model: str = "claude-sonnet-5") -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        messages=messages,
        system_instruction=SystemInstruction(base_instruction="You migrate workspaces."),
    )


async def _source(conversation_id: str, organization_id: str | None) -> LivePlanSnapshot:
    return LivePlanSnapshot(tasks=list(TASKS), settings=LivePlanSettings(nudge_after_tool_calls=15))


@pytest.fixture
def plan_source():
    set_live_plan_source(_source)
    yield
    set_live_plan_source(None)


def _anthropic_profile():
    return make_profile(
        model_name="claude-sonnet-5",
        wire_format="anthropic_chat",
        capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"},
    )


# ── the counter ──────────────────────────────────────────────────────────────


def test_counter_counts_calls_after_the_last_plan_write():
    assert tool_calls_since_plan_update(_loop_messages(extra_calls=4)) == 4


def test_a_tasks_list_read_does_not_reset_the_counter():
    messages = _loop_messages(extra_calls=2)
    messages.append(
        UnifiedMessage(
            role="assistant",
            content=[ToolCallContent(id="r", name="tasks", arguments={"action": "list"})],
        )
    )
    assert tool_calls_since_plan_update(messages) == 3


# ── the block ────────────────────────────────────────────────────────────────


def test_the_block_names_every_step_status_and_the_current_step():
    block = render_live_plan(TASKS, tool_calls_since_update=2, settings=LivePlanSettings())
    assert block is not None
    for task in TASKS:
        assert task.title in block and task.id in block
    assert "In progress now: Create the matching notes" in block
    assert "1 of 3 done" in block
    assert "without updating" not in block


def test_the_block_nudges_past_the_threshold():
    block = render_live_plan(TASKS, tool_calls_since_update=15, settings=LivePlanSettings(nudge_after_tool_calls=15))
    assert block is not None and "15 tool calls without updating your task list" in block


def test_no_open_tasks_means_no_block():
    finished = [PlanTask(id="t1", title="All done", status="done")]
    assert render_live_plan(finished, tool_calls_since_update=40, settings=LivePlanSettings()) is None


def test_max_steps_summarizes_the_rest():
    many = [PlanTask(id=f"t{i}", title=f"Step {i}", status="pending") for i in range(30)]
    block = render_live_plan(many, tool_calls_since_update=0, settings=LivePlanSettings(max_steps=5))
    assert block is not None and "Step 4" in block and "Step 5 " not in block
    assert "25 more step(s), 25 still open" in block


# ── the send boundary stages it on every loop send ──────────────────────────


@pytest.mark.asyncio
async def test_every_loop_send_stages_the_plan(plan_source):
    config = _config(_loop_messages(extra_calls=16))
    prep = await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    assert "live_plan" in prep.steps
    assert prep.live_plan and prep.live_plan["nudged"] is True
    staged = config.messages.tail_context_blocks().get(LIVE_PLAN_SLOT)
    assert staged and "Verify nothing was lost" in staged


@pytest.mark.asyncio
async def test_a_finished_plan_clears_the_slot(plan_source):
    config = _config(_loop_messages(extra_calls=1))
    config.messages.attach_tail_context("stale plan", slot=LIVE_PLAN_SLOT)

    async def finished(conversation_id, organization_id):
        return LivePlanSnapshot(tasks=[PlanTask(id="t1", title="x", status="done")])

    set_live_plan_source(finished)
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    assert LIVE_PLAN_SLOT not in config.messages.tail_context_blocks()


# ── every wire carries it at the end, never in the system prompt ───────────


@pytest.mark.asyncio
async def test_anthropic_wire_ends_with_the_plan_after_the_cache_breakpoint(plan_source):
    config = _config(_loop_messages(extra_calls=3))
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    wire = AnthropicTranslator().to_anthropic(config, _anthropic_profile())

    # Owner ruling 2026-10-18 (defects 23 + 35): host text never travels inside
    # the person's / tool-result message. The plan rides its OWN host turn after
    # the newest message.
    last = wire["messages"][-1]
    assert last["role"] == "user"
    tail = last["content"][-1]
    assert tail["type"] == "text" and "<your_plan" in tail["text"]
    assert len(last["content"]) == 1 and "cache_control" not in tail
    # The cache breakpoint stays on the newest tool_result turn, BEFORE the plan,
    # so the next send reads the prefix this one wrote.
    newest = wire["messages"][-2]
    assert newest["content"][-1]["type"] == "tool_result"
    assert "cache_control" in newest["content"][-1]
    assert "<your_plan" not in str(newest)
    system_text = " ".join(b.get("text", "") for b in wire.get("system", []))
    assert "<your_plan" not in system_text


@pytest.mark.asyncio
async def test_the_persons_own_turn_gets_nothing_appended(plan_source):
    config = _config(_loop_messages(extra_calls=0, plan_touch=False))
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    wire = AnthropicTranslator().to_anthropic(config, _anthropic_profile())
    assert "<your_plan" not in str(wire["messages"])


@pytest.mark.asyncio
async def test_openai_and_chat_completions_wires_end_with_the_plan(plan_source):
    config = _config(_loop_messages(extra_calls=2), model="gpt-5")
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())

    responses = OpenAITranslator().to_openai(
        config,
        make_profile(model_name="gpt-5", wire_format="openai_responses",
                     capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"}),
    )
    assert responses["input"][-1]["role"] == "developer"
    assert "<your_plan" in responses["input"][-1]["content"][0]["text"]
    assert "<your_plan" not in str(responses["input"][0])

    generic = GenericOpenAITranslator().to_generic_openai(
        config,
        make_profile(model_name="gpt-5", wire_format="openai_chat",
                     capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"}),
    )
    # Chat-Completions providers (owner ruling L29, 2026-10-18): the block rides its
    # OWN user turn after the newest message, exactly as on Anthropic/OpenAI/Google —
    # never in the system message (their exact-prefix caches include it) and never
    # inside the newest message. The plan is the last thing on the wire.
    assert generic["messages"][0]["role"] == "system"
    assert "<your_plan" not in str(generic["messages"][0])
    last = generic["messages"][-1]
    assert last["role"] == "user"
    last_text = last["content"] if isinstance(last["content"], str) else " ".join(
        b.get("text", "") for b in last["content"]
    )
    assert "<your_plan" in last_text
    assert last_text.rstrip().endswith("</your_plan>"), "the plan (and its reminder) must be last"
    assert generic["messages"][-2]["role"] == "tool"
    assert "<your_plan" not in str(generic["messages"][:-1])


@pytest.mark.asyncio
async def test_google_wire_ends_with_the_plan(plan_source):
    config = _config(_loop_messages(extra_calls=2), model="gemini-3-pro")
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    wire = GoogleTranslator().to_google(
        config,
        make_profile(model_name="gemini-3-pro", wire_format="google_genai",
                     capabilities={"input": ["text"], "output": ["text"], "features": ["function_calling"], "interaction": "turn"}),
    )
    last = wire["contents"][-1]
    assert last["role"] == "user"
    assert "<your_plan" in last["parts"][-1]["text"]
