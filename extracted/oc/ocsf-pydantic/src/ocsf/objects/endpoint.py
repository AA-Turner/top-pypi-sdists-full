from enum import Enum
from pydantic import IPvAnyAddress
from pydantic_extra_types.mac_address import MacAddress

from ._entity import Entity

from .user import User
from .agent import Agent
from .os import OperatingSystem
from .device_hw_info import DeviceHardwareInfo
from .location import GeoLocation
from .container import Container

class EndpointTypeId(Enum):
    """
    The endpoint type ID.
    """
    Server: int = 1
    Desktop: int = 2
    Laptop: int = 3
    Tablet: int = 4
    Mobile: int = 5
    Virtual: int = 6
    IOT: int = 7
    Browser: int = 8
    Firewall: int = 9
    Switch: int = 10
    Hub: int = 11

class Endpoint(Entity, Container):
    """
    The Endpoint object describes a physical or virtual device that connects to and
    exchanges information with a computer network. Some examples of endpoints are
    mobile devices, desktop computers, virtual machines, embedded devices, and
    servers. Internet-of-Things devices—like cameras, lighting, refrigerators,
    security systems, smart speakers, and thermostats—are also endpoints.
    """

    # Recommended:
    hostname: str | None = None # The fully qualified name of the endpoint.
    instance_uid: str | None = None
    interface_name: str | None = None
    interface_uid: str | None = None
    ip: IPvAnyAddress | None = None # The IP address of the endpoint, in either IPv4 or IPv6 format.
    owner: User | None = None # The identity of the service or user account that owns the endpoint or
                              # was last logged into it.
    type_id: EndpointTypeId | None = None # The endpoint type ID.

    # Optional:
    agent_list: list[Agent] | None = None
    domain: str | None = None
    hw_info: DeviceHardwareInfo | None = None
    location: GeoLocation | None = None # The geographical location of the endpoint.
    mac: MacAddress | None = None # The Media Access Control (MAC) address of the endpoint.
    name: str | None = None # The short name of the endpoint.
    os: OperatingSystem | None = None # The endpoint operating system.
    subnet_uid: str | None = None
    type: str | None = None # The endpoint type. For example: `unknown`,
                            # `server`, `desktop`, `laptop`,
                            # `tablet`, `mobile`, `virtual`,
                            # `browser`, or `other`.
    uid: str | None = None # The unique identifier of the endpoint.
    vlan_uid: str | None = None
    vpc_uid: str | None = None
    zone: str | None = None
