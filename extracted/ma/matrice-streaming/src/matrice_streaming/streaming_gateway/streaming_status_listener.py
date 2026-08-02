"""Kafka listener for streaming gateway status events (stop commands)."""

from __future__ import annotations

import logging
from typing import Callable

from matrice_common.session import Session
from matrice_common.stream import EventListener as GenericEventListener


class StreamingStatusListener:
    """Listener for streaming gateway status events from Kafka.

    This class listens to the Streaming_Events_Status topic and triggers
    a callback when a stop command is received for this gateway.
    """

    def __init__(
        self,
        session: Session,
        streaming_gateway_id: str,
        action_id: str,
        on_stop_callback: Callable[[], None],
    ) -> None:
        """Initialize status listener.

        Args:
            session: Session object for authentication
            streaming_gateway_id: ID of streaming gateway to filter events
            action_id: ID of action record to filter events
            on_stop_callback: Callback function to invoke when stop event is received
        """
        self.streaming_gateway_id = streaming_gateway_id
        self.action_id = action_id
        self.on_stop_callback = on_stop_callback
        self.logger = logging.getLogger(__name__)

        # Create generic event listener for Streaming_Events_Status
        self._listener = GenericEventListener(
            session=session,
            topics=["Streaming_Events_Status"],
            event_handler=self.handle_event,
            filter_field="streamingGatewayId",
            filter_value=streaming_gateway_id,
            consumer_group_id=f"stg_status_events_{streaming_gateway_id}_{str(action_id)}",
        )

        self.logger.info(f"StreamingStatusListener initialized for gateway {streaming_gateway_id}")

    @property
    def is_listening(self) -> bool:
        """Check if listener is active."""
        return self._listener.is_listening

    def start(self) -> bool:
        """Start listening to status events.

        Returns:
            bool: True if started successfully
        """
        return self._listener.start()

    def stop(self):
        """Stop listening."""
        self._listener.stop()

    def handle_event(self, event: dict):
        """Handle status event.

        Args:
            event: Status event dict with eventType, streamingGatewayId, timestamp
        """
        if event.get("actionId") != self.action_id:
            self.logger.info(f"Ignoring event for action {event.get('actionId')} - not matching {self.action_id}")
            return

        event_type = event.get("eventType")

        self.logger.info(f"Received status event: {event_type} for gateway {self.streaming_gateway_id}")

        if event_type == "stopped":
            self.logger.info(f"Stop command received for gateway {self.streaming_gateway_id}")
            try:
                self.on_stop_callback()
            except Exception as e:
                self.logger.error(f"Error executing stop callback: {e}", exc_info=True)
        else:
            self.logger.debug(f"Ignoring event type: {event_type}")

    def get_statistics(self) -> dict:
        """Get statistics."""
        return self._listener.get_statistics()
