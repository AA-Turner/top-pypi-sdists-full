import asyncio
import base64
import logging
import os
import queue
import threading
import time
from typing import Any, Dict

import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None
from datetime import datetime, timezone

from .face_recognition_client import FacialRecognitionClient


# codeql[py/should-be-context-manager]
class PeopleActivityLogging:
    """Background logging system for face recognition activity"""

    def __init__(self, face_client: FacialRecognitionClient = None):
        self.face_client = face_client
        self.logger = logging.getLogger(__name__)

        # Log project ID information for observability and debugging
        face_client_project_id = getattr(self.face_client, "project_id", None) if self.face_client else None
        env_project_id = os.getenv("MATRICE_PROJECT_ID", "")
        self.logger.info(
            "[PROJECT_ID] PeopleActivityLogging initialized "
            f"with face_client.project_id='{face_client_project_id}', "
            f"MATRICE_PROJECT_ID env='{env_project_id}'"
        )

        # Use thread-safe queue for cross-thread communication (Python 3.8 compatibility)
        self.activity_queue = queue.Queue()

        # Thread for background processing
        self.processing_thread = None
        self.is_running = False

        # Empty detection tracking
        self.last_detection_time = time.time()
        self.empty_detection_logged = False
        self.empty_detection_threshold = 10.0  # 10 seconds

        # Storage for unknown faces (for debugging/backup)
        self.unknown_faces_storage = {}

        # Detection dedup keyed on (track_id, camera_id) when available,
        # falling back to (employee_id, camera_id). The track_id key prevents
        # spam from the same tracked person across multiple frames within the
        # cooldown window, and the fallback keeps backward compatibility for
        # detection payloads that don't carry a track_id.
        self.recent_employee_detections: Dict[str, float] = {}
        self.employee_detection_threshold = 10.0  # seconds

        # Start background processing
        self.start_background_processing()

    def start_background_processing(self):
        """Start the background processing thread"""
        if not self.is_running:
            self.is_running = True
            self.processing_thread = threading.Thread(target=self._run_async_loop, daemon=True)
            self.processing_thread.start()
            self.logger.info("Started PeopleActivityLogging background processing")

    def stop_background_processing(self):
        """Stop the background processing thread"""
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5.0)
            self.logger.info("Stopped PeopleActivityLogging background processing")

    def _run_async_loop(self):
        """Run the async event loop in the background thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._process_activity_queue())
        except Exception as e:
            self.logger.error(f"Error in background processing loop: {e}", exc_info=True)
        finally:
            try:
                loop.close()
            except Exception:
                # Non-fatal: exception ignored here; execution continues per surrounding logic.
                pass

    async def _process_activity_queue(self):
        """Process activity queue continuously"""
        while self.is_running:
            try:
                # Process queued detections with timeout using thread-safe queue
                try:
                    activity_data = self.activity_queue.get(timeout=20)
                    await self._process_activity(activity_data)
                    self.activity_queue.task_done()
                except queue.Empty:
                    # Continue loop to check for empty detections
                    continue

            except Exception as e:
                self.logger.error(f"Error processing activity queue: {e}", exc_info=True)
                await asyncio.sleep(1.0)

    async def enqueue_detection(
        self,
        detection: Dict,
        current_frame: np.ndarray | None = None,
        location: str = "",
        camera_name: str = "",
        camera_id: str = "",
        rtp_number: str = "",
        application_id: str = "",
    ):
        """Enqueue a detection for background processing"""
        try:
            activity_data = {
                "detection_type": detection["recognition_status"],  # known, unknown
                "detection": detection,
                "current_frame": current_frame,
                "location": location,
                "camera_name": camera_name,
                "camera_id": camera_id,
                "application_id": application_id,
                "rtp_number": rtp_number,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "employee_id": detection.get("employee_id", None),
                "staff_id": detection.get("person_id"),
                "track_id": detection.get("track_id"),
                "similarity_score": detection.get("similarity_score"),
            }
            if detection["recognition_status"] not in ["known", "unknown"]:
                self.logger.warning(f"Invalid detection status: {detection['recognition_status']}")
                return
            if not detection.get("employee_id", None):
                self.logger.warning(f"No employee_id found for detection: {detection}")
                return
            if not detection.get("person_id", None):
                self.logger.warning(f"No person_id found for detection: {detection}")
                return

            bbox = detection.get("bounding_box", {})
            bbox_list = [
                bbox.get("xmin", 0),
                bbox.get("ymin", 0),
                bbox.get("xmax", 0),
                bbox.get("ymax", 0),
            ]
            activity_data["bbox"] = bbox_list
            # Update last detection time
            self.last_detection_time = time.time()
            self.empty_detection_logged = False

            # Use thread-safe put (no await needed for queue.Queue)
            self.activity_queue.put(activity_data)
        except Exception as e:
            self.logger.error(f"Error enqueueing detection: {e}", exc_info=True)

    def _should_log_detection(
        self,
        employee_id: str,
        camera_id: str = "",
        track_id: str | None = None,
    ) -> bool:
        """
        Check whether a detection should be logged, given a cooldown window.

        Dedupe key precedence:
          1. (track_id, camera_id) when track_id is available — most precise:
             prevents the same tracked instance from logging repeatedly across
             frames within the cooldown.
          2. (employee_id, camera_id) when no track_id — falls back to
             employee-level dedupe.
          3. employee_id alone when camera_id is also missing.
        """
        current_time = time.time()
        if track_id:
            dedupe_key = f"track::{track_id}::{camera_id}"
        elif camera_id:
            dedupe_key = f"emp::{employee_id}::{camera_id}"
        else:
            dedupe_key = f"emp::{employee_id}"

        expired_keys = [
            key
            for key, timestamp in self.recent_employee_detections.items()
            if current_time - timestamp > self.employee_detection_threshold
        ]
        for key in expired_keys:
            del self.recent_employee_detections[key]

        if dedupe_key in self.recent_employee_detections:
            last_detection = self.recent_employee_detections[dedupe_key]
            if current_time - last_detection < self.employee_detection_threshold:
                self.logger.debug(
                    "Skipping logging key=%s - detected %.1fs ago",
                    dedupe_key,
                    current_time - last_detection,
                )
                return False

        self.recent_employee_detections[dedupe_key] = current_time
        return True

    async def _process_activity(self, activity_data: Dict):
        """Process activity data - handle all face detections with embedded image data"""
        detection_type = activity_data["detection_type"]
        current_frame = activity_data["current_frame"]
        bbox = activity_data["bbox"]
        employee_id = activity_data["employee_id"]
        location = activity_data["location"]
        staff_id = activity_data["staff_id"]
        timestamp = activity_data["timestamp"]
        camera_name = activity_data.get("camera_name", "")
        camera_id = activity_data.get("camera_id", "")
        application_id = activity_data.get("application_id", "")
        rtp_number = activity_data.get("rtp_number", "")
        similarity_score = activity_data.get("similarity_score")

        self.logger.debug(
            f"Processing activity - location: '{location}', camera_name: '{camera_name}', camera_id: '{camera_id}'"
        )
        try:
            if not self.face_client:
                self.logger.warning("Face client not available for activity logging")
                return None

            # Check if we should log this detection (avoid duplicates within time window)
            track_id = activity_data.get("track_id")
            if not self._should_log_detection(employee_id, camera_id=camera_id, track_id=track_id):
                self.logger.debug(
                    "Skipping activity log for employee_id=%s (camera_id=%s, track_id=%s) (within cooldown)",
                    employee_id,
                    camera_id,
                    track_id,
                )
                return None

            # Encode frame as base64 JPEG
            image_data = None
            if current_frame is not None:
                try:
                    self.logger.debug(f"Encoding frame as base64 JPEG - employee_id={employee_id}")
                    _, buffer = cv2.imencode(".jpg", current_frame)
                    frame_bytes = buffer.tobytes()
                    image_data = base64.b64encode(frame_bytes).decode("utf-8")
                    self.logger.debug(f"Encoded image data - employee_id={employee_id}, size={len(frame_bytes)} bytes")
                except Exception as e:
                    self.logger.error(
                        f"Error encoding frame for employee_id={employee_id}: {e}",
                        exc_info=True,
                    )

            # Store activity data with embedded image
            self.logger.info(
                f"Processing activity log - type={detection_type}, employee_id={employee_id}, staff_id={staff_id}, location={location}"
            )
            response = await self.face_client.store_people_activity(
                staff_id=staff_id,
                detection_type=detection_type,
                bbox=bbox,
                location=location,
                employee_id=employee_id,
                timestamp=timestamp,
                image_data=image_data,
                camera_name=camera_name,
                camera_id=camera_id,
                application_id=application_id,
                rtp_number=rtp_number,
                similarity_score=similarity_score,
            )

            if response and response.get("success", False):
                self.logger.info(f"Activity log stored successfully for employee_id={employee_id}")
            else:
                error_msg = response.get("error", "Unknown error") if response else "No response"
                self.logger.warning(f"Failed to store activity log for employee_id={employee_id} - {error_msg}")

            return response
        except Exception as e:
            self.logger.error(
                f"Error processing activity log for employee_id={employee_id}: {e}",
                exc_info=True,
            )
            return None

    async def _upload_frame(self, current_frame: np.ndarray, upload_url: str, employee_id: str):
        try:
            self.logger.debug(f"Encoding frame for upload - employee_id={employee_id}")
            _, buffer = cv2.imencode(".jpg", current_frame)
            frame_bytes = buffer.tobytes()

            self.logger.info(f"Uploading frame to storage - employee_id={employee_id}, size={len(frame_bytes)} bytes")
            upload_success = await self.face_client.upload_image_to_url(frame_bytes, upload_url)

            if upload_success:
                self.logger.info(f"Frame uploaded successfully for employee_id={employee_id}")
            else:
                self.logger.warning(f"Failed to upload frame for employee_id={employee_id}")
        except Exception as e:
            self.logger.error(
                f"Error uploading frame for employee_id={employee_id}: {e}",
                exc_info=True,
            )

    async def _should_log_activity(self, activity_data: Dict) -> bool:
        """Check if activity should be logged"""
        detection_type = activity_data["detection_type"]
        if detection_type == "known":
            return True
        return False

    def _crop_face_from_frame(self, frame: np.ndarray, bounding_box: Dict) -> bytes:
        """
        Crop face from frame using bounding box and return as bytes

        Args:
            frame: Original frame as numpy array
            bounding_box: Dict with x1, y1, x2, y2 coordinates

        Returns:
            bytes: Cropped face image as JPEG bytes
        """
        try:
            # Extract coordinates - handle different bounding box formats
            x1 = int(bounding_box.get("xmin", bounding_box.get("x1", 0)))
            y1 = int(bounding_box.get("ymin", bounding_box.get("y1", 0)))
            x2 = int(bounding_box.get("xmax", bounding_box.get("x2", 0)))
            y2 = int(bounding_box.get("ymax", bounding_box.get("y2", 0)))

            # Ensure coordinates are within frame bounds
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            # Validate coordinates
            if x2 <= x1 or y2 <= y1:
                self.logger.warning("Invalid bounding box coordinates")
                return b""

            # Crop the face
            cropped_face = frame[y1:y2, x1:x2]

            # Convert to JPEG bytes
            _, buffer = cv2.imencode(".jpg", cropped_face)
            return buffer.tobytes()

        except Exception as e:
            self.logger.error(f"Error cropping face from frame: {e}", exc_info=True)
            return b""

    def get_unknown_faces_storage(self) -> Dict[str, bytes]:
        """Get stored unknown face images as bytes"""
        return self.unknown_faces_storage.copy()

    def clear_unknown_faces_storage(self) -> None:
        """Clear stored unknown face images"""
        self.unknown_faces_storage.clear()

    def __enter__(self) -> "PeopleActivityLogging":
        return self

    def __exit__(self, _exc_type: Any, _exc: Any, _tb: Any) -> None:
        return None

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.stop_background_processing()
        except Exception:
            # Non-fatal: exception ignored here; execution continues per surrounding logic.
            pass
