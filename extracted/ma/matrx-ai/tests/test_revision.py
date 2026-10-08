"""``revise_until_passing`` — check, revise in the SAME conversation, never pay twice.

Fakes record every turn sent, so a test cannot pass against a loop that sent
nothing, sent to the wrong conversation, or smuggled text through user_input.
"""

from __future__ import annotations

from typing import Any

import pytest
from matrx_graph.checks import ResponseCheckSpec

from matrx_ai.config import TextContent, UnifiedMessage, host_authored_user_turn
from matrx_ai.revision import find_revision_turn, revise_until_passing, revision_key

LENGTH = ResponseCheckSpec(key="length", type="length", target_value="target_word_count")
VALUES = {"target_word_count": 300}
ASK = "Please revise to fit the check report."


def words(n: int) -> str:
    return " ".join(["w"] * n)


class FakeConversation:
    """A conversation that persists turns; ``crash_after_host_turn`` kills the worker mid-turn."""

    def __init__(self, replies: list[str], *, crash_after_host_turn: bool = False) -> None:
        self.replies = list(replies)
        self.messages: list[Any] = []
        self.sent: list[dict[str, Any]] = []
        self.crash = crash_after_host_turn

    async def send(self, conversation_id, host_turn, context, retry):
        self.sent.append({"conversation_id": conversation_id, "host_turn": host_turn,
                          "context": context, "retry": retry})
        if host_turn is not None:
            msg = host_authored_user_turn(host_turn["text"], reason=host_turn["reason"])
            msg.metadata.update(host_turn["metadata"])
            self.messages.append(msg)
        if self.crash:
            self.crash = False
            raise RuntimeError("worker killed mid-turn")
        text = self.replies.pop(0)
        self.messages.append(UnifiedMessage(role="assistant", content=[TextContent(text=text)]))
        return text, f"req-{len(self.sent)}", 0.01, None

    async def read(self, conversation_id):
        return list(self.messages)


async def ask(_cid):
    return ASK


async def no_ask(_cid):
    return None


async def run(conv: FakeConversation, answer: str, **kw):
    base = dict(conversation_id="conv-1", answer=answer, checks=[LENGTH], values=VALUES,
                max_revisions=1, key_base="run:node:root:0", send_turn=conv.send,
                read_turns=conv.read, resolve_request=ask, tolerance_pct=20.0)
    base.update(kw)
    return await revise_until_passing(**base)


@pytest.mark.asyncio
async def test_passing_answer_costs_nothing():
    conv = FakeConversation([])
    out = await run(conv, words(300))
    assert out.outcome == "passed" and conv.sent == [] and out.warning_label() is None


@pytest.mark.asyncio
async def test_over_long_answer_is_revised_in_the_same_conversation_as_a_host_turn():
    conv = FakeConversation([words(310)])
    out = await run(conv, words(1450))
    assert out.outcome == "revised" and out.revision_turns == 1
    (turn,) = conv.sent
    assert turn["conversation_id"] == "conv-1" and turn["retry"] is False
    assert turn["host_turn"]["text"] == ASK
    assert turn["host_turn"]["metadata"]["revision_key"] == revision_key("run:node:root:0", 1)
    report = turn["context"]["response_check"]
    assert "1,450 words" in report["content"] and report["max_inline_chars"] > 200
    stored = conv.messages[0]
    assert stored.user_content == [] and stored.metadata["authored_by"] == "host"
    assert out.warning_label() == "response_check.revised"


@pytest.mark.asyncio
async def test_no_revision_request_variable_is_not_revisable_never_a_fallback_prompt():
    conv = FakeConversation([words(300)])
    out = await run(conv, words(1450), resolve_request=no_ask)
    assert out.outcome == "not_revisable" and conv.sent == []
    assert "revision_request" in out.reason
    assert out.warning_label() == "response_check.not_revisable"


@pytest.mark.asyncio
async def test_max_revisions_zero_is_check_only():
    conv = FakeConversation([])
    out = await run(conv, words(1450), max_revisions=0)
    assert out.outcome == "off_target" and conv.sent == []


@pytest.mark.asyncio
async def test_exhausted_keeps_the_closest_attempt():
    conv = FakeConversation([words(500), words(900)])
    out = await run(conv, words(1450), max_revisions=2)
    assert out.outcome == "off_target" and out.final.text == words(500)


@pytest.mark.asyncio
async def test_strict_check_fails_only_when_its_tries_are_used_up():
    strict = ResponseCheckSpec(key="length", type="length", target_value="target_word_count",
                               on_exhausted="fail")
    conv = FakeConversation([words(1000)])
    out = await run(conv, words(1450), checks=[strict])
    assert out.outcome == "failed"


@pytest.mark.asyncio
async def test_run_budget_from_durable_rows_stops_revising():
    conv = FakeConversation([words(300)])
    out = await run(conv, words(1450), run_budget_left=0)
    assert conv.sent == [] and out.outcome == "off_target" and "budget" in out.reason


@pytest.mark.asyncio
async def test_killed_worker_mid_turn_never_appends_a_second_host_turn_or_repays():
    conv = FakeConversation([words(300)], crash_after_host_turn=True)
    with pytest.raises(RuntimeError):
        await run(conv, words(1450))
    # The resumed invocation finds its own host turn (same deterministic key) with no
    # answer yet: it finishes THAT turn with retry — no second host turn is written.
    out = await run(conv, words(1450))
    assert out.outcome == "revised"
    assert [s["retry"] for s in conv.sent] == [False, True]
    assert conv.sent[1]["host_turn"] is None
    assert sum(1 for m in conv.messages if m.metadata.get("authored_by") == "host") == 1
    # And a THIRD run (the answer is now persisted) reuses it — zero new turns.
    before = len(conv.sent)
    again = await run(conv, words(1450))
    assert again.outcome == "revised" and len(conv.sent) == before
    assert again.attempts[-1].reused is True and again.revision_cost_usd == 0.0


def test_find_revision_turn_ignores_other_keys():
    m = host_authored_user_turn("x", reason="response_check_revision")
    m.metadata["revision_key"] = "other"
    assert find_revision_turn([m], "mine") == (False, None)


def test_a_host_turn_keeps_structured_output_enforced():
    """No forced override: a turn with user_input=None never relaxes the JSON contract."""
    from matrx_ai.config.response_format import (
        STRUCTURED_OUTPUT_SATISFIED_KEY,
        response_format_transition_after_first_structured_answer,
    )

    answered = UnifiedMessage(role="assistant", content=[TextContent(text='{"a": 1}')],
                              metadata={"provider_iteration": 0,
                                        STRUCTURED_OUTPUT_SATISFIED_KEY: True})

    class Cfg:
        response_format = {"type": "json_schema", "json_schema": {"schema": {"type": "object"}}}
        messages = [answered]

    # A human follow-up relaxes it (proves the fixture reaches the relaxing branch)...
    assert response_format_transition_after_first_structured_answer(Cfg(), user_input="why?") is not None
    # ...a host turn (user_input None) keeps it.
    assert response_format_transition_after_first_structured_answer(Cfg(), user_input=None) is None


def test_podcast_spoken_text_counts_only_what_tts_voices():
    from matrx_ai.agent_runners.podcast_generator import podcast_spoken_text

    script = (
        "Some thinking first.\n<podcast_dialogue>\nAlex: Hello there [laughs] friend.\n"
        "Sam: Hi Alex.\n</podcast_dialogue>"
    )
    from matrx_graph.checks import text_metrics

    assert text_metrics(podcast_spoken_text(script))["words"] == 5  # labels and tags not counted


def test_podcast_script_host_check_is_gate_2():
    from matrx_ai.agent_runners.podcast_generator import podcast_script_check

    ok = "<podcast_dialogue>\nAlex: Hello.\nSam: Hi.\n</podcast_dialogue>"
    assert podcast_script_check(ok, {"host_count": 2}) is None
    assert "exactly 3" in podcast_script_check(ok, {"host_count": 3})
    assert "Jordan" in podcast_script_check(ok, {"host_count": 2, "speaker_names": ["Alex", "Jordan"]})
    assert "no usable" in podcast_script_check("just prose", {"host_count": 2})


@pytest.mark.asyncio
async def test_the_real_activation_line_reader_resolves_the_agents_revision_request(monkeypatch):
    """The live seam, not a double: ``agent_revision_request`` reads the
    conversation's agent through the real agx facade. Its first live run
    (W3 run 2e349e5b, 2026-10-07) died on ``ImportError: cannot import name
    'agx' from 'matrx_ai.db'`` because every other test injects
    ``resolve_request`` — this one runs the real reader with only the two
    database reads stubbed."""
    from types import SimpleNamespace

    from matrx_ai import revision
    from matrx_ai.agents import live_structure
    from matrx_ai.db import agx_manager

    async def source(conversation_id):
        return SimpleNamespace(named_agent_id="agent-1", named_is_version=False, is_live=False)

    async def load(agent_id, is_version=False):
        assert (agent_id, is_version) == ("agent-1", False)
        return SimpleNamespace(
            variable_defaults={
                revision.REVISION_REQUEST_VARIABLE: SimpleNamespace(
                    default_value="Please revise the script to fit the target."
                )
            }
        )

    monkeypatch.setattr(live_structure, "read_structure_source", source)
    monkeypatch.setattr(agx_manager.agx, "load_for_execution", load)
    assert await revision.agent_revision_request("conv-1") == (
        "Please revise the script to fit the target."
    )
