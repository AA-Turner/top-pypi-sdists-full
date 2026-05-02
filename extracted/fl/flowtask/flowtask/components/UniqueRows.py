import asyncio
from typing import List
from collections.abc import Callable
import pandas as pd
from asyncdb.exceptions import StatementError, DataError
from ..exceptions import ComponentError
from .flow import FlowComponent


class UniqueRows(FlowComponent):
    """
    UniqueRows

        Overview

            The UniqueRows class is a component for extracting unique rows from a Pandas DataFrame.
            It supports pre-sorting of rows, custom options for handling duplicates, and an option to save
            rejected rows that are duplicates.

        :widths: auto

            | unique         |   Yes    | List of columns to use for identifying unique rows.                       |
            | order          |   No     | Dictionary specifying columns and sort order (`asc` or `desc`).           |
            | keep           |   No     | Specifies which duplicates to keep: `first`, `last`, or `False`.          |
            | save_rejected  |   No     | Dictionary with filename to save rejected rows as CSV, if specified.      |

        Returns

            This component returns a DataFrame containing only unique rows based on the specified columns.
            If sorting is defined in `order`, rows are pre-sorted before duplicates are removed. Metrics such as
            the number of rows passed and rejected are recorded. If `save_rejected` is specified, rejected rows
            are saved to a file. Any data errors encountered during execution are raised with detailed error messages.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UniqueRows:
          unique:
          - store_id
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
        self.unique: List = None
        super(UniqueRows, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Start Component"""
        if self.previous:
            self.data = self.input

    def close(self):
        """Close."""

    async def run(self):
        """Getting Unique rows from a Dataframe."""
        self._result = None
        try:
            if isinstance(self.data, pd.DataFrame):
                start = len(self.data.index)
                self.add_metric("Start", start)
                if hasattr(self, "order"):
                    # making a pre-ordering before drop duplicates:
                    ordering = []
                    ascending = []
                    for col, order in self.order.items():
                        ordering.append(col)
                        if order == "asc":
                            ascending.append(True)
                        else:
                            ascending.append(False)
                    self.data.sort_values(
                        by=ordering, inplace=True, ascending=ascending
                    )
                keep = {}
                if hasattr(self, "keep"):
                    keep = {"keep": self.keep}
                # get only unique rows from this dataframe
                print('UNIQUE > ', self.unique)
                self._result = self.data.drop_duplicates(self.unique, **keep)
                passed = len(self._result.index)
                self.add_metric("Passed", passed)
                rejected = start - passed
                self.add_metric("Rejected", rejected)
                self._variables[f"{self.StepName}_PASSED"] = passed
                self._variables[f"{self.StepName}_REJECTED"] = rejected
                if hasattr(self, "save_rejected"):
                    # Identify the indices of the rows that were removed
                    removed_indices = set(self.data.index) - set(self._result.index)
                    # Select these rows from the original DataFrame
                    rejected = self.data.loc[list(removed_indices)]
                    filename = self.save_rejected.get("filename", "rejected_rows.csv")
                    try:
                        rejected.to_csv(filename, sep="|")
                    except IOError:
                        self._logger.warning(f"Error writing Rejectd File: {filename}")
                    self.add_metric(
                        "rejected_file", filename
                    )
            else:
                # return expected data
                self._result = self.data
            return self._result
        except StatementError as err:
            print(err)
            return None
        except DataError as err:
            print(err)
            raise ComponentError(f"UniqueRows: Error with Data: {err}") from err
