from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Callable, DefaultDict, List

from pydantic import BaseModel

from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import (
    check_activity_is_sticky_to_worker,
)
from mistralai.workflows.core.rate_limiting.rate_limit import get_rate_limit

# A gRPC connection to Temporal allows a bounded number of concurrent streams (100 at Cloudflare's edge,
# configurable through `connection_stream_limit`). Every poller holds one stream open for the whole life
# of the worker, so the process worst case is the sum of all workers' pollers. Past the limit Temporal
# raises no ResourceExhausted: the extra pollers silently queue inside the worker, workflow-task results
# miss their 10s timeout, and results come back as NotFound.
#
# The estimate is a lower bound: it counts the permanent poll streams only. Respond and heartbeat calls
# from running activities (up to `max_concurrent_activities` per worker) and client calls through
# set_worker_service_client open short-lived streams on the same connection and are not included, which
# is why the warning fires at a fraction of the limit and why the headroom is the number to watch.
POLL_WARNING_THRESHOLD_RATIO = 0.8


class WorkerConfig(BaseModel):
    task_queue: str
    max_task_queue_activities_per_second: float | None = None

    def __hash__(self) -> int:
        return hash((self.task_queue, self.max_task_queue_activities_per_second))


@dataclass(frozen=True)
class WorkerActivityGroup:
    worker_config: WorkerConfig
    activities: List[Callable]
    is_main: bool
    is_sticky: bool
    rate_limit_key: str | None


@dataclass(frozen=True)
class PollEstimate:
    total_polls: int
    worker_count: int
    activity_polls_per_worker: int
    main_workflow_polls: int
    sticky_worker_count: int
    rate_limited_worker_count: int
    rate_limit_keys: List[str]
    multi_rate_keys: List[str]
    connection_stream_limit: int | None

    @property
    def warning_threshold(self) -> int | None:
        if self.connection_stream_limit is None:
            return None
        return int(self.connection_stream_limit * POLL_WARNING_THRESHOLD_RATIO)

    @property
    def headroom(self) -> int | None:
        """Streams left on the connection once the polls are open, for respond/heartbeat bursts."""
        if self.connection_stream_limit is None:
            return None
        return self.connection_stream_limit - self.total_polls


def group_activities_by_worker_config(
    activities: list[Callable], main_task_queue: str, sticky_task_queue: str
) -> list[WorkerActivityGroup]:
    """Split activities across internal workers exactly as _create_temporal_workers does:
    a dedicated worker for sticky activities, one worker per rate-limit config, and a main
    worker registering every activity (so they can also run through `run_activities_locally`)."""
    grouped: DefaultDict[WorkerConfig, list[Callable]] = defaultdict(list)
    group_meta: dict[WorkerConfig, tuple[bool, str | None]] = {}

    for act in activities:
        if check_activity_is_sticky_to_worker(act):
            worker_config = WorkerConfig(task_queue=sticky_task_queue)
            group_meta.setdefault(worker_config, (True, None))
        elif rate_limit := get_rate_limit(act):
            worker_config = WorkerConfig(
                task_queue=f"{main_task_queue}-{rate_limit.task_queue_suffix}",
                max_task_queue_activities_per_second=rate_limit.max_execution / rate_limit.time_window_in_sec,
            )
            group_meta.setdefault(worker_config, (False, rate_limit.key or act.__name__))
        else:
            continue
        grouped[worker_config].append(act)

    grouped[WorkerConfig(task_queue=main_task_queue)] = list(activities)

    return [
        WorkerActivityGroup(
            worker_config=worker_config,
            activities=grouped_activities,
            is_main=worker_config.task_queue == main_task_queue,
            is_sticky=group_meta.get(worker_config, (False, None))[0],
            rate_limit_key=group_meta.get(worker_config, (False, None))[1],
        )
        for worker_config, grouped_activities in grouped.items()
    ]


def _rate_limited_groups(groups: List[WorkerActivityGroup]) -> List[WorkerActivityGroup]:
    return [group for group in groups if not group.is_main and not group.is_sticky]


def distinct_rate_limit_keys(groups: List[WorkerActivityGroup]) -> List[str]:
    return sorted({group.rate_limit_key for group in _rate_limited_groups(groups) if group.rate_limit_key})


def estimate_connection_polls(
    groups: List[WorkerActivityGroup],
    activity_polls_per_worker: int,
    workflow_polls: int,
    connection_stream_limit: int | None,
) -> PollEstimate:
    """Minimum number of poll streams these workers open on their shared gRPC connection."""
    # Every worker runs activity polls up to the same configured maximum. Only the main worker hosts
    # workflows; Temporal splits those polls between the normal and sticky task queues up to the same
    # maximum, not double.
    rate_limited_groups = _rate_limited_groups(groups)
    workers_per_key = Counter(group.rate_limit_key for group in rate_limited_groups)

    return PollEstimate(
        total_polls=len(groups) * activity_polls_per_worker + workflow_polls,
        worker_count=len(groups),
        activity_polls_per_worker=activity_polls_per_worker,
        main_workflow_polls=workflow_polls,
        sticky_worker_count=sum(1 for group in groups if group.is_sticky),
        rate_limited_worker_count=len(rate_limited_groups),
        rate_limit_keys=distinct_rate_limit_keys(groups),
        multi_rate_keys=sorted(key for key, count in workers_per_key.items() if key and count > 1),
        connection_stream_limit=connection_stream_limit,
    )


def format_poll_warning(estimate: PollEstimate) -> str | None:
    threshold = estimate.warning_threshold
    if threshold is None or estimate.total_polls < threshold:
        return None
    message = (
        f"Workers may open at least {estimate.total_polls} concurrent poll streams on a single Temporal gRPC "
        f"connection, leaving {estimate.headroom} of the {estimate.connection_stream_limit} concurrent streams "
        f"allowed per connection (warning threshold: {threshold}). This counts poll streams only: respond and "
        f"heartbeat calls from running activities open further short-lived streams on the same connection and "
        f"are not included, so a burst of completions can exhaust the headroom. Past the per-connection limit, "
        f"new requests silently queue inside the worker until workflow-task results miss their 10s timeout and "
        f"come back as NotFound. Poll streams: {estimate.worker_count} workers (1 main + "
        f"{estimate.sticky_worker_count} sticky + {estimate.rate_limited_worker_count} rate-limited) x "
        f"{estimate.activity_polls_per_worker} activity polls each, plus {estimate.main_workflow_polls} workflow "
        f"polls on the main worker, for rate-limit keys [{', '.join(estimate.rate_limit_keys)}]. Reduce the poll "
        f"streams by sharing one rate-limit key across activities that hit the same external resource, or by "
        f"lowering MAX_ACTIVITY_TASK_POLLERS (currently {estimate.activity_polls_per_worker})."
    )
    if estimate.multi_rate_keys:
        message += (
            f" Rate-limit keys [{', '.join(estimate.multi_rate_keys)}] are used with different rates, which runs "
            f"one worker per rate: give every activity on such a key the same rate to share a single worker."
        )
    return message
