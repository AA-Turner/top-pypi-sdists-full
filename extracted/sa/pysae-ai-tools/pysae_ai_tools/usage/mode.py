"""Detect the Claude billing mode (team subscription vs API key) and, for API-key
mode, estimate the running cost of the current session from its transcript.

Claude Code's auth precedence: an ``ANTHROPIC_API_KEY`` / ``ANTHROPIC_AUTH_TOKEN``
in the environment overrides a subscription login, so its presence means the
session is billed per-token (treated here as permanent extra usage). Otherwise a
``claudeAiOauth`` block in the credentials means a subscription.
"""

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .client import CREDENTIALS_PATH
from .pricing import ModelPricing, cost_of_usage


class PlanMode(str, Enum):
    SUBSCRIPTION = "subscription"
    API_KEY = "api_key"
    UNKNOWN = "unknown"


def detect_mode() -> PlanMode:
    """Return how the current Claude Code session is billed."""
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
        if os.environ.get(var, "").strip():
            return PlanMode.API_KEY
    try:
        data = json.loads(CREDENTIALS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return PlanMode.UNKNOWN
    oauth = data.get("claudeAiOauth")
    if isinstance(oauth, dict) and oauth.get("accessToken"):
        return PlanMode.SUBSCRIPTION
    return PlanMode.UNKNOWN


@dataclass
class SessionCost:
    """Estimated cost of a session, with a per-model token breakdown for display."""

    total_usd: float
    by_model: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def top_model(self) -> str | None:
        if not self.by_model:
            return None
        return max(self.by_model, key=lambda m: self.by_model[m]["output"] + self.by_model[m]["input"])


def session_cost_from_transcript(transcript_path: str, table: dict[str, ModelPricing]) -> SessionCost | None:
    """Sum the cost of every assistant turn in a Claude Code transcript (JSONL).

    Returns None if the transcript is missing or unreadable.
    """
    path = Path(transcript_path)
    if not transcript_path or not path.exists():
        return None
    total = 0.0
    by_model: dict[str, dict[str, int]] = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message")
                if not isinstance(msg, dict) or msg.get("role") != "assistant":
                    continue
                usage = msg.get("usage")
                model = msg.get("model")
                if not isinstance(usage, dict) or not isinstance(model, str):
                    continue
                total += cost_of_usage(model, usage, table)
                agg = by_model.setdefault(model, {"input": 0, "output": 0})
                for key, field_name in (("input_tokens", "input"), ("output_tokens", "output")):
                    v = usage.get(key)
                    if isinstance(v, (int, float)):
                        agg[field_name] += int(v)
    except OSError:
        return None
    return SessionCost(total_usd=total, by_model=by_model)
