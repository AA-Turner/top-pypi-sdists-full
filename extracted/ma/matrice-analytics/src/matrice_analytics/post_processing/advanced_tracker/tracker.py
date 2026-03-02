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

from typing import Any, List, Optional, Tuple, Union, Dict, Set
import numpy as np
import logging
import time
import json
import os

from .base import BaseTrack, TrackState
from .config import TrackerConfig
from .kalman_filter import KalmanFilterXYAH
from .strack import STrack
from .matching import linear_assignment, iou_distance, fuse_score

logger = logging.getLogger(__name__)


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
        max_time_lost (int): The maximum frames for a track to be considered as 'lost'.
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
            self.class_aggregator = TrackClassAggregator(window_size=config.class_aggregation_window_size)
        
        # Track recovery for re-entries: stores recently removed tracks for potential re-matching
        # Structure: {track_id: {"last_xyxy": bbox, "lost_time": timestamp, "category": cat}}
        self._recovery_pool: Dict[int, Dict[str, Any]] = {}
        self._track_aliases: Dict[int, int] = {}  # Maps new IDs to recovered IDs
        
        # Cumulative tracking statistics (for accurate counting)
        self._all_track_ids: Set[int] = set()  # All track IDs ever seen
        self._category_track_ids: Dict[str, Set[int]] = {}  # Track IDs by category
        
        # State persistence
        self._last_state_save_frame = 0

    def update(self, detections: Union[List[Dict], Dict[str, List[Dict]]], 
               img: Optional[np.ndarray] = None) -> Union[List[Dict], Dict[str, List[Dict]]]:
        """
        Update the tracker with new detections and return the current list of tracked objects.

        Args:
            detections: Detection results in various formats:
                - List[Dict]: Single frame detections
                - Dict[str, List[Dict]]: Multi-frame detections with frame keys
            img: Optional image for motion compensation

        Returns:
            Tracking results in the same format as input
        """
        self.frame_id += 1
        
        # Handle different input formats
        if isinstance(detections, dict):
            # Multi-frame format
            return self._update_multi_frame(detections, img)
        else:
            # Single frame format
            return self._update_single_frame(detections, img)

    def _update_single_frame(self, detections: List[Dict], img: Optional[np.ndarray] = None) -> List[Dict]:
        """Update tracker with single frame detections."""
        # Convert detections to STrack format
        stracks = self._convert_detections_to_stracks(detections)
        
        # Perform tracking update
        tracked_objects = self._perform_tracking_update(stracks, img)
        
        # Convert back to detection format
        return self._convert_stracks_to_detections(tracked_objects)

    def _update_multi_frame(self, detections: Dict[str, List[Dict]], 
                           img: Optional[np.ndarray] = None) -> Dict[str, List[Dict]]:
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
            bbox = det.get('bounding_box', {})
            if 'x' in bbox and 'y' in bbox and 'width' in bbox and 'height' in bbox:
                # Center format
                x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            elif 'xmin' in bbox and 'ymin' in bbox and 'xmax' in bbox and 'ymax' in bbox:
                # Corner format
                x = (bbox['xmin'] + bbox['xmax']) / 2
                y = (bbox['ymin'] + bbox['ymax']) / 2
                w = bbox['xmax'] - bbox['xmin']
                h = bbox['ymax'] - bbox['ymin']
            else:
                # Try to extract from any format
                values = list(bbox.values())
                if len(values) >= 4:
                    x, y, w, h = values[0], values[1], values[2], values[3]
                else:
                    continue
            
            # Extract other properties
            score = det.get('confidence', 0.0)
            category = det.get('category', 'unknown')
            
            # Create STrack
            xywh = [x, y, w, h, i]  # Add index as last element
            strack = STrack(xywh, score, category)
            
            # CRITICAL FIX: Store the original detection data to preserve all fields
            # This ensures face recognition fields (embedding, landmarks, etc.) are preserved
            strack.original_detection = det.copy()
            
            stracks.append(strack)
        
        return stracks

    def _convert_stracks_to_detections(self, stracks: List[STrack]) -> List[Dict]:
        """Convert STrack objects back to detection format."""
        detections = []
        
        for strack in stracks:
            if strack.is_activated:
                # Get bounding box in xyxy format
                xyxy = strack.xyxy
                
                # CRITICAL FIX: Start with original detection data to preserve all fields
                if hasattr(strack, 'original_detection') and strack.original_detection:
                    # Start with the original detection to preserve all face recognition fields
                    detection = strack.original_detection.copy()
                    
                    # Update with tracking-specific fields
                    detection['bounding_box'] = {
                        'xmin': float(xyxy[0]),
                        'ymin': float(xyxy[1]),
                        'xmax': float(xyxy[2]),
                        'ymax': float(xyxy[3])
                    }
                    detection['confidence'] = float(strack.score)
                    detection['category'] = strack.cls
                    detection['track_id'] = int(strack.track_id)
                    detection['frame_id'] = int(strack.frame_id)
                else:
                    # Fallback to minimal detection if original data not available
                    detection = {
                        'bounding_box': {
                            'xmin': float(xyxy[0]),
                            'ymin': float(xyxy[1]),
                            'xmax': float(xyxy[2]),
                            'ymax': float(xyxy[3])
                        },
                        'confidence': float(strack.score),
                        'category': strack.cls,
                        'track_id': int(strack.track_id),
                        'frame_id': int(strack.frame_id)
                    }
                
                detections.append(detection)

        if self.class_aggregator is not None:
            for detection in detections:
                aggregated_class = self.class_aggregator.update_and_aggregate(
                    track_id=detection['track_id'],
                    observed_class=detection['category']
                )
                detection['category'] = aggregated_class
            
        return detections

    def _perform_tracking_update(self, detections: List[STrack],
                                img: Optional[np.ndarray] = None) -> List[STrack]:
        """Perform the core tracking update algorithm."""
        # Ensure namespace is set for any new track ID generation
        if self.namespace:
            BaseTrack.set_namespace(self.namespace)

        activated_stracks = []
        refind_stracks = []
        lost_stracks = []
        removed_stracks = []

        # Separate high and low confidence detections
        scores = np.array([det.score for det in detections])
        remain_inds = scores >= self.config.track_high_thresh
        inds_low = scores > self.config.track_low_thresh
        inds_high = scores < self.config.track_high_thresh

        inds_second = inds_low & inds_high
        dets_second = [detections[i] for i in range(len(detections)) if inds_second[i]]
        dets = [detections[i] for i in range(len(detections)) if remain_inds[i]]
        scores_keep = scores[remain_inds]
        scores_second = scores[inds_second]

        # Step 1: First association, with high score detection boxes
        unconfirmed = []
        tracked_stracks = []
        for track in self.tracked_stracks:
            if not track.is_activated:
                unconfirmed.append(track)
            else:
                tracked_stracks.append(track)

        # Predict the current location with KF
        strack_pool = self.joint_stracks(tracked_stracks, self.lost_stracks)
        self.multi_predict(strack_pool)

        # Calculate distances and perform matching
        dists = self.get_dists(strack_pool, dets)
        matches, u_track, u_detection = linear_assignment(dists, thresh=self.config.match_thresh)

        for itracked, idet in matches:
            track = strack_pool[itracked]
            det = dets[idet]
            if track.state == TrackState.Tracked:
                track.update(det, self.frame_id)
                activated_stracks.append(track)
            else:
                track.re_activate(det, self.frame_id, new_id=False)
                refind_stracks.append(track)

        # Step 2: Second association, with low score detection boxes
        # Uses secondary_match_thresh (configurable, default 0.5) for IoU-only matching
        r_tracked_stracks = [strack_pool[i] for i in u_track if strack_pool[i].state == TrackState.Tracked]
        dists = iou_distance(r_tracked_stracks, dets_second)
        secondary_thresh = getattr(self.config, 'secondary_match_thresh', 0.5)
        matches, u_track, u_detection_second = linear_assignment(dists, thresh=secondary_thresh)

        for itracked, idet in matches:
            track = r_tracked_stracks[itracked]
            det = dets_second[idet]
            if track.state == TrackState.Tracked:
                track.update(det, self.frame_id)
                activated_stracks.append(track)
            else:
                track.re_activate(det, self.frame_id, new_id=False)
                refind_stracks.append(track)

        for it in u_track:
            track = r_tracked_stracks[it]
            if track.state != TrackState.Lost:
                track.mark_lost()
                lost_stracks.append(track)

        # Step 3: Deal with unconfirmed tracks
        # Uses unconfirmed_match_thresh (configurable, default 0.7)
        detections = [dets[i] for i in u_detection]
        dists = self.get_dists(unconfirmed, detections)
        unconfirmed_thresh = getattr(self.config, 'unconfirmed_match_thresh', 0.7)
        matches, u_unconfirmed, u_detection = linear_assignment(dists, thresh=unconfirmed_thresh)

        for itracked, idet in matches:
            unconfirmed[itracked].update(detections[idet], self.frame_id)
            activated_stracks.append(unconfirmed[itracked])

        for it in u_unconfirmed:
            track = unconfirmed[it]
            track.mark_removed()
            removed_stracks.append(track)

        # Step 4: Init new stracks (with track recovery attempt)
        for inew in u_detection:
            track = detections[inew]
            if track.score < self.config.new_track_thresh:
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

        # Step 5: Update state
        for track in self.lost_stracks:
            if self.frame_id - track.end_frame > self.max_time_lost:
                track.mark_removed()
                removed_stracks.append(track)

        self.tracked_stracks = [t for t in self.tracked_stracks if t.state == TrackState.Tracked]
        self.tracked_stracks = self.joint_stracks(self.tracked_stracks, activated_stracks)
        self.tracked_stracks = self.joint_stracks(self.tracked_stracks, refind_stracks)
        self.lost_stracks = self.sub_stracks(self.lost_stracks, self.tracked_stracks)
        self.lost_stracks.extend(lost_stracks)
        self.lost_stracks = self.sub_stracks(self.lost_stracks, self.removed_stracks)
        self.tracked_stracks, self.lost_stracks = self.remove_duplicate_stracks(self.tracked_stracks, self.lost_stracks)
        self.removed_stracks.extend(removed_stracks)
        
        if len(self.removed_stracks) > 1000:
            self.removed_stracks = self.removed_stracks[-999:]
        
        # Clean up aggregator windows for removed tracks
        if self.class_aggregator is not None and removed_stracks:
            self.class_aggregator.remove_tracks([t.track_id for t in removed_stracks])

        # Update recovery pool with removed tracks for potential re-identification
        if removed_stracks:
            self._update_recovery_pool(removed_stracks)
        
        # Update cumulative tracking statistics
        active_stracks = [x for x in self.tracked_stracks if x.is_activated]
        self._update_tracking_statistics(active_stracks)
        
        # Periodically save state
        self._maybe_save_state()

        return active_stracks

    def get_kalmanfilter(self) -> KalmanFilterXYAH:
        """Return a Kalman filter object for tracking bounding boxes using KalmanFilterXYAH."""
        return KalmanFilterXYAH()

    def get_dists(self, tracks: List[STrack], detections: List[STrack]) -> np.ndarray:
        """Calculate the distance between tracks and detections using IoU and optionally fuse scores."""
        dists = iou_distance(tracks, detections)
        if self.config.fuse_score:
            dists = fuse_score(dists, detections)
        return dists

    def multi_predict(self, tracks: List[STrack]):
        """Predict the next states for multiple tracks using Kalman filter."""
        STrack.multi_predict(tracks)

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
        self.kalman_filter = self.get_kalmanfilter()
        # Ensure namespace is set before reset
        if self.namespace:
            BaseTrack.set_namespace(self.namespace)
        self.reset_id()

        if self.class_aggregator is not None:
            self.class_aggregator.reset()

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

    def remove_duplicate_stracks(self, stracksa: List[STrack], stracksb: List[STrack]) -> Tuple[List[STrack], List[STrack]]:
        """Remove duplicate stracks from two lists based on Intersection over Union (IoU) distance.

        Uses the configurable duplicate_removal_iou_thresh from config.
        Higher thresholds are more permissive (reduce false duplicates).
        Lower thresholds are more aggressive (remove more duplicates).
        """
        pdist = iou_distance(stracksa, stracksb)
        # Use configurable threshold (default 0.3, was hardcoded 0.15)
        dup_thresh = getattr(self.config, 'duplicate_removal_iou_thresh', 0.3)
        pairs = np.where(pdist < dup_thresh)
        dupa, dupb = [], []
        for p, q in zip(*pairs):
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
        if not getattr(self.config, 'enable_track_recovery', True):
            return
            
        now = time.time()
        recovery_window = getattr(self.config, 'track_recovery_time_window', 30.0)
        
        # Clean up expired entries
        expired_ids = [
            tid for tid, info in self._recovery_pool.items()
            if now - info.get("lost_time", 0) > recovery_window
        ]
        for tid in expired_ids:
            del self._recovery_pool[tid]
        
        # Add newly removed tracks
        for track in removed_stracks:
            self._recovery_pool[track.track_id] = {
                "last_xyxy": track.xyxy.tolist() if hasattr(track.xyxy, 'tolist') else list(track.xyxy),
                "lost_time": now,
                "category": track.cls,
                "score": track.score
            }
            logger.debug(f"[RECOVERY_POOL] Added track {track.track_id} to recovery pool")
    
    def _try_recover_track(self, detection: STrack) -> Optional[int]:
        """
        Try to match a new detection to a recently lost track.
        
        Returns the recovered track ID if a match is found, None otherwise.
        """
        if not getattr(self.config, 'enable_track_recovery', True):
            return None
            
        if not self._recovery_pool:
            return None
        
        det_xyxy = detection.xyxy
        det_category = detection.cls
        recovery_thresh = getattr(self.config, 'track_recovery_iou_thresh', 0.3)
        
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
            logger.info(f"[TRACK_RECOVERED] Matched new detection to lost track {best_match_id} (IoU={best_iou:.2f})")
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
    
    def _update_tracking_statistics(self, activated_stracks: List[STrack]) -> None:
        """Update cumulative tracking statistics for counting."""
        for track in activated_stracks:
            track_id = track.track_id
            category = track.cls
            
            # Track all IDs ever seen
            self._all_track_ids.add(track_id)
            
            # Track IDs by category
            if category not in self._category_track_ids:
                self._category_track_ids[category] = set()
            self._category_track_ids[category].add(track_id)
    
    def get_total_count(self) -> int:
        """Get total unique track count since tracker start."""
        return len(self._all_track_ids)
    
    def get_category_counts(self) -> Dict[str, int]:
        """Get unique track counts by category since tracker start."""
        return {cat: len(ids) for cat, ids in self._category_track_ids.items()}
    
    def get_new_tracks_this_frame(self, previous_ids: Set[int]) -> Set[int]:
        """Get track IDs that are new compared to a previous set."""
        return self._all_track_ids - previous_ids
    
    # =========================================================================
    # STATE PERSISTENCE - For preserving counts across restarts
    # =========================================================================
    
    def get_state_file_path(self) -> str:
        """Get the file path for state persistence."""
        import tempfile
        # Use MATRICE_STATE_DIR env var, or system temp directory as fallback
        default_dir = os.path.join(tempfile.gettempdir(), 'matrice_analytics')
        base_dir = os.environ.get('MATRICE_STATE_DIR', default_dir)
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
        if not getattr(self.config, 'enable_state_persistence', True):
            return False
            
        try:
            state = {
                "version": "1.0",
                "timestamp": time.time(),
                "namespace": self.namespace,
                "frame_id": self.frame_id,
                "all_track_ids": list(self._all_track_ids),
                "category_track_ids": {
                    cat: list(ids) for cat, ids in self._category_track_ids.items()
                },
                "recovery_pool": self._recovery_pool,
                "track_aliases": {str(k): v for k, v in self._track_aliases.items()},
                "id_counter": BaseTrack._id_counters.get(self.namespace, 0) if self.namespace else BaseTrack._count
            }
            
            file_path = self.get_state_file_path()
            with open(file_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"[STATE_SAVED] Saved tracker state to {file_path} "
                       f"(total_tracks={len(self._all_track_ids)}, frame={self.frame_id})")
            return True
            
        except Exception as e:
            logger.error(f"[STATE_SAVE_ERROR] Failed to save tracker state: {e}")
            return False
    
    def restore_state(self) -> bool:
        """
        Restore tracker state from persistent storage.
        
        Call this after creating a new tracker instance to recover accumulated counts.
        
        Returns:
            bool: True if state was restored successfully
        """
        if not getattr(self.config, 'enable_state_persistence', True):
            return False
            
        try:
            file_path = self.get_state_file_path()
            
            if not os.path.exists(file_path):
                logger.info(f"[STATE_RESTORE] No saved state found at {file_path}")
                return False
            
            with open(file_path, 'r') as f:
                state = json.load(f)
            
            # Check if state matches this namespace
            if state.get("namespace") != self.namespace:
                logger.warning(f"[STATE_RESTORE] Namespace mismatch: saved={state.get('namespace')}, current={self.namespace}")
                return False
            
            # Check if state is recent enough
            state_age = time.time() - state.get("timestamp", 0)
            expiry_seconds = getattr(self.config, 'state_expiry_seconds', 3600.0)
            if state_age > expiry_seconds:
                logger.warning(f"[STATE_RESTORE] Saved state is {state_age/60:.1f} minutes old, skipping restore")
                return False
            
            # Restore state
            self._all_track_ids = set(state.get("all_track_ids", []))
            self._category_track_ids = {
                cat: set(ids) for cat, ids in state.get("category_track_ids", {}).items()
            }
            self._recovery_pool = state.get("recovery_pool", {})
            self._track_aliases = {
                int(k): v for k, v in state.get("track_aliases", {}).items()
            }
            
            # Restore ID counter to prevent ID collisions
            saved_id_counter = state.get("id_counter", 0)
            if self.namespace:
                BaseTrack._id_counters[self.namespace] = saved_id_counter
            else:
                BaseTrack._count = saved_id_counter
            
            # Restore frame ID
            self.frame_id = state.get("frame_id", 0)
            
            logger.info(f"[STATE_RESTORED] Restored tracker state from {file_path} "
                       f"(total_tracks={len(self._all_track_ids)}, frame={self.frame_id})")
            return True
            
        except Exception as e:
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
        except Exception as e:
            logger.error(f"[STATE_CLEAR_ERROR] Failed to clear saved state: {e}")
            return False
    
    def _maybe_save_state(self) -> None:
        """Save state periodically based on config."""
        if not getattr(self.config, 'enable_state_persistence', True):
            return
            
        save_interval = getattr(self.config, 'state_save_interval', 300)
        if self.frame_id - self._last_state_save_frame >= save_interval:
            self.save_state()
            self._last_state_save_frame = self.frame_id