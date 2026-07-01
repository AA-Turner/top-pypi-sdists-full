"""Tool-call guardrails and destructive command detection."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Set


# ─────────────────────────────────────────────────────────
# 2.7 — ToolCallGuardrailController
# ─────────────────────────────────────────────────────────

# Tools that are safe to call repeatedly with identical arguments.
_IDEMPOTENT_TOOLS: Set[str] = {
    "read_file", "search_files", "skill_view", "skills_list",
    "browser_snapshot", "vision_analyze", "fact_store",
    "memory", "session_search", "todo",
}


class GuardrailVerdict(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    HALT = "halt"


@dataclass
class ToolGuardrailDecision:
    verdict: GuardrailVerdict
    reason: str = ""
    suggestion: str = ""


@dataclass
class ToolCallGuardrailController:
    # v2.69 — raised per-turn cap from 50 → 200 so deep exploration tasks
    # ("analyze every file") complete instead of stalling. Identical-args
    # halt at 3 still catches genuine loops.
    max_identical_per_turn: int = 3
    max_total_per_turn: int = 200
    _seen: Dict[str, int] = field(default_factory=dict)
    _total: int = 0

    def reset_turn(self) -> None:
        self._seen.clear()
        self._total = 0

    @staticmethod
    def _hash(name: str, args: Dict[str, Any]) -> str:
        try:
            ser = json.dumps(args, sort_keys=True, default=str)
        except Exception:  # noqa: BLE001
            ser = str(args)
        h = hashlib.md5(f"{name}|{ser}".encode("utf-8", errors="replace")).hexdigest()  # noqa: S324
        return h

    def observe(self, name: str, args: Dict[str, Any]) -> ToolGuardrailDecision:
        self._total += 1
        if self._total > self.max_total_per_turn:
            return ToolGuardrailDecision(
                verdict=GuardrailVerdict.HALT,
                reason=f"exceeded {self.max_total_per_turn} tool calls in this turn",
                suggestion="finalize a response or split work into a subagent",
            )

        key = self._hash(name, args)
        count = self._seen.get(key, 0) + 1
        self._seen[key] = count
        if count > self.max_identical_per_turn:
            if name in _IDEMPOTENT_TOOLS:
                return ToolGuardrailDecision(
                    verdict=GuardrailVerdict.WARN,
                    reason=f"called {name} {count}× with identical args (idempotent — likely loop)",
                    suggestion="vary arguments or move on",
                )
            return ToolGuardrailDecision(
                verdict=GuardrailVerdict.HALT,
                reason=f"called {name} {count}× with identical args (loop guard)",
                suggestion="stop repeating; address the underlying issue",
            )
        return ToolGuardrailDecision(verdict=GuardrailVerdict.ALLOW)


# ─────────────────────────────────────────────────────────
# 2.8 — Destructive command detection
# ─────────────────────────────────────────────────────────

_DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*|--recursive)", re.IGNORECASE),
    re.compile(r"\brm\s+-[a-zA-Z]*f", re.IGNORECASE),
    re.compile(r"\brm\s+\S*[*?]"),                                   # globs
    re.compile(r"\brm\s+-rf?\s+/"),                                   # rm -rf /
    re.compile(r"\brmdir\s"),
    re.compile(r"\bgit\s+reset\s+--hard\b", re.IGNORECASE),
    re.compile(r"\bgit\s+clean\s+-[a-zA-Z]*[fdx]", re.IGNORECASE),
    re.compile(r"\bdd\s+if=", re.IGNORECASE),
    re.compile(r"\bshred\b", re.IGNORECASE),
    re.compile(r"\bsed\s+-i\b", re.IGNORECASE),
    re.compile(r"\btruncate\s+-s\b", re.IGNORECASE),
    re.compile(r"\bmkfs(\.\w+)?\b", re.IGNORECASE),
    re.compile(r"\bfdisk\b", re.IGNORECASE),
    re.compile(r":\(\)\s*\{.*:\|:.*\}"),                              # fork bomb
    re.compile(r"\bchmod\s+(-R\s+)?000\b"),
    re.compile(r"\bchown\s+(-R\s+)?root\b"),
    # Single > overwrite (not >>)
    re.compile(r"(?<![>&])>(?!>)\s*[~/]?[\w./-]+"),
]


@dataclass
class DestructiveCheck:
    is_destructive: bool
    matched: list[str]
    reason: str = ""


def is_destructive(command: str) -> DestructiveCheck:
    if not command or not isinstance(command, str):
        return DestructiveCheck(False, [])
    matches: list[str] = []
    for pat in _DESTRUCTIVE_PATTERNS:
        m = pat.search(command)
        if m:
            matches.append(m.group(0))
    if matches:
        return DestructiveCheck(True, matches, reason=f"matched destructive pattern(s): {matches}")
    return DestructiveCheck(False, [])


__all__ = [
    "GuardrailVerdict",
    "ToolGuardrailDecision",
    "ToolCallGuardrailController",
    "DestructiveCheck",
    "is_destructive",
]
