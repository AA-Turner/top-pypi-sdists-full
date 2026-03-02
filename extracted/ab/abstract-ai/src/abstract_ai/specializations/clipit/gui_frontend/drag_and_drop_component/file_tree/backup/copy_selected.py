def copy_selected(self):
    """
    Gather all selected items (column=0 only), convert to paths,
    and hand them off to parent’s on_tree_copy().
    """
    indexes = self.tree.selectionModel().selectedIndexes()
    file_paths = set()
    for idx in indexes:
        if idx.column() == 0:
            path = self.model.filePath(idx)
            file_paths.add(path)

    if not file_paths:
        QtWidgets.QMessageBox.warning(self, "No Selection", "Please select at least one file or folder.")
        return

    msg = f"copy_selected: {len(file_paths)} item(s) selected."
    self._log(msg)

    parent = self.parent()
    if parent and hasattr(parent, "on_tree_copy"):
        parent.on_tree_copy(list(file_paths))
