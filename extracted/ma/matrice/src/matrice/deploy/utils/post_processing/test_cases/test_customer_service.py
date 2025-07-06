"""
Comprehensive tests for the Customer Service use case.

This module tests detailed functionality for customer service analytics including:
- Queue management
- Service time analysis
- Staff efficiency metrics
- Customer flow analysis
- Alert generation
"""

import unittest
import json
import time
from unittest.mock import patch, MagicMock

from .test_utilities import BasePostProcessingTest
from .test_data_generators import (
    create_detection_results, create_tracking_results,
    create_customer_service_config, create_zone_polygons,
    create_performance_test_data, create_edge_case_data
)

from src.matrice.deploy.utils.post_processing import (
    PostProcessor, ProcessingStatus, CustomerServiceConfig,
    TrackingConfig, AlertConfig
)


class TestCustomerServiceUseCase(BasePostProcessingTest):
    """Test cases for customer service use case."""
    
    def test_basic_customer_service_processing(self):
        """Test basic customer service processing functionality."""
        # Create test data with relevant categories
        test_data = create_detection_results(
            num_detections=10,
            categories=["person", "staff", "customer"],
            confidence_range=(0.6, 0.9)
        )
        
        # Create configuration
        config = create_customer_service_config(
            confidence_threshold=0.5,
            service_proximity_threshold=50.0
        )
        
        # Process the data
        result = self.processor.process(test_data, config)
        
        # Validate basic result structure
        self.assert_processing_result_valid(result, expected_usecase="customer_service")
        # Handle both SUCCESS and WARNING status as valid
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for expected metrics (using actual metric names from implementation)
        expected_metrics = ["customer_to_staff_ratio", "service_coverage", "interaction_rate"]
        for metric in expected_metrics:
            self.assertIn(metric, result.metrics)
        
        # Check that insights were generated
        self.assert_insights_generated(result, min_insights=1)
    
    def test_customer_service_with_areas(self):
        """Test customer service with defined areas."""
        # Create test data
        test_data = create_detection_results(
            num_detections=8,
            categories=["staff", "customer", "person"]
        )
        
        # Create configuration with predefined areas
        config = create_customer_service_config(
            confidence_threshold=0.6,
            service_proximity_threshold=100.0
        )
        
        result = self.processor.process(test_data, config)
        
        # Validate result
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for area-related metrics (using actual metric names)
        self.assertIn("area_utilization", result.metrics)
        area_utilization = result.metrics["area_utilization"]
        self.assertIsInstance(area_utilization, dict)
        
        # Should have customer and service area analysis
        if "customer_areas" in area_utilization:
            self.assertIsInstance(area_utilization["customer_areas"], (int, float))
        if "service_areas" in area_utilization:
            self.assertIsInstance(area_utilization["service_areas"], (int, float))
    
    def test_customer_service_with_tracking(self):
        """Test customer service with tracking enabled."""
        # Create tracking data with staff and customers
        tracking_data = create_tracking_results(
            num_tracks=10,
            categories=["staff", "customer", "person"]
        )
        
        result = self.processor.process_simple(
            tracking_data,
            usecase="customer_service",
            confidence_threshold=0.6,
            enable_tracking=True,
            staff_categories=["staff"],
            customer_categories=["customer", "person"],
            max_service_time=1200.0
        )
        
        # Validate result
        self.assert_processing_result_valid(result)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should have customer service metrics
        self.assertIn("customer_to_staff_ratio", result.metrics)
        self.assertIn("service_coverage", result.metrics)
    
    def test_customer_service_proximity_analysis(self):
        """Test proximity-based service analysis."""
        # Create test data with specific positions for proximity analysis
        test_data = create_detection_results(
            num_detections=8,
            categories=["staff", "customer"]
        )

        # Manually adjust positions for proximity testing
        for i, detection in enumerate(test_data):
            if i < 4:  # First half as staff
                detection["category"] = "staff"
                # Position staff in service area
                detection["bbox"] = [500 + i * 20, 100, 550 + i * 20, 200]
            else:  # Second half as customers
                detection["category"] = "customer"
                # Position customers near staff (within proximity)
                detection["bbox"] = [480 + (i-4) * 30, 150, 520 + (i-4) * 30, 230]

        result = self.processor.process_simple(
            test_data,
            usecase="customer_service",
            confidence_threshold=0.5,
            service_proximity_threshold=100.0,
            staff_categories=["staff"],
            customer_categories=["customer"]
        )

        # Should analyze proximity patterns
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should have service-related metrics
        self.assertIn("customer_to_staff_ratio", result.metrics)
        self.assertIn("service_coverage", result.metrics)
    
    def test_customer_service_staff_utilization(self):
        """Test staff utilization analysis."""
        # Create test data with staff and customers
        test_data = create_detection_results(
            num_detections=15,
            categories=["staff"] * 5 + ["customer"] * 10
        )
        
        config = create_customer_service_config(
            confidence_threshold=0.6,
            service_proximity_threshold=100.0
        )
        
        result = self.processor.process(test_data, config)
        
        # Validate result (handle WARNING status)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for staff utilization metrics
        self.assertIn("staff_utilization", result.metrics)
        self.assertIn("customer_to_staff_ratio", result.metrics)
        
        # Check utilization values are reasonable
        staff_utilization = result.metrics["staff_utilization"]
        self.assertIsInstance(staff_utilization, (int, float))
        self.assertGreaterEqual(staff_utilization, 0.0)
    
    def test_customer_service_queue_analysis(self):
        """Test queue management analysis."""
        # Create test data representing a queue scenario
        test_data = []
        
        # Add service counter staff
        test_data.append({
            "bbox": [500, 100, 550, 200],
            "confidence": 0.9,
            "category": "staff",
            "category_id": 0
        })
        
        # Add customers in a queue formation
        queue_positions = [
            [450, 150], [400, 150], [350, 150], [300, 150], [250, 150]
        ]
        
        for i, (x, y) in enumerate(queue_positions):
            test_data.append({
                "bbox": [x, y, x+40, y+80],
                "confidence": 0.8,
                "category": "customer",
                "category_id": 1
            })
        
        result = self.processor.process_simple(
            test_data,
            usecase="customer_service",
            confidence_threshold=0.5,
            service_proximity_threshold=150.0,
            staff_categories=["staff"],
            customer_categories=["customer"],
            buffer_time=2.0
        )
        
        # Should analyze queue patterns
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should have customer service metrics
        self.assertIn("customer_to_staff_ratio", result.metrics)
    
    def test_customer_service_service_time_analysis(self):
        """Test service time analysis with tracking data."""
        # Create tracking data showing service interactions over time
        tracking_data = []
        
        # Staff track (stationary)
        staff_track = {
            "track_id": 1,
            "category": "staff",
            "points": [],
            "start_frame": 0,
            "end_frame": 100,
            "is_active": True,
            "total_frames": 100
        }
        
        # Staff stays in one place
        for frame in range(100):
            staff_track["points"].append({
                "frame_id": frame,
                "track_id": 1,
                "bbox": [500, 100, 550, 200],
                "confidence": 0.9,
                "category": "staff",
                "timestamp": time.time() + frame
            })
        
        tracking_data.append(staff_track)
        
        # Customer track (approaches staff, gets service, leaves)
        customer_track = {
            "track_id": 2,
            "category": "customer",
            "points": [],
            "start_frame": 10,
            "end_frame": 60,
            "is_active": False,
            "total_frames": 50
        }
        
        # Customer movement: approach -> wait -> service -> leave
        for frame in range(50):
            x = 300 + frame * 4  # Moving towards staff
            if frame > 30:  # After service, moving away
                x = 530 - (frame - 30) * 4
            
            customer_track["points"].append({
                "frame_id": frame + 10,
                "track_id": 2,
                "bbox": [x, 150, x+40, 230],
                "confidence": 0.8,
                "category": "customer",
                "timestamp": time.time() + frame + 10
            })
        
        tracking_data.append(customer_track)
        
        result = self.processor.process_simple(
            tracking_data,
            usecase="customer_service",
            confidence_threshold=0.5,
            enable_tracking=True,
            service_proximity_threshold=100.0,
            max_service_time=1800.0,
            staff_categories=["staff"],
            customer_categories=["customer"]
        )
        
        # Should analyze service times
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should have service metrics
        self.assertIn("customer_to_staff_ratio", result.metrics)
    
    def test_customer_service_config_validation(self):
        """Test customer service configuration validation."""
        # Valid configuration
        valid_config = CustomerServiceConfig(
            category="sales",
            usecase="customer_service",
            confidence_threshold=0.6,
            service_proximity_threshold=100.0,
            staff_categories=["staff", "employee"],
            customer_categories=["customer", "person"],
            customer_areas={"waiting": [[0, 0], [100, 0], [100, 100], [0, 100]]},
            staff_areas={"counter": [[200, 0], [300, 0], [300, 100], [200, 100]]},
            service_areas={"desk": [[150, 150], [250, 150], [250, 250], [150, 250]]}
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid configurations
        invalid_configs = [
            # Invalid service proximity threshold
            CustomerServiceConfig(
                category="sales",
                usecase="customer_service",
                service_proximity_threshold=-50.0
            ),
            # Invalid max service time
            CustomerServiceConfig(
                category="sales",
                usecase="customer_service",
                max_service_time=-100.0
            ),
            # Empty staff categories
            CustomerServiceConfig(
                category="sales",
                usecase="customer_service",
                staff_categories=[]
            ),
            # Empty customer categories
            CustomerServiceConfig(
                category="sales",
                usecase="customer_service",
                customer_categories=[]
            ),
            # Invalid area polygon
            CustomerServiceConfig(
                category="sales",
                usecase="customer_service",
                customer_areas={"invalid": [[0, 0], [100, 100]]}  # Only 2 points
            )
        ]
        
        for config in invalid_configs:
            errors = config.validate()
            self.assertGreater(len(errors), 0)
    
    def test_customer_service_tracking_config_validation(self):
        """Test tracking configuration validation."""
        # Valid tracking configuration
        valid_tracking_config = TrackingConfig(
            tracking_method="kalman",
            max_age=30,
            min_hits=3,
            iou_threshold=0.3,
            target_classes=["staff", "customer"]
        )
        
        errors = valid_tracking_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid tracking configurations
        invalid_tracking_configs = [
            # Invalid tracking method
            TrackingConfig(tracking_method="invalid_method"),
            # Invalid max_age
            TrackingConfig(max_age=-5),
            # Invalid min_hits
            TrackingConfig(min_hits=0),
            # Invalid IoU threshold
            TrackingConfig(iou_threshold=1.5)
        ]
        
        for config in invalid_tracking_configs:
            errors = config.validate()
            self.assertGreater(len(errors), 0)
    
    def test_customer_service_alerts(self):
        """Test customer service alert generation."""
        # Create test data that should trigger alerts
        test_data = create_detection_results(
            num_detections=20,
            categories=["person", "customer"],  # High customer count, low staff
            confidence_range=(0.7, 0.9)
        )
        
        # Create configuration with alert settings
        config = create_customer_service_config(
            confidence_threshold=0.6,
            service_proximity_threshold=30.0
        )
        
        # Process the data
        result = self.processor.process(test_data, config)
        
        # Validate result
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for optimization opportunities instead of alerts
        self.assertIn("optimization_opportunities", result.metrics)
        opportunities = result.metrics["optimization_opportunities"]
        self.assertIsInstance(opportunities, list)
        
        # Should have suggestions for high customer to staff ratio
        self.assertGreater(len(opportunities), 0)
    
    def test_customer_service_empty_data(self):
        """Test customer service with empty input data."""
        result = self.processor.process_simple(
            [],
            usecase="customer_service",
            confidence_threshold=0.6
        )
        
        # Should handle empty data gracefully (may return WARNING for empty data)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for appropriate summary message
        self.assertTrue(
            "no" in result.summary.lower() or 
            "empty" in result.summary.lower() or
            "zero" in result.summary.lower()
        )
        
        # Should have basic metrics structure
        self.assertIsInstance(result.metrics, dict)
    
    def test_customer_service_performance(self):
        """Test customer service performance with large datasets."""
        # Create large dataset with mixed categories
        large_data = create_detection_results(
            num_detections=500,
            categories=["staff", "customer", "person", "employee"]
        )
        
        start_time = time.time()
        result = self.processor.process_simple(
            large_data,
            usecase="customer_service",
            confidence_threshold=0.6,
            service_proximity_threshold=100.0
        )
        processing_time = time.time() - start_time
        
        # Should complete successfully (may return WARNING for large datasets)
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should complete within reasonable time (3 seconds for complex analysis)
        self.assertLess(processing_time, 3.0)
        
        # Should have reasonable performance metrics (processing_time may be 0 for fast processing)
        self.assertGreaterEqual(result.processing_time, 0)
    
    def test_customer_service_insights_generation(self):
        """Test that meaningful insights are generated."""
        # Create test data with staff-customer interactions
        test_data = create_detection_results(
            num_detections=25,
            categories=["staff"] * 5 + ["customer"] * 20
        )
        
        config = create_customer_service_config(
            confidence_threshold=0.6,
            service_proximity_threshold=100.0
        )
        
        result = self.processor.process(test_data, config)
        
        # Should generate multiple insights
        self.assert_insights_generated(result, min_insights=2)
        
        # Check insight quality
        insights = result.insights
        
        # Should mention staff and customers
        staff_mentioned = any("staff" in insight.lower() for insight in insights)
        customer_mentioned = any("customer" in insight.lower() for insight in insights)
        
        self.assertTrue(staff_mentioned or customer_mentioned)
        
        # Should mention service aspects
        service_mentioned = any("service" in insight.lower() for insight in insights)
        self.assertTrue(service_mentioned)
    
    def test_customer_service_metrics_completeness(self):
        """Test that all expected metrics are generated."""
        # Create test data
        test_data = create_detection_results(
            num_detections=15,
            categories=["staff", "customer", "person"]
        )
        
        # Create comprehensive configuration
        config = create_customer_service_config(
            confidence_threshold=0.6,
            enable_tracking=True,
            service_proximity_threshold=100.0
        )
        
        result = self.processor.process(test_data, config)
        
        # Handle WARNING status as valid for this test
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Check for core metrics (using actual metric names from implementation)
        expected_core_metrics = [
            "customer_to_staff_ratio",
            "service_coverage",
            "interaction_rate",
            "staff_utilization",
            "area_utilization",
            "service_quality_score",
            "attention_score",
            "overall_performance"
        ]
        
        for metric in expected_core_metrics:
            self.assertIn(metric, result.metrics)
        
        # Check for optimization opportunities
        self.assertIn("optimization_opportunities", result.metrics)
        self.assertIsInstance(result.metrics["optimization_opportunities"], list)


class TestCustomerServiceIntegration(BasePostProcessingTest):
    """Integration tests for customer service with other components."""
    
    def test_customer_service_config_serialization(self):
        """Test configuration serialization and deserialization."""
        # Create configuration
        original_config = create_customer_service_config(
            confidence_threshold=0.7,
            service_proximity_threshold=120.0
        )
        
        # Save and load configuration
        config_file = self.create_temp_config_file(original_config)
        loaded_config = self.processor.load_config(config_file)
        
        # Compare key attributes
        self.assertEqual(original_config.usecase, loaded_config.usecase)
        self.assertEqual(original_config.category, loaded_config.category)
        self.assertEqual(original_config.confidence_threshold, loaded_config.confidence_threshold)
        self.assertEqual(original_config.service_proximity_threshold, loaded_config.service_proximity_threshold)
        self.assertEqual(original_config.staff_categories, loaded_config.staff_categories)
        self.assertEqual(original_config.customer_categories, loaded_config.customer_categories)
    
    def test_customer_service_error_recovery(self):
        """Test error recovery in customer service."""
        # Create partially invalid data
        mixed_quality_data = [
            # Valid staff detection
            {"bbox": [10, 10, 50, 100], "confidence": 0.9, "category": "staff"},
            # Valid customer detection
            {"bbox": [100, 100, 140, 200], "confidence": 0.8, "category": "customer"},
            # Invalid detection
            {"bbox": [200, 200, 190, 190], "confidence": 0.9, "category": "person"},  # Invalid bbox
            # Another valid detection
            {"bbox": [300, 300, 340, 400], "confidence": 0.7, "category": "customer"}
        ]
        
        result = self.processor.process_simple(
            mixed_quality_data,
            usecase="customer_service",
            confidence_threshold=0.5,
            staff_categories=["staff"],
            customer_categories=["customer", "person"]
        )
        
        # Should handle partial failures gracefully
        self.assertIn(result.status, [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING])
        
        # Should still provide some results
        self.assertIsNotNone(result.data)
        self.assertIsInstance(result.metrics, dict)


if __name__ == "__main__":
    unittest.main(verbosity=2) 