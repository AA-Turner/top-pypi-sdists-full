"""Provider router — resolves model IDs and handles fallback."""

from __future__ import annotations

import sys
from collections.abc import Iterator

from sage.providers.base import Message, ModelInfo, ProviderBase


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

    def resolve(self, model_id: str) -> tuple[ProviderBase, str]:
        """Resolve a model_id into (provider, model_name).

        Raises RuntimeError if no provider can serve the request.
        """
        effective = model_id or self._default_model

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
        provider, model_name = self.resolve(model_id)
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
        provider, model_name = self.resolve(model_id)
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
