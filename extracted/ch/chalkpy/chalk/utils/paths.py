from __future__ import annotations

import inspect
import os
from pathlib import Path
from typing import List, Optional


def get_classpath(x: object) -> Path | None:
    module = inspect.getmodule(x)
    if module is None:
        return
    filepath = getattr(module, "__file__", None)
    if filepath is None:
        return
    return Path(os.path.abspath(filepath))


def get_classpath_or_name(x: object) -> str | None:
    classpath = get_classpath(x)
    if classpath is not None:
        return str(classpath)
    return getattr(x, "__module__", None)


def get_directory_root() -> Optional[Path]:
    current = Path(os.path.dirname(os.path.abspath("dummy.txt")))
    while True:
        if any((current / f).exists() for f in ("chalk.yaml", "chalk.yml")):
            return current
        if Path(os.path.dirname(current)) == current:
            # This is '/'
            return None
        current = current.parent


def search_recursively_for_file(base: Path, filename: str) -> List[Path]:
    ans = []
    assert base.is_dir()
    while True:
        filepath = base / filename
        if filepath.exists():
            ans.append(filepath)
        parent = base.parent
        if parent == base:
            return ans
        base = parent
