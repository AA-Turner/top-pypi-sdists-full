"""Tests for render_report in rederive_deferral_variants."""

from __future__ import annotations

from tests.scripts.rederive_deferral_variants import rederive


def _result(variant: str = "SP", **kwargs):
    defaults = {
        "prs": 162,
        "rounds_saved": 1569,
        "findings_captured": 407,
        "posted_lost": 455,
        "executable_posted_lost": 0,
    }
    return rederive.VariantResult(variant=variant, **{**defaults, **kwargs})


def _diagnostics(**kwargs):
    defaults = {
        "total_rounds": 4068,
        "total_prs": 399,
        "sp_candidate_rounds": 162,
        "sp_g2_rejected": 23,
        "deferred_entries": 407,
        "non_path_entries": 31,
    }
    return rederive.Diagnostics(**{**defaults, **kwargs})


def test_reports_the_share_of_corpus_for_each_variant() -> None:
    """rounds saved / total rounds is rendered as a percentage."""
    report = rederive.render_report([_result()], _diagnostics())
    assert "| SP | 162 | 1569 | 38.6% | 407 | 455 | 0 |" in report


def test_states_the_g2_rejection_rate_as_a_number() -> None:
    """#3683 requires G2's rejection rate on SP cut rounds to be a stated number."""
    report = rederive.render_report([_result()], _diagnostics())
    assert "**G2 rejection rate on SP cut rounds:** 14.2% (23/162)" in report


def test_states_the_non_path_artefact_rate_as_a_number() -> None:
    """#3683 requires the non-path artefact rate to be a stated number."""
    report = rederive.render_report([_result()], _diagnostics())
    assert "**Non-path artefact rate among deferred entries:** 7.6% (31/407)" in report


def test_reports_net_of_follow_up_at_the_published_band() -> None:
    """Net saving subtracts 2.73 rounds per deferring PR."""
    report = rederive.render_report([_result()], _diagnostics())
    assert "| SP | 1569 | 442 | 1127 | 27.7% |" in report


def test_records_the_corpus_size_and_the_parser_basis() -> None:
    """The report states what it was measured on, so figures are not quotable bare."""
    report = rederive.render_report([_result()], _diagnostics())
    assert "399 merged PRs, 4068 CCR rounds" in report
    assert "G2 applied to every variant" in report


def test_an_empty_corpus_does_not_divide_by_zero() -> None:
    """A corpus with no rounds renders 0.0% rather than raising."""
    empty = rederive.Diagnostics()
    report = rederive.render_report([rederive.VariantResult(variant="SP")], empty)
    assert "| SP | 0 | 0 | 0.0% | 0 | 0 | 0 |" in report
    assert "0.0% (0/0)" in report
