"""Configuration management for Sage CLI.

Config lives at ~/.sage/config.json with environment variable overrides.

Environment variables:
    SAGE_DEFAULT_MODEL      — Override default model (e.g. "gemini:gemini-2.0-flash")
    SAGE_PREFERRED_CLOUD    — Preferred deployment target (e.g. "gcp", "aws", "azure")
    SAGE_GEMINI_API_KEY     — Google Gemini API key
    SAGE_GROQ_API_KEY       — Groq API key (free: console.groq.com)
    SAGE_OPENROUTER_API_KEY — OpenRouter API key (free models available)
    SAGE_CEREBRAS_API_KEY   — Cerebras API key (free: cloud.cerebras.ai)
    SAGE_SAMBANOVA_API_KEY  — SambaNova API key (free: cloud.sambanova.ai)
    SAGE_TOGETHER_API_KEY   — Together AI API key (free tier)
    SAGE_MISTRAL_API_KEY    — Mistral API key (free tier: console.mistral.ai)
    SAGE_COHERE_API_KEY     — Cohere API key (free: dashboard.cohere.com)
    SAGE_DEEPSEEK_API_KEY   — DeepSeek API key (cheap: platform.deepseek.com)
    SAGE_DEEPINFRA_API_KEY  — DeepInfra API key
    GITHUB_TOKEN            — GitHub token for GitHub Models (free)
    SAGE_TEMPERATURE        — Default temperature (0.0–2.0)
    SAGE_MAX_TOKENS         — Default max output tokens

Config version history:
    1 — Initial config format
    2 — Added version field, validation, available_providers
    3 — Added preferred_cloud for deployment targeting
"""

from __future__ import annotations

# Config format version for migrations
CONFIG_VERSION = 3

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from sage.core.credentials import load_project_env_files

SAGE_DIR = Path.home() / ".sage"
CONFIG_PATH = SAGE_DIR / "config.json"

# Env var → config key mapping
_ENV_MAP: dict[str, tuple[str, type]] = {
    "SAGE_DEFAULT_MODEL": ("default_model", str),
    "SAGE_PREFERRED_CLOUD": ("preferred_cloud", str),
    "SAGE_GEMINI_API_KEY": ("api_keys.gemini", str),
    "SAGE_GROQ_API_KEY": ("api_keys.groq", str),
    "SAGE_OPENROUTER_API_KEY": ("api_keys.openrouter", str),
    "SAGE_CEREBRAS_API_KEY": ("api_keys.cerebras", str),
    "SAGE_SAMBANOVA_API_KEY": ("api_keys.sambanova", str),
    "SAGE_TOGETHER_API_KEY": ("api_keys.together", str),
    "SAGE_MISTRAL_API_KEY": ("api_keys.mistral", str),
    "SAGE_COHERE_API_KEY": ("api_keys.cohere", str),
    "SAGE_DEEPSEEK_API_KEY": ("api_keys.deepseek", str),
    "SAGE_DEEPINFRA_API_KEY": ("api_keys.deepinfra", str),
    "GITHUB_TOKEN": ("api_keys.github", str),
    "SAGE_TEMPERATURE": ("temperature", float),
    "SAGE_MAX_TOKENS": ("max_tokens", int),
}


@dataclass
class LocalModel:
    """A registered local GGUF model."""

    path: str
    provider: str = "llama_cpp"
    threads: int | None = None


# Provider keys that can be configured
PROVIDER_KEYS: tuple[str, ...] = (
    "gemini",
    "groq",
    "openrouter",
    "cerebras",
    "sambanova",
    "together",
    "mistral",
    "cohere",
    "deepseek",
    "deepinfra",
    "github",
)

# Providers that work without API keys (free/open)
FREE_PROVIDERS: tuple[str, ...] = (
    "llama_cpp",
)


class ConfigValidationError(ValueError):
    """Raised when config validation fails."""

    pass


@dataclass
class SageConfig:
    """Full configuration state."""

    # Default: llama3.2-3b via llama_cpp (downloaded from GCS with sage pull)
    default_model: str = "llama_cpp:llama3.2-3b"
    temperature: float = 0.7
    max_tokens: int = 16384
    system_prompt: str = ""
    preferred_cloud: str = ""
    api_keys: dict[str, str] = field(default_factory=dict)
    models: dict[str, dict[str, Any]] = field(default_factory=dict)
    version: int = CONFIG_VERSION

    # ── Validation ─────────────────────────────────────────────

    def validate(self) -> list[str]:
        """Validate config values and return list of errors (empty if valid)."""
        errors: list[str] = []

        # Temperature must be 0.0-2.0
        if not 0.0 <= self.temperature <= 2.0:
            errors.append(f"temperature must be 0.0-2.0, got {self.temperature}")

        # Max tokens must be positive
        if self.max_tokens < 1:
            errors.append(f"max_tokens must be positive, got {self.max_tokens}")

        # Model format: provider:model_name or local model name
        if self.default_model and ":" in self.default_model:
            provider = self.default_model.split(":")[0]
            valid_providers = set(PROVIDER_KEYS) | set(FREE_PROVIDERS)
            if provider not in valid_providers:
                errors.append(f"unknown provider '{provider}' in default_model")

        return errors

    def validate_or_raise(self) -> None:
        """Validate config and raise ConfigValidationError if invalid."""
        errors = self.validate()
        if errors:
            raise ConfigValidationError("; ".join(errors))

    # ── Serialization ───────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SageConfig:
        # Handle version migrations
        data_version = data.get("version", 1)
        if data_version < CONFIG_VERSION:
            data = _migrate_config(data, data_version)

        dm = data.get("default_model", "ollama:llama3.2")
        if isinstance(dm, str) and dm.startswith("pollinations:"):
            dm = "ollama:llama3.2"
        return cls(
            default_model=dm,
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens", 16384),
            system_prompt=data.get("system_prompt", ""),
            preferred_cloud=data.get("preferred_cloud", ""),
            api_keys=data.get("api_keys", {}),
            models=data.get("models", {}),
            version=CONFIG_VERSION,
        )

    # ── Convenience accessors ───────────────────────────────

    def gemini_api_key(self) -> str | None:
        return self.api_keys.get("gemini") or None

    def available_providers(self) -> list[str]:
        """Return list of providers that have API keys configured."""
        configured: list[str] = []
        for key in PROVIDER_KEYS:
            if self.api_keys.get(key):
                configured.append(key)
        # Add free providers that are always available
        configured.extend(FREE_PROVIDERS)
        return configured

    def has_provider(self, provider: str) -> bool:
        """Check if a provider is available (has API key or is free)."""
        if provider in FREE_PROVIDERS:
            return True
        return bool(self.api_keys.get(provider))

    def get_local_model(self, name: str) -> LocalModel | None:
        entry = self.models.get(name)
        if not entry:
            return None
        return LocalModel(
            path=entry["path"],
            provider=entry.get("provider", "llama_cpp"),
            threads=entry.get("threads"),
        )

    def local_model_names(self) -> list[str]:
        return list(self.models.keys())


# ── Load / Save ─────────────────────────────────────────────


def _ensure_dir() -> None:
    SAGE_DIR.mkdir(parents=True, exist_ok=True)


def _migrate_config(data: dict[str, Any], from_version: int) -> dict[str, Any]:
    """Migrate config data from older versions to current."""
    # Version 1 -> 2: No structural changes, just added version field
    # Future migrations would go here:
    # if from_version < 2:
    #     data = _migrate_v1_to_v2(data)
    # if from_version < 3:
    #     data = _migrate_v2_to_v3(data)
    return data


def load_config(path: Path = CONFIG_PATH) -> SageConfig:
    """Load config from disk, then apply environment variable overrides."""
    load_project_env_files(Path.cwd(), override=False)
    if path.exists():
        try:
            data = json.loads(path.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}

    cfg = SageConfig.from_dict(data)
    _apply_env_overrides(cfg)
    return cfg


def save_config(cfg: SageConfig, path: Path = CONFIG_PATH) -> None:
    """Persist config to disk."""
    _ensure_dir()
    path.write_text(json.dumps(cfg.to_dict(), indent=2) + "\n", "utf-8")


def _apply_env_overrides(cfg: SageConfig) -> None:
    """Apply SAGE_* environment variables on top of loaded config."""
    for env_var, (key, cast) in _ENV_MAP.items():
        value = os.environ.get(env_var)
        if value is None:
            continue
        if "." in key:
            # Nested key like "api_keys.gemini"
            parts = key.split(".", 1)
            container = getattr(cfg, parts[0])
            container[parts[1]] = cast(value)
        else:
            setattr(cfg, key, cast(value))


def set_config_value(key: str, value: str, path: Path = CONFIG_PATH) -> None:
    """Set a single config key and save. Supports dot notation for nested keys."""
    cfg = load_config(path)

    if key == "default_model":
        cfg.default_model = value
    elif key == "preferred_cloud":
        cfg.preferred_cloud = value
    elif key == "temperature":
        cfg.temperature = float(value)
    elif key == "max_tokens":
        cfg.max_tokens = int(value)
    elif key == "system_prompt":
        cfg.system_prompt = value
    elif key.startswith("api_keys."):
        subkey = key.split(".", 1)[1]
        cfg.api_keys[subkey] = value
    elif key.startswith("models."):
        # models.deepseek.path = /path/to/file
        parts = key.split(".", 2)
        if len(parts) == 3:
            model_name, field_name = parts[1], parts[2]
            if model_name not in cfg.models:
                cfg.models[model_name] = {"path": "", "provider": "llama_cpp"}
            cfg.models[model_name][field_name] = value
    else:
        raise KeyError(f"Unknown config key: {key}")

    save_config(cfg, path)


def get_config_value(key: str, path: Path = CONFIG_PATH) -> Any:
    """Read a single config value. Supports dot notation."""
    cfg = load_config(path)

    if key == "default_model":
        return cfg.default_model
    elif key == "preferred_cloud":
        return cfg.preferred_cloud
    elif key == "temperature":
        return cfg.temperature
    elif key == "max_tokens":
        return cfg.max_tokens
    elif key == "system_prompt":
        return cfg.system_prompt
    elif key.startswith("api_keys."):
        subkey = key.split(".", 1)[1]
        return cfg.api_keys.get(subkey)
    elif key.startswith("models."):
        parts = key.split(".", 2)
        model_name = parts[1]
        if len(parts) == 3:
            return (cfg.models.get(model_name) or {}).get(parts[2])
        return cfg.models.get(model_name)
    else:
        raise KeyError(f"Unknown config key: {key}")
