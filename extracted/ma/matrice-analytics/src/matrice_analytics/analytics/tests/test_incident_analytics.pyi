"""Auto-generated stub for module: test_incident_analytics."""
from typing import Any, Optional

# Constants
ByteTrackWrapper: Any

# Functions
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index-to-category mapping according to the analytics manifest.
    
        Args:
            manifest_name: The YAML manifest name (e.g. "fire_detection").
    """
    ...

# Classes
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

