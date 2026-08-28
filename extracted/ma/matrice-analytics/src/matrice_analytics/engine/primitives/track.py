"""``track`` -- ID association, with all six methods reachable from the manifest.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §1 (the primitive),
``_contracts/09-tobe-engine-architecture.md`` §3 (the interface), §4 (state) and §6 (no
models, no I/O, no threads inside a primitive).

**What this file is for.**  Today the new flow's tracker is constructed at
``analytics/engine_session.py:483`` with seven literal numbers and one hard-coded class::

    cfg = TrackerConfig(track_high_thresh=0.4, ..., frame_rate=25)
    namespace = str(hash(stream_key) % 1000000) if stream_key else None
    self._tracker = AdvancedTracker(cfg, namespace=namespace)

No manifest can reach any of it -- not the method, not one threshold -- which is why every
use case that wanted a different tracker shipped its own copy.  :class:`TrackConfig` is the
manifest's handle on those knobs and this module is the one implementation behind it
(objective **O2**).

**Six methods, one association core.**  ``post_processing/Trackers/`` reaches its six
trackers through vendored clones and optional wheels: BoT-SORT needs ``cython_bbox`` and
``lap``, DeepSORT prefers ``deep-sort-realtime``, OC-SORT is a git clone pushed onto
``sys.path`` at import time (``Trackers/det_utils.ensure_vendor_on_path``), and the
``advanced`` tracker pulls ``numpy`` + ``scipy``.  A pipeline stage may not do any of that
(``09`` §6, and **PY-20**: an engine import that drags in the legacy tree costs 179 modules
and torch).  So the *logic* is ported, not the structure: one alpha-beta motion model, one
IoU association, one Hungarian solver, in the standard library -- and the six methods are
six :class:`_MethodProfile` parameterisations of it.  What each method actually contributes
is documented on :data:`_PROFILES`, including what is **not** ported.

**Confirmation is a manifest knob, not just an algorithm detail.**  Each method carries its
own ``min_hits`` (``advanced``/``bytetrack``/``botsort`` 1, ``sort`` 2, ``oc_sort``/``deepsort``
3), and with the default ``method: advanced`` that means a one-frame ghost detection counts.
Legacy footfall confirmed a track over three consecutive frames first
(``post_processing/usecases/people_counting.py:1196-1213``), so ``TrackConfig.min_hits``
overrides the method default and lets a migrated app keep that behaviour.  The per-method
numbers are untouched -- they are what each algorithm calls for.

Three constraints, each with a defect behind it:

**Deterministic track-id namespaces** (**PY-9**).  ``engine_session.py:499`` derives the
tracker namespace from ``hash(stream_key) % 1000000``.  ``hash()`` on a ``str`` is salted
by ``PYTHONHASHSEED``, so that namespace is a different number on every process start and
no track state can survive a restart.  :func:`~matrice_analytics.engine.state.store.stable_namespace`
is the same idea over ``hashlib`` and is used here for exactly that job.

**Frame time, never wall time** (**PY-13**).  :attr:`TrackState.first_seen` and
:attr:`TrackState.last_seen` come from :attr:`FrameContext.frame_ts`.  This module does not
import :mod:`time`.  The legacy recovery pool calls ``time.time()``
(``advanced_tracker/tracker.py:587``), so on replay every lost track expires against
wall-clock and re-identification silently stops working.

**All state in the store** (``09`` §4 rule 1, **D6**).  The tracker is not an object held on
``self``; it is a plain JSON-shaped dict under one
:attr:`~matrice_analytics.engine.state.store.Lifetime.PERSISTENT` key, and the association
code is pure functions over it.  That is also the only correct lifetime: a tracker cleared
at the 60-second boundary renumbers every object in frame once a minute, which downstream
reads as a footfall spike at :00 rather than as a bug.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, ClassVar

from matrice_analytics.engine.manifest.models import TrackConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    PipelineDetection,
    PrimitiveOutput,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.state import Lifetime, StateStore, stable_namespace

__all__ = ["Track"]


Box = tuple[float, float, float, float]
"""A box as ``(xmin, ymin, xmax, ymax)`` in the contract's normalized 0-1 space.

IoU is scale invariant, so association works directly in normalized coordinates and this
primitive never needs ``StreamInfo.resolution`` -- which also means it cannot make the
1920x mistake **PY-7** is about.
"""

#: The one state key holding the whole tracker.  PERSISTENT: a tracker is a fact about the
#: world, not a measurement of the current window (``09`` §4 rule 2).
_TRACKER_KEY = "tracker"

#: WINDOW-lifetime peak of ``active_tracks``, so :meth:`Track.window` reports the truth
#: even when the runtime does not retain per-frame outputs.
_PEAK_ACTIVE_KEY = "window_peak_active"

#: WINDOW-lifetime *last* ``active_tracks``. A window output is published verbatim, so the peak
#: and the current level need two names or ``agg_type: last`` silently gets the peak.
_LAST_ACTIVE_KEY = "window_last_active"

#: Track ids are ``namespace * _ID_STRIDE + local``.  ``Detection.track_id`` is an ``int``
#: on the wire, so the namespace cannot be the legacy ``"<ns>_<id>"`` string -- it is folded
#: into the integer instead.  A stride of a billion means a camera would have to create
#: 10^9 tracks before it could collide with the next namespace.
_ID_STRIDE = 1_000_000_000

#: Alpha-beta gains for the constant-velocity motion model.  ``alpha`` is how much of the
#: measurement is believed (position), ``beta`` how fast the velocity estimate adapts.
#: These are the steady-state behaviour of the Kalman filter in
#: ``advanced_tracker/kalman_filter.py`` for a constant-velocity model, without the 8x8
#: matrix algebra -- and therefore without numpy (**PY-20**).
_ALPHA = 0.8
_BETA = 0.15

#: How much of a lost track's velocity is believed while it has no measurements.
_LOST_DAMPING = 0.5

#: Cost stamped on a track/detection pair of different entities.  Large and finite: the
#: Hungarian solver cannot take an infinity, and any value above every gate is rejected.
_NO_MATCH = 1e6

#: How many past observations a track keeps, for OC-SORT's direction-consistency term.
_OBSERVATION_MEMORY = 4


# ---------------------------------------------------------------------------
# Geometry and assignment -- stdlib only
# ---------------------------------------------------------------------------


def iou(a: Box, b: Box) -> float:
    """Intersection over union of two boxes.

    Args:
        a: First box, ``(xmin, ymin, xmax, ymax)``.
        b: Second box.

    Returns:
        ``0.0`` for disjoint or degenerate boxes, up to ``1.0`` for identical ones.
    """
    left = max(a[0], b[0])
    top = max(a[1], b[1])
    right = min(a[2], b[2])
    bottom = min(a[3], b[3])
    if right <= left or bottom <= top:
        return 0.0
    intersection = (right - left) * (bottom - top)
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - intersection
    if union <= 0.0:
        return 0.0
    return intersection / union


def _center(box: Box) -> tuple[float, float]:
    """Box centre, ``(x, y)``."""
    return (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0


def hungarian(cost: list[list[float]]) -> list[tuple[int, int]]:
    """Optimal one-to-one assignment minimising total cost (Jonker-Volgenant).

    The shortest-augmenting-path form of the Hungarian algorithm, ``O(n^2 m)``.  It is here
    rather than ``scipy.optimize.linear_sum_assignment`` because a primitive may not import
    scipy (**PY-20**); it returns the same optimum, and at the frame sizes this runs at
    (tens of boxes) the pure-Python cost is irrelevant next to being able to import the
    engine at all.

    Greedy nearest-neighbour matching was the alternative and is rejected on purpose: it
    swaps the ids of two objects that cross, and an id swap is invisible in the counts
    while corrupting every downstream dwell and unique count.

    Args:
        cost: An ``n x m`` cost matrix.  Rows and columns may differ in length.

    Returns:
        ``(row, column)`` pairs, at most ``min(n, m)`` of them, sorted by row.  Every cost
        is assigned -- the caller drops the pairs it considers too expensive.
    """
    rows = len(cost)
    columns = len(cost[0]) if rows else 0
    if rows == 0 or columns == 0:
        return []
    transposed = rows > columns
    matrix = [[cost[r][c] for r in range(rows)] for c in range(columns)] if transposed else cost
    n = len(matrix)
    m = len(matrix[0])

    infinity = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (m + 1)
    parent = [0] * (m + 1)  # parent[j] = 1-based row currently matched to column j
    way = [0] * (m + 1)

    for i in range(1, n + 1):
        parent[0] = i
        j0 = 0
        minimum = [infinity] * (m + 1)
        used = [False] * (m + 1)
        while True:
            used[j0] = True
            i0 = parent[j0]
            delta = infinity
            j1 = 0
            for j in range(1, m + 1):
                if used[j]:
                    continue
                current = matrix[i0 - 1][j - 1] - u[i0] - v[j]
                if current < minimum[j]:
                    minimum[j] = current
                    way[j] = j0
                if minimum[j] < delta:
                    delta = minimum[j]
                    j1 = j
            for j in range(m + 1):
                if used[j]:
                    u[parent[j]] += delta
                    v[j] -= delta
                else:
                    minimum[j] -= delta
            j0 = j1
            if parent[j0] == 0:
                break
        while j0:
            j1 = way[j0]
            parent[j0] = parent[j1]
            j0 = j1

    pairs = [(parent[j] - 1, j - 1) for j in range(1, m + 1) if parent[j] != 0]
    if transposed:
        pairs = [(column, row) for row, column in pairs]
    return sorted(pairs)


def assign(cost: list[list[float]], threshold: float) -> tuple[list[tuple[int, int]], list[int], list[int]]:
    """Optimal assignment, then drop every pair costing more than ``threshold``.

    The order matters and is the legacy behaviour
    (``advanced_tracker/matching.linear_assignment``): solving first and gating second
    keeps the assignment globally optimal, where gating first would let a cheap-but-wrong
    pair win because the right one was pruned.

    Args:
        cost: An ``n x m`` cost matrix.
        threshold: The maximum acceptable cost.  **This is a cost, not an IoU** --
            ``TrackConfig.match_thresh`` of ``0.8`` accepts an IoU as low as ``0.2``.  The
            legacy field name reads like a similarity and is not one; the semantics are
            preserved here rather than quietly inverted, because inverting them would
            change the behaviour of every migrated app.

    Returns:
        ``(pairs, unmatched_rows, unmatched_columns)``.
    """
    rows = len(cost)
    columns = len(cost[0]) if rows else 0
    if rows == 0 or columns == 0:
        return [], list(range(rows)), list(range(columns))
    pairs = [(r, c) for r, c in hungarian(cost) if cost[r][c] <= threshold]
    matched_rows = {r for r, _ in pairs}
    matched_columns = {c for _, c in pairs}
    return (
        pairs,
        [r for r in range(rows) if r not in matched_rows],
        [c for c in range(columns) if c not in matched_columns],
    )


# ---------------------------------------------------------------------------
# The six methods
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class _MethodProfile:
    """What distinguishes one tracking method from another, as data.

    Everything the six trackers genuinely disagree about, and nothing else.  A profile is
    not a config: :class:`TrackConfig` always wins where the two overlap, so a manifest can
    say ``method: bytetrack`` and still set ``match_thresh``.
    """

    high_thresh: float
    """Detections at or above this go to the first (strong) association pass."""
    low_thresh: float
    """Floor for the second pass.  Below it a detection is ignored entirely."""
    second_stage: bool
    """Run BYTE's low-confidence recovery pass."""
    second_cost: float
    """Cost gate for the second pass -- IoU only, never score-fused."""
    unconfirmed_cost: float
    """Cost gate for matching not-yet-confirmed tracks."""
    fuse_score: bool
    """Weight the IoU similarity by detection confidence before gating."""
    min_hits: int
    """Frames a track must be seen before it is emitted.  ``1`` emits immediately.

    The method's *default*.  ``TrackConfig.min_hits`` overrides it when set -- these numbers
    are what each algorithm calls for, and are not adjusted to suit a use case.
    """
    recovery_pool: bool
    """Keep removed tracks for IoU re-identification (the ``advanced`` tracker's re-ID)."""
    observation_centric: bool
    """OC-SORT: re-seed velocity from the last real observation when a lost track returns,
    instead of trusting the drifted motion estimate."""
    direction_weight: float
    """OC-SORT OCM: weight of the velocity-direction consistency term in the cost."""
    cascade: bool
    """DeepSORT: match tracks in ascending order of how long they have been unseen."""


_PROFILES: dict[str, _MethodProfile] = {
    "advanced": _MethodProfile(
        # Ported from post_processing/advanced_tracker/. Thresholds are the ones
        # engine_session.py:483 hard-codes, which is the behaviour in production today.
        high_thresh=0.4,
        low_thresh=0.05,
        second_stage=True,
        second_cost=0.4,
        unconfirmed_cost=0.6,
        fuse_score=True,
        min_hits=1,
        recovery_pool=True,
        observation_centric=False,
        direction_weight=0.0,
        cascade=False,
    ),
    "bytetrack": _MethodProfile(
        # BYTE: two-stage association, the second pass over the detections everyone else
        # throws away. The whole method is that second pass.
        high_thresh=0.5,
        low_thresh=0.1,
        second_stage=True,
        second_cost=0.5,
        unconfirmed_cost=0.7,
        fuse_score=True,
        min_hits=1,
        recovery_pool=False,
        observation_centric=False,
        direction_weight=0.0,
        cascade=False,
    ),
    "botsort": _MethodProfile(
        # BoT-SORT = BYTE + camera-motion compensation + ReID. Neither is portable here: a
        # primitive gets detections, not frames (no CMC input), and may not load a model
        # (09 §6, and the legacy adapter defaults to `botsort_with_reid=False` anyway).
        # What remains is BYTE with BoT-SORT's stricter high-confidence gate.
        high_thresh=0.6,
        low_thresh=0.1,
        second_stage=True,
        second_cost=0.5,
        unconfirmed_cost=0.7,
        fuse_score=True,
        min_hits=1,
        recovery_pool=False,
        observation_centric=False,
        direction_weight=0.0,
        cascade=False,
    ),
    "sort": _MethodProfile(
        # SORT: one IoU pass over all detections, and min_hits before a track is believed.
        # No second stage -- that is precisely what ByteTrack added.
        high_thresh=0.0,
        low_thresh=0.0,
        second_stage=False,
        second_cost=0.75,
        unconfirmed_cost=0.75,
        fuse_score=False,
        min_hits=2,
        recovery_pool=False,
        observation_centric=False,
        direction_weight=0.0,
        cascade=False,
    ),
    "oc_sort": _MethodProfile(
        # OC-SORT: observation-centric. Two of its three ideas port cleanly -- OCM (the
        # direction-consistency term below) and OCR (re-seeding velocity from the last real
        # observation). ORU, which rewrites a track's history backwards after a
        # re-association, is NOT ported: it needs the full Kalman trajectory, and its gain
        # is in the smoothed boxes rather than in the ids, which is what this stage exists
        # to produce.
        high_thresh=0.3,
        low_thresh=0.1,
        second_stage=True,
        second_cost=0.5,
        unconfirmed_cost=0.7,
        fuse_score=False,
        min_hits=3,
        recovery_pool=True,
        observation_centric=True,
        direction_weight=0.2,
        cascade=False,
    ),
    "deepsort": _MethodProfile(
        # DeepSORT without the "deep": the matching cascade and the IoU gate, no appearance
        # embedding. That is not a shortcut, it is the legacy default -- Trackers/config.py
        # ships `deepsort_embedder=None`, documented as "IoU-only via dummy embeds",
        # because a ReID network cannot run inside a post-processing stage (09 §6).
        high_thresh=0.3,
        low_thresh=0.0,
        second_stage=False,
        second_cost=0.7,
        unconfirmed_cost=0.7,
        fuse_score=False,
        min_hits=3,
        recovery_pool=False,
        observation_centric=False,
        direction_weight=0.0,
        cascade=True,
    ),
}

METHODS: tuple[str, ...] = tuple(sorted(_PROFILES))
"""The six method names :class:`TrackConfig` accepts.  Kept in step with the manifest's
``Literal`` by :func:`_profile_for`, which fails loudly on a name it does not know."""


def _profile_for(method: str) -> _MethodProfile:
    """The profile for a manifest method name.

    Raises:
        ValueError: The manifest accepts a method this module has no profile for.  That is
            a loud failure on purpose: the alternative is silently tracking with the wrong
            algorithm, which shows up months later as an unexplained count drift.
    """
    try:
        return _PROFILES[method]
    except KeyError:
        raise ValueError(
            f"track.method={method!r} has no implementation profile. TrackConfig accepts "
            f"{', '.join(METHODS)}; a name the manifest allows but this module does not "
            f"implement would otherwise be tracked with the wrong algorithm, silently."
        ) from None


# ---------------------------------------------------------------------------
# The tracker: pure functions over a plain-dict state blob
# ---------------------------------------------------------------------------


def _new_blob(id_base: int) -> dict[str, Any]:
    """An empty tracker.

    Plain lists, dicts, floats and strings all the way down.  ``09`` §4 says a durable
    backing "will need it to be serialisable, which is a good reason to keep it plain
    now" -- so there are no dataclasses, no tuples and no enums inside the blob.
    """
    return {"tracks": [], "removed": [], "next_local": 0, "frame": 0, "id_base": id_base}


def _box_of(record: dict[str, Any]) -> Box:
    """The track's current box estimate as a tuple."""
    box = record["box"]
    return float(box[0]), float(box[1]), float(box[2]), float(box[3])


def _advance(blob: dict[str, Any]) -> None:
    """Move every track forward one frame under constant velocity.

    Run once at the top of the frame -- the standard predict/associate/correct order, and
    the same place ``advanced_tracker/tracker.py:336`` calls ``multi_predict``.  Predicting
    inside the cost function instead would advance a lost track twice per frame.

    A lost track's velocity is damped rather than trusted: it has no evidence, and an
    undamped estimate walks the box off screen and out of every subsequent IoU gate.
    """
    for record in blob["tracks"]:
        scale = 1.0 if record["state"] == "tracked" else _LOST_DAMPING
        record["box"] = [record["box"][i] + record["vel"][i] * scale for i in range(4)]


def _correct(record: dict[str, Any], measurement: Box, *, reseed_velocity: bool) -> None:
    """Fold a measurement into the track's motion estimate (alpha-beta).

    Args:
        record: The track, already advanced by :func:`_advance`, mutated in place.
        measurement: The matched detection's box.
        reseed_velocity: OC-SORT's OCR.  When a lost track is re-found, the velocity that
            carried it through the gap is a guess; the displacement from its last *real*
            observation to this one is evidence.  Prefer the evidence.
    """
    predicted = _box_of(record)
    residual = [measurement[i] - predicted[i] for i in range(4)]
    record["box"] = [predicted[i] + _ALPHA * residual[i] for i in range(4)]
    if reseed_velocity and record["obs"]:
        last = record["obs"][-1]
        gap = max(1, int(record["misses"]) + 1)
        record["vel"] = [(measurement[i] - float(last[i])) / gap for i in range(4)]
    else:
        record["vel"] = [record["vel"][i] + _BETA * residual[i] for i in range(4)]
    observations: list[list[float]] = record["obs"]
    observations.append(list(measurement))
    if len(observations) > _OBSERVATION_MEMORY:
        del observations[: len(observations) - _OBSERVATION_MEMORY]


def _direction_cost(record: dict[str, Any], measurement: Box) -> float:
    """OC-SORT's OCM term: how far this detection is off the track's heading.

    ``0.0`` for a detection straight ahead, ``1.0`` for one directly behind, ``0.5`` when
    the track has no heading yet.  IoU alone cannot separate two objects passing each
    other; their directions can.
    """
    observations = record["obs"]
    if len(observations) < 2:
        return 0.0
    previous = _center(tuple(observations[0]))  # type: ignore[arg-type]
    latest = _center(tuple(observations[-1]))  # type: ignore[arg-type]
    heading = (latest[0] - previous[0], latest[1] - previous[1])
    target = _center(measurement)
    step = (target[0] - latest[0], target[1] - latest[1])
    heading_norm = math.hypot(*heading)
    step_norm = math.hypot(*step)
    if heading_norm < 1e-9 or step_norm < 1e-9:
        return 0.0
    cosine = (heading[0] * step[0] + heading[1] * step[1]) / (heading_norm * step_norm)
    return (1.0 - max(-1.0, min(1.0, cosine))) / 2.0


@dataclass(frozen=True, slots=True)
class _Observation:
    """One detection as the association code sees it."""

    box: Box
    score: float
    entity: str
    index: int
    """Position in :attr:`FrameContext.detections`, published on the resulting
    :class:`TrackState` so a later stage can get back to the detection without the
    primitive having to mutate the frame's detection tuple."""


class _Tracker:
    """The association core, operating on a blob loaded from the :class:`StateStore`.

    Not a stateful object: :meth:`update` is called with the blob, mutates it, and the
    caller writes it back.  That is what keeps every byte of tracker state visible to the
    state layer (``09`` §4 rule 1) instead of hiding in an instance attribute.
    """

    __slots__ = ("_buffer", "_match_cost", "_max_lost", "_min_hits", "_new_thresh", "_profile")

    def __init__(self, profile: _MethodProfile, config: TrackConfig) -> None:
        """Combine the method's profile with the manifest's overrides.

        The manifest always wins where the two overlap -- that is the whole point of
        :class:`TrackConfig` existing (``engine_session.py:483``).

        :attr:`_min_hits` is the confirmation window, and the one knob where the profile's
        value is only a *default*.  Legacy footfall confirms a track over three consecutive
        frames before counting it
        (``post_processing/usecases/people_counting.py:1196-1213``); the default method here
        (``advanced``) has ``min_hits=1``, so without ``TrackConfig.min_hits`` a one-frame
        ghost detection counts -- a silent behaviour change against legacy.  ``None`` keeps
        the method's own number, so the per-method defaults are untouched.
        """
        self._profile = profile
        self._match_cost = float(config.match_thresh)
        self._new_thresh = float(config.new_track_thresh)
        self._max_lost = int(config.max_time_lost)
        self._buffer = int(config.track_buffer)
        self._min_hits = profile.min_hits if config.min_hits is None else int(config.min_hits)

    # -- cost matrices ------------------------------------------------------

    def _cost(
        self,
        tracks: Sequence[dict[str, Any]],
        observations: Sequence[_Observation],
        *,
        fuse: bool,
        direction: bool,
    ) -> list[list[float]]:
        """IoU cost, optionally score-fused and direction-penalised.

        Entities never match across each other: a person is not a forklift no matter how
        well the boxes overlap.  The legacy trackers are class-agnostic and rely on a
        separate aggregator to repair the damage
        (``advanced_tracker/track_class_aggregator.py``); refusing the match up front is
        cheaper and cannot be forgotten.
        """
        matrix: list[list[float]] = []
        for record in tracks:
            predicted = _box_of(record)
            row: list[float] = []
            for observation in observations:
                if record["entity"] != observation.entity:
                    row.append(_NO_MATCH)
                    continue
                similarity = iou(predicted, observation.box)
                if fuse:
                    similarity *= observation.score
                cost = 1.0 - similarity
                if direction and self._profile.direction_weight:
                    cost += self._profile.direction_weight * _direction_cost(record, observation.box)
                row.append(cost)
            matrix.append(row)
        return matrix

    def _associate(
        self,
        tracks: Sequence[dict[str, Any]],
        observations: Sequence[_Observation],
        threshold: float,
        frame: int,
        frame_ts: float,
        updated: set[int],
        *,
        fuse: bool,
        direction: bool,
    ) -> list[_Observation]:
        """One association pass: cost, assign, apply.  Returns what stayed unmatched.

        The empty cases are handled here rather than in :func:`assign`, which can only see
        the shape of the matrix it is given: a zero-row matrix is ``[]`` and carries no
        record of how many columns it should have had.  Getting that wrong silently drops
        every detection on the first frame, when there are no tracks yet.
        """
        if not tracks or not observations:
            return list(observations)
        pairs, _, unmatched = assign(self._cost(tracks, observations, fuse=fuse, direction=direction), threshold)
        for row, column in pairs:
            self._apply(tracks[row], observations[column], frame, frame_ts, updated)
        return [observations[column] for column in unmatched]

    # -- the frame ----------------------------------------------------------

    def update(
        self,
        blob: dict[str, Any],
        observations: Sequence[_Observation],
        frame_ts: float,
    ) -> list[dict[str, Any]]:
        """Advance the tracker by one frame and return the tracks to emit.

        The pipeline is the BYTE one the ``advanced`` tracker implements
        (``advanced_tracker/tracker.py:303-448``), with the per-method deviations folded in
        as profile flags:

        0. advance every track one frame under its motion model;
        1. split detections into strong and weak by confidence;
        2. associate confirmed tracks (plus lost ones, so they can be re-found) to the
           strong detections;
        3. associate whatever is left to the weak detections -- BYTE's contribution;
        4. offer the remaining strong detections to unconfirmed tracks;
        5. start a track for each strong detection still unmatched, re-using a removed
           track's id when the recovery pool recognises it;
        6. retire tracks unseen for longer than ``max_time_lost``.

        Args:
            blob: The tracker state, mutated in place.
            observations: This frame's detections.
            frame_ts: :attr:`FrameContext.frame_ts` -- frame time, never wall time
                (**PY-13**).

        Returns:
            The track records to emit this frame, i.e. those updated this frame and past
            the confirmation window (``TrackConfig.min_hits``, else the method's default).
        """
        profile = self._profile
        blob["frame"] = int(blob["frame"]) + 1
        frame = int(blob["frame"])
        _advance(blob)

        strong = [o for o in observations if o.score >= profile.high_thresh]
        weak = [o for o in observations if profile.low_thresh <= o.score < profile.high_thresh]

        tracks: list[dict[str, Any]] = blob["tracks"]
        confirmed = [t for t in tracks if t["confirmed"] or t["state"] == "lost"]
        unconfirmed = [t for t in tracks if not t["confirmed"] and t["state"] == "tracked"]

        updated: set[int] = set()

        # 1) strong detections against confirmed + lost tracks
        remaining_strong = list(strong)
        if profile.cascade:
            remaining_strong = self._match_cascade(confirmed, remaining_strong, frame, frame_ts, updated)
        else:
            remaining_strong = self._associate(
                confirmed,
                remaining_strong,
                self._match_cost,
                frame,
                frame_ts,
                updated,
                fuse=profile.fuse_score,
                direction=True,
            )

        # 2) BYTE's second pass: what is left of the tracked pool against weak detections
        if profile.second_stage and weak:
            stale = [t for t in confirmed if t["id"] not in updated and t["state"] == "tracked"]
            self._associate(stale, weak, profile.second_cost, frame, frame_ts, updated, fuse=False, direction=False)

        # 3) unconfirmed tracks get the leftovers
        remaining_strong = self._associate(
            unconfirmed,
            remaining_strong,
            profile.unconfirmed_cost,
            frame,
            frame_ts,
            updated,
            fuse=profile.fuse_score,
            direction=False,
        )

        # An unconfirmed track that missed this frame never existed: it is the one-frame
        # ghost (a shadow, a reflection) that inflates every unique count downstream.
        blob["tracks"] = [t for t in tracks if t["confirmed"] or t["id"] in updated]

        # 4) new tracks. A birth counts as "updated this frame" -- without that, _age would
        #    immediately mark the brand-new track lost and it would never be emitted.
        for observation in remaining_strong:
            if observation.score < self._new_thresh:
                continue
            born = self._birth(blob, observation, frame, frame_ts)
            blob["tracks"].append(born)
            updated.add(int(born["id"]))

        # 5) age everything the frame did not touch, and retire the long-lost
        self._age(blob, updated, frame)

        return [
            record
            for record in blob["tracks"]
            if record["id"] in updated and record["hits"] >= self._min_hits and record["state"] == "tracked"
        ]

    def _match_cascade(
        self,
        tracks: Sequence[dict[str, Any]],
        observations: list[_Observation],
        frame: int,
        frame_ts: float,
        updated: set[int],
    ) -> list[_Observation]:
        """DeepSORT's matching cascade: recently-seen tracks get first refusal.

        Solving one big assignment lets a track that has been missing for 20 frames -- and
        whose predicted box has drifted -- steal a detection from a track that was seen
        last frame.  The cascade removes the possibility by construction.

        Returns:
            The observations still unmatched after every age level.
        """
        remaining = list(observations)
        by_age: dict[int, list[dict[str, Any]]] = {}
        for record in tracks:
            by_age.setdefault(int(record["misses"]), []).append(record)
        for age in sorted(by_age):
            if not remaining:
                break
            remaining = self._associate(
                by_age[age],
                remaining,
                self._match_cost,
                frame,
                frame_ts,
                updated,
                fuse=self._profile.fuse_score,
                direction=False,
            )
        return remaining

    def _apply(
        self,
        record: dict[str, Any],
        observation: _Observation,
        frame: int,
        frame_ts: float,
        updated: set[int],
    ) -> None:
        """Attach a matched detection to a track."""
        was_lost = record["state"] == "lost"
        _correct(
            record,
            observation.box,
            reseed_velocity=was_lost and self._profile.observation_centric,
        )
        record["state"] = "tracked"
        record["score"] = observation.score
        record["hits"] = int(record["hits"]) + 1
        record["misses"] = 0
        record["last_frame"] = frame
        record["last_seen"] = frame_ts
        record["det_index"] = observation.index
        if record["hits"] >= self._min_hits:
            record["confirmed"] = True
        updated.add(int(record["id"]))

    def _birth(
        self,
        blob: dict[str, Any],
        observation: _Observation,
        frame: int,
        frame_ts: float,
    ) -> dict[str, Any]:
        """Start a track, re-using a recognised removed track's id where allowed."""
        recovered = self._recover(blob, observation) if self._profile.recovery_pool else None
        if recovered is None:
            blob["next_local"] = int(blob["next_local"]) + 1
            track_id = int(blob["id_base"]) * _ID_STRIDE + int(blob["next_local"])
        else:
            track_id = recovered
        return {
            "id": track_id,
            "entity": observation.entity,
            "box": list(observation.box),
            "vel": [0.0, 0.0, 0.0, 0.0],
            "obs": [list(observation.box)],
            "score": observation.score,
            "state": "tracked",
            "hits": 1,
            "misses": 0,
            "start_frame": frame,
            "last_frame": frame,
            "first_seen": frame_ts,
            "last_seen": frame_ts,
            "det_index": observation.index,
            "confirmed": self._min_hits <= 1,
        }

    def _recover(self, blob: dict[str, Any], observation: _Observation) -> int | None:
        """The ``advanced`` tracker's re-identification, ported off the wall clock.

        ``advanced_tracker/tracker.py:577-647`` keeps removed tracks in a pool and expires
        them with ``time.time()``, so on replay the pool empties on real-world elapsed time
        and re-identification stops working (**PY-13**).  Here the pool is bounded by
        ``TrackConfig.track_buffer`` entries instead of by seconds -- a frame-indexed bound
        that replays identically, and the only job ``track_buffer`` has: the legacy
        ``AdvancedTracker`` declares the field, documents it in its README and never reads
        it.
        """
        pool: list[dict[str, Any]] = blob["removed"]
        best_index: int | None = None
        best_iou = 0.3  # the legacy track_recovery_iou_thresh
        for index, entry in enumerate(pool):
            if entry["entity"] != observation.entity:
                continue
            overlap = iou(tuple(entry["box"]), observation.box)  # type: ignore[arg-type]
            if overlap > best_iou:
                best_iou = overlap
                best_index = index
        if best_index is None:
            return None
        return int(pool.pop(best_index)["id"])

    def _age(self, blob: dict[str, Any], updated: set[int], frame: int) -> None:
        """Mark unmatched tracks lost, retire the long-lost, and bound the recovery pool."""
        survivors: list[dict[str, Any]] = []
        for record in blob["tracks"]:
            if int(record["id"]) in updated:
                survivors.append(record)
                continue
            record["misses"] = int(record["misses"]) + 1
            record["det_index"] = -1
            if record["state"] == "tracked":
                record["state"] = "lost"
            if frame - int(record["last_frame"]) > self._max_lost:
                if self._profile.recovery_pool:
                    blob["removed"].append({"id": record["id"], "entity": record["entity"], "box": list(record["box"])})
                continue
            survivors.append(record)
        blob["tracks"] = survivors
        pool: list[dict[str, Any]] = blob["removed"]
        if len(pool) > self._buffer:
            del pool[: len(pool) - self._buffer]


# ---------------------------------------------------------------------------
# The primitive
# ---------------------------------------------------------------------------


@register(name="track")
class Track:
    """ID association for one zone, with the method chosen by the manifest.

    Publishes ``active_tracks`` into :attr:`PrimitiveOutput.values` and one
    :class:`TrackState` per emitted track into :attr:`PrimitiveOutput.tracks`.  The
    ``tracks`` mapping is the contract with downstream stages: ``unique_count``, ``dwell``
    and ``velocity_state`` read it rather than re-implementing tracking, which is the
    duplication this primitive exists to end.

    Each :class:`TrackState` carries ``score`` and ``det_index`` in
    :attr:`TrackState.attributes`.  ``det_index`` indexes
    :attr:`FrameContext.detections`, so a later stage can reach the detection's box without
    this primitive mutating the frame's detection tuple -- primitives do not write to what
    the next stage is about to read (``base.FrameContext``).

    Example:
        >>> from matrice_analytics.engine.state import InMemoryStateStore
        >>> state = InMemoryStateStore().for_primitive("cam-1", "footfall", "global", "track")
        >>> stage = Track(TrackConfig(method="bytetrack"), state)
        >>> out = stage.process(ctx)                       # doctest: +SKIP
        >>> sorted(out.tracks)                             # doctest: +SKIP
        [1, 2]
    """

    name: ClassVar[str] = "track"
    Config: ClassVar[type[TrackConfig]] = TrackConfig

    __slots__ = ("_config", "_id_base", "_state", "_tracker")

    def __init__(self, config: TrackConfig, state: StateStore) -> None:
        """Bind a validated config and an already-scoped state store.

        Args:
            config: The stage's validated :class:`TrackConfig`.  Unlike
                ``engine_session.py:483``, every knob here came from a manifest.
            state: A store scoped to ``<camera_id>/<app_id>/<zone>/<primitive>``.

        Note:
            The track-id namespace is
            :func:`~matrice_analytics.engine.state.store.stable_namespace` over
            :attr:`~matrice_analytics.engine.state.store.StateStore.prefix` -- the store's own
            scope, and **never** ``hash()`` (**PY-9**).  The prefix already encodes camera,
            app, zone and stage, so two cameras cannot collide and the same camera gets the
            same namespace in every process, forever.  It is read off the protocol rather
            than through a ``getattr``: scope identity is part of the ``StateStore``
            contract, so a store that cannot answer is a broken store, not a fallback case.
            An unscoped root store answers ``""``, which is no identity at all; the stage
            name stands in there, and is stable for the same reason.
        """
        self._config = config
        self._state = state
        seed = state.prefix or config.stage_name
        self._id_base = int(stable_namespace(seed))
        self._tracker = _Tracker(_profile_for(config.method), config)

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Associate this frame's detections with the running tracks.

        Args:
            ctx: One frame in one zone.  Boxes are read in the contract's normalized 0-1
                space and never converted to pixels, so this stage needs no resolution and
                cannot make the 1920x mistake (**PY-7**).

        Returns:
            ``active_tracks`` and the per-track :class:`TrackState` mapping.
        """
        blob = self._load()
        observations = [
            _Observation(
                box=(
                    float(detection.bounding_box.xmin),
                    float(detection.bounding_box.ymin),
                    float(detection.bounding_box.xmax),
                    float(detection.bounding_box.ymax),
                ),
                score=float(detection.confidence),
                entity=detection.entity,
                index=index,
            )
            for index, detection in enumerate(ctx.detections)
        ]

        emitted = self._tracker.update(blob, observations, ctx.frame_ts)
        self._state.set(_TRACKER_KEY, blob, lifetime=Lifetime.PERSISTENT)

        tracks = {
            int(record["id"]): TrackState(
                track_id=int(record["id"]),
                entity=str(record["entity"]),
                zone=ctx.zone,
                first_seen=float(record["first_seen"]),
                last_seen=float(record["last_seen"]),
                state=str(record["state"]),
                attributes={
                    "score": float(record["score"]),
                    "hits": int(record["hits"]),
                    "det_index": int(record["det_index"]),
                },
            )
            for record in emitted
        }

        active = len(tracks)
        self._state.set(
            _PEAK_ACTIVE_KEY,
            max(int(self._state.get(_PEAK_ACTIVE_KEY, 0)), active),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set(_LAST_ACTIVE_KEY, active, lifetime=Lifetime.WINDOW)
        return PrimitiveOutput(values={"active_tracks": active}, tracks=tracks)

    def _load(self) -> dict[str, Any]:
        """The tracker blob, created on first use.

        Read through the store rather than cached on ``self``: a cached copy is exactly the
        ``self._counts`` dict ``09`` §4 rule 1 forbids, and it would go stale the moment a
        durable backing was shared between processes.
        """
        blob = self._state.get(_TRACKER_KEY)
        if not isinstance(blob, dict):
            blob = _new_blob(self._id_base)
            self._state.set(_TRACKER_KEY, blob, lifetime=Lifetime.PERSISTENT)
        return blob

    # -- per window ---------------------------------------------------------

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Report the window's simultaneous track count, **both** readings, under two names.

        A sum would publish "1,500 tracks" for one person standing still for a minute
        (**PY-1**); the *distinct* count over the window is ``unique_count``'s job, not this
        one's.  What is left is a level, and a level has two honest window readings:

        ``active_tracks``
            How many were being tracked on the window's **last** frame -- ``agg_type: last``.
        ``active_tracks_peak``
            How many at once at the **busiest** moment -- ``agg_type: max``.

        Both are published because a :class:`WindowOutput` is published verbatim: the runtime
        does not re-apply ``agg_type`` to a registered primitive, so one name could only ever
        carry one of the two numbers, and a manifest asking for the other got this one silently.

        Args:
            frames: This stage's per-frame outputs, in frame order.  Folded into the peak so it
                is right either way; the last reading comes from the store, because the
                runtime caps retention and ``frames[-1]`` is then not the window's last frame.
        """
        peak = int(self._state.get(_PEAK_ACTIVE_KEY, 0))
        for frame in frames:
            value = frame.values.get("active_tracks", 0)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                peak = max(peak, int(value))
        values: dict[str, Scalar] = {
            "active_tracks": int(self._state.get(_LAST_ACTIVE_KEY, 0)),
            "active_tracks_peak": peak,
        }
        return WindowOutput(values=values)

    def reset(self) -> None:
        """Clear the window peak -- and emphatically **not** the tracker.

        ``09`` §4 rule 2.  :meth:`StateStore.end_window` drops the
        :attr:`Lifetime.WINDOW` peak and leaves the
        :attr:`Lifetime.PERSISTENT` tracker blob untouched.  Clearing the tracker here
        would hand every object in frame a brand-new id once a minute; ``unique_count``
        would then count the same person 60 times an hour and the footfall graph would show
        a spike on every window boundary.  That is the single most expensive way to get
        ``reset()`` wrong, and it is why the lifetime is declared at write time rather than
        inferred from which method is clearing what.
        """
        self._state.end_window()


def observations_from(detections: Sequence[PipelineDetection]) -> list[_Observation]:
    """Build tracker observations from detections -- exposed for tests.

    Lets a test drive :class:`_Tracker` directly with the same conversion
    :meth:`Track.process` uses, rather than re-deriving it and drifting.
    """
    return [
        _Observation(
            box=(
                float(detection.bounding_box.xmin),
                float(detection.bounding_box.ymin),
                float(detection.bounding_box.xmax),
                float(detection.bounding_box.ymax),
            ),
            score=float(detection.confidence),
            entity=detection.entity,
            index=index,
        )
        for index, detection in enumerate(detections)
    ]
