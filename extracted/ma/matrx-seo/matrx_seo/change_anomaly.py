"""Change-volume anomaly guard — decide whether a crawl's "these pages changed"
result is BELIEVABLE before anything acts on it. Pure logic: no DB, no I/O.

## Why this exists

Run-over-run change detection (content-hash diffing) is the trigger for
expensive downstream work: re-measuring PageSpeed, re-ingesting content,
alerting the user. That makes a FALSE change signal expensive in three ways at
once — wasted quota, wasted money, and a user told their site changed when it
did not.

And the most common large change signal is not a real edit. It is us:

* a dynamic fragment in the hashed content (a CSRF token, a timestamp, a
  rotating testimonial, a cache-buster in an inlined asset URL),
* a template/theme deploy that rewrote every page's shell,
* a crawl that authenticated differently, hit a CDN variant, or got a
  cookie-consent interstitial instead of the page,
* a change to OUR OWN hashing or extraction.

A human editor changing 15 of 500 pages is ordinary. All 500 changing at once
is either a site-wide event worth a human's attention, or our bug — and in
BOTH cases the right move is identical: stop, do not fan out, and tell someone.

## The rule

A changed-ratio alone is not enough: on a 4-page site, 3 changed pages is 75%
and completely normal. So an anomaly requires BOTH a high ratio AND enough
absolute pages to be meaningful, and small sites are exempt from the ratio test
entirely.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Verdict = Literal["normal", "suspicious", "anomalous"]

#: Below this many compared pages, ratios are statistically meaningless — a
#: 4-page site legitimately changes 100% when someone edits it.
MIN_PAGES_FOR_RATIO = 25

#: Fraction of compared pages that must change to be suspicious / anomalous.
SUSPICIOUS_RATIO = 0.40
ANOMALOUS_RATIO = 0.75

#: Absolute floor. Even at a high ratio, this few changed pages is a normal
#: editing session, not a site-wide event.
MIN_CHANGED_FOR_ANOMALY = 20


class ChangeVolumeInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    session_id: str
    #: Pages present in BOTH crawls — the only pages a change verdict can be
    #: computed over. New and removed URLs are reported separately and must
    #: never inflate the changed ratio.
    compared_pages: int
    changed_pages: int
    added_pages: int = 0
    removed_pages: int = 0
    #: The diff could not see the whole site (session hit a page cap), so the
    #: ratio describes a sample, not the site.
    truncated: bool = False

    @property
    def changed_ratio(self) -> float:
        return (self.changed_pages / self.compared_pages) if self.compared_pages else 0.0


class ChangeVolumeAssessment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    site_id: str
    session_id: str
    verdict: Verdict
    changed_pages: int
    compared_pages: int
    changed_ratio: float
    #: The gate every consumer must honor: may downstream work fan out?
    fan_out_allowed: bool
    #: Plain-language, for a non-technical site owner. No jargon, no ratios
    #: without an explanation of what they mean.
    headline: str
    detail: str
    likely_causes: list[str] = Field(default_factory=list)
    truncated: bool = False


def assess_change_volume(payload: ChangeVolumeInput) -> ChangeVolumeAssessment:
    """Classify one crawl's change volume and decide whether work may fan out."""
    ratio = payload.changed_ratio
    compared = payload.compared_pages
    changed = payload.changed_pages
    small_site = compared < MIN_PAGES_FOR_RATIO
    enough_absolute = changed >= MIN_CHANGED_FOR_ANOMALY

    if small_site or not enough_absolute:
        verdict: Verdict = "normal"
    elif ratio >= ANOMALOUS_RATIO:
        verdict = "anomalous"
    elif ratio >= SUSPICIOUS_RATIO:
        verdict = "suspicious"
    else:
        verdict = "normal"

    percent = round(ratio * 100)
    if verdict == "normal":
        headline = f"{changed} page{'s' if changed != 1 else ''} changed since the last check"
        detail = (
            f"{changed} of {compared} pages we compared have new content. "
            "That is a normal amount of editing, so we refreshed their scores."
            if changed
            else "Nothing changed since the last check."
        )
        causes: list[str] = []
    elif verdict == "suspicious":
        headline = f"A large share of this site changed ({percent}% of pages)"
        detail = (
            f"{changed} of {compared} pages look different from last time. That can be "
            "real — a site-wide content update or a redesign — but it is also what we "
            "see when something on every page changes automatically. We have paused the "
            "follow-up work so it does not run against bad information. Please confirm "
            "whether you made a site-wide change."
        )
        causes = _likely_causes()
    else:
        headline = f"Almost this entire site changed at once ({percent}% of pages)"
        detail = (
            f"{changed} of {compared} pages look different from last time. A change that "
            "large is usually not real editing — it normally means something on every "
            "page shifts on its own, or that our reading of the site needs adjusting. "
            "We have stopped here rather than acting on it. Nothing was lost; we just "
            "need a person to confirm what happened before we continue."
        )
        causes = _likely_causes()

    return ChangeVolumeAssessment(
        site_id=payload.site_id,
        session_id=payload.session_id,
        verdict=verdict,
        changed_pages=changed,
        compared_pages=compared,
        changed_ratio=round(ratio, 4),
        # Fail CLOSED: anything but a normal verdict stops the fan-out.
        fan_out_allowed=verdict == "normal",
        headline=headline,
        detail=detail,
        likely_causes=causes,
        truncated=payload.truncated,
    )


def _likely_causes() -> list[str]:
    """Ordered by how often each one is actually the answer."""
    return [
        "Something on every page changes by itself — a date, a rotating quote, "
        "a counter, or an advertisement.",
        "The site's theme or template was updated, which rewrites every page at once.",
        "A real site-wide content update was published.",
        "Our reader saw a different version of the site than usual — for example a "
        "cookie notice, a security check, or a cached copy.",
    ]


__all__ = [
    "ANOMALOUS_RATIO",
    "MIN_CHANGED_FOR_ANOMALY",
    "MIN_PAGES_FOR_RATIO",
    "SUSPICIOUS_RATIO",
    "ChangeVolumeAssessment",
    "ChangeVolumeInput",
    "Verdict",
    "assess_change_volume",
]
