"""Union grammar for tool_choice='auto' — Phase 2.5.

When the model picks WHICH tool to call (auto-mode), we want the
generated tool_call to be structurally valid no matter which branch
the model takes. The grammar must:

  1. Allow ANY of N tools to be selected
  2. Couple the chosen name with that tool's specific args schema
     (the model can't pick name=write_file but emit args matching
     read_file's schema — the grammar branches enforce the pairing)
  3. Match the JSON envelope shape the rest of drydock expects

Output shape (matches what the JSON-parser-side wrapper in
agent_loop._chat() expects):

  {"name": "<tool_name>", "arguments": <tool_specific_args>}

The dispatcher wrapper unpacks `name` into the synthetic ToolCall and
passes `arguments` (re-stringified) as the function arguments.

When grammar is engaged in auto-mode, the request strips the OpenAI
`tools` field entirely. Drydock's existing tool-call parser sees the
synthetic envelope and dispatches normally.

NOTE on llama.cpp grammar quirks: the converter sometimes generates
rules that duplicate common types (string, char, space, boolean). The
union builder deduplicates these so the grammar compiles cleanly.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Any

from drydock.core.llm.grammar._llamacpp_converter import SchemaConverter

logger = logging.getLogger(__name__)


# Reserved GBNF rule names that are common across tools — only emit once.
_COMMON_RULES = ("space", "string", "char", "boolean", "null", "number",
                 "integer", "value")


def _tighten_args_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Force fields with vacuous defaults to be required in the grammar.

    Pydantic args models in drydock use `Field(default="")` so the
    AUTO-INFER recovery path can rewrite partial calls. But that makes
    the JSON Schema mark those fields as optional, and the grammar then
    accepts `{}` as valid args — the model under grammar emits empty
    paths and garbage content because the schema permits it.
    Concretely: WriteFileArgs.path defaults to "" and the model under
    grammar emitted 18 writes with `path=None` and identical 428-char
    `out0 = out0\\nout1 = out1\\n...` gibberish (2026-06-06 v2.9.87 batch,
    circuit-fibsqrt trial).

    Heuristic: a field with default value `""`, `[]`, `{}`, or `None`
    (when the type isn't nullable) is "vacuous" — the default never
    represents a real intent, it's a placeholder for the recovery
    machinery. Strip the default from such fields and add them to
    `required`. Boolean / numeric / non-empty-string defaults are
    legitimate optionals and left alone.

    Returns a NEW dict; does not mutate the input.
    """
    if not isinstance(schema, dict):
        return schema
    out = dict(schema)
    props = dict(out.get("properties") or {})
    if not props:
        return out
    required = list(out.get("required") or [])
    for name, spec in list(props.items()):
        if not isinstance(spec, dict):
            continue
        if "default" not in spec:
            continue
        default = spec["default"]
        is_vacuous = False
        if default == "" or default == [] or default == {}:
            is_vacuous = True
        elif default is None:
            # `default=None` is fine when the type is nullable, e.g.
            # ReadFileArgs.limit (type: int|null). It's a problem only
            # for fields whose schema type doesn't allow null — those
            # are buggy-optionals. Detect via anyOf branches.
            any_of = spec.get("anyOf") or []
            type_allows_null = any(
                isinstance(b, dict) and b.get("type") == "null"
                for b in any_of
            ) or spec.get("type") == "null"
            if not type_allows_null:
                is_vacuous = True
        if is_vacuous:
            new_spec = {k: v for k, v in spec.items() if k != "default"}
            props[name] = new_spec
            if name not in required:
                required.append(name)
    out["properties"] = props
    if required:
        out["required"] = required
    return out


def build_union_gbnf(
    tool_specs: list[tuple[str, type]],
) -> str | None:
    """Build a GBNF accepting `{"name": "tool_A", "arguments": <A_args>} |
                                  {"name": "tool_B", "arguments": <B_args>} | ...`.

    `tool_specs` is a list of (tool_name, args_pydantic_class) pairs.

    Implementation: assemble ONE composite JSON Schema with `oneOf`
    branches (one per tool), embedding each tool's args under the
    `arguments` property and pinning `name` to a const literal. Hand
    that to the upstream converter — it handles all rule deconfliction
    internally so we don't have to. Cleaner than per-tool rewriting.
    """
    if not tool_specs:
        return None

    one_of_branches = []
    for tool_name, args_model in tool_specs:
        try:
            args_schema = args_model.model_json_schema()
        except Exception as e:
            logger.debug("[UNION] %s schema err: %s — skipping", tool_name, e)
            continue
        args_schema = _tighten_args_schema(args_schema)
        one_of_branches.append({
            "type": "object",
            "properties": {
                "name": {"type": "string", "const": tool_name},
                "arguments": args_schema,
            },
            "required": ["name", "arguments"],
            "additionalProperties": False,
        })

    if not one_of_branches:
        return None

    composite_schema = {"oneOf": one_of_branches}

    try:
        conv = SchemaConverter(
            prop_order={},
            allow_fetch=False,
            dotall=False,
            raw_pattern=False,
        )
        conv.visit(composite_schema, "")
        return conv.format_grammar()
    except Exception as e:
        logger.warning("[UNION] composite-schema compile failed: %s", e)
        return None


def select_union_grammar(
    *,
    tool_choice: Any,
    available_tools: list[Any],
    tool_manager: Any,
) -> str | None:
    """If tool_choice is auto/None AND grammar isn't kill-switched, build
    a union grammar over the tools the model can pick from.

    Returns the GBNF string or None.
    """
    if os.environ.get("DRYDOCK_GRAMMAR_DISABLE", "").strip() == "1":
        return None
    # Union grammar is now OFF BY DEFAULT (2026-06-06, v2.9.98).
    # Reason: a 72-tool grammar union makes the model pick whichever
    # branch has the simplest argument schema and iterate through them
    # mechanically — `task` (`{task: str}`), `exit_plan_mode` (`{}`),
    # `notebook_edit`, `count`, etc. — instead of selecting the right
    # tool for the work. Multiple visible user-facing loops 2026-06-06.
    # Defense in depth: keep forced-single-tool grammar (policy.py)
    # active so that when drydock explicitly forces tool_choice=write_file
    # we still get JSON-validity guarantees. Auto-mode falls back to
    # the model's native tool-call decisions, which Gemma 4 handles
    # well via llama.cpp `--jinja`.
    # Re-enable by setting DRYDOCK_UNION_GRAMMAR_ENABLE=1.
    if os.environ.get("DRYDOCK_UNION_GRAMMAR_ENABLE", "").strip() != "1":
        return None
    if os.environ.get("DRYDOCK_UNION_GRAMMAR_DISABLE", "").strip() == "1":
        return None

    # Only engage for auto/None — forced single tool goes through select_grammar
    if tool_choice not in (None, "auto"):
        return None
    if not available_tools:
        return None

    # Build (name, args_class) pairs for every available tool that has
    # a Pydantic args model.
    specs: list[tuple[str, type]] = []
    for at in available_tools:
        # Extract the tool name from the OpenAI tool spec
        try:
            name = at.function.name  # AvailableTool object
        except AttributeError:
            try:
                name = at["function"]["name"]
            except Exception:
                continue
        if not isinstance(name, str):
            continue
        tool_cls = tool_manager.available_tools.get(name)
        if tool_cls is None:
            continue
        try:
            args_model, _ = tool_cls._get_tool_args_results()
        except Exception:
            continue
        specs.append((name, args_model))

    if not specs:
        return None

    gbnf = build_union_gbnf(specs)
    if gbnf:
        logger.info(
            "[UNION-GRAMMAR] built union grammar with %d branches "
            "(%d chars total)",
            len(specs), len(gbnf),
        )
    return gbnf
