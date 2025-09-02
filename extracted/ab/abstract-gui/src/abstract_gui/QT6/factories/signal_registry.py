# signal_registry.py
from __future__ import annotations
from ..imports import Dict, List, Optional, Tuple, Iterable, Type, inspect, lru_cache, QtWidgets,QtCore
from .constants import INTERESTING_SUFFIXES,PRIORITY_ORDER,PRIORITY_INDEX,_CONSTRUCTOR_TRIES
# ---------- boilerplate ----------
def ensure_app():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    return app



def _rank(names: Iterable[str]) -> List[str]:
    names = list(dict.fromkeys(names))  # dedupe, keep order
    names.sort(key=lambda n: PRIORITY_INDEX.get(n, len(PRIORITY_ORDER)))
    return names


def _new_instance(cls: Type) -> Optional[object]:
    for args, kwargs in _CONSTRUCTOR_TRIES:
        try:
            return cls(*args, **kwargs)
        except Exception:
            continue
    return None

# ---------- discovery on an *instance* ----------
def _discover_signal_names(obj: object) -> List[str]:
    names: List[str] = []

    # A) Qt meta-object (reliable)
    try:
        mo = obj.metaObject()
        for i in range(mo.methodCount()):
            m = mo.method(i)
            mtype = m.methodType() if hasattr(m, "methodType") else m.methodType
            if mtype == QtCore.QMetaMethod.Signal:
                try:
                    n = bytes(m.name()).decode("utf-8")
                except Exception:
                    n = str(m.name())
                if n.endswith(INTERESTING_SUFFIXES):
                    names.append(n)
    except Exception:
        pass

    # B) Python attribute scan (useful in PyQt)
    pyqt_bound = getattr(QtCore, "pyqtBoundSignal", None)
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            attr = getattr(obj, name)
        except Exception:
            continue
        is_signal = (
            (pyqt_bound and isinstance(attr, pyqt_bound)) or
            (hasattr(attr, "connect") and hasattr(attr, "disconnect"))
        )
        if is_signal and name.endswith(INTERESTING_SUFFIXES):
            names.append(name)

    return _rank(names)

# ---------- per-class cached discovery ----------
@lru_cache(maxsize=None)
def build_registry_for_class(cls: Type) -> List[str]:
    ensure_app()
    # Skip non-QObject subclasses (layouts, etc.) early
    if not issubclass(cls, QtCore.QObject):
        return []
    obj = _new_instance(cls)
    if obj is None:
        return []
    return _discover_signal_names(obj)

# ---------- resolve for instance *or* class ----------
def resolve_signals(obj_or_cls) -> List[str]:
    cls = obj_or_cls if inspect.isclass(obj_or_cls) else type(obj_or_cls)
    return build_registry_for_class(cls)

# ---------- build a module-wide map, e.g., QtWidgets ----------
def derive_module_registry(module=QtWidgets, only_widgets=True) -> Dict[Type, List[str]]:
    ensure_app()
    out: Dict[Type, List[str]] = {}
    for name in dir(module):
        cls = getattr(module, name, None)
        if not inspect.isclass(cls):
            continue
        if only_widgets and not issubclass(cls, QtWidgets.QWidget):
            # QWidgetAction, QAction are QObject but not QWidget—include them if you want by setting only_widgets=False
            continue
        sigs = build_registry_for_class(cls)
        if sigs:
            out[cls] = sigs
    return out
