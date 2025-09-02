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
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)

        # Our custom Exit button
        exit_btn = QPushButton("Exit", self)
        exit_btn.clicked.connect(self.on_exit)
        layout.addWidget(exit_btn, alignment=Qt.AlignRight)

    def on_exit(self):
        self.exit_requested = True
        self.accept()   # close the dialog as a “rejection”
