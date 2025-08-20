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

    def start(self) -> float:
        """
        Start the performance counter.

        Records the current high-resolution time as the start time using
        `time.perf_counter()`. This marks the beginning of the interval to be measured.

        Returns
        -------
        float
            The timestamp (in fractional seconds) at which the counter was started.
        """

        # Record the current time as the start time
        self.__start_time = time.perf_counter()
        return self.__start_time

    def stop(self) -> float:
        """
        Stop the performance counter and calculate the elapsed time.

        Records the current high-resolution time as the end time and computes
        the elapsed time since `start()` was called. The elapsed time is the
        difference between the end and start timestamps.

        Returns
        -------
        float
            The elapsed time in seconds (as a float) between when `start()` and `stop()` were called.
        """

        # Record the current time as the end time
        self.__end_time = time.perf_counter()

        # Calculate and return the elapsed time
        return self.__end_time - self.__start_time