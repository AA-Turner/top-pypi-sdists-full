import asyncio
from typing import Union
import pandas as pd
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas

class tPivot(tPandas):
    """
    tPivot

    Overview

    Pivoting a Dataframe to transpose a column into other columns.

    Properties

    :widths: auto

    | columns          | Yes      | list      | The List of Columns to be Pivoted.                                                |
    | index            | No       | list      | List of columns to be preserved, default to all columns less "values"             |
    | values           | Yes      | str       | Columns that transpose the values for pivoted column(s).                          |

    Return
       The dataframe Pivoted by "columns" with values using the list of "values".

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tPivot:
          # attributes here
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self._columns: Union[str, list] = kwargs.pop("columns", None)
        self._index: list = kwargs.pop("index", [])
        self._values: list = kwargs.pop("values", [])
        self._sort: list = kwargs.pop('sort_by', [])
        self._aggfunc: Union[str, Callable] = kwargs.pop("aggfunc", None)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def _run(self):
        try:
            # default: unique, order-preserving list
            def uniq_list(s: pd.Series):
                s = s.dropna()
                out, seen = [], set()
                for x in s:
                    if x not in seen:
                        seen.add(x)
                        out.append(x)
                return out

            agg = self._aggfunc or uniq_list
            df_pivot = (
                self.data.pivot_table(
                    index=self._index,          # all “other” columns to preserve
                    columns=self._columns,      # e.g. "column_name"
                    values=self._values,        # e.g. ["image_data"]
                    aggfunc=agg,
                    dropna=False
                )
                .reset_index()
            )
            # Flatten any MultiIndex columns (harmless if not multi-index)
            if isinstance(df_pivot.columns, pd.MultiIndex):
                df_pivot.columns = [
                    "_".join([str(x) for x in tup if x != ""])
                    for tup in df_pivot.columns
                ]
            df_pivot.columns.name = None

            # Ensure missing groups produce [] instead of NaN — only on pivoted cols
            # But only if using the default uniq_list aggfunc (not for sum, mean, etc.)
            pivot_cols = [c for c in df_pivot.columns if c not in self._index]
            if getattr(agg, '__name__', None) == 'uniq_list':
                for col in pivot_cols:
                    df_pivot[col] = df_pivot[col].apply(lambda v: v if isinstance(v, list) else [])

            if self._sort:
                df_pivot = df_pivot.sort_values(
                    by=self._sort,
                    ascending=True
                ).reset_index(drop=True)

            self._result = df_pivot
            return df_pivot
        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err
