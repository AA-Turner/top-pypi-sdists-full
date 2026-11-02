"""Guard: a floor that would drop EVERY passage keeps the best few as weak; one text stored twice shows once.

Live 2026-10-24 (Memory search): the cross-encoder graded "Ava's ions test" at 0.56 and "ions test Ava's"
at 0.67 against a 0.45 floor in one case and below it in another — the all-or-nothing gate decided between
0 and 20 rows, so the same notes appeared and vanished with word order. And the same text stored as a PDF
and as the notes derived from it came back twice.

  (c) when recall found passages but the floor drops them ALL, a caller that asks (``keep_weak``) gets the
      best N back, each marked ``weak``, and the verdict says so; a caller that does not ask keeps the
      honest empty result (agents, feedback 2985b3aa);
  (d) a passage whose text is (nearly) contained in a better-ranked passage of ANOTHER source collapses
      into it, and the kept hit names the other as ``also_in``.
"""

from __future__ import annotations

from matrx_rag.search import (
    RELEVANCE_VERDICT_NONE,
    RELEVANCE_VERDICT_SCORED,
    RELEVANCE_VERDICT_WEAK,
    _apply_relevance_floor,
    _collapse_cross_source_duplicates,
    _keep_weak_matches,
)

TEXT = (
    "Ava ran the ions test on Tuesday: sodium and chloride ions were measured in the brine sample, "
    "the conductivity rose with temperature, and the result matched the expected curve for the lab."
)


def _row(source_id: str, text: str, doc: str | None = None, kind: str = "note") -> dict:
    return {
        "source_kind": kind,
        "source_id": source_id,
        "processed_document_id": doc,
        "content_text": text,
        "chunk_kind": "child",
        "derivation_kind": "initial_extract",
        "source_name": f"name-{source_id}",
    }


class TestWeakMatches:
    def test_floor_dropping_everything_keeps_the_best_few_marked_weak(self):
        ordered = [f"c{i}" for i in range(12)]
        scores = {cid: 0.40 - i * 0.01 for i, cid in enumerate(ordered)}
        kept, verdict, floor, _ = _apply_relevance_floor(ordered, scores, floor=0.45, limit=20)
        assert kept == [] and verdict == RELEVANCE_VERDICT_NONE
        out, verdict2, weak = _keep_weak_matches(ordered, kept, verdict, keep_weak=5)
        assert out == ordered[:5]
        assert weak == set(ordered[:5])
        assert verdict2 == RELEVANCE_VERDICT_WEAK

    def test_a_caller_that_does_not_ask_keeps_the_honest_empty_result(self):
        ordered = ["a", "b"]
        out, verdict, weak = _keep_weak_matches(ordered, [], RELEVANCE_VERDICT_NONE, keep_weak=0)
        assert out == [] and verdict == RELEVANCE_VERDICT_NONE and weak == set()

    def test_a_passing_result_is_never_marked_weak(self):
        out, verdict, weak = _keep_weak_matches(["a", "b"], ["a"], RELEVANCE_VERDICT_SCORED, keep_weak=5)
        assert out == ["a"] and verdict == RELEVANCE_VERDICT_SCORED and weak == set()


class TestCrossSourceDuplicates:
    def test_the_same_text_in_a_pdf_and_a_derived_note_shows_once_naming_the_other(self):
        rows = {
            "pdf": _row("file-1", TEXT, doc="doc-1", kind="cld_file"),
            "note": _row("note-9", "## Lab notes\n\n" + TEXT + "\n"),
            "other": _row("note-2", "A different passage about the quarterly budget review and the hiring plan for spring."),
        }
        ordered, also_in = _collapse_cross_source_duplicates(["pdf", "other", "note"], rows)
        assert ordered == ["pdf", "other"]
        assert also_in == {"pdf": ["note"]}

    def test_two_different_passages_of_different_sources_both_stay(self):
        rows = {
            "a": _row("s1", TEXT),
            "b": _row("s2", "Completely unrelated: the garden needs watering twice a week through the summer months."),
        }
        ordered, also_in = _collapse_cross_source_duplicates(["a", "b"], rows)
        assert ordered == ["a", "b"] and also_in == {}

    def test_same_source_is_left_to_the_existing_dedup(self):
        rows = {"a": _row("s1", TEXT), "b": _row("s1", TEXT + " More.")}
        ordered, also_in = _collapse_cross_source_duplicates(["a", "b"], rows)
        assert ordered == ["a", "b"] and also_in == {}
