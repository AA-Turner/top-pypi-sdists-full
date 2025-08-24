import random
from datetime import datetime
from typing import List, Optional, Union
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.console.contracts.event import IEvent
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
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

        This constructor sets up the initial state of an Event object, including its
        unique signature, arguments, purpose, and other optional attributes such as
        random delay, start and end dates, trigger, details, listener, and maximum
        instances. These attributes define the behavior and metadata of the event.

        Parameters
        ----------
        signature : str
            A unique identifier for the event. This is required and must be a non-empty string.
        args : list of str, optional
            A list of arguments associated with the event. Defaults to an empty list if None is provided.
        purpose : str, optional
            A human-readable description or purpose of the event. Defaults to None.

        Returns
        -------
        None
            This method does not return any value. It initializes the Event instance.

        Notes
        -----
        The `__trigger` attribute is initially set to None and can later be configured
        to a Cron, Date, or Interval trigger. Similarly, the `__listener` attribute is
        set to None and can be assigned an instance of `IScheduleEventListener` to handle
        event-specific logic.
        """

        # Store the event's unique signature
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

        # Initialize the listener attribute as None; can be set to an IScheduleEventListener instance
        self.__listener: Optional[IScheduleEventListener] = None

        # Initialize the maximum instances attribute as None
        self.__max_instances: Optional[int] = None

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

        # Validate arguments
        if not isinstance(self.__args, list):
            raise CLIOrionisValueError("Args must be a list.")

        # Validate that purpose is a string if it is set
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

        # Validate that listener is an IScheduleEventListener instance if it is set
        if self.__listener is not None and not issubclass(self.__listener, IScheduleEventListener):
            raise CLIOrionisValueError("Listener must implement IScheduleEventListener interface or be None.")

        # Construct and return an EventEntity with the current event's attributes
        return EventEntity(
            signature=self.__signature,
            args=self.__args,
            purpose=self.__purpose,
            random_delay=self.__random_delay,
            start_date=self.__start_date,
            end_date=self.__end_date,
            trigger=self.__trigger,
            details=self.__details,
            listener=self.__listener
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
        if not isinstance(max_seconds, int) or max_seconds <= 0 or max_seconds > 120:
            raise CLIOrionisValueError("Max seconds must be a positive integer between 1 and 120.")

        # Generate a random delay between 1 and max_seconds (inclusive)
        self.__random_delay = random.randint(1, max_seconds)

        # Return self to support method chaining
        return self

    def maxInstances(
        self,
        max_instances: int
    ) -> 'Event':
        """
        Set the maximum number of concurrent instances for the event.

        This method specifies the maximum number of instances of the event
        that can run concurrently. It is useful for preventing resource
        contention or overloading the system with too many simultaneous
        executions of the same event.

        Parameters
        ----------
        max_instances : int
            The maximum number of concurrent instances allowed for the event.
            Must be a positive integer.

        Returns
        -------
        Event
            The current instance of the Event, allowing method chaining.

        Raises
        ------
        CLIOrionisValueError
            If `max_instances` is not a positive integer.

        Notes
        -----
        This setting is particularly useful in scenarios where the event
        involves resource-intensive operations, ensuring that the system
        remains stable and responsive.
        """

        # Validate that max_instances is a positive integer
        if not isinstance(max_instances, int) or max_instances <= 0:
            raise CLIOrionisValueError("Max instances must be a positive integer.")

        # Set the internal max instances attribute
        self.__max_instances = max_instances

        # Return self to support method chaining
        return self

    def subscribeListener(
        self,
        listener: IScheduleEventListener
    ) -> 'Event':
        """
        Subscribe a listener to the event.

        This method allows you to attach a listener that implements the `IScheduleEventListener`
        interface to the event. The listener will be notified when the event is triggered.

        Parameters
        ----------
        listener : IScheduleEventListener
            An instance of a class that implements the `IScheduleEventListener` interface.

        Returns
        -------
        Event
            The current instance of the `Event` class, allowing method chaining.

        Raises
        ------
        CLIOrionisValueError
            If the provided `listener` does not implement the `IScheduleEventListener` interface.

        Notes
        -----
        The listener is stored internally and will be used to handle event-specific logic
        when the event is executed.
        """

        # Validate that the provided listener is an instance of IScheduleEventListener
        if not issubclass(listener, IScheduleEventListener):
            raise CLIOrionisValueError("Listener must be an instance of IScheduleEventListener.")

        # Assign the listener to the event's internal listener attribute
        self.__listener = listener

        # Return the current instance to support method chaining
        return self

    def onceAt(
        self,
        date: datetime
    ) -> bool:
        """
        Schedule the event to execute once at a specific date and time.

        This method configures the event to run a single time at the provided
        `date` and time. The `date` parameter must be a valid `datetime` instance.
        Internally, this sets both the start and end dates to the specified value,
        and uses a `DateTrigger` to ensure the event is triggered only once.

        Parameters
        ----------
        date : datetime
            The exact date and time at which the event should be executed. Must be a
            valid `datetime` object.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured for a single execution.

        Raises
        ------
        CLIOrionisValueError
            If `date` is not a valid `datetime` instance.
        """

        # Validate that the provided date is a datetime instance
        if not isinstance(date, datetime):
            raise CLIOrionisValueError("The date must be a datetime instance.")

        # Set both start and end dates to the specified date for a one-time execution
        self.__start_date = date
        self.__end_date = date

        # Use a DateTrigger to schedule the event to run once at the specified date and time
        self.__trigger = DateTrigger(run_date=date)

        # Optionally, store a human-readable description of the scheduled execution
        self.__details = f"Once At: {date.strftime('%Y-%m-%d %H:%M:%S')}"

        # Indicate that the scheduling was successful
        return True

    def everySecond(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in seconds.

        This method configures the event to execute repeatedly at a specified interval
        (in seconds). The event can optionally be restricted to a time window using
        previously set `start_date` and `end_date`. If a random delay (jitter) has been
        configured, it can be applied to the trigger.

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

        Notes
        -----
        The event will be triggered every `seconds` seconds, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set).
        """
        # Validate that the seconds parameter is a positive integer.
        if not isinstance(seconds, int) or seconds <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval,
        # using any previously set start_date and end_date.
        self.__trigger = IntervalTrigger(
            seconds=seconds,
            start_date=self.__start_date,
            end_date=self.__end_date
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every {seconds} seconds"

        # Indicate that the scheduling was successful.
        return True

    def everyFiveSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every five seconds.

        This method configures the event to execute at a fixed interval of five seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            five seconds.

        Notes
        -----
        The event will be triggered at 0, 5, 10, 15, ..., 55 seconds of each minute, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 5 seconds.
        return self.everySecond(5)

    def everyTenSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every ten seconds.

        This method configures the event to execute at a fixed interval of ten seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            ten seconds.

        Notes
        -----
        The event will be triggered at 0, 10, 20, 30, 40, and 50 seconds of each minute, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 10 seconds.
        return self.everySecond(10)

    def everyFifteenSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every fifteen seconds.

        This method configures the event to execute at a fixed interval of fifteen seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifteen seconds.

        Notes
        -----
        The event will be triggered at 0, 15, 30, and 45 seconds of each minute, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 15 seconds.
        return self.everySecond(15)

    def everyTwentySeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every twenty seconds.

        This method configures the event to execute at a fixed interval of twenty seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            twenty seconds. The event will be triggered at 0, 20, and 40 seconds of each minute,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 20 seconds.
        return self.everySecond(20)

    def everyTwentyFiveSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every twenty-five seconds.

        This method configures the event to execute at a fixed interval of twenty-five seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            twenty-five seconds. The event will be triggered at 0, 25, and 50 seconds of each minute,
            within the optional scheduling window defined by `start_date` and `end_date`. If a random
            delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0, 25, and 50 seconds of each minute.
        """

        # Delegate scheduling to the everySecond method with an interval of 25 seconds.
        return self.everySecond(25)

    def everyThirtySeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every thirty seconds.

        This method configures the event to execute at a fixed interval of thirty seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            thirty seconds.

        Notes
        -----
        The event will be triggered at 0 and 30 seconds of each minute, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 30 seconds.
        return self.everySecond(30)

    def everyThirtyFiveSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every thirty-five seconds.

        This method configures the event to execute at a fixed interval of thirty-five seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            thirty-five seconds. The event will be triggered at 0 and 35 seconds of each minute,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 35 seconds.
        return self.everySecond(35)

    def everyFortySeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every forty seconds.

        This method configures the event to execute at a fixed interval of forty seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            forty seconds. The event will be triggered at 0 and 40 seconds of each minute, within the
            optional scheduling window defined by `start_date` and `end_date`. If a random delay
            (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 40 seconds of each minute.
        """

        # Delegate scheduling to the everySecond method with an interval of 40 seconds.
        return self.everySecond(40)

    def everyFortyFiveSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every forty-five seconds.

        This method configures the event to execute at a fixed interval of forty-five seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            forty-five seconds. The event will be triggered at 0 and 45 seconds of each minute,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 45 seconds of each minute.
        """

        # Delegate scheduling to the everySecond method with an interval of 45 seconds.
        return self.everySecond(45)

    def everyFiftySeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every fifty seconds.

        This method configures the event to execute at a fixed interval of fifty seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifty seconds. The event will be triggered at 0 and 50 seconds of each minute, within the
            optional scheduling window defined by `start_date` and `end_date`. If a random delay
            (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 50 seconds of each minute.
        """

        # Delegate scheduling to the everySecond method with an interval of 50 seconds.
        return self.everySecond(50)

    def everyFiftyFiveSeconds(
        self
    ) -> bool:
        """
        Schedule the event to run every fifty-five seconds.

        This method configures the event to execute at a fixed interval of fifty-five seconds using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifty-five seconds. The event will be triggered at 0 and 55 seconds of each minute,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everySecond method with an interval of 55 seconds.
        return self.everySecond(55)

    def everyMinute(
        self,
        minutes: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in minutes.

        This method configures the event to execute repeatedly at a specified interval
        (in minutes). The interval must be a positive integer. Optionally, the event can be
        restricted to a time window using previously set `start_date` and `end_date`. If a
        random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        minutes : int
            The interval, in minutes, at which the event should be executed. Must be a positive integer.

        Returns
        -------
        bool
            Returns True if the interval scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minutes` is not a positive integer.

        Notes
        -----
        The event will be triggered every `minutes` minutes, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set). If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the minutes parameter is a positive integer.
        if not isinstance(minutes, int) or minutes <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval,
        # using any previously set start_date, end_date, and random_delay (jitter).
        self.__trigger = IntervalTrigger(
            minutes=minutes,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every {minutes} minutes"

        # Indicate that the scheduling was successful.
        return True

    def everyMinuteAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every minute at a specific second, without applying jitter.

        This method configures the event to execute at the specified second (0-59) of every minute.
        Any previously configured random delay (jitter) will be ignored for this schedule.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each minute at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every minute, with no jitter applied.
        """

        # Validate that the 'seconds' parameter is an integer between 0 and 59.
        if not isinstance(seconds, int) or not (0 <= seconds <= 59):
            raise CLIOrionisValueError("Seconds must be an integer between 0 and 59.")

        # Configure the trigger to execute the event every minute at the specified second,
        # explicitly disabling jitter regardless of previous configuration.
        self.__trigger = CronTrigger(
            minute="*",
            second=seconds,
            start_date=self.__start_date,
            end_date=self.__end_date
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every minute at {seconds} seconds"

        # Indicate that the scheduling was successful.
        return True

    def everyMinutesAt(
        self,
        minutes: int,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run at a specific second of every given interval in minutes.

        This method configures the event to execute at the specified second (0-59) of every
        `minutes` interval. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Parameters
        ----------
        minutes : int
            The interval, in minutes, at which the event should be executed. Must be a positive integer.
        seconds : int
            The specific second (0-59) of each interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minutes` is not a positive integer or `seconds` is not an integer between 0 and 59.

        Notes
        -----
        The event will be triggered at the specified second of every `minutes` interval, within the optional
        scheduling window defined by `start_date` and `end_date`.
        """

        # Validate that 'minutes' is a positive integer.
        if not isinstance(minutes, int) or minutes <= 0:
            raise CLIOrionisValueError("Minutes must be a positive integer.")

        # Validate that 'seconds' is an integer between 0 and 59.
        if not isinstance(seconds, int) or not (0 <= seconds <= 59):
            raise CLIOrionisValueError("Seconds must be an integer between 0 and 59.")

        # Configure the trigger to execute the event every 'minutes' minutes at the specified 'seconds'
        self.__trigger = CronTrigger(
            minute=f"*/{minutes}",
            second=seconds,
            start_date=self.__start_date,
            end_date=self.__end_date
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every {minutes} minutes at {seconds} seconds"

        # Indicate that the scheduling was successful.
        return True

    def everyFiveMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every five minutes.

        This method configures the event to execute at a fixed interval of five minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            five minutes. The method always returns True after setting up the interval trigger.

        Notes
        -----
        The event will be triggered at 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, and 55 minutes
        of each hour, within the optional scheduling window defined by `start_date` and `end_date`.
        If a random delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinute method with an interval of 5 minutes.
        return self.everyMinute(5)

    def everyFiveMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every five minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every five-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each five-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every five-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 5 minutes and the specified second.
        return self.everyMinutesAt(5, seconds)

    def everyTenMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every ten minutes.

        This method configures the event to execute at a fixed interval of ten minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            ten minutes. The event will be triggered at 0, 10, 20, 30, 40, and 50 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a random
            delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at every ten-minute interval within each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 10 minutes.
        return self.everyMinute(10)

    def everyTenMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every ten minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every ten-minute interval.
        Any previously configured random delay (jitter) will be ignored for this schedule. The scheduling window
        can be further restricted by previously set `start_date` and `end_date` attributes.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each ten-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every ten-minute interval, with no jitter applied.
        The schedule respects any configured `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 10 minutes and the specified second.
        return self.everyMinutesAt(10, seconds)

    def everyFifteenMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every fifteen minutes.

        This method configures the event to execute at a fixed interval of fifteen minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifteen minutes. The event will be triggered at 0, 15, 30, and 45 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a random
            delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at every fifteen-minute interval within each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 15 minutes.
        return self.everyMinute(15)

    def everyFifteenMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every fifteen minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every fifteen-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each fifteen-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every fifteen-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 15 minutes and the specified second.
        return self.everyMinutesAt(15, seconds)

    def everyTwentyMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every twenty minutes.

        This method configures the event to execute at a fixed interval of twenty minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            twenty minutes. The event will be triggered at 0, 20, and 40 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0, 20, and 40 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 20 minutes.
        return self.everyMinute(20)

    def everyTwentyMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every twenty minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every twenty-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each twenty-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every twenty-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 20 minutes and the specified second.
        return self.everyMinutesAt(20, seconds)

    def everyTwentyFiveMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every twenty-five minutes.

        This method configures the event to execute at a fixed interval of twenty-five minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            twenty-five minutes. The event will be triggered at 0, 25, and 50 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a random
            delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinute method with an interval of 25 minutes.
        return self.everyMinute(25)

    def everyTwentyFiveMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every twenty-five minutes at a specific second.

        This method sets up the event to execute at the specified second (0-59) of every twenty-five-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each twenty-five-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every twenty-five-minute interval,
        within the optional scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 25 minutes and the specified second.
        return self.everyMinutesAt(25, seconds)

    def everyThirtyMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every thirty minutes.

        This method configures the event to execute at a fixed interval of thirty minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            thirty minutes. The event will be triggered at 0 and 30 minutes of each hour, within the
            optional scheduling window defined by `start_date` and `end_date`. If a random delay
            (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 30 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 30 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(30)

    def everyThirtyMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every thirty minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every thirty-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each thirty-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every thirty-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 30 minutes and the specified second.
        return self.everyMinutesAt(30, seconds)

    def everyThirtyFiveMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every thirty-five minutes.

        This method configures the event to execute at a fixed interval of thirty-five minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            thirty-five minutes. The event will be triggered at 0 and 35 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 35 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 35 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(35)

    def everyThirtyFiveMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every 35 minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every 35-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each 35-minute interval at which the event should be executed.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input is invalid, a `CLIOrionisValueError`
            is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every 35-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 35 minutes
        # and the specified second.
        return self.everyMinutesAt(35, seconds)

    def everyFortyMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every forty minutes.

        This method configures the event to execute at a fixed interval of forty minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            forty minutes. The event will be triggered at 0, 40 minutes of each hour, within the
            optional scheduling window defined by `start_date` and `end_date`. If a random delay
            (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 40 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 40 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(40)

    def everyFortyMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every forty minutes at a specific second.

        This method configures the event to execute at the specified second (0-59) of every forty-minute interval.
        The scheduling window can be further restricted by previously set `start_date` and `end_date` attributes.
        If a random delay (jitter) has been configured, it will be applied to the trigger to help distribute load
        or avoid collisions.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each forty-minute interval at which the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every forty-minute interval, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter) is set,
        it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 40 minutes
        # and the specified second.
        return self.everyMinutesAt(40, seconds)

    def everyFortyFiveMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every forty-five minutes.

        This method configures the event to execute at a fixed interval of forty-five minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The event will be triggered at
            0 and 45 minutes of each hour, within the optional scheduling window defined by
            `start_date` and `end_date`. If a random delay (jitter) is set, it will be applied
            to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 45 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 45 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(45)

    def everyFortyFiveMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every forty-five minutes at a specific second.

        This method configures the event to execute at the specified second (0-59)
        of every forty-five-minute interval. The scheduling window can be further
        restricted by previously set `start_date` and `end_date` attributes. If a
        random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each forty-five-minute interval at which
            the event should be executed.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every forty-five-minute
        interval, within the optional scheduling window defined by `start_date` and
        `end_date`. If a random delay (jitter) is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyMinutesAt method with an interval of 45 minutes
        # and the specified second. This ensures consistent handling of start_date, end_date,
        # and random_delay (jitter).
        return self.everyMinutesAt(45, seconds)

    def everyFiftyMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every fifty minutes.

        This method configures the event to execute at a fixed interval of fifty minutes using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifty minutes. The event will be triggered at 0, 50 minutes of each hour, within the
            optional scheduling window defined by `start_date` and `end_date`. If a random delay
            (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 50 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 50 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(50)

    def everyFiftyMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Schedule the event to run every fifty minutes at a specific second.

        This method configures the event to execute at the specified second (0-59)
        of every fifty-minute interval. The scheduling window can be further restricted
        by previously set `start_date` and `end_date` attributes. If a random delay
        (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        seconds : int
            The specific second (0-59) of each fifty-minute interval at which the
            event should be executed.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `seconds` is not an integer between 0 and 59 (inclusive).

        Notes
        -----
        The event will be triggered at the specified second of every fifty-minute
        interval, within the optional scheduling window defined by `start_date`
        and `end_date`. If a random delay (jitter) is set, it will be applied to
        the trigger.
        """
        # Delegate scheduling to the everyMinutesAt method with an interval of 50 minutes
        # and the specified second. This ensures consistent handling of start_date, end_date,
        # and random_delay (jitter).
        return self.everyMinutesAt(50, seconds)

    def everyFiftyFiveMinutes(
        self
    ) -> bool:
        """
        Schedule the event to run every fifty-five minutes.

        This method configures the event to execute at a fixed interval of fifty-five minutes
        using an `IntervalTrigger`. The scheduling window can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for execution every
            fifty-five minutes. The event will be triggered at 0 and 55 minutes of each hour,
            within the optional scheduling window defined by `start_date` and `end_date`. If a
            random delay (jitter) is set, it will be applied to the trigger.

        Notes
        -----
        The event will be triggered at 0 and 55 minutes of each hour.
        """

        # Delegate scheduling to the everyMinute method with an interval of 55 minutes.
        # This ensures consistent handling of start_date, end_date, and random_delay (jitter).
        return self.everyMinute(55)

    def everyFiftyFiveMinutesAt(
        self,
        seconds: int
    ) -> bool:
        """
        Determines if the current time matches a schedule that triggers
        every 55 minutes at a specific second.

        Parameters
        ----------
        seconds : int
            The specific second of the 55th minute at which the event should trigger.

        Returns
        -------
        bool
            True if the current time matches the schedule (55 minutes past the hour
            at the specified second), False otherwise.

        Notes
        -----
        This method is a wrapper around `everyMinutesAt` with the minute parameter
        fixed at 55.
        """
        return self.everyMinutesAt(55, seconds)

    def hourly(
        self
    ) -> bool:
        """
        Schedule the event to run every hour.

        This method configures the event to execute once every hour, starting from the
        optionally set `start_date` and ending at the optionally set `end_date`. If a random
        delay (jitter) has been configured, it will be applied to the trigger to help distribute
        load or avoid collisions. The method ensures that the event is triggered at regular
        hourly intervals.

        Returns
        -------
        bool
            True if the hourly scheduling was successfully configured. The method always
            returns True after setting up the interval trigger.

        Notes
        -----
        The event will be triggered at the start of every hour, within the optional scheduling
        window defined by `start_date` and `end_date`. If a random delay (jitter) is set, it
        will be applied to the trigger.
        """

        # Configure the trigger to execute the event every hour.
        # The IntervalTrigger ensures the event is triggered at hourly intervals.
        self.__trigger = IntervalTrigger(
            hours=1,
            start_date=self.__start_date,  # Restrict the schedule start if set
            end_date=self.__end_date,      # Restrict the schedule end if set
            jitter=self.__random_delay     # Apply random delay if configured
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = "Every hour"

        # Indicate that the scheduling was successfully configured.
        return True

    def hourlyAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every hour at a specific minute and second.

        This method configures the event to execute once every hour at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger to help distribute load or avoid
        collisions.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            True if the hourly scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges [0, 59].

        Notes
        -----
        The event will be triggered every hour at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """
        # Validate that minute and second are integers.
        if not isinstance(minute, int) or not isinstance(second, int):
            raise CLIOrionisValueError("Minute and second must be integers.")

        # Validate that minute is within the range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that second is within the range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Set up the trigger to execute the event every hour at the specified minute and second.
        # The IntervalTrigger ensures the event is triggered at hourly intervals.
        self.__trigger = IntervalTrigger(
            hours=1,
            minute=minute,
            second=second,
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date      # Restrict the schedule end if set.
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = f"Every hour at {minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyOddHours(
        self
    ) -> bool:
        """
        Schedule the event to run at every odd hour of the day (e.g., 1 AM, 3 AM, 5 AM, ..., 11 PM).

        This method configures the event to execute at every odd-numbered hour using a `CronTrigger`.
        The schedule can be further restricted by previously set `start_date` and `end_date`.
        If a random delay (jitter) has been configured, it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The event will be triggered 
            at hours 1, 3, 5, ..., 23 of each day.

        Notes
        -----
        The event will be triggered at odd hours of the day, starting from 1 AM and ending at 11 PM.
        """
        # Configure the trigger to execute the event at every odd hour (1, 3, 5, ..., 23)
        # using a CronTrigger. The `hour='1-23/2'` specifies odd hours in the range.
        self.__trigger = CronTrigger(
            hour='1-23/2',                # Schedule the event for odd hours.
            start_date=self.__start_date, # Restrict the schedule start if set.
            end_date=self.__end_date,     # Restrict the schedule end if set.
            jitter=self.__random_delay    # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = "Every odd hour (1, 3, 5, ..., 23)"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyEvenHours(
        self
    ) -> bool:
        """
        Schedule the event to run at every even hour of the day (e.g., 12 AM, 2 AM, 4 AM, ..., 10 PM).

        This method configures the event to execute at every even-numbered hour using a `CronTrigger`.
        The schedule can be further restricted by previously set `start_date` and `end_date`.
        If a random delay (jitter) has been configured, it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The event will be triggered
            at hours 0, 2, 4, ..., 22 of each day.

        Notes
        -----
        The event will be triggered at even hours of the day, starting from 12 AM and ending at 10 PM.
        """
        # Configure the trigger to execute the event at every even hour (0, 2, 4, ..., 22)
        # using a CronTrigger. The `hour='0-22/2'` specifies even hours in the range.
        self.__trigger = CronTrigger(
            hour='0-22/2',                # Schedule the event for even hours.
            start_date=self.__start_date, # Restrict the schedule start if set.
            end_date=self.__end_date,     # Restrict the schedule end if set.
            jitter=self.__random_delay    # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = "Every even hour (0, 2, 4, ..., 22)"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyHours(
        self,
        hours: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in hours.

        This method configures the event to execute repeatedly at a specified interval
        (in hours). The interval must be a positive integer. Optionally, the event can be
        restricted to a time window using previously set `start_date` and `end_date`. If a
        random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        hours : int
            The interval, in hours, at which the event should be executed. Must be a positive integer.

        Returns
        -------
        bool
            True if the interval scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hours` is not a positive integer.

        Notes
        -----
        The event will be triggered every `hours` hours, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set). If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the `hours` parameter is a positive integer.
        if not isinstance(hours, int) or hours <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval.
        # The `start_date` and `end_date` define the optional scheduling window.
        # The `jitter` adds a random delay if configured.
        self.__trigger = IntervalTrigger(
            hours=hours,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = f"Every {hours} hours"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyHoursAt(
        self,
        hours: int,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every hour at a specific minute and second.

        This method configures the event to execute once every hour at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges [0, 59].

        Notes
        -----
        The event will be triggered every hour at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Validate that the `hours` parameter is a positive integer.
        if not isinstance(hours, int) or hours <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Validate that minute and second are integers.
        if not isinstance(minute, int) or not isinstance(second, int):
            raise CLIOrionisValueError("Minute and second must be integers.")

        # Validate that minute is within the range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that second is within the range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every hour at the specified minute and second.
        # The IntervalTrigger ensures the event is triggered at hourly intervals.
        self.__trigger = IntervalTrigger(
            hours=hours,
            minute=minute,
            second=second,
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date       # Restrict the schedule end if set.
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = f"Every hour at {minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyTwoHours(
        self
    ) -> bool:
        """
        Schedule the event to run every two hours.

        This method configures the event to execute at a fixed interval of two hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 2 hours.
        return self.everyHours(2)

    def everyTwoHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every two hours at a specific minute and second.

        This method configures the event to execute every two hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every two hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 2 hours
        # and the specified minute and second.
        return self.everyHoursAt(2, minute, second)

    def everyThreeHours(
        self
    ) -> bool:
        """
        Schedule the event to run every three hours.

        This method configures the event to execute at a fixed interval of three hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 3 hours.
        return self.everyHours(3)

    def everyThreeHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every three hours at a specific minute and second.

        This method configures the event to execute every three hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every three hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 3 hours
        # and the specified minute and second.
        return self.everyHoursAt(3, minute, second)

    def everyFourHours(
        self
    ) -> bool:
        """
        Schedule the event to run every four hours.

        This method configures the event to execute at a fixed interval of four hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 4:00, 8:00, ..., 20:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 4 hours.
        return self.everyHours(4)

    def everyFourHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every four hours at a specific minute and second.

        This method configures the event to execute every four hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every four hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 4 hours
        # and the specified minute and second.
        return self.everyHoursAt(4, minute, second)

    def everyFiveHours(
        self
    ) -> bool:
        """
        Schedule the event to run every five hours.

        This method configures the event to execute at a fixed interval of five hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 5:00, 10:00, 15:00, and 20:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 5 hours.
        return self.everyHours(5)

    def everyFiveHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every five hours at a specific minute and second.

        This method configures the event to execute every five hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every five hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 5 hours
        # and the specified minute and second.
        return self.everyHoursAt(5, minute, second)

    def everySixHours(
        self
    ) -> bool:
        """
        Schedule the event to run every six hours.

        This method configures the event to execute at a fixed interval of six hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 6:00, 12:00, and 18:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 6 hours.
        return self.everyHours(6)

    def everySixHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every six hours at a specific minute and second.

        This method configures the event to execute every six hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every six hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 6 hours
        # and the specified minute and second.
        return self.everyHoursAt(6, minute, second)

    def everySevenHours(
        self
    ) -> bool:
        """
        Schedule the event to run every seven hours.

        This method configures the event to execute at a fixed interval of seven hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 7:00, 14:00, and 21:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 7 hours.
        return self.everyHours(7)

    def everySevenHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every seven hours at a specific minute and second.

        This method configures the event to execute every seven hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every seven hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 7 hours
        # and the specified minute and second.
        return self.everyHoursAt(7, minute, second)

    def everyEightHours(
        self
    ) -> bool:
        """
        Schedule the event to run every eight hours.

        This method configures the event to execute at a fixed interval of eight hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 8:00, 16:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 8 hours.
        return self.everyHours(8)

    def everyEightHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every eight hours at a specific minute and second.

        This method configures the event to execute every eight hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every eight hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 8 hours
        # and the specified minute and second.
        return self.everyHoursAt(8, minute, second)

    def everyNineHours(
        self
    ) -> bool:
        """
        Schedule the event to run every nine hours.

        This method configures the event to execute at a fixed interval of nine hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 9:00, and 18:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 9 hours.
        return self.everyHours(9)

    def everyNineHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every nine hours at a specific minute and second.

        This method configures the event to execute every nine hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every nine hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 9 hours
        # and the specified minute and second.
        return self.everyHoursAt(9, minute, second)

    def everyTenHours(
        self
    ) -> bool:
        """
        Schedule the event to run every ten hours.

        This method configures the event to execute at a fixed interval of ten hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 10:00, and 20:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 10 hours.
        return self.everyHours(10)

    def everyTenHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every ten hours at a specific minute and second.

        This method configures the event to execute every ten hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every ten hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 10 hours
        # and the specified minute and second.
        return self.everyHoursAt(10, minute, second)

    def everyElevenHours(
        self
    ) -> bool:
        """
        Schedule the event to run every eleven hours.

        This method configures the event to execute at a fixed interval of eleven hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 11:00, and 22:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 11 hours.
        return self.everyHours(11)

    def everyElevenHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every eleven hours at a specific minute and second.

        This method configures the event to execute every eleven hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every eleven hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 11 hours
        # and the specified minute and second.
        return self.everyHoursAt(11, minute, second)

    def everyTwelveHours(
        self
    ) -> bool:
        """
        Schedule the event to run every twelve hours.

        This method configures the event to execute at a fixed interval of twelve hours using the
        `everyHours` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyHours`.

        Notes
        -----
        The event will be triggered at 0:00, 12:00 of each day.
        """

        # Delegate the scheduling to the `everyHours` method with an interval of 12 hours.
        return self.everyHours(12)

    def everyTwelveHoursAt(
        self,
        minute: int,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every twelve hours at a specific minute and second.

        This method configures the event to execute every twelve hours at the specified
        minute and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. Jitter (random delay) is not applied
        for this schedule.

        Parameters
        ----------
        minute : int
            The minute of the hour when the event should run. Must be in the range [0, 59].
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `minute` or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered every twelve hours at the specified minute and second,
        within the optional scheduling window defined by `start_date` and `end_date`.
        """

        # Delegate scheduling to the everyHoursAt method with an interval of 12 hours
        # and the specified minute and second.
        return self.everyHoursAt(12, minute, second)

    def daily(
        self
    ) -> bool:
        """
        Schedule the event to run once per day.

        This method configures the event to execute at a fixed interval of one day using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for daily execution.
            The method always returns True after setting up the interval trigger.

        Notes
        -----
        The event will be triggered once every day, within the optional scheduling window defined
        by `start_date` and `end_date`. If a random delay (jitter) is set, it will be applied to
        the trigger.
        """

        # Configure the trigger to execute the event every day.
        # Apply any configured start_date, end_date, and random_delay (jitter).
        self.__trigger = IntervalTrigger(
            days=1,
            start_date=self.__start_date,  # Restrict the schedule start if set
            end_date=self.__end_date,      # Restrict the schedule end if set
            jitter=self.__random_delay     # Apply random delay if configured
        )

        # Store a human-readable description of the schedule.
        self.__details = "Every day"

        # Indicate that the scheduling was successful.
        return True

    def dailyAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run daily at a specific hour, minute, and second.

        This method configures the event to execute once every day at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger to help distribute load or avoid
        collisions.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered once per day at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that hour, minute, and second are integers.
        if not isinstance(hour, int) or not isinstance(minute, int) or not isinstance(second, int):
            raise CLIOrionisValueError("Hour, minute, and second must be integers.")

        # Validate that hour is within valid range.
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that minute and second are within valid ranges.
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Set up the trigger to execute the event daily at the specified time.
        # The IntervalTrigger will fire every day at the given hour, minute, and second.
        self.__trigger = IntervalTrigger(
            days=1,
            hour=hour,
            minute=minute,
            second=second,
            start_date=self.__start_date,
            end_date=self.__end_date
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every day at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successful.
        return True

    def everyDays(
        self,
        days: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in days.

        This method configures the event to execute repeatedly at a specified interval
        (in days). The interval must be a positive integer. Optionally, the event can be
        restricted to a time window using previously set `start_date` and `end_date`.
        If a random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        days : int
            The interval, in days, at which the event should be executed. Must be a positive integer.

        Returns
        -------
        bool
            Returns True if the interval scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `days` is not a positive integer.

        Notes
        -----
        The event will be triggered every `days` days, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set). If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the days parameter is a positive integer.
        if not isinstance(days, int) or days <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval,
        # using any previously set start_date, end_date, and random_delay (jitter).
        self.__trigger = IntervalTrigger(
            days=days,
            start_date=self.__start_date,  # Restrict the schedule start if set
            end_date=self.__end_date,      # Restrict the schedule end if set
            jitter=self.__random_delay     # Apply random delay if configured
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every {days} days"

        # Indicate that the scheduling was successful.
        return True

    def everyDaysAt(
        self,
        days: int,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every day at a specific hour, minute, and second.

        This method configures the event to execute once per day at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger to help distribute load or avoid
        collisions.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised and the trigger is not set.
            On success, returns True.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within the valid ranges.

        Notes
        -----
        The event will be triggered once per day at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the days parameter is a positive integer.
        if not isinstance(days, int) or days <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Validate that hour, minute, and second are integers.
        if not isinstance(hour, int) or not isinstance(minute, int) or not isinstance(second, int):
            raise CLIOrionisValueError("Hour, minute, and second must be integers.")

        # Validate that hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that minute and second are within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Set up the trigger to execute the event daily at the specified time.
        # The IntervalTrigger will fire every day at the given hour, minute, and second.
        self.__trigger = IntervalTrigger(
            days=1,
            hour=hour,
            minute=minute,
            second=second,
            start_date=self.__start_date,
            end_date=self.__end_date
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every day at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successful.
        return True

    def everyTwoDays(
        self
    ) -> bool:
        """
        Schedule the event to run every two days.

        This method configures the event to execute at a fixed interval of two days using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyDays`.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 2 days.
        return self.everyDays(2)

    def everyTwoDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every two days at a specific hour, minute, and second.

        This method configures the event to execute every two days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every two days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 2 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(2, hour, minute, second)

    def everyThreeDays(
        self
    ) -> bool:
        """
        Schedule the event to run every three days.

        This method configures the event to execute at a fixed interval of three days using the
        `everyDays` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. The method always
            returns True after delegating the scheduling to `everyDays`.

        Notes
        -----
        The event will be triggered every three days, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 3 days.
        return self.everyDays(3)

    def everyThreeDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every three days at a specific hour, minute, and second.

        This method configures the event to execute every three days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every three days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 3 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(3, hour, minute, second)

    def everyFourDays(
        self
    ) -> bool:
        """
        Schedule the event to run every four days.

        This method configures the event to execute at a fixed interval of four days using the
        `everyDays` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyDays`.

        Notes
        -----
        The event will be triggered every four days, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 4 days.
        return self.everyDays(4)

    def everyFourDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every four days at a specific hour, minute, and second.

        This method configures the event to execute every four days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every four days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 4 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(4, hour, minute, second)

    def everyFiveDays(
        self
    ) -> bool:
        """
        Schedule the event to run every five days.

        This method configures the event to execute at a fixed interval of five days using the
        `everyDays` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyDays`.

        Notes
        -----
        The event will be triggered every five days, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 5 days.
        return self.everyDays(5)

    def everyFiveDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every five days at a specific hour, minute, and second.

        This method configures the event to execute every five days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every five days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 5 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(5, hour, minute, second)

    def everySixDays(
        self
    ) -> bool:
        """
        Schedule the event to run every six days.

        This method configures the event to execute at a fixed interval of six days using the
        `everyDays` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyDays`.

        Notes
        -----
        The event will be triggered every six days, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 6 days.
        return self.everyDays(6)

    def everySixDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every six days at a specific hour, minute, and second.

        This method configures the event to execute every six days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every six days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 6 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(6, hour, minute, second)

    def everySevenDays(
        self
    ) -> bool:
        """
        Schedule the event to run every seven days.

        This method configures the event to execute at a fixed interval of seven days using the
        `everyDays` method. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. The method always returns True
            after delegating the scheduling to `everyDays`.

        Notes
        -----
        The event will be triggered every seven days, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Delegate the scheduling to the `everyDays` method with an interval of 7 days.
        return self.everyDays(7)

    def everySevenDaysAt(
        self,
        hour: int,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every seven days at a specific hour, minute, and second.

        This method configures the event to execute every seven days at the specified
        hour, minute, and second. The schedule can be further restricted by previously
        set `start_date` and `end_date` attributes. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        hour : int
            The hour of the day when the event should run. Must be in the range [0, 23].
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59].
            Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59].
            Default is 0.

        Returns
        -------
        bool
            Returns True if the scheduling was successfully configured. If the input is invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Notes
        -----
        The event will be triggered every seven days at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Delegate scheduling to the everyDaysAt method with an interval of 7 days
        # and the specified hour, minute, and second.
        return self.everyDaysAt(7, hour, minute, second)

    def everyMondayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Monday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Mondays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Monday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Monday at the specified hour, minute, and second.
        # The `CronTrigger` is used to specify the day of the week and time for the event.
        self.__trigger = CronTrigger(
            day_of_week='mon',  # Schedule the event for Mondays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Monday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyTuesdayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Tuesday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Tuesdays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Tuesday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Tuesday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='tue',  # Schedule the event for Tuesdays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Tuesday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyWednesdayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Wednesday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Wednesdays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Wednesday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Wednesday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='wed',  # Schedule the event for Wednesdays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Wednesday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyThursdayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Thursday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Thursdays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Thursday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Thursday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='thu',  # Schedule the event for Thursdays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Thursday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyFridayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Friday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Fridays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Friday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Friday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='fri',  # Schedule the event for Fridays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Friday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everySaturdayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Saturday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Saturdays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Saturday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Saturday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='sat',  # Schedule the event for Saturdays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Saturday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def everySundayAt(
        self,
        hour: int = 0,
        minute: int = 0,
        second: int = 0
    ) -> bool:
        """
        Schedule the event to run every Sunday at a specific hour, minute, and second.

        This method configures the event to execute once every week on Sundays at the specified
        hour, minute, and second. The schedule can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger.

        Parameters
        ----------
        hour : int, optional
            The hour of the day when the event should run. Must be in the range [0, 23]. Default is 0.
        minute : int, optional
            The minute of the hour when the event should run. Must be in the range [0, 59]. Default is 0.
        second : int, optional
            The second of the minute when the event should run. Must be in the range [0, 59]. Default is 0.

        Returns
        -------
        bool
            True if the scheduling was successfully configured. If the input parameters are invalid,
            a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `hour`, `minute`, or `second` are not integers within their respective valid ranges.

        Notes
        -----
        The event will be triggered every Sunday at the specified time, within the optional
        scheduling window defined by `start_date` and `end_date`. If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the hour is within the valid range [0, 23].
        if not (0 <= hour < 24):
            raise CLIOrionisValueError("Hour must be between 0 and 23.")

        # Validate that the minute is within the valid range [0, 59].
        if not (0 <= minute < 60):
            raise CLIOrionisValueError("Minute must be between 0 and 59.")

        # Validate that the second is within the valid range [0, 59].
        if not (0 <= second < 60):
            raise CLIOrionisValueError("Second must be between 0 and 59.")

        # Configure the trigger to execute the event every Sunday at the specified hour, minute, and second.
        self.__trigger = CronTrigger(
            day_of_week='sun',  # Schedule the event for Sundays.
            hour=hour,          # Set the hour of execution.
            minute=minute,      # Set the minute of execution.
            second=second,      # Set the second of execution.
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay (jitter) if configured.
        )

        # Store a human-readable description of the schedule.
        self.__details = f"Every Sunday at {hour:02d}:{minute:02d}:{second:02d}"

        # Indicate that the scheduling was successfully configured.
        return True

    def weekly(
        self
    ) -> bool:
        """
        Schedule the event to run every week.

        This method configures the event to execute at a fixed interval of one week using an
        `IntervalTrigger`. The scheduling window can be further restricted by previously set
        `start_date` and `end_date` attributes. If a random delay (jitter) has been configured,
        it will be applied to the trigger to help distribute load or avoid collisions.

        Returns
        -------
        bool
            Returns True after successfully configuring the interval trigger for weekly execution.

        Notes
        -----
        The event will be triggered once every week, starting from the configured `start_date`
        (if set) and ending at `end_date` (if set). If a random delay (jitter) is set, it will
        be applied to the trigger.
        """

        # Configure the trigger to execute the event every week using an IntervalTrigger.
        # Apply any configured start_date, end_date, and random_delay (jitter).
        self.__trigger = IntervalTrigger(
            weeks=1,
            start_date=self.__start_date,  # Restrict the schedule start if set.
            end_date=self.__end_date,      # Restrict the schedule end if set.
            jitter=self.__random_delay     # Apply random delay if configured.
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = "Every week"

        # Indicate that the scheduling was successfully configured.
        return True

    def everyWeeks(
        self,
        weeks: int
    ) -> bool:
        """
        Schedule the event to run at fixed intervals measured in weeks.

        This method configures the event to execute repeatedly at a specified interval
        (in weeks). The interval must be a positive integer. Optionally, the event can
        be restricted to a time window using previously set `start_date` and `end_date`.
        If a random delay (jitter) has been configured, it will be applied to the trigger.

        Parameters
        ----------
        weeks : int
            The interval, in weeks, at which the event should be executed. Must be a positive integer.

        Returns
        -------
        bool
            True if the interval scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If `weeks` is not a positive integer.

        Notes
        -----
        The event will be triggered every `weeks` weeks, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set). If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that the `weeks` parameter is a positive integer.
        if not isinstance(weeks, int) or weeks <= 0:
            raise CLIOrionisValueError("The interval must be a positive integer.")

        # Configure the trigger to execute the event at the specified interval.
        # The `start_date` and `end_date` define the optional scheduling window.
        # The `jitter` adds a random delay if configured.
        self.__trigger = IntervalTrigger(
            weeks=weeks,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay
        )

        # Store a human-readable description of the schedule for reference or logging.
        self.__details = f"Every {weeks} week(s)"

        # Indicate that the scheduling was successfully configured.
        return True

    def every(
        self,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0
    ) -> bool:
        """
        Schedule the event to run at fixed intervals specified in weeks, days, hours, minutes, and seconds.

        This method configures the event to execute repeatedly at a specified interval
        composed of weeks, days, hours, minutes, and seconds. At least one of these parameters
        must be a positive integer. Optionally, the event can be restricted to a time window
        using previously set `start_date` and `end_date`. If a random delay (jitter) has been
        configured, it will be applied to the trigger.

        Parameters
        ----------
        weeks : int, optional
            The interval in weeks. Must be a non-negative integer. Default is 0.
        days : int, optional
            The interval in days. Must be a non-negative integer. Default is 0.
        hours : int, optional
            The interval in hours. Must be a non-negative integer. Default is 0.
        minutes : int, optional
            The interval in minutes. Must be a non-negative integer. Default is 0.
        seconds : int, optional
            The interval in seconds. Must be a non-negative integer. Default is 0.

        Returns
        -------
        bool
            True if the interval scheduling was successfully configured. If the input
            is invalid, a `CLIOrionisValueError` is raised, and the trigger is not set.

        Raises
        ------
        CLIOrionisValueError
            If all parameters are zero or if any parameter is not a non-negative integer.

        Notes
        -----
        The event will be triggered at the specified interval, starting from the configured
        `start_date` (if set) and ending at `end_date` (if set). If a random delay (jitter)
        is set, it will be applied to the trigger.
        """

        # Validate that all parameters are integers and non-negative.
        for param_name, param_value in {
            'weeks': weeks,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        }.items():
            if not isinstance(param_value, int) or param_value < 0:
                raise CLIOrionisValueError(f"{param_name.capitalize()} must be a non-negative integer.")

        # Ensure that at least one parameter is greater than zero to define a valid interval.
        if all(param == 0 for param in [weeks, days, hours, minutes, seconds]):
            raise CLIOrionisValueError("At least one interval parameter must be greater than zero.")

        # Configure the trigger to execute the event at the specified interval.
        # The `start_date` and `end_date` define the optional scheduling window.
        self.__trigger = IntervalTrigger(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay
        )

        # Build a human-readable description of the schedule.
        interval_parts = []
        if weeks > 0:
            interval_parts.append(f"{weeks} week(s)")
        if days > 0:
            interval_parts.append(f"{days} day(s)")
        if hours > 0:
            interval_parts.append(f"{hours} hour(s)")
        if minutes > 0:
            interval_parts.append(f"{minutes} minute(s)")
        if seconds > 0:
            interval_parts.append(f"{seconds} second(s)")
        self.__details = "Every " + ", ".join(interval_parts)

        # Indicate that the scheduling was successfully configured.
        return True

    def cron(
        self,
        year: str | None = None,
        month: str | None = None,
        day: str | None = None,
        week: str | None = None,
        day_of_week: str | None = None,
        hour: str | None = None,
        minute: str | None = None,
        second: str | None = None,
    ) -> bool:
        """
        Schedule the event using a CRON-like expression.

        This method configures the event to execute according to cron rules,
        allowing highly customizable schedules (e.g., every Monday at 8am).

        Parameters
        ----------
        year, month, day, week, day_of_week, hour, minute, second : str | None
            Cron-like expressions defining when the job should run.
            Examples: "*/5" (every 5 units), "1-5" (range), "0,15,30,45" (list).

        Returns
        -------
        bool
            True if the cron scheduling was successfully configured.
        """

        # Validate that at least one field is provided
        if all(v is None for v in [year, month, day, week, day_of_week, hour, minute, second]):
            raise CLIOrionisValueError("At least one CRON parameter must be specified.")

        self.__trigger = CronTrigger(
            year=year,
            month=month,
            day=day,
            week=week,
            day_of_week=day_of_week,
            hour=hour,
            minute=minute,
            second=second,
            start_date=self.__start_date,
            end_date=self.__end_date,
            jitter=self.__random_delay,
        )

        # Build human-readable description
        parts = []
        if day_of_week: parts.append(f"on {day_of_week}")
        if hour is not None and minute is not None:
            parts.append(f"at {hour}:{minute.zfill(2)}")
        elif hour is not None:
            parts.append(f"at {hour}:00")

        # Store a human-readable description of the schedule
        self.__details = "Cron schedule " + ", ".join(parts) if parts else "Custom CRON schedule"

        # Indicate that the scheduling was successfully configured.
        return True