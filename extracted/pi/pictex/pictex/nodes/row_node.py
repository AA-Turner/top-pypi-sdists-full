"""RowNode - horizontal flex container.

Layout is handled by stretchable with FlexDirection.ROW.
All layout computation (distribution, alignment, sizing) delegated to stretchable.
"""
from .container_node import ContainerNode


class RowNode(ContainerNode):
    """Row container - children laid out horizontally.
    
    Stretchable handles:
    - Horizontal distribution (justify-content)
    - Vertical alignment (align-items)
    - Gap between items
    - Flex sizing (grow/shrink)
    """
    pass
