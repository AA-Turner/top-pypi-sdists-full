"""Adapt rollout datums to prepared custom objectives."""

import json
import threading
from collections.abc import Callable
from dataclasses import asdict
from functools import partial

import numpy as np

from river_client.losses import CustomLoss, _input_array, _input_columns

from .batch import TrainingBatch
from .checkpoint import fingerprint
from .requirements import LossRequirements

_ADAPTER_LOCK = threading.Lock()


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
    """Convert datums into the custom loss's declared inputs.

    A ``TrainingBatch`` converts each datum when it is built, so the adapter
    may run again for the same trajectory (for example on replay).
    """
    if isinstance(data, TrainingBatch):
        return data.with_items(custom=partial(_custom_datum, loss, custom_loss_inputs))
    schemas = {column["name"]: column for column in _input_columns(loss.inputs)}
    result = []
    for datum in data:
        if "model_input" in datum:
            # Image targets are placeholders; the trajectory mask excludes them.
            ids = np.concatenate(
                [
                    chunk["tokens"]
                    if chunk["type"] == "text"
                    else np.zeros(chunk["expected_tokens"], dtype=np.int64)
                    for chunk in datum["model_input"]
                ],
                dtype=np.int64,
            )
        else:
            ids = np.asarray(datum["input_ids"], dtype=np.int64)
        columns = {
            "targets": np.append(ids[1:], 0),
            "old_logprobs": np.asarray(datum["old_logprobs"], dtype=np.float32),
            "advantages": np.asarray(datum["advantages"], dtype=np.float32),
            "mask": np.asarray(datum["loss_mask"], dtype=np.float32),
        }
        converted = {
            k: v
            for k, v in datum.items()
            if k not in {"old_logprobs", "advantages", "loss_mask"}
        }
        converted["loss_data"] = columns
        # Datums can be built on several threads at once, for example by a
        # submission and a checkpoint save. Adapters are never called
        # concurrently, and their outputs are copied before another call.
        with _ADAPTER_LOCK:
            columns = (
                custom_loss_inputs(converted)
                if custom_loss_inputs is not None
                else {name: columns[name] for name in loss.inputs}
            )
            if columns.keys() != schemas.keys():
                raise ValueError("custom loss inputs differ from the declared schema")
            columns = {
                name: _input_array(values, schemas[name]).copy()
                for name, values in columns.items()
            }
        converted.pop("sampling_metadata", None)
        converted["loss_data"] = columns
        result.append(converted)
    return result


def _custom_datum(loss, custom_loss_inputs, datum):
    (converted,) = custom_batch([datum], loss, custom_loss_inputs)
    return converted
