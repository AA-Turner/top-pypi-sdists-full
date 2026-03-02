from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_interface import NetworkInterface


class DHCPActivityActivityId(Enum):
    Discover: int = 1 # DHCPDISCOVER
    Offer: int = 2 # DHCPOFFER
    Request: int = 3 # DHCPREQUEST
    Decline: int = 4 # DHCPDECLINE
    Ack: int = 5 # DHCPACK
    Nak: int = 6 # DHCPNAK
    Release: int = 7 # DHCPRELEASE
    Inform: int = 8 # DHCPINFORM
    Expire: int = 9 # DHCPEXPIRE: A DHCP lease expired.

class DHCPActivity(Network):
    """
    DHCP Activity events report MAC to IP assignment via DHCP from a client or
    server.
    """

    class_uid: int = 4004
    class_name: str = 'DHCP Activity'

    activity_id: DHCPActivityActivityId

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The responder (server) of the DHCP connection.
    is_renewal: bool | None = None
    lease_dur: int | None = None
    src_endpoint: NetworkEndpoint | None = None # The initiator (client) of the DHCP connection.
    relay: NetworkInterface | None = None
    transaction_uid: str | None = None # The unique identifier of the transaction. This is typically a
                                       # random number generated from the client to associate a dhcp
                                       # request/response pair.
