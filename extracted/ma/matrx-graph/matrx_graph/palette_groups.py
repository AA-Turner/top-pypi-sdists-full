"""The step library's groups and tiers — ONE home, read by every surface.

Every palette entry (``NodeSpec.to_palette_descriptor``) carries ``group`` (the library
shelf a builder finds it on) and ``tier`` (how prominently an authoring agent is told
about it). Studio's library, the Conductor's step guide and catalog search all read
these two fields; none re-derives them.

``tier``:

- ``featured`` — an authoring agent is given its contract up front.
- ``named``    — an authoring agent is told it exists, by name, under its group.
- ``feature``  — one feature's own step; found by search, only its family is named.

The host hands in the featured list (``configure_featured_steps``). It is deliberately WIDE:
an agent that does not know a step exists bends the few it knows, and nothing reports what
it missed. It is trimmed only from measured builds (common-docs/systems/workflows/projects/conductor-token-cost/PLAN.md, Fix A).
"""

from __future__ import annotations

from typing import Final

#: Library groups in library order: (id, label). The Studio pairs each id with its icon
#: and color; the label here is the one an agent reads. A test holds the two in step.
#: The owner's layout of 2026-11-01 (conductor-token-cost/VISION.md): shelves by what a
#: builder wants to do, one feature's own steps folded into Features by family.
PALETTE_GROUPS: Final[tuple[tuple[str, str], ...]] = (
    ("plan", "Plan"),
    ("notes", "Notes & visuals"),
    ("agent", "Agents"),
    ("chat", "Chat"),
    ("llm", "Direct AI"),
    ("decide", "AI decisions"),
    ("subgraph", "Workflows"),
    ("io", "Start and finish"),
    ("flow", "Flow"),
    ("records", "Your data"),
    ("data", "Reshape"),
    ("lists", "Lists"),
    ("checks", "Checks"),
    ("text", "Text"),
    ("web", "Web"),
    ("docs", "Documents"),
    ("tool", "Connections"),
    ("features", "Features"),
    ("admin", "Admin"),
    ("custom", "Custom"),
)

PALETTE_GROUP_IDS: Final[frozenset[str]] = frozenset(g for g, _ in PALETTE_GROUPS)

#: Exact step types placed by hand, ahead of every prefix rule. A whole family of general
#: steps goes in ``_PREFIXES``; this list is only for the one-off step whose prefix misleads.
_EXACT: Final[dict[str, str]] = {
    # AI decisions: a judgment that routes or picks — threshold included (owner's layout).
    "ai.decision": "decide",
    "ai.judge.resolve": "decide",
    # Workflows.
    "workflow.start_system_run": "subgraph",
    # Start and finish.
    "records.changed": "io",
    "platform.assists.offer": "io",
    "realtime.room.publish": "io",
    "feedback.submit": "io",
    "log.record": "io",
    # Flow.
    "records.condition": "flow",
    # Your data: records, the knowledge base, files.
    "platform.items.find": "records",
    "settings.read": "records",
    "files.upload": "records",
    "files.adopt_object": "records",
    "assets.upload": "records",
    "sources.land": "records",
    # Reshape and Text.
    "ai.util.parse_llm_json": "data",
    "pipe.step": "data",
    "geo.places.find": "text",
    # Web: "Get data" is a paid import of a site's records, not a read.
    "data.fetch": "web",
    "ai.search.brave": "web",
    "ai.scrape.web": "web",
    "ai.util.extract_search_urls": "web",
    "ai.util.format_scraped_content": "web",
    "search.decide": "web",
    "media.stock_image.search": "web",
    # Documents.
    "files.read_text": "docs",
    "files.analyze": "docs",
    "files.read_bytes_b64": "docs",
    "files.download": "docs",
    "rag.parse": "docs",
    # Features whose prefix would otherwise place them on a general shelf.
    "ai.util.cost_summary": "features",
}

#: Prefix rules, longest match wins; a family prefix sends a step to Features.
_PREFIXES: Final[dict[str, str]] = {
    "ai.agent.": "agent",
    "ai.mandate.": "agent",
    "ai.conversation.": "chat",
    "decision.": "decide",
    "subgraph.": "subgraph",
    "io.": "io",
    "output.": "io",
    "notify.": "io",
    "control.": "flow",
    "flow.": "flow",
    "data.record.": "records",
    "data.read_record": "records",
    "data.function.": "records",
    "data.table.": "records",
    "data.items_into_tables": "records",
    "data.mapped_sync": "records",
    "data.notion_import": "records",
    "records.": "records",
    "association.": "records",
    "rag.": "records",
    "math.": "data",
    "web.": "web",
    "scraper.": "web",
    "http.": "web",
    "cloud_browser.": "web",
    "page_extraction.": "web",
    "factcheck.": "web",
    "weather.": "web",
    "docproc.": "docs",
    "office.": "docs",
    "image.": "docs",
    "code.": "docs",
    "tool.": "tool",
    "tools.": "tool",
    "connection.": "tool",
    "google.": "tool",
}

#: Engine categories that keep their own shelf when no rule placed the step.
_CATEGORY_GROUPS: Final = {"llm": "llm", "agent": "agent", "subgraph": "subgraph", "control": "flow"}

_DATA_CORE_PREFIXES: Final = ("data.", "datetime.", "crypto.")

#: Data steps that work a whole list (many items in, a list or numbers out).
_LIST_TYPES: Final = frozenset(
    {
        "data.map_template",
        "data.filter",
        "data.flatten",
        "data.join",
        "data.group",
        "data.dedupe",
        "data.sort",
        "data.limit",
        "data.choose",
        "data.score",
        "data.shuffle",
        "data.batch",
        "data.apportion",
        "data.aggregate",
    }
)

#: Data steps that check, judge or stop the run.
_CHECK_TYPES: Final = frozenset(
    {"data.assert", "data.criteria_gate", "data.check_items", "data.rules"}
)


def _longest_prefix(node_type: str, prefixes: dict[str, str]) -> str:
    best = ""
    for prefix in prefixes:
        if node_type.startswith(prefix) and len(prefix) > len(best):
            best = prefix
    return best


def palette_group(node_type: str, category: str, determinism: str | None = None) -> str:
    """The library group a step type sits in."""
    if node_type.startswith("admin."):
        return "admin"
    if category == "plan":
        return "plan"
    if category == "info" or node_type.startswith("info."):
        return "notes"
    if node_type in _EXACT:
        return _EXACT[node_type]
    shelf = _longest_prefix(node_type, _PREFIXES)
    family = _longest_prefix(node_type, _FAMILIES)
    if family and len(family) >= len(shelf):
        return "features"
    if shelf:
        return _PREFIXES[shelf]
    if node_type.startswith("text."):
        return "text"
    if node_type.startswith(_DATA_CORE_PREFIXES):
        if node_type in _LIST_TYPES:
            return "lists"
        if node_type in _CHECK_TYPES:
            return "checks"
        return "data"
    if category in _CATEGORY_GROUPS:
        return _CATEGORY_GROUPS[category]
    if category == "custom" and node_type.rsplit(".", 1)[-1] in _RECORD_VERBS:
        return "features"
    # Every other host or package step is one feature's own step.
    return "features" if category in {"data", "tool", "io", "custom"} else "custom"


#: Feature families, by step-type prefix, as the guide and the library name them.
_FAMILIES: Final[dict[str, str]] = {
    "seo.": "SEO",
    "brand.": "Brand",
    "news.": "News and PR",
    "pr.": "News and PR",
    "coverage.": "News and PR",
    "content_plan.": "Content plan",
    "social.": "Social",
    "media.": "Media and podcasts",
    "podcast.": "Media and podcasts",
    "meet.": "Meet",
    "agent.": "Agent building and testing",
    "agents.": "Agent building and testing",
    "agent_test.": "Agent building and testing",
    "agent_debrief.": "Agent building and testing",
    "mandate.": "Agent building and testing",
    "masterwork.": "Masterwork",
    "table.": "Tables",
    "cerbo.": "Health",
    "lulu.": "Printing",
    "esign.": "E-signatures",
    "org.": "Organization",
    "portal.": "Organization",
    "kg.": "Knowledge map",
    "knowledge.": "Knowledge map",
    "knowledge_buckets.": "Knowledge map",
    "crm.": "CRM",
    "batch.": "Batch work",
    "growth_loop.": "Growth loop",
    "product_capture.": "Product capture",
    "runtime.": "Spend",
    "speech.": "Spend",
    "content_ir.": "Shapes",
    "research.": "Research",
}

#: Step types whose family is not their prefix's.
_EXACT_FAMILIES: Final[dict[str, str]] = {"ai.util.cost_summary": "Spend"}

#: The last word of a per-record step (``note.create``, ``task.create_tree``).
_RECORD_VERBS: Final = frozenset({"create", "update", "delete", "create_tree", "find_or_create"})
_RECORD_FAMILY: Final = "Record steps (create, update, delete)"


def step_family(node_type: str, group: str, category: str | None = None) -> str | None:
    """The feature family a Features step folds under; None on every other shelf."""
    if group != "features":
        return None
    if node_type in _EXACT_FAMILIES:
        return _EXACT_FAMILIES[node_type]
    if category == "custom" and node_type.rsplit(".", 1)[-1] in _RECORD_VERBS:
        return _RECORD_FAMILY
    prefix = _longest_prefix(node_type, _FAMILIES)
    if prefix:
        return _FAMILIES[prefix]
    # A family name is curated; this fallback only keeps a new prefix from going unnamed
    # until it is added to ``_FAMILIES``.
    head = node_type.split(".", 1)[0].replace("_", " ")
    return head[:1].upper() + head[1:]


#: Groups whose steps are general building blocks: every one is at least NAMED to an
#: authoring agent. Steps in other groups belong to one feature and are found by search.
GENERAL_GROUPS: Final[frozenset[str]] = frozenset(
    {
        "notes", "agent", "chat", "llm", "decide", "subgraph", "io", "flow", "records",
        "data", "lists", "checks", "text", "web", "docs", "tool",
    }
)

#: Featured step types, handed in by the host (``configure_featured_steps``): which steps
#: an authoring agent is given up front is the host's curation, never this package's.
_featured_steps: frozenset[str] = frozenset()


def configure_featured_steps(node_types: frozenset[str] | set[str]) -> None:
    """Set the step types the host features to authoring agents."""
    global _featured_steps
    _featured_steps = frozenset(node_types)


def featured_steps() -> frozenset[str]:
    return _featured_steps


TIERS: Final[tuple[str, ...]] = ("featured", "named", "feature")


def step_tier(node_type: str, group: str) -> str:
    """How prominently an authoring agent is told about a step type."""
    if node_type in _featured_steps:
        return "featured"
    if group in GENERAL_GROUPS:
        return "named"
    return "feature"


__all__ = [
    "configure_featured_steps",
    "featured_steps",
    "GENERAL_GROUPS",
    "PALETTE_GROUPS",
    "PALETTE_GROUP_IDS",
    "TIERS",
    "palette_group",
    "step_family",
    "step_tier",
]
