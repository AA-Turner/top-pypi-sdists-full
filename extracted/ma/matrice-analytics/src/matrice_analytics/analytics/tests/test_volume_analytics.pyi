"""Auto-generated stub for module: test_volume_analytics."""
from typing import Any, Dict, Optional

# Constants
ByteTrackWrapper: Any
INDEX_TO_CATEGORY_MAP: Dict[Any, Any]

# Functions
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index-to-category mapping according to the analytics manifest.
    Args:
        manifest_name: The YAML manifest name or usecase (e.g., "vehicle_type_monitoring", "people_counting", "footfall").
    """
    ...

# Classes
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

