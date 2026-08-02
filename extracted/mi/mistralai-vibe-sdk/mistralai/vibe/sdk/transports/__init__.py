"""Canonical namespace for Vibe SDK transport (delivery / channel) implementations.

Transports own the boundary that streams state, events, and results between the
execution loop and its consumers: channel ports, event shapes, and the
local/HTTP/workflow adapters that carry them.
"""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "CallbackCallEvent",
    "CallbackCallPayload",
    "CallbackResultEvent",
    "CallbackResultPayload",
    "CallbackStateUpdateEvent",
    "CallbackStateUpdatePayload",
    "Channel",
    "DownstreamMessage",
    "TaskCancellationEvent",
    "TaskResultEvent",
    "TaskResultPayload",
    "TaskStateUpdateEvent",
    "TaskStateUpdatePayload",
    "UpstreamMessage",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.transports.channel import Channel
    from mistralai.vibe.sdk.transports.events import (
        CallbackCallEvent,
        CallbackCallPayload,
        CallbackResultEvent,
        CallbackResultPayload,
        CallbackStateUpdateEvent,
        CallbackStateUpdatePayload,
        DownstreamMessage,
        TaskCancellationEvent,
        TaskResultEvent,
        TaskResultPayload,
        TaskStateUpdateEvent,
        TaskStateUpdatePayload,
        UpstreamMessage,
    )

_LAZY_EXPORTS = {
    "CallbackCallEvent": "mistralai.vibe.sdk.transports.events",
    "CallbackCallPayload": "mistralai.vibe.sdk.transports.events",
    "CallbackResultEvent": "mistralai.vibe.sdk.transports.events",
    "CallbackResultPayload": "mistralai.vibe.sdk.transports.events",
    "CallbackStateUpdateEvent": "mistralai.vibe.sdk.transports.events",
    "CallbackStateUpdatePayload": "mistralai.vibe.sdk.transports.events",
    "Channel": "mistralai.vibe.sdk.transports.channel",
    "DownstreamMessage": "mistralai.vibe.sdk.transports.events",
    "TaskCancellationEvent": "mistralai.vibe.sdk.transports.events",
    "TaskResultEvent": "mistralai.vibe.sdk.transports.events",
    "TaskResultPayload": "mistralai.vibe.sdk.transports.events",
    "TaskStateUpdateEvent": "mistralai.vibe.sdk.transports.events",
    "TaskStateUpdatePayload": "mistralai.vibe.sdk.transports.events",
    "UpstreamMessage": "mistralai.vibe.sdk.transports.events",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
