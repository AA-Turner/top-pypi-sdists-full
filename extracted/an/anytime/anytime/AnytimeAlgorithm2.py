#!python3

"""
Anytime algorithm.
Improves its result indefinitely until it is stopped.

Implementation #2: a while-loop checking the time after each iteration.
Not accurate, but probably more efficient than multiprocessing.
"""

import abc, time, multiprocessing

class AnytimeAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self):
        """
        Makes a minimal update to the result.
        """

    @abc.abstractmethod
    def result(self):
        """
        return the most up-to-date result.
        """

    def run_for(self, seconds:float=None, iterations:int=None):
        """
        Continuously runs the "update" method. Stops whenever at least one of the following happens:
        * "seconds" seconds have passed (if seconds is given)
        * "iterations" iterations have passed (if iterations is given)
        """
        self.iteration = 0
        start = time.perf_counter()   # current time in seconds
        while True:
            if seconds is not None and time.perf_counter()-start>seconds:
                break
            if iterations is not None and self.iteration>=iterations:
                break
            self.iteration += 1
            self.update()

    def result_after(self, seconds:float=None, iterations:int=None):
        """
        Runs updates for the given amount of seconds, and returns the result.
        """
        self.run_for(seconds=seconds,iterations=iterations)
        return self.result()

