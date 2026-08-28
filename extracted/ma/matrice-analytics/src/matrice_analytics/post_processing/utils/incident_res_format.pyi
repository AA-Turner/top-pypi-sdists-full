"""Auto-generated stub for module: incident_res_format."""
from typing import Any, Dict, Optional

from ...analytics.engine_session import resolve_camera_fields_from_stream_info
from ...analytics.schemas import IncidentEvent, IncidentMessage, StreamInfo

# Functions
def build_incident_res_message(incident_data: Dict[str, Any], stream_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Serialize a legacy incident dict to the canonical ``incident_res`` envelope.
    """
    ...
def format_incident_human_text(incident_type: str, severity_level: str) -> str: ...
def is_valid_incident_end_time(value: Any) -> bool:
    """
    True when ``value`` is a real closing timestamp (not a lifecycle placeholder).
    """
    ...
def map_severity_for_wire(level: str) -> str:
    """
    Map internal ``significant`` to backend ``high``.
    """
    ...
def normalize_incident_timestamp(value: Any) -> str:
    """
    Coerce a legacy use case's start_time/end_time into RFC3339 (``%Y-%m-%dT%H:%M:%SZ``).
    
        Unparseable or empty input is returned unchanged (as ``_pick_str`` would leave it) --
        passing through rather than dropping data on a shape not seen before.
    """
    ...
def stream_info_dict_to_stream_info(stream_info: Optional[Dict[str, Any]]) -> Any:
    """
    Map legacy pipeline ``stream_info`` dict → :class:`StreamInfo`.
    """
    ...
def utc_now_iso_z() -> str: ...
