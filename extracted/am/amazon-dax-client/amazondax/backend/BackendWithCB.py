import logging
import threading

from .BaseBackend import BaseBackend
from ..Constants import Role

logger = logging.getLogger(__name__)


class BackendWithCB(BaseBackend):
    '''A pure connection holder for one cluster node.

    Owns the client and its factory.  All health-check logic, health
    state, and routing callbacks are handled externally (EndpointHealthChecker
    + EndpointRouter).  The only reason this class exists is to provide a
    stable, thread-safe home for the client reference.
    '''

    def __init__(self, service_endpoint):
        self._service_endpoint = service_endpoint
        self._client_factory = None  # set via set_client_factory before start()
        self.client = None
        self._closed = False
        self._lock = threading.RLock()

    def set_client_factory(self, factory):
        '''Supply the fully-baked node client factory (called by the router).'''
        self._client_factory = factory

    def start(self):
        '''Create the initial client connection (soft failure — errors are logged).'''
        try:
            self.client = self._client_factory()
        except Exception as e: # pylint: disable=broad-except
            logger.warning('Could not create client for %s: %s', self.addrport, e)

    def close(self):
        '''Close the client and mark the backend as closed.'''
        with self._lock:
            if self._closed:
                return
            logger.debug('Closing %s', self)
            if self.client:
                self.client.close()
                self.client = None
            self._closed = True

    def update(self, new_service_endpoint):
        if self._service_endpoint != new_service_endpoint:
            if self._service_endpoint.addrport != new_service_endpoint.addrport:
                raise ValueError('Cannot update backend to new address.')

            self._service_endpoint = new_service_endpoint
            return True

        return False

    def is_closed(self):
        '''Return True if the backend has been shut down.'''
        return self._closed

    def fetch_client(self):
        '''Return the current client.'''
        return self.client

    def replace_client(self, old, new):
        '''Atomically swap the client, closing the old one if it still matches.'''
        with self._lock:
            if self.client is old or old is None:
                if old:
                    try:
                        old.close()
                    except Exception: # pylint: disable=broad-except
                        pass
                self.client = new

    @property
    def addrport(self):
        return self._service_endpoint.addrport

    @property
    def role(self):
        return self._service_endpoint.role

    @property
    def leader(self):
        return self._service_endpoint.role == Role.LEADER

    def __repr__(self):
        return 'BackendWithCB({})'.format(self._service_endpoint)
