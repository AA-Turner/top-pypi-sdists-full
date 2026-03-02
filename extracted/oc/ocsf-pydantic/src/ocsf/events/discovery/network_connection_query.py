from enum import Enum

from ocsf.events.discovery import DiscoveryResult

from ocsf.objects.network_connection_info import NetworkConnectionInformation
from ocsf.objects.process import Process


class NetworkConnectionQueryStateId(Enum):
    """
    The state of the socket.
    """
    Unknown: int = 0
    ESTABLISHED: int = 1
    SYN_SENT: int = 2
    SYN_RECV: int = 3
    FIN_WAIT1: int = 4
    FIN_WAIT2: int = 5
    TIME_WAIT: int = 6
    CLOSED: int = 7
    CLOSE_WAIT: int = 8
    LAST_ACK: int = 9
    LISTEN: int = 10
    CLOSIING: int = 11
    Other: int = 99


class NetworkConnectionQuery(DiscoveryResult):
    """
    Network Connection Query events report information about active network
    connections.
    """

    class_uid: int = 5012
    class_name: str = 'Network Connection Query'

    connection_info: NetworkConnectionInformation
    process: Process # The process that owns the socket.
    state_id: NetworkConnectionQueryStateId # The state of the socket.

    # Recommended:
    state: str | None = None # The state of the socket, normalized to the caption of the state_id
                             # value. In the case of 'Other', it is defined by the event source.
