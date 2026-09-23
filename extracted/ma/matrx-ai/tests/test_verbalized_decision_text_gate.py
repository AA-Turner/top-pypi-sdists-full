"""A text model answering decision questions never streams its raw JSON.

THE BREAK THIS CATCHES: a verbalized decision (Sonnet answering the questions
bound to a structured output) streamed its raw reply as chunks, so the live
chat showed a JSON code block ABOVE the answers card — and the block vanished
on reload, because the stored message holds only the ``decision_answers`` part
(2026-09-22, "Feedback triage (Sonnet)" in /chat). Live must equal reloaded.
"""

from __future__ import annotations

import inspect
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    get_app_context,
    set_app_context,
)

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent
from matrx_ai.decisions.emit import VerbalizedDecisionTextGate
from matrx_ai.decisions.translate import prepare_verbalized_decision
from matrx_ai.orchestrator.requests import AIMatrixRequest
from matrx_ai.providers import unified_client as unified_client_mod
from matrx_ai.providers.unified_client import UnifiedAIClient

_ANSWER_JSON = (
    '{"answers": {"is_defect": {"answer": true, "probability": 0.97, "confidence": 0.92}}}'
)


class _Recorder:
    def __init__(self) -> None:
        self.chunks: list[str] = []
        self.data: list = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)

    async def send_data(self, payload) -> None:
        self.data.append(payload)


def _config() -> UnifiedConfig:
    message = UnifiedMessage(
        role="user",
        content=[
            TextContent(text="Filed as: bug\nPage: https://aimatrx.com/data-v2\n\nEvery quote card stays on Loading."),
            DecisionQuestionsContent(
                questions=[
                    {
                        "name": "is_defect",
                        "type": "noul",
                        "instructions": "Is this a defect rather than a request?",
                    }
                ]
            ),
        ],
    )
    return UnifiedConfig(model="claude-sonnet-5", messages=[message])


@pytest.mark.asyncio
async def test_the_gate_drops_answer_text_and_keeps_reasoning_whole():
    inner = _Recorder()
    gate = VerbalizedDecisionTextGate(inner)

    await gate.send_chunk("\n<reasoning>\nThe board never resolves")
    await gate.send_chunk(" its cards.\n</reasoning>\n")
    await gate.send_chunk(_ANSWER_JSON[:30])
    await gate.send_chunk(_ANSWER_JSON[30:])
    await gate.send_chunk("\n<reasoning>\nsecond pass\n</reasoning>\nleftover")

    streamed = "".join(inner.chunks)
    assert '"answers"' not in streamed and "leftover" not in streamed
    assert streamed.count("<reasoning>") == 2 and streamed.count("</reasoning>") == 2
    assert "The board never resolves its cards." in streamed
    assert gate.dropped_chars > len(_ANSWER_JSON)
    # Everything that is not a chunk passes straight through.
    await gate.send_data("event")
    assert inner.data == ["event"]


@pytest.mark.asyncio
async def test_a_verbalized_turn_streams_no_json_and_restores_the_emitter(monkeypatch):
    user_emitter = _Recorder()
    token = set_app_context(AppContext(emitter=user_emitter))
    try:
        config = _config()
        overlay = prepare_verbalized_decision(
            config, model_name="claude-sonnet-5", supports_structured_output=True
        )
        assert overlay is not None

        async def _dispatch(_self, request):
            # Exactly what _execute_dispatch does once the overlay exists, then
            # what a provider does: read the CONTEXT emitter and stream.
            request.config.metadata = {unified_client_mod._VERBALIZED_DECISION_KEY: overlay}
            unified_client_mod._install_decision_text_gate(request.config)
            emitter = get_app_context().emitter
            await emitter.send_chunk("\n<reasoning>\nweighing it\n</reasoning>\n")
            await emitter.send_chunk(_ANSWER_JSON)
            return SimpleNamespace(
                messages=[UnifiedMessage(role="assistant", content=[TextContent(text=_ANSWER_JSON)])],
                usage=SimpleNamespace(input_tokens=900, output_tokens=60),
                metadata={},
            )

        monkeypatch.setattr(UnifiedAIClient, "_execute_dispatch", _dispatch)
        response = await UnifiedAIClient().execute(
            AIMatrixRequest(conversation_id="triage-gate", config=config)
        )

        assert response.messages[-1].content[0].answers.answers["is_defect"].answer is True
        streamed = "".join(user_emitter.chunks)
        assert '"answers"' not in streamed, "the raw structured reply reached the live stream"
        assert "weighing it" in streamed
        assert [getattr(e, "type", "") for e in user_emitter.data] == ["decision_answers"]
        assert get_app_context().emitter is user_emitter, "the gate outlived its dispatch"
    finally:
        clear_app_context(token)


@pytest.mark.asyncio
async def test_the_emitter_is_restored_when_the_dispatch_raises(monkeypatch):
    user_emitter = _Recorder()
    token = set_app_context(AppContext(emitter=user_emitter))
    try:
        config = _config()

        async def _dispatch(_self, request):
            request.config.metadata = {}
            unified_client_mod._install_decision_text_gate(request.config)
            raise RuntimeError("provider refused")

        monkeypatch.setattr(UnifiedAIClient, "_execute_dispatch", _dispatch)
        with pytest.raises(RuntimeError):
            await UnifiedAIClient().execute(AIMatrixRequest(conversation_id="x", config=config))
        assert get_app_context().emitter is user_emitter
    finally:
        clear_app_context(token)


def test_the_real_dispatch_installs_the_gate_with_the_overlay():
    source = inspect.getsource(UnifiedAIClient._execute_dispatch)
    overlay_at = source.index("config.metadata[_VERBALIZED_DECISION_KEY] = _decision_overlay")
    assert "_install_decision_text_gate(config)" in source[overlay_at : overlay_at + 200]
