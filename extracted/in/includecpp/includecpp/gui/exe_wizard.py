"""
IncludeCPP EXE Builder Wizard
Modern PyQt6 wizard for building executables with PyInstaller.
Black/white frameless professional design.
"""

import sys
import os
import json
import threading
from pathlib import Path
from typing import Optional, Dict, Any

try:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QLineEdit, QCheckBox, QRadioButton, QButtonGroup,
        QFileDialog, QProgressBar, QStackedWidget, QFrame, QListWidget,
        QListWidgetItem, QTextEdit, QComboBox, QScrollArea, QSizePolicy,
        QSpacerItem, QGroupBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QPoint, QTimer
    from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter, QCursor
    PYQT6_AVAILABLE = True
except ImportError:
    PYQT6_AVAILABLE = False


# ============================================================================
# STYLE CONSTANTS
# ============================================================================

DARK_BG = "#0a0a0a"
DARK_SURFACE = "#141414"
DARK_CARD = "#1a1a1a"
DARK_BORDER = "#2a2a2a"
ACCENT_COLOR = "#ffffff"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#888888"
TEXT_MUTED = "#555555"
SUCCESS_COLOR = "#4ade80"
ERROR_COLOR = "#f87171"
WARNING_COLOR = "#fbbf24"

STYLESHEET = f"""
QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
}}

QFrame#card {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 12px;
    padding: 16px;
}}

QFrame#titleBar {{
    background-color: {DARK_SURFACE};
    border: none;
    border-bottom: 1px solid {DARK_BORDER};
}}

QLabel {{
    background: transparent;
    border: none;
}}

QLabel#title {{
    font-size: 24px;
    font-weight: bold;
    color: {TEXT_PRIMARY};
}}

QLabel#subtitle {{
    font-size: 14px;
    color: {TEXT_SECONDARY};
}}

QLabel#stepIndicator {{
    font-size: 12px;
    color: {TEXT_MUTED};
    font-weight: 500;
}}

QLabel#sectionTitle {{
    font-size: 16px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    padding-bottom: 8px;
}}

QPushButton {{
    background-color: {DARK_CARD};
    color: {TEXT_PRIMARY};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 500;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {DARK_SURFACE};
    border-color: {TEXT_SECONDARY};
}}

QPushButton:pressed {{
    background-color: {DARK_BORDER};
}}

QPushButton#primary {{
    background-color: {ACCENT_COLOR};
    color: {DARK_BG};
    border: none;
    font-weight: 600;
}}

QPushButton#primary:hover {{
    background-color: #e0e0e0;
}}

QPushButton#primary:disabled {{
    background-color: {DARK_BORDER};
    color: {TEXT_MUTED};
}}

QPushButton#danger {{
    background-color: transparent;
    color: {ERROR_COLOR};
    border: 1px solid {ERROR_COLOR};
}}

QPushButton#danger:hover {{
    background-color: {ERROR_COLOR};
    color: {DARK_BG};
}}

QPushButton#buildMode {{
    background-color: {DARK_CARD};
    border: 2px solid {DARK_BORDER};
    border-radius: 12px;
    padding: 20px;
    text-align: left;
    min-height: 80px;
}}

QPushButton#buildMode:hover {{
    border-color: {TEXT_SECONDARY};
}}

QPushButton#buildMode:checked {{
    border-color: {ACCENT_COLOR};
    background-color: {DARK_SURFACE};
}}

QLineEdit {{
    background-color: {DARK_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    padding: 10px 14px;
    selection-background-color: {ACCENT_COLOR};
    selection-color: {DARK_BG};
}}

QLineEdit:focus {{
    border-color: {ACCENT_COLOR};
}}

QLineEdit:disabled {{
    background-color: {DARK_CARD};
    color: {TEXT_MUTED};
}}

QTextEdit {{
    background-color: {DARK_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    padding: 10px;
}}

QTextEdit:focus {{
    border-color: {ACCENT_COLOR};
}}

QCheckBox {{
    spacing: 10px;
    color: {TEXT_PRIMARY};
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 2px solid {DARK_BORDER};
    background-color: {DARK_SURFACE};
}}

QCheckBox::indicator:hover {{
    border-color: {TEXT_SECONDARY};
}}

QCheckBox::indicator:checked {{
    background-color: {ACCENT_COLOR};
    border-color: {ACCENT_COLOR};
}}

QRadioButton {{
    spacing: 10px;
    color: {TEXT_PRIMARY};
}}

QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 2px solid {DARK_BORDER};
    background-color: {DARK_SURFACE};
}}

QRadioButton::indicator:hover {{
    border-color: {TEXT_SECONDARY};
}}

QRadioButton::indicator:checked {{
    background-color: {ACCENT_COLOR};
    border-color: {ACCENT_COLOR};
}}

QProgressBar {{
    background-color: {DARK_SURFACE};
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {ACCENT_COLOR};
    border-radius: 6px;
}}

QListWidget {{
    background-color: {DARK_SURFACE};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    padding: 8px;
    outline: none;
}}

QListWidget::item {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    padding: 8px 12px;
    border-radius: 6px;
    margin: 2px 0;
}}

QListWidget::item:hover {{
    background-color: {DARK_CARD};
}}

QListWidget::item:selected {{
    background-color: {DARK_BORDER};
    color: {TEXT_PRIMARY};
}}

QComboBox {{
    background-color: {DARK_SURFACE};
    color: {TEXT_PRIMARY};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    padding: 10px 14px;
    min-width: 150px;
}}

QComboBox:hover {{
    border-color: {TEXT_SECONDARY};
}}

QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {TEXT_SECONDARY};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {DARK_SURFACE};
    border: 1px solid {DARK_BORDER};
    border-radius: 8px;
    selection-background-color: {DARK_CARD};
    outline: none;
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background-color: {DARK_SURFACE};
    width: 8px;
    border-radius: 4px;
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

QGroupBox {{
    background-color: {DARK_CARD};
    border: 1px solid {DARK_BORDER};
    border-radius: 10px;
    margin-top: 16px;
    padding: 16px;
    padding-top: 24px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 0 8px;
    color: {TEXT_SECONDARY};
}}
"""


# ============================================================================
# BUILD THREAD
# ============================================================================

class BuildThread(QThread):
    """Background thread for building executable."""
    progress = pyqtSignal(int, str)  # progress percentage, status message
    finished_signal = pyqtSignal(bool, str)  # success, result message
    log = pyqtSignal(str)  # log message

    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        try:
            self.progress.emit(5, "Preparing build environment...")
            self.log.emit("Starting build process...")

            script_path = self.config.get('script_path', '')
            if not script_path or not os.path.exists(script_path):
                self.finished_signal.emit(False, f"Script not found: {script_path}")
                return

            # Build PyInstaller command
            self.progress.emit(10, "Configuring PyInstaller...")

            import subprocess

            # Use sys.executable -m PyInstaller to ensure we find it
            cmd = [sys.executable, '-m', 'PyInstaller']

            # Output name
            output_name = self.config.get('output_name', '')
            if output_name:
                cmd.extend(['--name', output_name])

            # One file or directory
            if self.config.get('onefile', True):
                cmd.append('--onefile')
            else:
                cmd.append('--onedir')

            # Console or windowed
            if self.config.get('windowed', False):
                cmd.append('--windowed')
            else:
                cmd.append('--console')

            # Icon
            icon_path = self.config.get('icon', '')
            if icon_path and os.path.exists(icon_path):
                cmd.extend(['--icon', icon_path])

            # Output directory
            output_dir = self.config.get('output_dir', '')
            if output_dir:
                cmd.extend(['--distpath', output_dir])

            # Additional data files
            data_files = self.config.get('data_files', [])
            for data_file in data_files:
                if os.path.exists(data_file):
                    # Preserve directory structure: use folder name as destination
                    if os.path.isdir(data_file):
                        dest = os.path.basename(data_file.rstrip('/\\'))
                        cmd.extend(['--add-data', f'{data_file};{dest}'])
                    else:
                        # For files, put in root
                        cmd.extend(['--add-data', f'{data_file};.'])

            # Additional DLLs
            dlls = self.config.get('dlls', [])
            for dll in dlls:
                if os.path.exists(dll):
                    cmd.extend(['--add-binary', f'{dll};.'])

            # Hidden imports
            hidden_imports = self.config.get('hidden_imports', [])
            for imp in hidden_imports:
                cmd.extend(['--hidden-import', imp])

            # Clean build
            if self.config.get('clean', True):
                cmd.append('--clean')

            # No confirm
            cmd.append('--noconfirm')

            # Add script path
            cmd.append(script_path)

            self.log.emit(f"Command: {' '.join(cmd)}")
            self.progress.emit(20, "Starting PyInstaller...")

            if self._cancelled:
                self.finished_signal.emit(False, "Build cancelled")
                return

            # Run PyInstaller
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(script_path) or '.',
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )

            # Read output
            progress_val = 20
            while True:
                if self._cancelled:
                    process.kill()
                    self.finished_signal.emit(False, "Build cancelled")
                    return

                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break

                if line:
                    line = line.strip()
                    self.log.emit(line)

                    # Update progress based on output
                    if 'Analyzing' in line:
                        progress_val = min(progress_val + 2, 50)
                        self.progress.emit(progress_val, "Analyzing dependencies...")
                    elif 'Processing' in line:
                        progress_val = min(progress_val + 1, 70)
                        self.progress.emit(progress_val, "Processing modules...")
                    elif 'Building' in line:
                        progress_val = min(progress_val + 5, 85)
                        self.progress.emit(progress_val, "Building executable...")
                    elif 'Copying' in line:
                        progress_val = min(progress_val + 2, 95)
                        self.progress.emit(progress_val, "Copying files...")

            # Check result
            if process.returncode == 0:
                self.progress.emit(100, "Build complete!")

                # Find output file
                if output_dir:
                    exe_dir = output_dir
                else:
                    exe_dir = os.path.join(os.path.dirname(script_path), 'dist')

                exe_name = output_name or Path(script_path).stem
                if sys.platform == 'win32':
                    exe_name += '.exe'

                exe_path = os.path.join(exe_dir, exe_name)
                if os.path.exists(exe_path):
                    self.finished_signal.emit(True, exe_path)
                else:
                    self.finished_signal.emit(True, f"Build complete. Check: {exe_dir}")
            else:
                self.finished_signal.emit(False, f"Build failed with code {process.returncode}")

        except Exception as e:
            self.finished_signal.emit(False, f"Build error: {str(e)}")


# ============================================================================
# WIZARD PAGES
# ============================================================================

class WizardPage(QWidget):
    """Base class for wizard pages."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Override in subclasses."""
        pass

    def validate(self) -> bool:
        """Validate page data. Override in subclasses."""
        return True

    def get_data(self) -> Dict[str, Any]:
        """Get page data. Override in subclasses."""
        return {}


class Step1BuildMode(WizardPage):
    """Step 1: Choose build mode (Automatic/Manual) and select script."""

    def __init__(self, parent=None, script_path: str = None):
        self.auto_mode = True
        self.script_path = script_path or ""
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("Build Configuration")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Select your script and build mode")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(12)

        # Script selection (always visible)
        script_group = QGroupBox("Script File")
        script_layout = QVBoxLayout(script_group)
        script_layout.setSpacing(8)

        script_row = QHBoxLayout()
        self.script_input = QLineEdit()
        self.script_input.setPlaceholderText("Select a Python script to build...")
        self.script_input.setText(self.script_path)
        self.script_btn = QPushButton("Browse...")
        self.script_btn.setFixedWidth(100)
        self.script_btn.clicked.connect(self._browse_script)
        script_row.addWidget(self.script_input)
        script_row.addWidget(self.script_btn)
        script_layout.addLayout(script_row)

        layout.addWidget(script_group)

        layout.addSpacing(8)

        # Build mode buttons
        modes_layout = QHBoxLayout()
        modes_layout.setSpacing(16)

        # Automatic mode
        self.auto_btn = QPushButton()
        self.auto_btn.setObjectName("buildMode")
        self.auto_btn.setCheckable(True)
        self.auto_btn.setChecked(True)
        self.auto_btn.setMinimumHeight(100)
        auto_layout = QVBoxLayout(self.auto_btn)
        auto_layout.setContentsMargins(16, 12, 16, 12)

        auto_title = QLabel("Automatic")
        auto_title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        auto_layout.addWidget(auto_title)

        auto_desc = QLabel("Quick build with smart defaults")
        auto_desc.setStyleSheet(f"font-size: 12px; color: {TEXT_SECONDARY}; background: transparent;")
        auto_desc.setWordWrap(True)
        auto_layout.addWidget(auto_desc)
        auto_layout.addStretch()

        modes_layout.addWidget(self.auto_btn)

        # Manual mode
        self.manual_btn = QPushButton()
        self.manual_btn.setObjectName("buildMode")
        self.manual_btn.setCheckable(True)
        self.manual_btn.setMinimumHeight(100)
        manual_layout = QVBoxLayout(self.manual_btn)
        manual_layout.setContentsMargins(16, 12, 16, 12)

        manual_title = QLabel("Manual")
        manual_title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {TEXT_PRIMARY}; background: transparent;")
        manual_layout.addWidget(manual_title)

        manual_desc = QLabel("Full control over settings")
        manual_desc.setStyleSheet(f"font-size: 12px; color: {TEXT_SECONDARY}; background: transparent;")
        manual_desc.setWordWrap(True)
        manual_layout.addWidget(manual_desc)
        manual_layout.addStretch()

        modes_layout.addWidget(self.manual_btn)

        # Button group
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.auto_btn, 0)
        self.mode_group.addButton(self.manual_btn, 1)
        self.mode_group.buttonClicked.connect(self._on_mode_changed)

        layout.addLayout(modes_layout)

        layout.addSpacing(12)

        # Quick settings (visible in both modes)
        quick_group = QGroupBox("Quick Settings")
        quick_layout = QVBoxLayout(quick_group)
        quick_layout.setSpacing(12)

        # Window mode
        window_layout = QHBoxLayout()
        window_layout.setSpacing(20)

        self.console_radio = QRadioButton("Console Application")
        self.console_radio.setChecked(True)
        self.windowed_radio = QRadioButton("Windowed (No Console)")

        window_group = QButtonGroup(self)
        window_group.addButton(self.console_radio)
        window_group.addButton(self.windowed_radio)

        window_layout.addWidget(self.console_radio)
        window_layout.addWidget(self.windowed_radio)
        window_layout.addStretch()

        quick_layout.addLayout(window_layout)

        layout.addWidget(quick_group)
        layout.addStretch()

    def _browse_script(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Python Script", "",
            "Python Files (*.py);;CSSL Files (*.cssl);;All Files (*)"
        )
        if path:
            self.script_input.setText(path)
            self.script_path = path

    def _on_mode_changed(self, btn):
        self.auto_mode = (btn == self.auto_btn)

    def validate(self) -> bool:
        """Check that a script is selected."""
        script = self.script_input.text().strip()
        return bool(script) and os.path.exists(script)

    def get_data(self) -> Dict[str, Any]:
        return {
            'auto_mode': self.auto_mode,
            'windowed': self.windowed_radio.isChecked(),
            'script_path': self.script_input.text().strip()
        }


class Step2Configuration(WizardPage):
    """Step 2: Detailed configuration."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("Build Configuration")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Configure your executable settings")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 8, 0)

        # Basic Settings
        basic_group = QGroupBox("Basic Settings")
        basic_layout = QVBoxLayout(basic_group)
        basic_layout.setSpacing(12)

        # Output name
        name_layout = QHBoxLayout()
        name_label = QLabel("Output Name:")
        name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("MyApplication (without .exe)")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        basic_layout.addLayout(name_layout)

        # Output directory
        dir_layout = QHBoxLayout()
        dir_label = QLabel("Output Directory:")
        dir_label.setFixedWidth(120)
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Same as script directory")
        self.dir_btn = QPushButton("Browse...")
        self.dir_btn.setFixedWidth(100)
        self.dir_btn.clicked.connect(self._browse_output_dir)
        dir_layout.addWidget(dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.dir_btn)
        basic_layout.addLayout(dir_layout)

        # Icon
        icon_layout = QHBoxLayout()
        icon_label = QLabel("Icon (.ico):")
        icon_label.setFixedWidth(120)
        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText("Optional: path to .ico file")
        self.icon_btn = QPushButton("Browse...")
        self.icon_btn.setFixedWidth(100)
        self.icon_btn.clicked.connect(self._browse_icon)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(self.icon_btn)
        basic_layout.addLayout(icon_layout)

        scroll_layout.addWidget(basic_group)

        # Build Options
        options_group = QGroupBox("Build Options")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(12)

        # One file vs directory
        self.onefile_check = QCheckBox("Single File (--onefile)")
        self.onefile_check.setChecked(True)
        options_layout.addWidget(self.onefile_check)

        # Clean build
        self.clean_check = QCheckBox("Clean Build (remove previous build files)")
        self.clean_check.setChecked(True)
        options_layout.addWidget(self.clean_check)

        scroll_layout.addWidget(options_group)

        # Data Files
        data_group = QGroupBox("Additional Data Files")
        data_layout = QVBoxLayout(data_group)
        data_layout.setSpacing(8)

        data_desc = QLabel("Add files/folders to include with the executable (config files, assets, etc.)")
        data_desc.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
        data_desc.setWordWrap(True)
        data_layout.addWidget(data_desc)

        self.data_list = QListWidget()
        self.data_list.setMaximumHeight(120)
        data_layout.addWidget(self.data_list)

        data_btn_layout = QHBoxLayout()
        self.add_file_btn = QPushButton("Add File")
        self.add_file_btn.clicked.connect(self._add_data_file)
        self.add_folder_btn = QPushButton("Add Folder")
        self.add_folder_btn.clicked.connect(self._add_data_folder)
        self.remove_data_btn = QPushButton("Remove")
        self.remove_data_btn.setObjectName("danger")
        self.remove_data_btn.clicked.connect(self._remove_data)
        data_btn_layout.addWidget(self.add_file_btn)
        data_btn_layout.addWidget(self.add_folder_btn)
        data_btn_layout.addWidget(self.remove_data_btn)
        data_btn_layout.addStretch()
        data_layout.addLayout(data_btn_layout)

        scroll_layout.addWidget(data_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _browse_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if path:
            self.dir_input.setText(path)

    def _browse_icon(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon", "", "Icon Files (*.ico);;All Files (*)"
        )
        if path:
            self.icon_input.setText(path)

    def _add_data_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Add Data File")
        if path:
            self.data_list.addItem(path)

    def _add_data_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Add Data Folder")
        if path:
            self.data_list.addItem(path)

    def _remove_data(self):
        current = self.data_list.currentRow()
        if current >= 0:
            self.data_list.takeItem(current)

    def get_data(self) -> Dict[str, Any]:
        data_files = []
        for i in range(self.data_list.count()):
            data_files.append(self.data_list.item(i).text())

        return {
            'output_name': self.name_input.text().strip(),
            'output_dir': self.dir_input.text().strip(),
            'icon': self.icon_input.text().strip(),
            'onefile': self.onefile_check.isChecked(),
            'clean': self.clean_check.isChecked(),
            'data_files': data_files
        }


class Step3Advanced(WizardPage):
    """Step 3: Advanced settings (DLLs, hidden imports)."""

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("Advanced Settings")
        title.setObjectName("title")
        layout.addWidget(title)

        subtitle = QLabel("Configure DLLs, imports, and project-specific options")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 8, 0)

        # DLLs
        dll_group = QGroupBox("DLLs / Binary Files")
        dll_layout = QVBoxLayout(dll_group)
        dll_layout.setSpacing(8)

        dll_desc = QLabel("Add DLL files from --make-dll or other binary dependencies")
        dll_desc.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
        dll_desc.setWordWrap(True)
        dll_layout.addWidget(dll_desc)

        self.dll_list = QListWidget()
        self.dll_list.setMaximumHeight(120)
        dll_layout.addWidget(self.dll_list)

        dll_btn_layout = QHBoxLayout()
        self.add_dll_btn = QPushButton("Add DLL")
        self.add_dll_btn.clicked.connect(self._add_dll)
        self.scan_dll_btn = QPushButton("Scan Project")
        self.scan_dll_btn.clicked.connect(self._scan_dlls)
        self.remove_dll_btn = QPushButton("Remove")
        self.remove_dll_btn.setObjectName("danger")
        self.remove_dll_btn.clicked.connect(self._remove_dll)
        dll_btn_layout.addWidget(self.add_dll_btn)
        dll_btn_layout.addWidget(self.scan_dll_btn)
        dll_btn_layout.addWidget(self.remove_dll_btn)
        dll_btn_layout.addStretch()
        dll_layout.addLayout(dll_btn_layout)

        scroll_layout.addWidget(dll_group)

        # Hidden imports
        import_group = QGroupBox("Hidden Imports")
        import_layout = QVBoxLayout(import_group)
        import_layout.setSpacing(8)

        import_desc = QLabel("Add Python modules that PyInstaller might miss (one per line)")
        import_desc.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
        import_desc.setWordWrap(True)
        import_layout.addWidget(import_desc)

        self.import_edit = QTextEdit()
        self.import_edit.setPlaceholderText("numpy\npandas\nrequests")
        self.import_edit.setMaximumHeight(100)
        import_layout.addWidget(self.import_edit)

        scroll_layout.addWidget(import_group)

        # Project-bound paths
        paths_group = QGroupBox("Project-Bound Paths")
        paths_layout = QVBoxLayout(paths_group)
        paths_layout.setSpacing(12)

        paths_desc = QLabel("Configure paths that should be relative to the executable")
        paths_desc.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")
        paths_desc.setWordWrap(True)
        paths_layout.addWidget(paths_desc)

        # Save path
        save_layout = QHBoxLayout()
        save_label = QLabel("Save Directory:")
        save_label.setFixedWidth(120)
        self.save_path_input = QLineEdit()
        self.save_path_input.setPlaceholderText("save/")
        save_layout.addWidget(save_label)
        save_layout.addWidget(self.save_path_input)
        paths_layout.addLayout(save_layout)

        # Config path
        config_layout = QHBoxLayout()
        config_label = QLabel("Config Directory:")
        config_label.setFixedWidth(120)
        self.config_path_input = QLineEdit()
        self.config_path_input.setPlaceholderText("config/")
        config_layout.addWidget(config_label)
        config_layout.addWidget(self.config_path_input)
        paths_layout.addLayout(config_layout)

        scroll_layout.addWidget(paths_group)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def _add_dll(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Add DLL", "", "DLL Files (*.dll *.pyd);;All Files (*)"
        )
        if path:
            self.dll_list.addItem(path)

    def _scan_dlls(self):
        """Scan project for DLL files."""
        path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if path:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f.endswith(('.dll', '.pyd')):
                        full_path = os.path.join(root, f)
                        # Check if already in list
                        exists = False
                        for i in range(self.dll_list.count()):
                            if self.dll_list.item(i).text() == full_path:
                                exists = True
                                break
                        if not exists:
                            self.dll_list.addItem(full_path)

    def _remove_dll(self):
        current = self.dll_list.currentRow()
        if current >= 0:
            self.dll_list.takeItem(current)

    def get_data(self) -> Dict[str, Any]:
        dlls = []
        for i in range(self.dll_list.count()):
            dlls.append(self.dll_list.item(i).text())

        imports_text = self.import_edit.toPlainText().strip()
        hidden_imports = [line.strip() for line in imports_text.split('\n') if line.strip()]

        return {
            'dlls': dlls,
            'hidden_imports': hidden_imports,
            'save_path': self.save_path_input.text().strip(),
            'config_path': self.config_path_input.text().strip()
        }


class StepBuild(WizardPage):
    """Build step with progress."""

    def __init__(self, parent=None):
        self.build_thread = None
        super().__init__(parent)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        self.title = QLabel("Building Executable")
        self.title.setObjectName("title")
        layout.addWidget(self.title)

        self.subtitle = QLabel("Please wait while your executable is being built...")
        self.subtitle.setObjectName("subtitle")
        layout.addWidget(self.subtitle)

        layout.addSpacing(20)

        # Progress
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

        # Status
        self.status_label = QLabel("Initializing...")
        self.status_label.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(self.status_label)

        layout.addSpacing(20)

        # Log output
        log_label = QLabel("Build Log:")
        log_label.setObjectName("sectionTitle")
        layout.addWidget(log_label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet(f"""
            QTextEdit {{
                background-color: {DARK_SURFACE};
                color: {TEXT_SECONDARY};
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.log_output)

        # Result message
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        layout.addWidget(self.result_label)

    def start_build(self, config: Dict[str, Any]):
        """Start the build process."""
        self.log_output.clear()
        self.progress.setValue(0)
        self.result_label.setText("")
        self.title.setText("Building Executable")
        self.subtitle.setText("Please wait while your executable is being built...")

        self.build_thread = BuildThread(config)
        self.build_thread.progress.connect(self._on_progress)
        self.build_thread.log.connect(self._on_log)
        self.build_thread.finished_signal.connect(self._on_finished)
        self.build_thread.start()

    def _on_progress(self, value: int, status: str):
        self.progress.setValue(value)
        self.status_label.setText(status)

    def _on_log(self, message: str):
        self.log_output.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def _on_finished(self, success: bool, message: str):
        if success:
            self.title.setText("Build Complete!")
            self.subtitle.setText("Your executable has been created successfully.")
            self.result_label.setStyleSheet(f"color: {SUCCESS_COLOR}; font-size: 14px; font-weight: 500;")
            self.result_label.setText(f"Output: {message}")
            self.status_label.setText("Done!")
        else:
            self.title.setText("Build Failed")
            self.subtitle.setText("There was an error during the build process.")
            self.result_label.setStyleSheet(f"color: {ERROR_COLOR}; font-size: 14px; font-weight: 500;")
            self.result_label.setText(f"Error: {message}")
            self.status_label.setText("Failed")

    def cancel_build(self):
        if self.build_thread and self.build_thread.isRunning():
            self.build_thread.cancel()


# ============================================================================
# MAIN WIZARD
# ============================================================================

class ExeBuilderWizard(QWidget):
    """Main wizard window."""

    def __init__(self, script_path: str = None):
        super().__init__()
        self.script_path = script_path
        self.current_step = 0
        self.is_auto_mode = True
        self.is_building = False
        self._drag_pos = None

        self.setup_ui()
        self.setStyleSheet(STYLESHEET)

    def setup_ui(self):
        self.setWindowTitle("IncludeCPP EXE Builder")
        self.resize(700, 600)
        self.setMinimumSize(600, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(50)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 10, 0)

        # App icon and title
        app_title = QLabel("EXE Builder")
        app_title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {TEXT_PRIMARY};")
        title_layout.addWidget(app_title)

        title_layout.addStretch()

        # Step indicator
        self.step_indicator = QLabel("Step 1 of 3")
        self.step_indicator.setObjectName("stepIndicator")
        title_layout.addWidget(self.step_indicator)

        title_layout.addSpacing(20)

        # Window controls
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(36, 36)
        minimize_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {TEXT_SECONDARY};
                font-size: 14px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {DARK_BORDER};
            }}
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_btn)

        close_btn = QPushButton("×")
        close_btn.setFixedSize(36, 36)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {TEXT_SECONDARY};
                font-size: 20px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {ERROR_COLOR};
                color: white;
            }}
        """)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        main_layout.addWidget(title_bar)

        # Content area
        content = QWidget()
        content.setStyleSheet(f"background-color: {DARK_BG};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(0)

        # Pages stack
        self.pages = QStackedWidget()

        self.step1 = Step1BuildMode(script_path=self.script_path)
        self.step2 = Step2Configuration()
        self.step3 = Step3Advanced()
        self.step_build = StepBuild()

        self.pages.addWidget(self.step1)
        self.pages.addWidget(self.step2)
        self.pages.addWidget(self.step3)
        self.pages.addWidget(self.step_build)

        content_layout.addWidget(self.pages)

        main_layout.addWidget(content, 1)  # stretch factor 1 to expand

        # Navigation bar
        nav_bar = QFrame()
        nav_bar.setObjectName("navBar")
        nav_bar.setStyleSheet(f"""
            QFrame#navBar {{
                background-color: {DARK_SURFACE};
                border-top: 1px solid {DARK_BORDER};
            }}
        """)
        nav_bar.setFixedHeight(70)
        nav_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(32, 0, 32, 0)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self._on_cancel)
        nav_layout.addWidget(self.cancel_btn)

        nav_layout.addStretch()

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self._go_back)
        self.back_btn.setVisible(False)
        nav_layout.addWidget(self.back_btn)

        nav_layout.addSpacing(12)

        self.next_btn = QPushButton("Next")
        self.next_btn.setObjectName("primary")
        self.next_btn.clicked.connect(self._go_next)
        nav_layout.addWidget(self.next_btn)

        main_layout.addWidget(nav_bar)

        # Update initial state
        self._update_navigation()

    def _update_navigation(self):
        """Update navigation buttons based on current step."""
        self.is_auto_mode = self.step1.auto_mode if hasattr(self.step1, 'auto_mode') else True

        if self.is_building:
            self.back_btn.setVisible(False)
            self.next_btn.setVisible(False)
            self.cancel_btn.setText("Cancel Build")
            self.step_indicator.setText("Building...")
            return

        # Auto: 1 config step | Manual: 3 config steps (Build step not counted)
        total_steps = 1 if self.is_auto_mode else 3

        if self.current_step == 3:  # Build page
            self.step_indicator.setText("Building...")
        else:
            actual_step = self.current_step + 1
            self.step_indicator.setText(f"Step {actual_step} of {total_steps}")

        # Back button
        self.back_btn.setVisible(self.current_step > 0)

        # Next button text
        if self.is_auto_mode and self.current_step == 0:
            self.next_btn.setText("Build")
        elif not self.is_auto_mode and self.current_step == 2:
            self.next_btn.setText("Build")
        elif self.current_step == 3:  # Build page
            self.next_btn.setText("Close")
        else:
            self.next_btn.setText("Next")

        self.cancel_btn.setText("Cancel")

    def _go_next(self):
        """Go to next step or start build."""
        if self.current_step == 3:  # Build complete
            self.close()
            return

        # Read auto_mode directly from step1 to get current selection
        is_auto = self.step1.auto_mode if hasattr(self.step1, 'auto_mode') else True
        self.is_auto_mode = is_auto  # Update cached value

        if is_auto and self.current_step == 0:
            # Auto mode: go directly to build
            self._start_build()
        elif not is_auto and self.current_step == 2:
            # Manual mode: after step 3, start build
            self._start_build()
        else:
            # Go to next step
            self.current_step += 1
            self.pages.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _go_back(self):
        """Go to previous step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.pages.setCurrentIndex(self.current_step)
            self._update_navigation()

    def _on_cancel(self):
        """Cancel button clicked."""
        if self.is_building:
            self.step_build.cancel_build()
            self.is_building = False
            self._update_navigation()
        else:
            self.close()

    def _start_build(self):
        """Collect all data and start build."""
        # Step 1 data (includes script path)
        step1_data = self.step1.get_data()

        # Validate script is selected
        script_path = step1_data.get('script_path', '')
        if not script_path or not os.path.exists(script_path):
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(
                self, "No Script Selected",
                "Please select a Python script to build.",
                QMessageBox.StandardButton.Ok
            )
            return

        # Collect configuration
        config = {
            'script_path': script_path,
            'windowed': step1_data.get('windowed', False)
        }

        if not self.is_auto_mode:
            # Step 2 data
            step2_data = self.step2.get_data()
            config.update(step2_data)

            # Step 3 data
            step3_data = self.step3.get_data()
            config.update(step3_data)
        else:
            # Auto mode defaults
            config['onefile'] = True
            config['clean'] = True

        # Go to build page
        self.current_step = 3
        self.pages.setCurrentIndex(3)
        self.is_building = True
        self._update_navigation()

        # Start build
        self.step_build.start_build(config)

        # Connect finished signal
        if self.step_build.build_thread:
            self.step_build.build_thread.finished_signal.connect(self._on_build_finished)

    def _on_build_finished(self, success: bool, message: str):
        """Build finished callback."""
        self.is_building = False
        self.next_btn.setVisible(True)
        self.next_btn.setText("Close")
        self.cancel_btn.setVisible(False)
        self.step_indicator.setText("Complete" if success else "Failed")

    # Frameless window drag support
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None


# ============================================================================
# ENTRY POINT
# ============================================================================

def run_wizard(script_path: str = None) -> bool:
    """
    Run the EXE Builder wizard.

    Args:
        script_path: Path to the Python script to build

    Returns:
        True if build succeeded, False otherwise
    """
    if not PYQT6_AVAILABLE:
        print("PyQt6 is required for the wizard. Install with: pip install PyQt6")
        return False

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    wizard = ExeBuilderWizard(script_path)
    wizard.show()

    # Center on screen
    screen = app.primaryScreen().geometry()
    wizard.move(
        (screen.width() - wizard.width()) // 2,
        (screen.height() - wizard.height()) // 2
    )

    return app.exec() == 0


def main():
    """Main entry point for testing."""
    script = sys.argv[1] if len(sys.argv) > 1 else None
    run_wizard(script)


if __name__ == '__main__':
    main()
