from __future__ import annotations
import skia
from stretchable import Edge, Node as StretchableNode
from ..utils import to_int_skia_rect


class LayoutResult:
    """Encapsulates layout computation results for a node.
    
    This wrapper provides a clean API for accessing bounds computed by stretchable,
    allowing Node to delegate bounds retrieval without depending on stretchable directly.
    """
    
    def __init__(self, stretchable_node: StretchableNode, offset_x: float = 0, offset_y: float = 0):
        """Initialize with the corresponding stretchable node.
        
        Args:
            stretchable_node: The StretchableNode containing computed layout.
            offset_x: Additional X offset to apply (for FIXED positioning).
            offset_y: Additional Y offset to apply (for FIXED positioning).
        """
        self._stretchable_node: StretchableNode = stretchable_node
        self._offset_x = offset_x
        self._offset_y = offset_y

    @property
    def stretchable_node(self) -> StretchableNode:
        return self._stretchable_node

    @property
    def offset_x(self) -> float:
        return self._offset_x
    
    @property
    def offset_y(self) -> float:
        return self._offset_y
    
    def get_content_bounds(self) -> skia.Rect:
        """Get content area bounds in absolute canvas coordinates.
        
        Returns:
            Rectangle defining the content area.
        """
        box = self._stretchable_node.get_box(Edge.CONTENT, relative=False)
        return to_int_skia_rect(skia.Rect.MakeXYWH(
            box.x + self._offset_x, box.y + self._offset_y, box.width, box.height
        ))
    
    def get_padding_bounds(self) -> skia.Rect:
        """Get padding box bounds in absolute canvas coordinates.
        
        Returns:
            Rectangle defining the padding box (content + padding).
        """
        box = self._stretchable_node.get_box(Edge.PADDING, relative=False)
        return to_int_skia_rect(skia.Rect.MakeXYWH(
            box.x + self._offset_x, box.y + self._offset_y, box.width, box.height
        ))
    
    def get_border_bounds(self) -> skia.Rect:
        """Get border box bounds in absolute canvas coordinates.
        
        Returns:
            Rectangle defining the border box (padding + border).
        """
        box = self._stretchable_node.get_box(Edge.BORDER, relative=False)
            
        return to_int_skia_rect(skia.Rect.MakeXYWH(
            box.x + self._offset_x, box.y + self._offset_y, box.width, box.height
        ))
    
    def get_margin_bounds(self) -> skia.Rect:
        """Get margin box bounds in absolute canvas coordinates.
        
        Returns:
            Rectangle defining the margin box (border + margin).
        """
        box = self._stretchable_node.get_box(Edge.MARGIN, relative=False)
        return to_int_skia_rect(skia.Rect.MakeXYWH(
            box.x + self._offset_x, box.y + self._offset_y, box.width, box.height
        ))
