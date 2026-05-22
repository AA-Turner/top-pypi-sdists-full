"""Stub file for post_processing directory."""
from typing import Any, Dict, List, Optional, Union

from .config import get_category_from_app_name, get_usecase_from_app_name
from .core.base import ProcessingContext, ProcessingResult, ProcessingStatus, registry
from .core.config import AlertConfig, BaseConfig, TrackingConfig, ZoneConfig, config_manager
from .core.config_utils import create_config_from_template
from .face_reg.face_recognition import FaceRecognitionEmbeddingUseCase
from .usecases import AbandonedObjectDetectionUseCase, AdvancedCustomerServiceUseCase, AgeDetectionUseCase, AgeGenderUseCase, AnimalDetectionUseCase, AntiSpoofingDetectionUseCase, AreaUtilizationUseCase, AssemblyLineUseCase, BananaMonitoringUseCase, BloodCancerDetectionUseCase, BottleDefectDetectionUseCase, BottleDefectUseCase, BurglaryDetectionUseCase, CarDamageDetectionUseCase, CardiomegalyUseCase, CarPartSegmentationUseCase, CellMicroscopyUseCase, ChickenPoseDetectionUseCase, ChildMonitoringUseCase, ClaudePeopleCountingUsecaseUseCase, ColorDetectionUseCase, ConcreteCrackUseCase, CropWeedDetectionUseCase, CrowdDensityHeatMapsUseCase, CrowdflowUseCase, CustomerServiceUseCase, DistractedDriverUseCase, DroneTrafficMonitoringUsecase, DrowsyDriverUseCase, DwellUseCase, EmergencyVehicleUseCase, FaceCoveringDetectionPoseUseCase, FaceEmotionUseCase, FallDetectionUseCase, FashionDetectionUseCase, FenceClimbingDetectionUseCase, FenceClimbingPoseGatedDetectionUseCase, FenceClimbingWithZoneUseCase, FieldMappingUseCase, FireSmokeUseCase, FlareAnalysisUseCase, FlowerUseCase, FootFallUseCase, GasLeakDetectionUseCase, GenderDetectionUseCase, GlovesBootsDetectionUseCase, HazardZoneEntryUseCase, HeatMapsUseCase, HistopathologicalCancerDetectionUseCase, HumanActivityUseCase, IntrusionUseCase, LandslideDetectionUseCase, LaneDetectionUseCase, LeafDiseaseDetectionUseCase, LeafUseCase, LeakDetectionUseCase, LicensePlateMonitorUseCase, LicensePlateUseCase, LiquidLeakDetectionUseCase, LitterDetectionUseCase, LoiteringUseCase, MaskDetectionUseCase, MaskTypeDetectionUseCase, NaturalDisasterUseCase, OvercrowdingDetectionUseCase, PackageDetectionUseCase, ParkingLotAnalyticsUseCase, ParkingSpaceUseCase, ParkingUseCase, PCBDefectUseCase, PedestrianDetectionUseCase, PeopleCountingInZoneUseCase, PeopleCountingUseCase, PeopleTrackingUseCase, PhoneScreenDefectDetectionUseCase, PipeCorrosionDetectionUseCase, PipeGasLeakDetectionUseCase, PipelineDetectionUseCase, PlaqueSegmentationUseCase, PotholeDetectionUseCase, PotholeSegmentationUseCase, PPEComplianceUseCase, PriceTagUseCase, ProximityUseCase, RoadTrafficUseCase, RoadViewSegmentationUseCase, RunningDetectionUseCase, ShelfInventoryUseCase, ShopliftingDetectionUseCase, ShoppingCartUseCase, SkinCancerClassificationUseCase, SmokerDetectionUseCase, SolarPanelUseCase, StoppedVehicleMonitoringUseCase, SusActivityUseCase, TailgatingDetectionUseCase, TheftDetectionUseCase, TrafficSignMonitoringUseCase, UndergroundPipelineDefectUseCase, UnderwaterPlasticUseCase, VegetableDetectionUseCase, VehicleColorDetectionUseCase, VehicleMonitoringDroneViewUseCase, VehicleMonitoringParkingLotUseCase, VehicleMonitoringUseCase, VehicleMonitoringWrongWayUseCase, WarehouseObjectUseCase, WaterBodyUseCase, WeaponDetectionUseCase, WeldDefectUseCase, WildLifeMonitoringUseCase, WindmillMaintenanceUseCase, WoundSegmentationUseCase

# Constants
APP_NAME_TO_CATEGORY: Dict[Any, Any] = ...  # From config
APP_NAME_TO_USECASE: Dict[Any, Any] = ...  # From config
logger: Any = ...  # From post_processor

# Functions
# From config
def get_category_from_app_name(app_name: str) -> str: ...

# From config
def get_usecase_from_app_name(app_name: str) -> str: ...

# From post_processor
def create_config_template(usecase: str) -> Dict[str, Any]:
    """
    Create a configuration template for a use case.
    
    Args:
        usecase: Use case name
    
    Returns:
        Dict[str, Any]: Configuration template
    """
    ...

# From post_processor
def list_available_usecases() -> Dict[str, List[str]]:
    """
    List all available use cases.
    
    Returns:
        Dict[str, List[str]]: Available use cases by category
    """
    ...

# From post_processor
async def process_simple(data: Any, usecase: str, category: Optional[str] = None, **config: Any) -> Any:
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
    ...

# From post_processor
def validate_config(config: Union[Any, Dict[str, Any]]) -> List[str]:
    """
    Validate a configuration.
    
    Args:
        config: Configuration to validate
    
    Returns:
        List[str]: List of validation errors
    """
    ...

# Classes
# From post_processor
class PostProcessor:
    # Unified post-processing interface with clean API and comprehensive functionality.
    #
    # This processor provides a simple yet powerful interface for processing model outputs
    # with various use cases, centralized configuration management, and comprehensive
    # error handling.
    #
    # Examples:
    #     # Simple usage
    #     processor = PostProcessor()
    #     result = processor.process_simple(
    #         raw_results, "people_counting",
    #         confidence_threshold=0.6,
    #         zones={"entrance": [[0, 0], [100, 0], [100, 100], [0, 100]]}
    #     )
    #
    #     # Configuration-based usage
    #     config = processor.create_config("people_counting", confidence_threshold=0.5)
    #     result = processor.process(raw_results, config)
    #
    #     # File-based configuration
    #     result = processor.process_from_file(raw_results, "config.json")

    def __init__(self: Any, post_processing_config: Optional[Union[Dict[str, Any], Any, str]] = None, app_name: Optional[str] = None, index_to_category: Optional[Dict[int, str]] = None, target_categories: Optional[List[str]] = None) -> None:
        """
        Initialize the PostProcessor with registered use cases.
        """
        ...

    def clear_use_case_cache(self: Any) -> None:
        """
        Clear the use case instance cache.
        """
        ...

    def create_config(self: Any, usecase: str, category: str = 'general', **kwargs: Any) -> Any:
        """
        Create a validated configuration object.
        
        Args:
            usecase: Use case name
            category: Use case category
            **kwargs: Configuration parameters
        
        Returns:
            BaseConfig: Validated configuration object
        """
        ...

    def get_cache_stats(self: Any) -> Dict[str, Any]:
        """
        Get statistics about the use case cache.
        
        Returns:
            Dict[str, Any]: Cache statistics
        """
        ...

    def get_config_template(self: Any, usecase: str) -> Dict[str, Any]:
        """
        Get configuration template for a use case.
        """
        ...

    def get_statistics(self: Any) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dict[str, Any]: Processing statistics
        """
        ...

    def get_supported_usecases(self: Any) -> List[str]:
        """
        Get list of supported use case names.
        """
        ...

    def get_use_case_schema(self: Any, usecase: str, category: str = 'general') -> Dict[str, Any]:
        """
        Get JSON schema for a use case configuration.
        
        Args:
            usecase: Use case name
            category: Use case category
        
        Returns:
            Dict[str, Any]: JSON schema for the use case
        """
        ...

    def list_available_usecases(self: Any) -> Dict[str, List[str]]:
        """
        List all available use cases by category.
        """
        ...

    def load_config(self: Any, file_path: Union[str, Any]) -> Any:
        """
        Load configuration from file.
        """
        ...

    async def process(self: Any, data: Any, config: Union[Any, Dict[str, Any], str, Any] = {}, input_bytes: Optional[Any] = None, stream_key: Optional[str] = 'default_stream', stream_info: Optional[Dict[str, Any]] = None, context: Optional[Any] = None, custom_post_processing_config: Optional[Union[Dict[str, Any], Any, str]] = None) -> Any:
        """
        Process data using the specified configuration.
        
        The uploaded config (from the inference pipeline) is passed via the config parameter
        and takes precedence. If config is not provided, self.post_processing_config is used.
        
        Args:
            data: Raw model output (detection, tracking, classification results)
            config: Configuration object, dict, or path to config file (uploaded config from pipeline)
            input_bytes: Optional input bytes for certain use cases
            stream_key: Stream key for the inference
            stream_info: Stream info for the inference (optional)
            context: Optional processing context
            custom_post_processing_config: Deprecated. Do not use; config parameter is used for uploaded config.
        Returns:
            ProcessingResult: Standardized result object
        """
        ...

    async def process_from_file(self: Any, data: Any, config_file: Union[str, Any], context: Optional[Any] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
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
        ...

    async def process_simple(self: Any, data: Any, usecase: str, category: Optional[str] = None, context: Optional[Any] = None, stream_key: Optional[str] = None, stream_info: Optional[Dict[str, Any]] = None, **config_params: Any) -> Any:
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
        ...

    def reset_statistics(self: Any) -> None:
        """
        Reset processing statistics.
        """
        ...

    def save_config(self: Any, config: Any, file_path: Union[str, Any], fmt: str = 'json') -> None:
        """
        Save configuration to file.
        """
        ...

    def validate_config(self: Any, config: Union[Any, Dict[str, Any]]) -> List[str]:
        """
        Validate a configuration object or dictionary.
        
        Args:
            config: Configuration to validate
        
        Returns:
            List[str]: List of validation errors (empty if valid)
        """
        ...


from . import config, post_processor