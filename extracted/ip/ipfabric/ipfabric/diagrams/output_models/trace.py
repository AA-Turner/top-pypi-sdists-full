import os
from typing import Optional, Union, Literal, Annotated

from pydantic import BaseModel, Field

from .protocols import PROTOCOLS

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class SeverityInfo(BaseModel, extra=PYDANTIC_EXTRAS):
    name: str
    severity: int
    topic: str
    details: Optional[list[str]] = Field(default_factory=list)


class ValueMatch(BaseModel, extra=PYDANTIC_EXTRAS):
    value: Union[str, list[str], None]


class PacketDataMatch(ValueMatch, BaseModel, extra=PYDANTIC_EXTRAS):
    field: str
    type: Literal["packet data match"]


class RouteDetail(ValueMatch, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["route detail"]


class RemoveHeader(BaseModel, extra=PYDANTIC_EXTRAS):
    index: int
    headerType: str
    type: Literal["remove header"]
    reason: Optional[str] = None
    tunnelDstIp: Optional[str] = None


class Filter(BaseModel, extra=PYDANTIC_EXTRAS):
    label: Optional[int] = None
    mask: Optional[int] = None
    vrf: Optional[str] = None
    prefix: Optional[str] = None
    ip: Optional[Union[str, list[str]]] = None
    groupIp: Optional[str] = None
    sourceIp: Optional[str] = None
    inIfaceName: Optional[str] = None
    mac: Optional[str] = None
    vlanNum: Optional[int] = None
    name: Optional[str] = None
    port: Optional[str] = None
    network: Optional[str] = None
    vrfVxlanId: Optional[int] = None


class TableEntry(BaseModel, extra=PYDANTIC_EXTRAS):
    filter: Filter
    table: str


class TableEntryMatch(TableEntry, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["table entry match"]


class TableEntryNotFound(TableEntry, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["table entry not found"]


class InsertHeader(BaseModel, extra=PYDANTIC_EXTRAS):
    header: PROTOCOLS
    headerType: str
    index: int
    type: Literal["insert header"]


class Patch(BaseModel, extra=PYDANTIC_EXTRAS):
    stack: Optional[list[int]] = None
    ttl: Optional[int] = None
    dst: Optional[Union[str, list[str]]] = None
    policyApplied: Optional[bool] = None


class PatchHeader(BaseModel, extra=PYDANTIC_EXTRAS):
    patch: Patch
    index: int
    type: Literal["patch header"]
    headerType: Optional[str] = None


class DropPacket(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["drop packet"]
    reason: str
    severityInfo: Optional[SeverityInfo] = None
    ips: Optional[list[str]] = None
    groupIp: Optional[list[str]] = None
    sourceIp: Optional[list[str]] = None


class SeverityEvent(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["severity event"]
    severityInfo: Optional[SeverityInfo] = None


class BaseEvent(BaseModel, extra=PYDANTIC_EXTRAS):
    decidingPolicyName: Optional[str] = None
    decidingRule: Optional[list[int]] = None
    protocolId: str
    securityType: str
    severityInfo: Optional[SeverityInfo] = None


class SecurityCheck(BaseEvent, extra=PYDANTIC_EXTRAS):
    type: Literal["security check"]
    isInvisible: Optional[bool] = None
    isDefaultRule: Optional[bool] = None
    allHidden: Optional[bool] = None


class SecurityCheckIgnored(SecurityCheck, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["security check ignored"]


class VirtualRouting(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["virtual routing"]
    ifaceName: str


class AcceptPacket(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["accept packet"]


class DestinationNAT(BaseEvent, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["destination NAT"]
    field: Optional[str] = None


class SourceNAT(BaseEvent, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["source NAT"]
    field: Optional[str] = None


class PolicyBasedRouting(BaseEvent, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["policy based routing"]
    field: Optional[str] = None


class FloodPacket(SeverityEvent, BaseModel, extra=PYDANTIC_EXTRAS):
    type: Literal["flood packet"]
    reason: str


EVENT = Annotated[
    Union[
        PacketDataMatch,
        RemoveHeader,
        TableEntryMatch,
        TableEntryNotFound,
        VirtualRouting,
        AcceptPacket,
        InsertHeader,
        PatchHeader,
        DropPacket,
        SeverityEvent,
        SecurityCheckIgnored,
        SecurityCheck,
        DestinationNAT,
        PolicyBasedRouting,
        SourceNAT,
        FloodPacket,
        RouteDetail,
    ],
    Field(discriminator="type"),
]


class Trace(BaseModel, extra=PYDANTIC_EXTRAS):
    chain: str
    phase: str
    events: list[EVENT]
