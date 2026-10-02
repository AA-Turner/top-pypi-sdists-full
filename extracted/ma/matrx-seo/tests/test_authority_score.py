"""The Matrx Authority Score's promises, pinned.

The two that matter most are behavioural, not numeric: an unmeasured domain must
never score 0 (it would sort as "worthless" when we simply do not know), and a
score must always be able to explain itself to a human.
"""

from __future__ import annotations

from decimal import Decimal

from matrx_seo.authority_score import (
    AuthorityInputs,
    MatrxAuthorityScore,
    score_authority,
)


def test_no_measurements_is_unmeasured_never_zero() -> None:
    result = score_authority(AuthorityInputs())
    assert result.value is None
    assert result.band is None
    assert result.confidence == "unmeasured"
    assert result.components == []
    assert "unranked rather than low" in result.why
    assert result.is_measured is False


def test_a_spam_score_alone_is_still_unmeasured() -> None:
    # Spam is a penalty on authority, never evidence OF authority. A domain we
    # know only the spam score for has no measured authority at all.
    result = score_authority(AuthorityInputs(spam_score=Decimal(0)))
    assert result.value is None
    assert result.confidence == "unmeasured"


def test_strong_domain_scores_high_and_explains_itself() -> None:
    result = score_authority(
        AuthorityInputs(
            domain_rank=Decimal(750),
            own_referring_domains=12_000,
            own_backlinks=900_000,
            spam_score=Decimal(3),
        )
    )
    assert result.value is not None
    assert result.value >= 70
    assert result.band in {"strong", "exceptional"}
    assert result.confidence == "measured"
    keys = {component.key for component in result.components}
    assert keys == {"domain_rank", "referring_domains", "backlinks", "spam_score"}
    assert result.missing == []
    for component in result.components:
        assert component.why.strip(), "every component must say why in plain words"


def test_weak_domain_scores_low() -> None:
    result = score_authority(
        AuthorityInputs(
            domain_rank=Decimal(40),
            own_referring_domains=3,
            own_backlinks=6,
            spam_score=Decimal(2),
        )
    )
    assert result.value is not None
    assert result.value < 25
    assert result.band in {"low", "minimal"}


def test_spam_cuts_the_score_and_names_the_cut() -> None:
    clean = score_authority(
        AuthorityInputs(
            domain_rank=Decimal(600), own_referring_domains=2_000, spam_score=Decimal(0)
        )
    )
    spammy = score_authority(
        AuthorityInputs(
            domain_rank=Decimal(600), own_referring_domains=2_000, spam_score=Decimal(95)
        )
    )
    assert clean.value is not None and spammy.value is not None
    assert spammy.value < clean.value
    # Measured-and-dangerous must not collapse to the same number as
    # measured-and-worthless.
    assert spammy.value > 0
    assert "spam" in spammy.why.lower()
    penalty = next(c for c in spammy.components if c.key == "spam_score")
    assert penalty.contribution < 0


def test_spam_below_the_free_threshold_costs_nothing() -> None:
    without = score_authority(AuthorityInputs(domain_rank=Decimal(500)))
    with_low_spam = score_authority(
        AuthorityInputs(domain_rank=Decimal(500), spam_score=Decimal(9))
    )
    assert without.value == with_low_spam.value
    penalty = next(c for c in with_low_spam.components if c.key == "spam_score")
    assert penalty.contribution == 0
    assert "clean" in penalty.why.lower()


def test_missing_signals_renormalize_rather_than_punish() -> None:
    """A rank-only domain is scored on its rank, not dragged down by silence.

    The provider genuinely omits link counts on `domain_intersection` responses,
    so punishing absence would systematically mis-rank the single method this
    score was built for.
    """
    rank_only = score_authority(AuthorityInputs(domain_rank=Decimal(800)))
    assert rank_only.value == 80
    assert rank_only.confidence == "partial"
    assert "linking sites" in rank_only.missing
    assert "total links" in rank_only.missing
    assert "approximate" in rank_only.why


def test_score_is_bounded_and_monotonic_in_rank() -> None:
    previous = -1
    for rank in (0, 100, 250, 500, 750, 1000):
        result = score_authority(AuthorityInputs(domain_rank=Decimal(rank), spam_score=Decimal(0)))
        assert result.value is not None
        assert 0 <= result.value <= 100
        assert result.value >= previous
        previous = result.value


def test_link_volume_is_logarithmic_not_linear() -> None:
    """Ten times the links is a bump, not a landslide — otherwise every ordinary
    site collapses into the bottom of the range and the metric cannot do the one
    comparison it exists for."""
    small = score_authority(AuthorityInputs(own_referring_domains=100))
    large = score_authority(AuthorityInputs(own_referring_domains=1_000))
    assert small.value is not None and large.value is not None
    assert large.value > small.value
    assert large.value - small.value < 40


def test_persisted_ranking_never_invents_a_zero_priority() -> None:
    """A gap domain the provider gave us no metrics for must land with a NULL
    priority, not 0 — otherwise it sorts to the bottom as though we had judged
    it, and the user has no way to tell the two apart."""
    from matrx_seo.contracts import LinkGapDomainItem
    from matrx_seo.orm_repository import _authority_ranking

    blind = _authority_ranking(
        LinkGapDomainItem(
            normalized_domain="unknown.example",
            display_domain="unknown.example",
            match_count=3,
        )
    )
    assert "priority_score" not in blind
    assert "priority_reason" not in blind
    assert blind["metadata"]["matrx_authority"]["value"] is None
    assert blind["metadata"]["matrx_authority"]["confidence"] == "unmeasured"

    measured = _authority_ranking(
        LinkGapDomainItem(
            normalized_domain="strong.example",
            display_domain="strong.example",
            match_count=4,
            domain_rank=Decimal(700),
            total_backlinks=50_000,
            spam_score=Decimal(4),
        )
    )
    assert 0 < measured["priority_score"] <= 100
    assert measured["priority_reason"].strip()
    assert measured["metadata"]["matrx_authority"]["components"]


def test_gap_links_to_competitors_are_never_read_as_the_domains_own_profile() -> None:
    """`LinkGapDomainItem.total_backlinks` counts links this domain sends to the
    COMPETITORS. Scoring it as the domain's own link profile is the misfeeding
    trap — it inflates chatty link farms and buries real publishers, and it is
    exactly what a live run against real data did before this was fixed."""
    from matrx_seo.contracts import LinkGapDomainItem
    from matrx_seo.orm_repository import _authority_ranking

    def rank_with(total_backlinks: int) -> int | None:
        return _authority_ranking(
            LinkGapDomainItem(
                normalized_domain="d.example",
                display_domain="d.example",
                match_count=5,
                domain_rank=Decimal(300),
                total_backlinks=total_backlinks,
                spam_score=Decimal(0),
            )
        ).get("priority_score")

    # A farm that fires 100,000 links at the competitors must not outrank a site
    # that sends three — the two are identical in AUTHORITY terms.
    assert rank_with(3) == rank_with(100_000)
    breakdown = _authority_ranking(
        LinkGapDomainItem(
            normalized_domain="d.example",
            display_domain="d.example",
            match_count=5,
            domain_rank=Decimal(300),
            total_backlinks=100_000,
        )
    )["metadata"]["matrx_authority"]
    assert not [c for c in breakdown["components"] if c["key"] == "backlinks"]


def test_out_of_range_spam_is_clamped_not_rejected() -> None:
    result = score_authority(AuthorityInputs(domain_rank=Decimal(500), spam_score=Decimal(140)))
    assert isinstance(result, MatrxAuthorityScore)
    assert result.value is not None
    assert result.value >= 0
