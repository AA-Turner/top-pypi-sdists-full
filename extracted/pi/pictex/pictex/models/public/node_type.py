from enum import Enum

class NodeType(str, Enum):
    """Enumeration of possible node types in the render tree."""
    TEXT = "text"
    ROW = "row"
    COLUMN = "column"
    ELEMENT = "element"