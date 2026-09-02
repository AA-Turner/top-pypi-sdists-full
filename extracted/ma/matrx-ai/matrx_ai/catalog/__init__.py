"""matrx_ai.catalog — the ai.endpoint / ai.api / ai.offering / ai.setting runtime.

Parses the certified catalog contract (ControlRule maps), compiles per-offering
control pipelines (canonical settings -> provider params, with adjustments),
and resolves a model reference to a full ResolvedCallProfile. This is THE routing
path — UnifiedAIClient.execute calls resolve_call_profile once per dispatch.
"""

from matrx_ai.catalog.canonicalize import canonical_settings_from_config
from matrx_ai.catalog.controls import (
    Adjustment,
    CompiledControlsMap,
    UnmappedValueError,
    compile_controls,
    merge_rule_dicts,
    validate_rules_against_settings,
)
from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.catalog.host_catalog import (
    CatalogModel,
    ModelCatalog,
    get_model_catalog,
    get_runtime_model,
    list_runtime_models,
    register_runtime_model,
    unregister_runtime_model,
)
from matrx_ai.catalog.manager import (
    QUARANTINED_ROWS,
    SPECIAL_WIRE_FORMATS,
    WIRE_FORMATS,
    AiCatalogManager,
    QuarantineRecord,
    ai_catalog_manager,
)
from matrx_ai.catalog.models import (
    CatalogApi,
    CatalogEndpoint,
    CatalogOffering,
    CatalogSetting,
    CatalogVoice,
    ClampSpec,
    ControlRule,
    ControlsMap,
    ResolvedCallProfile,
    RulesEnvelope,
)
from matrx_ai.catalog.processors import (
    ProcessorContext,
    UnknownProcessorError,
    get_processor,
    has_processor,
    register_processor,
)
from matrx_ai.catalog.resolve import (
    client_attr_for_wire_format,
    resolve_call_profile,
    resolve_tts_call_profile,
    resolve_tts_voice,
    select_tts_default_voice,
    validate_tts_voices,
)

__all__ = [
    "Adjustment",
    "AiCatalogManager",
    "CatalogModel",
    "ModelCatalog",
    "get_model_catalog",
    "get_runtime_model",
    "list_runtime_models",
    "register_runtime_model",
    "unregister_runtime_model",
    "CatalogApi",
    "CatalogEndpoint",
    "CatalogOffering",
    "CatalogRoutingError",
    "CatalogSetting",
    "CatalogVoice",
    "ClampSpec",
    "CompiledControlsMap",
    "ControlRule",
    "ControlsMap",
    "ProcessorContext",
    "QUARANTINED_ROWS",
    "QuarantineRecord",
    "ResolvedCallProfile",
    "RulesEnvelope",
    "UnknownProcessorError",
    "UnmappedValueError",
    "get_processor",
    "has_processor",
    "register_processor",
    "SPECIAL_WIRE_FORMATS",
    "WIRE_FORMATS",
    "ai_catalog_manager",
    "canonical_settings_from_config",
    "client_attr_for_wire_format",
    "compile_controls",
    "merge_rule_dicts",
    "resolve_call_profile",
    "resolve_tts_call_profile",
    "resolve_tts_voice",
    "select_tts_default_voice",
    "validate_tts_voices",
    "validate_rules_against_settings",
]
