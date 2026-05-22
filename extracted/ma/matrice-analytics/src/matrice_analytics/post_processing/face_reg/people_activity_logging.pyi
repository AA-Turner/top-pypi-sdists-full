"""Auto-generated stub for module: people_activity_logging."""
from typing import Any, Dict, Optional

from .face_recognition_client import FacialRecognitionClient

# Classes
class PeopleActivityLogging:
    # Background logging system for face recognition activity

    def __init__(self: Any, face_client: Any = None) -> None: ...

    def clear_unknown_faces_storage(self: Any) -> None:
        """
        Clear stored unknown face images
        """
        ...

    async def enqueue_detection(self: Any, detection: Dict, current_frame: Optional[Any.Any] = None, location: str = '', camera_name: str = '', camera_id: str = '', rtp_number: str = '') -> Any:
        """
        Enqueue a detection for background processing
        """
        ...

    def get_unknown_faces_storage(self: Any) -> Dict[str, Any]:
        """
        Get stored unknown face images as bytes
        """
        ...

    def start_background_processing(self: Any) -> Any:
        """
        Start the background processing thread
        """
        ...

    def stop_background_processing(self: Any) -> Any:
        """
        Stop the background processing thread
        """
        ...

