import os, sys, logging, threading, traceback, queue, logging
from typing import *
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QtMsgType, qInstallMessageHandler
from logging.handlers import RotatingFileHandler
# ─────────────────────────── Qt log bridge (structured, filterable) ───────────────
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

