"""Verification-only metric-key correspondence, so the payload diff can compare like with like.

.. warning::

   **THIS IS NOT A TRANSLATION LAYER.  IT NEVER TOUCHES WHAT THE ENGINE EMITS.**

   Nothing in this module is imported by the runtime, the manifest loader, the emitters, or
   anything else on the publish path -- only by
   :mod:`~matrice_analytics.engine.migration.differ`, which compares two payloads that have
   *already been produced*.  A mapping added here changes exactly one thing: which legacy
   metric the harness holds up against which new metric.  It does **not** rename a key, it
   does **not** make a legacy key appear on the new payload, and it will **not** stop a
   chart bound to a legacy key from going blank at cutover.  If you came here to fix a
   dashboard, this is the wrong file -- the fix is in the app's ``app.yaml`` and its
   ``metrics.json``/``widgets.json``, and it belongs to the app owner.

Why this exists
---------------
``people_counting`` ran on both engines against identical frames and **the analytics
agreed** -- unique arrivals 6, cumulative total 6 -- but **not one metric key matched**
(``clauding/BLOCKING.md`` M1, ``_contracts/12-defect-register.md`` §PY-1e).  Legacy publishes
``occupancy_in_interval`` where the new manifest publishes ``entry_count``; both read
``6.0``.  Matched by key, as :func:`~matrice_analytics.engine.migration.differ._diff_metrics`
must be, that is six BREAKING differences describing one fact: two engines that agree,
spelled differently.

The decision (2026-08-01, product owner) is that **the keys do not have to converge**.
Metric key naming belongs to the app owner, per app, per version -- it is published through
``app.yaml`` and bound in ``metrics.json``/``widgets.json``, and the migration is not the place to
relitigate it.
What the harness needs is not convergence but the *correspondence*: which legacy key is the
same measurement as which new key, so a value regression underneath a rename is still
caught.

Three states, deliberately distinct
-----------------------------------
================  ==========================================================
State             What the differ does
================  ==========================================================
**paired**        :class:`MetricKeyPair`.  The two entries are matched and
                  compared field by field -- ``agg_type``, ``category`` and
                  ``data``.  The correspondence itself is reported once, as
                  an ``IMPROVEMENT`` carrying this file's evidence, so the
                  map is auditable from the report rather than only from
                  the source.  **A value that disagrees underneath a pairing
                  is still BREAKING.**
**no counterpart**  :class:`UnpairedMetricKey`.  A key that is *known* to
                  exist on one side only, with a written reason -- the two
                  sides measure different things, so demanding a partner
                  would be demanding a metric nobody meant to publish.
                  Reported as an ``IMPROVEMENT``, never silent.
**unmapped**      Anything not named here.  **Stays BREAKING.**  This is
                  the load-bearing case: a key that quietly stopped being
                  published, or one that appeared from nowhere, is exactly
                  the regression the harness exists to catch, and an
                  unmapped key must never be mistaken for a benign rename.
                  Silence here would hollow the gate out.
================  ==========================================================

The distinction between the last two is the whole point.  "We know these two do not pair,
and here is why" is a reviewed statement with a citation; "nobody has looked at this key
yet" is not.  Collapsing them would let the second hide inside the first.

Adding an entry
---------------
An entry is a claim that two keys are the same measurement.  Back it:

1. Run the two engines on the same frames (``scripts/payload_diff.py``) and record that the
   values agree -- the ``occupancy_in_interval``/``entry_count`` pair below is seeded from a
   run where both read ``6.0``.
2. Put that run, or the source line that settles it, in ``evidence``.
3. Do not add a pair to make a diff go green.  If the values disagree, the pairing is
   *correct* and the port is *wrong*; the map's job is to make that visible, not to hide it.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "EMPTY_KEY_MAP",
    "VERIFICATION_KEY_MAPS",
    "MetricKeyPair",
    "MetricSide",
    "UnpairedMetricKey",
    "UsecaseKeyMap",
    "key_map_for",
]


class MetricSide(str, Enum):
    """Which payload a key appears on."""

    LEGACY = "LEGACY"
    """The legacy ``results-agg``, built by ``utils/legacy_analytics_bridge.py``."""

    NEW = "NEW"
    """The new engine's ``results-agg``, built from the app manifest."""


@dataclass(frozen=True, slots=True)
class MetricKeyPair:
    """Two spellings of one measurement: a legacy key and its new-engine counterpart.

    Attributes:
        legacy_key: ``metrics[].key`` as the legacy bridge publishes it.
        new_key: ``metrics[].key`` as the manifest publishes it.
        evidence: What settles the claim that these are the same measurement -- a
            payload-diff run in which both sides read the same value, or the ``file:line``
            that produces each.  **Required.**  Without it the pairing is an opinion, and an
            opinion that suppresses a difference is how a regression gets promoted.
        note: Anything a reviewer needs beyond the evidence.
    """

    legacy_key: str
    new_key: str
    evidence: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.legacy_key or not self.new_key:
            raise ValueError("a metric key pair needs both a legacy_key and a new_key")
        if not self.evidence.strip():
            raise ValueError(
                f"pairing {self.legacy_key!r} -> {self.new_key!r} carries no evidence; "
                "an unevidenced pairing suppresses differences on nothing but an opinion"
            )


@dataclass(frozen=True, slots=True)
class UnpairedMetricKey:
    """A key that **deliberately** has no counterpart -- not a key nobody has looked at.

    ``occupancy_percentage`` is legacy-only because it is a fraction of a configured
    capacity, and the new engine is given no capacity; ``peak_occupancy`` is new-only
    because legacy never computed a within-window maximum.  Neither is a rename waiting to
    be found, so neither is BREAKING -- but both are *reported*, because a metric that
    stops being published is a chart that stops drawing, and the app owner has to know.

    Attributes:
        key: The metric key.
        side: Which payload it appears on.  A key registered ``NEW`` that turns up on the
            **legacy** payload is *not* explained by this entry and stays BREAKING -- the
            registration is a statement about one side, not a blanket amnesty for the name.
        rationale: Why no counterpart exists.  Not "we did not port it": what it measures,
            and why the other engine has nothing that measures it.
        evidence: Doc section or ``file:line``.  **Required.**
    """

    key: str
    side: MetricSide
    rationale: str
    evidence: str

    def __post_init__(self) -> None:
        if not self.key:
            raise ValueError("an unpaired metric key entry needs a key")
        if not self.rationale.strip() or not self.evidence.strip():
            raise ValueError(
                f"{self.key!r} is registered as having no counterpart but carries no "
                "rationale/evidence; that is indistinguishable from nobody having looked"
            )


@dataclass(frozen=True, slots=True)
class UsecaseKeyMap:
    """One legacy use case's metric-key correspondence.

    Keyed by the *legacy* use-case name, because that is the side being retired and the side
    the harness is invoked with (``payload_diff.py --usecase``).
    """

    usecase: str
    pairs: tuple[MetricKeyPair, ...] = ()
    unpaired: tuple[UnpairedMetricKey, ...] = ()

    def __post_init__(self) -> None:
        """Reject a map that could pair one key two ways.

        An ambiguous map is worse than no map: which of two candidate pairings fires would
        depend on iteration order, so the same payloads could pass on one run and fail on
        the next.  A harness that is not reproducible authorises deletions nobody can check.
        """
        legacy_keys = [pair.legacy_key for pair in self.pairs]
        new_keys = [pair.new_key for pair in self.pairs]
        for label, keys in (("legacy", legacy_keys), ("new", new_keys)):
            duplicates = sorted({key for key in keys if keys.count(key) > 1})
            if duplicates:
                raise ValueError(
                    f"{self.usecase!r}: {label} metric key(s) {duplicates} appear in more than "
                    "one pairing, so the pairing is ambiguous"
                )
        for entry in self.unpaired:
            claimed = legacy_keys if entry.side is MetricSide.LEGACY else new_keys
            if entry.key in claimed:
                raise ValueError(
                    f"{self.usecase!r}: {entry.key!r} is registered both as paired and as "
                    "deliberately having no counterpart"
                )

    @property
    def is_empty(self) -> bool:
        """Whether this map says nothing -- every key is then unmapped, hence BREAKING."""
        return not self.pairs and not self.unpaired

    def pair_for_legacy(self, legacy_key: str) -> MetricKeyPair | None:
        """The pairing that claims ``legacy_key``, if any."""
        for pair in self.pairs:
            if pair.legacy_key == legacy_key:
                return pair
        return None

    def pair_for_new(self, new_key: str) -> MetricKeyPair | None:
        """The pairing that claims ``new_key``, if any."""
        for pair in self.pairs:
            if pair.new_key == new_key:
                return pair
        return None

    def new_key_for(self, legacy_key: str) -> str | None:
        """The new-engine key this legacy key should be compared against."""
        pair = self.pair_for_legacy(legacy_key)
        return pair.new_key if pair else None

    def legacy_key_for(self, new_key: str) -> str | None:
        """The legacy key this new-engine key should be compared against."""
        pair = self.pair_for_new(new_key)
        return pair.legacy_key if pair else None

    def unpaired_for(self, key: str, side: MetricSide) -> UnpairedMetricKey | None:
        """The "deliberately has no counterpart" entry for ``key`` **on that side**.

        Side-sensitive on purpose: ``current_occupancy`` is registered as new-only, so a
        ``current_occupancy`` that shows up on the *legacy* payload is unexplained and stays
        BREAKING.
        """
        for entry in self.unpaired:
            if entry.key == key and entry.side is side:
                return entry
        return None


EMPTY_KEY_MAP: Final[UsecaseKeyMap] = UsecaseKeyMap(usecase="")
"""What an unregistered use case gets: every key unmapped, so every mismatch is BREAKING."""


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------

_PY_1E: Final[str] = (
    "_contracts/12-defect-register.md §PY-1e; clauding/BLOCKING.md M1 "
    "(resolved 2026-08-01: app owners own key naming, the harness gets a verification map)"
)

_PEOPLE_COUNTING_RUN: Final[str] = (
    "payload_diff.py --usecase people_counting --manifest ml-applications/guidelines/examples/"
    "01-people-counting, 250 frames @25fps, frame-sequence digest 756b7ae0edabf6ee"
)

VERIFICATION_KEY_MAPS: Final[Mapping[str, UsecaseKeyMap]] = {
    "people_counting": UsecaseKeyMap(
        usecase="people_counting",
        pairs=(
            MetricKeyPair(
                legacy_key="occupancy_in_interval",
                new_key="entry_count",
                evidence=(
                    f"{_PY_1E}. Same run, same frames, both sides read data=6.0 with "
                    f"agg_type=sum, category=VOLUME ({_PEOPLE_COUNTING_RUN}). Legacy side "
                    "hard-coded at legacy_analytics_bridge.py:355-368"
                ),
                note=(
                    "Despite the name, the legacy metric counts ARRIVALS in the window, not "
                    "occupancy -- which is M2 / PY-1d, and is why entry_count is the honest "
                    "spelling of the same number."
                ),
            ),
            MetricKeyPair(
                legacy_key="total_occupancy",
                new_key="total_count",
                evidence=(
                    f"{_PY_1E}. Same run, both sides read data=6.0 with agg_type=last, "
                    f"category=VOLUME ({_PEOPLE_COUNTING_RUN}). Legacy side hard-coded at "
                    "legacy_analytics_bridge.py:355-368"
                ),
                note="Cumulative arrivals since reset on both sides.",
            ),
        ),
        unpaired=(
            UnpairedMetricKey(
                key="occupancy_percentage",
                side=MetricSide.LEGACY,
                rationale=(
                    "A fraction of a configured capacity. The new manifest is given no "
                    "capacity, so there is nothing for it to be a percentage of -- this is a "
                    "metric the app owner must reintroduce deliberately (with a capacity "
                    "input) or drop deliberately. It is NOT entry_count or total_count under "
                    "another name: in the same run legacy read 2.0 against their 6.0."
                ),
                evidence=(
                    f"{_PY_1E}; clauding/BLOCKING.md M2 (legacy published "
                    "occupancy_percentage=2.0 alongside current_counts=6 -- one person "
                    f"present against capacity 50, six arrivals). {_PEOPLE_COUNTING_RUN}"
                ),
            ),
            UnpairedMetricKey(
                key="current_occupancy",
                side=MetricSide.NEW,
                rationale=(
                    "Objects present at the end of the window. Legacy has no such metric: "
                    "its nearest name, occupancy_in_interval, is an arrival count (M2), so "
                    "pairing the two would compare 1 against 6 and call the engine wrong for "
                    "being right."
                ),
                evidence=f"{_PY_1E}; clauding/BLOCKING.md M2. {_PEOPLE_COUNTING_RUN}",
            ),
            UnpairedMetricKey(
                key="peak_occupancy",
                side=MetricSide.NEW,
                rationale=(
                    "The within-window maximum concurrent count. Legacy computes no "
                    "within-window maximum for this profile at all "
                    "(legacy_analytics_bridge.py:355-368 publishes three keys, none of them "
                    "a max), so there is no legacy series to compare it to."
                ),
                evidence=f"{_PY_1E}. {_PEOPLE_COUNTING_RUN}",
            ),
        ),
    ),
}
"""Legacy use-case name -> its verification-only key correspondence.

Seeded from ``people_counting``, the one use case both engines have actually been run on
(``_migration/wave-d1/``).  Every other use case is unregistered and therefore gets
:data:`EMPTY_KEY_MAP` -- which is the safe default: nothing is paired, so nothing is
forgiven.
"""


def key_map_for(usecase: str) -> UsecaseKeyMap:
    """The verification key map for a legacy use case.

    Args:
        usecase: The legacy use-case name, e.g. ``people_counting``.

    Returns:
        Its :class:`UsecaseKeyMap`, or :data:`EMPTY_KEY_MAP` when none is registered.  An
        unregistered use case is **not** an error: it means no key correspondence has been
        established yet, and every key difference stays BREAKING until one is.
    """
    return VERIFICATION_KEY_MAPS.get(usecase, EMPTY_KEY_MAP)
