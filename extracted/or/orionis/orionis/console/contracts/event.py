from abc import ABC, abstractmethod
from datetime import datetime
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
        pass

    @abstractmethod
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
        pass