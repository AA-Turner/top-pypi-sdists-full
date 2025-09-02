from __future__ import annotations
from ...imports import *
# collapsible_log_panel.py

from PyQt6 import QtCore, QtGui, QtWidgets

class CollapsibleLogPanel(QtWidgets.QWidget):
    """
    Collapsible panel that *adds* height to the top-level window when expanded,
    and subtracts it when collapsed, so the central area isn't squished.
    """
    toggled = QtCore.pyqtSignal(bool)

    def __init__(self, title: str, content_widget: QtWidgets.QWidget,
                 *, start_visible: bool = True, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent)
        self._content = content_widget
        self._frame = QtWidgets.QFrame(self)
        self._frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        # make the frame fixed-height so layout doesn’t steal from central area
        self._frame.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                  QtWidgets.QSizePolicy.Policy.Fixed)

        fl = QtWidgets.QVBoxLayout(self._frame)
        fl.setContentsMargins(0, 0, 0, 0)
        fl.addWidget(self._content)

        # header as a toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.toggle_action = QtGui.QAction(self)
        self.toggle_action.setCheckable(True)
        self.toggle_action.setChecked(start_visible)
        self._title = title
        self._refresh_toggle_text(start_visible)
        self.toggle_action.triggered.connect(self._on_toggled)

        clear_action = QtGui.QAction("Clear", self)
        clear_action.triggered.connect(self._try_clear)

        self.toolbar.addAction(self.toggle_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(clear_action)
        self.toolbar.addSeparator()

        # keyboard shortcuts for toggle
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+L"), self, activated=self.toggle_action.trigger)
        QtGui.QShortcut(QtGui.QKeySequence("F12"), self, activated=self.toggle_action.trigger)

        # compose
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)
        root.addWidget(self.toolbar)
        root.addWidget(self._frame)

        # initial visibility + prepared height
        self._frame.setVisible(start_visible)
        QtCore.QTimer.singleShot(0, self._sync_frame_height)

    # public helpers
    def expand(self): self.toggle_action.setChecked(True)
    def collapse(self): self.toggle_action.setChecked(False)
    def is_expanded(self) -> bool: return self.toggle_action.isChecked()
    def content_widget(self) -> QtWidgets.QWidget: return self._content

    # internals
    def _refresh_toggle_text(self, expanded: bool):
        arrow = "▾" if expanded else "▸"
        self.toggle_action.setText(f"{self._title} {arrow}")

    def _current_frame_hint(self) -> int:
        # the height we want when expanded
        # you can cap this if you want: return min(self._frame.sizeHint().height(), 240)
        return self._frame.sizeHint().height()

    def _sync_frame_height(self):
        # keep the frame’s max/min height consistent with its visibility
        if self._frame.isVisible():
            h = self._current_frame_hint()
            self._frame.setMinimumHeight(h)
            self._frame.setMaximumHeight(h)
        else:
            self._frame.setMinimumHeight(0)
            self._frame.setMaximumHeight(0)

    def _resize_top_level_by(self, delta_h: int):
        if delta_h == 0:
            return
        win = self.window()
        if not isinstance(win, QtWidgets.QWidget):
            return
        g = win.geometry()
        new_h = max(win.minimumHeight(), g.height() + delta_h)

        # keep within screen’s available geometry
        screen = win.screen() or QtGui.QGuiApplication.primaryScreen()
        if screen:
            avail = screen.availableGeometry()
            # leave a small margin from the bottom
            max_h = avail.height() - 16
            new_h = min(new_h, max_h)

        win.resize(g.width(), new_h)

    @QtCore.pyqtSlot(bool)
    def _on_toggled(self, checked: bool):
        # compute delta before we change visibility
        if checked:
            target_h = self._current_frame_hint()
            prev_h = 0 if not self._frame.isVisible() else self._frame.height()
            delta = target_h - prev_h
        else:
            prev_h = self._frame.height() if self._frame.isVisible() else 0
            delta = -prev_h

        self._frame.setVisible(checked)
        self._refresh_toggle_text(checked)
        self._sync_frame_height()

        # do the window resize after layout settles
        QtCore.QTimer.singleShot(0, lambda d=delta: self._resize_top_level_by(d))
        self.toggled.emit(checked)

    def _try_clear(self):
        w = self._content
        # try common editors
        for cls in (QtWidgets.QPlainTextEdit, QtWidgets.QTextEdit):
            edit = w if isinstance(w, cls) else w.findChild(cls)
            if edit:
                edit.clear()
                return
