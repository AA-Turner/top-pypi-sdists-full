"""
Enums for legacy_python compatibility.

Provides FindDirection and Traverse enums that match the legacy_python model.py versions,
used for document tree navigation operations.
"""
from enum import Enum


class FindDirection(Enum):
    """
    Enum class for defining the direction of search in a tree structure.

    Attributes:
        CHILDREN (int): Represents the direction towards children nodes.
        PARENT (int): Represents the direction towards parent node.
    """
    CHILDREN = 1
    PARENT = 2


class Traverse(Enum):
    """
    An enumeration class that represents different types of traversals.

    Attributes:
        SIBLING (int): Represents traversal to a sibling.
        CHILDREN (int): Represents traversal to children.
        PARENT (int): Represents traversal to a parent.
        ALL (int): Represents traversal to all types of nodes.

    Note: Values match legacy Python and Go's TraverseOption in constants.go (1-indexed)
    """
    SIBLING = 1
    CHILDREN = 2
    PARENT = 3
    ALL = 4