import asyncio
import logging
import time
import threading
from typing import Dict, Optional, Set
import numpy as np
import cv2
from datetime import datetime, timezone
from .face_recognition_client import FacialRecognitionClient


class PeopleActivityLogging:
    """Background logging system for face recognition activity"""

    def __init__(self, face_client: FacialRecognitionClient = None):
        self.face_client = face_client
        self.logger = logging.getLogger(__name__)

        # Queue for processing detections in background
        self.activity_queue = asyncio.Queue()

        # Thread for background processing
        self.processing_thread = None
        self.is_running = False

        # Empty detection tracking
        self.last_detection_time = time.time()
        self.empty_detection_logged = False
        self.empty_detection_threshold = 10.0  # 10 seconds

        # Storage for unknown faces (for debugging/backup)
        self.unknown_faces_storage = {}

        # Employee ID tracking with timestamps to prevent duplicate logging
        # TODO: Make this use track_id or similarity check instead of employee_id for better deduplication
        self.recent_employee_detections: Dict[str, float] = {}
        self.employee_detection_threshold = 10.0  # 10 seconds

        # Start background processing
        self.start_background_processing()

    def start_background_processing(self):
        """Start the background processing thread"""
        if not self.is_running:
            self.is_running = True
            self.processing_thread = threading.Thread(
                target=self._run_async_loop, daemon=True
            )
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
            except:
                pass

    async def _process_activity_queue(self):
        """Process activity queue continuously"""
        while self.is_running:
            try:
                # Process queued detections with timeout
                try:
                    activity_data = await asyncio.wait_for(
                        self.activity_queue.get(), timeout=20
                    )
                    await self._process_activity(activity_data)
                    self.activity_queue.task_done()
                except asyncio.TimeoutError:
                    # Continue loop to check for empty detections
                    continue

            except Exception as e:
                self.logger.error(f"Error processing activity queue: {e}", exc_info=True)
                await asyncio.sleep(1.0)

    async def enqueue_detection(
        self,
        detection: Dict,
        current_frame: Optional[np.ndarray] = None,
        location: str = "",
    ):
        """Enqueue a detection for background processing"""
        try:
            activity_data = {
                "detection_type": detection["recognition_status"],  # known, unknown
                "detection": detection,
                "current_frame": current_frame,
                "location": location,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "employee_id": detection.get("employee_id", None),
                "staff_id": detection.get("person_id")
            }
            if detection["recognition_status"] not in ["known", "unknown"]:
                self.logger.warning(
                    f"Invalid detection status: {detection['recognition_status']}"
                )
                return
            if not detection.get("employee_id", None):
                self.logger.warning(
                    f"No employee_id found for detection: {detection}"
                )
                return
            if not detection.get("person_id", None):
                self.logger.warning(
                    f"No person_id found for detection: {detection}"
                )
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

            await self.activity_queue.put(activity_data)
        except Exception as e:
            self.logger.error(f"Error enqueueing detection: {e}", exc_info=True)

    def _should_log_detection(self, employee_id: str) -> bool:
        """
        Check if detection should be logged based on employee ID and time threshold.
        Only log if employee_id was not detected in the past 10 seconds.
        
        TODO: Make this use track_id or similarity check instead of just employee_id in 10 secs window
        for better deduplication across different detection sessions.
        """
        current_time = time.time()
        
        # Clean up old entries (older than threshold)
        expired_keys = [
            emp_id for emp_id, timestamp in self.recent_employee_detections.items()
            if current_time - timestamp > self.employee_detection_threshold
        ]
        for emp_id in expired_keys:
            del self.recent_employee_detections[emp_id]
        
        # Check if employee was recently detected
        if employee_id in self.recent_employee_detections:
            last_detection = self.recent_employee_detections[employee_id]
            if current_time - last_detection < self.employee_detection_threshold:
                self.logger.debug(f"Skipping logging for employee {employee_id} - detected {current_time - last_detection:.1f}s ago")
                return False
        
        # Update detection time for this employee
        self.recent_employee_detections[employee_id] = current_time
        return True

    async def _process_activity(self, activity_data: Dict):
        """Process activity data - handle all face detections and uploads"""
        detection_type = activity_data["detection_type"]
        current_frame = activity_data["current_frame"]
        bbox = activity_data["bbox"]
        employee_id = activity_data["employee_id"]
        location = activity_data["location"]
        staff_id = activity_data["staff_id"]
        timestamp = activity_data["timestamp"]
        
        try:
            if not self.face_client:
                return

            # Check if we should log this detection (avoid duplicates within time window)
            if not self._should_log_detection(employee_id):
                return None

            # Store activity data
            self.logger.info(f"Storing activity data for employee {employee_id}")
            upload_url = await self.face_client.store_people_activity(
                staff_id=staff_id,
                detection_type=detection_type,
                bbox=bbox,
                location=location,
                employee_id=employee_id,
                timestamp=timestamp,
            )

            if upload_url:
                self.logger.debug("Successfully stored activity log and fetched upload URL")
                await self._upload_frame(current_frame, upload_url, employee_id)
            else:
                self.logger.warning("Failed to store activity log")

            return upload_url
        except Exception as e:
            self.logger.error(f"Error storing activity log: {e}", exc_info=True)


    async def _upload_frame(self, current_frame: np.ndarray, upload_url: str, employee_id: str):
        _, buffer = cv2.imencode(".jpg", current_frame)
        frame_bytes = buffer.tobytes()

        upload_success = await self.face_client.upload_image_to_url(
            frame_bytes, upload_url
        )

        if upload_success:
            self.logger.info(f"Successfully uploaded whole frame for employee {employee_id}")
        else:
            self.logger.warning("Failed to upload whole frame")

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

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            self.stop_background_processing()
        except:
            pass
