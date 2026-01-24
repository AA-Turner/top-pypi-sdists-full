# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contextvars import Context
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


def build_start_patch(orig_func, _):
    """
    Only used in python 3.13 and earlier.

    We store the parent thread's scope and request context on the thread object in
    `start` (which runs in the parent thread). Then, in `_bootstrap_inner`, we retrieve
    these values and set the corresponding contextvars in the child thread.

    In python 3.14, thread contextvar inheritance behavior was adjusted. 3.14+ uses
    different thread patching machinery.
    """

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
    """
    Only used in pythno 3.13 and earlier. See build_start_patch.
    """

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


def _set_contrast_contextvars(target_context: Context):
    """
    Set all contrast-relevant contextvars in the provided Context, taking their values
    from the current context. Overwrites them if they are already present in the
    provided context.
    """
    parent_scope = scope.current_scope()
    parent_context = contrast.REQUEST_CONTEXT.get()

    def set_vars():
        scope.set_scope(*parent_scope)
        contrast.REQUEST_CONTEXT.set(parent_context)

    target_context.run(set_vars)


def build_thread_init_patch(orig_func, _):
    """
    Only used in python 3.14 and later.

    Patch for threading.Thread.__init__. Executes in the parent thread. We need to make
    sure scope and request context are transferred to the child thread. This behavior is
    controlled by both sys.flags.thread_inherit_context and the `context` kwarg to this
    function.

    See https://docs.python.org/3.14/library/threading.html#threading.Thread.
    """

    def thread_init(wrapped, instance, args, kwargs):
        # `context` is kwarg-only. It defaults to None, so we don't need special
        # handling for the case where it is not provided at all.
        passed_context = kwargs.get("context")
        if passed_context is None:
            # sys.flags controls the behavior in this case
            if sys.flags.thread_inherit_context == 0:
                new_context = Context()
                _set_contrast_contextvars(new_context)
                kwargs["context"] = new_context
            # the `inherit_context != 0` case is a noop; contextvars are inherited
        else:
            _set_contrast_contextvars(passed_context)

        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, thread_init)


def patch_threading(threading_module):
    if sys.version_info[:2] <= (3, 13):
        # py313 this can be removed once we no longer need to support 3.13
        build_and_apply_patch(
            threading_module.Thread,
            "start",
            build_start_patch,
        )
        # This instruments the method that actually runs inside the system thread
        build_and_apply_patch(
            threading_module.Thread,
            "_bootstrap_inner",
            build_bootstrap_inner_patch,
        )
    else:
        build_and_apply_patch(
            threading_module.Thread, "__init__", build_thread_init_patch
        )


def register_patches():
    register_module_patcher(patch_threading, "threading")


def reverse_patches():
    unregister_module_patcher("threading")
    threading = sys.modules.get("threading")
    if not threading:
        return

    patch_manager.reverse_patches_by_owner(threading.Thread)
