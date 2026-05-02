"""Flow component for managing the flow of data between nodes."""

from typing import Any, Literal, Mapping, Sequence, TypedDict

import reflex
from reflex.event import (
    JavascriptPointerEvent,
    PointerEventInfo,
    passthrough_event_spec,
    pointer_event_spec,
)

from .types import (
    AriaLabelConfig,
    ColorMode,
    Connection,
    ConnectionInProgress,
    CoordinateExtent,
    DefaultEdgeOptions,
    Edge,
    EdgeChange,
    FitViewOptions,
    HandleType,
    NoConnection,
    Node,
    NodeChange,
    NodeOrigin,
    OnConnectStartParams,
    OnDelete,
    OnDeleteParams,
    PanelPosition,
    Position,
    ProOptions,
    SnapGrid,
    Viewport,
    XYPosition,
)
from .types import EdgeAddChange as EdgeAddChange
from .types import EdgeRemoveChange as EdgeRemoveChange
from .types import EdgeReplaceChange as EdgeReplaceChange
from .types import EdgeSelectionChange as EdgeSelectionChange
from .types import NodeAddChange as NodeAddChange
from .types import NodeDimensionChange as NodeDimensionChange
from .types import NodePositionChange as NodePositionChange
from .types import NodeRemoveChange as NodeRemoveChange
from .types import NodeReplaceChange as NodeReplaceChange
from .types import NodeSelectionChange as NodeSelectionChange

LIBRARY = "@xyflow/react@12.8.4"


def _on_delete_spec(event: reflex.Var[OnDelete]) -> tuple[reflex.Var[OnDeleteParams]]:
    return (event.to(dict).params,)


def _flip_mouse_event_and_node_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent], node: reflex.Var[Node]
) -> tuple[reflex.Var[Node], reflex.Var[PointerEventInfo]]:
    return (node, pointer_event_spec(event)[0])


def _flip_mouse_event_and_edge_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent], edge: reflex.Var[Edge]
) -> tuple[reflex.Var[Edge], reflex.Var[PointerEventInfo]]:
    return (edge, pointer_event_spec(event)[0])


def _on_reconnect_start_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent],
    edge: reflex.Var[Edge],
    handle_type: reflex.Var[HandleType],
) -> tuple[reflex.Var[Edge], reflex.Var[HandleType], reflex.Var[PointerEventInfo]]:
    return (edge, handle_type, pointer_event_spec(event)[0])


def _on_reconnect_end_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent],
    edge: reflex.Var[Edge],
    handle_type: reflex.Var[HandleType],
    connection_state: reflex.Var[NoConnection | ConnectionInProgress],
) -> tuple[
    reflex.Var[Edge],
    reflex.Var[HandleType],
    reflex.Var[NoConnection | ConnectionInProgress],
    reflex.Var[PointerEventInfo],
]:
    return (edge, handle_type, connection_state, pointer_event_spec(event)[0])


def _on_connect_start_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent],
    params: reflex.Var[OnConnectStartParams],
) -> tuple[reflex.Var[OnConnectStartParams], reflex.Var[PointerEventInfo]]:
    return (params, pointer_event_spec(event)[0])


def _on_connect_end_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent],
    connection_state: reflex.Var[NoConnection | ConnectionInProgress],
) -> tuple[
    reflex.Var[NoConnection | ConnectionInProgress], reflex.Var[PointerEventInfo]
]:
    return (connection_state, pointer_event_spec(event)[0])


def _flip_mouse_event_and_viewport_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent | None],
    viewport: reflex.Var[Viewport],
) -> tuple[reflex.Var[Viewport], reflex.Var[PointerEventInfo | None]]:
    return (viewport, reflex.cond(event.is_none(), None, pointer_event_spec(event)[0]))  # pyright: ignore[reportArgumentType]


class Flow(reflex.Component):
    """The <ReactFlow /> component is the heart of your React Flow application. It renders your nodes and edges, handles user interaction, and can manage its own state if used as an uncontrolled flow."""

    library = LIBRARY

    tag = "ReactFlow"

    is_default = False

    width: reflex.Var[float]
    """Sets a fixed width for the flow."""

    height: reflex.Var[float]
    """Sets a fixed height for the flow."""

    nodes: reflex.Var[Sequence[Node]]
    """An array of nodes to render in a controlled flow."""

    edges: reflex.Var[Sequence[Edge]]
    """An array of edges to render in a controlled flow."""

    default_nodes: reflex.Var[Sequence[Node]]
    """The initial nodes to render in an uncontrolled flow."""

    default_edges: reflex.Var[Sequence[Edge]]
    """The initial edges to render in an uncontrolled flow."""

    pane_click_distance: reflex.Var[float]
    """Distance that the mouse can move between mousedown/up that will trigger a click."""

    node_click_distance: reflex.Var[float]
    """Distance that the mouse can move between mousedown/up that will trigger a click."""

    node_types: reflex.Var[Mapping[str, Any]]
    """Custom node types to be available in a flow. React Flow matches a node’s type to a component in the nodeTypes object."""

    edge_types: reflex.Var[Mapping[str, Any]]
    """Custom edge types to be available in a flow. React Flow matches an edge’s type to a component in the edgeTypes object."""

    auto_pan_on_node_focus: reflex.Var[bool]
    """When true, the viewport will pan when a node is focused."""

    node_origin: reflex.Var[NodeOrigin]
    """The origin of the node to use when placing it in the flow or looking up its x and y position. An origin of [0, 0] means that a node’s top left corner will be placed at the x and y position."""

    pro_options: reflex.Var[ProOptions]
    """By default, we render a small attribution in the corner of your flows that links back to the project.

    Anyone is free to remove this attribution whether they’re a Pro subscriber or not but we ask that you take a quick look at our https://reactflow.dev/learn/troubleshooting/remove-attribution
    removing attribution guide before doing so.
    """

    node_drag_threshold: reflex.Var[float]
    """With a threshold greater than zero you can delay node drag events. If threshold equals 1, you need to drag the node 1 pixel before a drag event is fired. 1 is the default value, so that clicks don’t trigger drag events."""

    connection_drag_threshold: reflex.Var[float]
    """The threshold in pixels that the mouse must move before a connection line starts to drag. This is useful to prevent accidental connections when clicking on a handle."""

    color_mode: reflex.Var[ColorMode]
    """Controls color scheme used for styling the flow."""

    debug: reflex.Var[bool]
    """If set true, some debug information will be logged to the console like which events are fired."""

    aria_label_config: reflex.Var[AriaLabelConfig]
    """Configuration for customizable labels, descriptions, and UI text.

    Provided keys will override the corresponding defaults.
    Allows localization, customization of ARIA descriptions, control labels, minimap labels, and other UI strings.
    """

    default_viewport: reflex.Var[Viewport]
    """Sets the initial position and zoom of the viewport. If a default viewport is provided but fitView is enabled, the default viewport will be ignored."""

    viewport: reflex.Var[Viewport]
    """When you pass a viewport prop, it’s controlled, and you also need to pass onViewportChange to handle internal changes."""

    on_viewport_change: reflex.EventHandler[passthrough_event_spec(Viewport)]
    """Used when working with a controlled viewport for updating the user viewport state."""

    fit_view: reflex.Var[bool]
    """When true, the flow will be zoomed and panned to fit all the nodes initially provided."""

    fit_view_options: reflex.Var[FitViewOptions]
    """When you typically call fitView on a ReactFlowInstance, you can provide an object of options to customize its behavior.

    This prop lets you do the same for the initial fitView call.
    """

    min_zoom: reflex.Var[float]
    """Minimum zoom level."""

    max_zoom: reflex.Var[float]
    """Maximum zoom level."""

    snap_to_grid: reflex.Var[bool]
    """When enabled, nodes will snap to the grid when dragged."""

    snap_grid: reflex.Var[SnapGrid]
    """If snapToGrid is enabled, this prop configures the grid that nodes will snap to."""

    only_render_visible_elements: reflex.Var[bool]
    """You can enable this optimisation to instruct React Flow to only render nodes and edges that would be visible in the viewport.

    This might improve performance when you have a large number of nodes and edges but also adds an overhead.
    """

    translate_extent: reflex.Var[CoordinateExtent]
    """By default, the viewport extends infinitely. You can use this prop to set a boundary.

    The first pair of coordinates is the top left boundary and the second pair is the bottom right.
    """

    node_extent: reflex.Var[CoordinateExtent]
    """By default, nodes can be placed on an infinite flow. You can use this prop to set a boundary.

    The first pair of coordinates is the top left boundary and the second pair is the bottom right.
    """

    prevent_scrolling: reflex.Var[bool]
    """Disabling this prop will allow the user to scroll the page even when their pointer is over the flow."""

    attribution_position: reflex.Var[PanelPosition]
    """By default, React Flow will render a small attribution in the bottom right corner of the flow.

    You can use this prop to change its position in case you want to place something else there.
    """

    elevate_edges_on_select: reflex.Var[bool]
    """Enabling this option will raise the z-index of edges when they are selected."""

    default_marker_color: reflex.Var[str | None]
    """Color of edge markers. You can pass null to use the CSS variable --xy-edge-stroke for the marker color."""

    default_edge_options: reflex.Var[DefaultEdgeOptions]
    """Defaults to be applied to all new edges that are added to the flow. Properties on a new edge will override these defaults if they exist."""

    reconnect_radius: reflex.Var[float]
    """The radius around an edge connection that can trigger an edge reconnection."""

    edges_reconnectable: reflex.Var[bool]
    """Whether edges can be updated once they are created. When both this prop is true and an onReconnect handler is provided, the user can drag an existing edge to a new source or target.

    Individual edges can override this value with their reconnectable property.
    """

    on_error: reflex.EventHandler[passthrough_event_spec(str, str)]
    """Occasionally something may happen that causes React Flow to throw an error.

    Instead of exploding your application, we log a message to the console and then call this event handler. You might use it for additional logging or to show a message to the user.
    """

    on_delete: reflex.EventHandler[_on_delete_spec]
    """This event handler gets called when a node or edge is deleted."""

    # Ignored because callbacks are weird
    # on_before_delete

    on_node_click: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user clicks on a node."""

    on_node_double_click: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user double-clicks on a node."""

    on_node_drag_starts: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user starts to drag a node."""

    on_node_drag: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user drags a node."""

    on_node_drag_stop: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user stops dragging a node."""

    on_node_mouse_enter: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when mouse of a user enters a node."""

    on_node_mouse_move: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when mouse of a user moves over a node."""

    on_node_mouse_leave: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when mouse of a user leaves a node."""

    on_node_context_menu: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """This event handler is called when a user right-clicks on a node."""

    on_nodes_delete: reflex.EventHandler[passthrough_event_spec(list[Node])]
    """This event handler gets called when a node is deleted."""

    on_nodes_change: reflex.EventHandler[passthrough_event_spec(list[NodeChange])]
    """Use this event handler to add interactivity to a controlled flow. It is called on node drag, select, and move."""

    on_edge_click: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when a user clicks on an edge."""

    on_edge_double_click: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when a user double-clicks on an edge."""

    on_edge_mouse_enter: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when mouse of a user enters an edge."""

    on_edge_mouse_move: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when mouse of a user moves over an edge."""

    on_edge_mouse_leave: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when mouse of a user leaves an edge."""

    on_edge_context_menu: reflex.EventHandler[_flip_mouse_event_and_edge_spec]
    """This event handler is called when a user right-clicks on an edge."""

    on_reconnect: reflex.EventHandler[passthrough_event_spec(Edge, Connection)]
    """This handler is called when the source or target of a reconnectable edge is dragged from the current node.

    It will fire even if the edge’s source or target do not end up changing. You can use the reconnectEdge utility to convert the connection to a new edge.
    """

    on_reconnect_start: reflex.EventHandler[_on_reconnect_start_spec]
    """This event fires when the user begins dragging the source or target of an editable edge."""

    on_reconnect_end: reflex.EventHandler[_on_reconnect_end_spec]
    """This event fires when the user releases the source or target of an editable edge. It is called even if an edge update does not occur."""

    on_edges_delete: reflex.EventHandler[passthrough_event_spec(list[Edge])]
    """This event handler gets called when an edge is deleted."""

    on_edges_change: reflex.EventHandler[passthrough_event_spec(list[EdgeChange])]
    """Use this event handler to add interactivity to a controlled flow. It is called on edge select and remove."""

    on_connect: reflex.EventHandler[passthrough_event_spec(Connection)]
    """When a connection line is completed and two nodes are connected by the user, this event fires with the new connection.

    You can use the addEdge utility to convert the connection to a complete edge.
    """

    on_connect_start: reflex.EventHandler[_on_connect_start_spec]
    """This event handler gets called when a user starts to drag a connection line."""

    on_connect_end: reflex.EventHandler[_on_connect_end_spec]
    """This callback will fire regardless of whether a valid connection could be made or not. You can use the second connectionState parameter to have different behavior when a connection was unsuccessful."""

    on_click_connect_start: reflex.EventHandler[_on_connect_start_spec]
    on_click_connect_end: reflex.EventHandler[_on_connect_end_spec]

    # Ignored as callables are weird
    # is_valid_connection: Callable[[Edge | Connection], bool]  # noqa: ERA001

    on_move: reflex.EventHandler[_flip_mouse_event_and_viewport_spec]
    """This event handler is called while the user is either panning or zooming the viewport."""

    on_move_start: reflex.EventHandler[_flip_mouse_event_and_viewport_spec]
    """This event handler is called when the user begins to pan or zoom the viewport."""

    on_move_end: reflex.EventHandler[_flip_mouse_event_and_viewport_spec]
    """This event handler is called when panning or zooming viewport movement stops. If the movement is not user-initiated, the event parameter will be null."""

    on_pane_click: reflex.EventHandler[reflex.event.pointer_event_spec]
    """This event handler gets called when user clicks inside the pane."""

    on_pane_context_menu: reflex.EventHandler[reflex.event.pointer_event_spec]
    """This event handler gets called when user right clicks inside the pane."""

    # TODO: Pass WheelEvent
    on_pane_scroll: reflex.EventHandler[reflex.event.no_args_event_spec]
    """This event handler gets called when user scroll inside the pane."""

    on_pane_mouse_move: reflex.EventHandler[reflex.event.pointer_event_spec]
    """This event handler gets called when mouse moves over the pane."""

    on_pane_mouse_enter: reflex.EventHandler[reflex.event.pointer_event_spec]
    """This event handler gets called when mouse enters the pane."""

    on_pane_mouse_leave: reflex.EventHandler[reflex.event.pointer_event_spec]
    """This event handler gets called when mouse leaves the pane."""

    # TODO: Wrap Selection Events

    nodes_draggable: reflex.Var[bool]
    """Controls whether all nodes should be draggable or not.

    Individual nodes can override this setting by setting their draggable prop.

    If you want to use the mouse handlers on non-draggable nodes, you need to add the "nopan" class to those nodes.
    """

    nodes_connectable: reflex.Var[bool]
    """Controls whether all nodes should be connectable or not.

    Individual nodes can override this setting by setting their connectable prop.
    """

    nodes_focusable: reflex.Var[bool]
    """When true, focus between nodes can be cycled with the Tab key and selected with the Enter key.

    This option can be overridden by individual nodes by setting their focusable prop.
    """

    edges_focusable: reflex.Var[bool]
    """When true, focus between edges can be cycled with the Tab key and selected with the Enter key.

    This option can be overridden by individual edges by setting their focusable prop.
    """

    elements_selectable: reflex.Var[bool]
    """When true, elements (nodes and edges) can be selected by clicking on them. This option can be overridden by individual elements by setting their selectable prop."""

    auto_pan_on_connect: reflex.Var[bool]
    """When true, the viewport will pan automatically when the cursor moves to the edge of the viewport while creating a connection"""

    auto_pan_on_node_drag: reflex.Var[bool]
    """When true, the viewport will pan automatically when the cursor moves to the edge of the viewport while dragging a node."""

    auto_pan_speed: reflex.Var[float]
    """The speed at which the viewport pans while dragging a node or a selection box."""

    pan_on_drag: reflex.Var[bool | Sequence[float]]
    """Enabling this prop allows users to pan the viewport by clicking and dragging.

    You can also set this prop to an array of numbers to limit which mouse buttons can activate panning.
    """

    selection_on_drag: reflex.Var[bool]
    """Select multiple elements with a selection box, without pressing down selectionKey."""

    selection_mode: reflex.Var[Literal["partial", "full"]]
    """When set to "partial", when the user creates a selection box by click and dragging nodes that are only partially in the box are still selected."""

    pan_on_scroll: reflex.Var[bool]
    """Controls if the viewport should pan by scrolling inside the container. Can be limited to a specific direction with panOnScrollMode."""

    pan_on_scroll_speed: reflex.Var[float]
    """Controls how fast viewport should be panned on scroll. Use together with panOnScroll prop."""

    pan_on_scroll_mode: reflex.Var[Literal["horizontal", "vertical", "free"]]
    """This prop is used to limit the direction of panning when panOnScroll is enabled. The "free" option allows panning in any direction."""

    zoom_on_scroll: reflex.Var[bool]
    """Controls if the viewport should zoom by scrolling inside the container."""

    zoom_on_pinch: reflex.Var[bool]
    """Controls if the viewport should zoom by pinching on a touch screen."""

    zoom_on_double_click: reflex.Var[bool]
    """Controls if the viewport should zoom by double-clicking somewhere on the flow."""

    select_nodes_on_drag: reflex.Var[bool]
    """If true, nodes get selected on drag."""

    elevate_nodes_on_select: reflex.Var[bool]
    """Enabling this option will raise the z-index of nodes when they are selected."""

    connect_on_click: reflex.Var[bool]
    """The connectOnClick option lets you click or tap on a source handle to start a connection and then click on a target handle to complete the connection.

    If you set this option to false, users will need to drag the connection line to the target handle to create a connection.
    """

    connection_mode: reflex.Var[Literal["strict", "loose"]]
    """A loose connection mode will allow you to connect handles with differing types, including source-to-source connections. However, it does not support target-to-target connections.

    Strict mode allows only connections between source handles and target handles.
    """

    connection_line_style: reflex.Var[Mapping[str, Any]]
    """Styles to be applied to the connection line."""

    connection_line_type: reflex.Var[
        Literal["default", "straight", "step", "smoothstep", "simplebezier"]
    ]
    """The type of edge path to use for connection lines. Although created edges can be of any type, React Flow needs to know what type of path to render for the connection line before the edge is created!"""

    connection_radius: reflex.Var[float]
    """The radius around a handle where you drop a connection line to create a new edge."""

    connection_line_component: reflex.Var[Any]
    """React Component to be used as a connection line."""

    connection_line_container_style: reflex.Var[Mapping[str, Any]]
    """Styles to be applied to the container of the connection line."""

    delete_key_code: reflex.Var[str | Sequence[str] | None]
    """If set, pressing the key or chord will delete any selected nodes and edges. Passing an array represents multiple keys that can be pressed.

    For example, ["Delete", "Backspace"] will delete selected elements when either key is pressed."""

    selection_key_code: reflex.Var[str | Sequence[str] | None]
    """If set, holding this key will let you click and drag to draw a selection box around multiple nodes and edges. Passing an array represents multiple keys that can be pressed.

    For example, ["Shift", "Meta"] will allow you to draw a selection box when either key is pressed."""

    multi_selection_key_code: reflex.Var[str | Sequence[str] | None]
    """Pressing down this key you can select multiple elements by clicking."""

    zoom_activation_key_code: reflex.Var[str | Sequence[str] | None]
    """If a key is set, you can zoom the viewport while that key is held down even if panOnScroll is set to false.

    By setting this prop to null you can disable this functionality."""

    pan_activation_key_code: reflex.Var[str | Sequence[str] | None]
    """If a key is set, you can pan the viewport while that key is held down even if panOnScroll is set to false.

    By setting this prop to null you can disable this functionality."""

    disable_keyboard_a11y: reflex.Var[bool]
    """You can use this prop to disable keyboard accessibility features such as selecting nodes or moving selected nodes with the arrow keys."""

    no_pan_class_name: reflex.Var[str]
    """If an element in the canvas does not stop mouse events from propagating, clicking and dragging that element will pan the viewport. Adding the "nopan" class prevents this behavior and this prop allows you to change the name of that class."""

    no_drag_class_name: reflex.Var[str]
    """If a node is draggable, clicking and dragging that node will move it around the canvas. Adding the "nodrag" class prevents this behavior and this prop allows you to change the name of that class."""

    no_wheel_class_name: reflex.Var[str]
    """Typically, scrolling the mouse wheel when the mouse is over the canvas will zoom the viewport. Adding the "nowheel" class to an element in the canvas will prevent this behavior and this prop allows you to change the name of that class."""

    def add_imports(self) -> reflex.ImportDict:
        """Add the imports for the datatable component.

        Returns:
            The import dict for the component.
        """
        return {"": "@xyflow/react/dist/style.css"}


class FlowProvider(reflex.Component):
    """The <ReactFlowProvider /> component is a context provider  that makes it possible to access a flow’s internal state outside of the <ReactFlow /> component. Many of the hooks we provide rely on this component to work."""

    library = LIBRARY

    tag = "ReactFlowProvider"

    is_default = False

    initial_nodes: reflex.Var[Sequence[Node]]
    """These nodes are used to initialize the flow. They are not dynamic."""

    initial_edges: reflex.Var[Sequence[Edge]]
    """These edges are used to initialize the flow. They are not dynamic."""

    default_nodes: reflex.Var[Sequence[Node]]
    """These nodes are used to initialize the flow. They are not dynamic."""

    default_edges: reflex.Var[Sequence[Edge]]
    """These edges are used to initialize the flow. They are not dynamic."""

    initial_width: reflex.Var[float]
    """The initial width is necessary to be able to use fitView on the server."""

    initial_height: reflex.Var[float]
    """The initial height is necessary to be able to use fitView on the server."""

    fit_view: reflex.Var[bool]
    """When true, the flow will be zoomed and panned to fit all the nodes initially provided."""

    initial_fit_view_options: reflex.Var[FitViewOptions]
    """You can provide an object of options to customize the initial fitView behavior."""

    initial_min_zoom: reflex.Var[float]
    """Initial minimum zoom level."""

    initial_max_zoom: reflex.Var[float]
    """Initial maximum zoom level."""

    node_origin: reflex.Var[NodeOrigin]
    """The origin of the node to use when placing it in the flow or looking up its x and y position. An origin of [0, 0] means that a node’s top left corner will be placed at the x and y position."""

    node_extent: reflex.Var[CoordinateExtent]
    """By default, nodes can be placed on an infinite flow. You can use this prop to set a boundary.

    The first pair of coordinates is the top left boundary and the second pair is the bottom right."""


class Background(reflex.Component):
    """The <Background /> component makes it convenient to render different types of backgrounds common in node-based UIs. It comes with three variants: lines, dots and cross."""

    library = LIBRARY

    tag = "Background"

    is_default = False

    color: reflex.Var[str]
    """Color of the pattern."""

    bg_color: reflex.Var[str]
    """Color of the background."""

    pattern_class_name: reflex.Var[str]
    """Class applied to the pattern."""

    gap: reflex.Var[float | tuple[float, float]]
    """The gap between patterns. Passing in a tuple allows you to control the x and y gap independently."""

    size: reflex.Var[float]
    """The radius of each dot or the size of each rectangle if BackgroundVariant.Dots or BackgroundVariant.Cross is used. This defaults to 1 or 6 respectively, or ignored if BackgroundVariant.Lines is used."""

    offset: reflex.Var[float | tuple[float, float]]
    """Offset of the pattern."""

    line_width: reflex.Var[float]
    """The width of the line used in the pattern."""

    variant: reflex.Var[Literal["lines", "dots", "cross"]]
    """Variant of the pattern."""


class BaseEdge(reflex.Component):
    """The <BaseEdge /> component gets used internally for all the edges. It can be used inside a custom edge and handles the invisible helper edge and the edge label for you."""

    library = LIBRARY

    tag = "BaseEdge"

    is_default = False

    path: reflex.Var[str]
    """The SVG path string that defines the edge. This should look something like 'M 0 0 L 100 100' for a simple line. The utility functions like getSimpleBezierEdge can be used to generate this string for you."""

    marker_start: reflex.Var[str]
    """The id of the SVG marker to use at the start of the edge. This should be defined in a <defs> element in a separate SVG document or element. Use the format “url(#markerId)” where markerId is the id of your marker definition."""

    marker_end: reflex.Var[str]
    """The id of the SVG marker to use at the end of the edge. This should be defined in a <defs> element in a separate SVG document or element. Use the format “url(#markerId)” where markerId is the id of your marker definition."""

    label: reflex.Var[Any]
    """The label or custom element to render along the edge. This is commonly a text label or some custom controls."""

    label_style: reflex.Var[Mapping[str, Any]]
    """Custom styles to apply to the label."""

    label_show_bg: reflex.Var[bool]

    label_bg_style: reflex.Var[Mapping[str, Any]]

    label_bg_padding: reflex.Var[tuple[float, float]]

    label_bg_border_radius: reflex.Var[float]

    interaction_width: reflex.Var[float]
    """The width of the invisible area around the edge that the user can interact with. This is useful for making the edge easier to click or hover over."""

    label_x: reflex.Var[float]
    """The x position of edge label."""

    label_y: reflex.Var[float]
    """The y position of edge label."""


class ControlButton(reflex.el.elements.Button):
    """You can add buttons to the control panel by using the <ControlButton /> component and pass it as a child to the <Controls /> component."""

    library = LIBRARY

    tag = "ControlButton"

    is_default = False


class Controls(reflex.Component):
    """The <Controls /> component renders a small panel that contains convenient buttons to zoom in, zoom out, fit the view, and lock the viewport."""

    library = LIBRARY

    tag = "Controls"

    is_default = False

    show_zoom: reflex.Var[bool]
    """Whether or not to show the zoom in and zoom out buttons. These buttons will adjust the viewport zoom by a fixed amount each press."""

    show_fit_view: reflex.Var[bool]
    """Whether or not to show the fit view button. By default, this button will adjust the viewport so that all nodes are visible at once."""

    show_interactive: reflex.Var[bool]
    """Show button for toggling interactivity."""

    fit_view_options: reflex.Var[FitViewOptions]
    """Customise the options for the fit view button. These are the same options you would pass to the fitView function."""

    on_zoom_in: reflex.EventHandler[reflex.event.no_args_event_spec]
    """Called in addition the default zoom behavior when the zoom in button is clicked."""

    on_zoom_out: reflex.EventHandler[reflex.event.no_args_event_spec]
    """Called in addition the default zoom behavior when the zoom out button is clicked."""

    on_fit_view: reflex.EventHandler[reflex.event.no_args_event_spec]
    """Called when the fit view button is clicked. When this is not provided, the viewport will be adjusted so that all nodes are visible."""

    on_interactive_change: reflex.EventHandler[passthrough_event_spec(bool)]
    """Called when the interactive (lock) button is clicked."""

    position: reflex.Var[PanelPosition]
    """Position of the controls on the pane"""

    # TODO: wrap aria-label

    orientation: reflex.Var[Literal["horizontal", "vertical"]]


class EdgeLabelRenderer(reflex.Component):
    """Edges are SVG-based. If you want to render more complex labels you can use the <EdgeLabelRenderer /> component to access a div based renderer. This component is a portal that renders the label in a <div /> that is positioned on top of the edges. You can see an example usage of the component in the edge label renderer example."""

    library = LIBRARY

    tag = "EdgeLabelRenderer"

    is_default = False


class EdgeText(reflex.Component):
    """You can use the <EdgeText /> component as a helper component to display text within your custom edges."""

    library = LIBRARY

    tag = "EdgeText"

    is_default = False

    x: reflex.Var[float]
    """The x position where the label should be rendered."""

    y: reflex.Var[float]
    """The y position where the label should be rendered."""

    label: reflex.Var[Any]
    """The label or custom element to render along the edge. This is commonly a text label or some custom controls."""

    label_style: reflex.Var[Mapping[str, Any]]
    """Custom styles to apply to the label."""

    label_show_bg: reflex.Var[bool]

    label_bg_style: reflex.Var[Mapping[str, Any]]

    label_bg_padding: reflex.Var[tuple[float, float]]

    label_bg_border_radius: reflex.Var[float]


class Handle(reflex.Component):
    """The <Handle /> component is used in your custom nodes to define connection points."""

    library = LIBRARY

    tag = "Handle"

    is_default = False

    type: reflex.Var[Literal["source", "target"]]
    """Type of the handle."""

    position: reflex.Var[Position]
    """The position of the handle relative to the node. In a horizontal flow source handles are typically Position.Right and in a vertical flow they are typically Position.Top."""

    is_connectable: reflex.Var[bool]
    """Should you be able to connect to/from this handle."""

    is_connectable_start: reflex.Var[bool]
    """Dictates whether a connection can start from this handle."""

    is_connectable_end: reflex.Var[bool]
    """Dictates whether a connection can end on this handle."""

    # TODO: skipped is_valid_connection because callbacks are weird
    # is_valid_connection: Callable[[Edge | Connection], bool]  # noqa: ERA001
    # """Called when a connection is dragged to this handle. You can use this callback to perform some custom validation logic based on the connection target and source, for example. Where possible, we recommend you move this logic to the isValidConnection prop on the main ReactFlow component for performance reasons."""

    on_connect: reflex.EventHandler[passthrough_event_spec(Connection)]
    """Callback called when connection is made"""


def _flip_mouse_event_and_xy_position_spec(
    event: reflex.vars.ObjectVar[JavascriptPointerEvent],
    position: reflex.Var[XYPosition],
) -> tuple[reflex.Var[XYPosition], reflex.Var[PointerEventInfo]]:
    return (position, pointer_event_spec(event)[0])


class MiniMap(reflex.Component):
    """The <MiniMap /> component can be used to render an overview of your flow. It renders each node as an SVG element and visualizes where the current viewport is in relation to the rest of the flow."""

    library = LIBRARY

    tag = "MiniMap"

    is_default = False

    position: reflex.Var[PanelPosition]
    """Position of minimap on pane."""

    on_click: reflex.EventHandler[_flip_mouse_event_and_xy_position_spec]
    """Callback called when minimap is clicked."""

    node_color: reflex.Var[str | Any]
    """Color of nodes on minimap."""

    node_stroke_color: reflex.Var[str | Any]
    """Stroke color of nodes on minimap."""

    node_class_name: reflex.Var[str | Any]
    """Class name applied to nodes on minimap."""

    node_border_radius: reflex.Var[float]
    """Border radius of nodes on minimap."""

    node_stroke_width: reflex.Var[float]
    """Stroke width of nodes on minimap."""

    node_component: reflex.Var[Any]
    """A custom component to render the nodes in the minimap. This component must render an SVG element!"""

    bg_color: reflex.Var[str]
    """Background color of minimap."""

    mask_color: reflex.Var[str]
    """The color of the mask that covers the portion of the minimap not currently visible in the viewport."""

    mask_stroke_color: reflex.Var[str]
    """Stroke color of mask representing viewport."""

    mask_stroke_width: reflex.Var[float]
    """Stroke width of mask representing viewport."""

    on_node_click: reflex.EventHandler[_flip_mouse_event_and_node_spec]
    """Callback called when node on minimap is clicked."""

    pannable: reflex.Var[bool]
    """Determines whether you can pan the viewport by dragging inside the minimap."""

    zoomable: reflex.Var[bool]
    """Determines whether you can zoom the viewport by scrolling inside the minimap."""

    aria_label: str | None
    """There is no text inside the minimap for a screen reader to use as an accessible name, so it’s important we provide one to make the minimap accessible. The default is sufficient, but you may want to replace it with something more relevant to your app or product."""

    inverse_pan: reflex.Var[bool]
    """Invert direction when panning the minimap viewport."""

    zoom_step: reflex.Var[float]
    """Step size for zooming in/out on minimap."""

    offset_scale: reflex.Var[float]
    """Scale factor for offsetting the minimap viewport."""


class ResizeParams(TypedDict):
    """Parameters for resizing a node."""

    x: float
    y: float
    width: float
    height: float


class ResizeParamsWithDirection(TypedDict):
    """Parameters for resizing a node with direction."""

    direction: list[float]


ControlLinePosition = Literal["left", "right", "top", "bottom"]

ControlPosition = (
    ControlLinePosition
    | Literal["top-left", "top-right", "bottom-left", "bottom-right"]
)

ResizeControlVariant = Literal["line", "handle"]

ResizeControlDirection = Literal["horizontal", "vertical"]


class NodeResizeControl(reflex.Component):
    """To create your own resizing UI, you can use the NodeResizeControl component where you can pass children (such as icons)."""

    library = LIBRARY

    tag = "NodeResizeControl"

    is_default = False

    node_id: reflex.Var[str]
    """Id of the node it is resizing."""

    color: reflex.Var[str]
    """Color of the resize handle."""

    min_width: reflex.Var[float]
    """Minimum width of node."""

    min_height: reflex.Var[float]
    """Minimum height of node."""

    max_width: reflex.Var[float]
    """Maximum width of node."""

    max_height: reflex.Var[float]
    """Maximum height of node."""

    keep_aspect_ratio: reflex.Var[bool]
    """Keep aspect ratio when resizing."""

    # TODO: Callbacks are weird
    # should_resize: ShouldResize  # noqa: ERA001
    # """Callback to determine if node should resize."""

    auto_scale: reflex.Var[bool]
    """Scale the controls with the zoom level."""

    on_resize_start: reflex.EventHandler[passthrough_event_spec(ResizeParams)]
    """Callback called when resizing starts."""

    on_resize: reflex.EventHandler[passthrough_event_spec(ResizeParamsWithDirection)]
    """Callback called when resizing."""

    on_resize_end: reflex.EventHandler[passthrough_event_spec(ResizeParams)]
    """Callback called when resizing ends."""

    position: reflex.Var[ControlPosition]
    """Position of the control."""

    variant: reflex.Var[ResizeControlVariant]
    """Variant of the control."""

    resize_direction: reflex.Var[ResizeControlDirection]
    """The direction the user can resize the node. If not provided, the user can resize in any direction."""


class NodeResizer(reflex.Component):
    """The <NodeResizer /> component can be used to add a resize functionality to your nodes. It renders draggable controls around the node to resize in all directions."""

    library = LIBRARY

    tag = "NodeResizer"

    is_default = False

    node_id: reflex.Var[str]
    """Id of the node it is resizing."""

    color: reflex.Var[str]
    """Color of the resize handle."""

    handle_class_name: reflex.Var[str]
    """Class name applied to handle."""

    handle_style: reflex.Var[Mapping[str, Any]]
    """Style applied to handle."""

    line_class_name: reflex.Var[str]
    """Class name applied to line."""

    line_style: reflex.Var[Mapping[str, Any]]
    """Style applied to line."""

    is_visible: reflex.Var[bool]
    """Are the controls visible."""

    min_width: reflex.Var[float]
    """Minimum width of node."""

    min_height: reflex.Var[float]
    """Minimum height of node."""

    max_width: reflex.Var[float]
    """Maximum width of node."""

    max_height: reflex.Var[float]
    """Maximum height of node."""

    keep_aspect_ratio: reflex.Var[bool]
    """Keep aspect ratio when resizing."""

    auto_scale: reflex.Var[bool]
    """Scale the controls with the zoom level."""

    # TODO: Wrapping callbacks is weird
    # should_resize: ShouldResize  # noqa: ERA001
    # """Callback to determine if node should resize."""

    on_resize_start: reflex.EventHandler[passthrough_event_spec(ResizeParams)]
    """Callback called when resizing starts."""

    on_resize: reflex.EventHandler[passthrough_event_spec(ResizeParamsWithDirection)]
    """Callback called when resizing."""

    on_resize_end: reflex.EventHandler[passthrough_event_spec(ResizeParams)]
    """Callback called when resizing ends."""


Align = Literal["center", "start", "end"]


class NodeToolbar(reflex.Component):
    """This component can render a toolbar or tooltip to one side of a custom node. This toolbar doesn’t scale with the viewport so that the content is always visible."""

    library = LIBRARY

    tag = "NodeToolbar"

    is_default = False

    node_id: reflex.Var[str | Sequence[str]]
    """By passing in an array of node id’s you can render a single tooltip for a group or collection of nodes."""

    is_visible: reflex.Var[bool]
    """If true, node toolbar is visible even if node is not selected."""

    position: reflex.Var[Position]
    """Position of the toolbar relative to the node."""

    offset: reflex.Var[float]
    """The space between the node and the toolbar, measured in pixels."""

    align: reflex.Var[Align]
    """Align the toolbar relative to the node."""


class Panel(reflex.Component):
    """The <Panel /> component helps you position content above the viewport. It is used internally by the <MiniMap /> and <Controls /> components."""

    library = LIBRARY

    tag = "Panel"

    is_default = False

    position: reflex.Var[PanelPosition]
    """The position of the panel."""


class ViewportPortal(reflex.Component):
    """<ViewportPortal /> component can be used to add components to the same viewport of the flow where nodes and edges are rendered. This is useful when you want to render your own components that adhere to the same coordinate system as the nodes & edges and are also affected by zooming and panning."""

    library = LIBRARY

    tag = "ViewportPortal"

    is_default = False


flow = Flow.create
provider = FlowProvider.create
background = Background.create
base_edge = BaseEdge.create
control_button = ControlButton.create
controls = Controls.create
edge_label_renderer = EdgeLabelRenderer.create
edge_text = EdgeText.create
handle = Handle.create
mini_map = MiniMap.create
node_resize_control = NodeResizeControl.create
node_resizer = NodeResizer.create
node_toolbar = NodeToolbar.create
panel = Panel.create
viewport_portal = ViewportPortal.create
