"""Lag-one delivery queue for completed flow summaries (``runlayer run`` path).

A flow completes only after its own ``/post`` step returns, so the current
flow can never ride its own request. Instead, completed summaries queue here
and the next outgoing backend call (``RunlayerClient.pre``/``post``) drains the
queue into a ``client_flows`` envelope attached to its body — zero extra HTTP
requests. The final flow before process exit is lost; accepted trade-off.

Stdlib-only (cli/AGENTS.md): imported by ``api.py``, which is in the
``aiwatch`` PyInstaller closure.
"""

from __future__ import annotations

import threading
from collections import deque
from typing import Any

from runlayer_cli.flow_contract import MAX_FLOWS_PER_ENVELOPE, build_envelope


class FlowDeliveryQueue:
    """Bounded drop-oldest queue; ``enqueue`` is the flow sink for ``runlayer run``."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._flows: deque[dict[str, Any]] = deque(maxlen=MAX_FLOWS_PER_ENVELOPE)
        self._dropped = 0

    def enqueue(self, summary: dict[str, Any]) -> None:
        with self._lock:
            if len(self._flows) == MAX_FLOWS_PER_ENVELOPE:
                # deque(maxlen=...) evicts silently; count the drop ourselves.
                self._dropped += 1
            self._flows.append(summary)

    def drain(self) -> dict[str, Any] | None:
        """Return a ``client_flows`` envelope and empty the queue, or ``None``."""
        with self._lock:
            if not self._flows:
                return None
            flows = list(self._flows)
            dropped = self._dropped
            self._flows.clear()
            self._dropped = 0
        return build_envelope(flows, dropped)
