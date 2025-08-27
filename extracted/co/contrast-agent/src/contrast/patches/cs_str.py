# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
This module contains core instrumentation for patching builtin methods.

These are the "pure python string patches" that are applied to strlike types using
set_attr_on_type. They are called directly when the relevant strlike method is called -
our C extension is not called first to dispatch to them.
"""

import _io
from collections import UserString
import contrast
from contrast.agent import scope
from contrast.agent.assess.utils import is_tracked
from contrast.agent.policy import patch_manager, registry
from contrast.agent.assess.policy.propagation_policy import (
    PROPAGATOR_ACTIONS,
    propagate_stream,
    track_copy_without_new_event,
)
from contrast.agent.assess.policy.propagators import FormatPropagator, JoinPropagator
from contrast.agent.assess.policy.preshift import Preshift
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark
from contrast.assess_extensions import smart_setattr


from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def build_bytearray_join_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]

    def bytearray_join_patch(wrapped, instance, args, kwargs):
        # Since we need to make reference to the input multiple times, convert the
        # first argument to a list and use that instead. This prevents any iterators
        # from being exhausted before we can make use of them in propagation.
        # For bytearray.join, args == (list_or_iterator_of_things_to_join,...)
        # Note that this is different from the C hooks for other join methods. In
        # those cases, the PyObject *args argument corresponds to just the list or
        # iterator itself, in contrast to a tuple that contains that list or
        # iterator. (Got that straight?)
        if scope.in_contrast_or_propagation_scope():
            return wrapped(*args, **kwargs)

        args_list = [list(args[0])] + list(args[1:])
        result = wrapped(*args_list, **kwargs)

        with scope.contrast_scope():
            try:
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, args_list, kwargs)
                propagator = JoinPropagator(node, preshift, result)
                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagated()
            except Exception as ex:
                logger.debug("failed to propagate bytearray.join", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, bytearray_join_patch)


def build_strtype_join_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]

    def strtype_join_patch(wrapped, instance, args, kwargs):
        if scope.in_contrast_or_propagation_scope():
            return wrapped(*args, **kwargs)

        args_list = list(args[0])

        with scope.propagation_scope():
            result = wrapped(args_list, **kwargs)

        with scope.contrast_scope():
            try:
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, (args_list,), kwargs)
                propagator = JoinPropagator(node, preshift, result)
                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagated()
            except Exception as ex:
                logger.debug("failed to propagate join", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, strtype_join_patch)


def build_str_format_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]

    def str_format_patch(wrapped, instance, args, kwargs):
        """
        Propagation hook for str.format

        This hook is a special case because we need to enable some propagation to occur
        while we evaluate whether to propagate this particular event. With the current
        general hook infrastructure, this is not possible, so we need to account for it
        here. Eventually it may be possible to fit this back into the more general
        infrastructure if we overhaul the way that scope works.
        """
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        try:
            with scope.contrast_scope():
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, args, kwargs)
                propagator = FormatPropagator(node, preshift, result)

            # This evaluation must not occur in scope. This is what enables us
            # to perform any conversions from object to __str__ or __repr__,
            # while allowing propagation to occur through those methods if
            # necessary.
            if propagator.needs_propagation:
                with scope.contrast_scope():
                    propagator.track_and_propagate(result)
                    context.propagated()
        except Exception as ex:
            with scope.propagation_scope():
                logger.debug("failed to propagate str.format", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, str_format_patch)


def build_str_formatmap_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]

    def str_formatmap_patch(wrapped, instance, args, kwargs):
        """
        Propagation hook for str.format_map

        This hook is a special case because we need to enable some propagation to occur
        while we evaluate whether to propagate this particular event. With the current
        general hook infrastructure, this is not possible, so we need to account for it
        here. Eventually it may be possible to fit this back into the more general
        infrastructure if we overhaul the way that scope works.
        """
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope() or not args:
            return result

        try:
            with scope.contrast_scope():
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, (), args[0])
                propagator = FormatPropagator(node, preshift, result)

            # This evaluation must not occur in scope. This is what enables us
            # to perform any conversions from object to __str__ or __repr__,
            # while allowing propagation to occur through those methods if
            # necessary.
            if propagator.needs_propagation:
                with scope.contrast_scope():
                    propagator.track_and_propagate(result)
                    context.propagated()
        except Exception as ex:
            with scope.propagation_scope():
                logger.debug("failed to propagate str.format", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, str_formatmap_patch)


def build_generic_strtype_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]
    propagator_class = PROPAGATOR_ACTIONS.get(node.action)

    def str_patch(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)

        # This special case does not apply to bytearrays
        if result is instance:
            return result

        if scope.in_contrast_or_propagation_scope():
            return result

        with scope.contrast_scope():
            try:
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, args, kwargs)
                propagator = propagator_class(node, preshift, result)

                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagated()
            except Exception as ex:
                name = orig_method.__class__.__name__
                logger.debug(
                    "failed to propagate %s.%s", name, orig_method.__name__, exc_info=ex
                )

        return result

    return wrap_and_watermark(orig_method, str_patch)


def build_track_without_new_event_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]
    propagator_class = PROPAGATOR_ACTIONS.get(node.action)

    def str_patch(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        # This special case applies to all bytearray methods and all .translate methods
        if result == instance:
            track_copy_without_new_event(result, instance)
            return result

        with scope.contrast_scope():
            try:
                if (
                    context := contrast.REQUEST_CONTEXT.get()
                ) is None or context.stop_propagation:
                    return result

                preshift = Preshift(instance, args, kwargs)
                propagator = propagator_class(node, preshift, result)

                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagated()
            except Exception as ex:
                name = orig_method.__class__.__name__
                logger.debug(
                    "failed to propagate %s.%s", name, orig_method.__name__, exc_info=ex
                )

        return result

    return wrap_and_watermark(orig_method, str_patch)


def build_generic_stream_patch(orig_method, patch_policy):
    del patch_policy
    method_name = orig_method.__name__

    def stream_patch(wrapped, instance, args, kwargs):
        result = wrapped(*args, **kwargs)

        if scope.in_contrast_or_propagation_scope():
            return result

        if not (
            getattr(instance, "cs__tracked", False)
            or getattr(instance, "cs__source", False)
        ):
            return result

        if is_tracked(result):
            return result

        with scope.propagation_scope(), scope.contrast_scope():
            if (
                context := contrast.REQUEST_CONTEXT.get()
            ) is None or context.stop_propagation:
                return result

            propagate_stream(method_name, result, instance, result, args, kwargs)
            context.propagated()

        return result

    return wrap_and_watermark(orig_method, stream_patch)


def build_and_apply_str_patch(owner, method_name, patch_builder):
    orig_method = getattr(owner, method_name)

    policy_method_name = (
        "formatmap" if orig_method.__name__ == "format_map" else orig_method.__name__
    )

    patch_policy = registry.get_policy_by_name("builtins.str." + policy_method_name)
    patch = patch_builder(orig_method, patch_policy)

    patch_manager.patch(owner, method_name, patch)


def property_getter(self):
    return contrast.STRING_TRACKER.get(self, None)


def property_setter(self, value):
    contrast.STRING_TRACKER.update_properties(self, value)


def enable_str_properties():
    strprop = property(fget=property_getter, fset=property_setter)

    smart_setattr(str, "cs__properties", strprop)
    smart_setattr(bytes, "cs__properties", strprop)
    smart_setattr(bytearray, "cs__properties", strprop)

    for stream_type in (_io.StringIO, _io.BytesIO):
        smart_setattr(stream_type, "cs__tracked", False)
        smart_setattr(stream_type, "cs__source", False)
        smart_setattr(stream_type, "cs__properties", None)
        smart_setattr(stream_type, "cs__source_event", None)
        smart_setattr(stream_type, "cs__source_type", None)
        smart_setattr(stream_type, "cs__source_tags", None)

    # IPython assumes that UserString has the same attributes as str,
    # and raises AttributeErrors if that is not the case. So any
    # properties we add to str should also be added to UserString.
    # UserString will dispatch to str methods on self.data though, so
    # we don't need to actually add a strprop onto the type.
    smart_setattr(UserString, "cs__properties", None)


def patch_strtype_method(strtype, method_name):
    if patch_manager.is_patched(getattr(strtype, method_name)):
        return

    if method_name == "join":
        builder = (
            build_bytearray_join_patch
            if strtype is bytearray
            else build_strtype_join_patch
        )
    elif method_name == "format":
        builder = build_str_format_patch
    elif method_name == "format_map":
        builder = build_str_formatmap_patch
    elif method_name == "translate" and strtype is str:
        builder = build_track_without_new_event_patch
    else:
        builder = (
            build_track_without_new_event_patch
            if strtype is bytearray
            else build_generic_strtype_patch
        )

    build_and_apply_str_patch(strtype, method_name, patch_builder=builder)


def patch_stream_method(stream_type, method_name):
    build_and_apply_patch(stream_type, method_name, build_generic_stream_patch)


def unpatch_strtype_and_stream_methods():
    """
    Replace all patched strtype and stream methods with the original implementation.

    NOTE: repeatedly enabling and disabling these patches in the same python process can
    cause tp_version_tag to reach its maximum allowed value in the interpreter. This
    shouldn't be an issue, but it has been known to cause problems in the past. Minimize
    the use of this function.
    """
    patch_manager.reverse_patches_by_owner(str)
    patch_manager.reverse_patches_by_owner(bytes)
    patch_manager.reverse_patches_by_owner(bytearray)

    patch_manager.reverse_patches_by_owner(_io.StringIO)
    patch_manager.reverse_patches_by_owner(_io.BytesIO)
    patch_manager.reverse_patches_by_owner(_io._IOBase)

    patch_manager.reverse_patches_by_owner(UserString)
