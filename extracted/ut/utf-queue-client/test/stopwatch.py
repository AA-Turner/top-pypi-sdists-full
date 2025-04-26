import time


class Stopwatch:
    """Helper class for measuring elapsed time

    Examples:
        stopwatch = Stopwatch()
        # do some operation that takes time
        foo()
        print(f"elapsed time of foo(): {stopwatch.elapsed_sec} seconds")

    """

    def __init__(self):
        self.start = time.perf_counter()

    @property
    def elapsed_sec(self):
        now = time.perf_counter()
        return now - self.start
