"""Auto-generated stub for module: face_recognition_client."""
from typing import Any, Dict, List, Optional

# Functions
def create_face_client(account_number: str = None, access_key: str = None, secret_key: str = None, project_id: str = None, server_id: str = '', session: Any = None) -> Any:
    """
    Create a facial recognition client with automatic credential detection
    """
    ...

# Classes
class FacialRecognitionClient:
    # Simplified Face Recognition Client using Matrice Session.
    # All API calls are made through the Matrice session RPC interface.

    def __init__(self: Any, account_number: str = '', access_key: str = '', secret_key: str = '', project_id: str = '', server_id: str = '', session: Any = None) -> None: ...

    ACTION_ID_PATTERN: Any

    async def enroll_staff(self: Any, staff_data: Dict[str, Any], image_paths: List[str]) -> Dict[str, Any]:
        """
        Enroll a new staff member with face images
        
        Args:
            staff_data: Dictionary containing staff information (staffId, firstName, lastName, etc.)
            image_paths: List of file paths to face images
        
        Returns:
            Dict containing enrollment response
        """
        ...

    async def enroll_staff_base64(self: Any, staff_data: Dict[str, Any], base64_images: List[str]) -> Dict[str, Any]:
        """
        Enroll staff with base64 encoded images
        
                API: POST /v1/facial_recognition/staff/enroll?projectId={projectId}&serverID={serverID}
        """
        ...

    async def enroll_unknown_person(self: Any, embedding: List[float], image_source: str = None, timestamp: str = None, location: str = None, _employee_id: str = None) -> Dict[str, Any]:
        """
        Enroll an unknown person
        
                API: POST /v1/facial_recognition/enroll_unknown_person?projectId={projectId}&serverID={serverID}
        """
        ...

    async def get_all_staff_embeddings(self: Any) -> Dict[str, Any]:
        """
        Get all staff embeddings
        
                API: GET /v1/facial_recognition/get_all_staff_embeddings?projectId={projectId}&serverID={serverID}
        """
        ...

    async def get_redis_details(self: Any) -> Dict[str, Any]:
        """
        Get Redis connection details from facial recognition server
        
                API: GET /v1/facial_recognition/get_redis_details
        
                Returns:
                    Dict containing Redis connection details (REDIS_IP, REDIS_PORT, REDIS_PASSWORD)
        """
        ...

    def get_server_connection_info(self: Any) -> Optional[Dict[str, Any]]:
        """
        Fetch server connection info from RPC.
        """
        ...

    async def get_staff_details(self: Any, staff_id: str) -> Dict[str, Any]:
        """
        Get full staff details by staff ID
        
                API: GET /v1/facial_recognition/staff/:staffId?projectId={projectId}&serverID={serverID}
        """
        ...

    async def health_check(self: Any) -> Dict[str, Any]:
        """
        Check if the facial recognition service is healthy
        """
        ...

    async def search_similar_faces(self: Any, face_embedding: List[float], threshold: float = 0.3, limit: int = 10, collection: str = 'staff_embeddings', location: str = '', timestamp: str = '') -> Dict[str, Any]:
        """
        Search for staff members by face embedding vector
        
        API: POST /v1/facial_recognition/search/similar?projectId={projectId}&serverID={serverID}
        
        Args:
            face_embedding: Face embedding vector
            collection: Vector collection name
            threshold: Similarity threshold (0.0 to 1.0)
            limit: Maximum number of results to return
            location: Location identifier for logging
            timestamp: Current timestamp in ISO format
        
        Returns:
            Dict containing search results with detectionType (known/unknown)
        """
        ...

    async def shutdown_service(self: Any, action_record_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Gracefully shutdown the service
        
                API: DELETE /v1/facial_recognition/shutdown?projectId={projectId}&serverID={serverID}
        """
        ...

    async def store_people_activity(self: Any, staff_id: str, detection_type: str, bbox: List[float], location: str, employee_id: Optional[str] = None, timestamp: str = datetime.now(timezone.utc).isoformat(), image_data: Optional[str] = None, camera_name: Optional[str] = None, camera_id: Optional[str] = None, rtp_number: Optional[str] = None) -> Dict[str, Any]:
        """
        Store people activity data with optional image data
        
        API: POST /v1/facial_recognition/store_people_activity?projectId={projectId}&serverID={serverID}
        
        Args:
            staff_id: Staff identifier (empty for unknown faces)
            detection_type: Type of detection (known, unknown, empty)
            bbox: Bounding box coordinates [x1, y1, x2, y2]
            location: Location identifier
            employee_id: Employee ID (for unknown faces, this will be generated)
            timestamp: Timestamp in ISO format
            image_data: Base64-encoded JPEG image data (optional)
        
        Returns:
            Dict containing response data with success status
        """
        ...

    async def update_deployment_action(self: Any, deployment_id: str) -> Dict[str, Any]:
        """
        Update deployment action in backend
        
                API: PUT /internal/v1/actions/update_facial_recognition_deployment/:server_id?app_deployment_id=:deployment_id
        
                Args:
                    deployment_id: The deployment ID to update
        
                Returns:
                    Dict containing response data
        """
        ...

    async def update_staff_images(self: Any, image_url: str, employee_id: str) -> Dict[str, Any]:
        """
        Update staff images with uploaded image URL
        
                API: PUT /v1/facial_recognition/staff/update_images?projectId={projectId}&serverID={serverID}
        """
        ...

    async def upload_image_to_url(self: Any, image_bytes: Any, upload_url: str) -> bool:
        """
        Upload image bytes to the provided URL
        """
        ...

