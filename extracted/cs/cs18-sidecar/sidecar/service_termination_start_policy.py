from enum import Enum
from typing import List

from sidecar.model.objects import ISidecarService
from sidecar.services.service_status_state import ServiceStatusState, ServiceStatus


class CanStartTerminationProcessResult:
    TRUE = 'true'
    WAIT = 'wait'
    DEPENDENCIES_FAILURE = 'dependencies_failure'


class ServiceTerminationStartPolicy:
    def __init__(self, services: List[ISidecarService], service_status_state: ServiceStatusState):
        self._service_status_state = service_status_state

        service_names = set(s.name for s in services)
        # in teardown only dependencies between services are supported
        self._service_dependencies = {service.name: list([d for d in service.dependencies if d in service_names]) for
                                      service in services}

    def can_start_termination_process(self, service_name: str) -> str:
        dependencies = self._service_dependencies.get(service_name, [])
        service_statuses = self._service_status_state.get_status(service_names=dependencies)

        # ignore all services with validation failed status
        dependencies_status = [status for status in service_statuses.values()
                               if status != ServiceStatus.VALIDATION_FAILED]

        if not dependencies_status:
            return CanStartTerminationProcessResult.TRUE

        if all(status == ServiceStatus.TERMINATED for status in dependencies_status):
            return CanStartTerminationProcessResult.TRUE

        if any(status == ServiceStatus.TERMINATE_FAILED for status in dependencies_status):
            return CanStartTerminationProcessResult.DEPENDENCIES_FAILURE

        return CanStartTerminationProcessResult.WAIT
