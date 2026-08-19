from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

import numpy as np
import pyarrow as pa

from chalk.utils.pandas_utils import is_pandas_series

if TYPE_CHECKING:
    from chalk.features._encoding._feature_converters._base import FeatureConverter
    from chalk.features._encoding.missing_value import MissingValueStrategy

__all__ = ["values_to_pyarrow_array"]


def _typed_container_to_arrow(values: Any) -> Union[pa.Array, pa.ChunkedArray, None]:
    """Convert an already-typed container (arrow/polars/pandas/numpy) to arrow natively,
    without element-wise coercion. Returns None for plain python sequences and for
    containers arrow cannot convert directly (e.g. object-dtype arrays)."""
    if isinstance(values, (pa.Array, pa.ChunkedArray)):
        return values
    try:
        import polars as pl
    except ImportError:
        pl = None
    if pl is not None and isinstance(values, pl.Series):
        return values.to_arrow()
    if isinstance(values, np.ndarray) or is_pandas_series(values):
        try:
            # For pandas inputs, pa.array() applies pandas missing-value semantics
            # (NaN/NA/NaT become nulls).
            return pa.array(values)
        except (pa.ArrowException, ValueError, TypeError):
            return None
    return None


def values_to_pyarrow_array(
    values: Any,
    converter: Optional[FeatureConverter] = None,
    column_name: Optional[str] = None,
    missing_value_strategy: MissingValueStrategy = "allow",
) -> Union[pa.Array, pa.ChunkedArray]:
    """Convert one column of user-supplied values to a pyarrow array.

    Already-typed containers (arrow arrays, polars/pandas Series, numpy arrays) are
    converted to arrow natively and, when a converter is given, cast to its dtype --
    preserving the container's own missing-value semantics. Plain python sequences are
    converted element-wise with the converter, which handles rich values arrow cannot
    infer (chalk DataFrames for has-many features, feature-class instances, enums, ...).
    Without a converter, pyarrow type inference is used.
    """
    native = _typed_container_to_arrow(values)

    if converter is None:
        if native is not None:
            return native
        values_list = list(values)
        try:
            return pa.array(values_list)
        except (pa.ArrowException, ValueError, TypeError) as e:
            name_part = f" of column '{column_name}'" if column_name is not None else ""
            raise ValueError(f"Could not infer an arrow type for the values{name_part}: {e}") from e

    if native is not None:
        try:
            return native.cast(converter.pyarrow_dtype)
        except (pa.ArrowException, ValueError, TypeError):
            # The container's arrow type is not directly castable (e.g. strings for a
            # timestamp feature); fall through to element-wise conversion. to_pylist()
            # keeps the nulls the native conversion already normalized.
            values = native.to_pylist()

    values_list = list(values)
    try:
        return converter.from_rich_to_pyarrow(
            values_list, missing_value_strategy=missing_value_strategy, feature_name=column_name
        )
    except Exception as e:
        name_part = f" of column '{column_name}'" if column_name is not None else ""
        raise ValueError(
            f"Could not convert the values{name_part} to the feature type '{converter.pyarrow_dtype}': {e}"
        ) from e
