"""Tests for measure_corpus in rederive_deferral_variants."""

from __future__ import annotations

from tests.scripts.rederive_deferral_variants import (
    posted_body,
    record,
    rederive,
    round_,
    suppressed_body,
)


def test_pairs_each_record_with_its_rounds_metrics() -> None:
    """Metrics stay in round order and stay attached to their own record."""
    first = record(round_(body=suppressed_body("specs/1/spec.md")), number=1)
    second = record(
        round_(review_id=1, body=posted_body(1), posted_paths=("specs/2/spec.md",)),
        round_(review_id=2, body=suppressed_body("specs/2/spec.md", "specs/2/plan.md")),
        number=2,
    )

    measured = rederive.measure_corpus([first, second])

    assert [rec.number for rec, _ in measured] == [1, 2]
    assert [len(metrics) for _, metrics in measured] == [1, 2]
    assert measured[1][1][0].posted_count == 1
    assert measured[1][1][1].extracted_paths == ("specs/2/spec.md", "specs/2/plan.md")


def test_an_empty_corpus_measures_to_nothing() -> None:
    """No records means no work and no output rows."""
    assert rederive.measure_corpus([]) == []


def test_measuring_once_matches_measuring_per_round() -> None:
    """The shared parse is the same parse each consumer would have done itself."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md")))

    ((_, metrics),) = rederive.measure_corpus([rec])

    assert metrics == [rederive.measure_round(rec.rounds[0])]
