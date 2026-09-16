import logging
import threading

from .BaseBackend import BaseBackend
from ..ClusterUtil import periodic_task
from ..Constants import Role

logger = logging.getLogger(__name__)


class Backend(BaseBackend):

    def __init__(self, service_endpoint, client_factory, health_check_interval, on_up, on_down):
        self._service_endpoint = service_endpoint
        self._client_factory = client_factory
        self._health_check_interval = health_check_interval
        self._connection_timeout = self._health_check_interval / 2

        self._on_up = on_up
        self._on_down = on_down

        self._error_count = 0

        self.client = None
        self.session = None
        self.active = False
        self._healthy = True  # Healthy until proven otherwise
        self._closed = False

        self._lock = threading.RLock()
        self._timer = None

    def start(self):
        self._health_check()
        logger.debug('Creating health checker for %s', self)
        self._timer = periodic_task(
            self._health_check,
            self._health_check_interval,
            self._health_check_interval * 0.1)

    def update(self, new_service_endpoint):
        if self._service_endpoint != new_service_endpoint:
            if self._service_endpoint.addrport != new_service_endpoint.addrport:
                raise ValueError('Cannot update backend to new address.')

            self._service_endpoint = new_service_endpoint
            return True

        return False

    def close(self):
        with self._lock:
            if self._closed:
                return

            logger.debug('Closing %s', self)

            if self._timer:
                self._timer.cancel()
                self._timer = None

            if self.active:
                self.down()

            self._closed = True

    def is_closed(self):
        '''Return True if the backend has been shut down.'''
        return self._closed

    @property
    def addrport(self):
        return self._service_endpoint.addrport

    @property
    def role(self):
        return self._service_endpoint.role

    @property
    def leader(self):
        return self._service_endpoint.role == Role.LEADER

    @property
    def suspect(self):
        return self._error_count > 0

    def up(self):
        upped = False
        with self._lock:
            if not self.active:
                self._error_count = 0
                self.active = True
                upped = True

        if upped:
            self._on_up(self)

    def down(self):
        if self._closed:
            return

        self._on_down(self)

        with self._lock:
            self.active = False
            if self.client:
                self.client.close()
                self.client = None

    def _health_check(self):
        with self._lock:
            if self._closed:
                return

            if not self.client:
                try:
                    self.client = self._client_factory(
                        self._service_endpoint.hostname, self.addrport, self._service_endpoint.ip_version
                    )
                except Exception as e: # pylint: disable=broad-except
                    logger.warning("Health check failed to get client with Error %s", e)

            # Determine health by calling endpoints
            try:
                logger.debug('Running health check for %s', self)
                _ = self.client.endpoints()
            except Exception as e: # pylint: disable=broad-except
                logger.warning("Health check failed for %s: %s", self.addrport.address, e)
                if self.active:
                    self.down()

                return
            else:
                if not self.active:
                    self.up()

        return

    def __repr__(self):
        return 'Backend({})'.format(self._service_endpoint)
