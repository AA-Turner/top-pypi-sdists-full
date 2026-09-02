import asyncio
import ast
import json
from collections.abc import Callable
from typing import Any, Optional

import pandas
from pandas import json_normalize

from ..exceptions import ComponentError, DataNotFound
from ..interfaces.flow import FlowComponent


class tFlatten(FlowComponent):
    """tFlatten

    Overview

        Flattens a column containing (possibly nested) dictionaries into flat
        columns in a single **vectorized** ``pandas.json_normalize`` pass — the
        fast equivalent of a manual ``expand_dev`` (json_normalize + prefix).

        Unlike ``tExplode`` (which splits list columns into rows) or a chain of
        row-wise ``flatten_array`` calls, this expands every nested level at once
        with a separator and an optional prefix, so a ``dev`` column becomes
        ``dev_application``, ``dev_navigator_widget_id``, ``dev_user_id``, etc.

        Rows whose value is null or not a dict yield NaN for the new columns.

        .. table:: Properties
        :widths: auto

    +----------------+----------+-------------------------------------------------------------------+
    | Name           | Required | Summary                                                           |
    +----------------+----------+-------------------------------------------------------------------+
    | column         |   Yes    | Name of the column holding dicts (or JSON strings) to flatten.    |
    +----------------+----------+-------------------------------------------------------------------+
    | prefix         |   No     | Prefix added to every generated column (e.g. ``dev_``).           |
    +----------------+----------+-------------------------------------------------------------------+
    | sep            |   No     | Separator for nested keys (default ``_``).                        |
    +----------------+----------+-------------------------------------------------------------------+
    | max_level      |   No     | Max nesting depth to flatten (default: all levels).               |
    +----------------+----------+-------------------------------------------------------------------+
    | drop_original  |   No     | Drop the source column after flattening (default ``False``).      |
    +----------------+----------+-------------------------------------------------------------------+

    Returns

        The input DataFrame with the flattened columns appended (and the original
        column dropped when ``drop_original`` is True).

    Example:

    .. code-block:: yaml

        tFlatten:
          column: dev
          prefix: dev_
          sep: _
          drop_original: true
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        self.column: str = kwargs.pop("column", None)
        self.prefix: str = kwargs.pop("prefix", "")
        self.sep: str = kwargs.pop("sep", "_")
        self.max_level: Optional[int] = kwargs.pop("max_level", None)
        self.drop_original: bool = bool(kwargs.pop("drop_original", False))
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("tFlatten: Data Not Found", status=404)
        if not isinstance(self.data, pandas.DataFrame):
            raise ComponentError("tFlatten: Incompatible Pandas Dataframe", status=404)
        if not self.column:
            raise ComponentError("tFlatten: 'column' is required.")
        return True

    @staticmethod
    def _as_dict(value: Any) -> dict:
        """Coerce a cell to a dict (parse JSON/py-literal strings; else {})."""
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            txt = value.strip()
            if not txt:
                return {}
            try:
                return json.loads(txt)
            except (ValueError, TypeError):
                try:
                    parsed = ast.literal_eval(txt)
                    return parsed if isinstance(parsed, dict) else {}
                except (ValueError, SyntaxError):
                    return {}
        return {}

    async def run(self):
        df = self.data
        if self.column not in df.columns:
            raise ComponentError(
                f"tFlatten: column {self.column!r} not in DataFrame"
            )
        try:
            records = df[self.column].map(self._as_dict)
            # Single vectorized expansion of all nested levels.
            normalized = json_normalize(
                records.tolist(), sep=self.sep, max_level=self.max_level
            )
            if self.prefix:
                normalized.columns = [f"{self.prefix}{c}" for c in normalized.columns]
            normalized.index = df.index

            base = df.drop(columns=[self.column]) if self.drop_original else df
            result = pandas.concat([base, normalized], axis=1)
        except Exception as err:
            raise ComponentError(
                f"tFlatten: error flattening {self.column!r}: {err}"
            ) from err

        if result is None or result.empty:
            raise DataNotFound("tFlatten: Result is an empty Dataframe")

        self.add_metric("FLATTEN_COLUMNS", len(normalized.columns))
        self.add_metric("NUM_ROWS", len(result.index))
        self._result = result
        return self._result

    async def close(self):
        pass
