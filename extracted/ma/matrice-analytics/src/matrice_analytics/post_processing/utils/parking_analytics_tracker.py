"""
Parking Analytics Tracker

This module provides dwell time and parking status tracking for vehicles.
Tracks movement patterns to determine if vehicles are parked or moving.
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import math
import logging


@dataclass
class VehicleParkingState:
    """Per-vehicle parking state tracking"""
    track_id: int
    category: str
    first_seen_frame: int
    first_seen_timestamp: str
    last_seen_frame: int
    last_seen_timestamp: str
    
    # Position tracking for movement detection
    position_history: deque = field(default_factory=lambda: deque(maxlen=60))
    bbox_size_history: deque = field(default_factory=lambda: deque(maxlen=60))
    
    # Parking status
    is_parked: bool = False
    parked_since_frame: Optional[int] = None
    parked_since_timestamp: Optional[str] = None
    total_parked_frames: int = 0
    
    # Movement metrics
    movement_variance: float = 0.0
    
    @property
    def dwell_time_frames(self) -> int:
        """Total frames vehicle has been tracked"""
        return self.last_seen_frame - self.first_seen_frame + 1
    
    @property
    def parked_time_frames(self) -> int:
        """Total frames vehicle has been parked"""
        return self.total_parked_frames if self.is_parked else 0


class ParkingAnalyticsTracker:
    """
    Tracks parking duration and status for vehicles.
    
    Determines if vehicles are parked based on movement patterns:
    - Tracks bbox position over a sliding window (default 60 frames)
    - Calculates movement as percentage of bbox size
    - Marks vehicle as parked after threshold duration of stationary behavior
    """
    
    def __init__(
        self,
        parked_threshold_frames: int = 150,  # 5s @ 30fps
        movement_threshold_percent: float = 5.0,
        movement_window_frames: int = 60,
        fps: float = 30.0
    ):
        """
        Initialize parking analytics tracker.
        
        Args:
            parked_threshold_frames: Frames vehicle must be stationary to be marked as parked
            movement_threshold_percent: Max movement % of bbox size to be considered stationary
            movement_window_frames: Number of frames to analyze for movement
            fps: Frames per second for time calculations
        """
        self.parked_threshold_frames = parked_threshold_frames
        self.movement_threshold_percent = movement_threshold_percent
        self.movement_window_frames = movement_window_frames
        self.fps = fps
        
        self.active_tracks: Dict[int, VehicleParkingState] = {}
        self.removed_tracks: deque = deque(maxlen=100)
        
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(
            f"ParkingAnalyticsTracker initialized: "
            f"parked_threshold={parked_threshold_frames}f ({parked_threshold_frames/fps:.1f}s), "
            f"movement_threshold={movement_threshold_percent}%, "
            f"window={movement_window_frames}f"
        )
    
    def update(
        self,
        detections: List[Dict],
        current_frame: int,
        current_timestamp: str
    ) -> Dict[str, Any]:
        """
        Update parking analytics with current frame detections.
        
        Args:
            detections: List of detection dicts with track_id, category, bounding_box
            current_frame: Current frame number
            current_timestamp: Current timestamp string
            
        Returns:
            Analytics summary dict with active_vehicles, parked_vehicles, and summary stats
        """
        current_track_ids = set()
        
        # Log input summary
        self.logger.debug(
            f"[Frame {current_frame}] Parking analytics: "
            f"{len(detections)} detections, {len(self.active_tracks)} active"
        )
        
        # Process each detection
        for det in detections:
            track_id = det.get("track_id")
            if track_id is None:
                continue
            
            current_track_ids.add(track_id)
            
            # Get bbox center and size
            bbox = det.get("bounding_box", {})
            center = self._get_bbox_center(bbox)
            size = self._get_bbox_size(bbox)
            
            if track_id not in self.active_tracks:
                # New track - initialize
                self._initialize_track(
                    track_id=track_id,
                    category=det.get("category", "unknown"),
                    first_frame=current_frame,
                    first_timestamp=current_timestamp,
                    center=center,
                    size=size
                )
            else:
                # Update existing track
                self._update_track(
                    track_id=track_id,
                    category=det.get("category"),
                    current_frame=current_frame,
                    current_timestamp=current_timestamp,
                    center=center,
                    size=size
                )
        
        # Handle removed tracks
        removed_ids = set(self.active_tracks.keys()) - current_track_ids
        if removed_ids:
            self.logger.debug(
                f"[Frame {current_frame}] Archiving {len(removed_ids)} removed: "
                f"{list(removed_ids)[:5]}"
            )
            for track_id in removed_ids:
                self._archive_track(track_id)
        
        # Generate analytics summary
        analytics = self._generate_analytics_summary(current_frame, current_timestamp)
        
        # Log summary
        self.logger.debug(
            f"[Frame {current_frame}] Summary: "
            f"active={analytics['summary']['total_active']}, "
            f"parked={analytics['summary']['total_parked']}, "
            f"avg_dwell={analytics['summary']['average_dwell_time']:.1f}s"
        )
        
        return analytics
    
    def _initialize_track(self, track_id, category, first_frame, first_timestamp, center, size):
        """Initialize new vehicle track"""
        self.active_tracks[track_id] = VehicleParkingState(
            track_id=track_id,
            category=category,
            first_seen_frame=first_frame,
            first_seen_timestamp=first_timestamp,
            last_seen_frame=first_frame,
            last_seen_timestamp=first_timestamp
        )
        
        # Add initial position
        self.active_tracks[track_id].position_history.append(center)
        self.active_tracks[track_id].bbox_size_history.append(size)
        
        self.logger.debug(
            f"Init track {track_id} ({category}): "
            f"pos=({center[0]:.0f},{center[1]:.0f}), size={size:.0f}"
        )
    
    def _update_track(self, track_id, category, current_frame, current_timestamp, center, size):
        """Update existing track with new detection"""
        track_state = self.active_tracks[track_id]
        
        # Update basic info
        track_state.category = category
        track_state.last_seen_frame = current_frame
        track_state.last_seen_timestamp = current_timestamp
        
        # Update position history
        track_state.position_history.append(center)
        track_state.bbox_size_history.append(size)
        
        # Calculate movement and update parked status
        self._update_parking_status(track_state, current_frame, current_timestamp)
    
    def _update_parking_status(self, track_state: VehicleParkingState, current_frame: int, timestamp: str):
        """Determine if vehicle is parked based on movement"""
        
        # Need sufficient history
        if len(track_state.position_history) < self.movement_window_frames:
            return
        
        # Calculate movement variance relative to bbox size
        positions = list(track_state.position_history)
        sizes = list(track_state.bbox_size_history)
        avg_size = sum(sizes) / len(sizes)
        
        # Calculate max displacement in window
        max_displacement = 0.0
        for i in range(1, len(positions)):
            dx = positions[i][0] - positions[i-1][0]
            dy = positions[i][1] - positions[i-1][1]
            displacement = math.sqrt(dx*dx + dy*dy)
            max_displacement = max(max_displacement, displacement)
        
        # Movement as percentage of average bbox size
        movement_percent = (max_displacement / avg_size) * 100 if avg_size > 0 else 0
        track_state.movement_variance = movement_percent
        
        # Determine parked status
        is_stationary = movement_percent < self.movement_threshold_percent
        
        if is_stationary:
            if not track_state.is_parked:
                # Check if vehicle has been stationary long enough
                if track_state.dwell_time_frames >= self.parked_threshold_frames:
                    track_state.is_parked = True
                    track_state.parked_since_frame = current_frame
                    track_state.parked_since_timestamp = timestamp
                    
                    self.logger.info(
                        f"Track {track_state.track_id} ({track_state.category}) PARKED: "
                        f"dwell={track_state.dwell_time_frames}f "
                        f"({track_state.dwell_time_frames/self.fps:.1f}s), "
                        f"movement={movement_percent:.2f}%"
                    )
            
            # Increment parked time if already parked
            if track_state.is_parked:
                track_state.total_parked_frames += 1
        else:
            # Moving - reset parked status if was parked
            if track_state.is_parked:
                self.logger.info(
                    f"Track {track_state.track_id} MOVING: "
                    f"movement={movement_percent:.1f}% > {self.movement_threshold_percent}%, "
                    f"was_parked={track_state.total_parked_frames}f "
                    f"({track_state.total_parked_frames/self.fps:.1f}s)"
                )
                track_state.is_parked = False
                track_state.parked_since_frame = None
                track_state.parked_since_timestamp = None
    
    def _archive_track(self, track_id: int):
        """Move track from active to removed history"""
        if track_id in self.active_tracks:
            track_state = self.active_tracks.pop(track_id)
            self.removed_tracks.append(track_state)
            
            self.logger.debug(
                f"Archive {track_id}: dwell={track_state.dwell_time_frames}f, "
                f"parked={track_state.total_parked_frames}f, "
                f"status={'PARKED' if track_state.is_parked else 'MOVING'}"
            )
    
    def _generate_analytics_summary(self, current_frame: int, timestamp: str) -> Dict[str, Any]:
        """Generate summary of parking analytics"""
        
        active_vehicles = []
        parked_vehicles = []
        
        for track_state in self.active_tracks.values():
            vehicle_data = {
                "track_id": track_state.track_id,
                "category": track_state.category,
                "dwell_time_seconds": round(track_state.dwell_time_frames / self.fps, 1),
                "dwell_time_frames": track_state.dwell_time_frames,
                "is_parked": track_state.is_parked,
                "movement_percent": round(track_state.movement_variance, 2),
                "first_seen": track_state.first_seen_timestamp,
                "last_seen": track_state.last_seen_timestamp
            }
            
            if track_state.is_parked:
                vehicle_data["parked_time_seconds"] = round(track_state.parked_time_frames / self.fps, 1)
                vehicle_data["parked_since"] = track_state.parked_since_timestamp
                parked_vehicles.append(vehicle_data)
            
            active_vehicles.append(vehicle_data)
        
        return {
            "active_vehicles": active_vehicles,
            "parked_vehicles": parked_vehicles,
            "summary": {
                "total_active": len(active_vehicles),
                "total_parked": len(parked_vehicles),
                "average_dwell_time": self._calculate_average_dwell_time(),
                "longest_parked": self._get_longest_parked()
            },
            "timestamp": timestamp,
            "frame": current_frame
        }
    
    def _calculate_average_dwell_time(self) -> float:
        """Calculate average dwell time of active vehicles"""
        if not self.active_tracks:
            return 0.0
        total_frames = sum(t.dwell_time_frames for t in self.active_tracks.values())
        return round((total_frames / len(self.active_tracks)) / self.fps, 1)
    
    def _get_longest_parked(self) -> Optional[Dict]:
        """Get vehicle with longest parking duration"""
        parked = [t for t in self.active_tracks.values() if t.is_parked]
        if not parked:
            return None
        
        longest = max(parked, key=lambda t: t.total_parked_frames)
        return {
            "track_id": longest.track_id,
            "category": longest.category,
            "parked_time_seconds": round(longest.total_parked_frames / self.fps, 1),
            "parked_since": longest.parked_since_timestamp
        }
    
    @staticmethod
    def _get_bbox_center(bbox: Dict) -> Tuple[float, float]:
        """Extract center point from bounding box"""
        if "xmin" in bbox and "xmax" in bbox:
            return ((bbox["xmin"] + bbox["xmax"]) / 2, (bbox["ymin"] + bbox["ymax"]) / 2)
        elif "x1" in bbox and "x2" in bbox:
            return ((bbox["x1"] + bbox["x2"]) / 2, (bbox["y1"] + bbox["y2"]) / 2)
        return (0.0, 0.0)
    
    @staticmethod
    def _get_bbox_size(bbox: Dict) -> float:
        """Calculate bbox diagonal size (for relative movement calculation)"""
        if "xmin" in bbox and "xmax" in bbox:
            w = bbox["xmax"] - bbox["xmin"]
            h = bbox["ymax"] - bbox["ymin"]
        elif "x1" in bbox and "x2" in bbox:
            w = bbox["x2"] - bbox["x1"]
            h = bbox["y2"] - bbox["y1"]
        else:
            return 0.0
        return math.sqrt(w*w + h*h)