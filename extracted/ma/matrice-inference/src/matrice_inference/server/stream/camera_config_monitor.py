"""Background monitor for camera configuration updates."""

import hashlib
import json
import logging
import threading
import time
from typing import Dict, Optional

from matrice_inference.server.stream.utils import CameraConfig
from matrice_inference.server.stream.stream_pipeline import StreamingPipeline
from matrice_inference.server.stream.app_deployment import AppDeployment


class CameraConfigMonitor:
    """Monitors and syncs camera configurations from app deployment API."""

    DEFAULT_CHECK_INTERVAL = 120  # seconds
    DEFAULT_HEARTBEAT_INTERVAL = 30  # seconds
    MAX_RETRY_ATTEMPTS = 5  # Maximum number of retry attempts per camera operation

    def __init__(
        self,
        app_deployment: AppDeployment,
        streaming_pipeline: StreamingPipeline,
        check_interval: int = DEFAULT_CHECK_INTERVAL,
        heartbeat_interval: int = DEFAULT_HEARTBEAT_INTERVAL
    ):
        """Initialize the camera config monitor.

        Args:
            app_deployment: AppDeployment instance to fetch configs
            streaming_pipeline: StreamingPipeline instance to update
            check_interval: Seconds between config checks
            heartbeat_interval: Seconds between heartbeat sends
        """
        self.app_deployment = app_deployment
        self.streaming_pipeline = streaming_pipeline
        self.check_interval = max(10, int(check_interval))  # Minimum 10 seconds
        self.heartbeat_interval = max(10, int(heartbeat_interval))  # Minimum 10 seconds
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.logger = logging.getLogger(__name__)

        # Track camera configs by hash to detect changes (thread-safe access)
        self.camera_hashes: Dict[str, str] = {}
        self._hashes_lock = threading.Lock()

        # Track retry attempts per camera (camera_id -> retry_count)
        self.retry_counts: Dict[str, int] = {}
        self._retry_lock = threading.Lock()

        # Track last sync and heartbeat times
        self.last_sync_time = 0
        self.last_heartbeat_time = 0

        # Refresh state tracking - cameras managed by refresh events
        # Once a camera is in a refresh event, ONLY refresh can modify it (not app events or monitor)
        self._refresh_managed_cameras = set()  # Cameras that have been in ANY refresh event
        self._last_refresh_time = 0
        self._refresh_lock = threading.Lock()

    def start(self) -> None:
        """Start the background monitoring thread."""
        if self.running:
            self.logger.warning("Camera config monitor already running")
            return
        
        # DISABLED: Skip initial sync to avoid large API calls and Redis auth issues at startup
        # The system will rely on refresh events as the primary source of camera configurations.
        # The monitor will only poll as a backup mechanism after cameras are already active.
        try:
            self.logger.info(
                "Skipping initial camera config sync - waiting for refresh events to provide camera configurations. "
                "Monitor polling will activate after first refresh event."
            )
            self.last_sync_time = time.time()

            # Send initial heartbeat with empty camera list
            self._send_heartbeat_if_needed()
            self.last_heartbeat_time = time.time()
        except Exception as e:
            self.logger.error(f"Error during initial heartbeat: {e}")
        
        self.running = True
        self.thread = threading.Thread(
            target=self._monitor_loop,
            name="CameraConfigMonitor",
            daemon=False
        )
        self.thread.start()
        self.logger.info(f"Started camera config monitor (check interval: {self.check_interval}s)")

    def stop(self) -> None:
        """Stop the background monitoring thread."""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
            self.logger.info("Stopped camera config monitor")

    def _monitor_loop(self) -> None:
        """Main monitoring loop - periodically sync camera configs and send heartbeats."""
        while self.running:
            current_time = time.time()

            # Check if it's time to sync camera configs
            if current_time - self.last_sync_time >= self.check_interval:
                try:
                    self._sync_camera_configs()
                    self.last_sync_time = current_time
                except Exception as e:
                    self.logger.error(f"Error syncing camera configs: {e}")

            # Check and send heartbeat if needed (more frequent than config sync)
            try:
                self._send_heartbeat_if_needed()
            except Exception as e:
                self.logger.error(f"Error sending heartbeat: {e}")

            # Sleep for a short interval to allow quick shutdown and frequent heartbeat checks
            time.sleep(1)

    def _send_heartbeat_if_needed(self) -> None:
        """Send heartbeat if enough time has passed since last heartbeat."""
        current_time = time.time()

        # Check if it's time to send heartbeat
        if current_time - self.last_heartbeat_time < self.heartbeat_interval:
            return

        try:
            # Get current camera configs from streaming pipeline
            if self.streaming_pipeline and hasattr(self.streaming_pipeline, 'camera_configs'):
                camera_configs = self.streaming_pipeline.camera_configs

                # Get refresh-managed cameras count for logging
                with self._refresh_lock:
                    refresh_managed_count = len(self._refresh_managed_cameras)
                    refresh_managed_cameras = self._refresh_managed_cameras.copy()

                # Log detailed camera status
                if camera_configs:
                    self.logger.info(
                        f"📊 Heartbeat Status: {len(camera_configs)} active cameras, "
                        f"{refresh_managed_count} refresh-managed"
                    )

                    # Log each camera being reported with its management status
                    for camera_id in camera_configs.keys():
                        is_refresh_managed = camera_id in refresh_managed_cameras
                        management_type = "refresh-managed" if is_refresh_managed else "monitor/event-managed"
                        self.logger.debug(f"  ↳ Camera {camera_id}: {management_type}")

                # Send heartbeat with current configs
                success = self.app_deployment.send_heartbeat(camera_configs)

                if success:
                    self.last_heartbeat_time = current_time
                    self.logger.info(f"✓ Heartbeat sent successfully")
                else:
                    self.logger.warning("✗ Failed to send heartbeat")
            else:
                self.logger.warning("Streaming pipeline not available or has no camera_configs")

        except Exception as e:
            self.logger.error(f"Error sending heartbeat: {e}", exc_info=True)

    def _sync_camera_configs(self) -> None:
        """Fetch latest configs from API and sync with pipeline.

        Note: Cameras managed by refresh events are skipped - only refresh can modify them.
        """
        try:
            # Fetch current configs from app deployment API
            latest_configs = self.app_deployment.get_camera_configs()

            if not latest_configs:
                self.logger.warning("No camera configs returned from API")
                return

            # Get set of refresh-managed cameras (thread-safe)
            with self._refresh_lock:
                refresh_managed = self._refresh_managed_cameras.copy()
                refresh_managed_count = len(refresh_managed)

            # Log sync operation details
            self.logger.info(
                f"🔄 Monitor Sync: {len(latest_configs)} cameras in API, "
                f"{refresh_managed_count} refresh-managed (will skip)"
            )

            # Track what we're processing
            skipped_count = 0
            processed_count = 0

            # Process each camera config, but skip refresh-managed cameras
            for camera_id, camera_config in latest_configs.items():
                # Skip cameras managed by refresh - only refresh can modify them
                if camera_id in refresh_managed:
                    skipped_count += 1
                    self.logger.debug(
                        f"  ⊘ Skipping camera {camera_id} - refresh-managed (only refresh can modify)"
                    )
                    continue

                # Process non-refresh-managed cameras normally
                processed_count += 1
                self.logger.debug(f"  ⚙ Processing camera {camera_id} - monitor-managed")
                self._process_camera_config(camera_id, camera_config)

            # Log summary
            self.logger.info(
                f"✓ Monitor Sync completed: processed {processed_count} cameras, "
                f"skipped {skipped_count} refresh-managed cameras"
            )

            # Optional: Remove cameras that are no longer in API
            # Uncomment if you want to auto-remove deleted cameras
            # self._remove_deleted_cameras(latest_configs)

        except Exception as e:
            self.logger.error(f"Failed to sync camera configs: {e}")

    def _should_retry_operation(self, camera_id: str) -> bool:
        """Check if we should retry an operation for this camera.

        Returns True if retry count is below maximum, False otherwise.
        """
        with self._retry_lock:
            retry_count = self.retry_counts.get(camera_id, 0)
            return retry_count < self.MAX_RETRY_ATTEMPTS

    def _increment_retry_count(self, camera_id: str) -> int:
        """Increment and return the retry count for a camera."""
        with self._retry_lock:
            self.retry_counts[camera_id] = self.retry_counts.get(camera_id, 0) + 1
            return self.retry_counts[camera_id]

    def _reset_retry_count(self, camera_id: str) -> None:
        """Reset the retry count for a camera after successful operation."""
        with self._retry_lock:
            if camera_id in self.retry_counts:
                del self.retry_counts[camera_id]

    def _process_camera_config(self, camera_id: str, camera_config: CameraConfig) -> None:
        """Process a single camera config - add new or update changed."""
        try:
            # Calculate config hash to detect changes
            config_hash = self._hash_camera_config(camera_config)

            # Thread-safe read of previous hash
            with self._hashes_lock:
                previous_hash = self.camera_hashes.get(camera_id)

            # Check if this is a new camera or config changed
            if previous_hash is None:
                # New camera - add it
                self.logger.info(f"  ➕ Monitor: Adding NEW camera {camera_id}")
                self._add_new_camera(camera_id, camera_config, config_hash)
            elif previous_hash != config_hash:
                # Config changed - update it
                self.logger.info(f"  🔄 Monitor: Updating CHANGED camera {camera_id}")
                self._update_changed_camera(camera_id, camera_config, config_hash)
            else:
                # No change - skip
                self.logger.debug(f"  ✓ Camera {camera_id} config unchanged")

        except Exception as e:
            self.logger.error(f"Error processing camera {camera_id}: {e}")

    def _add_new_camera(self, camera_id: str, camera_config: CameraConfig, config_hash: str) -> None:
        """Add a new camera to the pipeline with retry logic."""
        try:
            # Check if we should retry this operation
            if not self._should_retry_operation(camera_id):
                # Max retries exceeded
                retry_count = self.retry_counts.get(camera_id, 0)
                self.logger.warning(
                    f"Max retry attempts ({self.MAX_RETRY_ATTEMPTS}) exceeded for camera {camera_id}, "
                    f"will retry on next successful event loop check"
                )
                return

            # Get event loop from streaming pipeline
            import asyncio
            event_loop = getattr(self.streaming_pipeline, '_event_loop', None)

            if not event_loop or not event_loop.is_running():
                # Increment retry count and log error
                retry_count = self._increment_retry_count(camera_id)
                self.logger.error(
                    f"No running event loop available in pipeline, cannot add camera {camera_id} "
                    f"(attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                )
                return

            # Schedule the coroutine on the pipeline's event loop
            future = asyncio.run_coroutine_threadsafe(
                self.streaming_pipeline.add_camera_config(camera_config),
                event_loop
            )

            # Wait for completion with timeout
            try:
                success = future.result(timeout=10.0)
                if success:
                    # Reset retry count on success
                    self._reset_retry_count(camera_id)
                    # Thread-safe write
                    with self._hashes_lock:
                        self.camera_hashes[camera_id] = config_hash
                    self.logger.info(f"Added new camera: {camera_id}")
                else:
                    retry_count = self._increment_retry_count(camera_id)
                    self.logger.warning(
                        f"Failed to add camera: {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                    )
            except TimeoutError:
                retry_count = self._increment_retry_count(camera_id)
                self.logger.error(
                    f"Timeout adding camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                )

        except Exception as e:
            retry_count = self._increment_retry_count(camera_id)
            self.logger.error(
                f"Error adding camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS}): {e}"
            )

    def _update_changed_camera(self, camera_id: str, camera_config: CameraConfig, config_hash: str) -> None:
        """Update an existing camera with changed config with retry logic."""
        try:
            # Check if we should retry this operation
            if not self._should_retry_operation(camera_id):
                # Max retries exceeded
                retry_count = self.retry_counts.get(camera_id, 0)
                self.logger.warning(
                    f"Max retry attempts ({self.MAX_RETRY_ATTEMPTS}) exceeded for camera {camera_id}, "
                    f"will retry on next successful event loop check"
                )
                return

            # Get event loop from streaming pipeline
            import asyncio
            event_loop = getattr(self.streaming_pipeline, '_event_loop', None)

            if not event_loop or not event_loop.is_running():
                # Increment retry count and log error
                retry_count = self._increment_retry_count(camera_id)
                self.logger.error(
                    f"No running event loop available in pipeline, cannot update camera {camera_id} "
                    f"(attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                )
                return

            # Schedule the coroutine on the pipeline's event loop
            future = asyncio.run_coroutine_threadsafe(
                self.streaming_pipeline.update_camera_config(camera_config),
                event_loop
            )

            # Wait for completion with timeout
            try:
                success = future.result(timeout=10.0)
                if success:
                    # Reset retry count on success
                    self._reset_retry_count(camera_id)
                    # Thread-safe write
                    with self._hashes_lock:
                        self.camera_hashes[camera_id] = config_hash
                    self.logger.info(f"Updated camera config: {camera_id}")
                else:
                    retry_count = self._increment_retry_count(camera_id)
                    self.logger.warning(
                        f"Failed to update camera: {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                    )
            except TimeoutError:
                retry_count = self._increment_retry_count(camera_id)
                self.logger.error(
                    f"Timeout updating camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                )

        except Exception as e:
            retry_count = self._increment_retry_count(camera_id)
            self.logger.error(
                f"Error updating camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS}): {e}"
            )

    def _remove_deleted_cameras(self, latest_configs: Dict[str, CameraConfig]) -> None:
        """Remove cameras that are no longer in the API response with retry logic."""
        # Thread-safe read
        with self._hashes_lock:
            current_camera_ids = set(self.camera_hashes.keys())

        latest_camera_ids = set(latest_configs.keys())
        deleted_camera_ids = current_camera_ids - latest_camera_ids

        for camera_id in deleted_camera_ids:
            try:
                # Check if we should retry this operation
                if not self._should_retry_operation(camera_id):
                    # Max retries exceeded
                    retry_count = self.retry_counts.get(camera_id, 0)
                    self.logger.warning(
                        f"Max retry attempts ({self.MAX_RETRY_ATTEMPTS}) exceeded for removing camera {camera_id}, "
                        f"will retry on next successful event loop check"
                    )
                    continue

                import asyncio
                event_loop = getattr(self.streaming_pipeline, '_event_loop', None)

                if not event_loop or not event_loop.is_running():
                    # Increment retry count and log error
                    retry_count = self._increment_retry_count(camera_id)
                    self.logger.error(
                        f"No running event loop available in pipeline, cannot remove camera {camera_id} "
                        f"(attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                    )
                    continue

                # Schedule the coroutine on the pipeline's event loop
                future = asyncio.run_coroutine_threadsafe(
                    self.streaming_pipeline.remove_camera_config(camera_id),
                    event_loop
                )

                # Wait for completion with timeout
                try:
                    success = future.result(timeout=10.0)
                    if success:
                        # Reset retry count on success
                        self._reset_retry_count(camera_id)
                        # Thread-safe delete
                        with self._hashes_lock:
                            del self.camera_hashes[camera_id]
                        self.logger.info(f"Removed deleted camera: {camera_id}")
                    else:
                        retry_count = self._increment_retry_count(camera_id)
                        self.logger.warning(
                            f"Failed to remove camera: {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                        )
                except TimeoutError:
                    retry_count = self._increment_retry_count(camera_id)
                    self.logger.error(
                        f"Timeout removing camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS})"
                    )

            except Exception as e:
                retry_count = self._increment_retry_count(camera_id)
                self.logger.error(
                    f"Error removing camera {camera_id} (attempt {retry_count}/{self.MAX_RETRY_ATTEMPTS}): {e}"
                )

    def notify_refresh_completed(
        self,
        new_camera_configs: Dict[str, CameraConfig],
        old_camera_configs: Dict[str, CameraConfig]
    ) -> None:
        """Notify monitor that a refresh event has completed successfully.

        Updates the internal hash cache and resets retry counts to prevent
        immediate re-syncing after refresh event handling. Makes refresh the
        PRIMARY source of truth.

        ALL cameras affected by the refresh event are marked as refresh-managed:
        - Cameras in the refresh event (added/updated)
        - Cameras that were in the OLD pipeline but NOT in refresh event (removed)

        Once a camera is managed by ANY refresh event, it can ONLY be modified by
        subsequent refresh events (never by app events or monitor polling).

        Args:
            new_camera_configs: Dictionary of camera_id -> CameraConfig from refresh event (NEW state)
            old_camera_configs: Dictionary of camera_id -> CameraConfig from pipeline before reconciliation (OLD state)
        """
        try:
            # Use OLD camera configs (before reconciliation) to capture removed cameras
            old_camera_ids = set(old_camera_configs.keys())

            # Track newly managed cameras for logging
            newly_managed = []
            removed_cameras = []

            with self._refresh_lock:
                # Cameras in the refresh event (NEW state)
                refresh_event_cameras = set(new_camera_configs.keys())

                # Cameras that were removed (in OLD pipeline but not in refresh event)
                removed_cameras = list(old_camera_ids - refresh_event_cameras)

                # Mark ALL cameras affected by refresh as refresh-managed:
                # 1. Cameras in refresh event (added/updated) - explicit management
                # 2. Cameras being removed - prevent re-add by monitor/events
                all_cameras_to_manage = old_camera_ids | refresh_event_cameras

                before_count = len(self._refresh_managed_cameras)

                for camera_id in all_cameras_to_manage:
                    if camera_id not in self._refresh_managed_cameras:
                        newly_managed.append(camera_id)
                    self._refresh_managed_cameras.add(camera_id)

                after_count = len(self._refresh_managed_cameras)
                self._last_refresh_time = time.time()

                self.logger.warning(
                    f"🔒 REFRESH MANAGEMENT UPDATE: "
                    f"{len(refresh_event_cameras)} cameras in refresh event, "
                    f"{len(old_camera_ids)} were in OLD pipeline, "
                    f"{len(removed_cameras)} removed, "
                    f"{after_count} total refresh-managed (+{after_count - before_count} new)"
                )

                # Log cameras in refresh event
                for camera_id in refresh_event_cameras:
                    is_new = camera_id in newly_managed
                    status = "NEW refresh-managed" if is_new else "already refresh-managed"
                    self.logger.info(f"  🔒 Camera {camera_id}: {status} (in refresh event)")

                # Log cameras being removed (implicitly managed)
                for camera_id in removed_cameras:
                    is_new = camera_id in newly_managed
                    status = "NEW refresh-managed" if is_new else "already refresh-managed"
                    self.logger.warning(
                        f"  🔒 Camera {camera_id}: {status} (REMOVED by refresh, locked from re-add)"
                    )

                # Log warning about permanent tracking
                if newly_managed:
                    self.logger.warning(
                        f"⚠️  {len(newly_managed)} cameras PERMANENTLY marked as refresh-managed: {', '.join(newly_managed)}"
                    )
                    self.logger.warning(
                        "⚠️  These cameras can ONLY be modified by subsequent refresh events (not by monitor or app events)"
                    )

            with self._hashes_lock:
                # Clear old hashes and build new cache from NEW refresh event configs only
                self.camera_hashes.clear()

                for camera_id, camera_config in new_camera_configs.items():
                    config_hash = self._hash_camera_config(camera_config)
                    self.camera_hashes[camera_id] = config_hash

            # Reset all retry counts
            with self._retry_lock:
                self.retry_counts.clear()

            # Defer next sync and heartbeat
            self.last_sync_time = time.time()
            self.last_heartbeat_time = time.time()

            self.logger.info(
                f"✓ Refresh notification complete: updated hash cache for {len(new_camera_configs)} cameras, "
                f"cleared retry counts, deferred next poll ({self.check_interval}s)"
            )

        except Exception as e:
            self.logger.error(f"Error processing refresh notification: {e}", exc_info=True)

    def _hash_camera_config(self, camera_config: CameraConfig) -> str:
        """Generate a hash of the camera config to detect changes."""
        try:
            # Create a dict with relevant config fields
            config_dict = {
                "camera_id": camera_config.camera_id,
                "input_topic": camera_config.input_topic,
                "output_topic": camera_config.output_topic,
                "stream_config": camera_config.stream_config,
                "enabled": camera_config.enabled
            }

            # Convert to JSON string (sorted for consistency) and hash
            config_str = json.dumps(config_dict, sort_keys=True)
            return hashlib.md5(config_str.encode()).hexdigest()

        except Exception as e:
            self.logger.error(f"Error hashing camera config: {e}")
            return ""

