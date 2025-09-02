# robust_logger.py — clean, dynamic, Qt6-friendly logging bridge (idempotent)

from __future__ import annotations

import os, sys, logging, traceback, threading, queue
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union, Callable

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QtMsgType, qInstallMessageHandler

# ─────────────────────────── constants / paths ────────────────────────────
APP_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "abstract_finder")
os.makedirs(APP_CACHE_DIR, exist_ok=True)
LOG_FILE = os.path.join(APP_CACHE_DIR, "finder.log")

# ───────────────────────────── idempotent guards ──────────────────────────
_LOGGING_WIRED = False
_QT_HANDLER_ATTACHED = False

# ─────────────────────────── core logging wiring ──────────────────────────
def setup_logging(*, level=logging.DEBUG, to_stderr_level=logging.INFO) -> None:
    """
    One-time setup for Python logging with:
      - Rotating file handler
      - Optional stderr stream (info+)
    Safe to call multiple times.
    """
    global _LOGGING_WIRED
    if _LOGGING_WIRED:
        return
    _LOGGING_WIRED = True

    root = logging.getLogger()
    root.setLevel(level)

    # Rotating file handler (avoid duplicates)
    if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == LOG_FILE
               for h in root.handlers):
        f = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        f.setLevel(level)
        f.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
        ))
        root.addHandler(f)

    # Stderr stream handler (avoid duplicates)
    if not any(isinstance(h, logging.StreamHandler) and getattr(h, "stream", None) is sys.stderr
               for h in root.handlers):
        c = logging.StreamHandler(sys.stderr)
        c.setLevel(to_stderr_level)
        c.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        root.addHandler(c)

def get_log_file_path() -> str:
    return LOG_FILE

# ───────────────────────── exception + Qt message hooks ───────────────────
def _format_exc(exctype, value, tb):
    return "".join(traceback.format_exception(exctype, value, tb))

def install_python_exception_hooks() -> None:
    """Route uncaught exceptions (main + threads) into logging."""
    def excepthook(exctype, value, tb):
        logging.critical("UNCAUGHT EXCEPTION:\n%s", _format_exc(exctype, value, tb))
    sys.excepthook = excepthook

    def threading_excepthook(args):
        logging.critical("THREAD EXCEPTION:\n%s", _format_exc(args.exc_type, args.exc_value, args.exc_traceback))
    threading.excepthook = threading_excepthook  # py3.8+

def install_qt_message_hook() -> None:
    """Optional: route Qt's qDebug/qWarning/... into Python logging."""
    global _QT_HANDLER_ATTACHED
    if _QT_HANDLER_ATTACHED:
        return
    _QT_HANDLER_ATTACHED = True

    def qt_message_handler(mode, ctx, message):
        level = {
            QtMsgType.QtDebugMsg: logging.DEBUG,
            QtMsgType.QtInfoMsg: logging.INFO,
            QtMsgType.QtWarningMsg: logging.WARNING,
            QtMsgType.QtCriticalMsg: logging.ERROR,
            QtMsgType.QtFatalMsg: logging.CRITICAL,
        }.get(mode, logging.INFO)
        # ctx.file/line can be None
        f = ctx.file or "unknown"
        ln = ctx.line or 0
        logging.log(level, "Qt: %s (%s:%d)", message, f, ln)

    qInstallMessageHandler(qt_message_handler)

# ─────────────────────────── GUI log bridge (Queue) ───────────────────────
class LogQueueHandler(logging.Handler):
    """
    Thread-safe handler that enqueues formatted log strings.
    A Qt-side timer drains the queue and appends to the widget in the GUI thread.
    """
    def __init__(self, q: queue.Queue[str], *, level=logging.DEBUG, formatter: Optional[logging.Formatter] = None):
        super().__init__(level=level)
        self.q = q
        if formatter is None:
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.q.put_nowait(self.format(record))
        except Exception:
            # Don't raise on logging failures
            pass

class QtLogBridge(QtCore.QObject):
    """
    Owns a QTimer that flushes a queue into a QPlainTextEdit.
    You can attach/detach at runtime; safe across threads.
    """
    def __init__(self, text_widget: QtWidgets.QPlainTextEdit, q: Optional[queue.Queue[str]] = None,
                 *, interval_ms: int = 120, max_batch: int = 500, parent: Optional[QtCore.QObject] = None):
        super().__init__(parent)
        self.text_widget = text_widget
        self.q: queue.Queue[str] = q or queue.Queue()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(interval_ms)
        self.max_batch = max_batch
        self.timer.timeout.connect(self._drain)
        self.timer.start()

    @QtCore.pyqtSlot()
    def _drain(self):
        # Pull a burst to keep UI snappy
        count = 0
        cursor = self.text_widget.textCursor()
        move_end = QtGui.QTextCursor.MoveOperation.End

        while count < self.max_batch:
            try:
                msg = self.q.get_nowait()
            except queue.Empty:
                break
            # Append without reflow
            cursor.movePosition(move_end)
            self.text_widget.setTextCursor(cursor)
            self.text_widget.appendPlainText(msg)
            count += 1

    def queue(self) -> queue.Queue[str]:
        return self.q

# ───────────────────────── convenience glue for widgets ───────────────────
class GuiLogAttachment:
    """
    Manages a single QueueHandler + QtLogBridge pair attached to the root logger.
    Idempotent per instance. Call .detach() to remove handler from root logger.
    """
    def __init__(self, text_widget: Optional[QtWidgets.QPlainTextEdit] = None):
        self.text_widget = text_widget
        self._bridge: Optional[QtLogBridge] = None
        self._queue_handler: Optional[LogQueueHandler] = None
        self._attached = False

    def _ensure_widget(self, host_widget: QtWidgets.QWidget) -> QtWidgets.QPlainTextEdit:
        # If none provided, create a minimal panel at the bottom of host_widget
        if self.text_widget is not None:
            return self.text_widget
        layout = host_widget.layout()
        if layout is None:
            layout = QtWidgets.QVBoxLayout(host_widget)
            host_widget.setLayout(layout)
        log_view = QtWidgets.QPlainTextEdit()
        log_view.setReadOnly(True)
        log_view.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        log_view.setObjectName("log_view")
        # small label row; optional
        row = QtWidgets.QHBoxLayout()
        row.addWidget(QtWidgets.QLabel("Log Output:"))
        row.addStretch(1)
        layout.addLayout(row)
        layout.addWidget(log_view)
        self.text_widget = log_view
        return log_view

    def attach(self, host_widget: QtWidgets.QWidget) -> None:
        if self._attached:
            return
        widget = self._ensure_widget(host_widget)
        self._bridge = QtLogBridge(widget)
        self._queue_handler = LogQueueHandler(self._bridge.queue())
        logging.getLogger().addHandler(self._queue_handler)
        self._attached = True

    def detach(self) -> None:
        if not self._attached:
            return
        root = logging.getLogger()
        if self._queue_handler in root.handlers:
            root.removeHandler(self._queue_handler)  # type: ignore[arg-type]
        self._queue_handler = None
        if self._bridge:
            self._bridge.timer.stop()
        self._bridge = None
        self._attached = False

# ───────────────────────── entry-point convenience ────────────────────────
def start_console(widget_or_cls: Union[QtWidgets.QWidget, type[QtWidgets.QWidget]],
                  *args, attach_logs: bool = True, hook_qt: bool = True, **kwargs) -> int:
    """
    Quick runner for a single-window tool.

    Args:
        widget_or_cls: a QWidget subclass *or* a QWidget instance.
        attach_logs: attach GUI log panel automatically.
        hook_qt: install Qt message handler into logging.

    Returns:
        app exit code.
    """
    setup_logging()
    install_python_exception_hooks()
    if hook_qt:
        install_qt_message_hook()

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)

    win = widget_or_cls(*args, **kwargs) if isinstance(widget_or_cls, type) else widget_or_cls

    if attach_logs:
        GuiLogAttachment().attach(win)

    win.show()
    return app.exec()

# ───────────────────────── optional: simple worker scaffold ───────────────
class DirScanWorker(QtCore.QObject):
    """
    Example directory scanner emitting chunks, safe to run in QThread.
    """
    progress = QtCore.pyqtSignal(list)  # list[str]
    done = QtCore.pyqtSignal(list)      # list[str]
    error = QtCore.pyqtSignal(str)

    def __init__(self, folder: Union[str, Path], exts: set[str], chunk_size: int = 256, parent=None):
        super().__init__(parent)
        self.folder = Path(folder)
        self.exts = {e.lower() for e in exts}
        self.chunk_size = max(1, chunk_size)
        self._cancel = False

    @QtCore.pyqtSlot()
    def run(self):
        try:
            if not self.folder.exists():
                self.done.emit([])
                return
            batch, all_paths = [], []
            for p in sorted(self.folder.iterdir()):
                if self._cancel:
                    return
                if p.is_file() and p.suffix.lower() in self.exts:
                    s = str(p)
                    batch.append(s)
                    all_paths.append(s)
                    if len(batch) >= self.chunk_size:
                        self.progress.emit(batch)
                        batch = []
            if batch and not self._cancel:
                self.progress.emit(batch)
            if not self._cancel:
                self.done.emit(all_paths)
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        self._cancel = True

def wire_dir_scan(host: QtWidgets.QWidget, folder: Union[str, Path], exts: set[str],
                  on_progress: Callable[[list[str]], None],
                  on_done: Callable[[list[str]], None],
                  on_error: Optional[Callable[[str], None]] = None) -> tuple[QtCore.QThread, DirScanWorker]:
    """
    Convenience to spin a DirScanWorker in a QThread and auto-clean up.
    """
    th = QtCore.QThread(host)
    worker = DirScanWorker(folder, exts)
    worker.moveToThread(th)

    th.started.connect(worker.run)
    worker.progress.connect(on_progress)
    worker.done.connect(on_done)
    if on_error:
        worker.error.connect(on_error)

    # cleanup
    worker.done.connect(th.quit)
    worker.error.connect(th.quit)
    th.finished.connect(worker.deleteLater)

    # Keep strong refs on host
    if not hasattr(host, "_threads"):
        host._threads = []             # type: ignore[attr-defined]
    if not hasattr(host, "_workers"):
        host._workers = []             # type: ignore[attr-defined]
    host._threads.append(th)           # type: ignore[attr-defined]
    host._workers.append(worker)       # type: ignore[attr-defined]

    th.start()
    return th, worker
