"""Old module paths keep working after the runtime-mode split.

Before the split every module lived at ``testmu_appium.<name>``. The v4
implementation now lives at ``testmu_appium._v4.<name>``, but code outside
this package imports the old paths and patches module globals through them
(host runtimes that run generated code in-process, their test suites), and
``testmu_appium.perception`` is a public module.

So each old path is an alias: importing ``testmu_appium._vars`` (or any
submodule, ``testmu_appium._helpers._tree``) returns the SAME module object as
``testmu_appium._v4._vars``. Same object means shared state, and ``setattr`` /
``mock.patch`` through the old path lands on the real module. Old paths always
mean v4: they are bound at import time, before ``configure(kane_version=...)``
picks a mode.

The table is frozen: it lists the top-level names that existed before the
split. Modules added under ``_v4/`` or ``_v3/`` later get no old path.
"""
from __future__ import annotations

import importlib
import importlib.abc
import importlib.util
import sys

PACKAGE = "testmu_appium"
TARGET = "testmu_appium._v4"

# Top-level names that moved into testmu_appium._v4 (frozen; never add new ones).
ALIASED = frozenset({
    "_action_click", "_action_drag", "_action_engine", "_action_scroll",
    "_action_scroll_until", "_action_select", "_action_type", "_action_web",
    "_decorator", "_evaluation", "_heal", "_helpers", "_reporter",
    "_route_failure", "_session", "_test_config", "_timing", "_vars",
    "perception"
})


def target_of(fullname: str) -> str | None:
    """``testmu_appium._helpers.x`` -> ``testmu_appium._v4._helpers.x``; None if not aliased."""
    prefix = PACKAGE + "."
    if not fullname.startswith(prefix):
        return None
    rest = fullname[len(prefix):]
    if rest.split(".", 1)[0] not in ALIASED:
        return None
    return f"{TARGET}.{rest}"


class _AliasLoader(importlib.abc.Loader):
    def __init__(self, target: str):
        self.target = target

    def create_module(self, spec):
        return None  # a placeholder; exec_module swaps in the real module

    def exec_module(self, module):
        # The import system re-reads sys.modules after exec, so the caller (and
        # the parent package's attribute) get the real module, not the placeholder.
        sys.modules[module.__name__] = importlib.import_module(self.target)


class _AliasFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        real = target_of(fullname)
        if real is None:
            return None
        return importlib.util.spec_from_loader(fullname, _AliasLoader(real))


def install() -> None:
    """Put the alias finder first on sys.meta_path (idempotent)."""
    if not any(isinstance(f, _AliasFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, _AliasFinder())


def package_getattr(name: str):
    """``testmu_appium.__getattr__``: ``testmu_appium._vars`` as an attribute
    (without an import statement first) resolves to the aliased module, as it
    did when ``testmu_appium/__init__`` imported every module itself."""
    if name in ALIASED:
        return importlib.import_module(f"{PACKAGE}.{name}")
    raise AttributeError(f"module {PACKAGE!r} has no attribute {name!r}")
