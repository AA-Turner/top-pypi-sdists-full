"""service: the Probe service's part a training process's SDK needs (plan D28), public and pure Python.

`SdkMethods` (outbox drains, box watchers, telemetry, the `api.call` relay, `files.hash` hashing,
held keys) is the one copy both the machine service and the delivery service (`DeliveryService`,
`python -m probe.sdk.delivery.service`) serve. DESIGN.md beside this file."""

from __future__ import annotations

from .connection import Connection
from .methods import SDK_METHODS, SdkMethods

__all__ = ["SDK_METHODS", "Connection", "SdkMethods"]
