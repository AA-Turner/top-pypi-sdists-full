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
    "CohereLegacyClient": (".cohere", "CohereLegacyClient"),
    "CohereReranker": (".cohere", "CohereReranker"),
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
    "GroqSTT": (".groq", "GroqSTT"),
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


def _load_provider_module(module_name: str):
    """Load one declared adapter module without concealing its import edge."""
    match module_name:
        case ".anthropic":
            return importlib.import_module(".anthropic", __name__)
        case ".base_translator":
            return importlib.import_module(".base_translator", __name__)
        case ".cerebras":
            return importlib.import_module(".cerebras", __name__)
        case ".cohere":
            return importlib.import_module(".cohere", __name__)
        case ".eleven_labs.elevenlabs_api":
            return importlib.import_module(".eleven_labs.elevenlabs_api", __name__)
        case ".errors":
            return importlib.import_module(".errors", __name__)
        case ".fastino":
            return importlib.import_module(".fastino", __name__)
        case ".generic_openai":
            return importlib.import_module(".generic_openai", __name__)
        case ".google":
            return importlib.import_module(".google", __name__)
        case ".groq":
            return importlib.import_module(".groq", __name__)
        case ".mock":
            return importlib.import_module(".mock", __name__)
        case ".moonshot":
            return importlib.import_module(".moonshot", __name__)
        case ".openai":
            return importlib.import_module(".openai", __name__)
        case ".replicate":
            return importlib.import_module(".replicate", __name__)
        case ".together":
            return importlib.import_module(".together", __name__)
        case ".unified_client":
            return importlib.import_module(".unified_client", __name__)
        case ".xai":
            return importlib.import_module(".xai", __name__)
        case _:
            raise AssertionError(f"undeclared provider module: {module_name}")

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    target = _EXPORTS.get(name)
    if target is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, symbol_name = target
    value = getattr(_load_provider_module(module_name), symbol_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
