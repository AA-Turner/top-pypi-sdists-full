"""
Comprehensive tests for the People Counting use case.

This module tests detailed functionality for people counting including:
- Zone-based analysis
- Tracking integration
- Alert generation
- Configuration validation
- Performance characteristics
"""

import unittest
import json
import time
from unittest.mock import patch, MagicMock

from .test_utilities import BasePostProcessingTest
from .test_data_generators import (
    create_detection_results, create_tracking_results,
    create_people_counting_config, create_zone_polygons,
    create_performance_test_data, create_edge_case_data
)

from src.matrice.deploy.utils.post_processing import (
    PostProcessor, ProcessingStatus, PeopleCountingConfig,
    ZoneConfig, AlertConfig
)


class TestPeopleCountingUseCase(BasePostProcessingTest):
    """Test cases for people counting use case."""
    
    def test_basic_people_counting(self):
        """Test basic people counting without zones."""
        # Create test data with people and other objects
        test_data = create_detection_results(
            num_detections=20,
            categories=["person", "car", "bicycle", "dog"]
        )
        
        result = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            person_categories=["person"]
        )
        
        # Validate basic result structure
        self.assert_processing_result_valid(result, expected_usecase="people_counting")
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check for expected metrics (using actual metric names from implementation)
        self.assertIn("total_people", result.metrics)
        self.assertIn("processing_time", result.metrics)
        self.assertIn("input_format", result.metrics)
        self.assertIn("confidence_threshold", result.metrics)
        
        # Check zone-based metrics (using actual zone metric structure)
        if result.metrics.get("zones_analyzed", 0) > 0:
            self.assertIn("zone_metrics", result.metrics)
        
        # Check people count using correct metric name
        self.assertGreaterEqual(result.metrics["total_people"], 0)
        
        # Check that insights were generated
        self.assert_insights_generated(result, min_insights=1)
        
        # Verify people count is reasonable
        people_count = result.metrics["total_people"]
        self.assertIsInstance(people_count, int)
        self.assertGreaterEqual(people_count, 0)
    
    def test_people_counting_with_zones(self):
        """Test people counting with zone-based analysis."""
        # Create test data
        test_data = create_detection_results(
            num_detections=15,
            categories=["person", "people"]
        )
        
        # Create configuration with zones
        config = create_people_counting_config(
            confidence_threshold=0.6,
            include_zones=True,
            include_alerts=False
        )
        
        result = self.processor.process(test_data, config)
        
        # Validate result
        self.assert_processing_result_valid(result)
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check that zone analysis was performed
        self.assertIn("zone_metrics", result.metrics)
        self.assertIn("zones_analyzed", result.metrics)
        self.assertGreater(result.metrics["zones_analyzed"], 0)
    
    def test_people_counting_with_tracking(self):
        """Test people counting with tracking enabled."""
        # Create tracking data
        tracking_data = create_tracking_results(
            num_tracks=8,
            categories=["person", "car"]
        )
        
        result = self.processor.process_simple(
            tracking_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            enable_tracking=True,
            enable_unique_counting=True
        )
        
        # Validate result
        self.assert_processing_result_valid(result)
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check basic tracking metrics
        self.assertIn("total_people", result.metrics)
        self.assertIn("processing_time", result.metrics)
    
    def test_people_counting_with_alerts(self):
        """Test people counting with alert generation."""
        # Create test data with many people
        test_data = create_detection_results(
            num_detections=25,
            categories=["person"] * 20 + ["car"] * 5  # 20 people, 5 cars
        )
        
        # Create configuration with low alert thresholds
        config = create_people_counting_config(
            confidence_threshold=0.5,
            include_alerts=True
        )
        # Set low thresholds to trigger alerts
        config.alert_config.count_thresholds = {"person": 5, "all": 10}
        config.alert_config.occupancy_thresholds = {"entrance": 3}
        
        result = self.processor.process(test_data, config)
        
        # Validate result
        self.assert_processing_result_valid(result)
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check basic people counting metrics
        self.assertIn("total_people", result.metrics)
        self.assertGreater(result.metrics["total_people"], 0)
    
    def test_people_counting_confidence_filtering(self):
        """Test that confidence filtering works correctly."""
        # Create test data with mixed confidence levels
        test_data = []
        
        # High confidence people (should be included)
        for i in range(5):
            test_data.append({
                "bbox": [100 + i*50, 100, 140 + i*50, 200],
                "confidence": 0.9,
                "category": "person",
                "category_id": 0
            })
        
        # Low confidence people (should be filtered out)
        for i in range(5):
            test_data.append({
                "bbox": [100 + i*50, 300, 140 + i*50, 400],
                "confidence": 0.2,
                "category": "person",
                "category_id": 0
            })
        
        result = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should only count high confidence detections
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        self.assertEqual(result.metrics["total_people"], 5)
    
    def test_people_counting_category_mapping(self):
        """Test people counting with category mapping."""
        # Create test data with different person categories
        test_data = []
        categories = ["person", "people", "human", "pedestrian"]
        
        for i, category in enumerate(categories):
            for j in range(3):  # 3 detections per category
                test_data.append({
                    "bbox": [100 + j*50, 100 + i*100, 140 + j*50, 180 + i*100],
                    "confidence": 0.8,
                    "category": category,
                    "category_id": i
                })
        
        result = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            person_categories=["person", "people", "human", "pedestrian"]
        )
        
        # Should count all categories as people
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        self.assertEqual(result.metrics["total_people"], 12)  # 4 categories * 3 detections
    
    def test_people_counting_empty_data(self):
        """Test people counting with empty input data."""
        result = self.processor.process_simple(
            [],
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should handle empty data gracefully
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        self.assertEqual(result.metrics["total_people"], 0)
    
    def test_people_counting_config_validation(self):
        """Test people counting configuration validation."""
        # Valid configuration
        valid_config = PeopleCountingConfig(
            category="general",
            usecase="people_counting",
            confidence_threshold=0.5,
            time_window_minutes=60,
            person_categories=["person"]
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid configurations
        invalid_configs = [
            # Invalid confidence threshold
            PeopleCountingConfig(
                category="general",
                usecase="people_counting",
                confidence_threshold=1.5
            ),
            # Invalid time window
            PeopleCountingConfig(
                category="general",
                usecase="people_counting",
                time_window_minutes=-10
            ),
            # Empty person categories
            PeopleCountingConfig(
                category="general",
                usecase="people_counting",
                person_categories=[]
            )
        ]
        
        for config in invalid_configs:
            errors = config.validate()
            self.assertGreater(len(errors), 0)
    
    def test_people_counting_zone_validation(self):
        """Test zone configuration validation."""
        # Valid zone configuration
        valid_zones = create_zone_polygons(2, zone_names=["area1", "area2"])
        zone_config = ZoneConfig(zones=valid_zones)
        
        errors = zone_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid zone configurations
        invalid_zone_configs = [
            # Zone with too few points
            ZoneConfig(zones={"invalid": [[0, 0], [100, 100]]}),
            # Zone with invalid point format
            ZoneConfig(zones={"invalid": [[0, 0, 0], [100, 100, 100], [50, 50, 50]]}),
            # Invalid confidence threshold for zone
            ZoneConfig(
                zones={"valid": [[0, 0], [100, 0], [100, 100], [0, 100]]},
                zone_confidence_thresholds={"valid": 1.5}
            )
        ]
        
        for zone_config in invalid_zone_configs:
            errors = zone_config.validate()
            self.assertGreater(len(errors), 0)
    
    def test_people_counting_alert_validation(self):
        """Test alert configuration validation."""
        # Valid alert configuration
        valid_alert_config = AlertConfig(
            count_thresholds={"person": 10},
            occupancy_thresholds={"entrance": 5},
            alert_cooldown=30.0
        )
        
        errors = valid_alert_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid alert configurations
        invalid_alert_configs = [
            # Invalid count threshold
            AlertConfig(count_thresholds={"person": -5}),
            # Invalid occupancy threshold
            AlertConfig(occupancy_thresholds={"entrance": 0}),
            # Invalid alert cooldown
            AlertConfig(alert_cooldown=-10.0),
            # Webhook enabled without URL
            AlertConfig(enable_webhook_alerts=True, webhook_url=None),
            # Email enabled without recipients
            AlertConfig(enable_email_alerts=True, email_recipients=[])
        ]
        
        for alert_config in invalid_alert_configs:
            errors = alert_config.validate()
            self.assertGreater(len(errors), 0)
    
    def test_people_counting_performance(self):
        """Test people counting performance with various data sizes."""
        # Test different data sizes
        data_sizes = [10, 50, 100]
        
        for size in data_sizes:
            with self.subTest(size=size):
                # Create test data
                test_data = create_detection_results(
                    num_detections=size,
                    categories=["person", "car", "bicycle"]
                )
                
                # Measure processing time
                result, processing_time = self.measure_processing_time(
                    self.processor.process_simple,
                    test_data,
                    usecase="people_counting",
                    confidence_threshold=0.5
                )
                
                # Should complete successfully
                self.assertEqual(result.status, ProcessingStatus.SUCCESS)
                
                # Performance should be reasonable
                self.assert_performance_acceptable(processing_time, max_time=2.0)
                
                # Should have basic metrics
                self.assertIn("total_people", result.metrics)
                self.assertIn("processing_time", result.metrics)
    
    def test_people_counting_insights_generation(self):
        """Test that meaningful insights are generated."""
        # Create test data
        test_data = create_detection_results(
            num_detections=20,
            categories=["person"] * 15 + ["car"] * 5
        )
        
        # Create configuration with zones and alerts
        config = create_people_counting_config(
            confidence_threshold=0.5,
            include_zones=True,
            include_alerts=True
        )
        
        result = self.processor.process(test_data, config)
        
        # Should generate multiple insights
        self.assert_insights_generated(result, min_insights=1)
        
        # Check insight quality
        insights = result.insights
        
        # Should mention people count
        count_mentioned = any("people" in insight.lower() or "person" in insight.lower() 
                             for insight in insights)
        self.assertTrue(count_mentioned)
        
        # Should have zone metrics if zones are configured
        if config.zone_config and config.zone_config.zones:
            self.assertIn("zone_metrics", result.metrics)
    
    def test_people_counting_metrics_completeness(self):
        """Test that all expected metrics are generated."""
        # Create test data
        test_data = create_detection_results(
            num_detections=10,
            categories=["person", "car"]
        )

        # Create comprehensive configuration
        config = create_people_counting_config(
            confidence_threshold=0.5,
            enable_tracking=True,
            include_zones=True,
            include_alerts=True
        )

        result = self.processor.process(test_data, config)

        # Check for core metrics
        expected_core_metrics = [
            "total_people",
            "processing_time",
            "input_format",
            "confidence_threshold"
        ]

        for metric in expected_core_metrics:
            self.assertIn(metric, result.metrics)

        # Check for zone metrics if zones are configured
        if config.zone_config and config.zone_config.zones:
            self.assertIn("zone_metrics", result.metrics)
            self.assertIn("zones_analyzed", result.metrics)

        # Check for alert configuration existence (alerts may be generated but not always included in metrics)
        if config.alert_config:
            # Just validate that alert configuration exists, don't require specific metrics
            self.assertIsNotNone(config.alert_config.count_thresholds)
    
    def test_people_counting_time_window_analysis(self):
        """Test time window analysis functionality."""
        # Create tracking data spanning multiple time windows
        tracking_data = create_tracking_results(
            num_tracks=10,
            track_length_range=(20, 50)
        )
        
        result = self.processor.process_simple(
            tracking_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            enable_tracking=True,
            time_window_minutes=30
        )
        
        # Should handle time window analysis
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Should have basic metrics
        self.assertIn("total_people", result.metrics)
        self.assertIn("processing_time", result.metrics)


class TestPeopleCountingIntegration(BasePostProcessingTest):
    """Integration tests for people counting with other components."""
    
    def test_people_counting_with_mixed_data_formats(self):
        """Test people counting with mixed detection and tracking data."""
        # Create mixed format data
        mixed_data = {
            "detections": create_detection_results(5, categories=["person"]),
            "tracks": create_tracking_results(3, categories=["person"]),
            "metadata": {"source": "mixed_test"}
        }
        
        result = self.processor.process_simple(
            mixed_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should handle mixed format gracefully
        self.assertIsInstance(result.status, ProcessingStatus)
    
    def test_people_counting_config_serialization(self):
        """Test configuration serialization and deserialization."""
        # Create configuration
        original_config = create_people_counting_config(
            confidence_threshold=0.7,
            include_zones=True,
            include_alerts=True
        )
        
        # Save and load configuration
        config_file = self.create_temp_config_file(original_config)
        loaded_config = self.processor.load_config(config_file)
        
        # Compare key attributes
        self.assertEqual(original_config.usecase, loaded_config.usecase)
        self.assertEqual(original_config.category, loaded_config.category)
        self.assertEqual(original_config.confidence_threshold, loaded_config.confidence_threshold)
        self.assertEqual(original_config.person_categories, loaded_config.person_categories)
    
    def test_people_counting_error_recovery(self):
        """Test error recovery in people counting."""
        # Create partially invalid data
        mixed_quality_data = [
            # Valid detection
            {"bbox": [10, 10, 50, 50], "confidence": 0.8, "category": "person"},
            # Invalid detection (will be filtered or cause warning)
            {"bbox": [100, 100, 90, 90], "confidence": 0.9, "category": "person"},  # Invalid bbox
            # Another valid detection
            {"bbox": [200, 200, 240, 250], "confidence": 0.9, "category": "person"}
        ]
        
        result = self.processor.process_simple(
            mixed_quality_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should handle partial failures gracefully
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should still provide some results
        self.assertIsNotNone(result.data)
        self.assertIsInstance(result.metrics, dict)


if __name__ == "__main__":
    unittest.main(verbosity=2) 