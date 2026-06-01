from enum import StrEnum


class EventSpanType(StrEnum):
    workflow_init = "workflow_init"
    workflow_report = "workflow_report"
    activity = "activity"
    signal = "signal"
    update = "update"
    query = "query"
    event = "event"
    custom_task = "custom_task"


class EventType(StrEnum):
    EVENT = "EVENT"
    """Standard event
    """

    EVENT_PROGRESS = "EVENT_PROGRESS"
    """Event progress event created using Task system context manager
    """


class EventProgressStatus(StrEnum):
    RUNNING = "RUNNING"
    """Event progress is running
    """

    COMPLETED = "COMPLETED"
    """Event progress has completed
    """

    FAILED = "FAILED"
    """Event progress has failed
    """
