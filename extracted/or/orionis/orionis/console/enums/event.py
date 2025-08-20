from dataclasses import dataclass, field
from typing import List, Optional, Union
from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.support.entities.base import BaseEntity

@dataclass(kw_only=True)
class Event(BaseEntity):
    """
    Represents an event with scheduling and execution details.

    Attributes
    ----------
    signature : str
        The unique identifier or signature of the event.
    args : Optional[List[str]]
        A list of arguments associated with the event.
    purpose : Optional[str]
        A description of the event's purpose.
    random_delay : Optional[int]
        An optional random delay (in seconds) before the event is triggered.
    start_date : Optional[datetime]
        The start date and time for the event.
    end_date : Optional[datetime]
        The end date and time for the event.
    trigger : Optional[Union[CronTrigger, DateTrigger, IntervalTrigger]]
        The trigger mechanism for the event.
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