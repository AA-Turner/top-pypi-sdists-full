"""Kafka event listener for deployment instance refresh events.

Subscribes to {instance_id}_application_deployment_event topic.
On ANY message, triggers a full API refresh (no event filtering).
Also runs a periodic auto-refresh as a safety net.
"""

import logging
import threading
import time
from typing import Any, Callable, Dict, Optional

from matrice_common.session import Session
from matrice_common.stream import EventListener as GenericEventListener


class DeploymentRefreshListener:
    """Listener for deployment instance events from Kafka.

    On ANY message on the topic, triggers a full API refresh callback.
    No event type filtering — the callback always re-fetches from the API.

    Also runs a periodic auto-refresh timer as a safety net in case
    Kafka events are missed.
    """

    def __init__(
        self,
        session: Session,
        deployment_instance_id: str,
        on_refresh: Callable[[], None],
        instance_id: str = "",
        auto_refresh_interval: float = 300.0,
    ) -> None:
        """Initialize deployment refresh listener.

        Args:
            session: Session object for authentication
            deployment_instance_id: ID of deployment instance
            on_refresh: No-arg callback that triggers full API refresh
            instance_id: Compute instance ID (required for topic subscription)
            auto_refresh_interval: Seconds between periodic auto-refreshes (default 5 min)
        """
        self.deployment_instance_id = deployment_instance_id
        self.instance_id = instance_id
        self.session = session
        self.on_refresh = on_refresh
        self.logger = logging.getLogger(__name__)

        # Debounce
        self._debounce_seconds = 2.0
        self._last_refresh_time = 0.0

        # Periodic auto-refresh
        self._auto_refresh_interval = auto_refresh_interval
        self._periodic_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Statistics tracking
        self.stats = {
            "events_received": 0,
            "refreshes_processed": 0,
            "refreshes_failed": 0,
            "refreshes_debounced": 0,
            "periodic_refreshes": 0,
            "consecutive_failures": 0,
            "last_refresh_timestamp": None,
        }

        # Circuit breaker configuration
        self.max_consecutive_failures = 10
        self.circuit_open = False
        self._circuit_open_time: Optional[float] = None
        self._circuit_cooldown: float = 60.0
        self._circuit_max_cooldown: float = 600.0

        # Topic name and consumer group
        self.topic_name = f"{instance_id}_application_deployment_event"
        consumer_group = f"deployment_refresh_instance_{instance_id}"

        # Create generic event listener
        self._listener = GenericEventListener(
            session=session,
            topics=[self.topic_name],
            event_handler=self.handle_event,
            filter_field=None,
            filter_value=None,
            consumer_group_id=consumer_group,
            offset_reset="earliest",
        )

        self.logger.info(
            f"DeploymentRefreshListener initialized for instance {instance_id}, "
            f"topic: {self.topic_name}, auto_refresh_interval: {auto_refresh_interval}s"
        )

    @property
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._listener.is_listening

    def start(self) -> bool:
        """Start listening to events and periodic refresh.

        Returns:
            bool: True if started successfully
        """
        success = self._listener.start()
        if success:
            # Start periodic auto-refresh thread
            self._stop_event.clear()
            self._periodic_thread = threading.Thread(
                target=self._periodic_refresh_loop,
                name="Inference-PeriodicRefresh",
                daemon=True,
            )
            self._periodic_thread.start()
            self.logger.info(
                f"Started listening + periodic refresh "
                f"(interval={self._auto_refresh_interval}s) on topic: {self.topic_name}"
            )
        else:
            self.logger.error(f"Failed to start listening to topic: {self.topic_name}")
        return success

    def stop(self):
        """Stop listening and periodic refresh."""
        self._stop_event.set()
        if self._periodic_thread and self._periodic_thread.is_alive():
            self._periodic_thread.join(timeout=5.0)
        self._listener.stop()
        self.logger.info(f"Stopped listening to topic: {self.topic_name}")

    def handle_event(self, event: Dict[str, Any]):
        """Handle ANY event by triggering a full API refresh.

        All events on the topic are treated as refresh triggers.
        The actual camera list is always re-fetched from the API.
        """
        self.stats["events_received"] += 1

        # Any message type (JSON dict, empty dict from non-JSON, etc.) triggers refresh
        if isinstance(event, dict) and event:
            event_type = event.get("eventType", "unknown")
            self.logger.info(f"Event received on deployment topic: type={event_type}")
        else:
            self.logger.info("Event received on deployment topic (non-JSON or empty) — triggering refresh")

        if not self._is_circuit_allowing_request():
            self.logger.error("Circuit breaker OPEN - ignoring event")
            return

        # Debounce
        now = time.time()
        if now - self._last_refresh_time < self._debounce_seconds:
            self.stats["refreshes_debounced"] += 1
            self.logger.debug("Debouncing refresh")
            return

        try:
            self.on_refresh()
            self._last_refresh_time = time.time()
            self.stats["refreshes_processed"] += 1
            self.stats["consecutive_failures"] = 0
            self.stats["last_refresh_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            if self.circuit_open:
                self.circuit_open = False
                self._circuit_open_time = None
                self._circuit_cooldown = 60.0
                self.logger.info("Circuit breaker CLOSED (probe succeeded)")
        except Exception as e:
            self.stats["refreshes_failed"] += 1
            self.stats["consecutive_failures"] += 1
            self._check_circuit_breaker()
            self.logger.error(f"Error during refresh: {e}", exc_info=True)

    def _periodic_refresh_loop(self):
        """Background loop for periodic auto-refresh."""
        self.logger.info(f"Periodic refresh loop started: interval={self._auto_refresh_interval}s")
        while not self._stop_event.wait(timeout=self._auto_refresh_interval):
            # Skip if a Kafka-triggered refresh happened recently
            now = time.time()
            if now - self._last_refresh_time < self._auto_refresh_interval * 0.5:
                self.logger.debug("Skipping periodic refresh - recent event refresh")
                continue

            if not self._is_circuit_allowing_request():
                self.logger.warning("Periodic refresh skipped - circuit breaker open")
                continue

            try:
                self.logger.info("Periodic auto-refresh triggered")
                self.on_refresh()
                self._last_refresh_time = time.time()
                self.stats["periodic_refreshes"] += 1
                self.stats["refreshes_processed"] += 1
                self.stats["consecutive_failures"] = 0
                if self.circuit_open:
                    self.circuit_open = False
                    self._circuit_open_time = None
                    self._circuit_cooldown = 60.0
                    self.logger.info("Circuit breaker CLOSED (periodic probe succeeded)")
            except Exception as e:
                self.stats["refreshes_failed"] += 1
                self.stats["consecutive_failures"] += 1
                self._check_circuit_breaker()
                self.logger.error(f"Periodic refresh error: {e}", exc_info=True)

    def _is_circuit_allowing_request(self) -> bool:
        """Check if circuit allows a request (closed or half-open probe)."""
        if not self.circuit_open:
            return True
        # Half-open: allow one probe after cooldown
        if self._circuit_open_time and (time.time() - self._circuit_open_time > self._circuit_cooldown):
            self.logger.info(
                f"Circuit breaker half-open — allowing probe request (cooldown={self._circuit_cooldown:.0f}s elapsed)"
            )
            return True
        return False

    def _check_circuit_breaker(self):
        """Check if circuit breaker should be opened based on consecutive failures."""
        if self.stats["consecutive_failures"] >= self.max_consecutive_failures:
            if not self.circuit_open:
                self.circuit_open = True
                self._circuit_open_time = time.time()
                self.logger.critical(
                    f"Circuit breaker OPENED after {self.stats['consecutive_failures']} "
                    f"consecutive failures. Will retry after {self._circuit_cooldown:.0f}s cooldown."
                )
            else:
                # Already open, extend cooldown with backoff on repeated failure
                self._circuit_cooldown = min(self._circuit_cooldown * 2, self._circuit_max_cooldown)
                self._circuit_open_time = time.time()
                self.logger.warning(
                    f"Circuit breaker probe failed, extending cooldown to {self._circuit_cooldown:.0f}s"
                )
        elif self.stats["consecutive_failures"] > self.max_consecutive_failures // 2:
            self.logger.warning(
                f"Approaching failure threshold: {self.stats['consecutive_failures']}/"
                f"{self.max_consecutive_failures} consecutive failures"
            )

    def get_statistics(self) -> dict:
        """Get refresh listener statistics."""
        listener_stats = self._listener.get_statistics()
        return {
            "refresh_listener": self.stats.copy(),
            "generic_listener": listener_stats,
            "topic_name": self.topic_name,
            "is_listening": self.is_listening,
            "auto_refresh_interval": self._auto_refresh_interval,
            "circuit_breaker": {
                "open": self.circuit_open,
                "max_consecutive_failures": self.max_consecutive_failures,
            },
        }
