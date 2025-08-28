#!/usr/bin/env python3
"""
Facial Recognition API - Python Client for Post-Processing

This client handles vector search and enrollment operations for face recognition
in the post-processing pipeline using Matrice Session.
"""

import os
import base64
import logging
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

# Import matrice session
try:
    from matrice.session import Session
    HAS_MATRICE_SESSION = True
except ImportError:
    HAS_MATRICE_SESSION = False
    logging.warning("Matrice session not available")


class FacialRecognitionClient:
    """
    Simplified Face Recognition Client using Matrice Session.
    All API calls are made through the Matrice session RPC interface.
    """

    def __init__(self, account_number: str = "", access_key: str = "", secret_key: str = "", 
                 project_id: str = "", server_id: str = "", session=None):

        # Set up logging
        self.logger = logging.getLogger(__name__)

        self.server_id = server_id
        if not self.server_id:
            raise ValueError("Server ID is required for Face Recognition Client")

        # Use existing session if provided, otherwise create new one
        if session is not None:
            self.session = session
            # Get project_id from session or parameter
            self.project_id = getattr(session, 'project_id', '') or project_id or os.getenv("MATRICE_PROJECT_ID", "")
            self.logger.info("Using existing Matrice session for face recognition client")
        else:
            # Initialize credentials from environment if not provided
            self.account_number = account_number or os.getenv("MATRICE_ACCOUNT_NUMBER", "")
            self.access_key = access_key or os.getenv("MATRICE_ACCESS_KEY_ID", "")
            self.secret_key = secret_key or os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
            self.project_id = project_id or os.getenv("MATRICE_PROJECT_ID", "")

            # Initialize Matrice session
            if not HAS_MATRICE_SESSION:
                raise ImportError("Matrice session is required for Face Recognition Client")

            # if not all([self.account_number, self.access_key, self.secret_key]):
            #     raise ValueError("Missing required credentials: account_number, access_key, secret_key")

            try:
                self.session = Session(
                    account_number=self.account_number,
                    access_key=self.access_key,
                    secret_key=self.secret_key,
                    project_id=self.project_id,
                )
                self.logger.info("Initialized new Matrice session for face recognition client")
            except Exception as e:
                self.logger.error(f"Failed to initialize Matrice session: {e}", exc_info=True)
                raise

    async def enroll_staff(self, staff_data: Dict[str, Any], image_paths: List[str]) -> Dict[str, Any]:
        """
        Enroll a new staff member with face images
        
        Args:
            staff_data: Dictionary containing staff information (staffId, firstName, lastName, etc.)
            image_paths: List of file paths to face images
            
        Returns:
            Dict containing enrollment response
        """
        # Convert images to base64
        base64_images = []
        for image_path in image_paths:
            try:
                with open(image_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    base64_images.append(base64_image)
            except Exception as e:
                self.logger.error(f"Error reading image {image_path}: {e}", exc_info=True)
                return {"success": False, "error": f"Failed to read image: {e}"}

        return await self.enroll_staff_base64(staff_data, base64_images)

    async def enroll_staff_base64(self, staff_data: Dict[str, Any], base64_images: List[str]) -> Dict[str, Any]:
        """Enroll staff with base64 encoded images"""

        # Prepare enrollment request
        enrollment_request = {
            "staff_info": staff_data,
            "images": base64_images
        }

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="POST",
            path=f"/v1/actions/facial_recognition/staff/enroll?serverID={self.server_id}",
            payload=enrollment_request
        )
        return self._handle_response(response)

    async def search_similar_faces(self, face_embedding: List[float], 
                           threshold: float = 0.3, limit: int = 10, 
                           collection: str = "staff_enrollment",
                           location: str = "",
                           timestamp: str = "") -> Dict[str, Any]:
        """
        Search for staff members by face embedding vector
        
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
        search_request = {
            "embedding": face_embedding,
            "collection": collection,
            "threshold": threshold,
            "limit": limit,
            "location": location,
            "timestamp": timestamp
        }

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="POST",
            path=f"/v1/actions/facial_recognition/search/similar?serverID={self.server_id}",
            payload=search_request
        )
        return self._handle_response(response)

    async def get_staff_details(self, staff_id: str) -> Dict[str, Any]:
        """Get full staff details by staff ID"""

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="GET",
            path=f"/v1/actions/facial_recognition/staff/{staff_id}?serverID={self.server_id}",
            payload={}
        )
        return self._handle_response(response)

    async def store_people_activity(self, 
                                  staff_id: str,
                                  detection_type: str,
                                  bbox: List[float],
                                  location: str,
                                  employee_id: Optional[str] = None,
                                  timestamp: str = datetime.now(timezone.utc).isoformat(),
                                  ) -> str | None:
        """
        Store people activity data and return response with potential upload URLs
        
        Args:
            staff_id: Staff identifier (empty for unknown faces)
            detection_type: Type of detection (known, unknown, empty)
            bbox: Bounding box coordinates [x1, y1, x2, y2]
            location: Location identifier
            employee_id: Employee ID (for unknown faces, this will be generated)
            timestamp: Timestamp in ISO format
            
        Returns:
            Dict containing response data including uploadUrl and employeeId for unknown faces,
            or None if the request failed
        """
        activity_request = {
            "staff_id": staff_id,
            "type": detection_type,
            "timestamp": timestamp,
            "bbox": bbox,
            "location": location,
        }

        # Add optional fields if provided
        if detection_type == "unknown":
            if employee_id:
                activity_request["anonymous_id"] = employee_id
        elif detection_type == "known" and employee_id:
            activity_request["employee_id"] = employee_id
        response = await self.session.rpc.async_send_request(
            method="POST",
            path=f"/v1/actions/facial_recognition/store_people_activity?serverID={self.server_id}",
            payload=activity_request
        )
        handled_response = self._handle_response(response)
        if handled_response.get("success", False):
            data = handled_response.get("data", {})
            self.logger.debug(f"Successfully stored {detection_type} activity")
            if not data:
                self.logger.warning("No data returned form store people activity")
                return None
            return data
        else:
            self.logger.error(f"Failed to store {detection_type} activity: {handled_response.get('error', 'Unknown error')}")
            return None

    async def update_staff_images(self, image_url: str, employee_id: str) -> Dict[str, Any]:
        """Update staff images with uploaded image URL"""

        update_request = {
            "imageUrl": image_url,
            "employeeId": employee_id
        }

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="PUT",
            path=f"/v1/actions/facial_recognition/update_staff_images?serverID={self.server_id}",
            payload=update_request
        )
        return self._handle_response(response)

    async def upload_image_to_url(self, image_bytes: bytes, upload_url: str) -> bool:
        """Upload image bytes to the provided URL"""
        try:
            # Upload the image to the signed URL using async httpx
            headers = {'Content-Type': 'image/jpeg'}
            async with httpx.AsyncClient() as client:
                response = await client.put(upload_url, content=image_bytes, headers=headers)

            if response.status_code in [200, 201]:
                self.logger.debug(f"Successfully uploaded image to URL")
                return True
            else:
                self.logger.error(f"Failed to upload image: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            self.logger.error(f"Error uploading image to URL: {e}", exc_info=True)
            return False

    async def shutdown_service(self, action_record_id: Optional[str] = None) -> Dict[str, Any]:
        """Gracefully shutdown the service"""

        payload = {} if not action_record_id else {"actionRecordId": action_record_id}

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="DELETE",
            path=f"/v1/actions/facial_recognition/shutdown?serverID={self.server_id}",
            payload=payload
        )
        return self._handle_response(response)

    async def get_all_staff_embeddings(self) -> Dict[str, Any]:
        """Get all staff embeddings"""

        payload = {}

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="GET",
            path=f"/v1/actions/facial_recognition/get_all_staff_embeddings?serverID={self.server_id}",
            payload=payload,
        )
        return self._handle_response(response)
    
    async def enroll_unknown_person(self, embedding: List[float], image_source: str = None, timestamp: str = None, location: str = None, employee_id: str = None) -> Dict[str, Any]:
        """Enroll an unknown person"""

        payload = {
            "embedding": embedding
        }
        
        if image_source:
            payload["imageSource"] = image_source
        if timestamp:
            payload["timestamp"] = timestamp
        else:
            payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        if location:
            payload["location"] = location
        if employee_id:
            payload["employeeId"] = employee_id

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="POST",
            path=f"/v1/actions/facial_recognition/enroll_unknown_person?serverID={self.server_id}",
            payload=payload,
        )
        return self._handle_response(response)

    async def health_check(self) -> Dict[str, Any]:
        """Check if the facial recognition service is healthy"""

        # Use Matrice session for async RPC call
        response = await self.session.rpc.async_send_request(
            method="GET",
            path=f"/v1/actions/facial_recognition/health?serverID={self.server_id}",
            payload={}
        )
        return self._handle_response(response)

    def _handle_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle RPC response and errors"""
        try:
            if response.get("success", True):
                return response
            else:
                error_msg = response.get("error", "Unknown RPC error")
                self.logger.error(f"RPC Error: {error_msg}", exc_info=True)
                return {"success": False, "error": error_msg}
        except Exception as e:
            self.logger.error(f"Error handling RPC response: {e}", exc_info=True)
            return {"success": False, "error": f"Response handling error: {e}"}


# Factory function for easy initialization
def create_face_client(account_number: str = None, access_key: str = None, 
                      secret_key: str = None, project_id: str = None, 
                      server_id: str = "", session=None) -> FacialRecognitionClient:
    """Create a facial recognition client with automatic credential detection"""
    return FacialRecognitionClient(
        account_number=account_number,
        access_key=access_key,
        secret_key=secret_key,
        project_id=project_id,
        server_id=server_id,
        session=session
    )
