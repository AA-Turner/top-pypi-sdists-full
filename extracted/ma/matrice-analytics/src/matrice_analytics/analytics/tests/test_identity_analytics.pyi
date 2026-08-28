"""Auto-generated stub for module: test_identity_analytics."""
from typing import Any

# Constants
ByteTrackWrapper: Any

# Functions
def get_index_to_category(manifest_name: str) -> dict[int, str]: ...

# Classes
class IdentityAnalyticsTestProcessor:
    # End-to-end test harness for the IDENTITY processor (LPR).

    def __init__(self: Any, manifest_name: str, model_path: str, video_path: str) -> None: ...

    def process_video(self: Any) -> Any: ...

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

