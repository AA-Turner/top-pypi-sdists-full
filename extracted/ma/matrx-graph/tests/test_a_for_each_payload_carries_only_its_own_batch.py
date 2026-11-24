"""Guard (FX8, 2026-11-02): a For each item carries ITS batch, never every batch.

Live run 424e086e (Brand foundation, stage 1): the Curator subgraph "Ask a mandate per batch and check
each answer" asked 30 batches (each holding ~300 KB of brand data once its held values were read back),
then fanned the checks out with ``src: "$in.batches"`` — the WHOLE list copied into every one of the 30
items (~9 MB x 30 = ~280 MB per super-step). The worker died on that step four times and recovery gave up.
Runs with small batches never noticed.

The fix reads only the item's own batch: ``src: ["$in.batches.[batch_id={$item.values.0.batch_id}]"]``.
This test runs the node's real template resolver (the one For each uses to build every dispatch) over the
same data shape and pins three things:
  * the bytes dispatched grow with the batches, not with batches x batches;
  * the answer of the check is the same as with the whole list (a real quote is kept, a made-up one dropped);
  * the old shape really is the multiplier (so the pin can fail).
"""

from __future__ import annotations

import json

from matrx_graph.checks import check_items, parse_item_checks
from matrx_graph.nodes._template import substitute_template

OWN_BATCH = ["$in.batches.[batch_id={$item.values.0.batch_id}]"]
WHOLE_LIST = "$in.batches"

_CHECKS = parse_item_checks([
    {"key": "quote_verbatim", "fold": "flat", "path": "answer_quote", "type": "verbatim", "optional": True,
     "source": "src", "source_by": "batch_id", "source_key_field": "batch_id", "source_text_field": "source_text"},
    {"key": "id_in_batch", "fold": "flat", "path": "answer_id", "type": "once", "optional": True,
     "allowed_from": "sent"},
])


def _batches(n: int, held_bytes: int) -> list[dict]:
    return [
        {"batch_id": f"b{i}", "sent_ids": [f"id{i}"], "source_text": f"page {i} says we make candles",
         "values": {"held": "x" * held_bytes}}
        for i in range(n)
    ]


def _payload(src_template, batches: list[dict], i: int) -> dict:
    template = {"src": src_template,
                "sent": {"default": [], "$optional": "$in.batches.[batch_id={$item.values.0.batch_id}].sent_ids"}}
    item = {"values": [{"batch_id": f"b{i}", "answer_id": f"id{i}", "answer_quote": "we make candles"}]}
    return substitute_template(template, item, index=i, extra={"batches": batches})


def _dispatched_bytes(src_template, n: int, held_bytes: int) -> int:
    batches = _batches(n, held_bytes)
    return sum(len(json.dumps(_payload(src_template, batches, i))) for i in range(n))


def test_dispatched_bytes_grow_with_the_batches_not_with_their_square() -> None:
    small = _dispatched_bytes(OWN_BATCH, 10, 20_000)
    big = _dispatched_bytes(OWN_BATCH, 30, 20_000)
    assert big < small * 3.5, f"3x the batches sent {big / small:.1f}x the bytes; the item is carrying more than its own batch"


def test_the_old_whole_list_shape_is_the_multiplier() -> None:
    small = _dispatched_bytes(WHOLE_LIST, 10, 20_000)
    big = _dispatched_bytes(WHOLE_LIST, 30, 20_000)
    assert big > small * 8, "the whole-list shape no longer multiplies; this guard can no longer fail"


def test_the_check_answers_the_same_with_only_its_own_batch() -> None:
    batches = _batches(5, 100)
    for quote, kept in (("we make candles", 1), ("we sell cars", 0)):
        item = {"values": [{"batch_id": "b2", "answer_id": "id2", "answer_quote": quote}]}
        for src in (OWN_BATCH, WHOLE_LIST):
            p = _payload(src, batches, 2)
            r = check_items(item["values"], _CHECKS, {"src": p["src"], "sent": p["sent"]})
            assert r.kept == kept, (src, quote, r.rejected)


# --- FX10 (2026-11-02): a batch whose agent answer held NO claims -----------------------------
# Live runs d13840b2 / 20ea98b2 (Brand discovery, via 80606a4e): a page batch came back with an empty
# values list, so ``$item.values.0.batch_id`` had nothing to read and the whole subgraph died with
# TemplatePathMissing, taking every non-empty batch's claims with it. The decision: an empty batch
# passes through as an empty answer (nothing to check, nothing kept, nothing rejected); the batch itself
# is still counted in batches_answered, and a FAILED call is a hole, reported separately.
OWN_BATCH_OR_NONE = [{"default": {}, "$optional": "$in.batches.[batch_id={$item.values.0.batch_id}]"}]
SENT_OR_NONE = {"default": [], "$optional": "$in.batches.[batch_id={$item.values.0.batch_id}].sent_ids"}


def _empty_batch_payload(src_template, batches: list[dict]) -> dict:
    template = {"src": src_template, "sent": SENT_OR_NONE}
    return substitute_template(template, {"values": []}, index=1, extra={"batches": batches})


def test_an_empty_batch_does_not_crash_the_old_template_is_red_the_new_green() -> None:
    batches = _batches(3, 100)
    try:
        _empty_batch_payload(OWN_BATCH, batches)
    except Exception as exc:  # the live failure: TemplatePathMissing
        assert "values.0.batch_id" in str(exc) or "TemplatePath" in type(exc).__name__, exc
    else:
        raise AssertionError("the old template no longer fails on an empty batch; this guard can no longer fail")
    p = _empty_batch_payload(OWN_BATCH_OR_NONE, batches)
    r = check_items([], _CHECKS, {"src": p["src"], "sent": p["sent"]})
    assert (r.kept, r.rejected) == (0, [])


def test_a_non_empty_batch_still_checks_with_the_empty_batch_tolerant_template() -> None:
    batches = _batches(5, 100)
    for quote, kept in (("we make candles", 1), ("we sell cars", 0)):
        item = {"values": [{"batch_id": "b2", "answer_id": "id2", "answer_quote": quote}]}
        template = {"src": OWN_BATCH_OR_NONE, "sent": SENT_OR_NONE}
        p = substitute_template(template, item, index=2, extra={"batches": batches})
        assert p["src"] == [batches[2]]
        r = check_items(item["values"], _CHECKS, {"src": p["src"], "sent": p["sent"]})
        assert r.kept == kept, (quote, r.rejected)


def test_the_tolerant_template_stays_linear() -> None:
    batches = _batches(30, 20_000)
    total = 0
    for i in range(30):
        item = {"values": [{"batch_id": f"b{i}", "answer_id": f"id{i}", "answer_quote": "we make candles"}]}
        p = substitute_template({"src": OWN_BATCH_OR_NONE, "sent": SENT_OR_NONE}, item, index=i, extra={"batches": batches})
        total += len(json.dumps(p))
    assert total < 30 * 25_000
