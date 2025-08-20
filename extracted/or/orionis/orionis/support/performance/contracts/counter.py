from abc import ABC, abstractmethod

class IPerformanceCounter(ABC):
    """
    A class for measuring the elapsed time between two points in code execution.

    This class provides methods to start and stop a high-resolution performance counter,
    allowing users to measure the duration of specific code segments with precision.
    """

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass