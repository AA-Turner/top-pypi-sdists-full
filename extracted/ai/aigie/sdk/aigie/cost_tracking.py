"""
Automatic cost tracking for LLM API calls

Supports major providers: OpenAI, Anthropic, Google, Groq, Cohere, Mistral, AWS Bedrock, xAI, Meta, DeepSeek, Qwen, Perplexity
"""

import logging
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class UsageMetadata:
    """Usage metadata extracted from LLM responses"""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    model: str | None = None
    provider: str | None = None


@dataclass
class CostBreakdown:
    """Cost breakdown for an LLM call"""

    input_cost: Decimal
    output_cost: Decimal
    total_cost: Decimal
    currency: str
    model: str
    provider: str
    input_tokens: int
    output_tokens: int
    total_tokens: int


@dataclass
class ModelPricing:
    """Pricing information per model"""

    input_cost_per_1m: Decimal  # Cost per 1M input tokens
    output_cost_per_1m: Decimal  # Cost per 1M output tokens
    provider: str


# Comprehensive pricing table (updated as of February 2026)
# Prices are per 1M tokens (input_cost_per_1m, output_cost_per_1m)
# Sources: OpenAI Official, Anthropic Official, Google Official, DeepSeek Official,
#          xAI Official, OpenRouter (for Meta, Cohere, Amazon, Perplexity, Qwen)
MODEL_PRICING: dict[str, ModelPricing] = {
    # ── OpenAI GPT-5.2 Family ──
    "gpt-5.2": ModelPricing(Decimal("1.75"), Decimal("14"), "openai"),
    "gpt-5.2-pro": ModelPricing(Decimal("21"), Decimal("168"), "openai"),
    "gpt-5.2-codex": ModelPricing(Decimal("1.75"), Decimal("14"), "openai"),
    # ── OpenAI GPT-5.1 Family ──
    "gpt-5.1": ModelPricing(Decimal("1.25"), Decimal("10"), "openai"),
    "gpt-5.1-codex": ModelPricing(Decimal("1.25"), Decimal("10"), "openai"),
    "gpt-5.1-codex-max": ModelPricing(Decimal("1.25"), Decimal("10"), "openai"),
    "gpt-5.1-codex-mini": ModelPricing(Decimal("0.25"), Decimal("2"), "openai"),
    # ── OpenAI GPT-5 Family ──
    "gpt-5": ModelPricing(Decimal("1.25"), Decimal("10"), "openai"),
    "gpt-5-pro": ModelPricing(Decimal("15"), Decimal("120"), "openai"),
    "gpt-5-mini": ModelPricing(Decimal("0.25"), Decimal("2"), "openai"),
    "gpt-5-nano": ModelPricing(Decimal("0.05"), Decimal("0.40"), "openai"),
    "gpt-5-codex": ModelPricing(Decimal("1.25"), Decimal("10"), "openai"),
    # ── OpenAI GPT-4.1 Family ──
    "gpt-4.1": ModelPricing(Decimal("2"), Decimal("8"), "openai"),
    "gpt-4.1-mini": ModelPricing(Decimal("0.40"), Decimal("1.60"), "openai"),
    "gpt-4.1-nano": ModelPricing(Decimal("0.10"), Decimal("0.40"), "openai"),
    # ── OpenAI GPT-4o Family ──
    "gpt-4o": ModelPricing(Decimal("2.50"), Decimal("10"), "openai"),
    "gpt-4o-mini": ModelPricing(Decimal("0.15"), Decimal("0.60"), "openai"),
    "gpt-4o-2024-11-20": ModelPricing(Decimal("2.50"), Decimal("10"), "openai"),
    "gpt-4o-2024-08-06": ModelPricing(Decimal("2.50"), Decimal("10"), "openai"),
    "gpt-4o-2024-05-13": ModelPricing(Decimal("5"), Decimal("15"), "openai"),
    # ── OpenAI GPT-4 Family (Legacy) ──
    "gpt-4": ModelPricing(Decimal("30"), Decimal("60"), "openai"),
    "gpt-4-turbo": ModelPricing(Decimal("10"), Decimal("30"), "openai"),
    "gpt-4-turbo-preview": ModelPricing(Decimal("10"), Decimal("30"), "openai"),
    "gpt-4-0125-preview": ModelPricing(Decimal("10"), Decimal("30"), "openai"),
    "gpt-4-1106-preview": ModelPricing(Decimal("10"), Decimal("30"), "openai"),
    # ── OpenAI GPT-3.5 Family (Legacy) ──
    "gpt-3.5-turbo": ModelPricing(Decimal("0.50"), Decimal("1.50"), "openai"),
    "gpt-3.5-turbo-0125": ModelPricing(Decimal("0.50"), Decimal("1.50"), "openai"),
    "gpt-3.5-turbo-1106": ModelPricing(Decimal("1"), Decimal("2"), "openai"),
    # ── OpenAI O-Series (Reasoning) ──
    "o1": ModelPricing(Decimal("15"), Decimal("60"), "openai"),
    "o1-preview": ModelPricing(Decimal("15"), Decimal("60"), "openai"),
    "o1-mini": ModelPricing(Decimal("1.10"), Decimal("4.40"), "openai"),
    "o1-pro": ModelPricing(Decimal("150"), Decimal("600"), "openai"),
    "o3": ModelPricing(Decimal("2"), Decimal("8"), "openai"),
    "o3-pro": ModelPricing(Decimal("20"), Decimal("80"), "openai"),
    "o3-mini": ModelPricing(Decimal("1.10"), Decimal("4.40"), "openai"),
    "o4-mini": ModelPricing(Decimal("1.10"), Decimal("4.40"), "openai"),
    # ── Anthropic Claude 4.x ──
    "claude-opus-4-6": ModelPricing(Decimal("5"), Decimal("25"), "anthropic"),
    "claude-opus-4.5": ModelPricing(Decimal("5"), Decimal("25"), "anthropic"),
    "claude-sonnet-4-5-20250929": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    "claude-haiku-4-5-20251001": ModelPricing(Decimal("1"), Decimal("5"), "anthropic"),
    "claude-opus-4.1": ModelPricing(Decimal("15"), Decimal("75"), "anthropic"),
    "claude-opus-4": ModelPricing(Decimal("15"), Decimal("75"), "anthropic"),
    "claude-sonnet-4": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    # ── Anthropic Claude 3.7 ──
    "claude-3.7-sonnet": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    # ── Anthropic Claude 3.5 ──
    "claude-3-5-sonnet-20241022": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    "claude-3-5-sonnet-20240620": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    "claude-3-5-haiku-20241022": ModelPricing(Decimal("0.80"), Decimal("4"), "anthropic"),
    # ── Anthropic Claude 3 ──
    "claude-3-opus-20240229": ModelPricing(Decimal("15"), Decimal("75"), "anthropic"),
    "claude-3-sonnet-20240229": ModelPricing(Decimal("3"), Decimal("15"), "anthropic"),
    "claude-3-haiku-20240307": ModelPricing(Decimal("0.25"), Decimal("1.25"), "anthropic"),
    # ── Google Gemini 3 ──
    "gemini-3-pro-preview": ModelPricing(Decimal("2"), Decimal("12"), "google"),
    "gemini-3-flash-preview": ModelPricing(Decimal("0.50"), Decimal("3"), "google"),
    # ── Google Gemini 2.5 ──
    "gemini-2.5-pro": ModelPricing(Decimal("1.25"), Decimal("10"), "google"),
    "gemini-2.5-pro-preview": ModelPricing(Decimal("1.25"), Decimal("10"), "google"),
    "gemini-2.5-flash": ModelPricing(Decimal("0.30"), Decimal("2.50"), "google"),
    "gemini-2.5-flash-preview": ModelPricing(Decimal("0.30"), Decimal("2.50"), "google"),
    "gemini-2.5-flash-lite": ModelPricing(Decimal("0.10"), Decimal("0.40"), "google"),
    # ── Google Gemini 2.0 ──
    "gemini-2.0-flash": ModelPricing(Decimal("0.10"), Decimal("0.40"), "google"),
    "gemini-2.0-flash-exp": ModelPricing(Decimal("0.10"), Decimal("0.40"), "google"),
    # ── Google Gemini 1.5 ──
    "gemini-1.5-pro": ModelPricing(Decimal("1.25"), Decimal("5"), "google"),
    "gemini-1.5-flash": ModelPricing(Decimal("0.075"), Decimal("0.30"), "google"),
    "gemini-1.5-flash-8b": ModelPricing(Decimal("0.0375"), Decimal("0.15"), "google"),
    # ── DeepSeek ──
    "deepseek-chat": ModelPricing(Decimal("0.28"), Decimal("0.42"), "deepseek"),
    "deepseek-reasoner": ModelPricing(Decimal("0.28"), Decimal("0.42"), "deepseek"),
    "deepseek-r1": ModelPricing(Decimal("0.70"), Decimal("2.50"), "deepseek"),
    "deepseek-r1-distill-llama-70b": ModelPricing(Decimal("0.03"), Decimal("0.11"), "deepseek"),
    "deepseek-r1-distill-qwen-32b": ModelPricing(Decimal("0.29"), Decimal("0.29"), "deepseek"),
    # ── xAI Grok ──
    "grok-4": ModelPricing(Decimal("3"), Decimal("15"), "xai"),
    "grok-4-fast": ModelPricing(Decimal("0.20"), Decimal("0.50"), "xai"),
    "grok-4.1-fast": ModelPricing(Decimal("0.20"), Decimal("0.50"), "xai"),
    "grok-3": ModelPricing(Decimal("3"), Decimal("15"), "xai"),
    "grok-3-mini": ModelPricing(Decimal("0.30"), Decimal("0.50"), "xai"),
    # ── Meta Llama ──
    "llama-4-maverick": ModelPricing(Decimal("0.15"), Decimal("0.60"), "meta"),
    "llama-4-scout": ModelPricing(Decimal("0.08"), Decimal("0.30"), "meta"),
    "llama-3.3-70b-instruct": ModelPricing(Decimal("0.10"), Decimal("0.32"), "meta"),
    "llama-3.1-405b-instruct": ModelPricing(Decimal("4"), Decimal("4"), "meta"),
    "llama-3.1-70b-instruct": ModelPricing(Decimal("0.40"), Decimal("0.40"), "meta"),
    "llama-3.1-8b-instruct": ModelPricing(Decimal("0.02"), Decimal("0.05"), "meta"),
    # ── Qwen ──
    "qwen3-max": ModelPricing(Decimal("1.20"), Decimal("6"), "qwen"),
    "qwen3-coder": ModelPricing(Decimal("0.22"), Decimal("1"), "qwen"),
    "qwen3-235b-a22b": ModelPricing(Decimal("0.30"), Decimal("1.20"), "qwen"),
    "qwen3-32b": ModelPricing(Decimal("0.08"), Decimal("0.24"), "qwen"),
    "qwen3-14b": ModelPricing(Decimal("0.05"), Decimal("0.22"), "qwen"),
    "qwen3-8b": ModelPricing(Decimal("0.05"), Decimal("0.40"), "qwen"),
    "qwen3-30b-a3b": ModelPricing(Decimal("0.06"), Decimal("0.22"), "qwen"),
    "qwq-32b": ModelPricing(Decimal("0.15"), Decimal("0.40"), "qwen"),
    # ── Cohere ──
    "command-a": ModelPricing(Decimal("2.50"), Decimal("10"), "cohere"),
    "command-r": ModelPricing(Decimal("0.15"), Decimal("0.60"), "cohere"),
    "command-r-plus": ModelPricing(Decimal("2.50"), Decimal("10"), "cohere"),
    "command-light": ModelPricing(Decimal("0.30"), Decimal("0.60"), "cohere"),
    "command": ModelPricing(Decimal("1"), Decimal("2"), "cohere"),
    # ── Mistral ──
    "mistral-large-2512": ModelPricing(Decimal("0.50"), Decimal("1.50"), "mistral"),
    "mistral-medium-3.1": ModelPricing(Decimal("0.40"), Decimal("2"), "mistral"),
    "mistral-large-latest": ModelPricing(Decimal("2"), Decimal("6"), "mistral"),
    "mistral-large-2411": ModelPricing(Decimal("2"), Decimal("6"), "mistral"),
    "mistral-small-latest": ModelPricing(Decimal("0.10"), Decimal("0.30"), "mistral"),
    "codestral-2508": ModelPricing(Decimal("0.30"), Decimal("0.90"), "mistral"),
    "devstral-2512": ModelPricing(Decimal("0.05"), Decimal("0.22"), "mistral"),
    "open-mistral-7b": ModelPricing(Decimal("0.25"), Decimal("0.25"), "mistral"),
    "open-mixtral-8x7b": ModelPricing(Decimal("0.70"), Decimal("0.70"), "mistral"),
    "mistral-nemo": ModelPricing(Decimal("0.02"), Decimal("0.04"), "mistral"),
    # ── Groq ──
    "groq-llama-3.3-70b": ModelPricing(Decimal("0.59"), Decimal("0.79"), "groq"),
    "groq-llama-3.1-70b": ModelPricing(Decimal("0.59"), Decimal("0.79"), "groq"),
    "groq-llama-3.1-8b": ModelPricing(Decimal("0.05"), Decimal("0.08"), "groq"),
    "groq-llama-4-maverick": ModelPricing(Decimal("0.50"), Decimal("0.77"), "groq"),
    "groq-llama-4-scout": ModelPricing(Decimal("0.11"), Decimal("0.34"), "groq"),
    "groq-mixtral-8x7b": ModelPricing(Decimal("0.24"), Decimal("0.24"), "groq"),
    "groq-gemma2-9b": ModelPricing(Decimal("0.20"), Decimal("0.20"), "groq"),
    "groq-deepseek-r1-distill-llama-70b": ModelPricing(Decimal("0.75"), Decimal("0.99"), "groq"),
    "groq-qwen-qwq-32b": ModelPricing(Decimal("0.29"), Decimal("0.39"), "groq"),
    # Groq custom/fine-tuned models (estimate based on similar size)
    "groq-gpt-oss-120b": ModelPricing(Decimal("0.80"), Decimal("1.20"), "groq"),
    "groq-gpt-oss-20b": ModelPricing(Decimal("0.10"), Decimal("0.20"), "groq"),
    # ── Perplexity ──
    "sonar-pro": ModelPricing(Decimal("3"), Decimal("15"), "perplexity"),
    "sonar": ModelPricing(Decimal("1"), Decimal("1"), "perplexity"),
    # ── Amazon Nova ──
    "nova-premier-v1": ModelPricing(Decimal("2.50"), Decimal("12.50"), "amazon"),
    "nova-pro-v1": ModelPricing(Decimal("0.80"), Decimal("3.20"), "amazon"),
    "nova-lite-v1": ModelPricing(Decimal("0.06"), Decimal("0.24"), "amazon"),
    "nova-micro-v1": ModelPricing(Decimal("0.035"), Decimal("0.14"), "amazon"),
    # ── AWS Bedrock - Anthropic ──
    "anthropic.claude-v2": ModelPricing(Decimal("8"), Decimal("24"), "bedrock"),
    "anthropic.claude-v2:1": ModelPricing(Decimal("8"), Decimal("24"), "bedrock"),
    "anthropic.claude-3-sonnet-20240229-v1:0": ModelPricing(Decimal("3"), Decimal("15"), "bedrock"),
    "anthropic.claude-3-haiku-20240307-v1:0": ModelPricing(
        Decimal("0.25"), Decimal("1.25"), "bedrock"
    ),
    "anthropic.claude-3-opus-20240229-v1:0": ModelPricing(Decimal("15"), Decimal("75"), "bedrock"),
    # ── AWS Bedrock - Titan ──
    "amazon.titan-text-express-v1": ModelPricing(Decimal("0.20"), Decimal("0.60"), "bedrock"),
    "amazon.titan-text-lite-v1": ModelPricing(Decimal("0.15"), Decimal("0.20"), "bedrock"),
    # ── AWS Bedrock - Meta Llama ──
    "meta.llama3-70b-instruct-v1:0": ModelPricing(Decimal("0.99"), Decimal("0.99"), "bedrock"),
    "meta.llama3-8b-instruct-v1:0": ModelPricing(Decimal("0.30"), Decimal("0.60"), "bedrock"),
}


def extract_usage_from_response(response: Any, provider: str | None = None) -> UsageMetadata | None:
    """
    Extract usage metadata from various provider response formats

    Args:
        response: LLM API response
        provider: Optional provider name

    Returns:
        UsageMetadata or None if extraction fails

    Example:
        >>> response = openai.chat.completions.create(...)
        >>> usage = extract_usage_from_response(response, 'openai')
        >>> print(f"Tokens used: {usage.total_tokens}")
    """
    try:
        # Anthropic format (check first - has input_tokens instead of prompt_tokens)
        if hasattr(response, "usage") and hasattr(response.usage, "input_tokens"):
            return UsageMetadata(
                input_tokens=getattr(response.usage, "input_tokens", 0),
                output_tokens=getattr(response.usage, "output_tokens", 0),
                total_tokens=(
                    getattr(response.usage, "input_tokens", 0)
                    + getattr(response.usage, "output_tokens", 0)
                ),
                model=getattr(response, "model", None),
                provider=provider or "anthropic",
            )

        # OpenAI format (prompt_tokens / completion_tokens)
        if hasattr(response, "usage") and response.usage:
            return UsageMetadata(
                input_tokens=getattr(response.usage, "prompt_tokens", 0),
                output_tokens=getattr(response.usage, "completion_tokens", 0),
                total_tokens=getattr(response.usage, "total_tokens", 0),
                model=getattr(response, "model", None),
                provider=provider or "openai",
            )

        # Dictionary format (for API responses as dicts)
        if isinstance(response, dict):
            # OpenAI dict format
            if "usage" in response:
                usage = response["usage"]
                return UsageMetadata(
                    input_tokens=usage.get("prompt_tokens", 0),
                    output_tokens=usage.get("completion_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                    model=response.get("model"),
                    provider=provider or "openai",
                )

            # Google Gemini format
            if "usageMetadata" in response:
                metadata = response["usageMetadata"]
                return UsageMetadata(
                    input_tokens=metadata.get("promptTokenCount", 0),
                    output_tokens=metadata.get("candidatesTokenCount", 0),
                    total_tokens=metadata.get("totalTokenCount", 0),
                    model=response.get("modelVersion"),
                    provider=provider or "google",
                )

            # Cohere format
            if "meta" in response and "billed_units" in response["meta"]:
                units = response["meta"]["billed_units"]
                return UsageMetadata(
                    input_tokens=units.get("input_tokens", 0),
                    output_tokens=units.get("output_tokens", 0),
                    total_tokens=units.get("input_tokens", 0) + units.get("output_tokens", 0),
                    model=response.get("model"),
                    provider=provider or "cohere",
                )

            # AWS Bedrock format
            if "amazon-bedrock-invocationMetrics" in response:
                metrics = response["amazon-bedrock-invocationMetrics"]
                return UsageMetadata(
                    input_tokens=metrics.get("inputTokenCount", 0),
                    output_tokens=metrics.get("outputTokenCount", 0),
                    total_tokens=(
                        metrics.get("inputTokenCount", 0) + metrics.get("outputTokenCount", 0)
                    ),
                    provider=provider or "bedrock",
                )

        return None

    except Exception as e:
        print(f"Warning: Failed to extract usage metadata: {e}")
        return None


def normalize_model_name(model: str) -> str:
    """
    Normalize model name for pricing lookup

    Args:
        model: Raw model name from API

    Returns:
        Normalized model name
    """
    import re

    # Remove common prefixes (e.g., Google's "models/" prefix)
    normalized = model
    if normalized.startswith("models/"):
        normalized = normalized[7:]  # Remove "models/" prefix

    # Remove common suffixes
    normalized = re.sub(r"-\d{8}$", "", normalized)  # Date suffixes
    normalized = re.sub(r"-v\d+:\d+$", "", normalized)  # Bedrock version suffixes
    normalized = normalized.lower()

    # ── Anthropic Claude ──
    if "claude-opus-4-6" in normalized or "claude-opus-4.6" in normalized:
        return "claude-opus-4-6"
    if "claude-opus-4.5" in normalized:
        return "claude-opus-4.5"
    if "claude-opus-4.1" in normalized:
        return "claude-opus-4.1"
    if "claude-opus-4" in normalized:
        return "claude-opus-4"
    if "claude-sonnet-4-5" in normalized or "claude-sonnet-4.5" in normalized:
        return "claude-sonnet-4-5-20250929"
    if "claude-sonnet-4" in normalized:
        return "claude-sonnet-4"
    if "claude-haiku-4-5" in normalized or "claude-haiku-4.5" in normalized:
        return "claude-haiku-4-5-20251001"
    if "claude-3.7-sonnet" in normalized or "claude-3-7-sonnet" in normalized:
        return "claude-3.7-sonnet"
    if "claude-3-5-haiku" in normalized or "claude-3.5-haiku" in normalized:
        return "claude-3-5-haiku-20241022"
    if "claude-3-5-sonnet" in normalized or "claude-3.5-sonnet" in normalized:
        return "claude-3-5-sonnet-20241022"

    # ── OpenAI GPT-5.x (check specific variants before base) ──
    if "gpt-5.2-pro" in normalized:
        return "gpt-5.2-pro"
    if "gpt-5.2-codex" in normalized:
        return "gpt-5.2-codex"
    if "gpt-5.2-chat" in normalized or "gpt-5.2" in normalized:
        return "gpt-5.2"
    if "gpt-5.1-codex-max" in normalized:
        return "gpt-5.1-codex-max"
    if "gpt-5.1-codex-mini" in normalized:
        return "gpt-5.1-codex-mini"
    if "gpt-5.1-codex" in normalized:
        return "gpt-5.1-codex"
    if "gpt-5.1-chat" in normalized or "gpt-5.1" in normalized:
        return "gpt-5.1"
    if "gpt-5-pro" in normalized:
        return "gpt-5-pro"
    if "gpt-5-nano" in normalized:
        return "gpt-5-nano"
    if "gpt-5-mini" in normalized:
        return "gpt-5-mini"
    if "gpt-5-codex" in normalized:
        return "gpt-5-codex"
    if "gpt-5-chat" in normalized or ("gpt-5" in normalized and "gpt-5." not in normalized):
        return "gpt-5"

    # ── OpenAI GPT-4.1 ──
    if "gpt-4.1-mini" in normalized:
        return "gpt-4.1-mini"
    if "gpt-4.1-nano" in normalized:
        return "gpt-4.1-nano"
    if "gpt-4.1" in normalized:
        return "gpt-4.1"

    # ── OpenAI GPT-4o / GPT-4 / GPT-3.5 ──
    if "gpt-4o-mini" in normalized:
        return "gpt-4o-mini"
    if "gpt-4o" in normalized:
        return "gpt-4o"
    if "gpt-4-turbo" in normalized:
        return "gpt-4-turbo"
    if "gpt-4" in normalized:
        return "gpt-4"
    if "gpt-3.5-turbo" in normalized:
        return "gpt-3.5-turbo"

    # ── OpenAI O-Series ──
    if "o3-pro" in normalized:
        return "o3-pro"
    if "o3-mini" in normalized:
        return "o3-mini"
    if "o4-mini" in normalized:
        return "o4-mini"
    if "o1-pro" in normalized:
        return "o1-pro"
    if "o1-mini" in normalized:
        return "o1-mini"

    # ── Google Gemini ──
    if "gemini-3-pro" in normalized:
        return "gemini-3-pro-preview"
    if "gemini-3-flash" in normalized:
        return "gemini-3-flash-preview"
    if "gemini-2.5-flash-lite" in normalized:
        return "gemini-2.5-flash-lite"
    if "gemini-2.5-flash" in normalized:
        return "gemini-2.5-flash"
    if "gemini-2.5-pro" in normalized:
        return "gemini-2.5-pro"
    if "gemini-2.0-flash" in normalized:
        return "gemini-2.0-flash"
    if "gemini-1.5-flash" in normalized:
        return "gemini-1.5-flash"
    if "gemini-1.5-pro" in normalized:
        return "gemini-1.5-pro"

    # ── DeepSeek ──
    if "deepseek-r1-distill-llama" in normalized:
        return "deepseek-r1-distill-llama-70b"
    if "deepseek-r1-distill-qwen" in normalized:
        return "deepseek-r1-distill-qwen-32b"
    if "deepseek-r1" in normalized or "deepseek-reasoner" in normalized:
        return "deepseek-r1"
    if "deepseek-chat" in normalized or "deepseek-v3" in normalized:
        return "deepseek-chat"

    # ── xAI Grok ──
    if "grok-4.1-fast" in normalized:
        return "grok-4.1-fast"
    if "grok-4-fast" in normalized:
        return "grok-4-fast"
    if "grok-4" in normalized:
        return "grok-4"
    if "grok-3-mini" in normalized:
        return "grok-3-mini"
    if "grok-3" in normalized:
        return "grok-3"

    # ── Meta Llama ──
    if "llama-4-maverick" in normalized:
        return "llama-4-maverick"
    if "llama-4-scout" in normalized:
        return "llama-4-scout"
    if "llama-3.3-70b" in normalized:
        return "llama-3.3-70b-instruct"
    if "llama-3.1-405b" in normalized:
        return "llama-3.1-405b-instruct"
    if "llama-3.1-70b" in normalized:
        return "llama-3.1-70b-instruct"
    if "llama-3.1-8b" in normalized:
        return "llama-3.1-8b-instruct"

    # ── Qwen ──
    if "qwen3-max" in normalized:
        return "qwen3-max"
    if "qwen3-coder" in normalized:
        return "qwen3-coder"
    if "qwen3-235b" in normalized:
        return "qwen3-235b-a22b"
    if "qwen3-32b" in normalized:
        return "qwen3-32b"
    if "qwen3-14b" in normalized:
        return "qwen3-14b"
    if "qwen3-8b" in normalized:
        return "qwen3-8b"
    if "qwen3-30b" in normalized:
        return "qwen3-30b-a3b"
    if "qwq-32b" in normalized:
        return "qwq-32b"

    # ── Groq ──
    # Groq models come as "groq:openai/model-name" or "groq:model-name"
    # Strip provider prefixes to get the base model name
    groq_normalized = normalized
    if groq_normalized.startswith("groq:"):
        groq_normalized = groq_normalized[5:]
    if groq_normalized.startswith("openai/"):
        groq_normalized = groq_normalized[7:]
    if normalized.startswith("groq:") or normalized.startswith("groq/"):
        if "gpt-oss-120b" in groq_normalized:
            return "groq-gpt-oss-120b"
        if "gpt-oss-20b" in groq_normalized:
            return "groq-gpt-oss-20b"
        if "llama-4-maverick" in groq_normalized:
            return "groq-llama-4-maverick"
        if "llama-4-scout" in groq_normalized:
            return "groq-llama-4-scout"
        if "llama-3.3-70b" in groq_normalized:
            return "groq-llama-3.3-70b"
        if "llama-3.1-70b" in groq_normalized:
            return "groq-llama-3.1-70b"
        if "llama-3.1-8b" in groq_normalized:
            return "groq-llama-3.1-8b"
        if "mixtral" in groq_normalized:
            return "groq-mixtral-8x7b"
        if "gemma" in groq_normalized:
            return "groq-gemma2-9b"
        if "deepseek-r1" in groq_normalized:
            return "groq-deepseek-r1-distill-llama-70b"
        if "qwq" in groq_normalized:
            return "groq-qwen-qwq-32b"

    # ── Amazon Nova ──
    if "nova-premier" in normalized:
        return "nova-premier-v1"
    if "nova-pro" in normalized:
        return "nova-pro-v1"
    if "nova-lite" in normalized:
        return "nova-lite-v1"
    if "nova-micro" in normalized:
        return "nova-micro-v1"

    return normalized


def calculate_cost(usage: UsageMetadata, model_override: str | None = None) -> CostBreakdown | None:
    """
    Calculate cost from usage metadata

    Args:
        usage: Usage metadata
        model_override: Optional model name override

    Returns:
        CostBreakdown or None if pricing not found

    Example:
        >>> usage = UsageMetadata(input_tokens=100, output_tokens=50, total_tokens=150, model="gpt-4")
        >>> cost = calculate_cost(usage)
        >>> print(f"Total cost: ${cost.total_cost}")
    """
    model = model_override or usage.model
    if not model:
        logger.debug("No model specified for cost calculation")
        return None

    # Normalize model name
    normalized_model = normalize_model_name(model)
    pricing = MODEL_PRICING.get(normalized_model)

    if not pricing:
        logger.debug(f"No pricing information for model: {model}")
        return None

    # Calculate costs (prices are per 1M tokens)
    input_cost = (Decimal(usage.input_tokens) / Decimal("1000000")) * pricing.input_cost_per_1m
    output_cost = (Decimal(usage.output_tokens) / Decimal("1000000")) * pricing.output_cost_per_1m
    total_cost = input_cost + output_cost

    return CostBreakdown(
        input_cost=input_cost,
        output_cost=output_cost,
        total_cost=total_cost,
        currency="USD",
        model=normalized_model,
        provider=pricing.provider,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        total_tokens=usage.total_tokens,
    )


def extract_and_calculate_cost(
    response: Any, provider: str | None = None, model_override: str | None = None
) -> CostBreakdown | None:
    """
    Extract and calculate cost from LLM response

    Args:
        response: LLM API response
        provider: Optional provider name
        model_override: Optional model name override

    Returns:
        CostBreakdown or None

    Example:
        >>> response = openai.chat.completions.create(...)
        >>> cost = extract_and_calculate_cost(response, 'openai')
        >>> print(f"Cost: ${cost.total_cost}")
    """
    usage = extract_usage_from_response(response, provider)
    if not usage:
        return None

    return calculate_cost(usage, model_override)


def add_model_pricing(
    model: str, input_cost_per_1m: float, output_cost_per_1m: float, provider: str
) -> None:
    """
    Add model pricing (for custom models or updates)

    Args:
        model: Model name
        input_cost_per_1m: Input cost per 1M tokens (USD)
        output_cost_per_1m: Output cost per 1M tokens (USD)
        provider: Provider name

    Example:
        >>> add_model_pricing('custom-model-v1', 5.0, 10.0, 'custom')
    """
    MODEL_PRICING[model] = ModelPricing(
        Decimal(str(input_cost_per_1m)), Decimal(str(output_cost_per_1m)), provider
    )


def get_supported_models() -> list[str]:
    """Get all supported models"""
    return list(MODEL_PRICING.keys())


def get_model_pricing(model: str) -> ModelPricing | None:
    """
    Get pricing for a specific model

    Args:
        model: Model name

    Returns:
        ModelPricing or None
    """
    normalized = normalize_model_name(model)
    return MODEL_PRICING.get(normalized)


class CostAggregator:
    """
    Cost aggregator for multiple LLM calls

    Example:
        >>> aggregator = CostAggregator()
        >>> aggregator.add_usage(usage1)
        >>> aggregator.add_usage(usage2)
        >>> summary = aggregator.get_summary()
        >>> print(f"Total cost: ${summary['total_cost']}")
    """

    def __init__(self):
        self.costs: list[CostBreakdown] = []

    def add(self, cost: CostBreakdown) -> None:
        """Add a cost breakdown to the aggregator"""
        self.costs.append(cost)

    def add_usage(self, usage: UsageMetadata, model_override: str | None = None) -> None:
        """Add usage and calculate cost"""
        cost = calculate_cost(usage, model_override)
        if cost:
            self.costs.append(cost)

    def get_total(self) -> Decimal:
        """Get total cost across all calls"""
        return sum((cost.total_cost for cost in self.costs), Decimal("0"))

    def get_total_input_cost(self) -> Decimal:
        """Get total input cost"""
        return sum((cost.input_cost for cost in self.costs), Decimal("0"))

    def get_total_output_cost(self) -> Decimal:
        """Get total output cost"""
        return sum((cost.output_cost for cost in self.costs), Decimal("0"))

    def get_total_tokens(self) -> int:
        """Get total tokens used"""
        return sum(cost.total_tokens for cost in self.costs)

    def get_by_model(self) -> dict[str, dict[str, Any]]:
        """Get breakdown by model"""
        breakdown: dict[str, dict[str, Any]] = {}

        for cost in self.costs:
            if cost.model not in breakdown:
                breakdown[cost.model] = {"cost": Decimal("0"), "calls": 0, "tokens": 0}

            breakdown[cost.model]["cost"] += cost.total_cost
            breakdown[cost.model]["calls"] += 1
            breakdown[cost.model]["tokens"] += cost.total_tokens

        return breakdown

    def get_by_provider(self) -> dict[str, dict[str, Any]]:
        """Get breakdown by provider"""
        breakdown: dict[str, dict[str, Any]] = {}

        for cost in self.costs:
            if cost.provider not in breakdown:
                breakdown[cost.provider] = {"cost": Decimal("0"), "calls": 0, "tokens": 0}

            breakdown[cost.provider]["cost"] += cost.total_cost
            breakdown[cost.provider]["calls"] += 1
            breakdown[cost.provider]["tokens"] += cost.total_tokens

        return breakdown

    def get_costs(self) -> list[CostBreakdown]:
        """Get all cost breakdowns"""
        return self.costs.copy()

    def clear(self) -> None:
        """Clear all costs"""
        self.costs.clear()

    def get_summary(self) -> dict[str, Any]:
        """
        Get summary statistics

        Returns:
            Dictionary with comprehensive cost summary
        """
        total_input_tokens = sum(cost.input_tokens for cost in self.costs)
        total_output_tokens = sum(cost.output_tokens for cost in self.costs)
        total_calls = len(self.costs)

        return {
            "total_cost": float(self.get_total()),
            "total_input_cost": float(self.get_total_input_cost()),
            "total_output_cost": float(self.get_total_output_cost()),
            "total_tokens": self.get_total_tokens(),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_calls": total_calls,
            "average_cost_per_call": (
                float(self.get_total() / total_calls) if total_calls > 0 else 0
            ),
            "by_model": {
                model: {
                    "cost": float(stats["cost"]),
                    "calls": stats["calls"],
                    "tokens": stats["tokens"],
                }
                for model, stats in self.get_by_model().items()
            },
            "by_provider": {
                provider: {
                    "cost": float(stats["cost"]),
                    "calls": stats["calls"],
                    "tokens": stats["tokens"],
                }
                for provider, stats in self.get_by_provider().items()
            },
        }
