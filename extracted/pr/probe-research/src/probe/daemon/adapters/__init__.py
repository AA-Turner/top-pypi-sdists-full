"""Harness adapters. `for_source` is the ONE place a harness name is looked up."""

from __future__ import annotations

from probe.daemon.adapters.base import Adapter, Capabilities
from probe.daemon.adapters.claude_code import ClaudeCode
from probe.daemon.adapters.codex import Codex
from probe.daemon.adapters.pi import Pi

_ADAPTERS: dict[str, type[Adapter]] = {"claude_code": ClaudeCode, "codex": Codex, "pi": Pi}
#: Spellings the capture side uses for the same harnesses.
_ALIASES = {"claude": "claude_code", "claude-code": "claude_code", "cc": "claude_code"}


def for_source(source: str | None) -> Adapter:
    key = _ALIASES.get((source or "").strip().lower(), (source or "claude_code").strip().lower())
    cls = _ADAPTERS.get(key)
    if cls is None:
        raise LookupError(f"no daemon adapter for harness {source!r}: daemon mode is unavailable there")
    return cls()


def known() -> tuple[str, ...]:
    return tuple(_ADAPTERS)


__all__ = ["Adapter", "Capabilities", "for_source", "known"]
