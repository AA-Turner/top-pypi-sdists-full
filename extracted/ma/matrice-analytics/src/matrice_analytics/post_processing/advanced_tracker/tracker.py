"""
Advanced tracker implementation.

This module provides the AdvancedTracker class that implements BYTETracker-like
functionality for object tracking with support for various input formats.

Features:
- BYTETracker-like multi-stage association
- Track recovery for re-identifying objects after temporary loss
- State persistence for preserving counts across restarts
- Configurable thresholds optimized for count accuracy
"""

import json
import logging
import math
import os
import time
from collections import OrderedDict, deque
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

from .base import BaseTrack, TrackState
from .config import TrackerConfig
from .kalman_filter import KalmanFilterXYAH
from .matching import fuse_score, iou_distance, linear_assignment
from .strack import STrack

logger = logging.getLogger(__name__)

# How many recently-seen track IDs to retain for de-duplicating cumulative counts.
# This caps memory for the counting bookkeeping; the counts themselves are exact
# integers and are NOT bounded by this. Sized well above the number of distinct IDs
# that can appear within track_recovery_time_window (default 30.0s) so an ID is
# never forgotten while it can still legitimately reappear -- at 50 new IDs/sec
# that window holds ~1,500 IDs, so 50,000 leaves a ~33x margin while bounding the
# structure to a few MB instead of growing without limit.
_RECENT_TRACK_ID_WINDOW = 50_000


class AdvancedTracker:
    """
    AdvancedTracker: A tracking algorithm similar to BYTETracker for object detection and tracking.

    This class encapsulates the functionality for initializing, updating, and managing the tracks for detected objects in a
    video sequence. It maintains the state of tracked, lost, and removed tracks over frames, utilizes Kalman filtering for
    predicting the new object locations, and performs data association.

    Attributes:
        tracked_stracks (List[STrack]): List of successfully activated tracks.
        lost_stracks (List[STrack]): List of lost tracks.
        removed_stracks (List[STrack]): List of removed tracks.
        frame_id (int): The current frame ID.
        config (TrackerConfig): Tracker configuration.
        max_time_lost (int): Frame-count view of the lost-track grace, kept for
            external readers. The grace ACTUALLY applied is in seconds of stream
            time (see ``_lost_grace_seconds``); under a sampler the two differ.
        kalman_filter (KalmanFilterXYAH): Kalman Filter object.
        class_smoother (Optional[ClassSmoother]): Optional class smoother for class label smoothing over flicker.
    """

    def __init__(self, config: TrackerConfig, namespace: Optional[str] = None):
        """
        Initialize an AdvancedTracker instance for object tracking.

        Args:
            config (TrackerConfig): Tracker configuration object.
            namespace (Optional[str]): Namespace for track ID generation (e.g., camera_id).
                If provided, track IDs are isolated to this namespace to prevent
                cross-camera collisions. Recommended to use hash of camera_id.
        """
        self.tracked_stracks = []  # type: List[STrack]
        self.lost_stracks = []  # type: List[STrack]
        self.removed_stracks = []  # type: List[STrack]

        self.frame_id = 0
        self.config = config
        self.max_time_lost = config.max_time_lost
        self.kalman_filter = self.get_kalmanfilter()

        # Set namespace for track ID isolation (prevents cross-camera ID collisions)
        self.namespace = namespace
        if namespace:
            BaseTrack.set_namespace(namespace)
            logger.debug(f"Tracker initialized with namespace: {namespace}")
        self.reset_id()

        self.class_aggregator = None
        if config.enable_class_aggregation:
            from .track_class_aggregator import TrackClassAggregator

            self.class_aggregator = TrackClassAggregator(
                window_size=config.class_aggregation_window_size
            )

        # Track recovery for re-entries: stores recently removed tracks for potential re-matching
        # Structure: {track_id: {"last_xyxy": bbox, "lost_time": timestamp, "category": cat}}
        self._recovery_pool: Dict[int, Dict[str, Any]] = {}
        self._track_aliases: Dict[int, int] = {}  # Maps new IDs to recovered IDs

        # Cumulative tracking statistics (for accurate counting).
        #
        # These are counters plus a BOUNDED de-duplication window, not unbounded
        # "every ID ever seen" sets. Holding every ID forever grew without limit
        # (~250-370 MB/day/device at 50 new IDs/sec) and made save_state()'s JSON
        # grow linearly with it. The same file already bounds the adjacent
        # structures (removed_stracks at 1000, _fps_samples via deque(maxlen=30),
        # _recovery_pool by explicit expiry), so the unbounded sets were an
        # oversight rather than a design choice.
        #
        # Correctness argument for the window: the totals are exact because they
        # are counters, incremented only on an ID's FIRST sighting. Dedup needs
        # memory of an ID only for as long as that ID can legitimately reappear
        # after dropping out of the activated set -- which is bounded by
        # track_recovery_time_window (default 30.0s, see _update_recovery_pool),
        # after which the recovery pool itself evicts the entry and the ID can
        # never come back. _RECENT_TRACK_ID_WINDOW is sized far above 30s worth of
        # distinct IDs at realistic rates, so an ID is never evicted while it is
        # still recoverable. Track IDs are also monotonically increasing, so an
        # evicted ID cannot be re-issued to a different object.
        self._total_track_count: int = 0
        self._category_track_counts: Dict[str, int] = {}
        # Insertion-ordered bounded sets: dict keys give O(1) membership plus O(1)
        # eviction of the oldest entry (a plain set has no eviction order).
        self._recent_track_ids: "OrderedDict[int, None]" = OrderedDict()
        self._recent_category_track_ids: Dict[str, "OrderedDict[int, None]"] = {}

        # State persistence
        self._last_state_save_frame = 0

        # ---------------------------------------------------------------------
        # CCTVTracker-parity feature state. All INERT unless the matching config
        # flag is on, so the default tracker is byte-for-byte unchanged.
        # ---------------------------------------------------------------------
        # FPS adaptation: cache base thresholds so blending toward the low-fps
        # floors never compounds, and reset() can restore them.
        self._base_match_thresh = config.match_thresh
        self._base_new_track_thresh = config.new_track_thresh
        # Effective (possibly FPS-adapted) thresholds live on the INSTANCE and are
        # what the association steps read — self.config is NEVER mutated, so a
        # TrackerConfig shared across trackers stays intact. Start == base.
        self._match_thresh = config.match_thresh
        self._new_track_thresh = config.new_track_thresh
        self._effective_fps = float(config.frame_rate)
        self._fps_samples: deque = deque(maxlen=30)  # update() monotonic stamps
        self._last_adapt_ts: Optional[float] = None

        # Per-frame time base (SG-24). `timestamp=` on update() carries the
        # frame's own presentation time in seconds (see rtp_clock.RtpClock for
        # the RTP -> seconds conversion). When present it is the source of the
        # effective interval; when absent or non-monotonic the tracker falls
        # back to counting frames at the effective fps, which reproduces the
        # historical behaviour exactly.
        self._last_frame_ts: Optional[float] = None
        self._last_frame_dt: Optional[float] = None
        self._using_frame_timestamps = False
        self._non_monotonic_ts_count = 0
        # Stream time: seconds elapsed over the frames this tracker has seen.
        # Advanced by the real per-frame dt when one is available, else by one
        # nominal frame at the effective fps. All ageing is measured on it.
        self._stream_time = 0.0
        self._frame_times: "OrderedDict[int, float]" = OrderedDict()

        # Temporal confirmation: per-track sliding-window hit buffers.
        self._hit_buffers: Dict[int, deque] = {}
        self._confirmed_ids: Set[int] = set()
        self._confirm_window = 2
        self._confirm_min_hits = 1
        self._recompute_confirm_params()

    def update(
        self,
        detections: Union[List[Dict], Dict[str, List[Dict]]],
        img: Optional[np.ndarray] = None,
        timestamp: Optional[float] = None,
    ) -> Union[List[Dict], Dict[str, List[Dict]]]:
        """
        Update the tracker with new detections and return the current list of tracked objects.

        Args:
            detections: Detection results in various formats:
                - List[Dict]: Single frame detections
                - Dict[str, List[Dict]]: Multi-frame detections with frame keys
            img: Optional image for motion compensation
            timestamp: Optional presentation time of THIS frame, in seconds on a
                monotonic media clock. For an RTSP source this is the forwarded
                RTP timestamp converted by ``rtp_clock.RtpClock`` — the gateway
                never rewrites it, so ``ts_now - ts_prev`` is the true interval
                even when a sampler dropped everything in between. Optional and
                backward compatible: callers that omit it (or pass a
                non-monotonic value) keep the previous frame-counting behaviour,
                and the fallback is logged rather than taken silently.

        Returns:
            Tracking results in the same format as input
        """
        # predict()-only gap glide on empty single-frame input (opt-in). predict()
        # does its own frame_id increment, so return BEFORE incrementing here.
        # Default (flag off) preserves the historical "empty in -> empty out".
        if (
            self.config.enable_predict_on_empty
            and isinstance(detections, list)
            and len(detections) == 0
        ):
            return self.predict(timestamp=timestamp)

        self.frame_id += 1

        # Establish this frame's interval, then advance the stream clock, BEFORE
        # any predict/threshold read. Sampled once per update() call rather than
        # per processed frame so the multi-frame dict format — which runs several
        # frames back-to-back inside ONE call — cannot mistake its own loop speed
        # for the camera's frame spacing.
        dt = self._frame_dt(timestamp)
        self._advance_stream_time(dt)
        self._maybe_adapt_fps(dt)

        # Handle different input formats
        if isinstance(detections, dict):
            # Multi-frame format
            return self._update_multi_frame(detections, img)
        else:
            # Single frame format
            return self._update_single_frame(detections, img)

    def _update_single_frame(
        self, detections: List[Dict], img: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """Update tracker with single frame detections."""
        # Convert detections to STrack format
        stracks = self._convert_detections_to_stracks(detections)

        # Perform tracking update
        tracked_objects = self._perform_tracking_update(stracks, img)

        # Convert back to detection format
        return self._convert_stracks_to_detections(tracked_objects)

    def _update_multi_frame(
        self, detections: Dict[str, List[Dict]], img: Optional[np.ndarray] = None
    ) -> Dict[str, List[Dict]]:
        """Update tracker with multi-frame detections."""
        results = {}

        for frame_key, frame_detections in detections.items():
            # Convert frame detections to STrack format
            stracks = self._convert_detections_to_stracks(frame_detections)

            # Perform tracking update
            tracked_objects = self._perform_tracking_update(stracks, img)

            # Convert back to detection format
            results[frame_key] = self._convert_stracks_to_detections(tracked_objects)

        return results

    def _convert_detections_to_stracks(self, detections: List[Dict]) -> List[STrack]:
        """Convert detection format to STrack objects."""
        stracks = []

        for i, det in enumerate(detections):
            # Extract bounding box
            bbox = det.get("bounding_box", {})
            if "x" in bbox and "y" in bbox and "width" in bbox and "height" in bbox:
                # Center format
                x, y, w, h = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
            elif "xmin" in bbox and "ymin" in bbox and "xmax" in bbox and "ymax" in bbox:
                # Corner format
                x = (bbox["xmin"] + bbox["xmax"]) / 2
                y = (bbox["ymin"] + bbox["ymax"]) / 2
                w = bbox["xmax"] - bbox["xmin"]
                h = bbox["ymax"] - bbox["ymin"]
            elif "x1" in bbox and "y1" in bbox and "x2" in bbox and "y2" in bbox:
                # Corner format (x1/y1/x2/y2) — emitted by _normalize_yolo_results.
                # Without this branch it falls through to the positional fallback
                # below and gets misread as center-x/center-y/width/height, which
                # massively inflates the tracked box.
                x = (bbox["x1"] + bbox["x2"]) / 2
                y = (bbox["y1"] + bbox["y2"]) / 2
                w = bbox["x2"] - bbox["x1"]
                h = bbox["y2"] - bbox["y1"]
            else:
                # Try to extract from any format
                values = list(bbox.values())
                if len(values) >= 4:
                    x, y, w, h = values[0], values[1], values[2], values[3]
                else:
                    continue

            # Extract other properties
            score = det.get("confidence", 0.0)
            category = det.get("category", "unknown")

            # Create STrack
            xywh = [x, y, w, h, i]  # Add index as last element
            strack = STrack(xywh, score, category)

            # CRITICAL FIX: Store the original detection data to preserve all fields
            # This ensures face recognition fields (embedding, landmarks, etc.) are preserved
            strack.original_detection = det.copy()

            stracks.append(strack)

        return stracks

    def _convert_stracks_to_detections(
        self, stracks: List[STrack], record_class_observation: bool = True
    ) -> List[Dict]:
        """Convert STrack objects back to detection format.

        Args:
            stracks: tracks to emit.
            record_class_observation: whether this frame carries new class evidence.
                False on predict-only (glide) frames, which re-emit the previous
                detection's class: pushing it into the aggregator window again would
                let a long gap outvote the real observations it is meant to smooth.
        """
        detections = []

        for strack in stracks:
            if strack.is_activated:
                # Get bounding box in xyxy format
                xyxy = strack.xyxy

                # CRITICAL FIX: Start with original detection data to preserve all fields
                if hasattr(strack, "original_detection") and strack.original_detection:
                    # Start with the original detection to preserve all face recognition fields
                    detection = strack.original_detection.copy()

                    # Update with tracking-specific fields
                    detection["bounding_box"] = {
                        "xmin": float(xyxy[0]),
                        "ymin": float(xyxy[1]),
                        "xmax": float(xyxy[2]),
                        "ymax": float(xyxy[3]),
                    }
                    detection["confidence"] = float(strack.score)
                    detection["category"] = strack.cls
                    detection["track_id"] = int(strack.track_id)
                    detection["frame_id"] = int(strack.frame_id)
                else:
                    # Fallback to minimal detection if original data not available
                    detection = {
                        "bounding_box": {
                            "xmin": float(xyxy[0]),
                            "ymin": float(xyxy[1]),
                            "xmax": float(xyxy[2]),
                            "ymax": float(xyxy[3]),
                        },
                        "confidence": float(strack.score),
                        "category": strack.cls,
                        "track_id": int(strack.track_id),
                        "frame_id": int(strack.frame_id),
                    }

                detections.append(detection)

        if self.class_aggregator is not None:
            for detection in detections:
                if record_class_observation:
                    aggregated_class = self.class_aggregator.update_and_aggregate(
                        track_id=detection["track_id"], observed_class=detection["category"]
                    )
                else:
                    aggregated_class = self.class_aggregator.get_aggregated_class(
                        detection["track_id"], detection["category"]
                    )
                detection["category"] = aggregated_class

        return detections

    def _perform_tracking_update(
        self, detections: List[STrack], _img: Optional[np.ndarray] = None
    ) -> List[STrack]:
        """Perform the core tracking update algorithm."""
        # Ensure namespace is set for any new track ID generation
        _ = (_img,)
        if self.namespace:
            BaseTrack.set_namespace(self.namespace)

        activated_stracks = []
        refind_stracks = []
        lost_stracks = []
        removed_stracks = []

        dets, dets_second = self._split_by_confidence(detections)

        # Step 1: First association, with high score detection boxes
        unconfirmed, tracked_stracks = self._partition_unconfirmed()

        # Predict the current location with KF
        strack_pool = self.joint_stracks(tracked_stracks, self.lost_stracks)
        self.multi_predict(strack_pool)

        # Calculate distances and perform matching
        dists = self.get_dists(strack_pool, dets)
        matches, u_track, u_detection = linear_assignment(dists, thresh=self._match_thresh)

        self._apply_matches(
            [(strack_pool[i], dets[j]) for i, j in matches],
            activated_stracks,
            refind_stracks,
        )

        # Step 2: Second association, with low score detection boxes
        # Uses secondary_match_thresh (configurable, default 0.5) for IoU-only matching
        r_tracked_stracks = [
            strack_pool[i] for i in u_track if strack_pool[i].state == TrackState.Tracked
        ]
        dists = iou_distance(STrack.xyxy_matrix(r_tracked_stracks), STrack.xyxy_matrix(dets_second))
        secondary_thresh = getattr(self.config, "secondary_match_thresh", 0.5)
        matches, u_track, _u_detection_second = linear_assignment(dists, thresh=secondary_thresh)

        self._apply_matches(
            [(r_tracked_stracks[i], dets_second[j]) for i, j in matches],
            activated_stracks,
            refind_stracks,
        )

        for it in u_track:
            track = r_tracked_stracks[it]
            if track.state != TrackState.Lost:
                track.mark_lost()
                lost_stracks.append(track)

        # Step 3: Deal with unconfirmed tracks
        # Uses unconfirmed_match_thresh (configurable, default 0.7)
        detections = [dets[i] for i in u_detection]
        dists = self.get_dists(unconfirmed, detections)
        unconfirmed_thresh = getattr(self.config, "unconfirmed_match_thresh", 0.7)
        matches, u_unconfirmed, u_detection = linear_assignment(dists, thresh=unconfirmed_thresh)

        # Unconfirmed tracks are state Tracked -> _apply_matches routes them through
        # the update() bookkeeping path, same as the old per-track .update() loop.
        self._apply_matches(
            [(unconfirmed[i], detections[j]) for i, j in matches],
            activated_stracks,
            refind_stracks,
        )

        for it in u_unconfirmed:
            track = unconfirmed[it]
            track.mark_removed()
            removed_stracks.append(track)

        # Step 4: Init new stracks (with track recovery attempt)
        self._init_new_tracks(detections, u_detection, activated_stracks)

        # Step 5: Update state.
        self._retire_expired_lost_tracks(removed_stracks)
        self._commit_frame_state(activated_stracks, refind_stracks, lost_stracks, removed_stracks)

        # Update cumulative tracking statistics
        active_stracks = [x for x in self.tracked_stracks if x.is_activated]

        # Temporal confirmation gates EMISSION + counting (not lifecycle): the
        # internal track lists above still hold every track, so recovery/re-ID
        # keep working; we only withhold unconfirmed (ghost) tracks from output
        # and from the cumulative counts. Flag off -> emit == active (unchanged).
        if self.config.enable_temporal_confirmation:
            emit_stracks = self._temporal_filter(active_stracks)
        else:
            emit_stracks = active_stracks

        # Count only what we emit, so single-frame ghosts don't inflate totals.
        self._update_tracking_statistics(emit_stracks)

        # Periodically save state
        self._maybe_save_state()

        return emit_stracks

    def _split_by_confidence(self, detections: List[STrack]) -> Tuple[List[STrack], List[STrack]]:
        """Split detections into the high-score set and the BYTE low-score set.

        Returns ``(dets, dets_second)``: the first drives the primary
        association, the second the low-score recovery pass.
        """
        scores = np.array([det.score for det in detections])
        remain_inds = scores >= self.config.track_high_thresh
        inds_low = scores > self.config.track_low_thresh
        inds_high = scores < self.config.track_high_thresh

        inds_second = inds_low & inds_high
        dets_second = [detections[i] for i in range(len(detections)) if inds_second[i]]
        dets = [detections[i] for i in range(len(detections)) if remain_inds[i]]
        return dets, dets_second

    def _partition_unconfirmed(self) -> Tuple[List[STrack], List[STrack]]:
        """Split the tracked list into ``(unconfirmed, activated)`` tracks."""
        unconfirmed = []
        tracked_stracks = []
        for track in self.tracked_stracks:
            if not track.is_activated:
                unconfirmed.append(track)
            else:
                tracked_stracks.append(track)
        return unconfirmed, tracked_stracks

    def _init_new_tracks(
        self,
        candidates: List[STrack],
        u_detection: Any,
        activated_stracks: List[STrack],
    ) -> None:
        """Step 4: start a track for each unmatched detection worth keeping,
        reusing a recovered id where one is available."""
        for inew in u_detection:
            track = candidates[inew]
            if track.score < self._new_track_thresh:
                continue

            # Try to recover a previously lost track before creating a new one
            recovered_id = self._try_recover_track(track)
            if recovered_id is not None:
                # Use the recovered track ID instead of creating a new one
                track.track_id = recovered_id
                self._track_aliases[track.track_id] = recovered_id
                logger.debug(f"[TRACK_RECOVERY] Reusing recovered track ID {recovered_id}")

            track.activate(self.kalman_filter, self.frame_id)
            activated_stracks.append(track)

    def _retire_expired_lost_tracks(self, removed_stracks: List[STrack]) -> None:
        """Remove lost tracks that are past the grace, appending them to
        ``removed_stracks``.

        Ageing is measured in SECONDS of stream time, not frames. A grace of N
        frames is N x the sampling factor in wall-clock seconds, so under a
        sampler a frame-counted grace keeps dead tracks alive far longer than
        intended and lets them steal associations from genuinely new objects.
        """
        lost_grace_sec = self._lost_grace_seconds()
        for track in self.lost_stracks:
            if self._elapsed_since_frame(track.end_frame) > lost_grace_sec:
                track.mark_removed()
                removed_stracks.append(track)

    def _commit_frame_state(
        self,
        activated_stracks: List[STrack],
        refind_stracks: List[STrack],
        lost_stracks: List[STrack],
        removed_stracks: List[STrack],
    ) -> None:
        """Fold this frame's activated/refound/lost/removed tracks back into the
        tracker's own lists, then run the bounded-growth and cleanup bookkeeping.

        Order matters and is unchanged: ``self.removed_stracks`` is read by
        ``sub_stracks`` BEFORE this frame's removals are appended to it.
        """
        self.tracked_stracks = [t for t in self.tracked_stracks if t.state == TrackState.Tracked]
        self.tracked_stracks = self.joint_stracks(self.tracked_stracks, activated_stracks)
        self.tracked_stracks = self.joint_stracks(self.tracked_stracks, refind_stracks)
        self.lost_stracks = self.sub_stracks(self.lost_stracks, self.tracked_stracks)
        self.lost_stracks.extend(lost_stracks)
        self.lost_stracks = self.sub_stracks(self.lost_stracks, self.removed_stracks)
        self.tracked_stracks, self.lost_stracks = self.remove_duplicate_stracks(
            self.tracked_stracks, self.lost_stracks
        )
        self.removed_stracks.extend(removed_stracks)

        if len(self.removed_stracks) > 1000:
            self.removed_stracks = self.removed_stracks[-999:]

        # Clean up aggregator windows for removed tracks
        if self.class_aggregator is not None and removed_stracks:
            self.class_aggregator.remove_tracks([t.track_id for t in removed_stracks])

        # Update recovery pool with removed tracks for potential re-identification
        if removed_stracks:
            self._update_recovery_pool(removed_stracks)

    def _apply_matches(self, pairs, activated_stracks, refind_stracks):
        """Apply matched (track, detection) pairs: ONE batched Kalman correction for
        all pairs (STrack.multi_kf_update), then the per-track bookkeeping that
        update()/re_activate(new_id=False) used to do — Tracked tracks go to
        activated_stracks, lost ones are re-activated into refind_stracks.
        Behaviorally identical to the old per-track .update()/.re_activate() loop."""
        if not pairs:
            return
        tracks = [t for t, _ in pairs]
        dets = [d for _, d in pairs]
        STrack.multi_kf_update(tracks, dets)
        for track, det in pairs:
            if track.state == TrackState.Tracked:
                track._post_kf_bookkeeping(det, self.frame_id, reactivate=False)
                activated_stracks.append(track)
            else:
                track._post_kf_bookkeeping(det, self.frame_id, reactivate=True)
                refind_stracks.append(track)

    def get_kalmanfilter(self) -> KalmanFilterXYAH:
        """Return a Kalman filter object for tracking bounding boxes using KalmanFilterXYAH."""
        return KalmanFilterXYAH()

    def get_dists(self, tracks: List[STrack], detections: List[STrack]) -> np.ndarray:
        """Calculate the distance between tracks and detections using IoU and optionally fuse scores."""
        # Stacked box matrices: one vectorized computation per list instead of a
        # per-track xyxy property call inside iou_distance (same values).
        dists = iou_distance(STrack.xyxy_matrix(tracks), STrack.xyxy_matrix(detections))
        if self.config.fuse_score:
            dists = fuse_score(dists, detections)
        return dists

    def multi_predict(self, tracks: List[STrack]):
        """Predict the next states for multiple tracks using Kalman filter.

        Uses this tracker's OWN filter instance (not the global STrack.shared_kalman)
        so per-camera FPS adaptation rescales dt without cross-tracker interference.
        At dt=1.0 the instance filter is byte-identical to the shared one, so the
        default path is unchanged."""
        STrack.multi_predict(tracks, self.kalman_filter)

    @staticmethod
    def reset_id():
        """Reset the ID counter for STrack instances to ensure unique track IDs across tracking sessions."""
        STrack.reset_id()

    def reset(self):
        """Reset the tracker by clearing all tracked, lost, and removed tracks and reinitializing the Kalman filter."""
        self.tracked_stracks = []
        self.lost_stracks = []
        self.removed_stracks = []
        self.frame_id = 0
        self.kalman_filter = self.get_kalmanfilter()  # fresh filter -> dt back to 1.0
        # Ensure namespace is set before reset
        if self.namespace:
            BaseTrack.set_namespace(self.namespace)
        self.reset_id()

        if self.class_aggregator is not None:
            self.class_aggregator.reset()

        # Restore CCTVTracker-parity feature state to its unadapted baseline.
        # Only instance attributes are touched; self.config is never written.
        self._match_thresh = self._base_match_thresh
        self._new_track_thresh = self._base_new_track_thresh
        self.max_time_lost = self.config.max_time_lost
        self._effective_fps = float(self.config.frame_rate)
        self._fps_samples.clear()
        self._last_adapt_ts = None
        self._last_frame_ts = None
        self._last_frame_dt = None
        self._using_frame_timestamps = False
        self._non_monotonic_ts_count = 0
        self._stream_time = 0.0
        self._frame_times.clear()
        self._hit_buffers.clear()
        self._confirmed_ids = set()
        self._recompute_confirm_params()

    @staticmethod
    def joint_stracks(tlista: List[STrack], tlistb: List[STrack]) -> List[STrack]:
        """Combine two lists of STrack objects into a single list, ensuring no duplicates based on track IDs."""
        exists = {}
        res = []
        for t in tlista:
            exists[t.track_id] = 1
            res.append(t)
        for t in tlistb:
            tid = t.track_id
            if not exists.get(tid, 0):
                exists[tid] = 1
                res.append(t)
        return res

    @staticmethod
    def sub_stracks(tlista: List[STrack], tlistb: List[STrack]) -> List[STrack]:
        """Filter out the stracks present in the second list from the first list."""
        track_ids_b = {t.track_id for t in tlistb}
        return [t for t in tlista if t.track_id not in track_ids_b]

    def remove_duplicate_stracks(
        self, stracksa: List[STrack], stracksb: List[STrack]
    ) -> Tuple[List[STrack], List[STrack]]:
        """Remove duplicate stracks from two lists based on Intersection over Union (IoU) distance.

        Uses the configurable duplicate_removal_iou_thresh from config.
        Higher thresholds are more permissive (reduce false duplicates).
        Lower thresholds are more aggressive (remove more duplicates).
        """
        # No pairs possible -> identical output to the full path, skip the IoU pass
        # (runs every frame; lost_stracks is empty most frames in steady state).
        if not stracksa or not stracksb:
            return list(stracksa), list(stracksb)
        pdist = iou_distance(STrack.xyxy_matrix(stracksa), STrack.xyxy_matrix(stracksb))
        # Use configurable threshold (default 0.3, was hardcoded 0.15)
        dup_thresh = getattr(self.config, "duplicate_removal_iou_thresh", 0.3)
        pairs = np.where(pdist < dup_thresh)
        dupa, dupb = [], []
        for p, q in zip(*pairs, strict=False):
            timep = stracksa[p].frame_id - stracksa[p].start_frame
            timeq = stracksb[q].frame_id - stracksb[q].start_frame
            if timep > timeq:
                dupb.append(q)
            else:
                dupa.append(p)
        resa = [t for i, t in enumerate(stracksa) if i not in dupa]
        resb = [t for i, t in enumerate(stracksb) if i not in dupb]
        return resa, resb

    # =========================================================================
    # TRACK RECOVERY METHODS - For re-identifying objects after temporary loss
    # =========================================================================

    def _update_recovery_pool(self, removed_stracks: List[STrack]) -> None:
        """
        Add removed tracks to recovery pool for potential re-identification.

        When a track is removed (lost for too long), we save its last known
        position so we can recognize it if it reappears.
        """
        if not getattr(self.config, "enable_track_recovery", True):
            return

        # monotonic(), not time(): "how long ago was this track lost" is an elapsed
        # duration within one process, so a wall-clock step must not affect it. With
        # time() a backwards step made entries un-expirable (the pool grew and stale
        # IDs stayed eligible for recovery) and a forwards step flushed the pool
        # instantly, breaking re-identification. Entries restored from a previous
        # process are normalised in restore_state().
        now = time.monotonic()
        recovery_window = getattr(self.config, "track_recovery_time_window", 30.0)

        # Clean up expired entries
        expired_ids = [
            tid
            for tid, info in self._recovery_pool.items()
            if now - info.get("lost_time", 0) > recovery_window
        ]
        for tid in expired_ids:
            del self._recovery_pool[tid]

        # Add newly removed tracks
        for track in removed_stracks:
            self._recovery_pool[track.track_id] = {
                "last_xyxy": track.xyxy.tolist()
                if hasattr(track.xyxy, "tolist")
                else list(track.xyxy),
                "lost_time": now,
                "category": track.cls,
                "score": track.score,
            }
            logger.debug(f"[RECOVERY_POOL] Added track {track.track_id} to recovery pool")

    def _try_recover_track(self, detection: STrack) -> Optional[int]:
        """
        Try to match a new detection to a recently lost track.

        Returns the recovered track ID if a match is found, None otherwise.
        """
        if not getattr(self.config, "enable_track_recovery", True):
            return None

        if not self._recovery_pool:
            return None

        det_xyxy = detection.xyxy
        det_category = detection.cls
        recovery_thresh = getattr(self.config, "track_recovery_iou_thresh", 0.3)

        best_match_id = None
        best_iou = 0.0

        for track_id, info in self._recovery_pool.items():
            # Only match same category
            if info.get("category") != det_category:
                continue

            lost_xyxy = info.get("last_xyxy")
            if lost_xyxy is None:
                continue

            # Compute IoU
            iou = self._compute_iou(det_xyxy, lost_xyxy)
            if iou > recovery_thresh and iou > best_iou:
                best_iou = iou
                best_match_id = track_id

        if best_match_id is not None:
            logger.info(
                f"[TRACK_RECOVERED] Matched new detection to lost track {best_match_id} (IoU={best_iou:.2f})"
            )
            # Remove from recovery pool since it's recovered
            del self._recovery_pool[best_match_id]
            return best_match_id

        return None

    def _compute_iou(self, box1: np.ndarray, box2: Union[np.ndarray, List]) -> float:
        """Compute IoU between two bounding boxes in xyxy format."""
        if isinstance(box2, list):
            box2 = np.array(box2)

        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        inter_area = max(0, x2 - x1) * max(0, y2 - y1)

        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

        union_area = area1 + area2 - inter_area

        return inter_area / union_area if union_area > 0 else 0.0

    # =========================================================================
    # CUMULATIVE TRACKING STATISTICS - For accurate counting
    # =========================================================================

    @staticmethod
    def _remember_track_id(seen: "OrderedDict[int, None]", track_id: int) -> bool:
        """Record ``track_id`` in a bounded, insertion-ordered seen-set.

        Returns True if this is the first sighting (i.e. the caller should count
        it), False if the ID is already known. Evicts the oldest entry once the
        window is full -- see the _recent_track_ids comment in __init__ for why
        eviction cannot cause double-counting.
        """
        if track_id in seen:
            return False
        seen[track_id] = None
        if len(seen) > _RECENT_TRACK_ID_WINDOW:
            seen.popitem(last=False)  # evict oldest
        return True

    def _update_tracking_statistics(self, activated_stracks: List[STrack]) -> None:
        """Update cumulative tracking statistics for counting."""
        for track in activated_stracks:
            track_id = track.track_id
            category = track.cls

            # Count each ID once, on first sighting.
            if self._remember_track_id(self._recent_track_ids, track_id):
                self._total_track_count += 1

            # Same, per category.
            seen_for_cat = self._recent_category_track_ids.get(category)
            if seen_for_cat is None:
                seen_for_cat = OrderedDict()
                self._recent_category_track_ids[category] = seen_for_cat
                self._category_track_counts.setdefault(category, 0)
            if self._remember_track_id(seen_for_cat, track_id):
                self._category_track_counts[category] = (
                    self._category_track_counts.get(category, 0) + 1
                )

    def get_total_count(self) -> int:
        """Get total unique track count since tracker start."""
        return self._total_track_count

    def get_category_counts(self) -> Dict[str, int]:
        """Get unique track counts by category since tracker start."""
        return dict(self._category_track_counts)

    def get_new_tracks_this_frame(self, previous_ids: Set[int]) -> Set[int]:
        """Get track IDs that are new compared to a previous set.

        Scoped to the bounded recent-ID window (see __init__); IDs older than the
        window are no longer individually retained. Callers pass a ``previous_ids``
        snapshot taken a frame or two earlier, which is far inside that window.
        """
        return set(self._recent_track_ids) - previous_ids

    # =========================================================================
    # STATE PERSISTENCE - For preserving counts across restarts
    # =========================================================================

    def get_state_file_path(self) -> str:
        """Get the file path for state persistence."""
        import tempfile

        # Use MATRICE_STATE_DIR env var, or system temp directory as fallback
        default_dir = os.path.join(tempfile.gettempdir(), "matrice_analytics")
        base_dir = os.environ.get("MATRICE_STATE_DIR", default_dir)
        os.makedirs(base_dir, exist_ok=True)
        namespace_suffix = f"_{self.namespace}" if self.namespace else ""
        return os.path.join(base_dir, f"tracker_state{namespace_suffix}.json")

    def save_state(self) -> bool:
        """
        Save tracker state to persistent storage.

        This preserves count accuracy across restarts or tracker recreation.

        Returns:
            bool: True if state was saved successfully
        """
        if not getattr(self.config, "enable_state_persistence", True):
            return False

        try:
            state = {
                "version": "1.1",
                "timestamp": time.time(),
                "monotonic_timestamp": time.monotonic(),
                "namespace": self.namespace,
                "frame_id": self.frame_id,
                # v1.1: cumulative counts are persisted as integers, and only the
                # bounded recent-ID window is persisted as a list -- v1.0 wrote every
                # ID ever seen, so this file grew without limit. restore_state()
                # still reads the v1.0 keys, so older state files load unchanged.
                "total_track_count": self._total_track_count,
                "category_track_counts": dict(self._category_track_counts),
                "recent_track_ids": list(self._recent_track_ids),
                "recent_category_track_ids": {
                    cat: list(ids) for cat, ids in self._recent_category_track_ids.items()
                },
                "recovery_pool": self._recovery_pool,
                "track_aliases": {str(k): v for k, v in self._track_aliases.items()},
                "id_counter": BaseTrack._id_counters.get(self.namespace, 0)
                if self.namespace
                else BaseTrack._count,
            }

            file_path = self.get_state_file_path()
            with open(file_path, "w") as f:
                json.dump(state, f, indent=2)

            logger.info(
                f"[STATE_SAVED] Saved tracker state to {file_path} "
                f"(total_tracks={self._total_track_count}, frame={self.frame_id})"
            )
            return True

        except (OSError, TypeError, ValueError) as e:
            logger.error(f"[STATE_SAVE_ERROR] Failed to save tracker state: {e}")
            return False

    def restore_state(self) -> bool:
        """
        Restore tracker state from persistent storage.

        Call this after creating a new tracker instance to recover accumulated counts.

        Returns:
            bool: True if state was restored successfully
        """
        if not getattr(self.config, "enable_state_persistence", True):
            return False

        try:
            file_path = self.get_state_file_path()

            if not os.path.exists(file_path):
                logger.info(f"[STATE_RESTORE] No saved state found at {file_path}")
                return False

            with open(file_path, "r") as f:
                state = json.load(f)

            # Check if state matches this namespace
            if state.get("namespace") != self.namespace:
                logger.warning(
                    f"[STATE_RESTORE] Namespace mismatch: saved={state.get('namespace')}, current={self.namespace}"
                )
                return False

            # Check if state is recent enough.
            #
            # This is a cross-process comparison, so it must use the wall clock --
            # monotonic() is only comparable within a single process lifetime and a
            # restore by definition spans a restart. A backwards wall-clock step
            # (NTP correction, VM restore) can therefore make state_age negative;
            # clamp at 0 so "the file appears to come from the future" reads as
            # "brand new" and restores, rather than sailing past the expiry check
            # with a nonsensical negative age.
            state_age = max(0.0, time.time() - state.get("timestamp", 0))  # nosemgrep
            expiry_seconds = getattr(self.config, "state_expiry_seconds", 3600.0)
            if state_age > expiry_seconds:
                logger.warning(
                    f"[STATE_RESTORE] Saved state is {state_age / 60:.1f} minutes old, skipping restore"
                )
                return False

            # Restore state. v1.1 persists exact counts plus a bounded recent-ID
            # window; v1.0 persisted every ID ever seen, so fall back to deriving
            # both from those lists when loading an older file.
            if "total_track_count" in state:
                self._total_track_count = int(state.get("total_track_count", 0))
                self._category_track_counts = {
                    cat: int(n) for cat, n in state.get("category_track_counts", {}).items()
                }
                recent_ids = state.get("recent_track_ids", [])
                recent_by_cat = state.get("recent_category_track_ids", {})
            else:
                recent_ids = state.get("all_track_ids", [])
                recent_by_cat = state.get("category_track_ids", {})
                self._total_track_count = len(recent_ids)
                self._category_track_counts = {cat: len(ids) for cat, ids in recent_by_cat.items()}

            # Keep only the newest window's worth, preserving insertion order.
            self._recent_track_ids = OrderedDict.fromkeys(recent_ids[-_RECENT_TRACK_ID_WINDOW:])
            self._recent_category_track_ids = {
                cat: OrderedDict.fromkeys(ids[-_RECENT_TRACK_ID_WINDOW:])
                for cat, ids in recent_by_cat.items()
            }
            # The recovery pool's "lost_time" is a monotonic() stamp, which is only
            # meaningful inside the process that wrote it. Rebase every restored
            # entry onto THIS process's clock, preserving each entry's real age
            # (measured with the wall clock, the only cross-process reference we
            # have) so the recovery window still expires them correctly. Without
            # this, a restored stamp from another process is an arbitrary number
            # and entries expire immediately or effectively never.
            self._recovery_pool = state.get("recovery_pool", {})
            saved_monotonic = state.get("monotonic_timestamp")
            if self._recovery_pool:
                now_monotonic = time.monotonic()
                for info in self._recovery_pool.values():
                    if saved_monotonic is None:
                        # v1.0 file: "lost_time" was a wall-clock stamp.
                        entry_age = max(0.0, time.time() - info.get("lost_time", 0))  # nosemgrep
                    else:
                        # v1.1: age within the writing process, plus the gap since.
                        entry_age = max(0.0, saved_monotonic - info.get("lost_time", 0)) + state_age
                    info["lost_time"] = now_monotonic - entry_age
            self._track_aliases = {int(k): v for k, v in state.get("track_aliases", {}).items()}

            # Restore ID counter to prevent ID collisions
            saved_id_counter = state.get("id_counter", 0)
            if self.namespace:
                BaseTrack._id_counters[self.namespace] = saved_id_counter
            else:
                BaseTrack._count = saved_id_counter

            # Restore frame ID
            self.frame_id = state.get("frame_id", 0)

            logger.info(
                f"[STATE_RESTORED] Restored tracker state from {file_path} "
                f"(total_tracks={self._total_track_count}, frame={self.frame_id})"
            )
            return True

        except (OSError, TypeError, ValueError) as e:
            logger.error(f"[STATE_RESTORE_ERROR] Failed to restore tracker state: {e}")
            return False

    def clear_saved_state(self) -> bool:
        """
        Clear saved tracker state (use when intentionally resetting counts).

        Returns:
            bool: True if state was cleared successfully
        """
        try:
            file_path = self.get_state_file_path()
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"[STATE_CLEARED] Removed saved state at {file_path}")
            return True
        except OSError as e:
            logger.error(f"[STATE_CLEAR_ERROR] Failed to clear saved state: {e}")
            return False

    def _maybe_save_state(self) -> None:
        """Save state periodically based on config."""
        if not getattr(self.config, "enable_state_persistence", True):
            return

        save_interval = getattr(self.config, "state_save_interval", 300)
        if self.frame_id - self._last_state_save_frame >= save_interval:
            self.save_state()
            self._last_state_save_frame = self.frame_id

    # =========================================================================
    # PER-FRAME TIME BASE (SG-24) - the frame's own timestamp drives dt/ageing
    # =========================================================================

    def _frame_dt(self, timestamp: Optional[float]) -> Optional[float]:
        """Interval in seconds between this frame and the previous timed frame.

        Returns ``None`` whenever the per-frame time base cannot be used for this
        frame — no timestamp supplied, a non-finite value, or a non-monotonic one
        (stream restart/seek). The caller then falls back to counting frames at
        the effective fps, which is the historical behaviour. Every fallback is
        logged; none of them is taken silently.
        """
        if timestamp is None:
            if self._using_frame_timestamps:
                logger.warning(
                    "[FRAME_DT] frame %d arrived without a timestamp after a timed run; "
                    "reverting to the frame-counting time base",
                    self.frame_id,
                )
                self._using_frame_timestamps = False
                self._last_frame_ts = None
            self._last_frame_dt = None
            return None

        try:
            ts = float(timestamp)
        except (TypeError, ValueError):
            logger.warning(
                "[FRAME_DT] frame %d carried a non-numeric timestamp (%r); "
                "falling back to the frame-counting time base",
                self.frame_id,
                timestamp,
            )
            self._last_frame_dt = None
            return None

        if not math.isfinite(ts):
            logger.warning(
                "[FRAME_DT] frame %d carried a non-finite timestamp (%r); "
                "falling back to the frame-counting time base",
                self.frame_id,
                timestamp,
            )
            self._last_frame_dt = None
            return None

        prev = self._last_frame_ts
        self._last_frame_ts = ts
        if not self._using_frame_timestamps:
            logger.info(
                "[FRAME_DT] frame %d: driving the tracker time base from per-frame timestamps",
                self.frame_id,
            )
            self._using_frame_timestamps = True

        if prev is None:
            # First timed frame: an origin, not yet an interval.
            self._last_frame_dt = None
            return None

        dt = ts - prev
        if dt <= 0.0:
            self._non_monotonic_ts_count += 1
            # Rate-limited: a resetting source would otherwise log every frame.
            if self._non_monotonic_ts_count == 1 or self._non_monotonic_ts_count % 100 == 0:
                logger.warning(
                    "[FRAME_DT] non-monotonic frame timestamp at frame %d (%.6fs -> %.6fs, %d so far); "
                    "falling back to the frame-counting time base for this frame",
                    self.frame_id,
                    prev,
                    ts,
                    self._non_monotonic_ts_count,
                )
            self._last_frame_dt = None
            return None

        self._last_frame_dt = dt
        return dt

    def _nominal_dt(self) -> float:
        """One frame's worth of seconds at the current effective fps."""
        return 1.0 / max(self._effective_fps, 1e-6)

    def _advance_stream_time(self, dt: Optional[float]) -> None:
        """Advance the stream clock by this frame's interval and record it.

        ``_frame_times`` maps frame_id -> stream time so ageing can be expressed
        in seconds without touching ``STrack`` (``end_frame`` stays the only
        per-track bookmark). It is pruned by time, so a frame_id that has fallen
        out of it is by construction older than any grace the tracker applies.
        """
        if dt is None:
            dt = self._nominal_dt()
        self._stream_time += dt
        self._frame_times[self.frame_id] = self._stream_time
        self._prune_frame_times()

    def _frame_time_horizon(self) -> float:
        """How far back frame->time bookmarks must be retained, in seconds."""
        recovery = float(getattr(self.config, "track_recovery_time_window", 30.0) or 0.0)
        return max(self._lost_grace_seconds(), recovery) * 2.0 + 10.0

    def _prune_frame_times(self) -> None:
        """Drop frame->time bookmarks older than the horizon (oldest first)."""
        cutoff = self._stream_time - self._frame_time_horizon()
        while self._frame_times:
            oldest_frame = next(iter(self._frame_times))
            if self._frame_times[oldest_frame] >= cutoff:
                break
            del self._frame_times[oldest_frame]

    def _elapsed_since_frame(self, frame_id: int) -> float:
        """Seconds of stream time since ``frame_id``.

        An unknown past frame_id was pruned, which means it is older than the
        retention horizon and therefore older than any grace — ``inf`` is the
        correct answer, not a guess.
        """
        recorded = self._frame_times.get(int(frame_id))
        if recorded is None:
            return 0.0 if frame_id >= self.frame_id else float("inf")
        return self._stream_time - recorded

    # =========================================================================
    # FPS ADAPTATION - auto-detect frame-rate and rescale time-dependent params
    # (ported from CCTVTracker; opt-in via config.enable_fps_adaptation)
    # =========================================================================

    def _lost_grace_seconds(self) -> float:
        """Lost-track grace in SECONDS. An explicit ``grace_period_sec`` wins,
        otherwise ``max_lost_seconds`` (which ``TrackerConfig`` derives from a
        caller-supplied ``max_time_lost`` when one was given, so an existing
        max_time_lost=1800 at reference_fps=30 still means exactly 60 s)."""
        grace = self.config.grace_period_sec
        if grace is None:
            grace = self.config.max_lost_seconds
        return float(grace)

    # Back-compat alias: the pre-SG-24 name, kept because tests and the
    # adaptation math both refer to it.
    def _grace_period_sec(self) -> float:
        """Deprecated alias for :meth:`_lost_grace_seconds`."""
        return self._lost_grace_seconds()

    def _propagation_dt(self, dt: float, ref: float) -> float:
        """Clamp the Kalman propagation step to ``config.max_extrapolation_sec``.

        ``dt`` here is in REFERENCE FRAMES (``reference_fps / fps``), which is
        the unit the motion matrix works in; the ceiling is in seconds, so it
        converts as ``ceiling * ref``. ``None`` (the default) means no bound and
        returns ``dt`` unchanged, so the pre-existing behaviour is byte-identical.

        Only the constant-velocity term is bounded. The lost-track grace and the
        low-fps threshold blend keep the true measured interval, because those
        are correct at any gap length — it is only the *mean displacement* that
        goes wrong, and it goes wrong because ``KalmanFilter.predict`` scales F
        by dt without scaling the process noise by dt: past a second or so the
        predicted box has moved a long way with an unchanged uncertainty
        ellipse, so IoU association reports a miss instead of a widened gate.
        """
        ceiling = self.config.max_extrapolation_sec
        if ceiling is None:
            return dt
        return min(dt, float(ceiling) * ref)

    def _compute_adaptation(self, fps: float) -> Dict[str, float]:
        """Pure math: map a measured fps to the rescaled params. Side-effect free
        so it can be unit-tested without touching the clock or tracker state.

        Mirrors CCTVTracker._apply_fps_params: thresholds blend from the cached
        BASE values toward the low-fps floors (never compounding), Kalman dt is
        reference_fps/fps, and the lost grace becomes time-based."""
        fps = min(
            max(float(fps), float(self.config.min_detected_fps)),
            float(self.config.max_detected_fps),
        )
        ref = float(self.config.reference_fps)
        fps_factor = min(1.0, fps / ref)
        return {
            "fps": fps,
            "dt": self._propagation_dt(ref / fps, ref),
            "fps_factor": fps_factor,
            "match_thresh": (
                self._base_match_thresh * fps_factor
                + (1.0 - fps_factor) * self.config.match_thresh_low_fps_floor
            ),
            "new_track_thresh": (
                self._base_new_track_thresh * fps_factor
                + (1.0 - fps_factor) * self.config.new_track_thresh_low_fps_floor
            ),
            "max_time_lost": max(1, int(self._grace_period_sec() * fps)),
        }

    def _apply_adaptation(self, fps: float) -> None:
        """Apply a computed adaptation: rescale this tracker's Kalman dt and the
        time-dependent thresholds. Only touches THIS tracker's filter instance
        (multi_predict/multi_kf_update both use it), never STrack.shared_kalman,
        so cameras adapting independently don't interfere."""
        a = self._compute_adaptation(fps)
        self._effective_fps = a["fps"]
        self.kalman_filter.set_dt(a["dt"])
        # Effective thresholds are held on the INSTANCE (read by the association
        # steps), never written back into self.config — so sharing one config
        # across trackers is safe. Blended from cached bases (no compounding).
        self._match_thresh = a["match_thresh"]
        self._new_track_thresh = a["new_track_thresh"]
        self.max_time_lost = int(a["max_time_lost"])
        self._recompute_confirm_params()

    def _maybe_adapt_fps(self, dt: Optional[float] = None) -> None:
        """Re-adapt the time-dependent params to this frame's real interval.

        Two estimators, in order of preference:

        1. ``dt`` — the interval taken from the frame's OWN timestamp. This is
           the correct estimator and is used per frame, with no drift gate and
           no rate limit: a sampler's drop pattern is bursty, and it is exactly
           the isolated 2-second gap that breaks association. Damping the
           response would reintroduce the bug this replaced.
        2. ``time.monotonic()`` spacing averaged over the last 30 update() calls
           — the legacy estimator, kept only for callers that cannot supply a
           per-frame timestamp. An average over a bursty stream reports the mean
           rate and is blind to the gaps, so it is a fallback, not a design.

        FULLY gated: with enable_fps_adaptation off (default) this returns before
        touching either clock, so the core path stays deterministic and the
        30-sample clock buffer is never populated.
        """
        if not self.config.enable_fps_adaptation:
            return

        if dt is not None:
            # Per-frame dt path: this frame's interval IS the effective interval.
            measured = min(
                max(1.0 / dt, float(self.config.min_detected_fps)),
                float(self.config.max_detected_fps),
            )
            if abs(measured - self._effective_fps) <= 1e-9:
                return  # already adapted to exactly this rate; nothing to do
            self._apply_adaptation(measured)
            logger.debug(
                "[FPS_ADAPT] dt=%.4fs -> fps=%.2f, kalman dt=%.3f",
                dt,
                measured,
                self.kalman_filter._dt,
            )
            return

        now = time.monotonic()
        self._fps_samples.append(now)
        if len(self._fps_samples) < 5:
            return
        # Re-adapt at most ~once per second to avoid thrashing.
        if self._last_adapt_ts is not None and (now - self._last_adapt_ts) < 1.0:
            return

        intervals = np.diff(np.asarray(self._fps_samples, dtype=np.float64))
        mean_interval = float(np.mean(intervals)) if len(intervals) else 0.0
        if mean_interval <= 0:
            return
        # Clamp to a plausible camera range. Offline/batch replay feeds frames back
        # to back, so raw wall-clock spacing can imply thousands of fps — which
        # would drive dt toward 0 (tracks stop predicting) and max_time_lost into
        # the millions (lost tracks never pruned). _compute_adaptation clamps too;
        # doing it here as well keeps _effective_fps and the drift gate in range.
        measured = min(
            max(1.0 / mean_interval, float(self.config.min_detected_fps)),
            float(self.config.max_detected_fps),
        )

        # Only adapt on a >20% change vs the current effective fps.
        if abs(measured - self._effective_fps) / max(self._effective_fps, 1.0) <= 0.2:
            return

        self._last_adapt_ts = now
        self._apply_adaptation(measured)
        logger.debug(f"[FPS_ADAPT] measured={measured:.2f} -> dt={self.kalman_filter._dt:.3f}")

    # =========================================================================
    # TEMPORAL CONFIRMATION - ghost suppression via a sliding-window hit buffer
    # (ported from CCTVTracker; opt-in via config.enable_temporal_confirmation)
    # =========================================================================

    def _recompute_confirm_params(self) -> None:
        """Derive the confirmation window (frames) and min-hits from the effective
        fps. Resizes any existing hit buffers when the window changes (fps adapt),
        preserving their most recent hits."""
        window = max(2, int(self.config.confirm_window_sec * self._effective_fps))
        self._confirm_window = window
        self._confirm_min_hits = max(1, int(window * self.config.confirm_min_hits_ratio))
        if self._hit_buffers:
            for tid, buf in list(self._hit_buffers.items()):
                if buf.maxlen != window:
                    self._hit_buffers[tid] = deque(buf, maxlen=window)

    def _temporal_filter(self, active_stracks: List[STrack]) -> List[STrack]:
        """Return only tracks confirmed by the sliding-window hit test.

        Mirrors CCTVTracker._temporal_filter: append 1 for ids seen this frame and
        0 for known-but-unseen ids, confirm an id once it is hit in >= min_hits of
        the last `window` frames, prune all-zero (dead) buffers. Confirmation gates
        emission/counting only — the caller's internal track lists are untouched."""
        window = self._confirm_window
        min_hits = self._confirm_min_hits
        active_ids = {t.track_id for t in active_stracks}

        # Record this frame's hit for seen ids (creating buffers for new ids)...
        for tid in active_ids:
            buf = self._hit_buffers.get(tid)
            if buf is None:
                buf = deque(maxlen=window)
                self._hit_buffers[tid] = buf
            buf.append(1)
        # ...and a miss for every known id not seen this frame.
        for tid, buf in self._hit_buffers.items():
            if tid not in active_ids:
                buf.append(0)

        # Recompute the confirmed set and prune dead buffers.
        confirmed: Set[int] = set()
        dead: List[int] = []
        for tid, buf in self._hit_buffers.items():
            total = sum(buf)
            if total == 0:
                dead.append(tid)
            elif total >= min_hits:
                confirmed.add(tid)
        for tid in dead:
            del self._hit_buffers[tid]

        self._confirmed_ids = confirmed
        return [t for t in active_stracks if t.track_id in confirmed]

    # =========================================================================
    # PREDICT-ONLY GAP GLIDE - advance tracks between inference frames
    # (ported from CCTVTracker; used by update([]) when enable_predict_on_empty)
    # =========================================================================

    def predict(self, timestamp: Optional[float] = None) -> List[Dict]:
        """Advance every track one frame via Kalman predict-only (no detections),
        so boxes glide smoothly on video frames rendered between inference frames.

        Returns the confirmed/active tracks (respecting temporal confirmation when
        on) plus recently-lost confirmed tracks within a short grace, converted to
        the standard detection-dict format. Does not consume detections, so it does
        not advance the temporal hit buffers (no evidence either way this frame).

        ``timestamp`` has the same meaning as on :meth:`update` — a glide frame
        still moves the stream clock, so it must be able to say by how much."""
        self.frame_id += 1
        dt = self._frame_dt(timestamp)
        self._advance_stream_time(dt)
        self._maybe_adapt_fps(dt)
        if self.namespace:
            BaseTrack.set_namespace(self.namespace)

        strack_pool = self.joint_stracks(self.tracked_stracks, self.lost_stracks)
        self.multi_predict(strack_pool)

        # Bound the glide. update([]) cannot tell "no inference this frame" from
        # "the detector genuinely saw nothing", and predict() bypasses the Step-2
        # association that normally marks unmatched tracks lost — so without this a
        # subject leaving the scene would leave a phantom box gliding off-screen
        # forever. Tracks unseen for longer than the glide grace are demoted to
        # lost here, after which the normal lost/removal machinery below applies.
        # Every real inference frame refreshes end_frame, so an interleaved
        # predict/update stream never reaches the budget.
        glide_budget_sec = float(self.config.predict_glide_grace_sec)
        stale = [
            t
            for t in self.tracked_stracks
            if self._elapsed_since_frame(t.end_frame) > glide_budget_sec
        ]
        if stale:
            stale_ids = {id(t) for t in stale}
            self.tracked_stracks = [t for t in self.tracked_stracks if id(t) not in stale_ids]
            for t in stale:
                t.mark_lost()
            self.lost_stracks.extend(stale)

        # Bound internal lost-track state over long predict-only runs (mirror the
        # Step-5 removal in _perform_tracking_update, which predict() bypasses).
        if self.lost_stracks:
            still_lost = []
            lost_grace_sec = self._lost_grace_seconds()
            for t in self.lost_stracks:
                if self._elapsed_since_frame(t.end_frame) > lost_grace_sec:
                    t.mark_removed()
                    self.removed_stracks.append(t)
                else:
                    still_lost.append(t)
            self.lost_stracks = still_lost
            if len(self.removed_stracks) > 1000:
                self.removed_stracks = self.removed_stracks[-999:]

        active_stracks = [t for t in self.tracked_stracks if t.is_activated]

        if self.config.enable_temporal_confirmation:
            emit = [t for t in active_stracks if t.track_id in self._confirmed_ids]
            short_grace_sec = 0.2
            emit += [
                t
                for t in self.lost_stracks
                if t.is_activated
                and t.track_id in self._confirmed_ids
                and self._elapsed_since_frame(t.end_frame) <= short_grace_sec
            ]
        else:
            emit = active_stracks

        # record_class_observation=False: a glide frame re-emits the last known
        # class with no new evidence behind it, so it must not vote in the
        # class-aggregation window.
        detections = self._convert_stracks_to_detections(emit, record_class_observation=False)
        # Glided boxes carry the CURRENT frame_id (they weren't .update()d, so the
        # strack's own frame_id is stale). Done on the output only, so internal
        # end_frame/grace math is untouched.
        for det in detections:
            det["frame_id"] = int(self.frame_id)
        return detections
