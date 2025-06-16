from ...imports import *
def on_tree_double_click(self, index: QtCore.QModelIndex):
    model = self.tree_wrapper.model
    path = model.filePath(index)
    if path:
        self._log(f"Double-clicked: {path}")
        self.drop_area.process_files([path])
