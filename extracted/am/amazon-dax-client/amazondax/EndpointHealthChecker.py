import logging
import threading
import time

logger = logging.getLogger(__name__)


class EndpointHealthCheckerDefaults:
    FAILURE_THRESHOLD = 5


class EndpointHealthChecker(EndpointHealthCheckerDefaults):
    '''Performs health checks for a single backend node and tracks its health state.

    Has no internal scheduler — check(is_closed) is driven externally by
    ClusterHealthChecker, which guarantees at most one in-flight check per
    backend at a time.

    client_factory is set after construction via the property setter to break
    the circular dependency: the factory's operation callbacks reference this
    checker, so the checker must exist before the factory can be built.

    Constructor parameters
    ----------------------
    addrport              — (address, port) of the node, used for logging.
    fetch_client          — callable() → current client or None; supplied by
                            BackendWithCB.fetch_client.
    replace_client        — callable(old, new): atomically swap the client;
                            supplied by BackendWithCB.replace_client.
    on_healthy            — callable(): invoked when a health check succeeds
                            and health state actually changed.
    on_unhealthy          — callable(): invoked when a health check fails
                            and health state actually changed.
    retry_delay           — delay in seconds between retry attempts.
    max_attempts          — total number of health-check attempts.

    Thread-safety
    -------------
    _healthy and _error_count are written by user request threads via
    on_read_success / on_read_failure, and by the health-check thread via
    _on_check_success / _on_check_failure / reset_health_status.  A plain
    threading.Lock guards both fields so they are always updated as a
    consistent pair.
    '''

    def __init__(
        self,
        addrport,
        fetch_client,
        replace_client,
        on_healthy,
        on_unhealthy,
        retry_delay,
        max_attempts,
    ):
        self._addrport = addrport
        self._client_factory = None  # set via set_client_factory
        self._fetch_client = fetch_client
        self._replace_client = replace_client
        self._on_healthy = on_healthy
        self._on_unhealthy = on_unhealthy
        self._retry_delay = retry_delay
        self._max_attempts = max_attempts

        self._healthy = True
        self._error_count = 0
        self._lock = threading.Lock()

    def set_client_factory(self, factory):
        '''Supply the fully-baked node client factory (called by the router).'''
        self._client_factory = factory

    def is_healthy(self):
        '''Return the current health state.'''
        with self._lock:
            return self._healthy

    def on_read_success(self):
        '''Reset the consecutive-failure counter on a successful client operation.'''
        with self._lock:
            if not self._healthy:
                return
            self._error_count = 0

    def on_read_failure(self, failure_handler=None):
        '''Increment the failure counter; mark the node unhealthy at the threshold.'''
        should_trigger_failure_handler = False
        with self._lock:
            if not self._healthy:
                return
            self._error_count += 1
            if self._error_count >= self.FAILURE_THRESHOLD:
                self._healthy = False
                logger.debug(
                    'Marked %s temporarily unhealthy after %d consecutive read failures',
                    self._addrport, self._error_count,
                )
                should_trigger_failure_handler = True

        # Called outside self._lock: failure_handler (BaseRouter.remove_route) acquires the
        # router lock, and the router lock is held while calling back into checker
        # methods (e.g. _rebuild_all_routes -> reset_health_status). Calling the handler
        # while still holding self._lock here would invert that lock order and deadlock.
        if should_trigger_failure_handler and callable(failure_handler):
            failure_handler()

    def reset_health_status(self):
        '''Restore the node to healthy with a zeroed failure counter.'''
        with self._lock:
            self._healthy = True
            self._error_count = 0
        logger.debug('Reset health status for %s', self._addrport)

    def check(self, is_closed):
        '''Run one health check cycle with retries and client purge.'''
        for attempt in range(1, self._max_attempts + 1):
            if is_closed():
                return

            logger.debug('Health check %d/%d for %s', attempt, self._max_attempts, self._addrport)
            try:
                self._get_or_create()
                self._fetch_client().endpoints()
                self._on_check_success()
                return
            except Exception as e:
                logger.warning(
                    'Health check %d/%d failed for %s: %s',
                    attempt, self._max_attempts, self._addrport, e,
                )
                if attempt < self._max_attempts:
                    time.sleep(self._retry_delay)

        if self._purge_client():
            self._on_check_success()
        else:
            self._on_check_failure()

    def _on_check_success(self):
        '''Reset health state and notify the router only when state changed.'''
        with self._lock:
            if self._error_count == 0 and self._healthy:
                return
            self._healthy = True
            self._error_count = 0
        self._on_healthy()

    def _on_check_failure(self):
        '''Mark unhealthy and notify the router only when state changed.'''
        with self._lock:
            if not self._healthy:
                return
            self._healthy = False
        self._on_unhealthy()

    def _get_or_create(self):
        '''Recreate the client if it is missing or already closed.'''
        client = self._fetch_client()
        if not client:
            self._replace_client(client, self._client_factory())

    def _purge_client(self):
        '''Attempt once to purge and replace the broken client.'''
        try:
            old = self._fetch_client()
            new = self._client_factory()
            new.endpoints()
            self._replace_client(old, new)
            logger.debug('Client purged succeeded for %s', self._addrport)
            return True
        except Exception: # pylint: disable=broad-except
            pass
        logger.debug('Client purged failed for %s', self._addrport)
        return False

    def ping(self):
        '''Ping the node with the regular backend client.

        Used by fail-open route rebuilds before resetting health status.
        '''
        try:
            self._get_or_create()
            self._fetch_client().endpoints()
            return True
        except Exception as e:
            logger.warning('Ping failed for %s: %s',self._addrport, e)
            return False
