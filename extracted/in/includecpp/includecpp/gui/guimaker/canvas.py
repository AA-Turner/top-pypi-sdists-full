"""
CSSL GUI Builder - Design canvas (QGraphicsView/Scene).
"""

from PyQt6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsRectItem,
                              QGraphicsItem)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, QMimeData
from PyQt6.QtGui import (QPainter, QColor, QPen, QBrush, QFont, QWheelEvent,
                          QDragEnterEvent, QDropEvent, QDragMoveEvent, QMouseEvent)

from .models import SceneModel, WidgetModel
from .commands import (CommandHistory, AddWidgetCommand, MoveWidgetCommand,
                       ResizeWidgetCommand)
from .canvas_items import CanvasWidgetItem, create_canvas_item
from .constants import CsslWidgetType, WIDGET_REGISTRY, cssl_type_from_string
from . import theme


class WindowFrameItem(QGraphicsRectItem):
    """The CSSL window background on the canvas."""

    def __init__(self, width: int, height: int):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(QColor(theme.CANVAS_WINDOW_BG)))
        self.setPen(QPen(QColor("#999999"), 1))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(-100)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()

        # Shadow
        shadow_offset = 4
        shadow_rect = rect.adjusted(shadow_offset, shadow_offset,
                                    shadow_offset, shadow_offset)
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(shadow_rect, 4, 4)

        # Window body
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        painter.drawRoundedRect(rect, 4, 4)

        # Title bar
        title_h = 30
        title_rect = QRectF(rect.left(), rect.top(), rect.width(), title_h)
        painter.setBrush(QBrush(QColor("#e0e0e0")))
        painter.setPen(Qt.PenStyle.NoPen)
        path = painter.clipPath()
        from PyQt6.QtGui import QPainterPath
        clip = QPainterPath()
        clip.addRoundedRect(rect, 4, 4)
        painter.setClipPath(clip)
        painter.drawRect(title_rect)
        painter.setClipping(False)

        # Title bar text
        painter.setPen(QPen(QColor("#333333")))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(title_rect.adjusted(12, 0, 0, 0),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                         "CSSL Window")

        # Window control dots
        dot_y = title_rect.center().y()
        for i, color in enumerate(["#ff5f57", "#ffbd2e", "#28c840"]):
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPointF(rect.right() - 16 - i * 20, dot_y), 6, 6)

        # Border line under title
        painter.setPen(QPen(QColor("#cccccc"), 1))
        painter.drawLine(int(rect.left()), int(rect.top() + title_h),
                         int(rect.right()), int(rect.top() + title_h))


class DesignCanvas(QGraphicsView):
    """Main visual design surface."""

    widget_selected = pyqtSignal(str)     # widget_id
    widget_deselected = pyqtSignal()
    widget_added = pyqtSignal(str)        # widget_id

    def __init__(self, scene_model: SceneModel, command_history: CommandHistory):
        self._gfx_scene = QGraphicsScene()
        super().__init__(self._gfx_scene)
        self._scene_model = scene_model
        self._command_history = command_history
        self._canvas_items: dict[str, CanvasWidgetItem] = {}
        self._window_frame: WindowFrameItem | None = None
        self._selected_id: str | None = None
        self._grid_visible = True
        self._snap_to_grid = True
        self._grid_size = 10
        self._zoom_level = 1.0

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setAcceptDrops(True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Listen to model changes
        self._scene_model.add_listener(self._on_model_change)

    def _on_model_change(self, event: str, **kwargs) -> None:
        if event == "widget_added":
            widget = kwargs.get("widget")
            if widget and widget.id not in self._canvas_items:
                if widget.widget_type != CsslWidgetType.WIDGET:
                    self._add_canvas_item(widget)
        elif event == "widget_removed":
            widget = kwargs.get("widget")
            if widget:
                self._remove_canvas_item(widget.id)
        elif event == "widget_moved":
            widget = kwargs.get("widget")
            if widget and widget.id in self._canvas_items:
                self._canvas_items[widget.id].update_from_model()
        elif event == "widget_resized":
            widget = kwargs.get("widget")
            if widget and widget.id in self._canvas_items:
                self._canvas_items[widget.id].update_from_model()
        elif event == "property_changed":
            widget = kwargs.get("widget")
            if widget and widget.id in self._canvas_items:
                item = self._canvas_items[widget.id]
                item.prepareGeometryChange()
                item.update()
        elif event == "widget_renamed":
            widget = kwargs.get("widget")
            if widget and widget.id in self._canvas_items:
                item = self._canvas_items[widget.id]
                item.prepareGeometryChange()
                item.update()
        elif event == "scene_cleared":
            self._clear_all()

    def setup_window(self, width: int = 800, height: int = 600) -> None:
        """Set up the window frame on the canvas."""
        if self._window_frame:
            self._gfx_scene.removeItem(self._window_frame)
        self._window_frame = WindowFrameItem(width, height)
        self._gfx_scene.addItem(self._window_frame)
        # Set scene rect with padding
        padding = 100
        self._gfx_scene.setSceneRect(-padding, -padding,
                                      width + padding * 2,
                                      height + padding * 2)
        self.centerOn(width / 2, height / 2)

    def _add_canvas_item(self, widget: WidgetModel) -> None:
        item = create_canvas_item(widget)
        self._gfx_scene.addItem(item)
        self._canvas_items[widget.id] = item
        item.setZValue(widget.z_order)

    def _remove_canvas_item(self, widget_id: str) -> None:
        item = self._canvas_items.pop(widget_id, None)
        if item:
            if item == self._gfx_scene.mouseGrabberItem():
                item.ungrabMouse()
            self._gfx_scene.removeItem(item)
        if self._selected_id == widget_id:
            self._selected_id = None
            self.widget_deselected.emit()

    def _clear_all(self) -> None:
        for item in list(self._canvas_items.values()):
            self._gfx_scene.removeItem(item)
        self._canvas_items.clear()
        if self._window_frame:
            self._gfx_scene.removeItem(self._window_frame)
            self._window_frame = None
        self._selected_id = None

    def select_widget(self, widget_id: str) -> None:
        """Select a widget by ID."""
        # Deselect current
        if self._selected_id and self._selected_id in self._canvas_items:
            self._canvas_items[self._selected_id].set_selected(False)

        self._selected_id = widget_id
        if widget_id and widget_id in self._canvas_items:
            self._canvas_items[widget_id].set_selected(True)
            self.widget_selected.emit(widget_id)
        else:
            self.widget_deselected.emit()

    def deselect_all(self) -> None:
        if self._selected_id and self._selected_id in self._canvas_items:
            self._canvas_items[self._selected_id].set_selected(False)
        self._selected_id = None
        self.widget_deselected.emit()

    def refresh_all(self) -> None:
        """Rebuild all canvas items from the scene model."""
        self._clear_all()
        if self._scene_model.window:
            w = self._scene_model.window
            self.setup_window(w.width, w.height)
        for widget in self._scene_model.get_all_widgets_ordered():
            if widget.widget_type != CsslWidgetType.WIDGET:
                self._add_canvas_item(widget)

    # --- Drag & Drop from palette ---

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            text = event.mimeData().text()
            if text.startswith("cssl_widget:"):
                event.acceptProposedAction()
                return
        event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasText() and \
           event.mimeData().text().startswith("cssl_widget:"):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        text = event.mimeData().text()
        if not text.startswith("cssl_widget:"):
            event.ignore()
            return

        type_name = text.split(":", 1)[1]
        widget_type = None
        for wt in CsslWidgetType:
            if wt.name == type_name:
                widget_type = wt
                break
        if widget_type is None:
            event.ignore()
            return

        # Map drop position to scene coordinates
        scene_pos = self.mapToScene(event.position().toPoint())
        grid = self._grid_size if self._snap_to_grid else 1
        x = max(0, round(scene_pos.x() / grid) * grid)
        y = max(0, round(scene_pos.y() / grid) * grid)

        type_def = WIDGET_REGISTRY.get(widget_type)
        if not type_def:
            return

        # Create widget model
        widget = WidgetModel(
            name=self._scene_model.generate_name(widget_type),
            widget_type=widget_type,
            parent_id=self._scene_model.window.id if self._scene_model.window else None,
            x=int(x),
            y=int(y),
            width=type_def.default_size[0],
            height=type_def.default_size[1],
            z_order=self._scene_model.get_next_z_order(),
        )

        # Set default properties
        for prop in type_def.properties:
            if prop.default is not None:
                widget.properties[prop.name] = prop.default

        # Execute via command for undo support
        cmd = AddWidgetCommand(self._scene_model, widget)
        self._command_history.execute(cmd)

        # Select the new widget
        self.select_widget(widget.id)
        self.widget_added.emit(widget.id)
        event.acceptProposedAction()

    # --- Mouse events for selection ---

    def mousePressEvent(self, event: QMouseEvent) -> None:
        item = self.itemAt(event.pos())
        if isinstance(item, CanvasWidgetItem):
            self.select_widget(item.model.id)
        elif not isinstance(item, CanvasWidgetItem):
            # Check if we clicked a resize handle's parent
            found = False
            from .canvas_items import ResizeHandle
            if isinstance(item, ResizeHandle):
                parent = item._parent_item
                if isinstance(parent, CanvasWidgetItem):
                    self.select_widget(parent.model.id)
                    found = True
            if not found:
                self.deselect_all()
        super().mousePressEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Delete:
            if self._selected_id:
                widget = self._scene_model.get_widget(self._selected_id)
                if widget and widget.widget_type != CsslWidgetType.WIDGET:
                    from .commands import RemoveWidgetCommand
                    cmd = RemoveWidgetCommand(self._scene_model, self._selected_id)
                    self._command_history.execute(cmd)
        super().keyPressEvent(event)

    # --- Callbacks from canvas items ---

    def _on_item_moved(self, item: CanvasWidgetItem,
                       old_x: int, old_y: int, new_x: int, new_y: int) -> None:
        """Called when a canvas item finishes being dragged."""
        cmd = MoveWidgetCommand(self._scene_model, item.model.id,
                                old_x, old_y, new_x, new_y)
        self._command_history.execute(cmd)

    def _on_item_resized(self, item: CanvasWidgetItem) -> None:
        """Called when a canvas item finishes being resized."""
        # The model already has updated values from the resize operation
        # We create a command with the current values for undo purposes
        # The resize handle already updated the model during drag
        pass

    # --- Zoom ---

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
            self._zoom_level *= factor
            self._zoom_level = max(0.25, min(4.0, self._zoom_level))
            self.setTransform(self.transform().scale(factor, factor) if abs(factor - 1) > 0.01
                              else self.transform())
            # Simpler zoom approach
            self.resetTransform()
            self.scale(self._zoom_level, self._zoom_level)
            event.accept()
        else:
            super().wheelEvent(event)

    def zoom_in(self) -> None:
        self._zoom_level = min(4.0, self._zoom_level * 1.2)
        self.resetTransform()
        self.scale(self._zoom_level, self._zoom_level)

    def zoom_out(self) -> None:
        self._zoom_level = max(0.25, self._zoom_level / 1.2)
        self.resetTransform()
        self.scale(self._zoom_level, self._zoom_level)

    def zoom_reset(self) -> None:
        self._zoom_level = 1.0
        self.resetTransform()

    # --- Grid background ---

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)
        if not self._grid_visible:
            return

        # Draw grid dots
        painter.setPen(QPen(QColor(theme.GRID_COLOR), 1))
        grid = self._grid_size
        left = int(rect.left()) - (int(rect.left()) % grid)
        top = int(rect.top()) - (int(rect.top()) % grid)

        x = left
        while x < rect.right():
            y = top
            while y < rect.bottom():
                painter.drawPoint(int(x), int(y))
                y += grid
            x += grid
