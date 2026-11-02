# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)


def build_noop_patch(original_func, patch_policy):
    del patch_policy

    def noop_intern(wrapped, instance, args, kwargs):
        """
        Defeat interning by returning the original string

        sys.intern takes no kwargs
        """
        del wrapped, instance, kwargs

        return args[0]

    return wrap_and_watermark(original_func, noop_intern)


def patch_sys(module):
    build_and_apply_patch(module, "intern", build_noop_patch)


def register_patches():
    register_module_patcher(patch_sys, "sys")


def reverse_patches():
    unregister_module_patcher("sys")
    # sys is always imported, no need to check
    patch_manager.reverse_patches_by_owner(sys)
