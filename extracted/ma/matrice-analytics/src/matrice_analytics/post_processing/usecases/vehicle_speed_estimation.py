"""Vehicle speed from a camera that calibrates itself off the road's own markings.

WHY THIS USE CASE NEEDS THE FRAME
    Speed needs a map from pixels to metres on the road, and that map needs the camera's
    geometry. Two perpendicular vanishing points give it. Vehicle motion supplies the
    first; nothing about vehicle motion can supply the second, because an axis-aligned
    detection box carries no direction at all. The second one comes from the painted road
    markings that run ACROSS the carriageway -- a stop line, a zebra crossing, a give-way
    triangle, a turn arrow -- and those are pixels.

    That is the whole reason this lives in py_analytics and takes ``input_bytes``. An
    ml-applications app receives detection boxes only, which is sufficient to measure
    speed once the camera is known and not sufficient to work out what the camera is.

WHAT THE INSTALLER DOES
    Measures how high the camera is, in metres, and sets ``camera_height_m``. That is the
    entire survey. Everything else is read out of the scene while the stream runs: the
    use case watches the road build up a clean background plate, finds the markings, and
    recovers the camera on its own within the first few hundred frames.

    The height cannot be recovered from an image and never will be -- a camera cannot
    tell a road from a scale model of a road. Every speed is exactly linear in it, so ten
    percent wrong there is ten percent wrong on every reading, uniformly, with nothing in
    the output to reveal it.

HOW A SPEED IS READ OFF A TRACK
    Each vehicle's ground contact point is projected onto the road plane, giving the
    distance it has travelled along the road. At constant speed that distance is linear
    in time, so the speed is the slope of a line -- fitted as the median of slopes over
    every earlier sample at least ``min_baseline_seconds`` old.

    Short pairs are excluded rather than down-weighted. Foot-point jitter divided by a
    one-frame interval is amplified by the frame rate; the same jitter over half a second
    is negligible, and there is no information in the short pairs worth salvaging. A
    median, not a least-squares line: when a tracker swaps ids and teleports one sample,
    the median ignores it where least squares would smear it across the fit.

WHEN IT REFUSES
    A camera with no transverse markings in view, or one aimed too nearly along the road
    for the across-road direction to be measurable, cannot be calibrated by this method.
    The use case says so and reports no speed, rather than producing confident numbers
    that are wrong by an unbounded factor. That is not a failure mode to paper over: it
    is the method's honest domain, and a motorway mainline sits outside it.

THE 3D-BOX FALLBACK
    When the detector sends each vehicle's 8 projected 3D-box corners as ``keypoints``
    (UrbanOmniDetect), the use case has a second way to find the camera: every car's
    four ground corners should be a car-sized rectangle on the road, and hundreds of
    them pin down focal length, tilt, roll and height (``utils/speed_box3d_utils.py``).
    Footprints are collected from the first frame; if the road markings have given no
    camera after ``box3d_fallback_after_seconds`` of frame time, or have given up, the
    footprint camera is solved and used. Its reference point is the footprint centre,
    which is on the road by construction. If the markings calibrate later they take over
    -- they need no assumption about car size -- and the tracks restart in their frame.
    ``calibration_method`` in the tracking stats says which one a speed came from.
"""

import re
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..advanced_tracker.rtp_clock import RtpClock
from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..utils import apply_category_mapping
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory
from ..utils.speed_box3d_utils import Box3DFallback
from ..utils.speed_fit_utils import (
    baseline_slope,
    over_limit_pct,
    severity_for,
    uncertainty_pct,
)
from ..utils.speed_geometry_utils import RoadPlane
from ..utils.speed_paint_calibration_utils import SelfCalibrator
from .vehicle_speed_estimation_config import (
    FACTORS,
    UNIT_LABELS,
    VEHICLE_SPEED_ESTIMATION_SCHEMA,
    VehicleSpeedEstimationConfig,
)

#: ``stream_info`` keys carrying the frame's raw 90 kHz RTP timestamp, in the order the
#: tracker adapter reads them. ``rtp_number`` is the key ``build_stream_info`` emits.
_RTP_KEYS = ("rtp_timestamp", "rtp_ts", "rtp_number")
#: RTP keys where ``0`` means "not stamped" rather than tick zero: the canonical builder
#: writes ``rtp_number`` as ``""`` when the worker had none, and some producers send ``0``.
_RTP_ZERO_IS_ABSENT = frozenset({"rtp_number"})
#: The frame counter at the end of a worker frame id ("shm_<camera>_<n>"). Only after an
#: underscore, so the digits a hex id happens to end in are never read as a counter.
_FRAME_COUNTER = re.compile(r"_(\d+)$")

#: ``incident_type`` of the speeding incident. The IncidentManager keys its default
#: severity thresholds on it (``SPEEDING_DEFAULT_THRESHOLDS``).
INCIDENT_TYPE = "vehicle_speed_estimation"
#: ``severity_for`` grades in "high"; the IncidentManager's word for that rung is
#: "significant".
_MANAGER_LEVELS = {"high": "significant"}
#: A track id unseen for this long (frame-clock seconds) is forgotten, and counts as a
#: new vehicle if it comes back. Bounds the per-camera id memory on a busy road.
_TRACK_MEMORY_SECONDS = 60.0
_DEFAULT_CAMERA_ID = "camera"


def _resolve_manager_camera_id(stream_info: Optional[Dict[str, Any]]) -> str:
    """Resolve the camera key used by IncidentManager state tracking."""
    if not stream_info:
        return _DEFAULT_CAMERA_ID
    inp = stream_info.get("input_settings")
    if not isinstance(inp, dict):
        inp = {}
    camera_info = stream_info.get("camera_info")
    if not isinstance(camera_info, dict):
        camera_info = {}
    camera_id = (
        stream_info.get("camera_id")
        or inp.get("camera_id")
        or camera_info.get("camera_id")
        or stream_info.get("stream_key")
    )
    return str(camera_id) if camera_id else _DEFAULT_CAMERA_ID


class _CameraState:
    """Everything remembered about one camera: its calibration, and its live tracks."""

    def __init__(self, calibrator: SelfCalibrator) -> None:
        self.calibrator = calibrator
        self.plane: Optional[RoadPlane] = None
        #: track id -> [[t, along_m, across_m], ...]
        self.trajectories: Dict[int, List[List[float]]] = {}
        #: track id -> [speed, over_limit_pct, uncertainty_pct]
        self.speeds: Dict[int, List[float]] = {}
        self.counted_offenders: set = set()
        self.reported_block = False
        #: The 3D-box fallback: None when disabled in the config.
        self.box3d: Optional[Box3DFallback] = None
        #: Which calibration the current trajectories were measured in.
        self.method: Optional[str] = None
        #: Frames this camera has processed. The frame clock's fallback when the
        #: stream carries neither an RTP stamp nor a frame counter in its frame id; it
        #: advances on every frame, calibrated or not, so time keeps moving after
        #: calibration stops feeding the calibrator.
        self.frames_seen = 0
        #: The frame clock's reading on the last unstamped frame, to catch it going back.
        self.frame_seconds: Optional[float] = None
        #: The camera's RTP clock, and the seconds it gave the last stamped frame.
        self.rtp_clock = RtpClock()
        self.rtp_seconds = 0.0
        #: Which clock the current trajectories were timed on: "rtp" or "frame".
        self.clock: Optional[str] = None
        #: track id -> frame time it was last seen, for the new-vehicle counts. Ids
        #: unseen for ``_TRACK_MEMORY_SECONDS`` are dropped.
        self.last_seen: Dict[int, float] = {}
        #: Unique vehicles per class since the stream started.
        self.total_by_class: Dict[str, int] = {}


class VehicleSpeedEstimationUseCase(BaseProcessor):
    """Measures vehicle speed using a camera recovered from the road's own markings."""

    _INCIDENT_LOG = "[INCIDENT_MANAGER]"

    def __init__(self) -> None:
        super().__init__("vehicle_speed_estimation")
        self.category = "traffic"
        self._cameras: Dict[str, _CameraState] = {}
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized = False

    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for vehicle speed estimation."""
        return VEHICLE_SPEED_ESTIMATION_SCHEMA

    def _resolve_frame(self, input_bytes: Any) -> Optional[np.ndarray]:
        """Resolve the pipeline's frame payload to a BGR array, or ``None``.

        Mirrors the forms license plate monitoring already accepts, so a worker that
        feeds one use case can feed this one unchanged: an array straight through, the
        ``__RAW_BGR__`` sentinel, or encoded bytes to decode.
        """
        import cv2  # noqa: PLC0415  (kept off the module import path; see the guide)

        if input_bytes is None:
            return None
        if isinstance(input_bytes, np.ndarray):
            return input_bytes
        if input_bytes == b"__RAW_BGR__":
            return None
        return cv2.imdecode(np.frombuffer(input_bytes, np.uint8), cv2.IMREAD_COLOR)

    @staticmethod
    def _frame_time(stream_info: Optional[Dict[str, Any]], fallback_index: int) -> float:
        """Seconds on the FRAME clock, never the wall clock.

        A replayed clip must produce the same speeds as the live run that produced it,
        and inference or queueing latency must never enter a measurement. Both rule out
        ``time.time()``. Falls back to a frame counter over an assumed frame rate when the
        stream does not say -- which keeps relative timing correct even if absolute time
        is unknown, and that is all a slope needs.
        """
        settings = (stream_info or {}).get("input_settings") or {}
        fps = float(settings.get("original_fps") or 0.0) or 25.0
        frame_id = (stream_info or {}).get("frame_id")
        if frame_id is None:
            frame_id = settings.get("start_frame")
        try:
            index = float(frame_id)
        except (TypeError, ValueError):
            # The worker's SHM ids end in the camera's frame counter: "shm_cam_c56e_5871".
            # That counter keeps its spacing when frames are dropped before analytics,
            # which a count of the frames seen here does not.
            counter = _FRAME_COUNTER.search(str(frame_id)) if frame_id is not None else None
            index = float(counter.group(1)) if counter else float(fallback_index)
        return index / fps

    @staticmethod
    def _rtp_ticks(stream_info: Optional[Dict[str, Any]]) -> Optional[int]:
        """The frame's raw RTP timestamp, or ``None`` when the stream did not stamp one."""
        info = stream_info or {}
        for key in _RTP_KEYS:
            raw = info.get(key)
            if raw is None or raw == "":
                continue
            try:
                ticks = int(raw)
            except (TypeError, ValueError):
                return None
            if ticks == 0 and key in _RTP_ZERO_IS_ABSENT:
                continue
            return ticks
        return None

    def _frame_seconds(self, state: _CameraState, stream_info: Optional[Dict[str, Any]]) -> float:
        """This frame's time on the camera's clock: RTP when stamped, else the frame clock.

        RTP comes first because it is the only clock that survives frame sampling. A
        stream sampled down before it arrives here still carries the source's 90 kHz
        stamps, while a frame count over an assumed frame rate runs fast by the sampling
        factor and inflates every speed by that same factor. A change of clock, or an RTP
        jump backwards, restarts every track: samples on two time bases share no slope.
        """
        ticks = self._rtp_ticks(stream_info)
        seconds = state.rtp_clock.to_seconds(ticks) if ticks is not None else None
        source = "frame" if ticks is None else "rtp"
        if source != state.clock or (ticks is not None and seconds is None):
            state.trajectories.clear()
            state.speeds.clear()
            state.clock = source
        if ticks is None:
            frame_seconds = self._frame_time(stream_info, state.frames_seen)
            if state.frame_seconds is not None and frame_seconds < state.frame_seconds:
                # The frame counter went back (source restart, looping file): same rule
                # as a backward RTP jump.
                state.trajectories.clear()
                state.speeds.clear()
            state.frame_seconds = frame_seconds
            return frame_seconds
        if seconds is not None:
            state.rtp_seconds = seconds
        # After a backward jump the clock re-bases on this frame without moving its
        # total, so the last stamped time is this frame's time on the continued clock.
        return state.rtp_seconds

    # ---------------------------------------------------------------- process

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """Measure speed for every tracked vehicle in this frame."""
        start = time.monotonic()
        try:
            if not isinstance(config, VehicleSpeedEstimationConfig):
                return self.create_error_result(
                    "Invalid configuration type for vehicle speed estimation",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )
            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)
            if context is None:
                context = ProcessingContext()

            frame = self._resolve_frame(input_bytes)
            if frame is None:
                # A hard error, not a quiet zero. Without the frame this use case cannot
                # work out the camera, so it cannot produce a speed -- and a speed of 0
                # on a busy road is indistinguishable from a quiet one. Note that the
                # decoupled analytics node never supplies input_bytes; this use case
                # requires the coupled flow.
                return self.create_error_result(
                    "input_bytes (the frame) is required for vehicle speed estimation: "
                    "the camera geometry is recovered from road markings in the image. "
                    "This use case runs only where the worker supplies frames.",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            camera_id = str((stream_info or {}).get("stream_key") or "default_stream")
            state = self._camera(camera_id, config)
            height, width = frame.shape[:2]

            detections = self._prepare(data, config)
            frame_ts = self._frame_seconds(state, stream_info)
            state.frames_seen += 1

            self._advance_calibration(state, frame, detections, config, width, height)
            self._advance_box3d(state, detections, frame_ts, width, height)
            measured = self._measure_all(state, detections, config, frame_ts, width, height)
            counts = self._count_vehicles(state, detections, config, frame_ts)

            # Every frame, {} included: the manager closes an incident on empty frames.
            incident = self._incident(measured, config, stream_info)
            self._send_incident_to_manager(incident, stream_info, context=context)

            context.mark_completed()
            agg_summary = self.create_agg_summary(
                "current_frame",
                None,
                None,
                self._business_analytics(state, measured, config),
                human_text=self._summary(state, measured, config),
            )
            agg_summary["current_frame"]["incidents"] = incident
            # A dict, as ``create_tracking_stats`` builds it for every other use case: the
            # worker reads ``tracking_stats["detections"]`` to normalise their boxes, and a
            # list there raised on every frame and dropped the whole published result.
            agg_summary["current_frame"]["tracking_stats"] = self._tracking_stats(
                state, measured, config, detections, counts
            )
            self.logger.debug(
                "vehicle_speed_estimation camera=%s frame_ms=%.1f measured=%d",
                camera_id,
                (time.monotonic() - start) * 1000.0,
                len(measured),
            )
            return self.create_result(
                data={"agg_summary": agg_summary},
                usecase=self.name,
                category=self.category,
                context=context,
            )
        except Exception as e:  # noqa: BLE001 - reported as an error result, never swallowed
            self.logger.error("Vehicle speed estimation failed: %s", e, exc_info=True)
            if context:
                context.mark_completed()
            return self.create_error_result(
                str(e),
                type(e).__name__,
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ------------------------------------------------------------- internals

    def _camera(self, camera_id: str, config: VehicleSpeedEstimationConfig) -> _CameraState:
        state = self._cameras.get(camera_id)
        if state is None:
            state = _CameraState(
                SelfCalibrator(
                    min_frames=config.calibration_min_frames,
                    min_tracks=config.calibration_min_tracks,
                    retry_interval_frames=config.calibration_retry_frames,
                    max_attempts=config.calibration_max_attempts,
                    max_vp2_diagonals=config.max_vp2_diagonals,
                    max_f_sensitivity_pct=config.max_f_sensitivity_pct,
                )
            )
            if config.box3d_fallback_enabled:
                state.box3d = Box3DFallback(
                    after_seconds=config.box3d_fallback_after_seconds,
                    ground_indices=config.box3d_ground_indices,
                    categories=config.box3d_calibration_categories,
                    car_length_m=config.box3d_car_length_m,
                    car_width_m=config.box3d_car_width_m,
                    init_height_m=config.camera_height_m,
                    min_footprints=config.box3d_min_footprints,
                    min_tracks=config.box3d_min_tracks,
                    min_corner_conf=config.box3d_min_corner_conf,
                    min_size_px=config.box3d_min_footprint_px,
                )
            self._cameras[camera_id] = state
        return state

    def _prepare(self, data: Any, config: VehicleSpeedEstimationConfig) -> List[Dict[str, Any]]:
        """Confidence filter, category mapping and target filter, in that order."""
        detections = data if isinstance(data, list) else []
        if config.confidence_threshold is not None:
            detections = [
                d for d in detections if d.get("confidence", 0) >= config.confidence_threshold
            ]
        # getattr, not attribute access: `index_to_category` is an optional field that
        # BaseConfig does not define, so a config built without one has no such attribute
        # at all. The template use case reads it directly and would raise here.
        index_to_category = getattr(config, "index_to_category", None)
        if index_to_category:
            detections = apply_category_mapping(detections, index_to_category)
        if config.target_categories:
            detections = [d for d in detections if d.get("category") in config.target_categories]
        return detections

    @staticmethod
    def _ground_point(det: Dict[str, Any]) -> Optional[Tuple[float, float]]:
        """Bottom-centre of the box, in pixels: where the vehicle meets the road.

        The road is a plane, so only points ON it project correctly. A box centre floats
        with vehicle height and lands further away than the vehicle really is, by an
        amount that grows with height -- which makes a bus read faster than the car
        beside it.
        """
        box = det.get("bounding_box") or det.get("bbox")
        if isinstance(box, dict):
            xmin = box.get("xmin", box.get("x1"))
            xmax = box.get("xmax", box.get("x2"))
            ymax = box.get("ymax", box.get("y2"))
        elif isinstance(box, (list, tuple)) and len(box) >= 4:
            xmin, _, xmax, ymax = box[0], box[1], box[2], box[3]
        else:
            return None
        if xmin is None or xmax is None or ymax is None:
            return None
        return (float(xmin) + float(xmax)) / 2.0, float(ymax)

    def _advance_calibration(
        self,
        state: _CameraState,
        frame: np.ndarray,
        detections: List[Dict[str, Any]],
        config: VehicleSpeedEstimationConfig,
        width: int,
        height: int,
    ) -> None:
        """Feed the calibrator, and build the road plane the moment it succeeds."""
        if state.plane is not None or state.calibrator.done:
            return
        state.calibrator.observe_frame(frame)
        for det in detections:
            track_id = det.get("track_id")
            point = self._ground_point(det)
            if track_id is not None and point is not None:
                state.calibrator.observe_track(int(track_id), point[0], point[1])

        if not state.calibrator.ready():
            return
        result = state.calibrator.attempt(width, height)
        if result.ok and result.vp1 and result.vp2 and result.focal:
            state.plane = RoadPlane(
                (width / 2.0, height / 2.0),
                result.focal,
                result.vp1,
                result.vp2,
                config.camera_height_m,
            )
            self.logger.info(
                "vehicle_speed_estimation: camera calibrated from road markings (%s)",
                ", ".join(f"{k}={v:.0f}" for k, v in sorted(result.diagnostics.items())),
            )
        elif result.permanent and not state.reported_block:
            state.reported_block = True
            self.logger.error(
                "vehicle_speed_estimation: this camera cannot be calibrated by road "
                "markings and will report no speeds. %s",
                result.reason,
            )

    def _advance_box3d(
        self,
        state: _CameraState,
        detections: List[Dict[str, Any]],
        frame_ts: float,
        width: int,
        height: int,
    ) -> None:
        """Feed the 3D-box fallback; it solves once the paint has had its chance."""
        if state.box3d is None or state.plane is not None:
            return
        if state.box3d.observe(detections, frame_ts, width, height, state.calibrator.failed):
            result = state.box3d.result
            self.logger.info(
                "vehicle_speed_estimation: road markings gave no camera; calibrated from "
                "vehicle 3D-box footprints instead (%s)",
                ", ".join(f"{k}={v:.2f}" for k, v in sorted(result.diagnostics.items()))
                if result is not None
                else "",
            )

    def _active_plane(self, state: _CameraState) -> Tuple[Any, Optional[str]]:
        """The camera to measure with, and its method. Road markings win when both exist."""
        if state.plane is not None:
            return state.plane, "road_markings"
        if state.box3d is not None and state.box3d.plane is not None:
            return state.box3d.plane, "box3d"
        return None, None

    def _sample(
        self,
        state: _CameraState,
        method: str,
        det: Dict[str, Any],
        config: VehicleSpeedEstimationConfig,
        width: int,
        height: int,
    ) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """``(pixel, (along, across))`` for one detection under ``method``, or ``None``."""
        if method == "box3d" and state.box3d is not None:
            return state.box3d.locate(det, width, height)
        point = self._ground_point(det)
        if point is None:
            return None
        # A box pinned to the frame edge has a frozen foot row while the vehicle is
        # still moving, so it is not a position sample at all. Skipping it costs
        # nothing here: the fit uses time baselines, so the next good sample simply
        # pairs over a slightly longer one.
        if point[1] >= height - config.edge_margin_px:
            return None
        ground = state.plane.project(point[0], point[1]) if state.plane is not None else None
        return None if ground is None else (point, ground)

    def _measure_all(
        self,
        state: _CameraState,
        detections: List[Dict[str, Any]],
        config: VehicleSpeedEstimationConfig,
        frame_ts: float,
        frame_width: int,
        frame_height: int,
    ) -> Dict[int, List[float]]:
        """Project, accumulate and fit. Returns ``{track_id: [speed, over_pct, unc]}``."""
        plane, method = self._active_plane(state)
        if method != state.method:
            # A new camera means a new road frame: positions measured in the old one
            # cannot share a slope with the new, so every track restarts.
            state.trajectories.clear()
            state.speeds.clear()
            state.method = method
        if plane is None or method is None:
            return {}
        factor = FACTORS[config.units]
        flag_above = config.speed_limit * (1.0 + config.tolerance)
        seen: set = set()
        live: Dict[int, List[float]] = {}

        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                continue
            track_id = int(track_id)
            seen.add(track_id)
            sample = self._sample(state, method, det, config, frame_width, frame_height)
            if sample is None:
                continue
            point, ground = sample

            window = state.trajectories.get(track_id, [])
            window = [*window, [frame_ts, ground[0], ground[1]]][-config.window_samples :]
            state.trajectories[track_id] = window
            if len(window) < config.min_samples:
                continue
            slope = baseline_slope(window, config.min_baseline_seconds)
            if slope is None:
                continue
            reading = abs(slope) * factor
            if reading > config.max_plausible_speed:
                continue
            speed = round(reading, 1)
            state.speeds[track_id] = [
                speed,
                round(over_limit_pct(speed, config.speed_limit), 1),
                uncertainty_pct(window, point, plane, config.jitter_px),
            ]

        for track_id in seen:
            if track_id in state.speeds:
                live[track_id] = state.speeds[track_id]
        # Trajectories are per vehicle and would otherwise grow for the life of the
        # stream. A track absent for one frame has ended as far as this can tell; a
        # reused id starts fresh, which is correct, since pairing across the gap would
        # fit a slope through two unrelated vehicles.
        state.trajectories = {t: w for t, w in state.trajectories.items() if t in seen}
        state.counted_offenders |= {t for t, v in live.items() if v[0] > flag_above}
        return live

    # ------------------------------------------------------------ components

    def _incident(
        self,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """This frame's speeding incident for the IncidentManager, or ``{}`` for none.

        ``incident_quant`` is the worst overage in percent, capped at 100: the manager
        grades it (``SPEEDING_DEFAULT_THRESHOLDS``: 25 / 50 / 100 % over, the same rungs
        as ``severity_for``), confirms it over consecutive frames, and owns the incident
        id, start and end times.
        """
        flag_above = config.speed_limit * (1.0 + config.tolerance)
        offenders = {t: v for t, v in measured.items() if v[0] > flag_above}
        if not offenders:
            return {}
        worst = max(v[1] for v in offenders.values())
        unit = UNIT_LABELS[config.units]
        level = severity_for(worst)
        camera_info = (stream_info or {}).get("camera_info")
        incident = self.create_incident(
            incident_id=f"incident_{INCIDENT_TYPE}_1",
            incident_type=INCIDENT_TYPE,
            severity_level=_MANAGER_LEVELS.get(level, level),
            human_text=(
                f"Speeding - {len(offenders)} vehicle(s) over the "
                f"{config.speed_limit:g} {unit} limit, worst {worst:.0f}% over"
            ),
            camera_info=camera_info if isinstance(camera_info, dict) else None,
            end_time="Incident still active",
        )
        incident.update(
            incident_quant=round(min(worst, 100.0), 1),
            speeding_vehicles=len(offenders),
            max_over_limit_pct=round(worst, 1),
        )
        return incident

    def _initialize_incident_manager_once(self, config: VehicleSpeedEstimationConfig) -> None:
        if self._incident_manager_initialized:
            return
        try:
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            if self._incident_manager is None:
                self.logger.warning(
                    "%s Incident manager unavailable; speeding incidents will not be published",
                    self._INCIDENT_LOG,
                )
        except Exception as e:  # noqa: BLE001 - logged; the use case runs without incidents
            self.logger.error(
                "%s Incident manager init failed: %s", self._INCIDENT_LOG, e, exc_info=True
            )
        finally:
            self._incident_manager_initialized = True

    def _send_incident_to_manager(
        self,
        incident: Dict[str, Any],
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
    ) -> None:
        """Feed the manager every frame -- ``{}`` included, so it can close the incident."""
        camera_id = _resolve_manager_camera_id(stream_info)
        if self._incident_manager:
            try:
                published = self._incident_manager.process_incident(
                    camera_id=camera_id,
                    incident_data=incident or {},
                    stream_info=stream_info,
                )
                if published:
                    self.logger.info(
                        "%s Incident published for camera: %s", self._INCIDENT_LOG, camera_id
                    )
            except Exception as e:  # noqa: BLE001 - logged; one bad publish must not drop the frame
                self.logger.error(
                    "%s Error publishing incident: %s", self._INCIDENT_LOG, e, exc_info=True
                )
        if context is not None:
            # When the manager is active it owns incident_res; the PostProcessor bridge
            # must not publish the same incident again from agg_summary.
            context.metadata["incident_published_via_manager"] = bool(self._incident_manager)

    @staticmethod
    def _count_vehicles(
        state: _CameraState,
        detections: List[Dict[str, Any]],
        config: VehicleSpeedEstimationConfig,
        frame_ts: float,
    ) -> Dict[str, Dict[str, int]]:
        """Per-class ``current`` / ``new`` / ``total`` vehicle counts for this frame.

        A vehicle is new the first frame its track id appears, or when the id comes back
        after ``_TRACK_MEMORY_SECONDS`` away (the tracker reused it).
        """
        current = {c: 0 for c in config.target_categories}
        new = {c: 0 for c in config.target_categories}
        for det in detections:
            category = str(det.get("category", ""))
            current[category] = current.get(category, 0) + 1
            track_id = det.get("track_id")
            if track_id is None:
                continue
            last = state.last_seen.get(int(track_id))
            if last is None or not 0.0 <= frame_ts - last <= _TRACK_MEMORY_SECONDS:
                new[category] = new.get(category, 0) + 1
                state.total_by_class[category] = state.total_by_class.get(category, 0) + 1
            state.last_seen[int(track_id)] = frame_ts
        state.last_seen = {
            t: seen
            for t, seen in state.last_seen.items()
            if 0.0 <= frame_ts - seen <= _TRACK_MEMORY_SECONDS
        }
        total = {c: state.total_by_class.get(c, 0) for c in current}
        return {"current": current, "new": new, "total": total}

    def _tracking_stats(
        self,
        state: _CameraState,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
        detections: List[Dict[str, Any]],
        counts: Optional[Dict[str, Dict[str, int]]] = None,
    ) -> Dict[str, Any]:
        speeds = [v[0] for v in measured.values()]
        unit = UNIT_LABELS[config.units]
        flag_above = config.speed_limit * (1.0 + config.tolerance)
        counts = counts or {"current": {}, "new": {}, "total": {}}

        def as_list(by_class: Dict[str, int]) -> List[Dict[str, Any]]:
            return [{"category": c, "count": n} for c, n in by_class.items()]

        return {
            # The legacy analytics bridge's count lists (results-agg tracking_stats).
            "current_counts": as_list(counts["current"]),
            "current_new_counts": as_list(counts["new"]),
            "total_counts": as_list(counts["total"]),
            # What the bridge's SAFETY metrics are built from: every vehicle measured
            # this frame, and whether it is over the limit (with the tolerance).
            "speed_analytics": {
                "frame_vehicles": [
                    {
                        "track_id": track_id,
                        "speed": v[0],
                        "over_limit_pct": v[1],
                        "speeding": bool(v[0] > flag_above),
                    }
                    for track_id, v in measured.items()
                ],
                "speed_limit": config.speed_limit,
                "speed_unit": unit,
            },
            "calibrated": state.method is not None,
            "calibration_method": state.method,
            "measured_vehicles": len(measured),
            "max_speed": round(max(speeds), 1) if speeds else 0.0,
            "avg_speed": round(sum(speeds) / len(speeds), 1) if speeds else 0.0,
            "speed_unit": unit,
            "total_speeding_vehicles": len(state.counted_offenders),
            "detections": self._speed_detections(
                measured, detections, unit, config.label_with_speed
            ),
        }

    def _speed_detections(
        self,
        measured: Dict[int, List[float]],
        detections: List[Dict[str, Any]],
        unit: str,
        label_with_speed: bool = True,
    ) -> List[Dict[str, Any]]:
        """One entry per vehicle with a speed this frame, keyed by ``track_id``.

        The box is the vehicle's whole-body 2D box when the producer sent one as
        ``bbox_2d`` (ml-codebases hands this use case the ground footprint as
        ``bounding_box``), so a frontend drawing these boxes draws the vehicle.

        With ``label_with_speed`` the label carries the reading ("car 127 km/h"), so a
        frontend drawing it shows the speed with no change of its own; the plain class
        stays in ``base_category`` for anything that groups or counts by class.
        """
        out: List[Dict[str, Any]] = []
        for det in detections:
            track_id = det.get("track_id")
            if track_id is None or int(track_id) not in measured:
                continue
            speed, over_pct, unc_pct = measured[int(track_id)]
            base_category = str(det.get("category", ""))
            label = f"{base_category} {speed:.0f} {unit}" if label_with_speed else base_category
            entry = self.create_detection_object(
                label,
                det.get("bbox_2d") or det.get("bounding_box") or {},
                track_id=int(track_id),
            )
            entry.update(
                base_category=base_category,
                speed=speed,
                speed_unit=unit,
                over_limit_pct=over_pct,
                uncertainty_pct=unc_pct,
            )
            out.append(entry)
        return out

    def _business_analytics(
        self,
        state: _CameraState,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
    ) -> List[Dict[str, Any]]:
        overages = [v[1] for v in measured.values()]
        return [
            {
                "max_over_limit_pct": round(max(overages), 1) if overages else 0.0,
                "speeding_vehicles": len(state.counted_offenders),
            }
        ]

    def _summary(
        self,
        state: _CameraState,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
    ) -> str:
        if state.method is None:
            box3d = state.box3d
            # Only once footprints have actually arrived: a detector without 3D corners
            # would otherwise be told "calibrating" forever.
            if box3d is not None and box3d.triggered and box3d.footprints_seen:
                why = f" ({box3d.result.reason})" if box3d.result is not None else ""
                return f"Calibrating from vehicle 3D boxes; no speeds yet{why}"
            result = state.calibrator.result
            if result is not None and result.permanent:
                return f"Speed unavailable on this camera: {result.reason}"
            return "Calibrating from road markings; no speeds yet"
        if not measured:
            return "No vehicle speeds measured in this frame"
        unit = UNIT_LABELS[config.units]
        speeds = [v[0] for v in measured.values()]
        return (
            f"{len(measured)} vehicle(s) measured, max {max(speeds):.0f} {unit}, "
            f"average {sum(speeds) / len(speeds):.0f} {unit}"
        )
