"""Auto-generated stub for module: legacy_analytics_bridge."""
from typing import Any, Dict, Optional

from ...analytics.engine_session import resolve_camera_fields_from_stream_info, resolve_location_for_publish
from ..core.base import registry
from .incident_res_format import build_incident_res_message
from .incident_res_format import is_valid_incident_end_time
from .location_name_cache import LocationNameCache
from .post_processing_config_client import PostProcessingConfigClient
from .post_processing_config_client import is_resolvable_location_id, normalize_location_id

# Constants
AGGREGATION_INTERVAL_SEC: float
ANALYTICS_ZONE_GLOBAL: str
LEGACY_PUBLISHER_ENV: str
logger: Any

# Functions
def build_incident_message(incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build ``incident_res`` payload matching NEW-flow ``IncidentMessage``.
    """
    ...
def extract_stream_context(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve camera / deployment identity fields for Redis envelopes.
    """
    ...
def get_legacy_profile(usecase: str) -> Optional[Any]:
    """
    Explicit profile if registered, else a synthesized default profile.
    
        Returns ``None`` only for the documented still-image exclusions, so that a
        caller can distinguish "no analytics wiring" from "default wiring".
    """
    ...
def get_legacy_session(stream_key: str) -> 'Any': ...
def legacy_redis_analytics_usecases() -> Any[str]:
    """
    Every legacy app the SDK self-publishes (incident_res + results-agg).
    
        Full coverage: the explicit profiles PLUS every use-case in the processor
        registry, minus the documented still-image exclusions. Returns an EMPTY set
        when :data:`LEGACY_PUBLISHER_ENV` is truthy, ceding ownership to the caller's
        old ``AnalyticsPublisher`` so there is no double-publish.
    """
    ...
def publish_legacy_frame_analytics() -> None:
    """
    Ingest one legacy frame and publish Redis analytics when due.
    
    ``incident_via_manager`` is True when ``IncidentManager`` already handled
    the incident for this frame (skip duplicate ``incident_res`` publish).
    """
    ...
def reset_legacy_sessions() -> None: ...

# Classes
class LegacyAnalyticsProfile:
    # Per-usecase Redis analytics wiring (incidents + VOLUME results-agg).

    ...
class LegacyAnalyticsSession:
    # Per-stream accumulator for 60s ``results-agg`` publishing.

    def ingest_agg_summary(self: Any, agg_summary: Any) -> None: ...

    def maybe_publish_incident(self: Any, incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> bool:
        """
        Publish to ``incident_res`` on severity transition (deduped).
        """
        ...

    def maybe_publish_results_agg(self: Any, stream_info: Optional[Dict[str, Any]]) -> bool:
        """
        Publish ``results-agg`` every ~60s with zone-keyed tracking_stats + metrics.
        """
        ...

class VolumeMetricSpec:
    ...
