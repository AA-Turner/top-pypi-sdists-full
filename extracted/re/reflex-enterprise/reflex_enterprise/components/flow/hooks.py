"""Hooks for the flow component."""

from typing import TYPE_CHECKING, Any, Mapping, Sequence, TypedDict

import reflex

from .flow import LIBRARY
from .types import (
    ConnectionState,
    ConnectionStateVar,
    Edge,
    EdgeVar,
    HandleType,
    Id,
    InternalNode,
    InternalNodeVar,
    Node,
    NodeConnection,
    NodeVar,
    Rect,
    RectVar,
    Viewport,
    ViewportVar,
    XYPosition,
    XYPositionVar,
)

react_flow_instance = reflex.Var(
    "reactFlowInstance",
    _var_data=reflex.vars.VarData(
        hooks=["const reactFlowInstance = useReactFlow();"],
        imports={LIBRARY: ["useReactFlow"]},
    ),
).to(dict)


# TODO: wrap deleteElements, getHandleConnections, getNodeConnections
# TODO: wrap isNodeIntersecting
# TODO: wrap zoomIn, zoomOut, zoomTo, getZoom, setViewport, getViewport
# TODO: wrap setCenter, fitBounds, viewportInitialized, fitView


def get_nodes() -> reflex.vars.ArrayVar[list[Node]]:
    """Returns an array of all nodes in the flow."""
    return (
        react_flow_instance["getNodes"]
        .to(reflex.vars.FunctionVar)
        .call()
        .to(list[Node])
    )  # pyright: ignore[reportReturnType]


def set_nodes(
    nodes: Sequence[Node] | reflex.Var[Sequence[Node]],
) -> reflex.vars.base.NoneVar:
    """Sets the nodes in the flow."""
    return react_flow_instance["setNodes"].to(reflex.vars.FunctionVar).call(nodes)  # pyright: ignore[reportReturnType]


def add_nodes(
    nodes: Node | Sequence[Node] | reflex.Var[Node | Sequence[Node]],
) -> reflex.vars.base.NoneVar:
    """Adds nodes to the flow."""
    return react_flow_instance["addNodes"].to(reflex.vars.FunctionVar).call(nodes)  # pyright: ignore[reportReturnType]


def get_node(
    id: str | reflex.Var[str],
) -> NodeVar | reflex.vars.base.NoneVar:
    """Returns a node by its ID."""
    return react_flow_instance["getNode"].to(reflex.vars.FunctionVar).call(id)  # pyright: ignore[reportReturnType]


def get_internal_node(
    id: str | reflex.Var[str],
) -> InternalNodeVar | reflex.vars.base.NoneVar:
    """Returns an internal node by its ID."""
    return (
        react_flow_instance["getInternalNode"]
        .to(reflex.vars.FunctionVar)
        .call(id)
        .to(InternalNode | None)
    )  # pyright: ignore[reportReturnType]


def get_edges() -> reflex.vars.ArrayVar[list[Edge]]:
    """Returns an array of all edges in the flow."""
    return (
        react_flow_instance["getEdges"]
        .to(reflex.vars.FunctionVar)
        .call()
        .to(list[Edge])
    )


def set_edges(
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
) -> reflex.vars.base.NoneVar:
    """Sets the edges in the flow."""
    return react_flow_instance["setEdges"].to(reflex.vars.FunctionVar).call(edges)  # pyright: ignore[reportReturnType]


def add_edges(
    edges: Edge | Sequence[Edge] | reflex.Var[Edge | Sequence[Edge]],
) -> reflex.vars.base.NoneVar:
    """Adds edges to the flow."""
    return react_flow_instance["addEdges"].to(reflex.vars.FunctionVar).call(edges)  # pyright: ignore[reportReturnType]


def get_edge(
    id: str | reflex.Var[str],
) -> EdgeVar | reflex.vars.base.NoneVar:
    """Returns an edge by its ID."""
    return (
        react_flow_instance["getEdge"]
        .to(reflex.vars.FunctionVar)
        .call(id)
        .to(Edge | None)
    )  # pyright: ignore[reportReturnType]


class ReactFlowJsonObject(TypedDict):
    """Represents the JSON object for the React Flow state."""

    nodes: list[Node]
    edges: list[Edge]
    viewport: Viewport


class ReactFlowJsonObjectVar(reflex.vars.ObjectVar[ReactFlowJsonObject]):
    """Var for ReactFlowJsonObject."""

    if TYPE_CHECKING:
        nodes: reflex.vars.ArrayVar[list[Node]]
        edges: reflex.vars.ArrayVar[list[Edge]]
        viewport: ViewportVar


def to_object() -> ReactFlowJsonObjectVar:
    """Converts the React Flow state to a JSON object."""
    return react_flow_instance["toObject"].to(reflex.vars.FunctionVar).call()  # pyright: ignore[reportReturnType]


def update_node(
    id: str | reflex.Var[str],
    node_update: Node | reflex.Var[Node],
    *,
    replace: bool | reflex.Var[bool] | None = None,
):
    """Updates a node in the flow."""
    options = (
        {
            "replace": replace,
        }
        if replace is not None
        else {}
    )
    return (
        react_flow_instance["updateNode"]
        .to(reflex.vars.FunctionVar)
        .call(id, node_update, options)
    )  # pyright: ignore[reportReturnType]


def update_node_data(
    id: str | reflex.Var[str],
    data_update: Mapping[str, Any] | reflex.Var[Mapping[str, Any]],
    *,
    replace: bool | reflex.Var[bool] | None = None,
) -> reflex.vars.base.NoneVar:
    """Updates a node's data in the flow."""
    options = (
        {
            "replace": replace,
        }
        if replace is not None
        else {}
    )
    return (
        react_flow_instance["updateNodeData"]
        .to(reflex.vars.FunctionVar)
        .call(id, data_update, options)
    )  # pyright: ignore[reportReturnType]


def update_edge(
    id: str | reflex.Var[str],
    edge_update: Edge | reflex.Var[Edge],
    *,
    replace: bool | reflex.Var[bool] | None = None,
) -> reflex.vars.base.NoneVar:
    """Updates an edge in the flow."""
    options = (
        {
            "replace": replace,
        }
        if replace is not None
        else {}
    )
    return (
        react_flow_instance["updateEdge"]
        .to(reflex.vars.FunctionVar)
        .call(id, edge_update, options)
    )  # pyright: ignore[reportReturnType]


def update_edge_data(
    id: str | reflex.Var[str],
    data_update: Mapping[str, Any] | reflex.Var[Mapping[str, Any]],
    *,
    replace: bool | reflex.Var[bool] | None = None,
) -> reflex.vars.base.NoneVar:
    """Updates an edge's data in the flow."""
    options = (
        {
            "replace": replace,
        }
        if replace is not None
        else {}
    )
    return (
        react_flow_instance["updateEdgeData"]
        .to(reflex.vars.FunctionVar)
        .call(id, data_update, options)
    )  # pyright: ignore[reportReturnType]


def get_nodes_bounds(
    nodes: Sequence[str | Node] | reflex.Var[Sequence[str | Node]],
) -> RectVar:
    """Returns the bounds of the given nodes."""
    return (
        react_flow_instance["getNodesBounds"]
        .to(reflex.vars.FunctionVar)
        .call(nodes)
        .to(Rect)
    )  # pyright: ignore[reportReturnType]


def screen_to_flow_position(
    *,
    x: float | reflex.Var[float],
    y: float | reflex.Var[float],
    snap_to_grid: bool | reflex.Var[bool] | None = None,
) -> XYPositionVar:
    """With this function you can translate a screen pixel position to a flow position. It is useful for implementing drag and drop from a sidebar for example."""
    options = {"snapToGrid": snap_to_grid} if snap_to_grid is not None else {}
    return (
        react_flow_instance["screenToFlowPosition"]
        .to(reflex.vars.FunctionVar)
        .call({"x": x, "y": y}, options)
    ).to(XYPosition)  # pyright: ignore[reportReturnType]


def flow_to_screen_position(
    *,
    x: float | reflex.Var[float],
    y: float | reflex.Var[float],
) -> XYPositionVar:
    """Translate a position inside the flow’s canvas to a screen pixel position."""
    return (
        react_flow_instance["flowToScreenPosition"]
        .to(reflex.vars.FunctionVar)
        .call({"x": x, "y": y})
    ).to(XYPosition)  # pyright: ignore[reportReturnType]


# This doesn't wrap getNodeConnections because that one is weird
def get_node_connections(
    *,
    id: str | reflex.Var[str] | None = None,
    handle_type: HandleType | reflex.Var[HandleType] | None = None,
    handle_id: str | reflex.Var[str | None] | None = None,
) -> reflex.vars.ArrayVar[list[NodeConnection]]:
    """This hook returns an array of connections on a specific node, handle type ("source", "target") or handle ID."""
    options = reflex.Var.create(
        {
            "id": id,
            "handleType": handle_type,
            "handleId": handle_id,
        }
    )
    id = reflex.vars.get_unique_variable_name()
    return (
        reflex.Var(
            f"connections_{id}",
            _var_data=reflex.vars.VarData.merge(
                options._get_all_var_data(),
                reflex.vars.VarData(
                    hooks=[
                        f"const connections_{id} = useNodeConnections({options!s});"
                    ],
                    imports={
                        LIBRARY: ["useNodeConnections"],
                    },
                ),
            ),
        )
    ).to(list[NodeConnection])


def get_connection() -> ConnectionStateVar:
    """The useConnection hook returns the current connection state when there is an active connection interaction.

    If no connection interaction is active, it returns null for every property.

    A typical use case for this hook is to colorize handles based on a certain condition (e.g. if the connection is valid or not).
    """
    id = reflex.vars.get_unique_variable_name()
    return (
        reflex.Var(
            f"connection_{id}",
            _var_data=reflex.vars.VarData(
                hooks=[f"const connection_{id} = useConnection();"],
                imports={
                    LIBRARY: ["useConnection"],
                },
            ),
        )
    ).to(ConnectionState)  # pyright: ignore[reportReturnType]


def get_intersecting_nodes(
    node: Node | Rect | Id | reflex.Var[Node | Rect | Id],
    *,
    partially: bool | reflex.Var[bool] = True,
    nodes: Sequence[Node | Rect | Id]
    | reflex.Var[Sequence[Node | Rect | Id]]
    | None = None,
) -> reflex.vars.ArrayVar[list[Node]]:
    """Find all the nodes currently intersecting with a given node or rectangle.

    The partially parameter can be set to true to include nodes that are only partially intersecting.
    """
    return (
        react_flow_instance["getIntersectingNodes"]
        .to(reflex.vars.FunctionVar)
        .call(node, partially, nodes)
        .to(list[Node])
    )
