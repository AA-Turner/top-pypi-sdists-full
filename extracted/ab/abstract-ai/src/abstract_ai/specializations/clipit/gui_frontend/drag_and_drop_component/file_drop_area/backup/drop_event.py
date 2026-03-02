from ...imports import QtGui
def dropEvent(self, e: QtGui.QDropEvent):
    try:
        raw_paths = [u.toLocalFile() for u in e.mimeData().urls() if u.isLocalFile()]
        if not raw_paths:
            raise ValueError("No local files detected.")
        self._log(f"dropped {len(raw_paths)} path(s)")
        self.process_files(raw_paths)
    except Exception as exc:
        self.status.setText(f"⚠️ {exc}")
        self._log(f"dropEvent ERROR: {exc}")
