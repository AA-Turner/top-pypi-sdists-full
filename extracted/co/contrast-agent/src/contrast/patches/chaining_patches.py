# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

"""
This module contains patches to support chaining Contrast instrumentation
with other tools, such as opentelemetry and DataDog's runner commands.
"""

from functools import partial
import os
from contrast.agent.scope import contrast_scope
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    wrap_and_watermark,
)


def register_patches():
    register_module_patcher(
        partial(
            build_and_apply_patch, attr_name="execl", patch_builder=build_os_execl_hook
        ),
        "os",
    )


def build_os_execl_hook(original_func, policy_node):
    loader_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "loader")

    @contrast_scope()
    def hook(wrapped, instance, args, kwargs):
        if (path := os.environ.get("PYTHONPATH")) and not path.startswith(loader_path):
            os.environ["PYTHONPATH"] = loader_path + os.path.pathsep + path

        return wrapped(*args, **kwargs)

    return wrap_and_watermark(original_func, hook)
