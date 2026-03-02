from .worker_scans import *
from .collapsable_log_panel import *
from ..log_utils import *
from .ensure_resizable import *
from PyQt6.QtWidgets import QApplication
from .log_manager import *
from ..imports import *
# ─────────────────────────── runner ───────────────────────────────────────────────

def startConsole(console_class, *args, **kwargs):
    """
    Creates the app/window, wires scanning + log view,
    wraps logs in a toolbar-style collapsible panel that expands the window
    (so the main content isn't squeezed).
    """
    app = QApplication.instance() or QApplication(sys.argv)

    win = console_class(*args, **kwargs)
    get_WorkerScans(win)  # ensures win.log (QTextEdit) and shutdown plumbing exist

    # Ensure main layout

    lay = win.layout()
    if lay is None:
        # No layout yet → give the window a VBox
        lay = QVBoxLayout(win)
        win.setLayout(lay)
    elif not isinstance(lay, (QVBoxLayout, QHBoxLayout)):
        # Has some other type (maybe abstract) → wrap it inside a VBox
        old_lay = lay
        lay = QVBoxLayout()
        win.setLayout(lay)
        lay.addLayout(old_lay)   # preserve the old one inside

    # Use a horizontal splitter to allow future extra panes next to the main log
    splitter = QtWidgets.QSplitter(Qt.Orientation.Horizontal, win)
    splitter.addWidget(win.log)  # win.log is the QTextEdit created by get_WorkerScans

    # Collapsible panel that grows/shrinks the window instead of squishing content
    log_panel = CollapsibleLogPanel("Logs", splitter, start_visible=False, parent=win)
    lay.addWidget(log_panel)

    # Reuse the same toggle action in a top toolbar if this is a QMainWindow
    if isinstance(win, QtWidgets.QMainWindow):
        tb = win.addToolBar("View")
        tb.setMovable(False); tb.setFloatable(False)
        tb.addAction(log_panel.toggle_action)

    # Stream live logs + tail existing file (if any). NOTE: only 2 args supported.
    attach_textedit_to_logs(win.log, tail_file=get_log_file_path())

    ensure_user_resizable(win, initial_size=(1100, 800), min_size=(600, 400))
    keep_capped_across_screen_changes(win, margin=8, fraction=0.95)

    # Clean shutdown for threads/workers
    if hasattr(win, "_graceful_shutdown"):
        app.aboutToQuit.connect(win._graceful_shutdown)

    win.show()
    return app.exec()
