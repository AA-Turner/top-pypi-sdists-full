"""Utility functions for working with flow components."""

from typing import TYPE_CHECKING, Any, Sequence, TypedDict

import reflex

from .flow import LIBRARY
from .types import Connection, Edge, EdgeChange, Node, NodeChange, Position


class Path(TypedDict):
    """Represents an SVG path.

    Args:
        path: the path to use in an SVG <path> element.
        label_x: the x position you can use to render a label for this edge.
        label_y: the y position you can use to render a label for this edge.
        offset_x: the absolute difference between the source x position and the x position of the middle of this path.
        offset_y: the absolute difference between the source y position and the y position of the middle of this path.
    """

    path: str
    label_x: float
    label_y: float
    offset_x: float
    offset_y: float


class PathVar(reflex.vars.ObjectVar[Path]):
    """Represents a SVG path variable."""

    if TYPE_CHECKING:
        path: reflex.vars.StringVar
        label_x: reflex.vars.NumberVar[float]
        label_y: reflex.vars.NumberVar[float]
        offset_x: reflex.vars.NumberVar[float]
        offset_y: reflex.vars.NumberVar[float]


def _array_return_to_object(array: reflex.vars.ArrayVar[Any]):
    return reflex.Var.create(
        {
            "path": array[0],
            "label_x": array[1],
            "label_y": array[2],
            "offset_x": array[3],
            "offset_y": array[4],
        }
    )


def get_simple_bezier_path(
    *,
    source_x: float | reflex.Var[float],
    source_y: float | reflex.Var[float],
    target_x: float | reflex.Var[float],
    target_y: float | reflex.Var[float],
    source_position: Position | reflex.Var[Position] = "bottom",
    target_position: Position | reflex.Var[Position] = "top",
):
    """The getSimpleBezierPath util returns everything you need to render a simple bezier edge between two nodes."""
    unique_id = reflex.vars.get_unique_variable_name()
    variable_name = f"simple_bezier_path_{unique_id}"

    get_simple_bezier_path_call = reflex.vars.FunctionStringVar.create(
        "getSimpleBezierPath"
    ).call(
        {
            "sourceX": source_x,
            "sourceY": source_y,
            "targetX": target_x,
            "targetY": target_y,
            "sourcePosition": source_position,
            "targetPosition": target_position,
        }
    )

    array_name = f"_path_array_{unique_id}"

    result_var = _array_return_to_object(reflex.Var(array_name).to(list))

    return reflex.Var(
        variable_name,
        _var_data=reflex.vars.VarData(
            hooks={
                f"const {array_name} = {get_simple_bezier_path_call!s};": get_simple_bezier_path_call._get_all_var_data(),
                f"const {variable_name} = {result_var!s};": None,
            },
            imports={LIBRARY: ["getSimpleBezierPath"]},
        ),
    ).to(Path)  # pyright: ignore[reportReturnType]


def get_bezier_path(
    *,
    source_x: float | reflex.Var[float],
    source_y: float | reflex.Var[float],
    target_x: float | reflex.Var[float],
    target_y: float | reflex.Var[float],
    source_position: Position | reflex.Var[Position] = "bottom",
    target_position: Position | reflex.Var[Position] = "top",
    curvature: float | reflex.Var[float] = 0.5,
) -> PathVar:
    """Returns everything you need to render a bezier edge between two nodes."""
    unique_id = reflex.vars.get_unique_variable_name()
    variable_name = f"bezier_path_{unique_id}"

    get_bezier_path_call = reflex.vars.FunctionStringVar.create("getBezierPath").call(
        {
            "sourceX": source_x,
            "sourceY": source_y,
            "targetX": target_x,
            "targetY": target_y,
            "sourcePosition": source_position,
            "targetPosition": target_position,
            "curvature": curvature,
        }
    )

    array_name = f"_path_array_{unique_id}"

    result_var = _array_return_to_object(reflex.Var(array_name).to(list))

    return reflex.Var(
        variable_name,
        _var_data=reflex.vars.VarData(
            hooks={
                f"const {array_name} = {get_bezier_path_call!s};": get_bezier_path_call._get_all_var_data(),
                f"const {variable_name} = {result_var!s};": None,
            },
            imports={LIBRARY: ["getBezierPath"]},
        ),
    ).to(Path)  # pyright: ignore[reportReturnType]


def get_straight_path(
    source_x: float | reflex.Var[float],
    source_y: float | reflex.Var[float],
    target_x: float | reflex.Var[float],
    target_y: float | reflex.Var[float],
):
    """Calculates the straight line path between two points."""
    unique_id = reflex.vars.get_unique_variable_name()
    variable_name = f"straight_path_{unique_id}"

    get_straight_path_call = reflex.vars.FunctionStringVar.create(
        "getStraightPath"
    ).call(
        {
            "sourceX": source_x,
            "sourceY": source_y,
            "targetX": target_x,
            "targetY": target_y,
        }
    )

    array_name = f"_path_array_{unique_id}"

    result_var = _array_return_to_object(reflex.Var(array_name).to(list))

    return reflex.Var(
        variable_name,
        _var_data=reflex.vars.VarData(
            hooks={
                f"const {array_name} = {get_straight_path_call!s};": get_straight_path_call._get_all_var_data(),
                f"const {variable_name} = {result_var!s};": None,
            },
            imports={LIBRARY: ["getStraightPath"]},
        ),
    ).to(Path)  # pyright: ignore[reportReturnType]


def get_smooth_step_path(
    *,
    source_x: float | reflex.Var[float],
    source_y: float | reflex.Var[float],
    target_x: float | reflex.Var[float],
    target_y: float | reflex.Var[float],
    source_position: Position | reflex.Var[Position] = "bottom",
    target_position: Position | reflex.Var[Position] = "top",
    border_radius: float | reflex.Var[float] = 5,
    center_x: float | reflex.Var[float] | None = None,
    center_y: float | reflex.Var[float] | None = None,
    offset: float | reflex.Var[float] = 20,
    step_position: float | reflex.Var[float] = 0.5,
) -> PathVar:
    """The getSmoothStepPath util returns everything you need to render a stepped path between two nodes.

    The borderRadius property can be used to choose how rounded the corners of those steps are.
    """
    unique_id = reflex.vars.get_unique_variable_name()
    variable_name = f"smooth_step_path_{unique_id}"

    get_smooth_step_path_call = reflex.vars.FunctionStringVar.create(
        "getSmoothStepPath"
    ).call(
        {
            "sourceX": source_x,
            "sourceY": source_y,
            "targetX": target_x,
            "targetY": target_y,
            "sourcePosition": source_position,
            "targetPosition": target_position,
            "borderRadius": border_radius,
            "centerX": center_x,
            "centerY": center_y,
            "offset": offset,
            "stepPosition": step_position,
        }
    )

    array_name = f"_path_array_{unique_id}"

    result_var = _array_return_to_object(reflex.Var(array_name).to(list))

    return reflex.Var(
        variable_name,
        _var_data=reflex.vars.VarData(
            hooks={
                f"const {array_name} = {get_smooth_step_path_call!s};": get_smooth_step_path_call._get_all_var_data(),
                f"const {variable_name} = {result_var!s};": None,
            },
            imports={LIBRARY: ["getSmoothStepPath"]},
        ),
    ).to(Path)  # pyright: ignore[reportReturnType]


def apply_node_changes(
    nodes: Sequence[Node] | reflex.Var[Sequence[Node]],
    changes: Sequence[NodeChange] | reflex.Var[Sequence[NodeChange]],
) -> reflex.vars.ArrayVar[list[Node]]:
    """Applies changes to nodes in the flow."""
    return (
        reflex.vars.FunctionStringVar.create(
            "applyNodeChanges",
            _var_data=reflex.vars.VarData(
                imports={LIBRARY: ["applyNodeChanges"]},
            ),
        )
        .call(changes, nodes)
        .to(list[Node])
    )


def apply_edge_changes(
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
    changes: Sequence[EdgeChange] | reflex.Var[Sequence[EdgeChange]],
) -> reflex.vars.ArrayVar[list[Edge]]:
    """Applies changes to edges in the flow."""
    return (
        reflex.vars.FunctionStringVar.create(
            "applyEdgeChanges",
            _var_data=reflex.vars.VarData(
                imports={LIBRARY: ["applyEdgeChanges"]},
            ),
        )
        .call(changes, edges)
        .to(list[Edge])
    )


def add_edge(
    params: Edge | Connection | reflex.Var[Edge | Connection],
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
) -> reflex.vars.ArrayVar[list[Edge]]:
    """Creates a new edge in the flow."""
    return reflex.vars.FunctionStringVar.create(
        "addEdge",
        _var_data=reflex.vars.VarData(
            imports={LIBRARY: ["addEdge"]},
        ),
    ).call(params, edges)  # pyright: ignore[reportReturnType]


def get_incomers(
    *, node_id: str, nodes: Sequence[Node], edges: Sequence[Edge]
) -> list[Node]:
    """Returns all incoming nodes connected to the given node."""
    if not node_id:
        return []
    incomers_ids = {edge["source"] for edge in edges if edge["target"] == node_id}
    return [n for n in nodes if n["id"] in incomers_ids]


def get_incomers_var(
    *,
    node_id: str | reflex.Var[str],
    nodes: Sequence[Node] | reflex.Var[Sequence[Node]],
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
) -> reflex.vars.ArrayVar[list[Node]]:
    """Returns all incoming nodes connected to the given node."""
    return (
        reflex.vars.FunctionStringVar.create(
            "getIncomers",
            _var_data=reflex.vars.VarData(
                imports={LIBRARY: ["getIncomers"]},
            ),
        )
        .call({"id": node_id}, nodes, edges)
        .to(list[Node])
    )


def get_outgoers(
    *, node_id: str, nodes: Sequence[Node], edges: Sequence[Edge]
) -> list[Node]:
    """Returns all outgoing nodes connected to the given node."""
    if not node_id:
        return []
    outgoers_ids = {edge["target"] for edge in edges if edge["source"] == node_id}
    return [n for n in nodes if n["id"] in outgoers_ids]


def get_outgoers_var(
    *,
    node_id: str | reflex.Var[str],
    nodes: Sequence[Node] | reflex.Var[Sequence[Node]],
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
) -> reflex.vars.ArrayVar[list[Node]]:
    """Returns all outgoing nodes connected to the given node."""
    return (
        reflex.vars.FunctionStringVar.create(
            "getOutgoers",
            _var_data=reflex.vars.VarData(
                imports={LIBRARY: ["getOutgoers"]},
            ),
        )
        .call({"id": node_id}, nodes, edges)
        .to(list[Node])
    )


def get_connected_edges(*, nodes: Sequence[Node], edges: Sequence[Edge]) -> list[Edge]:
    """Returns all edges connected to the given nodes."""
    node_ids = {node["id"] for node in nodes}
    return [
        edge
        for edge in edges
        if edge["source"] in node_ids or edge["target"] in node_ids
    ]


def get_connected_edges_var(
    *,
    nodes: Sequence[Node] | reflex.Var[Sequence[Node]],
    edges: Sequence[Edge] | reflex.Var[Sequence[Edge]],
) -> reflex.vars.ArrayVar[list[Edge]]:
    """Returns all edges connected to the given nodes."""
    return (
        reflex.vars.FunctionStringVar.create(
            "getConnectedEdges",
            _var_data=reflex.vars.VarData(
                imports={LIBRARY: ["getConnectedEdges"]},
            ),
        )
        .call(nodes, edges)
        .to(list[Edge])
    )
