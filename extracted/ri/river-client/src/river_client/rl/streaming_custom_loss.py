"""Prove and finalize additive custom-loss accumulation."""

import json
import math
from functools import cache

import numpy as np

from .custom_loss import custom_batch


class StreamingCustomLoss:
    def __init__(self, loss, *, batch_standardize, custom_loss_inputs):
        graph = json.loads(loss._graph)
        nodes, columns = graph["nodes"], graph["columns"]

        def reject():
            raise ValueError(
                "streaming CustomLoss requires additive sums, optionally divided by "
                "mask.sum().clamp_min(1); batch-standardized advantages must be "
                "positively homogeneous of degree one (or absent)"
            )

        @cache
        def advantage_degree(index):
            node = nodes[index]
            op = node["op"]
            if op == "sum":
                reject()
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
            if op in {"neg", "float", "detach", "sum_candidates"}:
                return degrees[0]
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

        @cache
        def extract_numerator(index):
            node = nodes[index]
            op, args = node["op"], node.get("args", [])
            if op == "sum":
                return index, False, advantage_degree(args[0]["node"])
            if op == "div" and mask_denominator(args[1]):
                numerator, mean, degree = extract_numerator(args[0]["node"])
                if mean:
                    reject()
                return numerator, True, degree
            if op in {"neg", "float", "detach"}:
                positions = [0]
            elif op in {"add", "sub"} and all("node" in a for a in args):
                positions = [0, 1]
            elif op in {"mul", "div"} and "constant" in args[1]:
                positions = [0]
            elif op == "mul" and "constant" in args[0]:
                positions = [1]
            else:
                reject()
            terms = [extract_numerator(args[p]["node"]) for p in positions]
            mean, degree = terms[0][1:]
            if any(term[1] != mean for term in terms):
                reject()
            if any(term[2] != degree for term in terms):
                degree = None
            rewritten = args.copy()
            for position, term in zip(positions, terms, strict=True):
                rewritten[position] = {"node": term[0]}
            if rewritten != args:
                index = len(nodes)
                nodes.append(node | {"args": rewritten})
            return index, mean, degree

        def mask_denominator(arg):
            if "node" not in arg:
                return False
            node = nodes[arg["node"]]
            if node["op"] != "clamp_min" or node["args"][1] != {"constant": 1.0}:
                return False
            node = nodes[node["args"][0]["node"]]
            if node["op"] != "sum":
                return False
            node = nodes[node["args"][0]["node"]]
            return node["op"] == "input" and columns[node["column"]] == {
                "name": "mask",
                "dtype": "float32",
                "layout": "token",
            }

        self.outputs = {}
        for name, index in {
            "loss": graph["loss"],
            **{f"custom/{key}": val for key, val in graph["metrics"].items()},
        }.items():
            numerator, mean, degree = extract_numerator(index)
            if batch_standardize and degree not in {0, 1}:
                reject()
            self.outputs[name] = (numerator, mean, degree if batch_standardize else 0)

        needed = {
            i for i, node in enumerate(nodes) if node["op"] in {"logits", "input"}
        }

        def retain(index):
            if index not in needed:
                needed.add(index)
                for arg in nodes[index].get("args", []):
                    if "node" in arg:
                        retain(arg["node"])

        for index, mean, degree in self.outputs.values():
            retain(index)
        indices = {old: new for new, old in enumerate(sorted(needed))}
        graph["nodes"] = [
            node
            | (
                {
                    "args": [
                        {"node": indices[a["node"]]} if "node" in a else a
                        for a in node["args"]
                    ]
                }
                if "args" in node
                else {}
            )
            for i, node in enumerate(nodes)
            if i in needed
        ]
        graph["loss"] = indices[self.outputs["loss"][0]]
        graph["metrics"] = {
            key: indices[self.outputs[f"custom/{key}"][0]] for key in graph["metrics"]
        }
        self.graph = json.dumps(graph, separators=(",", ":"), allow_nan=False).encode()
        self.loss = None
        self.custom_loss_inputs = custom_loss_inputs
        self.group_order = []
        self.dtypes = {c["name"]: c["dtype"] for c in columns}

    def finish(self, data, chunks, results, advantage_scale):
        streamed = [datum for chunk in chunks for datum in chunk]
        if len(data) != len(streamed):
            raise ValueError(
                "streamed custom inputs changed before the optimizer update"
            )
        mask_sums = []
        for datum, partial in zip(data, streamed, strict=True):
            if self.custom_loss_inputs is None:
                if "mask" in self.dtypes:
                    mask_sums.append(
                        float(
                            np.asarray(datum["loss_mask"], dtype=np.float32).sum(
                                dtype=np.float64
                            )
                        )
                    )
                continue
            final = custom_batch([datum], self.loss, self.custom_loss_inputs)[0]
            if {k: v for k, v in final.items() if k != "loss_data"} != {
                k: v for k, v in partial.items() if k != "loss_data"
            }:
                raise ValueError("streamed custom model inputs changed")
            for name, dtype in self.dtypes.items():
                actual = np.asarray(final["loss_data"][name], dtype=dtype)
                expected = np.asarray(partial["loss_data"][name], dtype=dtype)
                if name == "mask":
                    mask_sums.append(float(actual.sum(dtype=np.float64)))
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
        denominator = 1.0
        if any(mean for index, mean, degree in self.outputs.values()):
            denominator = float(np.float32(math.fsum(mask_sums)))
            if not math.isfinite(denominator):
                raise ValueError("custom loss mask sum must be finite")
            denominator = max(1.0, denominator)
        scales = {
            name: advantage_scale**degree / (denominator if mean else 1.0)
            for name, (index, mean, degree) in self.outputs.items()
        }
        return {
            name: math.fsum(result.metrics[name] for result in results) * scale
            for name, scale in scales.items()
        }, scales["loss"]
