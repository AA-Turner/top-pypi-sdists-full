"""Capture tensor objectives as bounded, data-only loss graphs."""

from __future__ import annotations

import hashlib
import json
import operator
import os
from concurrent.futures import ThreadPoolExecutor

import sympy

from .losses import LossInputs, LossObjective, _input_columns

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
            array = np.asarray(datum["loss_data"][name])
            if array.dtype.kind in "iu":
                array = array.astype(np.int64)
            elif array.dtype.kind == "f":
                array = array.astype(np.float32)
            else:
                raise TypeError(f"loss_data[{name!r}] must contain integers or floats")
            schema = schemas[column_index]
            expected = (length,) + ((schema["width"],) if "width" in schema else ())
            if array.shape != expected or not np.isfinite(array).all():
                raise ValueError(
                    f"data[{index}].loss_data[{name!r}]: expected finite shape {expected}"
                )
            if str(array.dtype) != schema["dtype"]:
                raise ValueError(
                    f"data[{index}].loss_data[{name!r}]: dtype does not match declared schema"
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
    if not (2, 4) <= version < (2, 12):
        raise ValueError("Custom loss capture requires PyTorch >=2.4,<2.12")
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
    logprob_sources = {}
    placeholders = iter(
        [{"op": "logits"}] + [{"op": "input", "column": i} for i in range(len(names))]
    )
    binary = {"add", "sub", "mul", "div", "minimum", "maximum"}
    unary = {"neg", "exp", "expm1", "log", "detach"}

    def argument(arg):
        if isinstance(arg, torch.fx.Node):
            return {"node": indices[arg]}
        if type(arg) in (int, float) and np.isfinite(arg):
            return {"constant": float(arg)}
        raise ValueError(f"unsupported loss argument: {type(arg).__name__}")

    for node in exported.graph.nodes:
        if node.op == "placeholder":
            ir = next(placeholders)
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
                if (
                    dtype != torch.float32
                    or set(node.kwargs) - {"dtype"}
                    or len(node.args) > 2
                ):
                    raise ValueError("only float32 loss casts are supported")
                ir = {"op": "float", "args": [argument(node.args[0])]}
            elif target == "aten.log_softmax.int":
                if len(node.args) != 2 or node.args[1] not in (-1, 1) or node.kwargs:
                    raise ValueError(
                        "selected logprobs require native log_softmax over vocabulary"
                    )
                if node.args[0] not in logits_nodes or any(
                    user.op != "call_function"
                    or str(user.target) != "aten.gather.default"
                    or user.args[0] is not node
                    for user in node.users
                ):
                    raise ValueError(
                        "log_softmax is only supported when gathering target logprobs"
                    )
                logprob_sources[node] = node.args[0]
                continue
            elif target == "aten.gather.default":
                if (
                    len(node.args) != 3
                    or node.kwargs
                    or node.args[1] not in (-1, 1)
                    or node.args[0] not in logprob_sources
                ):
                    raise ValueError(
                        "only vocabulary gather following log_softmax is supported"
                    )
                ir = {
                    "op": "selected_logprobs",
                    "args": [
                        argument(logprob_sources[node.args[0]]),
                        argument(node.args[2]),
                    ],
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
            elif (
                target == "aten.sum.default" and len(node.args) == 1 and not node.kwargs
            ):
                ir = {"op": "sum", "args": [argument(node.args[0])]}
            elif target == "aten.sum.dim_IntList":
                if (
                    len(node.args) != 2
                    or node.kwargs
                    or list(node.args[1]) not in ([-1], [1])
                    or node.args[0].meta["val"].ndim != 2
                ):
                    raise ValueError(
                        "only reduction over the candidate axis is supported"
                    )
                ir = {"op": "sum_candidates", "args": [argument(node.args[0])]}
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
        if ir["op"] == "logits" or (
            ir["op"] in ("detach", "div") and node.args[0] in logits_nodes
        ):
            logits_nodes.add(node)
        ir["source"] = str(node.meta.get("stack_trace", node.name))[-512:]
        indices[node] = len(nodes)
        nodes.append(ir)
    graph = {"version": 1, "columns": schemas, "nodes": nodes, **outputs}
    payload = json.dumps(
        graph, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()
    if len(nodes) > MAX_NODES or len(payload) > MAX_GRAPH_BYTES:
        raise ValueError(
            "objective exceeds graph node/byte budget; simplify the objective"
        )
    return graph
