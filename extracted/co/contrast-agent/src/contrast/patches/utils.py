# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.policy import registry
from contrast.agent.assess.policy.analysis import analyze
from contrast.utils.decorators import fail_quietly


def get_propagation_node(node):
    return node.propagator_nodes[0] if node.propagator_nodes else None


@fail_quietly("Failed to analyze policy")
def analyze_policy(name, result, args, kwargs):
    context = contrast.REQUEST_CONTEXT.get()
    if context is None or not context.propagate_assess or context.stop_propagation:
        return

    context.propagated()

    with scope.contrast_scope():
        patch_policy = registry.get_policy_by_name(name)
        if not patch_policy:
            return

    analyze(patch_policy, result, args, kwargs)
