import asyncio
from typing import Any
from collections.abc import Callable
import pandas as pd
from querysource.exceptions import DriverError, QueryException
from ..exceptions import ComponentError
from .flow import FlowComponent


class tMelt(FlowComponent):
    """
    tMelt

        Overview

            The tMelt class is a component for transforming a DataFrame from a wide format to a long format using the
            Pandas `melt` function. It reshapes data by unpivoting columns, making it easier to analyze or process data
            with a simpler, long-form structure.

        :widths: auto

            | index          |   Yes    | Column(s) to use as identifier variables for melting.                     |
            | name           |   No     | Name to use for the "variable" column in the result DataFrame.            |
            |                |          | Defaults to "name".                                                       |
            | value          |   No     | Name to use for the "value" column in the result DataFrame.               |
            |                |          | Defaults to "value".                                                      |
            | values         |   No     | List of columns to unpivot. If None, all remaining columns are used.      |

        Returns

            This component returns a DataFrame in long format where specified columns are unpivoted to create two
            new columns: one for variable names (`name`) and one for values (`value`). Metrics on the row and column
            counts of the transformed DataFrame are recorded. Any errors during transformation are logged and raised
            with descriptive error messages.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tMelt:
          index:
          - AL No.
          - Store Format
          name: product_name
          value: displays_quantity
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
        self.df1: Any = None
        self.df2: Any = None
        self.type = None
        super(tMelt, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe", status=404)
        if not hasattr(self, "index"):
            raise DriverError("Crosstab Transform: Missing Index on definition")
        if not hasattr(self, "name"):
            self.name = "name"
        if not hasattr(self, "value"):
            self.value = "value"

        if not hasattr(self, "values"):
            self.values = None

        return True

    async def close(self):
        pass

    async def run(self):
        try:
            df = pd.melt(
                self.data, id_vars=self.index, var_name=self.name, value_name=self.value
            )
            self._result = df
            self.add_metric("NUM_ROWS", self._result.shape[0])
            self.add_metric("NUM_COLUMNS", self._result.shape[1])
            if self._debug:
                print("Debugging: tCrosstab ===")
                print(self._result)
                columns = list(self._result.columns)
                for column in columns:
                    t = self._result[column].dtype
                    print(column, "->", t, "->", self._result[column].iloc[0])
            return self._result
        except (ValueError, KeyError) as err:
            raise QueryException(f"Crosstab Error: {err!s}") from err
        except Exception as err:
            raise QueryException(f"Unknown error {err!s}") from err
