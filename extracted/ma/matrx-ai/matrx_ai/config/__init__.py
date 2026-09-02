# ============================================================================
# ai/config — Public API
#
# Import strategy to prevent circular imports:
#
# Tier 1 (pure leaves — no local deps, safe to import anywhere):
#   enums, finish_reason, config_utils
#
# Tier 2 (external SDK deps only — safe unless those SDKs cause issues):
#   usage_config, extra_config, tools_config
#
# Tier 3 (imports from matrx_ai.media, ai.instructions, db.models — heavy):
#   media_config, unified_config
#
# Rule: import only the tier you need. If you only need Role or TokenUsage,
# import directly from the submodule to avoid loading the full unified_.
# ============================================================================

# --- Tier 1: Pure enums / constants / utilities ---
from .citations import (
    NormalizedCitation,
    ensure_normalized_citations,
    log_citations_disabled,
    normalize_anthropic_citation,
    normalize_google_grounding,
    normalize_openai_annotation,
    normalize_xai_citations,
    resolve_citations_disabled_reason,
)
from .config_utils import truncate_base64_in_dict
from .custom_tool import CustomTool, CustomToolInputSchema
from .enums import ContentType, Provider, Role
from .extra_config import (
    CodeExecutionContent,
    CodeExecutionResultContent,
    WebSearchCallContent,
)
from .finish_reason import FinishReason
from .json_schema_wire import JsonSchemaObjectDocument, JsonSchemaProperty
from .llm_params import LLMParams
from .llm_wire_types import (
    AspectRatio,
    AudioFormat,
    CompactionSettings,
    ImageLora,
    ImageStyle,
    MediaOutputFormat,
    MediaResolution,
    TtsDialogueTurn,
    TtsQuality,
    TtsVoiceSpeaker,
    Verbosity,
)

# --- Tier 3: Media + unified config (heavy — loads db.models, ai.instructions, etc.) ---
# These are intentionally last. Anything that only needs Tier 1/2 types
# should import from the submodule directly to avoid this overhead.
from .media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    MediaContent,
    MediaKind,
    VideoContent,
    YouTubeVideoContent,
    reconstruct_media_content,
)
from .message_config import MessageList, UnifiedMessage
from .response_format import (
    OutputSchemaEnvelope,
    ResponseFormat,
    ResponseFormatJsonObject,
    ResponseFormatJsonSchema,
    ResponseFormatText,
    response_format_for_model,
)
from .structured_input_config import (
    STRUCTURED_INPUT_TYPE_MAP,
    AgentAppInputContent,
    AgentInputContent,
    ContextInputContent,
    DataInputContent,
    DocumentInputContent,
    ListInputContent,
    NotesInputContent,
    ProjectInputContent,
    StructuredInputContent,
    TableInputContent,
    TaskInputContent,
    TranscriptInputContent,
    TranscriptSessionInputContent,
    WebpageInputContent,
    WorkbookInputContent,
    reconstruct_structured_input,
)
from .tools_config import ToolCallContent, ToolResultContent
from .tts_config import (
    GroqTTSRegistry,
    TTSSpeaker,
    TTSVoiceConfig,
    XAITTSRegistry,
    configure_multi_speaker_voice_pool,
)
from .unified_config import UnifiedConfig, UnifiedResponse
from .unified_content import (
    SearchResultContent,
    TextContent,
    ThinkingContent,
    UnifiedContent,
    reconstruct_content,
)

# --- Tier 2: Config dataclasses (external SDK deps only) ---
from .usage_config import (
    AggregatedUsage,
    ModelPricing,
    ModelUsageSummary,
    PricingTier,
    ProviderCharge,
    TokenUsage,
    UsageCostBreakdown,
    UsageTotals,
    openai_compatible_usage_counts,
    serialize_provider_usage,
)
from .validators import ModelReference

__all__ = [
    # Tier 1
    "NormalizedCitation",
    "ensure_normalized_citations",
    "log_citations_disabled",
    "normalize_anthropic_citation",
    "normalize_google_grounding",
    "normalize_openai_annotation",
    "normalize_xai_citations",
    "resolve_citations_disabled_reason",
    "ContentType",
    "Provider",
    "Role",
    "FinishReason",
    "LLMParams",
    "CustomTool",
    "CustomToolInputSchema",
    "JsonSchemaObjectDocument",
    "JsonSchemaProperty",
    "ModelReference",
    "AspectRatio",
    "AudioFormat",
    "CompactionSettings",
    "ImageLora",
    "ImageStyle",
    "MediaOutputFormat",
    "MediaResolution",
    "OutputSchemaEnvelope",
    "ResponseFormat",
    "ResponseFormatText",
    "ResponseFormatJsonObject",
    "ResponseFormatJsonSchema",
    "response_format_for_model",
    "TtsDialogueTurn",
    "TtsQuality",
    "TtsVoiceSpeaker",
    "Verbosity",
    "truncate_base64_in_dict",
    # Tier 2
    "AggregatedUsage",
    "ModelPricing",
    "ModelUsageSummary",
    "PricingTier",
    "ProviderCharge",
    "TokenUsage",
    "UsageCostBreakdown",
    "UsageTotals",
    "openai_compatible_usage_counts",
    "serialize_provider_usage",
    "TTSSpeaker",
    "configure_multi_speaker_voice_pool",
    "TTSVoiceConfig",
    "GroqTTSRegistry",
    "XAITTSRegistry",
    "CodeExecutionContent",
    "CodeExecutionResultContent",
    "WebSearchCallContent",
    "ToolCallContent",
    "ToolResultContent",
    # Tier 3
    "AudioContent",
    "DocumentContent",
    "ImageContent",
    "MediaContent",
    "MediaKind",
    "VideoContent",
    "YouTubeVideoContent",
    "reconstruct_media_content",
    "MessageList",
    "SearchResultContent",
    "TextContent",
    "ThinkingContent",
    "UnifiedConfig",
    "UnifiedContent",
    "UnifiedMessage",
    "UnifiedResponse",
    "reconstruct_content",
    # Structured input types
    "WebpageInputContent",
    "NotesInputContent",
    "TaskInputContent",
    "TableInputContent",
    "ListInputContent",
    "DataInputContent",
    "ContextInputContent",
    "AgentInputContent",
    "ProjectInputContent",
    "AgentAppInputContent",
    "TranscriptInputContent",
    "TranscriptSessionInputContent",
    "WorkbookInputContent",
    "DocumentInputContent",
    "StructuredInputContent",
    "STRUCTURED_INPUT_TYPE_MAP",
    "reconstruct_structured_input",
]
