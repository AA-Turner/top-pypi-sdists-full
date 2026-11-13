# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import importlib.abc
import importlib.util
import sys
from typing import TYPE_CHECKING

import contrast
from contrast.agent import scope
from contrast.agent.inventory.library_reader import observe_library
from contrast.applies.assess import unsafe_code_execution
from contrast_vendor.wrapt import importer as wrapt_importer

if TYPE_CHECKING:
    from types import ModuleType

    from contrast.reporting.fireball import Client


def register_path_finder() -> ContrastMetaPathFinder:
    """
    Add the ContrastMetaPathFinder to the sys.meta_path if it is not already present,
    and return it.
    """
    for path_finder in sys.meta_path:
        if isinstance(path_finder, ContrastMetaPathFinder):
            return path_finder
    path_finder = ContrastMetaPathFinder()
    sys.meta_path.insert(0, path_finder)
    return path_finder


def remove_path_finder():
    """
    Remove the ContrastMetaPathFinder from the sys.meta_path if it is present.
    """
    for path_finder in sys.meta_path:
        if isinstance(path_finder, ContrastMetaPathFinder):
            sys.meta_path.remove(path_finder)


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.in_progress = {}
        # None until library discovery has been reported, since Fireball drops
        # observations of libraries that haven't been discovered yet. Stays None if
        # library analysis is disabled.
        self.fireball_client: Client | None = None

    def enable_library_observations(self, fireball_client: Client) -> None:
        self.fireball_client = fireball_client

    def find_spec(self, fullname, path, target=None):
        if fullname in self.in_progress:
            return None
        self.in_progress[fullname] = True
        try:
            analyze_for_unsafe_code_execution(fullname)

            spec = importlib.util.find_spec(fullname)
            if spec is None:
                return None

            loader = getattr(spec, "loader", None)
            if loader and not isinstance(loader, _ContrastImportHookChainedLoader):
                spec.loader = _ContrastImportHookChainedLoader(loader, self)

            return spec
        finally:
            del self.in_progress[fullname]


def analyze_for_unsafe_code_execution(module_name: str):
    if scope.in_contrast_scope():
        return
    with scope.contrast_scope():
        context = contrast.CONTEXT.get()
        if context and context.assess_enabled:
            unsafe_code_execution.apply_rule(
                "importlib", "__import__", None, (module_name,), {}
            )


class _ContrastImportHookChainedLoader(wrapt_importer._ImportHookChainedLoader):
    def __init__(self, loader, path_finder: ContrastMetaPathFinder) -> None:
        super().__init__(loader)
        self._self_path_finder = path_finder

    @scope.contrast_scope()
    @scope.observe_scope()  # don't report file-open-create for imported source files
    def _self_exec_module(self, module: ModuleType) -> None:
        try:
            with scope.pop_contrast_scope():
                return super()._self_exec_module(module)
        finally:
            if fireball_client := self._self_path_finder.fireball_client:
                observe_library(fireball_client, module)
