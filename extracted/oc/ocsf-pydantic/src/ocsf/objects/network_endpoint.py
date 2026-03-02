from pydantic.networks import IPvAnyAddress

from .autonomous_system import AutonomousSystem
from .endpoint import Endpoint, EndpointTypeId

class NetworkEndpoint(Endpoint):
    """
    The Network Endpoint object describes characteristics of a network endpoint.
    These can be a source or destination of a network connection.
    """

    # Recommended:
    port: int | None = None # The port used for communication within the network connection.
    svc_name: str | None = None

    # Optional:
    autonomous_system: AutonomousSystem | None = None
    intermediate_ips: list[IPvAnyAddress] | None = None
    proxy_endpoint: 'NetworkProxy | None' = None # The network proxy information pertaining to a specific
                                               # endpoint. This can be used to describe information
                                               # pertaining to network address translation (NAT).
    type: str | None = None # The network endpoint type. For example: `unknown`,
                            # `server`, `desktop`, `laptop`,
                            # `tablet`, `mobile`, `virtual`,
                            # `browser`, or `other`.
    type_id: EndpointTypeId | None = None # The network endpoint type ID.

class NetworkProxy(NetworkEndpoint):
    pass
