from ...imports import *
# ---------------------------------------------------------------- ext row
def _rebuild_ext_row(self, paths: list[str]):
    # discover unique extensions
    exts = {os.path.splitext(p)[1].lower() for p in paths if os.path.isfile(p)}
    exts.discard("")                                     # safety
    if not exts:
        self.ext_row.setVisible(False)
        return

    self.ext_row_lay.setParent(None)                     # wipe
    self.ext_row_lay = QtWidgets.QHBoxLayout(self.ext_row_w)
    self.ext_row_lay.setContentsMargins(4, 4, 4, 4)
    self.ext_row_lay.setSpacing(10)

    new_checks = {}
    for ext in sorted(exts):
        cb = QtWidgets.QCheckBox(ext)
        cb.setChecked(self.ext_checks.get(ext, True))    # keep previous state
        cb.stateChanged.connect(self._apply_ext_filter)
        self.ext_row_lay.addWidget(cb)
        new_checks[ext] = cb

    self.ext_checks = new_checks
    self.ext_row.setVisible(True)
# ---------------------------------------------------------------- read
def process_files(self, raw_paths: List[str], *, rebuild_ext_row: bool = True):
    """Filter → read → copy to clipboard."""
    self._last_raw_paths = raw_paths                     # remember for toggles
    paths = self._filtered_file_list(raw_paths=raw_paths)
    if rebuild_ext_row:
        self._rebuild_ext_row(paths)

    # honour ext checkboxes
    visible_exts = {ext for ext, cb in self.ext_checks.items() if cb.isChecked()}
    paths = [
        p for p in paths
        if os.path.isdir(p) or os.path.splitext(p)[1].lower() in visible_exts
    ]
    if not paths:
        self.status.setText("⚠️ No files match current ext filter.")
        return

    msg = f"Reading {len(paths)} file(s)…"
    self.status.setText(msg); self._log(msg); QtWidgets.QApplication.processEvents()

    combined: list[str] = []
    for i, p in enumerate(paths):
        combined.append(f"=== {p} ===\n")
        try:
            combined.append(read_file_as_text(p))
        except Exception as err:
            combined.append(f"[Error reading {os.path.basename(p)}: {err}]\n")
            self._log(f"read error {p} – {err}")
        if i < len(paths) - 1:
            combined.append("\n\n――――――――――――――――――\n\n")

    QtWidgets.QApplication.clipboard().setText("".join(combined))
    self.status.setText(f"✅ Copied {len(paths)} file(s) to clipboard!")

def _apply_ext_filter(self):
    """Run when any ext checkbox toggles: store → re-process."""
    if not hasattr(self, "_last_raw_paths"):
        return
    self.process_files(self._last_raw_paths, rebuild_ext_row=False)

def _filtered_file_list(self, raw_paths: List[str]) -> List[str]:
    paths = collect_filepaths(
        raw_paths,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
        exclude_file_patterns=DEFAULT_EXCLUDE_FILE_PATTERNS,
    )
    self._log(f"_filtered_file_list → {len(paths)}")
    return paths
