"""Invocation-scoped imports of authored Python files and their sibling modules."""

import importlib
import sys
from pathlib import Path
from types import ModuleType

import click


class SourceModule:
    """Keep importable source names alive through publication, then restore host imports."""

    def __init__(self, filename: str) -> None:
        """Resolve an explicit Python file without executing its contents."""
        self.path = Path(filename).resolve()
        if self.path.suffix != ".py" or not self.path.is_file() or not self.path.stem.isidentifier():
            raise click.UsageError(f"Expected an importable Python file: {filename}")
        self.root = self.path.parent
        self.name = self.path.stem
        while (self.root / "__init__.py").is_file():
            self.name = self.root.name + "." + self.name
            self.root = self.root.parent
        self._modules = dict(sys.modules)
        self._path = list(sys.path)

    def load(self) -> ModuleType:
        """Import trusted authored code with sibling imports available until context cleanup."""
        existing = sys.modules.get(self.name)
        if existing is not None and Path(str(getattr(existing, "__file__", ""))).resolve() != self.path:
            raise click.UsageError(f"Module name {self.name!r} is already in use; rename the source file.")
        sys.path.insert(0, str(self.root))
        importlib.invalidate_caches()
        return importlib.import_module(self.name)

    def close(self) -> None:
        """Remove only invocation-owned source imports and restore the prior search path."""
        for name, module in tuple(sys.modules.items()):
            filename = getattr(module, "__file__", None)
            if name not in self._modules and filename and Path(filename).resolve().is_relative_to(self.root):
                sys.modules.pop(name, None)
        sys.path[:] = self._path
