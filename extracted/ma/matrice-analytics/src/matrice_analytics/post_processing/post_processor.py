"""
Main post-processing processor with unified, clean API.

This module provides the main PostProcessor class that serves as the entry point
for all post-processing operations. It manages use cases, configurations, and
provides both simple and advanced processing interfaces.
"""

import hashlib
import json
import logging
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Union

from .config import (
    get_category_from_app_name,
    get_usecase_from_app_name,
)
from .core.base import ProcessingContext, ProcessingResult, ProcessingStatus, registry
from .core.config import (
    AlertConfig,
    BaseConfig,
    TrackingConfig,
    ZoneConfig,
    config_manager,
)
from .core.config_utils import create_config_from_template

# Face recognition with embeddings (from face_reg module)
from .face_reg.face_recognition import FaceRecognitionEmbeddingUseCase
from .usecases import (
    AbandonedObjectDetectionUseCase,
    AccidentDetectionUseCase,
    AdvancedCustomerServiceUseCase,
    AgeDetectionUseCase,
    AgeGenderUseCase,
    AnimalDetectionUseCase,
    AntiSpoofingDetectionUseCase,
    AreaUtilizationUseCase,
    AssemblyLineUseCase,
    BananaMonitoringUseCase,
    # Put all IMAGE based usecases here
    BloodCancerDetectionUseCase,
    BottleDefectDetectionUseCase,
    BottleDefectUseCase,
    BurglaryDetectionUseCase,
    CarDamageDetectionUseCase,
    CardiomegalyUseCase,
    CarPartSegmentationUseCase,
    CellMicroscopyUseCase,
    ChickenPoseDetectionUseCase,
    ChildMonitoringUseCase,
    ClaudePeopleCountingUsecaseUseCase,
    ColorDetectionUseCase,
    ConcreteCrackUseCase,
    CropWeedDetectionUseCase,
    CrowdDensityHeatMapsUseCase,
    CrowdflowUseCase,
    CustomerServiceUseCase,
    DeepOCSortUseCase,
    DistractedDriverUseCase,
    DroneDetectionUseCase,
    DroneTrafficMonitoringUsecase,
    # FaceRecognitionUseCase,
    DrowsyDriverUseCase,
    DwellUseCase,
    EmergencyVehicleUseCase,
    FaceCoveringDetectionPoseUseCase,
    FaceEmotionUseCase,
    FallDetectionUseCase,
    FashionDetectionUseCase,
    FastPeopleCountingUseCase,
    FenceClimbingDetectionUseCase,
    FenceClimbingPoseGatedDetectionUseCase,
    FenceClimbingWithZoneUseCase,
    FieldMappingUseCase,
    FireSmokeUseCase,
    FlareAnalysisUseCase,
    FloodDetectionUseCase,
    FlowerUseCase,
    FootFallUseCase,
    GasLeakDetectionUseCase,
    GenderDetectionUseCase,
    GlovesBootsDetectionUseCase,
    HazardZoneEntryUseCase,
    HeatMapsUseCase,
    HistopathologicalCancerDetectionUseCase,
    HumanActivityUseCase,
    IllegalParkingDetectionUseCase,
    IntrusionUseCase,
    LandslideDetectionUseCase,
    LaneDetectionUseCase,
    LeafDiseaseDetectionUseCase,
    LeafUseCase,
    LeakDetectionUseCase,
    LicensePlateAccessControlUseCase,
    LicensePlateMonitorUseCase,
    LicensePlateSurveillanceUseCase,
    LicensePlateUseCase,
    LiquidLeakDetectionUseCase,
    LitterDetectionUseCase,
    LoiteringUseCase,
    MaskDetectionUseCase,
    MaskTypeDetectionUseCase,
    NaturalDisasterUseCase,
    OvercrowdingDetectionUseCase,
    PackageDetectionUseCase,
    ParkingLotAnalyticsUseCase,
    ParkingSpaceUseCase,
    ParkingUseCase,
    PCBDefectUseCase,
    PedestrianDetectionUseCase,
    PeopleCountingInZoneUseCase,
    PeopleCountingUseCase,
    PeopleTrackingUseCase,
    PhoneScreenDefectDetectionUseCase,
    PipeCorrosionDetectionUseCase,
    PipeGasLeakDetectionUseCase,
    PipelineDetectionUseCase,
    PlaqueSegmentationUseCase,
    PotholeDetectionUseCase,
    PotholeSegmentationUseCase,
    PPEComplianceUseCase,
    PriceTagUseCase,
    ProximityUseCase,
    RoadTrafficUseCase,
    RoadViewSegmentationUseCase,
    RunningDetectionUseCase,
    ShelfInventoryUseCase,
    ShopliftingDetectionUseCase,
    ShoppingCartUseCase,
    SkinCancerClassificationUseCase,
    SmokerDetectionUseCase,
    SolarPanelUseCase,
    StoppedVehicleMonitoringUseCase,
    StreetVendorDetectionUseCase,
    SusActivityUseCase,
    TailgatingDetectionUseCase,
    TheftDetectionUseCase,
    TrafficSignMonitoringUseCase,
    UnauthorizedEncampmentDetectionUseCase,
    UndergroundPipelineDefectUseCase,
    UnderwaterPlasticUseCase,
    UnwantedAnimalDetectionUseCase,
    VegetableDetectionUseCase,
    VehicleColorDetectionUseCase,
    VehicleMonitoringDroneViewUseCase,
    VehicleMonitoringParkingLotUseCase,
    VehicleMonitoringUseCase,
    VehicleMonitoringWrongWayUseCase,
    VehicleSegmentationUseCase,
    VehicleTypeClassificationUseCase,
    ViolenceDetectionTestingUseCase,
    ViolenceDetectionUseCase,
    WarehouseObjectUseCase,
    WaterBodyUseCase,
    WeaponDetectionUseCase,
    WeaponHumanDetectionUseCase,
    WeldDefectUseCase,
    WildLifeMonitoringUseCase,
    WindmillMaintenanceUseCase,
    WoundSegmentationUseCase,
)
from .usecases.fr_access_control import FaceRecognitionAccessControlUseCase
from .usecases.fr_surveillance import FaceRecognitionSurveillanceUseCase

logger = logging.getLogger(__name__)


def _resolve_new_flow_manifest(app_name: str | None) -> str | None:
    """Return the new-flow manifest for *app_name*, or None for the legacy flow.

    Lazily imports the analytics subpackage so a stale install that lacks it
    (or any resolution error) cleanly stays on the legacy path.
    """
    try:
        from ..analytics.flow import resolve_manifest_for_app

        return resolve_manifest_for_app(app_name)
    except Exception as e:  # ImportError on old layouts, or any resolver error
        logger.debug("New analytics flow unavailable for app '%s' (%s); using legacy", app_name, e)
        return None


#: Keys that describe *which app to run*, not how to configure a use case. They are stripped before
#: `create_config`, which would otherwise reject an app-bundle reference as an unknown field and
#: fall back to empty defaults. Only ever present on a config that names a bundle, so no legacy
#: app's behaviour changes.
_NON_USECASE_CONFIG_KEYS = (
    "usecase",
    "category",
    "app_bundle_url",
    "usecase_codebase_url",
    "app_url",
    "app_manifest",
    # Deployment identity, never use-case configuration. Present because a caller has to put it in
    # `post_processing_config` for `resolve_app_bundle_refs` to find a bundle to mint -- that is the
    # only channel it reads -- and `py_inference`'s analytics node now does exactly that. Stripping
    # them here keeps them out of `create_config`, which would otherwise drop each one with a
    # WARNING naming it and make every legacy app noisy. Same reasoning as `app_bundle_url` above.
    "application_id",
    "applicationId",
    "app_id",
    "appId",
    "app_deployment_id",
    "appDeploymentId",
    "application_version",
    "applicationVersion",
)


#: Analytics DOMAIN labels -- the metric-grouping vocabulary the dashboard and ClickHouse route by.
#: NOT detection class names. Source of truth is ``engine/manifest/models.py`` (``ANALYTICS_CATEGORIES``
#: = the three with backend meaning) plus ``INCIDENT`` and the two retired processor categories, which
#: still reach ClickHouse as literal strings. Duplicated here rather than imported: ``post_processing/``
#: does not otherwise import from ``engine/``, and a six-element frozenset is a cheaper dependency than
#: a new layer crossing. Keep in step with that module if the vocabulary ever grows.
_ANALYTICS_DOMAIN_LABELS = frozenset(("VOLUME", "SAFETY", "QUALITY", "INCIDENT", "IDENTITY", "SPECIAL"))


def _reject_domain_label_categories(target_categories: Any, source: str) -> Any:
    """Drop a ``target_categories`` list that is entirely analytics domain labels.

    Every ``target_categories`` consumer in this package means ML class names -- the use cases all do
    ``d.get("category") in self.target_categories`` -- while ``post_processing_config["category"]`` is a
    domain label (``VOLUME``/``SAFETY``/``QUALITY``). An engine that confuses the two hands us
    ``["SAFETY"]``, which matches no class, and every use case then counts zero. py_inference did
    exactly that (its resolver fell back to ``use_case_config.category``), and because
    ``_apply_instance_config_overrides`` writes this value ONTO the use-case config, the damage reached
    the counts as well as the published detections.

    This is the seam every caller passes through, so the guard belongs here as well as in the callers:
    the same defect existed independently in two engines.

    All-or-nothing. A mixed list (``["person", "SAFETY"]``) is a partly-wrong operator filter, not a
    vocabulary mix-up, and dropping it would lose ``person`` -- the half that works. Matched
    EXACT-UPPERCASE, so a model class legitimately named ``safety`` is untouched; a manifest cannot
    declare a lowercase domain label anyway (``AppSpec._validate_category``).

    Returns the list unchanged, or ``None`` when it is rejected.
    """
    if not target_categories or not isinstance(target_categories, (list, tuple, set, frozenset)):
        return target_categories
    values = [str(c) for c in target_categories]
    if not all(v in _ANALYTICS_DOMAIN_LABELS for v in values):
        return target_categories
    logger.warning(
        "target_categories=%s from %s is an analytics DOMAIN label list (%s), not ML class names -- "
        "ignoring it. Domain labels match no detection category, so honouring this would report zero "
        "counts and publish an empty detections list. The caller is conflating "
        "post_processing_config['category'] with a class filter.",
        values,
        source,
        "/".join(sorted(_ANALYTICS_DOMAIN_LABELS)),
    )
    return None


#: ``X.__init__() got an unexpected keyword argument 'name'`` -- CPython's wording, stable across
#: 3.8-3.12. Matched rather than assumed: an unrelated TypeError must still propagate.
_UNEXPECTED_KWARG_RE = re.compile(r"unexpected keyword argument ['\"]([^'\"]+)['\"]")


def _unexpected_kwarg(message: str) -> str | None:
    """The keyword name an unknown-kwarg ``TypeError`` names, or ``None`` for any other TypeError."""
    match = _UNEXPECTED_KWARG_RE.search(message or "")
    return match.group(1) if match else None


def _usecase_of(config: Any) -> str | None:
    """The ``usecase`` a config names, whichever shape it arrived in.

    Used only to ask the analytics engine "is there a manifest for this app?". A miss here just
    means the legacy path, so it never raises and never guesses.
    """
    if isinstance(config, dict):
        value = config.get("usecase")
    else:
        value = getattr(config, "usecase", None)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _backfill_stream_resolution(data: Any, stream_info: Dict[str, Any] | None) -> Dict[str, Any] | None:
    """``stream_info`` with ``stream_resolution`` filled from the payload, when it was missing.

    Gap-fill only, and copied rather than mutated -- the caller's dict is theirs, and a value
    they supplied is always right about their own stream.

    Why this is needed at all: zone membership is decided by testing a bbox-derived point
    against a polygon, and the two have to be in the same space. The polygons arrive in pixels
    (``PostProcessingConfigClient.denormalize_config``) while detections arrive normalized 0-1,
    so the scaling step needs the frame size -- and on the CUDA-SHM worker path nothing ever put
    one in ``stream_info``. Every zone then reported ``current_count`` 0 and nobody was
    relabelled ``at_risk``/``intruder``, with no error anywhere, because the scaling helper
    correctly fails open when it cannot find dimensions.

    The dimensions were never actually absent -- they were on the payload rather than on
    ``stream_info``. This reads them from there, which is why no ml-codebases change is needed.
    """
    # Imported here rather than at module scope to match how every other `utils` helper is
    # reached from this file, and to keep the import graph of a module this large unchanged.
    from .utils.geometry_utils import reference_size_from_payload, resolve_frame_dims

    if resolve_frame_dims(stream_info) != (0, 0):
        return stream_info
    width, height = reference_size_from_payload(data)
    if width <= 0 or height <= 0:
        return stream_info
    resolved = dict(stream_info or {})
    resolved["stream_resolution"] = {"width": width, "height": height}
    logger.debug(
        "PostProcessor: recovered stream_resolution %dx%d from the payload's coordinate_frame; the caller sent none",
        width,
        height,
    )
    return resolved


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
        post_processing_config: Union[Dict[str, Any], BaseConfig, str] | None = None,
        app_name: str | None = None,
        index_to_category: Dict[int, str] | None = None,
        target_categories: List[str] | None = None,
        redis_config: Dict[str, Any] | None = None,
    ):
        """Initialize the PostProcessor with registered use cases.

        Args:
            redis_config: Connection details for the analytics publisher
                (``host``/``port``/``password``/``username``/``db`` and, on an HA
                cluster, ``sentinel_hosts``/``master_name``). When omitted the
                publisher falls back to the environment. Passing it explicitly
                is what lets a caller that already resolved the topology avoid
                depending on the pod's env being set.
        """
        self._statistics = {
            "total_processed": 0,
            "successful": 0,
            "failed": 0,
            "total_processing_time": 0.0,
        }
        self.cache = {}
        self._use_case_cache = {}  # Cache for use case instances
        self._api_config_cache: Dict[str, BaseConfig] = {}

        # Register available use cases
        self._register_use_cases()

        # Set up default post-processing configuration
        self.post_processing_config = None
        self._init_pp_config_dict: Dict[str, Any] | None = None
        self.app_name = app_name
        self.index_to_category = index_to_category
        self.target_categories = _reject_domain_label_categories(target_categories, "the PostProcessor constructor")

        # New analytics flow: if this app routes to a bundled AnalyticsEngine
        # manifest, process() dispatches to a per-stream AnalyticsEngineSession
        # instead of the legacy use-case path. Resolved once (app_name is fixed
        # for the lifetime of a PostProcessor). None => legacy flow unchanged.
        self._new_flow_manifest: str | None = _resolve_new_flow_manifest(self.app_name)
        self._engine_sessions: Dict[str, Any] = {}  # stream_key -> AnalyticsEngineSession
        self._analytics_publisher: Any = None  # lazy AnalyticsRedisPublisher
        self._redis_config: Dict[str, Any] = redis_config or {}
        self._camera_metadata_cache: Dict[str, Dict[str, str]] = {}
        # Reused PostProcessingConfigClient (owns a Session/RPC with a thread
        # pool). Built once and cached for the PostProcessor's lifetime to avoid
        # spawning a fresh Session/RPC (6 threads) on every frame.
        self._config_client: Any = None
        #: Set once the client is known to be unbuildable (no credentials in the environment),
        #: so the engine's per-frame enrichment does not retry -- and re-log -- on every frame.
        self._config_client_unavailable: bool = False

        # New-flow apps still need index_to_category from the uploaded JSON; only
        # skip full legacy use-case config parsing.
        if self._new_flow_manifest:
            logging.info(
                "PostProcessor: app '%s' uses the new AnalyticsEngine flow (manifest=%s)",
                self.app_name,
                self._new_flow_manifest,
            )
            if isinstance(post_processing_config, dict):
                self._init_pp_config_dict = dict(post_processing_config)
                parsed = self._parse_post_processing_config(post_processing_config, self.app_name)
                if parsed:
                    self.post_processing_config = parsed
            self._ingest_new_flow_mapping(post_processing_config, None)
        elif post_processing_config or self.app_name:
            logging.debug(
                "Parsing post-processing config (input present=%s)",
                post_processing_config is not None,
            )
            if isinstance(post_processing_config, dict):
                self._init_pp_config_dict = dict(post_processing_config)
            self.post_processing_config = self._parse_post_processing_config(post_processing_config, self.app_name)
            if self.post_processing_config:
                logging.info(
                    f"Successfully parsed post-processing config for usecase: {self.post_processing_config.usecase}"
                )
            else:
                logging.warning("Failed to parse post-processing config")
        else:
            logging.info("No post-processing config provided")

    def _load_config_from_app_name(self, app_name: str) -> BaseConfig | None:
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
        app_name: str | None = None,
    ) -> BaseConfig | None:
        """Parse post-processing configuration from various formats."""
        try:
            if not config and not app_name:
                return None

            # Handle app-name based configuration first
            if app_name:
                if config and isinstance(config, dict):
                    # Pass config dict directly to create_config so mandatory fields
                    # (like zones for tailgating) are present at validation time
                    usecase = get_usecase_from_app_name(app_name)
                    category = get_category_from_app_name(app_name)
                    if usecase and category:
                        try:
                            config_kwargs = {k: v for k, v in config.items() if k not in _NON_USECASE_CONFIG_KEYS}
                            app_config = self.create_config(usecase, category, **config_kwargs)
                            return app_config
                        except Exception as _cc_e:
                            # Don't silently swallow — log so the user sees what
                            # made config creation fail. The fall-through to
                            # _load_config_from_app_name produces an empty
                            # default config which loses fields like
                            # facial_recognition_server_id, leading to confusing
                            # "Server ID is required" errors downstream.
                            logging.warning(
                                "create_config(%s, %s) raised — falling back to app-name defaults. kwargs_keys=%s err=%r",
                                usecase,
                                category,
                                list(config_kwargs.keys()),
                                _cc_e,
                            )
                app_config = self._load_config_from_app_name(app_name)
                if app_config:
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

    def _merge_config_into_app_config(self, app_config: BaseConfig, config_dict: Dict[str, Any]) -> BaseConfig:
        """Merge provided configuration dictionary into app-based config."""
        logging.debug("Merging provided config into app config")
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

    def _parse_config_by_type(self, config: Union[Dict[str, Any], BaseConfig, str]) -> BaseConfig | None:
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

    def _parse_config_dict(self, config: Dict[str, Any]) -> BaseConfig | None:
        """Parse configuration from a dictionary."""
        usecase = config.get("usecase")
        if not usecase:
            raise ValueError("Configuration dict must contain 'usecase' key")

        # Prepare config parameters
        config_params = config.copy()
        config_params.pop("usecase", None)
        config_params.pop("category", None)
        category = config.get("category")

        # Clean up use-case specific parameters
        self._clean_use_case_specific_params(usecase, config_params)

        # Normalize nested config objects
        self._normalize_nested_configs(config_params)

        # Create config using the factory
        return self.create_config(usecase, category, **config_params)

    def _clean_use_case_specific_params(self, usecase: str, config_params: Dict[str, Any]) -> None:
        """Remove parameters that aren't needed for specific use cases."""
        facial_recognition_usecases = {
            "face_recognition",
            "fr_access_control",
            "fr_surveillance",
        }
        license_plate_monitoring_usecases = {
            "license_plate_monitor",
            "lpr_access_control",
            "lpr_surveillance",
        }

        if usecase not in facial_recognition_usecases:
            if "facial_recognition_server_id" in config_params:
                logging.debug(f"Removing facial_recognition_server_id from {usecase} config")
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
                # Guarded on the way IN as well as out of the constructor: a platform config can
                # carry a domain label directly, and this branch adopts the config's value as the
                # processor's own, so an unguarded one would propagate to every later use case.
                kept = _reject_domain_label_categories(config.target_categories, "the use-case config")
                # `[]`, not None, on rejection: every consumer here does `in self.target_categories`
                # or `if not target_categories`, so an empty list reads as "no filter" while None
                # would raise TypeError inside the use case -- trading a wrong answer for a crash.
                self.target_categories = kept if kept else []
                config.target_categories = self.target_categories

    def _extract_app_name_from_stream_info(self, stream_info: Dict[str, Any] | None) -> str | None:
        """Resolve application display name from inference stream metadata."""
        if not stream_info or not isinstance(stream_info, dict):
            return None

        name_keys = ("app_name", "application_name", "applicationName", "Application Name")
        for key in name_keys:
            value = stream_info.get(key)
            if value:
                return str(value).strip()

        for nested_key in ("input_settings", "camera_info", "application"):
            nested = stream_info.get(nested_key)
            if not isinstance(nested, dict):
                continue
            for key in (*name_keys, "name"):
                value = nested.get(key)
                if value:
                    return str(value).strip()
        return None

    def _get_post_processing_config_client(self, stream_info: Dict[str, Any] | None = None):
        """Return a config client from stream_info or env-backed credentials."""
        client = stream_info.get("config_client") if stream_info else None
        if client is not None:
            return client

        # Reuse the per-PostProcessor client so we don't build a new
        # Session/RPC (and its thread pool) on every frame.
        if self._config_client is not None:
            return self._config_client

        # Remember the *absence* too. Credentials come from the environment and are fixed for the
        # life of the process, so a failure here is permanent -- but without this we rebuilt the
        # client, and re-logged its "missing Matrice credentials" warning, on every single frame.
        # Harmless while only the legacy route called this; the engine route is the per-frame hot
        # path, and 30fps x N cameras of the same warning buries everything else in the log.
        if self._config_client_unavailable:
            return None

        try:
            from .utils.post_processing_config_client import PostProcessingConfigClient

            client = PostProcessingConfigClient(logger=logger)
            if getattr(client, "_session", None) is None:
                logger.debug(
                    "PostProcessor: no Matrice session for API config fetch "
                    "(set MATRICE_ACCESS_KEY_ID / MATRICE_SECRET_ACCESS_KEY or stream_info['config_client'])"
                )
                self._config_client_unavailable = True
                return None
            self._config_client = client
            return client
        except Exception as exc:
            logger.warning("PostProcessor: could not create PostProcessingConfigClient: %s", exc)
            self._config_client_unavailable = True
            return None

    def _enrich_stream_info_camera_metadata(
        self,
        stream_info: Dict[str, Any] | None,
    ) -> Dict[str, Any]:
        """Merge display camera metadata from Matrice CameraManagement API.

        Per-frame ``stream_info`` from the inference worker often carries only
        ``camera_id`` (and repeats it as ``camera_group``). Legacy
        ``AnalyticsPublisher`` got human-readable names from ``camera_configs``
        passed at pipeline init; the new flow must look them up via API.
        """
        si = dict(stream_info or {})
        client = self._get_post_processing_config_client(si)
        if client is None or not hasattr(client, "get_camera_metadata"):
            return si

        camera_id = client.get_stream_identifiers(si).get("camera_id") or ""
        if not camera_id:
            return si

        meta = self._camera_metadata_cache.get(camera_id)
        if meta is None:
            meta = client.get_camera_metadata(camera_id)
            self._camera_metadata_cache[camera_id] = meta
            if meta.get("camera_name"):
                logger.info(
                    "PostProcessor: resolved camera_name=%r for camera_id=%s",
                    meta["camera_name"],
                    camera_id,
                )

        if not meta:
            return si

        if meta.get("camera_name"):
            si["camera_name"] = meta["camera_name"]
            camera_info = dict(si.get("camera_info") or {})
            camera_info["camera_name"] = meta["camera_name"]
            si["camera_info"] = camera_info
            stream_config = dict(si.get("stream_config") or {})
            stream_config["camera_name"] = meta["camera_name"]
            si["stream_config"] = stream_config

        if meta.get("camera_group"):
            si["camera_group"] = meta["camera_group"]
            camera_info = dict(si.get("camera_info") or {})
            camera_info["camera_group"] = meta["camera_group"]
            si["camera_info"] = camera_info

        from .utils.post_processing_config_client import (
            is_null_object_id,
            is_resolvable_location_id,
            looks_like_object_id,
            normalize_location_id,
        )

        camera_info = si.get("camera_info") if isinstance(si.get("camera_info"), dict) else {}

        location_id = (
            meta.get("location_id")
            or si.get("location_id")
            or si.get("locationId")
            or camera_info.get("location_id")
            or camera_info.get("locationId")
            or ""
        )
        location = ""
        for candidate in (
            camera_info.get("location"),
            si.get("location"),
            meta.get("location"),
        ):
            text = str(candidate or "").strip()
            if not text or is_null_object_id(text) or looks_like_object_id(text):
                continue
            location = text
            break
        if not location_id:
            for candidate in (
                camera_info.get("locationId"),
                camera_info.get("location_id"),
                si.get("locationId"),
                si.get("location_id"),
                meta.get("location_id"),
                camera_info.get("location"),
                si.get("location"),
                meta.get("location"),
            ):
                text = str(candidate or "").strip()
                if is_resolvable_location_id(text):
                    location_id = text
                    break
        if is_resolvable_location_id(location_id) and not location and hasattr(client, "fetch_location_name"):
            resolved = client.fetch_location_name(location_id)
            if resolved:
                location = resolved
                logger.info(
                    "PostProcessor: resolved location=%r for location_id=%s",
                    location,
                    location_id,
                )

        location_id = normalize_location_id(location_id)

        if location_id:
            si["location_id"] = location_id
            si["locationId"] = location_id
            camera_info = dict(si.get("camera_info") or {})
            camera_info["location_id"] = location_id
            camera_info["locationId"] = location_id
            si["camera_info"] = camera_info
            stream_config = dict(si.get("stream_config") or {})
            stream_config["location_id"] = location_id
            stream_config["locationId"] = location_id
            si["stream_config"] = stream_config

        if location:
            si["location"] = location
            camera_info = dict(si.get("camera_info") or {})
            camera_info["location"] = location
            si["camera_info"] = camera_info
            stream_config = dict(si.get("stream_config") or {})
            stream_config["location"] = location
            si["stream_config"] = stream_config

        return si

    def _resolve_config_from_stream(self, stream_info: Dict[str, Any] | None) -> BaseConfig | None:
        """Fetch and parse post-processing config from Matrice API using stream_info."""
        if not stream_info or not isinstance(stream_info, dict):
            return None

        client = self._get_post_processing_config_client(stream_info)
        if client is None:
            return None

        ids = client.get_stream_identifiers(stream_info)
        app_deployment_id = ids.get("app_deployment_id") or ""
        camera_id = ids.get("camera_id") or ""
        if not app_deployment_id or not camera_id:
            logger.debug(
                "PostProcessor: API config fetch skipped (app_deployment_id=%r camera_id=%r)",
                app_deployment_id or "(empty)",
                camera_id or "(empty)",
            )
            return None

        cache_key = f"{app_deployment_id}:{camera_id}"
        cached = self._api_config_cache.get(cache_key)
        if cached is not None:
            return cached

        configs, err, _ = client.get_post_processing_configs_by_app_deployment(app_deployment_id)
        if err or not configs:
            logger.info(
                "PostProcessor: API config fetch failed (app_deployment_id=%s err=%r count=%s)",
                app_deployment_id,
                err,
                len(configs) if configs else 0,
            )
            return None

        client.set_config_cache_from_api(configs)
        filtered = client.filter_configs_by_camera_id(configs, camera_id)
        if not filtered:
            logger.info(
                "PostProcessor: no postProcessing entry for camera_id=%s in deployment %s",
                camera_id,
                app_deployment_id,
            )
            return None

        doc = filtered[0]
        width, height = client.get_resolution(camera_id)
        if width is not None and height is not None:
            doc = client.denormalize_config(doc, width, height)

        post = doc.get("postProcessing") or {}
        cam_cfg = post.get(camera_id) or {}
        if not isinstance(cam_cfg, dict) or not cam_cfg:
            return None

        cfg_dict = dict(cam_cfg)
        if not cfg_dict.get("usecase"):
            app_name = self.app_name or self._extract_app_name_from_stream_info(stream_info)
            if app_name:
                usecase = get_usecase_from_app_name(app_name)
                category = get_category_from_app_name(app_name)
                if usecase:
                    cfg_dict.setdefault("usecase", usecase)
                if category:
                    cfg_dict.setdefault("category", category)

        if not cfg_dict.get("usecase"):
            logger.warning(
                "PostProcessor: API config for camera_id=%s missing usecase and no app_name mapping",
                camera_id,
            )
            return None

        try:
            parsed = self._parse_config_dict(cfg_dict)
        except Exception as exc:
            logger.error(
                "PostProcessor: failed to parse API config for camera_id=%s: %s",
                camera_id,
                exc,
                exc_info=True,
            )
            return None

        if parsed is not None:
            self._api_config_cache[cache_key] = parsed
            logger.info(
                "Successfully parsed post-processing config for usecase: %s (API camera_id=%s)",
                parsed.usecase,
                camera_id,
            )
        return parsed

    def _resolve_parsed_config(
        self,
        config: BaseConfig | None,
        stream_info: Dict[str, Any] | None = None,
    ) -> BaseConfig | None:
        """Resolve effective config: inline, init default, API, or app_name fallbacks."""
        parsed_config = config or self.post_processing_config
        if parsed_config:
            return parsed_config

        if stream_info:
            api_config = self._resolve_config_from_stream(stream_info)
            if api_config:
                self.post_processing_config = api_config
                return api_config

            stream_app_name = self._extract_app_name_from_stream_info(stream_info)
            if stream_app_name:
                app_config = self._load_config_from_app_name(stream_app_name)
                if app_config:
                    self.post_processing_config = app_config
                    self.app_name = self.app_name or stream_app_name
                    logger.info(
                        "Successfully parsed post-processing config for usecase: %s (stream app_name=%r)",
                        app_config.usecase,
                        stream_app_name,
                    )
                    return app_config

        if self.app_name:
            app_config = self._load_config_from_app_name(self.app_name)
            if app_config:
                self.post_processing_config = app_config
                logger.info(
                    "Successfully parsed post-processing config for usecase: %s (init app_name=%r)",
                    app_config.usecase,
                    self.app_name,
                )
                return app_config

        return None

    def _register_use_cases(self) -> None:
        """Register all available use cases."""
        # Register people counting use case
        registry.register_use_case("general", "people_counting", PeopleCountingUseCase)
        registry.register_use_case("general", "fast_people_counting", FastPeopleCountingUseCase)
        registry.register_use_case(
            "general",
            "claude_people_counting_usecase",
            ClaudePeopleCountingUsecaseUseCase,
        )
        registry.register_use_case("general", "deep_oc_sort", DeepOCSortUseCase)

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
        registry.register_use_case("ppe", "ppe_compliance", PPEComplianceUseCase)
        registry.register_use_case("infrastructure", "pothole_segmentation", PotholeSegmentationUseCase)
        registry.register_use_case("safety", "pothole_detection", PotholeDetectionUseCase)
        registry.register_use_case("car_damage", "car_damage_detection", CarDamageDetectionUseCase)

        registry.register_use_case("traffic", "vehicle_monitoring", VehicleMonitoringUseCase)
        registry.register_use_case("traffic", "fruit_monitoring", BananaMonitoringUseCase)
        registry.register_use_case("security", "theft_detection", TheftDetectionUseCase)
        registry.register_use_case("traffic", "traffic_sign_monitoring", TrafficSignMonitoringUseCase)
        registry.register_use_case("traffic", "drone_traffic_monitoring", DroneTrafficMonitoringUsecase)
        registry.register_use_case("security", "anti_spoofing_detection", AntiSpoofingDetectionUseCase)
        registry.register_use_case("retail", "shelf_inventory", ShelfInventoryUseCase)
        registry.register_use_case("traffic", "lane_detection", LaneDetectionUseCase)
        registry.register_use_case("security", "abandoned_object_detection", AbandonedObjectDetectionUseCase)
        registry.register_use_case("hazard", "fire_smoke_detection", FireSmokeUseCase)
        registry.register_use_case("flare_detection", "flare_analysis", FlareAnalysisUseCase)
        registry.register_use_case("general", "face_covering_detection_pose", FaceCoveringDetectionPoseUseCase)
        registry.register_use_case("general", "face_emotion", FaceEmotionUseCase)
        registry.register_use_case("parking_space", "parking_space_detection", ParkingSpaceUseCase)
        registry.register_use_case("environmental", "underwater_pollution_detection", UnderwaterPlasticUseCase)
        registry.register_use_case("pedestrian", "pedestrian_detection", PedestrianDetectionUseCase)
        registry.register_use_case("general", "age_detection", AgeDetectionUseCase)
        registry.register_use_case("weld", "weld_defect_detection", WeldDefectUseCase)
        registry.register_use_case("price_tag", "price_tag_detection", PriceTagUseCase)
        registry.register_use_case("mask_detection", "mask_detection", MaskDetectionUseCase)
        registry.register_use_case("mask_type_detection", "mask_type_detection", MaskTypeDetectionUseCase)
        registry.register_use_case("pipeline_detection", "pipeline_detection", PipelineDetectionUseCase)
        registry.register_use_case("automobile", "distracted_driver_detection", DistractedDriverUseCase)
        registry.register_use_case("traffic", "emergency_vehicle_detection", EmergencyVehicleUseCase)
        registry.register_use_case("energy", "solar_panel", SolarPanelUseCase)
        registry.register_use_case("agriculture", "chicken_pose_detection", ChickenPoseDetectionUseCase)
        registry.register_use_case("agriculture", "crop_weed_detection", CropWeedDetectionUseCase)
        registry.register_use_case("security", "child_monitoring", ChildMonitoringUseCase)
        registry.register_use_case("general", "gender_detection", GenderDetectionUseCase)
        registry.register_use_case("security", "weapon_detection", WeaponDetectionUseCase)
        registry.register_use_case("security", "weapon_human_detection", WeaponHumanDetectionUseCase)
        registry.register_use_case("security", "violence_detection", ViolenceDetectionUseCase)
        registry.register_use_case(
            "security",
            "violence_detection_testing",
            ViolenceDetectionTestingUseCase,
        )
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
        registry.register_use_case("general", "road_traffic_density", RoadTrafficUseCase)
        registry.register_use_case("automobile", "road_view_segmentation", RoadViewSegmentationUseCase)
        # registry.register_use_case("security", "face_recognition", FaceRecognitionUseCase)
        registry.register_use_case("security", "face_recognition", FaceRecognitionEmbeddingUseCase)
        registry.register_use_case("security", "fr_access_control", FaceRecognitionAccessControlUseCase)
        registry.register_use_case("security", "fr_surveillance", FaceRecognitionSurveillanceUseCase)
        registry.register_use_case("automobile", "drowsy_driver_detection", DrowsyDriverUseCase)
        registry.register_use_case("agriculture", "waterbody_segmentation", WaterBodyUseCase)
        registry.register_use_case("litter_detection", "litter_detection", LitterDetectionUseCase)
        registry.register_use_case("oil_gas", "leak_detection", LeakDetectionUseCase)
        registry.register_use_case("general", "human_activity_recognition", HumanActivityUseCase)
        registry.register_use_case("oil_gas", "gas_leak_detection", GasLeakDetectionUseCase)
        registry.register_use_case("license_plate_monitor", "license_plate_monitor", LicensePlateMonitorUseCase)
        registry.register_use_case("license_plate_monitor", "lpr_access_control", LicensePlateAccessControlUseCase)
        registry.register_use_case("license_plate_monitor", "lpr_surveillance", LicensePlateSurveillanceUseCase)
        registry.register_use_case("general", "dwell", DwellUseCase)
        registry.register_use_case("age_gender_detection", "age_gender_detection", AgeGenderUseCase)
        registry.register_use_case("general", "people_tracking", PeopleTrackingUseCase)
        registry.register_use_case("environmental", "wildlife_monitoring", WildLifeMonitoringUseCase)
        registry.register_use_case("manufacturing", "pcb_defect_detection", PCBDefectUseCase)
        registry.register_use_case("general", "underground_pipeline_defect", UndergroundPipelineDefectUseCase)
        registry.register_use_case("security", "suspicious_activity_detection", SusActivityUseCase)
        registry.register_use_case("environmental", "natural_disaster_detection", NaturalDisasterUseCase)
        registry.register_use_case("retail", "footfall", FootFallUseCase)
        registry.register_use_case(
            "traffic",
            "vehicle_monitoring_parking_lot",
            VehicleMonitoringParkingLotUseCase,
        )
        registry.register_use_case(
            "traffic",
            "vehicle_monitoring_drone_view",
            VehicleMonitoringDroneViewUseCase,
        )
        registry.register_use_case("traffic", "parking_lot_analytics", ParkingLotAnalyticsUseCase)
        registry.register_use_case("retail", "crowdflow", CrowdflowUseCase)
        registry.register_use_case("retail", "heatmaps", HeatMapsUseCase)
        registry.register_use_case("retail", "crowd_density_heatmaps", CrowdDensityHeatMapsUseCase)
        registry.register_use_case("general", "hazard_zone_entry", HazardZoneEntryUseCase)
        registry.register_use_case("general", "fence_climbing_detection", FenceClimbingDetectionUseCase)
        registry.register_use_case("general", "fence_climbing_detection_pose", FenceClimbingPoseGatedDetectionUseCase)
        registry.register_use_case("security", "fence_climbing_with_zone", FenceClimbingWithZoneUseCase)
        registry.register_use_case("traffic", "vehicle_monitoring_wrong_way", VehicleMonitoringWrongWayUseCase)
        registry.register_use_case("traffic", "stopped_vehicle_monitoring", StoppedVehicleMonitoringUseCase)
        registry.register_use_case("traffic", "illegal_parking_detection", IllegalParkingDetectionUseCase)
        registry.register_use_case("general", "area_utilization", AreaUtilizationUseCase)
        registry.register_use_case("general", "loitering_detection", LoiteringUseCase)
        registry.register_use_case("security", "tailgating_detection", TailgatingDetectionUseCase)
        registry.register_use_case("traffic", "vehicle_color_detection", VehicleColorDetectionUseCase)
        registry.register_use_case("traffic", "vehicle_segmentation", VehicleSegmentationUseCase)
        registry.register_use_case("traffic", "vehicle_type_classification", VehicleTypeClassificationUseCase)
        registry.register_use_case("general", "fall_detection", FallDetectionUseCase)
        registry.register_use_case("security", "running_detection", RunningDetectionUseCase)
        registry.register_use_case("security", "liquid_leak_detection", LiquidLeakDetectionUseCase)
        registry.register_use_case("security", "pipe_gas_leak_detection", PipeGasLeakDetectionUseCase)
        registry.register_use_case("general", "people_counting_in_zone", PeopleCountingInZoneUseCase)
        registry.register_use_case("security", "pipe_corrosion_detection", PipeCorrosionDetectionUseCase)
        registry.register_use_case("security", "overcrowding_detection", OvercrowdingDetectionUseCase)
        registry.register_use_case("general", "animal_detection", AnimalDetectionUseCase)
        registry.register_use_case("general", "unwanted_animal_detection", UnwantedAnimalDetectionUseCase)
        registry.register_use_case("security", "gloves_boots_detection", GlovesBootsDetectionUseCase)
        registry.register_use_case("security", "burglary_detection", BurglaryDetectionUseCase)
        registry.register_use_case("traffic", "accident_detection", AccidentDetectionUseCase)
        registry.register_use_case("environmental", "landslide_detection", LandslideDetectionUseCase)
        registry.register_use_case("environmental", "flood_detection", FloodDetectionUseCase)
        registry.register_use_case(
            "security",
            "unauthorized_encampment_detection",
            UnauthorizedEncampmentDetectionUseCase,
        )
        registry.register_use_case("aerial", "drone_detection", DroneDetectionUseCase)
        registry.register_use_case("general", "street_vendor_detection", StreetVendorDetectionUseCase)

        # Put all IMAGE based usecases here
        registry.register_use_case("healthcare", "bloodcancer_img_detection", BloodCancerDetectionUseCase)
        registry.register_use_case(
            "healthcare",
            "skincancer_img_classification",
            SkinCancerClassificationUseCase,
        )
        registry.register_use_case("healthcare", "plaque_img_segmentation", PlaqueSegmentationUseCase)
        registry.register_use_case("healthcare", "cardiomegaly_classification", CardiomegalyUseCase)
        registry.register_use_case(
            "healthcare",
            "histopathological_cancer_detection",
            HistopathologicalCancerDetectionUseCase,
        )
        registry.register_use_case("healthcare", "cell_microscopy_segmentation", CellMicroscopyUseCase)
        registry.register_use_case("industrial", "bottle_defect_detection", BottleDefectDetectionUseCase)
        registry.register_use_case(
            "industrial",
            "phone_screen_defect_detection",
            PhoneScreenDefectDetectionUseCase,
        )

        registry.register_use_case("manufacturing", "package_detection", PackageDetectionUseCase)

        registry.register_use_case("agriculture", "vegetable_detection", VegetableDetectionUseCase)

        logger.debug("Registered use cases with registry")

    def _generate_cache_key(self, config: BaseConfig, stream_key: str | None = None) -> str:
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
            "category": getattr(config, "category", "general"),
            "usecase": getattr(config, "usecase", "unknown"),
            "stream_key": stream_key or "default",
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
        return hashlib.md5(config_str.encode(), usedforsecurity=False).hexdigest()[:16]  # noqa: S324  # nosec B324  # nosemgrep: hashlib-md5-or-sha1

    async def _get_use_case_instance(self, config: BaseConfig, stream_key: str | None = None):
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
        tracking_usecases = {
            "people_counting",
            "people_tracking",
            "footfall",
            "crowdflow",
            "dwell",
            "vehicle_monitoring",
            "vehicle_tracking",
            "vehicle_counting",
        }
        usecase_name = getattr(config, "usecase", "unknown")
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

        if issubclass(use_case_class, FaceRecognitionEmbeddingUseCase):
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
        input_bytes: bytes | None,
        context: ProcessingContext,
        stream_info: Dict[str, Any] | None,
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
            LicensePlateAccessControlUseCase,
            LicensePlateSurveillanceUseCase,
            AgeGenderUseCase,
            PeopleTrackingUseCase,
            FaceRecognitionEmbeddingUseCase,
            VehicleColorDetectionUseCase,
        }

        # Async use cases
        async_use_cases = {FaceRecognitionEmbeddingUseCase, LicensePlateMonitorUseCase}

        # Determine the appropriate method signature and call
        use_case_type = type(use_case)

        if isinstance(use_case, FaceRecognitionEmbeddingUseCase):
            result = await use_case.process(data, config, input_bytes, context, stream_info)
        elif isinstance(use_case, LicensePlateMonitorUseCase):
            # isinstance, not `type(use_case) in async_use_cases`, so that LPR
            # profile subclasses (lpr_access_control / lpr_surveillance) dispatch
            # correctly. The identity check below matches the exact class only: a
            # subclass would miss both sets and fall through to the synchronous
            # branch, which calls this `async def` without awaiting it. Python
            # returns a coroutine, nothing runs, and no exception is raised -- the
            # use case would silently produce nothing. FR already avoids this via
            # the isinstance check above; LPR had no equivalent.
            result = await use_case.process(data, config, input_bytes, context, stream_info)
        elif use_case_type in async_use_cases:
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

    def _get_analytics_publisher(self) -> Any:
        """Lazy per-process Redis publisher for the new flow."""
        if self._analytics_publisher is None:
            from ..analytics.redis_publisher import AnalyticsRedisPublisher

            self._analytics_publisher = AnalyticsRedisPublisher(self._redis_config)
        return self._analytics_publisher

    def _publish_legacy_frame_analytics(
        self,
        config: Any,
        result: Any,
        stream_info: Dict[str, Any] | None,
        stream_key: str | None,
        context: ProcessingContext | None,
    ) -> None:
        """Publish ``results-agg`` (and incident fallback) for legacy incident apps."""
        usecase = getattr(config, "usecase", None)
        if not getattr(config, "enable_analytics", True):
            return
        try:
            from .utils.legacy_analytics_bridge import (
                legacy_redis_analytics_usecases,
                publish_legacy_frame_analytics,
            )
        except ImportError:
            return
        if usecase not in legacy_redis_analytics_usecases():
            return

        data = getattr(result, "data", None) or {}
        agg_summary = data.get("agg_summary") if isinstance(data, dict) else {}
        incident_data: Dict[str, Any] = {}
        if isinstance(agg_summary, dict) and agg_summary:
            frame_data = next(iter(agg_summary.values()), {})
            if isinstance(frame_data, dict):
                raw_incident = frame_data.get("incidents")
                if isinstance(raw_incident, dict):
                    incident_data = raw_incident

        incident_via_manager = False
        if context is not None:
            incident_via_manager = bool(context.metadata.get("incident_published_via_manager"))

        publish_legacy_frame_analytics(
            usecase=str(usecase),
            agg_summary=agg_summary,
            incident_data=incident_data,
            stream_info=stream_info,
            stream_key=stream_key or "default_stream",
            app_name=self.app_name,
            publisher=self._get_analytics_publisher(),
            incident_via_manager=incident_via_manager,
        )

    @staticmethod
    def _legacy_default_index_to_category_for_manifest(
        manifest_name: str | None,
    ) -> Dict[int, str] | None:
        """Fallback ``index_to_category`` from legacy use-case config dataclasses.

        Mirrors the car-damage fix: when deployment API omits ``index_to_category``
        but the manifest maps to a known legacy use case (``ppe_compliance``,
        ``car_damage_detection``), reuse the defaults from ``ppe_compliance.py`` /
        ``car_damage_detection.py``.
        """
        from ..analytics.engine_session import normalize_index_to_category

        if manifest_name == "ppe_compliance":
            from .usecases.ppe_compliance import PPEComplianceConfig

            return normalize_index_to_category(PPEComplianceConfig().index_to_category)
        if manifest_name == "car_damage_detection_new":
            from .usecases.car_damage_detection import CarDamageConfig

            return normalize_index_to_category(CarDamageConfig().index_to_category)
        return None

    def _index_to_category_from_usecase_config(
        self,
        config: Any,
    ) -> Dict[int, str] | None:
        """Build mapping via ``create_config(usecase, category)`` defaults."""
        if not isinstance(config, dict):
            return None
        usecase = config.get("usecase")
        if not usecase:
            return None
        category = config.get("category")
        try:
            kwargs = {k: v for k, v in config.items() if k not in _NON_USECASE_CONFIG_KEYS and v is not None}
            parsed = self.create_config(usecase, category, **kwargs)
            return self._extract_index_to_category_from_config(parsed)
        except Exception:
            return None

    @staticmethod
    def _extract_index_to_category_from_config(
        config: Any,
    ) -> Dict[int, str] | None:
        """Pull ``index_to_category`` from a dict or BaseConfig (incl. extra_params)."""
        from ..analytics.engine_session import normalize_index_to_category

        raw: Dict[Any, Any] | None = None
        if isinstance(config, dict):
            extra = config.get("extra_params") or {}
            if isinstance(extra, dict) and extra.get("index_to_category"):
                raw = extra.get("index_to_category")
            else:
                raw = config.get("index_to_category")
        elif isinstance(config, BaseConfig):
            extra = getattr(config, "extra_params", None) or {}
            if isinstance(extra, dict) and extra.get("index_to_category"):
                raw = extra.get("index_to_category")
            elif getattr(config, "index_to_category", None):
                raw = config.index_to_category
        if not raw:
            return None
        normalized = normalize_index_to_category(raw)
        return normalized or None

    def _select_index_to_category_mapping(
        self,
        candidates: list[Any],
        default_mapping: Dict[int, str] | None,
        *,
        reject_wrong_ppe: bool = False,
    ) -> Dict[int, str] | None:
        """Pick the first valid ``index_to_category`` from candidate configs."""
        from ..analytics.engine_session import (
            looks_like_coco_index_to_category,
            looks_like_wrong_ppe_index_to_category,
            normalize_index_to_category,
        )

        mapping: Dict[int, str] | None = None
        for cand in candidates:
            cand_mapping: Dict[int, str] | None = None
            if isinstance(cand, dict):
                cand_mapping = self._extract_index_to_category_from_config(cand)
                if not cand_mapping:
                    cand_mapping = self._index_to_category_from_usecase_config(cand)
            elif isinstance(cand, BaseConfig):
                cand_mapping = self._extract_index_to_category_from_config(cand)
            else:
                try:
                    parsed = self._parse_config(cand)
                    cand_mapping = self._extract_index_to_category_from_config(parsed)
                except Exception:
                    cand_mapping = None
            if not cand_mapping:
                continue
            if default_mapping:
                if reject_wrong_ppe and looks_like_wrong_ppe_index_to_category(cand_mapping):
                    logger.debug("Skipping wrong PPE index_to_category candidate: %s", cand_mapping)
                    continue
                if not reject_wrong_ppe and looks_like_coco_index_to_category(cand_mapping):
                    logger.debug("Skipping COCO-like index_to_category candidate")
                    continue
            mapping = cand_mapping
            break

        if not mapping:
            mapping = default_mapping
        return normalize_index_to_category(mapping) or None

    def _sanitize_ppe_index_to_category_on_config(self, config: BaseConfig | None) -> None:
        """Replace incomplete or COCO-like PPE maps with model defaults."""
        if config is None or getattr(config, "usecase", None) != "ppe_compliance":
            return
        from ..analytics.engine_session import looks_like_wrong_ppe_index_to_category, normalize_index_to_category
        from .usecases.ppe_compliance import PPEComplianceConfig

        default = normalize_index_to_category(PPEComplianceConfig().index_to_category)
        current = normalize_index_to_category(getattr(config, "index_to_category", None) or {})
        if not current or looks_like_wrong_ppe_index_to_category(current):
            config.index_to_category = default
            self.index_to_category = default
            logger.info("PPE legacy: using model index_to_category defaults: %s", default)

    def _ingest_legacy_index_to_category(
        self,
        config: Any = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> None:
        """Resolve ``index_to_category`` for legacy PPE (reject bad deployment maps)."""
        usecase = None
        if isinstance(config, BaseConfig):
            usecase = getattr(config, "usecase", None)
        elif isinstance(config, dict):
            usecase = config.get("usecase")
        if not usecase and self.post_processing_config:
            usecase = getattr(self.post_processing_config, "usecase", None)
        if not usecase and self.app_name:
            usecase = get_usecase_from_app_name(self.app_name)
        if usecase != "ppe_compliance":
            return

        from ..analytics.engine_session import normalize_index_to_category

        default = self._legacy_default_index_to_category_for_manifest("ppe_compliance")
        candidates: list[Any] = []
        if config is not None:
            candidates.append(config)
        if self._init_pp_config_dict:
            candidates.append(self._init_pp_config_dict)
        if self.post_processing_config:
            candidates.append(self.post_processing_config)
        if self.index_to_category:
            candidates.append({"index_to_category": self.index_to_category})
        if stream_info:
            api_cfg = self._resolve_config_from_stream(stream_info)
            if api_cfg:
                candidates.append(api_cfg)

        mapping = self._select_index_to_category_mapping(
            candidates,
            default,
            reject_wrong_ppe=True,
        )
        if not mapping:
            return
        if mapping == normalize_index_to_category(self.index_to_category or {}):
            return
        self.index_to_category = mapping
        logger.info("PPE legacy index_to_category loaded: %s", mapping)

    def _ingest_new_flow_mapping(
        self,
        config: Any = None,
        stream_info: Dict[str, Any] | None = None,
    ) -> None:
        """Apply uploaded/API/manifest ``index_to_category`` for new-flow apps.

        Uploaded JSON and init-time config take precedence over the deployment
        API (which may store UI defaults without ``index_to_category`` or with
        a generic COCO map). Manifest ``index_to_category`` is the last
        fallback before API.
        """
        from ..analytics.engine_session import normalize_index_to_category
        from ..analytics.flow import load_manifest_index_to_category

        candidates: list[Any] = []
        if config is not None:
            candidates.append(config)
        if self._init_pp_config_dict:
            candidates.append(self._init_pp_config_dict)
        if self.post_processing_config:
            candidates.append(self.post_processing_config)
        if self._new_flow_manifest:
            legacy_map = self._legacy_default_index_to_category_for_manifest(self._new_flow_manifest)
            if legacy_map:
                candidates.append({"index_to_category": legacy_map})
            manifest_map = load_manifest_index_to_category(self._new_flow_manifest)
            if manifest_map:
                candidates.append({"index_to_category": manifest_map})
        if stream_info:
            api_cfg = self._resolve_config_from_stream(stream_info)
            if api_cfg:
                candidates.append(api_cfg)

        manifest_default: Dict[int, str] | None = None
        if self._new_flow_manifest:
            manifest_default = self._legacy_default_index_to_category_for_manifest(self._new_flow_manifest)
            if not manifest_default:
                manifest_default = load_manifest_index_to_category(self._new_flow_manifest)

        reject_wrong_ppe = self._new_flow_manifest in (
            "ppe_compliance",
            "ppe_compliance_new",
            "ppe_detection_new",
        )
        mapping = self._select_index_to_category_mapping(
            candidates,
            manifest_default,
            reject_wrong_ppe=reject_wrong_ppe,
        )
        if not mapping:
            logger.warning(
                "New-flow app '%s' (manifest=%s): no index_to_category found",
                self.app_name,
                self._new_flow_manifest,
            )
            return
        if mapping == normalize_index_to_category(self.index_to_category or {}):
            return
        self.index_to_category = mapping
        for session in self._engine_sessions.values():
            session.index_to_category = mapping
        logger.info("New-flow index_to_category loaded: %s", mapping)

    def _process_new_flow(
        self,
        data: Any,
        stream_key: str | None,
        stream_info: Dict[str, Any] | None,
        start_time: float,
    ) -> ProcessingResult:
        """Dispatch one frame through the per-stream AnalyticsEngine session.

        Returns a ProcessingResult whose ``data['agg_summary']`` matches what
        callers extract from the legacy path (``to_dict()['data']['agg_summary']``).
        The per-frame agg_summary carries no count lists, so the legacy
        AnalyticsPublisher the pipeline still feeds skips it — results-agg comes
        only from the session's authoritative engine.aggregate().
        """
        key = stream_key or "default_stream"
        try:
            session = self._engine_sessions.get(key)
            if session is None:
                from ..analytics.engine_session import AnalyticsEngineSession

                session = AnalyticsEngineSession(
                    manifest_name=self._new_flow_manifest,
                    app_name=self.app_name,
                    index_to_category=self.index_to_category,
                    publisher=self._get_analytics_publisher(),
                    logger_=logger,
                )
                self._engine_sessions[key] = session

            if self.index_to_category:
                session.index_to_category = self.index_to_category

            raw_detections = data if isinstance(data, list) else (data or {}).get("detections", [])
            # Map once inside session.process(); output uses config/model labels.
            detection_copies = [dict(d) for d in (raw_detections or [])]
            enriched_stream_info = self._enrich_stream_info_camera_metadata(stream_info)
            agg_summary = session.process(detection_copies, enriched_stream_info, stream_key=key)

            if isinstance(data, dict):
                result_data: Any = dict(data)
                result_data["detections"] = detection_copies
                result_data["agg_summary"] = agg_summary
            else:
                result_data = {
                    "agg_summary": agg_summary,
                    "detections": detection_copies,
                }

            result = ProcessingResult(
                data=result_data,
                status=ProcessingStatus.SUCCESS,
                usecase=self._new_flow_manifest,
                category="analytics_engine",
            )
        except Exception as e:
            logger.error("New-flow processing failed: %s", e, exc_info=True)
            result = self._create_error_result(str(e), type(e).__name__)
        result.processing_time = time.monotonic() - start_time
        self._update_statistics(result)
        return result

    # ------------------------------------------------------------------
    # The analytics engine seam
    # ------------------------------------------------------------------

    def _resolve_engine_backend(self, config: Any) -> Any:
        """The analytics engine for this app, or ``None`` for the legacy path. Decided once.

        Kept deliberately small and total: any failure resolving it is a legacy decision, because
        an app that runs today must keep running whatever happens here.

        The **one** exception is a configured app bundle that will not load. That app's analytics
        exist only in the bundle, so a legacy run would emit zeros rather than nothing — which is
        worse, because zeros look like a working deployment. It is recorded and surfaced as an error
        result instead; see ``_engine_backend_error``.
        """
        if getattr(self, "_engine_backend_checked", False):
            return self._engine_backend
        self._engine_backend_checked = True
        self._engine_backend = None
        self._engine_backend_error = None
        try:
            from ..engine.routing import RoutingError
            from ..runtime.backends import BackendError, select_engine_backend
        except Exception:
            logger.debug("PostProcessor: engine routing unavailable; staying on legacy", exc_info=True)
            return None

        try:
            self._engine_backend = select_engine_backend(
                self.app_name or _usecase_of(config) or _usecase_of(self.post_processing_config),
                redis_config=self._redis_config,
                app_name=self.app_name,
                post_processing_config=self.post_processing_config,
                # The parsed config is what `EngineBackend` reads, and it drops keys `create_config`
                # does not know -- including an app-bundle reference. The raw dict is kept precisely
                # so nothing is lost, so hand it over too: without it this entry point would see no
                # bundle where `PostProcRunner`, which passes its dict directly, sees one.
                identity=self._init_pp_config_dict,
            )
        except RoutingError as exc:
            # Reachable only under MATRICE_ANALYTICS_FLOW=new, and it must be LOUD there. That flag
            # is an operator saying "require the engine", and answering it with a silent legacy run
            # is the exact failure the engine exists to remove -- `routing.RoutingError`'s own
            # docstring says so. Until this branch existed, RoutingError fell into the broad
            # `except Exception` below, logged at DEBUG, and returned None: the flag was a no-op on
            # this entry point while working correctly on `PostProcRunner`, so an operator could set
            # it, see a legacy run, and have nothing in the log to explain why.
            self._engine_backend_error = f"routing refused this app under MATRICE_ANALYTICS_FLOW=new: {exc}"
            logger.error("PostProcessor: %s", self._engine_backend_error)
        except BackendError as exc:
            self._engine_backend_error = str(exc)
            logger.error("PostProcessor: %s", exc)
        except Exception:
            logger.debug("PostProcessor: engine routing unavailable; staying on legacy", exc_info=True)
        return self._engine_backend

    def _engine_failure_cameras(self) -> set:
        """Cameras whose per-frame engine failure has already been reported at ERROR.

        Lazily attached rather than set in ``__init__``, matching how ``_engine_backend_checked``
        is handled a few lines below. Bounded by the camera count of one deployment.
        """
        cameras = getattr(self, "_engine_failure_cameras_set", None)
        if cameras is None:
            cameras = set()
            self._engine_failure_cameras_set = cameras
        return cameras

    def _require_engine_ready_once(
        self,
        engine: Any,
        camera_id: str,
        stream_info: Dict[str, Any] | None,
        input_bytes: bytes | None,
        detections: Any,
    ) -> None:
        """Refuse-early diagnostics for the engine path, **per camera**, at most once each.

        ``PostProcRunner`` runs this check in ``_check_stream``; this entry point had none at all,
        so a node with an unusable ``stream_info`` produced only symptoms -- empty ``agg_summary``
        on every frame, indistinguishable from a quiet camera -- and never the one line that names
        the missing field and the fix.

        Two things differ from the runner, both because of how this class is used:

        * **Per camera, not once.** A ``PostProcRunner`` is per worker thread and therefore serves
          one camera; ``py_inference``'s node builds **one** ``PostProcessor`` and passes every
          camera through it. A single global check would validate whichever camera arrived first
          and wave the rest through, which is worse than no check because it reads as coverage.
        * **It never disables the backend.** The runner sets ``self._backend = None`` on failure,
          which is right when the backend serves one stream. Here it is shared, so one camera's
          missing geometry would take every other camera on the node down with it. This logs and
          gets out of the way; the frame then fails on its own merits.

        A frame that resolves no dimensions **and** carries no detections cannot settle the
        question -- ``_boxes_look_normalised`` is trivially true for an empty list -- so it does not
        consume the check, exactly as in the runner (INF-2606).
        """
        checked = getattr(self, "_engine_ready_cameras", None)
        if checked is None:
            checked = set()
            self._engine_ready_cameras = checked
        if camera_id in checked:
            return

        try:
            from ..runtime.backends import BackendError, require_engine_ready, resolve_source_dims

            enriched = engine.enrich(stream_info or {}, input_bytes=input_bytes)
            if resolve_source_dims(enriched, input_bytes) is None and not detections:
                logger.debug(
                    "PostProcessor: readiness check deferred for camera %s -- this frame has no "
                    "detections and no resolvable dimensions, so it cannot decide either way",
                    camera_id,
                )
                return

            checked.add(camera_id)
            try:
                require_engine_ready(
                    enriched,
                    engine.app_id,
                    input_bytes=input_bytes,
                    detections=detections,
                    manifest=getattr(engine, "manifest", None),
                )
            except BackendError as exc:
                logger.error("PostProcessor: camera %s -- %s", camera_id, exc)
                if getattr(exc, "retryable", False):
                    # Geometry can appear without a restart, so this camera must be re-checked.
                    # Leaving it in `checked` would pin the diagnosis to the one frame that saw
                    # the zone missing -- the decoupled node has no `_deferred_cameras`, so
                    # simply not consuming the check is how it re-asks.
                    checked.discard(camera_id)
        except Exception:  # noqa: BLE001 - diagnostics must never break the frame loop
            checked.add(camera_id)
            logger.debug(
                "PostProcessor: engine readiness check unavailable for camera %s",
                camera_id,
                exc_info=True,
            )

    async def _process_on_engine(
        self,
        engine: Any,
        data: Any,
        stream_key: str | None,
        stream_info: Dict[str, Any] | None,
        input_bytes: bytes | None,
        start_time: float,
    ) -> ProcessingResult:
        """One frame through the engine, returned in the shape every caller already reads.

        The legacy path below is skipped in its entirety -- including
        ``_publish_legacy_frame_analytics`` -- so ``results-agg`` and ``incident_res`` are
        published once, by the engine's own publisher, and never twice.

        **No ``input_bytes`` reaches here from the decoupled analytics node.** ``process_simple``
        has no such parameter, so ``py_inference``'s node always arrives with ``None`` -- which
        means ``resolve_source_dims``' three-way search collapses to one: only
        ``stream_info["stream_resolution"]`` can supply the frame size, where the ml-codebases
        workers additionally hand over the frame as a JPEG or an image array. Anything relying on
        that fallback works in the coupled flow and silently does not here.
        """
        camera_id = stream_key or "default_stream"
        self._require_engine_ready_once(engine, camera_id, stream_info, input_bytes, data)
        try:
            out = await engine.process(
                detections=data,
                camera_id=camera_id,
                stream_info=stream_info or {},
                input_bytes=input_bytes,
                config=None,
                frame_ts=None,
            )
        except Exception as exc:
            # ERROR once per camera, DEBUG thereafter. Logging every frame -- what this did until
            # INF-2606 -- buries the first, most informative failure under thousands of identical
            # lines, and a camera failing at 30fps writes 30 ERRORs a second for as long as the
            # container runs. The mirror of the runner's old bug, which was DEBUG for every frame:
            # one was too quiet, this was too loud, and both hide the signal.
            reported = self._engine_failure_cameras()
            if camera_id not in reported:
                reported.add(camera_id)
                logger.error(
                    "PostProcessor: analytics engine failed for camera %s: %s "
                    "(first occurrence for this camera; further ones log at DEBUG)",
                    camera_id,
                    exc,
                    exc_info=True,
                )
            else:
                logger.debug("PostProcessor: analytics engine failed for camera %s: %s", camera_id, exc)
            result = ProcessingResult(data={}, usecase=engine.app_id)
            result.set_error(str(exc), error_type=type(exc).__name__)
            result.processing_time = time.monotonic() - start_time
            return result

        payload = (out or {}).get("result") or {}
        return ProcessingResult(
            data={"agg_summary": (out or {}).get("agg_summary") or {}},
            usecase=payload.get("usecase", engine.app_id),
            category=payload.get("category", ""),
            processing_time=time.monotonic() - start_time,
            metrics=payload.get("metrics") or {},
        )

    async def process(
        self,
        data: Any,
        config: Union[BaseConfig, Dict[str, Any], str, Path] = {},
        input_bytes: bytes | None = None,
        stream_key: str | None = "default_stream",
        stream_info: Dict[str, Any] | None = None,
        context: ProcessingContext | None = None,
        custom_post_processing_config: Union[Dict[str, Any], BaseConfig, str] | None = None,
    ) -> ProcessingResult:
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
        start_time = time.monotonic()

        # Before any routing: recover the frame resolution from the payload itself when the
        # caller did not send one. Both flows need it and neither could find it -- the legacy
        # zone helpers (`geometry_utils.resolve_frame_dims`) and the engine's `StreamInfo` both
        # read `stream_info["stream_resolution"]`, and the CUDA-SHM worker path reaches here
        # without ever calling `build_stream_info(source_dims=...)`. py_inference has stamped
        # the answer onto the data dict the whole time (`coordinate_frame.reference_size`).
        # Doing it once, here, fixes every legacy use case at the same moment as the engine.
        stream_info = _backfill_stream_resolution(data, stream_info)

        # Manifest apps run on the analytics engine. This is the same decision
        # `PostProcRunner` makes -- both entry points share `select_engine_backend`,
        # because py_inference's analytics node reaches this method directly
        # (pipeline_message_processor -> process_simple -> here) and never touches
        # the runner. An app with no manifest gets `None` and falls through to
        # byte-identical code below; today that is every production app.
        engine = self._resolve_engine_backend(config)
        if engine is not None:
            # The engine path was the one route that skipped this, which is why engine apps
            # published a raw ObjectID as the camera name: py_inference deletes `camera_info`
            # (pipeline_message_processor.py:780) on the stated assumption that "camera_name is
            # owned by the PostProcessor's config-API enrichment" -- true for the legacy route
            # below and for `_process_new_flow`, both of which call this, and false here.
            # Cost is one API fetch per camera per process: the helper caches by camera_id and
            # caches negatives too, so a camera that does not resolve is not retried per frame.
            stream_info = self._enrich_stream_info_camera_metadata(stream_info)
            return await self._process_on_engine(engine, data, stream_key, stream_info, input_bytes, start_time)
        if getattr(self, "_engine_backend_error", None):
            # A bundle was named and could not be loaded. Returning an ERROR result rather than
            # running legacy keeps the failure visible: the caller does not raise, but nor does it
            # get a frame of plausible zeros that reads as success.
            return self._create_error_result(self._engine_backend_error, "AppBundleError")

        # New analytics flow: route eligible apps to the per-stream
        # AnalyticsEngine session (tracking + incident_res/results-agg
        # publishing all happen inside the SDK). Legacy apps fall through
        # to the use-case path below, unchanged.
        if self._new_flow_manifest:
            self._ingest_new_flow_mapping(config, stream_info)
            return self._process_new_flow(data, stream_key, stream_info, start_time)

        self._ingest_legacy_index_to_category(config, stream_info)

        logger.info("PostProcessor.process started")
        logger.info("PostProcessor: incoming parameters received")
        # Avoid logging config objects or tainted-derived strings (CodeQL clear-text rules).
        logger.debug(
            "Config flags: has_inline=%s has_default_pp=%s has_custom_pp=%s",
            bool(config),
            self.post_processing_config is not None,
            custom_post_processing_config is not None,
        )
        logger.debug(
            "Stream flags: has_stream_key=%s has_stream_info=%s",
            stream_key is not None,
            stream_info is not None,
        )

        try:
            # Uploaded config from pipeline is passed as config; parse and use it (overrides default)
            if config:
                try:
                    config = self._parse_config(config)
                    logger.info("PostProcessor: configuration from input parsed")
                    logger.debug("Inline config parsed to BaseConfig successfully")
                except Exception as e:
                    logger.error("Failed to parse config: %s", e, exc_info=True)
                    raise ValueError(f"Failed to parse config: {e}")

            parsed_config = self._resolve_parsed_config(config, stream_info)
            self._sanitize_ppe_index_to_category_on_config(parsed_config)

            if not parsed_config:
                logger.info("PostProcessor: no valid configuration after resolution")
                logger.debug(
                    "No valid configuration found | has_inline=%s | has_default_pp=%s | has_stream_info=%s",
                    bool(config),
                    self.post_processing_config is not None,
                    stream_info is not None,
                )
                raise ValueError("No valid configuration found")

            # Get cached use case instance (await since it's async now)
            use_case = await self._get_use_case_instance(parsed_config, stream_key)

            # Create context if not provided
            if context is None:
                context = ProcessingContext()

            # Ensure stream_key is available in stream_info for tracker namespacing
            if stream_info is None:
                stream_info = {}
            if stream_key and "stream_key" not in stream_info:
                stream_info["stream_key"] = stream_key

            stream_info = self._enrich_stream_info_camera_metadata(stream_info)

            # Process with use case using dispatch pattern
            result = await self._dispatch_use_case_processing(
                use_case, data, parsed_config, input_bytes, context, stream_info
            )

            # Legacy Redis analytics (incident_res fallback + results-agg ~60s)
            if not self._new_flow_manifest:
                self._publish_legacy_frame_analytics(
                    parsed_config,
                    result,
                    stream_info,
                    stream_key,
                    context,
                )

            # Add processing time
            result.processing_time = time.monotonic() - start_time

            # Update statistics
            self._update_statistics(result)

            return result

        except Exception as e:
            processing_time = time.monotonic() - start_time
            logger.error(f"Processing failed: {str(e)}", exc_info=True)

            error_result = self._create_error_result(str(e), type(e).__name__, context=context)
            error_result.processing_time = processing_time

            # Update statistics
            self._update_statistics(error_result)

            return error_result

    async def process_simple(
        self,
        data: Any,
        usecase: str,
        category: str | None = None,
        context: ProcessingContext | None = None,
        stream_key: str | None = None,
        stream_info: Dict[str, Any] | None = None,
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
                elif usecase == "violence_detection":
                    category = "security"
                elif usecase == "violence_detection_testing":
                    category = "security"
                elif usecase == "ppe_compliance":
                    category = "ppe"
                elif usecase == "weapon_human_detection":
                    category = "security"
                else:
                    category = "general"  # Default fallback

            # A manifest app must not pay for a legacy config it will never read.
            #
            # `create_config` maps **config_params onto a legacy dataclass, and the params are the
            # deployment's post_processing_config -- which for an engine app is authored against
            # app.yaml, not against that dataclass. A key it has no field for is a TypeError that
            # kills the frame HERE, one line before dispatch, so the engine is never reached and
            # nothing diagnoses why: `DwellConfig.__init__() got an unexpected keyword argument
            # 'method'` on a dwell/loitering deployment carrying a line_crossing `method`.
            #
            # Not a dwell bug -- `create_config` does this for every usecase, so any engine-authored
            # key absent from the matching legacy dataclass fails identically. `method` was simply
            # the first one a live deployment happened to carry.
            #
            # `_process_on_engine` already passes `config=None` on the grounds that "a manifest app
            # takes its configuration from app.yaml … a per-frame override has no meaning here", so
            # for the engine this object is built, risks throwing, and is then discarded. This is
            # also why `PostProcRunner` never hit it: that entry point does not call `create_config`
            # at all, which is what made the coupled ml-codebases flow immune while the decoupled
            # analytics node broke.
            #
            # Legacy apps are untouched -- byte-for-byte the same config, including the same
            # TypeError for a genuinely wrong key. Deliberately NOT making `create_config` tolerate
            # unknown kwargs: that would silence real config typos across ~140 use cases, trading a
            # loud failure for a silent one.
            if self._resolve_engine_backend({"usecase": usecase}) is not None:
                return await self.process(
                    data,
                    {},
                    context=context,
                    stream_key=stream_key,
                    stream_info=stream_info,
                )

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
            return self._create_error_result(str(e), type(e).__name__, usecase, category or "general", context)

    async def process_from_file(
        self,
        data: Any,
        config_file: Union[str, Path],
        context: ProcessingContext | None = None,
        stream_key: str | None = None,
        stream_info: Dict[str, Any] | None = None,
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

    def close(self) -> None:
        """Release what this processor holds, flushing the engine's open windows first.

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
        backend = getattr(self, "_engine_backend", None)
        if backend is None:
            return
        self._engine_backend = None
        try:
            backend.close()
        except Exception:  # pragma: no cover - defensive; close must not raise on the way out
            logger.warning("PostProcessor: engine backend close failed", exc_info=True)

    def create_config(self, usecase: str, category: str = "general", **kwargs) -> BaseConfig:
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
        remaining = dict(kwargs)
        dropped: List[str] = []

        # One key is named per TypeError, so bound the loop by the number of keys there are.
        for _ in range(len(remaining) + 1):
            try:
                config = config_manager.create_config(usecase, category=category, **remaining)
            except TypeError as exc:
                key = _unexpected_kwarg(str(exc))
                if key is None or key not in remaining:
                    # Not an unknown-kwarg TypeError, or it names something we did not pass --
                    # a real error, so let it out untouched.
                    raise
                remaining.pop(key)
                dropped.append(key)
                continue

            if dropped:
                logger.warning(
                    "PostProcessor: usecase %r -- dropped %d config key(s) the legacy config class "
                    "does not declare: %s. These are almost certainly authored for the analytics "
                    "engine (app.yaml), which takes its configuration from the manifest rather than "
                    "from here. The app is running WITHOUT them; if one of them was meant for the "
                    "legacy use case, it is being ignored.",
                    usecase,
                    len(dropped),
                    ", ".join(sorted(dropped)),
                )
            return config

        # Unreachable: the loop bound exceeds the key count, and each pass removes one key.
        raise RuntimeError(  # pragma: no cover - defensive
            f"create_config({usecase!r}) could not resolve its keyword arguments after "
            f"{len(kwargs)} attempts; dropped so far: {', '.join(sorted(dropped))}"
        )

    def load_config(self, file_path: Union[str, Path]) -> BaseConfig:
        """Load configuration from file."""
        return config_manager.load_from_file(file_path)

    def save_config(self, config: BaseConfig, file_path: Union[str, Path], fmt: str = "json") -> None:
        """Save configuration to file."""
        config_manager.save_to_file(config, file_path, fmt)

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
                usecase = config.get("usecase")
                if not usecase:
                    return ["Configuration must specify 'usecase'"]

                category = config.get("category")
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
            "total_processing_time": 0.0,
        }

    def _parse_config(  # TODO: remove all of the kwargs that are not in the use case config
        self, config: Union[BaseConfig, Dict[str, Any], str, Path]
    ) -> BaseConfig:
        """Parse configuration from various input formats."""
        if isinstance(config, BaseConfig):
            return config
        elif isinstance(config, dict):
            usecase = config.get("usecase")
            if not usecase:
                raise ValueError("Configuration dict must contain 'usecase' key")

            category = config.get("category")
            # Avoid duplicate keyword args (same as load_from_file)
            data_copy = config.copy()
            data_copy.pop("usecase", None)
            data_copy.pop("category", None)
            return config_manager.create_config(usecase, category=category, **data_copy)
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
        context: ProcessingContext | None = None,
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
            "application_name": (f"{usecase.title()} Processing" if usecase else "Post Processing"),
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
async def process_simple(data: Any, usecase: str, category: str | None = None, **config) -> ProcessingResult:
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
