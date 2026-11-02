"""``data.batch`` splits ANY material by count, characters or real tokens — forced.

The 2026-10-26 side-by-side (generic vs custom study kit) found that one call over a
16k-word text used 1 and 5 of 133 terms unique to its last fifth: material that is
not split is not covered. These tests force every split option the step promises,
source-agnostically, including the coverage case itself.
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes.data.collections import BatchConfig, BatchExecutor, plan_batches

pytest.importorskip("tiktoken")


def _words(n: int, tag: str, start: int = 0) -> str:
    return " ".join(f"{tag}{i}" for i in range(start, start + n))


def _plan(items, **config):
    return plan_batches(items, BatchConfig(**config))


# ── back-compat: count mode is exactly the old behaviour ─────────────────────


def test_count_mode_is_the_classic_n_per_batch() -> None:
    out = _plan(list("abcdefg"), size=3)
    assert out.batches == [["a", "b", "c"], ["d", "e", "f"], ["g"]]
    assert (out.count, out.total_items, out.size, out.measure) == (3, 7, 3, "count")
    assert [p.item_count for p in out.parts] == [len(b) for b in out.batches]
    # The items live once, in `batches`; parts carry no copy (attack report I7).
    assert "items" not in out.parts[0].model_dump()


def test_empty_and_tiny() -> None:
    empty = _plan([], size=5, measure="tokens")
    assert (empty.batches, empty.count, empty.parts) == ([], 0, [])
    one = _plan(["word"], size=1000, measure="tokens")
    assert one.batches == [["word"]] and one.parts[0].size == 1


# ── budgets ─────────────────────────────────────────────────────────────────


def test_a_token_budget_is_never_exceeded_and_nothing_is_lost() -> None:
    items = [{"content": _words(40 + (i % 9) * 30, "t", i * 1000), "n": i} for i in range(120)]
    out = _plan(items, size=1200, measure="tokens", text_path="content")
    from matrx_utils.splitting import count_tokens

    for part in out.parts:
        assert part.size <= 1200
        assert part.size == sum(count_tokens(it["content"]) for it in out.batches[part.index])
    assert [it["n"] for b in out.batches for it in b] == list(range(120))


def test_an_oversized_item_is_cut_into_pieces_that_fit() -> None:
    big = {"content": "\n\n".join(_words(50, "p", k * 50) for k in range(40)), "id": "big"}
    out = _plan([{"content": "small", "id": "s"}, big], size=500, measure="chars", text_path="content")
    assert all(p.size <= 500 for p in out.parts)
    pieces = [it for b in out.batches for it in b if it["id"] == "big"]
    assert len(pieces) > 1
    assert " ".join(" ".join(i["content"] for i in pieces).split()) == " ".join(big["content"].split())
    assert any(p.split_items == [1] for p in out.parts)


def test_a_missing_text_path_is_refused_by_name() -> None:
    with pytest.raises(Exception, match="no value at text_path"):
        _plan([{"content": "a"}, {"other": "b"}], size=10, measure="chars", text_path="content")


async def test_the_step_returns_a_named_failure_not_a_crash() -> None:
    result = await BatchExecutor().execute(
        None,  # type: ignore[arg-type]
        BatchExecutor.spec.input_schema(items=[{"x": 1}]),  # type: ignore[call-arg]
        BatchConfig(size=10, measure="chars", text_path="content"),
    )
    assert result.error.code == "batch_text_missing"  # type: ignore[union-attr]


# ── natural cuts, keys, overlap ─────────────────────────────────────────────


def _pages(sections: list[tuple[str, int]], words_per_page: int = 200) -> list[dict]:
    pages, n = [], 0
    for title, count in sections:
        for k in range(count):
            pages.append(
                {
                    "content": (f"# {title}\n" if k == 0 else "") + _words(words_per_page, f"{title[:1]}", n * 1000),
                    "section_title": title,
                    "page": n + 1,
                    "is_continuation": False,
                }
            )
            n += 1
    return pages


def test_batches_cut_back_to_a_section_start_when_it_stays_half_full() -> None:
    pages = _pages([("Alpha", 3), ("Beta", 4), ("Gamma", 3)])
    out = _plan(pages, size=6000, measure="chars", text_path="content", prefer_cut_on=["section_title"])
    # Each page ~1500 chars: a batch holds 4 pages; the Beta start (page 4) is a natural cut.
    assert out.batches[0][-1]["section_title"] == "Alpha"
    assert out.parts[0].ended_by == "natural"
    assert out.batches[1][0]["section_title"] == "Beta"


def test_headings_alone_mark_natural_cuts() -> None:
    pages = _pages([("Alpha", 3), ("Beta", 4)])
    out = _plan(pages, size=6000, measure="chars", text_path="content", prefer_cut_at_headings=True)
    assert out.batches[1][0]["content"].startswith("# Beta")


def test_never_cross_keeps_sources_apart_and_continuation_joins() -> None:
    items = [{"t": "x" * 10, "src": "A"}] * 3 + [{"t": "y" * 10, "src": "B"}] * 3
    out = _plan(items, size=1000, measure="chars", text_path="t", never_cross=["src"])
    assert [{i["src"] for i in b} for b in out.batches] == [{"A"}, {"B"}]
    assert out.parts[0].ended_by == "forced"

    pages = [
        {"t": "a" * 10, "kind": "note", "cont": False},
        {"t": "b" * 10, "kind": "letter", "cont": True},
        {"t": "c" * 10, "kind": "letter", "cont": False},
        {"t": "d" * 10, "kind": "bill", "cont": False},
    ]
    out = _plan(pages, size=1000, measure="chars", text_path="t", never_cross=["kind"], continues_path="cont")
    assert [len(b) for b in out.batches] == [3, 1]


def test_overlap_repeats_items_but_never_across_a_key() -> None:
    items = [{"n": i, "src": "A" if i < 6 else "B"} for i in range(10)]
    out = _plan(items, size=4, overlap=1, never_cross=["src"])
    assert [[i["n"] for i in b] for b in out.batches] == [[0, 1, 2, 3], [3, 4, 5], [6, 7, 8, 9]]
    assert [p.overlap_count for p in out.parts] == [0, 1, 0]


# ── folding, quotas, ids, labels ────────────────────────────────────────────


def test_max_batches_folds_evenly_within_each_key() -> None:
    items = [{"n": i, "src": "A" if i < 12 else "B"} for i in range(16)]
    out = _plan(items, size=2, never_cross=["src"], max_batches=3)
    assert out.count == 3
    for b in out.batches:
        assert len({i["src"] for i in b}) == 1
    assert [i["n"] for b in out.batches for i in b] == list(range(16))


def test_more_keys_than_max_batches_is_said_not_hidden() -> None:
    items = [{"n": i, "src": str(i)} for i in range(5)]
    out = _plan(items, size=10, never_cross=["src"], max_batches=2)
    assert out.count == 5
    assert any("never_cross" in n for n in out.notes)


def test_quota_is_shared_by_size_and_sums_exactly() -> None:
    sizes = [200, 1200, 400, 2000]
    items = [{"content": "x" * s} for s in sizes]
    out = _plan(items, size=2000, measure="chars", text_path="content", quota_total=15)
    assert out.quota_total == 15
    assert sum(p.quota for p in out.parts) == 15
    assert all(p.quota >= 1 for p in out.parts)

    tight = _plan([{"c": "x"}] * 6, size=1, quota_total=3)
    assert tight.quota_total == 6 and tight.notes  # each batch needs one: said, not hidden


def test_ids_are_stable_and_labels_name_the_span() -> None:
    pages = _pages([("Alpha", 2), ("Beta", 2)], words_per_page=20)
    a = _plan(pages, size=2, label_path="section_title", id_path="page")
    b = _plan([dict(p) for p in pages], size=2, label_path="section_title", id_path="page")
    assert [p.id for p in a.parts] == [p.id for p in b.parts]
    assert len({p.id for p in a.parts}) == len(a.parts)
    assert [p.label for p in a.parts] == ["Alpha", "Beta"]
    mixed = _plan(pages, size=3, label_path="section_title")
    assert mixed.parts[0].label == "Alpha – Beta"
    dup = _plan(["same", "same"], size=1)
    assert dup.parts[0].id != dup.parts[1].id


# ── the coverage case and the huge case ─────────────────────────────────────


def test_a_16k_word_text_gives_every_fifth_its_share() -> None:
    """The side-by-side failure, inverted: a 16k-word text in five sections of unique
    terms, split by tokens at section starts with 15 questions to share. Every
    section is in a batch, every batch is asked for at least one question, and the
    last fifth gets its proportional share — not 1 of 133."""
    sections = [(f"Section{k}", 16) for k in range(5)]  # 80 pages × 200 words = 16k words
    pages = _pages(sections)
    assert sum(len(p["content"].split()) for p in pages) >= 16_000
    out = _plan(
        pages,
        size=6000,
        measure="tokens",
        text_path="content",
        prefer_cut_on=["section_title"],
        quota_total=15,
        label_path="section_title",
    )
    covered = [it["page"] for b in out.batches for it in b]
    assert covered == list(range(1, 81)), "a page was dropped or repeated"
    assert all(p.quota >= 1 for p in out.parts)
    last_fifth = [p for p in out.parts if any(it["section_title"] == "Section4" for it in out.batches[p.index])]
    assert last_fifth, "the last fifth has no batch"
    assert sum(p.quota for p in last_fifth) >= 2  # 15 × 1/5 = 3, rounding aside
    # Natural cuts held: a batch cut back to a natural division hands the next one a section start.
    natural = [i for i, p in enumerate(out.parts[:-1]) if p.ended_by == "natural"]
    assert natural, "no batch was cut at a section start"
    assert all(out.batches[i + 1][0]["content"].startswith("# ") for i in natural)


def test_500k_tokens_of_mixed_sources_split_by_tokens_never_mixing_sources() -> None:
    items = []
    for src in ("pdf", "video", "scrape", "table", "json"):
        for k in range(1100):
            items.append({"content": _words(90, src[:2], k * 100), "source_id": src})
    out = _plan(items, size=8000, measure="tokens", text_path="content", never_cross=["source_id"], quota_total=40)
    assert sum(p.size for p in out.parts) > 500_000
    assert all(p.size <= 8000 for p in out.parts)
    for b in out.batches:
        assert len({i["source_id"] for i in b}) == 1
    assert {b[0]["source_id"] for b in out.batches} == {"pdf", "video", "scrape", "table", "json"}
    assert out.quota_total == 40 or out.notes


def test_folding_keeps_equal_sections_equal_and_says_when_a_batch_runs_over() -> None:
    """Live proof 2026-10-26: folding by COUNT merged the early sections' batches and left the
    last fifth unmerged, so it took 5 of 15 questions. Folding balances by size."""
    items = [
        {"content": f"# Section{k}\n\n" + " ".join(f"s{k}t{i}." for i in range(3200)), "section_title": f"Section{k}"}
        for k in range(5)
    ]
    out = _plan(
        items,
        size=4000,
        measure="tokens",
        text_path="content",
        prefer_cut_on=["section_title"],
        quota_total=15,
        max_batches=15,
    )
    share = {}
    for p in out.parts:
        titles = [it["section_title"] for it in out.batches[p.index]]
        for t in set(titles):
            share[t] = share.get(t, 0) + p.quota * titles.count(t) / len(titles)
    assert all(2 <= v <= 4 for v in share.values()), share
    if any(p.size > 4000 for p in out.parts):
        assert any("over the size budget" in n for n in out.notes)


# ── second attack pass: the surviving mutants, killed ───────────────────────


def test_quota_follows_new_material_not_repeated_overlap() -> None:
    """C2: an overlap item repeated at a batch's start is not that batch's material."""
    out = _plan(list("abcde"), size=2, overlap=1, quota_total=10)
    assert [b for b in out.batches] == [["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"]]
    assert [p.quota for p in out.parts] == [4, 2, 2, 2]


def test_quota_lands_on_the_batch_that_earned_it() -> None:
    """C4: the largest batch gets the largest quota, in place — never mirrored."""
    items = [{"content": "x" * s, "k": i} for i, s in enumerate((200, 1200, 400, 2000))]
    out = _plan(
        items, size=2000, measure="chars", text_path="content", never_cross=["k"], quota_total=15
    )
    assert out.count == 4
    sizes = [p.size for p in out.parts]
    quotas = [p.quota for p in out.parts]
    assert sorted(range(4), key=lambda i: sizes[i]) == sorted(range(4), key=lambda i: quotas[i])
    assert quotas[3] > quotas[0]


def test_a_batch_id_comes_from_its_items_not_its_position() -> None:
    """C3: putting a new item first must not rename every later batch."""
    before = _plan(["x", "y", "z"], size=1)
    after = _plan(["w", "x", "y", "z"], size=1)
    assert [p.id for p in after.parts[1:]] == [p.id for p in before.parts]


def test_folding_never_repeats_an_overlap_item_inside_a_batch() -> None:
    """C8: folded neighbours share their overlap once, not twice."""
    out = _plan(list("abcdefghij"), size=2, overlap=1, max_batches=3)
    assert out.count == 3
    for batch in out.batches:
        assert len(batch) == len(set(batch)), batch
    fresh = [it for p, b in zip(out.parts, out.batches, strict=True) for it in b[p.overlap_count :]]
    assert fresh == list("abcdefghij")


def test_empty_sections_get_no_quota() -> None:
    """Finding 10: quota_min_each=1 handed a question to a section with no text."""
    items = [
        {"content": "word " * 300, "s": "A"},
        {"content": "", "s": "B"},
        {"content": "word " * 300, "s": "C"},
    ]
    out = _plan(
        items, size=4000, measure="chars", text_path="content", never_cross=["s"], quota_total=6
    )
    assert [p.quota for p in out.parts] == [3, 0, 3]
    assert out.quota_total == 6


def test_an_id_path_missing_on_items_is_said() -> None:
    """Finding 10: ids silently fell back to position when id_path was absent."""
    out = _plan([{"page": 1}, {"other": 2}], size=1, id_path="page")
    assert any("no value at id_path 'page'" in n for n in out.notes)
    assert not any("id_path" in n for n in _plan([{"page": 1}], size=1, id_path="page").notes)
