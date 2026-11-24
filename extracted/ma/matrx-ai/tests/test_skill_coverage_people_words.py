"""Template v3 (chat-agent-skills F8): a tool skill says what the tool is FOR in the words people use
(``ToolFacts.asked_as``, data on the tool row) and an MCP tool's skill names its service. Below v3
the bytes are exactly version 2's, so a boot sync on an unflipped build never rewrites a row."""

from __future__ import annotations

import pytest

from matrx_ai.skills import coverage as cov
from matrx_ai.skills.coverage import ToolFacts, asked_as_of, build_tool_skill, description_limit

WEB = ToolFacts(
    id="t1",
    name="web_search_results",
    description="Search the open web and return ranked pages with title, address and a text snippet. Use a short query.",
    parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    source_kind="catalog",
    display_name="Web search",
    job_key="web_search_results",
)
MCP = ToolFacts(
    id="t2",
    name="mcp.fibery.update_databases",
    description="Update databases in a workspace schema.",
    parameters={"type": "object", "properties": {}},
    source_kind="mcp_discovered",
    mcp_server_slug="fibery",
    mcp_server_name="Fibery",
    listers=("fibery_tools",),
)
ASKED = ("search the web", "look something up online", "find the latest news", "find current facts with sources to cite")


def _with(t: ToolFacts, **kw) -> ToolFacts:
    from dataclasses import replace

    return replace(t, **kw)


def test_below_v3_the_people_words_change_nothing(monkeypatch):
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 2)
    assert build_tool_skill(_with(WEB, asked_as=ASKED)) == build_tool_skill(WEB)
    assert build_tool_skill(MCP).label == "Update databases (tool)"


def test_v3_leads_with_the_persons_words_and_keeps_the_tools_own(monkeypatch):
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 3)
    g = build_tool_skill(_with(WEB, asked_as=ASKED))
    assert g.description.startswith("Use when the person wants to search the web, look something up online")
    assert "ranked pages" in g.description  # the tool's own terms stay, in brackets
    assert len(g.description) <= description_limit()
    assert 'People ask for it as: "search the web"' in g.body
    assert g.source_hash != build_tool_skill(WEB).source_hash


def test_v3_drops_whole_phrases_to_fit(monkeypatch):
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 3)
    many = tuple(f"do a long ordinary thing number {i} for the person" for i in range(8))
    g = build_tool_skill(_with(WEB, asked_as=many))
    assert len(g.description) <= description_limit()
    assert g.description.startswith("Use when the person wants to do a long ordinary thing number 0")
    assert "number 7" not in g.description


def test_v3_names_an_mcp_tools_service(monkeypatch):
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 3)
    g = build_tool_skill(MCP)
    assert g.label == "Update databases (Fibery tool)"  # service after the head word
    assert "Fibery" in g.description
    assert len(g.description) <= description_limit()


def test_without_people_words_a_native_tool_keeps_its_v2_description(monkeypatch):
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 2)
    before = build_tool_skill(WEB).description
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 3)
    assert build_tool_skill(WEB).description == before


@pytest.mark.parametrize(
    ("raw", "want"),
    [
        (None, ()),
        ("search the web", ()),
        (["search the web.", " Search the web ", "", 3, "read a page"], ("search the web", "read a page")),
    ],
)
def test_asked_as_of_reads_only_a_list_of_phrases(raw, want):
    assert asked_as_of(raw) == want


def test_v3_keeps_the_first_clause_when_the_tools_terms_do_not_fit_whole(monkeypatch):
    """Never a tail cut mid-clause ("… as soon)"): the first clause of the tool's own terms."""
    monkeypatch.setattr(cov, "TEMPLATE_VERSION", 3)
    page = ToolFacts(
        id="t3",
        name="quick_page",
        description="The person's quick-publish pages, live at a short address as soon as saved with nothing else to do (no draft or publish step).",
        parameters={"type": "object", "properties": {}},
        source_kind="native",
        asked_as=("make a web page", "publish a simple website or landing page", "share a page by link"),
    )
    g = build_tool_skill(page)
    assert g.description.endswith("(the person's quick-publish pages).")
