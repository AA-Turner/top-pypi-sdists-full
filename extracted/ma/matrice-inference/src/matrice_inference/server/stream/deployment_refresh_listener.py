"""Kafka event listener for deployment instance refresh events.

This listener subscribes to {deployment_instance_id}_app_event topic
to receive full camera configuration snapshots, acting as the primary
source of truth for configuration updates.
"""
import logging
from typing import Any, Dict, Callable, List
from matrice_common.session import Session
from matrice_common.stream import EventListener as GenericEventListener


class DeploymentRefreshListener:
    """Listener for deployment instance refresh events from Kafka.

    This class wraps the generic EventListener from matrice_common
    and provides deployment-specific event handling logic for full
    configuration refreshes.

    Events handled:
    - refresh: Complete snapshot of all streaming topics for this deployment

    The refresh event is the PRIMARY source of truth and triggers full
    reconciliation of camera configurations.
    """

    def __init__(
        self,
        session: Session,
        deployment_instance_id: str,
        on_refresh: Callable[[Dict[str, Any]], None],
    ) -> None:
        """Initialize deployment refresh listener.

        Args:
            session: Session object for authentication
            deployment_instance_id: ID of deployment instance
            on_refresh: Callback when a refresh event is received
        """
        self.deployment_instance_id = deployment_instance_id
        self.session = session
        self.on_refresh = on_refresh
        self.logger = logging.getLogger(__name__)

        # Statistics tracking
        self.stats = {
            "refreshes_received": 0,
            "refreshes_processed": 0,
            "refreshes_failed": 0,
            "consecutive_failures": 0,
            "last_refresh_timestamp": None,
            "last_camera_count": 0,
        }

        # Circuit breaker configuration
        self.max_consecutive_failures = 10
        self.circuit_open = False

        # Topic name based on deployment instance ID
        self.topic_name = f"{deployment_instance_id}_app_event"

        # Create generic event listener for deployment refresh topic
        # No filtering needed since topic is instance-specific
        self._listener = GenericEventListener(
            session=session,
            topics=[self.topic_name],
            event_handler=self.handle_event,
            filter_field=None,  # No filtering - topic is already specific
            filter_value=None,
            consumer_group_id=f"deployment_refresh_{deployment_instance_id}",
            offset_reset='earliest'
        )

        self.logger.info(
            f"DeploymentRefreshListener initialized for deployment {deployment_instance_id}, "
            f"topic: {self.topic_name}"
        )

    @property
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._listener.is_listening

    def start(self) -> bool:
        """Start listening to refresh events.

        Returns:
            bool: True if started successfully
        """
        success = self._listener.start()
        if success:
            self.logger.info(f"Started listening to refresh events on topic: {self.topic_name}")
        else:
            self.logger.error(f"Failed to start listening to topic: {self.topic_name}")
        return success

    def stop(self):
        """Stop listening."""
        self._listener.stop()
        self.logger.info(f"Stopped listening to refresh events on topic: {self.topic_name}")

    def handle_event(self, event: Dict[str, Any]):
        """Handle deployment refresh event.

        Args:
            event: Refresh event dict with structure:
                {
                    "eventType": "refresh",
                    "streamingGatewayId": "...",  # NOTE: Key name is wrong, this is actually deployInstanceId
                    "timestamp": "2025-01-14T10:30:00Z",
                    "data": [
                        {
                            "id": "...",
                            "accountNumber": "...",
                            "cameraId": "...",
                            "streamingGatewayId": "...",
                            "serverId": "...",
                            "serverType": "redis" | "kafka",
                            "appDeploymentId": "...",
                            "topicName": "...",
                            "topicType": "input" | "output",
                            "ipAddress": "...",
                            "port": 123,
                            "consumingAppsDeploymentIds": [...],
                            "cameraFPS": 30,
                            "deployInstanceId": "..."
                        },
                        ...
                    ]
                }

                NOTE: Backend sends "streamingGatewayId" but the value is actually
                the deployment instance ID. The key name is incorrect in the backend.
        """
        self.stats["refreshes_received"] += 1
        logging.info(f"Refresh event received: {event}")

        # Check circuit breaker
        if self.circuit_open:
            self.logger.error(
                f"Circuit breaker OPEN - ignoring refresh event due to {self.stats['consecutive_failures']} "
                f"consecutive failures (threshold: {self.max_consecutive_failures}). "
                f"Manual intervention required."
            )
            return

        try:
            # Validate event structure
            if not self._validate_event(event):
                self.stats["refreshes_failed"] += 1
                self.stats["consecutive_failures"] += 1
                self._check_circuit_breaker()
                return

            # Extract event data
            event_type = event.get('eventType')
            timestamp = event.get('timestamp')
            streaming_topics = event.get('data', [])

            # Log refresh event details
            self.logger.info(
                f"Refresh event received: eventType={event_type}, "
                f"timestamp={timestamp}, cameras_in_snapshot={len(streaming_topics)}"
            )

            # Update statistics
            self.stats["last_refresh_timestamp"] = timestamp
            self.stats["last_camera_count"] = len(streaming_topics)

            # Handle refresh event
            if event_type == 'refresh':
                self._handle_refresh_event(event, streaming_topics)
            else:
                self.logger.warning(f"Unknown event type: {event_type}, ignoring")
                self.stats["refreshes_failed"] += 1
                self.stats["consecutive_failures"] += 1
                self._check_circuit_breaker()

        except Exception as e:
            self.stats["refreshes_failed"] += 1
            self.stats["consecutive_failures"] += 1
            self._check_circuit_breaker()
            self.logger.error(
                f"Error handling refresh event: {e}\n"
                f"Event: {event}",
                exc_info=True
            )

    def _validate_event(self, event: Dict[str, Any]) -> bool:
        """Validate refresh event structure.

        Args:
            event: Event dict to validate

        Returns:
            bool: True if event is valid
        """
        # Check required fields
        if 'eventType' not in event:
            self.logger.error("Refresh event missing 'eventType' field")
            return False

        if 'data' not in event:
            self.logger.error("Refresh event missing 'data' field")
            return False

        # Validate data is a list
        if not isinstance(event.get('data'), list):
            self.logger.error(f"Refresh event 'data' must be a list, got {type(event.get('data'))}")
            return False

        # Validate each streaming topic entry
        streaming_topics = event.get('data', [])
        for idx, topic in enumerate(streaming_topics):
            if not isinstance(topic, dict):
                self.logger.error(f"Streaming topic at index {idx} is not a dict: {topic}")
                return False

            # Check required fields in each topic
            required_fields = ['cameraId', 'topicName', 'topicType', 'serverId', 'serverType']
            missing_fields = [field for field in required_fields if field not in topic]

            if missing_fields:
                self.logger.warning(
                    f"Streaming topic at index {idx} missing fields: {missing_fields}, "
                    f"topic: {topic}"
                )
                # Don't fail validation, just warn - might still be usable

        return True

    def _handle_refresh_event(self, event: Dict[str, Any], streaming_topics: List[Dict[str, Any]]):
        """Handle refresh event by triggering reconciliation.

        Args:
            event: Full event dict
            streaming_topics: List of StreamingTopics from event data
        """
        try:
            self.logger.warning(
                f"Refresh reconciliation triggered: {len(streaming_topics)} streaming topics in snapshot"
            )

            # Call the callback to handle refresh
            if self.on_refresh:
                self.on_refresh(event)
                self.stats["refreshes_processed"] += 1
                self.stats["consecutive_failures"] = 0
                # Reset circuit breaker on success
                if self.circuit_open:
                    self.logger.info("Circuit breaker CLOSED - refresh processed successfully after failures")
                    self.circuit_open = False
                self.logger.info("Refresh event successfully processed")
            else:
                self.logger.error("No refresh callback registered")
                self.stats["refreshes_failed"] += 1
                self.stats["consecutive_failures"] += 1
                self._check_circuit_breaker()

        except Exception as e:
            self.stats["refreshes_failed"] += 1
            self.stats["consecutive_failures"] += 1
            self._check_circuit_breaker()
            self.logger.error(
                f"Error processing refresh event: {e}\n"
                f"Event timestamp: {event.get('timestamp')}\n"
                f"Streaming topics count: {len(streaming_topics)}",
                exc_info=True
            )

    def _check_circuit_breaker(self):
        """Check if circuit breaker should be opened based on consecutive failures."""
        if self.stats["consecutive_failures"] >= self.max_consecutive_failures:
            if not self.circuit_open:
                self.circuit_open = True
                self.logger.critical(
                    f"Circuit breaker OPENED after {self.stats['consecutive_failures']} consecutive failures. "
                    f"Refresh listener will ignore all events until manual intervention. "
                    f"Total failures: {self.stats['refreshes_failed']}/{self.stats['refreshes_received']}"
                )
        elif self.stats["consecutive_failures"] > self.max_consecutive_failures // 2:
            # Warning at 50% threshold
            self.logger.warning(
                f"Refresh listener approaching failure threshold: {self.stats['consecutive_failures']}/"
                f"{self.max_consecutive_failures} consecutive failures"
            )

    def get_statistics(self) -> dict:
        """Get refresh listener statistics.

        Returns:
            dict: Statistics including refresh counts and listener stats
        """
        listener_stats = self._listener.get_statistics()

        return {
            "refresh_listener": self.stats.copy(),
            "generic_listener": listener_stats,
            "topic_name": self.topic_name,
            "is_listening": self.is_listening,
            "circuit_breaker": {
                "open": self.circuit_open,
                "max_consecutive_failures": self.max_consecutive_failures
            }
        }
