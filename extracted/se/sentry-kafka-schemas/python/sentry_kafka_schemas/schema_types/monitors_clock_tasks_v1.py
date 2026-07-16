from typing import Union, Required, TypedDict, Literal


class MarkMissing(TypedDict, total=False):
    """
    mark_missing.

    Indicates a monitor ID that should be marked as missed.
    """

    type: Required["_MarkMissingType"]
    """
    Discriminant marker identifying the task.

    Required property
    """

    ts: Required[Union[int, float]]
    """
    The timestamp the clock ticked at.

    Required property
    """

    monitor_environment_id: Required[Union[int, float]]
    """
    The monitor environment ID to generate a missed check-in for.

    Required property
    """



class MarkTimeout(TypedDict, total=False):
    """
    mark_timeout.

    Indicates a check-in should be marked as having timed out.
    """

    type: Required["_MarkTimeoutType"]
    """
    Discriminant marker identifying the task.

    Required property
    """

    ts: Required[Union[int, float]]
    """
    The timestamp the clock ticked at.

    Required property
    """

    monitor_environment_id: Required[Union[int, float]]
    """
    The monitor environment ID the check-in is part of.

    Required property
    """

    checkin_id: Required[Union[int, float]]
    """
    The check-in ID to mark as timed out.

    Required property
    """



class MarkUnknown(TypedDict, total=False):
    """
    mark_unknown.

    Indicates this monitor was in-progress when an anomolys click-tick was processed, meaning we are unable to know if a check-in may have been lost for this monitor.
    """

    type: Required["_MarkUnknownType"]
    """
    Discriminant marker identifying the task.

    Required property
    """

    ts: Required[Union[int, float]]
    """
    The timestamp the clock ticked at.

    Required property
    """

    monitor_environment_id: Required[Union[int, float]]
    """
    The monitor environment ID to generate a missed check-in for.

    Required property
    """

    checkin_id: Required[Union[int, float]]
    """
    The check-in ID to mark as unknown.

    Required property
    """



MonitorsClockTasks = Union["MarkTimeout", "MarkUnknown", "MarkMissing"]
"""
monitors_clock_tasks.

Aggregation type: oneOf
"""



_MarkMissingType = Union[Literal['mark_missing']]
""" Discriminant marker identifying the task. """
_MARKMISSINGTYPE_MARK_MISSING: Literal['mark_missing'] = "mark_missing"
"""The values for the 'Discriminant marker identifying the task' enum"""



_MarkTimeoutType = Union[Literal['mark_timeout']]
""" Discriminant marker identifying the task. """
_MARKTIMEOUTTYPE_MARK_TIMEOUT: Literal['mark_timeout'] = "mark_timeout"
"""The values for the 'Discriminant marker identifying the task' enum"""



_MarkUnknownType = Union[Literal['mark_unknown']]
""" Discriminant marker identifying the task. """
_MARKUNKNOWNTYPE_MARK_UNKNOWN: Literal['mark_unknown'] = "mark_unknown"
"""The values for the 'Discriminant marker identifying the task' enum"""

