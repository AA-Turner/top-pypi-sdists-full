"""
Test data generators for post-processing tests.

This module provides functions to generate realistic test data for all
post-processing use cases including detection results, tracking data,
zone configurations, and various edge cases.
"""

import random
import time
import math
from typing import Dict, List, Any, Optional, Tuple, Union

# Fix imports for proper module resolution
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from matrice.deploy.utils.post_processing import (
    PeopleCountingConfig, CustomerServiceConfig, ZoneConfig, AlertConfig, TrackingConfig
)


def create_detection_results(
    num_detections: int = 10,
    categories: List[str] = None,
    confidence_range: Tuple[float, float] = (0.5, 0.95),
    bbox_size_range: Tuple[int, int] = (20, 100),
    image_size: Tuple[int, int] = (640, 480),
    include_metadata: bool = True
) -> List[Dict[str, Any]]:
    """Create realistic detection results."""
    if categories is None:
        categories = ["person", "car", "bike", "truck", "bus"]
    
    detections = []
    
    for i in range(num_detections):
        # Generate random bbox
        width = random.randint(*bbox_size_range)
        height = random.randint(*bbox_size_range)
        x1 = random.randint(0, image_size[0] - width)
        y1 = random.randint(0, image_size[1] - height)
        x2 = x1 + width
        y2 = y1 + height
        
        detection = {
            "bbox": [x1, y1, x2, y2],
            "confidence": random.uniform(*confidence_range),
            "category": random.choice(categories)
        }
        
        if include_metadata:
            detection.update({
                "detection_id": i,
                "area": width * height,
                "aspect_ratio": width / height,
                "center": [(x1 + x2) / 2, (y1 + y2) / 2]
            })
        
        detections.append(detection)
    
    return detections


def create_tracking_results(
    num_tracks: int = 8,
    categories: List[str] = None,
    frames: int = 10,
    confidence_range: Tuple[float, float] = (0.6, 0.9),
    bbox_size_range: Tuple[int, int] = (30, 80),
    image_size: Tuple[int, int] = (640, 480),
    include_trajectory: bool = True
) -> List[Dict[str, Any]]:
    """Create realistic tracking results."""
    if categories is None:
        categories = ["person", "car", "bike"]
    
    tracks = []
    
    for track_id in range(1, num_tracks + 1):
        category = random.choice(categories)
        
        # Generate initial position and movement pattern
        initial_x = random.randint(50, image_size[0] - 150)
        initial_y = random.randint(50, image_size[1] - 150)
        
        # Movement pattern
        velocity_x = random.uniform(-2, 2)
        velocity_y = random.uniform(-2, 2)
        
        # Size variation
        base_width = random.randint(*bbox_size_range)
        base_height = random.randint(*bbox_size_range)
        
        for frame in range(1, frames + 1):
            # Calculate position with some noise
            x = initial_x + velocity_x * frame + random.uniform(-5, 5)
            y = initial_y + velocity_y * frame + random.uniform(-5, 5)
            
            # Ensure bbox stays within image
            x = max(0, min(x, image_size[0] - base_width))
            y = max(0, min(y, image_size[1] - base_height))
            
            # Size variation
            width = base_width + random.randint(-5, 5)
            height = base_height + random.randint(-5, 5)
            
            track = {
                "track_id": track_id,
                "bbox": [int(x), int(y), int(x + width), int(y + height)],
                "confidence": random.uniform(*confidence_range),
                "category": category,
                "frame": frame,
                "timestamp": time.time() + frame * 0.033  # ~30 FPS
            }
            
            if include_trajectory:
                track.update({
                    "velocity": [velocity_x, velocity_y],
                    "age": frame,
                    "hits": frame,
                    "time_since_update": 0
                })
            
            tracks.append(track)
    
    return tracks


def create_zone_polygons(
    zone_names: List[str],
    image_size: Tuple[int, int] = (640, 480),
    zone_types: List[str] = None
) -> Dict[str, List[List[int]]]:
    """Create zone polygon configurations."""
    if zone_types is None:
        zone_types = ["rectangular", "triangular", "complex"]
    
    zones = {}
    
    for i, zone_name in enumerate(zone_names):
        zone_type = random.choice(zone_types)
        
        if zone_type == "rectangular":
            # Create rectangular zone
            x1 = random.randint(0, image_size[0] // 2)
            y1 = random.randint(0, image_size[1] // 2)
            width = random.randint(100, image_size[0] // 2)
            height = random.randint(100, image_size[1] // 2)
            x2 = min(x1 + width, image_size[0])
            y2 = min(y1 + height, image_size[1])
            
            polygon = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        
        elif zone_type == "triangular":
            # Create triangular zone
            center_x = random.randint(100, image_size[0] - 100)
            center_y = random.randint(100, image_size[1] - 100)
            radius = random.randint(50, 100)
            
            polygon = [
                [center_x, center_y - radius],
                [center_x + int(radius * 0.866), center_y + radius // 2],
                [center_x - int(radius * 0.866), center_y + radius // 2]
            ]
        
        else:  # complex
            # Create complex polygon
            center_x = random.randint(150, image_size[0] - 150)
            center_y = random.randint(150, image_size[1] - 150)
            
            num_points = random.randint(5, 8)
            polygon = []
            
            for j in range(num_points):
                angle = (2 * math.pi * j) / num_points
                radius = random.randint(50, 100)
                x = center_x + int(radius * math.cos(angle))
                y = center_y + int(radius * math.sin(angle))
                polygon.append([x, y])
        
        zones[zone_name] = polygon
    
    return zones


def create_customer_service_areas() -> Dict[str, Dict[str, List[List[int]]]]:
    """Create customer service area configurations."""
    return {
        "customer_areas": {
            "entrance": [[0, 0], [200, 0], [200, 150], [0, 150]],
            "lobby": [[50, 150], [350, 150], [350, 300], [50, 300]],
            "waiting_area": [[100, 300], [300, 300], [300, 400], [100, 400]],
            "queue": [[200, 400], [250, 400], [250, 500], [200, 500]]
        },
        "staff_areas": {
            "counter": [[350, 200], [500, 200], [500, 350], [350, 350]],
            "office": [[500, 100], [600, 100], [600, 200], [500, 200]],
            "break_room": [[500, 350], [600, 350], [600, 450], [500, 450]]
        },
        "service_areas": {
            "service_desk_1": [[300, 200], [350, 200], [350, 250], [300, 250]],
            "service_desk_2": [[300, 250], [350, 250], [350, 300], [300, 300]],
            "consultation": [[400, 300], [500, 300], [500, 400], [400, 400]]
        }
    }


def create_line_crossing_data(
    lines: Dict[str, List[List[int]]],
    num_tracks: int = 5,
    frames: int = 20
) -> List[Dict[str, Any]]:
    """Create tracking data that crosses specified lines."""
    tracks = []
    
    for track_id in range(1, num_tracks + 1):
        # Pick a random line to cross
        line_name = random.choice(list(lines.keys()))
        line_points = lines[line_name]
        
        # Start on one side of the line, end on the other
        start_x = line_points[0][0] - 50
        start_y = line_points[0][1] + random.randint(-20, 20)
        end_x = line_points[1][0] + 50
        end_y = line_points[1][1] + random.randint(-20, 20)
        
        for frame in range(1, frames + 1):
            # Linear interpolation
            progress = frame / frames
            x = start_x + (end_x - start_x) * progress
            y = start_y + (end_y - start_y) * progress
            
            track = {
                "track_id": track_id,
                "bbox": [int(x), int(y), int(x + 40), int(y + 60)],
                "confidence": random.uniform(0.7, 0.9),
                "category": "person",
                "frame": frame,
                "timestamp": time.time() + frame * 0.033
            }
            
            tracks.append(track)
    
    return tracks


def create_people_counting_scenarios() -> List[Dict[str, Any]]:
    """Create various people counting test scenarios."""
    scenarios = []
    
    # Scenario 1: Basic counting
    scenarios.append({
        "name": "basic_counting",
        "description": "Basic people counting with simple detections",
        "data": create_detection_results(
            num_detections=15,
            categories=["person"],
            confidence_range=(0.6, 0.95)
        ),
        "config": {
            "confidence_threshold": 0.5,
            "person_categories": ["person"]
        }
    })
    
    # Scenario 2: Zone-based counting
    zones = create_zone_polygons(["entrance", "lobby", "exit"])
    scenarios.append({
        "name": "zone_counting",
        "description": "People counting with zone analysis",
        "data": create_detection_results(num_detections=20),
        "config": {
            "confidence_threshold": 0.6,
            "zone_config": {"zones": zones}
        }
    })
    
    # Scenario 3: Tracking-based unique counting
    scenarios.append({
        "name": "unique_counting",
        "description": "Unique people counting with tracking",
        "data": create_tracking_results(num_tracks=8, frames=15),
        "config": {
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "enable_unique_counting": True
        }
    })
    
    return scenarios


def create_customer_service_scenarios() -> List[Dict[str, Any]]:
    """Create customer service analysis test scenarios."""
    scenarios = []
    areas = create_customer_service_areas()
    
    # Scenario 1: Basic customer service
    scenarios.append({
        "name": "basic_service",
        "description": "Basic customer service analysis",
        "data": create_detection_results(
            num_detections=25,
            categories=["person", "staff"]
        ),
        "config": {
            "confidence_threshold": 0.6,
            "customer_areas": areas["customer_areas"],
            "staff_areas": areas["staff_areas"],
            "service_areas": areas["service_areas"],
            "staff_categories": ["staff"],
            "customer_categories": ["person"]
        }
    })
    
    # Scenario 2: Queue analysis
    scenarios.append({
        "name": "queue_analysis",
        "description": "Customer queue analysis with wait times",
        "data": create_tracking_results(
            num_tracks=12,
            frames=30,
            categories=["person", "staff"]
        ),
        "config": {
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "customer_areas": areas["customer_areas"],
            "service_areas": areas["service_areas"],
            "max_service_time": 300.0
        }
    })
    
    return scenarios


def create_basic_counting_tracking_scenarios() -> List[Dict[str, Any]]:
    """Create basic counting and tracking test scenarios."""
    scenarios = []
    
    # Scenario 1: Line crossing detection
    lines = {
        "entrance_line": [[100, 200], [200, 200]],
        "exit_line": [[400, 200], [500, 200]]
    }
    
    scenarios.append({
        "name": "line_crossing",
        "description": "Line crossing detection and counting",
        "data": create_line_crossing_data(lines, num_tracks=6, frames=25),
        "config": {
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "lines": lines
        }
    })
    
    # Scenario 2: Zone tracking
    zones = create_zone_polygons(["zone_a", "zone_b", "zone_c"])
    scenarios.append({
        "name": "zone_tracking",
        "description": "Object tracking within zones",
        "data": create_tracking_results(num_tracks=10, frames=20),
        "config": {
            "confidence_threshold": 0.5,
            "enable_tracking": True,
            "zones": zones
        }
    })
    
    return scenarios


def create_edge_case_data() -> Dict[str, List[Dict[str, Any]]]:
    """Create edge case test data."""
    return {
        "empty_results": [],
        "single_detection": create_detection_results(num_detections=1),
        "low_confidence": create_detection_results(
            num_detections=5,
            confidence_range=(0.1, 0.4)
        ),
        "high_confidence": create_detection_results(
            num_detections=5,
            confidence_range=(0.95, 1.0)
        ),
        "overlapping_bboxes": [
            {"bbox": [100, 100, 200, 200], "confidence": 0.8, "category": "person"},
            {"bbox": [150, 150, 250, 250], "confidence": 0.7, "category": "person"},
            {"bbox": [120, 120, 220, 220], "confidence": 0.9, "category": "person"}
        ],
        "boundary_bboxes": [
            {"bbox": [0, 0, 50, 50], "confidence": 0.8, "category": "person"},
            {"bbox": [590, 430, 640, 480], "confidence": 0.7, "category": "person"}
        ],
        "malformed_data": [
            {"bbox": [100, 100], "confidence": 0.8},  # Missing coordinates
            {"confidence": 0.7, "category": "person"},  # Missing bbox
            {"bbox": [100, 100, 200, 200]},  # Missing confidence
        ]
    }


def create_performance_test_data(scale: str = "medium") -> Dict[str, Any]:
    """Create performance test data at different scales."""
    scales = {
        "small": {"detections": 50, "tracks": 10, "frames": 10},
        "medium": {"detections": 500, "tracks": 50, "frames": 30},
        "large": {"detections": 2000, "tracks": 200, "frames": 100},
        "huge": {"detections": 10000, "tracks": 1000, "frames": 500}
    }
    
    if scale not in scales:
        scale = "medium"
    
    params = scales[scale]
    
    return {
        "detection_data": create_detection_results(
            num_detections=params["detections"]
        ),
        "tracking_data": create_tracking_results(
            num_tracks=params["tracks"],
            frames=params["frames"]
        ),
        "zones": create_zone_polygons([f"zone_{i}" for i in range(10)]),
        "scale_info": {
            "scale": scale,
            "expected_detections": params["detections"],
            "expected_tracks": params["tracks"],
            "expected_frames": params["frames"]
        }
    }


def create_multi_camera_data(num_cameras: int = 3) -> Dict[str, Any]:
    """Create multi-camera test data."""
    cameras = {}
    
    for camera_id in range(1, num_cameras + 1):
        cameras[f"camera_{camera_id}"] = {
            "detection_data": create_detection_results(
                num_detections=random.randint(10, 30),
                image_size=(1920, 1080) if camera_id == 1 else (640, 480)
            ),
            "tracking_data": create_tracking_results(
                num_tracks=random.randint(5, 15),
                frames=random.randint(10, 25)
            ),
            "zones": create_zone_polygons([f"cam{camera_id}_zone_{i}" for i in range(3)]),
            "metadata": {
                "camera_id": camera_id,
                "location": f"Location_{camera_id}",
                "resolution": (1920, 1080) if camera_id == 1 else (640, 480)
            }
        }
    
    return cameras


def create_temporal_data_series(duration_minutes: int = 60) -> List[Dict[str, Any]]:
    """Create temporal data series for time-based analysis."""
    data_series = []
    frames_per_minute = 30  # Assuming 0.5 FPS for analysis
    total_frames = duration_minutes * frames_per_minute
    
    base_time = time.time()
    
    for frame in range(total_frames):
        timestamp = base_time + frame * 2  # 2 seconds per frame
        
        # Simulate varying activity levels
        hour = (frame // frames_per_minute) % 24
        if 9 <= hour <= 17:  # Business hours
            activity_level = random.uniform(0.7, 1.0)
        elif 6 <= hour <= 9 or 17 <= hour <= 20:  # Rush hours
            activity_level = random.uniform(0.5, 0.8)
        else:  # Off hours
            activity_level = random.uniform(0.1, 0.4)
        
        num_detections = int(20 * activity_level)
        
        frame_data = {
            "timestamp": timestamp,
            "frame": frame,
            "hour": hour,
            "activity_level": activity_level,
            "detections": create_detection_results(
                num_detections=num_detections,
                categories=["person", "vehicle"]
            )
        }
        
        data_series.append(frame_data)
    
    return data_series


def create_configuration_variants() -> Dict[str, Dict[str, Any]]:
    """Create various configuration variants for testing."""
    return {
        "minimal_config": {
            "confidence_threshold": 0.5
        },
        "full_people_counting": {
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "enable_unique_counting": True,
            "time_window_minutes": 30,
            "person_categories": ["person", "people"],
            "zone_config": {
                "zones": create_zone_polygons(["entrance", "lobby", "exit"])
            },
            "alert_config": {
                "count_thresholds": {"person": 50},
                "occupancy_thresholds": {"lobby": 20}
            }
        },
        "customer_service_config": {
            "confidence_threshold": 0.7,
            "enable_tracking": True,
            "customer_categories": ["customer", "person"],
            "staff_categories": ["staff", "employee"],
            "service_proximity_threshold": 150.0,
            "max_service_time": 600.0,
            **create_customer_service_areas()
        },
        "high_performance_config": {
            "confidence_threshold": 0.8,
            "batch_size": 100,
            "max_objects": 500,
            "enable_analytics": False  # Disable for performance
        }
    }


def create_result_format_variants() -> Dict[str, Dict[str, Any]]:
    """Create test data in different result formats."""
    base_detections = create_detection_results(10)
    base_tracks = create_tracking_results(5, frames=8)
    
    return {
        "coco_format": {
            "images": [{"id": 1, "width": 640, "height": 480, "file_name": "test.jpg"}],
            "annotations": [
                {
                    "id": i,
                    "image_id": 1,
                    "category_id": 1,
                    "bbox": det["bbox"],
                    "area": (det["bbox"][2] - det["bbox"][0]) * (det["bbox"][3] - det["bbox"][1]),
                    "iscrowd": 0,
                    "score": det["confidence"]
                }
                for i, det in enumerate(base_detections)
            ],
            "categories": [{"id": 1, "name": "person"}]
        },
        "yolo_format": [
            {
                "class": 0,
                "confidence": det["confidence"],
                "bbox": [
                    (det["bbox"][0] + det["bbox"][2]) / 2 / 640,  # center_x normalized
                    (det["bbox"][1] + det["bbox"][3]) / 2 / 480,  # center_y normalized
                    (det["bbox"][2] - det["bbox"][0]) / 640,      # width normalized
                    (det["bbox"][3] - det["bbox"][1]) / 480       # height normalized
                ]
            }
            for det in base_detections
        ],
        "tracking_format": base_tracks,
        "custom_format": {
            "detections": base_detections,
            "metadata": {
                "timestamp": time.time(),
                "source": "test_camera",
                "resolution": [640, 480]
            }
        }
    } 