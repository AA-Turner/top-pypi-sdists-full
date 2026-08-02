"""Auto-generated stub for module: instance_event_listener."""
from typing import Any, Dict, Optional

from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from matrice_common.session import Session
from matrice_common.stream import EventListener
import logging
import os
import threading
import time

# Constants
PERIODIC_CIRCUIT_COOLDOWN_CAP_SEC: float
PHANTOM_GRACE_SEC: float

# Classes
class InstanceEventListener:
    """
    Refresh-based listener for instance-specific streaming events.
    
        Subscribes to:
        - {instance_id}_streaming_gateway_event
    
        On any message received, re-fetches the full camera list from the
        consuming topics API and diffs against the current camera manager state.
    
        Also runs a periodic auto-refresh timer as a safety net.
    """

    def __init__(self: Any, session: Session, instance_id: str, camera_manager: Any, instance_util: Any, auto_refresh_interval: float = 60.0) -> None: ...
        """
        Initialize instance event listener.
        
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

    def get_statistics(self: Any) -> dict: ...
        """
        Get event listener statistics.
        """

    def handle_event(self: Any, event: Dict[str, Any]) -> Any: ...
        """
        Handle any instance event by triggering a refresh.
        
                All events on instance topics are treated as refresh triggers.
                The actual camera list is always re-fetched from the API.
        
                Args:
                    event: Event dict (structure varies, but we only use it for logging)
        """

    def is_listening(self: Any) -> bool: ...
        """
        Check if listener is active.
        """

    def start(self: Any) -> bool: ...
        """
        Start listening to instance events and periodic refresh.
        
                Returns:
                    bool: True if started successfully
        """

    def stop(self: Any) -> Any: ...
        """
        Stop listening and periodic refresh.
        """

