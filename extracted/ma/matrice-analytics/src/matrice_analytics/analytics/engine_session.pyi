"""Auto-generated stub for module: engine_session."""
from typing import Any, Dict, List, Optional

from ..post_processing.Trackers.integration import ConfigDrivenTracker, TrackerProfile
from ..post_processing.utils.post_processing_config_client import is_null_object_id, normalize_location_id
from .engine import AnalyticsEngine

# Constants
logger: Any

# Functions
def build_coco_harness_mislabel_lookup(model_index_to_category: Dict[int, str]) -> Dict[str, int]:
    """
    Map wrong COCO string labels back to custom-model class ids.
    
        The inference harness labels PPE model outputs with COCO names at the same
        numeric index (e.g. class 0 → ``person`` instead of ``Hardhat``,
        class 5 → ``bus`` instead of ``Person``). When ``class_id`` is stripped
        and only the wrong string remains, reverse via the default COCO name at
        each model index.
    """
    ...
def detection_class_id_from_detection(det: Dict[str, Any]) -> Optional[int]:
    """
    Best-effort numeric class id from common inference field names.
    
        Prefer ``category_id`` / ``cls`` / ``class`` before ``class_id`` — the
        harness often sticks ``class_id`` at 0 while ``category_id`` still carries
        the true model class.
    """
    ...
def looks_like_coco_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """
    Heuristic: deployment UI often ships a generic COCO map for custom models.
    """
    ...
def looks_like_wrong_ppe_index_to_category(mapping: Optional[Dict[int, str]]) -> bool:
    """
    Detect incomplete or mis-typed PPE maps (e.g. ``{0: 'Person'}`` from the UI).
    """
    ...
def map_detection_categories(detections: List[Dict[str, Any]], index_to_category: Optional[Dict[Any, Any]]) -> List[Dict[str, Any]]:
    """
    Map detections to labels from ``index_to_category`` config.
    
        Shared by new-flow AnalyticsEngineSession and legacy ``ppe_compliance``.
    
        PPE harness reality (``ppe_coco_fixup=True``):
          - ``class_id`` is often stuck at 0 for every box — do not trust it alone.
          - Category string is the COCO name at the PPE model index:
            person→Hardhat, bicycle→Mask, …, bus→Person, truck→Safety Vest, …
          Priority:
            1. COCO harness strings (primary path)
            2. Keep known PPE labels already on the detection
            3. ``category_id`` / ``cls`` / ``class`` when present and not stuck-only
               via ``class_id`` (prefer those keys over ``class_id``)
            4. Numeric category field
    """
    ...
def normalize_index_to_category(mapping: Optional[Dict[Any, Any]]) -> Dict[int, str]:
    """
    Coerce ``index_to_category`` keys to ``int`` (JSON uploads use string keys).
    
        Values are stripped: this is the other ingestion boundary for the deployment's
        ``class_index_map``, and a single trailing space in it (``"gun "``) once made a
        weapon app detect nothing at all, silently, because an unmapped class is ignored
        rather than rejected. See ``post_processing.utils.filter_utils`` for the same guard
        on the other path -- the two must agree or the bug just moves.
    """
    ...
def resolve_camera_fields_from_stream_info(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve camera identity fields from the per-frame ``stream_info`` dict.
    
        Mirrors legacy ``AnalyticsPublisher`` / ``INCIDENT_MANAGER`` lookup paths
        so ``results-agg`` gets the human-readable ``camera_name``, not a duplicate
        of ``camera_id`` when the name lives under ``stream_config`` or nested
        ``input_streams``.
    """
    ...
def resolve_location_for_publish(stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Resolve ``locationId`` and display ``location`` for Redis / results-agg envelopes.
    
        Mirrors the field lookup paths used for incidents (``camera_info``, ``stream_config``,
        enriched top-level ``stream_info``). Null Mongo ObjectIds are blanked; missing names
        fall back to ``Unknown Location``.
    """
    ...

# Classes
class AnalyticsEngineSession:
    # One camera's AnalyticsEngine + tracker + publishing wiring.

    def __init__(self: Any, manifest_name: str, app_name: Optional[str], index_to_category: Optional[Dict[int, str]], publisher: Any, logger_: Optional[Any.Any] = None) -> None: ...

    def process(self: Any, detections: List[Dict[str, Any]], stream_info: Optional[Dict[str, Any]], stream_key: str = '') -> Dict[str, Any]:
        """
        Run one frame; return the per-frame zone-keyed agg_summary (or {}).
        """
        ...

