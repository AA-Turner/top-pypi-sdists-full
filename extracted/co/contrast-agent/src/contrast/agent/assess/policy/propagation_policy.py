# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import contrast
from contrast.agent import scope
from contrast.agent.assess.contrast_event import ContrastEvent
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.propagators import (
    PROPAGATOR_ACTIONS,
    STREAM_ACTIONS,
    BasePropagator,
    stream_propagator,
)
from contrast.agent.assess.policy.source_policy import SourceNode, apply_stream_source
from contrast.agent.assess.properties import Properties
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.utils import (
    copy_tags_to_offset,
    copy_events,
    copy_from,
    is_tracked,
    get_properties,
    set_properties,
    track_string,
)
from contrast.utils.assess.duck_utils import safe_getattr

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def apply(nodes, preshift, ret, **kwargs):  # pylint: disable=redefined-builtin
    if not nodes:
        return

    if not scope.in_propagation_scope():
        with scope.propagation_scope():
            for node in nodes:
                if not preshift:
                    continue

                target = node.get_matching_first_target(
                    preshift.obj, ret, preshift.args, preshift.kwargs
                )

                apply_propagator(node, preshift, target, ret)


def track_copy_without_new_event(target, self_obj):
    """
    In general, when a string propagation event results in a copy of the
    original object we track the newly created copy but don't record an event.
    This behavior might be modified in the future.

    Usually, python is smart enough not to create a new string object that is
    simply a copy of the original. However, there are several exceptions to
    this rule.

    This method should only be invoked in these special cases, and they should
    be documented heavily.
    """
    if is_tracked(self_obj):
        track_string(target)
        copy_from(target, self_obj, 0, set())


STREAM_SOURCES = ["read", "read1", "readline", "readlines", "getvalue"]
STREAM_WRITE_METHODS = ["write", "writelines"]


def create_stream_event(node_type, parents, stream, args, kwargs):
    context = contrast.REQUEST_CONTEXT.get()
    if context is None or not context.assess_enabled:
        return None

    module = stream.__class__.__module__
    class_name = stream.__class__.__name__

    if not args and not kwargs:
        # We add an empty string if an empty stream is created for reporting purposes
        args = ("",)

    source_type = safe_getattr(stream, "cs__source_type", None) or "BODY"

    if node_type == "source":
        node = SourceNode(
            module,
            class_name,
            True,
            "__init__",
            "ARG_0,KWARG:initial_value",
            source_type,
        )
    else:
        node = PropagationNode(
            module,
            class_name,
            True,
            "__init__",
            "ARG_0,KWARG:initial_value",
            "RETURN",
            source_type,
            None,
        )

    return ContrastEvent(node, stream, stream, None, args, kwargs, parents, 0, None)


def create_stream_source_event(stream, args, kwargs):
    """
    Called directly from C extensions to create source events for __init__
    """
    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        return

    source_type = safe_getattr(stream, "cs__source_type", None) or "BODY"

    init_event = create_stream_event("source", [], stream, args, kwargs)
    stream.cs__source_event = init_event

    if context.stop_source_creation(source_type, None):
        return

    if len(args) > 0:
        properties = get_properties(args[0])
        if properties is not None:
            _add_and_track_event_to_stream(stream, properties, args, kwargs)

    if kwargs and len(kwargs) > 0:
        properties = get_properties(kwargs.get("initial_value"))
        if properties is not None:
            _add_and_track_event_to_stream(stream, properties, args, kwargs)


def _add_and_track_event_to_stream(stream, properties, args, kwargs):
    stream_props = Properties(stream)
    set_properties(stream, stream_props)
    copy_tags_to_offset(stream_props, properties.tags, 0)
    copy_events(stream_props, properties)
    parents = [properties.event] if properties.event else []
    prop_event = create_stream_event("propagation", parents, stream, args, kwargs)
    if prop_event is not None:
        stream_props.event = prop_event
    stream.cs__tracked = True


def propagate_stream(method_name, target, self_obj, ret, args, kwargs):
    args = [] if args is None else args
    kwargs = {} if kwargs is None else kwargs
    preshift = Preshift(self_obj, args, kwargs)

    if method_name in STREAM_WRITE_METHODS:
        stream_propagator.propagate_stream_write(method_name, preshift, target, ret)

    elif (
        self_obj.cs__tracked
        and get_properties(self_obj)
        and get_properties(self_obj).tags
    ):
        propagation_method = STREAM_ACTIONS.get(method_name)
        if propagation_method is None:
            return

        propagation_method(method_name, preshift, target, ret)

    # If the stream is already considered tracked, it will not be treated as a
    # source.
    elif self_obj.cs__source and method_name in STREAM_SOURCES:
        apply_stream_source(method_name, target, self_obj, ret, args, kwargs)


def apply_propagator(propagator_node, preshift, target, ret):
    if not propagator_node or not target:
        return

    if isinstance(target, dict):
        for key, value in target.items():
            apply_propagator(propagator_node, preshift, key, ret)
            apply_propagator(propagator_node, preshift, value, ret)
    else:
        propagate_string(propagator_node, preshift, target, ret)


def propagate_string(propagator_node, preshift, target, ret):
    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        return

    if context.stop_propagation:
        return

    action = propagator_node.action
    propagator_class = PROPAGATOR_ACTIONS.get(action, BasePropagator)

    propagator = propagator_class(propagator_node, preshift, target)

    if not propagator.needs_propagation:
        return

    propagator.track_and_propagate(ret)
    logger.debug(
        "Propagator %s found: propagated to %s", propagator_node.name, id(target)
    )
    context.propagated()
