"""Accumulate finalized example losses and validate deferred advantage scaling."""

import json
import math
from functools import cache
from itertools import chain

import numpy as np

from .custom_loss import custom_batch


class StreamingCustomLoss:
    def __init__(self, loss, *, batch_standardize, custom_loss_inputs):
        graph = json.loads(loss._graph)
        nodes, columns = graph["nodes"], graph["columns"]

        @cache
        def advantage_degree(index):
            node = nodes[index]
            op = node["op"]
            if op == "input":
                return int(columns[node["column"]]["name"] == "advantages")
            degrees = [
                advantage_degree(arg["node"]) if "node" in arg else 0
                for arg in node.get("args", [])
            ]
            if not any(degree != 0 for degree in degrees):
                return 0
            if None in degrees:
                return None
            if op in {
                "neg",
                "float",
                "detach",
                "sum_candidates",
                "sum",
                "mean",
                "amin",
                "amax",
                "std",
            }:
                return degrees[0]
            if op == "var":
                return 2 * degrees[0]
            if op == "mul":
                return sum(degrees)
            if op == "div" and degrees[1] == 0:
                return degrees[0]
            if op in {"add", "sub", "minimum", "maximum"}:
                if degrees[0] == degrees[1]:
                    return degrees[0]
                for arg in node["args"]:
                    if arg.get("constant") == 0:
                        return max(degrees)
            if op in {"clamp_min", "clamp_max"}:
                if node["args"][1].get("constant") == 0:
                    return degrees[0]
            return None

        # Every submitted datum is a complete example. Its reductions and scalar
        # tail must stay in the server graph; only batch advantage scaling is deferred.
        self.degrees = {}
        for name, index in {
            "loss": graph["loss"],
            **{f"custom/{key}": val for key, val in graph["metrics"].items()},
        }.items():
            degree = advantage_degree(index) if batch_standardize else 0
            if degree not in {0, 1}:
                raise ValueError(
                    "streaming CustomLoss with batch-standardized advantages requires "
                    "each output to be positively homogeneous of degree one in "
                    "advantages (or independent of them); disable batch "
                    "standardization or backward overlap for other objectives"
                )
            self.degrees[name] = degree

        self.loss = loss
        self.custom_loss_inputs = custom_loss_inputs
        self.group_order = []
        self.dtypes = {c["name"]: c["dtype"] for c in columns}

    def finish(self, data, chunks, results, advantage_scale):
        if len(data) != sum(map(len, chunks)):
            raise ValueError(
                "streamed custom inputs changed before the optimizer update"
            )
        # Only an input adapter can change inputs between the streamed and
        # complete preparations. Datums are built one at a time.
        pairs = (
            zip(data, chain.from_iterable(chunks), strict=True)
            if self.custom_loss_inputs is not None
            else ()
        )
        for datum, partial in pairs:
            final = custom_batch([datum], self.loss, self.custom_loss_inputs)[0]
            if not _same_inputs(
                {k: v for k, v in final.items() if k != "loss_data"},
                {k: v for k, v in partial.items() if k != "loss_data"},
            ):
                raise ValueError("streamed custom model inputs changed")
            for name, dtype in self.dtypes.items():
                actual = np.asarray(final["loss_data"][name], dtype=dtype)
                expected = np.asarray(partial["loss_data"][name], dtype=dtype)
                if name == "advantages":
                    expected = expected * advantage_scale
                matches = actual.shape == expected.shape and (
                    np.allclose(actual, expected, rtol=2e-6, atol=0, equal_nan=False)
                    if name == "advantages"
                    else np.array_equal(actual, expected)
                )
                if not matches:
                    raise ValueError(
                        f"custom_loss_inputs changed {name!r} across streamed and "
                        "complete-batch preparation; optimizer update aborted"
                    )
        scales = {
            name: advantage_scale**degree for name, degree in self.degrees.items()
        }
        return {
            name: math.fsum(result.metrics[name] for result in results) * scale
            for name, scale in scales.items()
        }, scales["loss"]


def _same_inputs(left, right):
    """Compare datum fields that may hold NumPy arrays."""
    if isinstance(left, np.ndarray) or isinstance(right, np.ndarray):
        return np.array_equal(left, right)
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(
            _same_inputs(left[k], right[k]) for k in left
        )
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(map(_same_inputs, left, right))
    return left == right
