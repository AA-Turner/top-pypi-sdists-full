"""The library groups and tiers live in ONE place and every palette entry carries them."""

from __future__ import annotations


import pytest

from matrx_graph import NodeRegistry, register_builtin_nodes
from matrx_graph.palette_groups import (
    GENERAL_GROUPS,
    PALETTE_GROUP_IDS,
    TIERS,
    configure_featured_steps,
    step_family,
    featured_steps,
    palette_group,
    step_tier,
)


@pytest.mark.parametrize(
    ("node_type", "category", "determinism", "group"),
    [
        ("plan.step", "plan", None, "plan"),
        ("admin.users.list", "data", None, "admin"),
        ("ai.agent.start", "agent", None, "agent"),
        ("ai.agent.produce_batch.collect", "agent", None, "agent"),
        ("ai.conversation.continue", "agent", None, "chat"),
        ("ai.conversation.tool_calls", "data", None, "chat"),
        ("ai.llm.chat", "llm", None, "llm"),
        ("ai.generate_image", "llm", None, "llm"),
        ("decision.yes_no", "llm", None, "decide"),
        ("decision.threshold", "llm", None, "decide"),
        ("ai.judge.resolve", "llm", None, "decide"),
        ("subgraph.call", "subgraph", None, "subgraph"),
        ("workflow.start_system_run", "io", None, "subgraph"),
        ("io.user_input", "io", None, "io"),
        ("notify.email", "io", None, "io"),
        ("records.changed", "io", None, "io"),
        ("control.branch", "control", None, "flow"),
        ("records.condition", "control", None, "flow"),
        ("brand.offerings.wait_crawl", "control", None, "features"),
        ("batch.wait_for_units", "control", None, "features"),
        ("records.wait_until_match", "control", None, "records"),
        ("data.record.upsert", "data", "side_effect", "records"),
        ("data.read_record", "data", "idempotent", "records"),
        ("records.query", "data", "idempotent", "records"),
        ("rag.search", "io", "idempotent", "records"),
        ("rag.library.upsert", "io", None, "records"),
        ("rag.chunk", "data", None, "records"),
        ("rag.parse", "data", None, "docs"),
        ("kg.entity.mentions", "io", None, "features"),
        ("files.upload", "tool", None, "records"),
        ("data.transform", "data", "pure", "data"),
        ("datetime.now", "data", "pure", "data"),
        ("data.filter", "data", "pure", "lists"),
        ("data.assert", "data", "pure", "checks"),
        ("text.regex_extract", "data", "pure", "text"),
        ("data.fetch", "data", "idempotent", "web"),
        ("web.brave.search", "io", None, "web"),
        ("http.get", "tool", None, "web"),
        ("files.read_text", "tool", None, "docs"),
        ("office.extract", "tool", None, "docs"),
        ("connection.call_tool", "tool", None, "tool"),
        ("google.sheet.read", "tool", None, "tool"),
        ("seo.keywords.tag", "tool", None, "features"),
        ("table.row.list", "data", None, "features"),
        ("note.create", "custom", None, "features"),
        ("brand_new.thing", "io", None, "features"),
        ("brand_new.engine", "pipe", None, "custom"),
    ],
)
def test_each_step_lands_on_its_shelf(
    node_type: str, category: str, determinism: str | None, group: str
) -> None:
    assert palette_group(node_type, category, determinism) == group


def test_tier_featured_named_feature() -> None:
    before = featured_steps()
    try:
        configure_featured_steps({"ai.agent.start", "table.row.list"})
        assert step_tier("ai.agent.start", "agent") == "featured"
        assert step_tier("table.row.list", "features") == "featured"
        assert step_tier("ai.agent.produce_batch", "agent") == "named"
        assert step_tier("seo.keywords.tag", "features") == "feature"
    finally:
        configure_featured_steps(before)


def test_a_features_step_names_its_family_and_no_other_does() -> None:
    assert step_family("seo.keywords.tag", "features", "tool") == "SEO"
    assert step_family("note.create", "features", "custom") == "Record steps (create, update, delete)"
    assert step_family("agent.create", "features", "custom") == "Record steps (create, update, delete)"
    assert step_family("ai.util.cost_summary", "features", "data") == "Spend"
    assert step_family("brand_new.thing", "features", "io") == "Brand new"
    assert step_family("ai.agent.start", "agent", "agent") is None


def test_a_family_prefix_at_least_as_long_as_the_shelf_prefix_wins() -> None:
    # "agent." (a family) never captures "ai.agent." (the Agents shelf); "rag." (a shelf)
    # and a longer exact rule both beat a shorter family.
    assert palette_group("ai.agent.start", "agent") == "agent"
    assert palette_group("agent.build.intake", "data") == "features"
    assert palette_group("rag.library.upsert", "io") == "records"


def test_every_palette_entry_carries_a_known_group_and_tier() -> None:
    entries = register_builtin_nodes(NodeRegistry()).palette()
    assert entries
    for entry in entries:
        assert entry["group"] in PALETTE_GROUP_IDS, entry["type"]
        assert entry["tier"] in TIERS, entry["type"]
        assert (entry["family"] is not None) == (entry["group"] == "features"), entry["type"]


def test_general_groups_are_library_groups() -> None:
    assert GENERAL_GROUPS <= PALETTE_GROUP_IDS
