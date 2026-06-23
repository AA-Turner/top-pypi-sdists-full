"""
Aigie Callbacks - Custom callback handlers for observability data.

This module provides callback handlers that allow sending span/trace data
to custom destinations, inspired by LiteLLM's GenericAPILogger pattern.

Available Callbacks:
- GenericWebhookCallback: Send span data to any HTTP endpoint
- ConsoleCallback: Log spans to console (for debugging)
- FileCallback: Write spans to file

Usage:
    from aigie.callbacks import GenericWebhookCallback

    # Create webhook callback
    webhook = GenericWebhookCallback(
        endpoint="https://my-service.com/logs",
        headers={"Authorization": "Bearer token123"}
    )

    # Add to Aigie
    aigie.add_callback(webhook)
"""

from aigie.callbacks.base import BaseCallback, CallbackEvent, CallbackEventType
from aigie.callbacks.generic_webhook import GenericWebhookCallback

__all__ = [
    "BaseCallback",
    "CallbackEvent",
    "CallbackEventType",
    "GenericWebhookCallback",
]
