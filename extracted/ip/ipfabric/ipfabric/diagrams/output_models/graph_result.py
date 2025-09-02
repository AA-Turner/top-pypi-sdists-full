import os
from typing import Optional, List, Union
from uuid import UUID

from pydantic import BaseModel, Field

from .protocols import PROTOCOLS
from .trace import Trace
from ..input_models import NetworkSettings, PathLookupSettings

PYDANTIC_EXTRAS = os.getenv("IPFABRIC_PYDANTIC_EXTRAS", "allow")


class Extra(BaseModel, extra=PYDANTIC_EXTRAS):
    ip: Optional[str] = None


class Line(BaseModel, extra=PYDANTIC_EXTRAS):
    pattern: Optional[str] = None
    color: Optional[int] = None
    thickness: Optional[int] = None


class Style(BaseModel, extra=PYDANTIC_EXTRAS):
    background: Optional[str] = None
    line: Optional[Line] = None


class Position(BaseModel, extra=PYDANTIC_EXTRAS):
    x: Union[int, float]
    y: Union[int, float]


class EdgePosition(BaseModel, extra=PYDANTIC_EXTRAS):
    c: Position
    e: Position


class Label(BaseModel, extra=PYDANTIC_EXTRAS):
    type: Optional[str] = None
    visible: Optional[bool] = None
    text: Optional[str] = None
    angle: Optional[int] = None
    anchor: Optional[Position] = None
    position: Optional[Position] = None
    wrapText: Optional[bool] = None


class Labels(BaseModel, extra=PYDANTIC_EXTRAS):
    center: Optional[Union[list[Label], Label]] = None
    source: Optional[Union[list[Label], Label]] = None
    target: Optional[Union[list[Label], Label]] = None


class ArrowHeads(BaseModel, extra=PYDANTIC_EXTRAS):
    target: Optional[list[Position]] = Field(default_factory=list)
    source: Optional[list[Position]] = Field(default_factory=list)


class Positions(BaseModel, extra=PYDANTIC_EXTRAS):
    line: Optional[list[Union[Position, EdgePosition]]] = Field(default_factory=list)
    arrowHeads: Optional[ArrowHeads] = None
    labels: Optional[Labels] = None


class Checks(BaseModel, extra=PYDANTIC_EXTRAS):
    green: int = Field(alias="0")
    blue: int = Field(alias="10")
    amber: int = Field(alias="20")
    red: int = Field(alias="30")


class Severity(Checks, extra=PYDANTIC_EXTRAS):
    pass


class Topics(BaseModel, extra=PYDANTIC_EXTRAS):
    acl: Checks = Field(alias="ACL")
    forwarding: Checks = Field(alias="FORWARDING")
    zonefw: Checks = Field(alias="ZONEFW")
    nat44: Optional[Checks] = Field(None, alias="NAT44")
    pbr: Optional[Checks] = Field(None, alias="PBR")


class TrafficScore(BaseModel, extra=PYDANTIC_EXTRAS):
    accepted: int
    dropped: int
    forwarded: int
    total: int


class Packets(BaseModel, extra=PYDANTIC_EXTRAS):
    packet: Optional[list[PROTOCOLS]] = Field(default_factory=list)
    ifaceName: Optional[str] = None
    prevEdgeIds: Optional[list[str]] = Field(default_factory=list)
    nextEdgeIds: Optional[list[str]] = Field(default_factory=list)
    severityInfo: Optional[Checks] = None
    trafficScore: Optional[TrafficScore] = None


class Node(BaseModel, extra=PYDANTIC_EXTRAS):
    path: Optional[str] = None
    boxId: Optional[str] = None
    children: List
    graphType: str
    id: str
    label: str
    parentPath: Optional[str] = None
    sn: str
    type: str
    stack: Optional[bool] = None
    position: Optional[Position] = None
    style: Optional[Style] = None
    acceptedPackets: Optional[dict[str, Packets]] = Field(default_factory=dict)
    droppedPackets: Optional[dict[str, Packets]] = Field(default_factory=dict)
    generatedPackets: Optional[dict[str, Packets]] = Field(default_factory=dict)
    extra: Optional[Extra] = None


class Edge(BaseModel, extra=PYDANTIC_EXTRAS):
    direction: str
    source: str
    target: str
    edgeSettingsId: UUID
    id: str
    labels: Labels
    protocol: Optional[str] = ""
    shift: Optional[Union[int, float]] = None
    positions: Optional[Positions] = None
    style: Optional[Style] = None


class RelatedTechnology(BaseModel, extra=PYDANTIC_EXTRAS):
    vlanId: int
    rootId: str


class NetworkEdge(Edge, BaseModel, extra=PYDANTIC_EXTRAS):
    circle: bool
    children: list[str]
    relatedTechnology: Optional[RelatedTechnology] = None


class PathLookupEdge(Edge, BaseModel, extra=PYDANTIC_EXTRAS):
    nextEdgeIds: list[str]
    prevEdgeIds: list[str]
    packet: list[PROTOCOLS]
    severityInfo: Severity
    sourceIfaceName: Optional[str] = None
    targetIfaceName: Optional[str] = None
    trafficScore: TrafficScore
    nextEdge: Optional[list] = Field(default_factory=list)
    prevEdge: Optional[list] = Field(default_factory=list)
    loopIds: Optional[list[int]] = Field(default_factory=list)


class EventsSummary(BaseModel, extra=PYDANTIC_EXTRAS):
    flags: list
    topics: Topics
    global_list: list = Field(alias="global")


class Traces(BaseModel, extra=PYDANTIC_EXTRAS):
    severityInfo: Checks
    sourcePacketId: str
    targetPacketId: str
    trace: list[Trace]


class Decision(BaseModel, extra=PYDANTIC_EXTRAS):
    traces: list[Traces]
    trafficIn: Optional[dict[str, list[str]]] = Field(default_factory=dict)
    trafficOut: Optional[dict[str, list[str]]] = Field(default_factory=dict)


class Check(BaseModel, extra=PYDANTIC_EXTRAS):
    exists: bool


class PathLookup(BaseModel, extra=PYDANTIC_EXTRAS):
    eventsSummary: EventsSummary
    decisions: dict[str, Decision]
    passingTraffic: str
    check: Check


class GraphData(BaseModel, extra=PYDANTIC_EXTRAS):
    nodes: dict[str, Node]
    edges: dict[str, Union[NetworkEdge, PathLookupEdge]]


class Entities(BaseModel, extra=PYDANTIC_EXTRAS):
    deviceTypes: list[str]
    edgeSettingsIds: list[str]


class Path(BaseModel, extra=PYDANTIC_EXTRAS):
    defaultLayout: str
    layoutAlgorithm: str


class Topology(BaseModel, extra=PYDANTIC_EXTRAS):
    availableEntities: Entities
    allPathsSelected: bool
    paths: dict[str, Path]


class GraphResult(BaseModel, extra=PYDANTIC_EXTRAS):
    boxLabels: dict[str, str]
    graphData: GraphData
    settings: Union[NetworkSettings, PathLookupSettings]


class BaseResult(BaseModel, extra=PYDANTIC_EXTRAS):
    graphResult: GraphResult

    @property
    def nodes(self) -> dict[str, Node]:
        return self.graphResult.graphData.nodes


class TopologyResult(BaseResult, BaseModel, extra=PYDANTIC_EXTRAS):
    topology: Topology

    @property
    def edges(self) -> dict[str, NetworkEdge]:
        return self.graphResult.graphData.edges


class PathLookupResult(BaseResult, BaseModel, extra=PYDANTIC_EXTRAS):
    pathlookup: Optional[PathLookup] = None

    @property
    def edges(self) -> dict[str, PathLookupEdge]:
        return self.graphResult.graphData.edges
