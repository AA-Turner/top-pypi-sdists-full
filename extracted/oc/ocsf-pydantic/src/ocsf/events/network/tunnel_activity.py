from enum import Enum

from ocsf.events.network import Network

from ocsf.objects.device import Device
from ocsf.objects.network_connection_info import NetworkConnectionInformation
from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.network_interface import NetworkInterface
from ocsf.objects.network_traffic import NetworkTraffic
from ocsf.objects.user import User
from ocsf.objects.session import Session


class TunnelActivityActivityId(Enum):
    Unknown: int = 0 # The event activity is unknown.
    Open: int = 1 # Open a tunnel.
    Close: int = 2 # Close a tunnel.
    Renew: int = 3 # Renew a tunnel.
    Other: int = 99 # The event activity is not mapped.
    
class TunnelActivityTunnelTypeId(Enum):
    """
    The normalized tunnel type ID.
    """
    Unknown: int = 0
    Split_Tunnel: int = 1
    Full_Tunnel: int = 2
    Other: int = 99


class TunnelActivity(Network):
    """
    Tunnel Activity events report secure tunnel establishment (such as VPN),
    teardowns, renewals, and other network tunnel specific actions.
    """

    class_uid: int = 4014
    class_name: str = 'Tunnel Activity'

    activity_id: TunnelActivityActivityId

    # Recommended:
    dst_endpoint: NetworkEndpoint | None = None # The server responding to the tunnel connection.
    device: Device | None = None # The device that reported the event.
    src_endpoint: NetworkEndpoint | None = None # The initiator (client) of the tunnel connection.
    session: Session | None = None # The session associated with the tunnel.
    tunnel_interface: NetworkInterface | None = None # The information about the virtual tunnel
                                                     # interface, e.g. `utun0`. This is
                                                     # usually associated with the private (rfc-1918)
                                                     # ip of the tunnel.
    tunnel_type: str | None = None # The tunnel type. Example: `Split` or `Full`.
    tunnel_type_id: TunnelActivityTunnelTypeId | None = None # The normalized tunnel type ID.
    user: User | None = None # The user associated with the tunnel activity.

    # Optional:
    connection_info: NetworkConnectionInformation | None = None # The tunnel connection information.
    protocol_name: str | None = None # The networking protocol associated with the tunnel. E.g.
                                     # `IPSec`, `SSL`, `GRE`.
    traffic: NetworkTraffic | None = None # Traffic refers to the amount of data moving across the
                                          # tunnel at a given point of time. Ex: `bytes_in`
                                          # and `bytes_out`.
