from typing import Any, Dict, List, Optional
import time

# Core processing abstractions used by all processors
from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)

# Shared config objects
from ..core.config import BaseConfig, ZoneConfig, AlertConfig

# Generic utilities for detection filtering and geometry
from ..utils import (
    filter_by_confidence,
    match_results_structure,
    point_in_polygon,
    get_bbox_center,
    get_bbox_bottom25_center,
)

# Tailgating-specific runtime and geometry helpers
from ..utils.tailgating_utils import (
    DoorRuntime,
    CrossingRecord,
    AccessEventManager,
    analyze_passage,
    detect_crossing,
    compute_entry_normal,
    motion_vector,
    signed_distance,
    segment_intersects_line,
)

# ============================================================
# CONFIG
# ============================================================


class TailgatingConfig(BaseConfig):
    """
    Configuration container for tailgating detection.

    Holds thresholds, zones, and timing parameters controlling
    event grouping and follower detection.
    """

    def __init__(
        self,
        usecase: str = "tailgating_detection",
        category: str = "security",
        confidence_threshold: float = 0.5,
        target_categories: Optional[List[str]] = None,
        zones: Optional[Dict[str, ZoneConfig]] = None,
        access_window_sec: float = 5.0,
        silence_timeout_sec: float = 2.0,
        cooldown_sec: float = 4.0,
        allowed_persons_per_event: int = 1,
        max_follow_time_delta_sec: float = 3,
        alert_config: Optional[AlertConfig] = None,
        **kwargs,
    ):
        # Initialize shared base config fields
        super().__init__(usecase=usecase, category=category, **kwargs)

        # Detection filtering threshold
        self.confidence_threshold = confidence_threshold

        # Categories to consider as people
        self.target_categories = target_categories or ["person"]

        # Door zones configuration
        self.zones = zones or {}

        # Event grouping parameters
        self.access_window_sec = access_window_sec      # event open window
        self.silence_timeout_sec = silence_timeout_sec  # inactivity closing delay
        self.cooldown_sec = cooldown_sec                # cooldown after event

        # Tailgating rules
        self.allowed_persons_per_event = allowed_persons_per_event
        self.max_follow_time_delta_sec = max_follow_time_delta_sec

        # Optional alert configuration
        self.alert_config = alert_config

        # Memory helpers (currently unused externally)
        self._recent_crossings = {}      # track_id → frame number
        self._cross_memory_frames = 30   # ~1 second memory



# ============================================================
# USE CASE
# ============================================================


class TailgatingDetectionUseCase(BaseProcessor):
    """
    Main processor implementing tailgating detection.

    Tracks crossings across configured doors and groups them into
    events, then detects followers.
    """

    def __init__(self):
        super().__init__("tailgating_detection")
        self.category = "security"

        # Runtime state per door
        self._door_states: Dict[str, DoorRuntime] = {}

        # Last known positions per track
        self._last_positions: Dict[tuple, tuple] = {}

        # Prevent duplicate crossing detection per frame
        self._crossing_latch: Dict[tuple, bool] = {}

        # Backend-facing events accumulated during processing
        self._pending_events: List[Dict[str, Any]] = []

        # Manager handling door event lifecycle
        self.event_manager = AccessEventManager()

        # Recently detected crossings memory
        self._recent_crossings = {}

        # Frames to remember crossing (~3 seconds at 30 FPS)
        self._cross_memory_frames = 90


    # ========================================================
    # TEMPLATE REQUIRED
    # ========================================================

    def create_default_config(self, **overrides):
        """Return default config template."""
        defaults = {
            "usecase": self.name,
            "category": self.category,
            "confidence_threshold": 0.5,
        }
        defaults.update(overrides)
        return TailgatingConfig(**defaults)

    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Any] = None,
    ) -> ProcessingResult:
        """
        Entry point for processor execution.
        Routes data to frame or multi-frame processing.
        """

        # Validate config type
        if not isinstance(config, TailgatingConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Prepare processing context
        context = context or ProcessingContext()
        context.input_format = match_results_structure(data)

        # Decide single vs multi-frame path
        is_multi_frame = self.detect_frame_structure(data)

        if is_multi_frame:
            agg_summary = self._process_multi_frame(data, config, stream_info)
        else:
            agg_summary = self._process_single_frame(data, config, stream_info)

        context.mark_completed()

        # Package results
        result = self.create_result(
            data={
                "agg_summary": agg_summary,
                "events": self._pending_events,
            },
            usecase=self.name,
            category=self.category,
            context=context,
        )

        # Clear events buffer
        self._pending_events = []

        return result

    # ========================================================
    # FRAME ROUTING
    # ========================================================

    def _process_single_frame(self, data, config, stream_info):
        """Process a single frame."""

        # Normalize frame id
        frame_id = int(stream_info.get("frame_number", 0))

        (
            incidents,
            tracking_stats,
            business_analytics,
            summary,
            alerts,
        ) = self._process_frame_detections(
            data,
            config,
            frame_id,
            stream_info,
        )

        # Create standardized agg_summary output
        return self.create_agg_summary(
            frame_id,
            incidents,
            tracking_stats,
            business_analytics,
            alerts=alerts,
            human_text=summary,
        )

    def _process_multi_frame(self, data, config, stream_info):
        """Process multiple frames batch."""

        frame_incidents = {}
        frame_tracking_stats = {}
        frame_business_analytics = {}
        frame_human_text = {}

        for frame_id, frame_data in data.items():
            incidents, tracking_stats, business_analytics, summary = (
                self._process_frame_detections(
                    frame_data, config, str(frame_id), stream_info
                )
            )

            if incidents:
                frame_incidents[str(frame_id)] = incidents
            if summary:
                frame_human_text[str(frame_id)] = summary

        return self.create_frame_wise_agg_summary(
            frame_incidents,
            frame_tracking_stats,
            frame_business_analytics,
            frame_human_text=frame_human_text,
        )

    # ========================================================
    # CORE LOGIC
    # ========================================================

    def _process_frame_detections(
        self,
        detections,
        config,
        frame_id,
        stream_info,
    ):
        """
        Core detection loop:
        - filter detections
        - detect crossings
        - manage events
        - produce alerts/incidents
        """

        # Remove expired crossing memory
        expired = [
            key for key, f in self._recent_crossings.items()
            if frame_id - f > self._cross_memory_frames
        ]
        for key in expired:
            del self._recent_crossings[key]

        # Guard against memory growth
        if len(self._last_positions) > 5000:
            self._last_positions.clear()

        # Confidence filtering
        detections = filter_by_confidence(
            detections,
            config.confidence_threshold,
        )

        # Determine timestamp
        now_ts = (
            stream_info.get("video_ts")
            if stream_info and "video_ts" in stream_info
            else time.time()
        )

        analyses = []

        # Process each configured door
        for door_id, zone_cfg in config.zones.items():

            door = self._get_or_create_door_state(door_id, zone_cfg)

            line_p1, line_p2 = zone_cfg.zones["access_line"]
            secured_zone = zone_cfg.zones["secured_zone"]

            frame_had_crossing = False

            # Process detections
            for det in detections:

                track_id = det.get("track_id")
                if track_id is None:
                    continue

                key = (door_id, track_id)

                # Use foot location for crossing logic
                foot = get_bbox_bottom25_center(det["bounding_box"])

                prev = self._last_positions.get(key)
                self._last_positions[key] = foot

                if prev is None:
                    continue

                # Detect line crossing
                crossed = detect_crossing(
                    prev,
                    foot,
                    line_p1,
                    line_p2,
                    secured_zone,
                )

                # Prevent duplicate triggers in same frame
                last_cross_frame = self._crossing_latch.get(key)
                if last_cross_frame == frame_id:
                    continue

                if not crossed:
                    continue

                frame_had_crossing = True

                # Store crossing memory
                self._crossing_latch[key] = frame_id
                self._recent_crossings[key] = frame_id

                crossing = CrossingRecord(
                    track_id=track_id,
                    timestamp=now_ts,
                )

                # Pass crossing to event manager
                self._handle_crossing(
                    door,
                    crossing,
                    config,
                    now_ts,
                )

            # Update activity timestamp
            if frame_had_crossing:
                door.last_activity_ts = now_ts

            # Finalize event if timeout reached
            analysis = self._finalize_event_if_needed(
                door,
                config,
                now_ts,
            )

            if analysis:
                analyses.append((door_id, analysis))

        # Create outputs
        incidents = self._generate_incidents(
            analyses,
            frame_id,
            stream_info,
        )

        alerts = self._generate_alerts(
            analyses,
            frame_id,
            stream_info,
        )

        summary = self._generate_summary(analyses)

        return incidents, [], [], summary, alerts

    # ========================================================
    # INCIDENT & SUMMARY
    # ========================================================

    def _generate_alerts(self, analyses, frame_id, stream_info):
        """Create alert objects for backend/VMS."""

        alerts = []

        for door_id, analysis in analyses:
            if not analysis.suspected_tailgaters:
                continue

            alert_id = f"tailgating_{door_id}_{frame_id}"

            alert = self.create_alert_object(
                alert_type="tailgating",
                alert_id=alert_id,
                incident_category="security",
                threshold_value=float(len(analysis.suspected_tailgaters)),
                ascending=True,
                settings={
                    "door_id": door_id,
                    "tailgaters": analysis.suspected_tailgaters,
                    "confidence": analysis.confidence,
                    "camera": self.get_camera_info_from_stream(stream_info),
                },
            )

            alerts.append(alert)

            print(
                "[TAILGATING ALERT]",
                "door=", door_id,
                "tailgaters=", analysis.suspected_tailgaters,
            )

        return alerts

    def _generate_incidents(self, analyses, frame_id, stream_info):
        """Create incident records."""

        incidents = []

        for door_id, analysis in analyses:
            if not analysis.suspected_tailgaters:
                continue

            incident = self.create_incident(
                f"tailgating_{door_id}_{frame_id}",
                "tailgating",
                analysis.debug.get("severity", "warning"),
                self.get_camera_info_from_stream(stream_info),
            )

            incident["suspected_tailgaters"] = analysis.suspected_tailgaters
            incidents.append(incident)

        return incidents

    def _generate_summary(self, analyses):
        """Human-readable summary."""

        if not analyses:
            return "No tailgating events detected"

        total = sum(len(a.suspected_tailgaters) for _, a in analyses)
        return f"Tailgating detected: {total} unauthorized follower(s)"

    # ========================================================
    # HELPERS
    # ========================================================

    def _get_or_create_door_state(self, door_id, zone_cfg):
        """Create or reuse door runtime state."""

        if door_id in self._door_states:
            return self._door_states[door_id]

        secured = zone_cfg.zones["secured_zone"]

        # Compute secured zone centroid
        center = (
            sum(p[0] for p in secured) / len(secured),
            sum(p[1] for p in secured) / len(secured),
        )

        door = DoorRuntime(door_id=door_id)

        p1, p2 = zone_cfg.zones["access_line"]

        # Compute normal pointing into secured area
        normal = compute_entry_normal(p1, p2, center)

        dist = signed_distance(center, p1, p2)
        if dist < 0:
            normal = (-normal[0], -normal[1])

        door.entry_normal = normal

        self._door_states[door_id] = door
        return door

    def _handle_crossing(self, door, crossing, config, now_ts):
        """Add crossing into active event."""

        if door.active_event is None:
            self.event_manager.open_event(
                door, config.access_window_sec, now_ts
            )

        if not door.active_event:
            return

        self.event_manager.add_crossing(
            door.active_event, crossing
        )
        print("[HANDLE CROSSING] adding to event")

    def _finalize_event_if_needed(self, door, config, now_ts):
        """Close event when silence timeout occurs."""

        event = door.active_event
        if not event:
            return None

        print(
            "[FINALIZE CHECK]",
            "crossings=", len(event.crossings),
            "start_ts=", event.start_ts,
            "last_cross=", event.last_crossing_ts,
            "now=", now_ts,
            "since_start=", now_ts - event.start_ts,
            "since_last_cross=",
            now_ts - event.last_crossing_ts,
        )

        if not self.event_manager.should_close(
            event, door, now_ts, config.silence_timeout_sec
        ):
            return None

        closed = self.event_manager.close_event(
            door, config.cooldown_sec, now_ts
        )

        if not closed:
            return None

        # Analyze event crossings
        analysis = analyze_passage(
            closed.crossings,
            config.allowed_persons_per_event,
            config.max_follow_time_delta_sec,
        )

        # Send event summary to backend
        self._pending_events.append({
            "door_id": door.door_id,
            "crossings": [c.track_id for c in closed.crossings],
            "tailgaters": analysis.suspected_tailgaters,
            "confidence": analysis.confidence,
        })

        # Clear crossing latch
        for crossing in closed.crossings:
            key = (door.door_id, crossing.track_id)
            self._crossing_latch.pop(key, None)

        print("[EVENT CLOSED]", len(closed.crossings), "crossings")

        return analysis