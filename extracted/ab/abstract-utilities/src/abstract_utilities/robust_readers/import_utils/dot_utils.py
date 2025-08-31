from ...type_utils  import is_number,make_list
from .function_utils import *
from pathlib import Path
from typing import *
def get_dot_range(filepath=None,list_obj=None):
    imports = make_list(list_obj) or extract_imports(filepath)
    highest=0
    dots = [get_imp(fro) for fro in imports if fro]

    if dots:
        dots.sort()
        highest = dots[0]
    return highest
def dotted_from(file: Path, sysroot: Path) -> str:
    """
    Build dotted name from sysroot (directory *above* top package)
    e.g.  /repo/abstract_ide/consoles/launcherWindowTab/functions/core_utils.py
        sysroot=/repo  -> abstract_ide.consoles.launcherWindowTab.functions.core_utils
    """
    file = file.resolve()
    stem = file.with_suffix("")  # drop .py
    return ".".join(stem.relative_to(sysroot).parts)
def to_dotted_name(file_path: Path, top_package: str) -> str:
    """
    Convert .../abstract_ide/consoles/launcherWindowTab/functions/core_utils.py
    -> abstract_ide.consoles.launcherWindowTab.functions.core_utils
    """
    # find the index of the top_package in the path parts
    parts = file_path.resolve().parts
    i = None
    if is_number(top_package):
        i= int(top_package)
    if i is None:
        try:
            i = parts.index(top_package)
        except ValueError:
            raise RuntimeError(f"Cannot locate package '{top_package}' in {file_path}")
    rel_parts = parts[i:]  # from top_package onward
    if rel_parts[-1].endswith(".py"):
        rel_parts = list(rel_parts)
        rel_parts[-1] = rel_parts[-1][:-3]  # strip .py
    return ".".join(rel_parts)
def compute_dotted_and_sysroot(file_path: Path) -> Tuple[str, Path]:
    """
    If inside packages, build dotted name from the top package down.
    sysroot will be the directory *above* the top package.
    If not a package, we fall back to a repo-ish root guess (2 parents up).
    """
    file_path = file_path.resolve()
    stem = file_path.with_suffix("")  # drop .py

    top_pkg_dir = find_top_package_dir(file_path)
    if top_pkg_dir:
        sysroot = top_pkg_dir.parent
        dotted = ".".join(stem.relative_to(sysroot).parts)
        return dotted, sysroot

    # Fallback: not in a package tree — guess a root a couple levels up
    sysroot = file_path.parents[2]
    dotted = ".".join(stem.relative_to(sysroot).parts)
    return dotted, sysroot


