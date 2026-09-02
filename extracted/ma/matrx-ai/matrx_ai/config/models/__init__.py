"""Pydantic models for the engine contract.

THIS IS THE PERMANENT HOME of the contract types. During the migration they run
BESIDE the dataclasses in ``matrx_ai.config`` as shadow models — the dataclass
stays authoritative until a model has run S0→S4 (agent-engine-extraction
CUTOVER.md §3) — after which the dataclass is DELETED and these are the only
definition. They are not a "v2": there will be exactly one.

Why pydantic at all: ``model_json_schema()`` is what
``scripts/generate_types.py`` turns into TypeScript, and the TypeScript twin
(agent-engine-extraction D2) can only be generated against a type that emits a
schema. ``UnifiedConfig`` being a dataclass is precisely why the most important
type in the system has no cross-language definition today.

Every field here is modelled on the CORPUS, not on the old type hints — see
FIELD_TRUTH.md. Where the two disagree, the corpus wins and the disagreement is
recorded in the field's own comment.
"""

from matrx_ai.config.models.content import (
    TextContentModel,
    ThinkingContentModel,
    ToolCallContentModel,
    ToolResultContentModel,
)
from matrx_ai.config.models.extra import (
    CodeExecutionContentModel,
    CodeExecutionResultContentModel,
    ProviderChargeModel,
    WebSearchCallContentModel,
)
from matrx_ai.config.models.media import (
    AudioContentModel,
    DocumentContentModel,
    ImageContentModel,
    VideoContentModel,
    YouTubeVideoContentModel,
)
from matrx_ai.config.models.message import UnifiedMessageModel
from matrx_ai.config.models.unified import UnifiedConfigModel
from matrx_ai.config.models.usage import TokenUsageModel
from matrx_ai.config.models.structured_input import (
    STRUCTURED_INPUT_MODEL_MAP,
    StructuredInputBaseModel,
)
from matrx_ai.config.models.response import UnifiedResponseModel

__all__ = [
    "STRUCTURED_INPUT_MODEL_MAP",
    "AudioContentModel",
    "CodeExecutionContentModel",
    "CodeExecutionResultContentModel",
    "DocumentContentModel",
    "ImageContentModel",
    "ProviderChargeModel",
    "StructuredInputBaseModel",
    "TextContentModel",
    "TokenUsageModel",
    "ThinkingContentModel",
    "ToolCallContentModel",
    "ToolResultContentModel",
    "VideoContentModel",
    "WebSearchCallContentModel",
    "YouTubeVideoContentModel",
    "UnifiedConfigModel",
    "UnifiedMessageModel",
    "UnifiedResponseModel",
]
