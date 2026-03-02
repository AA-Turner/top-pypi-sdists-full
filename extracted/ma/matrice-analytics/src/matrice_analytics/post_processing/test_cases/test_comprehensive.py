"""
Comprehensive test suite for post processing module.

This module provides comprehensive test coverage for all post processing functionality
with correct API usage and data formats.
"""

import unittest
import time
import tempfile
import json
import os
from typing import Dict, List, Any

# Fix imports for proper module resolution
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.matrice_analytics.post_processing import (
    PostProcessor, ProcessingContext, ProcessingStatus, ProcessingResult,
    PeopleCountingConfig, CustomerServiceConfig,
    point_in_polygon, get_bbox_center, calculate_distance, calculate_iou,
    get_bbox_area, normalize_bbox, denormalize_bbox, line_segments_intersect,
    convert_to_coco_format, convert_to_yolo_format, match_results_structure,
    filter_by_confidence, filter_by_categories, count_objects_by_category,
    count_objects_in_zones, calculate_counting_summary
)
from src.matrice_analytics.post_processing.usecases.basic_counting_tracking import (
    BasicCountingTrackingUseCase, BasicCountingTrackingConfig
)


class TestPostProcessorCore(unittest.TestCase):
    """Test core PostProcessor functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = PostProcessor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_processor_initialization(self):
        """Test PostProcessor initialization."""
        processor = PostProcessor()
        self.assertIsNotNone(processor)
        
        # Check statistics initialization
        stats = processor.get_statistics()
        self.assertEqual(stats["total_processed"], 0)
        self.assertEqual(stats["successful"], 0)
        self.assertEqual(stats["failed"], 0)
    
    def test_simple_people_counting(self):
        """Test simple people counting processing."""
        # Create test detection data
        detections = [
            {"bbox": [10, 20, 50, 60], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 150, 200], "confidence": 0.9, "category": "person"},
            {"bbox": [200, 200, 250, 300], "confidence": 0.7, "category": "car"}
        ]
        
        # Process with simple interface
        result = self.processor.process_simple(
            detections, 
            "people_counting",
            confidence_threshold=0.6
        )
        
        # Verify result
        self.assertIsInstance(result, ProcessingResult)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assertIsNotNone(result.data)
        self.assertGreater(len(result.insights), 0)
    
    def test_people_counting_with_zones(self):
        """Test people counting with zone configuration."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},
            {"bbox": [125, 125, 175, 175], "confidence": 0.9, "category": "person"}
        ]
        
        zones = {
            "entrance": [[0, 0], [100, 0], [100, 100], [0, 100]],
            "lobby": [[100, 100], [200, 100], [200, 200], [100, 200]]
        }
        
        # Use zone_config parameter structure
        result = self.processor.process_simple(
            detections,
            "people_counting",
            confidence_threshold=0.5,
            zone_config={"zones": zones}
        )
        
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assertIsNotNone(result.data)
    
    def test_configuration_creation(self):
        """Test configuration creation."""
        # Test people counting config
        config = self.processor.create_config(
            "people_counting",
            confidence_threshold=0.7,
            enable_tracking=True
        )
        
        self.assertIsInstance(config, PeopleCountingConfig)
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertTrue(config.enable_tracking)
    
    def test_statistics_tracking(self):
        """Test processing statistics tracking."""
        detections = [{"bbox": [10, 20, 50, 60], "confidence": 0.8, "category": "person"}]
        
        # Process multiple times
        for _ in range(3):
            self.processor.process_simple(detections, "people_counting")
        
        stats = self.processor.get_statistics()
        self.assertEqual(stats["total_processed"], 3)
        self.assertGreaterEqual(stats["successful"], 0)


class TestGeometryUtils(unittest.TestCase):
    """Test geometry utility functions."""
    
    def test_point_in_polygon(self):
        """Test point in polygon detection."""
        # Square polygon
        square = [(0, 0), (100, 0), (100, 100), (0, 100)]
        
        # Test points inside
        self.assertTrue(point_in_polygon((50, 50), square))
        self.assertTrue(point_in_polygon((10, 10), square))
        self.assertTrue(point_in_polygon((90, 90), square))
        
        # Test points outside
        self.assertFalse(point_in_polygon((150, 50), square))
        self.assertFalse(point_in_polygon((50, 150), square))
        self.assertFalse(point_in_polygon((-10, 50), square))
    
    def test_get_bbox_center(self):
        """Test bounding box center calculation."""
        # Test list format
        bbox_list = [10, 20, 50, 60]
        center = get_bbox_center(bbox_list)
        self.assertEqual(center, (30.0, 40.0))
        
        # Test dict format
        bbox_dict = {"xmin": 10, "ymin": 20, "xmax": 50, "ymax": 60}
        center = get_bbox_center(bbox_dict)
        self.assertEqual(center, (30.0, 40.0))
    
    def test_calculate_distance(self):
        """Test distance calculation."""
        point1 = (0, 0)
        point2 = (3, 4)
        distance = calculate_distance(point1, point2)
        self.assertEqual(distance, 5.0)  # 3-4-5 triangle
    
    def test_calculate_iou(self):
        """Test IoU calculation with dict format."""
        # Identical boxes
        bbox1 = {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100}
        bbox2 = {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100}
        iou = calculate_iou(bbox1, bbox2)
        self.assertEqual(iou, 1.0)
        
        # Non-overlapping boxes
        bbox1 = {"xmin": 0, "ymin": 0, "xmax": 50, "ymax": 50}
        bbox2 = {"xmin": 100, "ymin": 100, "xmax": 150, "ymax": 150}
        iou = calculate_iou(bbox1, bbox2)
        self.assertEqual(iou, 0.0)
        
        # Partially overlapping boxes
        bbox1 = {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 100}
        bbox2 = {"xmin": 50, "ymin": 50, "xmax": 150, "ymax": 150}
        iou = calculate_iou(bbox1, bbox2)
        self.assertGreater(iou, 0.0)
        self.assertLess(iou, 1.0)
    
    def test_get_bbox_area(self):
        """Test bounding box area calculation."""
        bbox = {"xmin": 0, "ymin": 0, "xmax": 100, "ymax": 50}
        area = get_bbox_area(bbox)
        self.assertEqual(area, 5000.0)
    
    def test_normalize_denormalize_bbox(self):
        """Test bbox normalization and denormalization."""
        bbox = {"xmin": 100, "ymin": 200, "xmax": 300, "ymax": 400}
        image_width, image_height = 640, 480
        
        # Normalize
        normalized = normalize_bbox(bbox, image_width, image_height)
        self.assertAlmostEqual(normalized["xmin"], 100/640)
        self.assertAlmostEqual(normalized["ymin"], 200/480)
        
        # Denormalize back
        denormalized = denormalize_bbox(normalized, image_width, image_height)
        self.assertAlmostEqual(denormalized["xmin"], 100)
        self.assertAlmostEqual(denormalized["ymin"], 200)
    
    def test_line_segments_intersect(self):
        """Test line segment intersection detection."""
        # Intersecting lines
        p1, p2 = (0, 0), (100, 100)
        p3, p4 = (0, 100), (100, 0)
        self.assertTrue(line_segments_intersect(p1, p2, p3, p4))
        
        # Non-intersecting lines
        p1, p2 = (0, 0), (50, 50)
        p3, p4 = (100, 100), (150, 150)
        self.assertFalse(line_segments_intersect(p1, p2, p3, p4))


class TestFormatUtils(unittest.TestCase):
    """Test format utility functions."""
    
    def test_match_results_structure(self):
        """Test result structure matching."""
        # Detection format
        detections = [{"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"}]
        format_type = match_results_structure(detections)
        self.assertEqual(format_type.value, "detection")
        
        # Classification format
        classification = {"category": "person", "confidence": 0.8}
        format_type = match_results_structure(classification)
        self.assertEqual(format_type.value, "classification")
    
    def test_convert_to_coco_format(self):
        """Test conversion to COCO format."""
        detections = [
            {"bounding_box": {"xmin": 10, "ymin": 20, "xmax": 50, "ymax": 60}, "confidence": 0.8, "category": "person"},
            {"bounding_box": {"xmin": 100, "ymin": 100, "xmax": 150, "ymax": 200}, "confidence": 0.9, "category": "car"}
        ]
        
        coco_format = convert_to_coco_format(detections)
        
        self.assertEqual(len(coco_format), 2)
        
        # Check first detection
        first = coco_format[0]
        self.assertIn("bbox", first)
        self.assertIn("score", first)
        self.assertIn("category", first)
        self.assertEqual(first["score"], 0.8)
        self.assertEqual(first["category"], "person")
    
    def test_convert_to_yolo_format(self):
        """Test conversion to YOLO format."""
        detections = [
            {"bounding_box": {"xmin": 10, "ymin": 20, "xmax": 50, "ymax": 60}, "confidence": 0.8, "category": "person"}
        ]
        
        yolo_format = convert_to_yolo_format(detections)
        
        self.assertEqual(len(yolo_format), 1)
        self.assertEqual(len(yolo_format[0]), 6)  # [class_id, x_center, y_center, width, height, confidence]


class TestFilterUtils(unittest.TestCase):
    """Test filter utility functions."""
    
    def test_filter_by_confidence(self):
        """Test confidence-based filtering."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.9, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.3, "category": "person"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.7, "category": "car"}
        ]
        
        filtered = filter_by_confidence(detections, 0.5)
        self.assertEqual(len(filtered), 2)  # Only 0.9 and 0.7 confidence detections
        
        # Check that low confidence detection was filtered out
        confidences = [d["confidence"] for d in filtered]
        self.assertNotIn(0.3, confidences)
    
    def test_filter_by_categories(self):
        """Test category-based filtering."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.8, "category": "car"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.8, "category": "bike"}
        ]
        
        filtered = filter_by_categories(detections, ["person", "car"])
        self.assertEqual(len(filtered), 2)
        
        categories = [d["category"] for d in filtered]
        self.assertIn("person", categories)
        self.assertIn("car", categories)
        self.assertNotIn("bike", categories)


class TestCountingUtils(unittest.TestCase):
    """Test counting utility functions."""
    
    def test_count_objects_by_category(self):
        """Test object counting by category."""
        detections = [
            {"bbox": [0, 0, 100, 100], "confidence": 0.8, "category": "person"},
            {"bbox": [100, 100, 200, 200], "confidence": 0.8, "category": "person"},
            {"bbox": [200, 200, 300, 300], "confidence": 0.8, "category": "car"}
        ]
        
        counts = count_objects_by_category(detections)
        self.assertEqual(counts["person"], 2)
        self.assertEqual(counts["car"], 1)
    
    def test_count_objects_in_zones(self):
        """Test zone-based object counting."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},  # In zone1
            {"bbox": [125, 25, 175, 75], "confidence": 0.7, "category": "person"},  # In zone2
            {"bbox": [225, 225, 275, 275], "confidence": 0.9, "category": "car"}  # Outside zones
        ]
        
        zones = {
            "zone1": [[0, 0], [100, 0], [100, 100], [0, 100]],
            "zone2": [[100, 0], [200, 0], [200, 100], [100, 100]]
        }
        
        zone_counts = count_objects_in_zones(detections, zones)
        
        # Check that we have zone analysis
        self.assertIn("zone1", zone_counts)
        self.assertIn("zone2", zone_counts)
        
        # Check that person in zone1 is counted
        self.assertIn("person", zone_counts["zone1"])
        self.assertEqual(zone_counts["zone1"]["person"], 1)
    
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
        self.assertIn("total_objects", summary)
        self.assertIn("by_category", summary)
        self.assertEqual(summary["total_objects"], 3)
        self.assertEqual(summary["by_category"]["person"], 2)
        self.assertEqual(summary["by_category"]["car"], 1)


class TestBasicCountingTracking(unittest.TestCase):
    """Test basic counting tracking use case."""
    
    def setUp(self):
        """Set up test environment."""
        self.use_case = BasicCountingTrackingUseCase()
        self.processor = PostProcessor()
    
    def test_config_creation(self):
        """Test BasicCountingTrackingConfig creation."""
        config = BasicCountingTrackingConfig(
            confidence_threshold=0.7,
            target_categories=["person", "car"],
            zones={"entrance": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        )
        
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertEqual(config.target_categories, ["person", "car"])
        self.assertIn("entrance", config.zones)
        
        # Validate config
        errors = config.validate()
        self.assertEqual(len(errors), 0, f"Config validation failed: {errors}")
    
    def test_basic_processing(self):
        """Test basic counting tracking processing."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},
            {"bbox": [125, 125, 175, 175], "confidence": 0.9, "category": "person"}
        ]
        
        config = BasicCountingTrackingConfig(
            confidence_threshold=0.5,
            target_categories=["person"]
        )
        
        context = ProcessingContext()
        result = self.use_case.process(detections, config, context)
        
        self.assertIsInstance(result, ProcessingResult)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assertIsNotNone(result.data)
    
    def test_zone_based_processing(self):
        """Test zone-based processing."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},
            {"bbox": [125, 125, 175, 175], "confidence": 0.9, "category": "person"}
        ]
        
        config = BasicCountingTrackingConfig(
            confidence_threshold=0.5,
            target_categories=["person"],
            zones={
                "zone1": [[0, 0], [100, 0], [100, 100], [0, 100]],
                "zone2": [[100, 100], [200, 100], [200, 200], [100, 200]]
            }
        )
        
        result = self.use_case.process(detections, config)
        
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assertIsNotNone(result.data)
        
        # Check that zone analysis is included
        if "zone_analysis" in result.data:
            zone_analysis = result.data["zone_analysis"]
            self.assertIsInstance(zone_analysis, dict)


class TestIntegration(unittest.TestCase):
    """Test integration scenarios."""
    
    def setUp(self):
        """Set up test environment."""
        self.processor = PostProcessor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_end_to_end_people_counting(self):
        """Test end-to-end people counting scenario."""
        # Create realistic detection data
        detections = [
            {"bbox": [50, 50, 100, 150], "confidence": 0.85, "category": "person"},
            {"bbox": [200, 100, 250, 200], "confidence": 0.92, "category": "person"},
            {"bbox": [300, 50, 400, 100], "confidence": 0.78, "category": "car"},
            {"bbox": [450, 150, 500, 250], "confidence": 0.65, "category": "person"}
        ]
        
        # Define zones for entrance monitoring
        zones = {
            "entrance": [[0, 0], [150, 0], [150, 300], [0, 300]],
            "lobby": [[150, 0], [400, 0], [400, 300], [150, 300]],
            "exit": [[400, 0], [550, 0], [550, 300], [400, 300]]
        }
        
        # Process with people counting using correct zone_config structure
        result = self.processor.process_simple(
            detections,
            "people_counting",
            confidence_threshold=0.7,
            zone_config={"zones": zones},
            person_categories=["person"]
        )
        
        # Verify results
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assertIsNotNone(result.data)
        self.assertGreater(len(result.insights), 0)
        
        # Check that processing time is recorded
        self.assertGreaterEqual(result.processing_time, 0)
    
    def test_configuration_file_workflow(self):
        """Test configuration file save/load workflow."""
        # Create configuration
        config = self.processor.create_config(
            "people_counting",
            confidence_threshold=0.8,
            enable_tracking=True
        )
        
        # Save to file
        config_file = os.path.join(self.temp_dir, "test_config.json")
        self.processor.save_config(config, config_file)
        
        # Verify file exists
        self.assertTrue(os.path.exists(config_file))
        
        # Load configuration
        loaded_config = self.processor.load_config(config_file)
        
        # Verify loaded config
        self.assertEqual(loaded_config.confidence_threshold, 0.8)
        self.assertEqual(loaded_config.enable_tracking, True)
    
    def test_multiple_use_cases(self):
        """Test processing with multiple use cases."""
        detections = [
            {"bbox": [25, 25, 75, 75], "confidence": 0.8, "category": "person"},
            {"bbox": [125, 125, 175, 175], "confidence": 0.9, "category": "person"}
        ]
        
        # Test people counting
        result1 = self.processor.process_simple(
            detections, "people_counting", confidence_threshold=0.5
        )
        self.assertIn(result1.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Test basic counting tracking
        result2 = self.processor.process_simple(
            detections, "basic_counting_tracking", 
            confidence_threshold=0.5,
            target_categories=["person"]
        )
        self.assertIn(result2.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Verify both processed successfully
        self.assertIsNotNone(result1.data)
        self.assertIsNotNone(result2.data)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2) 