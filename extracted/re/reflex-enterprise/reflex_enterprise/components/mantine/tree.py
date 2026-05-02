"""Tree component for displaying nested data structures."""

from __future__ import annotations

from typing import Any, TypedDict

import reflex as rx

from reflex_enterprise.components.mantine.base import MantineCoreBase


class TreeNodeData(TypedDict):
    """Data structure for a node in the Tree."""

    value: str
    label: Any
    children: list[NestedTreeNode | LeafNode]


class NestedTreeNode(TypedDict):
    """Type for a node in the nested tree structure."""

    value: str
    label: Any
    children: list[NestedTreeNode2 | LeafNode]


class NestedTreeNode2(TypedDict):
    """Type for a node in the nested tree structure."""

    value: str
    label: Any
    children: list[NestedTreeNode3 | LeafNode]


class NestedTreeNode3(TypedDict):
    """Type for a node in the nested tree structure."""

    value: str
    label: Any
    children: list[NestedTreeNode4 | LeafNode]


class NestedTreeNode4(TypedDict):
    """Type for a node in the nested tree structure."""

    value: str
    label: Any
    children: list[LeafNode]


class LeafNode(TypedDict):
    """Type for a leaf node in the tree structure."""

    value: str
    label: Any


# Tree component
class Tree(MantineCoreBase):
    """Tree component to display nested data."""

    tag = "Tree"

    # Data for the tree structure. Expects a list of TreeNodeData objects or dicts.
    data: rx.Var[list[TreeNodeData]]

    # Key of the object property used for node label. Defaults to 'label'.
    label_key: rx.Var[str]

    # Indentation multiplier in px. Defaults to 0.
    level: rx.Var[int]

    # Key of the object property used for node value. Defaults to 'value'.
    value_key: rx.Var[str]

    # Controlled state for expanded nodes (list of node values).
    value: rx.Var[list[str]]

    # Initial state for uncontrolled expanded nodes.
    default_value: rx.Var[list[str]]

    # Event handler called when a node is clicked. Passes the node data (as dict).
    on_node_click: rx.EventHandler[lambda node_dict: [node_dict]]

    # Event handler called when a node is collapsed. Passes the node data (as dict).
    on_node_collapse: rx.EventHandler[lambda node_dict: [node_dict]]

    # Event handler called when a node is expanded. Passes the node data (as dict).
    on_node_expand: rx.EventHandler[lambda node_dict: [node_dict]]

    # Event handler called when the expanded nodes change (controlled mode). Passes the new list of expanded node values.
    on_change: rx.EventHandler[lambda value_list: [value_list]]


# Create alias for the Tree component
tree = Tree.create
