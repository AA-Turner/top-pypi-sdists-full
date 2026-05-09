"""Generic OpenAI-compatible provider — works with Groq, OpenRouter, Cerebras,
SambaNova, Together, Mistral, Cohere, GitHub Models, DeepSeek, and any other
service that implements the /v1/chat/completions endpoint.

Each service is configured as a ProviderSpec with its base URL, API key config
key, and list of free models.
"""

from __future__ import annotations

import json
import time
from collections.abc import Iterator
from dataclasses import dataclass

import httpx

from ..config import SageConfig
from .base import Message, ModelInfo, ProviderBase
from .retry import CircuitBreaker, RetryConfig, get_rate_limiter, get_retry_after


@dataclass(frozen=True)
class ProviderSpec:
    """Configuration for an OpenAI-compatible provider."""

    name: str
    base_url: str
    api_key_config: str  # Key in config.api_keys, e.g. "groq"
    env_var: str  # Environment variable override
    models: list[ModelInfo]
    default_model: str
    supports_streaming: bool = True
    requires_key: bool = True  # False for free providers like Pollinations


# ── Free model registries ──────────────────────────────────

GROQ_MODELS = [
    ModelInfo(
        id="llama-3.3-70b-versatile",
        provider="groq",
        name="Llama 3.3 70B",
        local=False,
        description="Best all-around Llama model for coding",
        pros="Very fast, free tier, great code quality",
        cons="Requires free API key",
    ),
    ModelInfo(
        id="llama-3.1-8b-instant",
        provider="groq",
        name="Llama 3.1 8B Instant",
        local=False,
        description="Ultra-fast small model for simple tasks",
        pros="Fastest responses, good for quick questions",
        cons="Less capable than 70B for complex code",
    ),
    ModelInfo(
        id="llama3-70b-8192",
        provider="groq",
        name="Llama 3 70B",
        local=False,
        description="Older Llama model, still capable",
        pros="Free tier, good code generation",
        cons="Older, use 3.3 70B instead",
    ),
    ModelInfo(
        id="llama3-8b-8192",
        provider="groq",
        name="Llama 3 8B",
        local=False,
        description="Small fast model for simple tasks",
        pros="Very fast, free tier",
        cons="Limited for complex coding",
    ),
    ModelInfo(
        id="gemma2-9b-it",
        provider="groq",
        name="Gemma 2 9B",
        local=False,
        description="Google's efficient small model",
        pros="Fast, good instruction following",
        cons="Limited context, less code-focused",
    ),
    ModelInfo(
        id="mixtral-8x7b-32768",
        provider="groq",
        name="Mixtral 8x7B",
        local=False,
        description="MoE model with 32K context",
        pros="Large context window, efficient",
        cons="Older architecture",
    ),
    ModelInfo(
        id="deepseek-r1-distill-llama-70b",
        provider="groq",
        name="DeepSeek R1 Distill 70B",
        local=False,
        description="Reasoning model for complex problems",
        pros="Great for debugging, step-by-step thinking",
        cons="Slower than regular models",
    ),
]

OPENROUTER_MODELS = [
    ModelInfo(
        id="meta-llama/llama-3.3-70b-instruct:free",
        provider="openrouter",
        name="Llama 3.3 70B (Free)",
        local=False,
        description="Best free Llama model via OpenRouter",
        pros="Free, high quality code generation",
        cons="Rate limited, needs free OpenRouter key",
    ),
    ModelInfo(
        id="deepseek/deepseek-r1:free",
        provider="openrouter",
        name="DeepSeek R1 (Free)",
        local=False,
        description="Top-tier reasoning model, free tier",
        pros="Excellent debugging, step-by-step thinking",
        cons="Slower, verbose output, rate limited",
    ),
    ModelInfo(
        id="deepseek/deepseek-chat-v3-0324:free",
        provider="openrouter",
        name="DeepSeek V3 (Free)",
        local=False,
        description="DeepSeek's fastest chat model",
        pros="Fast, good code, free tier",
        cons="Rate limited",
    ),
    ModelInfo(
        id="qwen/qwen3-235b-a22b:free",
        provider="openrouter",
        name="Qwen 3 235B (Free)",
        local=False,
        description="Huge model with MoE architecture",
        pros="Massive capacity, great reasoning",
        cons="May be slow, rate limited",
    ),
    ModelInfo(
        id="google/gemma-3-27b-it:free",
        provider="openrouter",
        name="Gemma 3 27B (Free)",
        local=False,
        description="Google's latest Gemma model",
        pros="Good balance of speed/quality",
        cons="Rate limited",
    ),
    ModelInfo(
        id="mistralai/mistral-small-3.1-24b-instruct:free",
        provider="openrouter",
        name="Mistral Small 3.1 (Free)",
        local=False,
        description="Efficient Mistral model",
        pros="Fast, good code generation",
        cons="Rate limited, smaller context",
    ),
    ModelInfo(
        id="microsoft/phi-4-reasoning-plus:free",
        provider="openrouter",
        name="Phi 4 Reasoning+ (Free)",
        local=False,
        description="Microsoft's reasoning model",
        pros="Good for math/logic, efficient",
        cons="Smaller model, may miss nuance",
    ),
]

CEREBRAS_MODELS = [
    ModelInfo(
        id="llama-3.3-70b", provider="cerebras", name="Llama 3.3 70B (Cerebras)", local=False
    ),
    ModelInfo(id="llama3.1-8b", provider="cerebras", name="Llama 3.1 8B (Cerebras)", local=False),
]

SAMBANOVA_MODELS = [
    ModelInfo(id="DeepSeek-R1", provider="sambanova", name="DeepSeek R1 (SambaNova)", local=False),
    ModelInfo(
        id="Meta-Llama-3.3-70B-Instruct",
        provider="sambanova",
        name="Llama 3.3 70B (SambaNova)",
        local=False,
    ),
    ModelInfo(
        id="DeepSeek-V3-0324", provider="sambanova", name="DeepSeek V3 (SambaNova)", local=False
    ),
    ModelInfo(id="QwQ-32B", provider="sambanova", name="QwQ 32B (SambaNova)", local=False),
    ModelInfo(id="Qwen3-32B", provider="sambanova", name="Qwen 3 32B (SambaNova)", local=False),
]

TOGETHER_MODELS = [
    ModelInfo(
        id="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        provider="together",
        name="Llama 3.3 70B Turbo (Free)",
        local=False,
    ),
    ModelInfo(
        id="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        provider="together",
        name="DeepSeek R1 Distill 70B (Free)",
        local=False,
    ),
]

MISTRAL_MODELS = [
    ModelInfo(id="mistral-small-latest", provider="mistral", name="Mistral Small", local=False),
    ModelInfo(id="open-mistral-nemo", provider="mistral", name="Mistral Nemo 12B", local=False),
    ModelInfo(id="codestral-latest", provider="mistral", name="Codestral", local=False),
]

COHERE_MODELS = [
    ModelInfo(id="command-r-plus", provider="cohere", name="Command R+ (Cohere)", local=False),
    ModelInfo(id="command-r", provider="cohere", name="Command R (Cohere)", local=False),
    ModelInfo(id="command-a-03-2025", provider="cohere", name="Command A (Cohere)", local=False),
]

GITHUB_MODELS = [
    ModelInfo(id="gpt-4o-mini", provider="github", name="GPT-4o Mini (GitHub)", local=False),
    ModelInfo(
        id="Phi-3.5-mini-instruct", provider="github", name="Phi 3.5 Mini (GitHub)", local=False
    ),
    ModelInfo(
        id="AI21-Jamba-1.5-Mini", provider="github", name="Jamba 1.5 Mini (GitHub)", local=False
    ),
    ModelInfo(id="Mistral-Nemo", provider="github", name="Mistral Nemo (GitHub)", local=False),
]

DEEPSEEK_MODELS = [
    ModelInfo(
        id="deepseek-chat",
        provider="deepseek",
        name="DeepSeek V3",
        local=False,
        description="Best value code model, very cheap API",
        pros="Excellent code, GPT-4 class, $0.14/M tokens",
        cons="Requires API key, China-based",
    ),
    ModelInfo(
        id="deepseek-reasoner",
        provider="deepseek",
        name="DeepSeek R1",
        local=False,
        description="Top reasoning model, beats o1-preview",
        pros="Best-in-class debugging, chain-of-thought",
        cons="Slower, verbose output, requires API key",
    ),
]

OLLAMA_MODELS: list[ModelInfo] = [
    # Ollama models are dynamic — discovered at runtime
]

DEEPINFRA_MODELS = [
    ModelInfo(
        id="deepseek-ai/DeepSeek-R1-0528",
        provider="deepinfra",
        name="DeepSeek R1 0528 (DeepInfra)",
        local=False,
    ),
    ModelInfo(
        id="deepseek-ai/DeepSeek-V3-0324",
        provider="deepinfra",
        name="DeepSeek V3 0324 (DeepInfra)",
        local=False,
    ),
    ModelInfo(
        id="meta-llama/Llama-4-Scout-17B-16E-Instruct",
        provider="deepinfra",
        name="Llama 4 Scout 17B (DeepInfra)",
        local=False,
    ),
    ModelInfo(
        id="Qwen/Qwen3-Coder", provider="deepinfra", name="Qwen3 Coder (DeepInfra)", local=False
    ),
    ModelInfo(
        id="THUDM/GLM-4.5-0414", provider="deepinfra", name="GLM 4.5 (DeepInfra)", local=False
    ),
]


# ── Provider specs ─────────────────────────────────────────

PROVIDER_SPECS: list[ProviderSpec] = [
    ProviderSpec(
        name="groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_config="groq",
        env_var="SAGE_GROQ_API_KEY",
        models=GROQ_MODELS,
        default_model="llama-3.3-70b-versatile",
    ),
    ProviderSpec(
        name="openrouter",
        base_url="https://openrouter.ai/api/v1",
        api_key_config="openrouter",
        env_var="SAGE_OPENROUTER_API_KEY",
        models=OPENROUTER_MODELS,
        default_model="meta-llama/llama-3.3-70b-instruct:free",
    ),
    ProviderSpec(
        name="cerebras",
        base_url="https://api.cerebras.ai/v1",
        api_key_config="cerebras",
        env_var="SAGE_CEREBRAS_API_KEY",
        models=CEREBRAS_MODELS,
        default_model="llama-3.3-70b",
    ),
    ProviderSpec(
        name="sambanova",
        base_url="https://api.sambanova.ai/v1",
        api_key_config="sambanova",
        env_var="SAGE_SAMBANOVA_API_KEY",
        models=SAMBANOVA_MODELS,
        default_model="DeepSeek-R1",
    ),
    ProviderSpec(
        name="together",
        base_url="https://api.together.xyz/v1",
        api_key_config="together",
        env_var="SAGE_TOGETHER_API_KEY",
        models=TOGETHER_MODELS,
        default_model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
    ),
    ProviderSpec(
        name="mistral",
        base_url="https://api.mistral.ai/v1",
        api_key_config="mistral",
        env_var="SAGE_MISTRAL_API_KEY",
        models=MISTRAL_MODELS,
        default_model="mistral-small-latest",
    ),
    ProviderSpec(
        name="cohere",
        base_url="https://api.cohere.com/compatibility/v1",
        api_key_config="cohere",
        env_var="SAGE_COHERE_API_KEY",
        models=COHERE_MODELS,
        default_model="command-r-plus",
    ),
    ProviderSpec(
        name="github",
        base_url="https://models.inference.ai.azure.com",
        api_key_config="github",
        env_var="GITHUB_TOKEN",
        models=GITHUB_MODELS,
        default_model="gpt-4o-mini",
    ),
    ProviderSpec(
        name="deepseek",
        base_url="https://api.deepseek.com/v1",
        api_key_config="deepseek",
        env_var="SAGE_DEEPSEEK_API_KEY",
        models=DEEPSEEK_MODELS,
        default_model="deepseek-chat",
    ),
    # ── Providers that need a free API key ─────────────────
    ProviderSpec(
        name="deepinfra",
        base_url="https://api.deepinfra.com/v1/openai",
        api_key_config="deepinfra",
        env_var="SAGE_DEEPINFRA_API_KEY",
        models=DEEPINFRA_MODELS,
        default_model="deepseek-ai/DeepSeek-V3-0324",
    ),
]


# ── Provider implementation ────────────────────────────────


class OpenAICompatProvider(ProviderBase):
    """Provider for any service with an OpenAI-compatible chat completions API."""

    def __init__(self, spec: ProviderSpec, config: SageConfig) -> None:
        self._spec = spec
        self.name = spec.name
        # Get API key from config or environment
        import os

        if spec.requires_key:
            self._api_key = (
                config.api_keys.get(spec.api_key_config) or os.environ.get(spec.env_var) or None
            )
        else:
            # Free provider — no key needed, but accept one if provided
            self._api_key = (
                config.api_keys.get(spec.api_key_config) or os.environ.get(spec.env_var)
                if spec.env_var
                else None
            )
        self._base_url = spec.base_url.strip().strip("`").rstrip("/")
        self._retry_config = self._build_retry_config()
        limiter_key = f"{self._spec.name}:{'keyed' if self._api_key else 'anonymous'}"
        self._rate_limiter = get_rate_limiter(
            limiter_key,
            requests_per_minute=self._requests_per_minute(),
        )
        self._circuit_breaker = CircuitBreaker(failure_threshold=6, recovery_timeout=30.0)

    def _requests_per_minute(self) -> int:
        """Return a conservative per-process request budget for this provider."""
        return 90

    def _build_retry_config(self) -> RetryConfig:
        """Build provider-specific retry behavior."""
        return RetryConfig(
            max_attempts=3,
            base_delay=0.5,
            max_delay=8.0,
            exponential_base=2.0,
            jitter=0.1,
        )

    def _before_request(self) -> None:
        """Apply local rate limiting and circuit breaking before an upstream call."""
        if self._circuit_breaker.is_open():
            raise RuntimeError(
                f"{self._spec.name} is temporarily unavailable after repeated transient failures. "
                "Please wait a moment and try again."
            )
        if not self._rate_limiter.acquire(timeout=10.0):
            raise RuntimeError(
                f"{self._spec.name} is currently saturated. Please retry in a few seconds."
            )

    def _retry_delay(self, attempt: int, exc: Exception) -> float:
        """Calculate the next retry delay for a transient failure."""
        return self._retry_config.calculate_delay(attempt, get_retry_after(exc))

    def _completion_url_candidates(self) -> list[str]:
        """Return completion endpoint candidates."""
        primary = f"{self._base_url}/chat/completions"
        return [primary]

    def is_available(self) -> bool:
        if not self._spec.requires_key:
            return True
        return bool(self._api_key)

    def list_models(self) -> list[ModelInfo]:
        if not self.is_available():
            return []
        return list(self._spec.models)

    def _headers(self) -> dict[str, str]:
        return self._headers_for_url(self._base_url)

    def _headers_for_url(self, url: str) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        if self._spec.name == "openrouter":
            headers["HTTP-Referer"] = "https://sageworksai.com"
            headers["X-Title"] = "Sage AI CLI"
        return headers

    def _build_payload(
        self,
        messages: list[Message],
        model: str,
        temperature: float,
        max_tokens: int,
        stream: bool = False,
    ) -> dict:
        chat_messages = []
        for msg in messages:
            chat_messages.append({"role": msg.role, "content": msg.content})
        return {
            "model": model,
            "messages": chat_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

    @staticmethod
    def _coerce_text_content(value: object) -> str:
        """Extract plain text from string or structured content blocks."""
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            parts: list[str] = []
            for item in value:
                if isinstance(item, str):
                    if item:
                        parts.append(item)
                    continue
                if not isinstance(item, dict):
                    continue
                text_value = item.get("text")
                if isinstance(text_value, str) and text_value:
                    parts.append(text_value)
                    continue
                if isinstance(text_value, dict):
                    nested = text_value.get("value")
                    if isinstance(nested, str) and nested:
                        parts.append(nested)
                        continue
                if item.get("type") == "output_text":
                    output_text = item.get("text")
                    if isinstance(output_text, str) and output_text:
                        parts.append(output_text)
            return "".join(parts)
        return ""

    def _extract_response_text(self, data: dict) -> str:
        """Extract assistant text from a non-streaming OpenAI-compatible payload."""
        choices = data.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0] if isinstance(choices[0], dict) else {}
            if isinstance(first_choice, dict):
                message = first_choice.get("message")
                if isinstance(message, dict):
                    content = self._coerce_text_content(message.get("content"))
                    if content:
                        return content
                    refusal = message.get("refusal")
                    if isinstance(refusal, str) and refusal:
                        return refusal
                text = first_choice.get("text")
                if isinstance(text, str) and text:
                    return text

        output_text = data.get("output_text")
        if isinstance(output_text, str) and output_text:
            return output_text

        message = data.get("message")
        if isinstance(message, dict):
            content = self._coerce_text_content(message.get("content"))
            if content:
                return content

        content = self._coerce_text_content(data.get("content"))
        if content:
            return content

        raise RuntimeError(
            f"{self._spec.name} returned a response without text content."
        )

    def _extract_stream_text(self, chunk: dict) -> str:
        """Extract assistant text from a streaming chunk."""
        choices = chunk.get("choices")
        if isinstance(choices, list) and choices:
            first_choice = choices[0] if isinstance(choices[0], dict) else {}
            if isinstance(first_choice, dict):
                delta = first_choice.get("delta")
                if isinstance(delta, dict):
                    content = self._coerce_text_content(delta.get("content"))
                    if content:
                        return content
                    text = delta.get("text")
                    if isinstance(text, str) and text:
                        return text
                message = first_choice.get("message")
                if isinstance(message, dict):
                    content = self._coerce_text_content(message.get("content"))
                    if content:
                        return content
                text = first_choice.get("text")
                if isinstance(text, str) and text:
                    return text
        return ""

    def generate(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if self._spec.requires_key and not self._api_key:
            raise RuntimeError(
                f"{self._spec.name} API key not configured. "
                f"Run: sage config set api_keys.{self._spec.api_key_config} YOUR_KEY"
            )
        model = model or self._spec.default_model
        payload = self._build_payload(messages, model, temperature, max_tokens)
        last_exc: Exception | None = None
        with httpx.Client(timeout=120, follow_redirects=True) as client:
            for url in self._completion_url_candidates():
                for attempt in range(self._retry_config.max_attempts):
                    try:
                        self._before_request()
                        resp = client.post(url, json=payload, headers=self._headers_for_url(url))
                        resp.raise_for_status()
                        data = resp.json()
                        self._circuit_breaker.record_success()
                        return self._extract_response_text(data)
                    except httpx.HTTPStatusError as exc:
                        last_exc = exc
                        self._circuit_breaker.record_failure()
                        status = exc.response.status_code
                        if status == 404:
                            break  # Try next URL
                        if status in {429, 500, 502, 503, 504}:
                            if attempt < self._retry_config.max_attempts - 1:
                                time.sleep(self._retry_delay(attempt, exc))
                                continue
                            break
                        raise
                    except RuntimeError as exc:
                        last_exc = exc
                        break
                    except (
                        httpx.ReadTimeout,
                        httpx.ConnectError,
                        httpx.ConnectTimeout,
                        httpx.RemoteProtocolError,
                    ) as exc:
                        last_exc = exc
                        self._circuit_breaker.record_failure()
                        if attempt < self._retry_config.max_attempts - 1:
                            time.sleep(self._retry_delay(attempt, exc))
                            continue
                        break
        if last_exc:
            raise last_exc
        raise RuntimeError("No completion endpoint candidates available")

    def stream(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        if self._spec.requires_key and not self._api_key:
            raise RuntimeError(
                f"{self._spec.name} API key not configured. "
                f"Run: sage config set api_keys.{self._spec.api_key_config} YOUR_KEY"
            )
        model = model or self._spec.default_model
        payload = self._build_payload(messages, model, temperature, max_tokens, stream=True)
        last_exc: Exception | None = None
        with httpx.Client(timeout=120, follow_redirects=True) as client:
            for url in self._completion_url_candidates():
                for attempt in range(self._retry_config.max_attempts):
                    try:
                        self._before_request()
                        with client.stream(
                            "POST", url, json=payload, headers=self._headers_for_url(url)
                        ) as resp:
                            resp.raise_for_status()
                            for line in resp.iter_lines():
                                if not line.startswith("data: "):
                                    continue
                                data_str = line[6:]
                                if data_str.strip() == "[DONE]":
                                    break
                                try:
                                    chunk = json.loads(data_str)
                                except json.JSONDecodeError:
                                    continue
                                content = self._extract_stream_text(chunk)
                                if content:
                                    yield content
                            self._circuit_breaker.record_success()
                            return
                    except httpx.HTTPStatusError as exc:
                        last_exc = exc
                        self._circuit_breaker.record_failure()
                        status = exc.response.status_code
                        if status == 404:
                            break  # Try next URL
                        if status in {429, 500, 502, 503, 504}:
                            if attempt < self._retry_config.max_attempts - 1:
                                time.sleep(self._retry_delay(attempt, exc))
                                continue
                            break
                        raise
                    except RuntimeError as exc:
                        last_exc = exc
                        break
                    except (
                        httpx.ReadTimeout,
                        httpx.ConnectError,
                        httpx.ConnectTimeout,
                        httpx.RemoteProtocolError,
                    ) as exc:
                        last_exc = exc
                        self._circuit_breaker.record_failure()
                        if attempt < self._retry_config.max_attempts - 1:
                            time.sleep(self._retry_delay(attempt, exc))
                            continue
                        break
        if last_exc:
            raise last_exc
        raise RuntimeError("No completion endpoint candidates available")


# ── Ollama (local, no API key needed) ──────────────────────


class OllamaProvider(ProviderBase):
    """Provider for Ollama — local models via REST API, no API key required.

    Lists both locally-pulled models AND all Ollama catalog models so users
    can see and select any model. Unpulled models are auto-pulled on first use.
    """

    name = "ollama"

    def __init__(self, config: SageConfig, base_url: str = "http://localhost:11434") -> None:
        import os

        self._base_url = os.environ.get("OLLAMA_HOST", base_url)
        self._pulled_names: set[str] | None = None  # lazy cache

    def is_available(self) -> bool:
        try:
            with httpx.Client(timeout=3) as client:
                resp = client.get(f"{self._base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    def _get_pulled_names(self) -> set[str]:
        """Return set of model names currently pulled in Ollama."""
        if self._pulled_names is not None:
            return self._pulled_names
        try:
            with httpx.Client(timeout=5) as client:
                resp = client.get(f"{self._base_url}/api/tags")
                resp.raise_for_status()
                data = resp.json()
                self._pulled_names = {m["name"] for m in data.get("models", [])}
        except Exception:
            self._pulled_names = set()
        return self._pulled_names

    def list_models(self) -> list[ModelInfo]:
        """List all Ollama models: locally pulled + entire catalog."""
        from sage.models.catalog import OLLAMA_CATALOG

        pulled = self._get_pulled_names()
        seen: set[str] = set()
        models: list[ModelInfo] = []

        # First add locally pulled models
        for name in sorted(pulled):
            base_name = name.split(":")[0] if ":" in name else name
            seen.add(base_name)
            models.append(ModelInfo(id=name, provider="ollama", name=name, local=True))

        # Then add all catalog models not already listed
        for m in OLLAMA_CATALOG:
            cat_name = m.name.removeprefix("ollama:")
            if cat_name not in seen:
                seen.add(cat_name)
                models.append(
                    ModelInfo(
                        id=cat_name,
                        provider="ollama",
                        name=f"{m.display_name} ({m.params})",
                        local=False,
                    )
                )

        return models

    def _ensure_pulled(self, model: str) -> None:
        """Auto-pull a model if not already available locally."""
        import subprocess
        import sys

        pulled = self._get_pulled_names()
        base = model.split(":", maxsplit=1)[0] if ":" in model else model
        # Check if any pulled model starts with this base name
        if any(p == model or p.startswith(f"{base}:") for p in pulled):
            return

        print(f"  Model '{model}' not pulled yet — downloading via Ollama...", file=sys.stderr)
        try:
            result = subprocess.run(
                ["ollama", "pull", model],
                check=False,
                timeout=600,
            )
            if result.returncode == 0:
                print(f"  '{model}' pulled successfully!", file=sys.stderr)
                self._pulled_names = None  # reset cache
            else:
                raise RuntimeError(
                    f"ollama pull {model} failed (exit {result.returncode}). "
                    "Is Ollama running? Check: ollama serve"
                )
        except FileNotFoundError:
            raise RuntimeError("Ollama is not installed. Get it from https://ollama.com")

    def _build_messages(self, messages: list[Message]) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]

    def generate(
        self,
        messages: list[Message],
        model: str = "llama3.2",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        self._ensure_pulled(model)
        url = f"{self._base_url}/api/chat"
        payload = {
            "model": model,
            "messages": self._build_messages(messages),
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        import os
        _read_timeout = float(os.environ.get("SAGE_OLLAMA_TIMEOUT", "600"))
        _http_timeout = httpx.Timeout(connect=10.0, read=_read_timeout, write=30.0, pool=10.0)
        with httpx.Client(timeout=_http_timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            msg = resp.json().get("message", {})
            content = msg.get("content", "")
            thinking = msg.get("thinking", "")
            # Thinking models (qwen3.5, deepseek-r1) may put all output in 'thinking'
            if not content.strip() and thinking.strip():
                return thinking.strip()
            if thinking.strip() and content.strip():
                return f"<thinking>\n{thinking.strip()}\n</thinking>\n\n{content.strip()}"
            return content

    def stream(
        self,
        messages: list[Message],
        model: str = "llama3.2",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        self._ensure_pulled(model)
        url = f"{self._base_url}/api/chat"
        payload = {
            "model": model,
            "messages": self._build_messages(messages),
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        import os
        _read_timeout = float(os.environ.get("SAGE_OLLAMA_TIMEOUT", "600"))
        _http_timeout = httpx.Timeout(connect=10.0, read=_read_timeout, write=30.0, pool=10.0)
        started_thinking = False
        with httpx.Client(timeout=_http_timeout) as client:
            with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = chunk.get("message", {})
                    content = msg.get("content", "")
                    thinking = msg.get("thinking", "")

                    if thinking:
                        if not started_thinking:
                            yield "<thinking>\n"
                            started_thinking = True
                        yield thinking

                    if content:
                        if started_thinking:
                            yield "\n</thinking>\n\n"
                            started_thinking = False
                        yield content

                    if chunk.get("done"):
                        if started_thinking:
                            yield "\n</thinking>\n\n"
                        break


def build_openai_compat_providers(config: SageConfig) -> list[ProviderBase]:
    """Build all OpenAI-compatible providers from their specs."""
    providers: list[ProviderBase] = []
    for spec in PROVIDER_SPECS:
        providers.append(OpenAICompatProvider(spec, config))
    return providers
