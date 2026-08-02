r"""Contain path utilities."""

from __future__ import annotations

__all__ = ["find_root_package_parent"]


from typing import TYPE_CHECKING

from coola.utils.path import sanitize_path

if TYPE_CHECKING:
    from pathlib import Path


def find_root_package_parent(start_path: str | Path) -> Path:
    """Given a file or directory path, walk upward through directories
    that contain __init__.py (i.e., are part of a package) and return
    the parent directory of the outermost (root) package.

    Example:
        my_project/
            pkg/
                __init__.py
                sub/
                    __init__.py
                    module.py

        find_root_package_parent(".../pkg/sub/module.py")
        -> Path(".../my_project")

    Args:
        start_path: Path to a file or directory inside the package.

    Returns:
        Absolute Path to the parent directory of the root package.
        If start_path itself is not part of a package (no __init__.py
        in its directory), its own directory is returned.
    """
    path = sanitize_path(start_path)

    # If it's a file, start from its containing directory
    if path.is_file():
        path = path.parent

    current = path
    while True:
        parent = current.parent
        init_file = current / "__init__.py"

        if not init_file.is_file():
            # 'current' is not a package -> the last package's parent was the root's parent
            return current

        if parent == current:
            # Reached filesystem root without leaving a package
            return current

        current = parent
