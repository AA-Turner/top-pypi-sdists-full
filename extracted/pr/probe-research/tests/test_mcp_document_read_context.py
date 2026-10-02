"""Direct document reads retain useful facts without hiding their exact text."""

from __future__ import annotations

import pytest

from probe.mcp.service import ResearchReadService
from tests.test_mcp_delivery import _bounded, _wire
from tests.test_mcp_delivery_sources import _walk
from tests.test_mcp_entity_projection import EntitySource

_CAVEAT = "Held-out set excludes multilingual traffic."
_HEADLINE = {"accuracy": 0.842, "baseline_accuracy": 0.816}


# 0220: the default kind is a PROJECT, not a run. These tests read the
# `summary` view, and a run no longer offers one -- it carries no authored
# document, so there is nothing for the view to page through.
def _source(kind="project", **overrides):
    return EntitySource(
        kind,
        {
            "id": "one",
            "name": "LoRA confirmation",
            "status": "completed",
            "summary": dict(_HEADLINE),
            "notes": _CAVEAT,
            "document": "# Confirmation\nAccuracy improved on the held-out split.",
            "config": {"unused": "private configuration" * 2000},
            "metadata": {"unused": "generated trace" * 2000},
            **overrides,
        },
    )


# 0220: a RUN has no `summary` view -- it carries no authored document.
@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_notes_first_answers_status_and_caveat_in_one_read(kind):
    source = _source(kind)
    page = _bounded(
        _wire(ResearchReadService(source), "entity", {"refs": [f"{kind}:one"], "view": "notes"}),
        2000,
    )
    assert page["data"]["entity"]["status"] == "completed"
    assert page["data"]["notes"] == _CAVEAT
    assert "next_cursor" not in page
    assert source.reads == [f"{kind}:one"]
    assert not {"config", "metadata", "notes", "document"} & page["data"]["entity"].keys()


# 0220: a RUN has no `summary` view -- it carries no authored document.
@pytest.mark.parametrize("kind", ["project", "experiment"])
def test_summary_first_answers_headline_and_caveat_in_one_read(kind):
    source = _source(kind)
    page = _bounded(
        _wire(ResearchReadService(source), "entity", {"refs": [f"{kind}:one"], "view": "summary"}),
        2000,
    )
    assert page["data"]["entity"]["summary"] == _HEADLINE
    assert page["data"]["entity"]["status"] == "completed"
    assert page["data"]["notes"] == {"text": _CAVEAT, "truncated": False}
    assert page["data"][f"{kind}_summary"]["document"] == source.entity["document"]
    assert "next_cursor" not in page
    assert source.reads == [f"{kind}:one"]
    assert not {"config", "metadata", "notes", "document"} & page["data"]["entity"].keys()


@pytest.mark.parametrize("view", ["notes", "summary"])
def test_long_document_has_first_page_context_once_and_exact_original_text(view):
    field = "notes" if view == "notes" else "document"
    body = "Evidence 🌍 <|endoftext|> preserves Unicode.\n" * 600
    source = _source(**{field: body})

    def append(_index, _page):
        source.entity[field] += "Appended after the original read.\n"

    delivered, pages = _walk(
        ResearchReadService(source),
        {"refs": ["run:one"], "view": view, "token_budget": 2000},
        after_page=append,
    )
    assert len(pages) > 1
    first = pages[0]["data"]
    assert first["format"] == "text_fragment" and first["text"]
    assert first["context"]["entity"]["status"] == "completed"
    assert first["context"]["entity"]["summary"] == _HEADLINE
    if view == "summary":
        assert first["context"]["notes"] == {"text": _CAVEAT, "truncated": False}
    else:
        assert "notes" not in first["context"]  # the document itself is not copied
    assert all("context" not in page["data"] for page in pages[1:])
    assert delivered == [body]
    assert len(source.reads) == len(pages)
    assert "completeness" not in pages[-1]


def test_summary_caveat_excerpt_keeps_its_valid_notes_door():
    source = _source(notes=_CAVEAT * 100, document="Document.\n" * 4000)
    first = _bounded(
        _wire(ResearchReadService(source), "entity", {"refs": ["run:one"], "view": "summary"}),
        2000,
    )
    excerpt = first["data"]["context"]["notes"]
    assert excerpt["truncated"] is True and excerpt["read_all"] == 'view="notes"'
    assert excerpt["text"].startswith(_CAVEAT)


@pytest.mark.parametrize("budget", [512, 2000])
def test_notes_with_sub_notes_keep_first_page_context_and_reconstruct_all_evidence(budget):
    body = "Primary evidence 🌍\n" * 500
    source = _source(notes=body)
    source.client.list_sub_notes = lambda *_: {
        "sub_notes": [{"id": "sub-one", "title": "Scorer caveat", "chars": len(_CAVEAT)}]
    }
    source.client.get_sub_note = lambda *_: {"body": _CAVEAT}
    delivered, pages = _walk(
        ResearchReadService(source),
        {"refs": ["run:one"], "view": "notes", "token_budget": budget},
    )
    assert len(pages) > 1
    first = pages[0]["data"]
    assert first["format"] == "json_fragment" and first["text"]
    assert first["context"]["entity"]["status"] == "completed"
    assert first["context"]["entity"]["summary"] == _HEADLINE
    assert all("context" not in page["data"] for page in pages[1:])
    assert len(delivered) == 1
    assert delivered[0]["data"]["notes"] == body
    assert delivered[0]["data"]["sub_notes"][0]["excerpt"] == _CAVEAT
    assert delivered[0]["data"]["sub_notes"][0]["title"] == "Scorer caveat"
    assert len(source.reads) == len(pages)


@pytest.mark.parametrize("view", ["notes", "summary"])
@pytest.mark.parametrize("empty", [False, True])
def test_oversized_optional_context_cannot_strand_a_document_at_minimum_budget(view, empty):
    field = "notes" if view == "notes" else "document"
    body = "" if empty else "序列🙂\n" * 800
    source = _source(name="🐍" * 6000, **{field: body})
    delivered, pages = _walk(
        ResearchReadService(source),
        {"refs": ["run:one"], "view": view, "token_budget": 512},
    )
    first = pages[0]["data"]
    assert first["context"] == {"omitted": True, "read_more": 'view="card"'}
    assert first["text"] or empty
    assert all("context" not in page["data"] for page in pages[1:])
    assert delivered == [body]
    assert "next_cursor" not in pages[-1] and pages[-1]["data"]["complete"] is True


@pytest.mark.parametrize("view", ["notes", "summary"])
def test_context_does_not_weaken_document_edit_detection(view):
    field = "notes" if view == "notes" else "document"
    source = _source(**{field: "Original document.\n" * 2000})
    service = ResearchReadService(source)
    arguments = {"refs": ["run:one"], "view": view, "token_budget": 2000}
    first = _bounded(_wire(service, "entity", arguments), 2000)
    assert first["data"]["context"]["entity"]["status"] == "completed"
    source.entity[field] = "Edit before the original prefix."
    error = _bounded(
        _wire(service, "entity", {**arguments, "cursor": first["next_cursor"]}),
        2000,
        error=True,
    )
    assert "source_changed" in error
