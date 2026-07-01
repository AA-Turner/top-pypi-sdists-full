"""Pydantic types for the hosted-training model catalog.

The catalog itself lives on the API — see ``GET /training/catalog`` and
``dn.api.get_training_catalog(...)`` on the SDK client. This module only
defines the shapes the API response decodes into, so downstream SDK/CLI code
can keep strong types without duplicating the list.

Why no hardcoded ``TINKER_MODELS`` here: mirrors drift. The API is the single
source of truth for which models Tinker actually accepts and what curatorial
metadata (pricing, context, algorithm support) the platform advertises.
``dn train catalog`` fetches it on demand; there is no offline cache here.
"""

import typing as t

from pydantic import BaseModel, ConfigDict, Field

ModelType = t.Literal["dense", "moe"]
ModelFamily = t.Literal["llama", "qwen"]
TrainingAlgorithm = t.Literal["sft", "importance_sampling", "ppo"]


class TrainingModelPricing(BaseModel):
    """Optional upstream pricing metadata.

    All values are USD per million tokens. ``None`` means "not published" —
    callers should fall back to the live Tinker console for authoritative
    numbers (pricing changes faster than we can update the SDK).
    """

    model_config = ConfigDict(extra="forbid")

    prefill: float | None = Field(default=None, ge=0)
    sample: float | None = Field(default=None, ge=0)
    train: float | None = Field(default=None, ge=0)


class TrainingModel(BaseModel):
    """One base model available for hosted training jobs."""

    model_config = ConfigDict(extra="forbid")

    tinker_id: str = Field(
        ...,
        description=(
            "Exact string to pass as `--model` / `base_model` on the training "
            "request. Matches Tinker's canonical model id."
        ),
    )
    display_name: str = Field(..., description="Human-readable name")
    family: ModelFamily = Field(..., description="Model family")
    type: ModelType = Field(..., description="Dense vs mixture-of-experts")
    size_b: float = Field(
        ...,
        ge=0.1,
        description=(
            "Parameter count in billions. For MoE models this is active "
            "parameters, which drives pricing."
        ),
    )
    context_length: int = Field(..., ge=1, description="Max context tokens")
    extended_context: bool = Field(
        default=False,
        description=(
            "Whether a `:peft:` variant with extended context is available "
            "(charged at a higher rate). See Tinker docs for details."
        ),
    )
    supported_algorithms: list[TrainingAlgorithm] = Field(
        ...,
        description=(
            "Training algorithms known to work with this base model. SFT is "
            "always present; `importance_sampling` and `ppo` are RL algorithms."
        ),
    )
    pricing: TrainingModelPricing | None = Field(
        default=None,
        description="Optional pricing metadata; not required for training to work",
    )


__all__ = [
    "ModelFamily",
    "ModelType",
    "TrainingAlgorithm",
    "TrainingModel",
    "TrainingModelPricing",
]
