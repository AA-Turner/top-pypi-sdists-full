# abstract_utilities/dynimport.py
from __future__ import annotations
import importlib, sys, os
from functools import lru_cache
from typing import Any, Callable, Iterable, Optional
import inspect, sys
from importlib import import_module
from .type_utils import make_list
from .robust_readers import get_for_all_tabs,call_for_all_tabs
class _LazyAttr:
    """Lazy resolver proxy to avoid import-time cycles.
    First use triggers actual import & attribute lookup.
    """
    __slots__ = ("_mod", "_attr", "_candidates", "_resolved")

    def __init__(self, module: str, attr: str, candidates: Iterable[str]):
        self._mod = module
        self._attr = attr
        self._candidates = candidates or None#tuple(candidates)
        self._resolved: Optional[Any] = None

    def _resolve(self) -> Any:
        if self._resolved is None:
            self._resolved = _resolve_attr(self._mod, self._attr, self._candidates)
        return self._resolved

    def __call__(self, *a, **k):
        return self._resolve()(*a, **k)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._resolve(), name)

    def __repr__(self) -> str:
        return f"<LazyAttr unresolved {self._mod}:{self._attr}>"
def _resolve_lazy(obj):
    for attr in ("resolve", "load"):
        if hasattr(obj, attr):
            try:
                return getattr(obj, attr)()
            except Exception:
                pass
    try:
        return obj()  # some lazy wrappers are callable
    except Exception:
        return obj

def import_symbols(specs, into=None, alias_map=None, update_all=False):
    """
    specs: [{module: str, symbols: [str, ...]}, ...]
    into: dict-like namespace to receive names (defaults to globals() of *this* module)
    alias_map: optional {orig: alias}
    update_all: if True, appends inserted names into 'into["__all__"]'
    """
    ns = into if into is not None else globals()
    out = {}
    exported_names = []

    for spec in specs:
        mod_name = spec["module"]
        names = spec["symbols"]
        try:
            mod = import_module(mod_name)
        except Exception:
            mod = None

        for sym in names:
            obj = getattr(mod, sym) if (mod and hasattr(mod, sym)) else get_abstract_import(module=mod_name, symbol=sym)
            obj = _resolve_lazy(obj)
            alias = alias_map.get(sym, sym) if alias_map else sym
            ns[alias] = obj
            out[alias] = obj
            exported_names.append(alias)

    if update_all:
        all_list = ns.get("__all__")
        if all_list is None:
            ns["__all__"] = exported_names[:]
        else:
            for n in exported_names:
                if n not in all_list:
                    all_list.append(n)

    return out
def import_symbols_to_parent(specs, *, levels_up=1, alias_map=None, update_all=False):
    """
    Inject into the caller's module namespace (parent frame by default).
    levels_up=1 => direct caller; raise it if you wrap this again.
    """
    frame = inspect.currentframe()
    for _ in range(levels_up):
        frame = frame.f_back
        if frame is None:
            raise RuntimeError("No parent frame available")
    parent_globals = frame.f_globals
    return import_symbols(specs, into=parent_globals, alias_map=alias_map, update_all=update_all)

def import_symbols_into_module(module_name: str, specs, *, alias_map=None, update_all=False):
    """
    Inject into an explicit module by name (e.g., package __init__).
    """
    if module_name not in sys.modules:
        raise KeyError(f"Module not loaded: {module_name}")
    target_ns = sys.modules[module_name].__dict__
    return import_symbols(specs, into=target_ns, alias_map=alias_map, update_all=update_all)
@lru_cache(maxsize=256)
def _resolve_attr(module: str, attr: str, candidates: Iterable[str]) -> Any:
    """Try module, then module + each candidate suffix for re-export patterns."""
    # 1) Try the module as-is
    candidates =candidates or tuple()
    mod = importlib.import_module(module)
    if hasattr(mod, attr):
        return getattr(mod, attr)

    # 2) Try dotted attribute lookup (e.g., attr="sub.mod:name" or "sub.name")
    if ":" in attr:
        left, right = attr.split(":", 1)
        submod = importlib.import_module(f"{module}.{left}")
        for part in right.split("."):
            submod = getattr(submod, part)
        return submod
    if "." in attr:
        obj = mod
        for part in attr.split("."):
            obj = getattr(obj, part)
        return obj

    # 3) Try common subpackages where APIs are often parked
    for suffix in candidates:
        try:
            sub = importlib.import_module(module + suffix)
        except Exception:
            continue
        if hasattr(sub, attr):
            return getattr(sub, attr)

    # 4) As a last resort, attempt an import that mimics "from pkg import name"
    #    by reloading after the import graph settles (helps with partial init).
    if module in sys.modules:
        try:
            mod = importlib.reload(sys.modules[module])
            if hasattr(mod, attr):
                return getattr(mod, attr)
        except Exception:
            pass

    raise ImportError(
        f"Could not resolve {attr!r} from {module!r}. "
        f"Tried direct, dotted, and suffixes: {list(candidates)}"
    )

def get_abstract_import(
    module: str,
    symbol: Optional[str] = None,
    *,
    lazy: bool = True,
    candidates: Iterable[str] = None,
    **kwargs: Any,
) -> Any:
    """Dynamic import helper that can return a lazy proxy to dodge cycles.

    Examples:
        get_abstract_import('abstract_gui', symbol='get_for_all_tabs')
        get_abstract_import(**{'module':'abstract_gui','import':'get_for_all_tabs'})
        get_abstract_import('abstract_gui', 'SIMPLEGUI:get_for_all_tabs')   # aliases
        get_abstract_import('abstract_gui', 'SIMPLEGUI.get_for_all_tabs')   # dotted
    """
    # Allow the exact call style the user wants: import='name'
    if symbol is None and 'import' in kwargs:
        symbol = kwargs['import']
    if not symbol:
        raise TypeError("get_abstract_import requires a 'symbol' (or pass import='...').")
    if lazy:
        return _LazyAttr(module, symbol, candidates)
    return _resolve_attr(module, symbol, candidates)
def get_many_module_imports(*args):
    all_modules = {}
    for arg in args:
        module = arg.get("module")
        symbols = make_list(arg.get("symbols"))
        for symbol in symbols:
            all_modules[symbol] = get_abstract_import(module = module,symbol=symbol)
    import_symbols(all_modules)
    return all_modules
def get_caller_path():
    frame = inspect.stack()[1]
    return os.path.abspath(frame.filename)
def get_caller_dir():
    frame = inspect.stack()[1]
    abspath = os.path.abspath(frame.filename)
    return os.path.dirname(abspath)
def call_for_all_tabs():
    
    root = get_caller_dir()
    get_for_all_tabs(root)
