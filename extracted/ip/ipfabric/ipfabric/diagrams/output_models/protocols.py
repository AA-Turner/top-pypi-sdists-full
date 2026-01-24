import os
from typing import Union, Optional, Literal, Annotated

from pydantic import BaseModel, Field

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class Number(BaseModel, extra=PYDANTIC_EXTRAS):
    min: int
    max: int


class Numbers(BaseModel, extra=PYDANTIC_EXTRAS):
    """Possibly only for Internal Testing"""

    numbers: list[Number]


class Transport(BaseModel, extra=PYDANTIC_EXTRAS):
    src: Union[list[str], str]
    dst: Union[list[str], Numbers, str]


class TCP(Transport, BaseModel, extra=PYDANTIC_EXTRAS):
    flags: list[str]
    type: Literal["tcp"]


class UDP(Transport, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["udp"]


class ICMP(BaseModel, extra=PYDANTIC_EXTRAS):
    icmpCode: int
    icmpType: int
    type: Literal["icmp"]


class ICMPv6(ICMP, extra=PYDANTIC_EXTRAS):
    type: Literal["icmpv6"]


class MPLS(BaseModel, extra=PYDANTIC_EXTRAS):
    stack: list[int]
    type: Literal["mpls"]


class Ethernet(BaseModel, extra=PYDANTIC_EXTRAS):
    src: Optional[str] = None
    dst: Optional[str] = None
    etherType: str
    type: Literal["ethernet"]
    vlan: Optional[int] = None


class ESP(BaseModel, extra=PYDANTIC_EXTRAS):
    payload: str
    nextHeader: str
    type: Literal["esp"]


class IP(BaseModel, extra=PYDANTIC_EXTRAS):
    src: list[str]
    dst: list[str]
    fragmentOffset: Optional[int] = Field(None, alias="fragment offset")
    protocol: str
    ttl: Optional[int] = None
    type: Literal["ip"]


class IPv6(IP, extra=PYDANTIC_EXTRAS):
    hopLimit: int
    type: Literal["ipv6"]


class VXLAN(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["vxlan"]
    vni: int
    groupPolicyId: Optional[int] = None
    policyApplied: Optional[bool] = None


class CAPWAP(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["capwap"]


class GRE(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["gre"]
    protoType: Optional[str] = None


class FabricPath(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["fp"]
    dstSubswitchId: int
    dstSwitchId: int
    etherType: str
    srcSwitchId: int
    ttl: int


class VCMP(BaseModel, extra=PYDANTIC_EXTRAS):
    proto: str
    vrfName: str
    type: Literal["vcmp"]


PROTOCOLS = Annotated[
    Union[ICMP, ICMPv6, UDP, TCP, Ethernet, IP, IPv6, MPLS, ESP, VXLAN, CAPWAP, GRE, FabricPath, VCMP],
    Field(discriminator="type"),
]
