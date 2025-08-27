# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

import contrast
from contrast.agent.scope import current_scope, set_scope

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

MODULE_TO_PATCH = "concurrent.futures.thread"
CLASS_TO_PATCH = "_WorkItem"


def build__init__patch(orig_method, _):
    """
    This patch is executed when a new _WorkItem object is created. After this happens it is put on a thread safe queue.
    Worker threads in the ThreadPoolExecutor class deque and execute the call back function contained in this object.
    We attach our request context on object creation since the thread this function is running on is the same
    thread that initially served the request.
    """

    def work_item__init__patch(wrapped, instance, args, kwargs):
        ret = wrapped(*args, **kwargs)

        # Save the scope of the current thread to copy to the thread running the route function
        instance.cs__parent_scope = current_scope()
        instance.cs__parent_context = contrast.REQUEST_CONTEXT.get()

        return ret

    return wrap_and_watermark(orig_method, work_item__init__patch)


def build_run_patch(orig_method, _):
    """
    This patch is executed in the worker thread. We need to reapply the context saved in _WorkItem.__init__
    """

    def work_item_run_patch(wrapped, instance, args, kwargs):
        with contrast.lifespan(instance.cs__parent_context):
            set_scope(*instance.cs__parent_scope)

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
