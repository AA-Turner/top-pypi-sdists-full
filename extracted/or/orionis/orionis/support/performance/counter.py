import time
from orionis.support.performance.contracts.counter import IPerformanceCounter

class PerformanceCounter(IPerformanceCounter):
    """
    A class for measuring the elapsed time between two points in code execution.

    This class provides methods to start and stop a high-resolution performance counter,
    allowing users to measure the duration of specific code segments with precision.

    Attributes
    ----------
    __start_time : float or None
        The timestamp when the counter was started.
    __end_time : float or None
        The timestamp when the counter was stopped.

    Methods
    -------
    start()
        Starts the performance counter.
    stop()
        Stops the performance counter and returns the elapsed time.

    Notes
    -----
    The counter uses `time.perf_counter()` for high-resolution timing.
    """

    def __init__(self):
        """
        Initialize a new PerformanceCounter instance.

        This constructor sets the internal start and end time attributes to None,
        preparing the counter for use. The counter can then be started and stopped
        to measure elapsed time between two points in code execution.

        Attributes
        ----------
        __start_time : float or None
            The timestamp when the counter is started, or None if not started.
        __end_time : float or None
            The timestamp when the counter is stopped, or None if not stopped.
        """

        # Time when the counter is started; initialized to None
        self.__start_time = None

        # Time when the counter is stopped; initialized to None
        self.__end_time = None

        # Difference between end time and start time; initialized to None
        self.__diff_time = None

    def start(self) -> 'PerformanceCounter':
        """
        Start the performance counter.

        Records the current high-resolution time as the start time using
        `time.perf_counter()`. This marks the beginning of the interval to be measured.

        Returns
        -------
        IPerformanceCounter
            The instance of the performance counter for method chaining.
        """

        # Record the current time as the start time
        self.__start_time = time.perf_counter()
        return self

    def stop(self) -> 'PerformanceCounter':
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

        # Record the current time as the end time
        self.__end_time = time.perf_counter()

        # Calculate and return the elapsed time
        self.__diff_time = self.__end_time - self.__start_time
        return self

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

        if self.__diff_time is None:
            raise ValueError("Counter has not been started and stopped properly.")

        return self.__diff_time

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

        return self.elapsedTime() * 1_000_000

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

        return self.elapsedTime() * 1_000

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

        return self.elapsedTime()

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

        return self.elapsedTime() / 60

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

        # Reset start and end times
        self.__start_time = None
        self.__end_time = None
        self.__diff_time = None

        # Start the counter again
        return self.start()