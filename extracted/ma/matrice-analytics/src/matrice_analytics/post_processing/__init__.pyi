"""Stub file for post_processing directory."""
from typing import Any, Dict, List, Optional, Union

from ..analytics.engine_session import AnalyticsEngineSession
from ..analytics.engine_session import looks_like_coco_index_to_category, looks_like_wrong_ppe_index_to_category, normalize_index_to_category
from ..analytics.engine_session import looks_like_wrong_ppe_index_to_category, normalize_index_to_category
from ..analytics.engine_session import normalize_index_to_category
from ..analytics.flow import load_manifest_index_to_category
from ..analytics.flow import resolve_manifest_for_app
from ..analytics.redis_publisher import AnalyticsRedisPublisher
from ..engine.routing import RoutingError
from ..runtime.backends import BackendError, require_engine_ready, resolve_source_dims
from ..runtime.backends import BackendError, select_engine_backend
from .config import get_category_from_app_name, get_usecase_from_app_name
from .core.base import ProcessingContext, ProcessingResult, ProcessingStatus, registry
from .core.config import AlertConfig, BaseConfig, TrackingConfig, ZoneConfig, config_manager
from .core.config_utils import create_config_from_template
from .face_reg.face_recognition import FaceRecognitionEmbeddingUseCase
from .usecases import AbandonedObjectDetectionUseCase, AccidentDetectionUseCase, AdvancedCustomerServiceUseCase, AgeDetectionUseCase, AgeGenderUseCase, AnimalDetectionUseCase, AntiSpoofingDetectionUseCase, AreaUtilizationUseCase, AssemblyLineUseCase, BananaMonitoringUseCase, BloodCancerDetectionUseCase, BottleDefectDetectionUseCase, BottleDefectUseCase, BurglaryDetectionUseCase, CarDamageDetectionUseCase, CardiomegalyUseCase, CarPartSegmentationUseCase, CellMicroscopyUseCase, ChickenPoseDetectionUseCase, ChildMonitoringUseCase, ClaudePeopleCountingUsecaseUseCase, ColorDetectionUseCase, ConcreteCrackUseCase, CropWeedDetectionUseCase, CrowdDensityHeatMapsUseCase, CrowdflowUseCase, CustomerServiceUseCase, DeepOCSortUseCase, DistractedDriverUseCase, DroneDetectionUseCase, DroneTrafficMonitoringUsecase, DrowsyDriverUseCase, DwellUseCase, EmergencyVehicleUseCase, FaceCoveringDetectionPoseUseCase, FaceEmotionUseCase, FallDetectionUseCase, FashionDetectionUseCase, FastPeopleCountingUseCase, FenceClimbingDetectionUseCase, FenceClimbingPoseGatedDetectionUseCase, FenceClimbingWithZoneUseCase, FieldMappingUseCase, FireSmokeUseCase, FlareAnalysisUseCase, FloodDetectionUseCase, FlowerUseCase, FootFallUseCase, GasLeakDetectionUseCase, GenderDetectionUseCase, GlovesBootsDetectionUseCase, HazardZoneEntryUseCase, HeatMapsUseCase, HistopathologicalCancerDetectionUseCase, HumanActivityUseCase, IllegalParkingDetectionUseCase, IntrusionUseCase, LandslideDetectionUseCase, LaneDetectionUseCase, LeafDiseaseDetectionUseCase, LeafUseCase, LeakDetectionUseCase, LicensePlateAccessControlUseCase, LicensePlateMonitorUseCase, LicensePlateSurveillanceUseCase, LicensePlateUseCase, LiquidLeakDetectionUseCase, LitterDetectionUseCase, LoiteringUseCase, MaskDetectionUseCase, MaskTypeDetectionUseCase, NaturalDisasterUseCase, OvercrowdingDetectionUseCase, PackageDetectionUseCase, ParkingLotAnalyticsUseCase, ParkingSpaceUseCase, ParkingUseCase, PCBDefectUseCase, PedestrianDetectionUseCase, PeopleCountingInZoneUseCase, PeopleCountingUseCase, PeopleTrackingUseCase, PhoneScreenDefectDetectionUseCase, PipeCorrosionDetectionUseCase, PipeGasLeakDetectionUseCase, PipelineDetectionUseCase, PlaqueSegmentationUseCase, PotholeDetectionUseCase, PotholeSegmentationUseCase, PPEComplianceUseCase, PriceTagUseCase, ProximityUseCase, RoadTrafficUseCase, RoadViewSegmentationUseCase, RunningDetectionUseCase, ShelfInventoryUseCase, ShopliftingDetectionUseCase, ShoppingCartUseCase, SkinCancerClassificationUseCase, SmokerDetectionUseCase, SolarPanelUseCase, StoppedVehicleMonitoringUseCase, StreetVendorDetectionUseCase, SusActivityUseCase, TailgatingDetectionUseCase, TheftDetectionUseCase, TrafficSignMonitoringUseCase, UnauthorizedEncampmentDetectionUseCase, UndergroundPipelineDefectUseCase, UnderwaterPlasticUseCase, UnwantedAnimalDetectionUseCase, VegetableDetectionUseCase, VehicleColorDetectionUseCase, VehicleMonitoringDroneViewUseCase, VehicleMonitoringParkingLotUseCase, VehicleMonitoringUseCase, VehicleMonitoringWrongWayUseCase, VehicleSegmentationUseCase, VehicleTypeClassificationUseCase, ViolenceDetectionTestingUseCase, ViolenceDetectionUseCase, WarehouseObjectUseCase, WaterBodyUseCase, WeaponDetectionUseCase, WeaponHumanDetectionUseCase, WeldDefectUseCase, WildLifeMonitoringUseCase, WindmillMaintenanceUseCase, WoundSegmentationUseCase
from .usecases.car_damage_detection import CarDamageConfig
from .usecases.fr_access_control import FaceRecognitionAccessControlUseCase
from .usecases.fr_surveillance import FaceRecognitionSurveillanceUseCase
from .usecases.ppe_compliance import PPEComplianceConfig
from .utils.geometry_utils import reference_size_from_payload, resolve_frame_dims
from .utils.legacy_analytics_bridge import legacy_redis_analytics_usecases, publish_legacy_frame_analytics
from .utils.post_processing_config_client import PostProcessingConfigClient
from .utils.post_processing_config_client import is_null_object_id, is_resolvable_location_id, looks_like_object_id, normalize_location_id

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
async def process_simple(data: Any, usecase: str, category: str | None = None, **config: Any) -> Any:
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

    def __init__(self: Any, post_processing_config: Union[Dict[str, Any], Any, str] | None = None, app_name: str | None = None, index_to_category: Dict[int, str] | None = None, target_categories: List[str] | None = None, redis_config: Dict[str, Any] | None = None) -> None:
        """
        Initialize the PostProcessor with registered use cases.
        
                Args:
                    redis_config: Connection details for the analytics publisher
                        (``host``/``port``/``password``/``username``/``db`` and, on an HA
                        cluster, ``sentinel_hosts``/``master_name``). When omitted the
                        publisher falls back to the environment. Passing it explicitly
                        is what lets a caller that already resolved the topology avoid
                        depending on the pod's env being set.
        """
        ...

    def clear_use_case_cache(self: Any) -> None:
        """
        Clear the use case instance cache.
        """
        ...

    def close(self: Any) -> None:
        """
        Release what this processor holds, flushing the engine's open windows first.
        
                **The window flush is the point.** ``EngineBackend.close`` is documented "Flush every open
                window, then release the publisher": without it the last partial window of every camera is
                discarded rather than published. On a long-running deployment that is once per camera per
                shutdown -- and shutdowns are routine (restart, redeploy, scale-down), so it is a recurring
                under-reported final interval that looks complete to every consumer downstream.
        
                ``PostProcRunner`` has always closed its backend for exactly this reason
                (``post_proc_runner.py``: "the engine flushes its open windows here"). This class had no
                ``close``/``flush``/``shutdown`` at all, so a caller that wanted to do the right thing had
                nothing to call -- which is why ``py_inference``'s analytics node never did.
        
                Idempotent, and never raises: a failure to flush must not turn an orderly shutdown into a
                crash, and the caller is on its way out anyway.
        """
        ...

    def create_config(self: Any, usecase: str, category: str = 'general', **kwargs: Any) -> Any:
        """
        Create a validated configuration object.
        
        A key the target config class does not declare is **dropped with a WARNING naming it**,
        not raised. Deliberate, and it is the fix for a live outage: a deployment's
        ``post_processing_config`` is authored for the analytics engine (``app.yaml``), while this
        builds a *legacy* dataclass, so keys legitimately exist in the config that no legacy class
        has a field for -- ``method`` from a ``line_crossing``/dwell stage being the first one a
        deployment carried. As an exception that was fatal::
        
            TypeError: DwellConfig.__init__() got an unexpected keyword argument 'method'
            ERROR - Simple processing failed: ... 'method'
        
        and it killed the frame before dispatch, so the app published nothing at all.
        
        Dropping-with-a-warning is strictly better than the alternatives here. Raising takes the
        whole deployment down for a key that is *valid* somewhere else in the system. Dropping
        silently would hide a genuine typo across the ~140 legacy use cases. A named WARNING keeps
        the diagnosis and keeps the app running -- and it is more diagnosable than the status quo,
        where one bad key produced a stack trace with no statement of which config was being built.
        
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

    async def process(self: Any, data: Any, config: Union[Any, Dict[str, Any], str, Any] = {}, input_bytes: Any | None = None, stream_key: str | None = 'default_stream', stream_info: Dict[str, Any] | None = None, context: Any | None = None, custom_post_processing_config: Union[Dict[str, Any], Any, str] | None = None) -> Any:
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

    async def process_from_file(self: Any, data: Any, config_file: Union[str, Any], context: Any | None = None, stream_key: str | None = None, stream_info: Dict[str, Any] | None = None) -> Any:
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

    async def process_simple(self: Any, data: Any, usecase: str, category: str | None = None, context: Any | None = None, stream_key: str | None = None, stream_info: Dict[str, Any] | None = None, **config_params: Any) -> Any:
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