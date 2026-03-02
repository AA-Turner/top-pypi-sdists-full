#!/usr/bin/env python3
# main.py

import os
os.environ["QT_XCB_GL_INTEGRATION"] = "none"

from PyQt5 import QtCore, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseSoftwareOpenGL)
from .drag_and_drop import DragDropWithFileBrowser, DragDropWithWebBrowser
from .file_drop_area  import FileDropArea
from .file_tree       import FileSystemTree
from .JSBridge import JSBridge
from .imports import *
import sys

def gui_main():
    win = DragDropWithFileBrowser
    run_app(win=win,win_kwargs={"FileSystemTree":FileSystemTree,"FileDropArea":FileDropArea})


def gui_web(target_url=None):
    from .JSBridge import JSBridge
    app = QtWidgets.QApplication(sys.argv)

    # Pass the URL into the constructor of your widget
    window = DragDropWithWebBrowser(
        FileDropArea=FileDropArea,
        FileSystemTree=FileSystemTree,
        JSBridge=JSBridge,
        url=target_url,                 # new parameter
    )
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "web":
        # e.g. `python -m clipit.main web https://my.site/to/inspect`
        url_to_load = sys.argv[2] if len(sys.argv) > 2 else None
        gui_web(target_url=url_to_load)
    else:
        gui_main()
