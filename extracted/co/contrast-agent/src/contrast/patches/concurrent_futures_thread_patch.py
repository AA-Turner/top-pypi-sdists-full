# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contextlib import ExitStack

from contrast.agent.policy import patch_manager
from contrast.patches.threading_patch import (
    restore_parent_contrast_state,
    save_parent_contrast_state,
)
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

MODULE_TO_PATCH = "concurrent.futures.thread"
CLASS_TO_PATCH = "_WorkItem"

# NOTE: We need this patch in addition to those in `threading_patch`, even though the
# logic is largely identical. Workers can be long-lived and handle multiple WorkItems
# throughout their life. Scope and Context need to be set for every new task a worker
# handles; our threading patch only covers thread creation (which would only be correct
# for the first task handled by a worker thread).


def build__init__patch(orig_method, _):
    def work_item__init__patch(wrapped, instance, args, kwargs):
        ret = wrapped(*args, **kwargs)

        save_parent_contrast_state(instance)

        return ret

    return wrap_and_watermark(orig_method, work_item__init__patch)


def build_run_patch(orig_method, _):
    """
    This patch is executed in the worker thread. We need to reapply the context saved in
    _WorkItem.__init__
    """

    def work_item_run_patch(wrapped, instance, args, kwargs):
        with ExitStack() as stack:
            restore_parent_contrast_state(instance, stack)
            return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_method, work_item_run_patch)


def patch_concurrent_futures_thread(module):
    cls = getattr(module, CLASS_TO_PATCH, None)
    if cls is None:
        return

    build_and_apply_patch(cls, "__init__", build__init__patch)
    build_and_apply_patch(cls, "run", build_run_patch)


def register_patches():
    register_module_patcher(patch_concurrent_futures_thread, MODULE_TO_PATCH)


def reverse_patches():
    unregister_module_patcher(MODULE_TO_PATCH)
    module = sys.modules.get(MODULE_TO_PATCH)
    if module is None:  # pragma: no cover
        return

    cls = getattr(module, CLASS_TO_PATCH)
    if cls is None:  # pragma: no cover
        return

    patch_manager.reverse_patches_by_owner(cls)
