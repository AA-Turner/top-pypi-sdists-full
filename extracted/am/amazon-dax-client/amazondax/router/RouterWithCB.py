# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# is located at
#
#    http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import functools
import itertools
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait as future_wait
from collections import defaultdict

from ..ClusterHealthChecker import ClusterHealthChecker
from ..Constants import Role
from ..DaxError import DaxClientError, DaxErrorCode
from ..EndpointHealthChecker import EndpointHealthChecker
from ..backend.BackendWithCB import BackendWithCB
from .BaseRouter import BaseRouter
from .RouterUtils import random_route

import logging
logger = logging.getLogger(__name__)


class RouterWithCBDefaults:
    HEALTH_CHECK_RETRY_DELAY = 0.5
    HEALTH_CHECK_MAX_ATTEMPTS = 3
    HEALTHY_ROUTE_REBUILD_TIMEOUT = 1.0
    BACKGROUND_EXECUTOR_MAX_WORKERS = 16


class RouterWithCB(BaseRouter, RouterWithCBDefaults):
    '''Determine which nodes to route requests to.

    Manages the BackendWithCB objects representing nodes in the cluster and
    exposes next_leader / next_any for request dispatch.

    Health check scheduling is delegated to ClusterHealthChecker.
    Circuit-breaker logic lives here, alongside the route table.
    '''

    def __init__(
        self,
        client_factory,
        health_check_interval,
        selector=None,
        executor=None,
        health_check_retry_delay=RouterWithCBDefaults.HEALTH_CHECK_RETRY_DELAY,
        health_check_max_attempts=RouterWithCBDefaults.HEALTH_CHECK_MAX_ATTEMPTS,
    ):
        self.selector = selector or random_route

        # _client_factory: callable(hostname, addrport, ip_version, **kwargs) -> client
        self._client_factory = client_factory

        self._service_endpoints = frozenset()

        # routes: dict[role, dict[addrport, BackendWithCB]] for active backends only.
        self.routes = defaultdict(dict)
        # backends: dict[addrport, BackendWithCB] for every known backend.
        self.backends = {}
        # checkers: dict[addrport, EndpointHealthChecker] — parallel to backends.
        self._checkers = {}

        self._health_check_interval = health_check_interval
        self._health_check_retry_delay = health_check_retry_delay
        self._health_check_max_attempts = health_check_max_attempts
        self._active_routes_threshold = 0

        self._lock = threading.RLock()
        self._route_change = threading.Condition(self._lock)

        # Executor for backend closing and asynchronous route rebuild work.
        self._background = executor or ThreadPoolExecutor(max_workers=self.BACKGROUND_EXECUTOR_MAX_WORKERS)
        # Keep route-rebuild pings separate so rebuild tasks cannot occupy every
        # worker while waiting for pings that are queued behind them.
        self._ping_background = ThreadPoolExecutor(max_workers=self.BACKGROUND_EXECUTOR_MAX_WORKERS)

        self._cluster_health_checker = ClusterHealthChecker(
            health_check_interval=health_check_interval,
        )

    def start(self):
        '''Bootstrap the cluster and start background refresh + health checks.'''
        self._cluster_health_checker.start()

    def close(self):
        logger.debug('Closing router...')
        self._cluster_health_checker.stop()

        closers = [
            self._background.submit(backend.close)
            for backend in self.backends.values()
        ]
        future_wait(closers, timeout=5.0)

        with self._lock:
            self.clear_routes()
            self.backends.clear()
            self._checkers.clear()

        self._background.shutdown()
        self._ping_background.shutdown()

    def update(self, service_endpoints):
        '''Incrementally update backends and rebuild routes for topology changes.'''
        if self._service_endpoints == service_endpoints:
            return

        logger.debug('Updating service endpoints from %s to %s', self._service_endpoints, service_endpoints)

        endpoints_by_addrport = {endpoint.addrport: endpoint for endpoint in service_endpoints}
        new_addrports = set(endpoints_by_addrport.keys())
        with self._lock:
            old_addrports = set(self.backends.keys())
            removed_addrports = old_addrports - new_addrports
            retained_addrports = old_addrports & new_addrports
            added_addrports = new_addrports - old_addrports

            to_remove = []
            for addrport in removed_addrports:
                backend = self.backends.pop(addrport)
                self._deregister(addrport)
                to_remove.append(backend)

            for addrport in retained_addrports:
                backend = self.backends[addrport]
                service_endpoint = endpoints_by_addrport[addrport]
                backend.update(service_endpoint)

            to_add = [
                self._create_backend(endpoints_by_addrport[addrport])
                for addrport in added_addrports
            ]
            to_add.sort(key=lambda b: not b.leader)

            for backend in to_add:
                self.backends[backend.addrport] = backend

            self.backends = dict(sorted(self.backends.items(), key=lambda item: not item[1].leader))
            self._active_routes_threshold = 2/3 * len(self.backends)
            self._service_endpoints = service_endpoints
            self._rebuild_all_routes()

        closers = [self._background.submit(backend.close) for backend in to_remove]
        future_wait(closers, timeout=5.0)

    def wait_for_routes(self, min_healthy=1, leader_min=1, timeout=None):
        start = time.time()
        while True:
            with self._lock:
                if self._has_active_any(min_healthy) and self._has_active_leaders(leader_min):
                    return

                now = time.time()
                if timeout is not None and now - start > timeout:
                    raise DaxClientError(
                        "Not enough routes after {}s: expected {}/{}, found {}/{} (healthy/leaders)".format(
                            timeout, min_healthy, leader_min, self._active_any(), self._active_leaders()),
                        DaxErrorCode.NoRoute)

                # Wait for a signal that the endpoints have changed
                self._route_change.wait(timeout)

    def _active_any(self):
        return sum(len(role_backend) for role, role_backend in self.routes.items())

    def _has_active_any(self, min_healthy):
        if min_healthy < 1:
            return True
        else:
            return self._active_any() >= min_healthy

    def _active_leaders(self):
        return len(self.routes[Role.LEADER])

    def _has_active_leaders(self, leader_min):
        if leader_min < 1:
            return True
        else:
            return self._active_leaders() >= leader_min

    def next_leader(self, prev_client):
        '''Return the client of the next leader backend, avoiding prev_client
        if possible. Falls back to any available backend if no leader route
        is currently active.
        '''
        with self._lock:
            if self.routes:
                route = self.selector(prev_client, list(self.leader_routes))
                if route:
                    return route.client
            return self.next_any(prev_client)

    def next_any(self, prev_client):
        '''Return the client of any backend, avoiding prev_client if possible.'''
        with self._lock:
            if self.routes:
                route = self.selector(prev_client, list(self.all_routes))
                if route:
                    return route.client
        return None

    @property
    def all_routes(self):
        return list(self._all_routes())

    def _all_routes(self):
        return itertools.chain.from_iterable(
            role_backends.values() for role_backends in self.routes.values()
        )

    @property
    def leader_routes(self):
        return list(self.routes[Role.LEADER].values())

    def add_route(self, backend):
        '''Add a backend to the active route table.'''
        with self._lock:
            checker = self._checkers.get(backend.addrport)
            if self.backends.get(backend.addrport) is not backend:
                return
            if checker and not checker.is_healthy():
                return

            already_present = bool(self.routes.get(backend.role, {}).get(backend.addrport))
            self.routes[backend.role][backend.addrport] = backend
            self._route_change.notify_all()
        if not already_present:
            logger.debug('Added route: %s', backend)

    def remove_route(self, backend):
        '''Remove the matching backend from the active route table.

        If the route is stale or already absent, this is a no-op.  When the
        removal drops active route count below the fail-open threshold, schedule
        an asynchronous rebuild from pingable backends.
        '''
        should_rebuild_healthy_routes = False
        with self._lock:
            current = self.routes.get(backend.role, {}).get(backend.addrport)
            if current is not backend:
                return
            self.routes.get(backend.role, {}).pop(backend.addrport, None)
            logger.debug('Removed 1 route: %s; routes left: %d', backend.addrport, len(self.all_routes))
            if len(self.all_routes) < self._active_routes_threshold:
                should_rebuild_healthy_routes = True
            self._route_change.notify_all()

        # Decouple rebuild healthy from request error
        if should_rebuild_healthy_routes:
            self._background.submit(self._rebuild_healthy_routes)

    def clear_routes(self):
        '''Reset the routing table, preserving leader-first ordering.'''
        logger.debug('Clearing %d route(s)...', sum([len(value) for value in self.routes.values()]))
        with self._lock:
            self.routes.clear()
            self.routes[Role.LEADER] = {}
            self.routes[Role.REPLICA] = {}

    def _rebuild_all_routes(self):
        '''Rebuild the routing table from all known backends, ignoring prior health state.

        Called at startup and on topology change.
        '''
        logger.debug('Rebuilding all routes')
        self.clear_routes()
        for addrport, backend in self.backends.items():
            checker = self._checkers.get(addrport)
            if checker:
                checker.reset_health_status()
            self.routes[backend.role][addrport] = backend
            logger.debug('Backend included in rebuild: %s', backend)
        self._route_change.notify_all()

    def _rebuild_healthy_routes(self):
        '''Rebuild the routing table from all known backends, given they are healthy.

        Called at the fail-open path.
        '''
        logger.debug('Rebuilding healthy routes')
        with self._lock:
            active = set(list(self.routes[Role.LEADER].keys()) + list(self.routes[Role.REPLICA].keys()))
            candidates = []
            for addrport, backend in self.backends.items():
                if addrport in active:
                    continue
                checker = self._checkers.get(addrport)
                if checker:
                    candidates.append((backend, checker))
                else:
                    logger.debug('Unresponsive backend excluded from rebuild: %s', backend)

        healthy = self._healthy_backends_from_ping_futures(candidates)
        if healthy:
            with self._lock:
                for backend, checker in healthy:
                    if (
                            self.backends.get(backend.addrport) is backend
                            and self._checkers.get(backend.addrport) is checker
                            and checker.is_healthy()
                    ):
                        self.routes[backend.role][backend.addrport] = backend
                self._route_change.notify_all()

    def _healthy_backends_from_ping_futures(self, candidates):
        '''Ping candidate backends concurrently and return only successful ones.'''
        ping_futures = {}
        for backend, checker in candidates:
            ping_futures[self._ping_background.submit(checker.ping)] = (backend, checker)

        done, not_done = future_wait(
            ping_futures.keys(),
            timeout=self.HEALTHY_ROUTE_REBUILD_TIMEOUT,
        )
        for future in not_done:
            future.cancel()

        healthy = []
        for future in done:
            backend, checker = ping_futures[future]
            try:
                if future.result():
                    checker.reset_health_status()
                    healthy.append((backend, checker))
                else:
                    logger.debug('Unresponsive backend excluded from rebuild: %s', backend)
            except Exception: # pylint: disable=broad-except
                logger.debug('Unresponsive backend excluded from rebuild: %s', backend, exc_info=True)

        return healthy


    def _deregister(self, addrport):
        '''Remove a backend's health checker from the cluster checker and local index.'''
        self._cluster_health_checker.deregister(addrport)
        self._checkers.pop(addrport, None)

    def _create_backend(self, service_endpoint):
        '''Instantiate a backend and its health checker, wire them together, and start.'''
        logger.debug('Creating backend for %s', service_endpoint)

        backend = BackendWithCB(service_endpoint)

        checker = EndpointHealthChecker(
            addrport=service_endpoint.addrport,
            fetch_client=backend.fetch_client,
            replace_client=backend.replace_client,
            on_healthy=functools.partial(self.add_route, backend),
            on_unhealthy=functools.partial(self.remove_route, backend),
            retry_delay=self._health_check_retry_delay,
            max_attempts=self._health_check_max_attempts,
        )

        # Build the fully-baked factory now that both backend and checker exist.
        # Operation callbacks are gated: only replicas affect health state
        # through the request-driven path.
        remove_route_on_failure = functools.partial(self.remove_route, backend)
        node_factory = functools.partial(
            self._client_factory,
            service_endpoint.hostname,
            service_endpoint.addrport,
            service_endpoint.ip_version,
            on_operation_success=lambda: checker.on_read_success() if not backend.leader else None,
            on_operation_failure=lambda: (
                checker.on_read_failure(remove_route_on_failure)
                if not backend.leader
                else None
            ),
        )

        checker.set_client_factory(node_factory)
        backend.set_client_factory(node_factory)

        backend.start()

        self._checkers[backend.addrport] = checker
        self._cluster_health_checker.register(
            backend.addrport,
            lambda is_closed: checker.check(is_closed),
            backend.is_closed,
        )
        return backend
