import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from . import ClusterUtil

logger = logging.getLogger(__name__)


class ClusterHealthChecker:
    '''Orchestrates periodic health checks across all registered backends.

    A single PeriodicTask fires every health_check_interval.  On each tick,
    each registered backend is checked in its own thread-pool future.  If a
    previous check for a backend is still in flight when the next tick fires,
    that backend is skipped — ensuring at most one concurrent check per backend
    regardless of how long a check takes.

    Usage:
        checker = ClusterHealthChecker(health_check_interval=5)
        checker.start()

        # when a backend is added:
        checker.register(addrport, check_fn, backend.is_closed)

        # when a backend is removed:
        checker.deregister(addrport)

        checker.stop()
    '''

    def __init__(self, health_check_interval, max_workers=None):
        self._health_check_interval = health_check_interval
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers or 11,
            thread_name_prefix='ClusterHealthCheck',
        )
        self._checkers = {}   # addrport -> (check_fn, is_closed_fn)
        self._futures = {}    # addrport -> Future — tracks in-flight checks
        self._lock = threading.Lock()
        self._task = None

    def register(self, addrport, check_fn, is_closed):
        '''Enrol a backend in the health check rotation. check_fn(is_closed)
        is invoked on each tick.'''
        with self._lock:
            self._checkers[addrport] = (check_fn, is_closed)
        logger.debug('Registered health check for %s', addrport)

    def deregister(self, addrport):
        '''Remove a backend from the health check rotation and discard its in-flight future.'''
        with self._lock:
            self._checkers.pop(addrport, None)
            self._futures.pop(addrport, None)
        logger.debug('Deregistered health check for %s', addrport)

    def start(self):
        '''Start the periodic tick that drives health checks.'''
        self._task = ClusterUtil.periodic_task(
            self._check_all,
            self._health_check_interval,
            jitter=self._health_check_interval * 0.1,
        )

    def stop(self):
        '''Cancel the periodic tick and shut down the executor.'''
        if self._task:
            self._task.cancel()
            self._task = None
        self._executor.shutdown(wait=False)

    def _check_all(self):
        '''Tick handler: submit a check future for each backend that is not already being checked.'''
        with self._lock:
            items = list(self._checkers.items())

        logger.debug('Running cluster health check for %d backend(s)', len(items))
        for addrport, registered in items:
            check_fn, is_closed = registered
            with self._lock:
                if self._checkers.get(addrport) != registered:
                    continue
                future = self._futures.get(addrport)
                if future and not future.done():
                    logger.debug('Skipping health check for %s — previous check still in flight', addrport)
                    continue
                self._futures[addrport] = self._executor.submit(check_fn, is_closed)
