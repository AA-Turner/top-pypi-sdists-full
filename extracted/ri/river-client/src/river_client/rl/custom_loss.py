"""Adapt rollout datums to prepared custom objectives."""

import json
from collections.abc import Callable
from dataclasses import asdict

import numpy as np

from river_client.losses import CustomLoss

from .checkpoint import fingerprint
from .requirements import LossRequirements


_INPUTS = {
    "targets": "int64",
    "old_logprobs": "float32",
    "advantages": "float32",
    "mask": "float32",
}


def validate_custom_loss_inputs(loss: CustomLoss, custom_loss_inputs: Callable | None):
    if custom_loss_inputs is not None:
        if not callable(custom_loss_inputs):
            raise TypeError("custom_loss_inputs must be callable")
        return
    if any(_INPUTS.get(name) != spec for name, spec in loss.inputs.items()):
        raise ValueError(
            "custom RL inputs must use targets:int64 and/or "
            "old_logprobs, advantages, mask:float32; "
            "provide custom_loss_inputs for other columns or shapes"
        )


def loss_contract(
    loss: CustomLoss,
    custom_loss_inputs: Callable | None,
    *,
    requirements=LossRequirements(),
):
    from river_client._loss_capture import _graph_formula

    return {
        **(
            {"requirements": asdict(requirements)}
            if requirements != LossRequirements()
            else {}
        ),
        "graph": fingerprint(_graph_formula(json.loads(loss._graph))),
        "inputs": None if custom_loss_inputs is None else custom_loss_inputs.contract(),
    }


def custom_batch(data, loss: CustomLoss, custom_loss_inputs: Callable | None):
    result = []
    for datum in data:
        if "model_input" in datum:
            # Image targets are placeholders; the trajectory mask excludes them.
            ids = [
                token
                for chunk in datum["model_input"]
                for token in (
                    chunk["tokens"]
                    if chunk["type"] == "text"
                    else [0] * chunk["expected_tokens"]
                )
            ]
        else:
            ids = datum["input_ids"]
        columns = {
            "targets": [*ids[1:], 0],
            "old_logprobs": datum["old_logprobs"],
            "advantages": datum["advantages"],
            "mask": datum["loss_mask"],
        }
        converted = {
            k: v
            for k, v in datum.items()
            if k not in {"old_logprobs", "advantages", "loss_mask"}
        }
        converted["loss_data"] = columns
        columns = (
            custom_loss_inputs(converted)
            if custom_loss_inputs is not None
            else {name: columns[name] for name in loss.inputs}
        )
        converted.pop("sampling_metadata", None)
        converted["loss_data"] = {
            name: np.asarray(values).tolist() for name, values in columns.items()
        }
        result.append(converted)
    return result
