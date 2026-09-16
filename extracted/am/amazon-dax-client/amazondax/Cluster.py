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
import logging
from urllib.parse import urlparse

from .DaxClient import DaxClient
from .DaxError import DaxClientError, DaxErrorCode, DaxValidationError
from .EndpointRefresher import EndpointRefresher
from .Tube import SocketTubePool
from .router.RouterWithCB import RouterWithCB


logger = logging.getLogger(__name__)

SCHEMES_TO_DEFAULT_PORTS = {'dax': 8111, 'daxs': 9111}


class ClusterDefaults:
    # All time intervals are in seconds to match time.time.
    CLUSTER_UPDATE_INTERVAL = 4.0
    HEALTH_CHECK_INTERVAL = 5.0
    IDLE_CONNECTION_REAP_DELAY = 30.0
    HEALTH_CHECK_RETRY_DELAY = 0.5
    # Attempts for the node health check mechanism, including the first attempt.
    HEALTH_CHECK_MAX_ATTEMPTS = 3


class Cluster(ClusterDefaults):
    '''
    Manages DAX cluster discovery, routing, and client creation.

    Topology discovery is delegated to EndpointRefresher.
    '''
    def __init__(self, region_name, discovery_endpoints, credentials, user_agent=None, user_agent_extra=None, connect_timeout=None,
                 read_timeout=None, skip_hostname_verification=None, router_factory=None, client_factory=None, ip_discovery=None):
        self._region_name = region_name
        self._discovery_endpoints = [_parse_host_ports(endpoint) for endpoint in discovery_endpoints]
        self._credentials = credentials
        self._user_agent = user_agent
        self._user_agent_extra = user_agent_extra
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._skip_hostname_verification = skip_hostname_verification
        self._ip_discovery = ip_discovery

        self._router_factory = router_factory or RouterWithCB

        self._closed = False

        self._cluster_update_interval = self.CLUSTER_UPDATE_INTERVAL
        self._health_check_interval = self.HEALTH_CHECK_INTERVAL
        self._idle_connection_reap_delay = self.IDLE_CONNECTION_REAP_DELAY

        # _client_factory: callable(scheme, hostname, addrport, ip_version, **kwargs) -> client
        self._client_factory = client_factory or self._new_client

        if len({scheme for scheme, _, _ in self._discovery_endpoints}) > 1:
            raise DaxValidationError('All endpoints must have the same scheme')
        scheme = self._discovery_endpoints[0][0]

        self._router = self._router_factory(
            client_factory=functools.partial(self._client_factory, scheme),
            health_check_interval=self._health_check_interval,
            health_check_retry_delay=self.HEALTH_CHECK_RETRY_DELAY,
            health_check_max_attempts=self.HEALTH_CHECK_MAX_ATTEMPTS,
        )

        self._refresher = EndpointRefresher(
            client_factory=functools.partial(self._client_factory, scheme),
            discovery_endpoints=self._discovery_endpoints,
            update_interval=self._cluster_update_interval,
            ip_discovery=ip_discovery,
            on_endpoints=self._router.update,
        )

    def start(self, min_healthy=1):
        '''Start the refresher'''
        try:
            self._refresher.start()
            self._router.start()
            self.wait_for_routes(min_healthy=min_healthy, leader_min=1, timeout=self._connect_timeout)
        except Exception:
            self.close()
            raise

    def close(self):
        if self._closed:
            return

        self._closed = True

        try:
            self._refresher.close()
        except Exception: # pylint: disable=broad-except
            logger.warning('Failed closing endpoint refresher', exc_info=True)
        finally:
            self._refresher = None

        try:
            self._router.close()
        except Exception: # pylint: disable=broad-except
            logger.warning('Failed closing router', exc_info=True)
        finally:
            self._router = None

    def read_client(self, prev_client=None):
        ''' Return a read client.

        Caller should not close the client.
        '''
        client = self._router.next_any(prev_client)
        if client is None:
            raise DaxClientError("No cluster endpoints available", DaxErrorCode.NoRoute)

        return client

    def write_client(self, prev_client=None):
        ''' Return a write client.

        Caller should not close the client.
        '''
        client = self._router.next_leader(prev_client)
        if client is None:
            raise DaxClientError("No cluster endpoints available", DaxErrorCode.NoRoute)

        return client

    def wait_for_routes(self, min_healthy=1, leader_min=1, timeout=None):
        return self._router.wait_for_routes(min_healthy=min_healthy, leader_min=leader_min, timeout=timeout)

    def _new_client(self, scheme, hostname, sockaddr, ip_version,
                    on_operation_success=None, on_operation_failure=None):
        ''' Create a new client.

        Caller is responsible for closing the client.
        '''
        tube_pool = SocketTubePool(
            scheme, hostname, sockaddr, ip_version,
            lambda: self._credentials,
            self._region_name,
            self._user_agent,
            self._user_agent_extra,
            self._connect_timeout,
            self._read_timeout,
            self._skip_hostname_verification,
        )
        return DaxClient(
            tube_pool,
            on_operation_success=on_operation_success,
            on_operation_failure=on_operation_failure,
        )

def _parse_host_ports(endpoint):
    # We accept endpoints in the form hostname:port. We also call these
    # endpoint_urls, although that is not a valid URL (the part before the
    # colon should be the scheme. Deal with that here by turning a non-URL
    # endpoint into a URL. Assume that the non-URL form represents a
    # non-encrypted URL.
    parts = urlparse(endpoint if '://' in endpoint else 'dax://' + endpoint)
    if parts.scheme not in SCHEMES_TO_DEFAULT_PORTS.keys():
        raise DaxValidationError('URL scheme must be one of {}'.format(
            ', '.join(SCHEMES_TO_DEFAULT_PORTS.keys())))

    netloc_parts = parts.netloc.split(':', 1)
    if len(netloc_parts) == 1:
        return parts.scheme, netloc_parts[0].strip(), SCHEMES_TO_DEFAULT_PORTS[parts.scheme]
    else:
        return parts.scheme, netloc_parts[0].strip(), int(netloc_parts[1].strip())
