#!/usr/bin/env python3
# Timestamp: 2026-03-13
# File: scitex_dev/app/__init__.py

"""App SDK — write-once interface for local + cloud SciTeX apps.

Usage (standalone):
    from scitex_dev.app import get_files

    files = get_files("./my_project")
    content = files.read("recipes/my_recipe.yaml")
    files.write("output/result.png", png_bytes)

Usage (cloud, auto-detected via SCITEX_API_TOKEN):
    files = get_files()  # routes through Platform REST API
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

from ._protocol import FilesBackend

# Backend registry: name -> factory callable
_registry: Dict[str, Callable[..., FilesBackend]] = {}


def register_backend(name: str, factory: Callable[..., FilesBackend]) -> None:
    """Register a files backend factory.

    Parameters
    ----------
    name : str
        Backend identifier (e.g., "cloud", "s3").
    factory : callable
        Callable(root, **kwargs) -> FilesBackend instance.
    """
    _registry[name] = factory


def get_files(
    root: Optional[Union[str, Path]] = None,
    *,
    backend: Optional[str] = None,
    **kwargs: Any,
) -> FilesBackend:
    """Get a files backend instance.

    Auto-detection logic:
    1. If ``backend`` is specified, use that.
    2. If ``SCITEX_API_TOKEN`` env var is set and "cloud" backend
       is registered, use cloud.
    3. Otherwise, use filesystem (default).

    Parameters
    ----------
    root : str or Path, optional
        Root directory for filesystem backend. Defaults to cwd.
    backend : str, optional
        Explicit backend name. If None, auto-detected.

    Returns
    -------
    FilesBackend
        A backend instance.

    Raises
    ------
    KeyError
        If the requested backend is not registered.
    """
    if backend:
        if backend not in _registry:
            raise KeyError(
                f"Backend {backend!r} not registered. "
                f"Available: {list(_registry.keys())}"
            )
        return _registry[backend](root, **kwargs)

    if os.environ.get("SCITEX_API_TOKEN") and "cloud" in _registry:
        return _registry["cloud"](root, **kwargs)

    from ._filesystem import FileSystemBackend

    return FileSystemBackend(root or Path.cwd())


__all__ = [
    "FilesBackend",
    "get_files",
    "register_backend",
]

# EOF
