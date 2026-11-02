"""Configuration resolution."""

from __future__ import annotations

import os
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


import runta as _public

DEFAULT_ENDPOINT = "https://api.runta.com"


def resolve_config(
    *,
    endpoint: str | None,
    token: str | None,
    config_path: str | Path | None,
) -> tuple[str, str]:
    file_config = _read_config(config_path)
    resolved_endpoint = (
        _clean(endpoint)
        or _clean(os.getenv("RUNTA_ENDPOINT"))
        or file_config[0]
        or DEFAULT_ENDPOINT
    )
    resolved_token = _clean(token) or _clean(os.getenv("RUNTA_TOKEN")) or file_config[1]
    if not resolved_token:
        raise _public.ConfigError("missing token: pass token=... or set RUNTA_TOKEN")
    return resolved_endpoint, resolved_token


def _read_config(config_path: str | Path | None) -> tuple[str | None, str | None]:
    path = (
        Path(config_path).expanduser()
        if config_path is not None
        else Path(os.getenv("RUNTA_CONFIG", "~/.config/runta/config.toml")).expanduser()
    )
    if not path.exists():
        return None, None
    try:
        data = tomllib.loads(path.read_text())
    except OSError as exc:
        raise _public.ConfigError(f"failed to read config file {path}: {exc}") from exc
    except tomllib.TOMLDecodeError as exc:
        raise _public.ConfigError(f"failed to parse config file {path}: {exc}") from exc
    return _clean(data.get("endpoint")), _clean(data.get("token"))


def _clean(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None
