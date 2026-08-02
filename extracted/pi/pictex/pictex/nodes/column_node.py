"""ColumnNode - vertical flex container.

Layout is handled by stretchable with FlexDirection.COLUMN.
All layout computation (distribution, alignment, sizing) delegated to stretchable.
"""
from .container_node import ContainerNode


class ColumnNode(ContainerNode):
    """Column container - children laid out vertically.
    
    Stretchable handles:
    - Vertical distribution (justify-content)
    - Horizontal alignment (align-items)
    - Gap between items
    - Flex sizing (grow/shrink)
    """
    pass
