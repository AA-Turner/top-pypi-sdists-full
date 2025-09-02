from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from pathlib import Path
from PyQt6.QtWidgets import QTextEdit
# ─────────────────────────── instance augmentation helpers ───────────────────────
def graceful_shutdown(self):
    for w in list(getattr(self, "_active_workers", [])):
        w.cancel()
    for t in list(getattr(self, "_threads", [])):
        if t.isRunning():
            t.requestInterruption()
            t.quit()
            t.wait(5000)
    self._active_workers = []
    self._threads = []

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
    self._graceful_shutdown = graceful_shutdown.__get__(self)

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
