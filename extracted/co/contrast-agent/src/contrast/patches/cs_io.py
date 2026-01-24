# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.agent.assess.policy import propagation_policy
from contrast.agent.assess.policy.source_policy import apply_stream_source
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy.propagators import STREAM_ACTIONS, stream_propagator
from contrast.agent.assess.utils import get_properties
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def build_and_patch_read_method(io_type, method_name):
    orig_func = getattr(io_type, method_name)
    if patch_manager.is_patched(orig_func):
        return

    propagation_method = STREAM_ACTIONS.get(method_name)

    def patched_func(wrapped, instance, args, kwargs):
        """
        This function has been optimized for performance. It looks similar to others in
        this module; however, do not attempt to deduplicate unless you're sure of the
        performance impact.
        """
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        with scope.propagation_scope():
            try:
                props = get_properties(instance)
                if props is not None and props.tags:
                    preshift = Preshift(instance, args, kwargs)
                    propagation_method(
                        method_name,
                        preshift,
                        result,
                        result,
                    )
                elif instance.cs__source:
                    apply_stream_source(
                        method_name, result, instance, result, args, kwargs
                    )
            except Exception as ex:
                _debug_log(method_name, ex)

        return result

    patch = wrap_and_watermark(orig_func, patched_func)
    patch_manager.patch(io_type, method_name, patch)


def build_and_patch_write_method(io_type, method_name):
    orig_func = getattr(io_type, method_name)
    if patch_manager.is_patched(orig_func):
        return

    def patched_func(wrapped, instance, args, kwargs):
        """
        This function has been optimized for performance. It looks similar to others in
        this module; however, do not attempt to deduplicate unless you're sure of the
        performance impact.
        """
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        with scope.propagation_scope():
            try:
                preshift = Preshift(instance, args, kwargs)
                stream_propagator.propagate_stream_write(
                    method_name, preshift, instance, result
                )
            except Exception as ex:
                _debug_log(method_name, ex)

        return result

    patch = wrap_and_watermark(orig_func, patched_func)
    patch_manager.patch(io_type, method_name, patch)


def build_and_patch_writelines(io_type, method_name):
    orig_func = getattr(io_type, method_name)
    if patch_manager.is_patched(orig_func):
        return

    def patched_func(wrapped, instance, args, kwargs):
        """
        This function has been optimized for performance. It looks similar to others in
        this module; however, do not attempt to deduplicate unless you're sure of the
        performance impact.
        """
        args_list = list(args[0:1]) + list(args[1:])

        result = wrapped(*args_list, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        with scope.propagation_scope():
            try:
                propagation_policy.propagate_stream(
                    method_name,
                    result,
                    instance,
                    result,
                    args_list,
                    kwargs,
                )
            except Exception as ex:
                _debug_log(method_name, ex)

        return result

    patch = wrap_and_watermark(orig_func, patched_func)
    patch_manager.patch(io_type, method_name, patch)


def _debug_log(method_name, ex):
    logger.debug("failed to propagate %s", method_name, exc_info=ex)


def patch_getvalue(io_module):
    build_and_patch_read_method(io_module.StringIO, "getvalue")
    build_and_patch_read_method(io_module.BytesIO, "getvalue")


def patch_io(io_module):
    """
    Apply patches to methods of builtin stream types
    """
    for io_type in [io_module.StringIO, io_module.BytesIO]:
        build_and_patch_write_method(io_type, "write")

    # No need to hook StringIO.writelines because it is implemented as str.join under
    # the hood, so we already propagate for free. Unfortunately this might make the
    # reporting look a little odd, so we maybe should consider another solution later.
    build_and_patch_writelines(io_module.BytesIO, "writelines")

    patch_getvalue(io_module)


def register_patches():
    register_module_patcher(patch_io, "io")


def reverse_patches():
    unregister_module_patcher("io")
    io_module = sys.modules.get("io")
    if not io_module:
        return

    patch_manager.reverse_patches_by_owner(io_module)
    patch_manager.reverse_patches_by_owner(io_module.BytesIO)
    patch_manager.reverse_patches_by_owner(io_module.StringIO)
