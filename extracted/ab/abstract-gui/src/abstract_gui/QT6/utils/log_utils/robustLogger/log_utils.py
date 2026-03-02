from __future__ import annotations
from pathlib import Path
import sys, os, logging, traceback, threading
from logging.handlers import RotatingFileHandler

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QTextEdit, QHBoxLayout, QLabel
from ..imports import QObject,pyqtSignal
# sizing helpers (safe to import; must not create widgets at import time)
from ...console_utils.ensure_resizable import ensure_user_resizable, keep_capped_across_screen_changes

# ─────────────────────────── logging setup (idempotent) ───────────────────────────
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "abstract_finder")
LOG_FILE = os.path.join(CACHE_DIR, "finder.log")
os.makedirs(CACHE_DIR, exist_ok=True)

def get_log_file_path() -> str:
    return LOG_FILE

# ---------- Python/Qt -> Qt signal bridge ----------
class QtLogEmitter(QObject):
    new_log = pyqtSignal(str)

_emitter_singleton: QtLogEmitter | None = None
_handler_singleton: logging.Handler | None = None

def _emitter() -> QtLogEmitter:
    global _emitter_singleton
    if _emitter_singleton is None:
        _emitter_singleton = QtLogEmitter()
    return _emitter_singleton

_log_configured = False
def setup_logging():
    global _log_configured
    if _log_configured:
        return
    _log_configured = True

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == LOG_FILE
               for h in root.handlers):
        f = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        f.setLevel(logging.DEBUG)
        f.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"))
        root.addHandler(f)

    if not any(isinstance(h, logging.StreamHandler) and getattr(h, "stream", None) is sys.stderr
               for h in root.handlers):
        c = logging.StreamHandler(sys.stderr)
        c.setLevel(logging.INFO)
        c.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        root.addHandler(c)

logger = logging.getLogger(__name__)
setup_logging()

# Crash -> log
def _format_exc(exctype, value, tb):
    return "".join(traceback.format_exception(exctype, value, tb))

def _excepthook(exctype, value, tb):
    logging.critical("UNCAUGHT EXCEPTION:\n%s", _format_exc(exctype, value, tb))
sys.excepthook = _excepthook

def _threading_excepthook(args):
    logging.critical("THREAD EXCEPTION:\n%s", "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)))
threading.excepthook = _threading_excepthook

# Qt → logging
def _qt_message_handler(mode, ctx, message):
    from PyQt6.QtCore import QtMsgType
    level = {
        QtMsgType.QtDebugMsg: logging.DEBUG,
        QtMsgType.QtInfoMsg: logging.INFO,
        QtMsgType.QtWarningMsg: logging.WARNING,
        QtMsgType.QtCriticalMsg: logging.ERROR,
        QtMsgType.QtFatalMsg: logging.CRITICAL,
    }.get(mode, logging.INFO)
    logging.log(level, "Qt: %s (%s:%d)", message, ctx.file or "unknown", ctx.line or 0)

QtCore.qInstallMessageHandler(_qt_message_handler)

def get_log_file_path() -> str:
    return LOG_FILE

# ─────────────────────────── lightweight Qt log bridge ───────────────────────────
class _QtLogEmitter(QtCore.QObject):
    new_log = QtCore.pyqtSignal(str)

class _QtLogHandler(logging.Handler):
    def __init__(self, emitter: _QtLogEmitter):
        super().__init__(level=logging.DEBUG)
        self.emitter = emitter
        self.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
        except Exception:
            msg = record.getMessage()
        self.emitter.new_log.emit(msg + "\n")

_emitter: _QtLogEmitter | None = None
_handler: _QtLogHandler  | None = None

def _get_emitter() -> _QtLogEmitter:
    global _emitter
    if _emitter is None:
        _emitter = _QtLogEmitter()
    return _emitter

def _ensure_qt_log_handler():
    global _handler
    if _handler is None:
        _handler = _QtLogHandler(_get_emitter())
        logging.getLogger().addHandler(_handler)

def attach_textedit_to_logs(textedit: QTextEdit, tail_file: str | None = None):
    """Stream live logs into a QTextEdit; optionally tail existing file content."""
    _ensure_qt_log_handler()
    _get_emitter().new_log.connect(textedit.append)

    if tail_file:
        # tail the file without blocking; poll with QTimer
        textedit._tail_pos = 0
        timer = QtCore.QTimer(textedit)
        timer.setInterval(500)
        def _poll():
            try:
                with open(tail_file, "r", encoding="utf-8", errors="replace") as f:
                    f.seek(getattr(textedit, "_tail_pos", 0))
                    chunk = f.read()
                    textedit._tail_pos = f.tell()
                    if chunk:
                        textedit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                        textedit.insertPlainText(chunk)
            except FileNotFoundError:
                pass
        timer.timeout.connect(_poll)
        timer.start()
        textedit._tail_timer = timer  # prevent GC

# ─────────────────────────── directory scan worker (QThread) ─────────────────────
class DirScanWorker(QtCore.QObject):
    progress = QtCore.pyqtSignal(list)  # list[str]
    done     = QtCore.pyqtSignal(list)  # list[str]
    error    = QtCore.pyqtSignal(str)

    def __init__(self, folder: Path, exts: set[str], chunk_size=256, parent=None):
        super().__init__(parent)
        self.folder = Path(folder)
        self.exts = {e.lower() for e in exts}
        self.chunk_size = max(1, chunk_size)
        self._cancel = False

    @QtCore.pyqtSlot()
    def run(self):
        try:
            if not self.folder.exists():
                self.done.emit([]); return
            batch, all_paths = [], []
            for p in sorted(self.folder.iterdir()):
                if self._cancel or QtCore.QThread.currentThread().isInterruptionRequested():
                    return
                if p.is_file() and p.suffix.lower() in self.exts:
                    s = str(p)
                    batch.append(s); all_paths.append(s)
                    if len(batch) >= self.chunk_size:
                        self.progress.emit(batch); batch = []
            if batch and not self._cancel:
                self.progress.emit(batch)
            if not self._cancel:
                self.done.emit(all_paths)
        except Exception as e:
            self.error.emit(str(e))

    def cancel(self):
        self._cancel = True

# ─────────────────────────── instance augmentation helpers ───────────────────────
def _graceful_shutdown(self):
    for w in list(getattr(self, "_active_workers", [])):
        w.cancel()
    for t in list(getattr(self, "_threads", [])):
        if t.isRunning():
            t.requestInterruption()
            t.quit()
            t.wait(5000)
    self._active_workers = []
    self._threads = []

def get_WorkerScans(self):
    """Augment an existing QWidget instance with scanning + logging hooks."""
    self._threads: list[QtCore.QThread] = []
    self._active_workers: list[DirScanWorker] = []

    # add a log view (only now, post-QApplication)
    self.log = QTextEdit(self)
    self.log.setReadOnly(True)
    self.log.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    # bind slots
    self._start_dir_scan = _start_dir_scan.__get__(self)
    self._on_scan_progress = _on_scan_progress.__get__(self)
    self._on_scan_done = _on_scan_done.__get__(self)
    self._on_scan_error = _on_scan_error.__get__(self)
    self._graceful_shutdown = _graceful_shutdown.__get__(self)

    # wrap closeEvent
    orig_close = getattr(self, "closeEvent", None)
    def _wrapped_close(ev):
        try:
            self._graceful_shutdown()
        finally:
            if orig_close:
                orig_close(ev)
            else:
                super(self.__class__, self).closeEvent(ev)
    self.closeEvent = _wrapped_close
    return self

def _start_dir_scan(self, folder: Path):
    # cancel existing
    for w in list(self._active_workers): w.cancel()
    for t in list(self._threads):
        if t.isRunning():
            t.requestInterruption(); t.quit(); t.wait(5000)

    th = QtCore.QThread()               # no parent; we manage lifetime
    th.setObjectName(f"DirScan::{folder}")
    worker = DirScanWorker(folder, self.EXTS)
    worker.moveToThread(th)

    th.started.connect(worker.run)
    worker.progress.connect(self._on_scan_progress)
    worker.done.connect(self._on_scan_done)
    worker.error.connect(self._on_scan_error)

    def _cleanup_refs():
        try: worker.deleteLater()
        except Exception: pass
        if th in self._threads: self._threads.remove(th)
        if worker in self._active_workers: self._active_workers.remove(worker)
        th.deleteLater()

    worker.done.connect(lambda *_: th.quit())
    worker.error.connect(lambda *_: th.quit())
    th.finished.connect(_cleanup_refs)

    self._threads.append(th)
    self._active_workers.append(worker)
    th.start()

@QtCore.pyqtSlot(list)
def _on_scan_progress(self, chunk: list[str]):
    for path in chunk:
        lbl = QtWidgets.QLabel()
        lbl.setFixedSize(self.expanded_thumb_size, self.expanded_thumb_size)
        lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("border:1px solid #ccc; background:#eee;")
        icon = QtGui.QIcon(path)
        pm = icon.pixmap(self.expanded_thumb_size, self.expanded_thumb_size)
        if not pm.isNull():
            lbl.setPixmap(pm)
        lbl.setProperty("path", path)
        lbl.mousePressEvent = (lambda ev, p=path: self._show_image(p))
        self.expanded_layout.addWidget(lbl)

@QtCore.pyqtSlot(list)
def _on_scan_done(self, all_paths: list[str]):
    self.current_images = all_paths
    self.current_index = 0 if all_paths else -1
    if all_paths:
        self._show_image(all_paths[0])

@QtCore.pyqtSlot(str)
def _on_scan_error(self, msg: str):
    logging.getLogger(__name__).exception("Dir scan error: %s", msg)

# ─────────────────────────── runner ───────────────────────────────────────────────
def startConsole(console_class, *args, **kwargs):
    """
    Safe entry: ensures QApplication exists, then builds the window, wires logs/workers,
    and applies your resizable/capping helpers.
    """
    try:
        logging.info("Starting console application")

        app = QApplication.instance() or QApplication(sys.argv)
        win = console_class(*args, **kwargs)          # 1) construct widget (no UI globals)
        get_WorkerScans(win)                          # 2) add worker/log plumbing

        # If your widget has a layout, mount the log view at the bottom.
        lay = win.layout() or QtWidgets.QVBoxLayout(win)
        if win.layout() is None:
            win.setLayout(lay)
        # optional label row
        row = QHBoxLayout(); row.addWidget(QLabel("Log Output:")); row.addStretch(1)
        lay.addLayout(row); lay.addWidget(win.log)

        attach_textedit_to_logs(win.log, tail_file=get_log_file_path())  # live logs + tail
        ensure_user_resizable(win, initial_size=(1100, 800), min_size=(600, 400))
        keep_capped_across_screen_changes(win, margin=8, fraction=0.95)

        app.aboutToQuit.connect(win._graceful_shutdown)

        win.show()
        return app.exec()
    except Exception:
        logging.critical("Startup failed:\n%s", traceback.format_exc())
        print(traceback.format_exc())
        return 1
