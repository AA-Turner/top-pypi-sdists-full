"""
Message utility functions for Observational Memory.
Handles message traversal, observation markers, and boundary detection.

Mirrors: packages/memory/src/processors/observational-memory/message-utils.ts
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Optional

from .types import Message, MessagePart


def find_last_completed_observation_boundary(message: Message) -> int:
    """
    Find the index of the last completed observation boundary (end marker) in a message's parts.
    Returns -1 if no completed observation is found.
    """
    content = message.content
    if not isinstance(content, list):
        return -1

    # Search from the end to find the most recent end marker
    for i in range(len(content) - 1, -1, -1):
        part = content[i]
        # We assume that data parts are stored as dicts or specific dataclasses 
        # that have a 'type' attribute. We can duck type it here.
        part_type = getattr(part, 'type', None)
        if isinstance(part, dict):
            part_type = part.get('type')
            
        if part_type == 'data-om-observation-end':
            return i
            
    return -1


def get_unobserved_parts(message: Message) -> list[Any]:
    """
    Get unobserved parts from a message.
    If the message has a completed observation (start + end), only return parts after the end.
    If observation is in progress (start without end), include parts before the start.
    Otherwise, return all parts.
    """
    content = message.content
    if not isinstance(content, list):
        # If it's a plain string, it's either fully observed or unobserved based on the marker logic elsewhere
        # But generally string content has no markers.
        return [content]

    end_marker_index = find_last_completed_observation_boundary(message)
    if end_marker_index == -1:
        # No completed observation - return parts that are not start markers
        unobserved = []
        for p in content:
            p_type = getattr(p, 'type', None)
            if isinstance(p, dict):
                p_type = p.get('type')
                
            if p_type != 'data-om-observation-start':
                unobserved.append(p)
        return unobserved

    # Return only parts after the end marker (excluding start/end/failed markers)
    unobserved = []
    for p in content[end_marker_index + 1:]:
        p_type = getattr(p, 'type', None)
        if isinstance(p, dict):
            p_type = p.get('type')
            
        if not (p_type and isinstance(p_type, str) and p_type.startswith('data-om-observation-')):
            unobserved.append(p)
            
    return unobserved


def has_unobserved_parts(message: Message) -> bool:
    """Check if a message has any unobserved parts."""
    return len(get_unobserved_parts(message)) > 0


def get_last_observed_message_cursor(messages: list[Message]) -> Optional[dict[str, str]]:
    """
    Compute a cursor pointing at the latest message by created_at.
    Returns {"created_at": iso_string, "id": message_id}
    """
    latest = None
    for msg in messages:
        if not msg.id or not msg.created_at:
            continue
        if not latest or msg.created_at > latest.created_at:
            latest = msg
            
    if latest:
        return {
            "created_at": latest.created_at.isoformat(),
            "id": latest.id
        }
    return None


def is_message_at_or_before_cursor(msg: Message, cursor: dict[str, str]) -> bool:
    """Check if a message is at or before a cursor (by created_at then id)."""
    if not msg.created_at:
        return False
    msg_iso = msg.created_at.isoformat()
    if msg_iso < cursor["created_at"]:
        return True
    if msg_iso == cursor["created_at"] and msg.id == cursor["id"]:
        return True
    return False


def combine_observations_for_buffering(
    active_observations: Optional[str],
    buffered_observations: Optional[str]
) -> Optional[str]:
    """Combine active and buffered observations for the buffering observer context."""
    if not active_observations and not buffered_observations:
        return None
    if not active_observations:
        return buffered_observations
    if not buffered_observations:
        return active_observations
    return f"{active_observations}\n\n--- BUFFERED (pending activation) ---\n\n{buffered_observations}"


def sort_threads_by_oldest_message(messages_by_thread: dict[str, list[Message]]) -> list[str]:
    """
    Sort threads by their oldest unobserved message.
    Returns thread IDs in order from oldest to most recent.
    """
    thread_infos = []
    for thread_id, messages in messages_by_thread.items():
        if not messages:
            continue
        oldest_timestamp = min(
            (m.created_at for m in messages if m.created_at), 
            default=datetime.utcnow()
        )
        thread_infos.append({
            "thread_id": thread_id,
            "oldest": oldest_timestamp
        })
        
    thread_infos.sort(key=lambda x: x["oldest"])
    return [t["thread_id"] for t in thread_infos]


def strip_thread_tags(observations: str) -> str:
    """
    Strip any thread tags that the Observer might have added.
    Thread attribution is handled externally by the system.
    """
    # Remove <thread ...> and </thread> tags
    stripped = re.sub(r'<\/?thread\b[^>]{0,1024}>', '', observations, flags=re.IGNORECASE)
    return stripped.strip()
