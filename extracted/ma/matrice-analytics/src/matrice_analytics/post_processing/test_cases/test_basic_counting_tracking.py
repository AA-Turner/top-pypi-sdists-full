"""
Tests for BasicCountingTrackingUseCase.

This module tests the basic counting and tracking functionality including
line crossing detection, zone-based counting, and tracking integration.
"""

import unittest
import time
from typing import Dict, List, Any
import tempfile
import os

# Fix imports for proper module resolution
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from src.matrice_analytics.post_processing import (
    PostProcessor, ProcessingResult, ProcessingStatus, ProcessingContext,
    BasicCountingTrackingUseCase, BaseConfig
)
from src.matrice_analytics.post_processing.usecases.basic_counting_tracking import BasicCountingTrackingUseCase, BasicCountingTrackingConfig
from src.matrice_analytics.post_processing.core.config import TrackingConfig, AlertConfig

from .test_utilities import BasePostProcessingTest, StressTestMixin, ConcurrencyTestMixin
from .test_data_generators import (
    create_detection_results, create_tracking_results, create_zone_polygons,
    create_line_crossing_data, create_basic_counting_tracking_scenarios,
    create_edge_case_data, create_performance_test_data
)


class TestBasicCountingTrackingUseCase(BasePostProcessingTest, StressTestMixin):
    """Test BasicCountingTrackingUseCase functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.use_case = BasicCountingTrackingUseCase()
        self.basic_config = BasicCountingTrackingConfig(
            confidence_threshold=0.5,
            enable_tracking=True
        )
    
    def test_use_case_initialization(self):
        """Test use case initialization."""
        self.assertEqual(self.use_case.name, "basic_counting_tracking")
        self.assertEqual(self.use_case.category, "general")
        self.assertIsNotNone(self.use_case.get_config_schema())
    
    def test_config_schema_validation(self):
        """Test configuration schema validation."""
        schema = self.use_case.get_config_schema()
        
        # Check required schema properties
        self.assertIn("type", schema)
        self.assertEqual(schema["type"], "object")
        self.assertIn("properties", schema)
        
        # Check key configuration properties
        properties = schema["properties"]
        self.assertIn("confidence_threshold", properties)
        self.assertIn("enable_tracking", properties)
        self.assertIn("zones", properties)
        self.assertIn("lines", properties)
    
    def test_default_config_creation(self):
        """Test default configuration creation."""
        config = self.use_case.create_default_config()
        
        self.assertIsInstance(config, BasicCountingTrackingConfig)
        self.assertEqual(config.category, "general")
        self.assertEqual(config.usecase, "basic_counting_tracking")
        self.assertIsNotNone(config.confidence_threshold)
        
        # Validate config
        errors = config.validate()
        self.assertEqual(len(errors), 0, f"Default config validation failed: {errors}")
    
    def test_config_with_overrides(self):
        """Test configuration creation with overrides."""
        config = self.use_case.create_default_config(
            confidence_threshold=0.7,
            enable_tracking=True,
            zones={"entrance": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        )
        
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertTrue(config.enable_tracking)
        self.assertIn("entrance", config.zones)
    
    def test_basic_detection_processing(self):
        """Test basic detection processing."""
        # Create test data
        detections = create_detection_results(
            num_detections=15,
            categories=["person", "car"],
            confidence_range=(0.6, 0.9)
        )
        
        # Process with use case
        result = self.use_case.process(detections, self.basic_config)
        
        # Validate result
        self.assert_processing_result(
            result,
            expected_status=ProcessingStatus.SUCCESS,
            min_insights=1,
            required_metrics=["total_count", "category_counts"]
        )
        
        # Check specific metrics
        self.assertIn("total_count", result.metrics)
        self.assertIn("category_counts", result.metrics)
        self.assertGreater(result.metrics["total_count"], 0)
    
    def test_tracking_processing(self):
        """Test tracking data processing."""
        # Create tracking data
        tracks = create_tracking_results(
            num_tracks=8,
            frames=15,
            categories=["person", "vehicle"]
        )
        
        # Create config with tracking enabled
        config = self.use_case.create_default_config(
            confidence_threshold=0.5,
            enable_tracking=True
        )
        
        # Process
        result = self.use_case.process(tracks, config)
        
        # Validate result
        self.assert_processing_result(result, min_insights=1)
        
        # Check tracking-specific metrics
        self.assertIn("unique_tracks", result.metrics)
        self.assertIn("track_duration_stats", result.metrics)
        self.assertGreater(result.metrics["unique_tracks"], 0)
    
    def test_zone_based_counting(self):
        """Test zone-based counting functionality."""
        # Create zones
        zones = create_zone_polygons(["entrance", "lobby", "exit"])
        
        # Create detection data
        detections = create_detection_results(num_detections=20)
        
        # Create config with zones
        config = self.use_case.create_default_config(
            confidence_threshold=0.5,
            zones=zones
        )
        
        # Process
        result = self.use_case.process(detections, config)
        
        # Validate result
        self.assert_processing_result(result, min_insights=1)
        
        # Check zone analysis
        self.assertIn("zone_analysis", result.metrics)
        zone_analysis = result.metrics["zone_analysis"]
        
        for zone_name in zones.keys():
            self.assertIn(zone_name, zone_analysis)
    
    def test_line_crossing_detection(self):
        """Test line crossing detection."""
        # Define crossing lines
        lines = {
            "entrance_line": [[100, 200], [200, 200]],
            "exit_line": [[400, 200], [500, 200]]
        }
        
        # Create crossing data
        crossing_data = create_line_crossing_data(lines, num_tracks=6, frames=25)
        
        # Create config with lines
        config = self.use_case.create_default_config(
            confidence_threshold=0.5,
            enable_tracking=True,
            lines=lines
        )
        
        # Process
        result = self.use_case.process(crossing_data, config)
        
        # Validate result
        self.assert_processing_result(result, min_insights=1)
        
        # Check line crossing analysis
        self.assertIn("line_crossings", result.metrics)
        line_crossings = result.metrics["line_crossings"]
        
        for line_name in lines.keys():
            self.assertIn(line_name, line_crossings)
    
    def test_combined_zones_and_lines(self):
        """Test processing with both zones and lines."""
        # Create zones and lines
        zones = create_zone_polygons(["zone_a", "zone_b"])
        lines = {"crossing_line": [[200, 100], [200, 300]]}
        
        # Create tracking data
        tracks = create_tracking_results(num_tracks=10, frames=20)
        
        # Create comprehensive config
        config = self.use_case.create_default_config(
            confidence_threshold=0.5,
            enable_tracking=True,
            zones=zones,
            lines=lines
        )
        
        # Process
        result = self.use_case.process(tracks, config)
        
        # Validate result
        self.assert_processing_result(result, min_insights=2)
        
        # Check both zone and line analysis
        self.assertIn("zone_analysis", result.metrics)
        self.assertIn("line_crossings", result.metrics)
    
    def test_confidence_filtering(self):
        """Test confidence threshold filtering."""
        # Create data with varying confidence levels
        low_conf_detections = create_detection_results(
            num_detections=10,
            confidence_range=(0.2, 0.4)
        )
        high_conf_detections = create_detection_results(
            num_detections=10,
            confidence_range=(0.7, 0.9)
        )
        
        all_detections = low_conf_detections + high_conf_detections
        
        # Test with high threshold
        high_threshold_config = self.use_case.create_default_config(
            confidence_threshold=0.6
        )
        
        result = self.use_case.process(all_detections, high_threshold_config)
        
        # Should filter out low confidence detections
        self.assert_processing_result(result)
        filtered_count = result.metrics["total_count"]
        
        # Test with low threshold
        low_threshold_config = self.use_case.create_default_config(
            confidence_threshold=0.1
        )
        
        result = self.use_case.process(all_detections, low_threshold_config)
        unfiltered_count = result.metrics["total_count"]
        
        # High threshold should result in fewer detections
        self.assertLessEqual(filtered_count, unfiltered_count)
    
    def test_empty_data_handling(self):
        """Test handling of empty input data."""
        empty_data = []
        
        result = self.use_case.process(empty_data, self.basic_config)
        
        self.assert_processing_result(result)
        self.assertEqual(result.metrics["total_count"], 0)
        self.assertIn("No objects detected", result.insights)
    
    def test_malformed_data_handling(self):
        """Test handling of malformed input data."""
        edge_cases = create_edge_case_data()
        malformed_data = edge_cases["malformed_data"]
        
        # Should handle gracefully without crashing
        result = self.use_case.process(malformed_data, self.basic_config)
        
        # May succeed with warnings or fail gracefully
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING, ProcessingStatus.ERROR])
        
        if result.status == ProcessingStatus.SUCCESS:
            self.assertGreaterEqual(len(result.warnings), 1)
    
    def test_invalid_configuration(self):
        """Test handling of invalid configuration."""
        # Create invalid config
        invalid_config = BasicCountingTrackingConfig(
            confidence_threshold=1.5,  # Invalid: > 1.0
            enable_tracking=True
        )
        
        # Validation should fail
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        
        # Processing should handle invalid config gracefully
        detections = create_detection_results(5)
        result = self.use_case.process(detections, invalid_config)
        
        # Should return error or warning
        self.assertIn(result.status, [ProcessingStatus.ERROR, ProcessingStatus.WARNING])
    
    def test_large_dataset_processing(self):
        """Test processing of large datasets."""
        # Create large dataset
        large_data = create_performance_test_data("large")
        detections = large_data["detection_data"]
        
        # Measure performance
        result, metrics = self.measure_performance(
            self.use_case.process,
            detections,
            self.basic_config
        )
        
        # Validate result
        self.assert_processing_result(result)
        
        # Check performance is acceptable
        self.assert_performance_acceptable(metrics, max_time=10.0, max_memory_mb=1000.0)
    
    def test_stress_testing(self):
        """Test stress testing with multiple iterations."""
        def test_iteration():
            detections = create_detection_results(50)
            result = self.use_case.process(detections, self.basic_config)
            self.assert_processing_result(result)
            return result
        
        stress_results = self.run_stress_test(test_iteration, iterations=50, max_failures=5)
        
        # Check stress test results
        self.assertGreaterEqual(stress_results["successful"], 45)  # 90% success rate
        self.assertLessEqual(stress_results["failed"], 5)
        
        if stress_results["execution_times"]:
            self.assertLess(stress_results["avg_execution_time"], 2.0)
    
    def test_scenarios_from_data_generator(self):
        """Test predefined scenarios from data generator."""
        scenarios = create_basic_counting_tracking_scenarios()
        
        for scenario in scenarios:
            with self.subTest(scenario=scenario["name"]):
                # Create config from scenario
                config_dict = scenario["config"]
                config = self.use_case.create_default_config(**config_dict)
                
                # Process scenario data
                result = self.use_case.process(scenario["data"], config)
                
                # Validate result
                self.assert_processing_result(result, min_insights=1)
                
                # Check scenario-specific expectations
                if scenario["name"] == "line_crossing":
                    self.assertIn("line_crossings", result.metrics)
                elif scenario["name"] == "zone_tracking":
                    self.assertIn("zone_analysis", result.metrics)
    
    def test_processing_context_usage(self):
        """Test processing with custom context."""
        detections = create_detection_results(10)
        
        # Create custom context
        context = ProcessingContext(
            confidence_threshold=0.6,
            enable_tracking=True,
            enable_counting=True,
            metadata={"test_id": "context_test"}
        )
        
        result = self.use_case.process(detections, self.basic_config, context)
        
        self.assert_processing_result(result)
        self.assertIsNotNone(result.context)
        self.assertEqual(result.context.metadata["test_id"], "context_test")
    
    def test_metrics_completeness(self):
        """Test that all expected metrics are present."""
        # Create comprehensive test data
        tracks = create_tracking_results(num_tracks=5, frames=10)
        zones = create_zone_polygons(["test_zone"])
        
        config = self.use_case.create_default_config(
            confidence_threshold=0.5,
            enable_tracking=True,
            zones=zones
        )
        
        result = self.use_case.process(tracks, config)
        
        # Check expected metrics
        expected_metrics = [
            "total_count",
            "category_counts",
            "unique_tracks",
            "zone_analysis",
            "processing_info"
        ]
        
        for metric in expected_metrics:
            self.assertIn(metric, result.metrics, f"Missing expected metric: {metric}")
    
    def test_insights_generation(self):
        """Test insight generation."""
        detections = create_detection_results(
            num_detections=25,
            categories=["person", "vehicle"]
        )
        
        result = self.use_case.process(detections, self.basic_config)
        
        self.assert_processing_result(result, min_insights=1)
        
        # Check that insights are meaningful
        insights_text = " ".join(result.insights).lower()
        self.assertTrue(
            any(keyword in insights_text for keyword in ["detected", "counted", "objects", "categories"]),
            "Insights should contain meaningful information"
        )
    
    def test_summary_generation(self):
        """Test summary generation."""
        detections = create_detection_results(15)
        result = self.use_case.process(detections, self.basic_config)
        
        self.assert_processing_result(result)
        self.assertIsNotNone(result.summary)
        self.assertGreater(len(result.summary), 0)
        
        # Summary should contain key information
        summary_lower = result.summary.lower()
        self.assertTrue(
            any(keyword in summary_lower for keyword in ["detected", "counted", "objects"]),
            f"Summary should contain meaningful information: {result.summary}"
        )


class TestBasicCountingTrackingIntegration(BasePostProcessingTest, ConcurrencyTestMixin):
    """Integration tests for BasicCountingTrackingUseCase."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.use_case = BasicCountingTrackingUseCase()
    
    def test_processor_integration(self):
        """Test integration with PostProcessor."""
        detections = create_detection_results(10)
        
        # Test through PostProcessor
        result = self.processor.process_simple(
            detections,
            "basic_counting_tracking",
            confidence_threshold=0.5,
            enable_tracking=True
        )
        
        self.assert_processing_result(result)
    
    def test_concurrent_processing(self):
        """Test concurrent processing."""
        def process_data():
            detections = create_detection_results(20)
            config = self.use_case.create_default_config(confidence_threshold=0.5)
            return self.use_case.process(detections, config)
        
        concurrent_results = self.run_concurrent_test(
            process_data,
            num_threads=3,
            iterations_per_thread=5
        )
        
        # Check concurrent processing results
        self.assertGreaterEqual(concurrent_results["success_rate"], 0.9)
        self.assertEqual(concurrent_results["failed"], 0)
    
    def test_configuration_file_integration(self):
        """Test integration with configuration files."""
        # Create config dict
        config_dict = {
            "category": "general",
            "usecase": "basic_counting_tracking",
            "confidence_threshold": 0.6,
            "enable_tracking": True,
            "zones": create_zone_polygons(["test_zone"])
        }
        
        # Create temporary config file
        config_file = self.create_temp_config_file(config_dict, "json")
        
        # Test processing from file
        detections = create_detection_results(15)
        result = self.processor.process_from_file(detections, config_file)
        
        self.assert_processing_result(result)
    
    def test_memory_stability(self):
        """Test memory stability over multiple processing cycles."""
        initial_memory = self.process.memory_info().rss / 1024 / 1024
        
        # Process multiple batches
        for i in range(10):
            detections = create_detection_results(100)
            config = self.use_case.create_default_config(confidence_threshold=0.5)
            result = self.use_case.process(detections, config)
            self.assert_processing_result(result)
        
        final_memory = self.process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB)
        self.assertLess(memory_increase, 100.0, 
                       f"Memory increased by {memory_increase:.2f}MB, possible memory leak")


if __name__ == "__main__":
    unittest.main() 