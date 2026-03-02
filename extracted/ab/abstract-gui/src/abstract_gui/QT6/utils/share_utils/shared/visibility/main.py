# abstract_visibility.py
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QLayout, QToolButton, QWidget
    )
from PyQt6.QtGui import QKeySequence,QShortcut
from PyQt6.QtCore import QPropertyAnimation, QObject,QSettings
def wrap_layout(layout: QLayout) -> QWidget:
    """
    Wrap any QLayout into a QWidget so it can be shown/hidden and animated.
    """
    container = QWidget()
    container.setContentsMargins(0, 0, 0, 0)     # helps stability
    container.setLayout(layout)
    return container
_QT_MAX = 16777215  # QWIDGETSIZE_MAX
class visibilityMgr(QObject):
    """
    Reusable manager for collapsible sections.
    - register() a section with a container widget or a layout (auto-wrapped)
    - auto create a QToolButton (or connect your own)
    - optional animation (height slide)
    - persists state in QSettings
    """
    toggled = QtCore.pyqtSignal(str, bool)  # name, visible
    
    def __init__(self, owner: QWidget, *,
                 settings_org="AbstractEndeavors",
                 settings_app="Visibility",
                 animate_default=False,
                 anim_duration_ms=160):
        super().__init__(owner)
        self._owner = owner
        self._sections = {}  # name -> dict
        self._settings = QSettings(settings_org, settings_app)
        self._animate_default = animate_default
        self._anim_ms = anim_duration_ms

    
    def set_visible(self, name: str, visible: bool):
        sec = self._sections.get(name)
        if not sec:
            return
        btn: QToolButton = sec["button"]
        if btn.isChecked() != visible:
            btn.setChecked(visible)  # this triggers toggle handler

    def is_visible(self, name: str) -> bool:
        sec = self._sections.get(name)
        return bool(sec and sec["button"].isChecked())

    def button(self, name: str) -> QToolButton | None:
        sec = self._sections.get(name)
        return sec["button"] if sec else None

    def container(self, name: str) -> QWidget | None:
        sec = self._sections.get(name)
        return sec["container"] if sec else None
    # ---- public API ----
    

    def register(self, *,
                 name: str,
                 container: QWidget | QLayout,
                 button: QToolButton | None = None,
                 start_visible: bool | None = None,
                 animate: bool | None = None,
                 shortcut: str | None = None,
                 button_host_layout: QLayout | None = None,
                 button_text_open: str = "−",
                 button_text_closed: str = "+",
                 persist: bool = True) -> QToolButton:
        """
        Flicker-free collapsible section:
        - Keep container visible; animate maximumHeight 0 <-> QWIDGETSIZE_MAX.
        - No owner.adjustSize() on toggle.
        - No sizeHint() measurement dependency.
        """
        # Wrap layouts
        if isinstance(container, QLayout):
            container = wrap_layout(container)

        # Button
        if button is None:
            button = QToolButton(self._owner)
            button.setCheckable(True)
            button.setAutoRaise(True)
            button.setToolTip(f"Toggle {name}")
            if button_host_layout is not None:
                button_host_layout.addWidget(button)

        key  = f"section/{name}/visible"
        anim = self._animate_default if animate is None else animate

        # Restore persisted state
        if start_visible is None:
            vis = self._settings.value(key, True, type=bool) if persist else True
        else:
            vis = bool(start_visible)

        # Always visible; we collapse by maxHeight=0
        container.setVisible(True)
        container.setMinimumHeight(0)
        container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # Initial height
        container.setMaximumHeight(_QT_MAX if vis else 0)

        animator = None
        if anim:
            animator = QPropertyAnimation(container, b"maximumHeight", self)
            animator.setDuration(self._anim_ms)
            animator.setEasingCurve(QtCore.QEasingCurve.Type.InOutCubic)

        # Button state/label
        button.setChecked(vis)
        button.setText(button_text_open if vis else button_text_closed)

        def _apply(checked: bool):
            button.setText(button_text_open if checked else button_text_closed)
            end_h = _QT_MAX if checked else 0

            if animator:
                start_h = container.maximumHeight()
                animator.stop()
                animator.setStartValue(start_h)
                animator.setEndValue(end_h)
                try:
                    animator.finished.disconnect()
                except TypeError:
                    pass
                animator.finished.connect(container.updateGeometry)
                animator.start()
            else:
                container.setMaximumHeight(end_h)
                container.updateGeometry()

            if persist:
                self._settings.setValue(key, checked)
            self.toggled.emit(name, checked)
            # DO NOT call self._owner.adjustSize() here — it causes flicker

        button.toggled.connect(_apply)

        if shortcut:
            QShortcut(QKeySequence(shortcut), self._owner, activated=lambda: button.toggle())

        self._sections[name] = dict(
            container=container, button=button, animator=animator,
            text_open=button_text_open, text_closed=button_text_closed,
            key=key, persist=persist, animate=anim
        )
        return button
