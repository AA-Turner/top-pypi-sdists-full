"""Competitor classification — the deterministic layer.

System of record: ``common-docs/systems/marketing/competitor-classification/FEATURE.md``.

**Arman's ruling, 2026-08-14:** *"This is not things that we wanna guess about...
We want true competitors."* Classification runs in three layers, in this order:

1. **This module — deterministic, zero tokens, zero AI.** A maintained universal
   registry plus TLD/pattern rules settles the cases that are not judgment calls
   at all: Wikipedia is a reference site, Reddit is a community, ``*.gov`` is not
   anyone's business competitor. Machines are strictly better than agents here,
   and free.
2. **An AI classifier** for everything layer 1 leaves ``None`` — the actual
   judgment about a real company.
3. **A human**, who confirms or overrides anything either layer proposed.

Nothing in this module decides that something IS a competitor. It decides what
KIND of organization a domain is, and derives the labels and defaults that fall
out of the axes. The competitor list itself is human-gated, always.

🚨 **The rules are DATA, not code.** Arman, 2026-08-15: *"there are some fairly
universal truths that we can actually record and a list that we can continue to
build on and grow... one day it could reach ten thousand sites. And the key is
that we just let each organization override it if they need."* The rules live in
``platform.domain_classification`` and are handed to :func:`classify_entity_role`
as a :class:`DomainRuleset`. A hardcoded list here would fork that registry the
moment anyone added a row to it, so there is deliberately none.

Pure functions over plain values: no DB, no network, no AI, no host imports —
the caller loads the rules (aidream: ``services/seo/domain_registry.py``) so this
module stays trivially testable and runs anywhere the package runs.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal, NamedTuple

BusinessOverlap = Literal["direct", "adjacent", "none"]
MarketOverlap = Literal["same_market", "different_market", "market_agnostic"]
SearchOverlapBand = Literal["dominant", "strong", "moderate", "slight", "none"]
#: The live vocabulary. Mirrors ``seo.competitor.competitor_entity_role_valid``
#: exactly — widened 2026-08-15 from the original 8 after real SERP evidence
#: turned up roles the first taxonomy had no name for (FEATURE.md §3a Finding 4).
EntityRole = Literal[
    "business",
    "manufacturer",
    "retail_channel",
    "marketplace",
    "adversary",
    "publisher",
    "professional_body",
    "community",
    "complementary_vendor",
    "reference",
    "supplier",
    "partner",
    "own_brand",
    "irrelevant",
    "spam",
]
PeerScale = Literal["smaller", "similar", "larger", "category_leader"]
Posture = Literal["compete", "copy", "outreach", "link_source", "monitor", "ignore"]

#: Roles whose linkers link to them *because of what they are*, not because of
#: the industry — so their backlink profile is worthless as a link-gap seed.
#: The test is "would a site that links to them plausibly link to me?" — only a
#: business in my industry passes it. See FEATURE.md §5.
NON_SEED_ROLES: frozenset[str] = frozenset(
    {
        "manufacturer",
        "retail_channel",
        "marketplace",
        "adversary",
        "publisher",
        "professional_body",
        "community",
        "complementary_vendor",
        "reference",
        "supplier",
        "partner",
        "own_brand",
        "irrelevant",
        "spam",
    }
)


class RoleVerdict(NamedTuple):
    """A deterministic role call, with the rule that made it — never a bare value.

    ``reason`` is written for a human to read in an approval queue, because a
    proposal a user cannot evaluate is a proposal they will rubber-stamp.
    """

    entity_role: EntityRole
    reason: str
    rule: str


# ── Layer 1: the universal registry ───────────────────────────────────────────
#
# The rules are ROWS in ``platform.domain_classification``, not constants here.
# The caller loads them and passes a ruleset in; this module only matches. A
# hardcoded copy would silently diverge from the registry the first time anyone
# added a row, which is exactly the failure the registry was built to end.


class DomainRule(NamedTuple):
    """One registry row, reduced to what matching needs.

    ``pattern_kind`` is ``domain`` (an exact registrable domain, or any subdomain
    of it) or ``suffix`` (a raw tail such as ``.gov`` — one row instead of ten
    thousand). ``is_org_override`` marks a row owned by the asking organization
    rather than the system org; those win, because ``entity_role`` is a property
    of the RELATIONSHIP (FEATURE.md §3 Axis 4) and a system row can only ever be
    a default.
    """

    pattern: str
    pattern_kind: str
    entity_role: str
    reason: str = ""
    confidence: int | None = None
    source: str = "system"
    is_org_override: bool = False


class DomainRuleset:
    """An indexed, reusable view over registry rows.

    Built once per load and cached by the caller: a linear scan of ten thousand
    rows per candidate domain is the thing this class exists to avoid. Exact
    domains resolve by dict lookup walking up the label chain (so
    ``en.wikipedia.org`` finds ``wikipedia.org`` in three lookups, not ten
    thousand comparisons); suffix rules are few and stay a scan, longest first
    so ``.gov.uk`` beats ``.uk``.
    """

    __slots__ = ("_domains", "_suffixes", "_size")

    def __init__(self, rules: Iterable[DomainRule]) -> None:
        domains: dict[str, DomainRule] = {}
        suffixes: list[DomainRule] = []
        size = 0
        for rule in rules:
            size += 1
            if rule.pattern_kind == "suffix":
                suffixes.append(rule)
                continue
            key = _registrable(rule.pattern)
            existing = domains.get(key)
            # An org row always displaces a system row for the same pattern.
            if existing is None or (rule.is_org_override and not existing.is_org_override):
                domains[key] = rule
        suffixes.sort(key=lambda rule: (rule.is_org_override, len(rule.pattern)), reverse=True)
        self._domains = domains
        self._suffixes = suffixes
        self._size = size

    def __len__(self) -> int:
        return self._size

    def match(self, host: str) -> DomainRule | None:
        labels = host.split(".")
        for index in range(len(labels) - 1):
            hit = self._domains.get(".".join(labels[index:]))
            if hit is not None:
                return hit
        for rule in self._suffixes:
            tail = rule.pattern if rule.pattern.startswith(".") else f".{rule.pattern}"
            if host.endswith(tail):
                return rule
        return None


#: What every caller gets before the registry loads, and what a site with no
#: rules at all sees. Safe by construction: an empty ruleset declines every
#: domain, so the AI layer handles it — never a wrong label.
EMPTY_RULESET = DomainRuleset(())


def _registrable(domain: str) -> str:
    """Lowercase, strip scheme/path/``www.``. Not a public-suffix parser — the
    registry stores registrable domains and the suffix rules work on the raw
    tail, so a PSL dependency buys nothing here."""
    value = domain.strip().lower()
    if "://" in value:
        value = value.split("://", 1)[1]
    value = value.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if value.startswith("www."):
        value = value[4:]
    return value.rstrip(".")


def classify_entity_role(domain: str, ruleset: DomainRuleset) -> RoleVerdict | None:
    """The deterministic role call, or ``None`` when this layer has no opinion.

    ``None`` is the expected result for most real companies and is NOT a
    failure — it is the handoff to the AI layer. This function never guesses: it
    either recognizes the domain in the registry or declines.
    """
    host = _registrable(domain)
    if not host:
        return None
    rule = ruleset.match(host)
    if rule is None:
        return None
    scope = "your organization's own rule" if rule.is_org_override else "the platform registry"
    reason = rule.reason.strip() or (
        f"{rule.pattern} is classified as a {rule.entity_role.replace('_', ' ')}."
    )
    return RoleVerdict(
        rule.entity_role,
        f"{reason} (Matched {rule.pattern} in {scope}.)",
        f"domain_classification:{rule.pattern_kind}:{rule.pattern}",
    )


# ── Derived values ────────────────────────────────────────────────────────────


def derive_label(
    *,
    business_overlap: str | None,
    market_overlap: str | None,
    entity_role: str | None,
    search_overlap_band: str | None = None,
    peer_scale: str | None = None,
) -> str:
    """The label a human reads. DERIVED, never stored as truth — see FEATURE.md §4.

    Unset axes degrade to "Unclassified" rather than guessing, because a
    confident wrong label is worse than an honest empty one.
    """
    #: Roles that ARE the answer — what the thing is matters more than any
    #: overlap it happens to have. FEATURE.md §4.
    role_labels: dict[str, str] = {
        "manufacturer": "Manufacturer / brand",
        "retail_channel": "Retail channel",
        "marketplace": "Marketplace / lead broker",
        "adversary": "Opposing interest",
        "publisher": "Publisher",
        "professional_body": "Industry body",
        "community": "Community site",
        "complementary_vendor": "Complementary vendor",
        "reference": "Reference site",
        "supplier": "Supplier",
        "partner": "Partner",
        "own_brand": "Your own brand",
        "irrelevant": "Ranks by accident",
        "spam": "Spam / link farm",
    }
    if entity_role in role_labels:
        return role_labels[entity_role]

    # `category_leader` outranks market overlap: "the national chain you build
    # toward" is more useful to a user than "technically in/out of my market".
    if (
        peer_scale == "category_leader"
        and entity_role == "business"
        and business_overlap in {"direct", "adjacent"}
    ):
        return "Aspirational model"

    if business_overlap == "none":
        if search_overlap_band in {"dominant", "strong", "moderate", "slight"}:
            return "Search-only competitor"
        return "Not a competitor"

    out_of_market = market_overlap == "different_market"
    if business_overlap == "direct":
        return "Out-of-market peer" if out_of_market else "Direct competitor"
    if business_overlap == "adjacent":
        return "Adjacent peer" if out_of_market else "Adjacent competitor"
    return "Unclassified"


def default_use_for_link_gap(*, business_overlap: str | None, entity_role: str | None) -> bool:
    """Should this competitor seed a paid link-gap run, absent a user override?

    The test is **"would a site that links to them plausibly link to me?"** —
    true for a business in my industry whatever its reach, false for
    marketplaces, publishers, reference and community sites.

    Note this deliberately INCLUDES out-of-market peers: same industry, same
    kind of linkers, and zero competitive risk in taking their link profile.
    They are the best seed in the system, and no incumbent tool can express
    that because none of them model geography (FEATURE.md §5).
    """
    if entity_role is None or entity_role in NON_SEED_ROLES:
        return False
    return business_overlap in {"direct", "adjacent"}


def default_posture(
    *,
    business_overlap: str | None,
    market_overlap: str | None,
    entity_role: str | None,
) -> Posture:
    """What we suggest doing about them. A default the user owns, not a decision."""
    if entity_role == "publisher":
        return "outreach"
    if entity_role in {"marketplace", "reference", "community"}:
        return "monitor"
    if entity_role in {"supplier", "partner", "own_brand"}:
        return "ignore"
    if business_overlap in {"direct", "adjacent"}:
        # Same business, out of reach: study them freely, they cost you nothing.
        return "copy" if market_overlap == "different_market" else "compete"
    return "monitor"


#: Share-of-our-keywords thresholds for the measured search-overlap axis.
#: PROVISIONAL — Arman's standing rule is that an inclusion threshold must be
#: validated across every site in the system rather than tuned on one account,
#: and today only 4 sites carry enough data to try. Tracked in FEATURE.md §8.
_BAND_THRESHOLDS: tuple[tuple[float, SearchOverlapBand], ...] = (
    (0.50, "dominant"),
    (0.25, "strong"),
    (0.10, "moderate"),
    (0.02, "slight"),
)

#: Absolute thresholds. NOT merely a fallback for a missing denominator — a
#: large absolute overlap is significant on its own. A 40,000-keyword site
#: sharing 400 keywords with you is only 1% of your surface, but 400 real
#: keywords is not "no overlap", and reporting it as such would hide a genuine
#: competitor behind a ratio.
_ABSOLUTE_THRESHOLDS: tuple[tuple[int, SearchOverlapBand], ...] = (
    (1000, "dominant"),
    (300, "strong"),
    (75, "moderate"),
    (10, "slight"),
)

#: Strength order, so the two signals can be combined by taking the stronger.
_BAND_ORDER: tuple[SearchOverlapBand, ...] = (
    "none",
    "slight",
    "moderate",
    "strong",
    "dominant",
)


def _stronger(left: SearchOverlapBand, right: SearchOverlapBand) -> SearchOverlapBand:
    return max(left, right, key=_BAND_ORDER.index)


def search_overlap_band(
    *, keyword_intersections: int | None, own_organic_keywords: int | None = None
) -> SearchOverlapBand | None:
    """The MEASURED axis: how much of your search surface do they take?

    Two signals, and the **stronger one wins**: the share of *our* keywords they
    take (what matters most when we are small) and the absolute count (what
    matters when they are huge). Using ratio alone reports a big site sharing
    400 of your keywords as "none", which is false; using the absolute count
    alone makes every large site look like a rival.

    Returns ``None`` when there is nothing to measure — never a default band,
    because a fabricated measurement is worse than an absent one on the one axis
    the machine is supposed to own.
    """
    if keyword_intersections is None or keyword_intersections < 0:
        return None
    if keyword_intersections == 0:
        return "none"

    absolute: SearchOverlapBand = "none"
    for floor, band in _ABSOLUTE_THRESHOLDS:
        if keyword_intersections >= floor:
            absolute = band
            break
    if not own_organic_keywords:
        return absolute

    ratio: SearchOverlapBand = "none"
    share = keyword_intersections / own_organic_keywords
    for floor, band in _BAND_THRESHOLDS:
        if share >= floor:
            ratio = band
            break
    return _stronger(absolute, ratio)
