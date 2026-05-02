"""
G13LogitechOPS Stylesheet

Windows Logitech Gaming Software inspired dark theme with signature blue accents.
"""

# Logitech signature colors
LOGITECH_BLUE = "#00B8FC"
LOGITECH_BLUE_HOVER = "#33c9ff"
LOGITECH_BLUE_PRESSED = "#0099d4"

DARK_THEME = """
/* ============================================
   G13LogitechOPS - Dark Theme
   Inspired by Windows Logitech Gaming Software
   ============================================ */

/* Main Window */
QMainWindow {
    background-color: #1a1a1a;
}

QWidget {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Segoe UI', 'Ubuntu', 'Noto Sans', sans-serif;
    font-size: 11px;
}

/* ============================================
   Tab Widget - Modern LGS Style
   ============================================ */
QTabWidget::pane {
    border: 1px solid #333;
    background-color: #222;
    border-radius: 4px;
    top: -1px;
}

QTabBar::tab {
    background-color: #2a2a2a;
    color: #888;
    padding: 10px 18px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 70px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background-color: #222;
    color: #00B8FC;
    border-bottom: 2px solid #00B8FC;
}

QTabBar::tab:hover:!selected {
    background-color: #333;
    color: #ccc;
}

/* ============================================
   Buttons - Logitech Style
   ============================================ */
QPushButton {
    background-color: #333;
    color: #e0e0e0;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 8px 16px;
    min-height: 26px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #444;
    border-color: #00B8FC;
    color: #fff;
}

QPushButton:pressed {
    background-color: #00B8FC;
    color: #000;
}

QPushButton:disabled {
    background-color: #222;
    color: #555;
    border-color: #333;
}

/* Primary Action Button */
QPushButton#primaryButton, QPushButton[primary="true"] {
    background-color: #00B8FC;
    color: #000;
    font-weight: bold;
    border: none;
}

QPushButton#primaryButton:hover, QPushButton[primary="true"]:hover {
    background-color: #33c9ff;
}

QPushButton#primaryButton:pressed, QPushButton[primary="true"]:pressed {
    background-color: #0099d4;
}

/* Danger Button */
QPushButton#dangerButton, QPushButton[danger="true"] {
    background-color: #4a2a2a;
    border-color: #6a3a3a;
}

QPushButton#dangerButton:hover, QPushButton[danger="true"]:hover {
    background-color: #6a3a3a;
    border-color: #ff5555;
    color: #ff8888;
}

/* ============================================
   List Widget - Profile List
   ============================================ */
QListWidget {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    padding: 10px 12px;
    border-radius: 3px;
    margin: 2px 0;
}

QListWidget::item:selected {
    background-color: #00B8FC;
    color: #000;
}

QListWidget::item:hover:!selected {
    background-color: #2a2a2a;
}

QListWidget::item:focus {
    outline: none;
}

/* ============================================
   Tree Widget
   ============================================ */
QTreeWidget {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 4px;
    outline: none;
}

QTreeWidget::item {
    padding: 6px 8px;
    border-radius: 3px;
}

QTreeWidget::item:selected {
    background-color: #00B8FC;
    color: #000;
}

QTreeWidget::item:hover:!selected {
    background-color: #2a2a2a;
}

QHeaderView::section {
    background-color: #2a2a2a;
    color: #888;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #333;
    font-weight: bold;
}

/* ============================================
   Group Box
   ============================================ */
QGroupBox {
    font-weight: bold;
    border: 1px solid #333;
    border-radius: 6px;
    margin-top: 14px;
    padding: 12px 8px 8px 8px;
    background-color: #222;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 10px;
    color: #00B8FC;
    font-size: 11px;
}

/* ============================================
   Combo Box
   ============================================ */
QComboBox {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 6px 12px;
    min-height: 26px;
    color: #e0e0e0;
}

QComboBox:hover {
    border-color: #00B8FC;
}

QComboBox:focus {
    border-color: #00B8FC;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
    subcontrol-position: center right;
}

QComboBox QAbstractItemView {
    background-color: #2a2a2a;
    border: 1px solid #444;
    selection-background-color: #00B8FC;
    selection-color: #000;
    padding: 4px;
}

/* ============================================
   Scroll Bars
   ============================================ */
QScrollBar:vertical {
    background-color: #1a1a1a;
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background-color: #444;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00B8FC;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #1a1a1a;
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background-color: #444;
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #00B8FC;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ============================================
   Status Bar
   ============================================ */
QStatusBar {
    background-color: #1a1a1a;
    color: #888;
    border-top: 1px solid #333;
    padding: 4px 8px;
}

QStatusBar::item {
    border: none;
}

/* ============================================
   Line Edit
   ============================================ */
QLineEdit {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 8px 10px;
    color: #e0e0e0;
    selection-background-color: #00B8FC;
    selection-color: #000;
}

QLineEdit:focus {
    border-color: #00B8FC;
}

QLineEdit:disabled {
    background-color: #222;
    color: #555;
}

/* ============================================
   Text Edit / Plain Text Edit
   ============================================ */
QTextEdit, QPlainTextEdit {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 8px;
    color: #e0e0e0;
    selection-background-color: #00B8FC;
    selection-color: #000;
    font-family: 'Consolas', 'Ubuntu Mono', 'DejaVu Sans Mono', monospace;
}

QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #00B8FC;
}

/* ============================================
   Slider
   ============================================ */
QSlider::groove:horizontal {
    height: 6px;
    background-color: #333;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #00B8FC;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background-color: #33c9ff;
}

QSlider::sub-page:horizontal {
    background-color: #00B8FC;
    border-radius: 3px;
}

/* ============================================
   Check Box
   ============================================ */
QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 2px solid #444;
    background-color: #2a2a2a;
}

QCheckBox::indicator:hover {
    border-color: #00B8FC;
}

QCheckBox::indicator:checked {
    background-color: #00B8FC;
    border-color: #00B8FC;
}

/* ============================================
   Radio Button
   ============================================ */
QRadioButton {
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #444;
    background-color: #2a2a2a;
}

QRadioButton::indicator:hover {
    border-color: #00B8FC;
}

QRadioButton::indicator:checked {
    background-color: #00B8FC;
    border-color: #00B8FC;
}

/* ============================================
   Spin Box
   ============================================ */
QSpinBox, QDoubleSpinBox {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e0e0e0;
}

QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #00B8FC;
}

QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    background-color: #333;
    border: none;
    width: 20px;
}

QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: #00B8FC;
}

/* ============================================
   Tool Tips
   ============================================ */
QToolTip {
    background-color: #333;
    color: #e0e0e0;
    border: 1px solid #00B8FC;
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 11px;
}

/* ============================================
   Frame Styles
   ============================================ */
QFrame[frameShape="4"] { /* StyledPanel */
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 6px;
}

/* ============================================
   Menu
   ============================================ */
QMenuBar {
    background-color: #1a1a1a;
    border-bottom: 1px solid #333;
}

QMenuBar::item {
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background-color: #333;
}

QMenu {
    background-color: #2a2a2a;
    border: 1px solid #444;
    padding: 4px;
}

QMenu::item {
    padding: 8px 24px;
    border-radius: 3px;
}

QMenu::item:selected {
    background-color: #00B8FC;
    color: #000;
}

QMenu::separator {
    height: 1px;
    background-color: #444;
    margin: 4px 8px;
}

/* ============================================
   Dialog
   ============================================ */
QDialog {
    background-color: #1e1e1e;
}

QDialogButtonBox {
    button-layout: 2; /* WinLayout */
}

/* ============================================
   Progress Bar
   ============================================ */
QProgressBar {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    text-align: center;
    color: #e0e0e0;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #00B8FC;
    border-radius: 3px;
}

/* ============================================
   Label Styles
   ============================================ */
QLabel#headerLabel {
    font-size: 14px;
    font-weight: bold;
    color: #00B8FC;
    padding: 8px 0;
}

QLabel#subHeaderLabel {
    font-size: 12px;
    font-weight: bold;
    color: #e0e0e0;
}

QLabel#mutedLabel {
    color: #888;
    font-style: italic;
}

/* ============================================
   Splitter
   ============================================ */
QSplitter::handle {
    background-color: #333;
}

QSplitter::handle:hover {
    background-color: #00B8FC;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* ============================================
   Table Widget
   ============================================ */
QTableWidget {
    background-color: #1e1e1e;
    border: 1px solid #333;
    border-radius: 4px;
    gridline-color: #333;
}

QTableWidget::item {
    padding: 6px;
}

QTableWidget::item:selected {
    background-color: #00B8FC;
    color: #000;
}

QTableWidget::item:hover:!selected {
    background-color: #2a2a2a;
}
"""

# Button styles for G13 key buttons
KEY_BUTTON_NORMAL = """
QPushButton {
    background-color: #2a2a2a;
    border: 1px solid #444;
    border-radius: 4px;
    color: #ccc;
    font-size: 9px;
    font-weight: bold;
}
"""

KEY_BUTTON_HOVER = """
QPushButton {
    background-color: #3a3a3a;
    border: 2px solid #00B8FC;
    border-radius: 4px;
    color: #fff;
    font-size: 9px;
    font-weight: bold;
}
"""

KEY_BUTTON_ACTIVE = """
QPushButton {
    background-color: #00B8FC;
    border: 2px solid #00B8FC;
    border-radius: 4px;
    color: #000;
    font-size: 9px;
    font-weight: bold;
}
"""

KEY_BUTTON_BOUND = """
QPushButton {
    background-color: #2a3a2a;
    border: 1px solid #4a6a4a;
    border-radius: 4px;
    color: #8c8;
    font-size: 9px;
    font-weight: bold;
}
"""
