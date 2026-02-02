"""
CSSL GUI Builder - Widget palette panel (left sidebar).
Categorized drag-and-drop widget buttons with search filtering.
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QScrollArea, QFrame, QToolButton,
                              QSizePolicy)
from PyQt6.QtCore import Qt, QMimeData, QSize, QPoint
from PyQt6.QtGui import QDrag, QFont, QColor, QMouseEvent, QPixmap, QPainter

from .constants import (WidgetCategory, CsslWidgetType, WidgetTypeDef,
                         WIDGET_REGISTRY, get_widgets_by_category)
from . import theme


class PaletteButton(QToolButton):
    """Draggable widget button in the palette."""

    def __init__(self, type_def: WidgetTypeDef, parent: QWidget = None):
        super().__init__(parent)
        self._type_def = type_def
        self._drag_start_pos: QPoint | None = None

        self.setText(f" {type_def.icon}  {type_def.display_name}")
        self.setToolTip(f"Drag to add {type_def.display_name} ({type_def.widget_type.value})")
        self.setFixedHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        self.setStyleSheet(f"""
            QToolButton {{
                background-color: {theme.DARK_CARD};
                border: 1px solid {theme.DARK_BORDER};
                border-radius: 4px;
                padding: 4px 10px;
                color: {theme.TEXT_SECONDARY};
                font-size: 12px;
                text-align: left;
            }}
            QToolButton:hover {{
                background-color: {theme.DARK_HOVER};
                border-color: {theme.TEXT_MUTED};
                color: {theme.TEXT_PRIMARY};
            }}
        """)

    @property
    def type_def(self) -> WidgetTypeDef:
        return self._type_def

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_start_pos is None:
            return
        if (event.pos() - self._drag_start_pos).manhattanLength() < 10:
            return

        # Start drag
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(f"cssl_widget:{self._type_def.widget_type.name}")
        drag.setMimeData(mime)

        # Create drag pixmap
        pixmap = QPixmap(140, 30)
        pixmap.fill(QColor(0, 0, 0, 0))
        p = QPainter(pixmap)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(theme.SELECTION_COLOR))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 0, 140, 30, 6, 6)
        p.setPen(QColor("#ffffff"))
        p.setFont(QFont("Segoe UI", 10))
        p.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter,
                   self._type_def.display_name)
        p.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(70, 15))

        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        drag.exec(Qt.DropAction.CopyAction)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self._drag_start_pos = None

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_start_pos = None
        super().mouseReleaseEvent(event)


class CategorySection(QWidget):
    """Collapsible section of widgets in a category."""

    def __init__(self, category: WidgetCategory, widgets: list[WidgetTypeDef],
                 parent: QWidget = None):
        super().__init__(parent)
        self._category = category
        self._collapsed = False
        self._buttons: list[PaletteButton] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self._header = QToolButton()
        self._header.setText(f"  \u25bc  {category.value}")
        self._header.setFixedHeight(28)
        self._header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self._header.clicked.connect(self._toggle)
        self._header.setStyleSheet(f"""
            QToolButton {{
                background-color: transparent;
                border: none;
                border-bottom: 1px solid {theme.DARK_BORDER};
                color: {theme.TEXT_MUTED};
                font-size: 11px;
                font-weight: bold;
                text-align: left;
                padding-left: 4px;
            }}
            QToolButton:hover {{
                color: {theme.TEXT_PRIMARY};
            }}
        """)
        layout.addWidget(self._header)

        # Button container
        self._container = QWidget()
        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(4, 4, 4, 8)
        self._container_layout.setSpacing(3)

        for wdef in widgets:
            btn = PaletteButton(wdef)
            self._container_layout.addWidget(btn)
            self._buttons.append(btn)

        layout.addWidget(self._container)

    def _toggle(self) -> None:
        self._collapsed = not self._collapsed
        self._container.setVisible(not self._collapsed)
        arrow = "\u25b6" if self._collapsed else "\u25bc"
        self._header.setText(f"  {arrow}  {self._category.value}")

    def filter_buttons(self, text: str) -> int:
        """Filter buttons by search text. Returns number of visible buttons."""
        visible = 0
        for btn in self._buttons:
            match = text.lower() in btn.type_def.display_name.lower() or \
                    text.lower() in btn.type_def.widget_type.value.lower()
            btn.setVisible(match)
            if match:
                visible += 1

        # Show category only if it has visible buttons
        self.setVisible(visible > 0 or not text)
        if text and visible > 0:
            self._collapsed = False
            self._container.setVisible(True)
            arrow = "\u25bc"
            self._header.setText(f"  {arrow}  {self._category.value}")
        return visible


class WidgetPalette(QWidget):
    """Left sidebar panel with categorized widget buttons for drag-and-drop."""

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._sections: list[CategorySection] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Search bar
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(8, 8, 8, 8)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search widgets...")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.textChanged.connect(self._on_search)
        self._search_input.setFixedHeight(28)
        search_layout.addWidget(self._search_input)

        layout.addWidget(search_container)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background-color: {theme.DARK_BORDER};")
        sep.setFixedHeight(1)
        layout.addWidget(sep)

        # Scroll area for categories
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4, 4, 4, 4)
        content_layout.setSpacing(2)

        # Build categories
        categories = get_widgets_by_category()
        # Order categories logically
        cat_order = [
            WidgetCategory.DISPLAY,
            WidgetCategory.INPUT,
            WidgetCategory.DATA,
            WidgetCategory.TIME,
            WidgetCategory.CONTAINER,
            WidgetCategory.NAVIGATION,
        ]
        for cat in cat_order:
            if cat in categories:
                section = CategorySection(cat, categories[cat])
                content_layout.addWidget(section)
                self._sections.append(section)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def _on_search(self, text: str) -> None:
        text = text.strip()
        for section in self._sections:
            section.filter_buttons(text)
