from .base_event import BaseEvent


class ScheduledEvent(BaseEvent):
    """
    Represents the execution event for a scheduled Lambda task.

    Inherits from BaseEvent and is used for tasks triggered by AWS scheduled events (e.g., cron, rate expressions).
    """
