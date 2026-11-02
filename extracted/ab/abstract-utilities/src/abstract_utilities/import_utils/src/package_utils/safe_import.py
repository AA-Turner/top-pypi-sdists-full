import inspect, importlib
from .context_utils import ensure_caller_package

def safe_import(
    name: str,
    *,
    member: str | None = None,
    package: str | None = None,
    file: str | None = None,
    caller_globals: dict | None = None,
):
    """
    Safe dynamic import that resolves relative imports when run as a script.
    """
    if file is None:
        frame = inspect.currentframe()
        assert frame is not None
        outer = frame.f_back
        caller_file = (outer.f_globals.get("__file__") if outer else None) or __file__
    else:
        caller_file = file

    if name.startswith(".") and not package:
        package = ensure_caller_package(caller_file, caller_globals=caller_globals)

    mod = importlib.import_module(name, package=package)
    return getattr(mod, member) if member else mod
