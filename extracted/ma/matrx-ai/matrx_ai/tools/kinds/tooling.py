"""Kinds for the platform's own tool-management tool results.

Ledger rows: the 43 ``bundle:list_*`` listers (KIND_TOOL_LEDGER, agent
``claude-tools-01``); ``find_tools`` (catalog discovery, third-party services
lane L9): what an agent reads back after searching the Tools catalog by the job.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import BaseModel, Field


@kind(
    "tool_bundle_listing",
    disposition="record",
    label="Tool Bundle Listing",
    family="tooling",
    example={
        "bundle": "supabase",
        "tools_loaded": ["execute_sql", "list_tables"],
        "count": 2,
        "skipped_unresolved": [],
        "server_slug": "supabase",
    },
    # PLACEHOLDER — this captures the outer structure honestly and completely;
    # there is no richer shape being flattened away. One generic handler
    # (``implementations/bundle_lister.py``) serves all 43 ``bundle:list_*``
    # rows and returns exactly these five keys, so the whole family is ONE kind
    # rather than 43 near-duplicate slugs (NOMENCLATURE.md).
    #
    # ``tools_loaded`` and ``skipped_unresolved`` are canonical tool NAMES, not
    # tool objects: the lister's job is to swap the active toolset, and the
    # member definitions it resolved are already the registry's to describe. A
    # kind that nested full tool definitions here would be inventing data this
    # result does not carry.
    maturity="placeholder",
)
class ToolBundleListing(KindModel):
    """What a ``bundle:list_<name>`` lister returns after swapping the toolset."""

    bundle: str = ""
    tools_loaded: list[str] = []
    count: int = 0
    skipped_unresolved: list[str] = []
    #: Set only for MCP-auto-managed bundles; ``None`` for hand-curated ones.
    server_slug: str | None = None


class FoundTool(BaseModel):
    """One Tool the search found, with how to call it now."""

    job_key: str = Field(title="Tool key")
    display_name: str = Field(title="Tool")
    display_noun: str = Field(default="Lookup", title="Kind of Tool")
    state: str = Field(default="live", title="State")
    added: bool = Field(default=False, title="Added to the agent's tools")
    how_to_call: str = Field(default="", title="How to call it")
    price_points: int | None = Field(default=None, title="Points a call")
    doc: str = Field(default="", title="What it does, inputs, returns, traps, price")


class FoundLibrary(BaseModel):
    """A Tool library (a skill paired with a bundle of similar Tools) that holds Tools the search found."""

    key: str = Field(title="Library key")
    label: str = Field(title="Library")
    description: str = Field(default="", title="What it is for")
    skill_id: str = Field(default="", title="Skill to attach")
    lister: str = Field(default="", title="Tool that opens the library")
    tools: list[str] = Field(default_factory=list, title="Tools in the library")
    matched: list[str] = Field(default_factory=list, title="Found Tools it holds")


@kind(
    "found_tools",
    disposition="record",
    label="Found Tools",
    family="tooling",
    example={
        "query": "domain authority of a bakery's website",
        "verdict": "strong",
        "tools": [
            {
                "job_key": "seo_domain_authority",
                "display_name": "Domain Authority",
                "display_noun": "Lookup",
                "state": "live",
                "added": True,
                "how_to_call": "Call seo_domain_authority directly; it is now in your tools.",
                "price_points": 134,
                "doc": "Domain Authority (seo_domain_authority) — Domain Authority (0-100) for one website ...",
            }
        ],
        "added": ["seo_domain_authority"],
        "note": "If an added Tool is not in your tool list on your next step, call use_tool with its job_key and inputs.",
    },
)
class FoundTools(KindModel):
    """The Tools a catalog search found for an agent, best first."""

    query: str = Field(default="", title="Searched for")
    verdict: str = Field(default="none", title="Match")
    tools: list[FoundTool] = Field(default_factory=list, title="Tools")
    added: list[str] = Field(default_factory=list, title="Added to the agent's tools")
    libraries: list[FoundLibrary] = Field(default_factory=list, title="Libraries that hold these Tools")
    note: str = Field(default="", title="Note")
