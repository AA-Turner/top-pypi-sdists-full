from ._entity import Entity

from .endpoint_connection import EndpointConnection
from .metric import Metric
from .network_endpoint import NetworkEndpoint


class LoadBalancer(Entity):
    """
    The load balancer object describes the load balancer entity and contains
    additional information regarding the distribution of traffic across a network.
    """

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The destination to which the load balancer is
                                                # distributing traffic.
    code: int | None = None # The numeric response status code detailing the connection from the load
                            # balancer to the destination target.
    endpoint_connections: list[EndpointConnection] | None = None # An object detailing the load
                                                                 # balancer connection attempts and
                                                                 # responses.

    # Optional:
    metrics: list[Metric] | None = None # General purpose metrics associated with the load balancer.
    classification: str | None = None # The request classification as defined by the load balancer.
    status_detail: str | None = None # The status detail contains additional status information about
                                     # the load balancer distribution event.
    error_message: str | None = None # The load balancer error message.
    message: str | None = None # The load balancer message.
    name: str | None = None # The name of the load balancer.
    uid: str | None = None # The unique identifier for the load balancer.
