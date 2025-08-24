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
    Represents an event with scheduling and execution details.

    Attributes
    ----------
    signature : str
        The unique identifier or signature of the event, used to distinguish it from other events.
    args : Optional[List[str]]
        A list of arguments associated with the event. Defaults to an empty list if not provided.
    purpose : Optional[str]
        A brief description of the event's purpose or intent. Can be None if not specified.
    random_delay : Optional[int]
        An optional random delay (in seconds) to be applied before the event is triggered. Can be None.
    start_date : Optional[datetime]
        The start date and time for the event. If None, the event starts immediately or based on the trigger.
    end_date : Optional[datetime]
        The end date and time for the event. If None, the event does not have a defined end time.
    trigger : Optional[Union[CronTrigger, DateTrigger, IntervalTrigger]]
        The trigger mechanism for the event, which determines when and how the event is executed.
        Can be a CronTrigger, DateTrigger, or IntervalTrigger. Defaults to None.
    details : Optional[str]
        Additional details or metadata about the event. Can be None if not specified.
    listener : Optional[IScheduleEventListener]
        An optional listener object that implements the IScheduleEventListener interface. 
        This listener can handle event-specific logic. Defaults to None.
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