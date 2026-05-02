from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .box import Box
from .node_type import NodeType

@dataclass(frozen=True)
class RenderNode:
    """Represents a rendered node in the composition tree.
    
    This class provides a simple read-only view of the internal render tree,
    exposing the bounds and hierarchical structure of rendered elements.
    
    Attributes:
        bounds (Box): The bounding rectangle of this node (border bounds).
        children (List[RenderNode]): List of child nodes in the render tree.
        node_type (NodeType): The type of node (NodeType.TEXT, NodeType.ROW, etc.).
    """
    bounds: Box
    children: List[RenderNode]
    node_type: NodeType
    
    def visit_children(self, visitor_func):
        """Recursively visits all children nodes.
        
        Args:
            visitor_func: A function that takes a RenderNode as argument.
        """
        for child in self.children:
            visitor_func(child)
            child.visit_children(visitor_func)
    
    def find_nodes_by_type(self, node_type: NodeType) -> List[RenderNode]:
        """Finds all nodes in the tree with the specified type.
        
        Args:
            node_type: The type of nodes to find.
            
        Returns:
            A list of RenderNode instances matching the specified type.
        """
        result = []
        if self.node_type == node_type:
            result.append(self)
        
        for child in self.children:
            result.extend(child.find_nodes_by_type(node_type))
        
        return result
