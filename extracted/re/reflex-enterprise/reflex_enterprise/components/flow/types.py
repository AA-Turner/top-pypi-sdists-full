"""Flow component for managing the flow of data between nodes."""

from typing import TYPE_CHECKING, Any, Literal, Mapping, Sequence, TypedDict

import reflex
from reflex.components.el.elements.base import AriaRole
from typing_extensions import NotRequired


class XYPosition(TypedDict):
    """All positions are stored in an object with x and y coordinates."""

    x: float
    y: float


class ProOptions(TypedDict):
    """By default, we render a small attribution in the corner of your flows that links back to the project.

    Anyone is free to remove this attribution whether they’re a Pro subscriber or not but we ask that you take a quick look at our removing attribution guide before doing so.
    """

    account: NotRequired[str]
    hideAttribution: bool


PanelPosition = Literal[
    "top-left",
    "top-center",
    "top-right",
    "bottom-left",
    "bottom-center",
    "bottom-right",
]

AriaLabelConfig = TypedDict(
    "AriaLabelConfig",
    {
        "node.a11yDescription.default": NotRequired[str],
        "node.a11yDescription.keyboardDisabled": NotRequired[str],
        "node.a11yDescription.ariaLiveMessage": NotRequired[Any],
        "edge.a11yDescription.default": NotRequired[str],
        "controls.ariaLabel": NotRequired[str],
        "controls.zoomIn.ariaLabel": NotRequired[str],
        "controls.zoomOut.ariaLabel": NotRequired[str],
        "controls.fitView.ariaLabel": NotRequired[str],
        "controls.interactive.ariaLabel": NotRequired[str],
        "minimap.ariaLabel": NotRequired[str],
        "handle.ariaLabel": NotRequired[str],
    },
)

SnapGrid = tuple[float, float]

Position = Literal["top", "right", "bottom", "left"]

CoordinateExtent = tuple[tuple[float, float], tuple[float, float]]

NodeOrigin = tuple[float, float]

HandleType = Literal["source", "target"]

ColorMode = Literal["light", "dark", "system"]


class Viewport(TypedDict):
    """Internally, React Flow maintains a coordinate system that is independent of the rest of the page.

    The Viewport type tells you where in that system your flow is currently being display at and how zoomed in or out it is.
    """

    x: float
    y: float
    zoom: float


class Rect(TypedDict):
    """The Rect type defines a rectangle in a two-dimensional space with dimensions and a position."""

    x: float
    y: float
    width: float
    height: float


class NodeHandle(TypedDict):
    """The NodeHandle type is used to define a handle for a node if server-side rendering is used.

    On the server, React Flow can’t measure DOM nodes, so it’s necessary to define the handle position dimensions.
    """

    width: NotRequired[float]
    height: NotRequired[float]
    id: NotRequired[str | None]
    x: float
    y: float
    pos: Position
    type: HandleType


class Measured(TypedDict):
    """Represents the measured dimensions of a node."""

    width: NotRequired[float]
    height: NotRequired[float]


NodeType = Literal["default", "input", "output", "group"]


class Id(TypedDict):
    """Represents a unique identifier for a node."""

    id: str


class Padding(TypedDict):
    """Represents the padding values for a node."""

    top: NotRequired[float]
    right: NotRequired[float]
    bottom: NotRequired[float]
    left: NotRequired[float]
    x: NotRequired[float]
    y: NotRequired[float]


class Node(TypedDict):
    """The Node type represents everything React Flow needs to know about a given node.

    Many of these properties can be manipulated both by React Flow or by you, but some such as width and height should be considered read-only.
    """

    id: str
    """Unique id of a node."""

    position: XYPosition
    """Position of a node on the pane."""

    data: NotRequired[dict[str, Any]]
    """Arbitrary data passed to a node."""

    sourcePosition: NotRequired[Position]
    """Only relevant for default, source, target nodeType. Controls source position."""

    targetPosition: NotRequired[Position]
    """Only relevant for default, source, target nodeType. Controls target position."""

    hidden: NotRequired[bool]
    """Whether or not the node should be visible on the canvas."""

    selected: NotRequired[bool]

    dragging: NotRequired[bool]
    """Whether or not the node is currently being dragged."""

    draggable: NotRequired[bool]
    """Whether or not the node is able to be dragged."""

    selectable: NotRequired[bool]

    connectable: NotRequired[bool]

    deletable: NotRequired[bool]

    dragHandle: NotRequired[str]
    """A class name that can be applied to elements inside the node that allows those elements to act as drag handles, letting the user drag the node by clicking and dragging on those elements."""

    width: NotRequired[float]

    height: NotRequired[float]

    initialWidth: NotRequired[float]

    initialHeight: NotRequired[float]

    parentId: NotRequired[str]
    """Parent node id, used for creating sub-flows."""

    zIndex: NotRequired[int]
    """The z-index of the node."""

    extent: NotRequired[CoordinateExtent | Literal["parent"]]
    """The boundary a node can be moved in."""

    expandParent: NotRequired[bool]
    """When true, the parent node will automatically expand if this node is dragged to the edge of the parent node’s bounds."""

    ariaLabel: NotRequired[str]
    """Aria label for the node."""

    origin: NotRequired[NodeOrigin]
    """Origin of the node relative to its position."""

    handles: NotRequired[Sequence[NodeHandle]]

    measured: NotRequired[Measured]

    type: NotRequired[str | NodeType]
    """Type of node defined in nodeTypes."""

    style: NotRequired[Any]

    className: NotRequired[str]

    resizing: NotRequired[bool]

    focusable: NotRequired[bool]

    ariaRole: NotRequired[AriaRole]
    """The ARIA role attribute for the node element, used for accessibility."""

    domAttributes: NotRequired[dict[str, Any]]
    """General escape hatch for adding custom attributes to the node’s DOM element."""


class NodeHandleBounds(TypedDict):
    """Represents the bounds of a node's handles."""

    source: list[NodeHandle]
    target: list[NodeHandle]


class NodeBounds(XYPosition):
    """Represents the bounds of a node."""

    width: float
    height: float


class NodeInternals(TypedDict):
    """Represents the internal state of a node."""

    positionAbsolute: XYPosition
    z: float
    userNode: Node
    handleBounds: NotRequired[NodeHandleBounds]
    bounds: NotRequired[NodeBounds]


class InternalNode(Node):
    """The InternalNode type is identical to the base Node type but is extended with some additional properties used internally by React Flow. Some functions and callbacks that return nodes may return an InternalNode."""

    internals: NodeInternals


class FitViewOptions(TypedDict):
    """When calling fitView these options can be used to customize the behavior.

    For example, the duration option can be used to transform the viewport smoothly over a given amount of time.
    """

    padding: NotRequired[str | float | Padding]
    includeHiddenNodes: NotRequired[bool]
    minZoom: NotRequired[float]
    maxZoom: NotRequired[float]
    duration: NotRequired[float]
    ease: NotRequired[Any]
    interpolate: NotRequired[Literal["smooth", "linear"]]
    nodes: NotRequired[Sequence[Node | Id]]


EdgeType = Literal["default", "straight", "step", "smoothstep", "simplebezier"]


class EdgeMarker(TypedDict):
    """Edges can optionally have markers at the start and end of an edge. The EdgeMarker type is used to configure those markers!

    Check the docs for MarkerType for details on what types of edge marker are available.
    """

    type: Literal["arrow", "arrowclosed"]
    color: NotRequired[str | None]
    width: NotRequired[float]
    height: NotRequired[float]
    markerUnits: NotRequired[str]
    orient: NotRequired[str]
    strokeWidth: NotRequired[float]


class Edge(TypedDict):
    """Where a Connection is the minimal description of an edge between two nodes, an Edge is the complete description with everything React Flow needs to know in order to render it."""

    id: str
    """Unique id of an edge."""

    type: NotRequired[EdgeType | str]
    """Type of edge defined in edgeTypes."""

    source: str
    """Id of source node."""

    target: str
    """Id of target node."""

    sourceHandle: NotRequired[str | None]
    """Id of source handle, only needed if there are multiple handles per node."""

    targetHandle: NotRequired[str | None]
    """Id of target handle, only needed if there are multiple handles per node."""

    animated: NotRequired[bool]

    hidden: NotRequired[bool]

    deletable: NotRequired[bool]

    selectable: NotRequired[bool]

    data: NotRequired[dict[str, Any]]
    """Arbitrary data passed to an edge."""

    selected: NotRequired[bool]

    markerStart: NotRequired[str | EdgeMarker]
    """Set the marker on the beginning of an edge."""

    markerEnd: NotRequired[str | EdgeMarker]
    """Set the marker on the end of an edge."""

    zIndex: NotRequired[float]

    ariaLabel: NotRequired[str]

    interactionWidth: NotRequired[float]
    """ReactFlow renders an invisible path around each edge to make them easier to click or tap on. This property sets the width of that invisible path."""

    label: NotRequired[Any]
    """The label or custom element to render along the edge. This is commonly a text label or some custom controls."""

    labelStyle: NotRequired[Any]
    """Custom styles to apply to the label."""

    labelShowBg: NotRequired[bool]

    labelBgStyle: NotRequired[Any]

    labelBgPadding: NotRequired[tuple[float, float]]

    labelBgBorderRadius: NotRequired[float]

    style: NotRequired[Any]

    className: NotRequired[str]

    reconnectable: NotRequired[bool | HandleType]
    """Determines whether the edge can be updated by dragging the source or target to a new node. This property will override the default set by the edgesReconnectable prop on the <ReactFlow /> component."""

    focusable: NotRequired[bool]

    ariaRole: NotRequired[AriaRole]
    """The ARIA role attribute for the edge, used for accessibility."""

    domAttributes: NotRequired[dict[str, Any]]
    """General escape hatch for adding custom attributes to the edge’s DOM element."""


class SmoothStepEdgePathOptions(TypedDict):
    """Options for customizing the path of a smooth step edge."""

    offset: NotRequired[float]
    borderRadius: NotRequired[float]


class SmoothStepEdge(Edge):
    """A smooth step edge is a type of edge that has a smooth transition between steps."""

    type: Literal["smoothstep"]  # pyright: ignore[reportIncompatibleVariableOverride]
    pathOptions: NotRequired[SmoothStepEdgePathOptions]


class BezierEdgePathOptions(TypedDict):
    """Options for customizing the path of a Bezier edge."""

    curvature: NotRequired[float]


class BezierEdge(Edge):
    """A Bezier edge is a type of edge that has a Bezier curve between two points."""

    type: Literal["bezier"]  # pyright: ignore[reportIncompatibleVariableOverride]

    pathOptions: NotRequired[BezierEdgePathOptions]


class DefaultEdgeOptions(TypedDict):
    """Many properties on an Edge are optional.

    When a new edge is created, the properties that are not provided will be filled in with the default values passed to the defaultEdgeOptions prop of the <ReactFlow /> component.
    """

    type: NotRequired[str | None]
    """Type of edge defined in edgeTypes."""

    animated: NotRequired[bool]

    hidden: NotRequired[bool]

    deletable: NotRequired[bool]

    selectable: NotRequired[bool]

    data: NotRequired[dict[str, Any]]
    """Arbitrary data passed to an edge."""

    markerStart: NotRequired[str | EdgeMarker]
    """Set the marker on the beginning of an edge."""

    markerEnd: NotRequired[str | EdgeMarker]
    """Set the marker on the end of an edge."""

    zIndex: NotRequired[float]

    ariaLabel: NotRequired[str]

    interactionWidth: NotRequired[float]
    """ReactFlow renders an invisible path around each edge to make them easier to click or tap on. This property sets the width of that invisible path."""

    label: NotRequired[Any]
    """The label or custom element to render along the edge. This is commonly a text label or some custom controls."""

    labelStyle: NotRequired[Any]
    """Custom styles to apply to the label."""

    labelShowBg: NotRequired[bool]

    labelBgStyle: NotRequired[Any]

    labelBgPadding: NotRequired[tuple[float, float]]

    labelBgBorderRadius: NotRequired[float]

    style: NotRequired[Any]

    className: NotRequired[str]

    reconnectable: NotRequired[bool | HandleType]
    """Determines whether the edge can be updated by dragging the source or target to a new node. This property will override the default set by the edgesReconnectable prop on the <ReactFlow /> component."""

    focusable: NotRequired[bool]

    ariaRole: NotRequired[AriaRole]
    """The ARIA role attribute for the edge, used for accessibility."""

    domAttributes: NotRequired[dict[str, Any]]
    """General escape hatch for adding custom attributes to the edge’s DOM element."""


class OnDeleteParams(TypedDict):
    """Parameters for the onDelete event."""

    nodes: list[Node]
    edges: list[Edge]


class OnDelete(TypedDict):
    """Triggered when nodes or edges are deleted."""

    params: OnDeleteParams


class Dimensions(TypedDict):
    """Represents the dimensions of a node."""

    width: float
    height: float


class NodeDimensionChange(TypedDict):
    """Triggered when a node's dimensions change."""

    id: str
    type: Literal["dimensions"]
    dimensions: NotRequired[Dimensions]
    resizing: NotRequired[bool]
    setAttributes: NotRequired[bool | Literal["width", "height"]]


class NodePositionChange(TypedDict):
    """Triggered when a node's position changes."""

    id: str
    type: Literal["position"]
    position: NotRequired[XYPosition]
    positionAbsolute: NotRequired[XYPosition]
    dragging: NotRequired[bool]


class NodeSelectionChange(TypedDict):
    """Triggered when a node's selection state changes."""

    id: str
    type: Literal["select"]
    selected: bool


class NodeRemoveChange(TypedDict):
    """Triggered when a node is removed."""

    id: str
    type: Literal["remove"]


class NodeAddChange(TypedDict):
    """Triggered when a node is added."""

    item: Node
    type: Literal["add"]
    index: NotRequired[int]


class NodeReplaceChange(TypedDict):
    """Triggered when a node is replaced."""

    id: str
    type: Literal["replace"]
    item: Node


NodeChange = (
    NodeDimensionChange
    | NodePositionChange
    | NodeSelectionChange
    | NodeRemoveChange
    | NodeAddChange
    | NodeReplaceChange
)


class Connection(TypedDict):
    """The Connection type is the basic minimal description of an Edge between two nodes.

    The addEdge util can be used to upgrade a Connection to an Edge.
    """

    source: str
    """The id of the node this connection originates from."""

    target: str
    """The id of the node this connection terminates at."""

    sourceHandle: str | None
    """When not null, the id of the handle on the source node that this connection originates from."""

    targetHandle: str | None
    """When not null, the id of the handle on the target node that this connection terminates at."""


class NodeConnection(Connection):
    """The NodeConnection type is an extension of a basic Connection that includes the edgeId."""

    edgeId: str


NoConnection = TypedDict(
    "NoConnection",
    {
        "inProgress": Literal[False],
        "isValid": None,
        "from": None,
        "fromHandle": None,
        "fromPosition": None,
        "fromNode": None,
        "to": None,
        "toHandle": None,
        "toPosition": None,
        "toNode": None,
    },
)

ConnectionInProgress = TypedDict(
    "ConnectionInProgress",
    {
        "inProgress": Literal[True],
        "isValid": bool | None,
        "from": XYPosition,
        "fromHandle": NodeHandle,
        "fromPosition": Position,
        "fromNode": Node,
        "to": XYPosition,
        "toHandle": NodeHandle | None,
        "toPosition": Position,
        "toNode": Node | None,
    },
)

ConnectionState = TypedDict(
    "ConnectionState",
    {
        "inProgress": bool,
        "isValid": bool | None,
        "from": XYPosition | None,
        "fromHandle": NodeHandle | None,
        "fromPosition": Position | None,
        "fromNode": Node | None,
        "to": XYPosition | None,
        "toHandle": NodeHandle | None,
        "toPosition": Position | None,
        "toNode": Node | None,
    },
)


class EdgeAddChange(TypedDict):
    """Triggered when an edge is added."""

    item: Edge
    type: Literal["add"]
    index: NotRequired[int]


class EdgeRemoveChange(TypedDict):
    """Triggered when an edge is removed."""

    id: str
    type: Literal["remove"]


class EdgeReplaceChange(TypedDict):
    """Triggered when an edge is replaced."""

    id: str
    item: Edge
    type: Literal["replace"]


class EdgeSelectionChange(TypedDict):
    """Triggered when an edge's selection state changes."""

    id: str
    type: Literal["select"]
    selected: bool


EdgeChange = EdgeAddChange | EdgeRemoveChange | EdgeReplaceChange | EdgeSelectionChange


class OnConnectStartParams(TypedDict):
    """Parameters for the onConnectStart event."""

    nodeId: str | None
    handleId: str | None
    handleType: HandleType | None


class ViewportVar(reflex.vars.ObjectVar[Viewport]):
    """Represents the viewport of the flow."""

    if TYPE_CHECKING:
        x: reflex.vars.NumberVar[float]
        y: reflex.vars.NumberVar[float]
        zoom: reflex.vars.NumberVar[float]


class RectVar(reflex.vars.ObjectVar[Rect]):
    """Represents a rectangle in the flow."""

    if TYPE_CHECKING:
        x: reflex.vars.NumberVar[float]
        y: reflex.vars.NumberVar[float]
        width: reflex.vars.NumberVar[float]
        height: reflex.vars.NumberVar[float]


class XYPositionVar(reflex.vars.ObjectVar[XYPosition]):
    """Represents the position of a node in the flow."""

    if TYPE_CHECKING:
        x: reflex.vars.NumberVar[float]
        y: reflex.vars.NumberVar[float]


class NodeHandleVar(reflex.vars.ObjectVar[NodeHandle]):
    """Represents a handle on a node in the flow."""

    if TYPE_CHECKING:
        width: reflex.vars.NumberVar[float]
        height: reflex.vars.NumberVar[float]
        id: reflex.vars.StringVar | None
        x: reflex.vars.NumberVar[float]
        y: reflex.vars.NumberVar[float]
        pos: reflex.vars.StringVar[Position]
        type: reflex.vars.StringVar[HandleType]


class MeasuredVar(reflex.vars.ObjectVar[Measured]):
    """Represents the measured properties of a node in the flow."""

    if TYPE_CHECKING:
        width: reflex.vars.NumberVar[float]
        height: reflex.vars.NumberVar[float]


class NodeVar(reflex.vars.ObjectVar[Node]):
    """Represents a node in the flow."""

    if TYPE_CHECKING:
        id: reflex.vars.StringVar
        position: XYPositionVar
        data: reflex.vars.ObjectVar[Mapping[str, Any]]
        sourcePosition: reflex.vars.StringVar[Position]  # noqa: N815
        targetPosition: reflex.vars.StringVar[Position]  # noqa: N815
        hidden: reflex.vars.BooleanVar
        selected: reflex.vars.BooleanVar
        dragging: reflex.vars.BooleanVar
        draggable: reflex.vars.BooleanVar
        selectable: reflex.vars.BooleanVar
        connectable: reflex.vars.BooleanVar
        deletable: reflex.vars.BooleanVar
        dragHandle: reflex.vars.StringVar  # noqa: N815
        width: reflex.vars.NumberVar[float]
        height: reflex.vars.NumberVar[float]
        initialWidth: reflex.vars.NumberVar[float]  # noqa: N815
        initialHeight: reflex.vars.NumberVar[float]  # noqa: N815
        parentId: reflex.vars.StringVar  # noqa: N815
        zIndex: reflex.vars.NumberVar[int]  # noqa: N815
        extent: (
            reflex.vars.ArrayVar[CoordinateExtent]
            | reflex.vars.StringVar[Literal["parent"]]
        )
        expandParent: reflex.vars.BooleanVar  # noqa: N815
        ariaLabel: reflex.vars.StringVar  # noqa: N815
        origin: reflex.vars.ArrayVar[NodeOrigin]
        handles: reflex.vars.ArrayVar[Sequence[NodeHandleVar]]
        measured: MeasuredVar
        type: reflex.vars.StringVar[str | NodeType]
        style: reflex.vars.ObjectVar[Mapping[str, Any]]
        className: reflex.vars.StringVar  # noqa: N815
        resizing: reflex.vars.BooleanVar
        focusable: reflex.vars.BooleanVar
        ariaRole: reflex.vars.StringVar[AriaRole]  # noqa: N815
        domAttributes: reflex.vars.ObjectVar[Mapping[str, Any]]  # noqa: N815


class NodeHandleBoundsVar(reflex.vars.ObjectVar[NodeHandleBounds]):
    """Represents the bounds of a node's handles."""

    if TYPE_CHECKING:
        source: reflex.vars.ArrayVar[Sequence[NodeHandle]]
        target: reflex.vars.ArrayVar[Sequence[NodeHandle]]


class NodeBoundsVar(XYPositionVar):
    """Represents the bounds of a node."""

    if TYPE_CHECKING:
        width: reflex.vars.NumberVar[float]
        height: reflex.vars.NumberVar[float]


class NodeInternalsVar(reflex.vars.ObjectVar[NodeInternals]):
    """Represents the internal state of a node."""

    if TYPE_CHECKING:
        positionAbsolute: XYPositionVar  # noqa: N815
        z: reflex.vars.NumberVar[float]
        userNode: NodeVar  # noqa: N815
        handleBounds: NodeHandleBoundsVar | reflex.vars.base.NoneVar  # noqa: N815
        bounds: NodeBoundsVar | reflex.vars.base.NoneVar


class InternalNodeVar(NodeVar):
    """Represents an internal node in the flow."""

    if TYPE_CHECKING:
        internals: NodeInternalsVar


class EdgeMarkerVar(reflex.vars.ObjectVar[EdgeMarker]):
    """Represents a marker on an edge."""

    if TYPE_CHECKING:
        type: reflex.vars.StringVar[Literal["arrow", "arrowclosed"]]
        color: reflex.vars.StringVar | reflex.vars.base.NoneVar
        width: reflex.vars.NumberVar[float] | reflex.vars.base.NoneVar
        height: reflex.vars.NumberVar[float] | reflex.vars.base.NoneVar
        markerUnits: reflex.vars.StringVar | reflex.vars.base.NoneVar  # noqa: N815
        orient: reflex.vars.StringVar | reflex.vars.base.NoneVar
        strokeWidth: reflex.vars.NumberVar[float] | reflex.vars.base.NoneVar  # noqa: N815


class EdgeVar(reflex.vars.ObjectVar[Edge]):
    """Represents an edge in the flow."""

    if TYPE_CHECKING:
        id: reflex.vars.StringVar[str]
        type: reflex.vars.StringVar[EdgeType | str]
        source: reflex.vars.StringVar[str]
        target: reflex.vars.StringVar[str]
        sourceHandle: reflex.vars.StringVar[str] | reflex.vars.base.NoneVar  # noqa: N815
        targetHandle: reflex.vars.StringVar[str] | reflex.vars.base.NoneVar  # noqa: N815
        animated: reflex.vars.BooleanVar
        hidden: reflex.vars.BooleanVar
        deletable: reflex.vars.BooleanVar
        selectable: reflex.vars.BooleanVar
        data: reflex.vars.ObjectVar[Mapping[str, Any]]
        selected: reflex.vars.BooleanVar
        markerStart: reflex.vars.StringVar | EdgeMarkerVar  # noqa: N815
        markerEnd: reflex.vars.StringVar | EdgeMarkerVar  # noqa: N815
        zIndex: reflex.vars.NumberVar[float]  # noqa: N815
        ariaLabel: reflex.vars.StringVar[str]  # noqa: N815
        interactionWidth: reflex.vars.NumberVar[float]  # noqa: N815
        label: reflex.Var
        labelStyle: reflex.Var  # noqa: N815
        labelShowBg: reflex.vars.BooleanVar  # noqa: N815
        labelBgStyle: reflex.Var  # noqa: N815
        labelBgPadding: reflex.vars.ArrayVar[tuple[float, float]]  # noqa: N815
        labelBgBorderRadius: reflex.vars.NumberVar[float]  # noqa: N815
        style: reflex.Var
        className: reflex.vars.StringVar[str]  # noqa: N815
        reconnectable: reflex.vars.StringVar[HandleType] | reflex.vars.BooleanVar
        focusable: reflex.vars.BooleanVar
        ariaRole: reflex.vars.StringVar[AriaRole]  # noqa: N815
        domAttributes: reflex.vars.ObjectVar[Mapping[str, Any]]  # noqa: N815


class ConnectionVar(reflex.vars.ObjectVar[Connection]):
    """Represents a connection between two nodes in the flow."""

    if TYPE_CHECKING:
        source: reflex.vars.StringVar[str]
        target: reflex.vars.StringVar[str]
        sourceHandle: reflex.vars.StringVar[str] | reflex.vars.base.NoneVar  # noqa: N815
        targetHandle: reflex.vars.StringVar[str] | reflex.vars.base.NoneVar  # noqa: N815


class NodeConnectionVar(ConnectionVar):
    """Represents a connection between two nodes in the flow."""

    if TYPE_CHECKING:
        edgeId: reflex.vars.StringVar[str]  # noqa: N815


class ConnectionStateVar(reflex.vars.ObjectVar[ConnectionState]):
    """Represents the state of a connection between two nodes in the flow."""

    if TYPE_CHECKING:
        inProgress: reflex.vars.BooleanVar  # noqa: N815
        isValid: reflex.vars.BooleanVar | reflex.vars.base.NoneVar  # noqa: N815
        # from: XYPositionVar | reflex.vars.base.NoneVar
        fromHandle: NodeHandleVar | reflex.vars.base.NoneVar  # noqa: N815
        fromPosition: reflex.vars.StringVar[Position] | reflex.vars.base.NoneVar  # noqa: N815
        fromNode: NodeVar | reflex.vars.base.NoneVar  # noqa: N815
        to: XYPositionVar | reflex.vars.base.NoneVar
        toHandle: NodeHandleVar | reflex.vars.base.NoneVar  # noqa: N815
        toPosition: reflex.vars.StringVar[Position] | reflex.vars.base.NoneVar  # noqa: N815
        toNode: NodeVar | reflex.vars.base.NoneVar  # noqa: N815
