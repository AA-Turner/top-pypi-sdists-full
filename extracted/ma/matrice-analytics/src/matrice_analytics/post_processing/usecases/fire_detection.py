"""
Fire and Smoke Detection use case implementation.

This module provides a structured implementation of fire and smoke detection
with counting, insights generation, alerting, and tracking.
"""
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import time
import re
from collections import Counter

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)
from ..core.config import BaseConfig, AlertConfig
from ..utils import (
    filter_by_confidence,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
    bbox_smoothing,
    BBoxSmoothingConfig,
    BBoxSmoothingTracker
)
# Import incident manager for publishing incidents on level change
from ..utils.incident_manager_utils import INCIDENT_MANAGER, IncidentManagerFactory


# ======================
# Config Definition
# ======================



@dataclass
class FireSmokeConfig(BaseConfig):
    confidence_threshold: float = 0.85

    # Only fire and smoke categories included here (exclude normal)
    fire_smoke_categories: List[str] = field(
        default_factory=lambda: ["fire", "smoke"]
    )
    target_categories: List[str] = field(
        default_factory=lambda: ['fire']
    )

    alert_config: Optional[AlertConfig] = field(
        default_factory=lambda: AlertConfig(
            count_thresholds={"fire": 0},
            alert_type=["email"],
            alert_value=["FIRE_INFO@matrice.ai"],
            alert_incident_category=["FIRE-ALERT"]
        )
    )
    

    time_window_minutes: int = 60
    enable_unique_counting: bool = True

    # Map only fire and smoke; ignore normal (index 1 not included)
    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {
            0: "fire",
            1: "smoke",
        }
    )

    #  BBox smoothing configuration (added)
    enable_smoothing: bool = False
    smoothing_algorithm: str = "linear"
    smoothing_window_size: int = 5
    smoothing_cooldown_frames: int = 10
    smoothing_confidence_range_factor: float = 0.2
    threshold_area: Optional[float] = 250200.0
    
    # Session and server configuration for incident manager
    session: Optional[Any] = None  # Matrice session for Redis/Kafka initialization
    server_id: Optional[str] = None  # Server ID for localhost/cloud detection

    def __post_init__(self):
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ValueError("confidence_threshold must be between 0.0 and 1.0")

        # Normalize category names to lowercase for consistent matching
        self.fire_smoke_categories = [cat.lower() for cat in self.fire_smoke_categories]
        if self.index_to_category:
            self.index_to_category = {k: v.lower() for k, v in self.index_to_category.items()}
        if self.target_categories:
                self.target_categories = [cat.lower() for cat in self.target_categories]



# ======================

# ======================
class FireSmokeUseCase(BaseProcessor):
    def __init__(self):
        super().__init__("fire_smoke_detection")
        self.category = "hazard"
        self.CASE_TYPE: Optional[str] = 'fire_smoke_detection'
        self.CASE_VERSION: Optional[str] = '1.3'

        self.smoothing_tracker = None  # Required for bbox smoothing
        self._fire_smoke_recent_history = []
        self.target_categories=['fire', 'smoke']  # Lowercase to match filtering logic at line 276

        # Tracker initialization (for frame-wise tracking)
        self.tracker = None
        self._total_frame_counter = 0
        
        # Per-category track ID tracking
        self._per_category_total_track_ids: Dict[str, set] = {}
        self._current_frame_track_ids: Dict[str, set] = {}
        self._previous_frame_track_ids: Dict[str, set] = {}
        self._new_track_ids_this_frame: Dict[str, set] = {}

        self._ascending_alert_list: List[str] = []
        self.current_incident_end_timestamp: str = "N/A"
        self.id_hit_list = ["low","medium","significant","critical","low"]
        self.id_hit_counter = 0
        self.latest_stack:str = None
        self.id_timing_list = []
        self.return_id_counter = 1
        self.start_timer = None
        self._tracking_start_time = None
        
        # Incident manager for publishing incidents on severity level change
        self._incident_manager_factory: Optional[IncidentManagerFactory] = None
        self._incident_manager: Optional[INCIDENT_MANAGER] = None
        self._incident_manager_initialized: bool = False

    def _initialize_incident_manager_once(self, config: FireSmokeConfig) -> None:
        """
        Initialize incident manager ONCE with Redis OR Kafka clients (Environment based).
        Called from process() on first invocation.
        Uses config.session (existing session from pipeline) or creates from environment.
        """
        if self._incident_manager_initialized:
            return
        
        try:
            self.logger.info("[INCIDENT_MANAGER] Starting incident manager initialization for fire detection...")
            
            # Create factory if not exists
            if self._incident_manager_factory is None:
                self._incident_manager_factory = IncidentManagerFactory(logger=self.logger)
            
            # Initialize using factory (handles session creation, Redis/Kafka setup)
            self._incident_manager = self._incident_manager_factory.initialize(config)
            
            if self._incident_manager:
                self.logger.info("[INCIDENT_MANAGER] ✓ Incident manager initialized successfully for fire detection")
            else:
                self.logger.warning("[INCIDENT_MANAGER] Incident manager not available, incidents won't be published")
        
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Incident manager initialization failed: {e}", exc_info=True)
        finally:
            self._incident_manager_initialized = True  # Mark as initialized (don't retry every frame)

    def _send_incident_to_manager(
        self, 
        incident: Dict, 
        stream_info: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Send incident to incident manager for level tracking and publishing.
        
        The incident manager will:
        1. Track the severity level
        2. Wait for consecutive frames before publishing:
           - 5 frames for medium/significant/critical
           - 10 frames for low (stricter to avoid false positives)
        3. Publish only when level changes
        4. Send 'info' level after 101 consecutive empty frames (incident ended)
        
        Args:
            incident: Incident dictionary from _generate_incidents
            stream_info: Stream metadata containing camera info
        """
        if not self._incident_manager:
            self.logger.debug("[INCIDENT_MANAGER] No incident manager available, skipping")
            return
        
        # Extract camera_id from stream_info
        # Priority: camera_info.camera_id > stream_info.camera_id > extract from topic
        camera_id = ""
        if stream_info:
            camera_info = stream_info.get("camera_info", {}) or {}
            camera_id = camera_info.get("camera_id", "") or camera_info.get("cameraId", "")
            
            if not camera_id:
                camera_id = stream_info.get("camera_id", "") or stream_info.get("cameraId", "")
            
            # Extract camera_id from topic if not found elsewhere
            # Topic format: {camera_id}_input_topic
            if not camera_id:
                topic = stream_info.get("topic", "")
                if topic:
                    if topic.endswith("_input_topic"):
                        camera_id = topic[: -len("_input_topic")]
                        self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic (underscore): {camera_id}")
                    elif topic.endswith("_input-topic"):
                        camera_id = topic[: -len("_input-topic")]
                        self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic (hyphen): {camera_id}")
                    else:
                        # Fallback: split on known markers if not strictly at the end
                        if "_input_topic" in topic:
                            camera_id = topic.split("_input_topic")[0]
                            self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic split (underscore): {camera_id}")
                        elif "_input-topic" in topic:
                            camera_id = topic.split("_input-topic")[0]
                            self.logger.debug(f"[INCIDENT_MANAGER] Extracted camera_id from topic split (hyphen): {camera_id}")
        
        if not camera_id:
            # Fallback to a default identifier
            camera_id = "default_camera"
            self.logger.debug(f"[INCIDENT_MANAGER] No camera_id found, using default: {camera_id}")
        else:
            self.logger.debug(f"[INCIDENT_MANAGER] Using camera_id: {camera_id}")
        
        try:
            # Process the incident through the manager
            published = self._incident_manager.process_incident(
                camera_id=camera_id,
                incident_data=incident,
                stream_info=stream_info
            )
            
            if published:
                self.logger.info(f"[INCIDENT_MANAGER] Incident published for camera: {camera_id}")
        except Exception as e:
            self.logger.error(f"[INCIDENT_MANAGER] Error sending incident to manager: {e}", exc_info=True)

    def process(
            self,
            data: Any,
            config: ConfigProtocol,
            context: Optional[ProcessingContext] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> ProcessingResult:
        """
        Process fire and smoke detection use case.
        """
        start_time = time.time()

        try:
            # Step 0: Validate config
            if not isinstance(config, FireSmokeConfig):
                return self.create_error_result(
                    "Invalid configuration type for fire and smoke detection",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

            # Step 0.5: Initialize incident manager once (for publishing incidents on level change)
            if not self._incident_manager_initialized:
                self._initialize_incident_manager_once(config)

            # Step 1: Init context
            if context is None:
                context = ProcessingContext()
            input_format = match_results_structure(data)
            context.input_format = input_format
            context.confidence_threshold = config.confidence_threshold
            self.logger.info(f"Processing fire and smoke detection with format: {input_format.value} with threshold: {config.confidence_threshold}")

            # Step 2: Confidence thresholding
            processed_data = data
            if config.confidence_threshold is not None:
                processed_data = filter_by_confidence(processed_data, config.confidence_threshold)
                self.logger.debug(f"Applied confidence filtering with threshold {config.confidence_threshold}")

            # Step 3: Category mapping
            if config.index_to_category:
                processed_data = apply_category_mapping(processed_data, config.index_to_category)
                self.logger.debug("Applied category mapping")

            if self.target_categories:
                processed_data = [d for d in processed_data if d.get('category').lower() in self.target_categories]
                self.logger.debug(f"Applied category filtering")

            # Step 3.5: BBox smoothing for fire/smoke
            if config.enable_smoothing:
                if self.smoothing_tracker is None:
                    smoothing_config = BBoxSmoothingConfig(
                        smoothing_algorithm=config.smoothing_algorithm,
                        window_size=config.smoothing_window_size,
                        cooldown_frames=config.smoothing_cooldown_frames,
                        confidence_threshold=config.confidence_threshold,
                        confidence_range_factor=config.smoothing_confidence_range_factor,
                        enable_smoothing=True
                    )
                    self.smoothing_tracker = BBoxSmoothingTracker(smoothing_config)

                smooth_categories = {"fire", "smoke"}
                fire_smoke_detections = [d for d in processed_data if d.get("category", "").lower() in smooth_categories]

                smoothed_detections = bbox_smoothing(
                    fire_smoke_detections,
                    self.smoothing_tracker.config,
                    self.smoothing_tracker
                )
                non_smoothed_detections = [d for d in processed_data if d.get("category", "").lower() not in smooth_categories]

                processed_data = non_smoothed_detections + smoothed_detections
                self.logger.debug("Applied bbox smoothing for fire/smoke categories")

            # Step 4: Summarization
            fire_smoke_summary = self._calculate_fire_smoke_summary(processed_data, config)
            general_summary = calculate_counting_summary(processed_data)

            # Step 5: Predictions
            predictions = self._extract_predictions(processed_data, config)

            # Step 6: Frame number extraction
            frame_number = None
            if stream_info:
                input_settings = stream_info.get("input_settings", {})
                start_frame = input_settings.get("start_frame")
                end_frame = input_settings.get("end_frame")
                if start_frame is not None and end_frame is not None and start_frame == end_frame:
                    frame_number = start_frame
                elif start_frame is not None:
                    frame_number = start_frame

             # Step 7: alerts
            # Ensure we have an AlertConfig object. `dataclasses.field` is only
            # meant for class-level default declarations – using it at runtime
            # produces a `Field` object which later breaks JSON serialization.
            if config.alert_config is None:
                config.alert_config = AlertConfig(
                    count_thresholds={"fire": 0},
                    alert_type=["email"],
                    alert_value=["FIRE_INFO@matrice.ai"],
                    alert_incident_category=["FIRE-ALERT"]
                )

            alerts = self._check_alerts(fire_smoke_summary, frame_number, config, stream_info)


            # Step 8: Incidents and tracking stats
            incidents_list = self._generate_incidents(fire_smoke_summary, alerts, config, frame_number=frame_number, stream_info=stream_info)
            tracking_stats_list = self._generate_tracking_stats(
                fire_smoke_summary, alerts, config,
                frame_number=frame_number,
                stream_info=stream_info
            )
            business_analytics_list = self._generate_business_analytics(fire_smoke_summary, alerts, config, stream_info, is_empty=True)
            
            # Step 8.5: Send incident to incident manager for level tracking and publishing
            # The incident manager handles:
            # - 5-consecutive-frame validation
            # - Publishing only on level change
            # - Skipping "low" level incidents
            incidents = incidents_list[0] if incidents_list else {}
            self._send_incident_to_manager(incidents, stream_info)
            # if incidents_list and len(incidents_list) > 0:
            #     incident = incidents_list[0]
            #     if incident and incident != {}:
            #         self._send_incident_to_manager(incident, stream_info)

             # Step 9: Human-readable summary
            summary_list = self._generate_summary(fire_smoke_summary, general_summary, incidents_list, tracking_stats_list, business_analytics_list, alerts)

            # Finalize context and return result
            context.processing_time = time.time() - start_time

            
            tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
            #EVENT ENDED SIGNAL

            if len(tracking_stats_list)>1:
                alerts = tracking_stats_list[1]
                incidents = tracking_stats_list[2]
                tracking_stats = tracking_stats_list[0]


            business_analytics = business_analytics_list[0] if business_analytics_list else []
            summary = summary_list[0] if summary_list else {}
            agg_summary = {str(frame_number): {
                            "incidents": incidents,
                            "tracking_stats": tracking_stats,
                            "business_analytics": business_analytics,
                            "alerts": alerts,
                            "human_text": summary}
                          }
       
            context.mark_completed()

            result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context)
            return result


        except Exception as e:
            self.logger.error(f"Error in fire and smoke processing: {str(e)}")
            return self.create_error_result(
                f"Fire and smoke processing failed: {str(e)}",
                error_type="FireSmokeProcessingError",
                usecase=self.name,
                category=self.category,
                context=context,
            )

    # ==== Internal Utilities ====
    def _check_alerts(
            self, summary: Dict, frame_number:Any, config: FireSmokeConfig, stream_info: Optional[Dict[str, Any]] = None
    ) -> List[Dict]:
        """Raise alerts if fire or smoke detected with severity based on intensity."""
        def get_trend(data, lookback=23, prior=14):
            '''
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with determining dominant levels.
            '''
            if len(data) < lookback:
                return True
            post=lookback-prior-1
            levels_list = ["low","medium","significant","critical","low"]

            current_dominant_incident = Counter(data[-lookback:][:-prior]).most_common(1)[0][0] #from LAST 23 elements fetch FIRST 15 elements
            potential_dominant_incident = Counter(data[-post:]).most_common(1)[0][0] #fetch LAST 8 elements
            current_dominant_incident_index = levels_list.index(current_dominant_incident)
            potential_dominant_incident_index = levels_list.index(potential_dominant_incident)

            if current_dominant_incident_index <= potential_dominant_incident_index:
                return True
            else:
                return False

        alerts = []
        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])
        frame_key = str(frame_number) if frame_number is not None else "current_frame"

        if total == 0:
            return []
        if not config.alert_config:
            return alerts

        if hasattr(config.alert_config, 'count_thresholds') and config.alert_config.count_thresholds:
            # Safely fetch the last recorded severity level as a **string** (empty if no history yet)
            last_level = self._ascending_alert_list[-1] if self._ascending_alert_list else "low"
            rank_ids, alert_id = self._get_alert_incident_ids(last_level, stream_info)
            if rank_ids not in [1,2,3,4,5]:
                alert_id = 1

            count_thresholds = {}
            if config.alert_config and hasattr(config.alert_config, "count_thresholds"):
                count_thresholds = config.alert_config.count_thresholds or {}

            for category, threshold in count_thresholds.items():
                alert_serial = getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default']
                alert_serial = alert_serial[0]
                if category == "all" and total > threshold:  
                    
                    alerts.append({
                        "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                        "alert_id": "alert_"+category+'_'+alert_serial+'_'+str(alert_id),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": threshold,
                        "ascending": get_trend(self._ascending_alert_list, lookback=23, prior=14),
                        "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                     getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                    }                    
                    })
                elif category in summary.get("per_category_count", {}):
                    
                    count = summary.get("per_category_count", {})[category]
                    if count > threshold:  # Fixed logic: alert when EXCEEDING threshold
                        alerts.append({
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                            "alert_id": "alert_"+category+'_'+alert_serial+'_'+str(alert_id),
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(self._ascending_alert_list, lookback=23, prior=14),
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                     getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                    }       
                        })
        else:
            pass

        return alerts

    def _generate_incidents(
            self,
            summary: Dict,
            alerts: List[Dict],
            config: FireSmokeConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """Generate structured events for fire and smoke detection output with frame-aware keys."""

        level_params=[{"level":"low","percentage":0.0001},{"level":"medium","percentage":3},
                      {"level":"significant","percentage":13},{"level":"critical","percentage":30}]

        def get_trend_incident(data, lookback=23, prior=14):
            '''
            Determine if the trend is ascending or descending based on actual value progression.
            Now works with determining dominant levels.
            '''
            if len(data) < lookback:
                return "",0,"",0

            post=lookback-prior-1
            levels_list = ["low","medium","significant","critical"]
            current_dominant_incident = Counter(data[-lookback:][:-prior]).most_common(1)[0][0] #from LAST 23 elements fetch FIRST 15 elements
            current_dominant_incident_index = levels_list.index(current_dominant_incident)

            potential_dominant_incident = Counter(data[-post:]).most_common(1)[0][0] #fetch LAST 8 elements
            potential_dominant_incident_index = levels_list.index(potential_dominant_incident)

            return current_dominant_incident, current_dominant_incident_index, potential_dominant_incident, potential_dominant_incident_index


        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        incidents = []
       
        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)
        self._ascending_alert_list = self._ascending_alert_list[-5000:] if len(self._ascending_alert_list) > 5000 else self._ascending_alert_list
        levels_list = ["low","medium","significant","critical"]

        if total > 0:
           # Calculate total bbox area
            total_area = 0.0
            # Safely retrieve count thresholds. If alert_config is None (e.g., when it
            # is not provided or failed to parse) we default to an empty mapping so
            # the subsequent logic can still execute without raising an AttributeError.
            count_thresholds = {}
            if config.alert_config and hasattr(config.alert_config, "count_thresholds"):
                count_thresholds = config.alert_config.count_thresholds or {}
            
            # CRITICAL FIX: Ensure we have at least one category to process
            # If count_thresholds is empty, use detected categories from per_category_count
            # This ensures incidents are always generated when detections exist
            per_category_count = summary.get("per_category_count", {})
            if not count_thresholds and per_category_count:
                # Create thresholds for all detected categories with threshold=0 (always trigger)
                count_thresholds = {cat: 0 for cat in per_category_count.keys()}
                self.logger.debug(f"[INCIDENT] count_thresholds was empty, using detected categories: {count_thresholds}")
            
            # Flag to track if we generated any incident
            incident_generated = False

            for category, threshold in count_thresholds.items():
                if category in per_category_count:
                    
                    #count = summary.get("per_category_count", {})[category]
                    start_timestamp = self._get_start_timestamp_str(stream_info)
                    
                    if start_timestamp and self.current_incident_end_timestamp=='N/A':
                        self.current_incident_end_timestamp = 'Incident still active'
                    elif start_timestamp and self.current_incident_end_timestamp=='Incident still active':
                        current_dominant_incident, current_dominant_incident_index, potential_dominant_incident, potential_dominant_incident_index = get_trend_incident(self._ascending_alert_list, lookback=23, prior=14) #from LAST 23 elements fetch FIRST 15 elements           
                        
                        if current_dominant_incident != potential_dominant_incident:
                            
                            self.current_incident_end_timestamp = current_timestamp
                            self.current_incident_end_timestamp='Incident active'
                    elif self.current_incident_end_timestamp!='Incident still active' and self.current_incident_end_timestamp!='N/A':
                        self.current_incident_end_timestamp = 'N/A'

                    for det in detections:
                        bbox = det.get("bounding_box") or det.get("bbox")
                        if bbox:
                            xmin = bbox.get("xmin")
                            ymin = bbox.get("ymin")
                            xmax = bbox.get("xmax")
                            ymax = bbox.get("ymax")
                            if None not in (xmin, ymin, xmax, ymax):
                                width = xmax - xmin
                                height = ymax - ymin
                                if width > 0 and height > 0:
                                    total_area += width * height

                    threshold_area = config.threshold_area  # 307200.0 | Same threshold as insights

                    intensity_pct = min(100.0, (total_area / threshold_area) * 100)

                    if config.alert_config and config.alert_config.count_thresholds:
                            if intensity_pct >= 30:
                                level = "critical"
                                self._ascending_alert_list.append(level)
                            elif intensity_pct >= 13:
                                level = "significant"
                                self._ascending_alert_list.append(level)
                            elif intensity_pct >= 3:
                                level = "medium"
                                self._ascending_alert_list.append(level)
                            else:
                                level = "low"
                                self._ascending_alert_list.append(level)
                    else:
                            if intensity_pct > 29:
                                level = "critical"
                                intensity = 10.0
                                self._ascending_alert_list.append(level)
                            elif intensity_pct > 12:
                                level = "significant"
                                intensity = 9.0
                                self._ascending_alert_list.append(level)
                            elif intensity_pct > 2:
                                level = "medium"
                                intensity = 7.0
                                self._ascending_alert_list.append(level)
                            else:
                                level = "low"
                                intensity = min(10.0, intensity_pct / 3.0)
                                self._ascending_alert_list.append(level)

                    # Generate human text in new format
                    human_text_lines = [f"INCIDENTS DETECTED @ {current_timestamp}:"]
                    if level=='significant':
                        print_level = "high"
                    else:
                        print_level = level
                    human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE,print_level)}")
                    human_text = "\n".join(human_text_lines)

                    # Pass the last severity level **value** instead of a single-element list
                    last_level = level if level else self._ascending_alert_list[-1]
                    rank_ids, incident_id = self._get_alert_incident_ids(last_level, stream_info)
                    if rank_ids not in [1,2,3,4,5]:
                        incident_id = 1
                    if len(self.id_timing_list)>0 and len(self.id_timing_list)==rank_ids:
                        start_timestamp = self.id_timing_list[-1]
                    if len(self.id_timing_list)>0 and len(self.id_timing_list)>4 and level=='critical':
                        start_timestamp = self.id_timing_list[-1]

                    alert_settings=[]
                    if config.alert_config and hasattr(config.alert_config, 'alert_type'):
                        alert_settings.append({
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                            "ascending": True,
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                                getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                        }
                        })
                
                    event= self.create_incident(incident_id='incident_'+self.CASE_TYPE+'_'+str(incident_id), incident_type=self.CASE_TYPE,
                            severity_level=level, human_text=human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                            start_time=start_timestamp, end_time=self.current_incident_end_timestamp,
                            level_settings= {"low": 3, "medium": 5, "significant":15, "critical": 30})
                    event['duration'] = self.get_duration_seconds(start_timestamp, self.current_incident_end_timestamp)
                    event['incident_quant'] = intensity_pct
                    incidents.append(event)
                    incident_generated = True
            
            # CRITICAL FALLBACK: If no incident was generated despite having detections,
            # generate a basic incident to ensure the incident manager receives data
            if not incident_generated and total > 0:
                self.logger.warning(f"[INCIDENT] No incident generated despite {total} detections. Generating fallback incident.")
                # Calculate area and intensity for fallback
                for det in detections:
                    bbox = det.get("bounding_box") or det.get("bbox")
                    if bbox:
                        xmin, ymin = bbox.get("xmin"), bbox.get("ymin")
                        xmax, ymax = bbox.get("xmax"), bbox.get("ymax")
                        if None not in (xmin, ymin, xmax, ymax):
                            width, height = xmax - xmin, ymax - ymin
                            if width > 0 and height > 0:
                                total_area += width * height
                
                threshold_area = config.threshold_area or 250200.0
                intensity_pct = min(100.0, (total_area / threshold_area) * 100)
                
                # Determine severity level
                if intensity_pct >= 30:
                    level = "critical"
                elif intensity_pct >= 13:
                    level = "significant"
                elif intensity_pct >= 3:
                    level = "medium"
                else:
                    level = "low"
                self._ascending_alert_list.append(level)
                
                start_timestamp = self._get_start_timestamp_str(stream_info)
                human_text = f"INCIDENTS DETECTED @ {current_timestamp}:\n\tSeverity Level: {(self.CASE_TYPE, level)}"
                
                event = self.create_incident(
                    incident_id='incident_' + self.CASE_TYPE + '_fallback',
                    incident_type=self.CASE_TYPE,
                    severity_level=level,
                    human_text=human_text,
                    camera_info=camera_info,
                    alerts=alerts,
                    alert_settings=[],
                    start_time=start_timestamp,
                    end_time='Incident still active',
                    level_settings={"low": 3, "medium": 5, "significant": 15, "critical": 30}
                )
                event['incident_quant'] = intensity_pct
                incidents.append(event)
                self.logger.info(f"[INCIDENT] Generated fallback incident with level={level}, intensity={intensity_pct:.2f}%")

        else:
            #self._ascending_alert_list.append(level)
            incidents.append({})
        return incidents

    def _generate_tracking_stats(
            self,
            summary: Dict,
            alerts: List,
            config: FireSmokeConfig,
            frame_number: Optional[int] = None,
            stream_info: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """Generate structured tracking stats for fire and smoke detection with frame-based keys."""

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        tracking_stats = []
        camera_info = self.get_camera_info_from_stream(stream_info)

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        # Maintain rolling detection history
        if frame_number is not None:
            self._fire_smoke_recent_history.append({
                "frame": frame_number,
                "fire": total_fire,
                "smoke": total_smoke,
            })
            if len(self._fire_smoke_recent_history) > 150:
                self._fire_smoke_recent_history.pop(0)
        
        # Generate human-readable tracking text (people-style format)
        current_timestamp = self._get_current_timestamp_str(stream_info)
        start_timestamp = self._get_start_timestamp_str(stream_info)
        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(stream_info, precision=True)
        high_precision_reset_timestamp = self._get_start_timestamp_str(stream_info, precision=True)

    
        # Build total_counts array in expected format
        # ALWAYS populate with all target categories to avoid empty arrays downstream
        total_counts = []
        if total > 0:
            total_counts.append({
                "category": 'Fire/Smoke',
                "count": 1
            })
        else:
            # When no detections, send count=0 for each category to avoid empty array
            total_counts.append({
                "category": 'Fire',
                "count": 0
            })
            total_counts.append({
                "category": 'Smoke',
                "count": 0
            })

        # Build current_counts array in expected format
        # ALWAYS populate with all target categories to avoid empty arrays downstream
        current_counts = []
        
        # Add Fire entry (count=1 if detected, count=0 if not)
        current_counts.append({
            "category": 'Fire',
            "count": 1 if total_fire > 0 else 0
        })
        
        # Add Smoke entry (count=1 if detected, count=0 if not)
        current_counts.append({
            "category": 'Smoke',
            "count": 1 if total_smoke > 0 else 0
        })

        # Get new track IDs count (requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()
        # current_new_counts: Only NEW objects that appeared for first time
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        human_lines = [f"CURRENT FRAME @ {current_timestamp}:"]
        if total_fire > 0:
            human_lines.append(f"\t- Fire regions detected: {total_fire}")
        if total_smoke > 0:
            human_lines.append(f"\t- Smoke clouds detected: {total_smoke}")
        if total_fire == 0 and total_smoke == 0:
            human_lines.append(f"\t- No fire or smoke detected")

        human_lines.append("")
        # human_lines.append(f"ALERTS SINCE @ {start_timestamp}:")

        recent_fire_detected = any(entry.get("fire", 0) > 0 for entry in self._fire_smoke_recent_history)
        recent_smoke_detected = any(entry.get("smoke", 0) > 0 for entry in self._fire_smoke_recent_history)

        # if recent_fire_detected:
        #     human_lines.append(f"\t- Fire alert")
        # if recent_smoke_detected:
        #     human_lines.append(f"\t- Smoke alert")
        # if not recent_fire_detected and not recent_smoke_detected:
        #     human_lines.append(f"\t- No fire or smoke detected in recent frames")

        human_text = "\n".join(human_lines)

        # Prepare detections without confidence scores (as per eg.json)
        detections = []
        for detection in summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("category", "Fire/Smoke")
            # Include segmentation if available (like in eg.json)
            if detection.get("masks"):
                segmentation= detection.get("masks", [])
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("segmentation"):
                segmentation= detection.get("segmentation")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            elif detection.get("mask"):
                segmentation= detection.get("mask")
                detection_obj = self.create_detection_object(category, bbox, segmentation=segmentation)
            else:
                detection_obj = self.create_detection_object(category, bbox)
            detections.append(detection_obj)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, 'alert_type'):
            alert_settings.append({
                "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                "incident_category": self.CASE_TYPE,
                "threshold_level": config.alert_config.count_thresholds if hasattr(config.alert_config, 'count_thresholds') else {},
                "ascending": True,
                "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                    getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                            }
            })
        
        reset_settings=[
                {
                    "interval_type": "daily",
                    "reset_time": {
                        "value": 9,
                        "time_unit": "hour"
                    }
                }
            ]

        tracking_stat=self.create_tracking_stats(total_counts=total_counts, current_counts=current_counts,
                             detections=detections, human_text=human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                             reset_settings=reset_settings, start_time=high_precision_start_timestamp ,
                             reset_time=high_precision_reset_timestamp)
        
        tracking_stat['target_categories'] = self.target_categories
        # current_new_counts: NEW track IDs that appeared for first time in this frame/aggregation
        tracking_stat['current_new_counts'] = current_new_counts
        tracking_stats.append(tracking_stat)

        if len(self.id_hit_list)==1:
            last_ending_id, incident_id = self._get_alert_incident_ids("",stream_info)
            
            if len(self.id_timing_list)>0 and len(self.id_timing_list)>=5:
                    start_timestamp = self.id_timing_list[-1]
            if incident_id==self.return_id_counter:
                incident_id = incident_id-1 
            if self.return_id_counter > incident_id:
                incident_id = self.return_id_counter-incident_id
            if last_ending_id==5:
                alert_serial = getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default']
                alert_serial = alert_serial[0]
                alerts=[{
                            "alert_type": getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                            "alert_id": "alert_"+'Event_Ended'+'_'+alert_serial+'_'+str(incident_id),
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": 0,
                            "ascending": False,
                            "settings": {t: v for t, v in zip(getattr(config.alert_config, 'alert_type', ['Default']) if hasattr(config.alert_config, 'alert_type') else ['Default'],
                                     getattr(config.alert_config, 'alert_value', ['JSON']) if hasattr(config.alert_config, 'alert_value') else ['JSON'])
                                    }       
                        }]
                tracking_stats.append(alerts)
                tracking_stats[0]['alerts']=alerts
                tracking_stats.append(self.create_incident(incident_id='incident_'+self.CASE_TYPE+'_'+str(incident_id), incident_type=self.CASE_TYPE,
                            severity_level='info', human_text='Event Over', camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
                            start_time=start_timestamp, end_time='Incident still active',
                            level_settings= {"low": 3, "medium": 5, "significant":15, "critical": 30}))
                
        
        return tracking_stats

    def _generate_summary(
            self, summary: dict, general_summary: dict, incidents: List, tracking_stats: List, business_analytics: List, alerts: List
    ) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

    def _calculate_fire_smoke_summary(
            self, data: Any, config: FireSmokeConfig
    ) -> Dict[str, Any]:
        """Calculate summary for fire and smoke detections."""
        if isinstance(data, list):
            # Normalize the categories to lowercase for matching
            valid_categories = [cat.lower() for cat in config.fire_smoke_categories]

            detections = [
                det for det in data
                if det.get("category", "").lower() in valid_categories
            ]
            counts = {}
            for det in detections:
                cat = det.get('category', 'unknown').lower()
                counts[cat] = counts.get(cat, 0) + 1
            

            summary = {
                "total_objects": len(detections),
                "by_category": {},
                "detections": detections,
                "per_category_count": counts,
            }

            # Count by each category defined in config
            for category in config.fire_smoke_categories:
                count = len([
                    det for det in detections
                    if det.get("category", "").lower() == category.lower()
                ])
                summary["by_category"][category] = count

            return summary

        return {"total_objects": 0, "by_category": {}, "detections": []}

    def _generate_business_analytics(self, counting_summary: Dict, alerts:Any, config: FireSmokeConfig, stream_info: Optional[Dict[str, Any]] = None, is_empty=False) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        if is_empty:
            return []

        #-----IF YOUR USECASE NEEDS BUSINESS ANALYTICS, YOU CAN USE THIS FUNCTION------#
        #camera_info = self.get_camera_info_from_stream(stream_info)
        # business_analytics = self.create_business_analytics(nalysis_name, statistics,
        #                          human_text, camera_info=camera_info, alerts=alerts, alert_settings=alert_settings,
        #                          reset_settings)
        # return business_analytics

    def _calculate_metrics(
            self,
            summary: Dict,
            config: FireSmokeConfig,
            context: ProcessingContext,
    ) -> Dict[str, Any]:
        """Calculate detailed metrics for fire and smoke analytics."""

        total = summary.get("total_objects", 0)
        by_category = summary.get("by_category", {})
        detections = summary.get("detections", [])

        total_fire = by_category.get("fire", 0)
        total_smoke = by_category.get("smoke", 0)

        metrics = {
            "total_detections": total,
            "total_fire": total_fire,
            "total_smoke": total_smoke,
            "processing_time": context.processing_time or 0.0,
            "confidence_threshold": config.confidence_threshold,
            "intensity_percentage": 0.0,
            "hazard_level": "unknown",
        }

        # Calculate total bbox area
        total_area = 0.0
        for det in detections:
            bbox = det.get("bounding_box") or det.get("bbox")
            if bbox:
                xmin = bbox.get("xmin")
                ymin = bbox.get("ymin")
                xmax = bbox.get("xmax")
                ymax = bbox.get("ymax")
                if None not in (xmin, ymin, xmax, ymax):
                    width = xmax - xmin
                    height = ymax - ymin
                    if width > 0 and height > 0:
                        total_area += width * height

        threshold_area = 250200.0  # Same threshold as insights/alerts

        intensity_pct = min(100.0, (total_area / threshold_area) * 100)
        metrics["intensity_percentage"] = intensity_pct

        if intensity_pct < 20:
            metrics["hazard_level"] = "low"
        elif intensity_pct < 50:
            metrics["hazard_level"] = "moderate"
        elif intensity_pct < 80:
            metrics["hazard_level"] = "high"
        else:
            metrics["hazard_level"] = "critical"

        return metrics

    def _extract_predictions(
            self, data: Any, config: FireSmokeConfig
    ) -> List[Dict[str, Any]]:
        """Extract predictions from processed data for API compatibility."""
        predictions = []

        try:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        prediction = {
                            "category": item.get("category", item.get("class", "unknown")),
                            "confidence": item.get("confidence", item.get("score", 0.0)),
                            "bounding_box": item.get("bounding_box", item.get("bbox", {})),
                        }
                        predictions.append(prediction)

        except Exception as e:
            self.logger.warning(f"Failed to extract predictions: {str(e)}")

        return predictions
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Get configuration schema for fire and smoke detection."""
        return {
            "type": "object",
            "properties": {
                "confidence_threshold": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0,
                    "default": 0.5,
                    "description": "Minimum confidence threshold for detections",
                },
                "fire_smoke_categories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["fire", "smoke"],
                    "description": "Category names that represent fire and smoke",
                },
                "index_to_category": {
                    "type": "object",
                    "additionalProperties": {"type": "string"},
                    "description": "Mapping from category indices to names",
                },
                "alert_config": {
                    "type": "object",
                    "properties": {
                        "count_thresholds": {
                            "type": "object",
                            "additionalProperties": {"type": "integer", "minimum": 1},
                            "description": "Count thresholds for alerts",
                        }
                    },
                },
            },
            "required": ["confidence_threshold"],
            "additionalProperties": False,
        }

    def create_default_config(self, **overrides) -> FireSmokeConfig:
        """Create default configuration with optional overrides."""
        defaults = {
            "category": self.category,
            "usecase": self.name,
            "confidence_threshold": 0.3,
            "fire_smoke_categories": ["fire", "smoke"],
        }
        defaults.update(overrides)
        return FireSmokeConfig(**defaults)

    def _count_unique_tracks(self, summary: Dict) -> Optional[int]:
        """Count unique track IDs from detections, if tracking info exists."""
        detections = summary.get("detections", [])
        if not detections:
            return None

        unique_tracks = set()
        for detection in detections:
            track_id = detection.get("track_id")
            if track_id is not None:
                unique_tracks.add(track_id)

        return len(unique_tracks) if unique_tracks else None

    def _update_tracking_state(self, detections: list):
        """
        Update tracking state with current frame detections.
        Computes which track IDs are NEW (appeared for first time this frame).
        """
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {cat: set() for cat in self.target_categories}
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}

        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            track_id = det.get("track_id")

            if cat not in self.target_categories:
                continue
            if track_id is not None:
                self._per_category_total_track_ids.setdefault(cat, set()).add(track_id)
                self._current_frame_track_ids[cat].add(track_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self) -> Dict[str, int]:
        """Get cumulative total of all unique track IDs ever seen per category."""
        return {cat: len(ids) for cat, ids in getattr(self, '_per_category_total_track_ids', {}).items()}

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame vs the previous one."""
        return {cat: len(ids) for cat, ids in getattr(self, '_new_track_ids_this_frame', {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, '_current_frame_track_ids', {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        # Guard against pre-Y2K timestamps from relative RTP values
        if dt.year < 2000:
            dt = datetime.now(timezone.utc)
        return dt.strftime('%Y:%m:%d %H:%M:%S')

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            # Guard against pre-Y2K timestamps from relative RTP values
            if dt.year < 2000:
                dt = datetime.now(timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(' UTC', '').strip()

        # Remove milliseconds if present (everything after the last dot)
        if '.' in timestamp_clean:
            timestamp_clean = timestamp_clean.split('.')[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count('-') >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split('-')
                if len(parts) >= 4:
                    # Guard against pre-Y2K timestamps from relative RTP values
                    try:
                        if int(parts[0]) < 2000:
                            return datetime.now(timezone.utc).strftime('%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        pass
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
           

            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        
        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        
        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            # Guard against pre-Y2K timestamps from relative RTP values
            if dt.year < 2000:
                dt = datetime.now(timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    def get_duration_seconds(self, start_time, end_time):
        def parse_relative_time(t):
            """Parse HH:MM:SS(.f) manually into timedelta"""
            try:
                parts = t.strip().split(":")
                if len(parts) != 3:
                    return None
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])  # works for 7.4
                return timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except:
                return None

        def parse_time(t):
            # Check for HH:MM:SS(.ms) format
            if re.match(r'^\d{1,2}:\d{2}:\d{1,2}(\.\d+)?$', t):
                return parse_relative_time(t)

            # Check for full UTC format like 2025-08-01-14:23:45.123456 UTC
            if "UTC" in t:
                try:
                    return datetime.strptime(t, "%Y-%m-%d-%H:%M:%S.%f UTC")
                except ValueError:
                    return None

            return None

        start_dt = parse_time(start_time)
        end_dt = parse_time(end_time)

        # Return None if invalid
        if start_dt is None or end_dt is None:
            return 'N/A'

        # If timedelta (relative time), subtract directly
        if isinstance(start_dt, timedelta) and isinstance(end_dt, timedelta):
            delta = end_dt - start_dt
        elif isinstance(start_dt, datetime) and isinstance(end_dt, datetime):
            delta = end_dt - start_dt
        else:
            return None

        return delta.total_seconds()

    def _get_alert_incident_ids(self, sev_level, stream_info: Optional[Dict[str, Any]] = None):

        if sev_level!="":
            if sev_level==self.id_hit_list[0] and len(self.id_hit_list)>=2:
                self.id_hit_counter+=1
                if self.id_hit_counter>7:
                    self.latest_stack = self.id_hit_list[0]
                    self.id_hit_list.pop(0)
                    self.id_hit_counter=0
                    self.id_timing_list.append(self._get_current_timestamp_str(stream_info))
                    return (5-len(self.id_hit_list),self.return_id_counter)
                
            elif self.id_hit_counter>0:
                self.id_hit_counter-=1
            elif self.id_hit_counter<0:
                self.id_hit_counter=0

            if len(self.id_hit_list) > 1:
                if sev_level==self.latest_stack:
                    return (5-len(self.id_hit_list),self.return_id_counter)
                else:
                    return (0,0)
        else:
            if len(self.id_hit_list)==1:
                self.id_hit_counter+=1
                if self.id_hit_counter>130:
                    self.id_hit_list = ["low","medium","significant","critical","low"]
                    pre_return_id = self.return_id_counter
                    self.return_id_counter+=1
                    self.id_hit_counter = 0
                    self.latest_stack = None
                    self.id_timing_list.append(self._get_current_timestamp_str(stream_info))
                    return (int(5),pre_return_id)
                if sev_level==self.latest_stack:
                    return (5-len(self.id_hit_list),self.return_id_counter)
                else:
                    return (0,0)
            elif self.id_hit_counter>0:
                self.id_hit_counter-=1
            elif self.id_hit_counter<0:
                self.id_hit_counter=0
        return (1,1)


