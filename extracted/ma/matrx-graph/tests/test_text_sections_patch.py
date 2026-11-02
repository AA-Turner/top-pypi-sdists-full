"""text.sections.patch: section edits by invisible marker, refusals reported, settings honored.

The first block ports the Vision Interview's own document-section tests
(aidream/services/vision_interview/tests/test_scribe_doc_patches.py) case for case; the
byte-for-byte comparison against that code lives in aidream
(aidream/graph_actions/tests/test_text_sections_patch_parity.py).
"""

from __future__ import annotations

from tests.test_text_nodes import _run_single_node

NODE = "text.sections.patch"
M = "<!-- matrx:section:{} -->"


async def _patch(document: str, *edits: dict, **config) -> dict:
    return await _run_single_node(
        NODE, {"document": document, "edits": list(edits)}, config or None
    )


def _e(key: str, op: str, markdown: str) -> dict:
    return {"section_key": key, "op": op, "markdown": markdown}


# --- ported parity cases -------------------------------------------------------------


async def test_create_makes_a_marker_section_with_no_visible_tags() -> None:
    out = await _patch("", _e("core_idea", "create", "## Core Idea\n\nThe idea."))
    assert out["document"] == f"{M.format('core_idea')}\n## Core Idea\n\nThe idea."
    assert [a["section_key"] for a in out["applied"]] == ["core_idea"]
    assert out["applied"][0]["result"] == "created"
    assert out["applied"][0]["title"] == "Core Idea"
    assert out["changed"] is True and out["refused"] == []
    assert out["__kind"] == "sections_patch_result"


async def test_replace_rewrites_only_the_target_section() -> None:
    first = await _patch(
        "", _e("core_idea", "create", "Old idea text."), _e("risks", "create", "Risk one.")
    )
    out = await _patch(first["document"], _e("core_idea", "replace", "New idea text."))
    assert "New idea text." in out["document"] and "Old idea text." not in out["document"]
    assert "Risk one." in out["document"]
    assert out["applied"][0]["result"] == "replaced"


async def test_append_keeps_existing_content_in_order() -> None:
    first = await _patch("", _e("core_idea", "create", "First."))
    out = await _patch(first["document"], _e("core_idea", "append", "Second."))
    assert out["document"] == f"{M.format('core_idea')}\nFirst.\n\nSecond."
    assert out["applied"][0]["result"] == "appended"


async def test_replace_creates_when_section_absent_by_default() -> None:
    first = await _patch("", _e("a", "create", "alpha text"))
    out = await _patch(first["document"], _e("b", "replace", "fresh text"))
    assert "fresh text" in out["document"] and "alpha text" in out["document"]
    assert out["applied"][0]["result"] == "created"


async def test_invalid_section_key_is_refused_and_reported_document_untouched() -> None:
    first = await _patch("", _e("a", "create", "alpha text"))
    out = await _patch(first["document"], _e("<script>", "create", "evil payload"))
    assert out["document"] == first["document"]
    assert out["applied"] == [] and out["changed"] is False
    assert out["refused"] == [
        {"section_key": "<script>", "op": "create", "reason": "invalid_section_key"}
    ]


async def test_placeholder_and_empty_bodies_are_refused_document_untouched() -> None:
    first = await _patch("", _e("vision", "create", "A real vision body."))
    for junk in ("placeholder", "TBD", "", "…", "n/a", "## TODO", "ok"):
        out = await _patch(first["document"], _e("vision", "append", junk))
        assert out["document"] == first["document"], junk
        assert out["refused"][0]["reason"] == "empty_or_placeholder_body", junk
        assert out["changed"] is False, junk


async def test_legacy_xml_document_is_converted_on_apply() -> None:
    legacy = "<core_idea>\n## Core Idea\n\nOld body.\n</core_idea>"
    out = await _patch(legacy, _e("risks", "create", "A new risk."))
    assert "<core_idea>" not in out["document"]
    assert out["document"] == (
        f"{M.format('core_idea')}\n## Core Idea\n\nOld body.\n\n{M.format('risks')}\nA new risk."
    )


async def test_section_list_and_titles() -> None:
    out = await _patch(
        "",
        _e("core_idea", "create", "## The Big Idea\n\nBody."),
        _e("open_risks", "create", "No heading here."),
    )
    assert out["sections"] == [
        {"key": "core_idea", "title": "The Big Idea"},
        {"key": "open_risks", "title": "Open Risks"},
    ]


# --- new cases -----------------------------------------------------------------------


async def test_no_edits_returns_the_document_unchanged() -> None:
    doc = f"Intro line.\n\n{M.format('a')}\nAlpha body."
    out = await _patch(doc)
    assert out["document"] == doc and out["changed"] is False
    assert out["sections"] == [{"key": "a", "title": "A"}]


async def test_preamble_before_the_first_marker_is_kept() -> None:
    doc = f"# My Doc\n\n{M.format('a')}\nAlpha body."
    out = await _patch(doc, _e("a", "replace", "Alpha two."))
    assert out["document"] == f"# My Doc\n\n{M.format('a')}\nAlpha two."


async def test_on_missing_refuse_reports_instead_of_creating() -> None:
    doc = f"{M.format('a')}\nAlpha body."
    out = await _patch(
        doc,
        _e("b", "replace", "Bravo body."),
        _e("c", "append", "Charlie body."),
        on_missing="refuse",
    )
    assert out["document"] == doc and out["changed"] is False
    assert [r["reason"] for r in out["refused"]] == ["section_missing", "section_missing"]


async def test_create_still_creates_when_on_missing_is_refuse() -> None:
    out = await _patch("", _e("a", "create", "Alpha body."), on_missing="refuse")
    assert out["applied"][0]["result"] == "created"


async def test_placeholder_words_and_minimum_are_settings() -> None:
    doc = f"{M.format('a')}\nAlpha body."
    out = await _patch(
        doc,
        _e("a", "append", "coming soon"),
        _e("a", "append", "ok"),
        placeholder_bodies=["coming soon"],
        min_body_chars=1,
    )
    assert [r["reason"] for r in out["refused"]] == ["empty_or_placeholder_body"]
    assert out["document"] == f"{M.format('a')}\nAlpha body.\n\nok"
    stricter = await _patch(doc, _e("a", "append", "Too short"), min_body_chars=20)
    assert stricter["refused"][0]["reason"] == "empty_or_placeholder_body"


async def test_unknown_op_is_refused_not_fatal() -> None:
    out = await _patch("", _e("a", "delete", "Alpha body."), _e("b", "create", "Bravo body."))
    assert out["refused"] == [{"section_key": "a", "op": "delete", "reason": "unknown_op"}]
    assert [a["section_key"] for a in out["applied"]] == ["b"]


async def test_marker_prefix_setting_reads_and_writes_its_own_markers() -> None:
    doc = "<!-- page:hero -->\nOld hero."
    out = await _patch(doc, _e("hero", "replace", "New hero."), marker_prefix="page")
    assert out["document"] == "<!-- page:hero -->\nNew hero."
    assert "matrx:section" not in out["document"]


async def test_legacy_upgrade_can_be_turned_off_for_html_bearing_documents() -> None:
    doc = "Intro.\n<div>\nkeep this html\n</div>"
    kept = await _patch(doc, _e("b", "create", "Bravo body."), upgrade_legacy_tags=False)
    assert "<div>\nkeep this html\n</div>" in kept["document"]
    upgraded = await _patch(doc, _e("b", "create", "Bravo body."))
    assert "<div>" not in upgraded["document"]


async def test_two_edits_to_one_section_apply_in_order() -> None:
    out = await _patch(
        "", _e("a", "create", "One."), _e("a", "append", "Two."), _e("a", "append", "Three.")
    )
    assert out["document"] == f"{M.format('a')}\nOne.\n\nTwo.\n\nThree."
    assert [a["result"] for a in out["applied"]] == ["created", "appended", "appended"]


async def test_html_in_an_edit_body_survives_and_makes_no_fake_section() -> None:
    doc = f"{M.format('a')}\nAlpha body."
    out = await _patch(
        doc, _e("a", "append", "Has <i>x</i> html."), _e("b", "create", "More <b>bold</b> text.")
    )
    assert out["document"] == (
        f"{M.format('a')}\nAlpha body.\n\nHas <i>x</i> html.\n\n{M.format('b')}\nMore <b>bold</b> text."
    )
    assert [s["key"] for s in out["sections"]] == ["a", "b"]


async def test_legacy_tags_in_the_input_document_are_still_upgraded_once() -> None:
    out = await _patch("<a>Alpha body.</a>", _e("b", "create", "Bravo <i>body</i>."))
    assert out["document"] == f"{M.format('a')}\nAlpha body.\n\n{M.format('b')}\nBravo <i>body</i>."


async def test_a_body_carrying_a_section_marker_is_refused() -> None:
    doc = f"{M.format('a')}\nAlpha body."
    out = await _patch(
        doc,
        _e("a", "append", f"Sneaky.\n{M.format('admin')}\nInjected section."),
        _e("b", "create", "Fine body."),
    )
    assert out["refused"] == [
        {"section_key": "a", "op": "append", "reason": "body_contains_section_marker"}
    ]
    assert out["document"] == f"{doc}\n\n{M.format('b')}\nFine body."
    custom = await _patch(
        "<!-- page:hero -->\nHero.",
        _e("hero", "replace", "New.\n<!-- page:footer -->\nx"),
        marker_prefix="page",
    )
    assert custom["refused"][0]["reason"] == "body_contains_section_marker"


async def test_a_saved_document_with_html_is_never_upgraded_again() -> None:
    """Live defect (run 60b4c2d8): pass 2 turned pass 1's kept <b> into a section `b`."""
    first = await _patch("", _e("notes", "create", "Driver confirmed the <b>pickup</b> window."))
    second = await _patch(first["document"])
    assert second["document"] == first["document"]
    assert second["changed"] is False and second["upgraded_legacy"] is False
    third = await _patch(
        first["document"], _e("notes", "append", "Also <i>noted</i>.\n<b>\nblock\n</b>")
    )
    assert [s["key"] for s in third["sections"]] == ["notes"]
    assert "<b>pickup</b>" in third["document"] and "<i>noted</i>" in third["document"]


async def test_inline_tags_in_a_legacy_free_document_are_not_sections() -> None:
    doc = "Plain notes with <b>bold</b> and <em>emphasis</em> inline."
    out = await _patch(doc)
    assert out["document"] == doc and out["upgraded_legacy"] is False and out["sections"] == []


async def test_an_upgrade_alone_is_reported_but_is_not_a_change() -> None:
    legacy = "<core_idea>\n## Core Idea\n\nOld body.\n</core_idea>"
    out = await _patch(legacy)
    assert out["upgraded_legacy"] is True and out["changed"] is False
    assert out["document"] == f"{M.format('core_idea')}\n## Core Idea\n\nOld body."
    edited = await _patch(legacy, _e("risks", "create", "A new risk."))
    assert edited["upgraded_legacy"] is True and edited["changed"] is True
