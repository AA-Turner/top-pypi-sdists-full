"""Model configuration loaded from JSON - single source of truth for all supported models."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Optional


@dataclass(frozen=True)
class ChatModelSpec:
    """Specification for a chat/LLM model."""

    provider: str  # "openai", "fireworks", etc.
    model_id: str  # The actual model identifier for the API
    api_model: str  # Model string to send to the API
    context_window: int  # Max context tokens
    max_output_tokens: int  # Max output tokens
    supports_tools: bool  # Whether model supports function calling
    supports_vision: bool  # Whether model supports image input
    supports_thinking: bool  # Whether model supports extended thinking
    description: str  # Human-readable description
    # Pricing per 1M tokens (USD)
    input_price: float = 0.0  # Cost per 1M input tokens
    output_price: float = 0.0  # Cost per 1M output tokens


@dataclass(frozen=True)
class ProviderConfig:
    """Configuration for an API provider."""

    name: str
    base_url: str | None  # None = OpenAI default
    api_key: str  # "$ENV_VAR" to read from env, or a literal key
    headers: tuple[tuple[str, str], ...] = ()  # (key, value) pairs; values support "$ENV_VAR"
    stream: bool = False  # Force streaming mode (required by some proxies)


@dataclass
class ModelEntry:
    """A model entry from the registry."""

    name: str  # canonical name (key in config)
    spec: ChatModelSpec
    aliases: list[str]

    @property
    def provider(self) -> str:
        return self.spec.provider

    @property
    def model_id(self) -> str:
        return self.spec.model_id

    @property
    def api_model(self) -> str:
        return self.spec.api_model

    @property
    def context_window(self) -> int:
        return self.spec.context_window


def _default_config() -> dict:
    """Return the default config.json structure for new projects."""
    return {
        "providers": {
            "fireworks": {
                "base_url": "https://api.fireworks.ai/inference/v1",
                "api_key": "$FIREWORKS_API_KEY",
                "models": {
                    "kimi-k2p5": {
                        "id": "accounts/fireworks/models/kimi-k2p5",
                        "supports_vision": True,
                        "supports_thinking": True,
                    },
                    "minimax-m2p1": {
                        "id": "accounts/fireworks/models/minimax-m2p1",
                        "supports_vision": False,
                        "supports_thinking": True,
                    },
                    "glm-4p7": {
                        "id": "accounts/fireworks/models/glm-4p7",
                        "supports_vision": False,
                        "supports_thinking": True,
                    },
                },
            }
        },
        "default_model": "fireworks:kimi-k2p5",
        "vision_model": "fireworks:kimi-k2p5",
        "fast_model": "fireworks:gpt-oss-120b",
        "settings": {
            "thinking_budget": 500,
            "reasoning_effort": "low",
            "reasoning": True,
            "thinking": True,
            "inject_context_frame": False,
            "enable_apply_diff": True,
            "session_autosave": True,
            "checkpoints_enabled": True,
            "log_llm_payload": False,
            "use_worktree": False,
            "tasks_v2": True,
            "max_workers": 4,
            "batch_size": 1000,
            "compaction_strategy": "observational_memory",
            "default_plan_mode": True,
        },
    }


class ModelRegistry:
    """Loads and indexes model config from JSON."""

    _instance: ClassVar[Optional["ModelRegistry"]] = None

    def __init__(self):
        self.providers: dict[str, ProviderConfig] = {}
        self.models: dict[str, ModelEntry] = {}  # canonical name -> entry
        self._alias_map: dict[str, str] = {}  # alias -> canonical name
        self.default_model: str = ""
        self.vision_model: str = ""
        self.fast_model: str = ""
        self.settings: dict = {}
        self.config_path: str = ""
        self._load()

    @classmethod
    def get(cls) -> "ModelRegistry":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None

    def _load(self) -> None:
        # Single source of truth: .emdash/config.json in current working directory.
        cwd_config = Path.cwd() / ".emdash" / "config.json"
        path = cwd_config if cwd_config.is_file() else None

        if path and path.is_file():
            self.config_path = str(path)
            with open(path) as f:
                data = json.load(f)
        else:
            # No config found — create a default config.json
            data = _default_config()
            # Write to the best location: cwd > repo root
            write_path = cwd_config
            try:
                write_path.parent.mkdir(parents=True, exist_ok=True)
                with open(write_path, "w") as f:
                    json.dump(data, f, indent=2)
                    f.write("\n")
                self.config_path = str(write_path)
                print(f"Created default config: {write_path}")
            except Exception as e:
                self.config_path = "(built-in)"
                print(f"Warning: could not write default config ({e}), using built-in defaults")

        # Load providers and their nested models
        for provider_name, prov_data in data.get("providers", {}).items():
            if not isinstance(prov_data, dict):
                # Skip non-dict entries (e.g. misplaced top-level keys inside providers)
                print(
                    f"Warning: '{provider_name}' inside 'providers' is not a dict "
                    f"— should it be a top-level key? Skipping."
                )
                continue
            raw_headers = prov_data.get("headers", {})
            headers = tuple((k, v) for k, v in raw_headers.items())
            self.providers[provider_name] = ProviderConfig(
                name=provider_name,
                base_url=prov_data.get("base_url"),
                api_key=prov_data.get("api_key", ""),
                headers=headers,
                stream=bool(prov_data.get("stream", False)),
            )

            # Models are nested under the provider
            for model_name, model_data in prov_data.get("models", {}).items():
                model_id = model_data.get("id", model_name)
                spec = ChatModelSpec(
                    provider=provider_name,
                    model_id=model_id,
                    api_model=model_id,
                    context_window=model_data.get("context_window", 128000),
                    max_output_tokens=model_data.get("max_output_tokens", 16384),
                    supports_tools=model_data.get("supports_tools", True),
                    supports_vision=model_data.get("supports_vision", False),
                    supports_thinking=model_data.get("supports_thinking", False),
                    description=model_data.get("description", ""),
                    input_price=model_data.get("input_price", 0.0),
                    output_price=model_data.get("output_price", 0.0),
                )
                aliases = model_data.get("aliases", [])
                entry = ModelEntry(name=model_name, spec=spec, aliases=aliases)
                self.models[model_name] = entry

                # Also store under provider/model_name for disambiguation
                # when multiple providers define the same model name
                provider_key = f"{provider_name}/{model_name}"
                self.models[provider_key] = entry

                # Index aliases
                for alias in aliases:
                    self._alias_map[alias.lower()] = model_name

        self.default_model = data.get("default_model", "")
        self.vision_model = data.get("vision_model", "")
        self.fast_model = data.get("fast_model", "")
        self.settings = data.get("settings", {}) if isinstance(data.get("settings", {}), dict) else {}

    def get_model(self, name: str) -> ModelEntry | None:
        """Look up a model by canonical name, alias, or raw model_id.

        Also handles provider:model_id format (e.g. "fireworks:accounts/fireworks/models/minimax-m2p1").
        """
        name = name.strip()

        # 1. Canonical name
        if name in self.models:
            return self.models[name]

        # 2. Alias (case-insensitive)
        canonical = self._alias_map.get(name.lower())
        if canonical:
            return self.models[canonical]

        # 3. provider:name format (e.g. "fireworks:kimi-k2p5")
        if ":" in name:
            provider, model_part = name.split(":", 1)
            # Direct lookup via provider/model_name key
            prefixed = f"{provider}/{model_part}"
            if prefixed in self.models:
                return self.models[prefixed]
            # Fallback: iterate and match by model_id or alias
            for _, entry in self.models.items():
                if entry.spec.provider != provider:
                    continue
                if (entry.spec.model_id == model_part
                        or model_part.lower() in [a.lower() for a in entry.aliases]):
                    return entry

        # 4. Raw model_id match
        for entry in self.models.values():
            if entry.spec.model_id == name:
                return entry

        return None

    def get_provider_config(self, provider_name: str) -> ProviderConfig | None:
        return self.providers.get(provider_name)

    def get_setting(self, key: str, default=None):
        """Read a setting from config.json settings."""
        return self.settings.get(key, default)

    def list_all(self) -> list[dict]:
        """List all models with their specs for display."""
        seen: set[int] = set()
        result = []
        for entry in self.models.values():
            eid = id(entry)
            if eid in seen:
                continue
            seen.add(eid)
            result.append({
                "name": entry.name,
                "provider": entry.spec.provider,
                "model_id": entry.spec.model_id,
                "api_model": entry.spec.api_model,
                "context_window": entry.spec.context_window,
                "supports_tools": entry.spec.supports_tools,
                "description": entry.spec.description,
            })
        return result

    def get_default(self) -> ModelEntry:
        entry = self.get_model(self.default_model)
        if entry is None:
            # Fallback to first model in registry
            return next(iter(self.models.values()))
        return entry


# ═══════════════════════════════════════════════════════════════════════════════
# Pricing Utilities
# ═══════════════════════════════════════════════════════════════════════════════

# Fallback pricing for models not in the registry (per 1M tokens)
FALLBACK_PRICING: dict[str, tuple[float, float]] = {
    # Format: "model_pattern": (input_price, output_price)
    # OpenAI
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4o": (2.50, 10.0),
    "gpt-4-turbo": (10.0, 30.0),
    # Fireworks (generic fallback)
    "fireworks": (0.50, 1.50),
    # Default fallback
    "default": (0.50, 1.50),
}


def get_model_pricing(model: str) -> tuple[float, float]:
    """Get pricing for a model (input_price, output_price per 1M tokens).

    Args:
        model: Model string (can be canonical name, alias, or raw model ID)

    Returns:
        Tuple of (input_price, output_price) per 1M tokens
    """
    # Try to look up in registry
    entry = ModelRegistry.get().get_model(model)
    if entry:
        return (entry.spec.input_price, entry.spec.output_price)

    # Try fallback patterns
    model_lower = model.lower()
    for pattern, pricing in FALLBACK_PRICING.items():
        if pattern in model_lower:
            return pricing

    # Default fallback
    return FALLBACK_PRICING["default"]


def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str,
    thinking_tokens: int = 0,
) -> float:
    """Calculate cost for token usage.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Model string
        thinking_tokens: Number of thinking tokens (charged as output)

    Returns:
        Total cost in USD
    """
    input_price, output_price = get_model_pricing(model)

    # Thinking tokens are typically charged at output rate
    total_output = output_tokens + thinking_tokens

    # Price is per 1M tokens
    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (total_output / 1_000_000) * output_price

    return input_cost + output_cost
