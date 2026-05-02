import asyncio
from typing import Union
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas
import html
from querysource.types.dt.transforms import remove_html_tags
import re
import pandas as pd

class tCrosstab(tPandas):
    """
    tCrosstab

    Overview

    Creates a cross-tabulation (contingency table) from a DataFrame.

    Properties

    :widths: auto

    | index            | Yes      | list      | List of columns to be used as index in the crosstab.                              |
    | columns          | Yes      | list      | List of columns to be used as columns in the crosstab.                            |
    | values           | No       | list      | List of columns to be used as values in the crosstab.                             |
    | aggregate        | No       | str       | Aggregation function to use when values are provided.                             |
    | totals           | No       | dict      | Dictionary with 'name' key to add totals row/column.                              |
    | reset_index      | No       | bool      | Whether to reset the index after creating the crosstab.                           |
    | alpha_first      | No       | bool      | Whether to sort columns alphabetically if they start with letters.                |

    Return
       The dataframe with the crosstab transformation applied.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tCrosstab:
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
        self._index: list = kwargs.pop("index", None)
        self._columns: list = kwargs.pop("columns", None)
        self._values: list = kwargs.pop("values", None)
        self._aggregate: str = kwargs.pop("aggregate", None)
        self._totals: dict = kwargs.pop("totals", None)
        self._reset_index: bool = kwargs.pop("reset_index", True)
        self._alpha_first: bool = kwargs.pop("alpha_first", False)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def _run(self):
        try:
            if not self._index:
                raise ConfigError("Crosstab Transform: Missing Index on definition")
            if not self._columns:
                raise ConfigError("Crosstab Transform: Missing Columns on definition")

            # General cleaning for all columns used as columns in the crosstab
            columns_to_clean = self._columns if isinstance(self._columns, list) else [self._columns]
            for col in columns_to_clean:
                if col in self.data.columns:
                    self.data[col] = self.data[col].apply(html.unescape)
                    self.data[col] = self.data[col].apply(remove_html_tags)
                    self.data[col] = self.data[col].str.split("\n").str[0].str.strip()

            index = self._index
            columns = self._columns[0] if isinstance(self._columns, list) and len(self._columns) == 1 else self._columns
            values = self._values[0] if isinstance(self._values, list) and len(self._values) == 1 else self._values

            # If the index has more than one column, group and use only the key column for the crosstab
            if isinstance(index, list) and len(index) > 1:
                # Group by all columns of the index and keep the first occurrence
                grouped = self.data.groupby(index, dropna=False).first().reset_index()
                crosstab_index = [index[0]]
                extra_index_cols = index[1:]
                # Do the crosstab only with the key column
                df_crosstab = self.data.pivot_table(
                    index=crosstab_index,
                    columns=columns,
                    values=values,
                    aggfunc=self._aggregate,
                    dropna=False
                )
                if self._reset_index:
                    df_crosstab.reset_index(inplace=True)
                # Sort columns numerically by prefix or alphabetically if alpha_first
                def sort_columns_alpha_first(cols):
                    alpha_cols = [col for col in cols if re.match(r"^[A-Za-z]", str(col))]
                    num_cols = [col for col in cols if re.match(r"^\s*\d+", str(col))]
                    def extract_number(col):
                        match = re.match(r"^\s*(\d+)", str(col))
                        return int(match.group(1)) if match else float('inf')
                    num_cols_sorted = sorted(num_cols, key=extract_number)
                    other_cols = [col for col in cols if col not in alpha_cols and col not in num_cols]
                    return alpha_cols + num_cols_sorted + other_cols
                def sort_columns_numerically(cols):
                    def extract_number(col):
                        match = re.match(r"^\s*(\d+)", str(col))
                        return int(match.group(1)) if match else float('inf')
                    return sorted(cols, key=lambda col: extract_number(col))
                if isinstance(df_crosstab.columns, pd.MultiIndex):
                    new_order = sort_columns_alpha_first(df_crosstab.columns.get_level_values(-1)) if self._alpha_first else sort_columns_numerically(df_crosstab.columns.get_level_values(-1))
                    df_crosstab = df_crosstab.reindex(columns=new_order, level=-1)
                else:
                    index_cols = crosstab_index
                    other_cols = [col for col in df_crosstab.columns if col not in index_cols]
                    sorted_other_cols = sort_columns_alpha_first(other_cols) if self._alpha_first else sort_columns_numerically(other_cols)
                    df_crosstab = df_crosstab[index_cols + sorted_other_cols]
                # Join the result of the crosstab with grouped using the key column
                df_final = pd.merge(grouped, df_crosstab, on=crosstab_index, how='inner')
                # Filter only the columns of the index and the crosstab
                crosstab_cols = [col for col in df_crosstab.columns if col not in crosstab_index]
                df_final = df_final[crosstab_index + extra_index_cols + crosstab_cols]
                return df_final
            else:
                df = self.data.pivot_table(
                    index=index,
                    columns=columns,
                    values=values,
                    aggfunc=self._aggregate,
                    dropna=False
                )
                if self._reset_index:
                    df.reset_index(inplace=True)
                # Sort columns numerically by prefix or alphabetically if alpha_first
                def sort_columns_alpha_first(cols):
                    alpha_cols = [col for col in cols if re.match(r"^[A-Za-z]", str(col))]
                    num_cols = [col for col in cols if re.match(r"^\s*\d+", str(col))]
                    def extract_number(col):
                        match = re.match(r"^\s*(\d+)", str(col))
                        return int(match.group(1)) if match else float('inf')
                    num_cols_sorted = sorted(num_cols, key=extract_number)
                    other_cols = [col for col in cols if col not in alpha_cols and col not in num_cols]
                    return alpha_cols + num_cols_sorted + other_cols
                def sort_columns_numerically(cols):
                    def extract_number(col):
                        match = re.match(r"^\s*(\d+)", str(col))
                        return int(match.group(1)) if match else float('inf')
                    return sorted(cols, key=lambda col: extract_number(col))
                if isinstance(df.columns, pd.MultiIndex):
                    new_order = sort_columns_alpha_first(df.columns.get_level_values(-1)) if self._alpha_first else sort_columns_numerically(df.columns.get_level_values(-1))
                    df = df.reindex(columns=new_order, level=-1)
                else:
                    index_cols = index if isinstance(index, list) else [index]
                    other_cols = [col for col in df.columns if col not in index_cols]
                    sorted_other_cols = sort_columns_alpha_first(other_cols) if self._alpha_first else sort_columns_numerically(other_cols)
                    df = df[index_cols + sorted_other_cols]
                return df
        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err 