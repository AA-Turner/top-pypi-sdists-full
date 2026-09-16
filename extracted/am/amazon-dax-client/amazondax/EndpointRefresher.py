import logging
import random
import socket
from collections import namedtuple

from .Assemblers import ENDPOINT_FIELDS
from .ClusterUtil import periodic_task
from .Constants import IpDiscovery
from .DaxError import DaxClientError, DaxErrorCode, DaxServiceError, DaxValidationError


logger = logging.getLogger(__name__)

_ServiceEndpoint = namedtuple('_ServiceEndpoint', ENDPOINT_FIELDS)
AddrPort = namedtuple('AddrPort', ('address', 'port'))


class ServiceEndpoint(_ServiceEndpoint):
    @classmethod
    def from_endpoint(cls, endpoint):
        # Set the hostname to the address if none provided
        if 'hostname' in endpoint:
            if 'address' not in endpoint:
                # No address, so go ask DNS
                addresses = _resolve_dns(endpoint['hostname'], endpoint['port'])
                # Filter addresses by endpoint address ip version
                addresses = [addr for addr in addresses if addr[2] == endpoint.get('ip_version')]
                if addresses:
                    # If multiple addresses, pick one
                    endpoint['address'] = random.choice(addresses)[0]
                else:
                    # Could not resolve hostname, bad endpoint, ignore it
                    return None
        else:
            if endpoint.setdefault('hostname', endpoint.get('address')) is None:
                # No hostname or address, go to the next endpoint
                return None

        endpoint.setdefault('leader_session_id', 0)

        return cls(**endpoint)

    @classmethod
    def from_endpoints(cls, endpoints):
        ''' Create a frozenset of ServiceEndpoint objects from a list of endpoints.

        Endpoints without valid addresses are dropped.
        '''
        service_endpoints = [cls.from_endpoint(endpoint) for endpoint in endpoints]
        return frozenset(service_endpoint for service_endpoint in service_endpoints if service_endpoint is not None)

    @property
    def addrport(self):
        try:
            return self._addrport
        except AttributeError:
            self._addrport = AddrPort(self.address, self.port) # pylint: disable=attribute-defined-outside-init
            return self._addrport


class EndpointRefresher:
    '''Bootstraps and periodically refreshes the cluster's service endpoints.

    The first bootstrap runs synchronously from start().  Subsequent bootstraps
    are driven by a PeriodicTask and call on_endpoints only when discovery
    returns a non-empty endpoint set.

    Constructor parameters
    ----------------------
    client_factory        — callable(hostname, sockaddr, ip_version) -> client.
    discovery_endpoints   — list of (scheme, host, port) discovery endpoints.
    update_interval       — seconds between background refreshes.
    ip_discovery          — IpDiscoveryValues constant or None.
    on_endpoints          — callable(frozenset[ServiceEndpoint]).
    make_endpoints        — callable(list[dict]) -> frozenset[ServiceEndpoint].

    '''

    def __init__(
            self,
            client_factory,
            discovery_endpoints,
            update_interval,
            ip_discovery,
            on_endpoints,
            make_endpoints=ServiceEndpoint.from_endpoints,
    ):
        # _client_factory: callable(hostname, addrport, ip_version, **kwargs) -> client
        self._client_factory = client_factory
        self._discovery_endpoints = discovery_endpoints
        self._update_interval = update_interval
        self._ip_discovery = ip_discovery
        self._make_endpoints = make_endpoints
        self._on_endpoints = on_endpoints
        self._task = None

    def start(self):
        '''Set up the initial roster, then schedule periodic background refreshes.'''
        try:
            service_endpoints = self._bootstrap()
        except DaxValidationError as e:
            logger.info('Could not start bootstrap due to DaxValidationError: %s', e)
            raise

        if not service_endpoints:
            raise DaxClientError(
                'Failed to configure cluster endpoints from {}'.format(self._discovery_endpoints),
                DaxErrorCode.NoRoute,
            )

        self._task = periodic_task(
            self._bootstrap_async, self._update_interval, jitter=0.5,
        )

    def close(self):
        '''Cancel the background refresh task.'''
        if self._task:
            self._task.cancel()
            self._task = None

    def _bootstrap_async(self):
        '''Non-throwing bootstrap, for calling from a background thread.'''
        try:
            self._bootstrap()
        except Exception:
            logger.warning('Failed to boostrap endpoints', exc_info=True)

    def _bootstrap(self):
        service_endpoints = self._bootstrap_endpoints()
        logger.debug('Bootstrapped endpoints: {}'.format(service_endpoints))
        if service_endpoints:
            self._on_endpoints(service_endpoints)

        return service_endpoints

    def _bootstrap_endpoints(self):
        logger.debug("Bootstrapping from discovery endpoints %s", self._discovery_endpoints)
        seeds = []
        endpoint_scheme = None
        for scheme, host, port in self._discovery_endpoints:
            seeds_from_endpoint = _resolve_dns(host, port)
            logger.debug('Resolved addresses %s for %s', seeds_from_endpoint, host)
            seeds.extend(seeds_from_endpoint)
            endpoint_scheme = scheme

        seeds = _filter_seeds_by_ip_discovery(seeds, self._ip_discovery)
        random.shuffle(seeds)
        logger.debug('seeds: %s', seeds)
        service_endpoints = self._get_endpoints_from_seeds(endpoint_scheme, seeds)
        logger.debug('service_endpoints: %s', service_endpoints)

        if service_endpoints:
            return service_endpoints

        return None

    def _get_endpoints_from_seeds(self, scheme, seeds):
        for hostname, sockaddr, ip_version in seeds:
            ip, port = sockaddr
            try:
                client = self._client_factory(hostname, sockaddr, ip_version)
            except Exception: # pylint: disable=broad-except
                logger.info(
                    'Could not connect to %s://%s:%s', scheme, ip, port, exc_info=True,
                )
                continue
            try:
                endpoints = client.endpoints()

                # Restore the DNS domain name of the discovery endpoint,
                # for certificate validation.
                for endpoint in endpoints:
                    endpoint['hostname'] = hostname
            except DaxServiceError as e:
                if e.auth_error:
                    logger.warning('Auth exception while starting up cluster client: %s', e)
                    raise
            except DaxValidationError:
                raise
            except Exception: # pylint: disable=broad-except
                logger.info(
                    'Failed to retrieve endpoints from %s://%s:%s', scheme, ip, port, exc_info=True,
                )
                continue
            else:
                if endpoints:
                    return self._make_endpoints(endpoints)
            finally:
                client.close()

        return None


def _resolve_dns(host, port):
    '''Resolve a hostname to a list of (host, (ip, port), ip_version) tuples. Returns [] on failure.'''
    try:
        return [
            (host, sockaddr[:2], ip_version)
            for ip_version, _socktype, _proto, _canonname, sockaddr
            in socket.getaddrinfo(host, port, socket.AF_UNSPEC, 0, socket.IPPROTO_TCP)
        ]
    except socket.gaierror:
        return []


def _filter_seeds_by_ip_discovery(seeds, ip_discovery=IpDiscovery.NONE.value):
    '''Filters a list of seeds (host, socket address and ip version)
    based on the desired ip_discovery.
    Below the behavior:
        1. The method splits the initial list based on Ip version.
        2. If both IPv4 and IPv6 lists exist, we have dual stack, if not, single stack.
        3. If single stack and stack type does not match ip discovery, raises error.
        4. If ip discovery matches stack type, returns the IPs.
        5. If ip discovery is not provided, IPv4 is preferred for dual stack and IPv4 stack,
        IPv6 is preferred for IPv6 stack.

    :raise DaxValidationError: if mismatch between discovered IP stack and provided
        ip discovery.
    :param seeds: List of seeds
    :param ip_discovery: Desired ip version.
    :return: Filtered list of seeds.
    '''
    ipv4_seeds = []
    ipv6_seeds = []
    for seed in seeds:
        if seed[2] == socket.AF_INET:
            ipv4_seeds.append(seed)
        elif seed[2] == socket.AF_INET6:
            ipv6_seeds.append(seed)

    if ip_discovery is None:
        return ipv4_seeds or ipv6_seeds

    if ip_discovery == IpDiscovery.IPV4.value:
        if not ipv4_seeds and ipv6_seeds:
            raise DaxValidationError(
                "ip_discovery does not match the SupportedNetworkType. "
                "ip_discovery: {}, SupportedNetworkType: {}.".format(
                    ip_discovery, IpDiscovery.IPV6.value
                )
            )
        return ipv4_seeds

    if ip_discovery == IpDiscovery.IPV6.value:
        if ipv4_seeds and not ipv6_seeds:
            raise DaxValidationError(
                "ip_discovery does not match the SupportedNetworkType. "
                "ip_discovery: {}, SupportedNetworkType: {}.".format(
                    ip_discovery, IpDiscovery.IPV4.value
                )
            )
        return ipv6_seeds

    return []
