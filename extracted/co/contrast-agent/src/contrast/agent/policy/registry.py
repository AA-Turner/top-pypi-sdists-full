# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import functools
from collections import OrderedDict

from contrast.agent.assess.policy.deadzone_node import DeadZoneNode
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.rules.trigger_rule import TriggerRule
from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
from contrast.agent.policy.policy_node import PolicyNode
from contrast.agent.policy.trigger_node import TriggerNode
from contrast.agent.policy.utils import generate_policy
from contrast.utils.namespace import Namespace


class _module(Namespace):
    """
    This class represents the central registry of all policy for the agent
    """

    sources: list[SourceNode] = []
    propagators: list[PropagationNode] = []
    triggers: OrderedDict[str, TriggerRule] = OrderedDict()
    providers = OrderedDict()
    deadzones: list[DeadZoneNode] = []

    # This is used to ensure that we only ever have one PatchLocationPolicy
    # instance per patch location.
    policy_by_name: OrderedDict[str, PatchLocationPolicy] = OrderedDict()
    # This is used to represent a list of PatchLocationPolicy instances per each
    # module. It is what enables the application of module-level import hooks.
    policy_by_module: OrderedDict[str, list[PatchLocationPolicy]] = OrderedDict()

    protect_policy_by_module: OrderedDict[str, list[PatchLocationPolicy]] = (
        OrderedDict()
    )


def _process_node(node: PolicyNode) -> PatchLocationPolicy:
    """
    Create patch location policy for node and update lookup tables if necessary
    """
    patch_policy = _module.policy_by_name.setdefault(
        node.name, PatchLocationPolicy(node)
    )
    patch_policy.add_node(node)

    policy_list = _module.policy_by_module.setdefault(node.module, [])
    policy_list.append(patch_policy)

    if isinstance(node, TriggerNode) and node.protect_mode:
        policy_list = _module.protect_policy_by_module.setdefault(node.module, [])
        policy_list.append(patch_policy)

    return patch_policy


def register_source_nodes(source_nodes: list) -> None:
    for node in generate_policy(SourceNode, source_nodes):
        _module.sources.append(node)
        _process_node(node)


def register_dynamic_source(
    *source_node_args,
    **source_node_kwargs,
) -> PatchLocationPolicy:
    node = SourceNode.dynamic(*source_node_args, **source_node_kwargs)
    node.validate()
    _module.sources.append(node)
    return _process_node(node)


def register_propagation_nodes(propagation_nodes: list) -> None:
    for node in generate_policy(PropagationNode, propagation_nodes):
        _module.propagators.append(node)
        _process_node(node)


def register_trigger_rule(rule: TriggerRule) -> None:
    assert rule.name not in _module.triggers
    _module.triggers[rule.name] = rule
    for node in rule.nodes:
        node.rule = rule
        _process_node(node)


def register_deadzone_nodes(deadzone_nodes: list) -> None:
    for node in generate_policy(DeadZoneNode, deadzone_nodes):
        _module.deadzones.append(node)
        _process_node(node)


def get_policy_by_name(name: str) -> PatchLocationPolicy | None:
    return _module.policy_by_name.get(name)


def get_policy(protect: bool = False) -> OrderedDict[str, list[PatchLocationPolicy]]:
    return _module.protect_policy_by_module if protect else _module.policy_by_module


def get_patch_policies(
    protect: bool = False,
) -> OrderedDict[str, list[PatchLocationPolicy]]:
    policy_patches = OrderedDict()
    for module, policy_list in get_policy(protect).items():
        if policies_with_patches := [
            policy for policy in policy_list if policy.has_patches
        ]:
            policy_patches[module] = policies_with_patches
    return policy_patches


def get_policy_by_module(
    module: str, protect: bool = False
) -> list[PatchLocationPolicy]:
    return get_policy(protect).get(module, [])


@functools.lru_cache(maxsize=1)
def get_string_method_nodes():
    return [
        node for node in get_policy_by_module("builtins") if node.class_name == "str"
    ]


# NOTE: it's possible that (some of) the methods below are only used by tests
def get_source_nodes() -> list[SourceNode]:
    return _module.sources


def get_propagation_nodes() -> list[PropagationNode]:
    return _module.propagators


def get_trigger_nodes() -> OrderedDict[str, TriggerRule]:
    return _module.triggers


def get_triggers_by_rule(rule_id: str) -> TriggerRule | None:
    return _module.triggers.get(rule_id)


def get_deadzone_nodes() -> list[DeadZoneNode]:
    return _module.deadzones
