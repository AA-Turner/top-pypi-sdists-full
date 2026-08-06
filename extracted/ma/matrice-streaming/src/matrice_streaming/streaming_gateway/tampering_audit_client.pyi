"""Auto-generated stub for module: tampering_audit_client."""
from typing import Any, Dict, Optional

from __future__ import annotations
from matrice_streaming.streaming_gateway.camera_streamer.camera_tampering_detector import TAMPERING_TYPES, utc_now_rfc3339
import logging

# Constants
AUDIT_TAMPERING_PATH: str
logger: Any

# Classes
class TamperingAuditClient:
    """
    Thin RPC client for camera tampering audit persistence.
    """

    def __init__(self: Any, session: Any) -> None: ...

    def report_tampering(self: Any, camera_id: str, tampering_type: str) -> bool: ...
        """
        Persist one tampering event. Returns True on HTTP 2xx / success payload.
        """

