"""
CSSL GUI Builder - Dark theme constants and QSS stylesheet.
"""

# Color constants (matching exe_wizard.py style)
DARK_BG = "#0a0a0a"
DARK_SURFACE = "#141414"
DARK_CARD = "#1a1a1a"
DARK_BORDER = "#2a2a2a"
DARK_HOVER = "#252525"
ACCENT_COLOR = "#ffffff"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#888888"
TEXT_MUTED = "#555555"
SUCCESS_COLOR = "#4ade80"
ERROR_COLOR = "#f87171"
WARNING_COLOR = "#fbbf24"
SELECTION_COLOR = "#3b82f6"
CANVAS_BG = "#1e1e1e"
CANVAS_WINDOW_BG = "#f0f0f0"
GRID_COLOR = "#2a2a2a"
HANDLE_COLOR = "#3b82f6"
WIDGET_BORDER = "#cccccc"
WIDGET_BG = "#ffffff"
WIDGET_TEXT = "#000000"

STYLESHEET = f"""
/* === Base === */
QMainWindow {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
    font-size: 13px;
}}

QWidget {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', sans-serif;
    font-size: 13px;
}}

/* === Dock Widgets === */
QDockWidget {{
    color: {TEXT_PRIMARY};
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
    font-weight: bold;
    font-size: 12px;
    border: none;
}}

QDockWidget::title {{
    background-color: {DARK_SURFACE};
    padding: 8px 12px;
    border-bottom: 1px solid {DARK_BORDER};
    text-align: left;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    border: none;
    background: transparent;
    padding: 0px;
    icon-size: 12px;
}}

/* === Toolbar === */
QToolBar {{
    background-color: {DARK_SURFACE};
    border-bottom: 1px solid {DARK_BORDER};
    padding: 4px 8px;
    spacing: 4px;
}}

QToolBar QToolButton {{
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 6px 12px;
    color: {TEXT_SECONDARY};
    font-size: 12px;
    min-width: 28px;
}}

QToolBar QToolButton:hover {{
    background-color: {DARK_HOVER};
    border-color: {DARK_BORDER};
    color: {TEXT_PRIMARY};
}}

QToolBar QToolButton:pressed {{
    background-color: {DARK_BORDER};
}}

QToolBar QToolButton:disabled {{
    color: {TEXT_MUTED};
}}

QToolBar::separator {{
    width: 1px;
    background-color: {DARK_BORDER};
    margin: 4px 6px;
}}

/* === Menu Bar === */
QMenuBar {{
    background-color: {DARK_SURFACE};
    color: {TEXT_SECONDARY};
    border-bottom: 1px solid {DARK_BORDER};
    padding: 2px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 6px 12px;
    border-radius: 4px;
}}

QMenuBar::item:selected {{
    background-color: {DARK_HOVER};
    color: {TEXT_PRIMARY};
}}

QMenu {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 32px 8px 16px;
    border-radius: 4px;
    color: {TEXT_SECONDARY};
}}

QMenu::item:selected {{
    background-color: {DARK_HOVER};
    color: {TEXT_PRIMARY};
}}

QMenu::separator {{
    height: 1px;
    background-color: {DARK_BORDER};
    margin: 4px 8px;
}}

/* === Scroll Bars === */
QScrollBar:vertical {{
    background-color: transparent;
    width: 8px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: {DARK_BORDER};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {TEXT_MUTED};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar:horizontal {{
    background-color: transparent;
    height: 8px;
    margin: 0;
}}

QScrollBar::handle:horizontal {{
    background-color: {DARK_BORDER};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {TEXT_MUTED};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* === Tree Widget === */
QTreeWidget {{
    background-color: {DARK_SURFACE};
    border: none;
    outline: none;
    font-size: 12px;
}}

QTreeWidget::item {{
    padding: 4px 8px;
    border-radius: 4px;
    color: {TEXT_SECONDARY};
}}

QTreeWidget::item:hover {{
    background-color: {DARK_HOVER};
    color: {TEXT_PRIMARY};
}}

QTreeWidget::item:selected {{
    background-color: {SELECTION_COLOR}30;
    color: {TEXT_PRIMARY};
    border: none;
}}

QTreeWidget::branch {{
    background-color: transparent;
}}

QHeaderView::section {{
    background-color: {DARK_SURFACE};
    color: {TEXT_MUTED};
    border: none;
    border-bottom: 1px solid {DARK_BORDER};
    padding: 6px 8px;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
}}

/* === Input Fields === */
QLineEdit {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
    selection-background-color: {SELECTION_COLOR};
}}

QLineEdit:focus {{
    border-color: {SELECTION_COLOR};
}}

QLineEdit:disabled {{
    color: {TEXT_MUTED};
    background-color: {DARK_SURFACE};
}}

/* === Spin Box === */
QSpinBox, QDoubleSpinBox {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 4px 8px;
    color: {TEXT_PRIMARY};
    min-width: 60px;
}}

QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {SELECTION_COLOR};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{
    border: none;
    background-color: transparent;
    width: 16px;
}}

/* === Combo Box === */
QComboBox {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    color: {TEXT_PRIMARY};
    min-width: 80px;
}}

QComboBox:hover {{
    border-color: {TEXT_MUTED};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 4px;
    selection-background-color: {DARK_HOVER};
    selection-color: {TEXT_PRIMARY};
    outline: none;
}}

/* === Check Box === */
QCheckBox {{
    color: {TEXT_SECONDARY};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid {DARK_BORDER};
    background-color: {DARK_CARD};
}}

QCheckBox::indicator:checked {{
    background-color: {SELECTION_COLOR};
    border-color: {SELECTION_COLOR};
}}

QCheckBox::indicator:hover {{
    border-color: {TEXT_MUTED};
}}

/* === Push Button === */
QPushButton {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 6px 16px;
    color: {TEXT_SECONDARY};
    min-height: 28px;
}}

QPushButton:hover {{
    background-color: {DARK_HOVER};
    color: {TEXT_PRIMARY};
    border-color: {TEXT_MUTED};
}}

QPushButton:pressed {{
    background-color: {DARK_BORDER};
}}

QPushButton:disabled {{
    color: {TEXT_MUTED};
    background-color: {DARK_SURFACE};
}}

QPushButton#primary {{
    background-color: {TEXT_PRIMARY};
    color: {DARK_BG};
    border: none;
    font-weight: bold;
}}

QPushButton#primary:hover {{
    background-color: #e0e0e0;
    color: {DARK_BG};
}}

QPushButton#primary:pressed {{
    background-color: #cccccc;
}}

QPushButton#danger {{
    color: {ERROR_COLOR};
    border-color: {ERROR_COLOR}40;
}}

QPushButton#danger:hover {{
    background-color: {ERROR_COLOR}20;
    border-color: {ERROR_COLOR};
}}

/* === Tab Widget === */
QTabWidget::pane {{
    border: 1px solid {DARK_BORDER};
    background-color: {DARK_SURFACE};
    border-radius: 4px;
}}

QTabBar::tab {{
    background-color: {DARK_CARD};
    color: {TEXT_MUTED};
    padding: 8px 16px;
    border: 1px solid {DARK_BORDER};
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {DARK_SURFACE};
    color: {TEXT_PRIMARY};
    border-bottom: 2px solid {SELECTION_COLOR};
}}

QTabBar::tab:hover:!selected {{
    background-color: {DARK_HOVER};
    color: {TEXT_SECONDARY};
}}

/* === Graphics View (Canvas) === */
QGraphicsView {{
    background-color: {CANVAS_BG};
    border: none;
}}

/* === Splitter === */
QSplitter::handle {{
    background-color: {DARK_BORDER};
}}

QSplitter::handle:horizontal {{
    width: 1px;
}}

QSplitter::handle:vertical {{
    height: 1px;
}}

/* === Status Bar === */
QStatusBar {{
    background-color: {DARK_SURFACE};
    color: {TEXT_MUTED};
    border-top: 1px solid {DARK_BORDER};
    font-size: 11px;
    padding: 2px 8px;
}}

/* === Label Styles === */
QLabel#sectionTitle {{
    color: {TEXT_MUTED};
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    padding: 4px 0;
}}

QLabel#propertyLabel {{
    color: {TEXT_SECONDARY};
    font-size: 12px;
    padding: 2px 0;
}}

/* === Tooltips === */
QToolTip {{
    background-color: {DARK_CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* === Group Box === */
QGroupBox {{
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 16px;
    color: {TEXT_SECONDARY};
    font-weight: bold;
    font-size: 11px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {TEXT_MUTED};
}}

/* === Text Edit === */
QTextEdit, QPlainTextEdit {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 4px;
    padding: 8px;
    color: {TEXT_PRIMARY};
    selection-background-color: {SELECTION_COLOR};
    font-family: 'Consolas', 'Fira Code', 'Courier New', monospace;
    font-size: 13px;
}}

QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {SELECTION_COLOR};
}}
"""
