import asyncio
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

from ...clients.fr_client import FRClient
from ...clients.models import build_people_activity
from ..utils.geometry_utils import bbox_xyxy_pixels

# The FR server stores the activity ``bbox`` as sent, and the VMS reads it back as pixels on a fixed
# 640 x 640 grid: fe-analytics ``FrameBboxImage`` with ``{kind: "detector", size:
# ALERT_BBOX_DETECTOR_SIZE}``, ``ALERT_BBOX_DETECTOR_SIZE = 640``. The legacy FR path met that grid
# implicitly, by handing this use case its 640 x 640 detector's pixel boxes. The new flow hands it
# normalized [0, 1] boxes, so they are scaled onto the same grid here. Pixel boxes pass through
# unchanged (``bbox_xyxy_pixels``), so the legacy path sends exactly what it sent before.
ACTIVITY_BBOX_GRID = 640

# Pending activity logs per logger. Producers never block: when the FR server falls behind, new
# items are dropped and counted rather than queued without limit.
ACTIVITY_QUEUE_MAXSIZE = 256
# Minimum seconds between two "activity queue full" warnings.
ACTIVITY_DROP_LOG_INTERVAL_S = 60.0


class _NonBlockingQueue(queue.Queue):
    """Bounded queue whose ``put`` never blocks: a full queue raises ``queue.Full`` at once."""

    def put(self, item: Any, block: bool = False, timeout: float | None = None) -> None:
        super().put(item, block=block, timeout=timeout)


# codeql[py/should-be-context-manager]
class PeopleActivityLogging:
    """Background logging system for face recognition activity"""

    def __init__(self, face_client: FRClient | None = None):
        self.face_client = face_client
        self.logger = logging.getLogger(__name__)

        # The client's own project id is deliberately not read here: resolving it calls
        # the platform, and a constructor is the wrong place to make a network request.
        # The client warns once on its own when it cannot resolve one.
        env_project_id = os.getenv("MATRICE_PROJECT_ID", "")
        self.logger.info(
            "[PROJECT_ID] PeopleActivityLogging initialized "
            f"with face_client={'yes' if self.face_client else 'no'}, "
            f"MATRICE_PROJECT_ID env='{env_project_id}'"
        )

        # Thread-safe, bounded queue for cross-thread communication
        self.activity_queue = _NonBlockingQueue(maxsize=ACTIVITY_QUEUE_MAXSIZE)
        self.dropped_activity_count = 0
        self._last_drop_log = float("-inf")

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
        # Same cooldown applied before enqueueing, so repeat sightings never reach the queue.
        self.recent_enqueued_detections: Dict[str, float] = {}
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
            except Exception:  # noqa: BLE001 - a spent loop that will not close is not worth
                # failing the activity thread over, but the reason belongs in the log.
                self.logger.error("Failed to close the activity event loop", exc_info=True)

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
            # A copy for the FR server only; the detection itself stays normalized.
            activity_data["bbox"] = list(
                bbox_xyxy_pixels(bbox, ACTIVITY_BBOX_GRID, ACTIVITY_BBOX_GRID)
            )
            # Update last detection time
            self.last_detection_time = time.time()
            self.empty_detection_logged = False

            self._queue_activity(activity_data)
        except Exception as e:
            self.logger.error(f"Error enqueueing detection: {e}", exc_info=True)

    def _queue_activity(self, activity_data: Dict) -> None:
        """Queue one activity log: cooldown first, no frame or image, never blocking.

        The item carries neither the frame nor an encoded image. The sidecar's request has no
        image field and fetches the frame itself from the media server by ``rtpNumber`` and
        ``camera_id`` (``PeopleActivityRequest``), so either would only inflate the bounded queue.
        """
        # Cooldown before the queue: a tracked face seen every frame is enqueued once per window.
        if "recent_enqueued_detections" not in self.__dict__:
            self.recent_enqueued_detections = {}
        if not self._admit_within_cooldown(
            self.recent_enqueued_detections,
            activity_data["employee_id"],
            camera_id=activity_data["camera_id"],
            track_id=activity_data["track_id"],
        ):
            return
        # Admitted by the cooldown above; the consumer does not apply it a second time.
        activity_data["cooldown_admitted"] = True
        try:
            # _NonBlockingQueue.put raises queue.Full at once instead of blocking the caller.
            self.activity_queue.put(activity_data)
        except queue.Full:
            self._record_dropped_activity()

    def _record_dropped_activity(self) -> None:
        """Count a dropped activity log; warn at most once per ACTIVITY_DROP_LOG_INTERVAL_S."""
        self.dropped_activity_count = getattr(self, "dropped_activity_count", 0) + 1
        now = time.monotonic()
        if now - getattr(self, "_last_drop_log", float("-inf")) >= ACTIVITY_DROP_LOG_INTERVAL_S:
            self._last_drop_log = now
            self.logger.warning(
                "Activity queue full (maxsize=%s); dropped %d activity logs so far",
                self.activity_queue.maxsize,
                self.dropped_activity_count,
            )

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
        return self._admit_within_cooldown(
            self.recent_employee_detections, employee_id, camera_id=camera_id, track_id=track_id
        )

    def _admit_within_cooldown(
        self,
        recent: Dict[str, float],
        employee_id: str,
        camera_id: str = "",
        track_id: str | None = None,
    ) -> bool:
        """Cooldown check of ``_should_log_detection`` against the ``recent`` key map."""
        current_time = time.time()
        if track_id:
            dedupe_key = f"track::{track_id}::{camera_id}"
        elif camera_id:
            dedupe_key = f"emp::{employee_id}::{camera_id}"
        else:
            dedupe_key = f"emp::{employee_id}"

        expired_keys = [
            key
            for key, timestamp in recent.items()
            if current_time - timestamp > self.employee_detection_threshold
        ]
        for key in expired_keys:
            del recent[key]

        if dedupe_key in recent:
            last_detection = recent[dedupe_key]
            if current_time - last_detection < self.employee_detection_threshold:
                self.logger.debug(
                    "Skipping logging key=%s - detected %.1fs ago",
                    dedupe_key,
                    current_time - last_detection,
                )
                return False

        recent[dedupe_key] = current_time
        return True

    async def _process_activity(self, activity_data: Dict):
        """Process activity data - handle all face detections with embedded image data"""
        detection_type = activity_data["detection_type"]
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

            # Check if we should log this detection (avoid duplicates within time window).
            # Items enqueue_detection already admitted through the same cooldown skip it here.
            track_id = activity_data.get("track_id")
            if not activity_data.get("cooldown_admitted") and not self._should_log_detection(
                employee_id, camera_id=camera_id, track_id=track_id
            ):
                self.logger.debug(
                    "Skipping activity log for employee_id=%s (camera_id=%s, track_id=%s) (within cooldown)",
                    employee_id,
                    camera_id,
                    track_id,
                )
                return None

            # The frame is not encoded here. The sidecar's request carries no image
            # field -- it fetches the frame itself from the media server using
            # rtpNumber and camera_id -- so base64-encoding one per detection only
            # spent CPU and memory on bytes that were dropped before the wire.
            self.logger.info(
                f"Processing activity log - type={detection_type}, employee_id={employee_id}, staff_id={staff_id}, location={location}"
            )
            request = build_people_activity(
                staff_id=staff_id,
                type=detection_type,
                timestamp=timestamp,
                bbox=bbox,
                location=location or "",
                camera_name=camera_name or "",
                camera_id=camera_id or "",
                application_id=application_id or "",
                rtp_number=rtp_number or "",
                # Mutually exclusive, chosen by whether the person was recognised.
                employee_id=employee_id if detection_type == "known" and employee_id else None,
                anonymous_id=employee_id if detection_type == "unknown" and employee_id else None,
                confidence_score=None if similarity_score is None else float(similarity_score),
            )
            stored_at = await self.face_client.store_people_activity(request)

            # A blank answer is a success on this route: the activity was recorded, the
            # sidecar simply had no frame to point at.
            self.logger.info(f"Activity log stored successfully for employee_id={employee_id}")
            return stored_at
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

            self.logger.info(
                f"Uploading frame to storage - employee_id={employee_id}, size={len(frame_bytes)} bytes"
            )
            upload_success = await self.face_client.upload_frame(upload_url, frame_bytes)

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
            # New-flow boxes arrive normalized [0, 1]; scale by this frame's own size before
            # slicing pixels (int() of a normalized box is a 0-size crop). Pixel boxes unchanged.
            h, w = frame.shape[:2]
            x1, y1, x2, y2 = (int(v) for v in bbox_xyxy_pixels(bounding_box, w, h))

            # Ensure coordinates are within frame bounds
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
        except Exception:  # noqa: BLE001 - the object is going away either way, but the
            # reason belongs in the log rather than a silent __del__.
            self.logger.error("Failed to stop activity logging during cleanup", exc_info=True)
