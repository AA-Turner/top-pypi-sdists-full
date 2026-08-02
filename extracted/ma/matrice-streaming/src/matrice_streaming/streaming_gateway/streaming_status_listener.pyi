"""Auto-generated stub for module: streaming_status_listener."""
from typing import Any

from __future__ import annotations
from matrice_common.session import Session
from matrice_common.stream import EventListener
import logging

# Classes
class StreamingStatusListener:
    """
    Listener for streaming gateway status events from Kafka.
    
        This class listens to the Streaming_Events_Status topic and triggers
        a callback when a stop command is received for this gateway.
    """

    def __init__(self: Any, session: Session, streaming_gateway_id: str, action_id: str, on_stop_callback: Any) -> None: ...
        """
        Initialize status listener.
        
                Args:
                    session: Session object for authentication
                    streaming_gateway_id: ID of streaming gateway to filter events
                    action_id: ID of action record to filter events
                    on_stop_callback: Callback function to invoke when stop event is received
        """

    def get_statistics(self: Any) -> dict: ...
        """
        Get statistics.
        """

    def handle_event(self: Any, event: dict) -> Any: ...
        """
        Handle status event.
        
                Args:
                    event: Status event dict with eventType, streamingGatewayId, timestamp
        """

    def is_listening(self: Any) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self: Any) -> bool: ...
        """
        Start listening to status events.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self: Any) -> Any: ...
        """
        Stop listening.
        """

