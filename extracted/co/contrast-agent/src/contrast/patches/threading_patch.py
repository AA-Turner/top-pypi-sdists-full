# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contextlib import ExitStack
from contextvars import Context

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


def save_parent_contrast_state(instance):
    """
    Save the current thread's scope and context onto `instance`, so that they can later
    be restored via `restore_parent_contrast_state`.
    """
    try:
        instance.cs__parent_scope = scope.current_scope()
        instance.cs__parent_context = contrast.CONTEXT.get()
        instance.cs__parent_web_context = contrast.WEB_CONTEXT.get()
    except Exception:
        logger.exception("Failed to save contrast state")


def restore_parent_contrast_state(instance, stack):
    """
    Restore the scope and context previously saved onto `instance` by
    `save_parent_contrast_state`.
    """
    try:
        parent_scope = getattr(instance, "cs__parent_scope", None)
        if parent_scope is not None:
            scope.set_scope(*parent_scope)
    except Exception:
        logger.exception("Failed to restore scope")

    try:
        parent_context = getattr(instance, "cs__parent_context", None)
        if parent_context is not None:
            stack.enter_context(parent_context.set_contextvar())
    except Exception:
        logger.exception("Failed to restore ContrastContext")

    try:
        parent_web_context = getattr(instance, "cs__parent_web_context", None)
        if parent_web_context is not None:
            stack.enter_context(parent_web_context.set_contextvar())
    except Exception:
        logger.exception("Failed to restore WebContext")


def build_start_patch(orig_func, _):
    """
    Only used in python 3.13 and earlier.

    We store the parent thread's scope, ContrastContext, and WebContext on the thread
    object in `start` (which runs in the parent thread). Then, in `_bootstrap_inner`, we
    retrieve these values and set the corresponding contextvars in the child thread.

    In python 3.14, thread contextvar inheritance behavior was adjusted. 3.14+ uses
    different thread patching machinery.
    """

    def start(wrapped, instance, args, kwargs):
        save_parent_contrast_state(instance)
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, start)


def build_bootstrap_inner_patch(orig_func, _):
    """
    Only used in python 3.13 and earlier. See build_start_patch.
    """

    def _bootstrap_inner(wrapped, instance, args, kwargs):  # pragma: no cover
        with ExitStack() as stack:
            restore_parent_contrast_state(instance, stack)
            return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, _bootstrap_inner)


def _set_contrast_contextvars(target_context: Context):
    """
    Set all contrast-relevant contextvars in the provided Context, taking their values
    from the current context. Overwrites them if they are already present in the
    provided context.
    """
    parent_scope = scope.current_scope()
    parent_context = contrast.CONTEXT.get()
    parent_web_context = contrast.WEB_CONTEXT.get()

    def set_vars():
        scope.set_scope(*parent_scope)
        # The target context may be a copy of the parent's, which would carry the
        # parent's shield scope along with it. Clear scope so that child calls don't
        # place the parent in CVE scope.
        scope.SHIELD_SCOPE.set(None)
        contrast.CONTEXT.set(parent_context)
        contrast.WEB_CONTEXT.set(parent_web_context)

    target_context.run(set_vars)


def build_thread_init_patch(orig_func, _):
    """
    Only used in python 3.14 and later.

    Patch for threading.Thread.__init__. Executes in the parent thread. We need to make
    sure scope, ContrastContext, and WebContext are transferred to the child thread.
    This behavior is controlled by both sys.flags.thread_inherit_context and the
    `context` kwarg to this function.

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
            # the `inherit_context != 0` case is handled by build_thread_start_patch
        else:
            _set_contrast_contextvars(passed_context)

        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, thread_init)


def build_thread_start_patch(orig_func, _):
    """
    Only used in python 3.14 and later, when sys.flags.thread_inherit_context is set.

    If no context was passed to Thread.__init__, Thread.start copies the caller's
    context for the child thread. That copy would share the parent's mutable shield
    scope, so we clear the shield scope in the parent while start makes the copy. Other
    contextvars are still captured as of the call to start.
    """

    def start(wrapped, instance, args, kwargs):
        token = scope.SHIELD_SCOPE.set(None)
        try:
            return wrapped(*args, **kwargs)
        finally:
            scope.SHIELD_SCOPE.reset(token)

    return wrap_and_watermark(orig_func, start)


def _call_without_shield_scope(func, /, *args, **kwargs):
    scope.SHIELD_SCOPE.set(None)
    return func(*args, **kwargs)


def build_to_thread_patch(orig_func, _):
    """
    asyncio.to_thread runs `func` in a shallow copy of the caller's context, so the
    thread would otherwise share the caller's mutable shield scope. We have `func` clear
    the shield scope in the copy before it runs.
    """

    async def to_thread(wrapped, instance, args, kwargs):
        if not args:
            return await wrapped(*args, **kwargs)
        func, *rest = args
        return await wrapped(_call_without_shield_scope, func, *rest, **kwargs)

    return wrap_and_watermark(orig_func, to_thread)


def patch_asyncio_to_thread(asyncio_threads_module):
    build_and_apply_patch(asyncio_threads_module, "to_thread", build_to_thread_patch)


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
        if sys.flags.thread_inherit_context:
            build_and_apply_patch(
                threading_module.Thread, "start", build_thread_start_patch
            )


def register_patches():
    register_module_patcher(patch_threading, "threading")
    register_module_patcher(patch_asyncio_to_thread, "asyncio.threads")


def reverse_patches():
    unregister_module_patcher("threading")
    unregister_module_patcher("asyncio")
    unregister_module_patcher("asyncio.threads")
    for name in ("asyncio", "asyncio.threads"):
        if module := sys.modules.get(name):
            patch_manager.reverse_patches_by_owner(module)

    threading = sys.modules.get("threading")
    if not threading:
        return

    patch_manager.reverse_patches_by_owner(threading.Thread)
