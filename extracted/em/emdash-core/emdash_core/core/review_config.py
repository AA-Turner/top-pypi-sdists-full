"""Configuration loader for PR review settings."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class ReviewConfig(BaseModel):
    """Configuration for PR review command."""

    max_files: int = Field(default=50, ge=1, le=500)
    max_tokens: int = Field(default=50000, ge=1000, le=200000)


def _find_config_path() -> Optional[Path]:
    """Find the review config file path."""
    env_path = os.getenv("EMDASH_CONFIG_PATH")
    if env_path:
        return Path(env_path)

    cwd = Path.cwd()
    candidates = [
        cwd / "emdash.config.json",
        cwd / ".emdash-rules" / "config.json",
    ]
    for path in candidates:
        if path.is_file():
            return path

    return None


def load_review_config() -> ReviewConfig:
    """Load review configuration from file if present."""
    path = _find_config_path()
    if not path or not path.is_file():
        return ReviewConfig()

    try:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (json.JSONDecodeError, OSError):
        return ReviewConfig()

    review = raw.get("review", {}) if isinstance(raw, dict) else {}
    if not isinstance(review, dict):
        return ReviewConfig()

    return ReviewConfig(
        max_files=review.get("max_files", 50),
        max_tokens=review.get("max_tokens", 50000),
    )
