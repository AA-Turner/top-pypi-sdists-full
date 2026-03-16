from ...imports import *
from .nullProxy import nullProxy,nullProxy_logger
from ..import_utils import inject_from_imports_map,get_imports
import importlib,importlib.util, pkgutil,sys
from pathlib import Path


def dynamic_import(target: str | Path):
    """
    Import module/package/file dynamically.
    Returns module or nullProxy if unavailable.
    """
    try:
        p = Path(target)

        # file import
        if p.exists():
            name = f"_dyn_{p.stem}_{hash(p)}"

            spec = importlib.util.spec_from_file_location(name, str(p))
            if spec is None or spec.loader is None:
                raise ImportError(target)

            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)

            return mod

        # module import
        return importlib.import_module(target)

    except Exception:
        return nullProxy(str(target))
def safe_attr(obj, attr):
    try:
        return getattr(obj, attr)
    except Exception:
        return nullProxy(f"{obj}.{attr}")
@lru_cache(maxsize=None)
def lazy_import_single(name: str,fallback=None):
    """
    Import module safely. If unavailable, return NullProxy.
    """

    if name in sys.modules:
        return sys.modules[name]

    try:
        module = importlib.import_module(name)
        return module
    except Exception as e:
        nullProxy_logger.warning(
            "[lazy_import] Failed to import '%s': %s",
            name,
            e,
        )
        return nullProxy(name,fallback=fallback)

def get_lazy_attr(module_name: str, *attrs,fallback=None):
    obj = lazy_import(module_name,fallback=fallback)

    for attr in attrs:
        try:
            obj = getattr(obj, attr)
        except Exception:
            return nullProxy(module_name, attrs,fallback=fallback)

    return obj
def lazy_import(name: str, *attrs,fallback=None):
    """
    Import module safely. If unavailable, return NullProxy.
    """
    if attrs:
        obj = get_lazy_attr(name, *attrs,fallback=fallback)
    else:
        obj = lazy_import_single(name,fallback=fallback)
    return obj
def lazy_import_star(files, *, self=None):
    imports_map = get_imports(files)

    return inject_from_imports_map(
        imports_map,
        into=globals(),
        self=self
    )
def lazy_import_star(targets, *, into=None, self=None):
    """
    Supports:
    - module names
    - packages
    - filesystem paths
    """

    import importlib
    import pkgutil
    from pathlib import Path

    ns = into or globals()

    for target in targets:

        # ----------------------------
        # MODULE / PACKAGE IMPORT
        # ----------------------------
        try:
            mod = importlib.import_module(target)

            if hasattr(mod, "__path__"):
                # package → import all submodules
                for _, name, _ in pkgutil.iter_modules(mod.__path__):
                    sub = importlib.import_module(f"{mod.__name__}.{name}")
                    ns[name] = sub
            else:
                # single module
                ns[target.split(".")[-1]] = mod

            continue

        except Exception:
            pass

        # ----------------------------
        # FILESYSTEM IMPORT
        # ----------------------------
        p = Path(target)

        if p.exists():
            imports_map = get_imports([str(p)])
            inject_from_imports_map(imports_map, self=self)

        else:
            nullProxy_logger.warning(f"[lazy_import] Could not import {target}")
