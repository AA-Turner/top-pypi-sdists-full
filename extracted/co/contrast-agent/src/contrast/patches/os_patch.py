# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import sys

from contrast.agent.scope import contrast_scope, pop_contrast_scope
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy.propagation_policy import propagate_string
from contrast_vendor import wrapt
from contrast.agent.assess.utils import get_properties
from contrast.utils.decorators import fail_quietly
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    get_arg,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)


class ContrastIteratorProxy(wrapt.ObjectProxy):
    def __init__(self, wrapped, path, _self_propagation_node):
        super().__init__(wrapped)

        try:
            # From os.fspath docs - If str or bytes is passed in, it is returned unchanged.
            # The point of this is to ensure we get a str/bytes object for the propagator.
            # path-like objects implement __fspath__ so we want the str/bytes value from that
            self._self_source_path = os.fspath(path)
        except TypeError:
            self._self_source_path = None

        self._self_propagation_node = _self_propagation_node

    def __enter__(self):
        self.__wrapped__.__enter__()
        return self

    def __iter__(self):
        return self

    @fail_quietly("Failed to propagate thru next iterator object")
    def _analyze_next(self, item):
        if item and self._self_source_path is not None:
            preshift = Preshift(None, [self._self_source_path], {})
            propagate_string(
                self._self_propagation_node,
                preshift,
                item.path,
                self.__wrapped__,
            )

    @contrast_scope()
    def __next__(self):
        item = None

        try:
            with pop_contrast_scope():
                item = self.__wrapped__.__next__()
        finally:
            self._analyze_next(item)
        return item


def build_os_scandir_hook(original_func, policy_node):
    """
    Builds patch for os.scandir(path="."). os.scandir returns an iterator of files/dir names based on the path argument
    """
    propagation_node = policy_node.propagator_nodes[0]

    @contrast_scope()
    def scandir_hook(wrapped, instance, args, kwargs):
        path = get_arg(args, kwargs, 0, "path")

        with pop_contrast_scope():
            dir_iter = wrapped(path)

        if get_properties(path) is None:
            return dir_iter

        dir_iter = ContrastIteratorProxy(dir_iter, path, propagation_node)

        return dir_iter

    return wrap_and_watermark(original_func, scandir_hook)


def patch_os(os_module):
    build_and_apply_patch(os_module, "scandir", build_os_scandir_hook)


def register_patches():
    register_module_patcher(patch_os, "os")


def reverse_patches():
    unregister_module_patcher("os")
    os_module = sys.modules.get("os")
    if not os_module:
        return

    patch_manager.reverse_patches_by_owner(os_module)
