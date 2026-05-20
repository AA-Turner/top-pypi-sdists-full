"""Forward-migration of existing `~/.drydock/config.toml` files.

Drydock's `ModelConfig` schema gains new fields over time (e.g. when we
introduced `context_window` so users could control the max context size
per model). Pydantic happily accepts a missing field and falls back to
the default, but the user never *sees* the knob in their config file —
so they don't know they can tune it.

This module bridges the gap. On every launch, after the existing-config
check, we walk the user's TOML and add any keys that the current
schema declares but their file doesn't have. Idempotent: if every key
is already present we don't touch the file.

Comments are not preserved (tomli_w doesn't write them, and tomlkit
isn't a hard dependency). The user's data is round-tripped through
`tomllib` → dict → `tomli_w`, so values and structure survive intact.
"""
from __future__ import annotations

from pathlib import Path
import tomllib
from typing import Any

import tomli_w
from rich import print as rprint

from drydock.core.logger import logger


# Per-model defaults applied during migration. Heuristic on the model's
# `provider` field: llama.cpp boxes typically run `-c 32768`, while
# vLLM/Mistral defaults match Gemma 4's 131K. Users can override these
# in config.toml after migration.
_LLAMACPP_CONTEXT_WINDOW = 32_768
_LLAMACPP_COMPACT_HEADROOM = 4_096
_DEFAULT_CONTEXT_WINDOW = 131_072
_DEFAULT_COMPACT_HEADROOM = 4_096


def _default_window_for(provider: str) -> int:
    if "llamacpp" in (provider or "").lower():
        return _LLAMACPP_CONTEXT_WINDOW
    return _DEFAULT_CONTEXT_WINDOW


def _default_compact_threshold_for(window: int) -> int:
    headroom = (
        _LLAMACPP_COMPACT_HEADROOM
        if window <= _LLAMACPP_CONTEXT_WINDOW
        else _DEFAULT_COMPACT_HEADROOM
    )
    return max(8_000, window - headroom)


def migrate_user_config(config_file: Path) -> None:
    """Add any missing schema keys to the user's existing config.

    Safe to call when the file is absent — returns silently. Safe to
    call repeatedly — only writes when at least one key was added.
    Failures (unreadable file, write error) are logged at debug level
    so a broken migration never blocks startup; the eventual
    `DrydockConfig.load()` call will surface any real config errors.
    """
    if not config_file.exists():
        return

    try:
        with config_file.open("rb") as f:
            data: dict[str, Any] = tomllib.load(f)
    except (tomllib.TOMLDecodeError, OSError) as e:
        logger.debug("config migration: cannot read %s: %s", config_file, e)
        return

    added: list[str] = []
    fixed: list[str] = []
    models = data.get("models")
    if isinstance(models, list):
        for model in models:
            if not isinstance(model, dict):
                continue
            label = model.get("alias") or model.get("name") or "?"
            provider = model.get("provider", "")
            if "context_window" not in model:
                model["context_window"] = _default_window_for(provider)
                added.append(f"models.{label}.context_window")
            if "auto_compact_threshold" not in model:
                window = model.get("context_window") or _default_window_for(provider)
                model["auto_compact_threshold"] = _default_compact_threshold_for(window)
                added.append(f"models.{label}.auto_compact_threshold")
            # llamacpp models written by v2.8.3–v2.8.5 used the
            # OpenAI-style `frequency_penalty`. llama.cpp's actual
            # repetition knob is `repeat_penalty` — rename it so the
            # server accepts the value instead of silently ignoring it.
            if "llamacpp" in provider.lower():
                extra = model.get("extra_params")
                if isinstance(extra, dict) and "frequency_penalty" in extra and "repeat_penalty" not in extra:
                    extra["repeat_penalty"] = extra.pop("frequency_penalty")
                    fixed.append(f"models.{label}.extra_params: frequency_penalty → repeat_penalty")

            # Gemma 4 anti-loop recipe (ai.plainenglish.io 2026 article,
            # confirmed in this codebase 2026-05-18). The article's #1
            # finding: temperature MUST be 1.0 for Gemma 4 — lower
            # values reinforce looping on quantized GGUF. The historic
            # default in pre-v2.7 configs was 0.2; if the file still
            # carries that stale value AND the model is Gemma-family,
            # bump it. We only touch 0.2 specifically so any deliberate
            # override (0.5, 0.7) is preserved.
            model_name = (model.get("name") or "").lower()
            if "gemma" in model_name and model.get("temperature") == 0.2:
                model["temperature"] = 1.0
                fixed.append(
                    f"models.{label}.temperature: 0.2 → 1.0 (Gemma 4 anti-loop)"
                )

            # If the gemma-family model has no extra_params block at
            # all, seed the article-recommended sampling. Skip when the
            # user has set their own — their choice wins.
            if "gemma" in model_name and not model.get("extra_params"):
                model["extra_params"] = {
                    "top_k": 40,
                    "top_p": 0.95,
                    "repeat_penalty": 1.1,
                    "max_tokens": 8192,
                }
                fixed.append(
                    f"models.{label}.extra_params: seeded Gemma 4 anti-loop recipe"
                )

            # 2026-05-19: bump stale max_tokens=2048 → 8192. The article
            # recipe value was too tight for write_file calls with
            # nontrivial content (8K+ chars of JSON-encoded source) —
            # the response got truncated mid-string and the parser
            # rejected it. 8192 still bounds runaway generation but
            # leaves room for normal code writes.
            if "gemma" in model_name:
                ep = model.get("extra_params")
                if isinstance(ep, dict) and ep.get("max_tokens") == 2048:
                    ep["max_tokens"] = 8192
                    fixed.append(
                        f"models.{label}.extra_params.max_tokens: 2048 → 8192 "
                        f"(avoid write_file truncation)"
                    )

    if not added and not fixed:
        return

    try:
        with config_file.open("wb") as f:
            tomli_w.dump(data, f)
    except OSError as e:
        logger.warning("config migration: cannot write %s: %s", config_file, e)
        return

    changes = added + fixed
    rprint(
        f"[cyan]Drydock config migrated: {len(changes)} change(s) to "
        f"{config_file}[/]\n  "
        + "\n  ".join(changes)
    )
