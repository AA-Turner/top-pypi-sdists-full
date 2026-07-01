"""Request-shaping options: prefill messages, service tier, request overrides,
streaming callbacks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ─────────────────────────────────────────────────────────
# 2.15 — Prefill messages
# ─────────────────────────────────────────────────────────

# Anthropic models that REJECT a trailing-assistant prefill in some configs.
_NO_TRAILING_ASSISTANT_PREFILL = (
    "claude-sonnet-4", "claude-opus-4", "claude-sonnet-4.6", "claude-opus-4.6",
    "claude-sonnet-4.5", "claude-opus-4.5",
)


def validate_prefill(messages: List[Dict[str, Any]], model: str) -> None:
    if not messages:
        return
    last = messages[-1]
    if last.get("role") != "assistant":
        return
    m = (model or "").lower()
    for bad in _NO_TRAILING_ASSISTANT_PREFILL:
        if bad in m:
            raise ValueError(
                f"prefill_messages cannot end with an assistant turn for {model}"
            )


def apply_prefill(messages: List[Dict[str, Any]], prefill: List[Dict[str, Any]] | None, model: str) -> List[Dict[str, Any]]:
    if not prefill:
        return messages
    validate_prefill(prefill, model)
    return list(prefill) + list(messages)


# ─────────────────────────────────────────────────────────
# 2.16 — Service tier
# ─────────────────────────────────────────────────────────

_VALID_TIERS = {"auto", "default", "priority", "flex", "scale"}


def normalize_service_tier(tier: str | None) -> str | None:
    if not tier:
        return None
    t = tier.strip().lower()
    if t in _VALID_TIERS:
        return t
    return None


# ─────────────────────────────────────────────────────────
# 2.17 — Request overrides
# ─────────────────────────────────────────────────────────

def merge_request_overrides(base: Dict[str, Any], overrides: Dict[str, Any] | None) -> Dict[str, Any]:
    """Deep-merge overrides into the base request kwargs."""
    if not overrides:
        return base
    out = dict(base)
    for k, v in overrides.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = merge_request_overrides(out[k], v)
        else:
            out[k] = v
    return out


# ─────────────────────────────────────────────────────────
# 2.18 — Streaming callbacks
# ─────────────────────────────────────────────────────────

@dataclass
class StreamingCallbacks:
    stream_delta_callback: Optional[Callable[[str], None]] = None
    interim_assistant_callback: Optional[Callable[[str], None]] = None
    thinking_callback: Optional[Callable[[str], None]] = None
    status_callback: Optional[Callable[[str], None]] = None

    def emit_delta(self, delta: str) -> None:
        if self.stream_delta_callback and delta:
            try:
                self.stream_delta_callback(delta)
            except Exception:  # noqa: BLE001
                pass

    def emit_interim(self, text: str) -> None:
        if self.interim_assistant_callback and text:
            try:
                self.interim_assistant_callback(text)
            except Exception:  # noqa: BLE001
                pass

    def emit_thinking(self, text: str) -> None:
        if self.thinking_callback and text:
            try:
                self.thinking_callback(text)
            except Exception:  # noqa: BLE001
                pass

    def emit_status(self, status: str) -> None:
        if self.status_callback and status:
            try:
                self.status_callback(status)
            except Exception:  # noqa: BLE001
                pass


__all__ = [
    "validate_prefill",
    "apply_prefill",
    "normalize_service_tier",
    "merge_request_overrides",
    "StreamingCallbacks",
]
