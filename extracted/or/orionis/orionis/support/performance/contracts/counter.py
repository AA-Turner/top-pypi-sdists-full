from abc import ABC, abstractmethod

class IPerformanceCounter(ABC):
    """
    A class for measuring the elapsed time between two points in code execution.

    This class provides methods to start and stop a high-resolution performance counter,
    allowing users to measure the duration of specific code segments with precision.
    """

    @abstractmethod
    def start(self) -> 'IPerformanceCounter':
        """
        Start the performance counter.

        Records the current high-resolution time as the start time using
        `time.perf_counter()`. This marks the beginning of the interval to be measured.

        Returns
        -------
        IPerformanceCounter
            The instance of the performance counter for method chaining.
        """
        pass

    @abstractmethod
    def stop(self) -> 'IPerformanceCounter':
        """
        Stop the performance counter and calculate the elapsed time.

        Records the current high-resolution time as the end time and computes
        the elapsed time since `start()` was called. The elapsed time is the
        difference between the end and start timestamps.

        Returns
        -------
        IPerformanceCounter
            The instance of the performance counter for method chaining.
        """
        pass

    @abstractmethod
    def elapsedTime(self) -> float:
        """
        Get the elapsed time between the last start and stop calls.

        This method returns the elapsed time calculated during the last
        `stop()` call. If the counter has not been started and stopped,
        it raises an exception.

        Returns
        -------
        float
            The elapsed time in seconds (as a float) between the last `start()` and `stop()` calls.

        Raises
        ------
        ValueError
            If the counter has not been started and stopped properly.
        """
        pass

    @abstractmethod
    def getMicroseconds(self) -> float:
        """
        Get the elapsed time in microseconds.

        This method returns the elapsed time in microseconds by converting
        the value obtained from `elapsedTime()`.

        Returns
        -------
        float
            The elapsed time in microseconds (as a float).
        """
        pass

    @abstractmethod
    def getMilliseconds(self) -> float:
        """
        Get the elapsed time in milliseconds.

        This method returns the elapsed time in milliseconds by converting
        the value obtained from `elapsedTime()`.

        Returns
        -------
        float
            The elapsed time in milliseconds (as a float).
        """
        pass

    @abstractmethod
    def getSeconds(self) -> float:
        """
        Get the elapsed time in seconds.

        This method returns the elapsed time in seconds, which is the same
        value as obtained from `elapsedTime()`.

        Returns
        -------
        float
            The elapsed time in seconds (as a float).
        """
        pass

    @abstractmethod
    def getMinutes(self) -> float:
        """
        Get the elapsed time in minutes.

        This method returns the elapsed time in minutes by converting
        the value obtained from `elapsedTime()`.

        Returns
        -------
        float
            The elapsed time in minutes (as a float).
        """
        pass

    @abstractmethod
    def restart(self) -> float:
        """
        Restart the performance counter.

        This method resets the start and end times to None and starts the counter again.
        It is useful for measuring a new interval without creating a new instance of
        PerformanceCounter.

        Returns
        -------
        float
            The timestamp (in fractional seconds) at which the counter was restarted.
        """
        pass