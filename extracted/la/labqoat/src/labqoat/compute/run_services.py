"""A run's services: the ones it serves to its project and the ones it calls there."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from labqoat.service.served_service import ServedService
    from labqoat.service.service import Service
    from labqoat.service.service_endpoint import ServiceEndpoint
    from labqoat.service.service_target import ServiceTarget
    from labqoat.worker.worker_api import WorkerApi


@dataclass(frozen=True)
class RunServices:
    """Name services under the run's own worker credentials, which decide the project they belong to.

    The tunnel and its websocket client load only when a run serves or calls a service.
    """

    NAME: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9][a-z0-9-]{0,62}")

    api: WorkerApi

    def serve(self, name: str, target: ServiceTarget, startup_timeout: float) -> ServedService:
        """Describe serving a local server under a name; entering the result starts it."""
        from labqoat.service.served_service import ServedService

        return ServedService(self._endpoint(name), target, startup_timeout)

    def lookup(self, name: str) -> Service:
        """Describe calling a name; nothing is contacted until it is used."""
        from labqoat.service.service import Service

        endpoint = self._endpoint(name)
        return Service(name, endpoint.call_url(), dict(endpoint.headers))

    def _endpoint(self, name: str) -> ServiceEndpoint:
        """Refuse a name the platform would refuse before any connection is made."""
        if self.NAME.fullmatch(name) is None:
            raise ValueError("A service name has 1 to 63 lowercase letters, digits or hyphens and starts with one")
        return self.api.service_endpoint(name)
