"""Run a wrap the moment a module first loads in this process (now, when it already has): what an RL adapter's Ray
setup hook calls in every worker. The finder looks at one module name and imports nothing itself, so an inference or
reward worker never pays for torch. Fails open."""

from __future__ import annotations

import importlib.abc
import importlib.util
import logging
import sys
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def watch_import(module_name: str, install: Callable[[Any], Any], *, framework: str) -> None:
    """``install(module)`` once ``module_name`` has run here; ``framework`` names who continues when it fails."""
    module = sys.modules.get(module_name)
    if module is not None:
        _install(install, module, framework)
        return
    if not any(isinstance(finder, ImportWatch) and finder.module_name == module_name and finder.install == install
               for finder in sys.meta_path):  # fmt: skip
        sys.meta_path.insert(0, ImportWatch(module_name, install, framework))


def _install(install: Callable[[Any], Any], module: Any, framework: str) -> None:
    try:
        install(module)
    except Exception as exc:  # noqa: BLE001 -- fail open: the module runs unwatched
        logger.warning("Probe could not watch %s; %s continues: %s", getattr(module, "__name__", module), framework, exc)


class ImportWatch(importlib.abc.MetaPathFinder):
    """Finds nothing itself: for the one module it hands back the real spec with a loader that runs the wrap."""

    def __init__(self, module_name: str, install: Callable[[Any], Any], framework: str) -> None:
        self.module_name = module_name
        self.install = install
        self.framework = framework
        self._busy = threading.local()

    def find_spec(self, fullname: str, path: Any, target: Any = None) -> Any:
        if fullname != self.module_name or getattr(self._busy, "active", False):
            return None
        self._busy.active = True
        try:
            spec = importlib.util.find_spec(fullname)
        except Exception:  # noqa: BLE001 -- Python's own import goes on, unwatched
            return None
        finally:
            self._busy.active = False
        if spec is None or spec.loader is None or not hasattr(spec.loader, "exec_module"):
            return None
        spec.loader = _WrappingLoader(spec.loader, self)
        return spec


class _WrappingLoader(importlib.abc.Loader):
    def __init__(self, loader: Any, watch: ImportWatch) -> None:
        self._loader = loader
        self._watch = watch

    def create_module(self, spec: Any) -> Any:
        return self._loader.create_module(spec)

    def exec_module(self, module: Any) -> None:
        self._loader.exec_module(module)
        _install(self._watch.install, module, self._watch.framework)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._loader, name)
