from ...imports import *
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
