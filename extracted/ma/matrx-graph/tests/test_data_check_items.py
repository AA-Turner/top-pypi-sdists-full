"""``data.check_items`` — answer checks, run through the real scheduler.

Every test compiles a graph, so the config is validated the way a saved
workflow's is and the output is what a downstream edge receives. The cases are
the real ones the custom steps handled by hand (generic-only STEP-CENSUS GAP 2):
a page reader's quotes (whitespace / curly quotes / case), an offering-role
answer's ids (sent twice, never sent, never answered), Curator labels outside
the allowed set, AI-visibility's forbidden register terms (another step's list,
width-folded, near-miss spelling), a citation list against the rule ids, an
empty answer, and a per-batch source chosen by key — on a whole list and inside
a For Each.
"""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from matrx_graph import (
    Definition,
    MemoryCheckpointer,
    NodeRegistry,
    RunStatus,
    Scheduler,
    compile_graph,
    register_builtin_nodes,
)
from matrx_graph.checks import ItemCheckSpec, flat, folded

from tests._fixtures import make_app_context


def _registry() -> NodeRegistry:
    reg = NodeRegistry()
    register_builtin_nodes(reg)
    return reg


async def _run(inputs: dict[str, Any], checks: list[dict[str, Any]], *, ok: bool = True) -> Any:
    registry = _registry()
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "n",
                    "type": "data.check_items",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {"checks": checks}, "inputs": inputs},
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    scheduler = Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry)
    result = await scheduler.run(run_id="t-check-items", inputs=inputs)
    if ok:
        assert result.status is RunStatus.COMPLETED, result.error
        return result.last_outputs["n"]
    assert result.status is not RunStatus.COMPLETED
    return result


def _nz(counts: dict[str, int]) -> dict[str, int]:
    return {k: v for k, v in counts.items() if v}


PAGE = (
    "Acme Recycling — We [shred hard drives on site](https://acme.example/shred) and\n"
    "  recycle   “old” laptops for free. Founded in 1999."
)


def test_the_step_is_registered_with_a_plain_description():
    spec = _registry().get("data.check_items").spec
    assert spec.display_name == "Check Items"
    assert "workflow" not in spec.description.lower()
    assert spec.config_schema.model_json_schema()["properties"]["checks"]


async def test_verbatim_folds_whitespace_quote_marks_and_links_and_drops_an_invented_quote():
    items = [
        {"name": "shredding", "quote": "shred hard drives on site and recycle \"old\" laptops"},
        {"name": "pickup", "quote": "free pickup for every household"},
        {"name": "history", "quote": "Founded  in 1999."},
    ]
    out = await _run(
        {"items": items, "page": PAGE},
        [{"type": "verbatim", "path": "quote", "source": "page"}],
    )
    assert [i["name"] for i in out["items"]] == ["shredding", "history"]
    assert (out["kept"], out["dropped"], out["total"]) == (2, 1, 3)
    assert _nz(out["counts"]) == {"quote.verbatim:not_verbatim": 1}
    assert out["rejected"][0]["index"] == 1
    assert out["rejected"][0]["reasons"][0]["code"] == "not_verbatim"
    assert out["passed"] is False


async def test_case_counts_under_flat_and_is_folded_under_folded():
    items = [{"quote": "FOUNDED IN 1999"}]
    flat_out = await _run({"items": items, "page": PAGE}, [{"type": "verbatim", "path": "quote", "source": "page"}])
    assert flat_out["kept"] == 0
    folded_out = await _run(
        {"items": items, "page": PAGE},
        [{"type": "verbatim", "path": "quote", "source": "page", "fold": "folded"}],
    )
    assert folded_out["kept"] == 1


async def test_a_list_of_texts_passes_when_any_holds_the_quote_and_an_empty_quote_is_missing():
    out = await _run(
        {"items": [{"q": "second page"}, {"q": ""}, {"q": "third"}], "pages": ["first page", "the second page"]},
        [{"type": "verbatim", "path": "q", "source": "pages"}],
    )
    assert [i["q"] for i in out["items"]] == ["second page"]
    assert _nz(out["counts"]) == {"q.verbatim:missing": 1, "q.verbatim:not_verbatim": 1}


async def test_per_item_source_chosen_by_key_never_borrows_another_batchs_text():
    batches = [{"id": "b1", "text": "We repair phones."}, {"id": "b2", "text": "We sell cases."}]
    items = [
        {"batch": "b1", "quote": "repair phones"},
        {"batch": "b2", "quote": "repair phones"},  # true of b1, not of its own batch
        {"batch": "b9", "quote": "sell cases"},  # no such batch was sent
    ]
    out = await _run(
        {"items": items, "batches": batches},
        [{"type": "verbatim", "path": "quote", "source": "batches", "source_by": "batch"}],
    )
    assert out["items"] == [items[0]]
    assert _nz(out["counts"]) == {"quote.verbatim:not_verbatim": 1, "quote.verbatim:no_source": 1}


async def test_once_drops_an_id_sent_twice_and_an_id_never_sent():
    items = [{"id": "o1", "role": "core"}, {"id": "o2", "role": "add_on"}, {"id": "o1", "role": "core"},
             {"id": "o7", "role": "core"}]
    out = await _run(
        {"items": items, "sent": [{"id": "o1"}, {"id": "o2"}, {"id": "o3"}]},
        [{"type": "once", "path": "id", "allowed_from": "sent", "from_field": "id"}],
    )
    assert [i["id"] for i in out["items"]] == ["o1", "o2"]
    assert _nz(out["counts"]) == {"id.once:duplicate": 1, "id.once:unknown": 1}
    assert out["sets"]["id.once"] == {"missing": [], "unknown": ["o7"], "duplicate": ["o1"]}


async def test_same_set_reports_missing_unknown_and_duplicate_separately():
    items = [{"id": 1}, {"id": 2}, {"id": 2}, {"id": 9}]
    out = await _run(
        {"items": items, "sent_ids": [1, 2, 3]},
        [{"type": "same_set", "path": "id", "allowed_from": "sent_ids"}],
    )
    assert out["sets"]["id.same_set"] == {"missing": ["3"], "unknown": ["9"], "duplicate": ["2"]}
    assert out["kept"] == 2
    assert out["passed"] is False


async def test_same_set_set_to_fail_fails_the_step_when_an_id_is_unanswered():
    result = await _run(
        {"items": [{"id": "a"}], "sent_ids": ["a", "b"]},
        [{"type": "same_set", "path": "id", "allowed_from": "sent_ids", "on_fail": "fail"}],
        ok=False,
    )
    assert "b" in str(result.error)


async def test_in_set_checks_every_value_of_a_list_field():
    items = [{"kinds": ["service", "product"]}, {"kinds": ["service", "vibes"]}]
    out = await _run(
        {"items": items},
        [{"type": "in_set", "path": "kinds", "allowed": ["service", "product", "bundle"]}],
    )
    assert out["items"] == [items[0]]
    assert _nz(out["counts"]) == {"kinds.in_set:not_in_set": 1}


async def test_citations_never_invented_fail_the_step_when_asked():
    result = await _run(
        {"items": [{"rule_id": "R1"}, {"rule_id": "R99"}], "rulebook": ["R1", "R2"]},
        [{"type": "in_set", "path": "rule_id", "allowed_from": "rulebook", "on_fail": "fail"}],
        ok=False,
    )
    assert "R99" in str(result.error)


async def test_not_contains_reads_terms_from_another_input_with_width_case_and_near_miss_folding():
    register = [{"term": "Recyclatron"}, {"term": "Acme Green"}]
    items = [
        {"text": "Ask ＡＣＭＥ green about it"},  # full-width + case
        {"text": "ask recyclatrom today"},  # near-miss spelling of a long word
        {"text": "a recycling company near me"},
        {"text": "Acme Greenhouse supplies"},  # whole words only: "Greenhouse" is not "Green"
    ]
    out = await _run(
        {"items": items, "register": register},
        [{"type": "not_contains", "path": "text", "terms_from": "register", "from_field": "term", "fuzzy": 0.86,
          "fuzzy_drops": True}],
    )
    assert [i["text"] for i in out["items"]] == ["a recycling company near me", "Acme Greenhouse supplies"]
    assert _nz(out["counts"]) == {"text.not_contains:contains_term": 2}
    exact = await _run(
        {"items": items[1:2], "register": register},
        [{"type": "not_contains", "path": "text", "terms_from": "register", "from_field": "term"}],
    )
    assert exact["kept"] == 1


async def test_max_length_and_required_count_their_own_reasons():
    items = [{"label": "Fast repair"}, {"label": "one two three four five six"}, {"note": "no label"}]
    out = await _run(
        {"items": items},
        [{"type": "required", "path": "label"}, {"type": "max_length", "path": "label", "max": 4, "unit": "words",
                                                 "optional": True}],
    )
    assert out["items"] == [items[0]]
    assert _nz(out["counts"]) == {"label.max_length:too_long": 1, "label.required:missing": 1}


async def test_an_empty_answer_passes_with_zero_counts_but_same_set_reports_every_id_missing():
    out = await _run({"items": []}, [{"type": "required", "path": "id"}])
    assert (out["kept"], out["dropped"], out["total"], out["passed"]) == (0, 0, 0, True)
    out = await _run({"items": [], "sent": ["a"]}, [{"type": "same_set", "path": "id", "allowed_from": "sent"}])
    assert out["sets"]["id.same_set"]["missing"] == ["a"]
    assert out["passed"] is False


async def test_a_source_the_step_was_not_given_fails_loudly_never_passes():
    result = await _run(
        {"items": [{"quote": "x"}]}, [{"type": "verbatim", "path": "quote", "source": "page"}], ok=False
    )
    assert "page" in str(result.error)


def test_a_check_missing_its_settings_is_refused_when_saved():
    with pytest.raises(ValidationError):
        ItemCheckSpec.model_validate({"type": "verbatim", "path": "quote"})
    with pytest.raises(ValidationError):
        ItemCheckSpec.model_validate({"type": "in_set", "path": "x"})


async def test_inside_a_for_each_each_batch_is_checked_against_its_own_text():
    registry = _registry()
    batches = [
        {"page": "We repair phones.", "answer": [{"quote": "repair phones"}, {"quote": "sell cases"}]},
        {"page": "We sell cases.", "answer": [{"quote": "sell cases"}]},
    ]
    defn = Definition.model_validate(
        {
            "nodes": [
                {"id": "each", "type": "control.map", "position": {"x": 0, "y": 0},
                 "data": {"config": {"target_node_id": "check",
                                     "payload_template": {"items": "$item.answer", "page": "$item.page"}},
                          "input": {"items": batches}}},
                {"id": "check", "type": "data.check_items", "position": {"x": 0, "y": 0},
                 "data": {"config": {"checks": [{"type": "verbatim", "path": "quote", "source": "page"}]}}},
                {"id": "gather", "type": "control.gather", "position": {"x": 0, "y": 0}, "data": {"config": {}}},
            ],
            "edges": [{"id": "e", "source": "check", "target": "gather", "type": "default", "data": {"kind": "data"}}],
            "entry_nodes": ["each"],
        }
    )
    graph = compile_graph(defn, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(run_id="t-ci-map")
    assert result.status is RunStatus.COMPLETED, result.error
    gathered = result.last_outputs["gather"]
    per_batch = sorted((r["kept"], r["dropped"]) for r in gathered["values"])
    assert per_batch == [(1, 0), (1, 1)]


def test_the_shared_folding_is_the_one_aidream_readers_used():
    assert flat("“Hello”  —  [world](https://x.y)") == '"Hello" - world'
    assert folded("<strong>Shred</strong> &amp; Recycle") == "shred & recycle"


async def test_every_reason_is_counted_even_when_zero():
    out = await _run({"items": [{"id": "a"}], "sent": ["a"]}, [{"type": "once", "path": "id", "allowed_from": "sent"}])
    assert out["counts"] == {"id.once:missing": 0, "id.once:unknown": 0, "id.once:duplicate": 0}


async def test_a_repeated_id_whose_first_answer_is_fake_keeps_the_real_one():
    items = [{"id": "a", "quote": "free pickup"}, {"id": "a", "quote": "Founded in 1999."}, {"id": "b", "quote": "nope"}]
    out = await _run(
        {"items": items, "page": PAGE, "sent": ["a", "b"]},
        [{"type": "verbatim", "path": "quote", "source": "page"},
         {"type": "same_set", "path": "id", "allowed_from": "sent"}],
    )
    assert out["items"] == [items[1]]
    # b's only answer was dropped by the quote check, so b was never honestly answered.
    assert out["sets"]["id.same_set"] == {"missing": ["b"], "unknown": [], "duplicate": []}
    assert _nz(out["counts"]) == {"quote.verbatim:not_verbatim": 2}


async def test_a_misspelled_from_field_fails_loudly_instead_of_turning_the_check_off():
    result = await _run(
        {"items": [{"text": "Recyclatron"}], "register": [{"term": "Recyclatron"}]},
        [{"type": "not_contains", "path": "text", "terms_from": "register", "from_field": "trem"}],
        ok=False,
    )
    assert "trem" in str(result.error)


async def test_source_records_without_the_text_field_fail_loudly_not_as_not_verbatim():
    result = await _run(
        {"items": [{"quote": "repair phones"}], "pages": [{"id": "p1", "body": "We repair phones."}]},
        [{"type": "verbatim", "path": "quote", "source": "pages"}],
        ok=False,
    )
    assert "text" in str(result.error)


async def test_a_term_with_no_letters_or_digits_is_refused():
    result = await _run(
        {"items": [{"text": "a - b"}]}, [{"type": "not_contains", "path": "text", "terms": ["--"]}], ok=False
    )
    assert "--" in str(result.error)


def test_settings_that_do_not_fit_the_check_type_are_refused_when_saved():
    for bad in (
        {"type": "in_set", "path": "x", "allowed": ["a"], "fuzzy": 0.9},
        {"type": "required", "path": "x", "source": "page"},
        {"type": "not_contains", "path": "x", "terms": ["a"], "fold": "exact"},
        {"type": "in_set", "path": "x", "allowed": ["a"], "from_field": "id"},
    ):
        with pytest.raises(ValidationError):
            ItemCheckSpec.model_validate(bad)
