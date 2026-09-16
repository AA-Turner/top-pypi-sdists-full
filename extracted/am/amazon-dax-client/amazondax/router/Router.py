import logging
import itertools
import threading
import time

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait as future_wait

from ..Constants import Role
from ..DaxError import DaxClientError, DaxErrorCode
from ..backend.Backend import Backend
from .BaseRouter import BaseRouter
from .RouterUtils import random_route

logger = logging.getLogger(__name__)


class Router(BaseRouter):
    ''' Determine which nodes to route requests to.

    This manages the Backend objects that represent nodes in the cluster, and allows retrieving the appropriate
    node type (leader or replica).
    '''
    def __init__(self,
                 client_factory,
                 health_check_interval,
                 selector=None,
                 executor=None,
                 **kwargs):
        self.selector = selector or random_route

        # _client_factory: callable(hostname, addrport, ip_version, **kwargs) -> client
        self._client_factory = client_factory

        # endpoints returned from last successful endpoints() call to the cluster
        self._service_endpoints = frozenset()

        # backends is a dict[role, dict[(hostname,port,node), backend] of the
        # active backends
        self.backends = defaultdict(dict)

        # dict of AddrPort -> Backend of inactive backends. When they
        # come up, they are moved to self.backends.
        self._pending_backends = {}

        self._health_check_interval = health_check_interval

        self._lock = threading.RLock()
        self._route_change = threading.Condition(self._lock)

        # Executor for health checks
        self._background = executor or ThreadPoolExecutor(max_workers=2)

    @property
    def all_backends(self):
        return list(self._all_backends())

    def _all_backends(self):
        return itertools.chain.from_iterable(role_backends.values() for role, role_backends in self.backends.items())

    @property
    def leader_backends(self):
        return list(self.backends[Role.LEADER].values())

    def close(self):
        with self._lock:
            backends = self.all_backends + list(self._pending_backends.values())

        closers = [self._background.submit(backend.close) for backend in backends]
        done, not_done = future_wait(closers, timeout=5.0) # pylint: disable=unused-variable
        # TODO What to do with not_done?

        with self._lock:
            self.backends.clear()
            self.backends = None

        self._background.shutdown()

    def update(self, service_endpoints):
        ''' Update the set of connected endpoints.

        If an endpoint has changed roles, move it. If it is new, create a new backend.
        If a backend is not in the new endpoint list, close & remove it.
        '''
        if self._service_endpoints == service_endpoints:
            # If the backends haven't changed, skip the update process
            return

        pending = []
        with self._lock:
            for ep in service_endpoints:
                self._update_endpoint(ep)

            pending.extend(self._purge_endpoints(service_endpoints))
            self._service_endpoints = service_endpoints

        done, not_done = future_wait(pending, timeout=5.0) # pylint: disable=unused-variable
        # TODO What to do with not_done?

        logger.debug('Current backends: %s', dict(self.backends))

    def _update_endpoint(self, service_endpoint):
        ''' Update any endpoints that have changed or are new.

        Not thread-safe. Must be called from inside update().
        '''
        new_addrport = service_endpoint.addrport
        new_role = service_endpoint.role

        backend = self.backends[new_role].get(new_addrport)
        if backend is not None:
            # Backend is up-to-date, no changes necessary
            logger.debug('Updating active backend %s', backend)
            backend.update(service_endpoint)
        else:
            # Role may have changed, so search other roles to see if we're already connected
            for role, role_backends in self.backends.items():
                if role == new_role:
                    # Already checked...
                    continue

                backend = role_backends.pop(new_addrport, None)
                if backend is not None:
                    # Backend has only changed roles, so just move it
                    backend.update(service_endpoint)
                    self.backends[new_role][new_addrport] = backend
                    logger.debug('%s changing role from %s to %s', backend, Role(role).name, Role(new_role).name)
                    break
            else: # no break
                # Update it if pending
                if new_addrport in self._pending_backends:
                    logger.debug('Updating pending backend %s', self._pending_backends[new_addrport])
                    self._pending_backends[new_addrport].update(service_endpoint)
                else:
                    # Backend does not exist, so create it
                    # It will add itself when it is ready
                    self._create_backend(service_endpoint)

    def _purge_endpoints(self, service_endpoints):
        ''' Remove backends that no longer have corresponding endpoints.

        Not thread-safe. Must be called from inside update().
        '''
        endpoints = {ep.addrport for ep in service_endpoints}

        pending = []
        for role_backends in self.backends.values():
            to_remove = []
            for addrport, backend in role_backends.items():
                if addrport not in endpoints:
                    # This backend is no longer in the service endpoints, so close it
                    # It will remove itself when closed
                    logger.debug('Removing unused backend %s', backend)
                    pending.append(self._background.submit(backend.close)) # Method ref, not call
                    to_remove.append(addrport) # Can't delete while looping

            # Remove all keys
            for addrport in to_remove:
                del role_backends[addrport]

        to_remove = []
        for addrport, backend in self._pending_backends.items():
            if addrport not in endpoints:
                logger.debug('Removing unused pending backend %s', addrport)
                pending.append(self._background.submit(backend.close))
                to_remove.append(addrport)

        for addrport in to_remove:
            del self._pending_backends[addrport]

        return pending

    def _create_backend(self, service_endpoint):
        ''' Create a new Backend instance and add it to the pending list.

        If a backend is already pending, do nothing.

        Not thread-safe. Must be called from inside update().
        '''

        logger.debug('Creating backend for %s', service_endpoint)

        pending_backend = self._pending_backends.get(service_endpoint.addrport)
        if pending_backend is None:
            logger.debug('Creating backend for %s', service_endpoint)
            pending_backend = Backend(
                service_endpoint,
                self._client_factory,
                self._health_check_interval,
                self._backend_up,
                self._backend_down)
            self._pending_backends[service_endpoint.addrport] = pending_backend

            # Bring the backend up in the background
            self._background.submit(pending_backend.start)
        else:
            # There is already a pending backend for this endpoint,
            # so let it continue instead
            pass

    def _backend_up(self, backend):
        with self._lock:
            self.backends[backend.role][backend.addrport] = backend
            self._pending_backends.pop(backend.addrport, None)
            self._route_change.notify_all()
        logger.debug('Backend up: %s', backend)

    def _backend_down(self, backend):
        role = backend.role
        with self._lock:
            # Move it to pending if it's being brought down because of a health
            # check or other failure. Otherwise it's been removed from the
            # roster.
            if next((e for e in self._service_endpoints if e.addrport == backend.addrport), False):
                self._pending_backends[backend.addrport] = backend
            self.backends[role].pop(backend.addrport, None)
            self._route_change.notify_all()
        logger.debug('Backend down: %s', backend)

    def wait_for_routes(self, min_healthy=1, leader_min=1, timeout=None):
        start = _clock()
        while True:
            with self._lock:
                if self._has_active_any(min_healthy) and self._has_active_leaders(leader_min):
                    return
                else:
                    now = _clock()
                    if timeout is not None and now - start > timeout:
                        raise DaxClientError(
                            "Not enough routes after {}s: expected {}/{}, found {}/{} (healthy/leaders)".format(
                                timeout, min_healthy, leader_min, self._active_any(), self._active_leaders()),
                            DaxErrorCode.NoRoute)

                # Wait for a signal that the endpoints have changed
                self._route_change.wait(timeout)

    def _active_any(self):
        return sum(len(role_backend) for role, role_backend in self.backends.items())

    def _has_active_any(self, min_healthy):
        if min_healthy < 1:
            return True
        else:
            return self._active_any() >= min_healthy

    def _active_leaders(self):
        return len(self.backends[Role.LEADER])

    def _has_active_leaders(self, leader_min):
        if leader_min < 1:
            return True
        else:
            return self._active_leaders() >= leader_min

    def next_leader(self, prev_client):
        ''' Returns the next leader entry that is not the given prev value if one such entry is available.

        If there is only one entry and that is equals to prev, prev is returned.
        Returns None if nothing is available.
        '''

        with self._lock:
            if self.backends is not None:
                backend = self.selector(prev_client, self.leader_backends)
                return backend.client if backend is not None else None

    def next_any(self, prev_client):
        ''' Returns any entry that is not the given prev value, if any such entry is available.

        If there is only one entry and that is equals to prev, prev is returned.
        Returns None if nothing is available.
        '''
        with self._lock:
            if self.backends is not None:
                backend = self.selector(prev_client, self.all_backends)
                return backend.client if backend is not None else None

    def start(self):
        ''' Set up the initial roster of nodes delegated to the cluster's
         endpoint refresher. '''
        pass


def _clock():
    return time.time()
