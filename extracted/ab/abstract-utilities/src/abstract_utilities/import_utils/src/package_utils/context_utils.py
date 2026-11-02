import sys, os
from pathlib import Path
from .path_utils import find_top_package_dir, derive_package_for_file

def ensure_package_context(file: str):
    """Ensure that running this file directly gives correct package context."""
    file = file or os.getcwd()
    here = Path(file).resolve()
    top_pkg_dir = find_top_package_dir(here)
    if not top_pkg_dir:
        raise RuntimeError(f"No package context above {here}. Add __init__.py files up the tree.")

    sysroot = top_pkg_dir.parent
    if str(sysroot) not in sys.path:
        sys.path.insert(0, str(sysroot))

    parts = here.with_suffix("").relative_to(sysroot).parts
    pkg_name = ".".join(parts[:-1])
    if (__name__ == "__main__") and not globals().get("__package__"):
        globals()["__package__"] = pkg_name

def ensure_caller_package(caller_file: str, caller_globals: dict | None = None) -> str:
    """Ensure sysroot is on sys.path and return caller's dotted package name."""
    pkg, _ = derive_package_for_file(caller_file)
    if caller_globals and caller_globals.get("__name__") == "__main__" and not caller_globals.get("__package__"):
        caller_globals["__package__"] = pkg
    return pkg
