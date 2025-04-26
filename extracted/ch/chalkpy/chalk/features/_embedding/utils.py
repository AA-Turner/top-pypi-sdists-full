from dataclasses import dataclass
from typing import Callable, Optional, Sequence

import pyarrow as pa


@dataclass
class ModelSpecs:
    default_dimensions: int
    validate_dimensions: Callable[[int], bool]
    validation_message: str
    requires_none_input: bool = False


def create_fixedsize_with_nulls(
    vectors: Sequence[Optional[Sequence[float]]], vector_size: int
) -> pa.FixedSizeListArray:
    flat_values = []
    for vec in vectors:
        if vec is not None:
            flat_values.extend(vec)
        else:
            flat_values.extend([0] * vector_size)  # placeholder values

    # Create mask as PyArrow boolean array (True means null)
    mask = pa.array([vec is None for vec in vectors], type=pa.bool_())

    # Create the FixedSizeListArray with the mask
    return pa.FixedSizeListArray.from_arrays(pa.array(flat_values), vector_size, mask=mask)
