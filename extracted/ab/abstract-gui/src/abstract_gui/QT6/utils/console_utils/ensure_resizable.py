from PyQt6.QtCore import Qt, QRect, QSize, QTimer
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QWidget, QMainWindow
# --- enum compatibility shim (PyQt5 & PyQt6) -------------------
from PyQt6.QtCore import Qt as _Qt6

def _screen_for_widget(win: QWidget):
    """Pick the screen that currently contains the window center (or the active screen)."""
    if win and win.isVisible():
        center = win.frameGeometry().center()
        scr = QGuiApplication.screenAt(center)
        if scr:
            return scr
    # Fallbacks
    if win.windowHandle() and win.windowHandle().screen():
        return win.windowHandle().screen()
    screens = QGuiApplication.screens()
    return screens[0] if screens else None

def cap_window_to_screen(win: QWidget, *, margin: int = 8, fraction: float = 1.0):
    """
    Ensure the window is not larger than its current screen.
    - margin: pixels to keep from the edges
    - fraction: use <= 1.0 (e.g., 0.95 for 95% of available area)
    """
    scr = _screen_for_widget(win)
    if not scr:
        return
    avail: QRect = scr.availableGeometry()
    max_w = max(100, int(avail.width()  * fraction) - margin*2)
    max_h = max(100, int(avail.height() * fraction) - margin*2)

    # Cap maximum size to screen; do NOT touch minimums here.
    win.setMaximumSize(QSize(max_w, max_h))

    # If current size is already over the cap, shrink to fit.
    cur = win.size()
    new_w = min(cur.width(),  max_w)
    new_h = min(cur.height(), max_h)
    if (new_w, new_h) != (cur.width(), cur.height()):
        win.resize(new_w, new_h)

    # Also keep the window inside the visible area if it overflows.
    fg = win.frameGeometry()
    x = min(max(avail.left()   + margin, fg.left()),  avail.right()  - new_w - margin)
    y = min(max(avail.top()    + margin, fg.top()),   avail.bottom() - new_h - margin)
    win.move(x, y)

def keep_capped_across_screen_changes(win: QWidget, *, margin: int = 8, fraction: float = 1.0):
    """
    Re-apply the cap when the window is shown, moved to another monitor,
    or when DPI/resolution changes.
    """
    # 1) After the initial show, apply once (frame metrics are known)
    def _after_show_apply():
        cap_window_to_screen(win, margin=margin, fraction=fraction)
    QTimer.singleShot(0, _after_show_apply)

    # 2) When the window switches screens (dragged between monitors)
    if win.windowHandle() is not None:
        win.windowHandle().screenChanged.connect(
            lambda _scr: cap_window_to_screen(win, margin=margin, fraction=fraction)
        )

    # 3) If the current screen’s geometry changes (resolution/DPI/taskbar)
    scr = _screen_for_widget(win)
    if scr:
        try:
            scr.geometryChanged.connect(lambda _=None: cap_window_to_screen(win, margin=margin, fraction=fraction))
            scr.availableGeometryChanged.connect(lambda _=None: cap_window_to_screen(win, margin=margin, fraction=fraction))
        except Exception:
            pass  # Older Qt versions may lack one of these signals

def QT_FLAG(enum_group: str, name: str):
    """
    Return the correct enum value for both PyQt6 and PyQt5.
    Example: QT_FLAG("WindowType", "Window")
    """
    try:
        return getattr(getattr(_Qt6, enum_group), name)      # PyQt6: Qt.WindowType.Window
    except Exception:
        from PyQt5.QtCore import Qt as _Qt5                  # fallback
        return getattr(_Qt5, name)                           # PyQt5: Qt.Window
def ensure_user_resizable(win: QWidget, *, initial_size=(1000, 750), min_size=(500, 350)):
    """Keeps your window freely resizable with expanding contents (short form)."""
    win.setWindowFlag(QT_FLAG("WindowType", "Window"), True)
    win.setMinimumSize(QSize(*min_size))
    win.resize(*initial_size)
