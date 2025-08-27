# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements patches for the operator module

Our propagation rewrites are implemented in terms of these patches, so they
must always be enabled when Assess is enabled.
"""

import sys
import contrast

from contrast.agent.assess.policy.propagators.base_propagator import SUPPORTED_TYPES

from contrast.agent import scope
from contrast.agent.assess.utils import is_trackable
from contrast.agent.policy import patch_manager
from contrast.patches.utils import analyze_policy, get_propagation_node
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)
from contrast.agent.assess.policy.propagators import BasePropagator, PROPAGATOR_ACTIONS
from contrast.agent.assess.policy.preshift import Preshift

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def build_mod_propagator(policy_node):
    """
    Build propagator function used in the operator.mod patch.

    Part of the complication here is that the format propagator expects the format
    string to be `OBJ` (not `ARG_0`). We need to perform some manual rearrangement of
    the operator.mod arguments for format propagation to work correctly.

    TODO: PYT-3718 - In the future, the format propagator should be able to select the
    format string out of a preshift object using the policy node (instead of being
    hardcoded to extract the format string from OBJ).
    """
    propagator_class = PROPAGATOR_ACTIONS.get(policy_node.action, BasePropagator)

    @fail_quietly("failed to propagate through mod")
    @scope.contrast_scope()
    @scope.propagation_scope()
    def propagate_mod(ret, orig_args, kwargs):
        assert kwargs == {}  # mod takes no kwargs
        fmt_str, args = orig_args
        if not isinstance(fmt_str, bytearray) and ret is fmt_str:
            return

        context = contrast.REQUEST_CONTEXT.get()
        if context is None or context.stop_propagation:
            return

        if not isinstance(args, tuple):
            args = (args,)

        preshift = Preshift(fmt_str, args, {})

        propagator = propagator_class(policy_node, preshift, ret)
        if not propagator.needs_propagation:
            return

        propagator.track_and_propagate(ret)

        logger.debug("Propagator %s found: propagated to %s", policy_node.name, id(ret))

        context.propagated()

    return propagate_mod


def build_add_hook(original_func, patch_policy):
    policy_node = get_propagation_node(patch_policy)

    def add(wrapped, instance, args, kwargs):
        del instance

        if not isinstance(args[0], SUPPORTED_TYPES) and not isinstance(
            args[1], SUPPORTED_TYPES
        ):
            # This is an operation we don't support, so we return the result
            # without any tracking.
            # Don't enter scope, because this could be an operation against
            # a class with a custom __add__ method, and we want to track
            # dataflow through that user code.
            return wrapped(*args, **kwargs)

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_contrast_or_propagation_scope():
            return result

        analyze_policy(policy_node.name, result, args, kwargs)

        return result

    return wrap_and_watermark(original_func, add)


def build_mod_hook(original_func, patch_policy):
    propagation_func = build_mod_propagator(patch_policy.propagator_nodes[0])

    def mod(wrapped, instance, args, kwargs):
        del instance

        format_string = args[0]
        if not isinstance(format_string, SUPPORTED_TYPES):
            # This is a modulo operation that we don't support,
            # so we return the result without any tracking.
            # Don't enter scope, because this could be an operation
            # against a class with a custom __mod__ method, and we
            # want to track dataflow through that user code.
            return wrapped(*args, **kwargs)

        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)
        if not is_trackable(result) or scope.in_contrast_or_propagation_scope():
            return result
        propagation_func(result, args, kwargs)

        return result

    return wrap_and_watermark(original_func, mod)


def patch_operator(operator_module):
    build_and_apply_patch(operator_module, "add", build_add_hook)
    build_and_apply_patch(operator_module, "iadd", build_add_hook)
    build_and_apply_patch(operator_module, "mod", build_mod_hook)


def register_patches():
    register_module_patcher(patch_operator, "operator")


def reverse_patches():
    unregister_module_patcher("operator")
    operator_module = sys.modules.get("operator")
    if not operator_module:
        return

    patch_manager.reverse_patches_by_owner(operator_module)
