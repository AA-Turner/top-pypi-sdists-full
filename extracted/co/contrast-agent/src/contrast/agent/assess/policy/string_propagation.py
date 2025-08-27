# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Builds/defines propagation functions to be called from C extension hooks. Only
propagation functions for NECESSARY_PROPAGATORS will be defined in this module.

NOTE: Propagator functions must be generated before the C extension is initialized.
"""

import sys

from contrast.agent.assess.utils import is_tracked
from contrast_vendor import structlog as logging

import contrast
from contrast.agent.assess.policy.preshift import Preshift
from contrast.agent.assess.policy.propagation_policy import track_copy_without_new_event

# We call these from the C extension - they're import aliases
from contrast.agent.assess.policy.propagation_policy import (  # noqa: F401
    create_stream_source_event,
    propagate_stream,
)
from contrast.agent.assess.policy.propagators import BasePropagator, PROPAGATOR_ACTIONS
from contrast.agent.policy import registry

NECESSARY_PROPAGATORS = (
    "__repr__",
    "repeat",
    "CAST",
    "subscript",
)
HOOK_TYPE_NAMES = ["unicode", "bytes", "bytearray"]

logger = logging.getLogger("contrast")
module = sys.modules[__name__]


def build_generic_strtype_propagator(policy_node):
    """
    Build propagator function used for most methods of unicode and bytes types

    By not accounting for bytearray propagation in this function we are able to
    optimize for the most frequent propagation events.

    We also optimize by avoiding handling for a few unicode/bytes special case methods
    in this function. Those special cases are handled by other builders below.

    While this leads to some code duplication, it allows us to optimize some of the
    most intensively called code in the agent.
    """
    propagator_class = PROPAGATOR_ACTIONS.get(policy_node.action, BasePropagator)

    def propagate_string(target, self_obj, ret, args, kwargs):
        # Short-circuit that applies to all string types except bytearray
        if ret is self_obj:
            return

        context = contrast.REQUEST_CONTEXT.get()
        if context is None or context.stop_propagation:
            return

        preshift = Preshift(self_obj, args or [], kwargs or {})

        propagator = propagator_class(policy_node, preshift, target)
        if not propagator.needs_propagation:
            return

        propagator.track_and_propagate(ret)

        logger.debug(
            "Propagator %s found: propagated to %s", policy_node.name, id(target)
        )

        context.propagated()

    return propagate_string


def build_bytearray_propagator(policy_node):
    """
    Build propagator function used for all methods of bytearray instances

    Copies of bytearrays return a new object, so it is necessary for us to track the
    new string, even if it hasn't changed.

    We could break the concat special case into a separate propagator function, but I'm
    not really sure it's worth it for bytearray since bytearay events are expected to
    be pretty rare. We can change it if it ever becomes a performance issue.

    Keeping this case separate from the generic builder allows us to avoid slowing down
    the propagation of the more frequently called unicode/bytes propagators, even if it
    leads to some duplicated code.
    """
    propagator_class = PROPAGATOR_ACTIONS.get(policy_node.action, BasePropagator)
    method_name = policy_node.method_name

    def propagate_bytearray(target, self_obj, ret, args, kwargs):
        context = contrast.REQUEST_CONTEXT.get()
        if context is None or context.stop_propagation:
            return

        if ret == self_obj and method_name != "concat":
            track_copy_without_new_event(target, self_obj)
            return

        preshift = Preshift(self_obj, args or [], kwargs or {})

        propagator = propagator_class(policy_node, preshift, target)
        if not propagator.needs_propagation:
            return

        propagator.track_and_propagate(ret)

        logger.debug(
            "Propagator %s found: propagated to %s", policy_node.name, id(target)
        )

        context.propagated()

    return propagate_bytearray


def build_generic_cast_propagator(policy_node):
    """
    Build propagator function used for cast propagation for unicode/bytes

    Having a separate builder here allows us to optimize for the translate special case
    without imposing a blanket performance overhead on all other unicode/bytes methods.
    """
    propagator_class = PROPAGATOR_ACTIONS.get(policy_node.action, BasePropagator)

    def propagate_cast(target, self_obj, ret, args, kwargs):
        if ret is (args and args[0]) or is_tracked(ret):
            # If the return value is the same as the first argument,
            # then no new object was created and we'll already be tracking
            # the return value (or not).
            # If the return value is already tracked, we already propagated
            # to it (likely via a custom __str__ or __bytes__ method) and
            # don't need to do so again.
            return

        context = contrast.REQUEST_CONTEXT.get()
        if context is None or context.stop_propagation:
            return

        preshift = Preshift(self_obj, args or [], kwargs or {})

        propagator = propagator_class(policy_node, preshift, target)
        if not propagator.needs_propagation:
            return

        propagator.track_and_propagate(ret)

        logger.debug(
            "Propagator %s found: propagated to %s", policy_node.name, id(target)
        )

        context.propagated()

    return propagate_cast


def build_bytearray_cast_propagator(policy_node):
    """
    Build propagator function used for cast propagation for bytearray

    Having a separate builder here allows us to optimize for the translate special case
    without imposing a blanket performance overhead on all other unicode/bytes methods.
    """
    propagator_class = PROPAGATOR_ACTIONS.get(policy_node.action, BasePropagator)

    def propagate_cast(target, self_obj, ret, args, kwargs):
        source = args and args[0]
        if (
            ret == source
            and isinstance(target, bytearray)
            and isinstance(source, bytearray)
        ):
            track_copy_without_new_event(target, source)
            return

        context = contrast.REQUEST_CONTEXT.get()
        if context is None or context.stop_propagation:
            return

        preshift = Preshift(self_obj, args or [], kwargs or {})

        propagator = propagator_class(policy_node, preshift, target)
        if not propagator.needs_propagation:
            return

        propagator.track_and_propagate(ret)

        logger.debug(
            "Propagator %s found: propagated to %s", policy_node.name, id(target)
        )

        context.propagated()

    return propagate_cast


def _create_propagator_function(strtype, location, propagation_node, builder):
    propagator_name = f"propagate_{strtype}_{location.method_name.lower()}"
    propagator = builder(propagation_node)
    propagator.__name__ = propagator_name
    setattr(module, propagator_name, propagator)


PROPAGATION_SPECIAL_CASES = {
    ("unicode", "CAST"): build_generic_cast_propagator,
    ("bytes", "CAST"): build_generic_cast_propagator,
    ("bytearray", "CAST"): build_bytearray_cast_propagator,
}


def build_string_propagator_functions():
    """
    Builds propagator functions that will be called from C extension hooks
    """
    for location in registry.get_string_method_nodes():
        if location.method_name not in NECESSARY_PROPAGATORS:
            continue
        prop_node = location.propagator_nodes[0]
        for strtype in HOOK_TYPE_NAMES:
            # Check whether there's a special case for this hook location
            propagator = PROPAGATION_SPECIAL_CASES.get(
                (strtype, location.method_name),
                (
                    # General case for either bytearray or other strtype
                    build_bytearray_propagator
                    if strtype == "bytearray"
                    else build_generic_strtype_propagator
                ),
            )
            _create_propagator_function(strtype, location, prop_node, propagator)
