"""Operation-level structured-data transformer contracts."""

import logging
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

type OperationDataValue = (
    str | bool | int | float | bytes | Sequence[OperationDataValue] | Mapping[str, OperationDataValue] | None
)
type OperationSignal = Literal["span", "log", "metric"]

_logger = logging.getLogger(__name__)


@runtime_checkable
class OperationDataTransformer(Protocol):
    """Transform one structured value before it reaches OpenTelemetry.

    Returning ``None`` drops the value. Implementations should recursively
    inspect mappings and sequences when they can contain sensitive leaves.
    """

    def transform(
        self,
        value: OperationDataValue,
        *,
        context: "OperationDataContext",
    ) -> OperationDataValue | None:
        """Return the value to record, or ``None`` to omit it."""
        ...


@dataclass(frozen=True, slots=True, kw_only=True)
class OperationDataContext:
    """Location of a value being transformed."""

    operation_name: str
    signal: OperationSignal
    field: str


@dataclass(frozen=True, slots=True, kw_only=True)
class OperationDataTransformers:
    """Ordered structured-data transformer chain for one configured SDK."""

    transformers: tuple[OperationDataTransformer, ...]

    def transform(
        self,
        value: OperationDataValue,
        *,
        operation_name: str,
        signal: OperationSignal,
        field: str,
    ) -> OperationDataValue | None:
        """Apply the configured transformer chain, dropping on failure."""
        transformed = value
        context = OperationDataContext(operation_name=operation_name, signal=signal, field=field)
        for transformer in self.transformers:
            try:
                transformed = transformer.transform(transformed, context=context)
            except Exception as exc:
                # Never include the value, exception message, or traceback: a
                # transformer failure may itself contain the data being redacted.
                _logger.debug(
                    "Operation data transformer %s failed for %s field %s with %s",
                    type(transformer).__name__,
                    signal,
                    field,
                    type(exc).__name__,
                )
                return None
            if transformed is None:
                return None
        return transformed

    def transform_attributes(
        self,
        attributes: Mapping[str, OperationDataValue],
        *,
        operation_name: str,
        signal: OperationSignal,
        already_transformed: frozenset[str] = frozenset(),
    ) -> dict[str, OperationDataValue]:
        """Transform every attribute that has not already passed through the chain."""
        transformed_attributes: dict[str, OperationDataValue] = {}
        for key, value in attributes.items():
            if key in already_transformed:
                transformed = value
            else:
                transformed = self.transform(
                    value,
                    operation_name=operation_name,
                    signal=signal,
                    field=key,
                )
            if transformed is not None:
                transformed_attributes[key] = transformed
        return transformed_attributes
