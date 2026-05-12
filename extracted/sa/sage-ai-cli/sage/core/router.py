"""Provider router — resolves model IDs and handles fallback."""

from __future__ import annotations

import re
import sys
from collections.abc import Iterator

from sage.providers.base import Message, ModelInfo, ProviderBase


# ── Task-aware model picking (C8) ─────────────────────────────────────


# Small-model context window estimate. Used to filter models that can't
# fit a large context. Conservative: real values vary 4k-128k. Anything
# below this we consider "small-context" and skip when context_size is
# large.
_SMALL_CTX_TOKENS = 16_000

# Token estimate per char (rough, English-ish): ~4 chars per token.
_CHARS_PER_TOKEN = 4

# Substrings that signal a complex task. Lowercased; matched as
# substrings, not whole words.
_COMPLEX_HINTS = (
    "architect", "refactor", "redesign", "design the", "design a",
    "rewrite", "overhaul", "migrate", "all modules", "across the codebase",
    "every file", "system", "multi-file", "subsystem", "the entire",
)

# Substrings that signal a trivial task.
_TRIVIAL_HINTS = (
    "rename", "typo", "format", "lint",
    "fix the typo", "fix typo", "add a comment", "add comment",
    "rename ", "remove unused",
)


# Small-tier model name fragments (3B-class).
_SMALL_TIER = (
    "3b", "-3b-", "llama3.2", "qwen2.5-coder-3b",
    "gemini-2.0-flash", "phi3-mini", "phi4-mini", "haiku",
)

# Big-tier model name fragments (≥30B-class).
_BIG_TIER = (
    "qwen3-coder", "qwen3.5", "deepseek-r1", "deepseek-coder-v2",
    "70b", "-65b", "-72b", "opus", "gpt-4", "gemini-2.5",
    "mistral-large", "qwen2.5-coder-32b",
)


def classify_task_complexity(prompt: str) -> str:
    """Heuristic complexity classifier.

    Returns "trivial", "medium", or "complex". Cheap, pattern-based.
    No model call — runs in microseconds so it's safe to invoke per turn.
    The output drives `pick_model_for_task` below.
    """
    text = (prompt or "").strip().lower()
    if not text:
        return "medium"

    # Length-based prior: very short prompts trend trivial, very long trend complex.
    n = len(text)

    if any(h in text for h in _COMPLEX_HINTS):
        return "complex"
    if n > 400:
        # Long prompts are usually multi-step or context-heavy.
        return "complex"

    if any(h in text for h in _TRIVIAL_HINTS):
        return "trivial"

    return "medium"


def _tier_of(model: ModelInfo) -> str:
    name = model.id.lower()
    if any(frag in name for frag in _BIG_TIER):
        return "big"
    if any(frag in name for frag in _SMALL_TIER):
        return "small"
    return "medium"


def _prompt_and_context(messages: list[Message]) -> tuple[str, int]:
    """Extract (latest_user_prompt, total_context_tokens_estimate) from
    a message list. Used by generate/stream to feed the auto-picker.

    Latest user message wins for prompt — it's what the user actually
    just asked. Total context is summed across all messages to spot
    when we're approaching small-model context limits.
    """
    latest_user = ""
    total_chars = 0
    for m in messages:
        total_chars += len(getattr(m, "content", "") or "")
        if getattr(m, "role", "") == "user":
            latest_user = m.content or latest_user
    # Rough token estimate: ~4 chars per token (English-ish)
    return latest_user, total_chars // _CHARS_PER_TOKEN


def pick_model_for_task(
    prompt: str,
    available: list[ModelInfo],
    context_size: int = 0,
) -> str | None:
    """Pick the smallest model strong enough for the task.

    Returns a model id (matching one of `available`), or None when the
    available list is empty.

    Strategy:
      1. Classify complexity from the prompt.
      2. Map complexity → desired tier (trivial→small, medium→medium, complex→big).
      3. If `context_size` indicates the prompt is large, force at least medium tier.
      4. Pick a model in the desired tier. Fall back to the closest tier
         when the desired one isn't available — never return None just
         because the user lacks a 70B model.
    """
    if not available:
        return None

    complexity = classify_task_complexity(prompt)
    desired = {"trivial": "small", "medium": "medium", "complex": "big"}[complexity]

    # Context-window guard: if context is large, small-tier models can't fit it.
    big_context = context_size and context_size >= _SMALL_CTX_TOKENS // 2
    if big_context and desired == "small":
        desired = "medium"

    # Bucket models by tier
    buckets: dict[str, list[ModelInfo]] = {"small": [], "medium": [], "big": []}
    for m in available:
        buckets[_tier_of(m)].append(m)

    if big_context:
        # Filter out small-tier from all buckets even if their tier resolves
        # higher — we don't trust a 3B model to hold 100k tokens.
        buckets["small"] = []

    # Try desired tier first, then walk up, then walk down.
    walk = {
        "small": ["small", "medium", "big"],
        "medium": ["medium", "big", "small"],
        "big": ["big", "medium", "small"],
    }[desired]

    for tier in walk:
        if buckets[tier]:
            return buckets[tier][0].id
    # Belt-and-braces — return any model if all buckets ended up empty
    # (shouldn't happen unless the available list itself is empty).
    return available[0].id


class ProviderRouter:
    """Routes generation requests to the right provider.

    Model ID formats:
      "gemini:gemini-2.0-flash"  — explicit provider prefix
      "deepseek"                 — looks up in registered providers
      ""                         — uses default_model from config

    Fallback: if the chosen provider raises, tries the next available one.
    """

    def __init__(
        self,
        providers: list[ProviderBase],
        default_model: str = "",
    ) -> None:
        self._providers: dict[str, ProviderBase] = {}
        self._fallback_order: list[str] = []
        for p in providers:
            self._providers[p.name] = p
            self._fallback_order.append(p.name)
        self._default_model = default_model

    # ── Resolution ──────────────────────────────────────────

    def resolve(self, model_id: str, prompt: str = "", context_size: int = 0) -> tuple[ProviderBase, str]:
        """Resolve a model_id into (provider, model_name).

        Special prefix: "auto" routes via task-complexity heuristics.
        Pass the user prompt (and optional context_size in tokens) so the
        picker can size the model to the task.

        Raises RuntimeError if no provider can serve the request.
        """
        effective = model_id or self._default_model

        if effective == "auto":
            available = self.list_all_models()
            picked = pick_model_for_task(prompt, available, context_size=context_size)
            if picked is None:
                raise RuntimeError(
                    "Auto-routing has no models to pick from. Configure a "
                    "provider (e.g. `sage config set api_keys.gemini ...`) or "
                    "pull a local model (`sage pull llama3.2`)."
                )
            # Re-resolve through the standard path so the (provider, name) lookup is consistent.
            for p in self._providers.values():
                if any(m.id == picked for m in p.list_models()):
                    return p, picked
            # Should not reach here, but fall through to first available provider:
            effective = picked

        if ":" in effective:
            provider_name, model_name = effective.split(":", 1)
            provider = self._providers.get(provider_name)
            if provider and provider.is_available():
                return provider, model_name
            if provider is None:
                raise RuntimeError(
                    f"Requested provider '{provider_name}' is not registered or not available."
                )
            raise RuntimeError(f"Requested provider '{provider_name}' is not available.")

        # No prefix — search providers for a matching model
        for name in self._fallback_order:
            provider = self._providers[name]
            if not provider.is_available():
                continue
            known_ids = {m.id for m in provider.list_models()}
            if effective in known_ids:
                return provider, effective

        # Still no match — return first available provider with its default model
        for name in self._fallback_order:
            provider = self._providers[name]
            if provider.is_available():
                models = provider.list_models()
                if models:
                    return provider, models[0].id

        raise RuntimeError(
            "No providers available. Configure Gemini API key or register a local model.\n"
            "  sage config set api_keys.gemini YOUR_KEY\n"
            "  sage config set models.mymodel.path /path/to/model.gguf"
        )

    # ── Generation with fallback ────────────────────────────

    def generate(
        self,
        messages: list[Message],
        model_id: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        lock_provider: bool = False,
    ) -> str:
        prompt, ctx = _prompt_and_context(messages) if model_id == "auto" else ("", 0)
        provider, model_name = self.resolve(model_id, prompt=prompt, context_size=ctx)
        errors: list[str] = [provider.name]
        error_details: list[str] = []

        try:
            return provider.generate(messages, model_name, temperature, max_tokens)
        except KeyboardInterrupt:
            raise  # Never swallow Ctrl+C
        except Exception as exc:
            print(f"  [{provider.name}] failed: {exc}", file=sys.stderr)
            error_details.append(f"{provider.name}: {exc}")
            if lock_provider:
                raise RuntimeError(
                    f"Requested model '{model_id}' failed on provider '{provider.name}': {exc}"
                ) from exc

        # Fallback to other providers
        for name in self._fallback_order:
            if name in errors:
                continue
            fallback = self._providers[name]
            if not fallback.is_available():
                continue
            errors.append(name)
            models = fallback.list_models()
            if not models:
                continue
            try:
                return fallback.generate(messages, models[0].id, temperature, max_tokens)
            except KeyboardInterrupt:
                raise  # Never swallow Ctrl+C
            except Exception as exc:
                print(f"  [{name}] fallback failed: {exc}", file=sys.stderr)
                error_details.append(f"{name}: {exc}")

        detail = " | ".join(error_details) if error_details else "no details"
        raise RuntimeError(f"All providers failed: {', '.join(errors)} ({detail})")

    def stream(
        self,
        messages: list[Message],
        model_id: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        lock_provider: bool = False,
    ) -> Iterator[str]:
        prompt, ctx = _prompt_and_context(messages) if model_id == "auto" else ("", 0)
        provider, model_name = self.resolve(model_id, prompt=prompt, context_size=ctx)
        errors: list[str] = [provider.name]
        error_details: list[str] = []

        try:
            yield from provider.stream(messages, model_name, temperature, max_tokens)
            return
        except KeyboardInterrupt:
            raise  # Never swallow Ctrl+C
        except Exception as exc:
            print(f"  [{provider.name}] failed: {exc}", file=sys.stderr)
            error_details.append(f"{provider.name}: {exc}")
            if lock_provider:
                raise RuntimeError(
                    f"Requested model '{model_id}' failed on provider '{provider.name}': {exc}"
                ) from exc

        # Fallback
        for name in self._fallback_order:
            if name in errors:
                continue
            fallback = self._providers[name]
            if not fallback.is_available():
                continue
            errors.append(name)
            models = fallback.list_models()
            if not models:
                continue
            try:
                yield from fallback.stream(messages, models[0].id, temperature, max_tokens)
                return
            except KeyboardInterrupt:
                raise  # Never swallow Ctrl+C
            except Exception as exc:
                print(f"  [{name}] fallback failed: {exc}", file=sys.stderr)
                error_details.append(f"{name}: {exc}")

        detail = " | ".join(error_details) if error_details else "no details"
        raise RuntimeError(f"All providers failed: {', '.join(errors)} ({detail})")

    # ── Listing ─────────────────────────────────────────────

    def list_all_models(self) -> list[ModelInfo]:
        """Aggregate models from all available providers."""
        out: list[ModelInfo] = []
        for provider in self._providers.values():
            if provider.is_available():
                out.extend(provider.list_models())
        return out
