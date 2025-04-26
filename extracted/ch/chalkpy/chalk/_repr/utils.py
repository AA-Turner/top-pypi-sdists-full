from enum import Enum
from typing import Any

import pandas as pd

from chalk.features import DataFrame

MAX_REPR_DEPTH = 2


def get_repr_value(raw: Any, depth: int = 0) -> Any:
    limit = 10 if depth < MAX_REPR_DEPTH else 0
    if isinstance(raw, (pd.DataFrame, DataFrame)):
        return f"DataFrame[shape={raw.shape}]"
    elif isinstance(raw, Enum):
        return raw.value
    elif isinstance(raw, dict) and "columns" in raw and "values" in raw and len(raw) == 2:
        # If feature not in registry, has-many results will not
        # be converted into a DataFrame, bringing us to this block.
        cols, vals = raw["columns"], raw["values"]
        num_cols = num_rows = "unknown no. of"
        if isinstance(cols, list):
            num_cols = len(cols)
        if isinstance(vals, list) and vals and isinstance(vals[0], list):
            num_rows = len(vals[0])
        col_tag = "col" if num_cols == 1 else "cols"
        row_tag = "row" if num_rows == 1 else "rows"
        return f"has_many[ {num_rows} {row_tag} x {num_cols} {col_tag}  ]"
    elif isinstance(raw, list):
        reprs = []
        for elem in raw[:limit]:
            if isinstance(elem, (dict, list)):
                reprs.append(get_repr_value(elem, depth + 1))
            else:
                reprs.append(repr(elem))
        if len(raw) > limit:
            reprs.append("...")
        list_contents = f", ".join(reprs)
        return f"[{list_contents}]"
    elif isinstance(raw, dict):
        reprs = []
        idx = 0
        for key, val in raw.items():
            if idx >= limit:
                break
            idx += 1
            key_repr = repr(key)
            if isinstance(val, (dict, list)):
                value_repr = get_repr_value(val, depth + 1)
            else:
                value_repr = repr(val)
            reprs.append(f"{key_repr}: {value_repr}")
        if len(raw) > limit:
            reprs.append("...")
        dict_contents = f", ".join(reprs)
        return f"{{{dict_contents}}}"
    else:
        return raw
