import threading
from typing import List, Dict

from sidecar.model.objects import ISidecarService


class ServiceStatus:
    PENDING = "Pending"
    SETUP = "Setup"
    DONE = "Done"
    SETUP_FAILED = "SetupFailed"
    ABORTED = "Aborted"
    TERMINATING = "Terminating"
    TERMINATE_FAILED = "TerminateFailed"
    TERMINATED = "Terminated"
    VALIDATION_FAILED = "ValidationFailed"

class ServiceStatusState:

    def __init__(self, services: List[ISidecarService]):
        self._lock = threading.RLock()
        self._service_statuses = {service.name: ServiceStatus.PENDING for service in services}

    def execution_done(self, names: List[str]) -> bool:
        with self._lock:
            for name in names:
                if self._service_statuses[name] not in [ServiceStatus.DONE]:
                    return False
            return True

    def any_execution_failed(self, names: List[str]) -> bool:
        with self._lock:
            for name in names:
                if self._service_statuses[name] in [ServiceStatus.SETUP_FAILED,
                                                    ServiceStatus.ABORTED,
                                                    ServiceStatus.VALIDATION_FAILED]:
                    return True
            return False

    def get_status(self, service_names: List[str]) -> Dict[str, str]:
        with self._lock:
            return {s: self._service_statuses.get(s, None) for s in service_names}

    def update_status(self, name: str, status: str):
        with self._lock:
            self._service_statuses[name] = status
