from .network_endpoint import NetworkEndpoint

from pydantic import BaseModel

class EndpointConnection(BaseModel):
    """
    The Endpoint Connection object contains information detailing a connection
    attempt to an endpoint.
    """

    # Recommended:
    code: int | None = None # A numerical response status code providing details about the connection.
    network_endpoint: NetworkEndpoint | None = None # Provides characteristics of the network endpoint.
