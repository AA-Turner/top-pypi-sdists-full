from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MonitorExecutionStatus:
    """Status of a manual monitor execution.

    Attributes:
        status: Execution status (IN_PROGRESS, SUCCESS, FAILURE)
        breached: Whether the monitor breached (None if still in progress)
        completed: Whether the execution has completed
    """

    status: str
    breached: Optional[bool]
    completed: bool


@dataclass
class AgentSpanFilterConfig:
    """Agent span filter configuration from a monitor."""

    agent: Optional[str] = None
    workflow: Optional[str] = None
    task: Optional[str] = None
    span_name: Optional[str] = None


@dataclass
class AgentMonitorConfig:
    """Monitor configuration retrieved from getMonitors API.

    Attributes:
        uuid: Monitor UUID
        name: Monitor name
        description: Monitor description
        monitor_type: Type of monitor (e.g., AGENT)
        mcon: MCON of the monitored table (first entityMcon)
        agent_span_filters: List of agent span filters for AGENT monitors
        runtime_variable_names: List of runtime variable names from filter conditions
        attribute_key: Attribute key from filter conditions
    """

    uuid: str
    name: str
    description: Optional[str]
    monitor_type: str
    mcon: Optional[str]
    agent_span_filters: list[AgentSpanFilterConfig] = field(default_factory=list)
    runtime_variable_names: list[str] = field(default_factory=list)
    attribute_key: Optional[str] = None
