#!python3

"""
Anytime algorithm.
Improves its result indefinitely until it is stopped.

Implementation #1: multiprocessing.
Currently does not work; requires a shared variable manager.
To fix it, see here:
https://stackoverflow.com/questions/48902620/anytime-algorithm-using-python-multiprocessing?noredirect=1#comment84811211_48902620

For now, better to use implementation #2.
"""

import abc, time, multiprocessing

class AnytimeAlgorithm(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self):
        """
        Makes a minimal update to the result.
        """

    def update_forever(self):
        while True:
            self.update()

    @abc.abstractmethod
    def result(self):
        """
        return the most up-to-date result.
        """

    def result_after(self, seconds):
        p = multiprocessing.Process(target=self.update_forever, name="update_forever", args=())
        p.start()
        time.sleep(seconds)
        if p.is_alive():
            p.terminate()
        p.join()
        return self.result()
