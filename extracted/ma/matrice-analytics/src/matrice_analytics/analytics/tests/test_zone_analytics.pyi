"""Auto-generated stub for module: test_zone_analytics."""
from typing import Any, Tuple

# Constants
ByteTrackWrapper: Any
DEFAULT_ZONE_COLOR: Tuple[Any, ...]
VIDEO_HEIGHT: int
VIDEO_WIDTH: int

# Classes
class ZoneAnalyticsTestProcessor:
    # End-to-end test for per-zone volume analytics.
    #
    #     Runs YOLO + ByteTrack on a video, feeds detections into the
    #     AnalyticsEngine with zone polygons configured, draws per-zone
    #     live counts on the video, and saves aggregation results.

    def __init__(self: Any, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...

