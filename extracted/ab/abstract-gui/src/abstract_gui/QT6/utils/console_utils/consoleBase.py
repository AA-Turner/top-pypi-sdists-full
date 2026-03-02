from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

class SharedStateBus(QObject):
    stateBroadcast = pyqtSignal(object, dict)  # (sender, state)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._snap: dict = {}

    def snapshot(self) -> dict:
        return dict(self._snap)

    def push(self, sender, state: dict):
        self._snap = dict(state)
        self.stateBroadcast.emit(sender, self.snapshot())
class ConsoleBase(QWidget):
    def __init__(self, *, bus=None, parent=None):
        super().__init__(parent)
        self.bus = bus or SharedStateBus(self)
        self.setLayout(QVBoxLayout())
