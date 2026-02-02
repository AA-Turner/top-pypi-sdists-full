"""
CSSL GUI Builder - Visual GUI designer for CSSL applications.

Launch via CLI:  includecpp cssl guimaker [optional_file.cssl]
Launch via Python:  python -m includecpp.gui.guimaker
"""


def run_guimaker(file_path: str = "") -> None:
    """Launch the CSSL GUI Builder application."""
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("\n[Error] PyQt6 is required for the CSSL GUI Builder.")
        print("Install it with:  pip install PyQt6")
        print()
        return

    import sys
    from .app import GuiMakerApp

    app = QApplication.instance()
    standalone = app is None
    if standalone:
        app = QApplication(sys.argv)

    window = GuiMakerApp(initial_file=file_path)
    window.show()

    if standalone:
        sys.exit(app.exec())
