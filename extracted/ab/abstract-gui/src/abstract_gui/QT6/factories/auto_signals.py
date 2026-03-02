# auto_signals.py
from typing import *
import inspect
from abstract_utilities import make_list
from .constants import PRIORITY_INDEX,PRIORITY_ORDER, _CONSTRUCTOR_TRIES
from .signal_registry import derive_module_registry
# --- cross-backend detection (PyQt5, PyQt6, PySide2/6) -----------------
_PYQT_BOUND_TYPE = None
_PYSIDE_SIGNAL_TYPE = None
_QMETA_METHOD = None
_QMETA_METHOD_SIGNAL = None

def _load_qt_types():
    global _PYQT_BOUND_TYPE, _PYSIDE_SIGNAL_TYPE, _QMETA_METHOD, _QMETA_METHOD_SIGNAL
    # Try PyQt6/PyQt5
    for mod in ("PyQt6.QtCore", "PyQt5.QtCore"):
        try:
            m = __import__(mod, fromlist=['pyqtBoundSignal', 'QMetaMethod'])
            if hasattr(m, "pyqtBoundSignal"):
                _PYQT_BOUND_TYPE = getattr(m, "pyqtBoundSignal")
            if hasattr(m, "QMetaMethod"):
                _QMETA_METHOD = getattr(m, "QMetaMethod")
                # PyQt6: QMetaMethod.MethodType.Signal; PyQt5: QMetaMethod.Signal
                _QMETA_METHOD_SIGNAL = getattr(_QMETA_METHOD, "MethodType", _QMETA_METHOD).Signal
            break
        except Exception:
            pass
    # Try PySide2/6
    for mod in ("PySide6.QtCore", "PySide2.QtCore"):
        try:
            m = __import__(mod, fromlist=['SignalInstance', 'QMetaMethod'])
            if hasattr(m, "SignalInstance"):
                _PYSIDE_SIGNAL_TYPE = getattr(m, "SignalInstance")
            if _QMETA_METHOD is None and hasattr(m, "QMetaMethod"):
                _QMETA_METHOD = getattr(m, "QMetaMethod")
                _QMETA_METHOD_SIGNAL = _QMETA_METHOD.MethodType.Signal
            break
        except Exception:
            pass

_load_qt_types()

# --- discovery ----------------------------------------------------------

def discover_signal_attrs(widget: Any) -> Dict[str, Any]:
    """
    Find signal attributes by scanning Python attributes.
    Works across PyQt5/6 and PySide (most cases).
    """
    sigs: Dict[str, Any] = {}
    for name in dir(widget):
        # skip dunders and private-ish names
        if name.startswith("_"):
            continue
        try:
            attr = getattr(widget, name)
        except Exception:
            continue
        # PyQt: pyqtBoundSignal; PySide: SignalInstance
        if (_PYQT_BOUND_TYPE and isinstance(attr, _PYQT_BOUND_TYPE)) or \
           (_PYSIDE_SIGNAL_TYPE and isinstance(attr, _PYSIDE_SIGNAL_TYPE)):
            sigs[name] = attr
            continue
        # Heuristic: a Qt signal-like object usually has a connect method
        if hasattr(attr, "connect") and hasattr(attr, "disconnect"):
            # narrow down to common names
            if any(name.endswith(suf) for suf in ("Changed", "Pressed", "Clicked", "Triggered", "Activated", "Released", "Toggled", "Moved")):
                sigs[name] = attr
    return sigs

def discover_signal_names_via_meta(widget: Any) -> List[str]:
    """
    Fallback using the Qt meta-object system. Returns *method names* of signals.
    These names typically match the Python attribute names you can getattr().
    """
    names: List[str] = []
    try:
        mo = widget.metaObject()
    except Exception:
        return names
    # iterate methods; keep only signals
    count = mo.methodCount()
    for i in range(count):
        m = mo.method(i)
        try:
            mtype = m.methodType()
        except Exception:
            # PyQt5 compatibility
            mtype = m.methodType
        if mtype == _QMETA_METHOD_SIGNAL:
            try:
                n = bytes(m.name()).decode("utf-8")  # PyQt returns QByteArray
            except Exception:
                n = str(m.name())
            if n and n not in names:
                names.append(n)
    return names

def rank_signals(names: List[str]) -> List[str]:
    """
    Prefer 'Changed' then common user interactions, then the rest.
    """

    return sorted(names, key=lambda n: PRIORITY_INDEX.get(n, len(PRIORITY_ORDER)))

def auto_signals(widget: Any) -> List[str]:
    """
    Unified entry: get a ranked list of available signal names for this widget.
    """
    # 1) attribute-based
    by_attr = set(discover_signal_attrs(widget).keys())
    # 2) meta-object fallback (union)
    by_meta = set(discover_signal_names_via_meta(widget))
    names = list(by_attr | by_meta)
    return rank_signals(names)

def default_signals(widget: Any):
    cls = type(widget)
    SIGNAL_REGISTRY = derive_module_registry(module=cls, only_widgets=True)
    if SIGNAL_REGISTRY:
        return SIGNAL_REGISTRY
    return auto_signals(widget)

# --- generic connector ---------------------------------------------------

def connect_signals_depriciated(
    widget: Any,
    callbacks: Callable | List[Callable],
    signals: Optional[List[str]] = None,
    *,
    allow_missing: bool = True
) -> List[Tuple[str, Callable]]:
    """
    Connect callbacks to discovered (or provided) signal names on widget.
    If you pass multiple callbacks, they map 1:1 by index; extra signals reuse the last callback.
    """
    if signals is None:
        signals = default_signals(widget)
    if not signals:
        return []

    if not isinstance(callbacks, (list, tuple)):
        callbacks = [callbacks]
    cbs: List[Callable] = list(callbacks)
    connected: List[Tuple[str, Callable]] = []
    signals = make_list(signals) or []
    for i, sig_name in enumerate(signals):
        try:
            sig = getattr(widget, sig_name, None)
        except Exception:
            sig = None
        if sig is None:
            if allow_missing:
                continue
            raise AttributeError(f"{type(widget).__name__} has no signal '{sig_name}'")

        cb = cbs[i] if i < len(cbs) else cbs[-1]
        try:
            sig.connect(cb)
            connected.append((sig_name, cb))
        except Exception:
            if not allow_missing:
                raise
            # Skip incompatible overloads etc.
            continue

    return connected
def connect_signals(
    widget: Any,
    callbacks: Callable | List[Callable],
    signals: Optional[List[str]] = None,
    *,
    allow_missing: bool = True,
    prepend_widget: bool = False,
) -> List[Tuple[str, Callable]]:
    """
    Connect callbacks to signals by name.
    If prepend_widget=True, your callback will be called as callback(widget, *args).
    """
    if signals is None:
        signals = default_signals(widget)
    if not isinstance(callbacks, (list, tuple)):
        callbacks = [callbacks]
    cbs: List[Callable] = list(callbacks)

    connected: List[Tuple[str, Callable]] = []
    for i, name in enumerate(make_list(signals) or []):
        sig = getattr(widget, name, None)
        if sig is None or not hasattr(sig, "connect"):
            if allow_missing:
                continue
            raise AttributeError(f"{type(widget).__name__} has no signal '{name}'")

        cb = cbs[i] if i < len(cbs) else cbs[-1]
        if prepend_widget:
            cb = partial(cb, widget)  # <-- THIS ensures your slot sees the widget first
        try:
            sig.connect(cb)
            connected.append((name, cb))
        except Exception:
            if not allow_missing:
                raise
            continue
    return connected

