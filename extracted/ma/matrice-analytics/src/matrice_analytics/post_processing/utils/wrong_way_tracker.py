import logging
import math
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class WrongWayState(Enum):
    """State machine states for wrong-way detection."""

    NORMAL = "NORMAL"
    SUSPECT = "SUSPECT"
    WRONG_WAY = "WRONG_WAY"


class ReferenceStatus(Enum):
    """Status of reference direction estimation."""

    NONE = "NONE"
    LEARNING = "LEARNING"
    CONFIRMED = "CONFIRMED"


class ReferenceSource(Enum):
    """Source of reference direction."""

    NONE = "NONE"
    USER_ZONE = "USER_ZONE"
    AUTO = "AUTO"


@dataclass
class TrackMotionState:
    """Per-track motion state for trajectory-based detection."""

    track_id: Any
    category: str

    # Position tracking
    position_prev: Optional[Tuple[float, float]] = None

    # EWMA velocity (smoothed)
    velocity_ewma: Tuple[float, float] = (0.0, 0.0)

    # Wrong-way confidence ∈ [0, 1]
    wrong_way_confidence: float = 0.0

    # State machine
    state: WrongWayState = WrongWayState.NORMAL

    # Tracking metadata
    first_seen_frame: int = 0
    last_seen_frame: int = 0
    frames_tracked: int = 0

    # For output
    last_bbox: Optional[Dict[str, Any]] = None
    last_detection_confidence: float = 0.0
    last_direction_score: float = 0.0


@dataclass
class AutoReferenceState:
    """State for auto-reference direction estimation."""

    status: ReferenceStatus = ReferenceStatus.NONE
    reference_vector: Optional[Tuple[float, float]] = None
    confidence: float = 0.0

    # Motion buffer for estimation
    motion_samples: deque = field(default_factory=lambda: deque(maxlen=100))

    # Stability tracking
    dominant_direction_history: deque = field(default_factory=lambda: deque(maxlen=30))
    frames_since_last_change: int = 0


class WrongWayDetectionTracker:
    """
    Trajectory-based wrong-way vehicle detection tracker.

    Uses EWMA velocity smoothing and continuous confidence accumulation
    to detect vehicles moving against the expected traffic direction.

    Reference Direction Sources (in priority order):
    1. User-defined zone_config (first point → last point)
    2. Auto-estimation from observed traffic flow

    Auto-Reference Re-Learning:
    - For AUTO sources, reference is periodically re-learned to adapt to
      changing traffic patterns (e.g., time-of-day flow changes)
    - Re-learning interval configurable via auto_ref_relearn_interval_frames
    - User-defined zones (USER_ZONE) are never re-learned
    """

    def __init__(
        self,
        # EWMA velocity smoothing
        alpha: float = 0.20,
        # Minimum velocity to consider motion (pixels/frame)
        v_min: float = 1.2,
        # Confidence accumulation
        beta: float = 0.10,  # Confidence gain per wrong-way frame
        gamma: float = 0.018,  # Confidence decay per frame
        # State thresholds
        c_suspect: float = 0.25,  # Threshold to enter SUSPECT
        c_confirm: float = 0.65,  # Threshold to confirm WRONG_WAY
        # Decay from WRONG_WAY
        c_decay_from_wrong: float = 0.30,  # Must drop below this to decay
        correct_direction_frames_to_decay: int = 20,  # Frames of correct movement
        # New: require this many consecutive strong wrong-way frames before confirming
        min_confirm_frames: int = 12,
        # Track cleanup
        stale_track_frames: int = 40,
        # Auto-reference parameters
        auto_ref_relearn_interval_frames: int = 108000,  # 1 hour at 30 FPS
        auto_ref_min_tracks: int = 5,
        auto_ref_warmup_frames: int = 90,
        auto_ref_alpha: float = 0.05,
        auto_ref_confirm_threshold: float = 0.7,
        auto_ref_stability_frames: int = 60,
    ):
        # EWMA parameters
        self.alpha = alpha
        self.v_min = v_min

        # Confidence parameters
        self.beta = beta
        self.gamma = gamma
        self.c_suspect = c_suspect
        self.c_confirm = c_confirm
        self.c_decay_from_wrong = c_decay_from_wrong
        self.correct_direction_frames_to_decay = correct_direction_frames_to_decay

        # New confirmation streak requirement
        self.min_confirm_frames = min_confirm_frames

        # Cleanup
        self.stale_track_frames = stale_track_frames

        # Auto-reference parameters
        self.auto_ref_relearn_interval_frames = auto_ref_relearn_interval_frames
        self.auto_ref_min_tracks = auto_ref_min_tracks
        self.auto_ref_warmup_frames = auto_ref_warmup_frames
        self.auto_ref_alpha = auto_ref_alpha
        self.auto_ref_confirm_threshold = auto_ref_confirm_threshold
        self.auto_ref_stability_frames = auto_ref_stability_frames

        # Reference direction state
        self._reference_vector: Optional[Tuple[float, float]] = None
        self._reference_source: ReferenceSource = ReferenceSource.NONE
        self._reference_status: ReferenceStatus = ReferenceStatus.NONE

        # Auto-reference estimation stateauto_ref_relearn_interval_frames
        self._auto_ref_state = AutoReferenceState()

        # Frame at which auto-reference was last confirmed (for re-learning)
        self._auto_ref_confirmed_at_frame: int = 0

        # Per-track states
        self._track_states: Dict[Any, TrackMotionState] = {}

        # For decay from WRONG_WAY tracking
        self._correct_direction_streak: Dict[Any, int] = {}

        # New: consecutive wrong-way evidence streak for confirmation
        self._wrong_way_streak: Dict[Any, int] = {}

        # Cumulative counts
        self._confirmed_wrong_way_track_ids: Set[Any] = set()

        # Frame counter
        self._frame_count = 0

        logger.info(
            f"WrongWayDetectionTracker initialized: "
            f"alpha={alpha}, v_min={v_min}, beta={beta}, gamma={gamma}, "
            f"c_suspect={c_suspect}, c_confirm={c_confirm}, "
            f"min_confirm_frames={min_confirm_frames}, "
            f"auto_ref_relearn_interval={auto_ref_relearn_interval_frames} frames"
        )

    def set_reference_from_zone(self, zone_polygon: List[List[float]]) -> bool:
        if not zone_polygon or len(zone_polygon) < 2:
            logger.warning("Zone polygon must have at least 2 points")
            return False

        first_point = zone_polygon[0]
        last_point = zone_polygon[-1]

        dx = last_point[0] - first_point[0]
        dy = last_point[1] - first_point[1]

        magnitude = math.sqrt(dx * dx + dy * dy)
        if magnitude < 1e-6:
            logger.warning("Zone first and last points are too close")
            return False

        self._reference_vector = (dx / magnitude, dy / magnitude)
        self._reference_source = ReferenceSource.USER_ZONE
        self._reference_status = ReferenceStatus.CONFIRMED

        logger.info(
            f"Reference direction set from zone: "
            f"({first_point[0]:.1f}, {first_point[1]:.1f}) → "
            f"({last_point[0]:.1f}, {last_point[1]:.1f}), "
            f"vector=({self._reference_vector[0]:.3f}, {self._reference_vector[1]:.3f})"
        )
        return True

    def _check_auto_ref_relearn(self, current_frame: int) -> None:
        """
        Check if auto-reference should be re-learned based on interval.

        Only applies to AUTO reference sources. USER_ZONE references are never re-learned.
        During re-learning, the current reference is preserved to avoid detection gaps.
        """
        # Only re-learn AUTO references, never USER_ZONE
        if self._reference_source != ReferenceSource.AUTO:
            return

        # Check if interval has elapsed since last confirmation
        frames_since_confirm = current_frame - self._auto_ref_confirmed_at_frame

        if frames_since_confirm >= self.auto_ref_relearn_interval_frames:
            logger.info(
                f"[Frame {current_frame}] Auto-reference RE-LEARN triggered: "
                f"{frames_since_confirm} frames since last confirmation "
                f"(interval={self.auto_ref_relearn_interval_frames}). "
                f"Current vector=({self._reference_vector[0]:.3f}, {self._reference_vector[1]:.3f})"
            )

            # Reset auto-reference state for fresh learning
            # NOTE: We preserve _reference_vector and _reference_status during re-learning
            # so detection continues to work. Only reset the learning state.
            self._auto_ref_state = AutoReferenceState()

            # Temporarily set source to NONE to trigger sample collection
            # but keep the current reference active for detection
            self._reference_source = ReferenceSource.NONE

            # Note: _reference_vector and _reference_status remain CONFIRMED
            # so wrong-way detection continues using the old reference
            # until a new one is confirmed

    def update(self, detections: List[Dict[str, Any]], current_frame: int) -> Dict[str, Any]:
        self._frame_count = current_frame

        # Check if auto-reference needs re-learning
        self._check_auto_ref_relearn(current_frame)

        seen_track_ids: Set[Any] = set()

        wrong_way_detections: List[Dict[str, Any]] = []
        suspect_detections: List[Dict[str, Any]] = []

        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is None:
                continue

            seen_track_ids.add(track_id)

            bbox = detection.get("bounding_box", detection.get("bbox"))
            if not bbox:
                continue

            position = self._get_bbox_bottom25_center(bbox)
            if position == (0, 0):
                continue

            state = self._get_or_create_state(
                track_id=track_id,
                category=detection.get("category", "unknown"),
                current_frame=current_frame,
                position=position,
            )

            state.last_bbox = bbox
            state.last_detection_confidence = detection.get("confidence", 0.0)
            state.last_seen_frame = current_frame
            state.frames_tracked += 1

            self._process_track_trajectory(state, position, current_frame)

            # Collect motion samples when no confirmed reference OR during re-learning
            if self._reference_source == ReferenceSource.NONE:
                self._collect_motion_sample(state)

            if state.state == WrongWayState.WRONG_WAY:
                wrong_way_detections.append(self._build_detection_output(state))
                if track_id not in self._confirmed_wrong_way_track_ids:
                    self._confirmed_wrong_way_track_ids.add(track_id)
                    logger.info(
                        f"[Frame {current_frame}] WRONG-WAY CONFIRMED: "
                        f"track_id={track_id}, category={state.category}, "
                        f"confidence={state.wrong_way_confidence:.2f}"
                    )
            elif state.state == WrongWayState.SUSPECT:
                suspect_detections.append(self._build_detection_output(state))

        # Update auto-reference when source is NONE (initial learning or re-learning)
        if self._reference_source == ReferenceSource.NONE:
            self._update_auto_reference(current_frame)

        self._cleanup_stale_tracks(seen_track_ids, current_frame)

        return {
            "reference_source": self._reference_source.value,
            "reference_status": self._reference_status.value,
            "current_wrong_way_count": len(wrong_way_detections),
            "total_wrong_way_count": len(self._confirmed_wrong_way_track_ids),
            "current_wrong_way_detections": wrong_way_detections,
            "current_suspect_count": len(suspect_detections),
            "current_suspect_detections": suspect_detections,
        }

    def _get_or_create_state(
        self,
        track_id: Any,
        category: str,
        current_frame: int,
        position: Tuple[float, float],
    ) -> TrackMotionState:
        if track_id not in self._track_states:
            self._track_states[track_id] = TrackMotionState(
                track_id=track_id,
                category=category,
                position_prev=position,
                first_seen_frame=current_frame,
                last_seen_frame=current_frame,
            )
            logger.debug(f"[Frame {current_frame}] New track: {track_id}")
        return self._track_states[track_id]

    def _process_track_trajectory(
        self, state: TrackMotionState, position: Tuple[float, float], current_frame: int
    ) -> None:
        if state.position_prev is None:
            state.position_prev = position
            return

        v_inst = (
            position[0] - state.position_prev[0],
            position[1] - state.position_prev[1],
        )

        state.velocity_ewma = (
            self.alpha * v_inst[0] + (1 - self.alpha) * state.velocity_ewma[0],
            self.alpha * v_inst[1] + (1 - self.alpha) * state.velocity_ewma[1],
        )

        state.position_prev = position

        velocity_magnitude = math.sqrt(state.velocity_ewma[0] ** 2 + state.velocity_ewma[1] ** 2)

        if velocity_magnitude < self.v_min:
            state.wrong_way_confidence = max(0, state.wrong_way_confidence - self.gamma)
            self._update_state_machine(state, _direction_score=0.0)
            return

        if self._reference_status != ReferenceStatus.CONFIRMED:
            state.last_direction_score = 0.0
            return

        v_hat = (
            state.velocity_ewma[0] / velocity_magnitude,
            state.velocity_ewma[1] / velocity_magnitude,
        )

        ref_hat = self._reference_vector

        direction_score = v_hat[0] * ref_hat[0] + v_hat[1] * ref_hat[1]
        state.last_direction_score = direction_score

        wrong_way_score = max(0, -direction_score)

        state.wrong_way_confidence = max(
            0,
            min(1, state.wrong_way_confidence + self.beta * wrong_way_score - self.gamma),
        )

        if direction_score > 0.5:
            self._correct_direction_streak[state.track_id] = self._correct_direction_streak.get(state.track_id, 0) + 1
        else:
            self._correct_direction_streak[state.track_id] = 0

        # New: track consecutive strong wrong-way evidence frames
        if wrong_way_score > 0.4:
            self._wrong_way_streak[state.track_id] = self._wrong_way_streak.get(state.track_id, 0) + 1
        else:
            self._wrong_way_streak[state.track_id] = 0

        self._update_state_machine(state, direction_score)

        logger.debug(
            f"[Frame {current_frame}] Track {state.track_id}: "
            f"v_mag={velocity_magnitude:.2f}, dir_score={direction_score:.2f}, "
            f"conf={state.wrong_way_confidence:.2f}, state={state.state.value}"
        )

    def _update_state_machine(self, state: TrackMotionState, _direction_score: float) -> None:
        _ = (_direction_score,)
        if state.state == WrongWayState.NORMAL:
            if state.wrong_way_confidence >= self.c_suspect:
                state.state = WrongWayState.SUSPECT
                logger.debug(f"Track {state.track_id}: NORMAL → SUSPECT")

        elif state.state == WrongWayState.SUSPECT:
            streak = self._wrong_way_streak.get(state.track_id, 0)
            if state.wrong_way_confidence >= self.c_confirm and streak >= self.min_confirm_frames:
                state.state = WrongWayState.WRONG_WAY
                logger.info(
                    f"Track {state.track_id}: SUSPECT → WRONG_WAY "
                    f"(conf={state.wrong_way_confidence:.2f}, streak={streak})"
                )
            elif state.wrong_way_confidence < self.c_suspect * 0.5:
                state.state = WrongWayState.NORMAL
                logger.debug(f"Track {state.track_id}: SUSPECT → NORMAL")

        elif state.state == WrongWayState.WRONG_WAY:
            correct_streak = self._correct_direction_streak.get(state.track_id, 0)

            if (
                state.wrong_way_confidence < self.c_decay_from_wrong
                and correct_streak >= self.correct_direction_frames_to_decay
            ):
                state.state = WrongWayState.SUSPECT
                logger.info(f"Track {state.track_id}: WRONG_WAY → SUSPECT (correct_streak={correct_streak})")

    def _collect_motion_sample(self, state: TrackMotionState) -> None:
        velocity_magnitude = math.sqrt(state.velocity_ewma[0] ** 2 + state.velocity_ewma[1] ** 2)

        if velocity_magnitude < self.v_min:
            return

        if state.frames_tracked < 5:
            return

        v_hat = (
            state.velocity_ewma[0] / velocity_magnitude,
            state.velocity_ewma[1] / velocity_magnitude,
        )

        self._auto_ref_state.motion_samples.append(
            {
                "vector": v_hat,
                "magnitude": velocity_magnitude,
                "track_id": state.track_id,
            }
        )

    def _update_auto_reference(self, current_frame: int) -> None:
        if current_frame < self.auto_ref_warmup_frames:
            self._reference_status = ReferenceStatus.LEARNING
            return

        samples = list(self._auto_ref_state.motion_samples)

        unique_tracks = set(s["track_id"] for s in samples)
        if len(unique_tracks) < self.auto_ref_min_tracks:
            self._reference_status = ReferenceStatus.LEARNING
            return

        avg_x = sum(s["vector"][0] * s["magnitude"] for s in samples)
        avg_y = sum(s["vector"][1] * s["magnitude"] for s in samples)

        magnitude = math.sqrt(avg_x * avg_x + avg_y * avg_y)
        if magnitude < 1e-6:
            self._reference_status = ReferenceStatus.LEARNING
            return

        guess = (avg_x / magnitude, avg_y / magnitude)

        cluster_a_strength = 0.0
        cluster_b_strength = 0.0
        cluster_a_vectors = []
        cluster_b_vectors = []

        for sample in samples:
            dot = sample["vector"][0] * guess[0] + sample["vector"][1] * guess[1]
            if dot >= 0:
                cluster_a_strength += sample["magnitude"]
                cluster_a_vectors.append(sample)
            else:
                cluster_b_strength += sample["magnitude"]
                cluster_b_vectors.append(sample)

        total_strength = cluster_a_strength + cluster_b_strength
        if total_strength < 1e-6:
            return

        dominance_ratio = max(cluster_a_strength, cluster_b_strength) / total_strength

        if dominance_ratio < 0.65:
            self._auto_ref_state.frames_since_last_change = 0
            return

        dominant_cluster = cluster_a_vectors if cluster_a_strength > cluster_b_strength else cluster_b_vectors

        dom_x = sum(s["vector"][0] * s["magnitude"] for s in dominant_cluster)
        dom_y = sum(s["vector"][1] * s["magnitude"] for s in dominant_cluster)
        dom_mag = math.sqrt(dom_x * dom_x + dom_y * dom_y)

        if dom_mag < 1e-6:
            return

        dominant_direction = (dom_x / dom_mag, dom_y / dom_mag)

        if self._auto_ref_state.reference_vector is None:
            self._auto_ref_state.reference_vector = dominant_direction
        else:
            self._auto_ref_state.reference_vector = (
                self.auto_ref_alpha * dominant_direction[0]
                + (1 - self.auto_ref_alpha) * self._auto_ref_state.reference_vector[0],
                self.auto_ref_alpha * dominant_direction[1]
                + (1 - self.auto_ref_alpha) * self._auto_ref_state.reference_vector[1],
            )
            ref_mag = math.sqrt(
                self._auto_ref_state.reference_vector[0] ** 2 + self._auto_ref_state.reference_vector[1] ** 2
            )
            if ref_mag > 1e-6:
                self._auto_ref_state.reference_vector = (
                    self._auto_ref_state.reference_vector[0] / ref_mag,
                    self._auto_ref_state.reference_vector[1] / ref_mag,
                )

        self._auto_ref_state.confidence = min(1.0, self._auto_ref_state.confidence + 0.02 * dominance_ratio)
        self._auto_ref_state.frames_since_last_change += 1

        if (
            self._auto_ref_state.confidence >= self.auto_ref_confirm_threshold
            and self._auto_ref_state.frames_since_last_change >= self.auto_ref_stability_frames
        ):
            # Log direction change if this is a re-learn
            if self._reference_vector is not None:
                old_vec = self._reference_vector
                new_vec = self._auto_ref_state.reference_vector
                # Calculate angle difference
                dot_product = old_vec[0] * new_vec[0] + old_vec[1] * new_vec[1]
                angle_diff_deg = math.degrees(math.acos(max(-1, min(1, dot_product))))
                logger.info(
                    f"[Frame {current_frame}] Auto-reference UPDATED: "
                    f"old=({old_vec[0]:.3f}, {old_vec[1]:.3f}) → "
                    f"new=({new_vec[0]:.3f}, {new_vec[1]:.3f}), "
                    f"angle_change={angle_diff_deg:.1f}°"
                )

            self._reference_vector = self._auto_ref_state.reference_vector
            self._reference_source = ReferenceSource.AUTO
            self._reference_status = ReferenceStatus.CONFIRMED

            # Record confirmation frame for re-learn interval tracking
            self._auto_ref_confirmed_at_frame = current_frame

            logger.info(
                f"[Frame {current_frame}] Auto-reference CONFIRMED: "
                f"vector=({self._reference_vector[0]:.3f}, {self._reference_vector[1]:.3f}), "
                f"confidence={self._auto_ref_state.confidence:.2f}"
            )
        else:
            self._reference_status = ReferenceStatus.LEARNING

    def _build_detection_output(self, state: TrackMotionState) -> Dict[str, Any]:
        return {
            "track_id": state.track_id,
            "category": state.category,
            "bbox": state.last_bbox,
            "confidence": state.last_detection_confidence,
            "wrong_way_confidence": round(state.wrong_way_confidence, 3),
            "direction_score": round(state.last_direction_score, 3),
            "state": state.state.value,
        }

    def _cleanup_stale_tracks(self, seen_track_ids: Set[Any], current_frame: int) -> None:
        stale_ids = [
            tid
            for tid, state in self._track_states.items()
            if tid not in seen_track_ids and current_frame - state.last_seen_frame > self.stale_track_frames
        ]

        for tid in stale_ids:
            del self._track_states[tid]
            self._correct_direction_streak.pop(tid, None)
            self._wrong_way_streak.pop(tid, None)
            logger.debug(f"[Frame {current_frame}] Removed stale track: {tid}")

    @staticmethod
    def _get_bbox_bottom25_center(bbox: Dict[str, Any]) -> Tuple[float, float]:
        if isinstance(bbox, dict):
            if "xmin" in bbox:
                x_center = (bbox["xmin"] + bbox["xmax"]) / 2
                height = bbox["ymax"] - bbox["ymin"]
                y_target = bbox["ymax"] - 0.25 * height
                return (x_center, y_target)
            elif "x1" in bbox:
                x_center = (bbox["x1"] + bbox["x2"]) / 2
                height = bbox["y2"] - bbox["y1"]
                y_target = bbox["y2"] - 0.25 * height
                return (x_center, y_target)
        return (0, 0)

    def reset(self) -> None:
        self._track_states.clear()
        self._correct_direction_streak.clear()
        self._wrong_way_streak.clear()
        self._confirmed_wrong_way_track_ids.clear()
        self._auto_ref_state = AutoReferenceState()
        self._auto_ref_confirmed_at_frame = 0
        self._frame_count = 0

        if self._reference_source != ReferenceSource.USER_ZONE:
            self._reference_vector = None
            self._reference_source = ReferenceSource.NONE
            self._reference_status = ReferenceStatus.NONE

        logger.info("WrongWayDetectionTracker reset")

    def get_reference_info(self) -> Dict[str, Any]:
        """Get current reference direction information including re-learn status."""
        info = {
            "source": self._reference_source.value,
            "status": self._reference_status.value,
            "vector": self._reference_vector,
            "auto_confidence": (
                self._auto_ref_state.confidence if self._reference_source == ReferenceSource.AUTO else None
            ),
        }

        # Add re-learn timing info for AUTO sources
        if self._reference_source == ReferenceSource.AUTO or self._auto_ref_confirmed_at_frame > 0:
            frames_since_confirm = self._frame_count - self._auto_ref_confirmed_at_frame
            frames_until_relearn = max(0, self.auto_ref_relearn_interval_frames - frames_since_confirm)
            info["frames_since_last_confirm"] = frames_since_confirm
            info["frames_until_relearn"] = frames_until_relearn
            info["relearn_interval_frames"] = self.auto_ref_relearn_interval_frames

        return info

    def get_stats(self) -> Dict[str, Any]:
        return {
            "active_tracks": len(self._track_states),
            "total_wrong_way_confirmed": len(self._confirmed_wrong_way_track_ids),
            "reference_source": self._reference_source.value,
            "reference_status": self._reference_status.value,
            "frame_count": self._frame_count,
            "auto_ref_confirmed_at_frame": self._auto_ref_confirmed_at_frame,
        }

    def __repr__(self) -> str:
        return (
            f"WrongWayDetectionTracker("
            f"ref={self._reference_source.value}/{self._reference_status.value}, "
            f"tracks={len(self._track_states)}, "
            f"wrong_way={len(self._confirmed_wrong_way_track_ids)})"
        )
