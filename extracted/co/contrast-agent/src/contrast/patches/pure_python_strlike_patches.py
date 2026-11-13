# Copyright © 2026 Contrast Security, Inc.
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
from contrast.agent.assess.adjusted_span import AdjustedSpan
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.propagation_policy import (
    PROPAGATOR_ACTIONS,
    propagate_stream,
    stop_propagation,
    track_copy_without_new_event,
)
from contrast.agent.assess.policy.propagators import FormatPropagator, JoinPropagator
from contrast.agent.assess.policy.source_policy import get_parents
from contrast.agent.assess.utils import (
    copy_tags_to_offset,
    get_properties,
    is_tracked,
    track_string,
)
from contrast.agent.policy import constants, patch_manager, registry
from contrast.extensions import smart_setattr
from contrast.utils.patch_utils import build_and_apply_patch, wrap_and_watermark
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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
                    return result

                preshift = Preshift(instance, args_list, kwargs)
                propagator = JoinPropagator(node, preshift, result)
                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagation_count += 1
            except Exception as ex:
                logger.debug("failed to propagate bytearray.join", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, bytearray_join_patch)


def propagate_bytearray_append(
    policy_node, target, source, pre_append_len, self_obj, ret, args, kwargs
):
    with scope.contrast_scope():
        try:
            if (context := contrast.CONTEXT.get()) is None or stop_propagation(context):
                return

            if source is None:
                return

            source_properties = get_properties(source)
            if source_properties is not None and source_properties.tags:
                target_properties = track_string(target)
                if target_properties is not None:
                    copy_tags_to_offset(
                        target_properties, source_properties.tags, pre_append_len
                    )

            target_properties = get_properties(target)
            if target_properties is not None and target_properties.tags:
                parents = get_parents(policy_node, self_obj, ret, args, kwargs)
                target_properties.build_event(
                    policy_node,
                    target,
                    self_obj,
                    ret,
                    args,
                    kwargs,
                    parents,
                    None,
                )
                context.propagation_count += 1
        except Exception as ex:
            logger.debug("failed to propagate bytearray append", exc_info=ex)


def build_bytearray_extend_patch(orig_method, patch_policy):
    policy_node = patch_policy.propagator_nodes[0]

    def bytearray_extend_patch(wrapped, instance, args, kwargs):
        if scope.in_contrast_or_propagation_scope():
            return wrapped(*args, **kwargs)

        pre_extend_len = len(instance)
        source = args[0] if args else None

        result = wrapped(*args, **kwargs)

        propagate_bytearray_append(
            policy_node,
            instance,
            source,
            pre_extend_len,
            instance,
            result,
            args,
            kwargs,
        )

        return result

    return wrap_and_watermark(orig_method, bytearray_extend_patch)


def build_bytearray_take_bytes_patch(orig_method, patch_policy):
    """
    bytearray.take_bytes(n) removes the first `n` bytes (slice semantics: None means
    all, negative counts from the end) from the bytearray and returns them as a new
    bytes object; `self` is mutated in place to hold the remainder.

    This needs two separate propagations against the same pre-call state, each with its
    own event since they represent different flows (O2R vs O2O):
      1. The returned head bytes inherit tags from the corresponding range of the
         original (pre-mutation) content, and get a new O2R (object-to-return) event.
      2. `self`'s own remaining tags need to be re-indexed to account for the removed
         prefix, since the tags on `instance` don't move automatically when its
         underlying buffer is mutated; `self` also gets its own new O2O
         (object-to-object) event, since this mutation is a distinct propagation step
         from whatever produced its prior tags.

    Neither of the generic SLICE (read-only, no self-mutation) or REMOVE (mutation-free,
    returns a new object) propagators handle this shape, so this is a dedicated patch
    rather than a PROPAGATOR_ACTIONS dispatch, following the same pattern as
    build_bytearray_extend_patch.
    """
    node_o2r = PropagationNode(
        "builtins",
        "bytearray",
        True,
        "take_bytes",
        source=constants.OBJECT,
        target=constants.RETURN,
        action="NONE",
        policy_patch=False,
    )
    node_o2o = PropagationNode(
        "builtins",
        "bytearray",
        True,
        "take_bytes",
        source=constants.OBJECT,
        target=constants.OBJECT,
        action="NONE",
        policy_patch=False,
    )

    def bytearray_take_bytes_patch(wrapped, instance, args, kwargs):
        if scope.in_contrast_or_propagation_scope():
            return wrapped(*args, **kwargs)

        pre_len = len(instance)
        source_properties = get_properties(instance)

        result = wrapped(*args, **kwargs)

        with scope.contrast_scope():
            try:
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
                    return result

                if source_properties is None or not source_properties.tags:
                    return result

                n = args[0] if args else None
                _, stop, _ = slice(None, n).indices(pre_len)
                head_range = AdjustedSpan(0, stop)

                # Both new events share the same parents, taken from the pre-mutation
                # state of `instance` (the event, if any, that produced the tags we're
                # propagating here). Both node_o2r and node_o2o share the same source
                # (OBJ), so either can be used to compute them.
                parents = get_parents(node_o2r, instance, result, args, kwargs)

                head_tags = source_properties.tags_at_range(head_range)
                if head_tags:
                    target_properties = track_string(result)
                    if target_properties is not None:
                        copy_tags_to_offset(target_properties, head_tags, 0)
                        target_properties.build_event(
                            node_o2r,
                            result,
                            instance,
                            result,
                            args,
                            kwargs,
                            parents,
                            None,
                        )

                # Removes tags in [0, stop) from self and shifts the remaining tags
                # left by `stop`, matching self's new (mutated) content.
                source_properties.delete_tags_at_ranges([head_range])
                source_properties.build_event(
                    node_o2o, instance, instance, result, args, kwargs, parents, None
                )

                context.propagation_count += 1
            except Exception as ex:
                logger.debug("failed to propagate bytearray.take_bytes", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, bytearray_take_bytes_patch)


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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
                    return result

                preshift = Preshift(instance, (args_list,), kwargs)
                propagator = JoinPropagator(node, preshift, result)
                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagation_count += 1
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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
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
                    context.propagation_count += 1
        except Exception as ex:
            with scope.propagation_scope():
                logger.debug("failed to propagate str.format", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, str_format_patch)


def build_str_format_map_patch(orig_method, patch_policy):
    node = patch_policy.propagator_nodes[0]

    def str_format_map_patch(wrapped, instance, args, kwargs):
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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
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
                    context.propagation_count += 1
        except Exception as ex:
            with scope.propagation_scope():
                logger.debug("failed to propagate str.format_map", exc_info=ex)

        return result

    return wrap_and_watermark(orig_method, str_format_map_patch)


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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
                    return result

                preshift = Preshift(instance, args, kwargs)
                propagator = propagator_class(node, preshift, result)

                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagation_count += 1
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
                if (context := contrast.CONTEXT.get()) is None or stop_propagation(
                    context
                ):
                    return result

                preshift = Preshift(instance, args, kwargs)
                propagator = propagator_class(node, preshift, result)

                if propagator.needs_propagation:
                    propagator.track_and_propagate(result)
                    context.propagation_count += 1
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
            if (context := contrast.CONTEXT.get()) is None or stop_propagation(context):
                return result

            propagate_stream(method_name, result, instance, result, args, kwargs)
            context.propagation_count += 1

        return result

    return wrap_and_watermark(orig_method, stream_patch)


def build_and_apply_str_patch(owner, method_name, patch_builder):
    orig_method = getattr(owner, method_name)

    policy_method_name = orig_method.__name__

    patch_policy = registry.get_policy_by_name(
        f"{owner.__module__}.{owner.__name__}.{policy_method_name}"
    )
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
        builder = build_str_format_map_patch
    elif method_name == "extend":
        builder = build_bytearray_extend_patch
    elif method_name == "take_bytes":
        builder = build_bytearray_take_bytes_patch
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
