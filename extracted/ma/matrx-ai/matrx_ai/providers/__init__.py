"""Provider adapters exposed lazily so importing the package never loads SDKs."""

from __future__ import annotations

import importlib
from typing import Any

_EXPORTS: dict[str, tuple[str, str]] = {
    "AnthropicChat": (".anthropic", "AnthropicChat"),
    "AnthropicTranslator": (".anthropic", "AnthropicTranslator"),
    "BaseTranslator": (".base_translator", "BaseTranslator"),
    "CerebrasChat": (".cerebras", "CerebrasChat"),
    "CerebrasTranslator": (".cerebras", "CerebrasTranslator"),
    "ElevenLabsChat": (".eleven_labs.elevenlabs_api", "ElevenLabsChat"),
    "ExtractedSpan": (".fastino", "ExtractedSpan"),
    "FastinoExtraction": (".fastino", "FastinoExtraction"),
    "GenericOpenAIChat": (".generic_openai", "GenericOpenAIChat"),
    "GenericOpenAITranslator": (".generic_openai", "GenericOpenAITranslator"),
    "GoogleChat": (".google", "GoogleChat"),
    "GoogleImageGeneration": (".google", "GoogleImageGeneration"),
    "GoogleInteractionsVideoGeneration": (".google", "GoogleInteractionsVideoGeneration"),
    "GoogleProviderConfig": (".google", "GoogleProviderConfig"),
    "GoogleTranslator": (".google", "GoogleTranslator"),
    "GoogleVideoGeneration": (".google", "GoogleVideoGeneration"),
    "GroqChat": (".groq", "GroqChat"),
    "GroqTranslator": (".groq", "GroqTranslator"),
    "HuggingFaceChat": (".generic_openai", "HuggingFaceChat"),
    "MockChat": (".mock", "MockChat"),
    "MoonshotChat": (".moonshot", "MoonshotChat"),
    "OpenAIChat": (".openai", "OpenAIChat"),
    "OpenAIImageGeneration": (".openai", "OpenAIImageGeneration"),
    "OpenAITranslator": (".openai", "OpenAITranslator"),
    "OpenAIVideoGeneration": (".openai", "OpenAIVideoGeneration"),
    "ReplicateImageGeneration": (".replicate", "ReplicateImageGeneration"),
    "ReplicateVideoGeneration": (".replicate", "ReplicateVideoGeneration"),
    "RetryableError": (".errors", "RetryableError"),
    "SpanExtractionResult": (".fastino", "SpanExtractionResult"),
    "TogetherChat": (".together", "TogetherChat"),
    "TogetherImageGeneration": (".together", "TogetherImageGeneration"),
    "TogetherTranslator": (".together", "TogetherTranslator"),
    "TogetherVideoGeneration": (".together", "TogetherVideoGeneration"),
    "UnifiedAIClient": (".unified_client", "UnifiedAIClient"),
    "XAIChat": (".xai", "XAIChat"),
    "XAIImageGeneration": (".xai", "XAIImageGeneration"),
    "XAITranslator": (".xai", "XAITranslator"),
    "XAIVideoGeneration": (".xai", "XAIVideoGeneration"),
    "classify_anthropic_error": (".errors", "classify_anthropic_error"),
    "classify_google_error": (".errors", "classify_google_error"),
    "classify_openai_error": (".errors", "classify_openai_error"),
    "classify_provider_error": (".errors", "classify_provider_error"),
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, symbol_name = target
    value = getattr(importlib.import_module(module_name, __name__), symbol_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
