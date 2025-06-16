from .apply_ext_filter import _apply_ext_filter
from .browse_files import browse_files
from .drag_enter_event import dragEnterEvent
from .drop_event import dropEvent
from .process_files import process_files
from .rebuild_ext_row import _rebuild_ext_row
from .browse_files import browse_files
from .filtered_file_list import _filtered_file_list
class fileDropManager:
    def __init__(self):
        self._rebuild_ext_row = _rebuild_ext_row
        self._filtered_file_list = _filtered_file_list
        self._apply_ext_filter = _apply_ext_filter
        self.process_files = process_files
        self.dropEvent = dropEvent
        self.browse_files = browse_files
        self._filtered_file_list = _filtered_file_list
    def get_functions(self,manager):
        manager._rebuild_ext_row = self._rebuild_ext_row
        manager._filtered_file_list = self._filtered_file_list
        manager._apply_ext_filter = self._apply_ext_filter
        manager.process_files = self.process_files
        manager.dropEvent = self.dropEvent
        manager.browse_files = self.browse_files
        manager._filtered_file_list = self._filtered_file_list
        return manager
