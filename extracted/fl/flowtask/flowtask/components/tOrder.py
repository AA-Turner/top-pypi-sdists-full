import asyncio
from typing import Union
from collections.abc import Callable
from ..exceptions import ComponentError, ConfigError
from .tPandas import tPandas

class tOrder(tPandas):
    """
    tOrder

    Overview

    The `tOrder` class is a component designed to order a Pandas DataFrame by a specified column.
    It allows sorting the DataFrame either in ascending or descending order based on the specified column.

    Properties

    :widths: auto

    | columns          | Yes      | str       | The name of the column to sort the DataFrame by.                                  |
    | ascending        | No       | bool      | Specifies whether to sort the DataFrame in ascending order. Defaults to True.     |

    Return
       The dataframe ordinated by the column give it in the order_by either ascending or descending.



    Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tOrder:
          columns:
          - district_id
          ascending: true
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
        self._column: Union[str, list] = kwargs.pop("columns", None)
        if isinstance(self._column, list):
            ascending = [True for x in self._column]
        elif isinstance(self._column, str):
            ascending = [True]
            self._column = [self._column]
        self._ascending: Union[bool, list] = kwargs.pop("ascending", ascending)
        if not self._column:
            raise ConfigError(
                "tOrder requires a column for ordering => **columns**"
            )
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def _run(self):
        try:
            # Check if the specified column exists in the DataFrame
            columns = self.data.columns
            for col in self._column:
                if col not in columns:
                    self._logger.warning(
                        f"The column '{self._column}' does not exist in the DataFrame."
                    )
                    return self.data  # Return the unsorted DataFrame
                # Check if the specified column is empty
                if self.data[self._column].empty:
                    self._logger.warning(
                        f"The column '{self._column}' is empty."
                    )
                    return self.data
            # Sort the DataFrame by the specified column
            df = self.data.sort_values(
                by=self._column,
                ascending=self._ascending,
                **self.pd_args
            ).reset_index(drop=True)
            self.add_metric('ORDER_BY', self._column)
            return df
        except Exception as err:
            raise ComponentError(
                f"Generic Error on Data: error: {err}"
            ) from err
