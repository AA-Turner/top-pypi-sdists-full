"""The agent's long-cache setting must survive EVERY door into UnifiedConfig.

2026-10-16: ``settings.extended_prompt_cache`` was a declared UnifiedConfig field, but
``UnifiedConfig.from_dict`` (the one door every run path funnels through: stored agent
definitions, the chat route, mandates, workflow nodes, MCP agent_run, agent_call children,
the Model view capture) built the config field by field and never read it, so the
translators always saw ``None`` and the capture showed a 5-minute mark. The stored
conversation config (``to_storage_dict``) dropped it too, so turn 2+ lost it as well.
"""

from __future__ import annotations

import dataclasses
from matrx_utils.source_guard import stable_source
import re

from matrx_ai.client_host.agent_source import ExecutionAgentDefinition, definition_to_agent_config
from matrx_ai.config import UnifiedConfig
from matrx_ai.providers.anthropic.translator import AnthropicTranslator
from matrx_ai.providers.unified_client import _build_provider_wire_config
from matrx_ai.testing.profile_factory import make_profile

ONE_HOUR = {"type": "ephemeral", "ttl": "1h"}
FIVE_MIN = {"type": "ephemeral"}


def _definition(settings: dict) -> ExecutionAgentDefinition:
    return ExecutionAgentDefinition.model_validate(
        {
            "definition_id": "d1",
            "agent_id": "a1",
            "model_id": "claude-haiku-4-5",
            "messages": [
                {"role": "system", "content": [{"type": "text", "text": "You are a careful drafter."}]},
                {"role": "user", "content": [{"type": "text", "text": "Draft a reply."}]},
            ],
            "settings": settings,
        }
    )


def _wire(config: UnifiedConfig) -> dict:
    """Exactly the hop the send makes: wire copy of the live config, then the translator."""
    profile = make_profile(model_name="claude-haiku-4-5", wire_format="anthropic_chat")
    wire_config = _build_provider_wire_config(config, profile)
    return AnthropicTranslator().to_anthropic(wire_config, profile)


def test_a_saved_agents_setting_puts_the_one_hour_ttl_on_the_wire() -> None:
    config = definition_to_agent_config(_definition({"stream": True, "extended_prompt_cache": True})).config
    assert config.extended_prompt_cache is True
    request = _wire(config)
    assert request["system"][0]["cache_control"] == ONE_HOUR


def test_without_the_setting_the_mark_stays_five_minutes() -> None:
    config = definition_to_agent_config(_definition({"stream": True})).config
    assert _wire(config)["system"][0]["cache_control"] == FIVE_MIN


def test_the_setting_survives_the_stored_conversation_config() -> None:
    """Turn 2+ rebuilds the config from cx_conversation.config (to_storage_dict -> from_dict)."""
    config = definition_to_agent_config(_definition({"extended_prompt_cache": True})).config
    stored = config.to_storage_dict()["config"]
    assert stored["extended_prompt_cache"] is True
    rebuilt = UnifiedConfig.from_dict({"model": "claude-haiku-4-5", "messages": [], **stored})
    assert rebuilt.extended_prompt_cache is True


def test_every_unified_config_field_is_read_by_from_dict_unless_it_is_runtime_only() -> None:
    """The class guard: a new setting field that from_dict forgets is a silent no-op on every
    run path. Runtime-only fields are computed during a run, never authored in settings."""
    runtime_only = {
        "matrx_model_name",
        "runtime_offering_id",
        "prompt_cache_key",  # stamped at the send boundary
        "prompt_cache_marks",  # stamped at the send boundary (config/cache_plan.py)
        "dynamic_tools_withheld",
        "prompt_block_texts",
        "tool_authority_filter_applied_runtime",
        "tool_delegation_filter_applied_runtime",
        "model_turn_only_restore",
        "supports_tools",
        "held_prompt",  # set by the resolver on a mandate-held turn, settled at the send boundary
    }
    source = stable_source(UnifiedConfig.from_dict)
    forgotten = [
        f.name
        for f in dataclasses.fields(UnifiedConfig)
        if f.name not in runtime_only and not re.search(rf"\b{f.name}\s*=|[\"']{f.name}[\"']", source)
    ]
    assert forgotten == [], f"UnifiedConfig.from_dict never reads: {forgotten}"


def test_a_mandates_held_call_carries_the_holders_long_cache_setting() -> None:
    """Mandate code calls rebuild the request from a Holder through a knob list of their own."""
    from types import SimpleNamespace

    from matrx_ai.mandates import held_request_config

    holder_config = definition_to_agent_config(_definition({"extended_prompt_cache": True})).config
    held = SimpleNamespace(
        model="claude-haiku-4-5",
        system="You label things.",
        turns=[{"role": "user", "content": "label this"}],
        offering_id=None,
        max_output_tokens=None,
        temperature=None,
        config=holder_config,
    )
    assert held_request_config(held).extended_prompt_cache is True
