import random
from datetime import datetime
from typing import List, Optional, Union
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.console.contracts.event import IEvent
from orionis.console.enums.event import Event as EventEntity
from orionis.console.exceptions import CLIOrionisValueError

class Event(IEvent):

    def __init__(
        self,
        signature: str,
        args: Optional[List[str]],
        purpose: Optional[str] = None,
    ):
        """
        Initialize a new Event instance.

        Parameters
        ----------
        signature : str
            The unique identifier or signature for the event. This is typically
            used to distinguish between different events in the system.
        args : Optional[List[str]]
            A list of arguments required by the event. If not provided, an empty
            list will be used.
        purpose : Optional[str], optional
            A human-readable description or purpose for the event, by default None.

        Returns
        -------
        None
            This constructor does not return any value. It initializes the internal
            state of the Event object.
        """

        # Store the event's signature
        self.__signature: str = signature

        # Store the event's arguments, defaulting to an empty list if None is provided
        self.__args: Optional[List[str]] = args if args is not None else []

        # Store the event's purpose or description
        self.__purpose: Optional[str] = purpose

        # Initialize the random delay attribute (in seconds) as None
        self.__random_delay: Optional[int] = None

        # Initialize the start date for the event as None
        self.__start_date: Optional[datetime] = None

        # Initialize the end date for the event as None
        self.__end_date: Optional[datetime] = None

        # Initialize the trigger for the event as None; can be set to a Cron, Date, or Interval trigger
        self.__trigger: Optional[Union[CronTrigger, DateTrigger, IntervalTrigger]] = None

        # Initialize the details for the event as None; can be used to store additional information
        self.__details: Optional[str] = None

    def toEntity(
        self
    ) -> EventEntity:
        """
        Retrieve the event details as an EventEntity instance.

        This method gathers all relevant attributes of the current Event object,
        such as its signature, arguments, purpose, random delay, start and end dates,
        and trigger, and returns them encapsulated in an EventEntity object.

        Returns
        -------
        EventEntity
            An EventEntity instance containing the event's signature, arguments,
            purpose, random delay, start date, end date, and trigger.
        """

        # Validate that the signature is set and is a non-empty string
        if not self.__signature:
            raise CLIOrionisValueError("Signature is required for the event.")
        if not isinstance(self.__args, list):
            raise CLIOrionisValueError("Args must be a list.")
        if self.__purpose is not None and not isinstance(self.__purpose, str):
            raise CLIOrionisValueError("Purpose must be a string or None.")

        # Validate that start_date and end_date are datetime instances if they are set
        if self.__start_date is not None and not isinstance(self.__start_date, datetime):
            raise CLIOrionisValueError("Start date must be a datetime instance.")
        if self.__end_date is not None and not isinstance(self.__end_date, datetime):
            raise CLIOrionisValueError("End date must be a datetime instance.")

        # Validate that trigger is one of the expected types if it is set
        if self.__trigger is not None and not isinstance(self.__trigger, (CronTrigger, DateTrigger, IntervalTrigger)):
            raise CLIOrionisValueError("Trigger must be a CronTrigger, DateTrigger, or IntervalTrigger.")

        # Validate that random_delay is an integer if it is set
        if self.__random_delay is not None and not isinstance(self.__random_delay, int):
            raise CLIOrionisValueError("Random delay must be an integer or None.")

        # Validate that details is a string if it is set
        if self.__details is not None and not isinstance(self.__details, str):
            raise CLIOrionisValueError("Details must be a string or None.")

        # Construct and return an EventEntity with the current event's attributes
        return EventEntity(
            signature=self.__signature,
            args=self.__args,
            purpose=self.__purpose,
            random_delay=self.__random_delay,
            start_date=self.__start_date,
            end_date=self.__end_date,
            trigger=self.__trigger,
            details=self.__details
        )

    def purpose(
        self,
        purpose: str
    ) -> 'Event':
        """
        Set the purpose or description for the scheduled command.

        This method assigns a human-readable purpose or description to the command
        that is being scheduled. The purpose must be a non-empty string. This can
        be useful for documentation, logging, or displaying information about the
        scheduled job.

        Parameters
        ----------
        purpose : str
            The purpose or description to associate with the scheduled command.
            Must be a non-empty string.

        Returns
        -------
        Scheduler
            Returns the current instance of the Scheduler to allow method chaining.

        Raises
        ------
        CLIOrionisValueError
            If the provided purpose is not a non-empty string.
        """

        # Validate that the purpose is a non-empty string
        if not isinstance(purpose, str) or not purpose.strip():
            raise CLIOrionisValueError("The purpose must be a non-empty string.")

        # Set the internal purpose attribute
        self.__purpose = purpose

        # Return self to support method chaining
        return self

    def startDate(
        self,
        start_date: datetime
    ) -> 'Event':
        """
        Set the start date for the event execution.

        This method allows you to specify a start date for when the event should
        begin execution. The start date must be a datetime instance.

        Parameters
        ----------
        start_date : datetime
            The start date for the event execution.

        Returns
        -------
        Event
            Returns the current instance of the Event to allow method chaining.
        """

        # Validate that start_date is a datetime instance
        if not isinstance(start_date, datetime):
            raise CLIOrionisValueError("Start date must be a datetime instance.")

        # Set the internal start date attribute
        self.__start_date = start_date

        # Return self to support method chaining
        return self

    def endDate(
        self,
        end_date: datetime
    ) -> 'Event':
        """
        Set the end date for the event execution.

        This method allows you to specify an end date for when the event should
        stop executing. The end date must be a datetime instance.

        Parameters
        ----------
        end_date : datetime
            The end date for the event execution.

        Returns
        -------
        Event
            Returns the current instance of the Event to allow method chaining.
        """

        # Validate that end_date is a datetime instance
        if not isinstance(end_date, datetime):
            raise CLIOrionisValueError("End date must be a datetime instance.")

        # Set the internal end date attribute
        self.__end_date = end_date

        # Return self to support method chaining
        return self

    def randomDelay(
        self,
        max_seconds: int = 10
    ) -> 'Event':
        """
        Set a random delay for the event execution.

        This method allows you to specify a random delay up to a maximum
        number of seconds before the event is executed. This can be useful for
        distributing load or avoiding collisions in scheduled tasks.

        Parameters
        ----------
        max_seconds : int
            The maximum number of seconds to wait before executing the event.

        Returns
        -------
        Event
            Returns the current instance of the Event to allow method chaining.
        """

        # Validate that max_seconds is a positive integer
        if not isinstance(max_seconds, int) or max_seconds <= 0:
            raise CLIOrionisValueError("max_seconds must be a positive integer.")

        # Generate a random delay between 1 and max_seconds (inclusive)
        self.__random_delay = random.randint(1, max_seconds)

        # Return self to support method chaining
        return self

    def onceAt(
        self,
        date: datetime
    ) -> bool:
        """
        Schedule the event to run once at a specific date and time.

        This method allows you to schedule the event to execute once at a specified
        date and time. The date must be a datetime instance.

        Parameters
        ----------
        date : datetime
            The specific date and time when the event should run.

        Returns
        -------
        bool
            Returns True if the scheduling was successful.
        """

        # Validate that date is a datetime instance
        if not isinstance(date, datetime):
            raise CLIOrionisValueError("The date must be a datetime instance.")

        # Set the start and end dates to the specified date
        self.__start_date = date
        self.__end_date = date

        # Set the trigger to a DateTrigger for the specified date
        self.__trigger = DateTrigger(run_date=date)

        # Optionally, set the details for the event
        self.__details = f"Once At: {date.strftime('%Y-%m-%d %H:%M:%S')}"

        # Return self to support method chaining
        return True

    def everySeconds(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in seconds.

        This method configures the event to execute repeatedly at a specified interval
        (in seconds). Optionally, the event can be restricted to a time window using
        previously set start and end dates. A random delay (jitter) can also be applied
        if configured.

        Parameters
        ----------
        seconds : int
            The interval, in seconds, at which the event should be executed. Must be a positive integer.

        Returns
        -------
        bool
            Returns True if the interval scheduling was successfully configured.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not a positive integer.
        """

        # Validate that the seconds parameter is a positive integer.
        if not isinstance(seconds, int) or seconds <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval,
        # using any previously set start_date, end_date, and random_delay (jitter).
        self.__trigger = IntervalTrigger(
            seconds=seconds,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay
        )

        # Indicate that the scheduling was successful.
        return True