# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


START_METHOD = "start"
BOOTSTRAP_METHOD = "_bootstrap_inner"


def build_start_patch(orig_func, _):
    def start(wrapped, instance, args, kwargs):
        context = contrast.REQUEST_CONTEXT.get()

        try:
            # Save the scope of the current active contextvars.Context to copy to the new thread
            instance.cs__parent_scope = scope.current_scope()
            instance.cs__parent_context = context
        except Exception:
            logger.exception("Failed to instrument thread start")

        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, start)


def build_bootstrap_inner_patch(orig_func, _):
    def _bootstrap_inner(wrapped, instance, args, kwargs):  # pragma: no cover
        # The new thread inherits the scope from the thread that created it
        try:
            scope.set_scope(*instance.cs__parent_scope)
        except Exception:
            logger.exception("Failed to initialize thread scope")

        with contrast.lifespan(instance.cs__parent_context):
            # Ensure child thread still runs with the same parent request context
            # even if the parent thread has already exited as long as
            # the parent thread is in request context.
            result = wrapped(*args, **kwargs)

        # We expect result to be None, but this is done for consistency/safety
        return result

    return wrap_and_watermark(orig_func, _bootstrap_inner)


def patch_threading(threading_module):
    build_and_apply_patch(threading_module.Thread, START_METHOD, build_start_patch)
    # This instruments the method that actually runs inside the system thread
    build_and_apply_patch(
        threading_module.Thread, BOOTSTRAP_METHOD, build_bootstrap_inner_patch
    )


def register_patches():
    register_module_patcher(patch_threading, "threading")


def reverse_patches():
    unregister_module_patcher("threading")
    threading = sys.modules.get("threading")
    if not threading:
        return

    patch_manager.reverse_patches_by_owner(threading.Thread)
