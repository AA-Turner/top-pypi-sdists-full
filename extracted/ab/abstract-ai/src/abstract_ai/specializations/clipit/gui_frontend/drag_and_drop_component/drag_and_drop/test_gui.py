# clipit/__init__.py
from ..imports import *

class DragDropWithFileBrowser(QtWidgets.QWidget):
    """
    Example composite widget:
      • A toolbar at the top with a toggle‐button for logs
      • A QSplitter in the middle: left side is a QFileSystemModel/view, right side is a file‐drop area
      • A QTextEdit at the bottom for logs
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        title = "ClipIt - File Browser + Drag/Drop + Logs"
        size=(950, 600)
        make_main_window(parent=self,
                         title=title,
                         size=size)
        main_layout = get_layout(parent=self)
        
        self.toolbar = make_toolbar(self)
        toggle_logs_action = get_toggle(self,
                                        action=self._on_toggle_logs,
                                        text="Toggle Logs",
                                        checkable=True)
        
        add_toolbar_action(self.toolbar,
                           toggle_logs_action)


        self.splitter = get_splitter(self,
                                     horizontal=True)
        self.fs_model = get_fs_model()

        self.tree_view = get_tree_view(model=self.fs_model,
                                       splitter=self.splitter)


        self.drop_area = get_drag_and_drop()

        add_to_splitter(self.splitter,
                        self.tree_view,
                        self.drop_area)
        self.log_textedit = get_logged_text_edits(parent=self,
                                                  readOnly=True,
                                                  visible=True)

        add_widgets(main_layout,
                    {"widget":self.toolbar,
                     "kwargs":{"stretch":1}},
                    {"widget":self.splitter},
                    {"widget":self.log_textedit}
                    )



    def _on_toggle_logs(self, checked: bool):
        """
        Show/hide the logs area when the toolbar button is toggled.
        """
        set_visible(parent = self.log_textedit,
                    checked=checked)

win = DragDropWithFileBrowser
run_app(win)
