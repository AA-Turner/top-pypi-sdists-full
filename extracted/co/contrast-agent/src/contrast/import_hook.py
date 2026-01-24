# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib.abc
import importlib.util

import sys
from types import ModuleType

import contrast
from contrast.agent import scope
from contrast.agent.settings import Settings
from contrast.applies.assess import unsafe_code_execution
from contrast_vendor.wrapt.importer import _ImportHookChainedLoader


def register_path_finder():
    """
    Add the ContrastMetaPathFinder to the sys.meta_path if it is not already present.
    """
    if not any(
        isinstance(path_finder, ContrastMetaPathFinder) for path_finder in sys.meta_path
    ):
        sys.meta_path.insert(0, ContrastMetaPathFinder())


def remove_path_finder():
    """
    Remove the ContrastMetaPathFinder from the sys.meta_path if it is present.
    """
    for path_finder in sys.meta_path:
        if isinstance(path_finder, ContrastMetaPathFinder):
            sys.meta_path.remove(path_finder)
            break


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.in_progress = {}

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
                spec.loader = _ContrastImportHookChainedLoader(loader)

            return spec
        finally:
            del self.in_progress[fullname]


def analyze_for_unsafe_code_execution(module_name: str):
    if scope.in_contrast_scope():
        return
    with scope.contrast_scope():
        context = contrast.REQUEST_CONTEXT.get()
        if context and context.assess_enabled:
            unsafe_code_execution.apply_rule(
                "importlib", "__import__", None, (module_name,), {}
            )


class _ContrastImportHookChainedLoader(_ImportHookChainedLoader):
    @scope.contrast_scope()
    @scope.observe_scope()  # don't report file-open-create for imported source files
    def _self_exec_module(self, module: ModuleType) -> None:
        in_scope = False
        try:
            with scope.pop_contrast_scope():
                in_scope = scope.in_contrast_scope()
                return super()._self_exec_module(module)
        finally:
            if (
                not in_scope
                and Settings().is_inventory_enabled()
                and (context := contrast.REQUEST_CONTEXT.get()) is not None
            ):
                context.observed_libraries.add_module(module)
