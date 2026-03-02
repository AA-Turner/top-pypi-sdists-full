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

from .core.base import ProcessingResult, ProcessingContext, ProcessingStatus, registry
from .core.config import (
    BaseConfig,
    PeopleCountingConfig,
    CustomerServiceConfig,
    IntrusionConfig,
    ProximityConfig,
    config_manager,
    ConfigValidationError,
    PeopleTrackingConfig,
)
from .usecases import (
    PeopleCountingUseCase,
    DroneTrafficMonitoringUsecase,
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
    # FaceRecognitionUseCase,
    DrowsyDriverUseCase,
    WaterBodyUseCase,
    LicensePlateMonitorUseCase,
    DwellUseCase,
    AgeGenderUseCase,
    PeopleTrackingUseCase,
    WildLifeMonitoringUseCase,
    PCBDefectUseCase,
    UndergroundPipelineDefectUseCase,
    SusActivityUseCase,
    NaturalDisasterUseCase,
    FootFallUseCase,
    CrowdflowUseCase,
    VehicleMonitoringParkingLotUseCase,
    VehicleMonitoringDroneViewUseCase,
    ParkingLotAnalyticsUseCase,
    VehicleMonitoringWrongWayUseCase,
    StoppedVehicleMonitoringUseCase,
    AreaUtilizationUseCase,
    HeatMapsUseCase,
    CrowdDensityHeatMapsUseCase,
    LoiteringUseCase,
    HazardZoneEntryUseCase,
    TailgatingDetectionUseCase,
    VehicleColorDetectionUseCase,
    FallDetectionUseCase,
    RunningDetectionUseCase,
    LiquidLeakDetectionUseCase,
    PipeGasLeakDetectionUseCase,
    PeopleCountingInZoneUseCase,
    PipeCorrosionDetectionUseCase,
    OvercrowdingDetectionUseCase,
    AnimalDetectionUseCase,
    BurglaryDetectionUseCase,
    # Put all IMAGE based usecases here
    BloodCancerDetectionUseCase,
    SkinCancerClassificationUseCase,
    PlaqueSegmentationUseCase,
    CardiomegalyUseCase,
    HistopathologicalCancerDetectionUseCase,
    CellMicroscopyUseCase,
)

# Face recognition with embeddings (from face_reg module)
from .face_reg.face_recognition import FaceRecognitionEmbeddingUseCase

from .core.config_utils import create_config_from_template
from .core.config import BaseConfig, AlertConfig, ZoneConfig, TrackingConfig
from .config import (
    get_usecase_from_app_name,
    get_category_from_app_name,
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

    def __init__(
        self,
        post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
        app_name: Optional[str] = None,
        index_to_category: Optional[Dict[int, str]] = None,
        target_categories: Optional[List[str]] = None,
    ):
        """Initialize the PostProcessor with registered use cases."""
        self._statistics = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_processing_time": 0.0,
        }
        self.cache = {}
        self._use_case_cache = {}  # Cache for use case instances

        # Register available use cases
        self._register_use_cases()

        # Set up default post-processing configuration
        self.post_processing_config = None
        self.app_name = app_name
        self.index_to_category = index_to_category
        self.target_categories = target_categories
        if post_processing_config or self.app_name:
            logging.debug(f"Parsing post-processing config: {post_processing_config}")
            self.post_processing_config = self._parse_post_processing_config(
                post_processing_config, self.app_name
            )
            if self.post_processing_config:
                logging.info(
                    f"Successfully parsed post-processing config for usecase: {self.post_processing_config.usecase}"
                )
            else:
                logging.warning("Failed to parse post-processing config")
        else:
            logging.info("No post-processing config provided")

    def _load_config_from_app_name(self, app_name: str) -> Optional[BaseConfig]:
        """Load default post-processing configuration based on app name."""
        usecase = get_usecase_from_app_name(app_name)
        category = get_category_from_app_name(app_name)
        if not usecase or not category:
            logging.warning(f"No usecase or category found for app: {app_name}")
            return None
        config = self.create_config(usecase, category)
        return config

    def _parse_post_processing_config(
        self,
        config: Union[Dict[str, Any], BaseConfig, str],
        app_name: Optional[str] = None,
    ) -> Optional[BaseConfig]:
        """Parse post-processing configuration from various formats."""
        try:
            if not config and not app_name:
                return None
            
            # Handle app-name based configuration first
            if app_name:
                app_config = self._load_config_from_app_name(app_name)
                if app_config and config and isinstance(config, dict):
                    return self._merge_config_into_app_config(app_config, config)
                elif app_config:
                    return app_config
                else:
                    logging.warning(f"No config found for app: {app_name}")
            
            # Handle different config input types
            parsed_config = self._parse_config_by_type(config)
            if parsed_config:
                self._apply_instance_config_overrides(parsed_config)
                
            return parsed_config
            
        except Exception as e:
            logging.error(f"Failed to parse post-processing config: {str(e)}")
            return None

    def _merge_config_into_app_config(
        self, app_config: BaseConfig, config_dict: Dict[str, Any]
    ) -> BaseConfig:
        """Merge provided configuration dictionary into app-based config."""
        logging.debug(f"Merging provided config into app config")
        logging.debug(f"Provided config keys: {list(config_dict.keys())}")
        
        for key, value in config_dict.items():
            if value is None:
                continue
                
            if hasattr(app_config, key):
                self._apply_config_value(app_config, key, value)
            else:
                logging.warning(f"Config key '{key}' not found in app config, skipping")
        
        logging.debug(f"Final app config zone_config: {getattr(app_config, 'zone_config', None)}")
        return app_config

    def _apply_config_value(self, config: BaseConfig, key: str, value: Any) -> None:
        """Apply a configuration value to a config object, handling nested dicts."""
        if isinstance(value, dict):
            current_value = getattr(config, key)
            try:
                # Try to convert known config dicts to dataclasses
                if key == "alert_config":
                    setattr(config, key, AlertConfig(**value))
                elif key == "zone_config":
                    setattr(config, key, ZoneConfig(**value))
                elif key == "tracking_config":
                    setattr(config, key, TrackingConfig(**value))
                elif isinstance(current_value, dict):
                    # Merge dictionaries
                    merged_dict = {**(current_value or {}), **value}
                    setattr(config, key, merged_dict)
                    logging.debug(f"Merged nested dict for {key}: {merged_dict}")
                else:
                    setattr(config, key, value)
            except Exception:
                # Fallback to direct assignment
                setattr(config, key, value)
                logging.debug(f"Applied config parameter {key}={value} (fallback)")
        else:
            setattr(config, key, value)
            logging.debug(f"Applied config parameter {key}={value}")

    def _parse_config_by_type(
        self, config: Union[Dict[str, Any], BaseConfig, str]
    ) -> Optional[BaseConfig]:
        """Parse configuration based on its input type."""
        if isinstance(config, BaseConfig):
            return config
        elif isinstance(config, dict):
            return self._parse_config_dict(config)
        elif isinstance(config, str):
            return create_config_from_template(config)
        else:
            logging.warning(f"Unsupported config type: {type(config)}")
            return None

    def _parse_config_dict(self, config: Dict[str, Any]) -> Optional[BaseConfig]:
        """Parse configuration from a dictionary."""
        usecase = config.get("usecase")
        if not usecase:
            raise ValueError("Configuration dict must contain 'usecase' key")
        
        # Prepare config parameters
        config_params = config.copy()
        config_params.pop("usecase", None)
        config_params.pop("category", None)
        category = config.get("category", "general")
        
        # Clean up use-case specific parameters
        self._clean_use_case_specific_params(usecase, config_params)
        
        # Normalize nested config objects
        self._normalize_nested_configs(config_params)
        
        # Create config using the factory
        return self.create_config(usecase, category, **config_params)

    def _clean_use_case_specific_params(
        self, usecase: str, config_params: Dict[str, Any]
    ) -> None:
        """Remove parameters that aren't needed for specific use cases."""
        facial_recognition_usecases = {"face_recognition"}
        license_plate_monitoring_usecases = {"license_plate_monitor"}
        
        if usecase not in facial_recognition_usecases:
            if "facial_recognition_server_id" in config_params:
                logging.debug(
                    f"Removing facial_recognition_server_id from {usecase} config"
                )
                config_params.pop("facial_recognition_server_id", None)
                config_params.pop("deployment_id", None)
        
        if usecase not in license_plate_monitoring_usecases:
            if "lpr_server_id" in config_params:
                logging.debug(f"Removing lpr_server_id from {usecase} config")
                config_params.pop("lpr_server_id", None)
        
        # Keep session and lpr_server_id only for use cases that need them
        if usecase not in facial_recognition_usecases and usecase not in license_plate_monitoring_usecases:
            if "session" in config_params:
                logging.debug(f"Removing session from {usecase} config")
                config_params.pop("session", None)

    def _normalize_nested_configs(self, config_params: Dict[str, Any]) -> None:
        """Convert nested config dictionaries to dataclass instances."""
        config_mappings = {
            "alert_config": AlertConfig,
            "zone_config": ZoneConfig,
            "tracking_config": TrackingConfig,
        }
        
        for key, config_class in config_mappings.items():
            if isinstance(config_params.get(key), dict):
                try:
                    config_params[key] = config_class(**config_params[key])
                except Exception:
                    # Leave as dict; downstream create_config will handle it
                    pass

    def _apply_instance_config_overrides(self, config: BaseConfig) -> None:
        """Apply instance-level configuration overrides."""
        if hasattr(config, "index_to_category"):
            if not config.index_to_category:
                config.index_to_category = self.index_to_category or {}
            else:
                self.index_to_category = config.index_to_category
                
        if hasattr(config, "target_categories"):
            if not config.target_categories:
                config.target_categories = self.target_categories
            else:
                self.target_categories = config.target_categories

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
        registry.register_use_case(
            "sales", "advanced_customer_service", AdvancedCustomerServiceUseCase
        )

        # Register license plate detection use case
        registry.register_use_case(
            "license_plate", "license_plate_detection", LicensePlateUseCase
        )

        # Register color detection use case
        registry.register_use_case(
            "visual_appearance", "color_detection", ColorDetectionUseCase
        )

        # Register video_color_classification as alias for color_detection
        registry.register_use_case(
            "visual_appearance", "video_color_classification", ColorDetectionUseCase
        )

        # Register PPE compliance use case
        registry.register_use_case(
            "ppe", "ppe_compliance_detection", PPEComplianceUseCase
        )
        registry.register_use_case(
            "infrastructure", "pothole_segmentation", PotholeSegmentationUseCase
        )
        registry.register_use_case(
            "car_damage", "car_damage_detection", CarDamageDetectionUseCase
        )

        registry.register_use_case(
            "traffic", "vehicle_monitoring", VehicleMonitoringUseCase
        )
        registry.register_use_case(
            "traffic", "fruit_monitoring", BananaMonitoringUseCase
        )
        registry.register_use_case("security", "theft_detection", TheftDetectionUseCase)
        registry.register_use_case(
            "traffic", "traffic_sign_monitoring", TrafficSignMonitoringUseCase
        )
        registry.register_use_case(
            "traffic", "drone_traffic_monitoring", DroneTrafficMonitoringUsecase
        )
        registry.register_use_case(
            "security", "anti_spoofing_detection", AntiSpoofingDetectionUseCase
        )
        registry.register_use_case("retail", "shelf_inventory", ShelfInventoryUseCase)
        registry.register_use_case("traffic", "lane_detection", LaneDetectionUseCase)
        registry.register_use_case(
            "security", "abandoned_object_detection", AbandonedObjectDetectionUseCase
        )
        registry.register_use_case("hazard", "fire_smoke_detection", FireSmokeUseCase)
        registry.register_use_case(
            "flare_detection", "flare_analysis", FlareAnalysisUseCase
        )
        registry.register_use_case("general", "face_emotion", FaceEmotionUseCase)
        registry.register_use_case(
            "parking_space", "parking_space_detection", ParkingSpaceUseCase
        )
        registry.register_use_case(
            "environmental", "underwater_pollution_detection", UnderwaterPlasticUseCase
        )
        registry.register_use_case(
            "pedestrian", "pedestrian_detection", PedestrianDetectionUseCase
        )
        registry.register_use_case("general", "age_detection", AgeDetectionUseCase)
        registry.register_use_case("weld", "weld_defect_detection", WeldDefectUseCase)
        registry.register_use_case("price_tag", "price_tag_detection", PriceTagUseCase)
        registry.register_use_case(
            "mask_detection", "mask_detection", MaskDetectionUseCase
        )
        registry.register_use_case(
            "pipeline_detection", "pipeline_detection", PipelineDetectionUseCase
        )
        registry.register_use_case(
            "automobile", "distracted_driver_detection", DistractedDriverUseCase
        )
        registry.register_use_case(
            "traffic", "emergency_vehicle_detection", EmergencyVehicleUseCase
        )
        registry.register_use_case("energy", "solar_panel", SolarPanelUseCase)
        registry.register_use_case(
            "agriculture", "chicken_pose_detection", ChickenPoseDetectionUseCase
        )
        registry.register_use_case(
            "agriculture", "crop_weed_detection", CropWeedDetectionUseCase
        )
        registry.register_use_case(
            "security", "child_monitoring", ChildMonitoringUseCase
        )
        registry.register_use_case(
            "general", "gender_detection", GenderDetectionUseCase
        )
        registry.register_use_case(
            "security", "weapon_detection", WeaponDetectionUseCase
        )
        registry.register_use_case(
            "general", "concrete_crack_detection", ConcreteCrackUseCase
        )
        registry.register_use_case(
            "retail", "fashion_detection", FashionDetectionUseCase
        )

        registry.register_use_case(
            "retail", "warehouse_object_segmentation", WarehouseObjectUseCase
        )
        registry.register_use_case(
            "retail", "shopping_cart_analysis", ShoppingCartUseCase
        )

        registry.register_use_case(
            "security", "shoplifting_detection", ShopliftingDetectionUseCase
        )
        registry.register_use_case(
            "retail", "defect_detection_products", BottleDefectUseCase
        )
        registry.register_use_case(
            "manufacturing", "assembly_line_detection", AssemblyLineUseCase
        )
        registry.register_use_case(
            "automobile", "car_part_segmentation", CarPartSegmentationUseCase
        )

        registry.register_use_case(
            "manufacturing", "windmill_maintenance", WindmillMaintenanceUseCase
        )

        registry.register_use_case(
            "infrastructure", "field_mapping", FieldMappingUseCase
        )
        registry.register_use_case(
            "medical", "wound_segmentation", WoundSegmentationUseCase
        )
        registry.register_use_case(
            "agriculture", "leaf_disease_detection", LeafDiseaseDetectionUseCase
        )
        registry.register_use_case("agriculture", "flower_segmentation", FlowerUseCase)
        registry.register_use_case("general", "parking_det", ParkingUseCase)
        registry.register_use_case("agriculture", "leaf_det", LeafUseCase)
        registry.register_use_case(
            "general", "smoker_detection", SmokerDetectionUseCase
        )
        registry.register_use_case(
            "automobile", "road_traffic_density", RoadTrafficUseCase
        )
        registry.register_use_case(
            "automobile", "road_view_segmentation", RoadViewSegmentationUseCase
        )
        # registry.register_use_case("security", "face_recognition", FaceRecognitionUseCase)
        registry.register_use_case(
            "security", "face_recognition", FaceRecognitionEmbeddingUseCase
        )
        registry.register_use_case(
            "automobile", "drowsy_driver_detection", DrowsyDriverUseCase
        )
        registry.register_use_case(
            "agriculture", "waterbody_segmentation", WaterBodyUseCase
        )
        registry.register_use_case(
            "litter_detection", "litter_detection", LitterDetectionUseCase
        )
        registry.register_use_case("oil_gas", "leak_detection", LeakDetectionUseCase)
        registry.register_use_case(
            "general", "human_activity_recognition", HumanActivityUseCase
        )
        registry.register_use_case(
            "oil_gas", "gas_leak_detection", GasLeakDetectionUseCase
        )
        registry.register_use_case(
            "license_plate_monitor", "license_plate_monitor", LicensePlateMonitorUseCase
        )
        registry.register_use_case("general", "dwell", DwellUseCase)
        registry.register_use_case(
            "age_gender_detection", "age_gender_detection", AgeGenderUseCase
        )
        registry.register_use_case("general", "people_tracking", PeopleTrackingUseCase)
        registry.register_use_case(
            "environmental", "wildlife_monitoring", WildLifeMonitoringUseCase
        )
        registry.register_use_case(
            "manufacturing", "pcb_defect_detection", PCBDefectUseCase
        )
        registry.register_use_case(
            "general", "underground_pipeline_defect", UndergroundPipelineDefectUseCase
        )
        registry.register_use_case(
            "security", "suspicious_activity_detection", SusActivityUseCase
        )
        registry.register_use_case(
            "environmental", "natural_disaster_detection", NaturalDisasterUseCase
        )
        registry.register_use_case(
            "retail", "footfall", FootFallUseCase
        )
        registry.register_use_case(
            "traffic", "vehicle_monitoring_parking_lot", VehicleMonitoringParkingLotUseCase
        )
        registry.register_use_case(
            "traffic", "vehicle_monitoring_drone_view", VehicleMonitoringDroneViewUseCase
        )
        registry.register_use_case(
            "traffic", "parking_lot_analytics", ParkingLotAnalyticsUseCase 
        )
        registry.register_use_case(
            "retail", "crowdflow", CrowdflowUseCase
        )
        registry.register_use_case(
            "retail", "heatmaps", HeatMapsUseCase
        )
        registry.register_use_case(
            "retail", "crowd_density_heatmaps", CrowdDensityHeatMapsUseCase
        )
        registry.register_use_case(
            "general", "hazard_zone_entry", HazardZoneEntryUseCase
        )
        registry.register_use_case(
            "traffic", "vehicle_monitoring_wrong_way", VehicleMonitoringWrongWayUseCase
        )
        registry.register_use_case(
            "traffic", "stopped_vehicle_monitoring", StoppedVehicleMonitoringUseCase
        )
        registry.register_use_case(
            "general", "area_utilization", AreaUtilizationUseCase
        )
        registry.register_use_case(
            "general", "loitering_detection", LoiteringUseCase
        )
        registry.register_use_case(
            "security", "tailgating_detection", TailgatingDetectionUseCase
        )
        registry.register_use_case(
            "traffic", "vehicle_color_detection", VehicleColorDetectionUseCase
        )
        registry.register_use_case(
            "general", "fall_detection", FallDetectionUseCase
        )
        registry.register_use_case(
            "security", "running_detection", RunningDetectionUseCase
        )
        registry.register_use_case(
            "security", "liquid_leak_detection", LiquidLeakDetectionUseCase
        )
        registry.register_use_case(
            "security", "pipe_gas_leak_detection", PipeGasLeakDetectionUseCase
        )
        registry.register_use_case(
            "general", "people_counting_in_zone", PeopleCountingInZoneUseCase
        )
        registry.register_use_case(
            "security", "pipe_corrosion_detection", PipeCorrosionDetectionUseCase
        )
        registry.register_use_case(
            "security", "overcrowding_detection", OvercrowdingDetectionUseCase
        )
        registry.register_use_case(
            "general", "animal_detection", AnimalDetectionUseCase
        )
        registry.register_use_case(
            "security", "burglary_detection", BurglaryDetectionUseCase
        )

        # Put all IMAGE based usecases here
        registry.register_use_case(
            "healthcare", "bloodcancer_img_detection", BloodCancerDetectionUseCase
        )
        registry.register_use_case(
            "healthcare",
            "skincancer_img_classification",
            SkinCancerClassificationUseCase,
        )
        registry.register_use_case(
            "healthcare", "plaque_img_segmentation", PlaqueSegmentationUseCase
        )
        registry.register_use_case(
            "healthcare", "cardiomegaly_classification", CardiomegalyUseCase
        )
        registry.register_use_case(
            "healthcare",
            "histopathological_cancer_detection",
            HistopathologicalCancerDetectionUseCase,
        )
        registry.register_use_case(
            "healthcare", "cell_microscopy_segmentation", CellMicroscopyUseCase
        )

        logger.debug("Registered use cases with registry")

    def _generate_cache_key(self, config: BaseConfig, stream_key: Optional[str] = None) -> str:
        """
        Generate a cache key for use case instances based on config and stream key.

        IMPORTANT: For tracking use cases (people_counting, people_tracking, etc.), the cache key
        should be STABLE to prevent tracker state reset. Only include:
        - category
        - usecase
        - stream_key (which should be camera_id)

        DO NOT include volatile config parameters (confidence_threshold, zones, etc.) as
        changes would cause cache miss → new use case instance → tracker reset → all tracks appear "new"

        Args:
            config: Configuration object
            stream_key: Optional stream key (should be camera_id for tracking use cases)

        Returns:
            str: Cache key for the use case instance
        """
        # Create a STABLE cache key - only use category, usecase, and stream_key
        # This ensures tracking state is preserved even if config parameters change
        cache_data = {
            'category': getattr(config, 'category', 'general'),
            'usecase': getattr(config, 'usecase', 'unknown'),
            'stream_key': stream_key or 'default',
        }

        # NOTE: We intentionally DO NOT include config parameters like:
        # - confidence_threshold
        # - zones
        # - tracking_config
        # - alert_config
        #
        # Including these would cause cache misses when config changes,
        # which resets tracker state and causes track ID inflation.
        # Config changes should apply to the existing instance, not create a new one.

        # Sort keys for consistent hashing
        config_str = json.dumps(cache_data, sort_keys=True, default=str)
        return hashlib.md5(config_str.encode()).hexdigest()[:16]

    async def _get_use_case_instance(
        self, config: BaseConfig, stream_key: Optional[str] = None
    ):
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

        # CACHE MISS - Log warning for tracking use cases as this resets tracker state
        tracking_usecases = {'people_counting', 'people_tracking', 'footfall', 'crowdflow', 'dwell',
                             'vehicle_monitoring', 'vehicle_tracking', 'vehicle_counting'}
        usecase_name = getattr(config, 'usecase', 'unknown')
        if usecase_name in tracking_usecases:
            logger.warning(
                f"[CACHE_MISS] Creating new use case instance for tracking usecase. "
                f"cache_key={cache_key}, stream_key={stream_key}, usecase={usecase_name}. "
                f"This will RESET all tracking state including accumulated track IDs!"
            )

        # Get appropriate use case class
        use_case_class = registry.get_use_case(config.category, config.usecase)
        if not use_case_class:
            raise ValueError(f"Use case '{config.category}/{config.usecase}' not found")


        if use_case_class == FaceRecognitionEmbeddingUseCase:
            use_case = use_case_class(config=config)
            # Await async initialization for face recognition use case
            await use_case.initialize(config)
        else:
            use_case = use_case_class()
        logger.info(f"Created use case instance for: {config.category}/{config.usecase}")


        # Cache the instance
        self._use_case_cache[cache_key] = use_case
        logger.debug(f"Cached new use case instance for key: {cache_key}")

        return use_case

    async def _dispatch_use_case_processing(
        self,
        use_case,
        data: Any,
        config: BaseConfig,
        input_bytes: Optional[bytes],
        context: ProcessingContext,
        stream_info: Optional[Dict[str, Any]]
    ) -> ProcessingResult:
        """
        Dispatch processing to the appropriate use case with correct parameters.
        
        This method handles the different method signatures required by different use cases.
        """
        # Use cases that require input_bytes parameter
        use_cases_with_bytes = {
            ColorDetectionUseCase,
            FlareAnalysisUseCase,
            LicensePlateMonitorUseCase,
            AgeGenderUseCase,
            PeopleTrackingUseCase,
            FaceRecognitionEmbeddingUseCase,
            VehicleColorDetectionUseCase
        }
        
        # Async use cases
        async_use_cases = {
            FaceRecognitionEmbeddingUseCase,
            LicensePlateMonitorUseCase
        }
        
        # Determine the appropriate method signature and call
        use_case_type = type(use_case)
        
        if use_case_type in async_use_cases:
            # Handle async use cases
            if use_case_type in use_cases_with_bytes:
                result = await use_case.process(data, config, input_bytes, context, stream_info)
            else:
                result = await use_case.process(data, config, context, stream_info)
        else:
            # Handle synchronous use cases
            if use_case_type in use_cases_with_bytes:
                result = use_case.process(data, config, input_bytes, context, stream_info)
            else:
                # Default signature for most use cases
                result = use_case.process(data, config, context, stream_info)
        
        return result

    async def process(
        self,
        data: Any,
        config: Union[BaseConfig, Dict[str, Any], str, Path] = {},
        input_bytes: Optional[bytes] = None,
        stream_key: Optional[str] = "default_stream",
        stream_info: Optional[Dict[str, Any]] = None,
        context: Optional[ProcessingContext] = None,
        custom_post_processing_config: Optional[Union[Dict[str, Any], BaseConfig, str]] = None,
    ) -> ProcessingResult:
        """
        Process data using the specified configuration.

        Args:
            data: Raw model output (detection, tracking, classification results)
            config: Configuration object, dict, or path to config file
            input_bytes: Optional input bytes for certain use cases
            custom_post_processing_config: Optional custom post processing configuration
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference (optional)
            context: Optional processing context
            custom_post_processing_config: Optional custom post processing configuration
        Returns:
            ProcessingResult: Standardized result object
        """
        start_time = time.time()
        
        try:
            if config:
                try:
                    config = self._parse_config(config)
                except Exception as e:
                    logger.error(f"Failed to parse config: {e}", exc_info=True)
                    raise ValueError(f"Failed to parse config: {e}")

            parsed_config = config or self.post_processing_config
                
            if not parsed_config:
                raise ValueError("No valid configuration found")


            # Get cached use case instance (await since it's async now)
            use_case = await self._get_use_case_instance(parsed_config, stream_key)

            # Create context if not provided
            if context is None:
                context = ProcessingContext()

            # Ensure stream_key is available in stream_info for tracker namespacing
            if stream_info is None:
                stream_info = {}
            if stream_key and 'stream_key' not in stream_info:
                stream_info['stream_key'] = stream_key

            # Process with use case using dispatch pattern
            result = await self._dispatch_use_case_processing(
                use_case, data, parsed_config, input_bytes, context, stream_info
            )

            # Add processing time
            result.processing_time = time.time() - start_time

            # Update statistics
            self._update_statistics(result)

            return result

        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Processing failed: {str(e)}", exc_info=True)

            error_result = self._create_error_result(
                str(e), type(e).__name__, context=context
            )
            error_result.processing_time = processing_time

            # Update statistics
            self._update_statistics(error_result)

            return error_result

    async def process_simple(
        self,
        data: Any,
        usecase: str,
        category: Optional[str] = None,
        context: Optional[ProcessingContext] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        **config_params,
    ) -> ProcessingResult:
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
                elif usecase == "people_tracking":
                    category = "general"
                else:
                    category = "general"  # Default fallback

            # Create configuration
            config = self.create_config(usecase, category=category, **config_params)
            return await self.process(
                data,
                config,
                context=context,
                stream_key=stream_key,
                stream_info=stream_info,
            )

        except Exception as e:
            logger.error(f"Simple processing failed: {str(e)}", exc_info=True)
            return self._create_error_result(
                str(e), type(e).__name__, usecase, category or "general", context
            )

    async def process_from_file(
        self,
        data: Any,
        config_file: Union[str, Path],
        context: Optional[ProcessingContext] = None,
        stream_key: Optional[str] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
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
            return await self.process(
                data,
                config,
                context=context,
                stream_key=stream_key,
                stream_info=stream_info,
            )

        except Exception as e:
            logger.error(f"File-based processing failed: {str(e)}", exc_info=True)
            return self._create_error_result(
                f"Failed to process with config file: {str(e)}",
                type(e).__name__,
                context=context,
            )

    def create_config(
        self, usecase: str, category: str = "general", **kwargs
    ) -> BaseConfig:
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

    def save_config(
        self, config: BaseConfig, file_path: Union[str, Path], format: str = "json"
    ) -> None:
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

    def get_use_case_schema(
        self, usecase: str, category: str = "general"
    ) -> Dict[str, Any]:
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
                usecase = config.get("usecase")
                if not usecase:
                    return ["Configuration must specify 'usecase'"]

                category = config.get("category", "general")
                parsed_config = config_manager.create_config(
                    usecase, category=category, **config
                )
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
            "cache_keys": list(self._use_case_cache.keys()),
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
            stats["average_processing_time"] = (
                stats["total_processing_time"] / stats["total_processed"]
            )
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
            "total_processing_time": 0.0,
        }

    def _parse_config( # TODO: remove all of the kwargs that are not in the use case config
        self, config: Union[BaseConfig, Dict[str, Any], str, Path]
    ) -> BaseConfig:
        """Parse configuration from various input formats."""
        if isinstance(config, BaseConfig):
            return config
        elif isinstance(config, dict):
            usecase = config.get("usecase")
            if not usecase:
                raise ValueError("Configuration dict must contain 'usecase' key")

            category = config.get("category", "general")
            return config_manager.create_config(usecase, category=category, **config)
        elif isinstance(config, (str, Path)):
            return config_manager.load_from_file(config)
        else:
            raise ValueError(f"Unsupported config type: {type(config)}")

    def _create_error_result(
        self,
        message: str,
        error_type: str = "ProcessingError",
        usecase: str = "",
        category: str = "",
        context: Optional[ProcessingContext] = None,
    ) -> ProcessingResult:
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
                "level_settings": {"info": 2, "warning": 5, "critical": 7},
            },
            "application_name": (
                f"{usecase.title()} Processing" if usecase else "Post Processing"
            ),
            "application_version": "1.0",
            "location_info": None,
            "human_text": f"Event: Processing Error\nLevel: Critical\nTime: {datetime.now(timezone.utc).strftime('%Y-%m-%d-%H:%M:%S UTC')}\nError: {message}",
        }

        result = ProcessingResult(
            data={
                "events": [error_event],
                "tracking_stats": [],
                "error_details": {"message": message, "type": error_type},
            },
            status=ProcessingStatus.ERROR,
            usecase=usecase,
            category=category,
            context=context,
            error_message=message,
            error_type=error_type,
            summary=f"Processing failed: {message}",
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
async def process_simple(
    data: Any, usecase: str, category: Optional[str] = None, **config
) -> ProcessingResult:
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
    return await processor.process_simple(data, usecase, category, **config)


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
