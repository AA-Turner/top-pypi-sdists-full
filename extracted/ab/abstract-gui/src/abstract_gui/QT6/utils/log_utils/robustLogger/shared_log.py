from __future__ import annotations
import os, sys, logging, threading, traceback, queue
from logging.handlers import RotatingFileHandler
from typing import Optional, Callable, Union
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QtMsgType, qInstallMessageHandler,QObject,pyqtSignal

# ── paths ────────────────────────────────────────────────────────────────
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "abstract_finder")
os.makedirs(CACHE_DIR, exist_ok=True)
LOG_FILE = os.path.join(CACHE_DIR, "finder.log")

# ── singletons / guards ─────────────────────────────────────────────────
_LOGGING_WIRED = False
_QT_MSG_HOOKED = False
_SERVICE_SINGLETON: "LogService|None" = None

def get_log_file_path() -> str:
    return LOG_FILE


class _QtLogEmitter(QtCore.QObject):
    # (logger_name, levelname, message)
    new_log = QtCore.pyqtSignal(str, str, str)


class _QtLogHandler(logging.Handler):
    def __init__(self, emitter: _QtLogEmitter):
        super().__init__(level=logging.DEBUG)
        self.emitter = emitter
        self.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"))
    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
        except Exception:
            msg = record.getMessage()
        # Structured emission: name, level, message
        try:
            # ensure newline for consistency
            if not msg.endswith("\n"):
                msg = msg + "\n"
            self.emitter.new_log.emit(record.name, record.levelname, msg)
        except Exception:
            # avoid logging.loop: fallback to stderr
            try:
                sys.stderr.write(f"LOG EMIT ERROR: {record}\n")
            except Exception:
                pass

_emitter: _QtLogEmitter | None = None
_handler: _QtLogHandler  | None = None

def _get_emitter() -> _QtLogEmitter:
    global _emitter
    if _emitter is None:
        # parent the emitter to the app if available so it has the correct thread affinity
        app = QtWidgets.QApplication.instance()
        parent = app if app is not None else None
        _emitter = _QtLogEmitter(parent)
        if app is not None:
            try:
                _emitter.moveToThread(app.thread())
            except Exception:
                pass
    return _emitter

def _ensure_qt_log_handler():
    global _handler
    if _handler is None:
        emitter = _get_emitter()
        _handler = _QtLogHandler(emitter)
        _handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(_handler)
        # ensure emitter lives on app thread if available
        app = QtWidgets.QApplication.instance()
        if app is not None:
            try:
                emitter.moveToThread(app.thread())
            except Exception:
                pass

def install_python_logging():
    root = logging.getLogger()
    if not root.handlers:
        root.setLevel(logging.DEBUG)

        f = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        f.setLevel(logging.DEBUG)
        f.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"))
        root.addHandler(f)

        c = logging.StreamHandler(sys.stderr)
        c.setLevel(logging.INFO)
        c.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        root.addHandler(c)

    def _format_exc(exctype, value, tb):
        return "".join(traceback.format_exception(exctype, value, tb))
    def excepthook(exctype, value, tb):
        logging.critical("UNCAUGHT EXCEPTION:\n%s", _format_exc(exctype, value, tb))
    sys.excepthook = excepthook

def install_qt_bridge():
    global _handler
    if _handler is None:
        _handler = _QtLogHandler(_get_emitter())
        _handler.setLevel(logging.DEBUG)
        _handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logging.getLogger().addHandler(_handler)

    def qt_msg(mode, ctx, message):
        level = {
            QtMsgType.QtDebugMsg:    logging.DEBUG,
            QtMsgType.QtInfoMsg:     logging.INFO,
            QtMsgType.QtWarningMsg:  logging.WARNING,
            QtMsgType.QtCriticalMsg: logging.ERROR,
            QtMsgType.QtFatalMsg:    logging.CRITICAL,
        }.get(mode, logging.INFO)
        logging.log(level, "Qt: %s (%s:%d)", message, ctx.file, ctx.line)
    qInstallMessageHandler(qt_msg)

def install_qt_logging():
    """Call once at app startup (idempotent)."""
    install_python_logging()
    install_qt_bridge()
# ── core logging wiring ─────────────────────────────────────────────────
def setup_root_logging(level=logging.DEBUG, stderr_level=logging.INFO) -> None:
    global _LOGGING_WIRED
    if _LOGGING_WIRED: return
    _LOGGING_WIRED = True

    root = logging.getLogger()
    root.setLevel(level)

    if not any(isinstance(h, RotatingFileHandler) and getattr(h, "baseFilename", "") == LOG_FILE for h in root.handlers):
        f = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        f.setLevel(level)
        f.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"))
        root.addHandler(f)

    if not any(isinstance(h, logging.StreamHandler) and getattr(h, "stream", None) is sys.stderr for h in root.handlers):
        c = logging.StreamHandler(sys.stderr)
        c.setLevel(stderr_level)
        c.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        root.addHandler(c)

def install_python_exception_hooks() -> None:
    def _fmt(e, v, tb): return "".join(traceback.format_exception(e, v, tb))
    def excepthook(exctype, value, tb):
        logging.critical("UNCAUGHT EXCEPTION:\n%s", _fmt(exctype, value, tb))
    sys.excepthook = excepthook

    def threading_excepthook(args):
        logging.critical("THREAD EXCEPTION:\n%s",
                         "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)))
    threading.excepthook = threading_excepthook  # py>=3.8

def install_qt_message_hook() -> None:
    global _QT_MSG_HOOKED
    if _QT_MSG_HOOKED: return
    _QT_MSG_HOOKED = True

    def qt_message_handler(mode, ctx, message):
        level = {
            QtMsgType.QtDebugMsg: logging.DEBUG,
            QtMsgType.QtInfoMsg: logging.INFO,
            QtMsgType.QtWarningMsg: logging.WARNING,
            QtMsgType.QtCriticalMsg: logging.ERROR,
            QtMsgType.QtFatalMsg: logging.CRITICAL,
        }.get(mode, logging.INFO)
        logging.log(level, "Qt: %s (%s:%s)", message, ctx.file or "unknown", ctx.line or 0)
    qInstallMessageHandler(qt_message_handler)

# ── queue handler + bridge ───────────────────────────────────────────────
class LogQueueHandler(logging.Handler):
    def __init__(self, q: "queue.Queue[str]", *, level=logging.DEBUG, fmt: Optional[logging.Formatter] = None):
        super().__init__(level=level)
        self.q = q
        self.setFormatter(fmt or logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    def emit(self, record: logging.LogRecord) -> None:
        try: self.q.put_nowait(self.format(record))
        except Exception: pass

class QtLogBridge(QtCore.QObject):
    def __init__(self, widget: QtWidgets.QPlainTextEdit, q: "queue.Queue[str]",
                 *, interval_ms=120, batch=500, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.q = q
        self.batch = batch
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self._drain)
        self.timer.start()

    @QtCore.pyqtSlot()
    def _drain(self):
        cursor = self.widget.textCursor()
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        self.widget.setTextCursor(cursor)
        for _ in range(self.batch):
            try:
                line = self.q.get_nowait()
            except queue.Empty:
                break
            self.widget.appendPlainText(line)

def attach_textedit_to_logs(target: Union[QtWidgets.QPlainTextEdit, QtWidgets.QTextEdit, Callable],
                            tail_file: Optional[str] = None,
                            logger_filter: Optional[Union[str, Callable[[str], bool]]] = None):
    """
    Attach a QPlainTextEdit/QTextEdit or a callable to receive structured logs.
    - `logger_filter` can be:
        * None -> accept all logs
        * str  -> prefix match on logger name (e.g. "apiTab" will accept "apiTab" or "apiTab.something")
        * callable(name)->bool -> custom accept function
    The displayed message will include the logger name as `[logger_name]`.
    """
    _ensure_qt_log_handler()
    emitter = _get_emitter()

    # normalize filter
    if logger_filter is None:
        def _accept(name: str) -> bool: return True
    elif isinstance(logger_filter, str):
        pref = logger_filter
        def _accept(name: str, pref=pref) -> bool:
            return name == pref or name.startswith(pref + ".") or name.startswith(pref + "_") or name.startswith(pref)
    elif callable(logger_filter):
        _accept = logger_filter
    else:
        raise TypeError("logger_filter must be None, str, or callable")

    # Build a slot that accepts (name, level, message)
    if callable(target) and not hasattr(target, "append"):
        # user provided a bare callable expecting a single string
        def _slot(name: str, level: str, message: str, target=target, _accept=_accept):
            if not _accept(name): return
            try:
                target(f"[{name}][{level}] {message}")
            except Exception:
                logging.exception("Log target callable failed")
        emitter.new_log.connect(_slot, QtCore.Qt.ConnectionType.QueuedConnection)
        use_widget = None
    else:
        # treat as widget (QPlainTextEdit or QTextEdit)
        te = target

        # detect best append method available on the widget
        append_fn = None
        if hasattr(te, "append") and callable(getattr(te, "append")):
            append_fn = te.append
            def _slot(name: str, level: str, message: str, append_fn=append_fn, _accept=_accept):
                if not _accept(name): return
                try:
                    append_fn(f"[{name}][{level}] {message}")
                except Exception:
                    logging.exception("Appending to text widget via .append() failed")
        elif hasattr(te, "appendPlainText") and callable(getattr(te, "appendPlainText")):
            append_fn = te.appendPlainText
            def _slot(name: str, level: str, message: str, te=te, append_fn=append_fn, _accept=_accept):
                if not _accept(name): return
                try:
                    # ensure cursor at end for nicer UX
                    try:
                        te.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                    except Exception:
                        pass
                    append_fn(f"[{name}][{level}] {message}")
                except Exception:
                    logging.exception("Appending to QPlainTextEdit failed")
        elif hasattr(te, "insertPlainText") and callable(getattr(te, "insertPlainText")):
            append_fn = te.insertPlainText
            def _slot(name: str, level: str, message: str, te=te, append_fn=append_fn, _accept=_accept):
                if not _accept(name): return
                try:
                    try:
                        te.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                    except Exception:
                        pass
                    append_fn(f"[{name}][{level}] {message}")
                except Exception:
                    logging.exception("Inserting into text widget failed")
        else:
            raise TypeError("attach_textedit_to_logs: target must be a widget with append()/appendPlainText()/insertPlainText() or a callable")

        # connect slot with queued connection
        emitter.new_log.connect(_slot, QtCore.Qt.ConnectionType.QueuedConnection)
        use_widget = te
        # Optional tailing (widget only)
    if tail_file and use_widget is not None:
        setattr(use_widget, "_tail_pos", getattr(use_widget, "_tail_pos", 0))
        timer = QtCore.QTimer(use_widget)
        timer.setInterval(500)
        def _poll():
            try:
                with open(tail_file, "r", encoding="utf-8", errors="replace") as f:
                    f.seek(getattr(use_widget, "_tail_pos", 0))
                    chunk = f.read()
                    use_widget._tail_pos = f.tell()
                    if chunk:
                        try:
                            use_widget.moveCursor(QtGui.QTextCursor.MoveOperation.End)
                            # chunk already likely contains line prefixes coming from the file format;
                            # we append raw file contents to preserve original formatting.
                            use_widget.insertPlainText(chunk)
                        except Exception:
                            try:
                                use_widget.append(chunk)
                            except Exception:
                                logging.exception("Failed to tail file into widget")
            except FileNotFoundError:
                pass
        timer.timeout.connect(_poll)
        timer.start()
        setattr(use_widget, "_tail_timer", timer)



# ── the service you’ll use everywhere ────────────────────────────────────
class LogService:
    """
    One shared queue + handler; attach the same stream to many widgets uniformly.
    """
    def __init__(self):
        setup_root_logging()
        install_python_exception_hooks()
        install_qt_message_hook()

        self.q: "queue.Queue[str]" = queue.Queue()
        self.handler = LogQueueHandler(self.q)
        self._attached_to_root = False
        self._bridges: list[QtLogBridge] = []

        self.attach_to_root()

    def attach_to_root(self):
        if self._attached_to_root: return
        logging.getLogger().addHandler(self.handler)
        self._attached_to_root = True

    def detach_from_root(self):
        if not self._attached_to_root: return
        logging.getLogger().removeHandler(self.handler)
        self._attached_to_root = False

    def _make_view(self, parent: QtWidgets.QWidget) -> QtWidgets.QPlainTextEdit:
        view = QtWidgets.QPlainTextEdit(parent)
        view.setReadOnly(True)
        view.setLineWrapMode(QtWidgets.QPlainTextEdit.LineWrapMode.NoWrap)
        view.setObjectName("abstract_log_view")
        return view

    def attach_log(self, host: QtWidgets.QWidget, *, place_in: Optional[QtWidgets.QLayout]=None,
                   with_label=True) -> QtWidgets.QPlainTextEdit:
        """
        Mount a log view inside host (or given layout) and start streaming.
        Returns the QPlainTextEdit so you can style or move it.
        """
        if place_in is None:
            layout = host.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(host)
                host.setLayout(layout)
        else:
            layout = place_in

        if with_label:
            row = QtWidgets.QHBoxLayout()
            row.addWidget(QtWidgets.QLabel("Logs"))
            row.addStretch(1)
            layout.addLayout(row)

        view = self._make_view(host)
        layout.addWidget(view)
        self._bridges.append(QtLogBridge(view, self.q, parent=host))
        return view

# singleton accessor
def get_log_service() -> LogService:
    global _SERVICE_SINGLETON
    if _SERVICE_SINGLETON is None:
        _SERVICE_SINGLETON = LogService()
    return _SERVICE_SINGLETON

### optional mini runner
##def startConsole(widget_or_cls: Union[type[QtWidgets.QWidget], QtWidgets.QWidget], *args, **kwargs) -> int:
##    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
##    win = widget_or_cls(*args, **kwargs) if isinstance(widget_or_cls, type) else widget_or_cls
##    win.show()
##    return app.exec()
##
