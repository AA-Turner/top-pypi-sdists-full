"""
Main post-processing processor with unified, clean API.

This module provides the main PostProcessor class that serves as the entry point
for all post-processing operations. It manages use cases, configurations, and
provides both simple and advanced processing interfaces.
"""

from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import logging
import time
from datetime import datetime, timezone
import hashlib
import json

from .core.base import (
    ProcessingResult, 
    ProcessingContext, 
    ProcessingStatus,
    registry
)
from .core.config import (
    BaseConfig, 
    PeopleCountingConfig, 
    CustomerServiceConfig,
    IntrusionConfig,
    ProximityConfig,
    config_manager,
    ConfigValidationError
)
from .usecases import (
    PeopleCountingUseCase,
    IntrusionUseCase,
    ProximityUseCase,
    CustomerServiceUseCase,
    AdvancedCustomerServiceUseCase,
    LicensePlateUseCase,
    ColorDetectionUseCase,
    PotholeSegmentationUseCase,
    PPEComplianceUseCase,
    VehicleMonitoringUseCase,
    ShopliftingDetectionUseCase,
    BananaMonitoringUseCase,
    FieldMappingUseCase,
    MaskDetectionUseCase,
    LeafUseCase,
    CarDamageDetectionUseCase,
    LeafDiseaseDetectionUseCase,
    FireSmokeUseCase,
    ShopliftingDetectionConfig,
    FlareAnalysisUseCase,
    WoundSegmentationUseCase,
    ParkingSpaceUseCase,
    ParkingUseCase,
    FaceEmotionUseCase,
    UnderwaterPlasticUseCase,
    PipelineDetectionUseCase,
    PedestrianDetectionUseCase,
    ChickenPoseDetectionUseCase,
    TheftDetectionUseCase,
    TrafficSignMonitoringUseCase,
    AntiSpoofingDetectionUseCase,
    ShelfInventoryUseCase,
    LaneDetectionUseCase,
    LitterDetectionUseCase,
    AbandonedObjectDetectionUseCase,

    LeakDetectionUseCase,
    HumanActivityUseCase,
    GasLeakDetectionUseCase,


    AgeDetectionUseCase,
    WeldDefectUseCase,
    WeaponDetectionUseCase,

    PriceTagUseCase,
    DistractedDriverUseCase,
    EmergencyVehicleUseCase,
    SolarPanelUseCase,
    CropWeedDetectionUseCase,
    ChildMonitoringUseCase,
    GenderDetectionUseCase,
    ConcreteCrackUseCase,
    FashionDetectionUseCase,
    WarehouseObjectUseCase,
    ShoppingCartUseCase,
    BottleDefectUseCase,
    AssemblyLineUseCase,
    CarPartSegmentationUseCase,
    WindmillMaintenanceUseCase,
    FlowerUseCase,
    SmokerDetectionUseCase,
    RoadTrafficUseCase,
    RoadViewSegmentationUseCase,
    FaceRecognitionUseCase,
    DrowsyDriverUseCase,
    WaterBodyUseCase,

    #Put all IMAGE based usecases here
    BloodCancerDetectionUseCase,
    SkinCancerClassificationUseCase,
    PlaqueSegmentationUseCase,
    CardiomegalyUseCase,
    HistopathologicalCancerDetectionUseCase,


)

logger = logging.getLogger(__name__)


class PostProcessor:
    """
    Unified post-processing interface with clean API and comprehensive functionality.
    
    This processor provides a simple yet powerful interface for processing model outputs
    with various use cases, centralized configuration management, and comprehensive
    error handling.
    
    Examples:
        # Simple usage
        processor = PostProcessor()
        result = processor.process_simple(
            raw_results, "people_counting", 
            confidence_threshold=0.6,
            zones={"entrance": [[0, 0], [100, 0], [100, 100], [0, 100]]}
        )
        
        # Configuration-based usage
        config = processor.create_config("people_counting", confidence_threshold=0.5)
        result = processor.process(raw_results, config)
        
        # File-based configuration
        result = processor.process_from_file(raw_results, "config.json")
    """
    
    def __init__(self):
        """Initialize the PostProcessor with registered use cases."""
        self._statistics = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_processing_time": 0.0
        }
        self.cache = {}
        self._use_case_cache = {}  # Cache for use case instances
        
        # Register available use cases
        self._register_use_cases()
    
    def _register_use_cases(self) -> None:
        """Register all available use cases."""
        # Register people counting use case
        registry.register_use_case("general", "people_counting", PeopleCountingUseCase)
        
        # Register intrusion detection use case
        registry.register_use_case("security", "intrusion_detection", IntrusionUseCase)
        
        # Register proximity detection use case
        registry.register_use_case("security", "proximity_detection", ProximityUseCase)
        
        # Register customer service use case
        registry.register_use_case("sales", "customer_service", CustomerServiceUseCase)
        
        # Register advanced customer service use case
        registry.register_use_case("sales", "advanced_customer_service", AdvancedCustomerServiceUseCase)
        
        # Register license plate detection use case
        registry.register_use_case("license_plate", "license_plate_detection", LicensePlateUseCase)
        
        # Register color detection use case
        registry.register_use_case("visual_appearance", "color_detection", ColorDetectionUseCase)
        
        # Register video_color_classification as alias for color_detection
        registry.register_use_case("visual_appearance", "video_color_classification", ColorDetectionUseCase)
        
        # Register PPE compliance use case
        registry.register_use_case("ppe", "ppe_compliance_detection", PPEComplianceUseCase)
        registry.register_use_case("infrastructure", "pothole_segmentation", PotholeSegmentationUseCase)
        registry.register_use_case("car_damage", "car_damage_detection", CarDamageDetectionUseCase)

        registry.register_use_case("traffic", "vehicle_monitoring", VehicleMonitoringUseCase)
        registry.register_use_case("traffic", "fruit_monitoring", BananaMonitoringUseCase)
        registry.register_use_case("security", "theft_detection", TheftDetectionUseCase)
        registry.register_use_case("traffic", "traffic_sign_monitoring", TrafficSignMonitoringUseCase)
        registry.register_use_case("security", "anti_spoofing_detection", AntiSpoofingDetectionUseCase)
        registry.register_use_case("retail", "shelf_inventory", ShelfInventoryUseCase)
        registry.register_use_case("traffic", "lane_detection", LaneDetectionUseCase)
        registry.register_use_case("security", "abandoned_object_detection", AbandonedObjectDetectionUseCase)
        registry.register_use_case("hazard", "fire_smoke_detection", FireSmokeUseCase)
        registry.register_use_case("flare_detection", "flare_analysis", FlareAnalysisUseCase)
        registry.register_use_case("general", "face_emotion", FaceEmotionUseCase)
        registry.register_use_case("parking_space", "parking_space_detection", ParkingSpaceUseCase)
        registry.register_use_case("environmental", "underwater_pollution_detection", UnderwaterPlasticUseCase)
        registry.register_use_case("pedestrian", "pedestrian_detection", PedestrianDetectionUseCase)  
        registry.register_use_case("general", "age_detection", AgeDetectionUseCase)
        registry.register_use_case("weld", "weld_defect_detection", WeldDefectUseCase)
        registry.register_use_case("price_tag", "price_tag_detection", PriceTagUseCase)
        registry.register_use_case("mask_detection", "mask_detection", MaskDetectionUseCase)
        registry.register_use_case("pipeline_detection", "pipeline_detection", PipelineDetectionUseCase)
        registry.register_use_case("automobile", "distracted_driver_detection", DistractedDriverUseCase)
        registry.register_use_case("traffic", "emergency_vehicle_detection", EmergencyVehicleUseCase)
        registry.register_use_case("energy", "solar_panel", SolarPanelUseCase)
        registry.register_use_case("agriculture", "chicken_pose_detection", ChickenPoseDetectionUseCase)
        registry.register_use_case("agriculture", "crop_weed_detection", CropWeedDetectionUseCase)
        registry.register_use_case("security", "child_monitoring", ChildMonitoringUseCase)
        registry.register_use_case("general", "gender_detection", GenderDetectionUseCase)
        registry.register_use_case("security", "weapon_detection", WeaponDetectionUseCase)
        registry.register_use_case("general", "concrete_crack_detection", ConcreteCrackUseCase)
        registry.register_use_case("retail", "fashion_detection", FashionDetectionUseCase)

        registry.register_use_case("retail", "warehouse_object_segmentation", WarehouseObjectUseCase)
        registry.register_use_case("retail", "shopping_cart_analysis", ShoppingCartUseCase)

        registry.register_use_case("security", "shoplifting_detection", ShopliftingDetectionUseCase)
        registry.register_use_case("retail", "defect_detection_products", BottleDefectUseCase)
        registry.register_use_case("manufacturing", "assembly_line_detection", AssemblyLineUseCase)
        registry.register_use_case("automobile", "car_part_segmentation", CarPartSegmentationUseCase)

        registry.register_use_case("manufacturing", "windmill_maintenance", WindmillMaintenanceUseCase)

        registry.register_use_case("infrastructure", "field_mapping", FieldMappingUseCase)
        registry.register_use_case("medical", "wound_segmentation", WoundSegmentationUseCase)
        registry.register_use_case("agriculture", "leaf_disease_detection", LeafDiseaseDetectionUseCase)
        registry.register_use_case("agriculture", "flower_segmentation", FlowerUseCase)
        registry.register_use_case("general", "parking_det", ParkingUseCase)
        registry.register_use_case("agriculture", "leaf_det", LeafUseCase)
        registry.register_use_case("general", "smoker_detection", SmokerDetectionUseCase)
        registry.register_use_case("automobile", "road_traffic_density", RoadTrafficUseCase)
        registry.register_use_case("automobile", "road_view_segmentation", RoadViewSegmentationUseCase)
        registry.register_use_case("security", "face_recognition", FaceRecognitionUseCase)
        registry.register_use_case("automobile", "drowsy_driver_detection", DrowsyDriverUseCase)
        registry.register_use_case("agriculture", "waterbody_segmentation", WaterBodyUseCase)
        registry.register_use_case("litter_detection", "litter_detection", LitterDetectionUseCase)
        registry.register_use_case("oil_gas", "leak_detection", LeakDetectionUseCase)
        registry.register_use_case("general", "human_activity_recognition", HumanActivityUseCase)
        registry.register_use_case("oil_gas", "gas_leak_detection", GasLeakDetectionUseCase)

        #Put all IMAGE based usecases here
        registry.register_use_case("healthcare", "bloodcancer_img_detection", BloodCancerDetectionUseCase)
        registry.register_use_case("healthcare", "skincancer_img_classification", SkinCancerClassificationUseCase)
        registry.register_use_case("healthcare", "plaque_img_segmentation", PlaqueSegmentationUseCase)
        registry.register_use_case("healthcare", "cardiomegaly_classification", CardiomegalyUseCase)
        registry.register_use_case("healthcare", "histopathological_cancer_detection", HistopathologicalCancerDetectionUseCase)
        

        logger.debug("Registered use cases with registry")
    
    def _generate_cache_key(self, config: BaseConfig, stream_key: Optional[str] = None) -> str:
        """
        Generate a cache key for use case instances based on config and stream key.
        
        Args:
            config: Configuration object
            stream_key: Optional stream key
            
        Returns:
            str: Cache key for the use case instance
        """
        # Create a deterministic hash based on config parameters and stream key
        config_dict = {
            'category': config.category,
            'usecase': config.usecase,
            'config_data': config.to_dict() if hasattr(config, 'to_dict') else str(config)
        }
        
        if stream_key:
            config_dict['stream_key'] = stream_key
        
        # Sort keys for consistent hashing
        config_str = json.dumps(config_dict, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()
    
    def _get_use_case_instance(self, config: BaseConfig, stream_key: Optional[str] = None):
        """
        Get or create a cached use case instance.
        
        Args:
            config: Configuration object
            stream_key: Optional stream key
            
        Returns:
            Use case instance
        """
        # Generate cache key
        cache_key = self._generate_cache_key(config, stream_key)
        
        # Check if we have a cached instance
        if cache_key in self._use_case_cache:
            logger.debug(f"Using cached use case instance for key: {cache_key}")
            return self._use_case_cache[cache_key]
        
        # Get appropriate use case class
        use_case_class = registry.get_use_case(config.category, config.usecase)
        if not use_case_class:
            raise ValueError(f"Use case '{config.category}/{config.usecase}' not found")
        
        # Instantiate use case
        use_case = use_case_class()
        
        # Cache the instance
        self._use_case_cache[cache_key] = use_case
        logger.debug(f"Cached new use case instance for key: {cache_key}")
        
        return use_case
    
    def process(self, data: Any, config: Union[BaseConfig, Dict[str, Any], str, Path], input_bytes: Optional[bytes] = None,
                context: Optional[ProcessingContext] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process data using the specified configuration.
        
        Args:
            data: Raw model output (detection, tracking, classification results)
            config: Configuration object, dict, or path to config file
            input_bytes: Optional input bytes for certain use cases
            context: Optional processing context
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference (optional)
        Returns:
            ProcessingResult: Standardized result object
        """
        start_time = time.time()
        
        try:
            # Parse configuration
            parsed_config = self._parse_config(config)
            
            # Get cached use case instance
            use_case = self._get_use_case_instance(parsed_config, stream_key)
            
            # Create context if not provided
            if context is None:
                context = ProcessingContext()
            
            # Process with use case
            if isinstance(use_case, ColorDetectionUseCase):
                result = use_case.process(data, parsed_config, input_bytes, context, stream_info)
            elif isinstance(use_case, VehicleMonitoringUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, BananaMonitoringUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ChickenPoseDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, FlareAnalysisUseCase):
                result = use_case.process(data, parsed_config, input_bytes, context, stream_info)
            elif isinstance(use_case, LicensePlateUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, CropWeedDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, EmergencyVehicleUseCase): 
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, PriceTagUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, AgeDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, GenderDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, FashionDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ShopliftingDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, PotholeSegmentationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, AssemblyLineUseCase): 
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, AntiSpoofingDetectionUseCase): 
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ShelfInventoryUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, CarPartSegmentationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ConcreteCrackUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, LaneDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, AbandonedObjectDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, WindmillMaintenanceUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)

            elif isinstance(use_case, FieldMappingUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, WoundSegmentationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, LeafDiseaseDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, FlowerUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ParkingUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, LeafUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, SmokerDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, BottleDefectUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, ParkingSpaceUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, RoadTrafficUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, RoadViewSegmentationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, FaceRecognitionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, DrowsyDriverUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, WaterBodyUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, LitterDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, LeakDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, HumanActivityUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, GasLeakDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            
            #Put all IMAGE based usecases here
            elif isinstance(use_case, BloodCancerDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, SkinCancerClassificationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, PlaqueSegmentationUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, CardiomegalyUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)
            elif isinstance(use_case, HistopathologicalCancerDetectionUseCase):
                result = use_case.process(data, parsed_config, context, stream_info)

            else:
                result = use_case.process(data, parsed_config, context, stream_info)

            
            # Add processing time
            result.processing_time = time.time() - start_time
            
            # Update statistics
            self._update_statistics(result)
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Processing failed: {str(e)}", exc_info=True)
            
            error_result = self._create_error_result(
                str(e),
                type(e).__name__,
                context=context
            )
            error_result.processing_time = processing_time
            
            # Update statistics
            self._update_statistics(error_result)
            
            return error_result
    
    def process_simple(self, data: Any, usecase: str, 
                      category: Optional[str] = None,
                      context: Optional[ProcessingContext] = None,
                      stream_key: Optional[str] = None,
                      stream_info: Optional[Dict[str, Any]] = None,
                      **config_params) -> ProcessingResult:
        """
        Simple processing interface for quick use cases.
        
        Args:
            data: Raw model output
            usecase: Use case name ('people_counting', 'customer_service', etc.)
            category: Use case category (auto-detected if not provided)
            context: Optional processing context
            stream_key: Optional stream key for caching
            stream_info: Stream info for the inference (optional)
            **config_params: Configuration parameters
            
        Returns:
            ProcessingResult: Standardized result object
        """
        try:
            # Auto-detect category if not provided
            if category is None:
                if usecase == "people_counting":
                    category = "general"
                elif usecase == "customer_service":
                    category = "sales"
                elif usecase in ["color_detection", "video_color_classification"]:
                    category = "visual_appearance"
                else:
                    category = "general"  # Default fallback
            
            # Create configuration
            config = self.create_config(usecase, category=category, **config_params)
            return self.process(data, config, context=context, stream_key=stream_key, stream_info=stream_info)
            
        except Exception as e:
            logger.error(f"Simple processing failed: {str(e)}", exc_info=True)
            return self._create_error_result(
                str(e),
                type(e).__name__,
                usecase,
                category or "general",
                context
            )
    
    def process_from_file(self, data: Any, config_file: Union[str, Path],
                         context: Optional[ProcessingContext] = None,
                         stream_key: Optional[str] = None,
                         stream_info: Optional[Dict[str, Any]] = None) -> ProcessingResult:
        """
        Process data using configuration from file.
        
        Args:
            data: Raw model output
            config_file: Path to configuration file (JSON or YAML)
            context: Optional processing context
            stream_key: Optional stream key for caching
            stream_info: Stream info for the inference (optional)
        Returns:
            ProcessingResult: Standardized result object
        """
        try:
            config = config_manager.load_from_file(config_file)
            return self.process(data, config, context=context, stream_key=stream_key, stream_info=stream_info)
            
        except Exception as e:
            logger.error(f"File-based processing failed: {str(e)}", exc_info=True)
            return self._create_error_result(
                f"Failed to process with config file: {str(e)}",
                type(e).__name__,
                context=context
            )
    
    def create_config(self, usecase: str, category: str = "general", **kwargs) -> BaseConfig:
        """
        Create a validated configuration object.
        
        Args:
            usecase: Use case name
            category: Use case category
            **kwargs: Configuration parameters
            
        Returns:
            BaseConfig: Validated configuration object
        """
        return config_manager.create_config(usecase, category=category, **kwargs)
    
    def load_config(self, file_path: Union[str, Path]) -> BaseConfig:
        """Load configuration from file."""
        return config_manager.load_from_file(file_path)
    
    def save_config(self, config: BaseConfig, file_path: Union[str, Path], 
                   format: str = "json") -> None:
        """Save configuration to file."""
        config_manager.save_to_file(config, file_path, format)
    
    def get_config_template(self, usecase: str) -> Dict[str, Any]:
        """Get configuration template for a use case."""
        return config_manager.get_config_template(usecase)
    
    def list_available_usecases(self) -> Dict[str, List[str]]:
        """List all available use cases by category."""
        return registry.list_use_cases()
    
    def get_supported_usecases(self) -> List[str]:
        """Get list of supported use case names."""
        return config_manager.list_supported_usecases()
    
    def get_use_case_schema(self, usecase: str, category: str = "general") -> Dict[str, Any]:
        """
        Get JSON schema for a use case configuration.
        
        Args:
            usecase: Use case name
            category: Use case category
            
        Returns:
            Dict[str, Any]: JSON schema for the use case
        """
        use_case_class = registry.get_use_case(category, usecase)
        if not use_case_class:
            raise ValueError(f"Use case '{category}/{usecase}' not found")
        
        use_case = use_case_class()
        return use_case.get_config_schema()
    
    def validate_config(self, config: Union[BaseConfig, Dict[str, Any]]) -> List[str]:
        """
        Validate a configuration object or dictionary.
        
        Args:
            config: Configuration to validate
            
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        try:
            if isinstance(config, dict):
                usecase = config.get('usecase')
                if not usecase:
                    return ["Configuration must specify 'usecase'"]
                
                category = config.get('category', 'general')
                parsed_config = config_manager.create_config(usecase, category=category, **config)
                return parsed_config.validate()
            elif isinstance(config, BaseConfig):
                return config.validate()
            else:
                return [f"Invalid configuration type: {type(config)}"]
                
        except Exception as e:
            return [f"Configuration validation failed: {str(e)}"]
    
    def clear_use_case_cache(self) -> None:
        """Clear the use case instance cache."""
        self._use_case_cache.clear()
        logger.debug("Cleared use case instance cache")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the use case cache.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        return {
            "cached_instances": len(self._use_case_cache),
            "cache_keys": list(self._use_case_cache.keys())
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dict[str, Any]: Processing statistics
        """
        stats = self._statistics.copy()
        if stats["total_processed"] > 0:
            stats["success_rate"] = stats["successful"] / stats["total_processed"]
            stats["failure_rate"] = stats["failed"] / stats["total_processed"]
            stats["average_processing_time"] = stats["total_processing_time"] / stats["total_processed"]
        else:
            stats["success_rate"] = 0.0
            stats["failure_rate"] = 0.0
            stats["average_processing_time"] = 0.0
        
        # Add cache statistics
        stats["cache_stats"] = self.get_cache_stats()
        
        return stats
    
    def reset_statistics(self) -> None:
        """Reset processing statistics."""
        self._statistics = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_processing_time": 0.0
        }
    
    def _parse_config(self, config: Union[BaseConfig, Dict[str, Any], str, Path]) -> BaseConfig:
        """Parse configuration from various input formats."""
        if isinstance(config, BaseConfig):
            return config
        elif isinstance(config, dict):
            usecase = config.get('usecase')
            if not usecase:
                raise ValueError("Configuration dict must contain 'usecase' key")
            
            category = config.get('category', 'general')
            return config_manager.create_config(usecase, category=category, **config)
        elif isinstance(config, (str, Path)):
            return config_manager.load_from_file(config)
        else:
            raise ValueError(f"Unsupported config type: {type(config)}")
    
    def _create_error_result(self, message: str, error_type: str = "ProcessingError",
                            usecase: str = "", category: str = "",
                            context: Optional[ProcessingContext] = None) -> ProcessingResult:
        """Create an error result with structured events."""
        # Create structured error event
        error_event = {
            "type": "processing_error",
            "stream_time": datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S UTC"),
            "level": "critical",
            "intensity": 5,
            "config": {
                "min_value": 0, 
                "max_value": 10, 
                "level_settings": {"info": 2, "warning": 5, "critical": 7}
            },
            "application_name": f"{usecase.title()} Processing" if usecase else "Post Processing",
            "application_version": "1.0",
            "location_info": None,
            "human_text": f"Event: Processing Error\nLevel: Critical\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\nError: {message}"
        }
        
        result = ProcessingResult(
            data={
                "events": [error_event],
                "tracking_stats": [],
                "error_details": {"message": message, "type": error_type}
            },
            status=ProcessingStatus.ERROR,
            usecase=usecase,
            category=category,
            context=context,
            error_message=message,
            error_type=error_type,
            summary=f"Processing failed: {message}"
        )
        
        if context:
            result.processing_time = context.processing_time or 0.0
        
        return result
    
    def _update_statistics(self, result: ProcessingResult) -> None:
        """Update processing statistics."""
        self._statistics["total_processed"] += 1
        self._statistics["total_processing_time"] += result.processing_time
        
        if result.is_success():
            self._statistics["successful"] += 1
        else:
            self._statistics["failed"] += 1


# Convenience functions for backward compatibility and simple usage
def process_simple(data: Any, usecase: str, category: Optional[str] = None, **config) -> ProcessingResult:
    """
    Simple processing function for quick use cases.
    
    Args:
        data: Raw model output
        usecase: Use case name ('people_counting', 'customer_service', etc.)
        category: Use case category (auto-detected if not provided)
        **config: Configuration parameters
        
    Returns:
        ProcessingResult: Standardized result object
    """
    processor = PostProcessor()
    return processor.process_simple(data, usecase, category, **config)


def create_config_template(usecase: str) -> Dict[str, Any]:
    """
    Create a configuration template for a use case.
    
    Args:
        usecase: Use case name
        
    Returns:
        Dict[str, Any]: Configuration template
    """
    processor = PostProcessor()
    return processor.get_config_template(usecase)


def list_available_usecases() -> Dict[str, List[str]]:
    """
    List all available use cases.
    
    Returns:
        Dict[str, List[str]]: Available use cases by category
    """
    processor = PostProcessor()
    return processor.list_available_usecases()


def validate_config(config: Union[BaseConfig, Dict[str, Any]]) -> List[str]:
    """
    Validate a configuration.
    
    Args:
        config: Configuration to validate
        
    Returns:
        List[str]: List of validation errors
    """
    processor = PostProcessor()
    return processor.validate_config(config)