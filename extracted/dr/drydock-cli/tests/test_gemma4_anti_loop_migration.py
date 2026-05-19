"""Regression: gemma4 stale temperature should migrate to 1.0.

Per the ai.plainenglish.io Gemma 4 anti-loop recipe, temperature MUST
be 1.0 for Gemma 4 — lower values reinforce looping on quantized GGUF.
Pre-v2.7 configs carried the historic 0.2 default. Auto-migration on
launch bumps it.
"""
from __future__ import annotations

import tomllib
from pathlib import Path

import tomli_w

from drydock.core.config.migrate import migrate_user_config


def _write(path: Path, data: dict) -> None:
    with path.open("wb") as f:
        tomli_w.dump(data, f)


def _read(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def test_gemma_stale_temperature_bumped_to_1_0(tmp_path: Path) -> None:
    cfg = tmp_path / "config.toml"
    _write(cfg, {
        "active_model": "local",
        "models": [
            {"name": "gemma4", "provider": "vllm", "alias": "local",
             "temperature": 0.2, "context_window": 131072,
             "auto_compact_threshold": 126976},
        ],
    })
    migrate_user_config(cfg)
    out = _read(cfg)
    assert out["models"][0]["temperature"] == 1.0


def test_user_override_temperature_preserved(tmp_path: Path) -> None:
    """Any non-0.2 temperature is treated as a deliberate choice."""
    cfg = tmp_path / "config.toml"
    _write(cfg, {
        "models": [
            {"name": "gemma4", "provider": "vllm", "alias": "local",
             "temperature": 0.5, "context_window": 131072},
        ],
    })
    migrate_user_config(cfg)
    out = _read(cfg)
    assert out["models"][0]["temperature"] == 0.5


def test_non_gemma_model_unaffected(tmp_path: Path) -> None:
    cfg = tmp_path / "config.toml"
    _write(cfg, {
        "models": [
            {"name": "devstral-small-latest", "provider": "mistral",
             "alias": "devstral", "temperature": 0.2, "context_window": 131072},
        ],
    })
    migrate_user_config(cfg)
    out = _read(cfg)
    assert out["models"][0]["temperature"] == 0.2


def test_gemma_missing_extra_params_seeded(tmp_path: Path) -> None:
    cfg = tmp_path / "config.toml"
    _write(cfg, {
        "models": [
            {"name": "gemma4", "provider": "llamacpp", "alias": "local",
             "temperature": 1.0, "context_window": 32768},
        ],
    })
    migrate_user_config(cfg)
    out = _read(cfg)
    extra = out["models"][0]["extra_params"]
    assert extra["top_k"] == 40
    assert extra["top_p"] == 0.95
    assert extra["repeat_penalty"] == 1.1
    assert extra["max_tokens"] == 2048


def test_gemma_existing_extra_params_preserved(tmp_path: Path) -> None:
    cfg = tmp_path / "config.toml"
    _write(cfg, {
        "models": [
            {"name": "gemma4", "provider": "llamacpp", "alias": "local",
             "temperature": 1.0, "context_window": 32768,
             "extra_params": {"top_k": 20, "max_tokens": 4096}},
        ],
    })
    migrate_user_config(cfg)
    out = _read(cfg)
    # User's choices are preserved verbatim.
    assert out["models"][0]["extra_params"] == {"top_k": 20, "max_tokens": 4096}
