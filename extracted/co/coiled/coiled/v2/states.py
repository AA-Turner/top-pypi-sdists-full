import logging
from collections import Counter
from datetime import datetime
from enum import Enum
from typing import Dict, List, NamedTuple, Optional, Tuple

from coiled.utils import COILED_LOGGER_NAME

logger = logging.getLogger(COILED_LOGGER_NAME)

DISPLAY_DATETIME_FORMAT = "%H:%M:%S (%Z)"


class BaseStateEnum(str, Enum):
    """
    Abstract class intended to be used for all state Enums
    inherits from str for easy comparisons
    """

    # important for 3.11 compatibility
    def __str__(self) -> str:
        return self.value


class ClusterStateEnum(BaseStateEnum):
    """
    Valid states for Clusters
    """

    pending = "pending"
    starting = "starting"
    scaling = "scaling"
    ready = "ready"
    pausing = "pausing"
    paused = "paused"
    stopping = "stopping"
    stopped = "stopped"
    error = "error"

    def awaiting_readiness(self):
        return self.value in ("pending", "starting", "scaling")


class ClusterInfraStateEnum(BaseStateEnum):
    """Valid states for ClusterInfra."""

    queued = "queued"
    creating = "creating"
    error = "error"
    created = "created"
    destroying = "destroying"
    destroyed = "destroyed"


class ProcessStateEnum(BaseStateEnum):
    """
    Valid states for Processes
    """

    pending = "pending"
    starting = "starting"
    started = "started"
    pausing = "pausing"
    paused = "paused"
    stopping = "stopping"
    stopped = "stopped"
    error = "error"

    def awaiting_readiness(self):
        return self.value in ("pending", "starting", "scaling")


class InstanceStateEnum(BaseStateEnum):
    """
    Valid states for Instances
    """

    queued = "queued"
    starting = "starting"
    started = "started"
    ready = "ready"
    pausing = "pausing"
    paused = "paused"
    stopping = "stopping"
    stopped = "stopped"
    error = "error"


class StatefulObjectType(str, Enum):
    cluster = "cluster"
    scheduler = "scheduler"
    scheduler_instance = "scheduler_instance"
    cluster_infra = "cluster_infra"
    worker = "worker"
    worker_instance = "worker_instance"

    # important for 3.11 compatibility
    def __str__(self) -> str:
        return self.value


class State(NamedTuple):
    type: StatefulObjectType
    updated: datetime
    name: str
    state: str
    reason: str


def flatten_log_states(types_to_states):
    states = []
    for type, one_type_states in types_to_states.items():
        for s in one_type_states:
            states.append(
                State(
                    type=StatefulObjectType(type),
                    updated=datetime.fromisoformat(s["updated"]),
                    name=s["stateful_object"]["name"] or "",
                    state=s["state"],
                    reason=s["reason"],
                )
            )

    states = sorted(states, key=lambda state: state.updated)
    return states


def log_states(states: List[State], level=None):
    """Log states, and return the latest one (for use in future queries)"""
    object_types_to_display = {
        StatefulObjectType.cluster: "Cluster",
        StatefulObjectType.scheduler: "Scheduler Process",
        StatefulObjectType.scheduler_instance: "Scheduler Instance",
        StatefulObjectType.cluster_infra: "Network Infrastructure",
        StatefulObjectType.worker: "Worker Process",
        StatefulObjectType.worker_instance: "Worker Instance",
    }
    max_type_length = max(len(v) for v in object_types_to_display.values())
    for s in states:
        updated_dt_str = datetime.strftime(s.updated.astimezone(), DISPLAY_DATETIME_FORMAT)
        log_string = (
            f"   | {object_types_to_display[s.type]:{max_type_length}} "
            f"| {s.name:46} | {s.state:10} at {updated_dt_str} | {s.reason}"
        )
        if s.state == "error":
            logger.log(msg=log_string, level=level or logging.ERROR)
        else:
            logger.log(msg=log_string, level=level or logging.DEBUG)


def get_process_instance_state(
    process: dict,
) -> Tuple[ProcessStateEnum, Optional[InstanceStateEnum]]:
    process_state = ProcessStateEnum(process["current_state"]["state"])
    instance = process["instance"]
    if instance is None:
        instance_state = None
    else:
        instance_state = InstanceStateEnum(instance["current_state"]["state"])
    return process_state, instance_state


class CombinedProcessStateEnum(BaseStateEnum):
    """This is a customer-facing type of status for a instance/process combo."""

    instance_queued = "queued"
    instance_starting = "starting"
    instance_running = "instance_running"  # instance is running; process not started or errored.
    downloading = "downloading"
    ready = "ready"
    pausing = "pausing"
    paused = "paused"
    stopping = "stopping"
    stopped = "stopped"
    error = "error"

    @classmethod
    def from_process_instance_states(cls, process_state, instance_state):
        if process_state == ProcessStateEnum.error or instance_state == InstanceStateEnum.error:
            return cls.error

        if instance_state is None:
            return cls.instance_queued  # a little bit of a lie
        elif instance_state == InstanceStateEnum.queued:
            return cls.instance_queued
        elif instance_state == InstanceStateEnum.starting:
            return cls.instance_starting
        elif instance_state == InstanceStateEnum.started:
            return cls.instance_running
        elif instance_state == InstanceStateEnum.ready:
            if process_state == ProcessStateEnum.started:
                return cls.ready
            elif process_state == ProcessStateEnum.starting:
                return cls.downloading
            elif process_state in [ProcessStateEnum.stopping, ProcessStateEnum.stopped]:
                return cls.stopping
            elif process_state in [ProcessStateEnum.pausing, ProcessStateEnum.paused]:
                return cls.pausing
            else:
                raise ValueError(f"unexpected instance/process state combo: {process_state}, {instance_state}")
        elif instance_state == InstanceStateEnum.pausing:
            return cls.pausing
        elif instance_state == InstanceStateEnum.paused:
            return cls.paused
        elif instance_state == InstanceStateEnum.stopping:
            return cls.stopping
        elif instance_state == InstanceStateEnum.stopped:
            return cls.stopped
        else:
            raise ValueError(f"unexpected instance state {instance_state}")


def get_combined_process_state(process) -> CombinedProcessStateEnum:
    """
    Collapses the process/instance state matrix to a single user-facing state summary.

    This necessarily elides some possible complexity and even lies a little.
    """
    process_state, instance_state = get_process_instance_state(process)

    return CombinedProcessStateEnum.from_process_instance_states(process_state, instance_state)


combined_state_to_description = {
    CombinedProcessStateEnum.instance_queued: "Queued",
    CombinedProcessStateEnum.instance_starting: "Starting",
    CombinedProcessStateEnum.instance_running: "Booted",
    CombinedProcessStateEnum.downloading: "Downloading Environment",
    CombinedProcessStateEnum.ready: "Ready",
    CombinedProcessStateEnum.pausing: "Pausing",
    CombinedProcessStateEnum.paused: "Paused",
    CombinedProcessStateEnum.stopping: "Stopping",
    CombinedProcessStateEnum.stopped: "Stopped",
    CombinedProcessStateEnum.error: "Error",
}


def summarize_status(details):
    max_description_length = max(len(desc) for desc in combined_state_to_description.values())

    cluster_state = details["current_state"]
    if cluster_state["state"] in [ClusterStateEnum.pending, ClusterStateEnum.starting]:
        return "Ensuring network infrastructure is ready..."
    else:
        scheduler = details["scheduler"]
        worker_state_counts = Counter(get_combined_process_state(worker) for worker in details["workers"])
        scheduler_status_to_show = f"Scheduler: {combined_state_to_description[get_combined_process_state(scheduler)]}"
        worker_status_descriptions = [
            f"{worker_state_counts[status]} {combined_state_to_description[status]}"
            for status in CombinedProcessStateEnum
            if worker_state_counts[status] > 0
        ]
        worker_statuses_to_show = (
            f"Workers: {', '.join(worker_status_descriptions)} (of {sum(worker_state_counts.values())})"
        )
        return f"{scheduler_status_to_show:{max_description_length + len('Scheduler: ') + 3}} {worker_statuses_to_show}"


def group_worker_errors(details: dict) -> Dict[str, int]:
    reasons = {}
    for worker in details.get("workers", []):
        state = worker.get("current_state", {}).get("state")
        reason = worker.get("current_state", {}).get("reason")
        if state == "error" and reason:
            if reason not in reasons:
                reasons[reason] = 1
            else:
                reasons[reason] += 1
    return reasons
