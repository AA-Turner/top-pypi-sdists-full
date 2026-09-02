"""Mermaid parser.

Forgiving contract: never returns None, never raises. The source passes
through verbatim — the server has no mermaid engine, so blind rewrites risk
corrupting valid sources and any fix rules would drift from the client's
sanitize ladder. Only cheap metadata is extracted here:

- ``title`` from YAML frontmatter (``---\ntitle: X\n---``)
- ``diagram_type`` from the first significant line (header keyword)
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.mermaid import MermaidBlockData

# Header keyword -> normalized diagram type. Mirrored client-side in
# matrx-frontend components/mermaid/diagram-type.ts — keep in lockstep.
_HEADERS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^(flowchart|graph)\b"), "flowchart"),
    (re.compile(r"^sequenceDiagram\b"), "sequence"),
    (re.compile(r"^classDiagram"), "class"),
    (re.compile(r"^stateDiagram"), "state"),
    (re.compile(r"^erDiagram"), "er"),
    (re.compile(r"^journey\b"), "journey"),
    (re.compile(r"^gantt\b"), "gantt"),
    (re.compile(r"^pie\b"), "pie"),
    (re.compile(r"^mindmap\b"), "mindmap"),
    (re.compile(r"^timeline\b"), "timeline"),
    (re.compile(r"^quadrantChart\b"), "quadrant"),
    (re.compile(r"^gitGraph\b"), "git"),
    (re.compile(r"^C4(Context|Container|Component|Dynamic|Deployment)\b"), "c4"),
    (re.compile(r"^sankey(-beta)?\b"), "sankey"),
    (re.compile(r"^xychart(-beta)?\b"), "xychart"),
    (re.compile(r"^block(-beta)?\b"), "block"),
    (re.compile(r"^packet(-beta)?\b"), "packet"),
    (re.compile(r"^kanban\b"), "kanban"),
    (re.compile(r"^architecture(-beta)?\b"), "architecture"),
    (re.compile(r"^radar(-beta)?\b"), "radar"),
    (re.compile(r"^requirementDiagram\b"), "requirement"),
    (re.compile(r"^zenuml\b"), "zenuml"),
]

_TITLE_RE = re.compile(r"title:\s*(.+)")


def parse_mermaid(content: str) -> MermaidBlockData:
    """Extract best-effort metadata; the source always ships verbatim."""
    source = content
    title: str | None = None
    diagram_type = "unknown"
    try:
        lines = content.split("\n")
        i = 0
        # YAML frontmatter (--- / title: X / ---) — read title, skip the block
        if lines and lines[0].strip() == "---":
            for j in range(1, min(len(lines), 30)):
                stripped = lines[j].strip()
                if stripped == "---":
                    i = j + 1
                    break
                m = _TITLE_RE.match(stripped)
                if m:
                    title = m.group(1).strip().strip('"').strip("'")
        # First significant line (skip blanks and %% comments / %%{init}%% directives)
        for line in lines[i:]:
            stripped = line.strip()
            if not stripped or stripped.startswith("%%"):
                continue
            for pattern, dtype in _HEADERS:
                if pattern.match(stripped):
                    diagram_type = dtype
                    break
            break
    except Exception:
        pass  # metadata extraction is best-effort; source still ships
    return MermaidBlockData(
        title=title,
        diagram_type=diagram_type,
        source=source,
        is_valid=None,
        diagnostics=[],
    )
