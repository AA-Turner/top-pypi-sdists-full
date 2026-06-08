"""Per-turn policy for engaging grammar-constrained sampling.

Decides whether to attach a `grammar` field to the LLM request, and which
grammar. Phase 2 MVP (2026-06-06):

  - tool_choice = specific function (forced)  → engage that tool's grammar
  - tool_choice = "auto" or None              → DO NOT engage (Phase 2.5)
  - tool_choice = "none"                      → DO NOT engage
  - env DRYDOCK_GRAMMAR_DISABLE=1             → DO NOT engage (kill switch)
  - tool class has no Pydantic args           → DO NOT engage

When grammar engages, the bare GBNF matches just the args JSON object.
We strip the OpenAI `tools` field from the request so the model's output
is the raw JSON object (not wrapped in <tool_call> markers). The caller
parses the JSON and constructs a synthetic tool_call to dispatch.

This is the "forced single-tool" code path. The "auto-mode union grammar"
work lives in policy_union.py (TBD).
"""

from __future__ import annotations

import logging
import os
from typing import Any


logger = logging.getLogger(__name__)


# Bump max_tokens when grammar engages — with constrained sampling the
# model emits structurally valid string chars indefinitely, so we need
# headroom to actually close the string.
GRAMMAR_MAX_TOKENS_FLOOR = 16000


def select_grammar(
    *,
    tool_choice: Any,
    tool_manager: Any,
) -> tuple[str | None, str | None]:
    """Return (grammar_gbnf, forced_tool_name) or (None, None).

    grammar_gbnf: GBNF string to pass to llama.cpp via the `grammar`
      request field. None when grammar should NOT engage.
    forced_tool_name: the tool name whose args this grammar constrains.
      Caller uses this to construct a synthetic tool_call from the raw
      JSON output. None when grammar isn't engaged.
    """
    if os.environ.get("DRYDOCK_GRAMMAR_DISABLE", "").strip() == "1":
        return None, None

    # Extract the forced tool name from tool_choice. OpenAI shape:
    #   {"type": "function", "function": {"name": "write_file"}}
    forced_name: str | None = None
    if isinstance(tool_choice, dict):
        fn = tool_choice.get("function")
        if isinstance(fn, dict):
            n = fn.get("name")
            if isinstance(n, str) and n:
                forced_name = n
    elif hasattr(tool_choice, "function") and tool_choice.function:
        n = getattr(tool_choice.function, "name", None)
        if isinstance(n, str) and n:
            forced_name = n

    if not forced_name:
        return None, None

    # Look up the tool's args class
    try:
        tool_cls = tool_manager.available_tools.get(forced_name)
    except Exception:
        tool_cls = None
    if tool_cls is None:
        logger.debug(
            "[GRAMMAR-POLICY] tool_choice forces %s but no class in registry",
            forced_name,
        )
        return None, None

    try:
        args_model, _ = tool_cls._get_tool_args_results()
    except Exception as e:
        logger.debug(
            "[GRAMMAR-POLICY] %s has no Pydantic args (%s) — skipping",
            forced_name, e,
        )
        return None, None

    # Tighten the schema: Pydantic `Field(default="")` markers in
    # drydock args models leak as non-required JSON-Schema fields, and
    # the grammar then lets the model emit empty paths / no-content
    # writes. Reuse the union-grammar tightener. See policy_union for
    # the heuristic.
    from drydock.core.llm.grammar.policy_union import _tighten_args_schema
    try:
        raw_schema = args_model.model_json_schema()
        tight_schema = _tighten_args_schema(raw_schema)
        from drydock.core.llm.grammar import json_schema_to_gbnf
        gbnf = json_schema_to_gbnf(tight_schema)
    except Exception as e:
        logger.warning(
            "[GRAMMAR-POLICY] failed to compile %s args to GBNF: %s",
            forced_name, e,
        )
        return None, None

    logger.info(
        "[GRAMMAR-POLICY] engaging %s GBNF (%d chars) for forced tool_choice",
        forced_name, len(gbnf),
    )
    return gbnf, forced_name


def apply_grammar(
    *,
    complete_kwargs: dict[str, Any],
    grammar_gbnf: str,
    forced_tool_name: str,
    extra_sampling: dict[str, Any] | None,
) -> dict[str, Any]:
    """Mutate complete_kwargs to engage grammar.

    - Sets extra_sampling['grammar'] = gbnf
    - Drops the `tools` field (model emits raw JSON, not OpenAI tool_call wrapper)
    - Drops `tool_choice` (no longer meaningful without tools)
    - Bumps max_tokens to at least GRAMMAR_MAX_TOKENS_FLOOR
    - Returns the new extra_sampling dict for caller to merge upstream

    The caller is responsible for:
      - Parsing the JSON output content
      - Constructing a synthetic LLMMessage with tool_calls=[{forced_tool_name: ...}]
        so the rest of the agent loop sees a normal tool_call.
    """
    merged = dict(extra_sampling) if extra_sampling else {}
    merged["grammar"] = grammar_gbnf
    complete_kwargs["extra_sampling"] = merged

    # Strip tools / tool_choice — grammar matches bare args JSON, not the
    # OpenAI tool_call envelope.
    complete_kwargs.pop("tools", None)
    complete_kwargs.pop("tool_choice", None)

    # Bump max_tokens floor — model can emit valid string chars forever
    # under grammar, so it needs room to actually close the string.
    current = complete_kwargs.get("max_tokens") or 0
    if current < GRAMMAR_MAX_TOKENS_FLOOR:
        complete_kwargs["max_tokens"] = GRAMMAR_MAX_TOKENS_FLOOR

    return merged
