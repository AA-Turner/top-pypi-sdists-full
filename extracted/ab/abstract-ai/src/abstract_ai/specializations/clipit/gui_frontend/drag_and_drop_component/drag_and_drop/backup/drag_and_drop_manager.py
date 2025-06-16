from .toggle_logs import _toggle_logs
from .on_tree_copy import on_tree_copy
from .on_tree_double_click import on_tree_double_click
class dragAndDropManager:
    def __init__(self):
        self.on_tree_copy = on_tree_copy
        self.on_tree_double_click = on_tree_double_click
        self._toggle_logs = _toggle_logs
    def get_functions(self,manager):
        manager._toggle_logs = self._toggle_logs
        manager.on_tree_copy = self.on_tree_copy
        manager.on_tree_double_click = self.on_tree_double_click
        return manager
