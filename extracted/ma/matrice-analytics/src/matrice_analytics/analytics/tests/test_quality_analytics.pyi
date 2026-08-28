"""Auto-generated stub for module: test_quality_analytics."""
from typing import Any

# Constants
ByteTrackWrapper: Any

# Functions
def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index→category mapping for a manifest.
    """
    ...

# Classes
class QualityAnalyticsTestProcessor:
    # End-to-end test harness for the QUALITY processor.
    #
    #     Runs a YOLO model + ByteTrackWrapper on a video, feeds tracked
    #     detections into the new ``AnalyticsEngine``, and dumps per-frame +
    #     aggregation JSONs.

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...

