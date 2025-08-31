from dataclasses import dataclass, field
from typing import List, Optional, Union
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener

@dataclass(kw_only=True)
class Event:
    """
    Represents a scheduled event with configuration for execution, timing, and event handling.

    Parameters
    ----------
    signature : str
        Unique identifier or signature for the event.
    args : Optional[List[str]], default: []
        List of arguments to be passed to the event.
    purpose : Optional[str], default: None
        Short description of the event's purpose.
    random_delay : Optional[int], default: None
        Random delay in seconds before the event is triggered.
    start_date : Optional[datetime], default: None
        The date and time when the event becomes active.
    end_date : Optional[datetime], default: None
        The date and time when the event is no longer active.
    trigger : Optional[Union[CronTrigger, DateTrigger, IntervalTrigger]], default: None
        Trigger mechanism that determines when the event is executed.
    details : Optional[str], default: None
        Additional metadata or information about the event.
    listener : Optional[IScheduleEventListener], default: None
        Listener object implementing IScheduleEventListener for event-specific logic.
    max_instances : int, default: 1
        Maximum number of concurrent instances allowed for the event.
    misfire_grace_time : Optional[int], default: None
        Grace period in seconds for handling misfired events.

    Returns
    -------
    Event
        An instance of the Event class with the specified configuration.
    """

    # Unique identifier for the event
    signature: str

    # List of arguments for the event, defaults to empty list if not provided
    args: Optional[List[str]] = field(default_factory=list)

    # Description of the event's purpose
    purpose: Optional[str] = None

    # Optional random delay (in seconds) before the event is triggered
    random_delay: Optional[int] = None

    # Start date and time for the event
    start_date: Optional[datetime] = None

    # End date and time for the event
    end_date: Optional[datetime] = None

    # Trigger mechanism for the event (cron, date, or interval)
    trigger: Optional[Union[CronTrigger, DateTrigger, IntervalTrigger]] = None

    # Optional details about the event
    details: Optional[str] = None

    # Optional listener that implements IScheduleEventListener
    listener: Optional[IScheduleEventListener] = None

    # Maximum number of concurrent instances allowed for the event
    max_instances: int = 1

    # Grace time in seconds for misfired events
    misfire_grace_time: Optional[int] = None