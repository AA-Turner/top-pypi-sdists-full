"""Mermaid block data model.

The raw mermaid text is the single source of truth. The server has no mermaid
engine, so it never validates or rewrites the source — the client (the only
place a mermaid renderer exists) owns validation and forgiving auto-fixes.
The server extracts cheap metadata only (title, diagram type).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_camel_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MermaidBlockData(BaseModel):
    """Parsed mermaid diagram metadata + verbatim source."""

    model_config = _camel_config

    title: str | None = None          # from YAML frontmatter `title:` if present
    diagram_type: str = "unknown"     # flowchart | sequence | class | state | er | ...
    source: str                       # verbatim mermaid text — NEVER modified server-side
    is_valid: bool | None = None      # None = server cannot validate (no engine)
    diagnostics: list[str] = []
