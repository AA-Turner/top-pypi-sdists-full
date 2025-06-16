from ..imports import *
def get_tree(model=None,index=None,root_path=None,hideColumns=True,dragEnabled=True):
    tree = QtWidgets.QTreeView()
    model = model or get_fs_model(index=index,root_path=root_path,hideColumns=hideColumns)
    tree.setModel(model)
    home_index = model.index
    # Multi-selection & drag from tree
    tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    tree.setDragEnabled(dragEnabled)
    tree.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
    return tree
class FileSystemTree(QtWidgets.QWidget):
    """
    Left‐hand pane: file browser + “Copy Selected” button.
    """
    def __init__(self, log_widget=None,parent=None):

        super().__init__(parent)
        self.log_widget = get_log_widget()
        layout = get_layout(parent=self)

        # QFileSystemModel + QTreeView
        self.model = get_fs_model()

        self.tree = get_tree(model=self.model,
                             hideColumns=True)
    
        # “Copy Selected” button
        text = "Copy Selected to Clipboard"
        copy_btn = get_push_button(text=text,
                        action=self.copy_selected)
        add_widgets(layout,
                    {"widget":self.tree},
                    {"widget":copy_btn}
                    )


        self.setLayout(layout)
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


    def _log(self, message: str):
        """Write out to the shared log widget (with timestamp)."""
        log_it(self=self, message=message)
