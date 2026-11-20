# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
What a policy of its own inputs and outputs declares of them, done where its code runs: the last step before its code
is handed an act's inputs, the first after its code answers - a deployment's worker and a policy server of your own
alike, this one module in both.

  * an observation its infer - or its observe method, where it has one - annotates torch.Tensor, alone or in a dict or a
    list (wants_tensors): each array reaches it as a torch tensor on the device it runs on - float64 as float32, any
    other dtype as it is - with a batch dimension of 1 first; each tensor it answers with goes back as an array, that
    dimension taken off. A @seq.concurrent policy's acts are a batch already, its list: each is handed, and answers,
    without that dimension, and its batch is stacked by engine.stack.
  * Every policy's answer, declared or not (`arrays`): each torch tensor in it, at any depth of its dicts and lists,
    leaves as a numpy array of its dtype - bfloat16 and the float8 kinds as float32, complex32 as complex64, which numpy
    has no dtype for and which hold each of their values exactly - so an act answered in msgpack carries an array, one
    in JSON its list, and an eval's the same as a robot's.

In one sentence: the policy's adapter (engine.adapter) builds its Conversions at load from its methods' annotations
(`of`) → converts each observation before its observe or infer method is handed it (`observation`) → converts what
infer returns (`answer`); a policy whose methods take no tensors is handed its inputs, and its answers leave,
untouched. A camera's frame reaches the policy as its robot sent it: nothing here decodes one.

WHY where its code runs: the tensors go on the policy's card, which only that process holds. WHY no unit batch
dimension for a @seq.concurrent policy: its list is the batch - each act with a dimension of 1 would stack into
(B, 1, ...).
"""
from __future__ import annotations

import inspect
import re
import sys
from typing import Any

__all__ = ["ConversionError", "Conversions", "InputsRejected", "arrays", "of", "tensor_array", "wants_tensors"]


class InputsRejected(ValueError):
    """An act's inputs that do not parse as what its policy is handed - the caller's error, answered 400 before the
    policy runs. `reason`: what the 400 says in details.reason - "observation" unless said otherwise ("reserved_key": a
    frame holding a key of the platform's; "no_observation": an episode with none yet to hand an act function)."""

    reason = "observation"

    def __init__(self, message: str = "", reason: str | None = None) -> None:
        super().__init__(message)
        if reason is not None:
            self.reason = reason


class ConversionError(InputsRejected):
    """An observation that does not hold what its policy declares it reads, said by key and why: the caller's error
    (400), as inputs that are not the robot-arm preset's Observation are."""


# A method's first parameter annotated a torch tensor: `torch.Tensor`, alone or in a generic (`dict[str, torch.Tensor]`,
# `list[torch.Tensor]`), the annotation itself or its text - `Tensor` alone as imported from torch.
_TENSOR = re.compile(r"(?<![\w.])Tensor\b|\btorch\.Tensor\b")


def wants_tensors(method: Any) -> bool:
    """Whether `method` (a bound infer or observe) takes its observation as torch tensors: its first parameter's
    annotation names torch.Tensor."""
    try:
        params = [p for p in inspect.signature(method).parameters.values()
                  if p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]
    except (TypeError, ValueError):
        return False
    note = params[0].annotation if params else inspect.Parameter.empty
    if note is inspect.Parameter.empty:
        return False
    return bool(_TENSOR.search(note if isinstance(note, str) else repr(note)))


def of(infer: Any, *, io_mode: str = "raw", observe: Any = None) -> "Conversions | None":
    """What a policy's methods take as torch tensors - its observe method's observation where it has one, else its
    infer's (wants_tensors) - or None when they take none."""
    if not wants_tensors(observe if observe is not None else infer):
        return None
    if io_mode != "raw":
        raise TypeError("an observation annotated torch.Tensor is for a policy of its own inputs and outputs; "
                        "this one's infer is written against the robot-arm preset, and is handed an Observation")
    return Conversions(tensors=True)


class Conversions:
    """One policy's conversions (see the module docstring). Built once, at its load: without torch in its image, a
    policy whose methods take tensors fails there - where its deploy's build checks it - not at its first act."""

    def __init__(self, *, tensors: bool = False, batch: bool = True) -> None:
        self.batch = bool(tensors) and batch
        self._torch = self._device = None
        if tensors:
            try:
                import torch
            except ImportError:
                raise ImportError("its infer takes torch tensors (annotated torch.Tensor), and its image has no torch: "
                                  "install it in the image (e.g. .uv_pip_install(\"torch\"))") from None
            self._torch = torch
            self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def observation(self, obs: Any, *, alone: bool = True) -> Any:
        """One observation - an act's inputs, or a frame its observe method is handed - as the policy's code is handed
        it. `alone`: the act is no @seq.concurrent batch's, so it takes the unit batch dimension
        tensors are handed with."""
        if self._torch is None:
            return obs
        if isinstance(obs, dict):
            return {k: self._tensors(v, str(k), alone) for k, v in obs.items()}
        return self._tensors(obs, "the observation", alone)

    def answer(self, value: Any, *, alone: bool = True) -> Any:
        """What the policy's code returned, for the wire: each torch tensor in it an array, the unit batch dimension it
        was handed taken off. Untouched where its methods take no tensors."""
        return value if self._torch is None else self._arrays(value, "the answer", alone)

    def _tensors(self, value: Any, where: str, alone: bool) -> Any:
        import numpy as np

        if isinstance(value, np.ndarray):
            return self._tensor(value, where, alone=alone)
        if isinstance(value, dict):
            return {k: self._tensors(v, f"{where}.{k}", alone) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return type(value)(self._tensors(v, f"{where}[{i}]", alone) for i, v in enumerate(value))
        return value

    def _tensor(self, array: Any, where: str, *, alone: bool = True) -> Any:
        torch = self._torch
        try:
            # an array read off the wire is read-only, and a tensor on the CPU would share its memory
            t = torch.from_numpy(array if array.flags.writeable else array.copy())
        except TypeError as exc:
            raise ConversionError(f"{where}: an array of {array.dtype} has no torch tensor ({exc})") from None
        t = t.to(self._device)                                      # a frame crosses as uint8, a quarter of its floats
        if t.dtype == torch.float64:
            t = t.to(torch.float32)
        return t.unsqueeze(0) if self.batch and alone else t

    def _arrays(self, value: Any, where: str, alone: bool) -> Any:
        torch = self._torch
        if isinstance(value, torch.Tensor):
            t = value.detach()
            if self.batch and alone and t.dim() > 0:
                if t.shape[0] != 1:
                    raise ValueError(f"a tensor the policy answers with has the batch "
                                     f"dimension it was handed first, of 1; {where} has shape {tuple(t.shape)}")
                t = t[0]
            return tensor_array(t)
        if isinstance(value, dict):
            return {k: self._arrays(v, f"{where}.{k}", alone) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return type(value)(self._arrays(v, f"{where}[{i}]", alone) for i, v in enumerate(value))
        return value


def arrays(value: Any) -> Any:
    """A policy's answer with each torch tensor in it - at any depth of its dicts, lists and tuples - a numpy array of
    its dtype (tensor_array); as it is when torch was never imported, as then nothing in it is a tensor."""
    torch = sys.modules.get("torch")
    return value if torch is None else _untorched(value, torch.Tensor)


def _untorched(value: Any, tensor: type) -> Any:
    if isinstance(value, tensor):
        return tensor_array(value)
    if isinstance(value, dict):
        return {k: _untorched(v, tensor) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_untorched(v, tensor) for v in value]
    return value


def tensor_array(t: Any) -> Any:
    """A torch tensor as a numpy array of its dtype - detached, on the CPU, a view's conjugation or negation resolved, a
    quantized one's values and a sparse one's whole - but for the dtypes numpy has none for: bfloat16 and the float8
    kinds as float32, complex32 as complex64, each of their values held exactly. One numpy holds no array of
    raises TypeError, naming its dtype."""
    torch = sys.modules["torch"]
    t = t.detach()
    if t.is_quantized:
        t = t.dequantize()
    if t.layout != torch.strided:
        t = t.to_dense()
    name = str(t.dtype).removeprefix("torch.")
    if name == "bfloat16" or name.startswith("float8"):
        t = t.to(torch.float32)
    elif name == "complex32":
        t = t.to(torch.complex64)
    t = t.cpu().resolve_conj().resolve_neg()
    try:
        return t.numpy()
    except (TypeError, RuntimeError) as exc:
        raise TypeError(f"infer() answered a torch tensor of {t.dtype}, which has no numpy array ({exc}): turn it into "
                        "one numpy has, e.g. .float()") from None
