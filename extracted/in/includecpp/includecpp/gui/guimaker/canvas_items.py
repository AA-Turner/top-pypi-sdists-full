"""
CSSL GUI Builder - QGraphicsItem subclasses for widget visual representations.
Each widget type gets a custom painter that draws a realistic preview.
"""

from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QFontMetrics, QPainterPath

from .models import WidgetModel
from .constants import CsslWidgetType, WIDGET_REGISTRY
from . import theme


# ---------------------------------------------------------------------------
# Resize handles
# ---------------------------------------------------------------------------

class ResizeHandle(QGraphicsRectItem):
    """Small square handle for resizing widgets."""

    HANDLE_SIZE = 7

    # Handle positions
    TOP_LEFT = 0
    TOP_CENTER = 1
    TOP_RIGHT = 2
    MIDDLE_LEFT = 3
    MIDDLE_RIGHT = 4
    BOTTOM_LEFT = 5
    BOTTOM_CENTER = 6
    BOTTOM_RIGHT = 7

    def __init__(self, position: int, parent_item: 'CanvasWidgetItem'):
        super().__init__(-self.HANDLE_SIZE / 2, -self.HANDLE_SIZE / 2,
                         self.HANDLE_SIZE, self.HANDLE_SIZE, parent_item)
        self._position = position
        self._parent_item = parent_item
        self.setBrush(QBrush(QColor(theme.HANDLE_COLOR)))
        self.setPen(QPen(QColor(theme.DARK_BG), 1))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(1000)
        self.setCursor(self._get_cursor())
        self.setVisible(False)

    def _get_cursor(self) -> Qt.CursorShape:
        cursors = {
            self.TOP_LEFT: Qt.CursorShape.SizeFDiagCursor,
            self.TOP_RIGHT: Qt.CursorShape.SizeBDiagCursor,
            self.BOTTOM_LEFT: Qt.CursorShape.SizeBDiagCursor,
            self.BOTTOM_RIGHT: Qt.CursorShape.SizeFDiagCursor,
            self.TOP_CENTER: Qt.CursorShape.SizeVerCursor,
            self.BOTTOM_CENTER: Qt.CursorShape.SizeVerCursor,
            self.MIDDLE_LEFT: Qt.CursorShape.SizeHorCursor,
            self.MIDDLE_RIGHT: Qt.CursorShape.SizeHorCursor,
        }
        return cursors.get(self._position, Qt.CursorShape.ArrowCursor)

    def update_position(self, rect: QRectF) -> None:
        """Update handle position based on parent rect."""
        positions = {
            self.TOP_LEFT: rect.topLeft(),
            self.TOP_CENTER: QPointF(rect.center().x(), rect.top()),
            self.TOP_RIGHT: rect.topRight(),
            self.MIDDLE_LEFT: QPointF(rect.left(), rect.center().y()),
            self.MIDDLE_RIGHT: QPointF(rect.right(), rect.center().y()),
            self.BOTTOM_LEFT: rect.bottomLeft(),
            self.BOTTOM_CENTER: QPointF(rect.center().x(), rect.bottom()),
            self.BOTTOM_RIGHT: rect.bottomRight(),
        }
        pos = positions.get(self._position, QPointF(0, 0))
        self.setPos(pos)


# ---------------------------------------------------------------------------
# Base canvas widget item
# ---------------------------------------------------------------------------

class CanvasWidgetItem(QGraphicsRectItem):
    """Base class for all widget representations on the canvas."""

    MIN_WIDTH = 20
    MIN_HEIGHT = 15

    def __init__(self, widget_model: WidgetModel, parent_item: QGraphicsItem = None):
        super().__init__(0, 0, widget_model.width, widget_model.height, parent_item)
        self._model = widget_model
        self._selected = False
        self._dragging = False
        self._resizing = False
        self._resize_handle_pos = -1
        self._drag_start_pos = QPointF()
        self._drag_start_scene_pos = QPointF()
        self._resize_start_rect = QRectF()
        self._resize_start_mouse = QPointF()
        self._handles: list[ResizeHandle] = []

        self.setPos(widget_model.x, widget_model.y)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        self._create_handles()

    @property
    def model(self) -> WidgetModel:
        return self._model

    def _create_handles(self) -> None:
        for i in range(8):
            handle = ResizeHandle(i, self)
            self._handles.append(handle)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        for handle in self._handles:
            handle.setVisible(selected)
        if selected:
            self._update_handle_positions()
        self.update()

    def _update_handle_positions(self) -> None:
        rect = self.rect()
        for handle in self._handles:
            handle.update_position(rect)

    def update_from_model(self) -> None:
        """Sync visual representation with model data."""
        self.setPos(self._model.x, self._model.y)
        self.setRect(0, 0, self._model.width, self._model.height)
        self._update_handle_positions()
        self.update()

    def paint(self, painter: QPainter, option, widget=None) -> None:
        """Default widget painting - subclasses override for specific looks."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        # Background
        painter.setBrush(QBrush(QColor(theme.WIDGET_BG)))
        painter.setPen(QPen(QColor(theme.WIDGET_BORDER), 1))
        painter.drawRoundedRect(rect, 3, 3)

        # Type label centered
        painter.setPen(QPen(QColor(theme.WIDGET_TEXT)))
        font = QFont("Segoe UI", 10)
        painter.setFont(font)
        name = self._model.name or self._model.widget_type.value
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, name)

        # Selection highlight
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2, Qt.PenStyle.DashLine))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if we're on a resize handle
            handle_pos = self._hit_test_handle(event.pos())
            if handle_pos >= 0:
                self._resizing = True
                self._resize_handle_pos = handle_pos
                self._resize_start_rect = QRectF(
                    self._model.x, self._model.y,
                    self._model.width, self._model.height
                )
                self._resize_start_mouse = event.scenePos()
                event.accept()
                return

            self._dragging = True
            self._drag_start_pos = QPointF(self._model.x, self._model.y)
            self._drag_start_scene_pos = event.scenePos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self._resizing:
            self._do_resize(event.scenePos())
            event.accept()
            return

        if self._dragging:
            delta = event.scenePos() - self._drag_start_scene_pos
            new_x = int(self._drag_start_pos.x() + delta.x())
            new_y = int(self._drag_start_pos.y() + delta.y())
            # Snap to grid
            grid = 10
            new_x = round(new_x / grid) * grid
            new_y = round(new_y / grid) * grid
            self.setPos(new_x, new_y)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self._resizing:
            self._resizing = False
            self._resize_handle_pos = -1
            # Notify canvas of resize completion
            canvas = self.scene()
            if canvas and hasattr(canvas, '_on_item_resized'):
                canvas._on_item_resized(self)
            event.accept()
            return

        if self._dragging:
            self._dragging = False
            new_pos = self.pos()
            new_x = int(new_pos.x())
            new_y = int(new_pos.y())
            if new_x != int(self._drag_start_pos.x()) or \
               new_y != int(self._drag_start_pos.y()):
                canvas = self.scene()
                if canvas and hasattr(canvas, '_on_item_moved'):
                    canvas._on_item_moved(
                        self,
                        int(self._drag_start_pos.x()),
                        int(self._drag_start_pos.y()),
                        new_x, new_y
                    )
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def _hit_test_handle(self, pos: QPointF) -> int:
        """Check if position hits any resize handle. Returns handle index or -1."""
        if not self._selected:
            return -1
        rect = self.rect()
        margin = 8
        corners = [
            (rect.topLeft(), ResizeHandle.TOP_LEFT),
            (QPointF(rect.center().x(), rect.top()), ResizeHandle.TOP_CENTER),
            (rect.topRight(), ResizeHandle.TOP_RIGHT),
            (QPointF(rect.left(), rect.center().y()), ResizeHandle.MIDDLE_LEFT),
            (QPointF(rect.right(), rect.center().y()), ResizeHandle.MIDDLE_RIGHT),
            (rect.bottomLeft(), ResizeHandle.BOTTOM_LEFT),
            (QPointF(rect.center().x(), rect.bottom()), ResizeHandle.BOTTOM_CENTER),
            (rect.bottomRight(), ResizeHandle.BOTTOM_RIGHT),
        ]
        for corner_pos, handle_idx in corners:
            if abs(pos.x() - corner_pos.x()) < margin and \
               abs(pos.y() - corner_pos.y()) < margin:
                return handle_idx
        return -1

    def _do_resize(self, scene_pos: QPointF) -> None:
        """Handle resize drag."""
        delta = scene_pos - self._resize_start_mouse
        r = self._resize_start_rect
        hp = self._resize_handle_pos
        new_x, new_y = r.x(), r.y()
        new_w, new_h = r.width(), r.height()

        if hp in (ResizeHandle.TOP_LEFT, ResizeHandle.MIDDLE_LEFT, ResizeHandle.BOTTOM_LEFT):
            new_x = r.x() + delta.x()
            new_w = r.width() - delta.x()
        if hp in (ResizeHandle.TOP_RIGHT, ResizeHandle.MIDDLE_RIGHT, ResizeHandle.BOTTOM_RIGHT):
            new_w = r.width() + delta.x()
        if hp in (ResizeHandle.TOP_LEFT, ResizeHandle.TOP_CENTER, ResizeHandle.TOP_RIGHT):
            new_y = r.y() + delta.y()
            new_h = r.height() - delta.y()
        if hp in (ResizeHandle.BOTTOM_LEFT, ResizeHandle.BOTTOM_CENTER, ResizeHandle.BOTTOM_RIGHT):
            new_h = r.height() + delta.y()

        # Enforce minimum size
        if new_w < self.MIN_WIDTH:
            if hp in (ResizeHandle.TOP_LEFT, ResizeHandle.MIDDLE_LEFT, ResizeHandle.BOTTOM_LEFT):
                new_x = r.x() + r.width() - self.MIN_WIDTH
            new_w = self.MIN_WIDTH
        if new_h < self.MIN_HEIGHT:
            if hp in (ResizeHandle.TOP_LEFT, ResizeHandle.TOP_CENTER, ResizeHandle.TOP_RIGHT):
                new_y = r.y() + r.height() - self.MIN_HEIGHT
            new_h = self.MIN_HEIGHT

        # Snap to grid
        grid = 10
        new_x = round(new_x / grid) * grid
        new_y = round(new_y / grid) * grid
        new_w = max(self.MIN_WIDTH, round(new_w / grid) * grid)
        new_h = max(self.MIN_HEIGHT, round(new_h / grid) * grid)

        self._model.x = int(new_x)
        self._model.y = int(new_y)
        self._model.width = int(new_w)
        self._model.height = int(new_h)
        self.setPos(new_x, new_y)
        self.setRect(0, 0, new_w, new_h)
        self._update_handle_positions()


# ---------------------------------------------------------------------------
# Widget-specific painters
# ---------------------------------------------------------------------------

class ButtonItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        bg = self._model.get_property("bg_color", "")
        fg = self._model.get_property("fg_color", "")
        font_size = self._model.get_property("font_size", 0)
        enabled = self._model.get_property("enabled", True)
        # Button body
        bg_color = QColor(bg) if bg else QColor("#e0e0e0")
        if not enabled:
            bg_color.setAlpha(120)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(QPen(QColor("#aaaaaa"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 4, 4)
        # Text
        text = self._model.get_property("text", "Button")
        fg_color = QColor(fg) if fg else QColor("#333333")
        if not enabled:
            fg_color.setAlpha(120)
        painter.setPen(QPen(fg_color))
        painter.setFont(QFont("Segoe UI", font_size if font_size > 0 else 10))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(text))
        # Selection
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRoundedRect(rect.adjusted(-1, -1, 1, 1), 4, 4)


class LabelItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        bg = self._model.get_property("bg_color", "")
        fg = self._model.get_property("fg_color", "")
        alignment = self._model.get_property("alignment", "left")
        bold = self._model.get_property("bold", False)
        font_size = self._model.get_property("font_size", 0)
        font_family = self._model.get_property("font_family", "")
        # Background
        if bg:
            painter.setBrush(QBrush(QColor(bg)))
            painter.setPen(QPen(QColor("#cccccc"), 1))
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
            painter.setPen(QPen(QColor("#cccccc"), 1, Qt.PenStyle.DotLine))
        painter.drawRect(rect)
        # Text
        text = self._model.get_property("text", "Label")
        painter.setPen(QPen(QColor(fg) if fg else QColor("#333333")))
        font = QFont(font_family if font_family else "Segoe UI",
                     font_size if font_size > 0 else 10)
        if bold:
            font.setBold(True)
        painter.setFont(font)
        align_map = {"left": Qt.AlignmentFlag.AlignLeft,
                     "center": Qt.AlignmentFlag.AlignHCenter,
                     "right": Qt.AlignmentFlag.AlignRight}
        h_align = align_map.get(alignment, Qt.AlignmentFlag.AlignLeft)
        painter.drawText(rect.adjusted(4, 0, -4, 0),
                         h_align | Qt.AlignmentFlag.AlignVCenter,
                         str(text))
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class InputFieldItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        bg = self._model.get_property("bg_color", "")
        fg = self._model.get_property("fg_color", "")
        # Input field look
        painter.setBrush(QBrush(QColor(bg) if bg else QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        # Placeholder/text
        text = self._model.get_property("text", "")
        placeholder = self._model.get_property("placeholder", "")
        display = text if text else placeholder
        if text:
            text_color = QColor(fg) if fg else QColor("#333333")
        else:
            text_color = QColor("#aaaaaa")
        painter.setPen(QPen(text_color))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(rect.adjusted(8, 0, -8, 0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         str(display) if display else "")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class TextAreaItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        bg = self._model.get_property("bg_color", "")
        fg = self._model.get_property("fg_color", "")
        font_family = self._model.get_property("font_family", "")
        font_size = self._model.get_property("font_size", 0)
        painter.setBrush(QBrush(QColor(bg) if bg else QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        # Draw lines to suggest multiline
        painter.setPen(QPen(QColor("#e0e0e0"), 1))
        y = rect.top() + 24
        while y < rect.bottom() - 8:
            painter.drawLine(int(rect.left() + 8), int(y),
                             int(rect.right() - 8), int(y))
            y += 18
        # Text content
        font = QFont(font_family if font_family else "Segoe UI",
                     font_size if font_size > 0 else 9)
        painter.setFont(font)
        text = self._model.get_property("text", "")
        if text:
            painter.setPen(QPen(QColor(fg) if fg else QColor("#333333")))
            painter.drawText(rect.adjusted(8, 6, -8, -6),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                             str(text)[:100])
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class CheckBoxItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        # Background
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.setPen(QPen(QColor("#cccccc"), 1, Qt.PenStyle.DotLine))
        painter.drawRect(rect)
        # Checkbox square
        box_size = 16
        box_y = int(rect.center().y() - box_size / 2)
        box_rect = QRectF(rect.left() + 4, box_y, box_size, box_size)
        checked = self._model.get_property("checked", False)
        painter.setBrush(QBrush(QColor("#3b82f6") if checked else QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(box_rect, 3, 3)
        if checked:
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.drawLine(int(box_rect.left() + 3), int(box_rect.center().y()),
                             int(box_rect.center().x()), int(box_rect.bottom() - 3))
            painter.drawLine(int(box_rect.center().x()), int(box_rect.bottom() - 3),
                             int(box_rect.right() - 3), int(box_rect.top() + 3))
        # Text
        text = self._model.get_property("text", "Checkbox")
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 10))
        text_rect = QRectF(rect.left() + box_size + 10, rect.top(),
                           rect.width() - box_size - 14, rect.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft |
                         Qt.AlignmentFlag.AlignVCenter, str(text))
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class RadioButtonItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.setPen(QPen(QColor("#cccccc"), 1, Qt.PenStyle.DotLine))
        painter.drawRect(rect)
        # Radio circle
        circle_r = 8
        cx = rect.left() + 4 + circle_r
        cy = rect.center().y()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawEllipse(QPointF(cx, cy), circle_r, circle_r)
        # Inner dot (selected state placeholder)
        painter.setBrush(QBrush(QColor("#888888")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(cx, cy), 4, 4)
        # Text
        text = self._model.get_property("text", "Option")
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 10))
        text_rect = QRectF(rect.left() + circle_r * 2 + 12, rect.top(),
                           rect.width() - circle_r * 2 - 16, rect.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft |
                         Qt.AlignmentFlag.AlignVCenter, str(text))
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class ComboBoxItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        # Down arrow
        arrow_x = rect.right() - 20
        arrow_y = rect.center().y()
        painter.setPen(QPen(QColor("#666666"), 2))
        painter.drawLine(int(arrow_x - 4), int(arrow_y - 2),
                         int(arrow_x), int(arrow_y + 2))
        painter.drawLine(int(arrow_x), int(arrow_y + 2),
                         int(arrow_x + 4), int(arrow_y - 2))
        # Items preview
        items = self._model.get_property("items", [])
        display = items[0] if items else "Select..."
        painter.setPen(QPen(QColor("#333333" if items else "#aaaaaa")))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(rect.adjusted(8, 0, -28, 0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         str(display))
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class SliderItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.setPen(QPen(QColor("#cccccc"), 1, Qt.PenStyle.DotLine))
        painter.drawRect(rect)
        # Track
        track_y = rect.center().y()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#cccccc")))
        track_rect = QRectF(rect.left() + 8, track_y - 2, rect.width() - 16, 4)
        painter.drawRoundedRect(track_rect, 2, 2)
        # Thumb
        min_v = self._model.get_property("min_val", 0)
        max_v = self._model.get_property("max_val", 100)
        val = self._model.get_property("value", 0)
        ratio = (val - min_v) / max(1, max_v - min_v)
        thumb_x = rect.left() + 8 + ratio * (rect.width() - 16)
        painter.setBrush(QBrush(QColor("#3b82f6")))
        painter.drawEllipse(QPointF(thumb_x, track_y), 7, 7)
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class ProgressBarItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        # Background
        painter.setBrush(QBrush(QColor("#e0e0e0")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        # Progress fill
        val = self._model.get_property("value", 0)
        max_v = self._model.get_property("max_val", 100)
        ratio = val / max(1, max_v)
        fill_w = (rect.width() - 4) * ratio
        if fill_w > 0:
            fill_rect = QRectF(rect.left() + 2, rect.top() + 2, fill_w, rect.height() - 4)
            painter.setBrush(QBrush(QColor("#3b82f6")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(fill_rect, 2, 2)
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class ListBoxItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        # Draw sample items
        items = self._model.get_property("items", [])
        painter.setFont(QFont("Segoe UI", 10))
        y = rect.top() + 4
        for i, item in enumerate(items[:8]):
            if y + 22 > rect.bottom():
                break
            item_rect = QRectF(rect.left() + 4, y, rect.width() - 8, 20)
            if i == 0:
                painter.setBrush(QBrush(QColor("#e8f0fe")))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(item_rect, 2, 2)
            painter.setPen(QPen(QColor("#333333")))
            painter.drawText(item_rect.adjusted(6, 0, -6, 0),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             str(item))
            y += 22
        if not items:
            painter.setPen(QPen(QColor("#aaaaaa")))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "List Box")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class TableItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRect(rect)
        # Header
        columns = self._model.get_property("columns", [])
        header_h = 28
        header_rect = QRectF(rect.left(), rect.top(), rect.width(), header_h)
        painter.setBrush(QBrush(QColor("#f0f0f0")))
        painter.drawRect(header_rect)
        if columns:
            col_w = rect.width() / len(columns)
            painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            painter.setPen(QPen(QColor("#333333")))
            for i, col in enumerate(columns):
                cr = QRectF(rect.left() + i * col_w, rect.top(), col_w, header_h)
                painter.drawText(cr, Qt.AlignmentFlag.AlignCenter, str(col))
            # Column lines
            painter.setPen(QPen(QColor("#dddddd"), 1))
            for i in range(1, len(columns)):
                x = rect.left() + i * col_w
                painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
        else:
            painter.setPen(QPen(QColor("#aaaaaa")))
            painter.setFont(QFont("Segoe UI", 10))
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Table")
        # Row lines
        painter.setPen(QPen(QColor("#eeeeee"), 1))
        y = rect.top() + header_h
        while y < rect.bottom():
            painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
            y += 24
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class SeparatorItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        rect = self.rect()
        orientation = self._model.get_property("orientation", "horizontal")
        color = self._model.get_property("color", "")
        thickness = self._model.get_property("thickness", 2)
        painter.setPen(QPen(QColor(color) if color else QColor("#cccccc"), thickness))
        if orientation == "horizontal":
            y = rect.center().y()
            painter.drawLine(int(rect.left()), int(y), int(rect.right()), int(y))
        else:
            x = rect.center().x()
            painter.drawLine(int(x), int(rect.top()), int(x), int(rect.bottom()))
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2, Qt.PenStyle.DashLine))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class PictureItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#f5f5f5")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRect(rect)
        # Image icon placeholder
        painter.setPen(QPen(QColor("#aaaaaa")))
        painter.setFont(QFont("Segoe UI", 24))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "\u25a6")
        # Path label
        path = self._model.get_property("image_path", "")
        if path:
            painter.setFont(QFont("Segoe UI", 8))
            painter.setPen(QPen(QColor("#888888")))
            painter.drawText(rect.adjusted(4, 0, -4, -4),
                             Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter,
                             str(path)[-30:])
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class TimePickerItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        h = self._model.get_property("hour", 0)
        m = self._model.get_property("minute", 0)
        s = self._model.get_property("second", 0)
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 11))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{h:02d}:{m:02d}:{s:02d}")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class DatePickerItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 3, 3)
        y = self._model.get_property("year", 2025)
        m = self._model.get_property("month", 1)
        d = self._model.get_property("day", 1)
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 11))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{y:04d}-{m:02d}-{d:02d}")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class TabControlItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        # Tab bar area
        tab_h = 30
        painter.setBrush(QBrush(QColor("#f0f0f0")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRect(QRectF(rect.left(), rect.top(), rect.width(), tab_h))
        # Sample tabs
        tabs = ["Tab 1", "Tab 2", "Tab 3"]
        x = rect.left() + 2
        painter.setFont(QFont("Segoe UI", 9))
        for i, tab in enumerate(tabs):
            tw = 70
            tr = QRectF(x, rect.top() + 2, tw, tab_h - 4)
            if i == 0:
                painter.setBrush(QBrush(QColor("#ffffff")))
                painter.setPen(QPen(QColor("#3b82f6"), 0))
                painter.drawRoundedRect(tr, 3, 3)
                painter.setPen(QPen(QColor("#333333")))
            else:
                painter.setPen(QPen(QColor("#888888")))
            painter.drawText(tr, Qt.AlignmentFlag.AlignCenter, tab)
            x += tw + 4
        # Content area
        content_rect = QRectF(rect.left(), rect.top() + tab_h, rect.width(),
                              rect.height() - tab_h)
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRect(content_rect)
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class ScrollPanelItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor("#888888"), 1))
        painter.drawRect(rect)
        # Scrollbar indicator
        sb_w = 10
        sb_rect = QRectF(rect.right() - sb_w - 2, rect.top() + 4,
                         sb_w, rect.height() * 0.4)
        painter.setBrush(QBrush(QColor("#cccccc")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(sb_rect, 4, 4)
        # Label
        painter.setPen(QPen(QColor("#aaaaaa")))
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "Scroll Panel")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class MenuBarItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#f0f0f0")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRect(rect)
        # Draw menus from property or fallback
        menus_data = self._model.get_property("menus", [])
        if menus_data:
            menu_labels = [m.get("label", "Menu") for m in menus_data
                           if isinstance(m, dict)]
        else:
            menu_labels = ["File", "Edit", "View", "Help"]
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 10))
        x = rect.left() + 8
        for label in menu_labels:
            fm = QFontMetrics(painter.font())
            tw = fm.horizontalAdvance(label) + 16
            painter.drawText(QRectF(x, rect.top(), tw, rect.height()),
                             Qt.AlignmentFlag.AlignCenter, label)
            x += tw
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


class ToolbarItem(CanvasWidgetItem):
    def paint(self, painter: QPainter, option, widget=None) -> None:
        rect = self.rect()
        painter.setBrush(QBrush(QColor("#f5f5f5")))
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawRect(rect)
        # Draw toolbar slots from property or fallback
        slots = self._model.get_property("slots", [])
        x = rect.left() + 6
        y = rect.center().y()
        btn_h = 28
        slot_font = QFont("Segoe UI", 8)
        fm = QFontMetrics(slot_font)
        if slots:
            for slot in slots:
                if not isinstance(slot, dict):
                    continue
                tooltip = slot.get("tooltip", "")
                # Auto-size width: measure text + padding, minimum 28px
                text_w = fm.horizontalAdvance(tooltip) if tooltip else 0
                btn_w = max(btn_h, text_w + 16)
                br = QRectF(x, y - btn_h / 2, btn_w, btn_h)
                painter.setBrush(QBrush(QColor("#e0e0e0")))
                painter.setPen(QPen(QColor("#bbbbbb"), 1))
                painter.drawRoundedRect(br, 3, 3)
                if tooltip:
                    painter.setPen(QPen(QColor("#555555")))
                    painter.setFont(slot_font)
                    painter.drawText(br, Qt.AlignmentFlag.AlignCenter, tooltip)
                x += btn_w + 4
        else:
            # Fallback: 5 generic placeholder buttons
            for i in range(5):
                br = QRectF(x, y - btn_h / 2, btn_h, btn_h)
                painter.setBrush(QBrush(QColor("#e0e0e0")))
                painter.setPen(QPen(QColor("#bbbbbb"), 1))
                painter.drawRoundedRect(br, 3, 3)
                x += btn_h + 4
            painter.setPen(QPen(QColor("#888888")))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(QRectF(x + 8, rect.top(), 80, rect.height()),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             "Toolbar")
        if self._selected:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(theme.SELECTION_COLOR), 2))
            painter.drawRect(rect.adjusted(-1, -1, 1, 1))


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_ITEM_MAP = {
    CsslWidgetType.BUTTON: ButtonItem,
    CsslWidgetType.LABEL: LabelItem,
    CsslWidgetType.INPUT_FIELD: InputFieldItem,
    CsslWidgetType.TEXT_AREA: TextAreaItem,
    CsslWidgetType.CHECK_BOX: CheckBoxItem,
    CsslWidgetType.RADIO_BUTTON: RadioButtonItem,
    CsslWidgetType.COMBO_BOX: ComboBoxItem,
    CsslWidgetType.SLIDER: SliderItem,
    CsslWidgetType.PROGRESS_BAR: ProgressBarItem,
    CsslWidgetType.LIST_BOX: ListBoxItem,
    CsslWidgetType.TABLE: TableItem,
    CsslWidgetType.SEPARATOR: SeparatorItem,
    CsslWidgetType.PICTURE: PictureItem,
    CsslWidgetType.TIME_PICKER: TimePickerItem,
    CsslWidgetType.DATE_PICKER: DatePickerItem,
    CsslWidgetType.TAB_CONTROL: TabControlItem,
    CsslWidgetType.SCROLL_PANEL: ScrollPanelItem,
    CsslWidgetType.MENU_BAR: MenuBarItem,
    CsslWidgetType.TOOLBAR: ToolbarItem,
}


def create_canvas_item(widget_model: WidgetModel,
                       parent_item: QGraphicsItem = None) -> CanvasWidgetItem:
    """Create the appropriate canvas item for a widget model."""
    item_class = _ITEM_MAP.get(widget_model.widget_type, CanvasWidgetItem)
    return item_class(widget_model, parent_item)
