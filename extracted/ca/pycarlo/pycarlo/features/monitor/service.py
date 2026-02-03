from __future__ import annotations

import time
from typing import Callable, Optional

from pycarlo.common import get_logger
from pycarlo.common.settings import (
    HEADER_MCD_TELEMETRY_REASON,
    HEADER_MCD_TELEMETRY_SERVICE,
    RequestReason,
)
from pycarlo.core import Client
from pycarlo.features.monitor.models import (
    AgentMonitorConfig,
    AgentSpanFilterConfig,
    MonitorExecutionStatus,
)
from pycarlo.features.monitor.queries import (
    GET_AGENT_MONITOR_MINIMAL,
    GET_MANUAL_MONITOR_EXECUTION_STATUS,
    RUN_MONITOR,
)

logger = get_logger(__name__)


class MonitorService:
    """Service for running and polling monitor executions."""

    def __init__(
        self,
        mc_client: Optional[Client] = None,
        print_func: Callable[..., None] = logger.info,
    ):
        """
        Initialize MonitorService.

        :param mc_client: MCD client (e.g. for creating a custom session); created otherwise.
        :param print_func: Function to use for echoing. Uses python logging by default.
        """
        self._client = mc_client or Client()
        self._print_func = print_func

    def run_monitor(
        self,
        monitor_uuid: str,
        runtime_variables: Optional[dict[str, str]] = None,
    ) -> str:
        """
        Run a monitor and return the execution UUID.

        :param monitor_uuid: UUID of the monitor to run
        :param runtime_variables: Optional runtime variables as key-value pairs
        :return: Manual monitor execution UUID
        :raises ValueError: If the monitor run fails
        """
        variables: dict[str, object] = {"monitorUuid": monitor_uuid}

        if runtime_variables:
            variables["runtimeVariables"] = [
                {"name": key, "value": value} for key, value in runtime_variables.items()
            ]

        response = self._client(
            query=RUN_MONITOR,
            variables=variables,
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "monitor_service",
            },
        )

        result = response.run_monitor  # type: ignore[union-attr]
        if not result.success:
            raise ValueError("Failed to run monitor")

        execution_uuid = str(result.manual_monitor_execution_uuid)
        self._print_func(f"Started monitor execution. UUID: {execution_uuid}")
        return execution_uuid

    def get_execution_status(self, execution_uuid: str) -> MonitorExecutionStatus:
        """
        Get status of a monitor execution.

        :param execution_uuid: Manual monitor execution UUID
        :return: MonitorExecutionStatus with status, breached, and completed fields
        """
        response = self._client(
            query=GET_MANUAL_MONITOR_EXECUTION_STATUS,
            variables={"manualMonitorExecutionUuid": execution_uuid},
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "monitor_service",
            },
        )

        result = response.get_manual_monitor_execution_status  # type: ignore[union-attr]
        return MonitorExecutionStatus(
            status=str(result.status),
            breached=bool(result.breached) if result.breached is not None else None,
            completed=bool(result.completed),
        )

    def run_and_poll(
        self,
        monitor_uuid: str,
        runtime_variables: Optional[dict[str, str]] = None,
        timeout_in_minutes: int = 10,
        poll_interval_seconds: int = 5,
    ) -> bool:
        """
        Run monitor and poll until complete.

        :param monitor_uuid: UUID of the monitor to run
        :param runtime_variables: Optional runtime variables as key-value pairs
        :param timeout_in_minutes: Polling timeout in minutes
        :param poll_interval_seconds: Seconds between poll attempts
        :return: True if breached, False otherwise
        :raises TimeoutError: If polling times out before completion
        :raises ValueError: If monitor execution fails
        """
        execution_uuid = self.run_monitor(monitor_uuid, runtime_variables)

        timeout_start = time.time()
        timeout_seconds = timeout_in_minutes * 60

        while time.time() < timeout_start + timeout_seconds:
            status = self.get_execution_status(execution_uuid)
            self._print_func(
                f"Monitor execution status: {status.status}, "
                f"completed: {status.completed}, breached: {status.breached}"
            )

            if status.completed:
                if status.status == "FAILURE":
                    raise ValueError(f"Monitor execution failed: {execution_uuid}")
                return status.breached is True

            self._print_func(f"Execution not complete. Polling again in {poll_interval_seconds}s.")
            time.sleep(poll_interval_seconds)

        raise TimeoutError(f"Monitor execution timed out after {timeout_in_minutes} minutes")

    def get_agent_monitor_config(self, monitor_uuid: str) -> AgentMonitorConfig:
        """
        Get agent monitor configuration by UUID.

        :param monitor_uuid: UUID of the monitor
        :return: AgentMonitorConfig with monitor details including agentSpanFilters and mcon
        :raises ValueError: If monitor not found
        """
        response = self._client(
            query=GET_AGENT_MONITOR_MINIMAL,
            variables={"uuids": [monitor_uuid]},
            additional_headers={
                HEADER_MCD_TELEMETRY_REASON: RequestReason.SERVICE.value,
                HEADER_MCD_TELEMETRY_SERVICE: "monitor_service",
            },
        )

        monitors = response.get_monitors  # type: ignore[union-attr]
        if not monitors or len(monitors) == 0:
            raise ValueError(f"Monitor not found: {monitor_uuid}")

        monitor = monitors[0]

        # Extract agent span filters
        agent_span_filters: list[AgentSpanFilterConfig] = []
        if monitor.agent_span_filters:
            for f in monitor.agent_span_filters:
                agent_span_filters.append(
                    AgentSpanFilterConfig(
                        agent=str(f.agent.value) if f.agent else None,
                        workflow=str(f.workflow.value) if f.workflow else None,
                        task=str(f.task.value) if f.task else None,
                        span_name=str(f.span_name.value) if f.span_name else None,
                    )
                )

        # Extract runtime variable names and attribute key from filter conditions
        runtime_var_names: list[str] = []
        attribute_key: str | None = None
        if monitor.filters and monitor.filters.conditions:
            for condition in monitor.filters.conditions:
                # Extract attribute key from left side (e.g., MAP_KEY with key)
                if hasattr(condition, "left") and condition.left:
                    for val in condition.left:
                        if hasattr(val, "key") and val.key:
                            attribute_key = str(val.key)
                # Extract runtime variable names from right side (e.g., {{ci_build_id}})
                if hasattr(condition, "right") and condition.right:
                    for val in condition.right:
                        if hasattr(val, "literal") and val.literal:
                            literal = str(val.literal)
                            if literal.startswith("{{") and literal.endswith("}}"):
                                runtime_var_names.append(literal[2:-2])

        # Get MCON from entityMcons
        mcon = None
        if monitor.entity_mcons and len(monitor.entity_mcons) > 0:
            mcon = str(monitor.entity_mcons[0])

        return AgentMonitorConfig(
            uuid=str(monitor.uuid),
            name=str(monitor.name) if monitor.name else "",
            description=str(monitor.description) if monitor.description else None,
            monitor_type=str(monitor.monitor_type) if monitor.monitor_type else "",
            mcon=mcon,
            agent_span_filters=agent_span_filters,
            runtime_variable_names=runtime_var_names,
            attribute_key=attribute_key,
        )
