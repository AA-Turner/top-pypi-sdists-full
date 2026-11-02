"""Validate vectorized handlers against their independently transported scalar interface."""

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import get_args, get_origin, get_type_hints

from labqoat.compute.function_signature import FunctionSignature
from labqoat.run_context import RunContext


@dataclass(frozen=True)
class BatchHandler:
    """Preserve named arguments, scalar result types and explicit per-input contexts in vectorized execution."""

    function: Callable[..., object]

    def validate(self, scalar: Callable[..., object]) -> None:
        """Require the batch signature to be the ordered list form of every scalar parameter and result."""
        signature = FunctionSignature(scalar)
        parameters = tuple(inspect.signature(self.function).parameters)
        annotations = get_type_hints(self.function)
        if not parameters or parameters[1:] != tuple(signature.signature.parameters):
            raise TypeError("Batch handler must preserve the scalar argument names and order")
        expected = {parameters[0]: RunContext, "return": signature.annotations["return"]}
        expected.update({name: signature.annotations[name] for name in parameters[1:]})
        for name, value in expected.items():
            annotation = annotations.get(name)
            if get_origin(annotation) is not list or get_args(annotation) != (value,):
                raise TypeError("Batch handler annotations must be lists of the scalar context, input and result types")
