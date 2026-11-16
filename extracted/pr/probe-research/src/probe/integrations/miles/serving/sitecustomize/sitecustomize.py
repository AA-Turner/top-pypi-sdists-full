"""Probe's site hook in the processes Miles launches (`../launch.py` puts this folder first on PYTHONPATH; Python
finds it by this name): runs the next sitecustomize on the path, then waits for the modules `PROBE_MILES_SERVING`
names. Imports nothing from Probe until one loads; any error is logged once and the process runs without Probe."""

import os
import sys


def _probe_serving_site():
    here = os.path.dirname(os.path.abspath(__file__))
    # Off the path first: the next sitecustomize (and one that chains like `probe exec`'s) never finds this one again.
    sys.path[:] = [entry for entry in sys.path if os.path.abspath(entry or ".") != here]
    try:
        import importlib.machinery
        import importlib.util

        spec = importlib.machinery.PathFinder.find_spec("sitecustomize", sys.path)
        if spec is not None and spec.loader is not None:
            spec.loader.exec_module(importlib.util.module_from_spec(spec))
    except Exception:
        _warn("the image's own sitecustomize failed")
    try:
        targets = dict(pair.split("=", 1) for pair in os.environ.get("PROBE_MILES_SERVING", "").split(",") if "=" in pair)
        if targets:
            sys.meta_path.insert(0, _Watcher(targets))
    except Exception:
        _warn("its import watcher could not start")


class _Watcher:
    """Finds a target module through the other finders and installs Probe once it has run."""

    def __init__(self, targets):
        self.targets = targets

    def find_spec(self, name, path=None, target=None):
        kind = self.targets.get(name)
        if kind is None:
            return None
        for finder in sys.meta_path:
            find = getattr(finder, "find_spec", None)
            if finder is self or find is None:
                continue
            spec = find(name, path, target)
            if spec is not None:
                break
        else:
            return None
        if spec.loader is not None and hasattr(spec.loader, "exec_module"):
            spec.loader = _Loader(spec.loader, kind)
        return spec


class _Loader:
    def __init__(self, loader, kind):
        self._loader = loader
        self._kind = kind

    def __getattr__(self, name):
        return getattr(self._loader, name)

    def create_module(self, spec):
        return self._loader.create_module(spec)

    def exec_module(self, module):
        self._loader.exec_module(module)
        try:
            from probe.integrations.miles.serving import install

            install(self._kind, module)
        except Exception:
            _warn(f"it could not load for {module.__name__}")


_warned = []


def _warn(what):
    if not _warned:
        _warned.append(what)
        import logging

        logging.getLogger("probe.miles.serving").warning(
            "Probe's GPU readings are off in this process (%s); it runs without them", what, exc_info=True)


_probe_serving_site()
