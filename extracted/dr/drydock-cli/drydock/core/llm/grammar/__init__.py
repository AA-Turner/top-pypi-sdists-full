"""GBNF grammar generation for constrained tool-call generation.

Background (2026-06-06 PRD §5.3.5): the model's tool_call arguments are
JSON serialized token-by-token via freeform sampling. Q3 quantization noise
causes ~5-25% of long generations to produce structurally invalid JSON.
Engine-level constrained decoding (GBNF on llama.cpp) physically prevents
the model from emitting invalid JSON during sampling.

This module provides:
  - `pydantic_to_gbnf(model)`: compile a Pydantic BaseModel to a GBNF
    grammar string suitable for llama.cpp's `grammar` request field.
  - `tools_to_union_gbnf(tools)`: build a union grammar that lets the
    model pick one of N tool calls, each constrained to its schema.

The actual JSON-Schema → GBNF compiler is `_llamacpp_converter.py`, a
verbatim copy of llama.cpp's `examples/json_schema_to_grammar.py`
(Apache 2.0). Keep that file in sync with upstream when llama.cpp
ships grammar bug fixes.
"""

from __future__ import annotations

from typing import Any

from drydock.core.llm.grammar._llamacpp_converter import SchemaConverter


def pydantic_to_gbnf(model_cls: Any) -> str:
    """Compile a Pydantic BaseModel class to a GBNF grammar string.

    The grammar matches valid JSON objects conforming to the model's
    schema. Strings get the proper char-class that excludes unescaped
    control chars and requires valid backslash escapes — exactly the
    constraint that fixes the "missing closing quote" failure mode.
    """
    schema = model_cls.model_json_schema()
    conv = SchemaConverter(
        prop_order={},
        allow_fetch=False,
        dotall=False,
        raw_pattern=False,
    )
    conv.visit(schema, "")
    return conv.format_grammar()


def json_schema_to_gbnf(schema: dict[str, Any]) -> str:
    """Compile a JSON Schema dict directly to a GBNF grammar string."""
    conv = SchemaConverter(
        prop_order={},
        allow_fetch=False,
        dotall=False,
        raw_pattern=False,
    )
    conv.visit(schema, "")
    return conv.format_grammar()


__all__ = ["pydantic_to_gbnf", "json_schema_to_gbnf"]
