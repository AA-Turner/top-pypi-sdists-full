""" This module contains functions and variables to control hiPhive's logging

* `logger` - the module logger
* set_config - function to control level and logfile
"""

import logging
import sys
from timeit import default_timer as timer

# This is the root logger of hiPhive
logger = logging.getLogger('hiphive')

# Will process all levels of INFO or higher
logger.setLevel(logging.INFO)

# If you know what you are doing you may set this to True
logger.propagate = False

# The hiPhive logger will collect events from childs and the default behaviour
# is to print it directly to stdout
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)

continuous_logging = False


# TODO: use Context management protocol instead
class Progress:
    """ Progress bar like functionality. """

    def __init__(self, tot=None, mode='frac', estimate_remaining=True):
        if tot is None:
            self._tot = '?'
            assert not estimate_remaining
        else:
            self._tot = tot
        self._progress = 0
        self._estimate_remaining = estimate_remaining
        self._last_update = 0
        self._start = timer()

    def tick(self):
        self._progress += 1
        delta = timer() - self._last_update
        if continuous_logging and delta > 2:
            self._last_update = timer()
            print('\r' + ' ' * 70 + '\r', end='', flush=True)
            print('{}/{}={:.3%}'.format(self._progress,
                  self._tot, self._progress/self._tot), end='', flush=True)
            if self._estimate_remaining and self._tot != '?':
                remaining_time = (self._tot - self._progress) * (
                    timer() - self._start) / self._progress
                print('  time remaining: {:.3}'.format(remaining_time), end='',
                      flush=True)

    def close(self):
        if continuous_logging:
            print('\r' + ' ' * 70 + '\r', end='', flush=True)
        s = timer() - self._start
        d, remainder = divmod(s, 60*60*24)
        h, remainder = divmod(remainder, 60*60)
        m, s = divmod(remainder, 60)
        logger.info('Done in {}d {}h {}m {:.3}s'
                    .format(int(d), int(h), int(m), s))


def set_config(filename=None, level=None, continuous=None):
    """
    Alters the way logging is handled.

    Parameters
    ----------
    filename : str
        name of file the log should be sent to
    level : int
        verbosity level; see `Python logging library
        <https://docs.python.org/3/library/logging.html>`_ for details
    continuous : bool
        if True the progress will be continously updated
    """

    # If a filename is provided a logfile will be created
    if filename is not None:
        fh = logging.FileHandler(filename)
        logger.addHandler(fh)

    if level is not None:
        logger.setLevel(level)

    if continuous is not None:
        global continuous_logging
        continuous_logging = continuous
