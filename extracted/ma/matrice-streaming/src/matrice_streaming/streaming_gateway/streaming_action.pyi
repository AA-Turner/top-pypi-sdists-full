"""Auto-generated stub for module: streaming_action."""
from typing import Any, Dict, Optional

from __future__ import annotations
from constants import GatewayStatus
from matrice_common.rpc import RPC
from matrice_common.session import Session
from metrics_reporter import MetricsConfig, MetricsManager
from streaming_gateway import USE_NVDEC, StreamingGateway
from streaming_gateway_utils import InstanceStreamingGatewayUtil, StreamingGatewayUtil
from streaming_status_listener import StreamingStatusListener
import logging
import os
import threading
import time

# Constants
logger: Any

# Classes
class StreamingAction:
    """
    High-level orchestrator for streaming gateway lifecycle management.
    
    This class automates the entire streaming process:
    1. Fetches configuration from API using streaming_gateway_id
    2. Sets up StreamingGateway with proper configuration
    3. Starts streaming with status updates to API
    4. Monitors streaming health
    5. Periodically checks if action ID matches streaming gateway's actionRecordID
    6. Automatically stops if action ID mismatch is detected
    7. Handles errors and recovery
    8. Provides clean shutdown
    
    Example usage:
        orchestrator = StreamingAction(
            session=session,
            action_id="your_action_id",
            action_id_check_interval=30.0,  # Check every 30 seconds
        )
    
        # Start streaming (auto-fetches config, sets up, and starts)
        if orchestrator.start():
            logger.info("Streaming started successfully!")
    
            # Monitor for a while
            time.sleep(60)
    
            # Stop when done
            orchestrator.stop()
        else:
            logger.error("Failed to start streaming")
    """

    def __init__(self: Any, session: Session, action_id: str, enable_intelligent_transmission: bool = True, monitoring_interval: float = 30.0, auto_restart: bool = True, max_restart_attempts: int = 3, action_id_check_interval: float = 600.0, enable_event_listening: bool = True, allow_empty_start: bool = True) -> None: ...
        """
        Initialize StreamingAction.
        
                Args:
                    session: Session object for authentication
                    action_id: ID of the action to manage
                    enable_intelligent_transmission: Whether to enable intelligent frame transmission
                    monitoring_interval: Interval in seconds between health checks and heartbeats (default: 30 seconds)
                    auto_restart: Whether to automatically restart on failures
                    max_restart_attempts: Maximum number of restart attempts before giving up
                    action_id_check_interval: Interval in seconds between checks to verify action ID matches streaming gateway
                    enable_event_listening: Enable dynamic event listening for configuration updates
                    allow_empty_start: Allow starting with zero cameras (default True). Cameras can be added dynamically.
        """

    def check_action_id_matches(self: Any) -> bool: ...
        """
        Check if the current action ID matches the streaming gateway's actionRecordID.
        
        Handles transient errors gracefully:
        - 502 Bad Gateway: Skip check, continue streaming (server temporarily unavailable)
        - 404 Not Found: Stop streaming (gateway may be deleted)
        - Other API errors: Skip check, continue streaming (don't stop on transient issues)
        
        Returns:
            bool: True if action ID matches or check should be skipped, False if mismatch or gateway deleted
        """

    def get_status(self: Any) -> Dict: ...
        """
        Get current orchestrator status and statistics.
        
        Returns:
            Dict: Complete status information
        """

    def is_healthy(self: Any) -> bool: ...
        """
        Check if the orchestrator is healthy.
        
        Returns:
            bool: True if healthy, False otherwise
        """

    def restart(self: Any) -> bool: ...
        """
        Restart the streaming orchestrator.
        
        Returns:
            bool: True if restarted successfully, False otherwise
        """

    def start(self: Any, block: bool = True) -> bool: ...
        """
        Start the streaming orchestrator.
        
        This method:
        1. Fetches streaming configuration from API
        2. Creates and configures StreamingGateway
        3. Starts streaming with API status updates
        4. Starts health monitoring
        
        Args:
            block: Whether to block the thread until the streaming gateway is started (default: True)
        
        Returns:
            bool: True if started successfully, False otherwise
        """

    def stop(self: Any) -> bool: ...
        """
        Stop the streaming orchestrator.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """

    def update_status(self: Any, step_code: str, status: str, status_description: str) -> None: ...
        """
        Update the status of the data processing job.
        """

