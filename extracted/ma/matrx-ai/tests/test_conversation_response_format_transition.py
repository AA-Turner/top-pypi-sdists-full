"""Turn-aware structured-output enforcement for persisted conversations."""

from __future__ import annotations

import logging
from copy import deepcopy
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.agents.cache import AgentCache
from matrx_ai.agents.resolver import ConversationResolver
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.response_format import (
    is_clean_structured_output_completion,
    mark_structured_output_contract_satisfied,
)
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

SCHEMA_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "answer",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
            "additionalProperties": False,
        },
    },
}


def _config(*assistant_messages: UnifiedMessage, response_format=None) -> UnifiedConfig:
    messages = MessageList()
    messages.append(UnifiedMessage(role="user", content=[TextContent(text="first request")]))
    for message in assistant_messages:
        messages.append(message)
    return UnifiedConfig(
        model="test-model",
        messages=messages,
        response_format=deepcopy(response_format or SCHEMA_FORMAT),
    )


def _assistant(
    text: str,
    *,
    generated: bool = True,
    status: str = "active",
    contract_satisfied: bool = True,
) -> UnifiedMessage:
    metadata = {"provider_iteration": 1} if generated else {}
    if generated and contract_satisfied:
        metadata["structured_output_contract_satisfied"] = True
    return UnifiedMessage(
        role="assistant",
        content=[TextContent(text=text)],
        status=status,
        metadata=metadata,
    )


async def _resolve(
    monkeypatch,
    config: UnifiedConfig,
    *,
    user_input="follow up",
    overrides=None,
    prior_request_status: str | None = None,
):
    conversation_id = str(uuid4())

    async def _load(_conversation_id: str) -> UnifiedConfig:
        assert _conversation_id == conversation_id
        return deepcopy(config)

    monkeypatch.setattr("matrx_ai.agents.resolver._load_unified_config", _load)
    if prior_request_status is not None:

        async def _load_row(_manager, _conversation_id: str):
            return SimpleNamespace(
                last_request_status=prior_request_status,
                cache_state=None,
                created_at=None,
            )

        monkeypatch.setattr(
            "matrx_ai.db._cx_managers_impl.CxConversationManager.load_conversation_by_id",
            _load_row,
        )
    AgentCache.remove(conversation_id)
    try:
        return await ConversationResolver.from_conversation_id(
            conversation_id,
            user_input=user_input,
            config_overrides=overrides,
        )
    finally:
        AgentCache.remove(conversation_id)


@pytest.mark.asyncio
async def test_followup_relaxes_after_generated_answer_satisfies_schema(
    monkeypatch, caplog
) -> None:
    caplog.set_level(logging.INFO, logger="matrx_ai.config.send_boundary")
    resolved = await _resolve(
        monkeypatch,
        _config(
            _assistant('{"answer":"authored example"}', generated=False),
            _assistant('{"answer":"generated result"}'),
        ),
    )

    assert resolved.response_format == {"type": "text"}
    assert resolved.messages.get_last_by_role("user").get_output() == "follow up"
    transition_logs = [
        record.message
        for record in caplog.records
        if "response_format_relaxed_after_first_structured_answer" in record.message
    ]
    assert len(transition_logs) == 1
    assert "from=json_schema to=text" in transition_logs[0]
    assert "properties" not in transition_logs[0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("assistant", "user_input"),
    [
        (_assistant('{"answer":"authored"}', generated=False), "follow up"),
        (_assistant("not valid JSON", contract_satisfied=False), "follow up"),
        (_assistant('{"answer":"failed"}', status="failed"), "follow up"),
        (_assistant('{"answer":"unconfirmed partial"}', contract_satisfied=False), "follow up"),
        (_assistant('{"answer":"generated result"}'), None),
    ],
)
async def test_schema_stays_bound_without_successful_natural_answer(
    monkeypatch,
    assistant: UnifiedMessage,
    user_input: str | None,
) -> None:
    resolved = await _resolve(monkeypatch, _config(assistant), user_input=user_input)

    assert resolved.response_format == SCHEMA_FORMAT


@pytest.mark.asyncio
async def test_explicit_turn_schema_override_wins_after_structured_answer(monkeypatch) -> None:
    override = LLMParams(response_format=deepcopy(SCHEMA_FORMAT))

    resolved = await _resolve(
        monkeypatch,
        _config(_assistant('{"answer":"generated result"}')),
        overrides=override,
    )

    assert resolved.response_format == SCHEMA_FORMAT


@pytest.mark.asyncio
async def test_null_turn_override_does_not_block_default_relaxation(monkeypatch) -> None:
    override = LLMParams(response_format=None)

    resolved = await _resolve(
        monkeypatch,
        _config(_assistant('{"answer":"generated result"}')),
        overrides=override,
    )

    assert resolved.response_format == {"type": "text"}


@pytest.mark.asyncio
async def test_json_object_relaxes_only_after_generated_object(monkeypatch) -> None:
    resolved = await _resolve(
        monkeypatch,
        _config(
            _assistant('{"answer":"generated result"}'),
            response_format={"type": "json_object"},
        ),
    )

    assert resolved.response_format == {"type": "text"}


def test_completed_valid_output_receives_persisted_success_marker() -> None:
    config = _config(_assistant('{"answer":"generated result"}', contract_satisfied=False))

    marked = mark_structured_output_contract_satisfied(config, result_start_position=1)

    assert marked is True
    assert config.messages[-1].metadata["structured_output_contract_satisfied"] is True


def test_schema_invalid_output_cannot_receive_success_marker() -> None:
    config = _config(_assistant('{"answer":42}', contract_satisfied=False))

    marked = mark_structured_output_contract_satisfied(config, result_start_position=1)

    assert marked is False
    assert "structured_output_contract_satisfied" not in config.messages[-1].metadata


@pytest.mark.asyncio
async def test_pre_marker_completed_conversation_relaxes_after_full_validation(monkeypatch) -> None:
    resolved = await _resolve(
        monkeypatch,
        _config(_assistant('{"answer":"legacy result"}', contract_satisfied=False)),
        prior_request_status="completed",
    )

    assert resolved.response_format == {"type": "text"}


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["failed", "processing", None])
async def test_pre_marker_output_requires_durable_completed_request(monkeypatch, status) -> None:
    resolved = await _resolve(
        monkeypatch,
        _config(_assistant('{"answer":"partial"}', contract_satisfied=False)),
        prior_request_status=status,
    )

    assert resolved.response_format == SCHEMA_FORMAT


@pytest.mark.asyncio
async def test_pre_marker_completed_but_schema_invalid_output_stays_bound(monkeypatch) -> None:
    resolved = await _resolve(
        monkeypatch,
        _config(_assistant('{"answer":42}', contract_satisfied=False)),
        prior_request_status="completed",
    )

    assert resolved.response_format == SCHEMA_FORMAT


@pytest.mark.parametrize("status", ["truncated", "suspended_provider_overload", "cancelled"])
def test_partial_terminal_outcomes_cannot_consume_contract(status: str) -> None:
    assert is_clean_structured_output_completion({"status": status}) is False


@pytest.mark.parametrize("metadata", [{}, {"status": "completed"}])
def test_clean_terminal_outcome_can_consume_contract(metadata: dict) -> None:
    assert is_clean_structured_output_completion(metadata) is True


# --------------------------------------------------------------------------- #
# DD-135 — a STANDING contract does NOT stop the relaxation (round 2).          #
# --------------------------------------------------------------------------- #
#
# Round 1 of DD-135 made a standing contract refuse to relax, so an acting agent
# could act on every turn. V-34 proved live that this costs the user their answer:
# with the schema forced back on, "what is the difference between a project and a
# task?" produced an empty directive, an empty card, and an Approve button reading
# "confirm to run 0 create project with taskses" — a control that would write
# nothing. The relaxation is RIGHT; it is what lets an acting agent speak. The
# dispatch was the thing keyed on the wrong fact, and it now reads the host's
# declared standing contract instead (see test_standing_output_contract_dispatch.py).
#
# This test pins the reversal so nobody re-introduces the suppression.


@pytest.mark.asyncio
async def test_a_standing_declaration_does_not_block_the_relaxation(monkeypatch) -> None:
    from matrx_connect.context.app_context import AppContext, set_app_context

    set_app_context(
        AppContext(
            emitter=None,
            user_id="dd135-test",
            metadata={
                "response_format_standing": True,
                "standing_output_contract": deepcopy(SCHEMA_FORMAT),
            },
        )
    )
    try:
        resolved = await _resolve(
            monkeypatch,
            _config(_assistant('{"answer":"generated result"}')),
        )
    finally:
        set_app_context(AppContext(emitter=None, user_id="dd135-test", metadata={}))

    assert resolved.response_format == {"type": "text"}, (
        "an acting run must still be able to answer in prose — forcing its schema "
        "back on turns a plain question into an empty directive with a live Approve"
    )
