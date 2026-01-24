"""
IncludeCPP Project Interface with CodeMaker
Professional visual system design and planning tool

Features:
- Modern dark frameless window with custom controls
- Interactive node-based mindmap canvas
- 24+ node types with categorized menus
- Pan/zoom navigation with smooth animations
- Multi-selection with rubber band
- Undo/redo system
- Copy/paste/duplicate
- Node grouping
- Code generation (C++/Python)
- Template system
- Search and filter
- Minimap overview
- Keyboard shortcuts
- Export (PNG/SVG/Code)
- Cross-platform support
"""

import sys
import json
import math
import uuid
import copy
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any, Set, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QFrame, QSplitter, QTreeWidget, QTreeWidgetItem,
        QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsRectItem,
        QGraphicsTextItem, QGraphicsLineItem, QGraphicsEllipseItem,
        QMenu, QInputDialog, QMessageBox, QGraphicsDropShadowEffect,
        QScrollArea, QSizePolicy, QGraphicsPathItem, QToolBar, QStatusBar,
        QGraphicsProxyWidget, QLineEdit, QTextEdit, QDialog, QDialogButtonBox,
        QFormLayout, QComboBox, QSpinBox, QColorDialog, QGraphicsPolygonItem,
        QToolButton, QWidgetAction, QSlider, QProgressBar, QFileDialog,
        QTabWidget, QListWidget, QListWidgetItem, QCheckBox, QGridLayout,
        QGroupBox, QPlainTextEdit, QRubberBand, QStackedWidget, QDockWidget
    )
    from PyQt6.QtCore import (
        Qt, QRectF, QPointF, QTimer, QPropertyAnimation, QEasingCurve,
        pyqtSignal, QObject, QLineF, QSize, QParallelAnimationGroup,
        QSequentialAnimationGroup, pyqtProperty, QVariantAnimation,
        QMimeData, QByteArray, QBuffer, QIODevice, QRect
    )
    from PyQt6.QtGui import (
        QFont, QColor, QPen, QBrush, QPainter, QPainterPath,
        QLinearGradient, QRadialGradient, QCursor, QWheelEvent,
        QMouseEvent, QKeyEvent, QTransform, QPolygonF, QFontMetrics,
        QPalette, QPixmap, QIcon, QAction, QClipboard, QImage,
        QKeySequence, QFontDatabase, QGuiApplication, QUndoStack,
        QUndoCommand, QShortcut
    )
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


# ============================================================================
# Cross-Platform Support
# ============================================================================

def get_system_font() -> str:
    """Get platform-appropriate system font."""
    if sys.platform == "win32":
        return "Segoe UI"
    elif sys.platform == "darwin":
        return "SF Pro"
    else:
        return "Ubuntu"

def get_monospace_font() -> str:
    """Get platform-appropriate monospace font."""
    if sys.platform == "win32":
        return "Consolas"
    elif sys.platform == "darwin":
        return "SF Mono"
    else:
        return "Ubuntu Mono"

def get_dpi_scale() -> float:
    """Get DPI scale factor for high-DPI displays."""
    if PYQT_AVAILABLE:
        app = QApplication.instance()
        if app:
            screen = app.primaryScreen()
            if screen:
                return screen.logicalDotsPerInch() / 96.0
    return 1.0


# ============================================================================
# Constants & Theme
# ============================================================================

SYSTEM_FONT = get_system_font() if PYQT_AVAILABLE else "Segoe UI"
MONO_FONT = get_monospace_font() if PYQT_AVAILABLE else "Consolas"

THEME = {
    'bg_dark': '#0d0d0d',
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#252525',
    'bg_tertiary': '#2d2d2d',
    'bg_hover': '#3d3d3d',
    'border': '#3d3d3d',
    'border_light': '#4d4d4d',
    'text_primary': '#e0e0e0',
    'text_secondary': '#a0a0a0',
    'text_muted': '#666666',
    'accent_blue': '#4a9eff',
    'accent_green': '#50c878',
    'accent_orange': '#ff9800',
    'accent_purple': '#e040fb',
    'accent_red': '#ff5555',
    'accent_cyan': '#00bcd4',
    'accent_yellow': '#ffeb3b',
    'accent_pink': '#ff4081',
    'accent_teal': '#009688',
    'accent_indigo': '#3f51b5',
    'accent_lime': '#cddc39',
    'success': '#4caf50',
    'warning': '#ff9800',
    'error': '#f44336',
    'shadow': 'rgba(0, 0, 0, 0.4)',
}

# Expanded node types with categories
NODE_CATEGORIES = {
    'Sources': ['source'],  # Primary - generates actual code files
    'Code Structures': ['class', 'struct', 'enum', 'interface', 'template_class', 'union'],
    'Functions': ['function', 'method', 'constructor', 'destructor', 'lambda', 'operator'],
    'Data': ['object', 'variable', 'constant', 'definition', 'typedef', 'pointer'],
    'Organization': ['namespace', 'module', 'package', 'file', 'folder', 'header'],
    'Flow': ['condition', 'loop', 'exception', 'async', 'callback', 'event'],
}

NODE_TYPES = {
    # Sources - Primary nodes that generate actual code files
    'source': {'color': '#00e676', 'icon': 'S', 'gradient_start': '#00ff88', 'gradient_end': '#00c853', 'label': 'Source', 'category': 'Sources', 'port_count': 8},

    # Code Structures
    'class': {'color': '#4a9eff', 'icon': 'C', 'gradient_start': '#5aaeff', 'gradient_end': '#3a8eef', 'label': 'Class', 'category': 'Code Structures'},
    'struct': {'color': '#9c27b0', 'icon': 'S', 'gradient_start': '#ac37c0', 'gradient_end': '#8c17a0', 'label': 'Struct', 'category': 'Code Structures'},
    'enum': {'color': '#ffeb3b', 'icon': 'E', 'gradient_start': '#fff34b', 'gradient_end': '#e0cc2b', 'label': 'Enum', 'category': 'Code Structures'},
    'interface': {'color': '#00bcd4', 'icon': 'I', 'gradient_start': '#20cce4', 'gradient_end': '#00acc4', 'label': 'Interface', 'category': 'Code Structures'},
    'template_class': {'color': '#7c4dff', 'icon': 'TC', 'gradient_start': '#8c5dff', 'gradient_end': '#6c3def', 'label': 'Template Class', 'category': 'Code Structures'},
    'union': {'color': '#795548', 'icon': 'U', 'gradient_start': '#896558', 'gradient_end': '#694538', 'label': 'Union', 'category': 'Code Structures'},

    # Functions
    'function': {'color': '#50c878', 'icon': 'fn', 'gradient_start': '#60d888', 'gradient_end': '#40b868', 'label': 'Function', 'category': 'Functions'},
    'method': {'color': '#66bb6a', 'icon': 'm', 'gradient_start': '#76cb7a', 'gradient_end': '#56ab5a', 'label': 'Method', 'category': 'Functions'},
    'constructor': {'color': '#81c784', 'icon': 'ctor', 'gradient_start': '#91d794', 'gradient_end': '#71b774', 'label': 'Constructor', 'category': 'Functions'},
    'destructor': {'color': '#a5d6a7', 'icon': 'dtor', 'gradient_start': '#b5e6b7', 'gradient_end': '#95c697', 'label': 'Destructor', 'category': 'Functions'},
    'lambda': {'color': '#4db6ac', 'icon': 'λ', 'gradient_start': '#5dc6bc', 'gradient_end': '#3da69c', 'label': 'Lambda', 'category': 'Functions'},
    'operator': {'color': '#26a69a', 'icon': 'op', 'gradient_start': '#36b6aa', 'gradient_end': '#16968a', 'label': 'Operator', 'category': 'Functions'},

    # Data
    'object': {'color': '#e040fb', 'icon': 'O', 'gradient_start': '#f050ff', 'gradient_end': '#c030db', 'label': 'Object', 'category': 'Data'},
    'variable': {'color': '#ba68c8', 'icon': 'var', 'gradient_start': '#ca78d8', 'gradient_end': '#aa58b8', 'label': 'Variable', 'category': 'Data'},
    'constant': {'color': '#ce93d8', 'icon': 'const', 'gradient_start': '#dea3e8', 'gradient_end': '#be83c8', 'label': 'Constant', 'category': 'Data'},
    'definition': {'color': '#ff9800', 'icon': 'D', 'gradient_start': '#ffa820', 'gradient_end': '#e08800', 'label': 'Definition', 'category': 'Data'},
    'typedef': {'color': '#ffb74d', 'icon': 'T', 'gradient_start': '#ffc75d', 'gradient_end': '#efa73d', 'label': 'Typedef', 'category': 'Data'},
    'pointer': {'color': '#ff7043', 'icon': '*', 'gradient_start': '#ff8053', 'gradient_end': '#ef6033', 'label': 'Pointer', 'category': 'Data'},

    # Organization
    'namespace': {'color': '#607d8b', 'icon': 'N', 'gradient_start': '#708d9b', 'gradient_end': '#506d7b', 'label': 'Namespace', 'category': 'Organization'},
    'module': {'color': '#78909c', 'icon': 'M', 'gradient_start': '#88a0ac', 'gradient_end': '#68808c', 'label': 'Module', 'category': 'Organization'},
    'package': {'color': '#90a4ae', 'icon': 'P', 'gradient_start': '#a0b4be', 'gradient_end': '#80949e', 'label': 'Package', 'category': 'Organization'},
    'file': {'color': '#b0bec5', 'icon': 'F', 'gradient_start': '#c0ced5', 'gradient_end': '#a0aeb5', 'label': 'File', 'category': 'Organization'},
    'folder': {'color': '#8d6e63', 'icon': 'D', 'gradient_start': '#9d7e73', 'gradient_end': '#7d5e53', 'label': 'Folder', 'category': 'Organization'},
    'header': {'color': '#a1887f', 'icon': 'H', 'gradient_start': '#b1988f', 'gradient_end': '#91786f', 'label': 'Header', 'category': 'Organization'},

    # Flow
    'condition': {'color': '#ef5350', 'icon': '?', 'gradient_start': '#ff6360', 'gradient_end': '#df4340', 'label': 'Condition', 'category': 'Flow'},
    'loop': {'color': '#e57373', 'icon': '⟳', 'gradient_start': '#f58383', 'gradient_end': '#d56363', 'label': 'Loop', 'category': 'Flow'},
    'exception': {'color': '#f44336', 'icon': '!', 'gradient_start': '#ff5346', 'gradient_end': '#e43326', 'label': 'Exception', 'category': 'Flow'},
    'async': {'color': '#42a5f5', 'icon': '⚡', 'gradient_start': '#52b5ff', 'gradient_end': '#3295e5', 'label': 'Async', 'category': 'Flow'},
    'callback': {'color': '#5c6bc0', 'icon': '↩', 'gradient_start': '#6c7bd0', 'gradient_end': '#4c5bb0', 'label': 'Callback', 'category': 'Flow'},
    'event': {'color': '#7e57c2', 'icon': '⚑', 'gradient_start': '#8e67d2', 'gradient_end': '#6e47b2', 'label': 'Event', 'category': 'Flow'},
}


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class PortData:
    """Data for a connection port on a node."""
    id: str = ""
    port_type: str = "bidirectional"  # input, output, bidirectional
    data_type: str = "any"  # any, int, float, string, object, function
    name: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class NodeData:
    """Data for a visual node in the CodeMaker"""
    id: str = ""
    node_type: str = "class"
    name: str = ""
    description: str = ""
    x: float = 0.0
    y: float = 0.0
    width: float = 200.0
    height: float = 100.0
    color: str = ""
    connections: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)
    ports: List[Dict] = field(default_factory=list)
    group_id: str = ""
    generated_files: Dict[str, str] = field(default_factory=dict)  # 'python': path, 'plugin': path
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.color:
            self.color = NODE_TYPES.get(self.node_type, {}).get('color', '#4a9eff')
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


@dataclass
class ConnectionData:
    """Data for a connection between nodes"""
    id: str = ""
    start_node_id: str = ""
    end_node_id: str = ""
    start_port: str = ""
    end_port: str = ""
    label: str = ""
    color: str = "#4a9eff"
    style: str = "solid"  # solid, dashed, dotted

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class GroupData:
    """Data for a node group"""
    id: str = ""
    name: str = ""
    color: str = "#607d8b"
    node_ids: List[str] = field(default_factory=list)
    collapsed: bool = False
    x: float = 0.0
    y: float = 0.0
    width: float = 300.0
    height: float = 200.0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]


@dataclass
class TemplateData:
    """Data for a node template"""
    name: str = ""
    category: str = "Custom"
    description: str = ""
    nodes: List[Dict] = field(default_factory=list)
    connections: List[Dict] = field(default_factory=list)
    code_template: str = ""


@dataclass
class MapData:
    """Data for a complete mindmap file"""
    name: str = ""
    description: str = ""
    nodes: List[NodeData] = field(default_factory=list)
    connections: List[ConnectionData] = field(default_factory=list)
    groups: List[GroupData] = field(default_factory=list)
    viewport_x: float = 0.0
    viewport_y: float = 0.0
    viewport_zoom: float = 1.0
    grid_visible: bool = True
    snap_to_grid: bool = False
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'nodes': [asdict(n) for n in self.nodes],
            'connections': [asdict(c) for c in self.connections],
            'groups': [asdict(g) for g in self.groups],
            'viewport_x': self.viewport_x,
            'viewport_y': self.viewport_y,
            'viewport_zoom': self.viewport_zoom,
            'grid_visible': self.grid_visible,
            'snap_to_grid': self.snap_to_grid,
            'created_at': self.created_at,
            'updated_at': datetime.now().isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'MapData':
        nodes = [NodeData(**n) for n in data.get('nodes', [])]
        connections = [ConnectionData(**c) for c in data.get('connections', [])]
        groups = [GroupData(**g) for g in data.get('groups', [])]
        return cls(
            name=data.get('name', 'Untitled'),
            description=data.get('description', ''),
            nodes=nodes,
            connections=connections,
            groups=groups,
            viewport_x=data.get('viewport_x', 0.0),
            viewport_y=data.get('viewport_y', 0.0),
            viewport_zoom=data.get('viewport_zoom', 1.0),
            grid_visible=data.get('grid_visible', True),
            snap_to_grid=data.get('snap_to_grid', False),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', '')
        )


if PYQT_AVAILABLE:

    # ========================================================================
    # Undo/Redo Commands
    # ========================================================================

    class AddNodeCommand(QUndoCommand):
        """Undoable command for adding a node."""
        def __init__(self, canvas, node_data: NodeData, description="Add Node"):
            super().__init__(description)
            self.canvas = canvas
            self.node_data = node_data
            self.node_id = node_data.id

        def redo(self):
            self.canvas._add_node_internal(self.node_data)

        def undo(self):
            if self.node_id in self.canvas.nodes:
                self.canvas._delete_node_internal(self.canvas.nodes[self.node_id])


    class DeleteNodeCommand(QUndoCommand):
        """Undoable command for deleting a node."""
        def __init__(self, canvas, node, description="Delete Node"):
            super().__init__(description)
            self.canvas = canvas
            self.node_data = copy.deepcopy(node.node_data)
            self.connections_data = []
            for conn in node.connections:
                self.connections_data.append(copy.deepcopy(conn.connection_data))

        def redo(self):
            if self.node_data.id in self.canvas.nodes:
                self.canvas._delete_node_internal(self.canvas.nodes[self.node_data.id])

        def undo(self):
            self.canvas._add_node_internal(self.node_data)
            for conn_data in self.connections_data:
                if conn_data.start_node_id in self.canvas.nodes and conn_data.end_node_id in self.canvas.nodes:
                    self.canvas._add_connection_internal(conn_data)


    class MoveNodeCommand(QUndoCommand):
        """Undoable command for moving nodes."""
        def __init__(self, canvas, node_id: str, old_pos: QPointF, new_pos: QPointF, description="Move Node"):
            super().__init__(description)
            self.canvas = canvas
            self.node_id = node_id
            self.old_pos = old_pos
            self.new_pos = new_pos

        def redo(self):
            if self.node_id in self.canvas.nodes:
                node = self.canvas.nodes[self.node_id]
                node.setPos(self.new_pos)
                node.node_data.x = self.new_pos.x()
                node.node_data.y = self.new_pos.y()
                for conn in node.connections:
                    conn.update_path()

        def undo(self):
            if self.node_id in self.canvas.nodes:
                node = self.canvas.nodes[self.node_id]
                node.setPos(self.old_pos)
                node.node_data.x = self.old_pos.x()
                node.node_data.y = self.old_pos.y()
                for conn in node.connections:
                    conn.update_path()


    class AddConnectionCommand(QUndoCommand):
        """Undoable command for adding a connection."""
        def __init__(self, canvas, conn_data: ConnectionData, description="Add Connection"):
            super().__init__(description)
            self.canvas = canvas
            self.conn_data = conn_data

        def redo(self):
            self.canvas._add_connection_internal(self.conn_data)

        def undo(self):
            for conn in self.canvas.connections:
                if conn.connection_data.id == self.conn_data.id:
                    self.canvas._delete_connection_internal(conn)
                    break


    # ========================================================================
    # Animated Button with Sophisticated Hover Effects
    # ========================================================================

    class AnimatedButton(QPushButton):
        """Modern animated button with gradient hover effects"""

        def __init__(self, text: str, icon_text: str = "", accent_color: str = None, parent=None):
            super().__init__(parent)
            self._text = text
            self._icon_text = icon_text
            self._accent = QColor(accent_color or THEME['accent_blue'])
            self._hover_progress = 0.0
            self._pressed = False

            self.setText(f"  {icon_text}  {text}" if icon_text else f"  {text}")
            self.setMinimumHeight(44)
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.setFont(QFont(SYSTEM_FONT, 11))

            self._animation = QVariantAnimation(self)
            self._animation.setDuration(150)
            self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self._animation.valueChanged.connect(self._update_hover)

            self._update_style()

        def _update_hover(self, value):
            self._hover_progress = value
            self._update_style()

        def _update_style(self):
            progress = self._hover_progress

            bg_base = QColor(THEME['bg_tertiary'])
            bg_hover = self._accent.darker(140)

            r = int(bg_base.red() + (bg_hover.red() - bg_base.red()) * progress)
            g = int(bg_base.green() + (bg_hover.green() - bg_base.green()) * progress)
            b = int(bg_base.blue() + (bg_hover.blue() - bg_base.blue()) * progress)

            bg_color = f"rgb({r}, {g}, {b})"
            border_color = self._accent.name() if progress > 0.3 else THEME['border']

            if self._pressed:
                bg_color = self._accent.name()
                border_color = self._accent.lighter(120).name()

            self.setStyleSheet(f'''
                QPushButton {{
                    background-color: {bg_color};
                    border: 1px solid {border_color};
                    border-radius: 8px;
                    color: {THEME['text_primary']};
                    padding: 10px 16px;
                    text-align: left;
                    font-weight: 500;
                }}
            ''')

        def enterEvent(self, event):
            self._animation.setStartValue(self._hover_progress)
            self._animation.setEndValue(1.0)
            self._animation.start()
            super().enterEvent(event)

        def leaveEvent(self, event):
            self._animation.setStartValue(self._hover_progress)
            self._animation.setEndValue(0.0)
            self._animation.start()
            super().leaveEvent(event)

        def mousePressEvent(self, event):
            self._pressed = True
            self._update_style()
            super().mousePressEvent(event)

        def mouseReleaseEvent(self, event):
            self._pressed = False
            self._update_style()
            super().mouseReleaseEvent(event)


    # ========================================================================
    # Visual Node with Professional Design
    # ========================================================================

    class VisualNode(QGraphicsRectItem):
        """A professional visual node with gradients, shadows, and animations"""

        def __init__(self, node_data: NodeData, parent=None):
            super().__init__(parent)
            self.node_data = node_data
            self.connections: List['ConnectionLine'] = []
            self._hover = False
            self._selected = False
            self._drag_start_pos = None

            self.setRect(0, 0, node_data.width, node_data.height)
            self.setPos(node_data.x, node_data.y)

            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
            self.setAcceptHoverEvents(True)
            self.setZValue(1)

            self.node_theme = NODE_TYPES.get(node_data.node_type, NODE_TYPES['class'])
            self.base_color = QColor(self.node_theme['color'])

            self._create_visual_elements()
            self._apply_shadow()

        def _create_visual_elements(self):
            """Create all visual elements for the node"""
            rect = self.rect()
            w, h = rect.width(), rect.height()

            gradient = QLinearGradient(0, 0, 0, h)
            gradient.setColorAt(0, QColor(self.node_theme['gradient_start']))
            gradient.setColorAt(0.3, QColor(self.node_theme['color']))
            gradient.setColorAt(1, QColor(self.node_theme['gradient_end']))

            self.setBrush(QBrush(gradient))
            self.setPen(QPen(self.base_color.darker(120), 2))

            self.header = QGraphicsRectItem(0, 0, w, 32, self)
            header_gradient = QLinearGradient(0, 0, 0, 32)
            header_gradient.setColorAt(0, QColor(255, 255, 255, 30))
            header_gradient.setColorAt(1, QColor(0, 0, 0, 30))
            self.header.setBrush(QBrush(header_gradient))
            self.header.setPen(QPen(Qt.PenStyle.NoPen))

            icon_size = 26
            self.icon_bg = QGraphicsEllipseItem(8, 4, icon_size, icon_size, self)
            self.icon_bg.setBrush(QBrush(QColor(THEME['bg_dark'])))
            self.icon_bg.setPen(QPen(self.base_color.lighter(120), 1.5))

            icon_text = self.node_theme['icon']
            self.icon_label = QGraphicsTextItem(icon_text, self)
            self.icon_label.setDefaultTextColor(self.base_color.lighter(130))
            icon_font = QFont(MONO_FONT, 10, QFont.Weight.Bold)
            self.icon_label.setFont(icon_font)
            icon_rect = self.icon_label.boundingRect()
            self.icon_label.setPos(
                8 + (icon_size - icon_rect.width()) / 2,
                4 + (icon_size - icon_rect.height()) / 2
            )

            self.name_label = QGraphicsTextItem(self.node_data.name, self)
            self.name_label.setDefaultTextColor(QColor("#ffffff"))
            self.name_label.setFont(QFont(SYSTEM_FONT, 11, QFont.Weight.Bold))
            self.name_label.setPos(40, 6)

            type_text = self.node_theme['label'].upper()
            self.type_label = QGraphicsTextItem(type_text, self)
            self.type_label.setDefaultTextColor(QColor(255, 255, 255, 150))
            self.type_label.setFont(QFont(SYSTEM_FONT, 8))
            type_rect = self.type_label.boundingRect()
            self.type_label.setPos(w - type_rect.width() - 10, 10)

            # Description area with background (always created, hidden if empty)
            self.desc_bg = QGraphicsRectItem(5, 36, w - 10, h - 44, self)
            self.desc_bg.setBrush(QBrush(QColor(0, 0, 0, 40)))
            self.desc_bg.setPen(QPen(Qt.PenStyle.NoPen))

            self.desc_label = QGraphicsTextItem("", self)
            self.desc_label.setDefaultTextColor(QColor(255, 255, 255, 200))
            self.desc_label.setFont(QFont(SYSTEM_FONT, 9))
            self.desc_label.setTextWidth(w - 20)
            self.desc_label.setPos(10, 38)

            if self.node_data.description:
                desc_text = self.node_data.description[:120]
                if len(self.node_data.description) > 120:
                    desc_text += "..."
                self.desc_label.setPlainText(desc_text)
                self.desc_bg.setVisible(True)
            else:
                self.desc_bg.setVisible(False)

            # Connection points - 8 for source nodes, 2 for others
            point_size = 10
            self.connection_points = []

            port_count = self.node_theme.get('port_count', 2)

            if port_count == 8:
                # Source node: 4 ports on each side
                for i in range(4):
                    y_pos = 20 + (h - 40) * (i + 0.5) / 4

                    # Right side ports
                    right_point = QGraphicsEllipseItem(
                        w - point_size/2, y_pos - point_size/2,
                        point_size, point_size, self
                    )
                    right_point.setBrush(QBrush(QColor(THEME['bg_dark'])))
                    right_point.setPen(QPen(self.base_color, 2))
                    right_point.setZValue(2)
                    self.connection_points.append((f'right_{i}', right_point))

                    # Left side ports
                    left_point = QGraphicsEllipseItem(
                        -point_size/2, y_pos - point_size/2,
                        point_size, point_size, self
                    )
                    left_point.setBrush(QBrush(QColor(THEME['bg_dark'])))
                    left_point.setPen(QPen(self.base_color, 2))
                    left_point.setZValue(2)
                    self.connection_points.append((f'left_{i}', left_point))
            else:
                # Standard node: 1 port on each side
                right_point = QGraphicsEllipseItem(
                    w - point_size/2, h/2 - point_size/2,
                    point_size, point_size, self
                )
                right_point.setBrush(QBrush(QColor(THEME['bg_dark'])))
                right_point.setPen(QPen(self.base_color, 2))
                right_point.setZValue(2)
                self.connection_points.append(('right', right_point))

                left_point = QGraphicsEllipseItem(
                    -point_size/2, h/2 - point_size/2,
                    point_size, point_size, self
                )
                left_point.setBrush(QBrush(QColor(THEME['bg_dark'])))
                left_point.setPen(QPen(self.base_color, 2))
                left_point.setZValue(2)
                self.connection_points.append(('left', left_point))

            self.bottom_line = QGraphicsRectItem(10, h - 4, w - 20, 2, self)
            self.bottom_line.setBrush(QBrush(self.base_color.lighter(130)))
            self.bottom_line.setPen(QPen(Qt.PenStyle.NoPen))

        def _apply_shadow(self):
            """Apply drop shadow effect"""
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(25)
            shadow.setColor(QColor(0, 0, 0, 120))
            shadow.setOffset(4, 4)
            self.setGraphicsEffect(shadow)

        def itemChange(self, change, value):
            """Handle position changes"""
            if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
                pos = self.pos()
                self.node_data.x = pos.x()
                self.node_data.y = pos.y()
                self.node_data.updated_at = datetime.now().isoformat()
                for conn in self.connections:
                    conn.update_path()
            elif change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
                self._selected = value
                self._update_visual_state()
            return super().itemChange(change, value)

        def _update_visual_state(self):
            """Update visual appearance based on state"""
            if self._selected:
                pen_width = 3
                pen_color = self.base_color.lighter(150)
            elif self._hover:
                pen_width = 2.5
                pen_color = self.base_color.lighter(130)
            else:
                pen_width = 2
                pen_color = self.base_color.darker(120)

            self.setPen(QPen(pen_color, pen_width))

        def get_connection_point(self, side: str) -> QPointF:
            """Get the connection point position for a side"""
            rect = self.sceneBoundingRect()
            if side == 'right':
                return QPointF(rect.right(), rect.center().y())
            elif side == 'left':
                return QPointF(rect.left(), rect.center().y())
            elif side == 'top':
                return QPointF(rect.center().x(), rect.top())
            elif side == 'bottom':
                return QPointF(rect.center().x(), rect.bottom())
            return rect.center()

        def get_nearest_connection_point(self, target: QPointF) -> Tuple[str, QPointF]:
            """Get the nearest connection point to a target"""
            sides = ['left', 'right', 'top', 'bottom']
            min_dist = float('inf')
            nearest = ('right', self.get_connection_point('right'))

            for side in sides:
                point = self.get_connection_point(side)
                dist = (point.x() - target.x())**2 + (point.y() - target.y())**2
                if dist < min_dist:
                    min_dist = dist
                    nearest = (side, point)

            return nearest

        def hoverEnterEvent(self, event):
            self._hover = True
            self._update_visual_state()
            super().hoverEnterEvent(event)

        def hoverLeaveEvent(self, event):
            self._hover = False
            self._update_visual_state()
            super().hoverLeaveEvent(event)

        def mousePressEvent(self, event):
            self._drag_start_pos = self.pos()
            super().mousePressEvent(event)

        def mouseReleaseEvent(self, event):
            if self._drag_start_pos and self._drag_start_pos != self.pos():
                canvas = self.scene().views()[0] if self.scene() and self.scene().views() else None
                if canvas and hasattr(canvas, 'undo_stack'):
                    cmd = MoveNodeCommand(canvas, self.node_data.id, self._drag_start_pos, self.pos())
                    canvas.undo_stack.push(cmd)
            self._drag_start_pos = None
            super().mouseReleaseEvent(event)

        def update_name(self, name: str):
            """Update the displayed name"""
            self.node_data.name = name
            self.name_label.setPlainText(name)
            self.node_data.updated_at = datetime.now().isoformat()

        def update_description(self, desc: str):
            """Update the description"""
            self.node_data.description = desc
            if hasattr(self, 'desc_label'):
                display_text = desc[:120] + "..." if len(desc) > 120 else desc
                self.desc_label.setPlainText(display_text)
            if hasattr(self, 'desc_bg'):
                self.desc_bg.setVisible(bool(desc))
            self.node_data.updated_at = datetime.now().isoformat()


    # ========================================================================
    # Connection Line with Bezier Curves and Arrows
    # ========================================================================

    class ConnectionLine(QGraphicsPathItem):
        """A sophisticated connection line with bezier curves and arrow head"""

        def __init__(self, start_node: VisualNode, end_node: VisualNode,
                     connection_data: ConnectionData = None, parent=None):
            super().__init__(parent)
            self.start_node = start_node
            self.end_node = end_node

            if connection_data:
                self.connection_data = connection_data
            else:
                self.connection_data = ConnectionData(
                    id=str(uuid.uuid4())[:8],
                    start_node_id=start_node.node_data.id,
                    end_node_id=end_node.node_data.id
                )

            start_node.connections.append(self)
            end_node.connections.append(self)

            self.line_color = QColor(self.connection_data.color)
            self._hover = False
            self._setup_style()
            self.setZValue(0)
            self.setAcceptHoverEvents(True)

            self.arrow_head = QGraphicsPolygonItem(self)
            self.arrow_head.setBrush(QBrush(self.line_color))
            self.arrow_head.setPen(QPen(Qt.PenStyle.NoPen))

            self.label_item = None
            if self.connection_data.label:
                self._create_label()

            self.update_path()

        def _setup_style(self):
            """Setup pen style based on connection data"""
            pen = QPen(self.line_color, 2.5)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)

            if self.connection_data.style == 'dashed':
                pen.setStyle(Qt.PenStyle.DashLine)
            elif self.connection_data.style == 'dotted':
                pen.setStyle(Qt.PenStyle.DotLine)
            else:
                pen.setStyle(Qt.PenStyle.SolidLine)

            self.setPen(pen)

        def _create_label(self):
            """Create label for the connection"""
            self.label_item = QGraphicsTextItem(self.connection_data.label, self)
            self.label_item.setDefaultTextColor(QColor(THEME['text_secondary']))
            self.label_item.setFont(QFont(SYSTEM_FONT, 9))

        def update_path(self):
            """Update the bezier curve path"""
            end_center = self.end_node.sceneBoundingRect().center()
            start_side, start_point = self.start_node.get_nearest_connection_point(end_center)

            start_center = self.start_node.sceneBoundingRect().center()
            end_side, end_point = self.end_node.get_nearest_connection_point(start_center)

            dx = end_point.x() - start_point.x()
            dy = end_point.y() - start_point.y()
            dist = math.sqrt(dx*dx + dy*dy)
            tension = min(dist * 0.4, 150)

            def get_direction(side):
                if side == 'right':
                    return QPointF(1, 0)
                elif side == 'left':
                    return QPointF(-1, 0)
                elif side == 'top':
                    return QPointF(0, -1)
                else:
                    return QPointF(0, 1)

            start_dir = get_direction(start_side)
            end_dir = get_direction(end_side)

            ctrl1 = QPointF(
                start_point.x() + start_dir.x() * tension,
                start_point.y() + start_dir.y() * tension
            )
            ctrl2 = QPointF(
                end_point.x() + end_dir.x() * tension,
                end_point.y() + end_dir.y() * tension
            )

            path = QPainterPath()
            path.moveTo(start_point)
            path.cubicTo(ctrl1, ctrl2, end_point)
            self.setPath(path)

            self._update_arrow(end_point, ctrl2)

            if self.label_item:
                mid_point = path.pointAtPercent(0.5)
                label_rect = self.label_item.boundingRect()
                self.label_item.setPos(
                    mid_point.x() - label_rect.width() / 2,
                    mid_point.y() - label_rect.height() / 2
                )

        def _update_arrow(self, tip: QPointF, control: QPointF):
            """Update arrow head at the end of the line"""
            dx = tip.x() - control.x()
            dy = tip.y() - control.y()
            length = math.sqrt(dx*dx + dy*dy)

            if length > 0:
                dx /= length
                dy /= length

            arrow_size = 12
            angle = math.pi / 6

            p1 = tip
            p2 = QPointF(
                tip.x() - arrow_size * (dx * math.cos(angle) - dy * math.sin(angle)),
                tip.y() - arrow_size * (dy * math.cos(angle) + dx * math.sin(angle))
            )
            p3 = QPointF(
                tip.x() - arrow_size * (dx * math.cos(angle) + dy * math.sin(angle)),
                tip.y() - arrow_size * (dy * math.cos(angle) - dx * math.sin(angle))
            )

            self.arrow_head.setPolygon(QPolygonF([p1, p2, p3]))

        def hoverEnterEvent(self, event):
            self._hover = True
            pen = self.pen()
            pen.setWidth(4)
            pen.setColor(self.line_color.lighter(130))
            self.setPen(pen)
            self.arrow_head.setBrush(QBrush(self.line_color.lighter(130)))
            super().hoverEnterEvent(event)

        def hoverLeaveEvent(self, event):
            self._hover = False
            self._setup_style()
            self.arrow_head.setBrush(QBrush(self.line_color))
            super().hoverLeaveEvent(event)

        def remove(self):
            """Remove this connection"""
            if self in self.start_node.connections:
                self.start_node.connections.remove(self)
            if self in self.end_node.connections:
                self.end_node.connections.remove(self)


    # ========================================================================
    # Node Properties Dialog
    # ========================================================================

    class NodePropertiesDialog(QDialog):
        """Dialog for editing node properties"""

        def __init__(self, node: VisualNode, parent=None):
            super().__init__(parent)
            self.node = node
            self.setWindowTitle("Node Properties")
            self.setMinimumSize(450, 400)
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            self._setup_ui()

        def _setup_ui(self):
            container = QFrame(self)
            container.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 12px;
                }}
                QLabel {{
                    color: {THEME['text_primary']};
                    font-size: 12px;
                }}
                QLineEdit, QTextEdit, QComboBox {{
                    background-color: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    padding: 8px;
                    color: {THEME['text_primary']};
                    font-size: 12px;
                }}
                QLineEdit:focus, QTextEdit:focus {{
                    border: 1px solid {THEME['accent_blue']};
                }}
            ''')

            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(container)

            layout = QVBoxLayout(container)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(16)

            header = QLabel("Edit Node")
            header.setFont(QFont(SYSTEM_FONT, 14, QFont.Weight.Bold))
            header.setStyleSheet(f'color: {THEME["accent_blue"]};')
            layout.addWidget(header)

            form = QFormLayout()
            form.setSpacing(12)

            self.name_edit = QLineEdit(self.node.node_data.name)
            form.addRow("Name:", self.name_edit)

            self.type_combo = QComboBox()
            for ntype in NODE_TYPES.keys():
                self.type_combo.addItem(NODE_TYPES[ntype]['label'], ntype)
            idx = self.type_combo.findData(self.node.node_data.node_type)
            if idx >= 0:
                self.type_combo.setCurrentIndex(idx)
            form.addRow("Type:", self.type_combo)

            self.desc_edit = QTextEdit()
            self.desc_edit.setPlainText(self.node.node_data.description)
            self.desc_edit.setMaximumHeight(100)
            form.addRow("Description:", self.desc_edit)

            layout.addLayout(form)

            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    padding: 10px 24px;
                    color: {THEME['text_primary']};
                }}
                QPushButton:hover {{
                    background-color: {THEME['bg_hover']};
                }}
            ''')
            cancel_btn.clicked.connect(self.reject)
            btn_layout.addWidget(cancel_btn)

            save_btn = QPushButton("Save")
            save_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {THEME['accent_blue']};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 24px;
                    color: white;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {QColor(THEME['accent_blue']).lighter(110).name()};
                }}
            ''')
            save_btn.clicked.connect(self.accept)
            btn_layout.addWidget(save_btn)

            layout.addLayout(btn_layout)

        def get_values(self) -> Tuple[str, str, str]:
            return (
                self.name_edit.text(),
                self.desc_edit.toPlainText(),
                self.type_combo.currentData()
            )


    # ========================================================================
    # Code Generator
    # ========================================================================

    class CodeGenerator:
        """Generates C++ and Python code from nodes."""

        @staticmethod
        def generate_cpp_header(node: NodeData) -> str:
            """Generate C++ header code for a node."""
            lines = []
            ntype = node.node_type
            name = node.name.replace(' ', '_')

            if ntype == 'class':
                lines.append(f"class {name} {{")
                lines.append("public:")
                lines.append(f"    {name}();")
                lines.append(f"    ~{name}();")
                lines.append("")
                lines.append("private:")
                lines.append("};")
            elif ntype == 'struct':
                lines.append(f"struct {name} {{")
                lines.append("};")
            elif ntype == 'enum':
                lines.append(f"enum class {name} {{")
                lines.append("    Value1,")
                lines.append("    Value2,")
                lines.append("};")
            elif ntype == 'function':
                lines.append(f"void {name}();")
            elif ntype == 'interface':
                lines.append(f"class I{name} {{")
                lines.append("public:")
                lines.append(f"    virtual ~I{name}() = default;")
                lines.append("};")
            elif ntype == 'namespace':
                lines.append(f"namespace {name} {{")
                lines.append("")
                lines.append(f"}} // namespace {name}")
            else:
                lines.append(f"// {node.node_type}: {name}")

            return '\n'.join(lines)

        @staticmethod
        def generate_cpp_source(node: NodeData) -> str:
            """Generate C++ source code for a node."""
            lines = []
            ntype = node.node_type
            name = node.name.replace(' ', '_')

            if ntype == 'class':
                lines.append(f"#include \"{name}.h\"")
                lines.append("")
                lines.append(f"{name}::{name}() {{")
                lines.append("}")
                lines.append("")
                lines.append(f"{name}::~{name}() {{")
                lines.append("}")
            elif ntype == 'function':
                lines.append(f"void {name}() {{")
                lines.append("    // TODO: Implement")
                lines.append("}")
            else:
                lines.append(f"// Implementation for {name}")

            return '\n'.join(lines)

        @staticmethod
        def generate_python(node: NodeData) -> str:
            """Generate Python code for a node."""
            lines = []
            ntype = node.node_type
            name = node.name.replace(' ', '_')

            if ntype in ('class', 'struct'):
                lines.append(f"class {name}:")
                lines.append('    """')
                if node.description:
                    lines.append(f"    {node.description}")
                lines.append('    """')
                lines.append("")
                lines.append("    def __init__(self):")
                lines.append("        pass")
            elif ntype == 'function':
                lines.append(f"def {name}():")
                lines.append('    """')
                if node.description:
                    lines.append(f"    {node.description}")
                lines.append('    """')
                lines.append("    pass")
            elif ntype == 'enum':
                lines.append("from enum import Enum, auto")
                lines.append("")
                lines.append(f"class {name}(Enum):")
                lines.append("    VALUE1 = auto()")
                lines.append("    VALUE2 = auto()")
            elif ntype == 'interface':
                lines.append("from abc import ABC, abstractmethod")
                lines.append("")
                lines.append(f"class {name}(ABC):")
                lines.append('    """Abstract base class."""')
                lines.append("")
                lines.append("    @abstractmethod")
                lines.append("    def method(self):")
                lines.append("        pass")
            else:
                lines.append(f"# {node.node_type}: {name}")

            return '\n'.join(lines)


    # ========================================================================
    # Code Preview Dialog
    # ========================================================================

    class CodePreviewDialog(QDialog):
        """Dialog for previewing generated code."""

        def __init__(self, node: VisualNode, parent=None):
            super().__init__(parent)
            self.node = node
            self.setWindowTitle("Code Preview")
            self.setMinimumSize(600, 500)
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self._setup_ui()

        def _setup_ui(self):
            container = QFrame(self)
            container.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 12px;
                }}
            ''')

            main_layout = QVBoxLayout(self)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(container)

            layout = QVBoxLayout(container)
            layout.setContentsMargins(20, 20, 20, 20)

            header = QHBoxLayout()
            title = QLabel("Code Preview")
            title.setFont(QFont(SYSTEM_FONT, 14, QFont.Weight.Bold))
            title.setStyleSheet(f'color: {THEME["accent_blue"]};')
            header.addWidget(title)
            header.addStretch()

            close_btn = QPushButton("×")
            close_btn.setFixedSize(28, 28)
            close_btn.setStyleSheet(f'''
                QPushButton {{
                    background: transparent;
                    color: {THEME['text_secondary']};
                    font-size: 18px;
                    border: none;
                }}
                QPushButton:hover {{
                    color: {THEME['accent_red']};
                }}
            ''')
            close_btn.clicked.connect(self.close)
            header.addWidget(close_btn)
            layout.addLayout(header)

            tabs = QTabWidget()
            tabs.setStyleSheet(f'''
                QTabWidget::pane {{
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    background: {THEME['bg_tertiary']};
                }}
                QTabBar::tab {{
                    background: {THEME['bg_tertiary']};
                    color: {THEME['text_secondary']};
                    padding: 10px 20px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }}
                QTabBar::tab:selected {{
                    background: {THEME['accent_blue']};
                    color: white;
                }}
            ''')

            cpp_header = QPlainTextEdit()
            cpp_header.setPlainText(CodeGenerator.generate_cpp_header(self.node.node_data))
            cpp_header.setFont(QFont(MONO_FONT, 11))
            cpp_header.setStyleSheet(f'''
                QPlainTextEdit {{
                    background: {THEME['bg_dark']};
                    color: {THEME['text_primary']};
                    border: none;
                    padding: 10px;
                }}
            ''')
            tabs.addTab(cpp_header, "C++ Header")

            cpp_source = QPlainTextEdit()
            cpp_source.setPlainText(CodeGenerator.generate_cpp_source(self.node.node_data))
            cpp_source.setFont(QFont(MONO_FONT, 11))
            cpp_source.setStyleSheet(cpp_header.styleSheet())
            tabs.addTab(cpp_source, "C++ Source")

            python_code = QPlainTextEdit()
            python_code.setPlainText(CodeGenerator.generate_python(self.node.node_data))
            python_code.setFont(QFont(MONO_FONT, 11))
            python_code.setStyleSheet(cpp_header.styleSheet())
            tabs.addTab(python_code, "Python")

            layout.addWidget(tabs)

            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            copy_btn = QPushButton("Copy to Clipboard")
            copy_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {THEME['accent_blue']};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 24px;
                    color: white;
                    font-weight: bold;
                }}
            ''')
            copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(
                tabs.currentWidget().toPlainText()
            ))
            btn_layout.addWidget(copy_btn)
            layout.addLayout(btn_layout)


    # ========================================================================
    # Search Panel
    # ========================================================================

    class SearchPanel(QFrame):
        """Panel for searching and filtering nodes."""

        search_requested = pyqtSignal(str)
        filter_changed = pyqtSignal(str)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedHeight(50)
            self._setup_ui()

        def _setup_ui(self):
            self.setStyleSheet(f'''
                QFrame {{
                    background: {THEME['bg_secondary']};
                    border-bottom: 1px solid {THEME['border']};
                }}
            ''')

            layout = QHBoxLayout(self)
            layout.setContentsMargins(16, 8, 16, 8)

            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Search nodes... (Ctrl+F)")
            self.search_input.setStyleSheet(f'''
                QLineEdit {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: {THEME['text_primary']};
                }}
                QLineEdit:focus {{
                    border: 1px solid {THEME['accent_blue']};
                }}
            ''')
            self.search_input.textChanged.connect(self.search_requested.emit)
            layout.addWidget(self.search_input)

            self.filter_combo = QComboBox()
            self.filter_combo.addItem("All Types", "all")
            for category, types in NODE_CATEGORIES.items():
                self.filter_combo.addItem(f"─ {category} ─", f"cat:{category}")
                for ntype in types:
                    if ntype in NODE_TYPES:
                        self.filter_combo.addItem(f"    {NODE_TYPES[ntype]['label']}", ntype)
            self.filter_combo.setStyleSheet(f'''
                QComboBox {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    padding: 8px 12px;
                    color: {THEME['text_primary']};
                    min-width: 150px;
                }}
            ''')
            self.filter_combo.currentIndexChanged.connect(
                lambda: self.filter_changed.emit(self.filter_combo.currentData())
            )
            layout.addWidget(self.filter_combo)


    # ========================================================================
    # Minimap Widget
    # ========================================================================

    class MinimapWidget(QFrame):
        """Minimap overview of the canvas."""

        def __init__(self, canvas: 'CodeMakerCanvas', parent=None):
            super().__init__(parent)
            self.canvas = canvas
            self.setFixedSize(200, 150)
            self._setup_ui()

        def _setup_ui(self):
            self.setStyleSheet(f'''
                QFrame {{
                    background: {THEME['bg_secondary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 8px;
                }}
            ''')

        def paintEvent(self, event):
            super().paintEvent(event)
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            painter.fillRect(self.rect(), QColor(THEME['bg_dark']))

            if not self.canvas.nodes:
                return

            min_x = min(n.node_data.x for n in self.canvas.nodes.values())
            max_x = max(n.node_data.x + n.node_data.width for n in self.canvas.nodes.values())
            min_y = min(n.node_data.y for n in self.canvas.nodes.values())
            max_y = max(n.node_data.y + n.node_data.height for n in self.canvas.nodes.values())

            content_width = max_x - min_x + 100
            content_height = max_y - min_y + 100

            scale_x = (self.width() - 20) / max(content_width, 1)
            scale_y = (self.height() - 20) / max(content_height, 1)
            scale = min(scale_x, scale_y)

            offset_x = 10 - min_x * scale
            offset_y = 10 - min_y * scale

            for node in self.canvas.nodes.values():
                x = node.node_data.x * scale + offset_x
                y = node.node_data.y * scale + offset_y
                w = node.node_data.width * scale
                h = node.node_data.height * scale

                color = QColor(node.node_theme['color'])
                painter.fillRect(int(x), int(y), int(w), int(h), color)

            viewport_rect = self.canvas.mapToScene(self.canvas.viewport().rect()).boundingRect()
            vx = viewport_rect.x() * scale + offset_x
            vy = viewport_rect.y() * scale + offset_y
            vw = viewport_rect.width() * scale
            vh = viewport_rect.height() * scale

            painter.setPen(QPen(QColor(THEME['accent_blue']), 2))
            painter.drawRect(int(vx), int(vy), int(vw), int(vh))

    def update_minimap(self):
        self.update()


    # ========================================================================
    # CodeMaker Canvas
    # ========================================================================

    class CodeMakerCanvas(QGraphicsView):
        """Professional interactive canvas with smooth pan/zoom"""

        node_count_changed = pyqtSignal(int)
        connection_count_changed = pyqtSignal(int)
        status_message = pyqtSignal(str)
        selection_changed = pyqtSignal(list)

        def __init__(self, parent=None):
            super().__init__(parent)

            self.scene = QGraphicsScene(self)
            self.scene.setSceneRect(-10000, -10000, 20000, 20000)
            self.setScene(self.scene)

            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
            self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            self._panning = False
            self._pan_start = QPointF()
            self._zoom_level = 1.0
            self._connecting_mode = False
            self._connect_start_node: Optional[VisualNode] = None
            self._temp_line: Optional[QGraphicsLineItem] = None
            self._rubber_band: Optional[QRubberBand] = None
            self._rubber_band_origin = QPointF()
            self._grid_visible = True
            self._clipboard: List[NodeData] = []

            self.nodes: Dict[str, VisualNode] = {}
            self.connections: List[ConnectionLine] = []
            self.groups: Dict[str, GroupData] = {}

            self.undo_stack = QUndoStack(self)

            self._draw_background()
            self._apply_style()
            self._setup_shortcuts()

        def _apply_style(self):
            self.setStyleSheet(f'''
                QGraphicsView {{
                    border: none;
                    background-color: {THEME['bg_dark']};
                }}
            ''')

        def _setup_shortcuts(self):
            """Setup keyboard shortcuts."""
            QShortcut(QKeySequence.StandardKey.Copy, self, self.copy_selected)
            QShortcut(QKeySequence.StandardKey.Paste, self, self.paste_nodes)
            QShortcut(QKeySequence.StandardKey.Cut, self, self.cut_selected)
            QShortcut(QKeySequence("Ctrl+D"), self, self.duplicate_selected)
            QShortcut(QKeySequence.StandardKey.Undo, self, self.undo_stack.undo)
            QShortcut(QKeySequence.StandardKey.Redo, self, self.undo_stack.redo)
            QShortcut(QKeySequence.StandardKey.SelectAll, self, self.select_all)
            QShortcut(QKeySequence("Ctrl+G"), self, self.group_selected)

        def _draw_background(self):
            """Draw professional grid background"""
            minor_pen = QPen(QColor(THEME['bg_secondary']), 0.5)
            minor_size = 25
            for x in range(-10000, 10000, minor_size):
                line = self.scene.addLine(x, -10000, x, 10000, minor_pen)
                line.setZValue(-100)
            for y in range(-10000, 10000, minor_size):
                line = self.scene.addLine(-10000, y, 10000, y, minor_pen)
                line.setZValue(-100)

            major_pen = QPen(QColor(THEME['bg_tertiary']), 1)
            major_size = 100
            for x in range(-10000, 10000, major_size):
                line = self.scene.addLine(x, -10000, x, 10000, major_pen)
                line.setZValue(-99)
            for y in range(-10000, 10000, major_size):
                line = self.scene.addLine(-10000, y, 10000, y, major_pen)
                line.setZValue(-99)

            center_pen = QPen(QColor(THEME['accent_blue']).darker(200), 2)
            self.scene.addLine(-50, 0, 50, 0, center_pen).setZValue(-98)
            self.scene.addLine(0, -50, 0, 50, center_pen).setZValue(-98)

        def add_node(self, node_type: str, name: str, x: float = None, y: float = None) -> VisualNode:
            """Add a new node to the canvas (with undo support)"""
            if x is None:
                x = self.mapToScene(self.viewport().rect().center()).x() - 100
            if y is None:
                y = self.mapToScene(self.viewport().rect().center()).y() - 50

            node_data = NodeData(
                id=str(uuid.uuid4())[:8],
                node_type=node_type,
                name=name,
                x=x,
                y=y
            )

            cmd = AddNodeCommand(self, node_data, f"Add {name}")
            self.undo_stack.push(cmd)

            return self.nodes.get(node_data.id)

        def _add_node_internal(self, node_data: NodeData) -> VisualNode:
            """Internal method to add node without undo."""
            visual_node = VisualNode(node_data)
            self.scene.addItem(visual_node)
            self.nodes[node_data.id] = visual_node
            self.node_count_changed.emit(len(self.nodes))
            self.status_message.emit(f"Created {node_data.node_type}: {node_data.name}")
            return visual_node

        def connect_nodes(self, start: VisualNode, end: VisualNode,
                         label: str = "", style: str = "solid") -> Optional[ConnectionLine]:
            """Create a connection between nodes"""
            if start == end:
                return None

            for conn in self.connections:
                if (conn.start_node == start and conn.end_node == end) or \
                   (conn.start_node == end and conn.end_node == start):
                    self.status_message.emit("Connection already exists")
                    return None

            conn_data = ConnectionData(
                id=str(uuid.uuid4())[:8],
                start_node_id=start.node_data.id,
                end_node_id=end.node_data.id,
                label=label,
                style=style
            )

            cmd = AddConnectionCommand(self, conn_data)
            self.undo_stack.push(cmd)

            return self.connections[-1] if self.connections else None

        def _add_connection_internal(self, conn_data: ConnectionData) -> Optional[ConnectionLine]:
            """Internal method to add connection without undo."""
            if conn_data.start_node_id not in self.nodes or conn_data.end_node_id not in self.nodes:
                return None

            start = self.nodes[conn_data.start_node_id]
            end = self.nodes[conn_data.end_node_id]

            connection = ConnectionLine(start, end, conn_data)
            self.scene.addItem(connection)
            self.connections.append(connection)

            if end.node_data.id not in start.node_data.connections:
                start.node_data.connections.append(end.node_data.id)
            if start.node_data.id not in end.node_data.connections:
                end.node_data.connections.append(start.node_data.id)

            self.connection_count_changed.emit(len(self.connections))
            return connection

        def delete_node(self, node: VisualNode):
            """Delete a node and its connections"""
            cmd = DeleteNodeCommand(self, node, f"Delete {node.node_data.name}")
            self.undo_stack.push(cmd)

        def _delete_node_internal(self, node: VisualNode):
            """Internal method to delete node without undo."""
            for conn in list(node.connections):
                self._delete_connection_internal(conn)

            if node.node_data.id in self.nodes:
                del self.nodes[node.node_data.id]

            self.scene.removeItem(node)
            self.node_count_changed.emit(len(self.nodes))
            self.status_message.emit(f"Deleted: {node.node_data.name}")

        def delete_connection(self, conn: ConnectionLine):
            """Delete a connection"""
            self._delete_connection_internal(conn)

        def _delete_connection_internal(self, conn: ConnectionLine):
            """Internal method to delete connection."""
            if conn in self.connections:
                self.connections.remove(conn)
            conn.remove()
            self.scene.removeItem(conn)
            self.connection_count_changed.emit(len(self.connections))

        def copy_selected(self):
            """Copy selected nodes to clipboard."""
            selected = [item for item in self.scene.selectedItems() if isinstance(item, VisualNode)]
            if not selected:
                return

            self._clipboard = [copy.deepcopy(node.node_data) for node in selected]
            self.status_message.emit(f"Copied {len(self._clipboard)} node(s)")

        def paste_nodes(self):
            """Paste nodes from clipboard."""
            if not self._clipboard:
                return

            center = self.mapToScene(self.viewport().rect().center())
            offset = 50

            self.scene.clearSelection()

            for node_data in self._clipboard:
                new_data = copy.deepcopy(node_data)
                new_data.id = str(uuid.uuid4())[:8]
                new_data.x = center.x() + offset
                new_data.y = center.y() + offset
                new_data.connections = []

                visual_node = self._add_node_internal(new_data)
                if visual_node:
                    visual_node.setSelected(True)
                offset += 30

            self.status_message.emit(f"Pasted {len(self._clipboard)} node(s)")

        def cut_selected(self):
            """Cut selected nodes."""
            self.copy_selected()
            for item in self.scene.selectedItems():
                if isinstance(item, VisualNode):
                    self.delete_node(item)

        def duplicate_selected(self):
            """Duplicate selected nodes."""
            self.copy_selected()
            self.paste_nodes()

        def select_all(self):
            """Select all nodes."""
            for node in self.nodes.values():
                node.setSelected(True)

        def group_selected(self):
            """Group selected nodes."""
            selected = [item for item in self.scene.selectedItems() if isinstance(item, VisualNode)]
            if len(selected) < 2:
                self.status_message.emit("Select at least 2 nodes to group")
                return

            name, ok = QInputDialog.getText(self, "Group Name", "Enter group name:")
            if not ok or not name:
                return

            group_data = GroupData(
                name=name,
                node_ids=[node.node_data.id for node in selected]
            )

            for node in selected:
                node.node_data.group_id = group_data.id

            self.groups[group_data.id] = group_data
            self.status_message.emit(f"Created group: {name}")

        def search_nodes(self, query: str):
            """Search and highlight nodes matching query."""
            query = query.lower()
            for node in self.nodes.values():
                matches = query in node.node_data.name.lower() or \
                         query in node.node_data.description.lower()
                node.setOpacity(1.0 if matches or not query else 0.3)

        def filter_by_type(self, type_filter: str):
            """Filter nodes by type."""
            if type_filter == "all":
                for node in self.nodes.values():
                    node.setVisible(True)
            elif type_filter.startswith("cat:"):
                category = type_filter[4:]
                types = NODE_CATEGORIES.get(category, [])
                for node in self.nodes.values():
                    node.setVisible(node.node_data.node_type in types)
            else:
                for node in self.nodes.values():
                    node.setVisible(node.node_data.node_type == type_filter)

        def get_map_data(self) -> MapData:
            """Export current state to MapData"""
            transform = self.transform()
            center = self.mapToScene(self.viewport().rect().center())

            return MapData(
                name="Untitled",
                nodes=[n.node_data for n in self.nodes.values()],
                connections=[c.connection_data for c in self.connections],
                groups=list(self.groups.values()),
                viewport_x=center.x(),
                viewport_y=center.y(),
                viewport_zoom=self._zoom_level,
                grid_visible=self._grid_visible
            )

        def load_map_data(self, map_data: MapData):
            """Load map from MapData"""
            self.clear_all()

            for node_data in map_data.nodes:
                visual_node = VisualNode(node_data)
                self.scene.addItem(visual_node)
                self.nodes[node_data.id] = visual_node

            for conn_data in map_data.connections:
                if conn_data.start_node_id in self.nodes and conn_data.end_node_id in self.nodes:
                    start = self.nodes[conn_data.start_node_id]
                    end = self.nodes[conn_data.end_node_id]
                    connection = ConnectionLine(start, end, conn_data)
                    self.scene.addItem(connection)
                    self.connections.append(connection)

            for group_data in map_data.groups:
                self.groups[group_data.id] = group_data

            self._zoom_level = map_data.viewport_zoom
            self.resetTransform()
            self.scale(self._zoom_level, self._zoom_level)
            self.centerOn(map_data.viewport_x, map_data.viewport_y)

            self.node_count_changed.emit(len(self.nodes))
            self.connection_count_changed.emit(len(self.connections))

        def clear_all(self):
            """Clear canvas"""
            for conn in list(self.connections):
                conn.remove()
                self.scene.removeItem(conn)
            for node in list(self.nodes.values()):
                self.scene.removeItem(node)

            self.nodes.clear()
            self.connections.clear()
            self.groups.clear()
            self.undo_stack.clear()

            self.node_count_changed.emit(0)
            self.connection_count_changed.emit(0)

        def export_to_image(self, file_path: str, format: str = "PNG"):
            """Export canvas to image."""
            if not self.nodes:
                return

            min_x = min(n.node_data.x for n in self.nodes.values()) - 50
            max_x = max(n.node_data.x + n.node_data.width for n in self.nodes.values()) + 50
            min_y = min(n.node_data.y for n in self.nodes.values()) - 50
            max_y = max(n.node_data.y + n.node_data.height for n in self.nodes.values()) + 50

            rect = QRectF(min_x, min_y, max_x - min_x, max_y - min_y)

            if format.upper() == "SVG":
                from PyQt6.QtSvg import QSvgGenerator
                generator = QSvgGenerator()
                generator.setFileName(file_path)
                generator.setSize(QSize(int(rect.width()), int(rect.height())))
                generator.setViewBox(QRect(0, 0, int(rect.width()), int(rect.height())))

                painter = QPainter(generator)
                self.scene.render(painter, QRectF(0, 0, rect.width(), rect.height()), rect)
                painter.end()
            else:
                image = QImage(int(rect.width()), int(rect.height()), QImage.Format.Format_ARGB32)
                image.fill(QColor(THEME['bg_dark']))

                painter = QPainter(image)
                painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                self.scene.render(painter, QRectF(0, 0, rect.width(), rect.height()), rect)
                painter.end()

                image.save(file_path, format)

            self.status_message.emit(f"Exported to {file_path}")

        def start_connection_mode(self, start_node: VisualNode):
            """Start connection mode from a node"""
            self._connecting_mode = True
            self._connect_start_node = start_node
            self.setCursor(Qt.CursorShape.CrossCursor)
            self.status_message.emit("Click on another node to connect (ESC to cancel)")

        def cancel_connection_mode(self):
            """Cancel connection mode"""
            self._connecting_mode = False
            self._connect_start_node = None
            if self._temp_line:
                self.scene.removeItem(self._temp_line)
                self._temp_line = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.status_message.emit("Connection cancelled")

        def wheelEvent(self, event: QWheelEvent):
            """Smooth zoom with wheel"""
            factor = 1.1

            if event.angleDelta().y() > 0:
                if self._zoom_level < 3.0:
                    self._zoom_level *= factor
                    self.scale(factor, factor)
            else:
                if self._zoom_level > 0.2:
                    self._zoom_level /= factor
                    self.scale(1/factor, 1/factor)

        def mousePressEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.MiddleButton:
                self._panning = True
                self._pan_start = event.position()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)
            elif self._connecting_mode and event.button() == Qt.MouseButton.LeftButton:
                scene_pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(scene_pos, self.transform())

                target_node = self._find_node_at(item)
                if target_node and target_node != self._connect_start_node:
                    self.connect_nodes(self._connect_start_node, target_node)
                    self.cancel_connection_mode()
                elif not target_node:
                    self.cancel_connection_mode()
            elif event.button() == Qt.MouseButton.LeftButton:
                scene_pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(scene_pos, self.transform())
                if not item or not self._find_node_at(item):
                    self._rubber_band_origin = event.pos()
                    if not self._rubber_band:
                        self._rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
                    self._rubber_band.setGeometry(QRect(event.pos(), QSize()))
                    self._rubber_band.show()
                super().mousePressEvent(event)
            else:
                super().mousePressEvent(event)

        def mouseMoveEvent(self, event: QMouseEvent):
            if self._panning:
                delta = event.position() - self._pan_start
                self._pan_start = event.position()
                self.horizontalScrollBar().setValue(
                    int(self.horizontalScrollBar().value() - delta.x())
                )
                self.verticalScrollBar().setValue(
                    int(self.verticalScrollBar().value() - delta.y())
                )
            elif self._rubber_band and self._rubber_band.isVisible():
                self._rubber_band.setGeometry(
                    QRect(self._rubber_band_origin, event.pos()).normalized()
                )
            elif self._connecting_mode and self._connect_start_node:
                scene_pos = self.mapToScene(event.pos())
                start = self._connect_start_node.get_connection_point('right')

                if not self._temp_line:
                    self._temp_line = self.scene.addLine(
                        start.x(), start.y(), scene_pos.x(), scene_pos.y(),
                        QPen(QColor(THEME['accent_blue']), 2, Qt.PenStyle.DashLine)
                    )
                else:
                    self._temp_line.setLine(start.x(), start.y(), scene_pos.x(), scene_pos.y())
            else:
                super().mouseMoveEvent(event)

        def mouseReleaseEvent(self, event: QMouseEvent):
            if event.button() == Qt.MouseButton.MiddleButton:
                self._panning = False
                self.setCursor(Qt.CursorShape.ArrowCursor)
            elif self._rubber_band and self._rubber_band.isVisible():
                selection_rect = self.mapToScene(self._rubber_band.geometry()).boundingRect()
                self._rubber_band.hide()

                if not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                    self.scene.clearSelection()

                for node in self.nodes.values():
                    if selection_rect.intersects(node.sceneBoundingRect()):
                        node.setSelected(True)
            else:
                super().mouseReleaseEvent(event)

        def keyPressEvent(self, event: QKeyEvent):
            move_amount = 50  # Grid step for arrow navigation

            if event.key() == Qt.Key.Key_Escape:
                if self._connecting_mode:
                    self.cancel_connection_mode()
                else:
                    self.scene.clearSelection()
            elif event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
                for item in self.scene.selectedItems():
                    if isinstance(item, VisualNode):
                        self.delete_node(item)
            elif event.key() == Qt.Key.Key_Home:
                self.centerOn(0, 0)
            elif event.key() == Qt.Key.Key_0 and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._zoom_level = 1.0
                self.resetTransform()
            # Arrow key navigation
            elif event.key() == Qt.Key.Key_Up:
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - move_amount)
            elif event.key() == Qt.Key.Key_Down:
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + move_amount)
            elif event.key() == Qt.Key.Key_Left:
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - move_amount)
            elif event.key() == Qt.Key.Key_Right:
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + move_amount)
            else:
                super().keyPressEvent(event)

        def _find_node_at(self, item) -> Optional[VisualNode]:
            """Find the VisualNode for an item"""
            if isinstance(item, VisualNode):
                return item
            elif item:
                parent = item.parentItem()
                while parent:
                    if isinstance(parent, VisualNode):
                        return parent
                    parent = parent.parentItem()
            return None

        def _create_categorized_menu(self, parent_menu: QMenu, scene_pos: QPointF):
            """Create categorized node creation submenu."""
            for category, types in NODE_CATEGORIES.items():
                cat_menu = parent_menu.addMenu(category)
                for node_type in types:
                    if node_type in NODE_TYPES:
                        config = NODE_TYPES[node_type]
                        action = cat_menu.addAction(f"{config['icon']}  {config['label']}")
                        action.setData((node_type, scene_pos))

        def contextMenuEvent(self, event):
            """Professional context menu"""
            scene_pos = self.mapToScene(event.pos())
            item = self.scene.itemAt(scene_pos, self.transform())
            node = self._find_node_at(item)

            menu = QMenu(self)
            menu.setStyleSheet(f'''
                QMenu {{
                    background-color: {THEME['bg_secondary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 8px;
                    padding: 8px;
                }}
                QMenu::item {{
                    background-color: transparent;
                    padding: 10px 24px 10px 16px;
                    color: {THEME['text_primary']};
                    border-radius: 4px;
                    margin: 2px 4px;
                }}
                QMenu::item:selected {{
                    background-color: {THEME['accent_blue']};
                }}
                QMenu::separator {{
                    height: 1px;
                    background: {THEME['border']};
                    margin: 6px 8px;
                }}
            ''')

            if node:
                props_action = menu.addAction("Properties...")
                rename_action = menu.addAction("Rename")
                desc_action = menu.addAction("Add Description...")
                menu.addSeparator()

                conn_menu = menu.addMenu("Connections")
                connect_action = conn_menu.addAction("Connect to...")
                disconnect_all = conn_menu.addAction("Disconnect All")

                menu.addSeparator()

                edit_menu = menu.addMenu("Edit")
                copy_action = edit_menu.addAction("Copy  (Ctrl+C)")
                cut_action = edit_menu.addAction("Cut  (Ctrl+X)")
                duplicate_action = edit_menu.addAction("Duplicate  (Ctrl+D)")

                menu.addSeparator()

                # Code menu - different options for source nodes
                code_menu = menu.addMenu("Code")
                create_python = None
                create_plugin = None
                preview_code = None
                gen_cpp_h = None
                gen_cpp_cpp = None
                gen_python = None

                if node.node_data.node_type == 'source':
                    # Source nodes get file generation options
                    if not node.node_data.generated_files.get('python'):
                        create_python = code_menu.addAction("Create Python")
                    if not node.node_data.generated_files.get('plugin'):
                        create_plugin = code_menu.addAction("Create Plugin")

                    if node.node_data.generated_files.get('python') or node.node_data.generated_files.get('plugin'):
                        code_menu.addSeparator()
                    if node.node_data.generated_files.get('python'):
                        code_menu.addAction(f"Python: {Path(node.node_data.generated_files['python']).name}").setEnabled(False)
                    if node.node_data.generated_files.get('plugin'):
                        code_menu.addAction(f"Plugin: {Path(node.node_data.generated_files['plugin']).name}").setEnabled(False)
                else:
                    # Non-source nodes get preview options
                    preview_code = code_menu.addAction("Preview Code...")
                    gen_cpp_h = code_menu.addAction("Generate C++ Header")
                    gen_cpp_cpp = code_menu.addAction("Generate C++ Source")
                    gen_python = code_menu.addAction("Generate Python")

                menu.addSeparator()
                delete_action = menu.addAction("Delete")

                action = menu.exec(event.globalPos())

                if action == props_action:
                    dialog = NodePropertiesDialog(node, self)
                    if dialog.exec() == QDialog.DialogCode.Accepted:
                        name, desc, ntype = dialog.get_values()
                        if name:
                            node.update_name(name)
                        node.update_description(desc)

                elif action == rename_action:
                    name, ok = QInputDialog.getText(
                        self, "Rename", "New name:", text=node.node_data.name
                    )
                    if ok and name:
                        node.update_name(name)

                elif action == desc_action:
                    desc, ok = QInputDialog.getMultiLineText(
                        self, "Description", "Enter description:",
                        text=node.node_data.description
                    )
                    if ok:
                        node.update_description(desc)

                elif action == connect_action:
                    self.start_connection_mode(node)

                elif action == disconnect_all:
                    for conn in list(node.connections):
                        self.delete_connection(conn)

                elif action == copy_action:
                    node.setSelected(True)
                    self.copy_selected()

                elif action == cut_action:
                    node.setSelected(True)
                    self.cut_selected()

                elif action == duplicate_action:
                    node.setSelected(True)
                    self.duplicate_selected()

                elif action == create_python and create_python:
                    self._create_python_file(node)

                elif action == create_plugin and create_plugin:
                    self._create_plugin_files(node)

                elif action == preview_code and preview_code:
                    dialog = CodePreviewDialog(node, self)
                    dialog.exec()

                elif action == gen_cpp_h and gen_cpp_h:
                    code = CodeGenerator.generate_cpp_header(node.node_data)
                    QApplication.clipboard().setText(code)
                    self.status_message.emit("C++ header copied to clipboard")

                elif action == gen_cpp_cpp and gen_cpp_cpp:
                    code = CodeGenerator.generate_cpp_source(node.node_data)
                    QApplication.clipboard().setText(code)
                    self.status_message.emit("C++ source copied to clipboard")

                elif action == gen_python and gen_python:
                    code = CodeGenerator.generate_python(node.node_data)
                    QApplication.clipboard().setText(code)
                    self.status_message.emit("Python code copied to clipboard")

                elif action == delete_action:
                    self.delete_node(node)

            else:
                # Quick Source creation at top
                create_source_action = menu.addAction("+ Create New Source")
                menu.addSeparator()

                create_menu = menu.addMenu("New")
                self._create_categorized_menu(create_menu, scene_pos)

                if self._clipboard:
                    menu.addSeparator()
                    paste_action = menu.addAction("Paste  (Ctrl+V)")

                menu.addSeparator()

                view_menu = menu.addMenu("View")
                center_action = view_menu.addAction("Center View  (Home)")
                fit_action = view_menu.addAction("Fit All Nodes")
                reset_zoom_action = view_menu.addAction("Reset Zoom  (Ctrl+0)")
                view_menu.addSeparator()
                toggle_grid = view_menu.addAction("Toggle Grid")
                toggle_grid.setCheckable(True)
                toggle_grid.setChecked(self._grid_visible)

                menu.addSeparator()

                select_menu = menu.addMenu("Selection")
                select_all_action = select_menu.addAction("Select All  (Ctrl+A)")
                deselect_action = select_menu.addAction("Deselect All")

                menu.addSeparator()

                export_menu = menu.addMenu("Export")
                export_png = export_menu.addAction("Export as PNG...")
                export_svg = export_menu.addAction("Export as SVG...")

                action = menu.exec(event.globalPos())

                if action == create_source_action:
                    name, ok = QInputDialog.getText(self, "New Source", "Source name:")
                    if ok and name:
                        self.add_node('source', name, scene_pos.x(), scene_pos.y())

                elif action and hasattr(action, 'data') and action.data():
                    data = action.data()
                    if isinstance(data, tuple):
                        node_type, pos = data
                        name, ok = QInputDialog.getText(
                            self, f"New {NODE_TYPES[node_type]['label']}", "Name:"
                        )
                        if ok and name:
                            self.add_node(node_type, name, pos.x(), pos.y())

                elif action and action.text() == "Paste  (Ctrl+V)":
                    self.paste_nodes()

                elif action == center_action:
                    self.centerOn(0, 0)

                elif action == fit_action:
                    if self.nodes:
                        min_x = min(n.node_data.x for n in self.nodes.values())
                        max_x = max(n.node_data.x + n.node_data.width for n in self.nodes.values())
                        min_y = min(n.node_data.y for n in self.nodes.values())
                        max_y = max(n.node_data.y + n.node_data.height for n in self.nodes.values())
                        rect = QRectF(min_x - 50, min_y - 50, max_x - min_x + 100, max_y - min_y + 100)
                        self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

                elif action == reset_zoom_action:
                    self._zoom_level = 1.0
                    self.resetTransform()

                elif action == toggle_grid:
                    self._grid_visible = not self._grid_visible

                elif action == select_all_action:
                    self.select_all()

                elif action == deselect_action:
                    self.scene.clearSelection()

                elif action == export_png:
                    file_path, _ = QFileDialog.getSaveFileName(
                        self, "Export as PNG", "", "PNG Files (*.png)"
                    )
                    if file_path:
                        self.export_to_image(file_path, "PNG")

                elif action == export_svg:
                    file_path, _ = QFileDialog.getSaveFileName(
                        self, "Export as SVG", "", "SVG Files (*.svg)"
                    )
                    if file_path:
                        self.export_to_image(file_path, "SVG")

        def _get_connected_nodes(self, source_node: VisualNode) -> List[VisualNode]:
            """Get all nodes connected to this source node (traverses full graph)."""
            connected = []
            visited = set()

            def traverse(node):
                if node.node_data.id in visited:
                    return
                visited.add(node.node_data.id)
                if node != source_node:
                    connected.append(node)
                for conn in node.connections:
                    other = conn.end_node if conn.start_node == node else conn.start_node
                    traverse(other)

            traverse(source_node)
            return connected

        def _create_python_file(self, node: VisualNode):
            """Create Python file from source node with all connected nodes."""
            name = node.node_data.name.replace(' ', '_').lower()
            project_path = self._get_project_path()
            file_path = project_path / f"{name}.py"

            connected = self._get_connected_nodes(node)

            # Build code from connections
            code_parts = [
                f'"""',
                f'{node.node_data.name}',
                f'{node.node_data.description or "Generated by IncludeCPP CodeMaker"}',
                f'"""',
                ''
            ]

            # Generate classes first
            for n in connected:
                if n.node_data.node_type in ('class', 'struct', 'interface', 'enum'):
                    code_parts.append(CodeGenerator.generate_python(n.node_data))
                    code_parts.append('')

            # Then functions
            for n in connected:
                if n.node_data.node_type in ('function', 'method', 'lambda', 'constructor', 'destructor'):
                    code_parts.append(CodeGenerator.generate_python(n.node_data))
                    code_parts.append('')

            # Main entry point
            code_parts.append('if __name__ == "__main__":')
            code_parts.append('    pass  # TODO: Entry point')

            try:
                file_path.write_text('\n'.join(code_parts), encoding='utf-8')
                node.node_data.generated_files['python'] = str(file_path)
                self.status_message.emit(f"Created: {file_path.name}")
            except Exception as e:
                self.status_message.emit(f"Error: {e}")

        def _create_plugin_files(self, node: VisualNode):
            """Create Plugin files from source node with all connected nodes."""
            name = node.node_data.name.replace(' ', '_').lower()
            project_path = self._get_project_path()
            connected = self._get_connected_nodes(node)

            # Create directories
            plugins_dir = project_path / "plugins"
            include_dir = project_path / "include"
            plugins_dir.mkdir(exist_ok=True)
            include_dir.mkdir(exist_ok=True)

            # Gather connected code
            classes = [n for n in connected if n.node_data.node_type in ('class', 'struct', 'interface', 'enum')]
            functions = [n for n in connected if n.node_data.node_type in ('function', 'method', 'constructor', 'destructor', 'lambda', 'operator')]

            try:
                # .h file (include/) - declarations for all connected nodes
                h_parts = [
                    '#pragma once',
                    f'// {node.node_data.name} - Generated by IncludeCPP CodeMaker',
                    f'// {node.node_data.description or ""}',
                    ''
                ]
                for c in classes:
                    h_parts.append(CodeGenerator.generate_cpp_header(c.node_data))
                    h_parts.append('')
                for f in functions:
                    h_parts.append(CodeGenerator.generate_cpp_header(f.node_data))
                    h_parts.append('')

                h_file = include_dir / f"{name}.h"
                h_file.write_text('\n'.join(h_parts), encoding='utf-8')

                # .cpp file (include/) - implementations
                cpp_parts = [f'#include "{name}.h"', '']
                for c in classes:
                    cpp_parts.append(CodeGenerator.generate_cpp_source(c.node_data))
                    cpp_parts.append('')
                for f in functions:
                    cpp_parts.append(CodeGenerator.generate_cpp_source(f.node_data))
                    cpp_parts.append('')

                cpp_file = include_dir / f"{name}.cpp"
                cpp_file.write_text('\n'.join(cpp_parts), encoding='utf-8')

                # .cp file (plugins/) - IncludeCPP plugin entry
                connected_names = ', '.join(n.node_data.name for n in connected) if connected else 'None'
                cp_content = f'''// {node.node_data.name} - IncludeCPP Plugin
// {node.node_data.description or 'Generated by CodeMaker'}
// Connected elements: {connected_names}

#include "{name}.h"

void {name}_init() {{
    // Plugin initialization
}}
'''
                cp_file = plugins_dir / f"{name}.cp"
                cp_file.write_text(cp_content, encoding='utf-8')

                node.node_data.generated_files['plugin'] = str(cp_file)
                self.status_message.emit(f"Created plugin: {name}.cp, {name}.h, {name}.cpp")
            except Exception as e:
                self.status_message.emit(f"Error: {e}")

        def _get_project_path(self) -> Path:
            """Get the project path from parent window."""
            for view in self.scene().views():
                if hasattr(view, 'window') and view.window():
                    win = view.window()
                    if hasattr(win, 'project_path'):
                        return win.project_path
            return Path.cwd()

        def align_horizontal(self):
            """Align selected nodes horizontally (same Y position)."""
            selected = [item for item in self.scene.selectedItems() if isinstance(item, VisualNode)]
            if len(selected) < 2:
                self.status_message.emit("Select at least 2 nodes to align")
                return

            # Use average Y position
            avg_y = sum(n.pos().y() for n in selected) / len(selected)
            for node in selected:
                node.setPos(node.pos().x(), avg_y)
                node.node_data.y = avg_y

            self.status_message.emit(f"Aligned {len(selected)} nodes horizontally")

        def align_vertical(self):
            """Align selected nodes vertically (same X position)."""
            selected = [item for item in self.scene.selectedItems() if isinstance(item, VisualNode)]
            if len(selected) < 2:
                self.status_message.emit("Select at least 2 nodes to align")
                return

            # Use average X position
            avg_x = sum(n.pos().x() for n in selected) / len(selected)
            for node in selected:
                node.setPos(avg_x, node.pos().y())
                node.node_data.x = avg_x

            self.status_message.emit(f"Aligned {len(selected)} nodes vertically")

        def auto_arrange(self):
            """Automatically arrange all nodes in a grid layout."""
            if not self.nodes:
                return

            nodes_list = list(self.nodes.values())
            n = len(nodes_list)

            # Calculate grid dimensions
            cols = max(1, int(n ** 0.5))
            rows = (n + cols - 1) // cols

            spacing_x = 250
            spacing_y = 150
            start_x = -((cols - 1) * spacing_x) / 2
            start_y = -((rows - 1) * spacing_y) / 2

            for i, node in enumerate(nodes_list):
                col = i % cols
                row = i // cols
                x = start_x + col * spacing_x
                y = start_y + row * spacing_y
                node.setPos(x, y)
                node.node_data.x = x
                node.node_data.y = y

            self.status_message.emit(f"Arranged {n} nodes in {rows}x{cols} grid")

        def distribute_horizontal(self):
            """Distribute selected nodes evenly horizontally."""
            selected = sorted(
                [item for item in self.scene.selectedItems() if isinstance(item, VisualNode)],
                key=lambda n: n.pos().x()
            )
            if len(selected) < 3:
                self.status_message.emit("Select at least 3 nodes to distribute")
                return

            min_x = selected[0].pos().x()
            max_x = selected[-1].pos().x()
            spacing = (max_x - min_x) / (len(selected) - 1)

            for i, node in enumerate(selected):
                new_x = min_x + i * spacing
                node.setPos(new_x, node.pos().y())
                node.node_data.x = new_x

            self.status_message.emit(f"Distributed {len(selected)} nodes horizontally")


    # ========================================================================
    # Properties Panel
    # ========================================================================

    class PropertiesPanel(QFrame):
        """Dockable panel for editing selected node properties."""

        property_changed = pyqtSignal(str, str, object)  # node_id, property, value

        def __init__(self, parent=None):
            super().__init__(parent)
            self.current_node = None
            self._setup_ui()

        def _setup_ui(self):
            self.setFixedWidth(260)
            self.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_primary']};
                    border-left: 1px solid {THEME['border']};
                }}
            ''')

            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            # Header
            header = QFrame()
            header.setFixedHeight(40)
            header.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-bottom: 1px solid {THEME['border']};
                }}
            ''')
            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(12, 0, 12, 0)

            title = QLabel("PROPERTIES")
            title.setFont(QFont(SYSTEM_FONT, 9, QFont.Weight.Bold))
            title.setStyleSheet(f'color: {THEME["text_muted"]}; letter-spacing: 1px;')
            header_layout.addWidget(title)
            layout.addWidget(header)

            # Content area (scrollable)
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.setStyleSheet(f'''
                QScrollArea {{
                    background-color: {THEME['bg_primary']};
                    border: none;
                }}
            ''')

            content = QWidget()
            content.setStyleSheet(f'background-color: {THEME["bg_primary"]};')
            self.content_layout = QVBoxLayout(content)
            self.content_layout.setContentsMargins(12, 12, 12, 12)
            self.content_layout.setSpacing(12)

            # Placeholder text
            self.placeholder = QLabel("Select a node to edit its properties")
            self.placeholder.setStyleSheet(f'color: {THEME["text_muted"]}; font-style: italic;')
            self.placeholder.setWordWrap(True)
            self.content_layout.addWidget(self.placeholder)

            # Name field
            self.name_label = QLabel("Name")
            self.name_label.setStyleSheet(f'color: {THEME["text_secondary"]}; font-size: 10px;')
            self.name_label.hide()
            self.content_layout.addWidget(self.name_label)

            self.name_input = QLineEdit()
            self.name_input.setStyleSheet(f'''
                QLineEdit {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 4px;
                    padding: 6px 8px;
                    color: {THEME['text_primary']};
                }}
                QLineEdit:focus {{ border-color: {THEME['accent_blue']}; }}
            ''')
            self.name_input.hide()
            self.name_input.textChanged.connect(self._on_name_changed)
            self.content_layout.addWidget(self.name_input)

            # Type display
            self.type_label = QLabel("Type")
            self.type_label.setStyleSheet(f'color: {THEME["text_secondary"]}; font-size: 10px;')
            self.type_label.hide()
            self.content_layout.addWidget(self.type_label)

            self.type_display = QLabel("")
            self.type_display.setStyleSheet(f'color: {THEME["text_primary"]}; font-weight: bold;')
            self.type_display.hide()
            self.content_layout.addWidget(self.type_display)

            # Description field
            self.desc_label = QLabel("Description")
            self.desc_label.setStyleSheet(f'color: {THEME["text_secondary"]}; font-size: 10px;')
            self.desc_label.hide()
            self.content_layout.addWidget(self.desc_label)

            self.desc_input = QTextEdit()
            self.desc_input.setMaximumHeight(80)
            self.desc_input.setStyleSheet(f'''
                QTextEdit {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 4px;
                    padding: 6px 8px;
                    color: {THEME['text_primary']};
                }}
                QTextEdit:focus {{ border-color: {THEME['accent_blue']}; }}
            ''')
            self.desc_input.hide()
            self.desc_input.textChanged.connect(self._on_desc_changed)
            self.content_layout.addWidget(self.desc_input)

            # Code status (for source nodes)
            self.code_section = QFrame()
            self.code_section.setStyleSheet(f'''
                QFrame {{
                    background: {THEME['bg_secondary']};
                    border-radius: 6px;
                    padding: 8px;
                }}
            ''')
            code_layout = QVBoxLayout(self.code_section)
            code_layout.setContentsMargins(8, 8, 8, 8)
            code_layout.setSpacing(4)

            code_title = QLabel("CODE STATUS")
            code_title.setStyleSheet(f'color: {THEME["text_muted"]}; font-size: 9px;')
            code_layout.addWidget(code_title)

            self.python_status = QLabel("Python: Not created")
            self.python_status.setStyleSheet(f'color: {THEME["text_secondary"]};')
            code_layout.addWidget(self.python_status)

            self.plugin_status = QLabel("Plugin: Not created")
            self.plugin_status.setStyleSheet(f'color: {THEME["text_secondary"]};')
            code_layout.addWidget(self.plugin_status)

            self.code_section.hide()
            self.content_layout.addWidget(self.code_section)

            self.content_layout.addStretch()

            scroll.setWidget(content)
            layout.addWidget(scroll)

        def update_selection(self, node: Optional[VisualNode]):
            """Update panel to show properties of selected node."""
            self.current_node = node

            if node is None:
                self.placeholder.show()
                self.name_label.hide()
                self.name_input.hide()
                self.type_label.hide()
                self.type_display.hide()
                self.desc_label.hide()
                self.desc_input.hide()
                self.code_section.hide()
                return

            self.placeholder.hide()

            # Show all fields
            self.name_label.show()
            self.name_input.show()
            self.type_label.show()
            self.type_display.show()
            self.desc_label.show()
            self.desc_input.show()

            # Update values
            self.name_input.blockSignals(True)
            self.name_input.setText(node.node_data.name)
            self.name_input.blockSignals(False)

            node_info = NODE_TYPES.get(node.node_data.node_type, {})
            self.type_display.setText(node_info.get('label', node.node_data.node_type))

            self.desc_input.blockSignals(True)
            self.desc_input.setPlainText(node.node_data.description)
            self.desc_input.blockSignals(False)

            # Code status for source nodes
            if node.node_data.node_type == 'source':
                self.code_section.show()
                py_path = node.node_data.generated_files.get('python', '')
                plugin_path = node.node_data.generated_files.get('plugin', '')

                if py_path:
                    self.python_status.setText(f"Python: {Path(py_path).name}")
                    self.python_status.setStyleSheet(f'color: {THEME["accent_green"]};')
                else:
                    self.python_status.setText("Python: Not created")
                    self.python_status.setStyleSheet(f'color: {THEME["text_secondary"]};')

                if plugin_path:
                    self.plugin_status.setText(f"Plugin: {Path(plugin_path).name}")
                    self.plugin_status.setStyleSheet(f'color: {THEME["accent_green"]};')
                else:
                    self.plugin_status.setText("Plugin: Not created")
                    self.plugin_status.setStyleSheet(f'color: {THEME["text_secondary"]};')
            else:
                self.code_section.hide()

        def _on_name_changed(self, text):
            if self.current_node and text:
                self.current_node.update_name(text)

        def _on_desc_changed(self):
            if self.current_node:
                self.current_node.update_description(self.desc_input.toPlainText())


    # ========================================================================
    # File Tree Panel
    # ========================================================================

    class FileTreePanel(QFrame):
        """Professional file tree for .ma map files"""

        file_selected = pyqtSignal(str)
        file_created = pyqtSignal(str)
        file_deleted = pyqtSignal(str)

        def __init__(self, project_path: Path, parent=None):
            super().__init__(parent)
            self.project_path = project_path
            self.maps_dir = project_path / ".includecpp" / "maps"
            self.maps_dir.mkdir(parents=True, exist_ok=True)

            self._setup_ui()
            self._load_files()

        def _setup_ui(self):
            self.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_primary']};
                    border-right: 1px solid {THEME['border']};
                }}
            ''')

            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            header = QFrame()
            header.setFixedHeight(48)
            header.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-bottom: 1px solid {THEME['border']};
                }}
            ''')

            header_layout = QHBoxLayout(header)
            header_layout.setContentsMargins(16, 0, 12, 0)

            title = QLabel("Maps")
            title.setFont(QFont(SYSTEM_FONT, 12, QFont.Weight.Bold))
            title.setStyleSheet(f'color: {THEME["text_primary"]};')
            header_layout.addWidget(title)

            header_layout.addStretch()

            new_btn = QPushButton("+")
            new_btn.setFixedSize(28, 28)
            new_btn.setStyleSheet(f'''
                QPushButton {{
                    background-color: {THEME['accent_blue']};
                    border: none;
                    border-radius: 14px;
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {QColor(THEME['accent_blue']).lighter(115).name()};
                }}
            ''')
            new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            new_btn.setToolTip("Create new map")
            new_btn.clicked.connect(self._create_new)
            header_layout.addWidget(new_btn)

            layout.addWidget(header)

            self.tree = QTreeWidget()
            self.tree.setHeaderHidden(True)
            self.tree.setIndentation(0)
            self.tree.setAnimated(True)
            self.tree.setStyleSheet(f'''
                QTreeWidget {{
                    background-color: {THEME['bg_primary']};
                    border: none;
                    color: {THEME['text_primary']};
                    font-size: 12px;
                    outline: none;
                }}
                QTreeWidget::item {{
                    padding: 12px 16px;
                    border-bottom: 1px solid {THEME['bg_secondary']};
                }}
                QTreeWidget::item:selected {{
                    background-color: {THEME['accent_blue']}40;
                    border-left: 3px solid {THEME['accent_blue']};
                }}
                QTreeWidget::item:hover:!selected {{
                    background-color: {THEME['bg_tertiary']};
                }}
            ''')
            self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.tree.customContextMenuRequested.connect(self._context_menu)
            self.tree.itemDoubleClicked.connect(self._on_double_click)
            layout.addWidget(self.tree)

        def _load_files(self):
            """Load .ma files"""
            self.tree.clear()

            for file_path in sorted(self.maps_dir.glob("*.ma")):
                item = QTreeWidgetItem([f"  {file_path.stem}"])
                item.setData(0, Qt.ItemDataRole.UserRole, str(file_path))
                item.setToolTip(0, file_path.name)
                self.tree.addTopLevelItem(item)

        def _create_new(self):
            """Create new map file"""
            name, ok = QInputDialog.getText(self, "New Map", "Map name:")
            if ok and name:
                safe_name = name.replace(" ", "_").replace("/", "_")
                file_path = self.maps_dir / f"{safe_name}.ma"

                map_data = MapData(name=name)
                file_path.write_text(json.dumps(map_data.to_dict(), indent=2), encoding='utf-8')

                self._load_files()
                self.file_created.emit(str(file_path))

        def _on_double_click(self, item, column):
            file_path = item.data(0, Qt.ItemDataRole.UserRole)
            if file_path:
                self.file_selected.emit(file_path)

        def _context_menu(self, pos):
            item = self.tree.itemAt(pos)
            if not item:
                return

            file_path = item.data(0, Qt.ItemDataRole.UserRole)

            menu = QMenu(self)
            menu.setStyleSheet(f'''
                QMenu {{
                    background-color: {THEME['bg_secondary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 8px;
                    padding: 4px;
                }}
                QMenu::item {{
                    padding: 10px 20px;
                    color: {THEME['text_primary']};
                    border-radius: 4px;
                    margin: 2px;
                }}
                QMenu::item:selected {{
                    background-color: {THEME['accent_blue']};
                }}
            ''')

            open_action = menu.addAction("Open")
            menu.addSeparator()
            rename_action = menu.addAction("Rename")
            clear_action = menu.addAction("Clear Contents")
            menu.addSeparator()
            delete_action = menu.addAction("Delete")

            action = menu.exec(self.tree.mapToGlobal(pos))

            if action == open_action:
                self.file_selected.emit(file_path)

            elif action == rename_action:
                old_name = Path(file_path).stem
                new_name, ok = QInputDialog.getText(
                    self, "Rename", "New name:", text=old_name
                )
                if ok and new_name and new_name != old_name:
                    new_path = self.maps_dir / f"{new_name}.ma"
                    Path(file_path).rename(new_path)
                    self._load_files()

            elif action == clear_action:
                map_data = MapData(name=Path(file_path).stem)
                Path(file_path).write_text(json.dumps(map_data.to_dict(), indent=2), encoding='utf-8')
                self.file_selected.emit(file_path)

            elif action == delete_action:
                reply = QMessageBox.question(
                    self, "Delete Map",
                    f"Are you sure you want to delete '{Path(file_path).stem}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.Yes:
                    Path(file_path).unlink()
                    self._load_files()
                    self.file_deleted.emit(file_path)


    # ========================================================================
    # Main Project Window
    # ========================================================================

    class ProjectWindow(QMainWindow):
        """Professional project interface main window"""

        def __init__(self, project_path: str = None):
            super().__init__()

            self.project_path = Path(project_path) if project_path else Path.cwd()
            self.current_file: Optional[str] = None
            self._drag_pos = None
            self._auto_save_timer = QTimer(self)
            self._auto_save_timer.timeout.connect(self._auto_save)
            self._auto_save_timer.start(30000)

            self._setup_window()
            self._setup_ui()

        def _setup_window(self):
            self.setWindowTitle("IncludeCPP - CodeMaker")
            self.setMinimumSize(1400, 900)
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        def _setup_ui(self):
            container = QWidget()
            container.setStyleSheet(f'''
                QWidget {{
                    background-color: {THEME['bg_primary']};
                    border-radius: 12px;
                }}
            ''')
            self.setCentralWidget(container)

            main_layout = QVBoxLayout(container)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)

            main_layout.addWidget(self._create_title_bar())
            main_layout.addWidget(self._create_toolbar())

            content = QWidget()
            content_layout = QHBoxLayout(content)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)

            content_layout.addWidget(self._create_sidebar())

            self.main_stack = QWidget()
            self.main_stack.setStyleSheet(f'background-color: {THEME["bg_dark"]};')
            self.main_stack_layout = QVBoxLayout(self.main_stack)
            self.main_stack_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.addWidget(self.main_stack, 1)

            main_layout.addWidget(content, 1)
            main_layout.addWidget(self._create_status_bar())

        def _create_title_bar(self) -> QFrame:
            bar = QFrame()
            bar.setFixedHeight(52)
            bar.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-top-left-radius: 12px;
                    border-top-right-radius: 12px;
                    border-bottom: 1px solid {THEME['border']};
                }}
            ''')

            layout = QHBoxLayout(bar)
            layout.setContentsMargins(20, 0, 16, 0)

            logo = QLabel("IncludeCPP")
            logo.setFont(QFont(SYSTEM_FONT, 13, QFont.Weight.Bold))
            logo.setStyleSheet(f'color: {THEME["accent_blue"]};')
            layout.addWidget(logo)

            sep = QLabel("|")
            sep.setStyleSheet(f'color: {THEME["border"]}; margin: 0 12px;')
            layout.addWidget(sep)

            self.title_label = QLabel("CodeMaker")
            self.title_label.setFont(QFont(SYSTEM_FONT, 11))
            self.title_label.setStyleSheet(f'color: {THEME["text_secondary"]};')
            layout.addWidget(self.title_label)

            exp_badge = QLabel("EXPERIMENTAL")
            exp_badge.setFont(QFont(SYSTEM_FONT, 8, QFont.Weight.Bold))
            exp_badge.setStyleSheet(f'''
                color: {THEME["accent_orange"]};
                background: {THEME["accent_orange"]}20;
                padding: 4px 8px;
                border-radius: 4px;
                margin-left: 12px;
            ''')
            layout.addWidget(exp_badge)

            layout.addStretch()

            for text, color, action in [
                ("−", THEME['bg_hover'], self.showMinimized),
                ("□", THEME['bg_hover'], self._toggle_maximize),
                ("×", THEME['accent_red'], self.close)
            ]:
                btn = QPushButton(text)
                btn.setFixedSize(40, 32)
                btn.setStyleSheet(f'''
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        border-radius: 6px;
                        color: {THEME['text_secondary']};
                        font-size: 16px;
                    }}
                    QPushButton:hover {{
                        background-color: {color};
                        color: {THEME['text_primary']};
                    }}
                ''')
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(action)
                layout.addWidget(btn)

            return bar

        def _create_toolbar(self) -> QFrame:
            """Create toolbar with common actions."""
            toolbar = QFrame()
            toolbar.setFixedHeight(44)
            toolbar.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-bottom: 1px solid {THEME['border']};
                }}
            ''')

            layout = QHBoxLayout(toolbar)
            layout.setContentsMargins(16, 4, 16, 4)
            layout.setSpacing(8)

            btn_style = f'''
                QPushButton {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    color: {THEME['text_primary']};
                    padding: 6px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: {THEME['bg_hover']};
                    border-color: {THEME['accent_blue']};
                }}
            '''

            save_btn = QPushButton("Save")
            save_btn.setStyleSheet(btn_style)
            save_btn.clicked.connect(self._save_current)
            layout.addWidget(save_btn)

            layout.addWidget(self._create_separator())

            undo_btn = QPushButton("Undo")
            undo_btn.setStyleSheet(btn_style)
            undo_btn.clicked.connect(lambda: self.canvas.undo_stack.undo() if hasattr(self, 'canvas') else None)
            layout.addWidget(undo_btn)

            redo_btn = QPushButton("Redo")
            redo_btn.setStyleSheet(btn_style)
            redo_btn.clicked.connect(lambda: self.canvas.undo_stack.redo() if hasattr(self, 'canvas') else None)
            layout.addWidget(redo_btn)

            layout.addWidget(self._create_separator())

            copy_btn = QPushButton("Copy")
            copy_btn.setStyleSheet(btn_style)
            copy_btn.clicked.connect(lambda: self.canvas.copy_selected() if hasattr(self, 'canvas') else None)
            layout.addWidget(copy_btn)

            paste_btn = QPushButton("Paste")
            paste_btn.setStyleSheet(btn_style)
            paste_btn.clicked.connect(lambda: self.canvas.paste_nodes() if hasattr(self, 'canvas') else None)
            layout.addWidget(paste_btn)

            layout.addWidget(self._create_separator())

            # Layout/Arrange buttons
            align_h_btn = QPushButton("Align H")
            align_h_btn.setStyleSheet(btn_style)
            align_h_btn.setToolTip("Align selected nodes horizontally")
            align_h_btn.clicked.connect(lambda: self.canvas.align_horizontal() if hasattr(self, 'canvas') else None)
            layout.addWidget(align_h_btn)

            align_v_btn = QPushButton("Align V")
            align_v_btn.setStyleSheet(btn_style)
            align_v_btn.setToolTip("Align selected nodes vertically")
            align_v_btn.clicked.connect(lambda: self.canvas.align_vertical() if hasattr(self, 'canvas') else None)
            layout.addWidget(align_v_btn)

            arrange_btn = QPushButton("Auto-Arrange")
            arrange_btn.setStyleSheet(btn_style)
            arrange_btn.setToolTip("Automatically arrange all nodes")
            arrange_btn.clicked.connect(lambda: self.canvas.auto_arrange() if hasattr(self, 'canvas') else None)
            layout.addWidget(arrange_btn)

            layout.addWidget(self._create_separator())

            # Quick-add buttons with accent colors
            source_btn = QPushButton("+ Source")
            source_btn.setStyleSheet(f'''
                QPushButton {{
                    background: {THEME['accent_green']};
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 6px 12px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: #00ff88;
                }}
            ''')
            source_btn.clicked.connect(lambda: self._quick_add_node('source'))
            layout.addWidget(source_btn)

            class_btn = QPushButton("+ Class")
            class_btn.setStyleSheet(f'''
                QPushButton {{
                    background: {THEME['accent_blue']};
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 6px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: #5abeff;
                }}
            ''')
            class_btn.clicked.connect(lambda: self._quick_add_node('class'))
            layout.addWidget(class_btn)

            func_btn = QPushButton("+ Function")
            func_btn.setStyleSheet(f'''
                QPushButton {{
                    background: #50c878;
                    border: none;
                    border-radius: 6px;
                    color: white;
                    padding: 6px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background: #60d888;
                }}
            ''')
            func_btn.clicked.connect(lambda: self._quick_add_node('function'))
            layout.addWidget(func_btn)

            layout.addStretch()

            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Search... (Ctrl+F)")
            self.search_input.setFixedWidth(200)
            self.search_input.setStyleSheet(f'''
                QLineEdit {{
                    background: {THEME['bg_tertiary']};
                    border: 1px solid {THEME['border']};
                    border-radius: 6px;
                    padding: 6px 12px;
                    color: {THEME['text_primary']};
                }}
                QLineEdit:focus {{
                    border-color: {THEME['accent_blue']};
                }}
            ''')
            self.search_input.textChanged.connect(
                lambda t: self.canvas.search_nodes(t) if hasattr(self, 'canvas') else None
            )
            layout.addWidget(self.search_input)

            return toolbar

        def _create_separator(self) -> QFrame:
            sep = QFrame()
            sep.setFixedSize(1, 24)
            sep.setStyleSheet(f'background: {THEME["border"]};')
            return sep

        def _create_sidebar(self) -> QFrame:
            sidebar = QFrame()
            sidebar.setFixedWidth(240)
            sidebar.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_primary']};
                    border-right: 1px solid {THEME['border']};
                }}
            ''')

            layout = QVBoxLayout(sidebar)
            layout.setContentsMargins(16, 20, 16, 20)
            layout.setSpacing(8)

            section = QLabel("TOOLS")
            section.setFont(QFont(SYSTEM_FONT, 9, QFont.Weight.Bold))
            section.setStyleSheet(f'color: {THEME["text_muted"]}; letter-spacing: 1px;')
            layout.addWidget(section)

            layout.addSpacing(8)

            codemaker_btn = AnimatedButton("CodeMaker", "◈", THEME['accent_blue'])
            codemaker_btn.clicked.connect(self._show_codemaker)
            layout.addWidget(codemaker_btn)

            layout.addStretch()

            info_frame = QFrame()
            info_frame.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-radius: 8px;
                    padding: 12px;
                }}
            ''')
            info_layout = QVBoxLayout(info_frame)
            info_layout.setContentsMargins(12, 12, 12, 12)
            info_layout.setSpacing(4)

            proj_label = QLabel("PROJECT")
            proj_label.setFont(QFont(SYSTEM_FONT, 8))
            proj_label.setStyleSheet(f'color: {THEME["text_muted"]};')
            info_layout.addWidget(proj_label)

            proj_name = QLabel(self.project_path.name)
            proj_name.setFont(QFont(SYSTEM_FONT, 10, QFont.Weight.Bold))
            proj_name.setStyleSheet(f'color: {THEME["text_primary"]};')
            proj_name.setWordWrap(True)
            info_layout.addWidget(proj_name)

            layout.addWidget(info_frame)

            return sidebar

        def _create_status_bar(self) -> QFrame:
            bar = QFrame()
            bar.setFixedHeight(28)
            bar.setStyleSheet(f'''
                QFrame {{
                    background-color: {THEME['bg_secondary']};
                    border-bottom-left-radius: 12px;
                    border-bottom-right-radius: 12px;
                    border-top: 1px solid {THEME['border']};
                }}
            ''')

            layout = QHBoxLayout(bar)
            layout.setContentsMargins(16, 0, 16, 0)

            self.status_label = QLabel("Ready")
            self.status_label.setFont(QFont(SYSTEM_FONT, 9))
            self.status_label.setStyleSheet(f'color: {THEME["text_muted"]};')
            layout.addWidget(self.status_label)

            layout.addStretch()

            self.node_count_label = QLabel("Nodes: 0")
            self.node_count_label.setStyleSheet(f'color: {THEME["text_muted"]}; margin-right: 16px;')
            layout.addWidget(self.node_count_label)

            self.connection_count_label = QLabel("Connections: 0")
            self.connection_count_label.setStyleSheet(f'color: {THEME["text_muted"]}; margin-right: 16px;')
            layout.addWidget(self.connection_count_label)

            self.zoom_label = QLabel("Zoom: 100%")
            self.zoom_label.setStyleSheet(f'color: {THEME["text_muted"]};')
            layout.addWidget(self.zoom_label)

            return bar

        def _show_codemaker(self):
            """Display CodeMaker interface"""
            while self.main_stack_layout.count():
                item = self.main_stack_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            self.title_label.setText("CodeMaker")

            codemaker = QWidget()
            codemaker_layout = QHBoxLayout(codemaker)
            codemaker_layout.setContentsMargins(0, 0, 0, 0)
            codemaker_layout.setSpacing(0)

            self.file_tree = FileTreePanel(self.project_path)
            self.file_tree.setFixedWidth(220)
            self.file_tree.file_selected.connect(self._load_map)
            codemaker_layout.addWidget(self.file_tree)

            self.canvas = CodeMakerCanvas()
            self.canvas.node_count_changed.connect(
                lambda n: self.node_count_label.setText(f"Nodes: {n}")
            )
            self.canvas.connection_count_changed.connect(
                lambda n: self.connection_count_label.setText(f"Connections: {n}")
            )
            self.canvas.status_message.connect(
                lambda msg: self.status_label.setText(msg)
            )
            # Wire selection changes to properties panel
            self.canvas.scene.selectionChanged.connect(self._on_selection_changed)
            codemaker_layout.addWidget(self.canvas, 1)

            # Properties panel on the right
            self.properties_panel = PropertiesPanel()
            codemaker_layout.addWidget(self.properties_panel)

            self.main_stack_layout.addWidget(codemaker)

        def _on_selection_changed(self):
            """Handle selection change in canvas."""
            if not hasattr(self, 'canvas') or not hasattr(self, 'properties_panel'):
                return

            selected = [item for item in self.canvas.scene.selectedItems()
                       if isinstance(item, VisualNode)]

            if len(selected) == 1:
                self.properties_panel.update_selection(selected[0])
            else:
                self.properties_panel.update_selection(None)

        def _load_map(self, file_path: str):
            """Load a map file"""
            try:
                data = json.loads(Path(file_path).read_text(encoding='utf-8'))
                map_data = MapData.from_dict(data)
                self.canvas.load_map_data(map_data)
                self.current_file = file_path
                self.title_label.setText(f"CodeMaker - {map_data.name}")
                self.status_label.setText(f"Loaded: {Path(file_path).stem}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load map: {e}")

        def _save_current(self):
            """Save current map"""
            if self.current_file and hasattr(self, 'canvas'):
                try:
                    map_data = self.canvas.get_map_data()
                    map_data.name = Path(self.current_file).stem
                    Path(self.current_file).write_text(
                        json.dumps(map_data.to_dict(), indent=2),
                        encoding='utf-8'
                    )
                    self.status_label.setText(f"Saved: {map_data.name}")
                except Exception as e:
                    self.status_label.setText(f"Save failed: {e}")

        def _auto_save(self):
            """Auto-save callback"""
            if self.current_file and hasattr(self, 'canvas'):
                self._save_current()

        def _toggle_maximize(self):
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

        def mousePressEvent(self, event):
            if event.button() == Qt.MouseButton.LeftButton and event.position().y() < 52:
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

        def mouseMoveEvent(self, event):
            if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
                self.move(event.globalPosition().toPoint() - self._drag_pos)

        def mouseReleaseEvent(self, event):
            self._drag_pos = None

        def _quick_add_node(self, node_type: str):
            """Quick-add a node from toolbar button."""
            if not hasattr(self, 'canvas'):
                return

            name, ok = QInputDialog.getText(
                self, f"New {NODE_TYPES[node_type]['label']}",
                "Name:"
            )
            if ok and name:
                # Add at center of current view
                center = self.canvas.mapToScene(
                    self.canvas.viewport().rect().center()
                )
                self.canvas.add_node(node_type, name, center.x(), center.y())

        def closeEvent(self, event):
            self._save_current()
            super().closeEvent(event)


    def show_project(project_path: str = None) -> Tuple[bool, str]:
        """Launch the project interface"""
        if not PYQT_AVAILABLE:
            return False, "PyQt6 not installed. Run: pip install PyQt6"

        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)

        window = ProjectWindow(project_path)
        window.show()
        window._show_codemaker()

        app.exec()
        return True, "Project closed"


else:
    def show_project(project_path: str = None) -> Tuple[bool, str]:
        return False, "PyQt6 not installed. Run: pip install PyQt6"


if __name__ == '__main__':
    success, msg = show_project()
    if not success:
        print(msg)
