"""Configuration management for Sage CLI.

Config lives at ~/.sage/config.json with environment variable overrides.
"""

from __future__ import annotations

CONFIG_VERSION = 3

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


def _noop_load(_cwd, override=False):
    return {}


try:
    from sage.core.credentials import load_project_env_files
except Exception:
    load_project_env_files = _noop_load


SAGE_DIR = Path.home() / ".sage"
CONFIG_PATH = SAGE_DIR / "config.json"

_ENV_MAP: dict[str, tuple[str, type]] = {
    "SAGE_DEFAULT_MODEL": ("default_model", str),
    "SAGE_PREFERRED_CLOUD": ("preferred_cloud", str),
    "SAGE_GEMINI_API_KEY": ("api_keys.gemini", str),
    "SAGE_GROQ_API_KEY": ("api_keys.groq", str),
    "SAGE_OPENROUTER_API_KEY": ("api_keys.openrouter", str),
    "SAGE_TEMPERATURE": ("temperature", float),
    "SAGE_MAX_TOKENS": ("max_tokens", int),
}


@dataclass
class LocalModel:
    path: str
    provider: str = "llama_cpp"
    threads: int | None = None


PROVIDER_KEYS: tuple[str, ...] = (
    "gemini", "groq", "openrouter", "cerebras", "sambanova",
    "together", "mistral", "cohere", "deepseek", "deepinfra", "github",
)
FREE_PROVIDERS: tuple[str, ...] = ("llama_cpp",)


class ConfigValidationError(ValueError):
    pass


@dataclass
class SageConfig:
    default_model: str = "llama_cpp:llama3.2-3b"
    temperature: float = 0.7
    max_tokens: int = 16384
    system_prompt: str = ""
    preferred_cloud: str = ""
    api_keys: dict[str, str] = field(default_factory=dict)
    models: dict[str, dict[str, Any]] = field(default_factory=dict)
    rag_enabled: bool = True
    rag_embedder: str = "ollama:nomic-embed-text"
    rag_top_k: int = 6
    speculative_draft_model: str = ""
    gcs_corpus_bucket: str = "gs://sage-ai-models"
    version: int = CONFIG_VERSION

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not 0.0 <= self.temperature <= 2.0:
            errors.append(f"temperature must be 0.0-2.0, got {self.temperature}")
        if self.max_tokens < 1:
            errors.append(f"max_tokens must be positive, got {self.max_tokens}")
        if self.default_model and ":" in self.default_model:
            provider = self.default_model.split(":")[0]
            valid = set(PROVIDER_KEYS) | set(FREE_PROVIDERS)
            if provider not in valid:
                errors.append(f"unknown provider '{provider}' in default_model")
        return errors

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SageConfig":
        dm = data.get("default_model", "ollama:llama3.2")
        return cls(
            default_model=dm,
            temperature=data.get("temperature", 0.7),
            max_tokens=data.get("max_tokens", 16384),
            system_prompt=data.get("system_prompt", ""),
            preferred_cloud=data.get("preferred_cloud", ""),
            api_keys=data.get("api_keys", {}),
            models=data.get("models", {}),
            rag_enabled=data.get("rag_enabled", True),
            rag_embedder=data.get("rag_embedder", "ollama:nomic-embed-text"),
            rag_top_k=int(data.get("rag_top_k", 6)),
            speculative_draft_model=data.get("speculative_draft_model", ""),
            gcs_corpus_bucket=data.get("gcs_corpus_bucket", "gs://sage-ai-models"),
            version=CONFIG_VERSION,
        )

    def gemini_api_key(self) -> str | None:
        return self.api_keys.get("gemini") or None

    def available_providers(self) -> list[str]:
        configured: list[str] = [k for k in PROVIDER_KEYS if self.api_keys.get(k)]
        configured.extend(FREE_PROVIDERS)
        return configured

    def has_provider(self, provider: str) -> bool:
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


def _ensure_dir() -> None:
    SAGE_DIR.mkdir(parents=True, exist_ok=True)


def load_config(path: Path = CONFIG_PATH) -> SageConfig:
    try:
        load_project_env_files(Path.cwd(), override=False)
    except Exception:
        pass
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
    _ensure_dir()
    path.write_text(json.dumps(cfg.to_dict(), indent=2) + "\n", "utf-8")


def _split_key(key: str) -> tuple[str, str | None]:
    if "." in key:
        head, tail = key.split(".", 1)
        return head, tail
    return key, None


def _cast_for(field_name: str, raw: str) -> Any:
    # Cast strings from the CLI into the dataclass field type. Unknown
    # fields fall through as plain strings — KeyError comes from the
    # caller when the field doesn't exist.
    field_types = {f: type(getattr(SageConfig(), f)) for f in SageConfig().__dataclass_fields__}
    target = field_types.get(field_name)
    if target is bool:
        return raw.lower() in ("1", "true", "yes", "on")
    if target is int:
        return int(raw)
    if target is float:
        return float(raw)
    return raw


def get_config_value(key: str, path: Path = CONFIG_PATH) -> Any:
    """Read a dotted config key. Raises KeyError for unknown keys."""
    cfg = load_config(path)
    head, tail = _split_key(key)
    if not hasattr(cfg, head):
        raise KeyError(f"unknown config key: {key}")
    container = getattr(cfg, head)
    if tail is None:
        return container
    if not isinstance(container, dict):
        raise KeyError(f"config key '{head}' is not a nested namespace")
    if tail not in container:
        raise KeyError(f"unknown config key: {key}")
    return container[tail]


def set_config_value(key: str, value: str, path: Path = CONFIG_PATH) -> None:
    """Set a dotted config key and persist. Raises KeyError for unknown keys."""
    cfg = load_config(path)
    head, tail = _split_key(key)
    if not hasattr(cfg, head):
        raise KeyError(f"unknown config key: {key}")
    if tail is None:
        setattr(cfg, head, _cast_for(head, value))
    else:
        container = getattr(cfg, head)
        if not isinstance(container, dict):
            raise KeyError(f"config key '{head}' is not a nested namespace")
        container[tail] = value
    save_config(cfg, path)


def _apply_env_overrides(cfg: SageConfig) -> None:
    for env_var, (key, cast) in _ENV_MAP.items():
        value = os.environ.get(env_var)
        if value is None:
            continue
        if "." in key:
            parts = key.split(".", 1)
            container = getattr(cfg, parts[0])
            container[parts[1]] = cast(value)
        else:
            setattr(cfg, key, cast(value))
