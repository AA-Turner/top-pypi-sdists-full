"""Stub file for analytics.tests directory."""
from typing import Any, Dict, Optional, Tuple

# Constants
ByteTrackWrapper: Any = ...  # From test_identity_analytics
ByteTrackWrapper: Any = ...  # From test_incident_analytics
ByteTrackWrapper: Any = ...  # From test_quality_analytics
ALLOWED_GEAR_LABELS: Any = ...  # From test_safety_analytics
CAPPED_GEAR_CATEGORIES: Tuple[Any, ...] = ...  # From test_safety_analytics
DEDUP_IOU_MERGE_THRESHOLD: float = ...  # From test_safety_analytics
DEFAULT_BASE: Any = ...  # From test_safety_analytics
DEFAULT_MANIFEST: Any = ...  # From test_safety_analytics
DEFAULT_OUT_DIR: Any = ...  # From test_safety_analytics
DEFAULT_PEOPLE_MODEL: Any = ...  # From test_safety_analytics
DEFAULT_PPE_MODEL: Any = ...  # From test_safety_analytics
DEFAULT_VIDEO: Any = ...  # From test_safety_analytics
GEAR_COLORS_BGR: Dict[Any, Any] = ...  # From test_safety_analytics
PERSON_BOX_BGR: Tuple[Any, ...] = ...  # From test_safety_analytics
PPE_ROI_EXPAND_FACTOR: float = ...  # From test_safety_analytics
VIOLATION_LABELS: Any = ...  # From test_safety_analytics
ByteTrackWrapper: Any = ...  # From test_volume_analytics
INDEX_TO_CATEGORY_MAP: Dict[Any, Any] = ...  # From test_volume_analytics
ByteTrackWrapper: Any = ...  # From test_zone_analytics
DEFAULT_ZONE_COLOR: Tuple[Any, ...] = ...  # From test_zone_analytics
VIDEO_HEIGHT: int = ...  # From test_zone_analytics
VIDEO_WIDTH: int = ...  # From test_zone_analytics

# Functions
# From test_identity_analytics
def get_index_to_category(manifest_name: str) -> dict[int, str]: ...

# From test_incident_analytics
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index-to-category mapping according to the analytics manifest.
    
        Args:
            manifest_name: The YAML manifest name (e.g. "fire_detection").
    """
    ...

# From test_quality_analytics
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index→category mapping for a manifest.
    """
    ...

# From test_safety_analytics
def main() -> None: ...

# From test_safety_analytics
def run(video_path: Any, people_model_path: str, ppe_model_path: Any, manifest_path: Any, out_dir: Any) -> None: ...

# From test_volume_analytics
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index-to-category mapping according to the analytics manifest.
    Args:
        manifest_name: The YAML manifest name or usecase (e.g., "vehicle_type_monitoring", "people_counting", "footfall").
    """
    ...

# Classes
# From test_identity_analytics
class IdentityAnalyticsTestProcessor:
    # End-to-end test harness for the IDENTITY processor (LPR).

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...


# From test_identity_analytics
class PlateOCR:
    # Wrap ``fast_plate_ocr.LicensePlateRecognizer`` with a per-track cache.
    #
    #     The OCR model runs only when:
    #       - we have not yet produced any text for this track_id, OR
    #       - the cached confidence is below ``refresh_conf`` AND the track
    #         has been re-seen since the last OCR attempt more than
    #         ``refresh_every`` frames ago.

    def __init__(self: Any, hub_model: str = 'cct-xs-v1-global-model', min_box_px: int = 24, refresh_conf: float = 0.75, refresh_every: int = 30) -> None: ...

    def enrich(self: Any, detections: list[dict[str, Any]], frame: Any.Any, frame_idx: int) -> None:
        """
        Attach ``plate_text`` + ``identity_confidence`` in place.
        """
        ...


# From test_incident_analytics
class IncidentAnalyticsTestProcessor:
    # End-to-end test harness for incident-type analytics (fire detection).
    #
    #     Runs YOLO inference on a video, converts detections into the format
    #     expected by the AnalyticsEngine with an INCIDENT category processor,
    #     and stores per-frame results, aggregation results, and incident events
    #     as JSON files.

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None:
        """
        Initialize the incident test processor.
        
                Args:
                    manifest_name: Name of the YAML manifest under analytics/config/
                        (e.g. "fire_detection").
                    model_path: Path to the YOLO model weights (.pt).
                    video_path: Path to the input video file.
                    max_frames: Stop after this many frames (None = all, across all loops).
                    loop_count: Number of times to loop the video (default 1 = no loop).
                    json_dir: Directory for per-frame JSON outputs.
                    draw_bboxes: If True, annotate frames and write an output video.
                    output_video_path: Path for the annotated output video.
                    confidence_threshold: Minimum confidence for detections.
                    stream_info: Optional stream metadata passed to the engine.
        """
        ...

    def process_video(self: Any) -> Any:
        """
        Run inference + incident analytics engine on every frame.
        """
        ...


# From test_quality_analytics
class QualityAnalyticsTestProcessor:
    # End-to-end test harness for the QUALITY processor.
    #
    #     Runs a YOLO model + ByteTrackWrapper on a video, feeds tracked
    #     detections into the new ``AnalyticsEngine``, and dumps per-frame +
    #     aggregation JSONs.

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...


# From test_redis_publisher_config
class TestClientConstruction:
    def test_connect_failure_degrades_to_a_no_op(self: Any) -> Any:
        """
        Publishing must never take the pipeline down with it.
        """
        ...

    def test_falls_back_to_a_direct_client_without_sentinel(self: Any) -> Any: ...

    def test_target_description_names_sentinel(self: Any) -> Any: ...

    def test_uses_sentinel_when_configured(self: Any) -> Any:
        """
        Sentinel resolves the CURRENT master and follows failover; a fixed
                host cannot, and on an HA Service it is a replica half the time.
        """
        ...


# From test_redis_publisher_config
class TestConfigSeam:
    # PostProcRunner -> PostProcessor -> publisher. This chain was severed:
    #     the correctly-resolved config existed upstream but was never forwarded.

    def test_post_processor_forwards_redis_config(self: Any) -> Any: ...

    def test_post_processor_without_config_still_works(self: Any) -> Any: ...


# From test_redis_publisher_config
class TestConnectionResolution:
    def test_defaults_to_localhost_when_nothing_is_configured(self: Any) -> Any:
        """
        The original bug's starting point, kept explicit so it stays visible.
        """
        ...

    def test_env_supplies_the_connection(self: Any, monkeypatch: Any) -> Any: ...

    def test_explicit_config_beats_the_environment(self: Any, monkeypatch: Any) -> Any:
        """
        A caller that already resolved the topology must not be overridden.
        """
        ...

    def test_sentinel_from_config(self: Any) -> Any: ...

    def test_sentinel_from_env(self: Any, monkeypatch: Any) -> Any: ...


# From test_redis_publisher_config
class TestPy38Compatibility:
    # The Orin image runs Python 3.8. A PEP 604 union in a module WITHOUT
    #     `from __future__ import annotations` is evaluated at import and raises
    #     TypeError there — that is exactly what crashed matrice_common on Orin.
    #     ruff's target-version is py311 while requires-python is >=3.8, so it will
    #     keep suggesting the unsafe form; this test is the guard.

    def test_no_pep604_unions_without_future_import(self: Any, module_path: Any) -> Any: ...


# From test_redis_publisher_config
class TestSentinelHostParsing:
    # The three shapes the value actually arrives in.

    def test_bad_entries_are_skipped_not_fatal(self: Any) -> Any: ...

    def test_comma_separated_string_from_env(self: Any) -> Any: ...

    def test_empty_yields_no_hosts(self: Any, empty: Any) -> Any: ...

    def test_explicit_ports_win_over_the_default(self: Any) -> Any: ...

    def test_list_of_pairs_passes_through(self: Any) -> Any: ...

    def test_list_of_strings(self: Any) -> Any: ...


# From test_volume_analytics
class AnalyticsEngineTestProcessor:
    # End-to-end test harness for the new AnalyticsEngine.
    #
    #     Runs YOLO inference + ByteTrackWrapper (same config as footfall use case)
    #     on a video, converts tracked detections into the format expected by the
    #     engine, and stores per-frame + aggregation results as JSON files.

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None:
        """
        Initialize the test processor.
        
                Args:
                    manifest_name: Name of the YAML manifest under analytics/config/
                        (e.g. "people_counting").
                    model_path: Path to the YOLO model weights (.pt).
                    video_path: Path to the input video file.
                    max_frames: Stop after this many frames (None = all, across all loops).
                    loop_count: Number of times to loop the video (default 1 = no loop).
                    json_dir: Directory for per-frame JSON outputs.
                    draw_bboxes: If True, annotate frames and write an output video.
                    draw_lines: If True, draw zone lines/zones from the engine's
                        ``stream_info.zone_config`` (and method from ``volume.counter``)
                        on the output video. Implies video output.
                    output_video_path: Path for the annotated output video.
                    confidence_threshold: Minimum confidence for detections.
                    stream_info: Optional stream metadata passed to the engine.
        """
        ...

    def process_video(self: Any) -> Any:
        """
        Run inference + tracking + analytics engine on every frame.
        """
        ...


# From test_zone_analytics
class ZoneAnalyticsTestProcessor:
    # End-to-end test for per-zone volume analytics.
    #
    #     Runs YOLO + ByteTrack on a video, feeds detections into the
    #     AnalyticsEngine with zone polygons configured, draws per-zone
    #     live counts on the video, and saves aggregation results.

    def __init__(self: Any, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...


from . import test_identity_analytics, test_incident_analytics, test_quality_analytics, test_redis_publisher_config, test_safety_analytics, test_volume_analytics, test_zone_analytics