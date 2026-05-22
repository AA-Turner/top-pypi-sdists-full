"""Auto-generated stub for module: license_plate_monitoring."""
from typing import Any, Dict, List, Optional, Set

from ..advanced_tracker import AdvancedTracker
from ..advanced_tracker.config import TrackerConfig
from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import AlertConfig, BaseConfig
from ..ocr.fast_plate_ocr_py38 import LicensePlateRecognizer
from ..ocr.preprocessing import ImagePreprocessor
from ..utils import BBoxSmoothingConfig, BBoxSmoothingTracker, apply_category_mapping, bbox_smoothing, filter_by_confidence, match_results_structure
from ..utils.alert_instance_utils import ALERT_INSTANCE

# Constants
HAS_MATRICE_SESSION: bool
major_version: Any
minor_version: Any

# Classes
class LicensePlateMonitorConfig:
    # Configuration for License plate detection use case in License plate monitoring.
    #
    #     Available OCR models (``ocr_model_name``):
    #
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | Model                                   | Architecture | Training Data       | Best For                          |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+
    #     | cct-s-v1-global-model          (default)| CCT (S)      | Global plates       | General use                       |
    #     | cct-xs-v1-global-model                  | CCT (XS)     | Global plates       | Faster / smaller                  |
    #     | cct-s-relu-v1-global-model              | CCT-ReLU (S) | Global plates       | Same as S but with ReLU           |
    #     | cct-xs-relu-v1-global-model             | CCT-ReLU(XS) | Global plates       | Fastest CCT variant               |
    #     | european-plates-mobile-vit-v2-model     | MobileViT-v2 | European plates     | European plates specifically      |
    #     | global-plates-mobile-vit-v2-model       | MobileViT-v2 | Global (65+ countries)| Most comprehensive coverage      |
    #     | argentinian-plates-cnn-model            | CNN          | Argentinian plates  | Argentina only                    |
    #     | argentinian-plates-cnn-synth-model      | CNN          | Argentinian (synth) | Argentina only                    |
    #     +-----------------------------------------+--------------+---------------------+-----------------------------------+

    def validate(self: Any) -> List[str]:
        """
        Validate configuration parameters.
        """
        ...

class LicensePlateMonitorLogger:
    def __init__(self: Any) -> None: ...

    def get_server_connection_info(self: Any) -> Optional[Dict[str, Any]]:
        """
        Fetch server connection info from RPC.
        """
        ...

    def initialize_session(self: Any, config: Any) -> None:
        """
        Initialize session and fetch server connection info if lpr_server_id is provided.
        """
        ...

    async def log_plate(self: Any, plate_text: str, timestamp: str, stream_info: Dict[str, Any], image_data: Optional[str] = None, cooldown: float = 30.0) -> bool:
        """
        Log plate to RPC server with cooldown period.
        
                Args:
                    plate_text: The license plate text
                    timestamp: Capture timestamp
                    stream_info: Stream information dict
                    image_data: Base64-encoded JPEG image of the license plate crop
                    cooldown: Cooldown period in seconds
        """
        ...

    def should_log_plate(self: Any, plate_text: str, cooldown: float) -> bool:
        """
        Check if enough time has passed since last log for this plate.
        """
        ...

    def update_log_timestamp(self: Any, plate_text: str) -> None:
        """
        Update the last log timestamp for a plate.
        """
        ...

class LicensePlateMonitorUseCase:
    def __init__(self: Any) -> None: ...

    CATEGORY_DISPLAY: Dict[Any, Any]

    def get_current_frame_counts(self: Any) -> Dict[str, int]:
        """
        Get count of ALL track IDs currently in this frame (existing + new).
        """
        ...

    def get_new_counts_this_frame(self: Any) -> Dict[str, int]:
        """
        Get count of NEW track IDs that appeared in this frame vs the previous one.
        """
        ...

    def get_total_counts(self: Any) -> Any:
        """
        Return total unique license plate texts encountered so far.
        """
        ...

    async def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any: ...

    def reset_all_tracking(self: Any) -> None:
        """
        Reset both advanced tracker and plate tracking state.
        """
        ...

    def reset_plate_tracking(self: Any) -> None:
        """
        Reset plate tracking state.
        """
        ...

    def reset_tracker(self: Any) -> None:
        """
        Reset the advanced tracker instance.
        """
        ...

    def set_alert_manager(self: Any, alert_manager: Any) -> None:
        """
        Set the alert manager instance for instant alerts.
        
        Args:
            alert_manager: ALERT_INSTANCE instance configured with Redis/Kafka clients
        """
        ...

    def set_bgr_frame(self: Any, bgr_frame: Any) -> Any:
        """
        Set raw BGR frame for OCR analysis (avoids JPEG encode/decode loss).
        """
        ...

