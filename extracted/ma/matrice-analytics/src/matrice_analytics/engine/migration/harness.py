"""Run both engines on one input and diff what they emit.

This is the gate every migration wave runs (``clauding/PHASE2_PLAN.md`` §5,
``clauding/STAGE_BC_PLAN.md`` §7): a legacy use case may only be deleted once the new
engine, **on the same frames**, emits the **same payload**.

Three pieces:

:func:`generate_frames`
    A deterministic synthetic detection sequence -- objects entering and leaving, crossing
    a line, dwelling in a zone, with stable ground-truth ids.  Deterministic is not a
    nicety: a flaky harness is worse than none, because a red run that goes green on retry
    trains everyone to retry.  There is no RNG anywhere in this module, and
    :attr:`FrameSequence.digest` pins the bytes.

:func:`run_new_engine` / :func:`run_legacy`
    The two adapters.  ``run_new_engine`` is ``load_app_bundle -> Session -> process_frame``
    (``STAGE_BC_PLAN`` §4).  ``run_legacy`` is ``PostProcessor.process`` per frame with the
    Redis publisher replaced by a collector.

:func:`compare_usecase`
    The two of them plus :func:`~matrice_analytics.engine.migration.differ.diff_results_agg`.

Import isolation (**PY-20**)
----------------------------
``PY-20`` is fixed for the engine only: ``matrice_analytics.post_processing`` still
executes ~180 legacy modules and pulls in torch and cv2 on import.  So **every legacy
import in this file is lazy and inside the legacy branch** -- this module, and the CLI that
wraps it, are importable and usable for the new-engine side alone.  ``tests`` asserts it.

Two structural facts about the legacy side that shape everything below
----------------------------------------------------------------------
1. **The legacy window boundary is wall-clock.**
   ``utils/legacy_analytics_bridge.py:3009`` gates ``results-agg`` on
   ``time.time() - last_agg_publish_ts < 60`` (**PY-13** on the emission path).  With
   ``last_agg_publish_ts == 0`` the *first frame publishes immediately*, with an empty
   window.  A harness that just fed frames and read the payloads would therefore compare
   the new engine's 250-frame window against a legacy zero-frame window.
   :func:`run_legacy` pins the clock forward after every frame so no boundary fires
   mid-run, then forces exactly one publish at the end -- one legacy window over exactly
   the frames the new engine's window covers.
2. **The legacy ``results-agg`` builder is the bridge, not the use case.**  The use case
   returns ``agg_summary``; ``publish_legacy_frame_analytics`` folds it into a window and
   builds the wire payload.  That is the surface worth diffing, because it is the one that
   reaches ClickHouse.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Final

from matrice_analytics.engine.contract.emit import STREAM_RESULTS_AGG
from matrice_analytics.engine.manifest.loader import load_app_bundle
from matrice_analytics.engine.migration.differ import (
    CANONICAL_GLOBAL_ZONE,
    DEFAULT_TOLERANCE,
    DiffContext,
    DiffReport,
    TolerancePolicy,
    diff_results_agg,
)
from matrice_analytics.engine.runtime import Session, resolve_stream_info

__all__ = [
    "BASE_FRAME_TS",
    "DEFAULT_FPS",
    "DEFAULT_RESOLUTION",
    "DWELL_ZONE",
    "LINE_X",
    "EngineRun",
    "FrameSequence",
    "SyntheticFrame",
    "compare_usecase",
    "default_stream_info",
    "dump_frames_to_json",
    "generate_frames",
    "load_frames_from_json",
    "run_legacy",
    "run_new_engine",
]

logger = logging.getLogger(__name__)


#: ``2026-07-31T09:00:00Z``.  A fixed anchor, because the new engine's window boundary and
#: every emitted timestamp are frame time (**PY-13**) -- so with a fixed anchor the new
#: payload is byte-identical across runs and machines, which is what makes a golden file
#: possible at all.
BASE_FRAME_TS: Final[float] = 1_785_488_400.0

DEFAULT_FPS: Final[float] = 25.0
DEFAULT_RESOLUTION: Final[tuple[int, int]] = (1920, 1080)

#: The half-plane boundary the traversing objects cross, normalized.  Two of them go
#: left-to-right and one right-to-left so a direction-aware counter has both signs.
LINE_X: Final[float] = 0.5

#: The dwell rectangle, normalized ``(xmin, ymin, xmax, ymax)``.  Dwellers sit inside it
#: for their whole life, so ``dwell`` measures a duration a test can predict.
DWELL_ZONE: Final[tuple[float, float, float, float]] = (0.55, 0.50, 0.95, 0.98)


# ---------------------------------------------------------------------------
# The synthetic input
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SyntheticFrame:
    """One frame of detections, in the shape the inference pipeline really sends."""

    index: int
    frame_ts: float
    """Epoch seconds.  ``BASE_FRAME_TS + index / fps`` -- frame time, never wall time."""

    detections: tuple[dict[str, Any], ...]
    """Normalized 0-1 boxes (contract §4), ``category`` + ``confidence`` + ``bounding_box``."""

    track_ids: tuple[int, ...] = ()
    """Ground-truth object id per detection, **parallel to** :attr:`detections`.

    Deliberately *not* written into the detection dicts.  Both engines run their own
    tracker, and handing them an id would make the comparison test the harness's tracker
    rather than theirs.  This is here so a test can assert what the answer should be.
    """

    def pixel_detections(self, resolution: tuple[int, int]) -> list[dict[str, Any]]:
        """The same detections in source-pixel coordinates.

        The legacy tree is fed source-pixel boxes -- ``runtime/post_proc_runner.py`` states
        it as the caller's contract ("Callers must supply detections already in
        SOURCE-PIXEL coordinates") -- while the new engine is normalized 0-1 by contract §4.
        Converting here, from one generator, is what keeps "the same input" true.
        """
        width, height = resolution
        out: list[dict[str, Any]] = []
        for detection in self.detections:
            box = detection["bounding_box"]
            scaled = dict(detection)
            scaled["bounding_box"] = {
                "xmin": box["xmin"] * width,
                "ymin": box["ymin"] * height,
                "xmax": box["xmax"] * width,
                "ymax": box["ymax"] * height,
            }
            out.append(scaled)
        return out


@dataclass(frozen=True, slots=True)
class FrameSequence:
    """A generated sequence plus the facts a test or a report wants to state."""

    frames: tuple[SyntheticFrame, ...]
    fps: float
    objects: int
    category: str
    resolution: tuple[int, int]
    line_x: float = LINE_X
    dwell_zone: tuple[float, float, float, float] = DWELL_ZONE

    def __len__(self) -> int:
        return len(self.frames)

    def __iter__(self) -> Any:
        return iter(self.frames)

    @property
    def span_seconds(self) -> float:
        """Frame-time span.  Under 60 s means exactly one aggregation window."""
        return 0.0 if not self.frames else len(self.frames) / self.fps

    @property
    def unique_objects(self) -> int:
        """How many distinct ground-truth ids appear at all."""
        return len({track_id for frame in self.frames for track_id in frame.track_ids})

    @property
    def digest(self) -> str:
        """sha256 of the canonical JSON of every detection, ids included.

        The determinism assertion in one value: two runs of :func:`generate_frames` with
        the same arguments have the same digest, on any machine, under any
        ``PYTHONHASHSEED``.  That last part is not hypothetical -- **PY-9** was a tracker
        namespace randomised by the hash seed.
        """
        payload = [
            {
                "index": frame.index,
                "frame_ts": frame.frame_ts,
                "detections": list(frame.detections),
                "track_ids": list(frame.track_ids),
            }
            for frame in self.frames
        ]
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(blob).hexdigest()


def generate_frames(
    frames: int = 250,
    *,
    objects: int = 6,
    fps: float = DEFAULT_FPS,
    base_ts: float = BASE_FRAME_TS,
    category: str = "person",
    resolution: tuple[int, int] = DEFAULT_RESOLUTION,
) -> FrameSequence:
    """Build a deterministic synthetic detection sequence.

    The sequence exercises the four temporal behaviours the counting/geometry/temporal
    primitives are built around, so a diff over it is not just a diff over "some boxes":

    * **entering and leaving** -- object ``k`` appears at frame ``k*frames//(2*objects)``
      and disappears at ``frames - k*frames//(4*objects)``, so the population rises and
      falls and ``current_counts`` is not a constant.  A constant occupancy makes ``sum``,
      ``mean``, ``max`` and ``last`` indistinguishable, which is exactly the four agg types
      **PY-1** confuses.
    * **crossing a line** -- two thirds of the objects traverse the frame horizontally,
      crossing ``x = 0.5`` once, at a frame determined only by their entry frame.  One of
      them travels right-to-left so a direction-aware counter sees both signs.
    * **dwelling in a zone** -- every third object sits inside :data:`DWELL_ZONE` for its
      whole life with a small, periodic, integer-driven wobble, so ``dwell`` measures a
      duration a test can predict and ``velocity_state`` reports ``stationary``.
    * **stable ids** -- motion per frame is a fraction of a box width, which is what lets
      both trackers keep an object's identity across frames.  Without that, ``unique_count``
      counts each person once per frame: the classic "the numbers are far too high" report.

    There is **no randomness**: every position is a closed-form function of
    ``(object index, frame index)``.  ``random.Random(seed)`` would also be reproducible,
    but only for as long as nobody adds a draw in the middle, and the failure is silent.

    Args:
        frames: How many frames to generate.  At the default 25 fps, 250 frames is 10 s of
            frame time -- comfortably inside one 60-second aggregation window, so both
            engines produce exactly one comparable window.
        objects: How many distinct objects appear over the sequence.
        fps: Frame rate, used for the frame timestamps.  Must be > 0.
        base_ts: Epoch seconds for frame 0.
        category: The model label every detection carries.  Must match the right-hand side
            of the app's ``model.entity_mapping`` character for character, or the new engine
            counts every detection as unmapped and every number is zero.
        resolution: Source ``(width, height)``, for :meth:`SyntheticFrame.pixel_detections`.

    Returns:
        A :class:`FrameSequence`.

    Raises:
        ValueError: ``frames`` < 1, ``objects`` < 1 or ``fps`` <= 0.
    """
    if frames < 1:
        raise ValueError(f"frames must be >= 1, got {frames}")
    if objects < 1:
        raise ValueError(f"objects must be >= 1, got {objects}")
    if fps <= 0:
        raise ValueError(f"fps must be > 0, got {fps}")

    box_w, box_h = 0.05, 0.18
    generated: list[SyntheticFrame] = []
    for index in range(frames):
        detections: list[dict[str, Any]] = []
        ids: list[int] = []
        for obj in range(objects):
            enter = (obj * frames) // (2 * objects)
            leave = frames - (obj * frames) // (4 * objects)
            if not enter <= index < leave:
                continue
            life = max(1, leave - enter - 1)
            progress = (index - enter) / life
            if obj % 3 == 2:
                # A dweller: parked inside DWELL_ZONE, wobbling on a 15-frame integer cycle
                # so it is unambiguously stationary but not a frozen box.
                lane = (obj // 3) % 3
                wobble = 0.004 * (((index // 5) % 3) - 1)
                # The +0.01 inset keeps the whole wobble inside DWELL_ZONE, so "is this
                # object in the zone" has one answer for its entire life and a dwell
                # duration is predictable rather than a function of the wobble phase.
                xmin = DWELL_ZONE[0] + 0.01 + 0.10 * lane + wobble
                ymin = DWELL_ZONE[1] + 0.12 * lane
            elif obj % 3 == 1:
                # Right-to-left traverser: crosses LINE_X with the opposite sign.
                lane = (obj // 3) % 4
                xmin = 0.90 - 0.85 * progress
                ymin = 0.04 + 0.10 * lane
            else:
                # Left-to-right traverser.
                lane = (obj // 3) % 4
                xmin = 0.05 + 0.85 * progress
                ymin = 0.06 + 0.10 * lane
            xmin = min(max(xmin, 0.0), 1.0 - box_w)
            ymin = min(max(ymin, 0.0), 1.0 - box_h)
            detections.append(
                {
                    "category": category,
                    # Deterministic, and always above the 0.45 threshold the handover
                    # manifests declare, so intake never silently drops an object.
                    "confidence": round(0.62 + 0.03 * (obj % 8), 4),
                    "bounding_box": {
                        "xmin": round(xmin, 6),
                        "ymin": round(ymin, 6),
                        "xmax": round(xmin + box_w, 6),
                        "ymax": round(ymin + box_h, 6),
                    },
                }
            )
            ids.append(obj + 1)
        generated.append(
            SyntheticFrame(
                index=index,
                frame_ts=base_ts + index / fps,
                detections=tuple(detections),
                track_ids=tuple(ids),
            )
        )
    return FrameSequence(
        frames=tuple(generated),
        fps=fps,
        objects=objects,
        category=category,
        resolution=resolution,
    )


def default_stream_info(
    *,
    camera_id: str = "65f0c2b9a1d4e8f7b3c9d2e1",
    camera_name: str = "Store Entrance",
    camera_group: str = "Ground Floor",
    app_id: str = "app-migration-diff",
    app_deployment_id: str = "dep-migration-diff",
    application_name: str = "Migration Diff",
    application_key_name: str = "people_counting",
    application_version: str = "1.0",
    location: str = "",
    fps: float = DEFAULT_FPS,
    resolution: tuple[int, int] = DEFAULT_RESOLUTION,
    stream_time: str = "2026-07-31-09:00:00.000000 UTC",
) -> dict[str, Any]:
    """The untyped worker ``stream_info`` dict both engines are given (surface S4).

    Intentionally the *nested, mixed-casing* shape a real worker sends rather than the
    typed model: ``engine_session.py:263-389`` reverse-engineers this across five nested
    lookup paths in two casings, and that function *is* the undocumented input contract.
    Feeding both engines the identical dict is the only way a payload difference can be
    attributed to the pipeline rather than to the two parsers.

    Every identity field is written at **both** the top level and inside ``camera_info``,
    because the two parsers do not read the same path: the new engine's
    :func:`~...runtime.stream_info.resolve_stream_info` prefers ``camera_info.camera_group``
    while the legacy ``extract_stream_context`` reads only
    ``stream_info["camera_group"]`` / ``input_settings["camera_group"]`` and otherwise
    substitutes the literal ``"default_group"``
    (``utils/legacy_analytics_bridge.py:1337``).  Supplying the union is not papering over
    anything -- it removes a *parser* difference from a comparison that is about the
    *analytics*.  That the union is necessary at all is the input contract's own defect and
    is reported separately, not silenced.
    """
    width, height = resolution
    return {
        "camera_id": camera_id,
        "camera_name": camera_name,
        "camera_group": camera_group,
        "location": location,
        "camera_info": {
            "camera_id": camera_id,
            "camera_name": camera_name,
            "camera_group": camera_group,
            "location": location,
        },
        "app_id": app_id,
        "app_deployment_id": app_deployment_id,
        "application_id": app_id,
        "application_name": application_name,
        "application_key_name": application_key_name,
        "application_version": application_version,
        "input_settings": {
            "original_fps": fps,
            "start_frame": 0,
            "end_frame": 0,
            "camera_group": camera_group,
        },
        "stream_resolution": {"width": width, "height": height},
        "rtp_number": "41",
        "frame_id": "",
        "stream_time": stream_time,
    }


# ---------------------------------------------------------------------------
# What one engine produced
# ---------------------------------------------------------------------------


@dataclass
class EngineRun:
    """Everything one engine emitted over one frame sequence."""

    engine: str
    """``"new"`` or ``"legacy"``."""

    aggregations: tuple[dict[str, Any], ...] = ()
    """Every ``results-agg`` payload published, in order."""

    incidents: tuple[dict[str, Any], ...] = ()
    """Every ``incident_res`` payload published, in order."""

    frames_processed: int = 0
    error: str = ""
    """Why the run stopped early, or ``""``.  Never raised out of the adapter: "the legacy
    side will not run" is itself a finding worth reporting, not a traceback."""

    notes: list[str] = field(default_factory=list)

    @property
    def window(self) -> dict[str, Any] | None:
        """The ``results-agg`` payload to compare -- the **last** one published.

        Both adapters are arranged so exactly one window covers the whole sequence.  When
        more than one arrives (a sequence longer than 60 s of frame time, or a legacy
        wall-clock boundary that fired anyway) the last is the complete one and a note says
        how many there were.
        """
        return self.aggregations[-1] if self.aggregations else None


class _Collector:
    """A :class:`~matrice_analytics.engine.contract.emit.Publisher` that keeps payloads."""

    def __init__(self) -> None:
        self.messages: list[tuple[str, dict[str, Any]]] = []

    def publish(self, stream: str, payload: dict[str, Any]) -> None:
        self.messages.append((stream, dict(payload)))

    def of(self, stream: str) -> tuple[dict[str, Any], ...]:
        return tuple(payload for name, payload in self.messages if name == stream)


class _LegacyCollector:
    """The legacy publisher interface: ``publish_aggregation`` / ``publish_incident``.

    ``analytics/redis_publisher.py``'s methods return truthy on success, and
    ``maybe_publish_results_agg`` only advances its window when the publish returned true --
    so returning ``True`` here is load-bearing, not politeness.
    """

    def __init__(self) -> None:
        self.aggregations: list[dict[str, Any]] = []
        self.incidents: list[dict[str, Any]] = []

    def publish_aggregation(self, camera_id: str, payload: Mapping[str, Any]) -> bool:
        self.aggregations.append(dict(payload))
        return True

    def publish_incident(self, camera_id: str, payload: Mapping[str, Any]) -> bool:
        self.incidents.append(dict(payload))
        return True


# ---------------------------------------------------------------------------
# The new engine
# ---------------------------------------------------------------------------


def _app_folder(manifest_path: str | os.PathLike[str]) -> str | os.PathLike[str]:
    """Accept either the app folder or its ``app.yaml``.

    ``load_app_bundle`` wants the folder -- it also resolves ``logic.py``, samples and
    goldens relative to it -- and refuses a file with a clear message.  A human running a
    migration wave will point at the manifest they were just reading, so the pointer is
    followed here rather than turned into an error a second time.  A non-path ref (a
    registry name, a URL) passes straight through.
    """
    if not isinstance(manifest_path, (str, os.PathLike)):
        return manifest_path
    candidate = Path(manifest_path)
    if candidate.is_file() and candidate.name in {"app.yaml", "app.yml"}:
        return candidate.parent
    return manifest_path


def run_new_engine(
    manifest_path: str | os.PathLike[str],
    frames: Sequence[SyntheticFrame],
    *,
    stream_info: Mapping[str, Any] | None = None,
) -> tuple[EngineRun, Session]:
    """Run the new engine over ``frames``: ``load_app_bundle -> Session -> process_frame``.

    The chain is ``STAGE_BC_PLAN`` §4's, with nothing stubbed but the transport.

    Args:
        manifest_path: The app folder or ``app.yaml`` -- anything
            :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle` resolves.
        frames: The sequence from :func:`generate_frames`.
        stream_info: The untyped worker dict.  Defaults to :func:`default_stream_info`.

    Returns:
        ``(run, session)``.  The session is returned because the comparison needs facts
        only it knows -- ``emission_zones`` and the resolved reference point -- to build the
        :class:`~matrice_analytics.engine.migration.differ.DiffContext`.

    Raises:
        AppLoadError: The manifest is invalid.  A migration wave should not swallow that.
        SessionError: The manifest cannot run against this stream.
    """
    bundle = load_app_bundle(_app_folder(manifest_path))
    parsed = resolve_stream_info(dict(stream_info or default_stream_info()))
    collector = _Collector()
    session = Session.from_loaded_app(
        bundle,
        parsed.stream,
        publisher=collector,
        # FROZEN-4: totals mean "since this instant". Anchoring on the first frame makes
        # reset_timestamp reproducible, which a golden file depends on.
        started_at=frames[0].frame_ts if frames else BASE_FRAME_TS,
    )
    run = EngineRun(engine="new")
    if parsed.fallbacks:
        run.notes.append(
            "stream_info fallbacks taken: "
            + ", ".join(sorted({source.field for source in parsed.fallbacks}))
        )
    try:
        for frame in frames:
            session.process_frame(list(frame.detections), frame_ts=frame.frame_ts)
            run.frames_processed += 1
        # Close the partial window so the whole sequence is one comparable aggregation.
        session.flush()
    except Exception as exc:  # a wave wants the finding, not a traceback
        run.error = f"{type(exc).__name__}: {exc}"
        logger.exception("new engine failed after %d frame(s)", run.frames_processed)

    run.aggregations = collector.of(STREAM_RESULTS_AGG)
    run.incidents = tuple(
        payload for name, payload in collector.messages if name != STREAM_RESULTS_AGG
    )
    if len(run.aggregations) > 1:
        run.notes.append(
            f"the new engine published {len(run.aggregations)} windows; comparing the last. "
            f"Frame-time span was {len(frames) / max(DEFAULT_FPS, 1e-9):.1f}s at the default fps."
        )
    if not run.aggregations:
        run.notes.append(
            "the new engine published no results-agg. With emission.emit_empty_windows "
            "false, an app that counted nothing emits nothing -- check the entity mapping "
            "first: an unmapped model label is the most common cause of an all-zero window."
        )
    return (run, session)


# ---------------------------------------------------------------------------
# The legacy engine
# ---------------------------------------------------------------------------


def run_legacy(
    usecase: str,
    frames: Sequence[SyntheticFrame],
    *,
    stream_info: Mapping[str, Any] | None = None,
    resolution: tuple[int, int] = DEFAULT_RESOLUTION,
    index_to_category: Mapping[int, str] | None = None,
    legacy_category: str | None = None,
    config_overrides: Mapping[str, Any] | None = None,
) -> EngineRun:
    """Run the legacy ``PostProcessor`` over ``frames`` and collect its ``results-agg``.

    **Every import here is lazy and local.**  ``matrice_analytics.post_processing``
    executes ~180 modules and pulls in torch and cv2 (**PY-20**, fixed for the engine
    only), so importing this harness must not pay that cost and must not fail on a box
    without those wheels.

    Two adjustments are made to the legacy accumulator, both because its window boundary is
    wall-clock (``legacy_analytics_bridge.py:3009``) and the comparison needs a window that
    covers the same frames as the new engine's:

    1. ``last_agg_publish_ts`` is pinned to *now* before the first frame and re-pinned after
       every frame.  Without the first pin the very first frame publishes an **empty**
       window, because the gate is ``if not force and self.last_agg_publish_ts and ...`` and
       zero is falsy.  Without the re-pin, a sequence that takes over 60 s of wall time
       splits into windows at positions that depend on how busy the machine is.
    2. Exactly one publish is then forced (``force=True``), covering every frame.

    Args:
        usecase: The legacy use-case name, e.g. ``people_counting``.
        frames: The sequence from :func:`generate_frames`.
        stream_info: The untyped worker dict -- the *same* one the new engine gets.
        resolution: Source ``(width, height)``; the legacy tree is fed pixel boxes.
        index_to_category: Class index -> model label.  Derive it from the manifest so both
            engines see the same class list.
        legacy_category: The registry category the use case is registered under.  Resolved
            from the legacy registry when omitted.
        config_overrides: Extra keys merged into the legacy config dict.

    Returns:
        An :class:`EngineRun`.  ``error`` is set rather than raised: "the legacy side will
        not run" is a finding, and it is the finding that decides whether an app can be
        diffed at all.
    """
    run = EngineRun(engine="legacy")
    try:
        import asyncio

        from matrice_analytics.post_processing.post_processor import PostProcessor
        from matrice_analytics.post_processing.utils import legacy_analytics_bridge as bridge
    except Exception as exc:  # torch/cv2 absence is a legitimate outcome, not a crash
        run.error = (
            f"the legacy tree could not be imported ({type(exc).__name__}: {exc}). "
            "post_processing pulls in ~180 modules plus torch and cv2 (PY-20); the engine "
            "is importable without them, the legacy side is not."
        )
        return run

    raw_stream_info = dict(stream_info or default_stream_info())
    stream_key = str(raw_stream_info.get("camera_id") or "default_stream")

    if usecase not in bridge.legacy_redis_analytics_usecases():
        run.notes.append(
            f"{usecase!r} is not in legacy_redis_analytics_usecases(), so the legacy tree "
            "publishes no results-agg for it at all. Either it is one of the documented "
            "still-image exclusions or MATRICE_LEGACY_PUBLISHER is set, which cedes "
            "publishing to the caller's old AnalyticsPublisher."
        )

    collector = _LegacyCollector()
    try:
        processor = PostProcessor(
            app_name=usecase,
            index_to_category=dict(index_to_category) if index_to_category else None,
        )
    except Exception as exc:
        run.error = f"PostProcessor({usecase!r}) raised {type(exc).__name__}: {exc}"
        return run

    # The publisher is created lazily and cached on the instance; replacing it here is what
    # keeps the harness off Redis. It is private state, deliberately: there is no injection
    # seam on PostProcessor, and adding one is not this workstream's file to touch.
    processor._analytics_publisher = collector

    config: dict[str, Any] = {
        "usecase": usecase,
        "category": legacy_category or _legacy_category_for(usecase),
        "enable_analytics": True,
    }
    config.update(dict(config_overrides or {}))

    bridge.reset_legacy_sessions()
    session = bridge.get_legacy_session(stream_key)
    loop = asyncio.new_event_loop()
    try:
        for frame in frames:
            # See the docstring: pin the wall clock forward so no boundary fires mid-run.
            session.last_agg_publish_ts = _wall_clock_now()
            try:
                loop.run_until_complete(
                    processor.process(
                        data=frame.pixel_detections(resolution),
                        config=config,
                        stream_key=stream_key,
                        stream_info=raw_stream_info,
                    )
                )
            except Exception as exc:
                run.error = (
                    f"legacy process() raised on frame {frame.index}: "
                    f"{type(exc).__name__}: {exc}"
                )
                break
            run.frames_processed += 1
        if not run.error:
            forced = session.maybe_publish_results_agg(
                raw_stream_info,
                usecase=usecase,
                app_name=usecase,
                publisher=collector,
                force=True,
            )
            if not forced:
                run.notes.append(
                    "the forced legacy results-agg publish returned False. "
                    "maybe_publish_results_agg refuses when the profile declares no "
                    "volume_metrics, or when no frame carried tracking_stats "
                    "(session.saw_tracking is still False) -- an incident-only app has no "
                    "window to roll up."
                )
    finally:
        try:
            loop.close()
        except Exception:  # a loop that will not close is not a finding
            logger.debug("could not close the legacy event loop", exc_info=True)

    run.aggregations = tuple(collector.aggregations)
    run.incidents = tuple(collector.incidents)
    if len(run.aggregations) > 1:
        run.notes.append(
            f"the legacy side published {len(run.aggregations)} windows despite the pinned "
            "clock; comparing the last."
        )
    if not run.aggregations and not run.error:
        run.error = (
            "the legacy side published no results-agg over "
            f"{run.frames_processed} frame(s), so there is nothing to diff against."
        )
    return run


def _wall_clock_now() -> float:
    """Wall-clock seconds, for pinning the legacy accumulator's own ``time.time()`` gate."""
    return time.time()


def _legacy_category_for(usecase: str) -> str:
    """The legacy registry category a use case is registered under.

    ``PostProcessor._parse_config`` needs ``{"usecase": ..., "category": ...}``, and the
    category is not derivable from the name: the catalogue is 140 ``(category, name)``
    pairs across 36 categories.  Looked up rather than guessed, falling back to
    ``"general"`` -- the value ``process_simple`` itself defaults ``people_counting`` to.
    """
    try:
        from matrice_analytics.post_processing.core.base import registry
    except Exception:
        return "general"
    for category, entries in getattr(registry, "_use_cases", {}).items():
        if usecase in entries:
            return str(category)
    return "general"


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------


def compare_usecase(
    legacy_usecase: str,
    manifest_path: str | os.PathLike[str],
    frames: Sequence[SyntheticFrame] | FrameSequence,
    *,
    stream_info: Mapping[str, Any] | None = None,
    resolution: tuple[int, int] = DEFAULT_RESOLUTION,
    tolerance: TolerancePolicy = DEFAULT_TOLERANCE,
    legacy_category: str | None = None,
) -> DiffReport:
    """Feed identical frames to both engines and diff the ``results-agg`` they emit.

    This is the whole gate.  Both engines get the *same* :class:`SyntheticFrame` sequence
    and the *same* untyped ``stream_info``; the only conversion is normalized-to-pixel for
    the legacy side, which is that tree's stated input contract
    (``runtime/post_proc_runner.py``, "bbox contract").

    Args:
        legacy_usecase: The legacy use-case name being retired.
        manifest_path: The new app's folder or ``app.yaml``.
        frames: A :class:`FrameSequence` or any sequence of :class:`SyntheticFrame`.
        stream_info: The untyped worker dict.  Defaults to :func:`default_stream_info`
            with ``application_key_name`` set to ``legacy_usecase``.
        resolution: Source ``(width, height)``.
        tolerance: What may be forgiven.  See
            :class:`~matrice_analytics.engine.migration.differ.TolerancePolicy`.
        legacy_category: The legacy registry category, when the lookup cannot find it.

    Returns:
        A :class:`~matrice_analytics.engine.migration.differ.DiffReport`.
        :attr:`~...DiffReport.passed` is the verdict a wave acts on.
    """
    sequence = frames if isinstance(frames, FrameSequence) else None
    frame_list = tuple(sequence.frames if sequence is not None else frames)
    if not frame_list:
        raise ValueError("compare_usecase needs at least one frame; generate_frames() makes them")
    effective_fps = sequence.fps if sequence is not None else DEFAULT_FPS

    raw_stream_info = dict(
        stream_info
        or default_stream_info(
            application_key_name=legacy_usecase,
            # The legacy publisher prefers its own ``app_name`` over stream_info
            # (``legacy_analytics_bridge.py:1340``), and ``run_legacy`` passes the use-case
            # name -- so naming the app the same thing on both sides keeps a pure label out
            # of the difference list.
            application_name=legacy_usecase,
            fps=effective_fps,
            resolution=resolution,
        )
    )

    new_run, session = run_new_engine(manifest_path, frame_list, stream_info=raw_stream_info)
    manifest = session.manifest
    legacy_run = run_legacy(
        legacy_usecase,
        frame_list,
        stream_info=raw_stream_info,
        resolution=resolution,
        index_to_category=_index_to_category_from_manifest(manifest),
        legacy_category=legacy_category,
    )

    zones = tuple(session.emission_zones)
    context = DiffContext(
        usecase=legacy_usecase,
        app_id=manifest.app.id,
        frames=len(frame_list),
        zoned=zones not in ((), (CANONICAL_GLOBAL_ZONE,)),
        reference_point=_reference_point_of(session),
        legacy_reference_point="box_center",
    )
    notes = [*new_run.notes, *legacy_run.notes]
    if new_run.error:
        notes.append(f"new engine error: {new_run.error}")
    notes.append(
        f"frames={len(frame_list)} span={len(frame_list) / effective_fps:.1f}s "
        f"new_windows={len(new_run.aggregations)} legacy_windows={len(legacy_run.aggregations)}"
    )
    if sequence is not None:
        notes.append(f"frame-sequence digest {sequence.digest[:16]} (determinism anchor)")

    return diff_results_agg(
        legacy_run.window,
        new_run.window,
        context=context,
        tolerance=tolerance,
        legacy_error=legacy_run.error,
        notes=notes,
    )


def _index_to_category_from_manifest(manifest: Any) -> dict[int, str]:
    """``{class_index: model_label}`` for the legacy side, from the new manifest.

    Derived from the manifest rather than hand-written so both engines are told about the
    same classes.  ``model.index_to_category`` wins when the app declares it; otherwise the
    right-hand side of ``entity_mapping`` is enumerated in sorted order, which is
    deterministic and is the only information available.
    """
    declared = getattr(manifest.model, "index_to_category", None) or {}
    if declared:
        return {int(index): str(label) for index, label in declared.items()}
    labels: list[str] = []
    for aliases in manifest.model.entity_mapping.values():
        for alias in aliases:
            if alias not in labels:
                labels.append(alias)
    return dict(enumerate(sorted(labels)))


def _reference_point_of(session: Session) -> str:
    """The session's resolved zone-membership reference point.

    Read through the private attribute because it is resolved once at setup and not
    re-exposed; ``foot_center`` is the documented default
    (``engine/runtime/session.py:_resolve_reference_point``) and is what the
    ``FOOT-CENTER-IS-THE-DEFAULT-REFERENCE-POINT`` deliberate-change predicate keys on.
    """
    return str(getattr(session, "_reference_point", "foot_center"))


def load_frames_from_json(path: str | os.PathLike[str]) -> tuple[SyntheticFrame, ...]:
    """Read a frame sequence back from the JSON :func:`dump_frames_to_json` writes.

    Recorded frames from a real camera are strictly better evidence than synthetic ones;
    this is the seam for them, and it keeps the format one thing.
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(
        SyntheticFrame(
            index=int(entry["index"]),
            frame_ts=float(entry["frame_ts"]),
            detections=tuple(dict(det) for det in entry["detections"]),
            track_ids=tuple(int(value) for value in entry.get("track_ids", ())),
        )
        for entry in payload
    )


def dump_frames_to_json(frames: Sequence[SyntheticFrame], path: str | os.PathLike[str]) -> None:
    """Write a frame sequence to JSON, so a failing wave can archive its exact input."""
    payload = [
        {
            "index": frame.index,
            "frame_ts": frame.frame_ts,
            "detections": list(frame.detections),
            "track_ids": list(frame.track_ids),
        }
        for frame in frames
    ]
    Path(path).write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8"
    )

