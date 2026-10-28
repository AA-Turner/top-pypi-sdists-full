"""``ai.conversation.fork_and_run``: the node forks through the host seam and asks its question on the copy."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.graph_nodes.tests.test_graph_nodes import _FakeContinueRequest, _make_completed


@pytest.mark.asyncio
async def test_the_question_is_a_host_turn_on_the_fork_and_the_result_names_the_fork():
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    import matrx_ai
    from matrx_ai._ext import _registry
    from matrx_ai.graph_nodes.conversation_action import (
        ConversationForkAndRunInput,
        conversation_fork_and_run,
    )

    calls: dict[str, Any] = {}

    async def _fake_fork(conversation_id, request, ctx):
        calls["source"] = conversation_id
        calls["request"] = request
        fork = SimpleNamespace(new_conversation_id="fork-1", forked_at_position=6)
        return fork, _make_completed(text="my reflection", conversation_id="fork-1")

    matrx_ai.configure(conversation_fork_runner=_fake_fork, ForkAndRunRequest=_FakeContinueRequest)
    try:
        inputs = ConversationForkAndRunInput(
            conversation_id="conv-1",
            from_message_id="m6",
            question="Debrief your answer. The person said: too long",
            question_reason="agent_debrief",
            config_overrides={"model": "model-x"},
            model_this_turn_only=True,
        )
        step = SimpleNamespace(app=AppContext(user_id="u1", request_id="r1", emitter=None), node_id="n1")
        token = set_app_context(step.app)
        try:
            result = await conversation_fork_and_run(step, inputs)
        finally:
            clear_app_context(token)
    finally:
        _registry.pop("conversation_fork_runner", None)
        _registry.pop("ForkAndRunRequest", None)

    sent = calls["request"].kwargs
    assert calls["source"] == "conv-1"
    assert sent["host_turn"] == {
        "text": "Debrief your answer. The person said: too long",
        "reason": "agent_debrief",
        "metadata": {"visible_to_person": True},
    }
    assert "user_input" not in sent and "question" not in sent and "conversation_id" not in sent
    assert sent["from_message_id"] == "m6" and sent["model_this_turn_only"] is True
    assert sent["keep_whole"] is True  # a question about the copied run sees it uncondensed
    assert sent["config_overrides"] == {"model": "model-x"}
    assert result.status == "success"
    assert result.result.metadata["fork"] == {"source_conversation_id": "conv-1", "forked_at_position": 6}
    assert result.result.final_text == "my reflection"


def test_a_turn_has_one_author():
    import matrx_ai
    from matrx_ai._ext import _registry
    from matrx_ai.graph_nodes.conversation_action import (
        ConversationForkAndRunInput,
        build_fork_request,
    )

    matrx_ai.configure(ForkAndRunRequest=_FakeContinueRequest)
    try:
        asked = build_fork_request(ConversationForkAndRunInput(conversation_id="c", question="Said: ok."))
        assert asked.kwargs["host_turn"]["text"] == "Said: ok."
        with pytest.raises(ValueError, match="mutually exclusive"):
            build_fork_request(ConversationForkAndRunInput(conversation_id="c", question="q", user_input="typed"))
    finally:
        _registry.pop("ForkAndRunRequest", None)


def test_a_workflow_names_the_last_message_and_the_agents_own_model_in_words():
    import matrx_ai
    from matrx_ai._ext import _registry
    from matrx_ai.graph_nodes.conversation_action import (
        ConversationForkAndRunInput,
        build_fork_request,
    )

    matrx_ai.configure(ForkAndRunRequest=_FakeContinueRequest)
    try:
        sent = build_fork_request(ConversationForkAndRunInput(
            conversation_id="c", question="q", from_message_id="last",
            config_overrides={"model": "agent", "max_tokens": 10},
        )).kwargs
        assert "from_message_id" not in sent  # every live message: the fork ends at the last one
        assert sent["config_overrides"] == {"max_tokens": 10}  # the agent keeps its own model
        named = build_fork_request(ConversationForkAndRunInput(
            conversation_id="c", question="q", from_message_id="m6",
            config_overrides={"model": "claude-opus-5-5"},
        )).kwargs
        assert named["from_message_id"] == "m6" and named["config_overrides"] == {"model": "claude-opus-5-5"}
    finally:
        _registry.pop("ForkAndRunRequest", None)
