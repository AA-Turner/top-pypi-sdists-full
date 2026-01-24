import sys
import json
from pathlib import Path

try:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QLineEdit, QCheckBox, QComboBox, QFrame,
        QScrollArea
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


def is_experimental_enabled() -> bool:
    """Check if experimental features are enabled globally."""
    config_path = Path.home() / '.includecpp' / '.secret'
    if config_path.exists():
        try:
            config = json.loads(config_path.read_text(encoding='utf-8'))
            return config.get('experimental_features', False)
        except Exception:
            pass
    return False


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.config_path = Path.home() / '.includecpp' / '.secret'
        self.config = self._load_config()
        self._setup_ui()
        self._load_values()

    def _load_config(self):
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text(encoding='utf-8'))
            except Exception:
                pass
        return {}

    def _save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self.config, indent=2), encoding='utf-8')

    def _setup_ui(self):
        self.setWindowTitle('IncludeCPP Settings')
        self.setFixedSize(360, 580)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main container with background
        main = QWidget(self)
        main.setGeometry(0, 0, 360, 580)

        base_style = '''
            QWidget {
                background-color: #1a1a1a;
                border-radius: 12px;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                background-color: transparent;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 8px 10px;
                color: #e0e0e0;
                font-size: 12px;
                min-height: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 8px 16px;
                color: #e0e0e0;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #4a9eff;
            }
            QCheckBox {
                color: #e0e0e0;
                font-size: 12px;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
            }
            QCheckBox::indicator:checked {
                background-color: #4a9eff;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 6px;
                padding: 8px 10px;
                color: #e0e0e0;
                font-size: 12px;
                min-height: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #e0e0e0;
                selection-background-color: #4a9eff;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #4a4a4a;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5a5a5a;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        '''
        main.setStyleSheet(base_style)

        # Main layout for the container
        main_layout = QVBoxLayout(main)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(8)

        # Header (fixed, not scrollable)
        header = QHBoxLayout()
        title = QLabel('IncludeCPP Settings')
        title.setFont(QFont('Segoe UI', 13, QFont.Weight.Bold))
        title.setStyleSheet('color: #4a9eff; background-color: transparent;')
        header.addWidget(title)
        header.addStretch()
        close_btn = QPushButton('×')
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet('font-size: 16px; border-radius: 12px;')
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)
        main_layout.addLayout(header)

        self._add_separator(main_layout)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet('QScrollArea { background-color: transparent; border: none; }')

        # Content widget inside scroll area
        content = QWidget()
        content.setStyleSheet('background-color: transparent;')
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 8, 0)
        content_layout.setSpacing(10)

        # --- Experimental Features Section ---
        exp_label = QLabel('Experimental')
        exp_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        exp_label.setStyleSheet('color: #ff9800; background-color: transparent;')
        content_layout.addWidget(exp_label)

        self.experimental_enabled = QCheckBox('Enable Experimental Features')
        self.experimental_enabled.setToolTip('Enables AI and CPPY commands (may contain bugs)')
        content_layout.addWidget(self.experimental_enabled)

        self._add_separator(content_layout)

        # --- AI Configuration Section ---
        ai_label = QLabel('AI Configuration')
        ai_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        content_layout.addWidget(ai_label)

        self.ai_enabled = QCheckBox('Enable AI Features')
        content_layout.addWidget(self.ai_enabled)

        content_layout.addWidget(QLabel('OpenAI API Key'))
        self.api_key = QLineEdit()
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.setPlaceholderText('sk-...')
        content_layout.addWidget(self.api_key)

        content_layout.addWidget(QLabel('Model'))
        self.model = QComboBox()
        self.model.addItems(['gpt-5', 'gpt-5-nano', 'gpt-4o', 'gpt-4-turbo', 'gpt-3.5-turbo'])
        content_layout.addWidget(self.model)

        self._add_separator(content_layout)

        # --- API Tokens Section ---
        tokens_label = QLabel('API Tokens')
        tokens_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        content_layout.addWidget(tokens_label)

        content_layout.addWidget(QLabel('Brave Search API'))
        self.brave_key = QLineEdit()
        self.brave_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.brave_key.setPlaceholderText('Token for --websearch')
        content_layout.addWidget(self.brave_key)

        self._add_separator(content_layout)

        # --- Usage Limits Section ---
        limits_label = QLabel('Usage Limits')
        limits_label.setFont(QFont('Segoe UI', 10, QFont.Weight.Bold))
        content_layout.addWidget(limits_label)

        content_layout.addWidget(QLabel('Daily Token Limit'))
        self.daily_limit = QLineEdit()
        self.daily_limit.setPlaceholderText('220000')
        content_layout.addWidget(self.daily_limit)

        content_layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Save button (fixed at bottom)
        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Save')
        save_btn.setStyleSheet('background-color: #4a9eff; font-weight: bold;')
        save_btn.clicked.connect(self._save)
        btn_layout.addWidget(save_btn)
        main_layout.addLayout(btn_layout)

        self._drag_pos = None

    def _add_separator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet('background-color: #3d3d3d; max-height: 1px;')
        layout.addWidget(line)

    def _load_values(self):
        # Experimental features
        self.experimental_enabled.setChecked(self.config.get('experimental_features', False))
        # AI settings
        self.ai_enabled.setChecked(self.config.get('enabled', False))
        api = self.config.get('api_key', '')
        if api:
            self.api_key.setText(api)
        model = self.config.get('model', 'gpt-5')
        idx = self.model.findText(model)
        if idx >= 0:
            self.model.setCurrentIndex(idx)
        brave = self.config.get('brave_api_key', '')
        if brave:
            self.brave_key.setText(brave)
        daily_limit = self.config.get('daily_limit', 220000)
        self.daily_limit.setText(str(daily_limit))

    def _save(self):
        # Experimental features
        self.config['experimental_features'] = self.experimental_enabled.isChecked()
        # AI settings
        self.config['enabled'] = self.ai_enabled.isChecked()
        api = self.api_key.text().strip()
        if api:
            self.config['api_key'] = api
        # Only update model if user explicitly changed it (preserve existing if combo unchanged)
        self.config['model'] = self.model.currentText()
        brave = self.brave_key.text().strip()
        if brave:
            self.config['brave_api_key'] = brave
        limit_text = self.daily_limit.text().strip()
        if limit_text.isdigit() and int(limit_text) >= 1000:
            self.config['daily_limit'] = int(limit_text)
        self._save_config()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()


def show_settings():
    if not PYQT_AVAILABLE:
        return False, 'PyQt6 not installed. Run: pip install PyQt6'
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    widget = SettingsWidget()
    widget.show()
    app.exec()
    return True, 'Settings saved'

if __name__ == '__main__':
    success, message = show_settings()
    if not success:
        print(message)