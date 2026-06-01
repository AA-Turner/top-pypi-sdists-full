"""
Client-side sampling for SDK events.

Implements hash-based deterministic sampling to reduce bandwidth
and processing load for high-volume applications.
"""

import hashlib
import logging

logger = logging.getLogger(__name__)


def is_trace_sampled(trace_id: str, sample_rate: float) -> bool:
    """
    Check if a trace should be sampled using deterministic hashing.

    Args:
        trace_id: Trace ID to check
        sample_rate: Sample rate (0.0-1.0)

    Returns:
        True if trace should be sampled, False otherwise
    """
    if sample_rate >= 1.0:
        return True

    if sample_rate <= 0.0:
        return False

    # Hash trace_id using SHA-256
    hash_obj = hashlib.sha256(trace_id.encode("utf-8"))
    hash_hex = hash_obj.hexdigest()

    # Take first 8 characters (32 bits)
    hash_int = int(hash_hex[:8], 16)

    # Normalize to 0-1 range
    normalized = hash_int / (16**8)  # Max value for 8 hex chars

    # Check if within sample rate
    return normalized < sample_rate


def should_send_event(trace_id: str | None, sample_rate: float | None) -> bool:
    """
    Determine if an event should be sent based on sampling.

    Args:
        trace_id: Optional trace ID (if None, always send)
        sample_rate: Optional sample rate (if None, always send)

    Returns:
        True if event should be sent, False otherwise
    """
    if sample_rate is None:
        return True

    if trace_id is None:
        return True

    return is_trace_sampled(trace_id, sample_rate)
