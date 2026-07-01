"""Platform-aware system prompt fragments + safe stdio installer."""
from __future__ import annotations

import io
import sys
from typing import Optional


# ─────────────────────────────────────────────────────────
# 2.19 — Platform-aware system prompts
# ─────────────────────────────────────────────────────────

PLATFORM_PROMPT_FRAGMENTS = {
    "cli": (
        "You are on a CLI surface. You may use full markdown including tables, "
        "ANSI-friendly formatting, code fences, and rich layouts. Long output is fine."
    ),
    "telegram": (
        "You are on Telegram. Standard markdown is auto-converted: **bold**, *italic*, "
        "~~strikethrough~~, ||spoiler||, `code`, ```blocks```, [links](url), ## headers. "
        "Telegram has NO table syntax — prefer bullet lists or `key: value` pairs over pipe tables. "
        "Keep messages concise; long replies are split."
    ),
    "discord": (
        "You are on Discord. Use markdown: **bold**, *italic*, ```fenced code blocks``` "
        "(with language hint), and headers. Tables render as monospaced code blocks. "
        "Messages cap at 2000 characters per send."
    ),
    "web": (
        "You are on a web chat surface with full HTML/markdown support. Tables, images, "
        "and rich formatting all work."
    ),
    "sms": (
        "You are on SMS. Plain text only. No markdown. No emoji. Be concise — assume "
        "160-character segments."
    ),
}


def platform_prompt(platform: Optional[str]) -> str:
    if not platform:
        return ""
    return PLATFORM_PROMPT_FRAGMENTS.get(platform.strip().lower(), "")


def detect_platform_from_session(session_meta: dict | None) -> Optional[str]:
    """Best-effort platform detection from gateway session metadata."""
    if not session_meta:
        return None
    for key in ("platform", "source", "channel"):
        v = session_meta.get(key)
        if isinstance(v, str) and v.strip():
            v = v.strip().lower()
            if v in PLATFORM_PROMPT_FRAGMENTS:
                return v
    return None


# ─────────────────────────────────────────────────────────
# 2.20 — Safe stdio installation
# ─────────────────────────────────────────────────────────

_INSTALLED = False


def install_safe_stdio() -> bool:
    """Force UTF-8 on stdin/stdout/stderr. No-op on POSIX where already UTF-8.

    Must be called before any other I/O.
    Returns True if anything was reconfigured.
    """
    global _INSTALLED
    if _INSTALLED:
        return False
    _INSTALLED = True

    changed = False
    for stream_name in ("stdout", "stderr", "stdin"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            enc = (getattr(stream, "encoding", "") or "").lower()
        except Exception:  # noqa: BLE001
            enc = ""
        if enc.startswith("utf"):
            continue
        try:
            # Python 3.7+ TextIOWrapper.reconfigure
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
            changed = True
        except (AttributeError, io.UnsupportedOperation, ValueError):
            try:
                buf = getattr(stream, "buffer", None)
                if buf is not None:
                    new_stream = io.TextIOWrapper(buf, encoding="utf-8", errors="replace", line_buffering=True)
                    setattr(sys, stream_name, new_stream)
                    changed = True
            except Exception:  # noqa: BLE001
                pass
    return changed


__all__ = [
    "PLATFORM_PROMPT_FRAGMENTS",
    "platform_prompt",
    "detect_platform_from_session",
    "install_safe_stdio",
]
