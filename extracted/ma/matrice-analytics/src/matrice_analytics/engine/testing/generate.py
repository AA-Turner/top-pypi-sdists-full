"""Derive a whole test suite from a manifest alone -- objective **O5**.

``_contracts/08-tobe-app-manifest.md`` §7 and ``ml-applications/guidelines/FIELD_REFERENCE.md`` §7
both tell app authors, in writing, that *a config-only app writes no tests*.  This module
is what makes that true.  Given nothing but an app reference it produces the checks those
documents promise:

======  ====================  ===================================================
Check   Name                  What it asserts
======  ====================  ===================================================
1       ``schema_validity``   the manifest loads, every ``metrics[].source``
                              resolves against a declared stage, every enum is
                              legal in the *contract's* vocabulary, and every
                              primitive named is registered **and** implemented.
2       ``contract_conformance`` synthesised detections go through a real
                              :class:`~matrice_analytics.engine.runtime.session.Session`
                              and every emitted payload passes all six checks in
                              :mod:`matrice_analytics.engine.contract.conformance`.
3       ``metric_presence``   every declared metric really appears in
                              ``results-agg.metrics[]`` with the declared
                              ``agg_type``, ``category`` and zone shape.
4       ``app_config_files``  ``metrics.json``, ``widgets.json`` and
                              ``post_processing_config.json`` agree with
                              ``app.yaml`` and with each other.
5       ``dashboard_reachability`` every key those files send to ClickHouse is
                              one a real run publishes -- the only check that can
                              verify a ``custom`` stage.
6       ``incident_lifecycle`` a synthetic run produces open -> escalate -> close
                              with a stable ``incident_id`` and monotonic
                              timestamps; severity never goes down and only an
                              ``end_time`` closes an incident.
7       ``determinism``       the same input twice produces **byte-identical**
                              payloads, in two subprocesses with *different*
                              ``PYTHONHASHSEED`` values (**PY-9**).
======  ====================  ===================================================

Checks 4 and 5 need the app *folder*, so they skip for an in-memory manifest and for a
folder that ships none of the three files.

Why checks 3, 4 and 5 exist
---------------------------
A dashboard declaring a metric key the engine never emits is a live production defect: the
join between ``metrics[].key`` and ``metrics.json``'s ``key`` is validated by
nothing at all (``06-vocabularies.md`` §13), so the chart is simply empty forever.  Check 3
is the assertion that would have caught it, and it is why this suite exists per app rather
than once for the engine.

Check 3 only sees the manifest, though, and the manifest is not what the dashboard reads.
Check 4 compares the three uploaded files to it, and check 5 puts their key strings through
a real run.  Check 5 is also the *only* verification a ``custom`` stage ever gets: the
manifest cannot know a ``logic.py``'s value keys, so ``resolve_source`` records the source
as unverified and the runtime merely warns when it is wrong.

Why check 7 runs subprocesses
-----------------------------
**PY-9** is ``str.hash`` salting: ``engine_session.py:499`` namespaces tracker state by
``str(hash(stream_key) % 1000000)``, and that namespace changes on every process start.
Two calls inside one interpreter share one ``PYTHONHASHSEED`` and therefore *cannot* see
it.  So this check runs the app twice, in two fresh interpreters, with two explicit seeds,
and compares a sha256 over the concatenated payload JSON.  A determinism check that could
not have caught the defect it cites would be theatre.

Runnable files, or a parametrised in-process suite?
---------------------------------------------------
**Chosen: a parametrised in-process suite driven by an app reference.**
:func:`suite_checks` returns one :class:`GeneratedCheck` per assertion and a host repo
turns them into pytest cases in four lines::

    from matrice_analytics.engine.testing import suite_checks

    @pytest.mark.parametrize("check", suite_checks(APP_DIR), ids=lambda c: c.name)
    def test_generated_suite(check: GeneratedCheck) -> None:
        result = check()
        assert result.status != "failed", result.detail()

Why, in order of weight:

1. **There is no generated code to be wrong.**  A template emitting Python has two failure
   modes -- the assertion is wrong, or the *rendering* is wrong -- and only the second is
   invisible to the engine's own test suite.  Here the checks are ordinary functions that
   this repo's own tests exercise on all five handover examples, so the thing app authors
   run is the thing we test.
2. **It cannot go stale.**  Emitted files are a snapshot: a manifest edit, or a change to
   the six conformance checks, silently invalidates every previously generated file until
   someone re-runs the generator.  An in-process suite reads the manifest at collection
   time, so it is never out of date with either input.
3. **It reuses the real checks.**  Check 2 calls
   :func:`~matrice_analytics.engine.contract.conformance.conformance_errors` directly, so
   there is exactly one definition of "conforms" in the tree.

What that gives up, honestly:

* **Inspectability.**  An author cannot open ``test_my_app.py``, read the assertions, set a
  breakpoint on line 40, or copy a case as the seed of a hand-written test.
  :func:`describe_suite` is the compensation -- it prints the plan, the synthetic frame
  phases and the exact magnitudes derived from the manifest -- but reading a report is not
  reading code.
* **Local edits.**  Tuning one generated assertion means ``tests.skip`` in the manifest
  (with a written reason, which :class:`~...models.SkipEntry` enforces) plus a hand-written
  replacement, rather than editing a line.
* **Per-assertion granularity is ours, not pytest's.**  Each check reports a list of
  problems instead of failing on the first one.  That is usually better, but it does mean
  one red pytest case can cover twenty distinct violations.

What the generator does *not* consume yet: ``tests.fixtures`` (real recorded frames) and
``tests.golden`` (a golden payload file).  Both are declared in the schema, both are
optional, and neither is read here -- the synthetic run is manifest-derived only.  A
manifest that declares them is not silently degraded: :func:`generate_suite` reports the
gap on the ``schema_validity`` check.

Nothing here imports ``post_processing`` or ``analytics`` (**PY-20**).
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import os
import subprocess  # noqa: S404 - the determinism check is *about* separate interpreters
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Final, Literal

from matrice_analytics.engine.appconfig import (
    CHART_TYPES_RENDERED,
    RESERVED_WIDGET_TOKENS,
    AppConfigBundle,
    load_app_config,
)
from matrice_analytics.engine.contract.conformance import CHECKS, Surface, conformance_errors
from matrice_analytics.engine.contract.emit import to_payload
from matrice_analytics.engine.contract.schemas import (
    GLOBAL_ZONE,
    SEVERITY_RANK,
    AggType,
    Category,
    Severity,
    StreamInfo,
    ZoneConfig,
)
from matrice_analytics.engine.manifest.loader import (
    MANIFEST_FILENAME,
    AppLoadError,
    LoadedApp,
    load_app_bundle,
)
from matrice_analytics.engine.manifest.models import (
    ANALYTICS_CATEGORIES,
    UNIT_DIMENSIONS,
    AppManifest,
    CustomConfig,
    DetectConfig,
    DwellConfig,
    IncidentQuantiseConfig,
    VelocityStateConfig,
    ZoneOccupancyConfig,
    resolve_source,
)
from matrice_analytics.engine.primitives import REGISTRY
from matrice_analytics.engine.runtime.session import Session

if TYPE_CHECKING:  # pragma: no cover - typing only
    from matrice_analytics.engine.manifest.loader import CustomImpl
    from matrice_analytics.engine.runtime.session import FrameOutcome

__all__ = [
    "CHECK_APP_CONFIG",
    "CHECK_CONFORMANCE",
    "CHECK_DETERMINISM",
    "CHECK_INCIDENTS",
    "CHECK_METRICS",
    "CHECK_NAMES",
    "CHECK_REACHABILITY",
    "CHECK_SCHEMA",
    "CheckResult",
    "FramePlan",
    "GeneratedCheck",
    "SuiteResult",
    "SyntheticFrame",
    "SyntheticRun",
    "check_app_config_files",
    "check_contract_conformance",
    "check_dashboard_reachability",
    "check_determinism",
    "check_incident_lifecycle",
    "check_metric_presence",
    "check_schema_validity",
    "describe_suite",
    "frame_plan",
    "generate_suite",
    "main",
    "run_synthetic",
    "suite_checks",
    "synthesise_frames",
    "synthetic_stream_info",
]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Names and constants
# ---------------------------------------------------------------------------

CHECK_SCHEMA: Final[str] = "schema_validity"
CHECK_CONFORMANCE: Final[str] = "contract_conformance"
CHECK_METRICS: Final[str] = "metric_presence"
CHECK_APP_CONFIG: Final[str] = "app_config_files"
CHECK_REACHABILITY: Final[str] = "dashboard_reachability"
CHECK_INCIDENTS: Final[str] = "incident_lifecycle"
CHECK_DETERMINISM: Final[str] = "determinism"

CHECK_NAMES: Final[tuple[str, ...]] = (
    CHECK_SCHEMA,
    CHECK_CONFORMANCE,
    CHECK_METRICS,
    CHECK_APP_CONFIG,
    CHECK_REACHABILITY,
    CHECK_INCIDENTS,
    CHECK_DETERMINISM,
)
"""The generated checks, in ``08`` §7 order.

Checks 4 and 5 (:data:`CHECK_APP_CONFIG`, :data:`CHECK_REACHABILITY`) extend 1-3 from the manifest
to the three files an app version actually uploads.  They sit next to
:data:`CHECK_METRICS` because they answer the other half of the same question -- 3 asks whether the
engine publishes what ``app.yaml`` declares, 4 asks whether ``metrics.json`` and ``widgets.json``
agree with ``app.yaml``, and 5 asks whether the dashboard's own key strings survive a real run.
"""

#: Aliases a ``tests.skip[].test`` entry may use, so an author does not have to guess the
#: internal name.  Skipping is deliberately awkward *enough* to need a reason, not awkward
#: enough to need a lookup table in another file.
_SKIP_ALIASES: Final[dict[str, str]] = {
    "schema": CHECK_SCHEMA,
    "schema_validity": CHECK_SCHEMA,
    "conformance": CHECK_CONFORMANCE,
    "contract": CHECK_CONFORMANCE,
    "contract_conformance": CHECK_CONFORMANCE,
    "metrics": CHECK_METRICS,
    "metric_presence": CHECK_METRICS,
    "app_config": CHECK_APP_CONFIG,
    "app_config_files": CHECK_APP_CONFIG,
    "config_files": CHECK_APP_CONFIG,
    "dashboard": CHECK_REACHABILITY,
    "dashboard_reachability": CHECK_REACHABILITY,
    "reachability": CHECK_REACHABILITY,
    "incidents": CHECK_INCIDENTS,
    "incident_lifecycle": CHECK_INCIDENTS,
    "determinism": CHECK_DETERMINISM,
}

#: The synthetic run's start instant, 2026-01-01T00:00:00Z.  A **fixed** epoch, never
#: ``time.time()`` (**PY-13**): the generated determinism assertion compares payload bytes
#: across two processes, and a wall-clock anchor would make every one of them differ.
SYNTHETIC_EPOCH: Final[float] = 1_767_225_600.0

#: Frame-time step, seconds.  One second per frame keeps a 60 s window at 60 frames, so a
#: generated run crosses real window boundaries without simulating 1,500 frames.
FRAME_STEP_SECONDS: Final[float] = 1.0

#: What the synthetic camera declares.  ``original_fps`` is the *stream's* rate and is
#: independent of :data:`FRAME_STEP_SECONDS` -- dwell and velocity maths divide by it.
SYNTHETIC_FPS: Final[float] = 25.0
SYNTHETIC_RESOLUTION: Final[tuple[int, int]] = (1920, 1080)
SYNTHETIC_CAMERA_ID: Final[str] = "generated-camera"

#: Bounds on the synthesised detection count.  The lower bound keeps a tracker meaningful;
#: the upper one keeps every box inside the normalized 0-1 frame (**BE-10**/**BE-12**: a box
#: outside 0-1 is a hard failure by design, so the generator must never emit one).
_MIN_COUNT: Final[int] = 3
_MAX_COUNT: Final[int] = 36

#: Cap on how much extra ramp/escalate time a `dwell`/`velocity_state` time constant can add
#: (seconds). A manifest cannot declare an upper bound on `threshold_seconds`, so an unclamped
#: value would let one malformed app inflate the whole suite's runtime unboundedly; five
#: minutes comfortably covers any realistic dwell/loiter threshold with margin to spare.
_MAX_DWELL_BOUND_SECONDS: Final[float] = 300.0

#: The two hash seeds check 5 runs under.  Explicit and fixed, because a *random* seed would
#: make the check itself nondeterministic -- and a flaky determinism check is worse than none.
DEFAULT_HASH_SEEDS: Final[tuple[str, str]] = ("0", "1048573")

_DIGEST_FLAG: Final[str] = "--digest"

Status = Literal["passed", "failed", "skipped"]


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CheckResult:
    """The verdict of one generated check.

    Attributes:
        name: One of :data:`CHECK_NAMES`.
        status: ``passed``, ``failed`` or ``skipped``.
        problems: Every violation found, not just the first -- one malformed zone fails a
            whole message on the Go side (**BE-7**), so it is worth reporting all of them.
        reason: Why the check was skipped.  Always set when ``status == "skipped"``: a skip
            without a written reason is how a suite rots (``08`` §7).
        notes: Non-fatal observations -- a declared-but-unread ``tests.fixtures``, a rule
            the synthetic input could not drive.  Never a failure on their own.
    """

    name: str
    status: Status
    problems: tuple[str, ...] = ()
    reason: str = ""
    notes: tuple[str, ...] = ()

    @property
    def failed(self) -> bool:
        """Whether this check reports a real violation."""
        return self.status == "failed"

    def detail(self) -> str:
        """A multi-line explanation suitable for a pytest assertion message."""
        lines = [f"{self.name}: {self.status}"]
        if self.reason:
            lines.append(f"  reason: {self.reason}")
        lines.extend(f"  - {problem}" for problem in self.problems)
        lines.extend(f"  note: {note}" for note in self.notes)
        return "\n".join(lines)

    def __str__(self) -> str:
        suffix = f" ({len(self.problems)} problem(s))" if self.problems else ""
        return f"{self.name}: {self.status}{suffix}"


@dataclass(frozen=True)
class GeneratedCheck:
    """One check, not yet run -- what :func:`suite_checks` hands to pytest.

    Callable so a parametrised test body is one line.  The generated suite is built lazily
    on purpose: a host that parametrises over five apps builds five plans and runs exactly
    the sessions the selected tests need.
    """

    name: str
    description: str
    run: Callable[[], CheckResult]

    def __call__(self) -> CheckResult:
        return self.run()

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


@dataclass(frozen=True, slots=True)
class SuiteResult:
    """Every check's verdict for one app."""

    app_id: str
    source: str
    results: tuple[CheckResult, ...]

    @property
    def passed(self) -> bool:
        """``True`` when nothing failed.  A skip is not a failure; it is a recorded gap."""
        return not any(result.failed for result in self.results)

    @property
    def failures(self) -> tuple[CheckResult, ...]:
        return tuple(result for result in self.results if result.failed)

    def by_name(self, name: str) -> CheckResult:
        """The result of one check.

        Raises:
            KeyError: No check by that name ran.
        """
        for result in self.results:
            if result.name == name:
                return result
        raise KeyError(f"no check named {name!r}; ran: {', '.join(r.name for r in self.results)}")

    def report(self) -> str:
        """A human-readable report -- what the CLI prints and what a CI log should show."""
        verdict = "PASS" if self.passed else "FAIL"
        lines = [f"[{verdict}] {self.app_id}  ({self.source})"]
        for result in self.results:
            mark = {"passed": "ok  ", "failed": "FAIL", "skipped": "skip"}[result.status]
            lines.append(f"  {mark} {result.name}")
            if result.reason:
                lines.append(f"        reason: {result.reason}")
            lines.extend(f"        - {problem}" for problem in result.problems)
            lines.extend(f"        note: {note}" for note in result.notes)
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# The app under test
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class _AppUnderTest:
    """A normalised app: the manifest, its custom code, and how to reload it."""

    manifest: AppManifest | None
    custom: Mapping[str, CustomImpl]
    #: The reference a *fresh interpreter* can reload from -- a folder path or a bare app id.
    #: ``None`` when the caller passed an in-memory manifest, which no subprocess can see.
    ref: str | None
    source: str
    load_error: str = ""
    #: The app folder, when there is one.  ``None`` for an in-memory manifest, which has no
    #: ``metrics.json`` to read -- checks 4 and 5 skip rather than fail in that case.
    root: Path | None = None

    @property
    def app_id(self) -> str:
        return self.manifest.app.id if self.manifest is not None else "<unloadable>"


def _resolve_app(app: str | os.PathLike[str] | AppManifest | LoadedApp) -> _AppUnderTest:
    """Accept any of the four things a caller has, and never raise.

    A load failure is *data* here, not an exception: the suite has to be able to report "the
    manifest does not load" as a red check rather than blowing up during collection.
    """
    if isinstance(app, AppManifest):
        return _AppUnderTest(manifest=app, custom={}, ref=None, source=f"<in-memory manifest {app.app.id}>")
    if isinstance(app, LoadedApp):
        return _AppUnderTest(
            manifest=app.manifest,
            custom=app.custom,
            ref=str(app.root),
            source=str(app.root),
            root=app.root,
        )

    raw = os.fspath(app)
    candidate = Path(raw)
    if candidate.name == MANIFEST_FILENAME and candidate.is_file():
        # An author's muscle memory points at app.yaml; the loader takes the folder.
        raw = str(candidate.parent)
    try:
        bundle = load_app_bundle(raw)
    except AppLoadError as exc:
        folder = Path(raw)
        return _AppUnderTest(
            manifest=None,
            custom={},
            ref=raw,
            source=raw,
            load_error=f"{type(exc).__name__}: {exc}",
            root=folder if folder.is_dir() else None,
        )
    return _AppUnderTest(
        manifest=bundle.manifest,
        custom=bundle.custom,
        ref=raw,
        source=str(bundle.root),
        root=bundle.root,
    )


# ---------------------------------------------------------------------------
# The synthetic input
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SyntheticFrame:
    """One frame of synthesised detections, in the dict shape the pipeline really sends."""

    index: int
    ts: float
    phase: Literal["quiet", "ramp", "escalate", "clear"]
    detections: tuple[dict[str, Any], ...]


@dataclass(frozen=True, slots=True)
class FramePlan:
    """The magnitudes the generator derived from the manifest, and the frames they produce.

    Exposed rather than kept private because it is the answer to "why did my generated
    incident test not open an incident?" -- see :meth:`describe`.
    """

    app_id: str
    labels: tuple[str, ...]
    """One *model label* per mapped entity -- the right-hand side of ``entity_mapping``.

    Synthesising the label rather than the entity name is deliberate: the mapping's
    right-hand side must match the detector character for character (``08`` §3) and nothing
    can check that from the manifest, so the generated run at least exercises the mapping
    the author wrote instead of bypassing it.
    """

    quiet_frames: int
    ramp_frames: int
    escalate_frames: int
    clear_frames: int
    ramp_count: int
    escalate_count: int
    ramp_area: float
    escalate_area: float
    ramp_confidence: float
    escalate_confidence: float
    zone_names: tuple[str, ...]
    line_names: tuple[str, ...]

    @property
    def total_frames(self) -> int:
        return self.quiet_frames + self.ramp_frames + self.escalate_frames + self.clear_frames

    def phases(self) -> tuple[tuple[str, int, int, float, float], ...]:
        """``(phase, frames, count, total_area, confidence)`` for each phase, in order."""
        return (
            ("quiet", self.quiet_frames, 0, 0.0, 0.0),
            ("ramp", self.ramp_frames, self.ramp_count, self.ramp_area, self.ramp_confidence),
            ("escalate", self.escalate_frames, self.escalate_count, self.escalate_area, self.escalate_confidence),
            ("clear", self.clear_frames, 0, 0.0, 0.0),
        )

    def frames(self) -> tuple[SyntheticFrame, ...]:
        """The whole sequence: quiet -> ramp -> escalate -> clear.

        Four phases, because the lifecycle assertion needs all four transitions to be
        observable: a baseline the incident is *not* open in, a magnitude that opens it, a
        larger magnitude that escalates it, and enough empty frames to close it
        (``incidents.lifecycle.close_after_empty_frames``, default 101).
        """
        produced: list[SyntheticFrame] = []
        index = 0
        for phase, frames, count, area, confidence in self.phases():
            for _ in range(frames):
                produced.append(
                    SyntheticFrame(
                        index=index,
                        ts=SYNTHETIC_EPOCH + index * FRAME_STEP_SECONDS,
                        phase=phase,  # type: ignore[arg-type]
                        detections=_detections(self.labels, count, area, confidence, index),
                    )
                )
                index += 1
        return tuple(produced)

    def describe(self) -> str:
        """The plan in words -- the report an author reads instead of generated code."""
        lines = [
            f"synthetic input plan for {self.app_id}",
            f"  model labels emitted : {', '.join(self.labels) or '(none)'}",
            f"  drawn zones          : {', '.join(self.zone_names) or '(none)'}",
            f"  drawn lines          : {', '.join(self.line_names) or '(none)'}",
            f"  frames               : {self.total_frames} at {FRAME_STEP_SECONDS}s of frame time",
        ]
        for phase, frames, count, area, confidence in self.phases():
            lines.append(
                f"  {phase:<9} {frames:>4} frame(s)  {count:>3} detection(s) per label  "
                f"total_area={area:.4f}  confidence={confidence:.2f}"
            )
        return "\n".join(lines)


def _dwell_time_bound(manifest: AppManifest) -> float:
    """Longest per-track warm-up a ``dwell``/``velocity_state`` stage needs, in seconds.

    Population and duration are independent knobs, and only this function accounts for the
    second one. ``_threshold_bounds`` below sizes the ramp/escalate *detection count* so
    enough tracks exist to cross a metric threshold — but a ``dwell`` stage's
    ``over_threshold_count`` cannot go above zero until a track has been continuously
    satisfied for ``threshold_seconds``, and it cannot even start counting until
    ``velocity_state`` has enough history (``window_seconds``) to stop reporting
    ``UNKNOWN_STATE``. A ramp/escalate phase shorter than ``threshold_seconds +
    window_seconds`` can therefore never drive such a metric above zero no matter how many
    detections are synthesised — which is exactly how a correctly configured Loitering
    Detection (``dwell.threshold_seconds: 10``, a 7-frame default ramp) failed
    ``incident_lifecycle`` with "the trigger never fires": the trigger's population was
    right and its clock was not.

    Only relevant when there is an incident to try to reach — an app that merely uses
    ``dwell``/``velocity_state`` for something other than an incident does not need extra
    ramp/escalate time to prove one is reachable, so this returns ``0.0`` and leaves that
    app's synthetic run exactly as short as it was.
    """
    if manifest.incidents is None:
        return 0.0
    dwell_seconds = 0.0
    warmup_seconds = 0.0
    for stage in manifest.pipeline:
        if isinstance(stage, DwellConfig):
            dwell_seconds = max(dwell_seconds, float(stage.threshold_seconds))
        if isinstance(stage, VelocityStateConfig):
            warmup_seconds = max(warmup_seconds, float(stage.window_seconds))
    return min(dwell_seconds + warmup_seconds, _MAX_DWELL_BOUND_SECONDS)


def _dwell_timeout_bound(manifest: AppManifest) -> float:
    """Longest ``dwell.track_timeout_seconds`` any stage declares, in seconds.

    The counterpart to :func:`_dwell_time_bound`, for *closing* rather than opening: once
    detections stop, a track's session is not reaped -- and its stale count keeps
    contributing to ``over_threshold_count`` -- until ``now - last_seen > track_timeout_seconds``
    (:meth:`Dwell._reap`). The incident's own "empty" streak does not start counting until
    that lingering count actually drops to zero, so a ``clear`` phase only ``close_after_empty_frames
    + 4`` long can run out before the streak even begins -- which is exactly how a correctly
    configured Loitering Detection (``close_after_empty_frames: 250``, deliberately matched to
    its own ``track_timeout_seconds: 10``) still failed to close: the margin assumed severity
    drops the instant detections do, and a lingering ``dwell`` session does not.

    Same ``incidents is None`` gate as :func:`_dwell_time_bound`, for the same reason.
    """
    if manifest.incidents is None:
        return 0.0
    timeout_seconds = 0.0
    for stage in manifest.pipeline:
        if isinstance(stage, DwellConfig):
            timeout_seconds = max(timeout_seconds, float(stage.track_timeout_seconds))
    return min(timeout_seconds, _MAX_DWELL_BOUND_SECONDS)


def frame_plan(manifest: AppManifest) -> FramePlan:
    """Derive the synthetic magnitudes from the manifest.

    Every number below comes out of the manifest, which is the whole point: an incident
    threshold of ``> 15`` has to produce 16+ detections or the generated lifecycle assertion
    would fail on a perfectly good app, and an ``area_ratio`` quantiser with
    ``threshold_area: 0.121`` has to see 12% of the frame covered before it reports anything
    at all.
    """
    lifecycle = manifest.incidents.lifecycle if manifest.incidents is not None else None
    confirm = lifecycle.confirm_frames if lifecycle is not None else 5
    close_after = lifecycle.close_after_empty_frames if lifecycle is not None else 101

    # Each of ramp and escalate gets its OWN full dwell-crossing window, rather than relying on
    # a track surviving the ramp->escalate transition to accumulate across both: that survival
    # is a tracker-continuity detail this module should not need to depend on for correctness.
    dwell_frames = _clamp_int(
        math.ceil(_dwell_time_bound(manifest) / FRAME_STEP_SECONDS) + 4, confirm + 4, _MAX_COUNT * 10
    )
    # The clear phase needs close_after_empty_frames PLUS however long a lingering dwell
    # session takes to actually reap -- see _dwell_timeout_bound.
    clear_frames = _clamp_int(
        close_after + math.ceil(_dwell_timeout_bound(manifest) / FRAME_STEP_SECONDS) + 4,
        close_after + 4,
        (_MAX_COUNT * 10) + close_after,
    )

    labels = tuple(
        manifest.model.entity_mapping[entity][0]
        for entity in sorted(manifest.model.entity_mapping)
        if manifest.model.entity_mapping[entity]
    )

    lowest_bound, highest_bound = _threshold_bounds(manifest)
    ramp_count = _clamp_int(math.ceil(lowest_bound) + 2, _MIN_COUNT, _MAX_COUNT)
    escalate_count = _clamp_int(
        max(math.ceil(highest_bound) + 2, ramp_count + max(3, ramp_count // 2)), _MIN_COUNT, _MAX_COUNT
    )

    ramp_area, escalate_area = _area_targets(manifest)
    floor = _intake_floor(manifest)
    ramp_confidence, escalate_confidence = _confidence_targets(manifest, floor)

    for stage in manifest.pipeline:
        if isinstance(stage, IncidentQuantiseConfig) and stage.strategy == "count_based":
            threshold = stage.count_threshold or 1
            lowest = min(rung.percentage for rung in stage.levels)
            ramp_count = _clamp_int(max(ramp_count, math.ceil(threshold * (lowest + 5) / 100)), _MIN_COUNT, _MAX_COUNT)
            escalate_count = _clamp_int(max(escalate_count, threshold), ramp_count, _MAX_COUNT)

    zone_names, line_names = _geometry_names(manifest)
    return FramePlan(
        app_id=manifest.app.id,
        labels=labels,
        quiet_frames=3,
        ramp_frames=dwell_frames,
        escalate_frames=dwell_frames,
        clear_frames=clear_frames,
        ramp_count=ramp_count,
        escalate_count=escalate_count,
        ramp_area=ramp_area,
        escalate_area=escalate_area,
        ramp_confidence=ramp_confidence,
        escalate_confidence=escalate_confidence,
        zone_names=zone_names,
        line_names=line_names,
    )


def synthesise_frames(manifest: AppManifest) -> tuple[SyntheticFrame, ...]:
    """The synthetic frame sequence for one manifest.  No RNG, no clock -- see **PY-9**."""
    return frame_plan(manifest).frames()


def _threshold_bounds(manifest: AppManifest) -> tuple[float, float]:
    """``(lowest, highest)`` numeric bound any ``severity_from`` threshold declares.

    Both, not just the largest, because the two phases mean different things:
    ``{current_occupancy: {">": 15}}`` needs 16+ detections to open at all, while a *graded*
    ``levels: [{value: 4, level: low}, {value: 9, level: high}]`` needs the ramp phase to land
    on the **bottom** rung and the escalate phase to clear the **top** one -- otherwise both
    phases report ``high`` and the generated escalation assertion fails a correct manifest.

    A percentage- or seconds-shaped bound is not reachable by adding detections at all;
    :func:`_undrivable_rules` says so rather than the lifecycle check failing an app it cannot
    exercise.
    """
    bounds: list[float] = []
    if manifest.incidents is None:
        return (0.0, 0.0)
    for incident in manifest.incidents.types:
        source = incident.severity_from
        if not isinstance(source, Mapping):
            continue
        for threshold in source.values():
            bounds.extend(float(value) for value in threshold.operators.values())
            bounds.extend(float(level.value) for level in threshold.levels)
    if not bounds:
        return (0.0, 0.0)
    return (min(bounds), max(bounds))


def _area_targets(manifest: AppManifest) -> tuple[float, float]:
    """``(ramp, escalate)`` total box area, as a fraction of the frame.

    For an ``area_ratio`` quantiser the level ladder is measured as
    ``total_area / threshold_area * 100`` (capped at 100), so the ramp target sits just above
    the lowest rung and the escalate target saturates the ladder -- which is what makes the
    generated *escalation* assertion meaningful rather than accidental.
    """
    ramp, escalate = 0.02, 0.06
    for stage in manifest.pipeline:
        if not isinstance(stage, IncidentQuantiseConfig) or stage.strategy != "area_ratio":
            continue
        threshold = float(stage.threshold_area or 0.0)
        if threshold <= 0:  # pragma: no cover - the config model enforces gt=0
            continue
        lowest = min(rung.percentage for rung in stage.levels)
        ramp = max(ramp, threshold * (lowest + 5) / 100.0)
        escalate = max(escalate, threshold)
    return (min(ramp, 0.45), min(max(escalate, ramp * 2), 0.9))


def _confidence_targets(manifest: AppManifest, floor: float) -> tuple[float, float]:
    """``(ramp, escalate)`` detection confidence.

    Both are above the intake floor by construction -- a generated frame that the intake
    filter silently drops would make every downstream assertion fail for the wrong reason.
    For a ``max_confidence`` quantiser (``severity = max(confidence) * 100``) the ramp value
    lands on the lowest rung and the escalate value on the highest.
    """
    ramp = min(0.99, max(floor + 0.02, 0.6))
    for stage in manifest.pipeline:
        if not isinstance(stage, IncidentQuantiseConfig) or stage.strategy != "max_confidence":
            continue
        lowest = min(rung.percentage for rung in stage.levels)
        ramp = min(ramp, max(floor, (lowest + 3) / 100.0))
    return (min(0.99, max(ramp, floor)), 0.99)


def _intake_floor(manifest: AppManifest) -> float:
    """``model.confidence_threshold``, lowered by any ``detect`` override.

    Mirrors :meth:`Session._resolve_intake_floor`.  Duplicated deliberately: the generator
    must know what the session will discard *before* it builds a frame, and importing the
    private method would couple the two in the wrong direction.

    The duplication has to be *maintained*, though, and it had already drifted: this ignored
    ``min_confidence_per_class``, so an app whose per-class floor sits below its stage floor got
    synthetic detections above the generator's idea of the floor and below the session's, and the
    checks that depend on those detections quietly had less to work with.  Both halves now walk
    the same two fields.
    """
    floor = float(manifest.model.confidence_threshold)
    for stage in manifest.pipeline:
        if not isinstance(stage, DetectConfig):
            continue
        if stage.min_confidence is not None:
            floor = min(floor, float(stage.min_confidence))
        for per_class in stage.min_confidence_per_class.values():
            floor = min(floor, float(per_class))
    return floor


def _geometry_names(manifest: AppManifest) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """The zone and line names the synthetic camera has to have drawn on it.

    Three sources, in order:

    1. every zone a ``zone_occupancy`` stage lists by name -- an undrawn one is a
       :class:`~matrice_analytics.engine.runtime.session.SessionError` at setup;
    2. every plausible zone name in a ``custom`` stage's ``config:`` block.  A custom stage's
       config is the author's own Pydantic model, so the generator cannot know *which* field
       names a zone -- it takes every short, name-shaped string value.  Drawing a zone the app
       never asked for is harmless; failing to draw one it did is a false failure;
    3. generated ``zone_1..n`` / ``line_1..n`` filler to satisfy whatever
       :meth:`AppManifest.geometry_requirements` still asks for -- including
       ``line_crossing.method: abline``, which needs **exactly** two lines and reports zero
       forever with any other number.
    """
    zones: list[str] = []
    wants_zones = manifest.zones is not None

    for stage in manifest.pipeline:
        if isinstance(stage, ZoneOccupancyConfig):
            wants_zones = True
            if stage.zones != "all":
                for name in stage.zones:
                    if name not in zones:
                        zones.append(name)
        elif isinstance(stage, CustomConfig):
            # ``config`` is the raw block on the manifest model; the loader validates it against
            # the author's own ``Config`` model separately, so accept either shape.
            block = stage.config if isinstance(stage.config, Mapping) else stage.config.model_dump()
            for value in block.values():
                if _looks_like_a_zone_name(value) and value not in zones:
                    zones.append(str(value))

    lines: list[str] = []
    for requirement in manifest.geometry_requirements():
        needed = requirement.exact if requirement.exact is not None else (requirement.minimum or 0)
        target = zones if requirement.kind == "zones" else lines
        prefix = "zone" if requirement.kind == "zones" else "line"
        if requirement.kind == "zones":
            wants_zones = True
        while len(target) < needed:
            target.append(f"{prefix}_{len(target) + 1}")

    if wants_zones and not zones:
        # An app that opts into zoning with no named zone still needs geometry to partition
        # over; two stripes exercise the partition rather than collapsing to one bucket.
        zones = ["zone_1", "zone_2"]
    return (tuple(zones), tuple(lines))


def _looks_like_a_zone_name(value: Any) -> bool:
    """Whether a ``custom.config`` value could plausibly be a drawn zone name."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or len(text) > 40 or text != value:
        return False
    if any(char in text for char in "/\\:.,{}[]()"):
        return False
    return text[0].isalpha()


def synthetic_stream_info(manifest: AppManifest) -> StreamInfo:
    """The synthetic camera (surface **S4**) an app's generated suite runs against.

    Fully determined by the manifest, so two processes build the identical stream -- the
    precondition for the byte-identical assertion in :func:`check_determinism`.
    ``camera_name`` deliberately differs from ``camera_id``: an equal pair is blanked on the
    wire (**FROZEN-8**) and the generated conformance assertion should see the normal path.
    """
    zone_names, line_names = _geometry_names(manifest)
    zone_config: ZoneConfig | None = None
    if zone_names or line_names:
        zone_config = ZoneConfig(
            zones={name: _stripe(index, len(zone_names)) for index, name in enumerate(zone_names)},
            lines={
                name: [[_round(0.3 + 0.2 * index), 0.1], [_round(0.3 + 0.2 * index), 0.9]]
                for index, name in enumerate(line_names)
            },
        )
    return StreamInfo(
        camera_id=SYNTHETIC_CAMERA_ID,
        camera_name="Generated Camera",
        camera_group="generated",
        app_id=f"app-{manifest.app.id}",
        app_deployment_id="generated-deployment",
        application_name=manifest.app.name,
        application_key_name=manifest.app.id,
        application_version=manifest.app.version,
        original_fps=SYNTHETIC_FPS,
        resolution=SYNTHETIC_RESOLUTION,
        zone_config=zone_config,
    )


def _stripe(index: int, count: int) -> list[list[float]]:
    """Zone ``index`` of ``count`` as a full-height vertical stripe polygon.

    Stripes rather than blobs so that the synthesised detections, which are laid out across
    the frame's width, land in *different* zones -- a partition that puts everything in one
    bucket would not exercise the per-zone path at all.
    """
    width = 1.0 / max(1, count)
    left = _round(index * width + 0.004)
    right = _round((index + 1) * width - 0.004)
    return [[left, 0.02], [right, 0.02], [right, 0.98], [left, 0.98]]


def _detections(
    labels: Sequence[str], count: int, total_area: float, confidence: float, frame_index: int
) -> tuple[dict[str, Any], ...]:
    """``count`` co-located boxes per model label, summing to ``total_area`` of the frame.

    Co-located on purpose: ``ratio_compliance`` associates an attribute with a subject by
    overlap (``association_score``), so a ``hardhat`` box drawn somewhere else would make
    every worker read as non-compliant for a reason that has nothing to do with the manifest.

    The small per-frame drift is what lets ``track`` keep one id per object across frames --
    without it ``unique_count`` counts the same object once per frame, the classic "counts far
    too high" report.  Coordinates are rounded to six places so the payload bytes are stable.
    """
    if count <= 0 or not labels:
        return ()

    total = count * len(labels)
    columns = max(1, math.ceil(math.sqrt(count)))
    rows = math.ceil(count / columns)
    margin = 0.02
    cell = min((1.0 - 2 * margin) / columns, (1.0 - 2 * margin) / max(1, rows))
    side = min(cell * 0.85, math.sqrt(max(total_area, 1e-6) / total))
    side = max(side, 0.01)
    drift = 0.0008 * frame_index

    produced: list[dict[str, Any]] = []
    for slot in range(count):
        column, row = slot % columns, slot // columns
        span = max(1e-6, 1.0 - 2 * margin - side)
        x = margin + (span * column / max(1, columns - 1) if columns > 1 else 0.0) + drift
        y = margin + (row * cell if rows > 1 else 0.0)
        x = min(x, 1.0 - side - 1e-6)
        y = min(y, 1.0 - side - 1e-6)
        box = {
            "xmin": _round(x),
            "ymin": _round(y),
            "xmax": _round(x + side),
            "ymax": _round(y + side),
        }
        for label in labels:
            produced.append({"category": label, "confidence": _round(confidence), "bounding_box": dict(box)})
    return tuple(produced)


def _round(value: float) -> float:
    return round(float(value), 6)


def _clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


# ---------------------------------------------------------------------------
# The synthetic run
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SyntheticRun:
    """Everything one synthetic run produced, on all three surfaces."""

    app_id: str
    plan: FramePlan
    frames: tuple[SyntheticFrame, ...]
    aggregations: tuple[dict[str, Any], ...]
    """``results-agg`` payloads (**S1**), in publication order."""

    incidents: tuple[dict[str, Any], ...]
    """``incident_res`` payloads (**S2**), in publication order -- transitions only."""

    frame_results: tuple[dict[str, Any], ...]
    """Per-frame return payloads (**S3**); empty when ``emission.frame_summary`` is false."""

    emission_zones: tuple[str, ...] = ()
    error: str = ""
    """Non-empty when the run raised.  A run that cannot start is a failed check, not a crash."""

    def digest(self) -> str:
        """sha256 over the payload JSON, **without** ``sort_keys``.

        Key order is part of "byte-identical": a dict built by iterating a set would change
        order between processes under a different ``PYTHONHASHSEED`` and a key-sorted digest
        would hide exactly the class of defect **PY-9** is.
        """
        return _digest(self.section_digests()["payloads"])

    def section_digests(self) -> dict[str, str]:
        """Per-surface digests, so a determinism failure can name *which* surface diverged."""
        payloads = _dumps(
            {
                "aggregations": list(self.aggregations),
                "incidents": list(self.incidents),
                "frames": list(self.frame_results),
            }
        )
        return {
            "payloads": payloads,
            "results_agg": _digest(_dumps(list(self.aggregations))),
            "incident_res": _digest(_dumps(list(self.incidents))),
            "frame_result": _digest(_dumps(list(self.frame_results))),
        }

    def incident_entries(self) -> tuple[dict[str, Any], ...]:
        """Every ``incidents[]`` entry across every message, in emission order."""
        entries: list[dict[str, Any]] = []
        for payload in self.incidents:
            for entry in payload.get("incidents") or ():
                if isinstance(entry, Mapping):
                    entries.append(dict(entry))
        return tuple(entries)


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def run_synthetic(
    app: str | os.PathLike[str] | AppManifest | LoadedApp,
    *,
    frames: Sequence[SyntheticFrame] | None = None,
) -> SyntheticRun:
    """Push synthesised detections through a **real** session and keep every payload.

    No publisher is attached: a session with ``publisher=None`` builds and validates the
    payloads and hands them back on :class:`~...runtime.session.FrameOutcome`, which is
    exactly what a test wants and keeps the generated suite free of any transport.

    Args:
        app: An app folder, a bare app id, a :class:`~...manifest.loader.LoadedApp`, or an
            already-validated :class:`~...manifest.models.AppManifest`.
        frames: Override the synthetic sequence -- for a fixture-driven run, or to shorten a
            long ``close_after_empty_frames`` tail in an engine-side test.

    Returns:
        The :class:`SyntheticRun`.  A failure during setup or on a frame is recorded in
        :attr:`SyntheticRun.error`, never raised: every generated check needs to be able to
        *report* a broken app rather than fail to run.
    """
    return _run_resolved(_resolve_app(app), frames=frames)


def _run_resolved(
    resolved: _AppUnderTest, *, frames: Sequence[SyntheticFrame] | None = None
) -> SyntheticRun:
    """:func:`run_synthetic` over an already-normalised app.

    Separate so :func:`suite_checks` can share one loaded bundle -- and, more importantly, one
    set of imported ``custom`` implementations -- across checks 2, 3 and 4.  Re-resolving from
    the manifest alone would drop the custom code, and a ``custom`` stage with no implementation
    is a :class:`~...runtime.session.SessionError` at setup.
    """
    if resolved.manifest is None:
        empty_plan = FramePlan(
            app_id=resolved.app_id,
            labels=(),
            quiet_frames=0,
            ramp_frames=0,
            escalate_frames=0,
            clear_frames=0,
            ramp_count=0,
            escalate_count=0,
            ramp_area=0.0,
            escalate_area=0.0,
            ramp_confidence=0.0,
            escalate_confidence=0.0,
            zone_names=(),
            line_names=(),
        )
        return SyntheticRun(
            app_id=resolved.app_id,
            plan=empty_plan,
            frames=(),
            aggregations=(),
            incidents=(),
            frame_results=(),
            error=resolved.load_error or "the manifest did not load",
        )

    manifest = resolved.manifest
    plan = frame_plan(manifest)
    sequence = tuple(frames) if frames is not None else plan.frames()

    aggregations: list[dict[str, Any]] = []
    incidents: list[dict[str, Any]] = []
    frame_results: list[dict[str, Any]] = []
    error = ""
    emission_zones: tuple[str, ...] = ()

    try:
        session = Session(
            manifest,
            synthetic_stream_info(manifest),
            custom=resolved.custom,
            started_at=SYNTHETIC_EPOCH,
        )
        emission_zones = session.emission_zones
    except Exception as exc:  # noqa: BLE001 - a broken app must be reportable, not fatal
        return SyntheticRun(
            app_id=manifest.app.id,
            plan=plan,
            frames=sequence,
            aggregations=(),
            incidents=(),
            frame_results=(),
            error=f"session setup raised {type(exc).__name__}: {exc}",
        )

    for frame in sequence:
        try:
            outcome: FrameOutcome = session.process_frame(list(frame.detections), frame_ts=frame.ts)
        except Exception as exc:  # noqa: BLE001 - same reason: report it, do not crash
            error = f"frame {frame.index} ({frame.phase}) raised {type(exc).__name__}: {exc}"
            break
        if outcome.aggregation is not None:
            aggregations.append(to_payload(outcome.aggregation))
        for message in outcome.incidents:
            incidents.append(to_payload(message))
        payload = outcome.payload()
        if payload:
            frame_results.append(payload)

    if not error:
        try:
            final = session.flush()
        except Exception as exc:  # noqa: BLE001
            error = f"flush() raised {type(exc).__name__}: {exc}"
        else:
            if final is not None:
                aggregations.append(to_payload(final))

    return SyntheticRun(
        app_id=manifest.app.id,
        plan=plan,
        frames=sequence,
        aggregations=tuple(aggregations),
        incidents=tuple(incidents),
        frame_results=tuple(frame_results),
        emission_zones=emission_zones,
        error=error,
    )


# ---------------------------------------------------------------------------
# Check 1 -- schema validity
# ---------------------------------------------------------------------------


def check_schema_validity(app: str | os.PathLike[str] | AppManifest | LoadedApp) -> CheckResult:
    """Check 1: the manifest loads and everything it names exists.

    Four assertions, each with a defect behind it:

    * **the manifest loads** -- including its custom code, which only the full loader imports;
    * **every ``metrics[].source`` resolves** against a declared stage.  A typo produces a
      metric that reads zero forever and nothing anywhere says so (``09`` §3);
    * **every enum is legal in the contract's own vocabulary**, not just in the manifest
      schema's.  The two are separate modules and an ``agg_type`` the backend does not know is
      silently summed (**PY-1**), an ``IDENTITY`` category lands in ClickHouse as an
      unfilterable literal (**V7**), and ``significant`` must never reach the wire
      (**FROZEN-7**);
    * **every primitive is registered and implemented**.  ``IMPLEMENTED = False`` is a valid
      manifest the runtime refuses at startup (``08`` §2), so a generated suite has to fail
      here rather than at the first frame.
    """
    return _check_schema(_resolve_app(app))


def _check_schema(resolved: _AppUnderTest) -> CheckResult:
    """:func:`check_schema_validity` over an already-normalised app."""
    problems: list[str] = []
    notes: list[str] = []

    if resolved.manifest is None:
        return CheckResult(
            name=CHECK_SCHEMA,
            status="failed",
            problems=(resolved.load_error or "the manifest did not load",),
        )

    manifest = resolved.manifest
    legal_agg = {member.value for member in AggType}
    legal_category = {member.value for member in Category}
    legal_severity = {member.value for member in Severity}

    for index, metric in enumerate(manifest.metrics):
        where = f"metrics[{index}] ({metric.key})"
        try:
            resolve_source(manifest, metric.source, where=where)
        except ValueError as exc:
            problems.append(str(exc))
        if metric.agg_type not in legal_agg:
            problems.append(f"{where}.agg_type {metric.agg_type!r} is not in the contract vocabulary {sorted(legal_agg)}")
        if metric.category not in legal_category:
            problems.append(
                f"{where}.category {metric.category!r} is not in the contract vocabulary {sorted(legal_category)}"
            )
        if metric.zone not in {"global", "per_zone", "collapsed"}:
            problems.append(
                f"{where}.zone {metric.zone!r} is not one of 'global', 'per_zone', 'collapsed'"
            )

    if manifest.incidents is not None:
        for index, incident in enumerate(manifest.incidents.types):
            where = f"incidents.types[{index}] ({incident.key})"
            if incident.category not in legal_category:
                problems.append(
                    f"{where}.category {incident.category!r} is not in the contract vocabulary "
                    f"{sorted(legal_category)}"
                )
            for severity in _declared_severities(manifest, incident.severity_from):
                if severity not in legal_severity:
                    problems.append(
                        f"{where} can produce severity {severity!r}, which is not on the wire "
                        f"vocabulary {sorted(legal_severity)} (FROZEN-7)"
                    )

    unimplemented = manifest.unimplemented_primitives()
    if unimplemented:
        problems.append(
            f"primitive(s) {', '.join(unimplemented)} are declared but not implemented by this "
            "engine build; the manifest is valid and the session will refuse at startup (08 §2)"
        )
    for stage in manifest.pipeline:
        if stage.PRIMITIVE in unimplemented:
            continue  # already reported; an unimplemented primitive is unregistered by construction
        if isinstance(stage, CustomConfig):
            if stage.stage_name not in resolved.custom:
                notes.append(
                    f"stage {stage.stage_name!r} is custom code ({stage.impl!r}); it was not "
                    "supplied, so the generated run cannot exercise it. Load the app with "
                    "load_app_bundle(<folder>) rather than passing a bare manifest."
                )
            continue
        if stage.PRIMITIVE not in REGISTRY:
            problems.append(
                f"pipeline stage {stage.stage_name!r} names primitive {stage.PRIMITIVE!r}, which is "
                f"not registered. Registered: {', '.join(REGISTRY.names()) or '(none)'}"
            )

    if manifest.tests.fixtures:
        notes.append(
            f"tests.fixtures declares {len(manifest.tests.fixtures)} file(s); the generator does not "
            "read them yet, so the run below is manifest-derived only"
        )
    if manifest.tests.golden:
        notes.append(
            f"tests.golden declares {manifest.tests.golden!r}; the generator does not diff against a "
            "golden file yet"
        )

    return CheckResult(
        name=CHECK_SCHEMA,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=tuple(notes),
    )


def _declared_severities(manifest: AppManifest, severity_from: str | Mapping[str, Any]) -> tuple[str, ...]:
    """Every severity string one ``severity_from`` can produce.

    Three shapes: a fixed level, a quantiser stage (its ladder's rungs), or metric thresholds
    (their graded ``levels``, plus the ungraded default the runtime uses).
    """
    if isinstance(severity_from, Mapping):
        found: list[str] = []
        for threshold in severity_from.values():
            levels = getattr(threshold, "levels", ())
            found.extend(level.level for level in levels)
            if not levels:
                found.append("medium")  # DEFAULT_THRESHOLD_SEVERITY -- a bare threshold
        return tuple(found)

    stage = manifest.stages.get(severity_from) or next(
        (candidate for candidate in manifest.pipeline if severity_from == candidate.PRIMITIVE), None
    )
    if isinstance(stage, IncidentQuantiseConfig):
        return tuple(rung.level for rung in stage.levels)
    if stage is not None:
        return ()
    return (severity_from,)  # a fixed level


# ---------------------------------------------------------------------------
# Check 2 -- contract conformance
# ---------------------------------------------------------------------------


def check_contract_conformance(run: SyntheticRun) -> CheckResult:
    """Check 2: every emitted payload passes all six checks from contract §7.

    The six checks are *reused*, never reimplemented -- :func:`~...conformance.conformance_errors`
    is the single definition of "conforms" in the tree, and the emit path already asserts with
    it, so a payload that reaches here has been validated twice by the same code.
    """
    problems: list[str] = []
    if run.error:
        problems.append(run.error)
    if len(CHECKS) != 6:  # pragma: no cover - a guard against the check set changing silently
        problems.append(f"contract §7 declares six checks; conformance.CHECKS has {len(CHECKS)}")

    if not run.aggregations and not run.error:
        problems.append(
            "the run produced no results-agg message at all. Every app publishes on the window "
            "boundary; an app that publishes nothing is invisible on every dashboard"
        )

    for surface, payloads in (
        (Surface.results_agg, run.aggregations),
        (Surface.incident_res, run.incidents),
        (Surface.frame_result, run.frame_results),
    ):
        for index, payload in enumerate(payloads):
            for error in conformance_errors(payload, surface):
                problems.append(f"{surface.value}[{index}]: {error}")

    return CheckResult(
        name=CHECK_CONFORMANCE,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=(
            f"validated {len(run.aggregations)} results-agg, {len(run.incidents)} incident_res and "
            f"{len(run.frame_results)} frame payload(s) against all six checks",
        ),
    )


# ---------------------------------------------------------------------------
# Check 3 -- metric presence
# ---------------------------------------------------------------------------


def _silent_buckets_for(
    manifest: AppManifest, metric: Any, *, zoned: bool = False
) -> frozenset[str]:
    """Buckets this metric cannot publish in because its source stage publishes nothing there.

    Without this, the per-zone presence check below reads a *deliberate* silence as a missing
    series -- and the only honest alternative would be for the stage to publish the ``0`` that
    silence replaced, which is the defect (``dwell`` in ``unassigned``: see
    ``DwellConfig.silent_buckets``).

    A ``derived[]`` entry is silent wherever **any** of its operands is, because one missing
    operand skips the whole expression. A ``global.``-prefixed operand is excluded: it reads
    the whole-frame bucket, so a stage's silence in some *other* bucket cannot affect it.

    Args:
        zoned: Whether this run partitions detections. ``dwell`` with ``state: in_zone`` is
            silent in ``global`` only then -- unzoned, that combination is a manifest error the
            primitive raises on, and treating it as silence would hide it.
    """
    sources: list[str] = []
    expression = getattr(metric, "expression", None)
    if expression is not None:  # derived[]
        sources = list(expression.operands)
    elif getattr(metric, "source", None):
        sources = [metric.source]

    silent: set[str] = set()
    for source in sources:
        try:
            resolved = resolve_source(manifest, source, allow_global_prefix=True)
        except ValueError:  # already reported by schema_validity; not this check's business
            continue
        if resolved.from_global:
            continue
        stage = next((s for s in manifest.pipeline if s.stage_name == resolved.stage), None)
        if stage is None:
            stage = next((s for s in manifest.pipeline if s.PRIMITIVE == resolved.stage), None)
        if stage is not None:
            silent |= stage.silent_buckets(zoned=zoned)
    return frozenset(silent)


def check_metric_presence(manifest: AppManifest, run: SyntheticRun) -> CheckResult:
    """Check 3: every declared metric really reaches ``results-agg.metrics[]``.

    This is the check that would have caught the live defect where a dashboard declares metric
    keys the engine never emits.  ``metrics[].key`` is a *shared namespace* joined to
    ``metrics.json``'s ``key`` by nothing at all (``06`` §13), so a metric that is
    declared and never published is an empty chart with no error anywhere.

    Asserted per metric:

    * the key appears in at least one window's ``metrics[]`` -- the engine deliberately
      **omits** a metric whose source did not resolve this window rather than publishing a
      fabricated ``0.0`` (``09`` §3), so "in at least one window" is the honest bar;
    * ``agg_type`` and ``category`` are the manifest's, character for character;
    * the zone shape matches: ``zone: global`` publishes one entry keyed ``global``;
      ``zone: per_zone`` publishes one entry per emission zone (**PY-5**).

    The inverse direction is checked too: a published key that no metric declared is a
    dashboard nobody built and a ClickHouse series nobody can attribute.
    """
    problems: list[str] = []
    notes: list[str] = []
    if run.error:
        problems.append(run.error)

    seen: dict[str, list[Mapping[str, Any]]] = {}
    for payload in run.aggregations:
        for entry in payload.get("metrics") or ():
            if isinstance(entry, Mapping):
                seen.setdefault(str(entry.get("key")), []).append(entry)

    # Both lists, because both reach ``results-agg`` and the wire cannot tell them apart. Checking
    # only ``metrics`` left every ``derived[]`` key unasserted in the one direction that matters --
    # "is it actually published" -- for any app that ships no metrics.json.
    declared = [(f"metrics[{i}]", spec) for i, spec in enumerate(manifest.metrics)]
    declared += [(f"derived[{i}]", spec) for i, spec in enumerate(manifest.derived)]

    for label, metric in declared:
        where = f"{label} ({metric.key})"
        entries = seen.get(metric.key)
        if not entries:
            problems.append(
                f"{where} is declared but never appears in results-agg.metrics[] across "
                f"{len(run.aggregations)} window(s). Published keys: "
                f"{', '.join(sorted(seen)) or '(none)'}. A declared-but-unpublished key is an empty "
                f"chart with no error anywhere (06 §13)"
            )
            continue
        wrong_agg = sorted({str(entry.get("agg_type")) for entry in entries} - {metric.agg_type})
        if wrong_agg:
            problems.append(f"{where} was published with agg_type {wrong_agg}, not {metric.agg_type!r}")
        wrong_category = sorted({str(entry.get("category")) for entry in entries} - {metric.category})
        if wrong_category:
            problems.append(f"{where} was published with category {wrong_category}, not {metric.category!r}")

        zones = {str(entry.get("zone")) for entry in entries}
        if metric.zone in {"global", "collapsed"}:
            # `collapsed` is one row too -- its zones are already reduced by `across_zones`, and
            # it is labelled `global` because that is what "this camera, all of it" means on the
            # wire. The difference from `global` is where the number came from, not its shape.
            if zones != {GLOBAL_ZONE}:
                problems.append(
                    f"{where} declares zone: {metric.zone} but was published under "
                    f"{sorted(zones)}; that is one series keyed {GLOBAL_ZONE!r}"
                )
            if metric.zone == "collapsed" and len(entries) != 1:
                problems.append(
                    f"{where} declares zone: collapsed but published {len(entries)} entries for "
                    f"one window; the whole point of collapsed is exactly one row per period"
                )
        else:
            # `global` is not an emission zone once the app partitions, so its absence is what
            # "zoned" means here -- the same test `Session._resolve_emission_zones` encodes.
            zoned = GLOBAL_ZONE not in run.emission_zones
            expected = set(run.emission_zones) - _silent_buckets_for(
                manifest, metric, zoned=zoned
            )
            missing = sorted(expected - zones)
            if missing:
                problems.append(
                    f"{where} declares zone: per_zone but no entry was published for zone(s) "
                    f"{missing} (emission zones: {sorted(expected)})"
                )
            if GLOBAL_ZONE in zones and GLOBAL_ZONE not in expected:
                problems.append(
                    f"{where} declares zone: per_zone but was published under {GLOBAL_ZONE!r}; a "
                    f"per-zone series and a whole-frame series double-count in any dashboard that "
                    f"sums zones"
                )

    # `published_keys`, not `metrics` -- a derived[] key is published on the same wire and shares
    # the same namespace, so subtracting only the sourced metrics reported every app's own derived
    # metric as undeclared. No shipped example uses derived:, which is why it went unnoticed.
    undeclared = sorted(set(seen) - set(manifest.published_keys))
    if undeclared:
        problems.append(
            f"the engine published metric key(s) {undeclared} that this manifest never declared; "
            f"nothing downstream can attribute them"
        )
    if seen:
        notes.append(f"published metric keys: {', '.join(sorted(seen))}")

    return CheckResult(
        name=CHECK_METRICS,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=tuple(notes),
    )


# ---------------------------------------------------------------------------
# Check 4 -- the three uploaded files agree with the manifest
# ---------------------------------------------------------------------------


def _declared_metrics(manifest: AppManifest) -> dict[str, Any]:
    """``{key: spec}`` over ``metrics[]`` **and** ``derived[]`` -- both reach the dashboard."""
    declared: dict[str, Any] = {spec.key: spec for spec in manifest.metrics}
    declared.update({spec.key: spec for spec in manifest.derived})
    return declared


def check_app_config_files(manifest: AppManifest, bundle: AppConfigBundle) -> CheckResult:
    """Check 4: ``metrics.json``, ``widgets.json`` and ``post_processing_config.json`` agree.

    ``be-application`` validates only that a widget's ``dataKey`` resolves *within the uploaded
    config itself*.  Nothing anywhere compares those files to ``app.yaml``, so a renamed metric key
    is an empty chart with no error at publish time or at runtime -- the **PY-1b** defect, live
    across the published catalogue.  This check is that comparison.

    Asserted:

    * ``metrics.json`` declares exactly the keys the manifest publishes (``metrics[]`` +
      ``derived[]``), in both directions;
    * per entry, ``aggType`` / ``category`` / ``unit`` match the manifest character for character;
    * every widget resolves -- a ``dataSource`` that is missing, unknown, or a CSV of the wrong
      length drops the whole widget before it renders (**PY-1c**);
    * ``dataSource: metric`` tokens name a ``metrics.json`` key; ``dataSource: tracking_class``
      tokens name a left-hand ``entity_mapping`` entry.  Two keyspaces, no fallback between them;
    * ``post_processing_config.json`` ``usecase`` is ``app.id`` -- without it the deployment gets
      no analytics node and the worker never starts.

    ``chartType`` outside ``bar``/``line`` is a **note**, not a failure: the live dashboard renders
    it as a line rather than rejecting it (**PY-1d**).
    """
    problems: list[str] = []
    notes: list[str] = []

    problems.extend(str(problem) for problem in bundle.errors)
    notes.extend(str(problem) for problem in bundle.warnings)
    if bundle.missing:
        problems.append(
            f"missing beside app.yaml: {', '.join(bundle.missing)}. A version needs all three; "
            f"without post_processing_config.json the deployment gets no analytics node at all"
        )

    declared = _declared_metrics(manifest)

    if bundle.metrics is not None:
        uploaded = {entry.key: entry for entry in bundle.metrics}
        for key in sorted(set(declared) - set(uploaded)):
            problems.append(
                f"app.yaml publishes {key!r} but metrics.json does not declare it; the dashboard "
                f"only ever asks for keys its own config names, so the series is stored in "
                f"ClickHouse and never read"
            )
        for key in sorted(set(uploaded) - set(declared)):
            problems.append(
                f"metrics.json declares {key!r}, which app.yaml never publishes. Published keys: "
                f"{', '.join(sorted(declared)) or '(none)'}"
            )
        for key in sorted(set(uploaded) & set(declared)):
            problems.extend(_metric_entry_problems(key, uploaded[key], declared[key]))
        problems.extend(_uploaded_vocabulary_problems(bundle))

    if bundle.widgets is not None:
        metric_keys = bundle.metric_keys if bundle.metrics is not None else set(declared)
        entities = manifest.model.entities
        for index, widget in enumerate(bundle.widgets):
            where = f"widgets.json[{index}] ({widget.key})"
            bindings, reason = widget.resolve_bindings()
            if reason is not None:
                problems.append(f"{where} does not render: {reason}")
                continue
            if widget.category and widget.category not in ANALYTICS_CATEGORIES:
                problems.append(
                    f"{where} category {widget.category!r} is not one of "
                    f"{', '.join(sorted(ANALYTICS_CATEGORIES))}"
                )
            if widget.chart_type and widget.chart_type not in CHART_TYPES_RENDERED:
                notes.append(
                    f"{where} chartType {widget.chart_type!r} renders as a line on the live "
                    f"dashboard; only {', '.join(sorted(CHART_TYPES_RENDERED))} are honoured (PY-1d)"
                )
            for binding in bindings:
                problems.extend(_binding_problems(where, binding, metric_keys, entities))

    if bundle.post_processing is not None:
        config = bundle.post_processing
        if not config.usecase:
            problems.append(
                f"post_processing_config.json has no 'usecase'; it must equal app.id "
                f"({manifest.app.id!r})"
            )
        elif config.usecase != manifest.app.id:
            problems.append(
                f"post_processing_config.json usecase is {config.usecase!r} but app.id is "
                f"{manifest.app.id!r}; they are joined by exact string match"
            )
        if config.category and config.category != manifest.app.category:
            problems.append(
                f"post_processing_config.json category is {config.category!r} but app.category is "
                f"{manifest.app.category!r}"
            )

    return CheckResult(
        name=CHECK_APP_CONFIG,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=tuple(notes),
    )


def _metric_entry_problems(key: str, entry: Any, spec: Any) -> list[str]:
    """Field-by-field agreement between one ``metrics.json`` entry and its manifest spec."""
    where = f"metrics.json ({key})"
    problems: list[str] = []
    if entry.agg_type is not None and entry.agg_type != spec.agg_type:
        problems.append(
            f"{where} aggType is {entry.agg_type!r} but app.yaml declares agg_type "
            f"{spec.agg_type!r}; the backend selects the rollup value by the agg type the engine "
            f"publishes, so the dashboard's label would describe a different number"
        )
    if entry.category is not None and entry.category != spec.category:
        problems.append(f"{where} category is {entry.category!r} but app.yaml declares {spec.category!r}")
    if entry.unit != spec.unit and not (entry.unit is None and spec.unit is None):
        problems.append(
            f"{where} unit is {entry.unit!r} but app.yaml declares {spec.unit!r}; alert thresholds "
            f"are compared by unit dimension, so a mismatch silently rescales them"
        )
    return problems


def _uploaded_vocabulary_problems(bundle: AppConfigBundle) -> list[str]:
    """Enum-level checks on ``metrics.json`` that do not depend on the manifest."""
    problems: list[str] = []
    for index, entry in enumerate(bundle.metrics or ()):
        where = f"metrics.json[{index}] ({entry.key})"
        if entry.category is not None and entry.category not in ANALYTICS_CATEGORIES:
            problems.append(
                f"{where} category {entry.category!r} is not one of "
                f"{', '.join(sorted(ANALYTICS_CATEGORIES))} -- lowercase and 'zone' are both live "
                f"mistakes, and a metric outside the enum is unfilterable"
            )
        if entry.unit is not None and entry.unit not in UNIT_DIMENSIONS:
            problems.append(
                f"{where} unit {entry.unit!r} is not in the units registry, so nobody can set an "
                f"alert threshold against it"
            )
    return problems


def _binding_problems(
    where: str, binding: Any, metric_keys: Any, entities: frozenset[str]
) -> list[str]:
    """Does one resolved ``dataKey`` token name something that exists?"""
    if binding.token in RESERVED_WIDGET_TOKENS:
        return [
            f"{where} binds to the reserved token {binding.token!r}; the dashboard skips that "
            f"literal when it builds its query, so the widget fetches nothing. It is fine as a "
            f"metrics.json entry"
        ]
    if binding.data_source == "metric":
        if binding.token not in metric_keys:
            return [
                f"{where} dataKey {binding.token!r} (dataSource: metric) is not a metrics.json key. "
                f"Declared: {', '.join(sorted(metric_keys)) or '(none)'}"
            ]
        return []
    if binding.token not in entities:
        return [
            f"{where} dataKey {binding.token!r} (dataSource: tracking_class) is not an "
            f"entity_mapping name. Entities: {', '.join(sorted(entities)) or '(none)'}. A "
            f"tracking_class token is a class name, not a metric key -- the two are separate "
            f"keyspaces with no fallback between them"
        ]
    return []


# ---------------------------------------------------------------------------
# Check 5 -- the dashboard's own keys survive a real run
# ---------------------------------------------------------------------------


def check_dashboard_reachability(
    manifest: AppManifest, bundle: AppConfigBundle, run: SyntheticRun
) -> CheckResult:
    """Check 5: every key the dashboard asks for is one a real run actually produces.

    Check 3 proves the engine honours ``app.yaml``.  Check 4 proves the uploaded files honour
    ``app.yaml``.  Neither proves the thing that matters to a customer: that the strings
    ``metrics.json`` and ``widgets.json`` send to ClickHouse come back with data in them.

    This is the only check that can verify a ``custom`` stage.  ``resolve_source`` records a
    ``custom.<value>`` source as **unverified** because the value keys live in the author's Python
    (``models.py``), and at runtime a wrong key only logs a warning and drops the series
    (``window.py``).  A ``logic.py`` that loads cleanly, validates cleanly and publishes nothing at
    all is caught here and nowhere else.

    Asserted against the synthetic run:

    * every ``metrics.json`` key appears in ``results-agg.metrics[]``;
    * every published key is declared in ``metrics.json`` -- otherwise the dashboard never asks
      for it and the series is invisible;
    * every ``tracking_class`` widget token appears as a ``tracking_stats[*].current_counts[]``
      category, which is the *other* keyspace and has never been checked anywhere.

    The metric half overlaps check 3 whenever check 4 is also green, and that is deliberate: it
    words the same finding in the dashboard's terms ("this is an empty chart in production") and
    it covers ``derived[]``, which check 3 does not look at.  The category half overlaps nothing.
    ``current_counts`` is populated by ``unique_count``, so an app without one publishes no
    categories at all and every ``tracking_class`` widget on it renders empty forever -- which is
    what two of the five shipped examples did until this check was written.
    """
    problems: list[str] = []
    notes: list[str] = []
    if run.error:
        problems.append(run.error)

    published: set[str] = set()
    for payload in run.aggregations:
        for entry in payload.get("metrics") or ():
            if isinstance(entry, Mapping):
                published.add(str(entry.get("key")))

    categories: set[str] = set()
    for payload in run.aggregations:
        stats = payload.get("tracking_stats")
        if not isinstance(stats, Mapping):
            continue
        for zone_stats in stats.values():
            if not isinstance(zone_stats, Mapping):
                continue
            for entry in zone_stats.get("current_counts") or ():
                if isinstance(entry, Mapping):
                    categories.add(str(entry.get("category")))

    if bundle.metrics is not None:
        uploaded = bundle.metric_keys
        for key in sorted(uploaded - published):
            problems.append(
                f"metrics.json declares {key!r} but no results-agg window published it across "
                f"{len(run.aggregations)} window(s). Published: "
                f"{', '.join(sorted(published)) or '(none)'}. This is an empty chart in production"
            )
        for key in sorted(published - uploaded):
            problems.append(
                f"the engine published {key!r}, which metrics.json never declares; the dashboard "
                f"only requests keys its config names, so this series is written and never read"
            )

    if bundle.widgets is not None:
        wanted: dict[str, list[str]] = {}
        for index, widget in enumerate(bundle.widgets):
            bindings, reason = widget.resolve_bindings()
            if reason is not None:
                continue  # check 4 owns that failure; do not report it twice
            for binding in bindings:
                if binding.data_source == "tracking_class":
                    wanted.setdefault(binding.token, []).append(f"widgets.json[{index}] ({widget.key})")
        for token in sorted(set(wanted) - categories):
            problems.append(
                f"{', '.join(wanted[token])} plots tracking class {token!r}, but no window "
                f"published a current_counts entry for that category. Published categories: "
                f"{', '.join(sorted(categories)) or '(none)'}"
            )

    if published:
        notes.append(f"published metric keys: {', '.join(sorted(published))}")
    if categories:
        notes.append(f"published categories: {', '.join(sorted(categories))}")
    unverified = sorted(stage.stage_name for stage in manifest.custom_stages())
    if unverified:
        notes.append(
            f"custom stage(s) {', '.join(unverified)}: their value keys are unverifiable from the "
            f"manifest, so this check is the only thing standing between them and a silent zero"
        )

    return CheckResult(
        name=CHECK_REACHABILITY,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=tuple(notes),
    )


# ---------------------------------------------------------------------------
# Check 6 -- incident lifecycle
# ---------------------------------------------------------------------------


def check_incident_lifecycle(manifest: AppManifest, run: SyntheticRun) -> CheckResult:
    """Check 6: open -> escalate -> close, with a stable id and monotonic timestamps.

    The backend does **find-or-create on ``incident_id``** with up-only escalation (contract
    §3.2/§3.4), which fixes five properties this asserts:

    1. an occurrence's ``incident_id`` and ``start_time`` are identical in every message that
       mentions it -- a changing id creates a second alert for one event;
    2. severity never decreases.  A de-escalation is not representable, so emitting one is a
       message the backend silently ignores;
    3. the first message of an occurrence carries ``end_time: ""``.  **Only** a non-empty
       ``end_time`` closes an incident -- not a lull, not a restart;
    4. exactly one closing message, and it is the last one for that id;
    5. ``end_time >= start_time``.

    When the manifest declares incidents that the *synthetic* input cannot drive -- a threshold
    on a ``custom`` stage's output, or one whose bound is not a detection count -- the check is
    **skipped with the reason**, never quietly passed: see :func:`_undrivable_rules`.
    """
    problems: list[str] = []
    notes: list[str] = []
    if run.error:
        problems.append(run.error)

    if manifest.incidents is None or not manifest.incidents.types:
        return CheckResult(
            name=CHECK_INCIDENTS,
            status="skipped",
            reason="this manifest declares no 'incidents:' block, so there is no lifecycle to assert",
        )
    if manifest.incidents.lifecycle.emit_on == "never":
        return CheckResult(
            name=CHECK_INCIDENTS,
            status="skipped",
            reason="incidents.lifecycle.emit_on is 'never', so no incident_res message is emitted by design",
        )

    entries = run.incident_entries()
    undrivable = _undrivable_rules(manifest)
    if not entries and not problems:
        if len(undrivable) == len(manifest.incidents.types):
            return CheckResult(
                name=CHECK_INCIDENTS,
                status="skipped",
                reason=(
                    "no incident type in this manifest can be driven by manifest-derived synthetic "
                    "input: " + "; ".join(undrivable.values()) + ". Write a hand-written test for "
                    "these -- a generated suite that passed here would be asserting nothing"
                ),
            )
        problems.append(
            "no incident was raised by the synthetic run, although "
            f"{len(manifest.incidents.types) - len(undrivable)} of "
            f"{len(manifest.incidents.types)} incident type(s) should be reachable from it. "
            "Either the threshold is unreachable in practice or the trigger never fires"
        )

    by_id: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for entry in entries:
        incident_id = str(entry.get("incident_id", ""))
        if incident_id not in by_id:
            by_id[incident_id] = []
            order.append(incident_id)
        by_id[incident_id].append(entry)

    closed = 0
    escalated = 0
    for incident_id in order:
        occurrence = by_id[incident_id]
        where = f"incident {incident_id}"
        first = occurrence[0]
        if str(first.get("end_time", "")):
            problems.append(
                f"{where} was first emitted already closed (end_time={first.get('end_time')!r}); an "
                f"occurrence opens with end_time \"\" -- the backend derives status from it"
            )
        start_times = {str(entry.get("start_time", "")) for entry in occurrence}
        if len(start_times) > 1:
            problems.append(
                f"{where} was emitted with {len(start_times)} different start_times {sorted(start_times)}; "
                f"the backend does find-or-create on incident_id, so one occurrence has one start"
            )
        types = {str(entry.get("incident_type", "")) for entry in occurrence}
        if len(types) > 1:
            problems.append(f"{where} was emitted under {len(types)} incident_types {sorted(types)}")

        ranks = [_severity_rank(str(entry.get("severity_level", ""))) for entry in occurrence]
        for previous, current in pairwise(ranks):
            if current < previous:
                problems.append(
                    f"{where} de-escalated ({previous} -> {current}); the backend ignores a downward "
                    f"severity change entirely, so emitting one is a message that does nothing"
                )
        if len(set(ranks)) > 1:
            escalated += 1

        closings = [index for index, entry in enumerate(occurrence) if str(entry.get("end_time", ""))]
        if closings:
            closed += 1
            if len(closings) > 1:
                problems.append(f"{where} was closed {len(closings)} times; only the last message closes it")
            if closings[-1] != len(occurrence) - 1:
                problems.append(f"{where} emitted {len(occurrence) - 1 - closings[-1]} message(s) after closing")
            end_time = str(occurrence[closings[-1]].get("end_time", ""))
            start_time = str(occurrence[0].get("start_time", ""))
            if end_time < start_time:
                problems.append(f"{where} closes at {end_time} which is before it opened at {start_time}")

    if entries and not closed:
        problems.append(
            f"no incident closed across {run.plan.clear_frames} empty frame(s), although "
            f"close_after_empty_frames is {manifest.incidents.lifecycle.close_after_empty_frames}. "
            "An incident that never closes stays 'active' in the alert feed forever"
        )
    if entries and _expects_escalation(manifest) and not escalated:
        problems.append(
            "no incident escalated, although the severity source is a graded ladder and the "
            "synthetic run raises the magnitude between its 'ramp' and 'escalate' phases"
        )
    if undrivable:
        notes.extend(f"{key}: {reason}" for key, reason in undrivable.items())
    if entries:
        notes.append(f"{len(order)} occurrence(s), {closed} closed, {escalated} escalated")

    return CheckResult(
        name=CHECK_INCIDENTS,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=tuple(notes),
    )


def _severity_rank(level: str) -> int:
    """The wire severity's rank, or ``-1`` for anything not in the vocabulary."""
    try:
        return SEVERITY_RANK[Severity(level)]
    except (KeyError, ValueError):
        return -1


def _expects_escalation(manifest: AppManifest) -> bool:
    """Whether the synthetic magnitude ramp *should* produce an escalation.

    True only when some rule's severity comes from a ladder with more than one rung -- a bare
    ``{metric: {">": 0}}`` threshold has exactly one severity by design
    (:data:`~...runtime.session.DEFAULT_THRESHOLD_SEVERITY`) and demanding an escalation from
    it would be a generated test failing a correct manifest.
    """
    if manifest.incidents is None:
        return False
    for incident in manifest.incidents.types:
        source = incident.severity_from
        if isinstance(source, Mapping):
            if any(len(threshold.levels) > 1 for threshold in source.values()):
                return True
            continue
        if len(_declared_severities(manifest, source)) > 1:
            return True
    return False


def _undrivable_rules(manifest: AppManifest) -> dict[str, str]:
    """``{incident key: why the synthetic input cannot raise it}``.

    Two honest limits of manifest-derived synthesis:

    * a threshold on a metric whose source is a ``custom`` stage -- the value comes out of the
      author's Python and only the author knows what input moves it;
    * a threshold whose bound is larger than the largest detection count the generator will
      synthesise (:data:`_MAX_COUNT`), e.g. ``avg_wait_seconds > 300``.  A generated frame
      cannot make a duration exceed five minutes.

    Naming these is the difference between a suite that reports a gap and one that reports a
    false pass.
    """
    if manifest.incidents is None:
        return {}
    sources = {metric.key: metric for metric in manifest.metrics}
    undrivable: dict[str, str] = {}
    for incident in manifest.incidents.types:
        source = incident.severity_from
        if not isinstance(source, Mapping):
            continue
        reasons: list[str] = []
        for metric_key, threshold in source.items():
            metric = sources.get(metric_key)
            if metric is None:  # pragma: no cover - the manifest validator rejects this
                continue
            try:
                resolved = resolve_source(manifest, metric.source)
            except ValueError:  # pragma: no cover - check 1 reports it
                continue
            if resolved.unverified:
                reasons.append(
                    f"severity_from thresholds {metric_key!r}, whose source {metric.source!r} is a "
                    f"custom stage; its value comes from the author's Python"
                )
                continue
            bounds = [abs(float(value)) for value in threshold.operators.values()]
            bounds += [abs(float(level.value)) for level in threshold.levels]
            if bounds and min(bounds) > _MAX_COUNT:
                reasons.append(
                    f"severity_from thresholds {metric_key!r} at {min(bounds):g}, above the "
                    f"{_MAX_COUNT} detections the generator will synthesise"
                )
        if reasons:
            undrivable[incident.key] = "; ".join(reasons)
    return undrivable


# ---------------------------------------------------------------------------
# Check 7 -- determinism (subprocesses, different hash seeds)
# ---------------------------------------------------------------------------


def check_determinism(
    ref: str | None,
    *,
    seeds: tuple[str, str] = DEFAULT_HASH_SEEDS,
    timeout: float = 600.0,
) -> CheckResult:
    """Check 7: two fresh interpreters, two ``PYTHONHASHSEED`` values, identical bytes.

    **This is the assertion that would have caught PY-9.**  ``engine_session.py:499``
    namespaces tracker state by ``str(hash(stream_key) % 1000000)``; ``hash()`` on a ``str`` is
    salted per process, so the namespace changes on every restart.  Two calls in *one*
    interpreter share the salt and cannot see it -- which is why this check pays for two
    subprocesses instead of calling :func:`run_synthetic` twice.

    Args:
        ref: The app reference a fresh interpreter can reload -- a folder path or a bare app
            id.  ``None`` skips the check with a reason: an in-memory manifest cannot be
            reconstructed in another process, and pretending otherwise would report a pass for
            an assertion that never ran.
        seeds: The two hash seeds.  Fixed by default, because a random seed would make the
            check itself nondeterministic.
        timeout: Per-subprocess timeout, seconds.

    Returns:
        The :class:`CheckResult`.  On divergence the problem names *which surface* differs, so
        the reader is not left diffing two hex digests.
    """
    if not ref:
        return CheckResult(
            name=CHECK_DETERMINISM,
            status="skipped",
            reason=(
                "determinism runs the app in two subprocesses with different PYTHONHASHSEED values "
                "(PY-9), which needs a manifest a fresh interpreter can load. Pass an app folder or "
                "a bare app id rather than an in-memory AppManifest"
            ),
        )

    problems: list[str] = []
    observed: list[dict[str, Any]] = []
    for seed in seeds:
        try:
            observed.append(_digest_in_subprocess(ref, seed=seed, timeout=timeout))
        except RuntimeError as exc:
            problems.append(str(exc))
    if problems:
        return CheckResult(name=CHECK_DETERMINISM, status="failed", problems=tuple(problems))

    first, second = observed[0], observed[1]
    for index, seed in enumerate(seeds):
        if observed[index].get("error"):
            problems.append(f"PYTHONHASHSEED={seed}: the run failed: {observed[index]['error']}")
    if problems:
        return CheckResult(name=CHECK_DETERMINISM, status="failed", problems=tuple(problems))

    if first["digest"] != second["digest"]:
        diverged = [
            surface
            for surface in ("results_agg", "incident_res", "frame_result")
            if first["sections"].get(surface) != second["sections"].get(surface)
        ]
        problems.append(
            f"the same input produced different payloads under PYTHONHASHSEED={seeds[0]} "
            f"({first['digest'][:12]}) and PYTHONHASHSEED={seeds[1]} ({second['digest'][:12]}). "
            f"Diverging surface(s): {', '.join(diverged) or 'unknown'}. This is the PY-9 class of "
            f"defect: something in the pipeline is keyed by a salted hash, a set iteration order or "
            f"a wall clock"
        )
    for surface in ("aggregations", "incidents", "frames"):
        if first["counts"].get(surface) != second["counts"].get(surface):
            problems.append(
                f"the two runs emitted a different number of {surface} payloads "
                f"({first['counts'].get(surface)} vs {second['counts'].get(surface)})"
            )

    return CheckResult(
        name=CHECK_DETERMINISM,
        status="failed" if problems else "passed",
        problems=tuple(problems),
        notes=(
            f"PYTHONHASHSEED={seeds[0]} and {seeds[1]} both produced digest {first['digest'][:12]} over "
            f"{first['counts'].get('aggregations')} results-agg, {first['counts'].get('incidents')} "
            f"incident_res and {first['counts'].get('frames')} frame payload(s)",
        ),
    )


#: What the determinism subprocess executes.  ``-c`` rather than ``-m`` on purpose: importing
#: this module through its package would re-enter it as ``__main__`` and print a ``runpy``
#: warning onto the child's stderr, and a check whose output has to be parsed should not have
#: to tolerate chatter it caused itself.  The equivalent human-facing entry point is
#: ``python -m matrice_analytics.engine.testing.generate --digest <app>``.
_WORKER_SOURCE: Final[str] = (
    "import sys, warnings, logging\n"
    "warnings.filterwarnings('ignore')\n"
    "logging.disable(logging.CRITICAL)\n"
    "from matrice_analytics.engine.testing.generate import _digest_record, _dumps\n"
    "print(_dumps(_digest_record(sys.argv[1])))\n"
)


def _digest_in_subprocess(ref: str, *, seed: str, timeout: float) -> dict[str, Any]:
    """Run the app in a fresh interpreter under ``seed`` and return its digest record.

    Raises:
        RuntimeError: The subprocess failed to start, timed out, or printed nothing parseable.
            Raised rather than returned so the caller reports it as a failed check with the
            interpreter's own stderr attached -- a silent zero here would be the same class of
            defect the whole suite exists to catch.
    """
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = seed
    # The child must import the same tree this process did, whether that is an editable
    # install, a src/ layout on sys.path, or a wheel.
    existing = env.get("PYTHONPATH", "")
    entries = [entry for entry in sys.path if entry] + ([existing] if existing else [])
    env["PYTHONPATH"] = os.pathsep.join(dict.fromkeys(entries))
    env["PYTHONWARNINGS"] = env.get("PYTHONWARNINGS", "ignore")

    command = [sys.executable, "-c", _WORKER_SOURCE, ref]
    try:
        completed = subprocess.run(  # noqa: S603 - fixed argv, no shell
            command,
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"PYTHONHASHSEED={seed}: the run did not finish within {timeout}s") from exc

    if completed.returncode != 0:
        raise RuntimeError(
            f"PYTHONHASHSEED={seed}: the interpreter exited {completed.returncode}\n"
            f"--- stdout ---\n{completed.stdout}\n--- stderr ---\n{completed.stderr}"
        )
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not lines:
        raise RuntimeError(f"PYTHONHASHSEED={seed}: the interpreter printed nothing.\nstderr:\n{completed.stderr}")
    try:
        record = json.loads(lines[-1])
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"PYTHONHASHSEED={seed}: could not read the digest line {lines[-1]!r}: {exc}") from exc
    if not isinstance(record, dict) or "digest" not in record:
        raise RuntimeError(f"PYTHONHASHSEED={seed}: the digest line is not a digest record: {lines[-1]!r}")
    return record


def _digest_record(ref: str) -> dict[str, Any]:
    """The JSON record the ``--digest`` mode prints.  Also useful on its own, in a REPL."""
    run = run_synthetic(ref)
    sections = run.section_digests()
    return {
        "app_id": run.app_id,
        "ref": ref,
        "digest": _digest(sections["payloads"]),
        "sections": {key: value for key, value in sections.items() if key != "payloads"},
        "counts": {
            "aggregations": len(run.aggregations),
            "incidents": len(run.incidents),
            "frames": len(run.frame_results),
        },
        "error": run.error,
        "hash_seed": os.environ.get("PYTHONHASHSEED", ""),
    }


# ---------------------------------------------------------------------------
# The suite
# ---------------------------------------------------------------------------


def suite_checks(
    app: str | os.PathLike[str] | AppManifest | LoadedApp,
    *,
    seeds: tuple[str, str] = DEFAULT_HASH_SEEDS,
) -> tuple[GeneratedCheck, ...]:
    """The generated checks for one app, as callables -- the pytest entry point.

    The synthetic run is built **once** and shared by every check that needs it, lazily, and the
    uploaded config files are read once, so parametrising over an app costs one session.

    Args:
        app: An app folder, a bare app id, a :class:`~...manifest.loader.LoadedApp` or an
            :class:`~...manifest.models.AppManifest`.
        seeds: The two ``PYTHONHASHSEED`` values check 5 runs under.

    Returns:
        One :class:`GeneratedCheck` per entry in :data:`CHECK_NAMES`, in that order.  A check
        named in the manifest's ``tests.skip`` is still returned -- it reports ``skipped`` with
        the author's reason, so the gap stays visible in the test report instead of vanishing.
    """
    resolved = _resolve_app(app)
    manifest = resolved.manifest
    skips = _skips(manifest)
    cache: dict[str, SyntheticRun] = {}
    cache_config: dict[str, AppConfigBundle] = {}

    def run() -> SyntheticRun:
        if "run" not in cache:
            cache["run"] = _run_resolved(resolved)
        return cache["run"]

    def unloadable(name: str) -> CheckResult:
        return CheckResult(
            name=name,
            status="failed",
            problems=(f"the manifest did not load, so this check could not run: {resolved.load_error}",),
        )

    def schema() -> CheckResult:
        return _check_schema(resolved)

    def conformance() -> CheckResult:
        return unloadable(CHECK_CONFORMANCE) if manifest is None else check_contract_conformance(run())

    def metrics() -> CheckResult:
        return unloadable(CHECK_METRICS) if manifest is None else check_metric_presence(manifest, run())

    def config() -> AppConfigBundle | None:
        if resolved.root is None:
            return None
        if "config" not in cache_config:
            cache_config["config"] = load_app_config(resolved.root)
        return cache_config["config"]

    def no_folder(name: str) -> CheckResult:
        return CheckResult(
            name=name,
            status="skipped",
            reason="no app folder (in-memory manifest), so there are no uploaded files to check",
        )

    def no_files(name: str) -> CheckResult:
        return CheckResult(
            name=name,
            status="skipped",
            reason=(
                "no metrics.json, widgets.json or post_processing_config.json beside app.yaml; "
                "the app cannot be published without them, but nothing here can be checked"
            ),
        )

    def app_config() -> CheckResult:
        if manifest is None:
            return unloadable(CHECK_APP_CONFIG)
        bundle = config()
        if bundle is None:
            return no_folder(CHECK_APP_CONFIG)
        if bundle.none_present:
            return no_files(CHECK_APP_CONFIG)
        return check_app_config_files(manifest, bundle)

    def reachability() -> CheckResult:
        if manifest is None:
            return unloadable(CHECK_REACHABILITY)
        bundle = config()
        if bundle is None:
            return no_folder(CHECK_REACHABILITY)
        if bundle.none_present:
            return no_files(CHECK_REACHABILITY)
        return check_dashboard_reachability(manifest, bundle, run())

    def incidents() -> CheckResult:
        return unloadable(CHECK_INCIDENTS) if manifest is None else check_incident_lifecycle(manifest, run())

    def determinism() -> CheckResult:
        return check_determinism(resolved.ref, seeds=seeds)

    bodies: dict[str, Callable[[], CheckResult]] = {
        CHECK_SCHEMA: schema,
        CHECK_CONFORMANCE: conformance,
        CHECK_METRICS: metrics,
        CHECK_APP_CONFIG: app_config,
        CHECK_REACHABILITY: reachability,
        CHECK_INCIDENTS: incidents,
        CHECK_DETERMINISM: determinism,
    }
    descriptions: dict[str, str] = {
        CHECK_SCHEMA: "the manifest loads, every source resolves, every enum is legal, every primitive exists",
        CHECK_CONFORMANCE: "synthesised detections through a real Session; all six contract §7 checks",
        CHECK_METRICS: "every declared metric appears in results-agg.metrics[] with its declared shape",
        CHECK_APP_CONFIG: "metrics.json, widgets.json and post_processing_config.json agree with app.yaml",
        CHECK_REACHABILITY: "every key the dashboard asks for is one a real run publishes (PY-1b)",
        CHECK_INCIDENTS: "open -> escalate -> close, stable incident_id, monotonic timestamps",
        CHECK_DETERMINISM: "byte-identical payloads in two subprocesses with different PYTHONHASHSEED (PY-9)",
    }

    checks: list[GeneratedCheck] = []
    for name in CHECK_NAMES:
        reason = skips.get(name)
        body = bodies[name] if reason is None else _skipped(name, reason)
        checks.append(GeneratedCheck(name=name, description=descriptions[name], run=body))
    return tuple(checks)


def _skipped(name: str, reason: str) -> Callable[[], CheckResult]:
    def body() -> CheckResult:
        return CheckResult(name=name, status="skipped", reason=f"tests.skip in the manifest: {reason}")

    return body


def _skips(manifest: AppManifest | None) -> dict[str, str]:
    """``{check name: author's reason}`` from the manifest's ``tests.skip`` block."""
    if manifest is None:
        return {}
    skips: dict[str, str] = {}
    for entry in manifest.tests.skip:
        name = _SKIP_ALIASES.get(entry.test.strip().lower())
        if name is None:
            logger.warning(
                "tests.skip names %r, which is not a generated check. Known checks: %s",
                entry.test,
                ", ".join(CHECK_NAMES),
            )
            continue
        skips[name] = entry.reason
    return skips


def generate_suite(
    app: str | os.PathLike[str] | AppManifest | LoadedApp,
    *,
    seeds: tuple[str, str] = DEFAULT_HASH_SEEDS,
) -> SuiteResult:
    """Run every generated check for one app and collect the verdicts.

    The one-call form, for a CLI or a smoke test.  A host repo that wants one pytest case per
    check parametrises over :func:`suite_checks` instead.
    """
    resolved = _resolve_app(app)
    results = tuple(check() for check in suite_checks(app, seeds=seeds))
    return SuiteResult(app_id=resolved.app_id, source=resolved.source, results=results)


def describe_suite(app: str | os.PathLike[str] | AppManifest | LoadedApp) -> str:
    """What the generated suite *is*, without running it.

    The compensation for not emitting readable test files: it names every check, every skip,
    and the exact synthetic magnitudes derived from the manifest -- which is what an author
    actually needs when a generated assertion surprises them.
    """
    resolved = _resolve_app(app)
    lines = [f"generated suite for {resolved.app_id}  ({resolved.source})"]
    if resolved.manifest is None:
        lines.append(f"  the manifest does not load: {resolved.load_error}")
        return "\n".join(lines)

    skips = _skips(resolved.manifest)
    for check in suite_checks(app):
        marker = "skip" if check.name in skips else "run "
        lines.append(f"  {marker} {check.name}: {check.description}")
        if check.name in skips:
            lines.append(f"        tests.skip reason: {skips[check.name]}")
    lines.append("")
    lines.append(frame_plan(resolved.manifest).describe())
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """``python -m matrice_analytics.engine.testing.generate <app> [...]``.

    Two modes:

    * ``--digest <app>`` prints one JSON line -- the payload digest for this interpreter's
      ``PYTHONHASHSEED``.  This is what :func:`check_determinism` spawns; it is a public mode
      rather than a private one so the determinism check can be reproduced by hand.
    * ``[--describe] <app> [<app> ...]`` runs (or describes) the generated suite and prints a
      report.  Exit code 1 when any check failed.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == _DIGEST_FLAG:
        if len(args) != 2:
            print(f"usage: {_DIGEST_FLAG} <app-reference>", file=sys.stderr)
            return 2
        print(_dumps(_digest_record(args[1])))
        return 0

    describe = "--describe" in args
    refs = [arg for arg in args if not arg.startswith("-")]
    if not refs:
        print(
            "usage: python -m matrice_analytics.engine.testing.generate [--describe] <app-reference> ...",
            file=sys.stderr,
        )
        return 2

    failed = False
    for ref in refs:
        if describe:
            print(describe_suite(ref))
            continue
        result = generate_suite(ref)
        print(result.report())
        failed = failed or not result.passed
    return 1 if failed else 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main())
