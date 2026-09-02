"""
Threshold and budget calculation functions.

Direct port of: packages/memory/src/processors/observational-memory/thresholds.ts
"""

from __future__ import annotations

import math
from typing import Union

from .types import BufferedObservationChunk, ThresholdRange


TokenThreshold = Union[int, ThresholdRange]


# ---------------------------------------------------------------------------
# Dynamic threshold (shared budget mode)
# ---------------------------------------------------------------------------

def calculate_dynamic_threshold(
    threshold: TokenThreshold,
    current_other_tokens: int,
) -> int:
    """
    When share_token_budget is True, the effective threshold for one tier
    is: max(total_budget - current_other_tokens, min_threshold).
    
    Args:
        threshold: A fixed int, or a ThresholdRange(min, max).
        current_other_tokens: Current token count in the OTHER tier
            (e.g., observation tokens when computing message threshold).
    
    Returns:
        Effective token threshold (always >= min).
    """
    if isinstance(threshold, int):
        return threshold

    total_budget = threshold.max
    min_threshold = threshold.min
    effective = max(total_budget - current_other_tokens, min_threshold)
    return round(effective)


# ---------------------------------------------------------------------------
# Buffer threshold
# ---------------------------------------------------------------------------

def resolve_buffer_tokens(
    buffer_tokens: float,
    message_tokens_threshold: int,
) -> int:
    """
    Convert the buffer_tokens config value to an absolute token count.
    
    If buffer_tokens < 1.0, it's a fraction of message_tokens_threshold.
    If buffer_tokens >= 1.0, it's already an absolute count.
    
    Default: 0.2 → 20% of 30,000 = 6,000 tokens.
    """
    if buffer_tokens < 1.0:
        return round(buffer_tokens * message_tokens_threshold)
    return round(buffer_tokens)


# ---------------------------------------------------------------------------
# Block-after threshold (force synchronous observation)
# ---------------------------------------------------------------------------

def resolve_block_after(
    block_after: float,
    message_tokens_threshold: int,
) -> int:
    """
    Values 1.0–100.0 are treated as multipliers of message_tokens_threshold.
    Values >100 are treated as absolute token counts.
    
    Default: 1.2 → 1.2 × 30,000 = 36,000 tokens.
    """
    if 1.0 < block_after <= 100.0:
        return round(block_after * message_tokens_threshold)
    return round(block_after)


# ---------------------------------------------------------------------------
# Buffer activation / retention
# ---------------------------------------------------------------------------

def resolve_retention_floor(
    buffer_activation: float,
    message_tokens_threshold: int,
) -> int:
    """
    After activation, how many message tokens to RETAIN (not remove).
    
    buffer_activation=0.8 means: activate when we have 80% pending, which
    implies retain 20% (the floor).
    
    retention_floor = (1 - buffer_activation) × threshold
    
    Values >= 1000 are treated as absolute token counts.
    """
    if buffer_activation >= 1000:
        return round(buffer_activation)
    # 0-1 range: convert to absolute
    retention_ratio = 1.0 - buffer_activation
    return round(retention_ratio * message_tokens_threshold)


def resolve_activation_ratio(
    buffer_activation: float,
    message_tokens_threshold: int,
) -> float:
    """
    Returns a 0.0–1.0 ratio used to determine if buffered chunks should activate.
    
    buffer_activation=0.8 means: activate when unobserved tokens >= 80% of threshold.
    
    Values >= 1000 become: absolute_value / threshold.
    """
    if buffer_activation >= 1000:
        return buffer_activation / message_tokens_threshold
    return buffer_activation


# ---------------------------------------------------------------------------
# Projected message removal (for activation estimation)
# ---------------------------------------------------------------------------

def calculate_projected_message_removal(
    chunks: list[BufferedObservationChunk],
    buffer_activation: float,
    threshold: int,
    current_pending_tokens: int,
) -> int:
    """
    Estimate how many message tokens would be removed if we activated all
    buffered chunks right now.
    
    During activation we retain a floor of messages. The rest are removed.
    
    Returns the projected token count that would remain after activation.
    """
    retention_floor = resolve_retention_floor(buffer_activation, threshold)
    total_chunk_message_tokens = sum(c.message_tokens for c in chunks)

    # We remove the chunk tokens from the pending tokens
    remaining_pending = max(0, current_pending_tokens - total_chunk_message_tokens)

    # Remaining must be at least the retention floor
    retained = max(remaining_pending, retention_floor)
    return retained


# ---------------------------------------------------------------------------
# Convenience: get effective thresholds from config
# ---------------------------------------------------------------------------

def get_effective_message_threshold(
    message_tokens_config: TokenThreshold,
    current_observation_tokens: int,
) -> int:
    """Get the effective message threshold given current observation size."""
    return calculate_dynamic_threshold(message_tokens_config, current_observation_tokens)


def get_effective_observation_threshold(
    observation_tokens_config: TokenThreshold,
    current_message_tokens: int,
) -> int:
    """Get the effective observation threshold given current message size."""
    return calculate_dynamic_threshold(observation_tokens_config, current_message_tokens)
