from typing import *
from ...imports import *
from abstract_utilities.robust_reader import collect_filepaths
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
def _rebuild_ext_row(self, paths: List[str]):
    """
    1. Collect unique extensions from `paths` (only actual files).
    2. Wipe any existing checkboxes.
    3. Create a checkbox for each extension, preserving prior states.
    4. Show the row, or hide if no extensions found.
    """
    exts = {os.path.splitext(p)[1].lower() for p in paths if os.path.isfile(p)}
    exts.discard("")   # drop empty ext (e.g. directories)
    self._log(f"Unique extensions: {exts}")

    if not exts:
        # No file‐extensions → hide the row
        self.ext_row.setVisible(False)
        self.ext_checks.clear()
        return

    # Remove any existing checkboxes from the layout
    _clear_layout(self.ext_row_lay)

    new_checks: dict[str, QtWidgets.QCheckBox] = {}
    for ext in sorted(exts):
        cb = QtWidgets.QCheckBox(ext)
        # Keep prior check state if exists, else default True
        cb.setChecked(self.ext_checks.get(ext, True))
        cb.stateChanged.connect(self._apply_ext_filter)
        self.ext_row_lay.addWidget(cb)
        new_checks[ext] = cb

    # Replace with new map
    self.ext_checks = new_checks
    # Make the row visible now that it has content
    self.ext_row.setVisible(True)
def process_files(self, raw_paths: List[str], *, rebuild_ext_row: bool = True):
    """
    1. Expand directories → flat list of file‐paths.
    2. If rebuild_ext_row: re-derive the set of extensions.
    3. Filter by checked extensions.
    4. Read each file, concatenate, copy to clipboard.
    """
    self._last_raw_paths = raw_paths
    # Expand directories, apply exclusion rules
    all_paths = collect_filepaths(
        raw_paths,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
        exclude_file_patterns=DEFAULT_EXCLUDE_FILE_PATTERNS
    )
    self._log(f"{len(all_paths)} total path(s) after expansion")

    # Step 2: maybe rebuild the extension-filter row
    if rebuild_ext_row:
        self._rebuild_ext_row(paths=all_paths)

    # Step 3: determine which extensions remain checked
    if self.ext_checks:
        visible_exts = {ext for ext, cb in self.ext_checks.items() if cb.isChecked()}
        self._log(f"Visible extensions: {visible_exts}")
        # Filter out any file that isn’t a directory or whose ext isn’t in visible_exts
        filtered_paths = [
            p for p in all_paths
            if os.path.isdir(p) or os.path.splitext(p)[1].lower() in visible_exts
        ]
    else:
        # No checkboxes exist ⇒ no filtering
        filtered_paths = all_paths

    if not filtered_paths:
        self.status.setText("⚠️ No files match current extension filter.")
        return

    # Step 4: Read + combine
    count = len(filtered_paths)
    msg = f"Reading {count} file(s)…"
    self.status.setText(msg)
    self._log(msg)
    QtWidgets.QApplication.processEvents()

    combined: list[str] = []
    for idx, p in enumerate(filtered_paths):
        combined.append(f"=== {p} ===\n")
        try:
            text = read_file_as_text(p)
            combined.append(str(text) or "")
        except Exception as exc:
            combined.append(f"[Error reading {os.path.basename(p)}: {exc}]\n")
            self._log(f"Error reading {p} → {exc}")
        if idx < count - 1:
            combined.append("\n\n――――――――――――――――――\n\n")

    # Copy to clipboard
    QtWidgets.QApplication.clipboard().setText("".join(combined))
    self.status.setText(f"✅ Copied {count} file(s) to clipboard!")
    self._log(f"Copied {count} file(s) successfully")
