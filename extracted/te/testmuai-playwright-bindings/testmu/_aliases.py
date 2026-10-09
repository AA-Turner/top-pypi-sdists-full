"""Old private module paths keep working after the v3/v4 split.

Before the split every module lived at ``testmu.<name>``. The v4
implementation now lives at ``testmu._v4.<name>``, but code outside this
package imports the old paths and patches module globals through them. That
includes exported tests (``from testmu._step import ...``), host runtimes that
run generated code in-process, and their test suites.

So each old path is an alias: importing ``testmu._vars`` (or any submodule,
``testmu._helpers.devtools_network``) returns the SAME module object as
``testmu._v4._vars``. Same object means shared state, and ``setattr`` /
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

PACKAGE = "testmu"
TARGET = "testmu._v4"

# Top-level names that moved into testmu._v4 (frozen; never add new ones).
ALIASED = frozenset({
    "_action_engine", "_action_specs", "_capability", "_decorator",
    "_devtools_capture", "_downloads_path", "_heal_cascade", "_heal_patch",
    "_helpers", "_matchers", "_ranked_locator", "_relay_proxy", "_reporter",
    "_route_failure", "_session", "_step_variables", "_test_config", "_vars",
    "_vision_locator", "playwright_async",
})


def target_of(fullname: str) -> str | None:
    """``testmu._helpers.x`` -> ``testmu._v4._helpers.x``; None if not aliased."""
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
    """``testmu.__getattr__``: ``testmu._vars`` as an attribute (without an
    import statement first) resolves to the aliased module, as it did when
    ``testmu/__init__`` imported every module itself."""
    if name in ALIASED:
        return importlib.import_module(f"{PACKAGE}.{name}")
    raise AttributeError(f"module {PACKAGE!r} has no attribute {name!r}")
