"""Tighter ReAct loop primitives (B6).

The original engine generates a full multi-step plan in one model call,
then executes every step. When step 3 fails, the agent often plows
forward with stale plan, or replans from zero. A tighter ReAct loop
emits ONE action per turn, observes its output, then re-plans the next
step with the new evidence in context. Same total work, more recovery
points, better error handling.

This module provides the minimal pieces the engine needs to opt in:

  - `first_tool_action(response)` — extract only the FIRST tool action.
  - `ReActConfig` — feature flag plumbed through the engine.
  - `bound_actions(actions, cfg)` — gate that returns either all actions
    (legacy mode) or just the first (ReAct mode). The engine can drop
    this in as a one-line addition to its existing extractor pipeline.

The engine wiring (calling bound_actions on the extracted action list)
is intentionally out of scope here — that integration belongs in the
engine refactor, and this module provides the seam.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["ReActConfig", "bound_actions", "first_tool_action"]


# Same shape as main.py's extractors: optional bullet prefix, then KEYWORD:
_ACTION_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(READ|SEARCH|RUN|FILE):\s*(\S.*)$",
    re.MULTILINE,
)


@dataclass
class ReActConfig:
    """Opt-in ReAct discipline.

    Default off — keeps the current engine behavior. Flip
    `one_tool_per_turn = True` to bound each turn to a single tool call
    so the engine observes its output before planning the next step.
    """

    one_tool_per_turn: bool = False


def first_tool_action(response: str) -> tuple[str, str] | None:
    """Return the FIRST tool action in a model response, or None.

    Matches the same protocol as `_extract_tool_commands` in main.py
    (READ/SEARCH/RUN/FILE at start of line, optional list bullet) but
    only returns the first hit. FILE: blocks are returned with the
    bare path; the engine reads the following code-fence to get content.
    """
    if not response:
        return None
    m = _ACTION_RE.search(response)
    if not m:
        return None
    return (m.group(1).upper(), m.group(2).strip())


def bound_actions(
    actions: list[tuple[str, str]],
    cfg: ReActConfig,
) -> list[tuple[str, str]]:
    """Gate the action list according to the ReAct config.

    Legacy mode (cfg.one_tool_per_turn=False): pass through unchanged.
    ReAct mode: return only the first action, letting the engine observe
    its output before re-prompting.
    """
    if not actions:
        return list(actions)
    if cfg.one_tool_per_turn:
        return [actions[0]]
    return list(actions)
