from ...imports import QtGui
def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
    if e.mimeData().hasUrls():
        e.acceptProposedAction()
