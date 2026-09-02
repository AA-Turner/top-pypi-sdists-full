"""Kinds for the code-docs fetchers (KIND_TOOL_LEDGER, ``lead-w2d``):
``llms_txt_fetch`` and ``code_fetch_tree``.

``code_fetch_tree`` does NOT reuse the registered ``file_tree_result`` kind
(the ledger's generated reuse candidate): that kind is exactly
``{tree, file_count}`` — the ``admin.dev.filetree`` node's minimal display
artifact — while this tool also reports project_root/subdirectory scoping and
the per-extension file-type census. Binding it there would declare keys the
other producer never emits; a claim-time guess is a candidate, not a
conclusion. The ``tree`` field keeps that kind's law: it is a PRE-RENDERED
display artifact, never to be parsed.

PLACEHOLDER tier: envelopes fully captured; ``llms_txt_outline`` is a light
parse of a plain-text standard, not rich provider data.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind

_FAMILY = "code_docs"


@kind(
    "llms_txt_link",
    label="LLM-Docs Link",
    family=_FAMILY,
    example={"title": "Quickstart", "url": "https://example.com/docs/quickstart.md", "notes": None},
    maturity="placeholder",
)
class LlmsTxtLink(KindModel):
    """One markdown link inside an ``llms.txt`` section."""

    title: str = ""
    url: str = ""
    notes: str | None = None


@kind(
    "llms_txt_section",
    label="LLM-Docs Section",
    family=_FAMILY,
    example={"name": "Docs", "links": []},
    maturity="placeholder",
)
class LlmsTxtSection(KindModel):
    """One ``## Section`` block of an ``llms.txt`` file."""

    name: str = ""
    links: list[LlmsTxtLink] = []


@kind(
    "llms_txt_outline",
    label="LLM-Docs Outline",
    family=_FAMILY,
    example={"title": "Example Docs", "summary": "Docs for Example.", "sections": []},
    maturity="placeholder",
)
class LlmsTxtOutline(KindModel):
    """The light parse of an ``llms.txt``: H1 title, blockquote summary,
    ``##`` sections with their link lists."""

    title: str | None = None
    summary: str | None = None
    sections: list[LlmsTxtSection] = []


@kind(
    "llms_txt_document",
    label="LLM-Docs File",
    family=_FAMILY,
    example={
        "url": "https://example.com/llms.txt",
        "content": "# Example Docs\n> Docs for Example.\n## Docs\n- [Quickstart](https://example.com/q.md)",
        "chars_returned": 92,
        "total_chars": 92,
        "truncated": False,
        "note": None,
        "parsed": {"__kind": "llms_txt_outline", "title": "Example Docs", "sections": []},
    },
    maturity="placeholder",
)
class LlmsTxtDocument(KindModel):
    """``llms_txt_fetch`` — the fetched ``llms.txt``/``llms-full.txt`` body
    plus its parsed outline. ``note`` appears only when the body was capped
    (the cap keys are part of the shape)."""

    url: str = ""
    content: str = ""
    chars_returned: int = 0
    total_chars: int = 0
    truncated: bool = False
    note: str | None = None
    parsed: LlmsTxtOutline = LlmsTxtOutline()


@kind(
    "code_tree_result",
    label="Code Tree",
    family=_FAMILY,
    example={
        "project_root": "/repo",
        "subdirectory": "src",
        "files_included": 12,
        "directories": 3,
        "file_types": {".py": 12},
        "tree": "src/\n├── __init__.py\n└── main.py",
    },
    maturity="placeholder",
)
class CodeTreeResult(KindModel):
    """``code_fetch_tree`` — the tree-only project census. ``tree`` is a
    pre-rendered display artifact (never parse it; the structured census is
    the sibling fields)."""

    project_root: str = ""
    #: empty string when the whole project root was walked.
    subdirectory: str = ""
    files_included: int = 0
    directories: int = 0
    #: extension → file count.
    file_types: dict[str, int] = {}
    tree: str = ""
