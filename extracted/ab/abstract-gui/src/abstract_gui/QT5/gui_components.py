from .gui_utils import run_app
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel,
    QLineEdit, QDialogButtonBox, QPushButton
)
from PyQt5.QtCore import Qt
class InputDialog(QDialog):
    def __init__(self,prompt=None,title=None):
        super().__init__(flags=Qt.Window)
        self.setWindowTitle(title)
        self.exit_requested = False

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(prompt))

        # Text field
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)

        # Button box with OK / Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            parent=self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Our custom Exit button
        exit_btn = QPushButton("Exit", self)
        exit_btn.clicked.connect(self.on_exit)
        layout.addWidget(exit_btn, alignment=Qt.AlignRight)

    def on_exit(self):
        self.exit_requested = True
        self.reject()   # close the dialog as a “rejection”

def getUserInputwindow(prompt="Enter text:", title="Input"):
    """
    Pops up a dialog with OK / Cancel / Exit.
    Returns:
      • (str, bool) → (what the user typed, whether Exit was pressed)
    """
    # Show the dialog
    dlg = run_app(win=InputDialog,
                  win_kwargs={"prompt": prompt, "title": title})
    text, exit_pressed = dlg.line_edit.text(), dlg.exit_requested
    # Grab whatever’s in the line-edit and whether Exit was clicked
    

    return text, exit_pressed

