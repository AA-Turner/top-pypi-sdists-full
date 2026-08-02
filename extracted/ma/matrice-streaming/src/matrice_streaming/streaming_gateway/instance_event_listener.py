"""Refresh-based Kafka event listener for instance-based streaming gateway.

Subscribes to instance-specific Kafka topics and on any message,
re-fetches the full camera list via consuming topics API and diffs
against the current camera manager state.

Also runs a periodic auto-refresh as a safety net in case Kafka events
are missed.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Optional

from matrice_common.session import Session
from matrice_common.stream import EventListener as GenericEventListener

# Cap the circuit-breaker cooldown that applies to the *periodic* refresh
# path. The event-driven path keeps the full _circuit_max_cooldown (up to
# 600s) so a thundering herd of Kafka events doesn't all probe at once; but
# the periodic backstop must recover faster after a transient API outage,
# otherwise a single bad probe at the wrong moment can pin the gateway
# blind for 10 minutes (step 9 in fix plan).
PERIODIC_CIRCUIT_COOLDOWN_CAP_SEC = 120.0

# How long a camera must be tracked in DCM without an SHM file existing
# before the reconciler treats it as a phantom. Needs to exceed the worst
# case "lazy SHM creation on first frame" delay for cameras with width=0/
# height=0 (configured for native resolution).
PHANTOM_GRACE_SEC = 90.0


class InstanceEventListener:
    """Refresh-based listener for instance-specific streaming events.

    Subscribes to:
    - {instance_id}_streaming_gateway_event

    On any message received, re-fetches the full camera list from the
    consuming topics API and diffs against the current camera manager state.

    Also runs a periodic auto-refresh timer as a safety net.
    """

    def __init__(
        self,
        session: Session,
        instance_id: str,
        camera_manager,
        instance_util,
        auto_refresh_interval: float = 60.0,
    ) -> None:
        """Initialize instance event listener.

        Args:
            session: Session object for authentication
            instance_id: Compute instance ID
            camera_manager: DynamicCameraManager variant instance
            instance_util: InstanceStreamingGatewayUtil instance for API calls
            auto_refresh_interval: Seconds between periodic auto-refreshes
                (default 60s). Acts as a safety-net backstop in case a Kafka
                event is missed. With 1K+ cameras, polling more often would
                hammer the consuming-topics API for no benefit — Kafka events
                drive the fast-path; periodic refresh is just for resilience.
        """
        self.instance_id = instance_id
        self.camera_manager = camera_manager
        self.instance_util = instance_util
        self.session = session
        self.logger = logging.getLogger(__name__)

        # Debounce: only applies to *periodic* refreshes that fire while a
        # Kafka-triggered refresh is in flight. Event-driven refreshes are
        # user-actionable and never debounced (see handle_event below).
        self._debounce_seconds = 0.2
        self._last_refresh_time = 0.0
        # Serialize concurrent refresh executions: Kafka event + periodic
        # tick can both fire near-simultaneously after a gateway start.
        self._refresh_lock = threading.Lock()

        # Periodic auto-refresh
        self._auto_refresh_interval = auto_refresh_interval
        self._periodic_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Circuit breaker configuration (protected by _circuit_lock —
        # accessed from both the Kafka consumer thread and periodic refresh thread)
        self._circuit_lock = threading.Lock()
        self._max_consecutive_failures = 10
        self._circuit_open = False
        self._circuit_open_time: Optional[float] = None
        self._circuit_cooldown: float = 60.0
        self._circuit_max_cooldown: float = 600.0
        self._consecutive_failures = 0

        # Statistics
        self.stats = {
            "events_received": 0,
            "refreshes_executed": 0,
            "refreshes_debounced": 0,
            "periodic_refreshes": 0,
            "cameras_added": 0,
            "cameras_removed": 0,
            "cameras_updated": 0,
            "phantoms_reconciled": 0,
            "errors": 0,
        }

        # Per-camera "first seen tracked" timestamp for phantom detection.
        # A camera is a phantom if it's been in DCM.cameras for >
        # PHANTOM_GRACE_SEC but its SHM file does not exist.
        self._camera_first_tracked_at: Dict[str, float] = {}

        # Subscribe to instance-specific topics
        self._topics = [
            f"{instance_id}_streaming_gateway_event",
        ]

        self._listener = GenericEventListener(
            session=session,
            topics=self._topics,
            event_handler=self.handle_event,
            filter_field=None,  # No filtering — topic is already instance-specific
            filter_value=None,
            consumer_group_id=f"stg_instance_events_{instance_id}",
            # Default to "latest". The API gives us the current camera list
            # on every refresh, so replaying historical events would just
            # re-trigger ADDs for cameras that are already running — at 1K
            # cameras that's a stampede. _initial_refresh() on start() reads
            # the full state from the API; events only carry the delta from
            # there onward, which is exactly what "latest" gives us.
            offset_reset="latest",
        )

        self.logger.info(
            f"InstanceEventListener initialized for instance {instance_id}, "
            f"topics: {self._topics}, auto_refresh_interval: {auto_refresh_interval}s"
        )

    @property
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._listener.is_listening

    def start(self) -> bool:
        """Start listening to instance events and periodic refresh.

        Returns:
            bool: True if started successfully
        """
        success = self._listener.start()
        if not success:
            self.logger.error(f"Failed to start listening to topics: {self._topics}")
        # Start the API refresh path regardless of Kafka listener health. If the
        # consumer cannot start during a transient broker outage, this backstop
        # still discovers cameras added while the gateway container is running.
        self._start_refresh_threads(kafka_listener_started=success)
        return success

    def _start_refresh_threads(self, kafka_listener_started: bool) -> None:
        """Start immediate and periodic API refresh threads."""
        # Kick off an immediate refresh so the gateway picks up the current
        # camera list without waiting for the first periodic tick or Kafka event.
        threading.Thread(
            target=self._initial_refresh,
            name="SG-InitialRefresh",
            daemon=True,
        ).start()

        self._stop_event.clear()
        if self._periodic_thread and self._periodic_thread.is_alive():
            return
        self._periodic_thread = threading.Thread(
            target=self._periodic_refresh_loop,
            name="SG-PeriodicRefresh",
            daemon=True,
        )
        self._periodic_thread.start()

        if kafka_listener_started:
            self.logger.info(
                f"Started listening + periodic refresh "
                f"(interval={self._auto_refresh_interval}s) on topics: {self._topics}"
            )
        else:
            self.logger.warning(
                f"Started periodic API refresh fallback without Kafka listener "
                f"(interval={self._auto_refresh_interval}s) on topics: {self._topics}"
            )

    def _initial_refresh(self):
        """One-shot refresh on listener start so cameras are picked up
        without waiting for either a Kafka event or the first periodic tick.
        """
        if not self._refresh_lock.acquire(timeout=10.0):
            self.logger.warning(
                "Initial camera-list refresh skipped — refresh lock held "
                "for >10s at startup; first sync will come from the next "
                "Kafka event or periodic tick"
            )
            return
        try:
            self.logger.info("Initial camera-list refresh after start")
            self._execute_refresh()
            self._last_refresh_time = time.time()
            self.stats["refreshes_executed"] += 1
        except Exception as e:
            self.logger.error(f"Initial refresh failed: {e}", exc_info=True)
        finally:
            self._refresh_lock.release()

    def stop(self):
        """Stop listening and periodic refresh."""
        self._stop_event.set()
        if self._periodic_thread and self._periodic_thread.is_alive():
            self._periodic_thread.join(timeout=5.0)
        self._listener.stop()
        self.logger.info("Instance event listener stopped")

    def handle_event(self, event: Dict[str, Any]):
        """Handle any instance event by triggering a refresh.

        All events on instance topics are treated as refresh triggers.
        The actual camera list is always re-fetched from the API.

        Args:
            event: Event dict (structure varies, but we only use it for logging)
        """
        self.stats["events_received"] += 1

        # Any message (JSON dict, empty dict from non-JSON, etc.) triggers refresh
        if isinstance(event, dict) and event:
            event_type = event.get("eventType", "unknown")
            timestamp = event.get("timestamp", "unknown")
            self.logger.info(f"Instance event received: type={event_type}, timestamp={timestamp}")
        else:
            self.logger.info("Instance event received (non-JSON or empty) — triggering refresh")

        # Event-driven refreshes are NOT debounced — users expect their
        # camera-add/remove actions to take effect promptly. The debounce
        # exists only for the periodic-tick path, where overlapping work
        # would be wasted.

        if not self._is_circuit_allowing_request():
            self.logger.warning("Refresh skipped - circuit breaker open")
            return

        # Serialize against periodic-tick refresh so we never run two
        # diff/apply cycles concurrently. Event-driven refreshes wait
        # rather than dropping the user action — but with a generous
        # upper bound so a hung previous refresh (slow API, network
        # stall) cannot wedge the Kafka consumer thread indefinitely.
        # Default raised from 120s → 600s because bulk-add scenarios
        # (200+ cameras at once) routinely take >120s and the original
        # default caused user-visible "refresh skipped" warnings even
        # when the system was making progress. Override via
        # MATRICE_REFRESH_LOCK_TIMEOUT_SEC.
        _refresh_timeout_sec = float(os.environ.get("MATRICE_REFRESH_LOCK_TIMEOUT_SEC", "600.0"))
        if not self._refresh_lock.acquire(timeout=_refresh_timeout_sec):
            self.stats["refreshes_debounced"] += 1
            self.logger.warning(
                f"Event-driven refresh skipped — previous refresh still in "
                f"flight after {_refresh_timeout_sec:.0f}s; consumer will "
                f"pick up the next event"
            )
            return
        try:
            self._run_refresh_guarded("event")
        finally:
            self._refresh_lock.release()

    def _is_circuit_allowing_request(self, *, periodic: bool = False) -> bool:
        """Check if circuit allows a request (closed or half-open probe).

        For the periodic path, the cooldown is capped at
        PERIODIC_CIRCUIT_COOLDOWN_CAP_SEC so we recover faster after a
        transient API outage — step 9 in the fix plan.
        """
        with self._circuit_lock:
            if not self._circuit_open:
                return True
            if self._circuit_open_time is None:
                return False
            effective_cooldown = self._circuit_cooldown
            if periodic:
                effective_cooldown = min(effective_cooldown, PERIODIC_CIRCUIT_COOLDOWN_CAP_SEC)
            if time.time() - self._circuit_open_time > effective_cooldown:
                self.logger.info(
                    f"Circuit breaker half-open — allowing "
                    f"{'periodic' if periodic else 'event'} probe "
                    f"(cooldown={effective_cooldown:.0f}s)"
                )
                return True
            return False

    def _check_circuit_breaker(self):
        """Open or extend circuit breaker based on consecutive failures."""
        with self._circuit_lock:
            if self._consecutive_failures >= self._max_consecutive_failures:
                if not self._circuit_open:
                    self._circuit_open = True
                    self._circuit_open_time = time.time()
                    self.logger.critical(
                        f"Circuit breaker OPENED after {self._consecutive_failures} failures. "
                        f"Will retry after {self._circuit_cooldown:.0f}s."
                    )
                else:
                    self._circuit_cooldown = min(self._circuit_cooldown * 2, self._circuit_max_cooldown)
                    self._circuit_open_time = time.time()

    def _run_refresh_guarded(self, source: str) -> bool:
        """Execute a refresh with circuit-breaker bookkeeping.

        Shared by the event-driven and periodic paths (previously two
        near-identical try/except blocks). The caller owns acquisition and
        release of ``self._refresh_lock``. Returns True on success, False if the
        refresh raised (the breaker has already been updated in that case).
        """
        if source == "periodic":
            self.logger.info("Periodic auto-refresh triggered")
        try:
            self._execute_refresh()
            self._last_refresh_time = time.time()
            self.stats["refreshes_executed"] += 1
            if source == "periodic":
                self.stats["periodic_refreshes"] += 1
            with self._circuit_lock:
                self._consecutive_failures = 0
                if self._circuit_open:
                    self._circuit_open = False
                    self._circuit_open_time = None
                    self._circuit_cooldown = 60.0
                    self.logger.info("Circuit breaker CLOSED (%s probe succeeded)", source)
            return True
        except Exception as e:
            self.stats["errors"] += 1
            with self._circuit_lock:
                self._consecutive_failures += 1
            self._check_circuit_breaker()
            self.logger.error("Error during %s refresh: %s", source, e, exc_info=True)
            return False

    def _periodic_refresh_loop(self):
        """Background loop that triggers periodic refresh as a safety net."""
        self.logger.info(f"Periodic refresh loop started: interval={self._auto_refresh_interval}s")
        while not self._stop_event.wait(timeout=self._auto_refresh_interval):
            # Skip if a refresh ran in the last `_debounce_seconds` — this
            # avoids wasted API calls when Kafka events fire just before
            # a periodic tick. Event-driven refreshes are unaffected.
            now = time.time()
            if now - self._last_refresh_time < self._debounce_seconds:
                self.stats["refreshes_debounced"] += 1
                self.logger.debug(
                    f"Skipping periodic refresh - just refreshed ({now - self._last_refresh_time:.2f}s ago)"
                )
                continue
            if not self._is_circuit_allowing_request(periodic=True):
                self.logger.warning("Periodic refresh skipped - circuit breaker open")
                continue
            # Try to acquire the refresh lock without blocking — if a Kafka
            # event-driven refresh is mid-flight, just skip this tick.
            if not self._refresh_lock.acquire(blocking=False):
                self.logger.debug("Periodic refresh skipped - event-driven refresh in flight")
                continue
            try:
                self._run_refresh_guarded("periodic")
            finally:
                self._refresh_lock.release()

    def _execute_refresh(self):
        """Re-fetch consuming topics and diff against current camera manager state."""
        # Fetch current full camera list from API
        topics = self.instance_util.get_consuming_topics()

        # Build camera ID set from ALL topics (no topicType filtering)
        input_topics_by_camera = {}
        for topic in topics:
            camera_id = topic.get("cameraId")
            if camera_id:
                input_topics_by_camera[camera_id] = topic

        new_camera_ids = set(input_topics_by_camera.keys())

        # Get current camera IDs from camera manager
        current_camera_ids = set()
        if hasattr(self.camera_manager, "cameras") and self.camera_manager.cameras:
            current_camera_ids = set(self.camera_manager.cameras.keys())

        # C1 guard: get_consuming_topics() collapses any transport error or
        # success=false response to an empty list. Treat "no topics at all while
        # we still track cameras" as a suspected transient API failure rather
        # than a legitimate "remove everything" instruction — otherwise a single
        # backend hiccup tears down every running decoder/ring buffer at once.
        # Raise so the caller's circuit breaker counts it; the next successful
        # refresh will remove any cameras that are genuinely gone.
        if not new_camera_ids and current_camera_ids:
            self.stats["empty_topic_aborts"] = self.stats.get("empty_topic_aborts", 0) + 1
            raise RuntimeError(
                "Refresh returned zero consuming topics while "
                f"{len(current_camera_ids)} cameras are active — treating as a "
                "transient API failure and skipping teardown"
            )

        # Diff
        to_add = new_camera_ids - current_camera_ids
        to_remove = current_camera_ids - new_camera_ids
        to_maybe_update = new_camera_ids & current_camera_ids

        self.logger.info(
            f"Refresh diff: +{len(to_add)} add, -{len(to_remove)} remove, "
            f"~{len(to_maybe_update)} potential updates "
            f"(new={len(new_camera_ids)}, current={len(current_camera_ids)})"
        )

        # Remove cameras no longer in the list
        for camera_id in to_remove:
            try:
                if self.camera_manager.remove_camera(camera_id):
                    self.stats["cameras_removed"] += 1
                else:
                    self.logger.warning(f"Camera manager failed to remove {camera_id}")
            except Exception as e:
                self.logger.error(f"Error removing camera {camera_id}: {e}")

        # Add new cameras.
        # For small batches (≤ MATRICE_PARALLEL_ADD_THRESHOLD) we keep the
        # serial loop — its overhead is negligible and it preserves the
        # original log ordering. For bulk-add scenarios (hundreds of cameras)
        # we fan out to a thread pool so the ~10-30s per-camera producer_ready
        # waits run concurrently instead of in series. This drops a 200-camera
        # bulk-add from ~50 min worst case to ~3 min.
        _parallel_threshold = int(os.environ.get("MATRICE_PARALLEL_ADD_THRESHOLD", "10"))
        _max_workers = int(os.environ.get("MATRICE_PARALLEL_ADD_WORKERS", "32"))
        if len(to_add) <= _parallel_threshold:
            for camera_id in to_add:
                try:
                    topic_data = input_topics_by_camera[camera_id].copy()
                    topic_data["id"] = camera_id  # camera managers use 'id'
                    if self.camera_manager.add_camera(topic_data):
                        self.stats["cameras_added"] += 1
                    else:
                        self.logger.warning(f"Camera manager failed to add {camera_id}")
                except Exception as e:
                    self.logger.error(f"Error adding camera {camera_id}: {e}")
        else:
            workers = max(1, min(_max_workers, len(to_add)))
            self.logger.info(f"Bulk-add: dispatching {len(to_add)} camera adds across {workers} workers")

            def _add_one(camera_id: str) -> tuple:
                try:
                    topic_data = input_topics_by_camera[camera_id].copy()
                    topic_data["id"] = camera_id
                    return (
                        camera_id,
                        bool(self.camera_manager.add_camera(topic_data)),
                        None,
                    )
                except Exception as e:  # noqa: BLE001
                    return camera_id, False, repr(e)

            success = 0
            failures = 0
            with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="ParallelAdd") as pool:
                futures = {pool.submit(_add_one, cid): cid for cid in to_add}
                for fut in as_completed(futures):
                    cid, ok, err = fut.result()
                    if ok:
                        success += 1
                        self.stats["cameras_added"] += 1
                    else:
                        failures += 1
                        if err:
                            self.logger.error(f"Error adding camera {cid}: {err}")
                        else:
                            self.logger.warning(f"Camera manager failed to add {cid}")
            self.logger.info(f"Bulk-add complete: {success} added, {failures} failed (out of {len(to_add)})")

        # Update existing cameras — update_camera() has a diff guard that
        # short-circuits when config hasn't changed, so this is safe at scale.
        for camera_id in to_maybe_update:
            try:
                topic_data = input_topics_by_camera[camera_id].copy()
                topic_data["id"] = camera_id
                self.camera_manager.update_camera(topic_data)
            except Exception as e:
                self.logger.error(f"Error updating camera {camera_id}: {e}")

        # Self-healing phantom reconcile (step 8 in fix plan).
        # A "phantom" is a camera DCM thinks is tracked but for which the
        # producer SHM file does not exist. Caused by hot-add failures that
        # slipped past the ACK protocol (e.g., a producer crash AFTER the
        # ACK was sent, or a race with worker respawn). Dropping the phantom
        # here lets the very next periodic refresh re-add it cleanly.
        self._reconcile_phantoms(input_topics_by_camera)

    def _reconcile_phantoms(self, input_topics_by_camera: Dict[str, Dict[str, Any]]) -> None:
        """Drop cameras DCM tracks but whose SHM file is missing past grace.

        This is the "auto refresh of new cams without too much waiting or
        restart" piece of the fix — the gateway self-heals within one
        refresh interval instead of needing a whole-container restart.
        """
        try:
            tracked: Dict[str, Any] = getattr(self.camera_manager, "cameras", {}) or {}
        except Exception:
            return

        now = time.time()
        phantoms: list = []
        currently_tracked: set = set(tracked.keys())

        # Maintain first-seen-at map: stamp new arrivals, drop stale entries.
        for cid in list(self._camera_first_tracked_at.keys()):
            if cid not in currently_tracked:
                self._camera_first_tracked_at.pop(cid, None)
        for cid in currently_tracked:
            self._camera_first_tracked_at.setdefault(cid, now)

        for cid in currently_tracked:
            first_seen = self._camera_first_tracked_at.get(cid, now)
            if now - first_seen < PHANTOM_GRACE_SEC:
                continue
            shm_path = f"/dev/shm/databus__{cid}__sg__frames"  # nosec B108
            try:
                if os.path.exists(shm_path):
                    continue
            except OSError:
                continue
            # Only reconcile cameras the API still wants us to run. If the
            # API has dropped this camera, the normal to_remove path handles
            # it on this same refresh; skip to avoid duplicate work.
            if cid not in input_topics_by_camera:
                continue
            phantoms.append(cid)

        if not phantoms:
            return

        self.logger.warning(
            f"Reconciler: {len(phantoms)} phantom camera(s) tracked but no SHM: "
            f"{phantoms[:5]}{'...' if len(phantoms) > 5 else ''}"
        )

        for cid in phantoms:
            # Drop from DCM so the *next* periodic refresh's diff treats
            # this camera as a fresh add. We use remove_camera (not the
            # late-failure helper) because the producer truly is gone —
            # backend.remove_camera() is a no-op on a missing camera but
            # ensures any worker-side bookkeeping is consistent.
            try:
                self.camera_manager.remove_camera(cid)
            except Exception as e:
                self.logger.warning(f"Reconciler: failed to drop phantom {cid}: {e}")
            self._camera_first_tracked_at.pop(cid, None)
            self.stats["phantoms_reconciled"] += 1

        # Immediately re-add the still-wanted cameras in this same refresh
        # cycle (don't wait another auto_refresh_interval). They go through
        # the new ACK-gated add_camera() so a re-failure surfaces loudly.
        for cid in phantoms:
            topic_data = input_topics_by_camera.get(cid)
            if not topic_data:
                continue
            try:
                td = topic_data.copy()
                td["id"] = cid
                if self.camera_manager.add_camera(td):
                    self.stats["cameras_added"] += 1
                else:
                    self.logger.warning(
                        f"Reconciler: re-add of phantom {cid} failed; will be retried on next periodic refresh"
                    )
            except Exception as e:
                self.logger.error(f"Reconciler: re-add error for {cid}: {e}")

    def get_statistics(self) -> dict:
        """Get event listener statistics."""
        listener_stats = self._listener.get_statistics()
        return {
            "instance_listener": self.stats.copy(),
            "generic_listener": listener_stats,
            "topics": self._topics,
            "is_listening": self.is_listening,
            "auto_refresh_interval": self._auto_refresh_interval,
        }
