"""Private PyTorch monkey patches for scan backward compatibility.

All direct interaction with PyTorch scan autograd internals is isolated here so
callers do not need to import or reason about those private symbols.
"""

from __future__ import annotations

from typing import Any

from pyvers import implement_for


def _differentiable_sample_requires_grad(value: Any) -> Any:
    import torch

    if not isinstance(value, torch.Tensor):
        return value
    sample = value.detach().clone()
    if value.dtype.is_floating_point or value.dtype.is_complex:
        sample.requires_grad_(True)
    return sample


def _map_differentiable_samples(value: Any) -> Any:
    import torch

    if isinstance(value, torch.Tensor):
        return _differentiable_sample_requires_grad(value)
    if isinstance(value, tuple):
        return tuple(_map_differentiable_samples(item) for item in value)
    if isinstance(value, list):
        return [_map_differentiable_samples(item) for item in value]
    if isinstance(value, dict):
        return {key: _map_differentiable_samples(item) for key, item in value.items()}
    return value


def _register_scan_autograd_impl(scan_module: Any, scan_autograd: Any) -> bool:
    import torch

    scan_op = getattr(scan_module, "scan_op", None)
    if scan_op is None or not hasattr(scan_op, "py_autograd_impl"):
        return False

    py_kernels = getattr(scan_op, "py_kernels", None)
    if py_kernels is None:
        return False

    autograd_key = torch._C.DispatchKey.Autograd
    previous = py_kernels.pop(autograd_key, None)
    if hasattr(scan_op, "_dispatch_cache"):
        scan_op._dispatch_cache.clear()
    try:
        scan_op.py_autograd_impl(scan_autograd)
    except Exception:
        py_kernels.pop(autograd_key, None)
        if previous is not None:
            py_kernels[autograd_key] = previous
        if hasattr(scan_op, "_dispatch_cache"):
            scan_op._dispatch_cache.clear()
        return False

    scan_module.scan_autograd = scan_autograd
    return True


def _patch_scan_autograd_aliasing(scan_module: Any) -> bool:
    import torch
    import torch.fx

    try:
        from torch.multiprocessing.reductions import StorageWeakRef
    except Exception:
        return False

    scan_autograd_impl = getattr(scan_module, "ScanAutogradImpl", None)
    if scan_autograd_impl is None:
        return False
    if getattr(scan_autograd_impl, "_hoptorch_scan_backward_alias_patch", False):
        return True

    scan_forward_policy = getattr(scan_module, "ScanForwardIntermediatesHandlingPolicy", None)
    find_hop_subgraph_outputs = getattr(scan_module, "_find_hop_subgraph_outputs", None)
    pytree = getattr(scan_module, "pytree", None)
    if (
        scan_forward_policy is None
        or find_hop_subgraph_outputs is None
        or pytree is None
        or not callable(getattr(scan_autograd_impl, "_insert_clone", None))
        or not callable(getattr(scan_autograd_impl, "_optimize_forward_intermediates", None))
    ):
        return False

    def _graph_output_node(graph: torch.fx.Graph) -> torch.fx.Node:
        output_node = getattr(graph, "output_node", None)
        if callable(output_node):
            return output_node()
        return next(iter(graph.find_nodes(op="output")))

    def _aliases_placeholder_predicate(graph: torch.fx.Graph):
        placeholder_storages = set()
        for placeholder in graph.find_nodes(op="placeholder"):
            val = placeholder.meta.get("val", None) if hasattr(placeholder, "meta") else None
            if isinstance(val, torch.Tensor):
                placeholder_storages.add(StorageWeakRef(val._typed_storage()))

        def aliases_placeholder(node: torch.fx.Node) -> bool:
            if node.op == "placeholder":
                return True
            val = node.meta.get("val", None) if hasattr(node, "meta") else None
            if isinstance(val, torch.Tensor):
                return StorageWeakRef(val._typed_storage()) in placeholder_storages
            return False

        return aliases_placeholder

    def _break_bw_input_output_aliasing(self) -> None:
        if not hasattr(self, "_insert_clone"):
            raise AssertionError("ScanAutogradImpl must define _insert_clone")

        bw_gm = self.hop_partitioned_graph.bw_gm
        bw_output_node = _graph_output_node(bw_gm.graph)
        if len(bw_output_node.args) != 1:
            raise AssertionError(
                "expected bw_gm output to have 1 arg, got "
                f"{len(bw_output_node.args)}"
            )

        bw_outputs = bw_output_node.args[0]
        if not isinstance(bw_outputs, (tuple, list)):
            bw_outputs = (bw_outputs,)

        aliases_placeholder = self._hoptorch_aliases_placeholder_predicate(bw_gm.graph)

        new_bw_outputs = []
        rewrote = False
        for output in bw_outputs:
            if isinstance(output, torch.fx.Node) and aliases_placeholder(output):
                new_bw_outputs.append(self._insert_clone(output, bw_output_node))
                rewrote = True
            else:
                new_bw_outputs.append(output)

        if rewrote:
            bw_output_node.args = (tuple(new_bw_outputs),)
            bw_gm.graph.lint()
            bw_gm.recompile()

    def _optimize_forward_intermediates(self) -> None:
        fw_gm = self.hop_partitioned_graph.fw_gm
        fw_all_outputs = find_hop_subgraph_outputs(fw_gm)
        placeholders = list(fw_gm.graph.find_nodes(op="placeholder"))
        fw_outputs = fw_all_outputs[: self.hop_partitioned_graph.n_fw_outputs]
        fw_intermediates = fw_all_outputs[self.hop_partitioned_graph.n_fw_outputs :]

        init_placeholders, xs_placeholders, additional_input_placeholders = (
            pytree.tree_unflatten(placeholders, self.fw_spec)
        )
        init_node_set, xs_node_set, additional_input_node_set = (
            set(init_placeholders),
            set(xs_placeholders),
            set(additional_input_placeholders),
        )

        if len(self.forward_intermediates_handling_policies) != 0:
            raise AssertionError(
                "forward_intermediates_handling_policies should be empty"
            )
        if len(self.saved_fw_xs) != 0:
            raise AssertionError("saved_fw_xs should be empty")
        if len(self.saved_fw_additional_inputs) != 0:
            raise AssertionError("saved_fw_additional_inputs should be empty")

        intermediate_idx_to_placeholder_idx = {}
        placeholder_idx = {
            placeholder: idx for idx, placeholder in enumerate(placeholders)
        }
        for idx, output in enumerate(fw_intermediates):
            if output in init_node_set:
                self.forward_intermediates_handling_policies.append(
                    scan_forward_policy.CLONE
                )
                intermediate_idx_to_placeholder_idx[idx] = placeholder_idx[output]
            elif output in xs_node_set:
                self.forward_intermediates_handling_policies.append(
                    scan_forward_policy.REMOVE_XS
                )
                intermediate_idx_to_placeholder_idx[idx] = placeholder_idx[output]
            elif output in additional_input_node_set:
                self.forward_intermediates_handling_policies.append(
                    scan_forward_policy.REMOVE_ADDITIONAL_INPUTS
                )
                intermediate_idx_to_placeholder_idx[idx] = placeholder_idx[output]
            else:
                self.forward_intermediates_handling_policies.append(
                    scan_forward_policy.KEEP
                )

        new_output_node = []
        real_graph_inputs = (
            list(self.init) + list(self.xs) + list(self.additional_inputs)
        )
        fw_output_node = _graph_output_node(fw_gm.graph)
        aliases_placeholder = self._hoptorch_aliases_placeholder_predicate(fw_gm.graph)
        for intermediate_idx, (node, policy) in enumerate(
            zip(fw_intermediates, self.forward_intermediates_handling_policies)
        ):
            if policy == scan_forward_policy.CLONE:
                new_output_node.append(self._insert_clone(node, fw_output_node))
            elif policy == scan_forward_policy.REMOVE_XS:
                if intermediate_idx not in intermediate_idx_to_placeholder_idx:
                    raise AssertionError(
                        "missing placeholder index for REMOVE_XS intermediate "
                        f"{intermediate_idx}"
                    )
                input_idx = intermediate_idx_to_placeholder_idx[intermediate_idx]
                self.saved_fw_xs.append(real_graph_inputs[input_idx])
            elif policy == scan_forward_policy.REMOVE_ADDITIONAL_INPUTS:
                if intermediate_idx not in intermediate_idx_to_placeholder_idx:
                    raise AssertionError(
                        "missing placeholder index for "
                        f"REMOVE_ADDITIONAL_INPUTS intermediate {intermediate_idx}"
                    )
                input_idx = intermediate_idx_to_placeholder_idx[intermediate_idx]
                self.saved_fw_additional_inputs.append(real_graph_inputs[input_idx])
            elif isinstance(node, torch.fx.Node) and aliases_placeholder(node):
                new_output_node.append(self._insert_clone(node, fw_output_node))
            else:
                new_output_node.append(node)

        fw_output_node.args = (tuple(fw_outputs) + tuple(new_output_node),)
        fw_gm.graph.lint()
        fw_gm.recompile()

    original_init = scan_autograd_impl.__init__
    original_optimize_forward_intermediates = (
        scan_autograd_impl._optimize_forward_intermediates
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)
        self._break_bw_input_output_aliasing()

    scan_autograd_impl._hoptorch_aliases_placeholder_predicate = staticmethod(
        _aliases_placeholder_predicate
    )
    scan_autograd_impl._break_bw_input_output_aliasing = _break_bw_input_output_aliasing
    scan_autograd_impl._optimize_forward_intermediates = _optimize_forward_intermediates
    scan_autograd_impl.__init__ = __init__
    scan_autograd_impl._hoptorch_scan_backward_original_init = original_init
    scan_autograd_impl._hoptorch_scan_backward_original_optimize_forward_intermediates = (
        original_optimize_forward_intermediates
    )
    scan_autograd_impl._hoptorch_scan_backward_alias_patch = True
    return True


def _patch_current_scan_autograd(scan_module: Any) -> bool:
    required = (
        "HopGraphMinCutPartitioner",
        "ScanAutogradImpl",
        "ScanAutogradOp",
        "disable_proxy_modes_tracing",
    )
    if not all(hasattr(scan_module, name) for name in required):
        return False

    if not _patch_scan_autograd_aliasing(scan_module):
        return False

    def scan_autograd(combine_fn, init, xs, additional_inputs):
        with scan_module.disable_proxy_modes_tracing():
            sample_init = [_differentiable_sample_requires_grad(t) for t in init]
            sample_args = (*sample_init, *[x[0] for x in xs], *additional_inputs)
            try:
                hop_partitioned_graph = (
                    scan_module.HopGraphMinCutPartitioner.create_partitioned_graph(
                        combine_fn,
                        sample_args,
                        always_recompute_complex_exprs=True,
                    )
                )
            except TypeError:
                real_args = (*init, *[x[0] for x in xs], *additional_inputs)
                hop_partitioned_graph = (
                    scan_module.HopGraphMinCutPartitioner.create_partitioned_graph(
                        combine_fn,
                        real_args,
                        sample_args,
                        always_recompute_complex_exprs=True,
                    )
                )

        return scan_module.ScanAutogradOp.apply(
            hop_partitioned_graph,
            len(init),
            len(xs),
            len(additional_inputs),
            *init,
            *xs,
            *additional_inputs,
        )

    return _register_scan_autograd_impl(scan_module, scan_autograd)


def _patch_older_scan_autograd(scan_module: Any) -> bool:
    materialize_as_graph = getattr(scan_module, "materialize_as_graph", None)
    if materialize_as_graph is None:
        return False
    if getattr(materialize_as_graph, "_hoptorch_scan_backward_sample_patch", False):
        return True

    def patched_materialize_as_graph(fn, args, *other_args, **kwargs):
        return materialize_as_graph(
            fn,
            _map_differentiable_samples(args),
            *other_args,
            **kwargs,
        )

    patched_materialize_as_graph._hoptorch_scan_backward_sample_patch = True
    patched_materialize_as_graph._hoptorch_scan_backward_original = materialize_as_graph
    scan_module.materialize_as_graph = patched_materialize_as_graph
    return True


@implement_for("torch")
def install_scan_backward_patch(scan_module: Any) -> bool:
    """Attempt to install a scan backward compatibility patch."""

    return False


@install_scan_backward_patch.register(from_version="2.7", to_version="2.8")
def _(scan_module: Any) -> bool:
    from ._scan_backport_27 import install_scan_27_backport

    return install_scan_27_backport(scan_module)


@install_scan_backward_patch.register(from_version="2.8")
def _(scan_module: Any) -> bool:
    try:
        return _patch_current_scan_autograd(scan_module) or _patch_older_scan_autograd(scan_module)
    except Exception:
        return False


@implement_for("torch")
def rollback_failed_scan_backward_patch(scan_module: Any) -> bool:
    """Best-effort rollback for reversible compatibility patches."""

    return False


@rollback_failed_scan_backward_patch.register(from_version="2.7", to_version="2.8")
def _(scan_module: Any) -> bool:
    from ._scan_backport_27 import rollback_scan_27_backport

    return rollback_scan_27_backport(scan_module)


@rollback_failed_scan_backward_patch.register(from_version="2.8")
def _(scan_module: Any) -> bool:
    materialize_as_graph = getattr(scan_module, "materialize_as_graph", None)
    original = getattr(materialize_as_graph, "_hoptorch_scan_backward_original", None)
    if original is None:
        return False
    scan_module.materialize_as_graph = original
    return True
