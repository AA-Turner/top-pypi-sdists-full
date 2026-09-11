"""Fact-check archive kinds — what the world's fact-checkers already published.

Why a kind and not a dict: *"Is there anything on Snopes related to this?"* is
the Verification Handbook's cheapest and most-skipped move, and its answer has
to be actionable — a desk renders the reviews, an agent quotes a rating back,
a workflow branches on whether anything was found at all. A shape with no
identity can do none of that.

ONE kind per capability, shared by the workflow node and the agent tool — the
precedent ``media_forensics`` set for the image-verification pair.
``aidream/graph_actions/web/factcheck.py`` imports ``FactCheckReviewSet`` as its
node ``output_schema``, ``aidream/services/fact_check/service.py`` builds it,
and the ``factcheck_search`` agent tool returns it, so node, tool and published
registry row cannot drift apart.

It lives in the package, not in ``aidream/kinds/``, because the TOOL
implementation imports it and a package never imports aidream
(``scripts/check_package_boundaries.py``).

``FactCheckReview`` is a ``KindSubModel``: a single review has no meaning apart
from the search that produced it, and minting a slug for every nested object is
how a family ends up with a hundred kinds.

**Zero results is a first-class SUCCESS, and the shape says so out loud.**
``review_count == 0`` with a ``summary`` that states plainly that no fact-checker
has published on this claim is a real, useful answer — never an error, and never
to be read as "the claim is true". ``searched_reviewers_note`` keeps the reader
honest about what that silence does and does not mean.

Publish with::

    uv run python scripts/publish_kind_catalog.py matrx_ai.tools.kinds.fact_check --apply
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind
from pydantic import Field


class FactCheckReview(KindSubModel):
    """One published ClaimReview: a claim, and what a fact-checker made of it."""

    claim_text: str = Field(default="", description="The claim as the fact-checker stated it.")
    claimant: str = Field(
        default="",
        description="Who made the claim, as recorded by the fact-checker (person, outlet, or 'Facebook posts').",
    )
    claim_date: str | None = Field(
        default=None,
        description="When the claim was made, ISO-8601, when the reviewer recorded it.",
    )
    publisher_name: str = Field(
        default="",
        description="The fact-checking organisation, e.g. 'Snopes.com' or 'Lead Stories'.",
    )
    publisher_site: str = Field(
        default="", description="The fact-checker's site, e.g. 'snopes.com'."
    )
    review_title: str = Field(default="", description="Headline of the published review.")
    textual_rating: str = Field(
        default="",
        description=(
            "The reviewer's own verdict in their own words — 'False', 'Fake News', "
            "'Mostly True', 'Originally Satire'. Ratings are NOT comparable across "
            "publishers; quote them, never normalise them."
        ),
    )
    review_url: str = Field(default="", description="Direct link to the published review.")
    review_date: str | None = Field(
        default=None, description="When the review was published, ISO-8601."
    )
    language_code: str = Field(
        default="", description="BCP-47 language code of the review, e.g. 'en'."
    )


@kind(
    "fact_check_review_set",
    label="Fact-Check Reviews",
    family="verification",
    # A REAL measured payload, captured from the Google Fact Check Tools API
    # ClaimReview corpus. An invented example is a lie about what this looks like.
    example={
        "__kind": "fact_check_review_set",
        "claim": "bear carried injured raccoon to wildlife center",
        "review_count": 1,
        "reviews": [
            {
                "claim_text": "A bear carried an injured raccoon to a wildlife center.",
                "claimant": "Facebook posts",
                "claim_date": "2026-09-08",
                "publisher_name": "Lead Stories",
                "publisher_site": "leadstories.com",
                "review_title": "Fact Check: Bear Did NOT Carry Injured Raccoon To Wildlife Center",
                "textual_rating": "AI Generated",
                "review_url": "https://leadstories.com/hoax-alert/2026/09/fact-check-bear-raccoon.html",
                "review_date": "2026-09-10",
                "language_code": "en",
            }
        ],
        "summary": "1 published fact-check matches this claim.",
        "searched_reviewers_note": (
            "Covers the ClaimReview corpus Google indexes — Snopes, Lead Stories, AFP, "
            "Reuters, PolitiFact, Full Fact and hundreds more. Finding nothing means no "
            "indexed fact-checker has published on this claim; it is not evidence the "
            "claim is true."
        ),
    },
    # DISTILLED — `review_count` is the load-bearing field: a surface must render
    # "nobody has checked this" differently from "three people rated it false",
    # and a lookup that failed differently from both (that is a node Failure, not
    # a zero here). `textual_rating` is deliberately the publisher's raw wording.
    maturity="distilled",
)
class FactCheckReviewSet(KindModel):
    """Every published fact-check the ClaimReview corpus holds for one claim."""

    claim: str = Field(description="The claim text that was searched for.")
    review_count: int = Field(
        default=0,
        ge=0,
        description=(
            "How many published reviews matched. ZERO is a legitimate answer — it means "
            "no indexed fact-checker has written about this claim, NOT that the claim is true."
        ),
    )
    reviews: list[FactCheckReview] = Field(
        default_factory=list, description="The matching published reviews, most relevant first."
    )
    summary: str = Field(
        description="One plain-English sentence stating what the search found, including when it found nothing."
    )
    searched_reviewers_note: str = Field(
        description="What corpus was searched, and what a zero result does and does not prove."
    )


FACT_CHECK_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "factcheck_search": FactCheckReviewSet,
}


__all__ = [
    "FACT_CHECK_TOOL_RESULT_KINDS",
    "FactCheckReview",
    "FactCheckReviewSet",
]
