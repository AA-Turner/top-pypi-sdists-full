"""
Tests for post processing configuration system.

This module tests all configuration classes, validation, serialization,
ConfigManager functionality, and file-based configuration management.
"""

import unittest
import json
import yaml
import tempfile
import os
from typing import Dict, List, Any

# Fix imports for proper module resolution
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from matrice.deploy.utils.post_processing.core.config import (
    BaseConfig, PeopleCountingConfig, CustomerServiceConfig,
    ZoneConfig, TrackingConfig, AlertConfig, ConfigManager, config_manager,
    ConfigValidationError
)
from matrice.deploy.utils.post_processing.usecases.basic_counting_tracking import BasicCountingTrackingConfig

from .test_utilities import BasePostProcessingTest
from .test_data_generators import create_zone_polygons, create_customer_service_areas


class TestBaseConfig(BasePostProcessingTest):
    """Test BaseConfig functionality."""
    
    def test_base_config_creation(self):
        """Test basic configuration creation."""
        config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.7
        )
        
        self.assertEqual(config.category, "test")
        self.assertEqual(config.usecase, "test_usecase")
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertEqual(config.version, "1.0")
    
    def test_base_config_validation(self):
        """Test base configuration validation."""
        # Valid config
        valid_config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.7
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid confidence threshold
        invalid_config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=1.5  # > 1.0
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("confidence_threshold" in error for error in errors))
        
        # Negative confidence threshold
        invalid_config2 = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=-0.1
        )
        
        errors = invalid_config2.validate()
        self.assertGreater(len(errors), 0)
    
    def test_base_config_serialization(self):
        """Test configuration serialization."""
        config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.7,
            enable_tracking=True
        )
        
        # Test to_dict
        config_dict = config.to_dict()
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["category"], "test")
        self.assertEqual(config_dict["confidence_threshold"], 0.7)
        self.assertEqual(config_dict["enable_tracking"], True)
        
        # Test from_dict
        restored_config = BaseConfig.from_dict(config_dict)
        self.assertEqual(restored_config.category, config.category)
        self.assertEqual(restored_config.confidence_threshold, config.confidence_threshold)
        self.assertEqual(restored_config.enable_tracking, config.enable_tracking)
    
    def test_base_config_json_serialization(self):
        """Test JSON serialization."""
        config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.7
        )
        
        # Test to_json
        json_str = config.to_json()
        self.assertIsInstance(json_str, str)
        
        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertEqual(parsed["category"], "test")
        
        # Test from_json
        restored_config = BaseConfig.from_json(json_str)
        self.assertEqual(restored_config.category, config.category)
        self.assertEqual(restored_config.confidence_threshold, config.confidence_threshold)
    
    def test_config_inheritance(self):
        """Test configuration parameter inheritance."""
        base_config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.6,
            enable_tracking=True
        )
        
        # Override some parameters
        child_config = BaseConfig(
            category="test",
            usecase="test_usecase",
            confidence_threshold=0.8,  # Override
            enable_tracking=True,      # Keep same
            enable_counting=True       # New parameter
        )
        
        self.assertEqual(child_config.confidence_threshold, 0.8)
        self.assertEqual(child_config.enable_tracking, True)
        self.assertEqual(child_config.enable_counting, True)


class TestPeopleCountingConfig(BasePostProcessingTest):
    """Test PeopleCountingConfig functionality."""
    
    def test_people_counting_config_creation(self):
        """Test people counting configuration creation."""
        zones = create_zone_polygons(["entrance", "lobby", "exit"])
        
        config = PeopleCountingConfig(
            confidence_threshold=0.6,
            enable_tracking=True,
            enable_unique_counting=True,
            time_window_minutes=30,
            person_categories=["person", "people"],
            zones=zones
        )
        
        self.assertEqual(config.category, "people_counting")
        self.assertEqual(config.usecase, "people_counting")
        self.assertEqual(config.confidence_threshold, 0.6)
        self.assertTrue(config.enable_tracking)
        self.assertTrue(config.enable_unique_counting)
        self.assertEqual(config.time_window_minutes, 30)
        self.assertEqual(config.person_categories, ["person", "people"])
        self.assertEqual(config.zones, zones)
    
    def test_people_counting_config_validation(self):
        """Test people counting configuration validation."""
        # Valid config
        valid_config = PeopleCountingConfig(
            confidence_threshold=0.6,
            time_window_minutes=30,
            person_categories=["person"]
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid time window
        invalid_config = PeopleCountingConfig(
            confidence_threshold=0.6,
            time_window_minutes=-10,  # Negative
            person_categories=["person"]
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        
        # Empty person categories
        invalid_config2 = PeopleCountingConfig(
            confidence_threshold=0.6,
            person_categories=[]  # Empty
        )
        
        errors = invalid_config2.validate()
        self.assertGreater(len(errors), 0)
    
    def test_people_counting_config_with_zones(self):
        """Test people counting configuration with zone validation."""
        # Valid zones
        valid_zones = create_zone_polygons(["entrance", "lobby"])
        
        config = PeopleCountingConfig(
            confidence_threshold=0.6,
            zones=valid_zones
        )
        
        errors = config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid zones (too few points)
        invalid_zones = {
            "entrance": [[0, 0], [100, 0]]  # Only 2 points
        }
        
        config_invalid = PeopleCountingConfig(
            confidence_threshold=0.6,
            zones=invalid_zones
        )
        
        errors = config_invalid.validate()
        self.assertGreater(len(errors), 0)
    
    def test_people_counting_config_serialization(self):
        """Test people counting configuration serialization."""
        zones = create_zone_polygons(["entrance", "lobby"])
        
        config = PeopleCountingConfig(
            confidence_threshold=0.7,
            enable_unique_counting=True,
            zones=zones,
            person_categories=["person", "people"]
        )
        
        # Serialize and deserialize
        config_dict = config.to_dict()
        restored_config = PeopleCountingConfig.from_dict(config_dict)
        
        self.assertEqual(restored_config.confidence_threshold, config.confidence_threshold)
        self.assertEqual(restored_config.enable_unique_counting, config.enable_unique_counting)
        self.assertEqual(restored_config.zones, config.zones)
        self.assertEqual(restored_config.person_categories, config.person_categories)


class TestCustomerServiceConfig(BasePostProcessingTest):
    """Test CustomerServiceConfig functionality."""
    
    def test_customer_service_config_creation(self):
        """Test customer service configuration creation."""
        areas = create_customer_service_areas()
        
        config = CustomerServiceConfig(
            confidence_threshold=0.7,
            enable_tracking=True,
            customer_categories=["customer", "person"],
            staff_categories=["staff", "employee"],
            service_proximity_threshold=150.0,
            max_service_time=600.0,
            **areas
        )
        
        self.assertEqual(config.category, "customer_service")
        self.assertEqual(config.usecase, "customer_service")
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertEqual(config.customer_categories, ["customer", "person"])
        self.assertEqual(config.staff_categories, ["staff", "employee"])
        self.assertEqual(config.service_proximity_threshold, 150.0)
        self.assertEqual(config.max_service_time, 600.0)
        self.assertIn("customer_areas", config.to_dict())
        self.assertIn("staff_areas", config.to_dict())
    
    def test_customer_service_config_validation(self):
        """Test customer service configuration validation."""
        areas = create_customer_service_areas()
        
        # Valid config
        valid_config = CustomerServiceConfig(
            confidence_threshold=0.7,
            customer_categories=["customer"],
            staff_categories=["staff"],
            service_proximity_threshold=150.0,
            **areas
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid proximity threshold
        invalid_config = CustomerServiceConfig(
            confidence_threshold=0.7,
            customer_categories=["customer"],
            staff_categories=["staff"],
            service_proximity_threshold=-50.0,  # Negative
            **areas
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        
        # Empty categories
        invalid_config2 = CustomerServiceConfig(
            confidence_threshold=0.7,
            customer_categories=[],  # Empty
            staff_categories=["staff"],
            **areas
        )
        
        errors = invalid_config2.validate()
        self.assertGreater(len(errors), 0)
    
    def test_customer_service_config_serialization(self):
        """Test customer service configuration serialization."""
        areas = create_customer_service_areas()
        
        config = CustomerServiceConfig(
            confidence_threshold=0.8,
            customer_categories=["person"],
            staff_categories=["staff"],
            service_proximity_threshold=100.0,
            **areas
        )
        
        # Test JSON serialization
        json_str = config.to_json()
        restored_config = CustomerServiceConfig.from_json(json_str)
        
        self.assertEqual(restored_config.confidence_threshold, config.confidence_threshold)
        self.assertEqual(restored_config.customer_categories, config.customer_categories)
        self.assertEqual(restored_config.service_proximity_threshold, config.service_proximity_threshold)


class TestBasicCountingTrackingConfig(BasePostProcessingTest):
    """Test BasicCountingTrackingConfig functionality."""
    
    def test_basic_counting_tracking_config_creation(self):
        """Test basic counting tracking configuration creation."""
        zones = create_zone_polygons(["zone_a", "zone_b"])
        lines = {
            "entrance_line": [[100, 200], [200, 200]],
            "exit_line": [[400, 200], [500, 200]]
        }
        
        config = BasicCountingTrackingConfig(
            confidence_threshold=0.5,
            enable_tracking=True,
            zones=zones,
            lines=lines
        )
        
        self.assertEqual(config.category, "general")
        self.assertEqual(config.usecase, "basic_counting_tracking")
        self.assertEqual(config.confidence_threshold, 0.5)
        self.assertTrue(config.enable_tracking)
        self.assertEqual(config.zones, zones)
        self.assertEqual(config.lines, lines)
    
    def test_basic_counting_tracking_config_validation(self):
        """Test basic counting tracking configuration validation."""
        # Valid config
        valid_config = BasicCountingTrackingConfig(
            confidence_threshold=0.6,
            enable_tracking=True
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Valid config with zones and lines
        zones = create_zone_polygons(["zone_a"])
        lines = {"line1": [[0, 100], [200, 100]]}
        
        valid_config_full = BasicCountingTrackingConfig(
            confidence_threshold=0.6,
            zones=zones,
            lines=lines
        )
        
        errors = valid_config_full.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid line (not enough points)
        invalid_lines = {"line1": [[0, 100]]}  # Only 1 point
        
        invalid_config = BasicCountingTrackingConfig(
            confidence_threshold=0.6,
            lines=invalid_lines
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)


class TestZoneConfig(BasePostProcessingTest):
    """Test ZoneConfig functionality."""
    
    def test_zone_config_creation(self):
        """Test zone configuration creation."""
        polygon = [[0, 0], [100, 0], [100, 100], [0, 100]]
        
        zone_config = ZoneConfig(
            name="test_zone",
            polygon=polygon,
            zone_type="entrance",
            enabled=True
        )
        
        self.assertEqual(zone_config.name, "test_zone")
        self.assertEqual(zone_config.polygon, polygon)
        self.assertEqual(zone_config.zone_type, "entrance")
        self.assertTrue(zone_config.enabled)
    
    def test_zone_config_validation(self):
        """Test zone configuration validation."""
        # Valid zone
        valid_polygon = [[0, 0], [100, 0], [100, 100], [0, 100]]
        valid_zone = ZoneConfig(
            name="valid_zone",
            polygon=valid_polygon
        )
        
        errors = valid_zone.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid zone (too few points)
        invalid_polygon = [[0, 0], [100, 0]]
        invalid_zone = ZoneConfig(
            name="invalid_zone",
            polygon=invalid_polygon
        )
        
        errors = invalid_zone.validate()
        self.assertGreater(len(errors), 0)
        
        # Empty name
        invalid_zone2 = ZoneConfig(
            name="",
            polygon=valid_polygon
        )
        
        errors = invalid_zone2.validate()
        self.assertGreater(len(errors), 0)


class TestAlertConfig(BasePostProcessingTest):
    """Test AlertConfig functionality."""
    
    def test_alert_config_creation(self):
        """Test alert configuration creation."""
        alert_config = AlertConfig(
            enabled=True,
            count_thresholds={"person": 50, "vehicle": 20},
            occupancy_thresholds={"lobby": 30, "entrance": 15},
            alert_cooldown_minutes=5
        )
        
        self.assertTrue(alert_config.enabled)
        self.assertEqual(alert_config.count_thresholds["person"], 50)
        self.assertEqual(alert_config.occupancy_thresholds["lobby"], 30)
        self.assertEqual(alert_config.alert_cooldown_minutes, 5)
    
    def test_alert_config_validation(self):
        """Test alert configuration validation."""
        # Valid config
        valid_config = AlertConfig(
            enabled=True,
            count_thresholds={"person": 50},
            alert_cooldown_minutes=5
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid cooldown
        invalid_config = AlertConfig(
            enabled=True,
            alert_cooldown_minutes=-1  # Negative
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        
        # Invalid threshold values
        invalid_config2 = AlertConfig(
            enabled=True,
            count_thresholds={"person": -10}  # Negative threshold
        )
        
        errors = invalid_config2.validate()
        self.assertGreater(len(errors), 0)


class TestTrackingConfig(BasePostProcessingTest):
    """Test TrackingConfig functionality."""
    
    def test_tracking_config_creation(self):
        """Test tracking configuration creation."""
        tracking_config = TrackingConfig(
            enabled=True,
            max_age=30,
            min_hits=3,
            iou_threshold=0.3,
            track_buffer_size=1000
        )
        
        self.assertTrue(tracking_config.enabled)
        self.assertEqual(tracking_config.max_age, 30)
        self.assertEqual(tracking_config.min_hits, 3)
        self.assertEqual(tracking_config.iou_threshold, 0.3)
        self.assertEqual(tracking_config.track_buffer_size, 1000)
    
    def test_tracking_config_validation(self):
        """Test tracking configuration validation."""
        # Valid config
        valid_config = TrackingConfig(
            enabled=True,
            max_age=30,
            min_hits=3,
            iou_threshold=0.3
        )
        
        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)
        
        # Invalid IoU threshold
        invalid_config = TrackingConfig(
            enabled=True,
            iou_threshold=1.5  # > 1.0
        )
        
        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)
        
        # Invalid max_age
        invalid_config2 = TrackingConfig(
            enabled=True,
            max_age=0  # Should be > 0
        )
        
        errors = invalid_config2.validate()
        self.assertGreater(len(errors), 0)


class TestConfigManager(BasePostProcessingTest):
    """Test ConfigManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.config_manager = ConfigManager()
    
    def test_config_registration(self):
        """Test configuration registration."""
        # Register configs
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        self.config_manager.register_config("customer_service", CustomerServiceConfig)
        
        # Check registration
        self.assertIn("people_counting", self.config_manager.get_registered_configs())
        self.assertIn("customer_service", self.config_manager.get_registered_configs())
    
    def test_config_creation(self):
        """Test configuration creation through manager."""
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        
        # Create config
        config = self.config_manager.create_config(
            "people_counting",
            confidence_threshold=0.7,
            enable_tracking=True
        )
        
        self.assertIsInstance(config, PeopleCountingConfig)
        self.assertEqual(config.confidence_threshold, 0.7)
        self.assertTrue(config.enable_tracking)
    
    def test_config_validation_through_manager(self):
        """Test configuration validation through manager."""
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        
        # Valid config
        valid_config = self.config_manager.create_config(
            "people_counting",
            confidence_threshold=0.6
        )
        
        is_valid, errors = self.config_manager.validate_config(valid_config)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Invalid config
        invalid_config = PeopleCountingConfig(
            confidence_threshold=1.5  # Invalid
        )
        
        is_valid, errors = self.config_manager.validate_config(invalid_config)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_config_file_operations(self):
        """Test configuration file save/load operations."""
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        
        # Create config
        config = self.config_manager.create_config(
            "people_counting",
            confidence_threshold=0.8,
            enable_tracking=True,
            person_categories=["person", "people"]
        )
        
        # Save to file
        config_file = os.path.join(self.temp_dir, "test_config.json")
        self.config_manager.save_config_to_file(config, config_file)
        
        # Check file exists
        self.assertTrue(os.path.exists(config_file))
        
        # Load from file
        loaded_config = self.config_manager.load_config_from_file(config_file)
        
        self.assertIsInstance(loaded_config, PeopleCountingConfig)
        self.assertEqual(loaded_config.confidence_threshold, config.confidence_threshold)
        self.assertEqual(loaded_config.enable_tracking, config.enable_tracking)
        self.assertEqual(loaded_config.person_categories, config.person_categories)
    
    def test_config_yaml_operations(self):
        """Test YAML configuration operations."""
        self.config_manager.register_config("customer_service", CustomerServiceConfig)
        
        areas = create_customer_service_areas()
        config = self.config_manager.create_config(
            "customer_service",
            confidence_threshold=0.7,
            customer_categories=["person"],
            staff_categories=["staff"],
            **areas
        )
        
        # Save to YAML file
        yaml_file = os.path.join(self.temp_dir, "test_config.yaml")
        self.config_manager.save_config_to_file(config, yaml_file, format="yaml")
        
        # Load from YAML file
        loaded_config = self.config_manager.load_config_from_file(yaml_file)
        
        self.assertIsInstance(loaded_config, CustomerServiceConfig)
        self.assertEqual(loaded_config.confidence_threshold, config.confidence_threshold)
        self.assertEqual(loaded_config.customer_categories, config.customer_categories)
    
    def test_config_import_export(self):
        """Test configuration import/export functionality."""
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        
        # Create multiple configs
        configs = {
            "config1": self.config_manager.create_config(
                "people_counting",
                confidence_threshold=0.6
            ),
            "config2": self.config_manager.create_config(
                "people_counting",
                confidence_threshold=0.8,
                enable_tracking=True
            )
        }
        
        # Export configs
        export_file = os.path.join(self.temp_dir, "exported_configs.json")
        self.config_manager.export_configs(configs, export_file)
        
        # Import configs
        imported_configs = self.config_manager.import_configs(export_file)
        
        self.assertEqual(len(imported_configs), 2)
        self.assertIn("config1", imported_configs)
        self.assertIn("config2", imported_configs)
        
        # Check imported config values
        self.assertEqual(imported_configs["config1"].confidence_threshold, 0.6)
        self.assertEqual(imported_configs["config2"].confidence_threshold, 0.8)
        self.assertTrue(imported_configs["config2"].enable_tracking)
    
    def test_config_schema_generation(self):
        """Test configuration schema generation."""
        self.config_manager.register_config("people_counting", PeopleCountingConfig)
        
        # Get schema
        schema = self.config_manager.get_config_schema("people_counting")
        
        self.assertIsInstance(schema, dict)
        self.assertIn("type", schema)
        self.assertIn("properties", schema)
        
        # Check for expected properties
        properties = schema["properties"]
        self.assertIn("confidence_threshold", properties)
        self.assertIn("enable_tracking", properties)
        self.assertIn("person_categories", properties)
    
    def test_config_defaults(self):
        """Test configuration default values."""
        self.config_manager.register_config("basic_counting_tracking", BasicCountingTrackingConfig)
        
        # Create config with defaults
        config = self.config_manager.create_config("basic_counting_tracking")
        
        # Should have default values
        self.assertIsNotNone(config.confidence_threshold)
        self.assertIsNotNone(config.category)
        self.assertIsNotNone(config.usecase)
        
        # Validate defaults
        is_valid, errors = self.config_manager.validate_config(config)
        self.assertTrue(is_valid, f"Default config should be valid: {errors}")


class TestConfigIntegration(BasePostProcessingTest):
    """Integration tests for configuration system."""
    
    def test_config_roundtrip_serialization(self):
        """Test complete serialization roundtrip."""
        areas = create_customer_service_areas()
        zones = create_zone_polygons(["entrance", "lobby"])
        
        original_config = CustomerServiceConfig(
            confidence_threshold=0.75,
            enable_tracking=True,
            customer_categories=["person", "customer"],
            staff_categories=["staff", "employee"],
            service_proximity_threshold=120.0,
            max_service_time=480.0,
            zones=zones,
            **areas
        )
        
        # JSON roundtrip
        json_str = original_config.to_json()
        json_restored = CustomerServiceConfig.from_json(json_str)
        
        self.assertEqual(json_restored.confidence_threshold, original_config.confidence_threshold)
        self.assertEqual(json_restored.customer_categories, original_config.customer_categories)
        self.assertEqual(json_restored.service_proximity_threshold, original_config.service_proximity_threshold)
        
        # Dict roundtrip
        config_dict = original_config.to_dict()
        dict_restored = CustomerServiceConfig.from_dict(config_dict)
        
        self.assertEqual(dict_restored.confidence_threshold, original_config.confidence_threshold)
        self.assertEqual(dict_restored.zones, original_config.zones)
    
    def test_config_parameter_override(self):
        """Test configuration parameter override behavior."""
        base_config = PeopleCountingConfig(
            confidence_threshold=0.5,
            enable_tracking=False,
            time_window_minutes=15
        )
        
        # Override with new parameters
        override_dict = {
            "confidence_threshold": 0.8,
            "enable_tracking": True,
            "enable_unique_counting": True  # New parameter
        }
        
        # Create new config with overrides
        overridden_config = PeopleCountingConfig(
            **{**base_config.to_dict(), **override_dict}
        )
        
        # Check overrides
        self.assertEqual(overridden_config.confidence_threshold, 0.8)
        self.assertTrue(overridden_config.enable_tracking)
        self.assertTrue(overridden_config.enable_unique_counting)
        
        # Check preserved values
        self.assertEqual(overridden_config.time_window_minutes, 15)
    
    def test_config_validation_edge_cases(self):
        """Test configuration validation with edge cases."""
        # Test with None values
        config_with_none = PeopleCountingConfig(
            confidence_threshold=None,  # Should use default
            person_categories=None      # Should use default
        )
        
        # Should handle None values gracefully
        errors = config_with_none.validate()
        # May have errors or use defaults - depends on implementation
        
        # Test with extreme values
        extreme_config = PeopleCountingConfig(
            confidence_threshold=0.0001,  # Very low but valid
            time_window_minutes=10080     # 1 week in minutes
        )
        
        errors = extreme_config.validate()
        self.assertEqual(len(errors), 0)  # Should be valid
    
    def test_multiple_config_types_integration(self):
        """Test integration of multiple configuration types."""
        manager = ConfigManager()
        
        # Register all config types
        manager.register_config("people_counting", PeopleCountingConfig)
        manager.register_config("customer_service", CustomerServiceConfig)
        manager.register_config("basic_counting_tracking", BasicCountingTrackingConfig)
        
        # Create configs of different types
        configs = {
            "people_config": manager.create_config(
                "people_counting",
                confidence_threshold=0.6,
                enable_tracking=True
            ),
            "service_config": manager.create_config(
                "customer_service",
                confidence_threshold=0.7,
                customer_categories=["person"],
                staff_categories=["staff"]
            ),
            "basic_config": manager.create_config(
                "basic_counting_tracking",
                confidence_threshold=0.5,
                enable_tracking=True
            )
        }
        
        # Validate all configs
        for name, config in configs.items():
            is_valid, errors = manager.validate_config(config)
            self.assertTrue(is_valid, f"Config {name} should be valid: {errors}")
        
        # Export all configs
        export_file = os.path.join(self.temp_dir, "multi_configs.json")
        manager.export_configs(configs, export_file)
        
        # Import and verify
        imported = manager.import_configs(export_file)
        self.assertEqual(len(imported), 3)
        
        # Check types are preserved
        self.assertIsInstance(imported["people_config"], PeopleCountingConfig)
        self.assertIsInstance(imported["service_config"], CustomerServiceConfig)
        self.assertIsInstance(imported["basic_config"], BasicCountingTrackingConfig)


if __name__ == "__main__":
    unittest.main() 