from dataclasses import dataclass
from datetime import datetime
from operator import attrgetter
from typing import Optional

from bigeye_sdk.generated.com.bigeye.models.generated import MetricInfo, MetricRun, SimpleBoundType
from bigeye_sdk.log import get_logger

log = get_logger(__name__)


@dataclass
class UpperLower:
    upper: Optional[float] = None
    lower: Optional[float] = None


def get_most_recent_run_point(metric_info: MetricInfo) -> MetricRun:
    """
        Returns the most recent MetricRun object from the Metric Info based on the grain start of a lookback window or
        the run at time.
        Args:
            metric_info: a MetricInfo object

        Returns: the most recent MetricRun.

    """
    try:
        return max(metric_info.latest_metric_runs, key=attrgetter('grain_start_epoch_seconds'))
    except AttributeError:
        return get_most_recent_run(metric_info=metric_info)


def get_most_recent_run_by_id(metric_info: MetricInfo) -> MetricRun:
    """
    Returns the most recent MetricRun object from the Metric Info based on the max MetricRun id.
        Args:
            metric_info: a MetricInfo object

        Returns: the most recent MetricRun.
    """
    try:
        return max(metric_info.latest_metric_runs, key=attrgetter('id'))
    except AttributeError:
        return get_most_recent_run(metric_info=metric_info)


def get_most_recent_run(metric_info: MetricInfo) -> MetricRun:
    """
    Returns the most recent MetricRun object from the Metric Info.
    Args:
        metric_info: a MetricInfo object

    Returns: the most recent MetricRun.

    """
    return max(metric_info.latest_metric_runs, key=attrgetter('run_at_epoch_seconds'))


def get_most_recent_run_time(most_recent_run: MetricRun) -> str:
    """
    Returns the time of a most recent run.
    Args:
        most_recent_run: a MetricRun object

    Returns: a datetime object created from the MetricRun.

    """
    return datetime.fromtimestamp(most_recent_run.run_at_epoch_seconds).strftime('%Y-%m-%d %H:%M:%S')


def get_upper_lower_thresholds(most_recent_run: MetricRun) -> UpperLower:
    """
    Gets the upper and lower thresholds from a MetricRun.
    Args:
        most_recent_run: a MetricRun object

    Returns: an UpperLower object containing the upper and lower thresholds for the run.

    """
    ul = UpperLower()

    # log.debug(most_recent_run.thresholds)

    for t in most_recent_run.thresholds:
        if t.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
            ul.upper = t.bound.value
        elif t.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
            ul.lower = t.bound.value

    return ul
