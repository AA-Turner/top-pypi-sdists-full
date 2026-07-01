"""CVC agentic loop primitives — Phase 1, Category 2.

Each module is a focused concern; nothing is wired into ``cvc/agent/llm.py``
or ``cvc/agent/chat.py`` yet. Integration happens in Category 3.
"""
from .budget import IterationBudget
from .compression import CompressionConfig, CompressionResult, ContextCompressor
from .cost_budget import (
    DEFAULT_PRICING,
    CostBudget,
    CostBudgetExceeded,
    ModelPricing,
    estimate_turn_cost,
)
from .dispatch import (
    DispatchConfig,
    DispatchResult,
    DispatchStats,
    DispatchStatus,
    ToolDispatcher,
    dispatch_tool_call,
)
from .errors import (
    Classification,
    FailoverReason,
    RecoveryAction,
    classify_http,
    jittered_backoff,
)
from .guardrails import (
    DestructiveCheck,
    GuardrailVerdict,
    ToolCallGuardrailController,
    ToolGuardrailDecision,
    is_destructive,
)
from .multimodal import (
    cache_image_block,
    is_multimodal_tool_result,
    multimodal_text_summary,
)
from .output_limits import DEFAULT_LIMITS, TruncationResult, get_limit, truncate_output
from .parallel import ToolCall, ToolResult, execute_parallel, partition_calls
from .platform import (
    PLATFORM_PROMPT_FRAGMENTS,
    detect_platform_from_session,
    install_safe_stdio,
    platform_prompt,
)
from .read_cache import (
    CachedRead,
    ReadCache,
    SessionReadCaches,
    TreeCache,
    compute_path_signature,
)
from .request_options import (
    StreamingCallbacks,
    apply_prefill,
    merge_request_overrides,
    normalize_service_tier,
    validate_prefill,
)
from .sanitize import (
    ThinkScrubber,
    redact_dict,
    redact_text,
    repair_tool_call_arguments,
    sanitize_messages,
    sanitize_surrogates,
    scrub_think_blocks,
    strip_non_ascii,
)
from .text_salvage import (
    SyntheticToolCall,
    apply_salvage,
    extract_synthetic_tool_calls,
    salvage_and_clean,
    strip_provider_tags,
)
from .tool_risk import (
    DEFAULT_RISK_TIERS,
    ToolRiskDecision,
    ToolRiskRegistry,
    ToolRiskTier,
    classify_tool_risk,
    requires_confirmation,
)
from .trajectory import TrajectoryRecorder, TurnRecord
from .verify import (
    VerifyResult,
    VerifyStatus,
    verify_patch,
    verify_replace,
    verify_write,
)

__all__ = [
    "IterationBudget",
    "CostBudget", "CostBudgetExceeded", "ModelPricing",
    "DEFAULT_PRICING", "estimate_turn_cost",
    "DispatchConfig", "DispatchResult", "DispatchStats", "DispatchStatus",
    "ToolDispatcher", "dispatch_tool_call",
    "CompressionConfig", "CompressionResult", "ContextCompressor",
    "Classification", "FailoverReason", "RecoveryAction",
    "classify_http", "jittered_backoff",
    "DestructiveCheck", "GuardrailVerdict",
    "ToolCallGuardrailController", "ToolGuardrailDecision", "is_destructive",
    "cache_image_block", "is_multimodal_tool_result", "multimodal_text_summary",
    "DEFAULT_LIMITS", "TruncationResult", "get_limit", "truncate_output",
    "ToolCall", "ToolResult", "execute_parallel", "partition_calls",
    "PLATFORM_PROMPT_FRAGMENTS", "detect_platform_from_session",
    "install_safe_stdio", "platform_prompt",
    "CachedRead", "ReadCache", "SessionReadCaches", "TreeCache",
    "compute_path_signature",
    "StreamingCallbacks", "apply_prefill", "merge_request_overrides",
    "normalize_service_tier", "validate_prefill",
    "ThinkScrubber", "redact_dict", "redact_text", "repair_tool_call_arguments",
    "sanitize_messages", "sanitize_surrogates", "scrub_think_blocks", "strip_non_ascii",
    "SyntheticToolCall", "apply_salvage", "extract_synthetic_tool_calls",
    "salvage_and_clean", "strip_provider_tags",
    "ToolRiskTier", "ToolRiskDecision", "ToolRiskRegistry",
    "DEFAULT_RISK_TIERS", "classify_tool_risk", "requires_confirmation",
    "TrajectoryRecorder", "TurnRecord",
    "VerifyResult", "VerifyStatus", "verify_write", "verify_patch", "verify_replace",
]
