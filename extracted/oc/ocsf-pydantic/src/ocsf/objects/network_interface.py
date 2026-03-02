from enum import Enum

from pydantic import IPvAnyAddress
from pydantic_extra_types.mac_address import MacAddress

from ._entity import Entity

class NetworkInterfaceTypeId(Enum):
    """
    The network interface type identifier.
    """
    Unknown: int = 0
    Wired: int = 1
    Wireless: int = 2
    Mobile: int = 3
    Tunnel: int = 4
    Other: int = 99

class NetworkInterface(Entity):
    """
    The Network Interface object describes the type and associated attributes of a
    network interface.
    """

    type_id: NetworkInterfaceTypeId # The network interface type identifier.

    # Recommended:
    hostname: str | None = None # The hostname associated with the network interface.
    ip: IPvAnyAddress | None = None # The IP address associated with the network interface.
    mac: MacAddress | None = None # The MAC address of the network interface.

    # Optional:
    name: str | None = None # The name of the network interface.
    namespace: str | None = None
    subnet_prefix: int | None = None
    type: str | None = None # The type of network interface.
    uid: str | None = None # The unique identifier for the network interface.
