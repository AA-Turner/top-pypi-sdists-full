from ...imports import *
from .nullProxy import nullProxy,nullProxy_logger
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
