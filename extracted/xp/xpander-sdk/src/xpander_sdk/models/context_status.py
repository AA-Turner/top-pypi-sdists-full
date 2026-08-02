from pydantic import Field

from xpander_sdk.models.shared import XPanderSharedModel


class ContextStatus(XPanderSharedModel):
    """Per-turn snapshot of the LLM context window for the chat UI indicator."""

    estimated_tokens: int = Field(
        ...,
        description="Rough token count of the current message list (post-Layer-1 microcompaction).",
    )
    context_window: int = Field(..., description="Model context window size in tokens.")
    percent: float = Field(
        ...,
        description="estimated_tokens / context_window * 100, clamped to [0, 100].",
    )
    auto_compact_threshold: int = Field(
        ...,
        description="Token level at which Layer 2 auto-compaction fires.",
    )
    emergency_threshold: int = Field(
        ...,
        description="Token level at which the emergency safety net (88%) fires.",
    )
    compacting: bool = Field(
        default=False,
        description="True while a Layer 2 compaction is in flight on the current turn.",
    )
