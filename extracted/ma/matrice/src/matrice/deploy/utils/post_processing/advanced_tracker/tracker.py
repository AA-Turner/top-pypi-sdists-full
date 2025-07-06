"""
Advanced tracker implementation.

This module provides the AdvancedTracker class that implements BYTETracker-like
functionality for object tracking with support for various input formats.
"""

from typing import Any, List, Optional, Tuple, Union, Dict
import numpy as np
import logging

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
    """

    def __init__(self, config: TrackerConfig):
        """
        Initialize an AdvancedTracker instance for object tracking.

        Args:
            config (TrackerConfig): Tracker configuration object.
        """
        self.tracked_stracks = []  # type: List[STrack]
        self.lost_stracks = []  # type: List[STrack]
        self.removed_stracks = []  # type: List[STrack]

        self.frame_id = 0
        self.config = config
        self.max_time_lost = config.max_time_lost
        self.kalman_filter = self.get_kalmanfilter()
        self.reset_id()

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
            stracks.append(strack)
        
        return stracks

    def _convert_stracks_to_detections(self, stracks: List[STrack]) -> List[Dict]:
        """Convert STrack objects back to detection format."""
        detections = []
        
        for strack in stracks:
            if strack.is_activated:
                # Get bounding box in xyxy format
                xyxy = strack.xyxy
                
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
        
        return detections

    def _perform_tracking_update(self, detections: List[STrack], 
                                img: Optional[np.ndarray] = None) -> List[STrack]:
        """Perform the core tracking update algorithm."""
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
        r_tracked_stracks = [strack_pool[i] for i in u_track if strack_pool[i].state == TrackState.Tracked]
        dists = iou_distance(r_tracked_stracks, dets_second)
        matches, u_track, u_detection_second = linear_assignment(dists, thresh=0.5)

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
        detections = [dets[i] for i in u_detection]
        dists = self.get_dists(unconfirmed, detections)
        matches, u_unconfirmed, u_detection = linear_assignment(dists, thresh=0.7)

        for itracked, idet in matches:
            unconfirmed[itracked].update(detections[idet], self.frame_id)
            activated_stracks.append(unconfirmed[itracked])

        for it in u_unconfirmed:
            track = unconfirmed[it]
            track.mark_removed()
            removed_stracks.append(track)

        # Step 4: Init new stracks
        for inew in u_detection:
            track = detections[inew]
            if track.score < self.config.new_track_thresh:
                continue
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

        return [x for x in self.tracked_stracks if x.is_activated]

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
        self.reset_id()

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

    @staticmethod
    def remove_duplicate_stracks(stracksa: List[STrack], stracksb: List[STrack]) -> Tuple[List[STrack], List[STrack]]:
        """Remove duplicate stracks from two lists based on Intersection over Union (IoU) distance."""
        pdist = iou_distance(stracksa, stracksb)
        pairs = np.where(pdist < 0.15)
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