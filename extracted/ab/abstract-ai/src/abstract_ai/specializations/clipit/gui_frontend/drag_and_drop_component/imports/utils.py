# ─── Third-party ──────────────────────────────────────────────────────────────
from .index import QtCore,QtWidgets
from abstract_utilities import get_logFile
logger = get_logFile('clipit_logs')
def log_it(self, message: str):
    """Append a line to the shared log widget, with timestamp."""
    timestamp = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
    logger.info(f"[{timestamp}] {message}")
    self.log_widget.append(f"[{timestamp}] {message}")
    
def _log(self, m: str):
    """Helper to write to both QTextEdit and Python logger."""
    logger.debug(m)
    log_it(self, m)

def _clear_layout(layout: QtWidgets.QLayout):
    """Recursively delete all widgets in a layout (Qt-safe)."""
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().setParent(None)      # detach
            item.widget().deleteLater()        # mark for deletion
        elif item.layout():
            _clear_layout(item.layout())
