"""Style mapping for pictex to stretchable conversion.

Converts pictex Style properties to stretchable (Taffy) style objects,
enabling CSS Flexbox layout computation.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from stretchable.style import (
    Style as StretchableStyle,
    FlexDirection,
    AlignItems,
    AlignSelf as StretchableAlignSelf,
    FlexWrap as StretchableFlexWrap,
    JustifyContent,
    Display,
    Position as StretchablePosition,
    AUTO,
    PCT,
)

if TYPE_CHECKING:
    from ..nodes import Node
    from ..models import SizeValue, Padding, Margin, Border, Position


class StyleMapper:
    """Converts pictex styles to stretchable styles for layout computation."""

    def create_row_style(self, node: 'Node') -> StretchableStyle:
        computed = node.computed_styles
        return self._create_container_style(
            node,
            flex_direction=FlexDirection.ROW,
            justify_content=self._to_justify_content(computed.justify_content.get().value),
            align_items=self._to_align_items(computed.align_items.get().value),
        )

    def create_column_style(self, node: 'Node') -> StretchableStyle:
        computed = node.computed_styles
        return self._create_container_style(
            node,
            flex_direction=FlexDirection.COLUMN,
            justify_content=self._to_justify_content(computed.justify_content.get().value),
            align_items=self._to_align_items(computed.align_items.get().value),
        )

    def create_leaf_style(self, node: 'Node') -> StretchableStyle:
        return self._create_container_style(node)

    def _create_container_style(
        self,
        node: 'Node',
        flex_direction: Optional[FlexDirection] = None,
        justify_content: Optional[JustifyContent] = None,
        align_items: Optional[AlignItems] = None,
    ) -> StretchableStyle:
        computed = node.computed_styles
        
        kwargs = {
            'display': Display.FLEX,
            'padding': self._to_spacing(computed.padding.get()),
            'margin': self._to_spacing(computed.margin.get()),
            'border': self._to_border_width(computed.border.get()),
            'gap': computed.gap.get(),
        }
        
        if flex_direction is not None:
            kwargs['flex_direction'] = flex_direction
        if justify_content is not None:
            kwargs['justify_content'] = justify_content
        if align_items is not None:
            kwargs['align_items'] = align_items
        
        self._apply_size(node, kwargs)
        self._apply_flex_properties(computed, kwargs)
        self._apply_position(computed, kwargs)
        
        return StretchableStyle(**kwargs)

    def _apply_size(self, node: 'Node', kwargs: dict) -> None:
        """Apply width/height and constraints to style kwargs."""
        computed = node.computed_styles
        
        width_value = computed.width.get()
        height_value = computed.height.get()
        kwargs['size'] = self._to_size_tuple(node, width_value, height_value)
        
        min_w, min_h = computed.min_width.get(), computed.min_height.get()
        if min_w or min_h:
            kwargs['min_size'] = self._to_size_tuple(node, min_w, min_h)
        
        max_w, max_h = computed.max_width.get(), computed.max_height.get()
        if max_w or max_h:
            kwargs['max_size'] = self._to_size_tuple(node, max_w, max_h)
        
        aspect_ratio = computed.aspect_ratio.get()
        if aspect_ratio:
            kwargs['aspect_ratio'] = aspect_ratio

    def _apply_flex_properties(self, computed, kwargs: dict) -> None:
        """Apply flex_grow, flex_shrink, align_self, flex_wrap."""
        flex_grow = computed.flex_grow.get()
        if flex_grow > 0:
            kwargs['flex_grow'] = flex_grow
        
        flex_shrink = computed.flex_shrink.get()
        if flex_shrink != 1.0:
            kwargs['flex_shrink'] = flex_shrink
        
        align_self = computed.align_self.get()
        if align_self.value != 'auto':
            kwargs['align_self'] = self._to_align_self(align_self.value)
        
        flex_wrap = computed.flex_wrap.get()
        if flex_wrap.value != 'nowrap':
            kwargs['flex_wrap'] = self._to_flex_wrap(flex_wrap.value)

    def _apply_position(self, computed, kwargs: dict) -> None:
        """Apply position type and insets."""
        position_config: 'Position' = computed.position.get()
        if not position_config:
            return
        
        position_type, inset = self._to_position_and_inset(position_config)
        if position_type:
            kwargs['position'] = position_type
        if inset:
            kwargs['inset'] = inset

    def _to_size_tuple(self, node: 'Node', width: Optional['SizeValue'], height: Optional['SizeValue']) -> tuple:
        w = self._to_length(node, width, 'width') if width else AUTO
        h = self._to_length(node, height, 'height') if height else AUTO
        return (w, h)

    def _to_length(self, node: 'Node', size_value: Optional['SizeValue'], dimension: str):
        if not size_value:
            return AUTO
        
        mode = size_value.mode
        value = size_value.value
        
        if mode in ('auto', 'fit-content'):
            return AUTO
        elif mode == 'absolute':
            return value
        elif mode == 'percent':
            return value * PCT
        elif mode == 'fit-background-image':
            return self._get_background_image_size(node, dimension)
        
        return AUTO

    def _get_background_image_size(self, node: 'Node', dimension: str) -> float:
        bg_image_info = node.computed_styles.background_image.get()
        if bg_image_info:
            bg_image = bg_image_info.get_skia_image()
            if bg_image:
                return float(bg_image.width() if dimension == 'width' else bg_image.height())
        return AUTO

    def _to_position_and_inset(self, position: 'Position') -> tuple:
        from ..models import PositionType
        
        position_type = None
        if position.type == PositionType.ABSOLUTE:
            position_type = StretchablePosition.ABSOLUTE
        elif position.type == PositionType.RELATIVE:
            position_type = StretchablePosition.RELATIVE
        elif position.type == PositionType.FIXED:
            # FIXED is mapped to ABSOLUTE in Taffy
            # The layout engine will post-process these to be canvas-relative
            position_type = StretchablePosition.ABSOLUTE
        
        inset = position.inset
        if not inset:
            return position_type, None
        
        top = self._to_inset_value(inset.top)
        right = self._to_inset_value(inset.right)
        bottom = self._to_inset_value(inset.bottom)
        left = self._to_inset_value(inset.left)
        
        if all(v is AUTO for v in [top, right, bottom, left]):
            return position_type, None
        
        return position_type, (top, right, bottom, left)

    def _to_inset_value(self, value):
        if value is None:
            return AUTO
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str) and value.endswith('%'):
            return float(value.rstrip('%')) * PCT
        return AUTO

    def _to_spacing(self, spacing: 'Padding | Margin') -> tuple:
        return (spacing.top, spacing.right, spacing.bottom, spacing.left)

    def _to_border_width(self, border: Optional['Border']) -> float:
        return border.width if border else 0.0

    def _to_justify_content(self, value: str) -> JustifyContent:
        mapping = {
            'start': JustifyContent.START,
            'center': JustifyContent.CENTER,
            'end': JustifyContent.END,
            'space-between': JustifyContent.SPACE_BETWEEN,
            'space-around': JustifyContent.SPACE_AROUND,
            'space-evenly': JustifyContent.SPACE_EVENLY,
        }
        return mapping.get(value, JustifyContent.START)

    def _to_align_items(self, value: str) -> AlignItems:
        mapping = {
            'start': AlignItems.START,
            'center': AlignItems.CENTER,
            'end': AlignItems.END,
            'stretch': AlignItems.STRETCH,
        }
        return mapping.get(value, AlignItems.START)

    def _to_align_self(self, value: str) -> StretchableAlignSelf:
        mapping = {
            'start': StretchableAlignSelf.START,
            'center': StretchableAlignSelf.CENTER,
            'end': StretchableAlignSelf.END,
            'stretch': StretchableAlignSelf.STRETCH,
        }
        return mapping.get(value, StretchableAlignSelf.START)

    def _to_flex_wrap(self, value: str) -> StretchableFlexWrap:
        mapping = {
            'nowrap': StretchableFlexWrap.NO_WRAP,
            'wrap': StretchableFlexWrap.WRAP,
            'wrap-reverse': StretchableFlexWrap.WRAP_REVERSE,
        }
        return mapping.get(value, StretchableFlexWrap.NO_WRAP)
