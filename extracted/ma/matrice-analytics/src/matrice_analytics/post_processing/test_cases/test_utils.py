"""
Tests for post processing utility functions.

This module tests all utility functions including geometry calculations,
format conversions, filtering, counting, and tracking utilities.
"""

import unittest
import math
from typing import Dict, List, Any

# Fix imports for proper module resolution
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.matrice_analytics.post_processing.utils import (
    # Geometry utilities
    point_in_polygon, get_bbox_center, calculate_distance, calculate_bbox_overlap,
    calculate_iou, get_bbox_area, normalize_bbox, denormalize_bbox, line_segments_intersect,
    
    # Format utilities
    convert_to_coco_format, convert_to_yolo_format, convert_to_tracking_format,
    convert_detection_to_tracking_format, convert_tracking_to_detection_format,
    match_results_structure,
    
    # Filter utilities
    filter_by_confidence, filter_by_categories, calculate_bbox_fingerprint,
    clean_expired_tracks, remove_duplicate_detections, apply_category_mapping,
    filter_by_area,
    
    # Counting utilities
    count_objects_by_category, count_objects_in_zones, count_unique_tracks,
    calculate_counting_summary,
    
    # Tracking utilities
    track_objects_in_zone, detect_line_crossings, analyze_track_movements,
    filter_tracks_by_duration
)

from .test_utilities import BasePostProcessingTest
from .test_data_generators import (
    create_detection_results, create_tracking_results, create_zone_polygons,
    create_line_crossing_data, create_edge_case_data
)


class TestGeometryUtils(BasePostProcessingTest):
    """Test geometry utility functions."""
    
    def test_point_in_polygon(self):
        """Test point in polygon detection."""
        # Square polygon
        square = [[0, 0], [100, 0], [100, 100], [0, 100]]
        
        # Test points inside
        self.assertTrue(point_in_polygon([50, 50], square))
        self.assertTrue(point_in_polygon([10, 10], square))
        self.assertTrue(point_in_polygon([90, 90], square))
        
        # Test points outside
        self.assertFalse(point_in_polygon([150, 50], square))
        self.assertFalse(point_in_polygon([50, 150], square))
        self.assertFalse(point_in_polygon([-10, 50], square))
        
        # Test boundary points
        self.assertTrue(point_in_polygon([0, 50], square))  # Edge case
        self.assertTrue(point_in_polygon([50, 0], square))  # Edge case
    
    def test_point_in_polygon_complex(self):
        """Test point in polygon with complex shapes."""
        # Triangle
        triangle = [[0, 0], [100, 0], [50, 100]]
        
        self.assertTrue(point_in_polygon([50, 30], triangle))
        self.assertFalse(point_in_polygon([10, 90], triangle))
        
        # Concave polygon
        concave = [[0, 0], [100, 0], [100, 50], [50, 50], [50, 100], [0, 100]]
        
        self.assertTrue(point_in_polygon([25, 25], concave))
        self.assertTrue(point_in_polygon([75, 25], concave))
        self.assertFalse(point_in_polygon([75, 75], concave))  # In the "notch"
    
    def test_get_bbox_center(self):
        """Test bounding box center calculation."""
        # Simple rectangle
        bbox = [10, 20, 50, 60]
        center = get_bbox_center(bbox)
        self.assertEqual(center, [30.0, 40.0])
        
        # Square
        bbox = [0, 0, 100, 100]
        center = get_bbox_center(bbox)
        self.assertEqual(center, [50.0, 50.0])
        
        # Single point (degenerate case)
        bbox = [50, 50, 50, 50]
        center = get_bbox_center(bbox)
        self.assertEqual(center, [50.0, 50.0])
    
    def test_calculate_distance(self):
        """Test distance calculation between points."""
        # Simple cases
        self.assertEqual(calculate_distance([0, 0], [3, 4]), 5.0)
        self.assertEqual(calculate_distance([0, 0], [0, 0]), 0.0)
        self.assertEqual(calculate_distance([1, 1], [4, 5]), 5.0)
        
        # Negative coordinates
        self.assertEqual(calculate_distance([-3, -4], [0, 0]), 5.0)
        
        # Floating point coordinates
        dist = calculate_distance([1.5, 2.5], [4.5, 6.5])
        self.assertAlmostEqual(dist, 5.0, places=5)
    
    def test_calculate_bbox_overlap(self):
        """Test bounding box overlap calculation."""
        # Overlapping boxes
        bbox1 = [0, 0, 50, 50]
        bbox2 = [25, 25, 75, 75]
        overlap = calculate_bbox_overlap(bbox1, bbox2)
        expected_overlap = 25 * 25  # 625
        self.assertEqual(overlap, expected_overlap)
        
        # Non-overlapping boxes
        bbox1 = [0, 0, 50, 50]
        bbox2 = [100, 100, 150, 150]
        overlap = calculate_bbox_overlap(bbox1, bbox2)
        self.assertEqual(overlap, 0)
        
        # Identical boxes
        bbox1 = [0, 0, 100, 100]
        bbox2 = [0, 0, 100, 100]
        overlap = calculate_bbox_overlap(bbox1, bbox2)
        self.assertEqual(overlap, 10000)  # 100 * 100
        
        # Touching boxes (no overlap)
        bbox1 = [0, 0, 50, 50]
        bbox2 = [50, 0, 100, 50]
        overlap = calculate_bbox_overlap(bbox1, bbox2)
        self.assertEqual(overlap, 0)
    
    def test_calculate_iou(self):
        """Test IoU (Intersection over Union) calculation."""
        # Identical boxes
        bbox1 = [0, 0, 100, 100]
        bbox2 = [0, 0, 100, 100]
        iou = calculate_iou(bbox1, bbox2)
        self.assertEqual(iou, 1.0)
        
        # Non-overlapping boxes
        bbox1 = [0, 0, 50, 50]
        bbox2 = [100, 100, 150, 150]
        iou = calculate_iou(bbox1, bbox2)
        self.assertEqual(iou, 0.0)
        
        # Partially overlapping boxes
        bbox1 = [0, 0, 100, 100]
        bbox2 = [50, 50, 150, 150]
        iou = calculate_iou(bbox1, bbox2)
        # Intersection: 50*50 = 2500, Union: 10000 + 10000 - 2500 = 17500
        expected_iou = 2500 / 17500
        self.assertAlmostEqual(iou, expected_iou, places=5)
    
    def test_get_bbox_area(self):
        """Test bounding box area calculation."""
        # Rectangle
        bbox = [0, 0, 100, 50]
        area = get_bbox_area(bbox)
        self.assertEqual(area, 5000)
        
        # Square
        bbox = [10, 10, 60, 60]
        area = get_bbox_area(bbox)
        self.assertEqual(area, 2500)
        
        # Degenerate case (line)
        bbox = [0, 0, 100, 0]
        area = get_bbox_area(bbox)
        self.assertEqual(area, 0)
        
        # Point
        bbox = [50, 50, 50, 50]
        area = get_bbox_area(bbox)
        self.assertEqual(area, 0)
    
    def test_normalize_denormalize_bbox(self):
        """Test bbox normalization and denormalization."""
        bbox = [100, 200, 300, 400]
        image_size = (640, 480)
        
        # Normalize
        normalized = normalize_bbox(bbox, image_size)
        expected = [100/640, 200/480, 300/640, 400/480]
        self.assertEqual(normalized, expected)
        
        # Denormalize
        denormalized = denormalize_bbox(normalized, image_size)
        self.assertEqual(denormalized, bbox)
        
        # Round trip test
        original = [50, 75, 150, 225]
        normalized = normalize_bbox(original, image_size)
        denormalized = denormalize_bbox(normalized, image_size)
        self.assertEqual(denormalized, original)
    
    def test_line_segments_intersect(self):
        """Test line segment intersection detection."""
        # Intersecting lines
        line1 = [[0, 0], [100, 100]]
        line2 = [[0, 100], [100, 0]]
        self.assertTrue(line_segments_intersect(line1, line2))
        
        # Non-intersecting lines
        line1 = [[0, 0], [50, 50]]
        line2 = [[100, 100], [150, 150]]
        self.assertFalse(line_segments_intersect(line1, line2))
        
        # Parallel lines
        line1 = [[0, 0], [100, 0]]
        line2 = [[0, 50], [100, 50]]
        self.assertFalse(line_segments_intersect(line1, line2))
        
        # Touching at endpoint
        line1 = [[0, 0], [50, 50]]
        line2 = [[50, 50], [100, 100]]
        self.assertTrue(line_segments_intersect(line1, line2))


class TestFormatUtils(BasePostProcessingTest):
    """Test format utility functions."""
    
    def test_convert_to_coco_format(self):
        """Test conversion to COCO format."""
        detections = [
            {"bbox": [10, 20, 50, 60], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 150, 200], "confidence": 0.9, "category": "car"}
        ]
        
        coco_format = convert_to_coco_format(detections)
        
        # Check structure
        self.assertIn("annotations", coco_format)
        self.assertIn("categories", coco_format)
        
        # Check annotations
        annotations = coco_format["annotations"]
        self.assertEqual(len(annotations), 2)
        
        # Check first annotation
        ann = annotations[0]
        self.assertEqual(ann["bbox"], [10, 20, 40, 40])  # COCO format: [x, y, width, height]
        self.assertEqual(ann["score"], 0.8)
        self.assertEqual(ann["area"], 1600)  # 40 * 40
    
    def test_convert_to_yolo_format(self):
        """Test conversion to YOLO format."""
        detections = [
            {"bbox": [10, 20, 50, 60], "confidence": 0.8, "category": "person"}
        ]
        image_size = (640, 480)
        
        yolo_format = convert_to_yolo_format(detections, image_size)
        
        self.assertEqual(len(yolo_format), 1)
        
        yolo_det = yolo_format[0]
        # YOLO format: [class, confidence, center_x_norm, center_y_norm, width_norm, height_norm]
        self.assertEqual(yolo_det["class"], 0)  # Assuming first category gets index 0
        self.assertEqual(yolo_det["confidence"], 0.8)
        
        # Check normalized coordinates
        expected_center_x = (10 + 50) / 2 / 640  # 30 / 640
        expected_center_y = (20 + 60) / 2 / 480  # 40 / 480
        expected_width = 40 / 640
        expected_height = 40 / 480
        
        self.assertAlmostEqual(yolo_det["bbox"][0], expected_center_x, places=5)
        self.assertAlmostEqual(yolo_det["bbox"][1], expected_center_y, places=5)
        self.assertAlmostEqual(yolo_det["bbox"][2], expected_width, places=5)
        self.assertAlmostEqual(yolo_det["bbox"][3], expected_height, places=5)
    
    def test_convert_to_tracking_format(self):
        """Test conversion to tracking format."""
        detections = [
            {"bbox": [10, 20, 50, 60], "confidence": 0.8, "category": "person", "detection_id": 1}
        ]
        
        tracking_format = convert_to_tracking_format(detections)
        
        self.assertEqual(len(tracking_format), 1)
        
        track = tracking_format[0]
        self.assertIn("track_id", track)
        self.assertEqual(track["bbox"], [10, 20, 50, 60])
        self.assertEqual(track["confidence"], 0.8)
        self.assertEqual(track["category"], "person")
    
    def test_match_results_structure(self):
        """Test result structure matching."""
        # Detection format
        detections = [{"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"}]
        format_type = match_results_structure(detections)
        self.assertEqual(format_type.value, "detection")
        
        # Tracking format
        tracks = [{"track_id": 1, "bbox": [0, 0, 100, 100], "confidence": 0.8, "frame": 1}]
        format_type = match_results_structure(tracks)
        self.assertEqual(format_type.value, "tracking")
        
        # Empty data
        format_type = match_results_structure([])
        self.assertEqual(format_type.value, "unknown")


class TestFilterUtils(BasePostProcessingTest):
    """Test filter utility functions."""
    
    def test_filter_by_confidence(self):
        """Test confidence filtering."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.3, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.7, "category": "car"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.9, "category": "person"}
        ]
        
        # Filter with threshold 0.5
        filtered = filter_by_confidence(detections, 0.5)
        self.assertEqual(len(filtered), 2)
        
        # Check that low confidence detection was removed
        confidences = [det["confidence"] for det in filtered]
        self.assertNotIn(0.3, confidences)
        self.assertIn(0.7, confidences)
        self.assertIn(0.9, confidences)
        
        # Filter with high threshold
        filtered = filter_by_confidence(detections, 0.8)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["confidence"], 0.9)
    
    def test_filter_by_categories(self):
        """Test category filtering."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.7, "category": "car"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.9, "category": "bike"}
        ]
        
        # Filter for specific categories
        filtered = filter_by_categories(detections, ["person", "bike"])
        self.assertEqual(len(filtered), 2)
        
        categories = [det["category"] for det in filtered]
        self.assertIn("person", categories)
        self.assertIn("bike", categories)
        self.assertNotIn("car", categories)
        
        # Filter for single category
        filtered = filter_by_categories(detections, ["person"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["category"], "person")
    
    def test_filter_by_area(self):
        """Test area-based filtering."""
        detections = [
            {"bbox": [0, 0, 10, 10], "confidence": 0.8, "category": "person"},      # Area: 100
            {"bbox": [0, 0, 50, 50], "confidence": 0.8, "category": "person"},     # Area: 2500
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"}    # Area: 10000
        ]
        
        # Filter by minimum area
        filtered = filter_by_area(detections, min_area=1000)
        self.assertEqual(len(filtered), 2)  # Should exclude the smallest
        
        # Filter by maximum area
        filtered = filter_by_area(detections, max_area=5000)
        self.assertEqual(len(filtered), 2)  # Should exclude the largest
        
        # Filter by area range
        filtered = filter_by_area(detections, min_area=1000, max_area=5000)
        self.assertEqual(len(filtered), 1)  # Should only include middle one
        self.assertEqual(get_bbox_area(filtered[0]["bbox"]), 2500)
    
    def test_apply_category_mapping(self):
        """Test category mapping application."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": 0},
            {"bbox": [100, 100, 200, 200], "confidence": 0.7, "category": 1},
            {"bbox": [200, 200, 300, 300], "confidence": 0.9, "category": 2}
        ]
        
        # Apply mapping
        mapping = {0: "person", 1: "car", 2: "bike"}
        mapped = apply_category_mapping(detections, mapping)
        
        self.assertEqual(len(mapped), 3)
        categories = [det["category"] for det in mapped]
        self.assertIn("person", categories)
        self.assertIn("car", categories)
        self.assertIn("bike", categories)
        
        # Test with missing mapping
        incomplete_mapping = {0: "person", 1: "car"}
        mapped = apply_category_mapping(detections, incomplete_mapping)
        
        # Should handle missing mapping gracefully
        self.assertEqual(len(mapped), 3)
        self.assertEqual(mapped[2]["category"], 2)  # Unchanged
    
    def test_remove_duplicate_detections(self):
        """Test duplicate detection removal."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"},
            {"bbox": [5, 5, 105, 105], "confidence": 0.7, "category": "person"},  # Similar bbox
            {"bbox": [200, 200, 300, 300], "confidence": 0.9, "category": "car"}
        ]
        
        # Remove duplicates with IoU threshold
        unique = remove_duplicate_detections(detections, iou_threshold=0.5)
        
        # Should remove one of the overlapping detections
        self.assertLessEqual(len(unique), 2)
        
        # Higher confidence detection should be kept
        if len(unique) == 2:
            confidences = [det["confidence"] for det in unique]
            self.assertIn(0.8, confidences)  # Higher confidence from overlapping pair
            self.assertIn(0.9, confidences)  # Non-overlapping detection


class TestCountingUtils(BasePostProcessingTest):
    """Test counting utility functions."""
    
    def test_count_objects_by_category(self):
        """Test object counting by category."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.7, "category": "person"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.9, "category": "car"},
            {"bbox": [300, 300, 400, 400], "confidence": 0.6, "category": "bike"}
        ]
        
        counts = count_objects_by_category(detections)
        
        self.assertEqual(counts["person"], 2)
        self.assertEqual(counts["car"], 1)
        self.assertEqual(counts["bike"], 1)
        self.assertEqual(len(counts), 3)
    
    def test_count_objects_in_zones(self):
        """Test zone-based object counting."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},    # In zone1
            {"bbox": [125, 25, 175, 75], "confidence": 0.7, "category": "person"},  # In zone2
            {"bbox": [225, 225, 275, 275], "confidence": 0.9, "category": "car"}   # Outside zones
        ]
        
        zones = {
            "zone1": [[0, 0], [100, 0], [100, 100], [0, 100]],
            "zone2": [[100, 0], [200, 0], [200, 100], [100, 100]]
        }
        
        zone_counts = count_objects_in_zones(detections, zones)
        
        self.assertEqual(zone_counts["zone1"]["total"], 1)
        self.assertEqual(zone_counts["zone2"]["total"], 1)
        self.assertEqual(zone_counts["zone1"]["by_category"]["person"], 1)
        self.assertEqual(zone_counts["zone2"]["by_category"]["person"], 1)
    
    def test_count_unique_tracks(self):
        """Test unique track counting."""
        tracks = [
            {"track_id": 1, "bbox": [0, 0, 100, 100], "confidence": 0.8, "frame": 1},
            {"track_id": 1, "bbox": [10, 10, 110, 110], "confidence": 0.8, "frame": 2},
            {"track_id": 2, "bbox": [200, 200, 300, 300], "confidence": 0.7, "frame": 1},
            {"track_id": 2, "bbox": [210, 210, 310, 310], "confidence": 0.7, "frame": 2}
        ]
        
        unique_count = count_unique_tracks(tracks)
        self.assertEqual(unique_count, 2)
        
        # Test with categories
        tracks_with_categories = [
            {"track_id": 1, "category": "person", "frame": 1},
            {"track_id": 2, "category": "person", "frame": 1},
            {"track_id": 3, "category": "car", "frame": 1}
        ]
        
        category_counts = count_unique_tracks(tracks_with_categories, by_category=True)
        self.assertEqual(category_counts["person"], 2)
        self.assertEqual(category_counts["car"], 1)
    
    def test_calculate_counting_summary(self):
        """Test comprehensive counting summary."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},
            {"bbox": [125, 25, 175, 75], "confidence": 0.7, "category": "person"},
            {"bbox": [225, 225, 275, 275], "confidence": 0.9, "category": "car"}
        ]
        
        zones = {
            "zone1": [[0, 0], [100, 0], [100, 100], [0, 100]]
        }
        
        summary = calculate_counting_summary(detections, zones=zones)
        
        # Check summary structure
        self.assertIn("total_count", summary)
        self.assertIn("category_counts", summary)
        self.assertIn("zone_analysis", summary)
        self.assertIn("confidence_stats", summary)
        
        # Check values
        self.assertEqual(summary["total_count"], 3)
        self.assertEqual(summary["category_counts"]["person"], 2)
        self.assertEqual(summary["category_counts"]["car"], 1)


class TestTrackingUtils(BasePostProcessingTest):
    """Test tracking utility functions."""
    
    def test_track_objects_in_zone(self):
        """Test zone-based object tracking."""
        tracks = [
            {"track_id": 1, "bbox": [25, 25, 75, 75], "frame": 1},    # In zone
            {"track_id": 1, "bbox": [125, 125, 175, 175], "frame": 2}, # Outside zone
            {"track_id": 2, "bbox": [50, 50, 100, 100], "frame": 1}   # In zone
        ]
        
        zone = [[0, 0], [100, 0], [100, 100], [0, 100]]
        
        zone_tracks = track_objects_in_zone(tracks, zone)
        
        # Should track objects that entered the zone
        self.assertGreater(len(zone_tracks), 0)
        
        # Check that we have tracking information
        for track_info in zone_tracks:
            self.assertIn("track_id", track_info)
            self.assertIn("enter_time", track_info)
    
    def test_detect_line_crossings(self):
        """Test line crossing detection."""
        # Create tracks that cross a line
        line = [[100, 0], [100, 200]]
        tracks = create_line_crossing_data({"test_line": line}, num_tracks=3, frames=10)
        
        crossings = detect_line_crossings(tracks, {"test_line": line})
        
        # Should detect crossings
        self.assertIn("test_line", crossings)
        self.assertGreater(len(crossings["test_line"]), 0)
        
        # Check crossing information
        for crossing in crossings["test_line"]:
            self.assertIn("track_id", crossing)
            self.assertIn("crossing_frame", crossing)
            self.assertIn("direction", crossing)
    
    def test_analyze_track_movements(self):
        """Test track movement analysis."""
        tracks = [
            {"track_id": 1, "bbox": [0, 0, 50, 50], "frame": 1, "timestamp": 1.0},
            {"track_id": 1, "bbox": [10, 10, 60, 60], "frame": 2, "timestamp": 2.0},
            {"track_id": 1, "bbox": [20, 20, 70, 70], "frame": 3, "timestamp": 3.0}
        ]
        
        movements = analyze_track_movements(tracks)
        
        # Should have movement analysis for track 1
        self.assertIn(1, movements)
        
        track_movement = movements[1]
        self.assertIn("total_distance", track_movement)
        self.assertIn("average_speed", track_movement)
        self.assertIn("direction_changes", track_movement)
        
        # Check calculated values
        self.assertGreater(track_movement["total_distance"], 0)
        self.assertGreater(track_movement["average_speed"], 0)
    
    def test_filter_tracks_by_duration(self):
        """Test track filtering by duration."""
        tracks = [
            {"track_id": 1, "frame": 1, "timestamp": 1.0},
            {"track_id": 1, "frame": 2, "timestamp": 2.0},
            {"track_id": 1, "frame": 3, "timestamp": 3.0},  # Duration: 2 seconds
            {"track_id": 2, "frame": 1, "timestamp": 1.0},
            {"track_id": 2, "frame": 2, "timestamp": 6.0}   # Duration: 5 seconds
        ]
        
        # Filter tracks with minimum duration
        long_tracks = filter_tracks_by_duration(tracks, min_duration=3.0)
        
        # Should only include track 2
        track_ids = set(track["track_id"] for track in long_tracks)
        self.assertIn(2, track_ids)
        self.assertNotIn(1, track_ids)
        
        # Filter tracks with maximum duration
        short_tracks = filter_tracks_by_duration(tracks, max_duration=3.0)
        
        # Should only include track 1
        track_ids = set(track["track_id"] for track in short_tracks)
        self.assertIn(1, track_ids)
        self.assertNotIn(2, track_ids)


class TestUtilsIntegration(BasePostProcessingTest):
    """Integration tests for utility functions."""
    
    def test_detection_processing_pipeline(self):
        """Test complete detection processing pipeline."""
        # Create test data
        detections = create_detection_results(
            num_detections=20,
            categories=["person", "car", "bike"],
            confidence_range=(0.3, 0.95)
        )
        
        # Step 1: Filter by confidence
        filtered = filter_by_confidence(detections, 0.5)
        
        # Step 2: Apply category mapping
        mapping = {"person": "pedestrian", "car": "vehicle", "bike": "bicycle"}
        mapped = []
        for det in filtered:
            if det["category"] in mapping:
                det_copy = det.copy()
                det_copy["category"] = mapping[det["category"]]
                mapped.append(det_copy)
            else:
                mapped.append(det)
        
        # Step 3: Remove duplicates
        unique = remove_duplicate_detections(mapped, iou_threshold=0.5)
        
        # Step 4: Count by category
        counts = count_objects_by_category(unique)
        
        # Verify pipeline
        self.assertLessEqual(len(unique), len(detections))  # Should filter some
        self.assertGreater(len(counts), 0)  # Should have categories
        
        # Check that mapping worked
        original_categories = set(det["category"] for det in detections)
        final_categories = set(det["category"] for det in unique)
        
        # Should have some mapped categories
        if "person" in original_categories:
            self.assertIn("pedestrian", final_categories)
    
    def test_tracking_analysis_pipeline(self):
        """Test complete tracking analysis pipeline."""
        # Create tracking data
        tracks = create_tracking_results(num_tracks=5, frames=15)
        
        # Define zones and lines
        zones = create_zone_polygons(["entrance", "lobby"])
        lines = {"crossing_line": [[200, 0], [200, 400]]}
        
        # Step 1: Filter by duration
        long_tracks = filter_tracks_by_duration(tracks, min_duration=0.1)
        
        # Step 2: Analyze movements
        movements = analyze_track_movements(long_tracks)
        
        # Step 3: Count in zones
        zone_counts = count_objects_in_zones(long_tracks, zones)
        
        # Step 4: Detect line crossings
        crossings = detect_line_crossings(long_tracks, lines)
        
        # Verify pipeline
        self.assertGreater(len(movements), 0)
        self.assertIn("entrance", zone_counts)
        self.assertIn("lobby", zone_counts)
        self.assertIn("crossing_line", crossings)
        
        # Check movement analysis
        for track_id, movement in movements.items():
            self.assertIn("total_distance", movement)
            self.assertIn("average_speed", movement)
    
    def test_format_conversion_roundtrip(self):
        """Test format conversion round trip."""
        # Create detection data
        original_detections = create_detection_results(5)
        
        # Convert to COCO format
        coco_format = convert_to_coco_format(original_detections)
        
        # Convert to tracking format
        tracking_format = convert_detection_to_tracking_format(original_detections)
        
        # Convert back to detection format
        back_to_detection = convert_tracking_to_detection_format(tracking_format)
        
        # Verify conversions
        self.assertEqual(len(back_to_detection), len(original_detections))
        
        # Check that essential information is preserved
        for orig, converted in zip(original_detections, back_to_detection):
            self.assertEqual(orig["bbox"], converted["bbox"])
            self.assertEqual(orig["confidence"], converted["confidence"])
            self.assertEqual(orig["category"], converted["category"])
    
    def test_edge_cases_handling(self):
        """Test utility functions with edge cases."""
        edge_cases = create_edge_case_data()
        
        # Test with empty data
        empty_data = edge_cases["empty_results"]
        
        # All functions should handle empty data gracefully
        self.assertEqual(filter_by_confidence(empty_data, 0.5), [])
        self.assertEqual(count_objects_by_category(empty_data), {})
        self.assertEqual(count_unique_tracks(empty_data), 0)
        
        # Test with single detection
        single_detection = edge_cases["single_detection"]
        
        filtered = filter_by_confidence(single_detection, 0.3)
        self.assertGreaterEqual(len(filtered), 0)
        
        counts = count_objects_by_category(single_detection)
        self.assertGreater(len(counts), 0)
        
        # Test with boundary cases
        boundary_data = edge_cases["boundary_bboxes"]
        
        # Should handle boundary cases without errors
        for bbox_data in boundary_data:
            area = get_bbox_area(bbox_data["bbox"])
            self.assertGreaterEqual(area, 0)
            
            center = get_bbox_center(bbox_data["bbox"])
            self.assertEqual(len(center), 2)


if __name__ == "__main__":
    unittest.main() 