"""``data.dedupe`` says WHAT each dropped item matched, and can match against saved entries (2026-10-27).

The break this catches: after a normalized or near-duplicate match the dropped items vanish
without a trace, so "skip what is already filed and hand on the saved id" is impossible.
Users: testimony filing (a re-cut quote -> the saved testimony id), an already-open choice ->
its id, news mentions already filed, a CRM import against existing contacts.
"""

from __future__ import annotations

from tests.test_data_collections import _out


def _m(out):
    return [m for m in out["matches"]]


async def test_matches_name_the_survivor_for_in_list_duplicates():
    items = [
        {"id": "a", "t": "Fast Delivery "},
        {"id": "b", "t": "fast  delivery"},
        {"id": "c", "t": "Free returns"},
        {"id": "d", "t": "FAST DELIVERY"},
    ]
    out = await _out("data.dedupe", {"items": items}, {"key": "t", "normalize": "case_space"})
    assert [i["id"] for i in out["items"]] == ["a", "c"]
    assert [(m["index"], m["survivor_index"], m["survivor_id"], m["against_index"]) for m in _m(out)] == [
        (1, 0, "a", None),
        (3, 0, "a", None),
    ]


async def test_keep_last_reports_the_last_as_survivor():
    items = [{"id": "a", "k": 1}, {"id": "b", "k": 1}]
    out = await _out("data.dedupe", {"items": items}, {"key": "k", "keep": "last"})
    assert [(m["index"], m["survivor_index"], m["survivor_id"]) for m in _m(out)] == [(0, 1, "b")]


async def test_against_drops_items_already_saved_and_hands_on_the_saved_id():
    saved = [{"id": "rec-1", "t": "Fast Delivery"}, {"id": "rec-2", "t": "Free returns"}]
    items = [{"t": "fast  delivery"}, {"t": "Handmade in Portland"}, {"t": "FREE RETURNS "}]
    out = await _out("data.dedupe", {"items": items, "against": saved}, {"key": "t", "normalize": "case_space"})
    assert out["items"] == [{"t": "Handmade in Portland"}]  # saved entries are never output
    assert out["kept"] == 1 and out["dropped"] == 2
    assert [(m["index"], m["against_index"], m["survivor_id"], m["survivor_index"]) for m in _m(out)] == [
        (0, 0, "rec-1", None),
        (2, 1, "rec-2", None),
    ]


async def test_against_with_similar_matches_a_recut_to_the_saved_testimony():
    saved = [{"id": "t-9", "q": "Our guides know the tides so well that every paddler returns relaxed and happy after the long morning tour"}]
    items = [
        {"q": "every paddler returns relaxed and happy after the long morning tour"},
        {"q": "The marina staff found us a slip within an hour of calling"},
    ]
    out = await _out(
        "data.dedupe",
        {"items": items, "against": saved},
        {"similar": {"text": "q", "measure": "containment", "threshold": 0.85}},
    )
    assert [i["q"][:10] for i in out["items"]] == ["The marina"]
    assert [(m["index"], m["against_index"], m["survivor_id"]) for m in _m(out)] == [(0, 0, "t-9")]


async def test_against_and_in_list_duplicates_together_and_merge_still_works():
    saved = [{"id": "s1", "url": "https://a.example/x"}]
    items = [
        {"url": "https://b.example/y", "engines": ["brave"]},
        {"url": "https://a.example/x", "engines": ["google"]},
        {"url": "https://b.example/y", "engines": ["bing"]},
    ]
    out = await _out(
        "data.dedupe",
        {"items": items, "against": saved},
        {"key": "url", "merge": {"combine_lists": ["engines"]}},
    )
    assert out["items"] == [{"url": "https://b.example/y", "engines": ["brave", "bing"]}]
    assert [(m["index"], m["survivor_index"], m["against_index"]) for m in _m(out)] == [(1, None, 0), (2, 0, None)]


async def test_against_hole_never_matches_and_id_path_is_settable():
    saved = [{"ref": 7, "k": None}, {"ref": 8, "k": "x"}]
    items = [{"k": "x"}, {"other": 1}]
    out = await _out("data.dedupe", {"items": items, "against": saved}, {"key": "k", "id_path": "ref"})
    assert out["kept"] == 1 and out["items"] == [{"other": 1}]
    assert [(m["index"], m["survivor_id"]) for m in _m(out)] == [(0, 8)]


async def test_two_passes_compose_territory_answers_vs_all_stored_then_plain_vs_plain():
    # Stored: same element+text under any territory blocks a territory answer; a no-territory
    # answer is blocked only by a stored no-territory item. The caller runs two passes.
    stored = [
        {"id": "s-us", "ek": "tone|warm and direct", "territory": "US"},
        {"id": "s-none", "ek": "voice|plain", "territory": None},
        {"id": "s-eu", "ek": "voice|plain", "territory": "EU"},
    ]
    territory_answers = [
        {"ek": "tone|warm and direct", "territory": "UK"},  # blocked by the US item
        {"ek": "tone|formal", "territory": "UK"},
    ]
    plain_answers = [
        {"ek": "voice|plain", "territory": None},  # blocked by the stored no-territory item
        {"ek": "tone|warm and direct", "territory": None},  # NOT blocked: the stored one has a territory
    ]
    stored_plain = [s for s in stored if s["territory"] is None]
    cfg = {"key": "ek"}
    one = await _out("data.dedupe", {"items": territory_answers, "against": stored}, cfg)
    two = await _out("data.dedupe", {"items": plain_answers, "against": stored_plain}, cfg)
    assert [i["ek"] for i in one["items"]] == ["tone|formal"]
    assert [(m["index"], m["survivor_id"]) for m in _m(one)] == [(0, "s-us")]
    assert [i["ek"] for i in two["items"]] == ["tone|warm and direct"]
    assert [(m["index"], m["survivor_id"]) for m in _m(two)] == [(0, "s-none")]
    # Each pass numbers its own input list, so a caller maps back by its own position
    # and the two match lists concatenate without clashing meaning.
    assert one["matches"][0]["index"] == two["matches"][0]["index"] == 0


async def test_without_against_old_calls_are_unchanged():
    out = await _out("data.dedupe", {"items": [{"u": 1}, {"u": 1}, {"u": 2}]}, {"key": "u"})
    assert out["items"] == [{"u": 1}, {"u": 2}] and out["kept"] == 2 and out["dropped"] == 1


# --------------------------------------------------------------------------- normalize: text


async def test_normalize_text_ignores_punctuation_case_space_does_not():
    items = [{"id": 1, "t": "What is X?"}, {"id": 2, "t": "what is x"}, {"id": 3, "t": "What -- is X!!"}]
    cs = await _out("data.dedupe", {"items": items}, {"key": "t", "normalize": "case_space"})
    assert cs["kept"] == 3  # case_space is unchanged: punctuation still differs
    out = await _out("data.dedupe", {"items": items}, {"key": "t", "normalize": "text"})
    assert [i["id"] for i in out["items"]] == [1]
    assert [(m["index"], m["survivor_index"]) for m in out["matches"]] == [(1, 0), (2, 0)]


async def test_normalize_text_applies_to_against():
    saved = [{"id": "q-1", "t": "How do I book a tour?"}]
    out = await _out(
        "data.dedupe",
        {"items": [{"t": "how do i book a tour"}, {"t": "Is parking free?"}], "against": saved},
        {"key": "t", "normalize": "text"},
    )
    assert [i["t"] for i in out["items"]] == ["Is parking free?"]
    assert [(m["index"], m["against_index"], m["survivor_id"]) for m in out["matches"]] == [(0, 0, "q-1")]


def _prompt_key(text):  # matrx_seo.ai_visibility_design.normalize_prompt, verbatim
    import re
    import unicodedata

    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]+", " ", folded)).strip()


def _quote_key(text):  # brand_discovery.saving.claim_quote_key's quote part (flat ~ whitespace join)
    import re

    return " ".join(re.sub(r"[^\w]+", " ", " ".join(str(text).split()).lower()).split())


PARITY = [
    "What's the best kayak tour in Tampa Bay?",
    "WHAT'S the best kayak tour in Tampa Bay",
    "whats the best kayak tour in tampa bay",  # apostrophe becomes a space: NOT the same, in all three
    "“Free delivery”, on every order — over $50!",
    "Free delivery on every order over 50",
    "Ｆｕｌｌ　width text",  # NFKC: fullwidth letters and the ideographic space
    "full width text",
    "snake_case_prompt?",
    "snake_case_prompt",
    "Café ouvert?",
    "cafe ouvert",  # accents are kept by every one of them: NOT the same
    "tabs\tand\n\nnewlines",
    "tabs and newlines",
]


async def test_normalize_text_groups_exactly_like_the_seo_prompt_and_brand_quote_keys():
    # The seo prompt key is NFKC + casefold + punctuation; the brand quote key is the same minus
    # NFKC (it does not fold fullwidth forms), so the quote key is compared on the cases without them.
    for reference, texts in (
        (_prompt_key, PARITY),
        (_quote_key, [t for t in PARITY if "Ｆ" not in t and t != "full width text"]),
    ):
        out = await _out("data.dedupe", {"items": [{"t": t} for t in texts]}, {"key": "t", "normalize": "text"})
        seen: dict[str, int] = {}
        expected = []
        for i, t in enumerate(texts):
            k = reference(t)
            if k in seen:
                expected.append(i)
            else:
                seen[k] = i
        assert [m["index"] for m in out["matches"]] == expected, reference.__name__
        assert expected, "the parity set must contain duplicates or it proves nothing"
