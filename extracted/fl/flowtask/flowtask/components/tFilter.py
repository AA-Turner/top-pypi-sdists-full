import asyncio
from collections.abc import Callable
import re
import pandas as pd
import numpy as np
from querysource.types.dt import filters as qsffunctions
from querysource.queries.multi.operators.filter.flt import (
    create_filter,
    valid_operators
)
from .FilterRows import functions as dffunctions
# create_filter
from ..exceptions import (
    ConfigError,
    ComponentError,
    DataNotFound
)
from .flow import FlowComponent


class tFilter(FlowComponent):
    """
    tFilter

        Overview

            The tFilter class is a component that applies specified filters to a Pandas DataFrame.
            It allows filtering rows based on multiple conditions and expressions, enabling targeted
            data extraction within a task flow.

        :widths: auto

            | operator     |   Yes    | Logical operator (e.g., `and`, `or`) used to combine filter conditions.   |
            | conditions   |   Yes    | List of conditions with columns, values, and expressions for filtering.   |
            |              |          | Format: `{ "column": <col_name>, "value": <val>, "expression": <expr> }`  |

        Returns

            This component returns a filtered Pandas DataFrame based on the provided conditions.
            The component tracks metrics
            such as the initial and filtered row counts, and optionally limits the returned columns if specified.
            Additional debugging information can be outputted based on configuration.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tFilter:
          operator: '&'
          filter:
          - column: ClientId
          value:
          - 11076
          expression: ==
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
        self.condition: str = ""
        self.fields: dict = kwargs.pop('fields', {})
        self.operator = kwargs.pop('operator', '&')
        self.filter = kwargs.pop('filter', [])
        self.filter_conditions: dict = {}
        super(tFilter, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe")
        return True

    async def close(self):
        pass

    def _filter_conditions(self, df: pd.DataFrame) -> pd.DataFrame:
        it = df.copy()
        for ft, args in self.filter_conditions.items():
            self._applied.append(f"Filter: {ft!s} args: {args}")
            try:
                try:
                    func = getattr(qsffunctions, ft)
                except AttributeError:
                    try:
                        func = getattr(dffunctions, ft)
                    except AttributeError:
                        func = globals()[ft]
                if callable(func):
                    it = func(it, **args)
            except Exception as err:
                print(f"Error on {ft}: {err}")
        df = it
        if df is None or df.empty:
            raise DataNotFound(
                "No Data was Found after Filtering."
            )
        return df

    def _filter_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, value in self.fields.items():
            if column in df.columns:
                if isinstance(value, list):
                    for v in value:
                        df = df[df[column] == v]
                else:
                    df = df[df[column] == value]
        return df

    async def run(self):
        self.add_metric("STARTED_ROWS", len(self.data.index))
        df = self.data.copy()
        # iterate over all filtering conditions:
        df = self._filter_conditions(df)
        # Applying filter expressions by Column:
        if self.fields:
            df = self._filter_fields()
        if self.filter:
            # conditions = self._create_filter()
            conditions = create_filter(self.filter, df)
            # Joining all conditions
            self.condition = f" {self.operator} ".join(conditions)
            self._logger.notice(
                f"Filter conditions >> {self.condition}"
            )
            df = df.loc[
                eval(self.condition)
            ]  # pylint: disable=W0123
        if df is None or df.empty:
            raise DataNotFound(
                "No Data was Found after Filtering."
            )
        self._result = df
        # print(": Filtered : ")
        # print(self._result)
        self.add_metric(
            "FILTERED_ROWS", len(self._result.index)
        )
        # Calculate the rejected rows between self.data and df dataframe:
        self.add_metric(
            "REJECTED_ROWS", len(self.data.index) - len(self._result.index)
        )
        if hasattr(self, "save_rejected"):
            # Identify the indices of the rows that were removed
            removed_indices = set(self.data.index) - set(self._result.index)
            # Select these rows from the original DataFrame
            rejected = self.data.loc[list(removed_indices)]
            filename = self.mask_replacement(
                self.save_rejected.get("filename", "rejected_rows.csv")
            )
            try:
                rejected.to_csv(filename, sep="|")
            except IOError:
                self._logger.warning(f"Error writing Rejectd File: {filename}")
            self.add_metric(
                "rejected_file", filename
            )
        if hasattr(self, "columns"):
            # returning only a subset of data
            self._result = self._result[self.columns]
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in self._result.dtypes.items():
                print(column, "->", t, "->", self._result[column].iloc[0])
        self.add_metric(
            "FILTERED_COLS", len(self._result.columns)
        )
        return self._result
