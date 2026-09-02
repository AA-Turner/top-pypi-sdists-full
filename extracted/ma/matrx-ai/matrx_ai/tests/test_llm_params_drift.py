"""Drift detection: LLMParams ↔ UnifiedConfig.

Ensures every overridable field on UnifiedConfig has a corresponding field in
LLMParams, and vice versa. When a new parameter is added to either side but
not the other, this test fails with a clear diff.

Run with:  python -m pytest ai/tests/test_llm_params_drift.py -v
"""

from dataclasses import fields as dc_fields

from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.unified_config import UnifiedConfig

UNIFIED_CONFIG_INTERNAL_FIELDS = {
    # Conversation / request envelope — not LLM parameter overrides
    "messages",
    "system_instruction",
    "tools",
    "custom_configs",
    "metadata",
    # Resolved at request-prep from model capabilities — never client-overridable
    "supports_tools",
    # The canonical matrx model name, stamped at dispatch by UnifiedAIClient.execute
    # alongside the provider_model_id rewrite of `model`. Server-side attribution
    # bookkeeping, never an LLM param override.
    "matrx_model_name",
    # Ephemeral sibling-offering reroute pin. Executor-owned and deliberately
    # never persisted or exposed as a caller override.
    "runtime_offering_id",
    # Host-resolved ElevenLabs dictionary locators (aidream/services/dictionary/locators.py)
    "pronunciation_dictionary_locators",
    # Skill-injection bookkeeping — the tool ids the skill-merge pipeline injected
    # this turn, written server-side only (aidream/services/tooling/skill_merge.py)
    # for cross-turn diffing. Part of the tool envelope, not an LLM param override.
    "skill_injected_tool_ids",
    # Conversation/tool-policy state. These preserve authored declarations,
    # dynamic mutations, and host-policy transition markers across turns.
    # Exposing them through LLMParams would let a caller forge internal state.
    "system_prompt_frozen",
    "authored_tools",
    "dynamic_tools",
    "tool_authority_filtered",
    "tool_authority_exclusions",
    "tool_authority_filter_applied_runtime",
    "tool_capability_filtered",
    "tool_delegation_filtered",
    "tool_delegation_executors",
    "tool_delegation_disabled_policy",
    "tool_delegation_registry_fingerprint",
    "tool_delegation_filter_applied_runtime",
    "authored_custom_tools",
    "authored_mcp_servers",
}


def test_llm_params_covers_all_overridable_unified_config_fields():
    """Every overridable UnifiedConfig field must exist in LLMParams."""
    config_fields = {f.name for f in dc_fields(UnifiedConfig)} - UNIFIED_CONFIG_INTERNAL_FIELDS

    param_fields = set(LLMParams.model_fields.keys())

    missing_from_params = config_fields - param_fields
    assert not missing_from_params, (
        f"Fields in UnifiedConfig but missing from LLMParams: {missing_from_params}. "
        f"Add them to ai/config/llm_params.py."
    )


def test_llm_params_has_no_extra_fields():
    """Every LLMParams field must correspond to a UnifiedConfig field."""
    config_fields = {f.name for f in dc_fields(UnifiedConfig)}
    param_fields = set(LLMParams.model_fields.keys())

    extra_in_params = param_fields - config_fields
    assert not extra_in_params, (
        f"Fields in LLMParams but missing from UnifiedConfig: {extra_in_params}. "
        f"Either add them to UnifiedConfig or remove from LLMParams."
    )
