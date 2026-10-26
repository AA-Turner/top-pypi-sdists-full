"""Capture tensor objectives as bounded, data-only loss graphs."""

from __future__ import annotations

import hashlib
import json
import operator
import os
from concurrent.futures import ThreadPoolExecutor

import sympy

from .losses import LossInputs, LossObjective, _input_array, _input_columns

import numpy as np
import torch
from torch.utils import _pytree
from torch._subclasses.fake_tensor import FakeTensorMode

LOSS_NAME = "loss_graph_v1"
GRAPH_KEY = "__river_loss_graph_v1"
COLUMN_PREFIX = "__river_loss_column_"
POSITION_KEY = "__river_loss_position"
MAX_GRAPH_BYTES = 65536
MAX_NODES = 128


def _reset_capture_executor():
    global _capture_executor
    # Keep PyTorch's thread-owned fake CUDA guard alive and serialize exports.
    _capture_executor = ThreadPoolExecutor(
        max_workers=1, thread_name_prefix="river-loss-capture"
    )


_reset_capture_executor()
if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_reset_capture_executor)


def encode_custom_loss_batch(
    data: list[dict],
    *,
    inputs: LossInputs,
    graph: bytes,
) -> list[dict]:
    """Validate batch columns and attach a captured graph."""

    if not data:
        raise ValueError("custom loss requires a nonempty batch")
    names = sorted(data[0].get("loss_data", {}))
    if not names or len(names) > 16:
        raise ValueError("custom loss requires 1..16 loss_data columns")
    schemas = _input_columns(inputs)
    if names != [c["name"] for c in schemas]:
        raise ValueError("loss_data does not match the declared custom-loss inputs")
    prepared = []
    for index, datum in enumerate(data):
        if set(datum) - {
            "input_ids",
            "model_input",
            "attention_mask",
            "loss_data",
            "expert_routing_handle",
        }:
            raise ValueError(
                "custom loss accepts text input_ids or model_input chunks, attention_mask, loss_data, and expert_routing_handle"
            )
        if ("input_ids" in datum) == ("model_input" in datum):
            raise ValueError(
                "custom loss requires exactly one of input_ids or model_input"
            )
        if "model_input" in datum:
            chunks = datum["model_input"]
            if not isinstance(chunks, list) or not chunks:
                raise ValueError("model_input must be a nonempty list of chunks")
            length = 0
            for chunk in chunks:
                if chunk["type"] == "text":
                    tokens = np.asarray(chunk["tokens"])
                    if tokens.ndim != 1 or (
                        tokens.size and tokens.dtype.kind not in "iu"
                    ):
                        raise ValueError("text chunk tokens must be an integer vector")
                    length += len(tokens)
                elif chunk["type"] == "image":
                    expected = chunk["expected_tokens"]
                    if not isinstance(expected, (int, np.integer)) or expected <= 0:
                        raise ValueError(
                            "image expected_tokens must be a positive integer"
                        )
                    length += int(expected)
                else:
                    raise ValueError("model_input only supports text and image chunks")
            if not length:
                raise ValueError("model_input must expand to a nonempty sequence")
            encoded = {"model_input": chunks}
        else:
            ids = np.asarray(datum["input_ids"], dtype=np.int64)
            if ids.ndim != 1 or not len(ids):
                raise ValueError(f"data[{index}]: input_ids must be a nonempty vector")
            length = len(ids)
            encoded = {"input_ids": ids}
        if sorted(datum.get("loss_data", {})) != names:
            raise ValueError(
                f"data[{index}]: loss_data schema differs from the first datum"
            )
        if "expert_routing_handle" in datum:
            handle = datum["expert_routing_handle"]
            if isinstance(handle, str):
                handle = handle.encode("utf-8")
            if not isinstance(handle, bytes) or not 0 < len(handle) <= 4096:
                raise ValueError(
                    "expert_routing_handle must be a nonempty string or bytes, at most 4096 bytes"
                )
            handle.decode("utf-8")
            encoded["expert_routing_handle"] = np.frombuffer(
                handle, dtype=np.uint8
            ).copy()
        for column_index, name in enumerate(names):
            schema = schemas[column_index]
            array = _input_array(datum["loss_data"][name], schema)
            expected = (length,) + ((schema["width"],) if "width" in schema else ())
            if array.shape != expected or not np.isfinite(array).all():
                raise ValueError(
                    f"data[{index}].loss_data[{name!r}]: expected finite shape {expected}"
                )
            encoded[COLUMN_PREFIX + str(column_index)] = array
        encoded[POSITION_KEY] = np.ones(length, dtype=np.int64)
        mask = (
            np.asarray(datum["attention_mask"], dtype=np.int64)
            if "attention_mask" in datum
            else np.ones(length, dtype=np.int64)
        )
        if mask.shape != (length,) or not np.all(mask == 1):
            raise ValueError(
                "custom loss requires unpadded inputs with an all-one attention_mask"
            )
        encoded["attention_mask"] = mask
        prepared.append(encoded)
    envelope = np.frombuffer(graph, dtype=np.uint8).copy()
    for datum in prepared:
        datum[GRAPH_KEY] = envelope
    return prepared


def capture_loss_graph(objective: LossObjective, inputs: LossInputs) -> bytes:
    """Capture closure constants once, using only the declared column schema."""

    return _capture_executor.submit(_capture_loss_graph, objective, inputs).result()


def _capture_loss_graph(objective: LossObjective, inputs: LossInputs) -> bytes:

    version = tuple(int(part) for part in torch.__version__.split(".")[:2])
    if not (2, 4) <= version < (2, 14):
        raise ValueError("Custom loss capture requires PyTorch >=2.4,<2.14")
    schemas = _input_columns(inputs)
    names = [s["name"] for s in schemas]
    graph = None
    for dtype in (torch.float32, torch.bfloat16, torch.float16):
        captures = []
        for requires_grad in (False, True):
            sizes = [
                _capture_graph(objective, schemas, names, dtype, requires_grad, tokens)
                for tokens in (3, 1)
            ]
            if _graph_formula(sizes[0]) != _graph_formula(sizes[1]):
                raise ValueError("token-count-dependent objectives are unsupported")
            captures.append(sizes[0])
        if _graph_formula(captures[0]) != _graph_formula(captures[1]):
            raise ValueError("autograd-dependent objectives are unsupported")
        candidate = captures[0]
        if graph is None:
            graph = candidate
        elif _graph_formula(candidate) != _graph_formula(graph):
            raise ValueError(
                "custom loss must use the same formula for float32, bfloat16, and float16 logits; "
                "dtype-dependent objectives are unsupported"
            )
    return json.dumps(
        graph, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def graph_digest(payload: bytes) -> str:
    """Content key; data values are not captured Python constants."""
    return hashlib.sha256(payload).hexdigest()


def _graph_formula(graph):
    return graph | {
        "nodes": [
            {k: v for k, v in node.items() if k != "source"} for node in graph["nodes"]
        ]
    }


def _capture_graph(objective, schemas, names, dtype, requires_grad, tokens):

    class Wrapper(torch.nn.Module):
        def forward(self, logits, inputs):
            return objective(logits, inputs)

    n = {0: torch.export.Dim("N", min=2)} if tokens > 1 else {}
    v = torch.export.Dim("V", min=2, max=262144)
    with FakeTensorMode(), torch.set_grad_enabled(requires_grad):
        inputs = {
            s["name"]: torch.zeros(
                (tokens, s["width"]) if "width" in s else (tokens,),
                dtype=getattr(torch, s["dtype"]),
                device="cpu",
            )
            for s in schemas
        }
        exported = torch.export.export(
            Wrapper(),
            (
                torch.zeros(
                    tokens, 17, dtype=dtype, device="cpu", requires_grad=requires_grad
                ),
                inputs,
            ),
            dynamic_shapes=(n | {1: v}, {name: n for name in names}),
            strict=True,
        )
    # Some export versions emit redundant symbolic shape assertions. Only
    # discard proven tautologies; live shape arithmetic remains unsupported.
    for node in list(exported.graph.nodes):
        if (
            node.op == "call_function"
            and str(node.target) == "aten._assert_scalar.default"
        ):
            guard = node.args[0]
            value = guard.meta.get("val") if isinstance(guard, torch.fx.Node) else guard
            if not node.users and (
                value is True
                or isinstance(value, torch.SymBool)
                and value.node.expr is sympy.true
            ):
                exported.graph.erase_node(node)
    for node in reversed(list(exported.graph.nodes)):
        if (
            node.op == "call_function"
            and not node.users
            and (
                str(node.target) == "aten.sym_size.int"
                or node.target in (operator.eq, operator.le)
            )
        ):
            exported.graph.erase_node(node)
    if any(s.kind.name != "USER_INPUT" for s in exported.graph_signature.input_specs):
        raise ValueError(
            "custom loss may not capture parameters, buffers, or tensor constants"
        )
    nodes = []
    indices = {}
    logits_nodes = set()
    normalized_nodes = set()
    index_columns = set()
    placeholders = iter(
        [{"op": "logits"}] + [{"op": "input", "column": i} for i in range(len(names))]
    )
    binary = {"add", "sub", "mul", "div", "minimum", "maximum"}
    unary = {"neg", "exp", "expm1", "log", "sqrt", "detach"}
    model_nodes = set()
    scalar_nodes = set()
    bounded_nodes = set()
    reductions = {"sum", "mean", "amin", "amax", "logsumexp", "var", "std"}

    def argument(arg):
        if isinstance(arg, torch.fx.Node):
            return {"node": indices[arg]}
        if type(arg) in (int, float) and np.isfinite(arg):
            return {"constant": float(arg)}
        raise ValueError(f"unsupported loss argument: {type(arg).__name__}")

    for node in exported.graph.nodes:
        if node.op == "placeholder":
            ir = next(placeholders)
            if ir["op"] == "input":
                schema = schemas[ir["column"]]
                if schema["dtype"] in ("int32", "int64") and "width" in schema:
                    index_columns.add(node)
        elif node.op == "output":
            result = _pytree.tree_unflatten(
                list(node.args[0]), exported.call_spec.out_spec
            )
            if isinstance(result, tuple) and len(result) == 2:
                root, metrics = result
            else:
                root, metrics = result, {}
            if not isinstance(root, torch.fx.Node) or not isinstance(metrics, dict):
                raise ValueError(
                    "loss must return a scalar tensor or (scalar tensor, scalar metric dict)"
                )
            if len(metrics) > 16 or any(
                not isinstance(k, str)
                or not k
                or len(k) > 64
                or not isinstance(val, torch.fx.Node)
                for k, val in metrics.items()
            ):
                raise ValueError("expected at most 16 named tensor metrics")
            outputs = {
                "loss": indices[root],
                "metrics": {key: indices[val] for key, val in metrics.items()},
            }
            break
        elif node.op == "call_function":
            target = str(node.target)
            if target == "aten._assert_tensor_metadata.default":
                if (
                    len(node.args) != 1
                    or not isinstance(node.args[0], torch.fx.Node)
                    or node.kwargs
                    != {
                        "dtype": node.args[0].meta["val"].dtype,
                        "device": node.args[0].meta["val"].device,
                        "layout": torch.strided,
                    }
                ):
                    raise ValueError("unsupported tensor metadata guard")
                continue
            op = target.split(".")[1] if target.startswith("aten.") else ""
            if target in {"aten.to.dtype", "aten._to_copy.default"}:
                if node.args[0] in logits_nodes:
                    raise ValueError(
                        "logits casts are unsupported; use the model's native logits dtype"
                    )
                dtype = node.args[1] if len(node.args) > 1 else node.kwargs.get("dtype")
                source = node.args[0]
                source_ir = nodes[indices[source]]
                if (
                    dtype == torch.int64
                    and source_ir["op"] == "input"
                    and schemas[source_ir["column"]]["dtype"] in ("int32", "int64")
                    and not (set(node.kwargs) - {"dtype"})
                    and len(node.args) <= 2
                    and (
                        schemas[source_ir["column"]]["dtype"] == "int64"
                        or all(
                            (
                                str(user.target) == "aten.gather.default"
                                and user.args[2] is node
                            )
                            or (
                                str(user.target) == "aten.cross_entropy_loss.default"
                                and user.args[1] is node
                            )
                            for user in node.users
                        )
                    )
                ):
                    # Preserve the direct edge for server vocabulary checks.
                    # Gather accepts int32; CE widens only the active tile.
                    indices[node] = indices[source]
                    bounded_nodes.add(node)
                    if source in index_columns:
                        index_columns.add(node)
                    continue
                if (
                    dtype != torch.float32
                    or set(node.kwargs) - {"dtype"}
                    or len(node.args) > 2
                ):
                    raise ValueError(
                        "only float32 loss and int64 input-index casts are supported"
                    )
                ir = {"op": "float", "args": [argument(node.args[0])]}
            elif target == "aten.log_softmax.int":
                normalization_dtype = (
                    node.args[2] if len(node.args) > 2 else node.kwargs.get("dtype")
                )
                if (
                    not 2 <= len(node.args) <= 3
                    or node.args[1] not in (-1, 1)
                    or set(node.kwargs) - {"dtype"}
                    or normalization_dtype not in (None, torch.float32)
                ):
                    raise ValueError(
                        "log_softmax requires the vocabulary axis and native or float32 dtype"
                    )
                if node.args[0] not in logits_nodes:
                    raise ValueError(
                        "log_softmax requires logits, temperature scaling, or detach"
                    )
                ir = {"op": "log_softmax", "args": [argument(node.args[0])]}
                if normalization_dtype is not None:
                    ir["dtype"] = "float32"
                normalized_nodes.add(node)
            elif target == "aten.gather.default":
                if (
                    len(node.args) != 3
                    or node.kwargs
                    or node.args[1] not in (-1, 1)
                    or node.args[0] not in normalized_nodes
                    or node.args[2] not in index_columns
                ):
                    raise ValueError(
                        "gather requires last-axis log_softmax values and a rank-2 int32/int64 index column"
                    )
                ir = {
                    "op": "gather",
                    "args": [argument(node.args[0]), argument(node.args[2])],
                }
            elif target == "aten.cross_entropy_loss.default":
                args = node.args
                if (
                    len(args) > 4
                    or len(args) < 4
                    or args[2:] != (None, 0)
                    or node.kwargs
                ):
                    raise ValueError(
                        "cross_entropy requires reduction='none', default ignore_index, and no class weights"
                    )
                ir = {"op": "ce", "args": [argument(args[0]), argument(args[1])]}
            elif op in reductions:
                source = node.args[0]
                rank = source.meta["val"].ndim
                overload = target.rsplit(".", 1)[1]
                allowed = {
                    "sum": {"default", "dim_IntList"},
                    "mean": {"default", "dim"},
                    "amin": {"default"},
                    "amax": {"default"},
                    "logsumexp": {"default"},
                    "var": {"default", "dim", "correction"},
                    "std": {"default", "dim", "correction"},
                }
                if (
                    overload not in allowed[op]
                    or source not in bounded_nodes
                    or not source.meta["val"].is_floating_point()
                ):
                    raise ValueError(
                        "per-example reductions require bounded floating selected values"
                    )
                args = list(node.args[1:])
                kwargs = dict(node.kwargs)
                correction = None
                if op in {"var", "std"} and overload == "default":
                    unbiased = args.pop(0) if args else True
                    if type(unbiased) is not bool:
                        raise ValueError("variance unbiased must be a boolean")
                    correction = int(unbiased)
                    dims = None
                else:
                    dims = args.pop(0) if args else None
                    if op in {"var", "std"}:
                        if overload == "correction":
                            correction = kwargs.pop("correction", None)
                            correction = 1 if correction is None else correction
                        else:
                            unbiased = args.pop(0) if args else True
                            if type(unbiased) is not bool:
                                raise ValueError("variance unbiased must be a boolean")
                            correction = int(unbiased)
                keepdim = args.pop(0) if args else kwargs.pop("keepdim", False)
                if args or kwargs or keepdim is not False:
                    raise ValueError(
                        "reductions require keepdim=False and no dtype override"
                    )
                if correction is not None and (
                    type(correction) is not int or correction < 0
                ):
                    raise ValueError(
                        "variance correction must be a nonnegative integer"
                    )
                axes = list(range(rank)) if dims is None or dims == [] else list(dims)
                if any(
                    type(axis) is not int or not -rank <= axis < rank for axis in axes
                ):
                    raise ValueError("unsupported reduction axes")
                axes = [axis % rank for axis in axes]
                if sorted(axes) == list(range(rank)) and rank in (1, 2):
                    ir = {"op": op, "args": [argument(source)]}
                    if correction is not None:
                        ir["correction"] = correction
                elif op == "sum" and rank == 2 and axes == [1]:
                    ir = {"op": "sum_candidates", "args": [argument(source)]}
                else:
                    raise ValueError(
                        "only per-example reductions or sum over the candidate axis are supported"
                    )
            elif (
                op in binary
                and target in {f"aten.{op}.Tensor", f"aten.{op}.default"}
                and len(node.args) == 2
                and not node.kwargs
            ):
                ir = {"op": op, "args": [argument(arg) for arg in node.args]}
            elif (
                op in unary
                and target == f"aten.{op}.default"
                and len(node.args) == 1
                and not node.kwargs
            ):
                ir = {"op": op, "args": [argument(node.args[0])]}
            elif (
                target == "aten.square.default"
                and len(node.args) == 1
                and not node.kwargs
            ) or (
                target == "aten.pow.Tensor_Scalar"
                and len(node.args) == 2
                and type(node.args[1]) in (int, float)
                and node.args[1] == 2
                and not node.kwargs
            ):
                value = argument(node.args[0])
                ir = {"op": "mul", "args": [value, value]}
            elif target == "aten.clamp.default":
                if not 2 <= len(node.args) <= 3 or node.kwargs:
                    raise ValueError("clamp requires finite scalar bounds")
                bounds = [
                    (op, bound)
                    for op, bound in zip(("clamp_min", "clamp_max"), node.args[1:])
                    if bound is not None
                ]
                if not bounds or any(
                    type(item[1]) not in (int, float) or not np.isfinite(item[1])
                    for item in bounds
                ):
                    raise ValueError("clamp requires finite scalar bounds")
                value = argument(node.args[0])
                for op, bound in bounds[:-1]:
                    nodes.append(
                        {
                            "op": op,
                            "args": [value, argument(bound)],
                            "source": str(node.meta.get("stack_trace", node.name))[
                                -512:
                            ],
                        }
                    )
                    value = {"node": len(nodes) - 1}
                op, bound = bounds[-1]
                ir = {"op": op, "args": [value, argument(bound)]}
            elif (
                target == "aten.clamp_min.default"
                and len(node.args) == 2
                and not node.kwargs
            ):
                ir = {"op": "clamp_min", "args": [argument(arg) for arg in node.args]}
            elif (
                target == "aten.clamp_max.default"
                and len(node.args) == 2
                and not node.kwargs
            ):
                ir = {"op": "clamp_max", "args": [argument(arg) for arg in node.args]}
            else:
                raise ValueError(
                    f"unsupported loss operator {target} at {node.meta.get('stack_trace', node.name)}"
                )
        else:
            raise ValueError(f"unsupported loss node {node.op}")
        if (
            ir["op"] == "logits"
            or (ir["op"] == "detach" and node.args[0] in logits_nodes)
            or (
                ir["op"] == "div"
                and node.args[0] in logits_nodes
                and type(node.args[1]) in (int, float)
                and np.isfinite(node.args[1])
                and node.args[1] > 0
            )
        ):
            logits_nodes.add(node)
        if ir["op"] == "detach" and node.args[0] in normalized_nodes:
            normalized_nodes.add(node)
        if node in normalized_nodes and any(
            user.op != "call_function"
            or str(user.target) not in {"aten.gather.default", "aten.detach.default"}
            or user.args[0] is not node
            for user in node.users
        ):
            raise ValueError(
                "log_softmax values only support gather or detach consumers"
            )
        # Provenance is independent of autograd: detach must not turn a model
        # summary into an input scalar that can be broadcast back over tokens.
        model = ir["op"] == "logits" or any(
            source in model_nodes for source in node.all_input_nodes
        )
        scalar = getattr(node.meta.get("val"), "ndim", None) == 0
        if not scalar and any(
            source in scalar_nodes and source in model_nodes
            for source in node.all_input_nodes
        ):
            raise ValueError(
                "model-dependent scalars cannot feed token or candidate tensors"
            )
        if model:
            model_nodes.add(node)
        if scalar:
            scalar_nodes.add(node)
        if ir["op"] in {"input", "ce", "gather"} or (
            not scalar
            and node.all_input_nodes
            and all(
                source in bounded_nodes or source in scalar_nodes
                for source in node.all_input_nodes
            )
        ):
            bounded_nodes.add(node)
        ir["source"] = str(node.meta.get("stack_trace", node.name))[-512:]
        indices[node] = len(nodes)
        nodes.append(ir)
    # Graph v2 fixes reductions/finalization to independent example scope.
    graph = {"version": 2, "columns": schemas, "nodes": nodes, **outputs}
    payload = json.dumps(
        graph, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()
    if len(nodes) > MAX_NODES or len(payload) > MAX_GRAPH_BYTES:
        raise ValueError(
            "objective exceeds graph node/byte budget; simplify the objective"
        )
    return graph
