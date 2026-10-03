"""Per-tool budgets for what a tool definition costs a model on every run that carries it.

A tool's description and input schema are sent to the provider on EVERY turn of every run
that carries the tool, whether or not the model calls it. ``records`` cost ~7,200
Anthropic tokens per run before it went lean (2026-10-02, owner-approved). Anthropic's
own tool guidance is the reference: a short definition, details loaded on demand.

The budget is a TABLE so a tool is added by one line. Only tools in the table are held to
a number; :func:`definition_report` measures every other one so the next candidates are
visible without tightening anything on someone else's behalf.

ESTIMATE, CALIBRATED. Tokens are estimated offline from the provider JSON at
:data:`CHARS_PER_TOKEN` — 3.2, below every ratio measured with Anthropic's
``count_tokens`` on 2026-10-02 (3.45 to 3.80 across records, data, dataset, picklist,
skill, sql, user and web), so the estimate OVERSTATES and a tool that passes here passes
for real. The tool-use system prompt Anthropic adds once per request (~530 tokens) is not
any one tool's cost and is excluded.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any

#: tool name -> the most estimated tokens its provider definition may cost per run.
TOOL_TOKEN_BUDGETS: dict[str, int] = {
    "records": 1_500,
}

#: Conservative characters-per-token for provider tool JSON (see the module docstring).
CHARS_PER_TOKEN = 3.2


@dataclass(frozen=True)
class DefinitionSize:
    name: str
    chars: int
    tokens: int
    budget: int | None

    @property
    def over(self) -> bool:
        return self.budget is not None and self.tokens > self.budget

    def sentence(self) -> str:
        limit = f"budget {self.budget:,}" if self.budget is not None else "no budget"
        return f"{self.name}: ~{self.tokens:,} tokens ({self.chars:,} chars; {limit})"


def estimate_tokens(provider_definition: dict[str, Any]) -> tuple[int, int]:
    """``(chars, estimated tokens)`` of one provider-format tool definition."""
    chars = len(json.dumps(provider_definition, ensure_ascii=False))
    return chars, math.ceil(chars / CHARS_PER_TOKEN)


def measure(tool: Any) -> DefinitionSize:
    """Size of a :class:`~matrx_ai.tools.models.ToolDefinition` as Anthropic is sent it."""
    chars, tokens = estimate_tokens(tool.to_anthropic_format())
    return DefinitionSize(tool.name, chars, tokens, TOOL_TOKEN_BUDGETS.get(tool.name))


def over_budget(tools: list[Any]) -> list[str]:
    """One plain sentence per budgeted tool over its budget. Empty is green."""
    return [
        f"{size.sentence()} — over budget. Move wording into the tool's on-demand guide "
        "(a `guide`/help action or a skill) instead of the definition sent on every run."
        for size in (measure(t) for t in tools)
        if size.over
    ]


def definition_report(tools: list[Any]) -> list[DefinitionSize]:
    """Every tool's size, largest first — the report, never a gate."""
    return sorted((measure(t) for t in tools), key=lambda s: s.tokens, reverse=True)


__all__ = [
    "CHARS_PER_TOKEN",
    "DefinitionSize",
    "TOOL_TOKEN_BUDGETS",
    "definition_report",
    "estimate_tokens",
    "measure",
    "over_budget",
]
