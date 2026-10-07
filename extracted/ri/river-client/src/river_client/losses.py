"""Loss definitions for River's forward and training methods."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from torch import Tensor


LossInputs = Mapping[str, str | Mapping[str, object]]


def _input_columns(inputs: LossInputs) -> list[dict]:
    if not isinstance(inputs, Mapping) or not 1 <= len(inputs) <= 16:
        raise ValueError("inputs must declare 1..16 named int64/float32 columns")
    if any(not isinstance(name, str) or not 1 <= len(name) <= 64 for name in inputs):
        raise ValueError("input columns must have names containing 1..64 characters")
    columns = []
    for name, spec in sorted(inputs.items()):
        column = {"name": name, "layout": "token"}
        if isinstance(spec, str):
            dtype = spec
        elif isinstance(spec, Mapping) and set(spec) == {"dtype", "shape"}:
            dtype, shape = spec["dtype"], spec["shape"]
            if (
                not isinstance(shape, (tuple, list))
                or len(shape) != 2
                or shape[0] != "T"
                or type(shape[1]) is not int
                or not 1 <= shape[1] <= 262144
            ):
                raise ValueError(
                    "matrix inputs require shape ('T', K), with 1 <= K <= 262144"
                )
            column["width"] = shape[1]
        else:
            raise ValueError(
                "input declarations require a dtype or a dtype and token shape"
            )
        if dtype not in ("int64", "float32"):
            raise ValueError("inputs require int64/float32 columns")
        columns.append(column | {"dtype": dtype})
    return columns


class LossObjective(Protocol):
    def __call__(
        self, logits: Tensor, inputs: dict[str, Tensor]
    ) -> Tensor | tuple[Tensor, dict[str, Tensor]]: ...


class Loss(ABC):
    """A loss definition accepted by Model's forward and training methods."""

    @abstractmethod
    def _resolve(self) -> tuple[str | LossObjective, dict[str, float]]:
        """Resolve to an existing wire name or a client-captured objective."""


@dataclass(frozen=True)
class BuiltinLoss(Loss):
    """A built-in loss with copied configuration; duplicate options are errors."""

    name: str
    config: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("built-in loss name must be a nonempty string")
        object.__setattr__(self, "config", MappingProxyType(dict(self.config)))

    def _resolve(self) -> tuple[str, dict[str, float]]:
        return self.name, dict(self.config)


@dataclass(frozen=True)
class CustomLoss(Loss):
    """A tensor objective with declared inputs; call model.prepare_loss before use.

    Return a scalar or (scalar, dict of scalar metrics). The result's loss
    preserves the objective's reduction without additional averaging. Named
    metrics use the custom/ prefix. Built-in loss diagnostics and per-token
    logprobs are not returned.

    The CPU-captured graph defines the formula executed on the server. Device
    branching is unsupported and may be frozen during capture; CUDA is not
    required on the client. Install river-client[custom-loss] for capture.

    Inputs and targets are aligned at every position, including the last.
    Mask unwanted positions explicitly; built-in losses mask the last position.
    With sampler routing replay, the uncaptured last position uses live routing.

    Image-conditioned inputs use model_input chunks. Columns align to the full
    expanded sequence, including each image's expected_tokens slots; mask image
    targets explicitly. AsyncTrainer supplies that mask and next-text targets.

    For screenshots, use session.upload_image() handles to avoid repeating image
    bytes in uploads. Custom requests have a 1 GiB upload limit and cannot split
    automatically without changing global reductions. Handles still count toward
    server limits after resolution: 128 MiB per datum and 2 GiB total image bytes
    per request, including repeated images.
    """

    objective: LossObjective
    inputs: LossInputs
    _graph: bytes | None = field(default=None, init=False, repr=False, compare=False)

    _prepared_for: object | None = field(
        default=None, init=False, repr=False, compare=False
    )

    def __post_init__(self):
        if not callable(self.objective):
            raise TypeError("custom loss objective must be callable")
        columns = _input_columns(self.inputs)
        frozen = {
            c["name"]: MappingProxyType(
                {"dtype": c["dtype"], "shape": ("T", c["width"])}
            )
            if "width" in c
            else c["dtype"]
            for c in columns
        }
        object.__setattr__(self, "inputs", MappingProxyType(frozen))

    def _resolve(self) -> tuple[LossObjective, dict[str, float]]:
        return self.objective, {}
