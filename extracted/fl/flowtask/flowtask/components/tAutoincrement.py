import asyncio
from collections.abc import Callable
import pandas as pd
from ..exceptions import ComponentError, DataNotFound, TaskError
from .flow import FlowComponent
from ..interfaces import DBSupport


class tAutoincrement(DBSupport, FlowComponent):
    """
    tAutoincrement

    Overview

    The `tAutoincrement` component is designed to automatically increment values in a specific column of a dataset.
    This is particularly useful when you need to fill in missing (null) values in a column with unique, sequential
    integers starting from the maximum value currently present in the column.

    Properties

    :widths: auto

    | datasource       | Yes      | str       | The datasource name (e.g., schema name) where the dataset is located.                |
    | dataset          | Yes      | str       | The name of the dataset (e.g., table name) to work on.                               |
    | column           | Yes      | str       | The name of the column in which values will be auto-incremented.                     |

    Return

        Returns the dataframe with the given column and its auto-incremented sequence.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tAutoincrement:
          skipError: skip
          datasource: pokemon
          dataset: districts
          column: district_id
          description: Auto-increment district_id for new districts
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self.datasource: str = None
        self.dataset: str = None
        self.column: str = None
        self.pd_args = kwargs.pop("pd_args", {})
        super(tAutoincrement, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Start method."""
        if not self.datasource:
            raise TaskError("Missing *datasource* parameter.")
        if not self.dataset:
            raise TaskError("Missing *dataset* parameter.")
        if not self.column:
            raise TaskError("Missing *column* parameter.")

        # Set the DataFrame if provided via kwargs
        self.data = kwargs.get('data', None)
        if self.data is None and hasattr(self, 'previous'):
            self.data = self.previous.output()

        if self.data is None:
            raise ComponentError(
                "No input DataFrame provided to tAutoincrement component."
            )
        await super().start(**kwargs)
        self.processing_credentials()
        return True

    async def run(self):
        """Run method to fetch the max value and auto-increment."""
        # Establishing the connection
        self.connection = self.pg_connection()
        try:
            async with await self.connection.connection() as conn:
                query = f"SELECT MAX({self.column}) as alias_column FROM {self.datasource}.{self.dataset};"
                result = await conn.fetchval(query)
                if result is None:
                    result = 0
                self._logger.info(f"Executing query: {query} MAX: {result}")
                # Incrementing and assigning the values to null columns
                if self.data.empty:
                    raise DataNotFound("Input DataFrame is empty.")

                mask = self.data[self.column].isnull()
                self.data.loc[mask, self.column] = range(result + 1, result + 1 + mask.sum())
                self._result = self.data

        except Exception as ex:
            raise ComponentError(f"Error in tAutoincrement: {str(ex)}") from ex

        finally:
            self.connection = None

        return True

    async def close(self):
        pass
