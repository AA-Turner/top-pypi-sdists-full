from .copy_selected import copy_selected
class FileSystemTreeManager:
    def __init__(self):
        self.copy_selected = copy_selected
    def get_functions(self,manager):
        manager.copy_selected = self.copy_selected
        return manager

