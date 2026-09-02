"""Parser for the ``schema_proposal`` JSON block.

What the "JSON Schema Generator" agent emits: ``{name, schema, strict?}``.
Recognized so a surface can offer "Apply to an agent" (writes
``agent.definition.output_schema``) instead of showing raw JSON.
"""

from __future__ import annotations

import json

from matrx_ai.processing.blocks.models.schema_proposal import SchemaProposalBlockData
from matrx_ai.processing.blocks.parsers._llm_json import loads_block_json


def parse_schema_proposal(content: str) -> SchemaProposalBlockData | None:
    try:
        parsed = loads_block_json(content)
    except (json.JSONDecodeError, ValueError):
        return None

    if not isinstance(parsed, dict):
        return None
    name = parsed.get("name")
    schema = parsed.get("schema")
    if not isinstance(name, str) or not isinstance(schema, dict):
        return None

    strict = parsed.get("strict")
    return SchemaProposalBlockData(
        name=name,
        json_schema=schema,
        strict=strict if isinstance(strict, bool) else None,
    )
