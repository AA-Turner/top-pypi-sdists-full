"""
Main Window

Primary application window for G13LogitechOPS GUI.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSplitter,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .app_profiles import AppProfilesWidget
from .button_mapper import ButtonMapperWidget
from .hardware_control import HardwareControlWidget
from .joystick_settings import JoystickSettingsWidget
from .live_monitor import LiveMonitorWidget
from .macro_editor import MacroEditorWidget
from .profile_manager import ProfileManagerWidget


class DeviceStatusBanner(QFrame):
    """Banner showing device connection status."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("deviceStatusBanner")
        self._is_connected = False

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 6, 10, 6)

        self.icon_label = QLabel("⚠")
        self.icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.icon_label)

        self.text_label = QLabel("G13 device not connected")
        self.text_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.text_label)

        layout.addStretch()

        self.hint_label = QLabel("Connect your G13 or run with sudo for button input")
        self.hint_label.setStyleSheet("font-size: 11px; color: #aaa;")
        layout.addWidget(self.hint_label)

        self.setLayout(layout)
        self._update_style()

    def set_connected(self, connected: bool, message: str = ""):
        """Update connection status."""
        self._is_connected = connected
        if connected:
            self.icon_label.setText("✓")
            self.text_label.setText(message or "G13 device connected")
            self.hint_label.setText("")
        else:
            self.icon_label.setText("⚠")
            self.text_label.setText(message or "G13 device not connected")
            self.hint_label.setText("Connect your G13 or run with sudo for button input")
        self._update_style()

    def _update_style(self):
        """Update banner style based on connection state."""
        if self._is_connected:
            self.setStyleSheet("""
                #deviceStatusBanner {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1a3a1a, stop:1 #0d2a0d);
                    border: 1px solid #2a5a2a;
                    border-radius: 4px;
                }
                #deviceStatusBanner QLabel {
                    color: #88ff88;
                }
            """)
        else:
            self.setStyleSheet("""
                #deviceStatusBanner {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3a2a1a, stop:1 #2a1a0d);
                    border: 1px solid #5a3a2a;
                    border-radius: 4px;
                }
                #deviceStatusBanner QLabel {
                    color: #ffaa55;
                }
            """)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("G13LogitechOPS - Configuration Tool")
        self.setMinimumSize(1200, 700)

        # Create widgets
        self.device_banner = DeviceStatusBanner()
        self.button_mapper = ButtonMapperWidget()
        self.profile_widget = ProfileManagerWidget()
        self.monitor_widget = LiveMonitorWidget()
        self.hardware_widget = HardwareControlWidget()
        self.macro_widget = MacroEditorWidget()
        self.joystick_widget = JoystickSettingsWidget()
        self.app_profiles_widget: AppProfilesWidget | None = None  # Set by controller
        self._tabs: QTabWidget | None = None

        self._init_ui()

    def _init_ui(self):
        """Setup UI layout"""

        # Central widget with vertical layout
        central = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(6)

        # Device status banner at top
        main_layout.addWidget(self.device_banner)

        # Main splitter (left/right)
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left side: Button mapper
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.button_mapper)
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        # Right side: Tabs
        self._tabs = QTabWidget()
        self._tabs.addTab(self.profile_widget, "Profiles")
        self._tabs.addTab(self.joystick_widget, "Joystick")
        self._tabs.addTab(self.macro_widget, "Macros")
        self._tabs.addTab(self.hardware_widget, "Hardware")
        self._tabs.addTab(self.monitor_widget, "Monitor")

        splitter.addWidget(self._tabs)
        splitter.setSizes([800, 400])

        main_layout.addWidget(splitter, 1)  # Stretch factor 1

        central.setLayout(main_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - No device connected")

        self.setCentralWidget(central)

    def set_status(self, message: str):
        """Update status bar message"""
        self.status_bar.showMessage(message)

    def set_device_connected(self, connected: bool, message: str = ""):
        """Update device connection status banner."""
        self.device_banner.set_connected(connected, message)

    def setup_app_profiles(self, rules_manager, profiles: list[str]):
        """Set up the app profiles widget with the rules manager.

        Called by ApplicationController after initialization.
        """

        self.app_profiles_widget = AppProfilesWidget(rules_manager, profiles)
        if self._tabs:
            # Insert after Profiles tab
            self._tabs.insertTab(1, self.app_profiles_widget, "App Profiles")
