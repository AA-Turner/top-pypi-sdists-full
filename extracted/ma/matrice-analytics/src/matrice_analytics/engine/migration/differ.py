"""Semantic comparison of a legacy ``results-agg`` payload against the new engine's.

Migration-wave policy (``clauding/PHASE2_PLAN.md`` §5, ``clauding/STAGE_BC_PLAN.md`` §7):
a legacy use case may only be deleted once the new engine, **on the same input**, emits
the **same payload**.  Not "the tests pass" -- the payloads match.  This module is what
decides whether that sentence is true, and it is deliberately *not* a dict diff.

Why a dict diff is the wrong tool
---------------------------------
Three separate reasons, each of which produces either a false alarm or a miss:

1. **The two engines legitimately differ in ways that do not matter.**  Every timestamp
   is different, because the legacy window boundary runs on wall-clock
   (``utils/legacy_analytics_bridge.py:3009`` calls ``time.time()``) while the new engine
   aggregates on frame time (**PY-13**).  ``incident_id`` is a UUID.  A dict diff flags
   all of it.
2. **They differ in ways a dict diff cannot see.**  ``metrics`` is a JSON *array*, and
   its order is not contractual -- the backend indexes by ``key`` -- so a list diff
   reports a shift when nothing changed, and can report *nothing* when a metric quietly
   swapped its ``agg_type`` from ``max`` to ``sum``.  ``metrics[]`` must be matched by
   ``(key, zone)``.
3. **Four differences are deliberate** and must be recognised, not flagged.  They are
   registered in :data:`DELIBERATE_CHANGES`, each with a citation, so the classification
   is auditable rather than a maintainer's opinion.

Every difference is therefore classified:

============  =============================================================
Class         Meaning
============  =============================================================
BREAKING      A consumer sees different data: a metric key present in one
              payload and not the other, a count that differs, a
              ``category`` or ``agg_type`` change.  **Blocks the wave.**
BENIGN        Cannot change what a dashboard shows: a timestamp, a UUID, a
              field's position in a list, ``""`` vs an absent optional
              string, an envelope label both engines copy verbatim out of
              the same untyped ``stream_info``.
IMPROVEMENT   A **known deliberate change** from :data:`DELIBERATE_CHANGES`.
              Cited, so a reviewer can check the claim.
============  =============================================================

The verdict is one bit: :meth:`DiffReport.passed` is true when there is no BREAKING
difference.  BENIGN and IMPROVEMENT differences are still *listed* -- a policy that hides
what it forgives is a policy nobody can audit.

One more thing the comparison consults
--------------------------------------
``metrics[]`` is matched by ``(key, zone)``, and the two engines do not agree on key
*spelling* -- legacy's ``occupancy_in_interval`` is the new engine's ``entry_count``, both
reading ``6.0`` on the same frames (**PY-1e**).  Metric key naming belongs to the app owner,
so the keys are not required to converge; instead
:mod:`~matrice_analytics.engine.migration.keymap` records, per use case, which legacy key is
the same measurement as which new key, and this module pairs on it before comparing.  That
map is **verification-only** -- it never changes what the engine emits -- and an *unmapped*
key stays BREAKING, which is the property that keeps it from becoming an amnesty.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Final

from matrice_analytics.engine.migration.keymap import (
    EMPTY_KEY_MAP,
    MetricSide,
    UsecaseKeyMap,
    key_map_for,
)

__all__ = [
    "BENIGN_LEGACY_ONLY_ENVELOPE_FIELDS",
    "DEFAULT_TOLERANCE",
    "DELIBERATE_CHANGES",
    "ENVELOPE_DESCRIPTIVE_FIELDS",
    "ENVELOPE_IDENTITY_FIELDS",
    "Classification",
    "DeliberateChange",
    "DiffContext",
    "DiffReport",
    "Difference",
    "TolerancePolicy",
    "Verdict",
    "diff_results_agg",
]


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------


class Classification(str, Enum):
    """What one difference means for a migration wave."""

    BREAKING = "BREAKING"
    """A consumer reads different data.  The wave stops here."""

    BENIGN = "BENIGN"
    """Cannot change what any dashboard, alert rule or rollup shows."""

    IMPROVEMENT = "IMPROVEMENT"
    """A registered deliberate change -- see :data:`DELIBERATE_CHANGES`."""


class Verdict(str, Enum):
    """The single answer a migration wave asks for."""

    PASS = "PASS"
    """No BREAKING difference.  This port may be promoted and the legacy file deleted."""

    FAIL = "FAIL"
    """At least one BREAKING difference."""

    LEGACY_UNAVAILABLE = "LEGACY_UNAVAILABLE"
    """The legacy side could not be run or published nothing, so **no comparison exists**.

    Deliberately *not* ``PASS``: "the old engine would not start" is not evidence that the
    new one matches it.  It is also deliberately not ``FAIL`` -- nothing about the new
    payload was disproved -- so the CLI gives it its own exit code and a wave operator has
    to make a call rather than reading a green tick.
    """


#: ``results-agg`` envelope fields that *identify* the row.  A difference here re-points
#: the data at a different camera, app or team, so it is always BREAKING.
#: Contract ``07-tobe-canonical-contract.md`` §2.1: ``camera_id`` drives team resolution
#: and zone lookup, ``app_id`` is the primary read-scope key for every dashboard query.
ENVELOPE_IDENTITY_FIELDS: Final[tuple[str, ...]] = (
    "camera_id",
    "app_id",
    "app_deployment_id",
    "application_key_name",
)

#: Envelope fields that are *labels*.  Both engines copy them out of the same untyped
#: ``stream_info`` (surface S4) through two different parsers, so a difference here is a
#: difference between the two parsers, not between the two analytics pipelines -- and the
#: migration question is about the analytics.  Classified BENIGN and **always listed**.
ENVELOPE_DESCRIPTIVE_FIELDS: Final[tuple[str, ...]] = (
    "camera_name",
    "camera_group",
    "locationId",
    "location",
    "application_name",
    "application_version",
    "rtp_number",
)

#: Fields the legacy bridge stamps onto ``results-agg`` that the S1 DTO does not declare
#: (they belong to S2, ``incident_res``).  The Go parser ignores an undeclared key, so
#: their presence is BENIGN -- but it is reported, because it is how the legacy envelope
#: drifted from the contract in the first place.
BENIGN_LEGACY_ONLY_ENVELOPE_FIELDS: Final[frozenset[str]] = frozenset(
    {"frame_id", "stream_time", "category", "application_id", "location_name"}
)

#: Every ``results-agg`` field whose value is a timestamp, on either surface.  Contract
#: §1 rule 2 (RFC3339 Z) and §3.3 (``stream_time``).
_TIMESTAMP_FIELDS: Final[frozenset[str]] = frozenset(
    {"input_timestamp", "reset_timestamp", "start_time", "end_time", "stream_time"}
)

#: Fields whose value is an opaque generated id.  ``incident_id`` is a UUID by contract
#: §3.2; the new engine makes it a *deterministic* UUID5 so replays are diffable
#: (``engine/runtime/session.py:_incident_id``), but the legacy side is random, so the two
#: can never agree and a difference carries no information.
_UUID_FIELDS: Final[frozenset[str]] = frozenset({"incident_id", "id"})

_UUID_RE: Final[re.Pattern[str]] = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

#: The three non-zone shapes the legacy ``agg_summary``/``tracking_stats`` key takes
#: (**PY-5**): ``str(frame_number)`` unguarded (hence the literal ``"None"``) in ~6
#: use-case files, and the guarded ``"current_frame"`` in ~4 others.
_NON_ZONE_KEY_RE: Final[re.Pattern[str]] = re.compile(r"^(?:\d+|None|current_frame|)$")

#: The legacy "no zone" sentinel (**PY-6**), e.g. ``usecases/people_counting.py:307``.
LEGACY_GLOBAL_SENTINEL: Final[str] = "__global__"

#: The contract's sentinel -- ``07`` §2.2: "Single-bucket apps use the literal key
#: ``global``. Never ``__global__``."
CANONICAL_GLOBAL_ZONE: Final[str] = "global"

_ABSENT: Final[object] = object()
"""Sentinel for "this payload does not have that field at all"."""


# ---------------------------------------------------------------------------
# Tolerance policy
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TolerancePolicy:
    """What the comparison is allowed to forgive, stated explicitly.

    Every entry exists because the two engines *provably* differ on it for a reason that
    cannot reach a consumer.  Nothing here is a convenience.

    Attributes:
        float_abs_tol: Absolute tolerance on ``metrics[].data``.  ``data`` is a float on
            the wire (contract §1 rule 6) and both engines reach it through a different
            number of float operations -- a percentage computed as ``a / b * 100`` differs
            in the last bit depending on the order.  Counts are **ints** and get no
            tolerance at all (see :attr:`int_counts_are_exact`).
        float_rel_tol: Relative tolerance, for the same reason at large magnitudes.
        timestamps_may_differ: Every timestamp is allowed to differ.  The legacy window
            boundary and its ``input_timestamp`` come from ``time.time()``
            (``legacy_analytics_bridge.py:3009,3013``); the new engine's come from frame
            time (**PY-13**).  They therefore *always* differ, on every run, and a policy
            that called that BREAKING would never pass anything.
        uuids_may_differ: A value that is a UUID on both sides may differ.  Ids are
            opaque to every consumer except the backend's find-or-create, which only needs
            them stable *within* a stream, not equal *across* engines.
        empty_string_equals_absent: ``""`` and an absent key are the same value for an
            optional string.  Contract §1 rule 7 forbids ``None`` and requires ``""``;
            ``to_payload`` uses ``exclude_none=True`` so an unset optional simply does not
            serialise.  Both spellings reach the Go parser as the zero value.
        absent_count_is_zero: A category absent from a count list is a count of zero.
            The legacy builder emits an explicit ``{"category": "person", "count": 0}``;
            the new engine omits the entry.  A dashboard cannot tell them apart.
        int_counts_are_exact: Counts are never tolerated.  ``current_counts`` feeds
            ``raw_analytics.count``, the primary series -- one person of drift there is
            exactly the class of bug this harness exists to catch.
        ignored_paths: Paths never compared, for diagnostics that are not payload.
    """

    float_abs_tol: float = 1e-6
    float_rel_tol: float = 1e-9
    timestamps_may_differ: bool = True
    uuids_may_differ: bool = True
    empty_string_equals_absent: bool = True
    absent_count_is_zero: bool = True
    int_counts_are_exact: bool = True
    ignored_paths: frozenset[str] = frozenset()

    def numbers_equal(self, left: float, right: float) -> bool:
        """Whether two floats are equal under this policy."""
        return math.isclose(left, right, rel_tol=self.float_rel_tol, abs_tol=self.float_abs_tol)


DEFAULT_TOLERANCE: Final[TolerancePolicy] = TolerancePolicy()
"""The policy a migration wave runs.  Override it only with a written reason."""


# ---------------------------------------------------------------------------
# One difference
# ---------------------------------------------------------------------------


def _jsonable(value: Any) -> Any:
    """A JSON-safe rendering of a payload fragment, for the report."""
    if value is _ABSENT:
        return None
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return repr(value)
    return value


@dataclass(frozen=True, slots=True)
class Difference:
    """One place the two payloads disagree, and what that disagreement means."""

    path: str
    """Where, in a stable notation that does not depend on list order.

    e.g. ``tracking_stats["global"].current_counts["person"].count`` or
    ``metrics["entry_count"@"global"].agg_type``.
    """

    legacy: Any
    """The legacy value, or ``None`` when the legacy payload has no such field."""

    new: Any
    """The new engine's value, or ``None`` when the new payload has no such field."""

    classification: Classification
    reason: str
    """One sentence a reviewer can act on."""

    citation: str = ""
    """Defect id / file:line backing the classification.  Required for IMPROVEMENT."""

    legacy_present: bool = True
    new_present: bool = True

    @property
    def is_breaking(self) -> bool:
        return self.classification is Classification.BREAKING

    def to_dict(self) -> dict[str, Any]:
        """The JSON form the ``--json`` CLI mode emits."""
        return {
            "path": self.path,
            "classification": self.classification.value,
            "legacy": _jsonable(self.legacy),
            "new": _jsonable(self.new),
            "legacy_present": self.legacy_present,
            "new_present": self.new_present,
            "reason": self.reason,
            "citation": self.citation,
        }

    def render(self) -> str:
        """One line for the human-readable report."""
        left = "<absent>" if not self.legacy_present else json.dumps(_jsonable(self.legacy))
        right = "<absent>" if not self.new_present else json.dumps(_jsonable(self.new))
        return f"{self.path}\n      legacy={left}\n      new   ={right}\n      {self.reason}" + (
            f"\n      cite: {self.citation}" if self.citation else ""
        )


# ---------------------------------------------------------------------------
# What the comparison knows about the port
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DiffContext:
    """Facts about the port that some classifications depend on.

    A difference cannot be classified from its two values alone.  "This zone count moved
    by one" is BREAKING for an app that never changed its reference point and an
    IMPROVEMENT for one that did -- so the deliberate-change predicates read this.
    """

    usecase: str = ""
    """The legacy use-case name, e.g. ``people_counting``."""

    app_id: str = ""
    """The new manifest's ``app.id``."""

    frames: int = 0
    """How many frames both engines were fed.  Used by the **PY-1** ``mean`` predicate."""

    zoned: bool = False
    """Whether the new engine partitioned by zone (``Session.emission_zones`` > global)."""

    reference_point: str = "foot_center"
    """The new engine's zone-membership reference point.

    ``engine/runtime/session.py:_resolve_reference_point`` defaults to ``foot_center``.
    """

    legacy_reference_point: str = "box_center"
    """The legacy reference point -- ``analytics/geometry.py:184`` (``use_foot_center=False``)."""

    global_counts_agree: bool | None = None
    """Whether the whole-frame (``global``) counts matched.

    Computed by :func:`diff_results_agg` before classification, because the
    ``foot_center`` predicate depends on it: moving the reference point can move an object
    from one zone to another, but it can never change how many objects are in the frame.
    """


# ---------------------------------------------------------------------------
# The registry of deliberate changes
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeliberateChange:
    """A known, intended behaviour change -- recognised, never flagged as breakage.

    The ``citation`` is the point of this class.  Without it, "we meant to do that" is
    unfalsifiable, and a real regression that happens to look like an intended change gets
    waved through by whoever is running the wave that day.
    """

    change_id: str
    """Stable id, used in reports and tests."""

    summary: str
    """One line: what changed."""

    citation: str
    """Where it was decided.  Doc + section, or file:line."""

    rationale: str
    """Why it cannot be a regression."""

    predicate: Callable[[Difference, DiffContext], bool]
    """Whether this change explains that candidate difference."""

    def explains(self, difference: Difference, context: DiffContext) -> bool:
        """Whether this registered change accounts for ``difference``."""
        return bool(self.predicate(difference, context))


#: The path a *rename* difference is reported under.  A rename is reported as one
#: difference whose two values are the two key spellings -- **not** as a missing key plus an
#: extra key.  That distinction is load-bearing: reporting it as a pair would let the
#: rename's IMPROVEMENT classification swallow the two zones' counts, and a real counting
#: regression hiding behind a rename is precisely the failure this harness must not have.
ZONE_KEY_PATH: Final[str] = "tracking_stats{key}"


def _zone_of(path: str) -> str:
    """The zone name out of a ``tracking_stats["<zone>"]...`` path, or ``""``."""
    match = re.match(r'^tracking_stats\["([^"]*)"\]', path)
    return match.group(1) if match else ""


def _is_key_rename(difference: Difference) -> bool:
    """Whether the difference is a key *rename* -- one difference, both spellings present.

    Two shapes carry a rename: :data:`ZONE_KEY_PATH` for a ``tracking_stats`` zone key, and
    ``metrics["<key>"].zone`` for a metric's zone label.
    """
    is_rename_path = difference.path == ZONE_KEY_PATH or difference.path.endswith("].zone")
    return is_rename_path and difference.legacy_present and difference.new_present


def _matches_agg_summary_rekey(difference: Difference, context: DiffContext) -> bool:
    """**PY-5** -- the key changed from a frame number / sentinel to a zone id."""
    if not _is_key_rename(difference):
        return False
    legacy, new = str(difference.legacy), str(difference.new)
    return bool(_NON_ZONE_KEY_RE.match(legacy)) and bool(new) and not _NON_ZONE_KEY_RE.match(new)


def _matches_global_sentinel_rename(difference: Difference, context: DiffContext) -> bool:
    """**PY-6** -- ``"__global__"`` became ``"global"``."""
    return (
        difference.legacy == LEGACY_GLOBAL_SENTINEL and difference.new == CANONICAL_GLOBAL_ZONE
    )


def _matches_foot_center_default(difference: Difference, context: DiffContext) -> bool:
    """``foot_center`` replaced the box centre as the default reference point.

    Only ever explains a **per-zone** count.  Moving the reference point from the middle of
    the box to the middle of its bottom edge can move an object from one zone to another --
    that is the whole point, a tall person is standing in the zone at their feet, not the
    one behind them -- but it cannot change how many objects are in the frame.  So this
    predicate refuses to fire unless the ``global`` bucket agreed, which makes it unable to
    launder a genuine counting regression as an intended change.
    """
    if context.reference_point != "foot_center":
        return False
    if context.legacy_reference_point == "foot_center":
        return False
    if not context.zoned or context.global_counts_agree is not True:
        return False
    zone = _zone_of(difference.path)
    if zone in {"", CANONICAL_GLOBAL_ZONE, LEGACY_GLOBAL_SENTINEL}:
        return False
    return difference.path.endswith(".count")


def _matches_mean_no_longer_summed(difference: Difference, context: DiffContext) -> bool:
    """**PY-1** -- ``agg_type: mean`` is no longer silently summed.

    Legacy dispatch handles ``sum|max|min|avg|last`` and falls back to ``sum`` for anything
    else (``analytics/base_processor.py:353-365``), so a *mean* percentage was published as
    the **sum of every per-frame percentage in the window**: the register's own example is a
    compliance percentage that read ~150,000 where the truth was ~85.

    The signature is therefore "legacy is the new value multiplied by roughly the frame
    count".  The window is bounded by the frame count with 50% slack on both sides, so a
    metric that merely drifted upward does not qualify and a metric that got *smaller*
    never does.
    """
    if not difference.path.startswith("metrics[") or not difference.path.endswith("].data"):
        return False
    if not isinstance(difference.legacy, (int, float)) or not isinstance(
        difference.new, (int, float)
    ):
        return False
    if "agg_type=mean" not in difference.reason:
        return False
    legacy, new = float(difference.legacy), float(difference.new)
    if context.frames < 2 or new <= 0.0 or legacy <= new:
        return False
    ratio = legacy / new
    return 1.5 <= ratio <= context.frames * 1.5


DELIBERATE_CHANGES: Final[tuple[DeliberateChange, ...]] = (
    DeliberateChange(
        change_id="PY-5-agg-summary-rekeyed-by-zone",
        summary="agg_summary / tracking_stats are keyed by zone, not by frame number.",
        citation=(
            "_contracts/12-defect-register.md §PY-5; "
            "_contracts/07-tobe-canonical-contract.md §4; "
            "clauding/STAGE_BC_PLAN.md §6b 'Deliberate behaviour changes' (1)"
        ),
        rationale=(
            "Legacy emits '<int>', 'None' (unguarded str(frame_number) in ~6 use-case files) "
            "or 'current_frame' (guarded, in ~4 others). Zone-keying is the only form that "
            "works for a multi-zone app -- three consumers currently break on them -- and it "
            "matches results-agg, which the Go parser already reads zone-keyed (FROZEN-2). "
            "Visible to three consumers: announce, do not slip in."
        ),
        predicate=_matches_agg_summary_rekey,
    ),
    DeliberateChange(
        change_id="PY-6-global-sentinel-renamed",
        summary='The no-zone sentinel is "global"; never "__global__".',
        citation=(
            "_contracts/12-defect-register.md §PY-6 (usecases/people_counting.py:307 vs "
            "analytics/engine.py:399); _contracts/07-tobe-canonical-contract.md §2.2; "
            "clauding/STAGE_BC_PLAN.md §6b 'Deliberate behaviour changes' (3)"
        ),
        rationale=(
            "The sentinel becomes raw_analytics.zoneId, so the two spellings are two "
            "unrelated ClickHouse series. 'global' is what the backend documents and what "
            "the new flow already emits. Migrating an app SPLITS ITS HISTORY -- flag every "
            "affected app before cutover."
        ),
        predicate=_matches_global_sentinel_rename,
    ),
    DeliberateChange(
        change_id="FOOT-CENTER-IS-THE-DEFAULT-REFERENCE-POINT",
        summary="Zone membership is decided by the box's foot centre, not its centre.",
        citation=(
            "clauding/STAGE_BC_PLAN.md §6b 'Deliberate behaviour changes' (2); "
            "engine/runtime/session.py:_resolve_reference_point; legacy default "
            "analytics/geometry.py:184 (use_foot_center=False)"
        ),
        rationale=(
            "Box-centre membership puts a tall person in the zone BEHIND the one they are "
            "standing in. Changing the reference point can move an object between zones; it "
            "cannot change the whole-frame total -- so this only ever explains a per-zone "
            "count, and only when the 'global' bucket agreed."
        ),
        predicate=_matches_foot_center_default,
    ),
    DeliberateChange(
        change_id="PY-1-mean-no-longer-silently-summed",
        summary="agg_type: mean is a mean. It used to fall through to sum.",
        citation=(
            "_contracts/12-defect-register.md §PY-1 (analytics/base_processor.py:353-365, "
            "analytics/config/ppe_compliance_new.yaml:90); "
            "_contracts/07-tobe-canonical-contract.md §2.3"
        ),
        rationale=(
            "A 60-second window at 25 fps published a 'compliance percentage' of ~150,000 "
            "because every per-frame percentage was added up. ~85 is the correct reading of "
            "the same frames, so a large DECREASE on a mean metric is the fix landing, not a "
            "regression. An unrecognised agg_type is now a manifest-load error, not a "
            "runtime fallback."
        ),
        predicate=_matches_mean_no_longer_summed,
    ),
)


def _classify_candidate(difference: Difference, context: DiffContext) -> Difference:
    """Offer a BREAKING candidate to the registry; reclassify on the first match."""
    if not difference.is_breaking:
        return difference
    for change in DELIBERATE_CHANGES:
        if change.explains(difference, context):
            return replace(
                difference,
                classification=Classification.IMPROVEMENT,
                reason=f"{change.change_id}: {change.summary} {change.rationale}",
                citation=change.citation,
            )
    return difference


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DiffReport:
    """The structured answer, plus the one bit a migration wave needs."""

    usecase: str
    app_id: str
    context: DiffContext
    differences: tuple[Difference, ...] = ()
    legacy_payload: Mapping[str, Any] | None = None
    new_payload: Mapping[str, Any] | None = None
    tolerance: TolerancePolicy = DEFAULT_TOLERANCE
    legacy_error: str = ""
    """Why the legacy side produced nothing, when it produced nothing."""

    notes: tuple[str, ...] = ()
    """Anything a wave operator has to know that is not itself a difference."""

    @property
    def breaking(self) -> tuple[Difference, ...]:
        return tuple(d for d in self.differences if d.classification is Classification.BREAKING)

    @property
    def benign(self) -> tuple[Difference, ...]:
        return tuple(d for d in self.differences if d.classification is Classification.BENIGN)

    @property
    def improvements(self) -> tuple[Difference, ...]:
        return tuple(d for d in self.differences if d.classification is Classification.IMPROVEMENT)

    @property
    def verdict(self) -> Verdict:
        """``PASS`` / ``FAIL`` / ``LEGACY_UNAVAILABLE`` -- see :class:`Verdict`."""
        if self.legacy_error or self.legacy_payload is None:
            return Verdict.LEGACY_UNAVAILABLE
        return Verdict.FAIL if self.breaking else Verdict.PASS

    @property
    def passed(self) -> bool:
        """Does this port pass?  True only for :attr:`Verdict.PASS`."""
        return self.verdict is Verdict.PASS

    def to_dict(self) -> dict[str, Any]:
        """The full JSON report -- what ``--json`` prints and what a wave archives."""
        return {
            "usecase": self.usecase,
            "app_id": self.app_id,
            "verdict": self.verdict.value,
            "passed": self.passed,
            "counts": {
                "breaking": len(self.breaking),
                "benign": len(self.benign),
                "improvement": len(self.improvements),
            },
            "legacy_error": self.legacy_error,
            "notes": list(self.notes),
            "context": {
                "frames": self.context.frames,
                "zoned": self.context.zoned,
                "reference_point": self.context.reference_point,
                "legacy_reference_point": self.context.legacy_reference_point,
                "global_counts_agree": self.context.global_counts_agree,
            },
            "tolerance": {
                "float_abs_tol": self.tolerance.float_abs_tol,
                "float_rel_tol": self.tolerance.float_rel_tol,
                "timestamps_may_differ": self.tolerance.timestamps_may_differ,
                "uuids_may_differ": self.tolerance.uuids_may_differ,
                "empty_string_equals_absent": self.tolerance.empty_string_equals_absent,
                "absent_count_is_zero": self.tolerance.absent_count_is_zero,
            },
            "differences": [d.to_dict() for d in self.differences],
            "legacy_payload": _jsonable(self.legacy_payload),
            "new_payload": _jsonable(self.new_payload),
        }

    def render(self) -> str:
        """The readable report the CLI prints."""
        lines = [
            f"payload diff  legacy:{self.usecase or '(none)'}  ->  new:{self.app_id or '(none)'}",
            f"  frames={self.context.frames}  zoned={self.context.zoned}  "
            f"reference_point={self.context.legacy_reference_point}->{self.context.reference_point}",
            f"  VERDICT: {self.verdict.value}"
            f"  (breaking={len(self.breaking)} benign={len(self.benign)} "
            f"improvement={len(self.improvements)})",
        ]
        if self.legacy_error:
            lines += ["", f"  LEGACY SIDE DID NOT PRODUCE A PAYLOAD: {self.legacy_error}"]
        for note in self.notes:
            lines.append(f"  note: {note}")
        for label, group in (
            ("BREAKING", self.breaking),
            ("IMPROVEMENT", self.improvements),
            ("BENIGN", self.benign),
        ):
            if not group:
                continue
            lines += ["", f"{label} ({len(group)})"]
            lines += [f"  - {d.render()}" for d in group]
        if not self.differences and not self.legacy_error:
            lines += ["", "  no differences: the payloads match."]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# The comparison
# ---------------------------------------------------------------------------


def diff_results_agg(
    legacy: Mapping[str, Any] | None,
    new: Mapping[str, Any] | None,
    *,
    context: DiffContext | None = None,
    tolerance: TolerancePolicy = DEFAULT_TOLERANCE,
    key_map: UsecaseKeyMap | None = None,
    legacy_error: str = "",
    notes: Sequence[str] = (),
) -> DiffReport:
    """Compare two ``results-agg`` payloads structurally and classify every difference.

    The three parts of the payload are compared three different ways, because they are
    three different shapes (contract §2):

    * **the envelope** -- field by field, split into identity (BREAKING) and label
      (BENIGN) fields;
    * **``tracking_stats``** -- zone-keyed (**FROZEN-2**), and for every zone all four
      count lists (**PY-2**/**FROZEN-5**), matched by ``category``;
    * **``metrics[]``** -- matched by ``(key, zone)``, **never by list position**: the
      array's order is not contractual, the backend indexes by ``key``, and a positional
      comparison both invents differences and hides an ``agg_type`` swap.

    Args:
        legacy: The legacy ``results-agg`` payload, or ``None`` when the legacy side
            produced nothing (then ``legacy_error`` should say why).
        new: The new engine's ``results-agg`` payload.
        context: Facts the deliberate-change predicates need.  ``global_counts_agree`` is
            filled in here and any caller-supplied value is overwritten.
        tolerance: What may be forgiven.  See :class:`TolerancePolicy`.
        key_map: The verification-only metric-key correspondence
            (:mod:`~matrice_analytics.engine.migration.keymap`).  Defaults to the map
            registered for ``context.usecase``, or an empty one -- in which case every key
            that differs in spelling is BREAKING, which is the safe default.  Pass
            :data:`~matrice_analytics.engine.migration.keymap.EMPTY_KEY_MAP` explicitly to
            see the raw, unmapped truth.
        legacy_error: Why the legacy side produced nothing.  Forces
            :attr:`Verdict.LEGACY_UNAVAILABLE`.
        notes: Free-text findings for the report.

    Returns:
        A :class:`DiffReport`.  :attr:`DiffReport.passed` is the verdict.
    """
    ctx = context or DiffContext()
    effective_key_map = key_map if key_map is not None else key_map_for(ctx.usecase)
    if legacy is None or new is None:
        return DiffReport(
            usecase=ctx.usecase,
            app_id=ctx.app_id,
            context=ctx,
            legacy_payload=legacy,
            new_payload=new,
            tolerance=tolerance,
            legacy_error=legacy_error
            or ("the new engine published no results-agg" if new is None else "no legacy payload"),
            notes=tuple(notes),
        )

    legacy_stats = _as_mapping(legacy.get("tracking_stats"))
    new_stats = _as_mapping(new.get("tracking_stats"))
    # The foot_center predicate is only allowed to fire when the whole-frame count agreed,
    # so that answer has to exist before anything is classified.
    ctx = replace(ctx, global_counts_agree=_global_counts_agree(legacy_stats, new_stats, tolerance))

    raw: list[Difference] = []
    raw += _diff_envelope(legacy, new, tolerance)
    raw += _diff_tracking_stats(legacy_stats, new_stats, tolerance)
    raw += _diff_metrics(legacy.get("metrics"), new.get("metrics"), tolerance, effective_key_map)

    classified = tuple(
        _classify_candidate(difference, ctx)
        for difference in raw
        if difference.path not in tolerance.ignored_paths
    )
    return DiffReport(
        usecase=ctx.usecase,
        app_id=ctx.app_id,
        context=ctx,
        differences=classified,
        legacy_payload=dict(legacy),
        new_payload=dict(new),
        tolerance=tolerance,
        notes=tuple(notes),
    )


# -- envelope ---------------------------------------------------------------


def _diff_envelope(
    legacy: Mapping[str, Any], new: Mapping[str, Any], tolerance: TolerancePolicy
) -> list[Difference]:
    """Compare the S1 envelope (contract §2.1) field by field.

    Three groups, then everything else.  Every top-level key that is not ``tracking_stats``
    or ``metrics`` is compared -- including one neither payload was expected to carry, since
    an undeclared field is how ``inferencePipelineId`` and ``deployment_instance_id`` ended
    up on the third legacy builder (**PY-3**).
    """
    out: list[Difference] = []
    for name in ENVELOPE_IDENTITY_FIELDS:
        out += _diff_scalar(
            name,
            legacy.get(name, _ABSENT),
            new.get(name, _ABSENT),
            tolerance,
            breaking_reason=(
                "envelope identity field. camera_id drives team resolution and zone lookup "
                "and app_id is the primary read-scope key for every dashboard query "
                "(contract §2.1), so a difference re-points the whole row."
            ),
        )
    for name in ENVELOPE_DESCRIPTIVE_FIELDS:
        out += _diff_scalar(
            name,
            legacy.get(name, _ABSENT),
            new.get(name, _ABSENT),
            tolerance,
            breaking_reason="",
            benign_reason=(
                "envelope label. Both engines copy it out of the same untyped stream_info "
                "(surface S4) through two different parsers, so this is a parser difference, "
                "not an analytics difference. Listed so it is never invisible."
            ),
        )

    handled = {*ENVELOPE_IDENTITY_FIELDS, *ENVELOPE_DESCRIPTIVE_FIELDS, "tracking_stats", "metrics"}
    for name in sorted((set(legacy) | set(new)) - handled):
        left, right = legacy.get(name, _ABSENT), new.get(name, _ABSENT)
        legacy_only = right is _ABSENT and left is not _ABSENT
        out += _diff_scalar(
            name,
            left,
            right,
            tolerance,
            breaking_reason=(
                ""
                if legacy_only and name in BENIGN_LEGACY_ONLY_ENVELOPE_FIELDS
                else (
                    "field present on the legacy payload and absent from the new one."
                    if legacy_only
                    else "envelope field differs, or is present on one payload only."
                )
            ),
            benign_reason=(
                "legacy-only envelope field the S1 DTO does not declare; the Go parser "
                "ignores an undeclared key, so it cannot reach a consumer."
            ),
        )
    return out


def _diff_scalar(
    path: str,
    left: Any,
    right: Any,
    tolerance: TolerancePolicy,
    *,
    breaking_reason: str,
    benign_reason: str = "",
) -> list[Difference]:
    """Compare one scalar under the tolerance policy.

    ``breaking_reason`` empty means "a difference here is BENIGN", and ``benign_reason``
    carries the explanation.

    A tolerated timestamp or UUID is **reported as BENIGN, not swallowed**.  Dropping it
    silently would be the cheaper implementation and the wrong one: an ``input_timestamp``
    that differs by 48 minutes because the legacy window runs on wall-clock is a fact about
    the port a reviewer should see once, even though no consumer can read it.
    """
    if _scalar_equal(path, left, right, tolerance):
        return []
    field_name = path.rsplit(".", 1)[-1]
    if field_name in _TIMESTAMP_FIELDS:
        if tolerance.timestamps_may_differ:
            classification, reason = Classification.BENIGN, (
                "timestamps are allowed to differ: the legacy window boundary and its "
                "input_timestamp come from time.time() "
                "(legacy_analytics_bridge.py:3009,3013) while the new engine's come from "
                "frame time (PY-13)."
            )
        else:
            classification, reason = Classification.BREAKING, (
                "timestamp differs and this policy has timestamps_may_differ=False."
            )
    elif field_name in _UUID_FIELDS and _both_uuid(left, right):
        if tolerance.uuids_may_differ:
            classification, reason = Classification.BENIGN, (
                "both values are UUIDs; ids are opaque to every consumer except the backend's "
                "find-or-create, which needs them stable within a stream, not equal across "
                "engines."
            )
        else:
            classification, reason = Classification.BREAKING, (
                "id differs and this policy has uuids_may_differ=False."
            )
    elif not breaking_reason:
        classification, reason = Classification.BENIGN, benign_reason
    else:
        classification, reason = Classification.BREAKING, breaking_reason
    return [
        Difference(
            path=path,
            legacy=_present_or_none(left),
            new=_present_or_none(right),
            classification=classification,
            reason=reason,
            legacy_present=left is not _ABSENT,
            new_present=right is not _ABSENT,
        )
    ]


def _scalar_equal(path: str, left: Any, right: Any, tolerance: TolerancePolicy) -> bool:
    """Whether two scalars are literally the same value under the policy.

    Only the *value* rules live here -- ``""``-vs-absent and the float epsilon.  Timestamps
    and UUIDs are deliberately **not** short-circuited: they are classified as BENIGN by
    :func:`_diff_scalar` so they still appear in the report.
    """
    if tolerance.empty_string_equals_absent:
        left = "" if left is _ABSENT else left
        right = "" if right is _ABSENT else right
    if left is _ABSENT or right is _ABSENT:
        return False
    if isinstance(left, bool) or isinstance(right, bool):
        return left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if isinstance(left, int) and isinstance(right, int):
            return left == right
        return tolerance.numbers_equal(float(left), float(right))
    return left == right


def _both_uuid(left: Any, right: Any) -> bool:
    return bool(
        isinstance(left, str) and isinstance(right, str)
        and _UUID_RE.match(left) and _UUID_RE.match(right)
    )


def _present_or_none(value: Any) -> Any:
    return None if value is _ABSENT else value


def _as_mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


# -- tracking_stats ---------------------------------------------------------

#: The four count lists, defined once (contract §2.2).  All four must be present on every
#: zone -- **PY-2**/**FROZEN-5**: two are ignored on the main ingestion path and the
#: instant-metric path depends on them anyway.
COUNT_LISTS: Final[tuple[str, ...]] = (
    "current_counts",
    "current_new_counts",
    "total_counts",
    "total_current_counts",
)


def _counts_by_category(value: Any, tolerance: TolerancePolicy) -> dict[str, int]:
    """One count list as ``{category: count}``, dropping zeros when they equal absence."""
    out: dict[str, int] = {}
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return out
    for entry in value:
        if not isinstance(entry, Mapping):
            continue
        category = str(entry.get("category", ""))
        if not category:
            continue
        try:
            count = int(entry.get("count", 0) or 0)
        except (TypeError, ValueError):
            continue
        if count == 0 and tolerance.absent_count_is_zero:
            continue
        out[category] = count
    return out


def _global_counts_agree(
    legacy_stats: Mapping[str, Any], new_stats: Mapping[str, Any], tolerance: TolerancePolicy
) -> bool | None:
    """Whether the whole-frame bucket's four count lists matched on both sides.

    ``None`` when neither payload has a whole-frame bucket to compare, which is what stops
    the ``foot_center`` predicate from firing on an app it knows nothing about.
    """
    legacy_zone = _pick_global_zone(legacy_stats)
    new_zone = _pick_global_zone(new_stats)
    if legacy_zone is None or new_zone is None:
        return None
    left, right = _as_mapping(legacy_stats[legacy_zone]), _as_mapping(new_stats[new_zone])
    for name in COUNT_LISTS:
        if _counts_by_category(left.get(name), tolerance) != _counts_by_category(
            right.get(name), tolerance
        ):
            return False
    return True


def _pick_global_zone(stats: Mapping[str, Any]) -> str | None:
    """The whole-frame bucket key: ``global``, ``__global__`` (**PY-6**), or a lone key."""
    for candidate in (CANONICAL_GLOBAL_ZONE, LEGACY_GLOBAL_SENTINEL):
        if candidate in stats:
            return candidate
    if len(stats) == 1:
        return next(iter(stats))
    return None


def _diff_tracking_stats(
    legacy: Mapping[str, Any], new: Mapping[str, Any], tolerance: TolerancePolicy
) -> list[Difference]:
    """Compare the zone-keyed ``tracking_stats`` block (contract §2.2, **FROZEN-2**).

    Keys are **paired first** (:func:`_pair_zone_keys`).  A key that was renamed is reported
    as one rename difference and its counts are still compared; only a key with no
    counterpart at all is a missing or extra zone.
    """
    out: list[Difference] = []
    pairs, legacy_only, new_only = _pair_zone_keys(legacy, new)
    for zone in legacy_only:
        out.append(
            Difference(
                path=f'tracking_stats["{zone}"]',
                legacy=_summarise_zone(legacy[zone], tolerance),
                new=None,
                classification=Classification.BREAKING,
                reason=(
                    f"zone {zone!r} is present in tracking_stats on the legacy payload and "
                    "absent on the new one. Every top-level key becomes raw_analytics.zoneId "
                    "(FROZEN-2), so a zone that vanishes is a series that stops."
                ),
                legacy_present=True,
                new_present=False,
            )
        )
    for zone in new_only:
        out.append(
            Difference(
                path=f'tracking_stats["{zone}"]',
                legacy=None,
                new=_summarise_zone(new[zone], tolerance),
                classification=Classification.BREAKING,
                reason=(
                    f"zone {zone!r} is present in tracking_stats on the new payload and absent "
                    "on the legacy one -- a new ClickHouse series."
                ),
                legacy_present=False,
                new_present=True,
            )
        )
    for legacy_zone, zone in pairs:
        left, right = _as_mapping(legacy[legacy_zone]), _as_mapping(new[zone])
        prefix = f'tracking_stats["{zone}"]'
        if legacy_zone != zone:
            out.append(
                Difference(
                    path=ZONE_KEY_PATH,
                    legacy=legacy_zone,
                    new=zone,
                    classification=Classification.BREAKING,
                    reason=(
                        f"the tracking_stats key changed from {legacy_zone!r} to {zone!r}. Every "
                        "top-level key is stamped onto raw_analytics.zoneId, so a rename is a "
                        "new series -- unless it is one of the registered deliberate changes."
                    ),
                    legacy_present=True,
                    new_present=True,
                )
            )
        for name in ("input_timestamp", "reset_timestamp"):
            out += _diff_scalar(
                f"{prefix}.{name}",
                left.get(name, _ABSENT),
                right.get(name, _ABSENT),
                tolerance,
                breaking_reason="",
                benign_reason=(
                    "per-zone timestamp; allowed to differ (legacy is wall-clock, the new "
                    "engine is frame time -- PY-13)."
                ),
            )
        for name in COUNT_LISTS:
            out += _diff_count_list(
                f"{prefix}.{name}", left.get(name), right.get(name), name, tolerance
            )
    return out


def _pair_zone_keys(
    legacy: Mapping[str, Any], new: Mapping[str, Any]
) -> tuple[list[tuple[str, str]], list[str], list[str]]:
    """Match legacy zone keys to new zone keys before anything is compared.

    Three passes, most specific first:

    1. **exact name.**
    2. **``__global__`` -> ``global``** (**PY-6**) -- the two spellings of one bucket.
    3. **a non-zone key -> the new payload's single remaining key** (**PY-5**) -- the legacy
       key is ``str(frame_number)``, the literal ``"None"``, ``"current_frame"`` or empty,
       so it names no zone at all and there is only one bucket it can mean.

    Pairing before comparing is what stops a rename's IMPROVEMENT classification from
    swallowing the two zones' counts.  Reporting the rename as "one zone vanished, another
    appeared" would mean a count regression inside a renamed zone is never even looked at.

    Returns:
        ``(pairs, legacy_only, new_only)``, all deterministically ordered.
    """
    pairs: list[tuple[str, str]] = []
    legacy_left = list(legacy)
    new_left = list(new)

    for zone in sorted(set(legacy_left) & set(new_left)):
        pairs.append((zone, zone))
        legacy_left.remove(zone)
        new_left.remove(zone)

    if LEGACY_GLOBAL_SENTINEL in legacy_left and CANONICAL_GLOBAL_ZONE in new_left:
        pairs.append((LEGACY_GLOBAL_SENTINEL, CANONICAL_GLOBAL_ZONE))
        legacy_left.remove(LEGACY_GLOBAL_SENTINEL)
        new_left.remove(CANONICAL_GLOBAL_ZONE)

    non_zone = [key for key in legacy_left if _NON_ZONE_KEY_RE.match(key)]
    if len(non_zone) == 1 and len(new_left) == 1:
        pairs.append((non_zone[0], new_left[0]))
        legacy_left.remove(non_zone[0])
        new_left.remove(new_left[0])

    return (pairs, sorted(legacy_left), sorted(new_left))


def _summarise_zone(value: Any, tolerance: TolerancePolicy) -> dict[str, Any]:
    """A zone block reduced to its four count lists, for a readable report line."""
    block = _as_mapping(value)
    return {name: _counts_by_category(block.get(name), tolerance) for name in COUNT_LISTS}


def _diff_count_list(
    path: str, left: Any, right: Any, list_name: str, tolerance: TolerancePolicy
) -> list[Difference]:
    """Compare one count list, matched by ``category`` rather than by position."""
    reasons = {
        "current_counts": (
            "current_counts feeds raw_analytics.count -- the primary series. One object of "
            "drift here is exactly what this harness exists to catch."
        ),
        "total_current_counts": (
            "total_current_counts is the occupancy carry (previous window's last-frame "
            "current + this window's new arrivals) and feeds the backend's totalCount "
            "rollup formula (PY-4). It is NOT a copy of current_counts."
        ),
        "current_new_counts": (
            "current_new_counts is read by the instant-metric / dataField path (FROZEN-5)."
        ),
        "total_counts": (
            "total_counts is cumulative-since-restart (FROZEN-4) and is read by the "
            "instant-metric / dataField path (FROZEN-5)."
        ),
    }
    reason = reasons.get(list_name, "count list difference.")
    out: list[Difference] = []
    legacy_counts = _counts_by_category(left, tolerance)
    new_counts = _counts_by_category(right, tolerance)
    for category in sorted(set(legacy_counts) | set(new_counts)):
        legacy_count = legacy_counts.get(category, _ABSENT)
        new_count = new_counts.get(category, _ABSENT)
        if tolerance.absent_count_is_zero:
            legacy_count = 0 if legacy_count is _ABSENT else legacy_count
            new_count = 0 if new_count is _ABSENT else new_count
        if legacy_count == new_count:
            continue
        out.append(
            Difference(
                path=f'{path}["{category}"].count',
                legacy=_present_or_none(legacy_count),
                new=_present_or_none(new_count),
                classification=Classification.BREAKING,
                reason=f"count differs for category {category!r}. {reason}",
                legacy_present=category in legacy_counts,
                new_present=category in new_counts,
            )
        )
    return out


# -- metrics ----------------------------------------------------------------


def _metrics_by_key(value: Any) -> dict[tuple[str, str], dict[str, Any]]:
    """``metrics[]`` indexed by ``(key, zone)`` -- list order is not contractual.

    ``zone`` defaults to ``"global"``, which is what the contract says the producer means
    when it does not set it (§2.3); ``zone_id`` is accepted on input because the Go DTO
    accepts both, with ``zone`` winning (**PY-8**).
    """
    out: dict[tuple[str, str], dict[str, Any]] = {}
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return out
    for entry in value:
        if not isinstance(entry, Mapping):
            continue
        key = str(entry.get("key", ""))
        if not key:
            continue
        zone = str(entry.get("zone") or entry.get("zone_id") or CANONICAL_GLOBAL_ZONE)
        out[(key, zone)] = dict(entry)
    return out


def _pair_metric_idents(
    legacy: Mapping[tuple[str, str], dict[str, Any]],
    new: Mapping[tuple[str, str], dict[str, Any]],
    key_map: UsecaseKeyMap = EMPTY_KEY_MAP,
) -> tuple[list[tuple[tuple[str, str], tuple[str, str]]], list[tuple[str, str]], list[tuple[str, str]]]:
    """Match ``(key, zone)`` idents across the two payloads before anything is compared.

    Three passes, most specific first:

    1. **exact ident** -- same key, same zone.
    2. **the verification key map** (:mod:`~matrice_analytics.engine.migration.keymap`) --
       a legacy key the map pairs with a new key, at the same zone if both sides have one
       there, otherwise the map's single remaining candidate.  This is the only pass that
       crosses a *key* boundary, and it crosses it only where a reviewed, cited entry says
       the two keys are the same measurement.
    3. **a re-spelled zone** -- for a metric key that exists on both sides under exactly one
       zone label each, the two labels are treated as the same series (**PY-6**
       ``"__global__"`` -> ``"global"``, **PY-5** a frame-number key -> a zone id).

    Pairing before comparing is what keeps a re-label -- of the zone *or* of the key -- from
    hiding a changed value: the pair's ``data``, ``agg_type`` and ``category`` are still
    compared, and a disagreement there is still BREAKING.

    Returns:
        ``(renamed_pairs, legacy_only, new_only)``.  ``renamed_pairs`` holds only the pairs
        whose idents differ; identical idents need no pairing record and are compared by the
        caller's intersection walk.
    """
    pairs: list[tuple[tuple[str, str], tuple[str, str]]] = []
    legacy_left = [ident for ident in legacy if ident not in new]
    new_left = [ident for ident in new if ident not in legacy]

    # Pass 2 -- the key map.  Sorted, so the pairing cannot depend on dict order.
    for legacy_ident in sorted(legacy_left):
        mapped_key = key_map.new_key_for(legacy_ident[0])
        if not mapped_key:
            continue
        candidates = [ident for ident in new_left if ident[0] == mapped_key]
        same_zone = [ident for ident in candidates if ident[1] == legacy_ident[1]]
        if same_zone:
            chosen = same_zone[0]
        elif len(candidates) == 1 and sum(1 for i in legacy_left if i[0] == legacy_ident[0]) == 1:
            # One legacy spelling, one new spelling, different zone labels: the zone was
            # re-spelled too (PY-6). Any other multiplicity is ambiguous, so it is left
            # unpaired and reported rather than guessed at.
            chosen = candidates[0]
        else:
            continue
        pairs.append((legacy_ident, chosen))
        legacy_left.remove(legacy_ident)
        new_left.remove(chosen)

    # Pass 3 -- same key, re-spelled zone.
    for key in sorted({ident[0] for ident in legacy_left} & {ident[0] for ident in new_left}):
        legacy_matches = [ident for ident in legacy_left if ident[0] == key]
        new_matches = [ident for ident in new_left if ident[0] == key]
        if len(legacy_matches) != 1 or len(new_matches) != 1:
            continue
        pairs.append((legacy_matches[0], new_matches[0]))
        legacy_left.remove(legacy_matches[0])
        new_left.remove(new_matches[0])
    return (pairs, sorted(legacy_left), sorted(new_left))


def _diff_metric_entry(
    prefix: str,
    legacy_entry: Mapping[str, Any],
    new_entry: Mapping[str, Any],
    tolerance: TolerancePolicy,
) -> list[Difference]:
    """Compare one matched ``metrics[]`` entry: ``agg_type``, ``category``, ``data``."""
    out: list[Difference] = []
    agg_type = str(new_entry.get("agg_type", ""))
    out += _diff_scalar(
        f"{prefix}.agg_type",
        legacy_entry.get("agg_type", _ABSENT),
        new_entry.get("agg_type", _ABSENT),
        tolerance,
        breaking_reason=(
            "agg_type change. It decides how 60 seconds of frames collapse into one number, "
            "so 'sum' where the truth is 'max' multiplies the value by the frame count "
            "(PY-1). An unrecognised value is now a manifest-load error, never a runtime "
            "fallback (contract §2.3)."
        ),
    )
    out += _diff_scalar(
        f"{prefix}.category",
        legacy_entry.get("category", _ABSENT),
        new_entry.get("category", _ABSENT),
        tolerance,
        breaking_reason=(
            "category change. VOLUME / SAFETY / QUALITY is how the dashboard routes the "
            "metric; a change moves the series to a different page (contract §2.3)."
        ),
    )
    legacy_data = legacy_entry.get("data", _ABSENT)
    new_data = new_entry.get("data", _ABSENT)
    if not _scalar_equal(f"{prefix}.data", legacy_data, new_data, tolerance):
        out.append(
            Difference(
                path=f"{prefix}.data",
                legacy=_present_or_none(legacy_data),
                new=_present_or_none(new_data),
                classification=Classification.BREAKING,
                # The literal 'agg_type=<...>' is what the PY-1 predicate reads: the
                # deliberate change is only about mean, and the predicate must not have to
                # re-look-up the payload to find that out.
                reason=(
                    f"metric value differs (agg_type={agg_type or '(unset)'}). This is the "
                    "number the chart draws."
                ),
                legacy_present=legacy_data is not _ABSENT,
                new_present=new_data is not _ABSENT,
            )
        )
    return out


def _diff_metrics(
    legacy: Any,
    new: Any,
    tolerance: TolerancePolicy,
    key_map: UsecaseKeyMap = EMPTY_KEY_MAP,
) -> list[Difference]:
    """Compare ``metrics[]`` matched by ``(key, zone)`` (contract §2.3).

    Matched by identity, **never by list position**: the array's order is not contractual
    and the backend indexes by ``key``, so a positional comparison both invents differences
    and hides an ``agg_type`` swap.  Idents whose zone label was re-spelled, or whose key the
    verification map pairs across the two spellings, are paired by
    :func:`_pair_metric_idents` so their values are still compared.

    ``key_map`` only decides *what is compared with what*.  A key it says nothing about is
    still BREAKING when it appears on one payload only -- that is the case the harness
    exists for, and it must not be softened into "probably a rename".
    """
    out: list[Difference] = []
    legacy_metrics = _metrics_by_key(legacy)
    new_metrics = _metrics_by_key(new)
    renamed, legacy_only, new_only = _pair_metric_idents(legacy_metrics, new_metrics, key_map)

    for legacy_ident, new_ident in renamed:
        key = new_ident[0]
        if legacy_ident[0] != key:
            pair = key_map.pair_for_legacy(legacy_ident[0])
            out.append(
                Difference(
                    path=f'metrics["{legacy_ident[0]}"->"{key}"].key',
                    legacy=legacy_ident[0],
                    new=key,
                    # Not BREAKING: the verification map states these are the same
                    # measurement, so the honest report is "renamed, values still checked"
                    # rather than "one metric vanished and an unrelated one appeared".
                    # Listed, never swallowed -- the rename is real and the app owner has to
                    # rebind metrics.json and widgets.json for it.
                    classification=Classification.IMPROVEMENT,
                    reason=(
                        f"metric key {legacy_ident[0]!r} is spelled {key!r} on the new "
                        "engine. The verification key map pairs them, so agg_type, category "
                        "and data below are compared and a disagreement there is still "
                        "BREAKING. VERIFICATION ONLY: this mapping does not rename anything "
                        "at runtime -- a dashboard bound to the legacy key still goes blank "
                        "at cutover unless the app owner rebinds metrics.json and widgets.json."
                        + (f" {pair.note}" if pair and pair.note else "")
                    ),
                    citation=pair.evidence if pair else "",
                    legacy_present=True,
                    new_present=True,
                )
            )
        if legacy_ident[1] != new_ident[1]:
            out.append(
                Difference(
                    path=f'metrics["{key}"].zone',
                    legacy=legacy_ident[1],
                    new=new_ident[1],
                    classification=Classification.BREAKING,
                    reason=(
                        f"the zone label on metric {key!r} changed from {legacy_ident[1]!r} "
                        f"to {new_ident[1]!r}. metrics[].zone reaches ClickHouse alongside "
                        "the value."
                    ),
                    legacy_present=True,
                    new_present=True,
                )
            )
        out += _diff_metric_entry(
            _metric_path(new_ident),
            legacy_metrics[legacy_ident],
            new_metrics[new_ident],
            tolerance,
        )
    for ident in legacy_only:
        out.append(
            _unmatched_metric(ident, legacy_metrics[ident], MetricSide.LEGACY, key_map)
        )
    for ident in new_only:
        out.append(_unmatched_metric(ident, new_metrics[ident], MetricSide.NEW, key_map))
    for ident in sorted(set(legacy_metrics) & set(new_metrics)):
        out += _diff_metric_entry(
            _metric_path(ident), legacy_metrics[ident], new_metrics[ident], tolerance
        )
    return out


#: What :func:`_unmatched_metric` says about a key present on one payload only.
_LEGACY_ONLY_REASON: Final[str] = (
    "metric key present on the legacy payload and absent from the new one. "
    "metrics[].key is a producer-defined, unvalidated namespace: a rename silently empties "
    "every chart and alert rule built on it (contract §2.3, and PY-1b for what that looks "
    "like in production)."
)

_NEW_ONLY_REASON: Final[str] = (
    "metric key present on the new payload and absent from the legacy one. Nothing "
    "downstream is bound to it until metrics.json declares it (PY-1b)."
)


def _unmatched_metric(
    ident: tuple[str, str],
    entry: Mapping[str, Any],
    side: MetricSide,
    key_map: UsecaseKeyMap,
) -> Difference:
    """One metric key that ended up on one payload only.

    Three outcomes, and keeping them apart is the point of the key map:

    * the map registers this key, **on this side**, as deliberately having no counterpart ->
      IMPROVEMENT, with the registered rationale and citation;
    * the map *pairs* this key but the partner is missing from the other payload -> BREAKING,
      and the reason names the partner, because "the map says entry_count should be here and
      it is not" is a much sharper finding than "a key is missing";
    * the map says nothing -> BREAKING, unchanged.  An unmapped key is not a rename until
      somebody has looked at it and written down why.
    """
    is_legacy = side is MetricSide.LEGACY
    key = ident[0]
    deliberate = key_map.unpaired_for(key, side)
    if deliberate is not None:
        return Difference(
            path=_metric_path(ident),
            legacy=dict(entry) if is_legacy else None,
            new=None if is_legacy else dict(entry),
            classification=Classification.IMPROVEMENT,
            reason=(
                f"metric {key!r} is registered as having no counterpart on the "
                f"{'new' if is_legacy else 'legacy'} side: {deliberate.rationale} "
                "This is a reviewed 'no counterpart', not an unmapped key -- an unmapped key "
                "is still BREAKING."
            ),
            citation=deliberate.evidence,
            legacy_present=is_legacy,
            new_present=not is_legacy,
        )
    expected = key_map.new_key_for(key) if is_legacy else key_map.legacy_key_for(key)
    reason = _LEGACY_ONLY_REASON if is_legacy else _NEW_ONLY_REASON
    if expected:
        reason = (
            f"the verification key map pairs {key!r} with {expected!r}, but no such metric is "
            f"on the {'new' if is_legacy else 'legacy'} payload at a matching zone -- so the "
            f"pairing could not be applied. {reason}"
        )
    return Difference(
        path=_metric_path(ident),
        legacy=dict(entry) if is_legacy else None,
        new=None if is_legacy else dict(entry),
        classification=Classification.BREAKING,
        reason=reason,
        legacy_present=is_legacy,
        new_present=not is_legacy,
    )


def _metric_path(ident: tuple[str, str]) -> str:
    key, zone = ident
    return f'metrics["{key}"@"{zone}"]'
