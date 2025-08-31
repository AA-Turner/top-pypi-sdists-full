# --- auto-package bootstrap (run-safe) ---------------------------------
import sys, importlib,os

from pathlib import Path
from ...string_clean import eatAll
from .dot_utils import get_dot_range
from .sysroot_utils import get_sysroot
def get_module_from_import(imp,path=None):
    path = path or os.getcwd()
    i = get_dot_range(None,[imp])
    imp = eatAll(imp,'.')
    sysroot = get_sysroot(path,i)
    return os.path.join(sysroot, imp)
def find_top_pkg_dir(p: Path) -> Path | None:
    p = p.resolve()
    if p.is_file():
        p = p.parent
    top = None
    while (p / "__init__.py").exists():
        top = p
        if p.parent == p:
            break
        p = p.parent
    return top
def ensure_package_context(file: str):
    """
    Ensure that running this file directly still gives it the correct package.
    Sets sys.path and __package__ based on the __init__.py chain.
    """
    file = file or os.getcwd()
    here = Path(file).resolve()
    top_pkg_dir = find_top_pkg_dir(here)
    if not top_pkg_dir:
        raise RuntimeError(f"No package context above {here}. Add __init__.py files up the tree.")

    sysroot = top_pkg_dir.parent  # dir ABOVE the top package (e.g., .../src)
    if str(sysroot) not in sys.path:
        sys.path.insert(0, str(sysroot))

    # Compute this module's package (exclude the filename)
    parts = here.with_suffix("").relative_to(sysroot).parts
    pkg_name = ".".join(parts[:-1])  # e.g. abstract_ide.consoles.launcherWindowTab

    # When run as a script, __package__ is empty -> set it
    if (__name__ == "__main__") and (not globals().get("__package__")):
        globals()["__package__"] = pkg_name


def safe_import(name: str, *, package: str | None = None, member: str | None = None, file: str | None = None):
    """
    Wrapper over importlib.import_module that:
    - if `name` is relative (starts with '.'), ensures `package` is set.
    - if `package` is missing, derives it from `file` (defaults to __file__).
    """
    file = file or __file__
    ensure_package_context(file)
    if name.startswith(".") and not package:
        
            
        pkg_name = get_module_from_import(name,path=None)
        # also set __package__ if we are running as a script
        if __name__ == "__main__" and (not globals().get("__package__")):
            globals()["__package__"] = pkg_name
        package = pkg_name

    mod = importlib.import_module(name, package=package)
    return getattr(mod, member) if member else mod



