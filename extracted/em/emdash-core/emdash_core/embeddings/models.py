"""Embedding models enum - single source of truth for all supported models."""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ModelSpec:
    """Specification for an embedding model."""

    provider: str  # "openai", "fireworks"
    model_id: str  # The actual model identifier for the API
    dimensions: int  # Output embedding dimensions
    max_tokens: int  # Max input tokens
    batch_size: int  # Recommended batch size
    description: str  # Human-readable description


class EmbeddingModel(Enum):
    """
    All supported embedding models.

    Format: PROVIDER_MODEL_NAME

    Usage:
        model = EmbeddingModel.OPENAI_TEXT_3_SMALL
        print(model.spec.dimensions)  # 1536
        print(model.spec.provider)    # "openai"
    """

    # ═══════════════════════════════════════════════════════════════════════════
    # OpenAI Models
    # ═══════════════════════════════════════════════════════════════════════════

    OPENAI_TEXT_3_SMALL = ModelSpec(
        provider="openai",
        model_id="text-embedding-3-small",
        dimensions=1536,
        max_tokens=8191,
        batch_size=100,
        description="OpenAI's small, fast embedding model (best value)",
    )

    OPENAI_TEXT_3_LARGE = ModelSpec(
        provider="openai",
        model_id="text-embedding-3-large",
        dimensions=3072,
        max_tokens=8191,
        batch_size=50,
        description="OpenAI's large, high-quality embedding model",
    )

    OPENAI_ADA_002 = ModelSpec(
        provider="openai",
        model_id="text-embedding-ada-002",
        dimensions=1536,
        max_tokens=8191,
        batch_size=100,
        description="OpenAI's legacy Ada model (deprecated, use text-3-small)",
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Fireworks AI Models
    # ═══════════════════════════════════════════════════════════════════════════

    FIREWORKS_NOMIC_EMBED_V1_5 = ModelSpec(
        provider="fireworks",
        model_id="nomic-ai/nomic-embed-text-v1.5",
        dimensions=768,
        max_tokens=8192,
        batch_size=100,
        description="Nomic's open-source embedding model (fast, good quality)",
    )

    FIREWORKS_E5_MISTRAL_7B = ModelSpec(
        provider="fireworks",
        model_id="intfloat/e5-mistral-7b-instruct",
        dimensions=4096,
        max_tokens=4096,
        batch_size=20,
        description="E5-Mistral 7B (highest quality, slower)",
    )

    FIREWORKS_UAE_LARGE_V1 = ModelSpec(
        provider="fireworks",
        model_id="WhereIsAI/UAE-Large-V1",
        dimensions=1024,
        max_tokens=512,
        batch_size=50,
        description="UAE-Large-V1 (good balance of speed/quality)",
    )

    FIREWORKS_GTE_LARGE = ModelSpec(
        provider="fireworks",
        model_id="thenlper/gte-large",
        dimensions=1024,
        max_tokens=512,
        batch_size=50,
        description="GTE-Large (Alibaba's efficient embedding model)",
    )

    FIREWORKS_BGE_LARGE_EN = ModelSpec(
        provider="fireworks",
        model_id="BAAI/bge-large-en-v1.5",
        dimensions=1024,
        max_tokens=512,
        batch_size=50,
        description="BGE-Large-EN (BAAI's high-quality English model)",
    )

    # ═══════════════════════════════════════════════════════════════════════════

    @property
    def spec(self) -> ModelSpec:
        """Get the model specification."""
        return self.value

    @property
    def provider(self) -> str:
        """Shortcut to get provider name."""
        return self.value.provider

    @property
    def model_id(self) -> str:
        """Shortcut to get the API model ID."""
        return self.value.model_id

    @property
    def dimensions(self) -> int:
        """Shortcut to get embedding dimensions."""
        return self.value.dimensions

    @classmethod
    def get_default(cls) -> "EmbeddingModel":
        """Get the default embedding model."""
        return cls.OPENAI_TEXT_3_SMALL

    @classmethod
    def from_string(cls, value: str) -> Optional["EmbeddingModel"]:
        """
        Parse model from string.

        Accepts:
            - Enum name: "OPENAI_TEXT_3_SMALL"
            - Provider:model: "openai:text-embedding-3-small"
            - Just model_id: "text-embedding-3-small"
        """
        value = value.strip()

        # Try enum name first
        try:
            return cls[value.upper().replace("-", "_").replace(":", "_")]
        except KeyError:
            pass

        # Try provider:model format
        if ":" in value:
            provider, model_id = value.split(":", 1)
            for model in cls:
                if model.provider == provider and model.model_id == model_id:
                    return model

        # Try just model_id
        for model in cls:
            if model.model_id == value:
                return model

        return None

    @classmethod
    def list_by_provider(cls, provider: str) -> list["EmbeddingModel"]:
        """List all models for a specific provider."""
        return [m for m in cls if m.provider == provider]

    @classmethod
    def list_all(cls) -> list[dict]:
        """List all models with their specs for display."""
        return [
            {
                "name": m.name,
                "provider": m.provider,
                "model_id": m.model_id,
                "dimensions": m.dimensions,
                "description": m.spec.description,
            }
            for m in cls
        ]

    def __str__(self) -> str:
        """String representation as provider:model_id."""
        return f"{self.provider}:{self.model_id}"
