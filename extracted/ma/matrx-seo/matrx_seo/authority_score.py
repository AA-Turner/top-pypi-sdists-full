"""The Matrx Authority Score — our own answer to "is this link worth chasing?".

Every prospecting tool in this category sorts opportunities by an authority
metric, and every one of them sorts by somebody else's: Ahrefs DR, Moz DA,
Majestic Trust Flow. We cannot.

🚨 **THE LICENSE WALL — this is why this module exists and it is not negotiable.**
Ahrefs' Domain Rating license explicitly prohibits reselling or embedding DR into
a competing product (ahrefs.com/legal/domain-rating-license); Majestic sits in the
same category. **No Ahrefs, Majestic, Moz or SEMrush value may ever reach this
function, be stored beside its output, or be shown as OUR metric.** A user's own
BYO API key showing their own licensed data back to only them is a different
feature and does not live here (project decision D3).

DataForSEO — which we already pay for, per call, on every backlink and gap run —
publishes no DR-equivalent single score. It publishes the *primitives* the score
is made of, and it means them to be composited. So we composite them ourselves,
and the result is ours to sort, filter, explain and ship.

**Three properties that make this better than the thing it replaces, not merely
legal:**

1. **It explains itself.** Every component reports the raw value it saw, the
   points it contributed, and one sentence of prose a non-technical expert can
   read. A number with no "why" is a dead end (THE DOOR LAW).
2. **Unmeasured is NEVER zero.** A domain the provider returned no metrics for
   scores ``None``, not ``0`` — a zero sorts to the bottom as though we had
   measured it and found it worthless, which is a lie the user cannot see
   through. ``confidence`` says exactly how much evidence stood behind the
   number.
3. **It is a pure function of plain values.** No DB, no network, no AI, no host
   imports — so every prospecting method (competitor gap, SERP, resource pages,
   broken links, CSV import) scores on the SAME scale, and the scale is
   trivially testable.

Consumers rank with it; they never filter with it silently. Per the human-gate
rule that governs all of prospecting, a score ORDERS a list — only a human
removes a row from it.
"""

from __future__ import annotations

import math
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

AuthorityBand = Literal["exceptional", "strong", "moderate", "low", "minimal"]
AuthorityConfidence = Literal["measured", "partial", "unmeasured"]

#: DataForSEO's ``rank`` is a 0-1000 logarithmic domain-strength metric. It is
#: the single most informative primitive available, so it carries the most
#: weight — but never all of it, because a rank alone cannot tell a genuinely
#: linked-to site from an old domain with a good history.
WEIGHT_RANK = 0.55
#: How many distinct sites link to it. The closest thing to editorial consensus.
WEIGHT_REFERRING_DOMAINS = 0.30
#: Raw backlink volume. Weakest of the three on purpose: it is the easiest of
#: the three to manufacture, and a site with 2M links from 40 domains is a
#: network, not an authority.
WEIGHT_BACKLINKS = 0.15

#: Spam below this is treated as clean. DataForSEO's spam score is noisy at the
#: bottom of its range and penalising an 8 would demote ordinary real sites.
SPAM_FREE_THRESHOLD = Decimal(10)
#: The most a spam signal may cut a score. A fully-spammy domain keeps a small
#: residue rather than collapsing to zero, because zero is reserved for
#: "measured and worthless" and this is "measured and dangerous" — a different
#: sentence for the user, and one the band + prose must be able to say.
MAX_SPAM_PENALTY = 0.85

#: 🚨 PROVISIONAL — these weights, thresholds and band edges have NOT been
#: validated against human rulings, because none exist yet for link prospects.
#: They follow the same rule as the competitor-classification thresholds
#: (`competitor_classification._BAND_THRESHOLDS`): a scoring constant is
#: re-derived from real human decisions corpus-wide, never tuned against one
#: account. The moment ``seo.link_gap_domain.human_ruling`` carries approvals and
#: rejections, re-derive these against them — that is what the review gate is
#: collecting.
_BAND_EDGES: tuple[tuple[int, AuthorityBand], ...] = (
    (80, "exceptional"),
    (60, "strong"),
    (40, "moderate"),
    (20, "low"),
)


class AuthorityInputs(BaseModel):
    """The DataForSEO primitives the score is composited from.

    🚨 **THE MISFEEDING TRAP — read this before wiring a new caller.** Backlink
    tables carry two completely different families of number that share the same
    field names, and mixing them silently produces a confident, wrong score:

    * **The domain's OWN authority** — how strong that site is on the open web.
      This is what belongs here.
    * **The LINK RELATIONSHIP** — how many links that site sends *to a specific
      target*, and how strong those particular links are. This does NOT belong
      here.

    Measured live 2026-08-15: `seo.backlink_dimension_snapshot` rows for
    ``dimension_kind='referring_domain'`` carry `backlinks=38`,
    `referring_domains=2`, `rank_score=42` for **ocregister.com** — a major
    regional newspaper. Those are relationship numbers (38 links to *us*, from 2
    IPs). Feeding them here scored the Orange County Register 10/100, below
    several link farms. The same domain's own rank lives in
    `seo.referring_domain_profile.provider_metrics.domain_rank`.

    The ``own_`` prefixes exist so that this mistake reads as wrong at the call
    site instead of compiling quietly. Every field is optional because the
    provider genuinely omits them, and an omitted field is handled honestly
    (see ``confidence``) rather than guessed at.
    """

    model_config = ConfigDict(extra="forbid")

    #: DataForSEO ``rank`` for the DOMAIN ITSELF — 0-1000.
    domain_rank: Decimal | None = None
    #: How many distinct sites link to THIS domain, across the whole web.
    #: Never "how many links it sends us".
    own_referring_domains: int | None = None
    #: Total inbound links to THIS domain, across the whole web.
    own_backlinks: int | None = None
    #: DataForSEO spam score — 0-100.
    spam_score: Decimal | None = None


class AuthorityComponent(BaseModel):
    """One measured signal's contribution, in the user's language."""

    model_config = ConfigDict(extra="forbid")

    key: Literal["domain_rank", "referring_domains", "backlinks", "spam_score"]
    label: str
    raw: float | None
    #: 0-100 on this component's own scale, before weighting.
    normalized: float | None
    #: Points this component put into (or took out of) the final score.
    contribution: float
    why: str


class MatrxAuthorityScore(BaseModel):
    """The composite, and everything needed to defend it to a human."""

    model_config = ConfigDict(extra="forbid")

    #: 0-100, or ``None`` when nothing measurable came back. NEVER 0 for absent
    #: data — see the module docstring.
    value: int | None
    band: AuthorityBand | None
    confidence: AuthorityConfidence
    components: list[AuthorityComponent] = Field(default_factory=list)
    #: Which inputs the provider did not give us, named for the UI.
    missing: list[str] = Field(default_factory=list)
    #: One sentence, written for a non-technical subject-matter expert.
    why: str

    @property
    def is_measured(self) -> bool:
        return self.value is not None


def _log_scale(value: int, *, per_decade: float) -> float:
    """Map a count onto 0-100 logarithmically.

    Link counts span six orders of magnitude, so a linear scale would put every
    ordinary site in the bottom 1% and make the metric useless for exactly the
    comparison it exists to serve.
    """
    if value <= 0:
        return 0.0
    return min(100.0, math.log10(float(value) + 1.0) * per_decade)


def _clamp_percent(value: float) -> float:
    return max(0.0, min(100.0, value))


def _band_for(value: int) -> AuthorityBand:
    for edge, band in _BAND_EDGES:
        if value >= edge:
            return band
    return "minimal"


def _format_count(value: float) -> str:
    count = int(value)
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M".replace(".0M", "M")
    if count >= 1_000:
        return f"{count / 1_000:.1f}k".replace(".0k", "k")
    return str(count)


def _sites_link_phrase(count: int) -> str:
    return "1 site links to it" if count == 1 else f"{_format_count(count)} sites link to it"


def score_authority(inputs: AuthorityInputs) -> MatrxAuthorityScore:
    """Composite the Matrx Authority Score for one domain.

    Weighted signals are renormalized over the signals that are actually
    present, so a domain with a rank but no link counts is scored on its rank
    rather than punished for the provider's silence — with ``confidence``
    telling the user that is what happened.
    """
    components: list[AuthorityComponent] = []
    missing: list[str] = []
    weighted_total = 0.0
    weight_present = 0.0

    if inputs.domain_rank is not None:
        rank = _clamp_percent(float(inputs.domain_rank) / 10.0)
        weighted_total += rank * WEIGHT_RANK
        weight_present += WEIGHT_RANK
        components.append(
            AuthorityComponent(
                key="domain_rank",
                label="Domain strength",
                raw=float(inputs.domain_rank),
                normalized=round(rank, 1),
                contribution=round(rank * WEIGHT_RANK, 1),
                why=(
                    f"Rated {int(inputs.domain_rank)} out of 1000 for overall link strength"
                    if rank >= 40
                    else f"Rated only {int(inputs.domain_rank)} out of 1000 for link strength"
                ),
            )
        )
    else:
        missing.append("domain strength")

    if inputs.own_referring_domains is not None:
        # 100 linking domains ≈ 50 points, 10,000 ≈ 100 — the shape practitioners
        # already reason in.
        referring = _log_scale(inputs.own_referring_domains, per_decade=25.0)
        weighted_total += referring * WEIGHT_REFERRING_DOMAINS
        weight_present += WEIGHT_REFERRING_DOMAINS
        components.append(
            AuthorityComponent(
                key="referring_domains",
                label="Sites linking to it",
                raw=float(inputs.own_referring_domains),
                normalized=round(referring, 1),
                contribution=round(referring * WEIGHT_REFERRING_DOMAINS, 1),
                why=_sites_link_phrase(inputs.own_referring_domains),
            )
        )
    else:
        missing.append("linking sites")

    if inputs.own_backlinks is not None:
        volume = _log_scale(inputs.own_backlinks, per_decade=18.0)
        weighted_total += volume * WEIGHT_BACKLINKS
        weight_present += WEIGHT_BACKLINKS
        components.append(
            AuthorityComponent(
                key="backlinks",
                label="Total links",
                raw=float(inputs.own_backlinks),
                normalized=round(volume, 1),
                contribution=round(volume * WEIGHT_BACKLINKS, 1),
                why=f"{_format_count(inputs.own_backlinks)} links point to it in total",
            )
        )
    else:
        missing.append("total links")

    if weight_present == 0.0:
        return MatrxAuthorityScore(
            value=None,
            band=None,
            confidence="unmeasured",
            components=[],
            missing=missing,
            why=(
                "We have no authority measurements for this domain yet, so it is "
                "unranked rather than low — judge it on the other evidence."
            ),
        )

    base = weighted_total / weight_present

    penalty_multiplier = 1.0
    if inputs.spam_score is not None:
        spam = max(Decimal(0), min(Decimal(100), inputs.spam_score))
        if spam > SPAM_FREE_THRESHOLD:
            over = float(spam - SPAM_FREE_THRESHOLD) / float(Decimal(100) - SPAM_FREE_THRESHOLD)
            penalty_multiplier = 1.0 - (over * MAX_SPAM_PENALTY)
        lost = base - (base * penalty_multiplier)
        components.append(
            AuthorityComponent(
                key="spam_score",
                label="Spam signals",
                raw=float(spam),
                normalized=round(100.0 - float(spam), 1),
                contribution=-round(lost, 1),
                why=(
                    "Spam signals are clean"
                    if spam <= SPAM_FREE_THRESHOLD
                    else f"Carries a spam score of {int(spam)} out of 100, which cuts its value"
                ),
            )
        )
    else:
        missing.append("spam signals")

    value = int(round(_clamp_percent(base * penalty_multiplier)))
    band = _band_for(value)
    measured_signals = len([c for c in components if c.key != "spam_score"])
    confidence: AuthorityConfidence = (
        "measured" if measured_signals >= 2 and inputs.spam_score is not None else "partial"
    )

    return MatrxAuthorityScore(
        value=value,
        band=band,
        confidence=confidence,
        components=components,
        missing=missing,
        why=_prose(value, band, inputs, penalty_multiplier, confidence),
    )


def _prose(
    value: int,
    band: AuthorityBand,
    inputs: AuthorityInputs,
    penalty_multiplier: float,
    confidence: AuthorityConfidence,
) -> str:
    lead = {
        "exceptional": "One of the strongest sites you could earn a link from",
        "strong": "A strong site worth real effort",
        "moderate": "A solid, ordinary site — worth contacting",
        "low": "A weak site; contact it only if it is a close topical fit",
        "minimal": "Very little link value here",
    }[band]

    facts: list[str] = []
    if inputs.own_referring_domains is not None:
        facts.append(_sites_link_phrase(inputs.own_referring_domains))
    if inputs.domain_rank is not None:
        facts.append(f"link strength {int(inputs.domain_rank)}/1000")
    detail = f" ({', '.join(facts)})" if facts else ""

    spam_note = ""
    if penalty_multiplier < 1.0:
        spam_note = (
            f" Its spam signals cut the score by {int(round((1.0 - penalty_multiplier) * 100))}%."
        )

    confidence_note = ""
    if confidence == "partial":
        confidence_note = " Some measurements were unavailable, so treat this as approximate."

    return f"{lead}{detail}. Scored {value}/100.{spam_note}{confidence_note}"


__all__ = [
    "AuthorityBand",
    "AuthorityComponent",
    "AuthorityConfidence",
    "AuthorityInputs",
    "MatrxAuthorityScore",
    "score_authority",
]
