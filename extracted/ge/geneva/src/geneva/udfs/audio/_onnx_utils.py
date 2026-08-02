# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared helpers for ONNX-backed audio UDFs."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence

    import pyarrow as pa

_LOG = logging.getLogger(__name__)


def _extract_optional_column(
    batch: pa.RecordBatch,
    column: str | None,
    expected_types: type | tuple[type, ...],
    default_value: Any,
    label: str,
) -> list[Any]:
    """Return per-row values for an optional column, filling defaults."""

    if column is None:
        return [default_value] * batch.num_rows

    index = batch.schema.get_field_index(column)
    if index == -1:
        raise ValueError(f"{label} column '{column}' not found in RecordBatch")

    values = batch.column(index).to_pylist()
    normalized: list[Any] = []
    for value in values:
        if value is None:
            normalized.append(default_value)
            continue
        if not isinstance(value, expected_types):
            raise TypeError(
                f"{label} column '{column}' must contain {expected_types} values; "
                f"received {type(value).__name__}."
            )
        normalized.append(value)
    return normalized


def _resolve_providers(num_gpus: float, providers: Sequence[str] | None) -> list[str]:
    """Resolve ONNX Runtime execution providers for a worker."""

    if providers is not None:
        return list(providers)

    try:
        import onnxruntime as ort
    except ImportError:
        return ["CPUExecutionProvider"]

    if num_gpus <= 0:
        return ["CPUExecutionProvider"]

    available = ort.get_available_providers()
    if "CUDAExecutionProvider" in available:
        return ["CUDAExecutionProvider", "CPUExecutionProvider"]

    _LOG.warning("GPU requested but CUDAExecutionProvider is unavailable; using CPU")
    return ["CPUExecutionProvider"]
