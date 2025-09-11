# safe_import_utils.py
import sys, importlib, os, inspect
from pathlib import Path

# --- tiny utils ---
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

def derive_package_for_file(file: str) -> tuple[str, Path]:
    """Return (pkg_name, sysroot) for the module file."""
    here = Path(file).resolve()
    top_pkg_dir = find_top_pkg_dir(here)
    if not top_pkg_dir:
        raise RuntimeError(f"No package context above {here}. Add __init__.py up the tree.")
    sysroot = top_pkg_dir.parent
    if str(sysroot) not in sys.path:
        sys.path.insert(0, str(sysroot))
    parts = here.with_suffix("").relative_to(sysroot).parts
    pkg_name = ".".join(parts[:-1])  # package of the module (drop the filename)
    return pkg_name, sysroot

def ensure_caller_package(caller_file: str, caller_globals: dict | None = None) -> str:
    """
    Ensure sysroot is on sys.path and return the caller's dotted package.
    Optionally set caller_globals['__package__'] when running as a script.
    """
    pkg, _ = derive_package_for_file(caller_file)
    if caller_globals and caller_globals.get("__name__") == "__main__" and not caller_globals.get("__package__"):
        caller_globals["__package__"] = pkg
    return pkg

# --- public API ---
def safe_import(
    name: str,
    *,
    member: str | None = None,
    package: str | None = None,
    file: str | None = None,
    caller_globals: dict | None = None,
):
    """
    Import `name` (relative or absolute).
    - If `name` is relative and `package` is missing, derive it from `file` (or caller).
    - If running the caller as a script, we can set its __package__ when caller_globals is provided.
    """
    if file is None:
        # best-effort: use the immediate caller's file
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
