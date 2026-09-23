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
"""

import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..core.base import (
    BaseProcessor,
    ConfigProtocol,
    ProcessingContext,
    ProcessingResult,
)
from ..utils import apply_category_mapping
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


class VehicleSpeedEstimationUseCase(BaseProcessor):
    """Measures vehicle speed using a camera recovered from the road's own markings."""

    def __init__(self) -> None:
        super().__init__("vehicle_speed_estimation")
        self.category = "traffic"
        self._cameras: Dict[str, _CameraState] = {}

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
            index = float(fallback_index)
        return index / fps

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
            frame_ts = self._frame_time(stream_info, state.calibrator._frames)

            self._advance_calibration(state, frame, detections, config, width, height)
            measured = self._measure_all(state, detections, config, frame_ts, height)

            context.mark_completed()
            agg_summary = self.create_agg_summary(
                "current_frame",
                self._incidents(state, measured, config, stream_info),
                self._tracking_stats(state, measured, config),
                self._business_analytics(state, measured, config),
                human_text=self._summary(state, measured, config),
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

    def _measure_all(
        self,
        state: _CameraState,
        detections: List[Dict[str, Any]],
        config: VehicleSpeedEstimationConfig,
        frame_ts: float,
        frame_height: int,
    ) -> Dict[int, List[float]]:
        """Project, accumulate and fit. Returns ``{track_id: [speed, over_pct, unc]}``."""
        if state.plane is None:
            return {}
        plane = state.plane
        factor = FACTORS[config.units]
        flag_above = config.speed_limit * (1.0 + config.tolerance)
        seen: set = set()
        live: Dict[int, List[float]] = {}

        for det in detections:
            track_id = det.get("track_id")
            point = self._ground_point(det)
            if track_id is None or point is None:
                continue
            track_id = int(track_id)
            seen.add(track_id)
            # A box pinned to the frame edge has a frozen foot row while the vehicle is
            # still moving, so it is not a position sample at all. Skipping it costs
            # nothing here: the fit uses time baselines, so the next good sample simply
            # pairs over a slightly longer one.
            if point[1] >= frame_height - config.edge_margin_px:
                continue
            ground = plane.project(point[0], point[1])
            if ground is None:
                continue

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

    def _incidents(
        self,
        state: _CameraState,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
        stream_info: Optional[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        flag_above = config.speed_limit * (1.0 + config.tolerance)
        offenders = {t: v for t, v in measured.items() if v[0] > flag_above}
        if not offenders:
            return []
        worst = max(v[1] for v in offenders.values())
        unit = UNIT_LABELS[config.units]
        return [
            {
                "type": "vehicle_speeding",
                "severity": severity_for(worst),
                "count": len(offenders),
                "human_text": (
                    f"Speeding - {len(offenders)} vehicle(s) over the "
                    f"{config.speed_limit:g} {unit} limit, worst {worst:.0f}% over"
                ),
            }
        ]

    def _tracking_stats(
        self,
        state: _CameraState,
        measured: Dict[int, List[float]],
        config: VehicleSpeedEstimationConfig,
    ) -> List[Dict[str, Any]]:
        speeds = [v[0] for v in measured.values()]
        return [
            {
                "calibrated": state.plane is not None,
                "measured_vehicles": len(measured),
                "max_speed": round(max(speeds), 1) if speeds else 0.0,
                "avg_speed": round(sum(speeds) / len(speeds), 1) if speeds else 0.0,
                "speed_unit": UNIT_LABELS[config.units],
                "total_speeding_vehicles": len(state.counted_offenders),
            }
        ]

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
        if state.plane is None:
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
