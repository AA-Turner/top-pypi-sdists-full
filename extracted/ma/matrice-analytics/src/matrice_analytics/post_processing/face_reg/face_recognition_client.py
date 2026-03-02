#!/usr/bin/env python3
"""
Facial Recognition API - Python Client for Post-Processing

This client handles vector search and enrollment operations for face recognition
in the post-processing pipeline using Matrice Session.
"""

import os
import re
import base64
import logging
import httpx
import urllib
import urllib.request
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from pathlib import Path

# Import matrice session
try:
    from  matrice_common.session import Session
    HAS_MATRICE_SESSION = True
except ImportError:
    HAS_MATRICE_SESSION = False
    logging.warning("Matrice session not available")


class FacialRecognitionClient:
    """
    Simplified Face Recognition Client using Matrice Session.
    All API calls are made through the Matrice session RPC interface.
    """
    
    # Pattern for matching action IDs (hex strings of at least 8 characters)
    ACTION_ID_PATTERN = re.compile(r"^[0-9a-f]{8,}$", re.IGNORECASE)

    @classmethod
    def _discover_action_id(cls) -> Optional[str]:
        """Discover action_id from current working directory name (and parents)."""
        candidates: List[str] = []
        try:
            cwd = Path.cwd()
            candidates.append(cwd.name)
            for parent in cwd.parents:
                candidates.append(parent.name)
        except Exception:
            pass

        try:
            usr_src = Path("/usr/src")
            if usr_src.exists():
                for child in usr_src.iterdir():
                    if child.is_dir():
                        candidates.append(child.name)
        except Exception:
            pass

        for candidate in candidates:
            if candidate and len(candidate) >= 8 and cls.ACTION_ID_PATTERN.match(candidate):
                return candidate
        return None

    def _fetch_project_id_from_action(self) -> Optional[str]:
        """
        Fetch project ID from action details using discovered action ID.
        
        This method discovers the action ID from the working directory name,
        fetches action details from the API, and extracts the _idProject field.
        If successful, it also updates the MATRICE_PROJECT_ID environment variable.
        
        Returns:
            The project ID string if found, None otherwise.
        """
        action_id = self._discover_action_id()
        if not action_id:
            self.logger.warning("[PROJECT_ID] Could not discover action_id from folder name")
            return None
        
        self.logger.info(f"[PROJECT_ID] Discovered action_id from folder: {action_id}")
        
        try:
            url = f"/v1/actions/action/{action_id}/details"
            self.logger.info(f"[PROJECT_ID] Fetching action details from: {url}")
            response = self.session.rpc.get(url)
            
            if response and response.get("success", False) and response.get("code") == 200:
                data = response.get("data", {})
                project_id = data.get("_idProject", "")
                
                if project_id:
                    self.logger.info(f"[PROJECT_ID] Successfully fetched project ID from action details: {project_id}")
                    # Update environment variable so other components can use it
                    os.environ["MATRICE_PROJECT_ID"] = project_id
                    self.logger.info(f"[PROJECT_ID] Updated MATRICE_PROJECT_ID environment variable: {project_id}")
                    return project_id
                else:
                    self.logger.warning(f"[PROJECT_ID] _idProject not found in action details for action_id={action_id}")
            else:
                error_msg = response.get('message', 'Unknown error') if response else 'Empty response'
                self.logger.warning(f"[PROJECT_ID] Failed to fetch action details: {error_msg}")
        except Exception as e:
            self.logger.error(f"[PROJECT_ID] Error fetching action details for action_id={action_id}: {e}", exc_info=True)
        
        return None

    def __init__(self, account_number: str = "", access_key: str = "", secret_key: str = "", 
                 project_id: str = "", server_id: str = "", session=None):

        # Set up logging
        self.logger = logging.getLogger(__name__)

        self.server_id = server_id
        if not self.server_id:
            raise ValueError("Server ID is required for Face Recognition Client")

        self.server_info = None
        self.server_base_url = None
        self.public_ip = self._get_public_ip()

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
        
        # If project_id is still empty, try to fetch from action details
        if not self.project_id:
            self.logger.info("[PROJECT_ID] Project ID is empty, attempting to fetch from action details...")
            fetched_project_id = self._fetch_project_id_from_action()
            if fetched_project_id:
                self.project_id = fetched_project_id
                self.logger.info(f"[PROJECT_ID] Successfully set project_id from action details: {self.project_id}")
                # Update session with the new project_id if possible
                if hasattr(self.session, 'update'):
                    try:
                        self.session.update(self.project_id)
                        self.logger.info(f"[PROJECT_ID] Updated session with project_id: {self.project_id}")
                    except Exception as e:
                        self.logger.warning(f"[PROJECT_ID] Failed to update session with project_id: {e}")
            else:
                self.logger.warning("[PROJECT_ID] Could not fetch project_id from action details")

        # Fetch server connection info if server_id is provided
        if self.server_id:
            try:
                self.server_info = self.get_server_connection_info()
                if self.server_info:
                    self.logger.info(f"Successfully fetched facial recognition server info: {self.server_info.get('name', 'Unknown')}")
                    # Compare server host with public IP to determine if it's localhost
                    server_host = self.server_info.get('host', 'localhost')
                    server_port = self.server_info.get('port', 8081)
                    
                    if server_host == self.public_ip:
                        self.server_base_url = f"http://localhost:{server_port}"
                        self.logger.warning(f"Server host matches public IP, using localhost: {self.server_base_url}")
                    else:
                        self.server_base_url = f"http://{server_host}:{server_port}"
                        self.logger.warning(f"Facial recognition server base URL: {self.server_base_url}")
                    
                    # Update project_id from server_info if available and current project_id is empty
                    server_project_id = self.server_info.get('projectID', '')
                    if server_project_id:
                        if not self.project_id:
                            self.project_id = server_project_id
                            self.logger.info(f"[PROJECT_ID] Set project_id from server_info: {self.project_id}")
                            # Update environment variable
                            os.environ["MATRICE_PROJECT_ID"] = self.project_id
                            self.logger.info(f"[PROJECT_ID] Updated MATRICE_PROJECT_ID env var from server_info: {self.project_id}")
                        self.session.update(server_project_id)
                        self.logger.info(f"Updated Matrice session with project ID: {server_project_id}")
                    else:
                        self.logger.warning("[PROJECT_ID] server_info.projectID is empty")
                else:
                    self.logger.warning("Failed to fetch facial recognition server connection info")
            except Exception as e:
                self.logger.error(f"Error fetching facial recognition server connection info: {e}", exc_info=True)
        
        # Final check: log the project_id status
        if self.project_id:
            self.logger.info(f"[PROJECT_ID] Final project_id: {self.project_id}")
        else:
            self.logger.error("[PROJECT_ID] WARNING: project_id is still empty after all initialization attempts!")
    
    def _get_public_ip(self) -> str:
        """Get the public IP address of this machine."""
        try:
            public_ip = urllib.request.urlopen("https://v4.ident.me", timeout=120).read().decode("utf8").strip()
            self.logger.warning(f"Successfully fetched external IP: {public_ip}")
            return public_ip
        except Exception as e:
            self.logger.error(f"Error fetching external IP: {e}", exc_info=True)
            return "localhost"

    def get_server_connection_info(self) -> Optional[Dict[str, Any]]:
        """Fetch server connection info from RPC."""
        if not self.server_id:
            return None
        
        try:
            response = self.session.rpc.get(f"/v1/actions/get_facial_recognition_server/{self.server_id}")
            if response.get("success", False) and response.get("code") == 200:
                # Response format:
                # {'success': True, 'code': 200, 'message': 'Success', 'serverTime': '2025-10-21T09:56:14Z',
                #  'data': {'id': '68f28be1f74ae116727448c4', 'name': 'Local Server', 'host': '68.36.82.163', 'port': 8081, 'status': 'active', 'accountNumber': '3823255831182978487149732',
                #           'projectID': '68aff0bbce98491879437909', 'region': 'United States', 'isShared': False}}
                return response.get("data", {})
            else:
                self.logger.warning(f"Failed to fetch server info: {response.get('message', 'Unknown error')}")
                return None
        except Exception as e:
            self.logger.error(f"Exception while fetching server connection info: {e}", exc_info=True)
            return None

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
        """Enroll staff with base64 encoded images
        
        API: POST /v1/facial_recognition/staff/enroll?projectId={projectId}&serverID={serverID}
        """

        # Prepare enrollment request matching API spec
        enrollment_request = {
            "staffId": staff_data.get("staffId", ""),
            "firstName": staff_data.get("firstName", ""),
            "lastName": staff_data.get("lastName", ""),
            "email": staff_data.get("email", ""),
            "position": staff_data.get("position", ""),
            "department": staff_data.get("department", ""),
            "images": base64_images
        }

        self.logger.info(f"API REQUEST: Enrolling staff with {len(base64_images)} images - Staff ID: {staff_data.get('staffId', 'N/A')}")
        self.logger.debug(f"Enrollment request payload: {list(enrollment_request.keys())}, num_images={len(base64_images)}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="POST",
                path=f"/v1/facial_recognition/staff/enroll?projectId={self.project_id}&serverID={self.server_id}",
                payload=enrollment_request,
                base_url=self.server_base_url
            )
            self.logger.info(f"API RESPONSE: Staff enrollment completed - Success: {response.get('success', False)}")
            if not response.get('success', False):
                self.logger.warning(f"Staff enrollment failed: {response.get('error', 'Unknown error')}")
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Staff enrollment request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def search_similar_faces(self, face_embedding: List[float], 
                           threshold: float = 0.3, limit: int = 10, 
                           collection: str = "staff_enrollment",
                           location: str = "",
                           timestamp: str = "") -> Dict[str, Any]:
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
        search_request = {
            "embedding": face_embedding,
            "collection": collection,
            "threshold": threshold,
            "limit": limit,
            "images_required":False,
        }
        
        # Add optional fields only if provided
        if location:
            search_request["location"] = location
        if timestamp:
            search_request["timestamp"] = timestamp

        self.logger.debug(f"API REQUEST: Searching similar faces - threshold={threshold}, limit={limit}, collection={collection}, location={location}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="POST",
                path=f"/v1/facial_recognition/search/similar?projectId={self.project_id}&serverID={self.server_id}",
                payload=search_request,
                base_url=self.server_base_url
            )
            
            results_count = 0
            if response.get('success', False):
                data = response.get('data', [])
                results_count = len(data) if isinstance(data, list) else 0
                self.logger.info(f"API RESPONSE: Face search completed - Found {results_count} matches")
                if results_count > 0:
                    self.logger.debug(f"Top match: staff_id={data[0].get('staffId', 'N/A')}, score={data[0].get('score', 0):.3f}")
            else:
                self.logger.warning(f"Face search failed: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Face search request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def get_staff_details(self, staff_id: str) -> Dict[str, Any]:
        """Get full staff details by staff ID
        
        API: GET /v1/facial_recognition/staff/:staffId?projectId={projectId}&serverID={serverID}
        """

        self.logger.debug(f"API REQUEST: Getting staff details - staff_id={staff_id}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="GET",
                path=f"/v1/facial_recognition/staff/{staff_id}?projectId={self.project_id}&serverID={self.server_id}",
                payload={},
                base_url=self.server_base_url
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Staff details retrieved successfully - staff_id={staff_id}")
            else:
                self.logger.warning(f"Failed to get staff details for staff_id={staff_id}: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Get staff details request failed for staff_id={staff_id} - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def store_people_activity(self, 
                                  staff_id: str,
                                  detection_type: str,
                                  bbox: List[float],
                                  location: str,
                                  employee_id: Optional[str] = None,
                                  timestamp: str = datetime.now(timezone.utc).isoformat(),
                                  image_data: Optional[str] = None,
                                  camera_name: Optional[str] = None,
                                  camera_id: Optional[str] = None,
                                  ) -> Dict[str, Any]:
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
        activity_request = {
            "staff_id": staff_id,
            "type": detection_type,
            "timestamp": timestamp,
            "bbox": bbox,
            "location": location,
            "camera_name": camera_name,
            "camera_id": camera_id,
        }

        # Add optional fields if provided based on API spec
        if detection_type == "unknown" and employee_id:
            activity_request["anonymous_id"] = employee_id
        elif detection_type == "known" and employee_id:
            activity_request["employee_id"] = employee_id
        
        # Add image data if provided
        if image_data:
            activity_request["imageData"] = image_data
        
        self.logger.info(f"API REQUEST: Storing people activity - type={detection_type}, staff_id={staff_id}, location={location}, camera_name={camera_name}, camera_id={camera_id}, has_image={bool(image_data)}")
        self.logger.debug(f"Activity request payload: bbox={bbox}, employee_id={employee_id}, camera_name={camera_name}, camera_id={camera_id}")
        
        try:
            response = await self.session.rpc.async_send_request(
                method="POST",
                path=f"/v1/facial_recognition/store_people_activity?projectId={self.project_id}&serverID={self.server_id}",
                payload=activity_request,
                base_url=self.server_base_url
            )
            handled_response = self._handle_response(response)
            
            if handled_response.get("success", False):
                self.logger.info(f"API RESPONSE: Successfully stored {detection_type} activity for staff_id={staff_id}")
                return handled_response
            else:
                self.logger.warning(f"Failed to store {detection_type} activity: {handled_response.get('error', 'Unknown error')}")
                return handled_response
        except Exception as e:
            self.logger.error(f"API ERROR: Store people activity request failed - type={detection_type}, staff_id={staff_id} - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def update_staff_images(self, image_url: str, employee_id: str) -> Dict[str, Any]:
        """Update staff images with uploaded image URL
        
        API: PUT /v1/facial_recognition/staff/update_images?projectId={projectId}&serverID={serverID}
        """

        update_request = {
            "imageUrl": image_url,
            "employeeId": employee_id
        }

        self.logger.info(f"API REQUEST: Updating staff images - employee_id={employee_id}")
        self.logger.debug(f"Update request: image_url={image_url[:50]}...")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="PUT",
                path=f"/v1/facial_recognition/staff/update_images?projectId={self.project_id}&serverID={self.server_id}",
                payload=update_request,
                base_url=self.server_base_url
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Staff images updated successfully - employee_id={employee_id}")
            else:
                self.logger.warning(f"Failed to update staff images for employee_id={employee_id}: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Update staff images request failed - employee_id={employee_id} - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def upload_image_to_url(self, image_bytes: bytes, upload_url: str) -> bool:
        """Upload image bytes to the provided URL"""
        try:
            self.logger.info(f"API REQUEST: Uploading image to URL - size={len(image_bytes)} bytes")
            self.logger.debug(f"Upload URL: {upload_url[:100]}...")
            
            # Upload the image to the signed URL using async httpx
            headers = {'Content-Type': 'image/jpeg'}
            async with httpx.AsyncClient() as client:
                response = await client.put(upload_url, content=image_bytes, headers=headers)

            if response.status_code in [200, 201]:
                self.logger.info(f"API RESPONSE: Successfully uploaded image - status={response.status_code}")
                return True
            else:
                self.logger.error(f"API ERROR: Failed to upload image - status={response.status_code}, response={response.text[:200]}")
                return False

        except Exception as e:
            self.logger.error(f"API ERROR: Exception during image upload - {e}", exc_info=True)
            return False

    async def shutdown_service(self, action_record_id: Optional[str] = None) -> Dict[str, Any]:
        """Gracefully shutdown the service
        
        API: DELETE /v1/facial_recognition/shutdown?projectId={projectId}&serverID={serverID}
        """

        payload = {} if not action_record_id else {"actionRecordId": action_record_id}

        self.logger.info(f"API REQUEST: Shutting down service - action_record_id={action_record_id}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="DELETE",
                path=f"/v1/facial_recognition/shutdown?projectId={self.project_id}&serverID={self.server_id}",
                payload=payload,
                base_url=self.server_base_url
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Service shutdown successful")
            else:
                self.logger.warning(f"Service shutdown failed: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Shutdown service request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def get_all_staff_embeddings(self) -> Dict[str, Any]:
        """Get all staff embeddings
        
        API: GET /v1/facial_recognition/get_all_staff_embeddings?projectId={projectId}&serverID={serverID}
        """

        payload = {}

        self.logger.info(f"API REQUEST: Getting all staff embeddings")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="GET",
                path=f"/v1/facial_recognition/get_all_staff_embeddings?projectId={self.project_id}&serverID={self.server_id}",
                payload=payload,
                base_url=self.server_base_url
            )
            
            embeddings_count = 0
            if response:
                # Handle both list and dict responses
                if isinstance(response, list):
                    # API returned list directly
                    data = response
                    embeddings_count = len(data)
                    self.logger.info(f"API RESPONSE: Retrieved {embeddings_count} staff embeddings (list format)")
                    # Return in standard format for consistency
                    return {"success": True, "data": data}
                elif isinstance(response, dict):
                    # API returned dict with 'data' key
                    data = response.get('data', [])
                    embeddings_count = len(data) if isinstance(data, list) else 0
                    self.logger.info(f"API RESPONSE: Retrieved {embeddings_count} staff embeddings (dict format)")
                    return self._handle_response(response)
                else:
                    self.logger.error(f"Unexpected response type: {type(response)}")
                    return {"success": False, "error": f"Unexpected response type: {type(response)}"}
            else:
                error_msg = response.get('error', 'Unknown error') if isinstance(response, dict) else 'Empty response'
                self.logger.warning(f"Failed to get staff embeddings: {error_msg}")
                return {"success": False, "error": error_msg}
            
        except Exception as e:
            self.logger.error(f"API ERROR: Get all staff embeddings request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    async def update_deployment_action(self, deployment_id: str) -> Dict[str, Any]:
        """Update deployment action in backend
        
        API: PUT /internal/v1/actions/update_facial_recognition_deployment/:server_id?app_deployment_id=:deployment_id
        
        Args:
            deployment_id: The deployment ID to update
            
        Returns:
            Dict containing response data
        """
        if not deployment_id:
            self.logger.warning("No deployment_id provided for update_deployment_action")
            return {"success": False, "error": "deployment_id is required"}

        self.logger.info(f"API REQUEST: Updating deployment action - deployment_id={deployment_id}")

        # Use Matrice session for async RPC call to backend (not facial recognition server).
        try:
            response = await self.session.rpc.async_send_request(
                method="PUT",
                path=f"/v1/actions/update_facial_recognition_deployment/{self.server_id}?app_deployment_id={deployment_id}",
                payload={},
                base_url="https://prod.backend.app.matrice.ai"
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Deployment action updated successfully - deployment_id={deployment_id}")
            else:
                self.logger.warning(f"Failed to update deployment action for deployment_id={deployment_id}: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Update deployment action request failed - deployment_id={deployment_id} - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def update_deployment(self, deployment_id: str) -> Dict[str, Any]:
        """Update deployment to notify facial recognition server
        
        API: PUT /v1/facial_recognition/update_deployment/:deployment_id
        
        Args:
            deployment_id: The deployment ID to update
            
        Returns:
            Dict containing response data
        """
        if not deployment_id:
            self.logger.warning("No deployment_id provided for update_deployment")
            return {"success": False, "error": "deployment_id is required"}

        self.logger.info(f"API REQUEST: Updating deployment - deployment_id={deployment_id}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="PUT",
                path=f"/v1/facial_recognition/update_deployment/{deployment_id}",
                payload={},
                base_url=self.server_base_url
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Deployment updated successfully - deployment_id={deployment_id}")
            else:
                self.logger.warning(f"Failed to update deployment for deployment_id={deployment_id}: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Update deployment request failed - deployment_id={deployment_id} - {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    async def enroll_unknown_person(self, embedding: List[float], image_source: str = None, timestamp: str = None, location: str = None, employee_id: str = None) -> Dict[str, Any]:
        """Enroll an unknown person
        
        API: POST /v1/facial_recognition/enroll_unknown_person?projectId={projectId}&serverID={serverID}
        """

        payload = {
            "embedding": embedding
        }
        
        # Add optional fields based on API spec
        if image_source:
            payload["imageSource"] = image_source
        if timestamp:
            payload["timestamp"] = timestamp
        else:
            payload["timestamp"] = datetime.now(timezone.utc).isoformat()
        if location:
            payload["location"] = location

        self.logger.info(f"API REQUEST: Enrolling unknown person - location={location}")
        self.logger.debug(f"Unknown enrollment payload: has_embedding={bool(embedding)}, has_image_source={bool(image_source)}")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="POST",
                path=f"/v1/facial_recognition/enroll_unknown_person?projectId={self.project_id}&serverID={self.server_id}",
                payload=payload,
                base_url=self.server_base_url
            )
            
            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Unknown person enrolled successfully")
            else:
                self.logger.warning(f"Failed to enroll unknown person: {response.get('error', 'Unknown error')}")
            
            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Enroll unknown person request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """Check if the facial recognition service is healthy"""

        self.logger.debug(f"API REQUEST: Health check")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="GET",
                path=f"/v1/facial_recognition/health?serverID={self.server_id}",
                payload={},
                base_url=self.server_base_url
            )

            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Service is healthy")
            else:
                self.logger.warning(f"Health check failed: {response.get('error', 'Unknown error')}")

            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Health check request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    async def get_redis_details(self) -> Dict[str, Any]:
        """Get Redis connection details from facial recognition server

        API: GET /v1/facial_recognition/get_redis_details

        Returns:
            Dict containing Redis connection details (REDIS_IP, REDIS_PORT, REDIS_PASSWORD)
        """

        self.logger.info(f"API REQUEST: Getting Redis connection details")

        # Use Matrice session for async RPC call
        try:
            response = await self.session.rpc.async_send_request(
                method="GET",
                path=f"/v1/facial_recognition/get_redis_details",
                payload={},
                base_url=self.server_base_url
            )

            if response.get('success', False):
                self.logger.info(f"API RESPONSE: Redis details retrieved successfully")
            else:
                self.logger.warning(f"Failed to get Redis details: {response.get('error', 'Unknown error')}")

            return self._handle_response(response)
        except Exception as e:
            self.logger.error(f"API ERROR: Get Redis details request failed - {e}", exc_info=True)
            return {"success": False, "error": str(e)}

    def _handle_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle RPC response and errors"""
        try:
            if response:
                return response
            else:
                error_msg = response #.get("error", "Unknown RPC error")
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