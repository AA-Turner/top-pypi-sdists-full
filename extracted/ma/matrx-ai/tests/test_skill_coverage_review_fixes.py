"""Generated-skill review fixes (chat-agent-skills lane F, 2026-11-19 review): every name is the
wire name the model sees; near-identical tools collapse into one family skill; descriptions are
whole "Use when …" sentences; no filler, no invented example, no pitfall that is false for the
tool; a skill is never more visible than its tool; nothing reads as a variable."""

from __future__ import annotations

import re

import pytest

from matrx_ai.config.wire_names import to_wire_name
from matrx_ai.skills.coverage import (
    BundleFacts,
    ShapeFacts,
    ToolFacts,
    build_bundle_skill,
    build_family_skill,
    build_shape_tools_skill,
    build_tool_skill,
    conditional_pitfalls,
    description_limit,
    find_families,
    params_of,
    trigger_description,
)

URL = {"type": "object", "required": ["url"], "properties": {"url": {"type": "string", "description": "Page address"}}}


def store_tool(store: str, i: int, **kw) -> ToolFacts:
    key = re.sub(r"\W+", "_", store.lower())
    return ToolFacts(
        id=f"s{i}", name=f"data_{key}_products", description="", parameters=URL, source_kind="catalog",
        display_name=f"{store} products", job_key=f"data_{key}_products", output_kind="data_records",
        summary=f"Product pages from {store} with price and images; use for price tracking.",
        tags=("data", "online stores"), price_points=5, **kw,
    )


STORES = [store_tool(f"Shop {chr(65 + i)}{chr(65 + i)}", i) for i in range(25)]


def connector_tool(svc: str, i: int) -> ToolFacts:
    slug = svc.lower().replace(" ", "-")
    return ToolFacts(
        id=f"c{i}", name=f"mcp.{slug}.search_{slug}", source_kind="mcp_discovered",
        description=f"Search across the {svc} knowledge base to find relevant guides. Use it for questions about {svc}.",
        parameters={"type": "object", "required": ["query"], "properties": {"query": {"type": "string"}}},
        mcp_server_slug=slug, mcp_server_name=svc, listers=(f"bundle:list_{slug}",),
    )


# -- 1. names are the wire names the model sees -------------------------------------------------

@pytest.mark.parametrize(
    "name, listers",
    [
        ("org_team_list", ()),                                          # native: unchanged
        ("mcp.fibery.get_automation", ("bundle:list_fibery",)),          # connector: dots
        ("bundle:list_new-relic", ()),                                   # lister: colon
        ("mcp.a-very-long-server-name-for-tests." + "x" * 60, ("bundle:list_a",)),  # past 64: digest
    ],
)
def test_every_tool_name_in_a_skill_is_its_wire_name(name, listers):
    t = ToolFacts(id="t", name=name, description="Fetches one automation by id.", parameters={}, source_kind="native", listers=listers)
    g = build_tool_skill(t)
    assert f"`{to_wire_name(name)}`" in g.body
    names = re.findall(r"`([^`\s]+)`", g.body)
    assert not [n for n in names if ":" in n or n.startswith("mcp.")], names
    for lister in listers:
        assert f"`{to_wire_name(lister)}`" in g.body


def test_bundle_and_shape_skills_name_wire_forms():
    m = connector_tool("Acme Docs", 1)
    b = build_bundle_skill(BundleFacts(id="b", name="acme-docs", description="Acme.", lister_id="l", lister_name="bundle:list_acme-docs", members=(m,), mcp_server_slug="acme-docs", mcp_server_name="Acme Docs"))
    assert "`bundle__list_acme-docs`" in b.body and f"`{to_wire_name(m.name)}`" in b.body
    assert "bundle:list" not in b.body and "`mcp." not in b.body


# -- 2. families -------------------------------------------------------------------------------

def test_tools_that_differ_only_by_their_store_become_one_family():
    fams = find_families(STORES, min_members=21)
    assert len(fams) == 1
    f = fams[0]
    assert f.label == "Product pages by store" and len(f.members) == 25
    g = build_family_skill(f)
    assert g.skill_id == "tools-family-product-pages-by-store"
    assert all(s.display_name.removesuffix(" products") in g.body for s in STORES)
    assert "`find_tools`" in g.body and "`use_tool`" in g.body and "job_key `data_shop_aa_products`" in g.body
    assert g.description.startswith("Use when you need product pages from one store")
    assert set(g.link["tool_definition_ids"]) == {s.id for s in STORES}


def test_a_small_cluster_keeps_its_own_skills():
    assert find_families(STORES[:20], min_members=21) == []


def test_different_inputs_never_join_a_family():
    odd = store_tool("Odd Shop", 99)
    odd = ToolFacts(**{**odd.__dict__, "parameters": {"type": "object", "required": ["url", "zip"], "properties": {"url": {"type": "string"}, "zip": {"type": "string"}}}})
    fams = find_families([*STORES, odd], min_members=21)
    assert "s99" not in {t.id for _, t in fams[0].members}


def test_connector_tools_form_a_family_got_through_each_lister():
    tools = [connector_tool(f"Svc{chr(65 + i)} Docs", i) for i in range(22)]
    fams = find_families(tools, min_members=21)
    assert len(fams) == 1 and fams[0].kind == "connector"
    g = build_family_skill(fams[0])
    assert "one service's knowledge base" in g.body
    assert "`bundle__list_svca-docs`" in g.body and "SvcA Docs" in g.body


def test_a_store_name_appears_only_in_its_own_or_its_familys_skill():
    """No shared sentence names a store: the shape skill over family members names the family."""
    fams = find_families(STORES, min_members=21)
    members = [ToolFacts(**{**t.__dict__, "family_skill": fams[0].skill_id, "family_label": fams[0].label}) for _, t in fams[0].members]
    s = build_shape_tools_skill(ShapeFacts(id="k", kind="data_records", label="Data records", description=None, producers=tuple(members)))
    assert not [t for t in STORES if t.display_name.removesuffix(" products") in s.body]
    assert fams[0].skill_id in s.body


# -- 3. descriptions ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "job, want",
    [
        ("Design and run experiments on prompts.", "Use when you need to design and run experiments"),
        ("User reviews for an Android app by country; use for product feedback.", "Use when you need user reviews for"),
        ("Put a form under a section.", "Use when you need to put a form"),
        ("Permanently delete a skill by name.", "Use when you need to permanently delete a skill"),
        ("Admins: keep each page's address word in a section.", "Use when you need to keep each page's"),
        ("Chrome downloads. list: 50 most recent (id, filename).", "Use when you need chrome downloads."),
        ("Run one news monitor now (queued run). -> {run_id, …}.", "Use when you need to run one news monitor now"),
    ],
)
def test_trigger_reads_as_a_sentence(job, want):
    d = trigger_description(job, fallback="x")
    assert d.startswith(want), d


def test_a_long_trigger_is_cut_at_a_clause_never_an_ellipsis():
    job = "List every calendar the person can open, in every organization they belong to, with " + "its name, kind, colour and owner, " * 8 + "sorted by name."
    d = trigger_description(job, fallback="Calendars")
    assert len(d) <= description_limit() and d.endswith(".") and "…" not in d
    assert d.count("(") == d.count(")")


# -- 4/5. no filler bullet, no invented example -------------------------------------------------

def test_no_filler_bullet_and_no_example_without_a_declared_one():
    t = ToolFacts(id="t", name="widget_text_patch", description="Patch a widget's text.", parameters={"type": "object", "required": ["q"], "properties": {"q": {"type": "string"}}}, source_kind="native")
    body = build_tool_skill(t).body
    assert "none of your other tools" not in body
    assert "## Example call" not in body and "<" not in body.split("## How to get it")[0].replace("`", "")


def test_a_declared_example_is_used_as_written():
    params = {"type": "object", "required": ["action"], "properties": {"action": {"type": "string", "examples": ["query"]}}}
    t = ToolFacts(id="t", name="sql_like", description="Read rows.", parameters=params, source_kind="native")
    assert '## Example call\n\n```json\n{"action": "query"}\n```' in build_tool_skill(t).body


# -- 6. pitfalls are true for the tool ------------------------------------------------------------

SQL_LIKE = (
    "Structured CRUD on the platform Postgres; never pass SQL text. Tables are schema-qualified.\n"
    "- update and delete need a non-empty match.\n"
    "- patch: str_replace on one text column of exactly one row. Use it instead of update for small edits to long text.\n"
    "Read-only here: platform-internal schemas."
)


def test_a_sentence_scoped_to_one_action_never_speaks_for_the_tool():
    body = build_tool_skill(ToolFacts(id="t", name="sql", description=SQL_LIKE, parameters={}, source_kind="native")).body
    assert "instead of update" not in body
    assert "Structured CRUD on the platform Postgres" in body


@pytest.mark.parametrize("flag", ["destructive", "paid", "admin_only", "required", "requires"])
def test_each_template_pitfall_appears_only_when_its_condition_holds(flag):
    sentences = {
        "destructive": "It changes or deletes data",
        "paid": "It spends the person's points",
        "admin_only": "Only platform admins can run it.",
        "required": "Required: `q`.",
        "requires": "It runs only when",
    }
    base = ToolFacts(id="t", name="x", description="Does x.", parameters={}, source_kind="native")
    on = {
        "destructive": {"destructive": True},
        "paid": {"price_points": 3},
        "admin_only": {"admin_only": True},
        "required": {"parameters": {"type": "object", "required": ["q"], "properties": {"q": {"type": "string"}}}},
        "requires": {"requires": ("It runs only when the person's matrx-local app is connected.",)},
    }[flag]
    without = conditional_pitfalls(base, params_of(base.parameters))
    t = ToolFacts(**{**base.__dict__, **on})
    with_ = conditional_pitfalls(t, params_of(t.parameters))
    assert not any(sentences[flag] in s for s in without)
    assert any(sentences[flag] in s for s in with_)
    assert any(sentences[flag] in s for s in build_tool_skill(t).body.splitlines())


# -- 7. visibility --------------------------------------------------------------------------------

def test_an_admin_only_tools_skill_is_never_public_and_never_named_publicly():
    admin = ToolFacts(id="a", name="sql", description="Admin CRUD.", parameters={}, source_kind="native", admin_only=True)
    assert build_tool_skill(admin).published is False
    pub = ToolFacts(id="p", name="read_rows", description="Read rows.", parameters={}, source_kind="native")
    b = build_bundle_skill(BundleFacts(id="b", name="db", description="DB tools.", lister_id="l", lister_name="bundle:list_db", members=(admin, pub)))
    assert b.published and "`sql`" not in b.body and "`read_rows`" in b.body


# -- 9. nothing in a generated text is a variable ---------------------------------------------------

def test_no_generated_text_holds_an_unescaped_variable():
    t = ToolFacts(id="t", name="widget_text_patch", source_kind="native", parameters={},
                  description="Patch text. It must never cut through a code block, math or a {{variable}}; {{ spaced }} too.")
    g = build_tool_skill(t)
    for text in (g.body, g.description):
        assert not re.search(r"\{\{(?!!)", text), text
    assert "{{!variable}}" in g.body
