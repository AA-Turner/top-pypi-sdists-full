#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""JSON-safe cleaning of input records before they are sent to the API.

One owner for every client path that posts records (predictor, published
predictor, prediction network, API endpoint, vector database, reference
record, foundational model). Stdlib only: the client does not import numpy
or pandas at module load, so numpy scalars and pandas missing-value
sentinels are recognized by duck typing.
"""

import math
from typing import Any, Dict

# pandas missing-value sentinels: pd.NA (NAType) and pd.NaT (NaTType).
_PANDAS_MISSING_TYPE_NAMES = frozenset({"NAType", "NaTType"})


def _is_pandas_missing(value: Any) -> bool:
    value_type = type(value)
    return (
        value_type.__name__ in _PANDAS_MISSING_TYPE_NAMES
        and value_type.__module__.startswith("pandas")
    )


def clean_value(value: Any) -> Any:
    """Return a JSON-safe version of one record value.

    - pd.NA / pd.NaT / None -> None
    - numpy scalars (np.float32, np.int64, np.bool_, ...) -> Python scalars
    - numpy arrays -> lists (cleaned element-wise)
    - NaN / +-Inf (Python or numpy floats) -> None
    """
    if value is None or _is_pandas_missing(value):
        return None
    # numpy scalar or array: unwrap BEFORE the float check so np.float32('nan')
    # (not a float subclass) is caught below.
    if hasattr(value, "item") and hasattr(value, "ndim"):
        if value.ndim == 0:
            value = value.item()
        else:
            return [clean_value(v) for v in value.tolist()]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``record`` with every value made JSON-safe."""
    return {key: clean_value(value) for key, value in record.items()}
