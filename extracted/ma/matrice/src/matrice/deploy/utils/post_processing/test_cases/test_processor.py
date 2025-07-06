"""
Comprehensive tests for the PostProcessor class.

This module tests the main PostProcessor functionality including:
- Simple processing interface
- Configuration-based processing
- File-based configuration
- Error handling
- Performance characteristics
"""

import unittest
import json
import os
import time
from unittest.mock import patch, MagicMock

from .test_utilities import BasePostProcessingTest
from .test_data_generators import (
    create_detection_results, create_tracking_results,
    create_people_counting_config, create_customer_service_config,
    create_edge_case_data, create_performance_test_data
)

from src.matrice.deploy.utils.post_processing import (
    PostProcessor, ProcessingStatus, ProcessingContext,
    PeopleCountingConfig, CustomerServiceConfig, ConfigValidationError
)


class TestPostProcessor(BasePostProcessingTest):
    """Test cases for PostProcessor class."""
    
    def test_processor_initialization(self):
        """Test that PostProcessor initializes correctly."""
        processor = PostProcessor()
        
        # Check that statistics are initialized
        stats = processor.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats["total_processed"], 0)
        self.assertEqual(stats["successful"], 0)
        self.assertEqual(stats["failed"], 0)
        
        # Check that use cases are available
        use_cases = processor.list_available_usecases()
        self.assertIsInstance(use_cases, dict)
        self.assertIn("general", use_cases)
        self.assertIn("sales", use_cases)
    
    def test_simple_people_counting_processing(self):
        """Test simple people counting processing."""
        # Create test data
        test_data = create_detection_results(
            num_detections=10,
            categories=["person", "car", "bicycle"]
        )
        
        # Process with simple interface
        result = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            enable_tracking=True
        )
        
        # Validate result
        self.assert_processing_result_valid(
            result,
            expected_usecase="people_counting",
            expected_category="general"
        )
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        self.assert_insights_generated(result, min_insights=1)
        
        # Check for expected metrics (using actual names from implementation)
        expected_metrics = ["total_people", "processing_time", "input_format"]
        self.assert_metrics_present(result, expected_metrics)
    
    def test_simple_customer_service_processing(self):
        """Test simple customer service processing."""
        # Create test data with relevant categories
        test_data = create_detection_results(
            num_detections=15,
            categories=["person", "staff", "customer"]
        )
        
        # Process with simple interface
        result = self.processor.process_simple(
            test_data,
            usecase="customer_service",
            confidence_threshold=0.6,
            service_proximity_threshold=100.0
        )
        
        # Validate result (may return WARNING status for some scenarios)
        self.assert_processing_result_valid(
            result,
            expected_usecase="customer_service",
            expected_category="sales"
        )
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        self.assert_insights_generated(result, min_insights=1)
    
    def test_configuration_based_processing(self):
        """Test processing with configuration objects."""
        # Create test data
        test_data = create_detection_results(num_detections=8)
        
        # Create configuration
        config = create_people_counting_config(
            confidence_threshold=0.7,
            enable_tracking=True,
            include_zones=True,
            include_alerts=True
        )
        
        # Process with configuration
        result = self.processor.process(test_data, config)
        
        # Validate result
        self.assert_processing_result_valid(
            result,
            expected_usecase="people_counting",
            expected_category="general"
        )
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check that zone analysis was performed (using actual metric names)
        if result.metrics.get("zones_analyzed", 0) > 0:
            self.assertIn("zone_metrics", result.metrics)
    
    def test_file_based_configuration(self):
        """Test processing with configuration files."""
        # Create test data
        test_data = create_detection_results(num_detections=5)
        
        # Create configuration
        config = create_people_counting_config(confidence_threshold=0.6)
        
        # Save configuration to file
        config_file = self.create_temp_config_file(config, "people_counting_test.json")
        
        # Process from file
        result = self.processor.process_from_file(test_data, config_file)
        
        # Validate result
        self.assert_processing_result_valid(
            result,
            expected_usecase="people_counting",
            expected_category="general"
        )
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
    
    def test_invalid_configuration_handling(self):
        """Test handling of invalid configurations."""
        test_data = create_detection_results(num_detections=3)
        
        # Test with invalid confidence threshold
        config = PeopleCountingConfig(
            category="general",
            usecase="people_counting",
            confidence_threshold=1.5  # Invalid: >1.0
        )
        
        result = self.processor.process(test_data, config)
        
        # Should handle gracefully
        self.assertIsInstance(result.status, ProcessingStatus)
        if result.status == ProcessingStatus.ERROR:
            self.assertIsNotNone(result.error_message)
    
    def test_unknown_usecase_handling(self):
        """Test handling of unknown use cases."""
        test_data = create_detection_results(num_detections=3)
        
        # Try to process with unknown use case
        result = self.processor.process_simple(
            test_data,
            usecase="unknown_usecase",
            confidence_threshold=0.5
        )
        
        # Should return error result
        self.assertEqual(result.status, ProcessingStatus.ERROR)
        self.assertIsNotNone(result.error_message)
        # Check for appropriate error message
        self.assertTrue(
            "unknown" in result.error_message.lower() or 
            "not found" in result.error_message.lower()
        )
    
    def test_empty_data_handling(self):
        """Test handling of empty input data."""
        # Test with empty list
        result = self.processor.process_simple(
            [],
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should handle gracefully
        self.assertIsInstance(result.status, ProcessingStatus)
        if result.status == ProcessingStatus.SUCCESS:
            # Check for appropriate message indicating no data
            self.assertTrue(
                "no people" in result.summary.lower() or 
                "no detections" in result.summary.lower() or
                "empty" in result.summary.lower()
            )
    
    def test_malformed_data_handling(self):
        """Test handling of malformed input data."""
        # Test with malformed detections
        malformed_data = create_edge_case_data()
        
        result = self.processor.process_simple(
            malformed_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Should handle gracefully - either success with warnings or error
        self.assertIsInstance(result.status, ProcessingStatus)
        if result.status == ProcessingStatus.WARNING:
            self.assertTrue(len(result.warnings) > 0)
    
    def test_context_propagation(self):
        """Test that processing context is properly propagated."""
        test_data = create_detection_results(num_detections=3)
        
        # Create context with specific parameters
        context = ProcessingContext(
            confidence_threshold=0.8,
            enable_tracking=True,
            enable_analytics=True,
            metadata={"source": "test_camera", "location": "test_location"}
        )
        
        # Process with context
        result = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.8,
            context=context
        )
        
        # Check context propagation
        self.assertIsNotNone(result.context)
        self.assertEqual(result.context.confidence_threshold, 0.8)
        self.assertTrue(result.context.enable_tracking)
        self.assertTrue(result.context.enable_analytics)
        self.assertEqual(result.context.metadata.get("source"), "test_camera")
        self.assertEqual(result.context.metadata.get("location"), "test_location")
    
    def test_statistics_tracking(self):
        """Test that processing statistics are tracked correctly."""
        # Get initial statistics
        initial_stats = self.processor.get_statistics()
        
        # Process some data
        test_data = create_detection_results(num_detections=3)
        
        # Successful processing
        result1 = self.processor.process_simple(
            test_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Check intermediate statistics
        intermediate_stats = self.processor.get_statistics()
        self.assertEqual(intermediate_stats["total_processed"], initial_stats["total_processed"] + 1)
        self.assertEqual(intermediate_stats["successful"], initial_stats["successful"] + 1)
        
        # Failed processing (unknown use case) - this should not increment counters
        try:
            result2 = self.processor.process_simple(
                test_data,
                usecase="unknown_usecase"
            )
        except Exception:
            pass  # Expected to fail
        
        # Check final statistics - failed request shouldn't be counted
        final_stats = self.processor.get_statistics()
        self.assertEqual(final_stats["total_processed"], initial_stats["total_processed"] + 1)
        self.assertEqual(final_stats["successful"], initial_stats["successful"] + 1)
    
    def test_config_template_generation(self):
        """Test configuration template generation."""
        # Test people counting template
        template = self.processor.get_config_template("people_counting")
        
        self.assertIsInstance(template, dict)
        self.assertIn("confidence_threshold", template)
        self.assertIn("enable_tracking", template)
        self.assertIn("person_categories", template)
        
        # Test customer service template
        template = self.processor.get_config_template("customer_service")
        
        self.assertIsInstance(template, dict)
        self.assertIn("service_proximity_threshold", template)
        self.assertIn("staff_categories", template)
        self.assertIn("customer_categories", template)
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid configuration
        valid_config = create_people_counting_config(confidence_threshold=0.5)
        errors = self.processor.validate_config(valid_config)
        self.assertEqual(len(errors), 0)
        
        # Invalid configuration
        invalid_config = PeopleCountingConfig(
            category="general",
            usecase="people_counting",
            confidence_threshold=2.0,  # Invalid
            time_window_minutes=-5     # Invalid
        )
        errors = self.processor.validate_config(invalid_config)
        self.assertGreater(len(errors), 0)
    
    def test_available_usecases_listing(self):
        """Test listing of available use cases."""
        use_cases = self.processor.list_available_usecases()
        
        self.assertIsInstance(use_cases, dict)
        
        # Check expected categories and use cases
        self.assertIn("general", use_cases)
        self.assertIn("people_counting", use_cases["general"])
        
        self.assertIn("sales", use_cases)
        self.assertIn("customer_service", use_cases["sales"])
    
    def test_supported_usecases_listing(self):
        """Test getting list of supported use case names."""
        supported = self.processor.get_supported_usecases()
        
        self.assertIsInstance(supported, list)
        self.assertIn("people_counting", supported)
        self.assertIn("customer_service", supported)
    
    def test_processing_with_tracking_data(self):
        """Test processing with tracking format data."""
        # Create tracking data
        tracking_data = create_tracking_results(
            num_tracks=5,
            categories=["person", "car"]
        )
        
        result = self.processor.process_simple(
            tracking_data,
            usecase="people_counting",
            confidence_threshold=0.5,
            enable_tracking=True
        )
        
        # Should handle tracking data format
        self.assert_processing_result_valid(result)
        
        # Should have basic metrics
        self.assertIn("total_people", result.metrics)
        self.assertIn("processing_time", result.metrics)
    
    def test_config_save_and_load(self):
        """Test saving and loading configurations."""
        # Create configuration
        original_config = create_customer_service_config(
            confidence_threshold=0.7,
            service_proximity_threshold=150.0
        )
        
        # Save configuration
        config_file = os.path.join(self.temp_dir, "customer_service_config.json")
        self.processor.save_config(original_config, config_file)
        
        # Load configuration
        loaded_config = self.processor.load_config(config_file)
        
        # Compare configurations
        self.assertEqual(original_config.usecase, loaded_config.usecase)
        self.assertEqual(original_config.category, loaded_config.category)
        self.assertEqual(original_config.confidence_threshold, loaded_config.confidence_threshold)
        self.assertEqual(original_config.service_proximity_threshold, loaded_config.service_proximity_threshold)
    
    def test_reset_statistics(self):
        """Test resetting processing statistics."""
        # Process some data to generate statistics
        test_data = create_detection_results(num_detections=3)
        self.processor.process_simple(test_data, usecase="people_counting")
        
        # Check that statistics exist
        stats_before = self.processor.get_statistics()
        self.assertGreater(stats_before["total_processed"], 0)
        
        # Reset statistics
        self.processor.reset_statistics()
        
        # Check that statistics are reset
        stats_after = self.processor.get_statistics()
        self.assertEqual(stats_after["total_processed"], 0)
        self.assertEqual(stats_after["successful"], 0)
        self.assertEqual(stats_after["failed"], 0)
        self.assertEqual(stats_after["total_processing_time"], 0.0)


class TestPostProcessorPerformance(BasePostProcessingTest):
    """Performance tests for PostProcessor."""
    
    def test_large_dataset_processing(self):
        """Test processing performance with large datasets."""
        # Create large dataset
        large_data = create_performance_test_data(size=1000)
        
        # Measure processing time
        result, processing_time = self.measure_processing_time(
            self.processor.process_simple,
            large_data,
            usecase="people_counting",
            confidence_threshold=0.5
        )
        
        # Check that processing completed successfully
        self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check performance (should complete within reasonable time)
        self.assert_performance_acceptable(processing_time, max_time=5.0)
        
        # Check basic metrics are present
        self.assertIn("total_people", result.metrics)
        self.assertIn("processing_time", result.metrics)
    
    def test_batch_processing_performance(self):
        """Test performance with multiple batch processing calls."""
        # Create multiple small batches
        batches = [create_detection_results(num_detections=50) for _ in range(10)]
        
        total_start_time = time.time()
        results = []
        
        for batch in batches:
            result = self.processor.process_simple(
                batch,
                usecase="people_counting",
                confidence_threshold=0.5
            )
            results.append(result)
        
        total_processing_time = time.time() - total_start_time
        
        # Check that all batches processed successfully
        for result in results:
            self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check overall performance
        self.assert_performance_acceptable(total_processing_time, max_time=10.0)
        
        # Check statistics
        stats = self.processor.get_statistics()
        self.assertEqual(stats["total_processed"], len(batches))
        self.assertEqual(stats["successful"], len(batches))
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable during processing."""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Process multiple datasets
        for i in range(20):
            test_data = create_detection_results(num_detections=100)
            result = self.processor.process_simple(
                test_data,
                usecase="people_counting",
                confidence_threshold=0.5
            )
            self.assertEqual(result.status, ProcessingStatus.SUCCESS)
        
        # Check final memory usage
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        max_memory_increase = 100 * 1024 * 1024  # 100MB
        self.assertLess(memory_increase, max_memory_increase,
                       f"Memory increased by {memory_increase / 1024 / 1024:.2f}MB")


if __name__ == "__main__":
    import time
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestPostProcessor))
    suite.addTest(unittest.makeSuite(TestPostProcessorPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    print(f"\nTest execution completed in {end_time - start_time:.2f} seconds")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}") 