from ...imports import *
def on_tree_copy(self, paths: List[str]):
   """
   Called when the “Copy Selected” button is pressed.
   We log how many items, then forward to drop_area.
   """
   self._log(f"Copy Selected triggered on {len(paths)} path(s).")
   self.drop_area.process_files(paths)
