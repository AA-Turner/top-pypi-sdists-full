# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import copy
from itertools import product


def _to_list(obj):
    return obj if isinstance(obj, list) else [obj]


def _generate_nodes(node_cls, node_kwargs, dataflow=None):
    """
    Generates policy objects using the given node class and kwargs

    The "module", "method_name", and "class_name" attributes can optionally be lists.
    This function generates nodes based on the product of those attributes, which
    helps reduce code duplication in policy.
    """
    node_kwargs = copy.copy(node_kwargs)
    # NOTE: this really needs to be fixed on the nodes themselves
    node_kwargs.setdefault("instance_method", True)

    if dataflow is not None:
        node_kwargs["dataflow"] = dataflow

    modules = _to_list(node_kwargs.pop("module"))
    method_names = _to_list(node_kwargs.pop("method_name"))
    class_names = _to_list(node_kwargs.pop("class_name", ""))

    for module, class_name, method_name in product(modules, class_names, method_names):
        yield node_cls(
            module=module,
            class_name=class_name,
            method_name=method_name,
            **node_kwargs,
        )


def generate_policy(node_cls, nodes, dataflow=None):
    """
    Generate policy objects given a policy node class and a list of putative nodes

    Objects in the node list can either by Python dicts or CompositeNode instances.
    """
    for node in nodes:
        yield from (
            node.generate_from_class(node_cls, dataflow=dataflow)
            if isinstance(node, CompositeNode)
            else _generate_nodes(node_cls, node, dataflow=dataflow)
        )


class CompositeNode:
    """
    CompositeNode allows multiple policy nodes to share an arbitrary set of attributes

    This is intended to reduce duplication in policy definitions by reducing
    the number of repeated attributes.
    """

    def __init__(self, common_kwargs, nodes):
        self.common_kwargs = common_kwargs
        self.nodes = nodes

    def generate_from_class(self, node_cls, dataflow=None):
        """
        Generates policy objects of the given class based on common kwargs and the list of nodes
        """
        for node in self.nodes:
            # NOTE: the order of composition matters here in order to allow
            # more specific nodes to override the common kwargs
            # Once we support only >=3.9 we can use the | operator for dicts
            kwargs = {**self.common_kwargs, **node}
            yield from _generate_nodes(node_cls, kwargs, dataflow=dataflow)


def get_self_for_method(patch_policy, args):
    """
    Retrieves self for a method's PatchLocationPolicy,

    If any node in the policy has a False instance_method attribute return None
    """
    for node in patch_policy.all_nodes:
        if not node.instance_method:
            return None

    return args[0] if args else None
