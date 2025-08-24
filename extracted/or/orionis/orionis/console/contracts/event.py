from abc import ABC, abstractmethod
from datetime import datetime
from orionis.console.contracts.schedule_event_listener import IScheduleEventListener
from orionis.console.enums.event import Event as EventEntity

class IEvent(ABC):

    @abstractmethod
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
        pass

    @abstractmethod
    def purpose(
        self,
        purpose: str
    ) -> 'IEvent':
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
        pass

    @abstractmethod
    def startDate(
        self,
        start_date: datetime
    ) -> 'IEvent':
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
        pass

    @abstractmethod
    def endDate(
        self,
        end_date: datetime
    ) -> 'IEvent':
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
        pass

    @abstractmethod
    def randomDelay(
        self,
        max_seconds: int = 10
    ) -> 'IEvent':
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
        pass

    @abstractmethod
    def maxInstances(
        self,
        max_instances: int
    ) -> 'IEvent':
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
        pass

    @abstractmethod
    def subscribeListener(
        self,
        listener: IScheduleEventListener
    ) -> 'IEvent':
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass