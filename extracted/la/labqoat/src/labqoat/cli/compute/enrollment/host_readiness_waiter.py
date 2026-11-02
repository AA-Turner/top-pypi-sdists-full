"""Bounded polling until an enrolled host reports ready with a derived resource share."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field

from labqoat.cli.compute.enrollment.enrollment_error import EnrollmentError
from labqoat.compute_client import ComputeClient
from labqoat.json_document import JsonDocument


@dataclass
class HostReadinessWaiter:
    """Poll the host resource with an injectable clock so tests never sleep."""

    client: ComputeClient
    timeout_seconds: float = 120.0
    interval_seconds: float = 2.0
    clock: Callable[[], float] = field(default=time.monotonic)
    sleep: Callable[[float], None] = field(default=time.sleep)

    def wait(self, host_id: str) -> JsonDocument:
        """Return the ready host or fail with the last observed state and share."""
        deadline = self.clock() + self.timeout_seconds
        while True:
            host = self.host(self.client.host(host_id))
            if host.get("state") == "ready" and host.get("share"):
                return host
            if self.clock() >= deadline:
                raise EnrollmentError(
                    f"Host {host_id} was not ready after {self.timeout_seconds:g}s; last observed "
                    f"state={host.get('state')!r}, share={host.get('share')!r}, devices={host.get('gpu_devices')!r}"
                )
            self.sleep(self.interval_seconds)

    @staticmethod
    def host(document: JsonDocument) -> JsonDocument:
        """Accept the host either bare or wrapped in a ``host`` member."""
        wrapped = document.get("host")
        return JsonDocument.expect_dict(wrapped) if isinstance(wrapped, dict) else document
