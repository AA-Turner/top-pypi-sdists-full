from __future__ import annotations

from importlib.util import find_spec
from types import ModuleType
from typing import TYPE_CHECKING, Any, TypeGuard

from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    import pandas as pd


def get_pandas() -> ModuleType | None:
    try:
        if find_spec("pandas") is None:
            return None
        import pandas as pd
    except (ImportError, ValueError):
        return None
    return pd


def require_pandas() -> ModuleType:
    pd = get_pandas()
    if pd is None:
        raise missing_dependency_exception("pandas")
    return pd


def is_pandas_dataframe(value: Any) -> TypeGuard[pd.DataFrame]:
    pd = get_pandas()
    return pd is not None and isinstance(value, pd.DataFrame)


def is_pandas_series(value: Any) -> TypeGuard[pd.Series]:
    pd = get_pandas()
    return pd is not None and isinstance(value, pd.Series)
