from ocsf.events.base import BaseEvent, CategoryId

from ocsf.objects.network_connection_info import NetworkConnectionInformation
from ocsf.objects.network_endpoint import NetworkEndpoint, NetworkProxy
from ocsf.objects.network_traffic import NetworkTraffic
from ocsf.objects.tls import TLS


class Network(BaseEvent):
    """
    Network event is a generic event that defines a set of attributes available in
    the Network category.
    """

    category_uid: CategoryId = CategoryId.Network_Activity

    dst_endpoint: NetworkEndpoint # The responder (server) in a network connection.
    src_endpoint: NetworkEndpoint # The initiator (client) of the network connection.

    # Recommended:
    connection_info: NetworkConnectionInformation | None = None
    proxy: NetworkProxy | None = None
    traffic: NetworkTraffic | None = None

    # Optional:
    app_name: str | None = None
    tls: TLS | None = None
