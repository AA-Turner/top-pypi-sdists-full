import asyncio
from typing import Any, Union
from collections.abc import Callable
import pandas
from pandas import DataFrame
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent


class tPandas(FlowComponent):
    """
    tPandas

        Overview

            The tPandas class is an abstract interface for performing various data transformations on Pandas DataFrames.
            It provides foundational methods and structure for components that need to apply transformations, merges, or other
            DataFrame operations within a task.

            This interface provides methods to initialize, transform, and debug Pandas DataFrame operations.
            Concrete implementations using `tPandas` can define specific transformations. On execution, metrics
            for rows and columns are recorded, and any transformation errors or data mismatches are raised as exceptions
            with detailed error messages for effective debugging.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tPandas:
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
        self.df1: Union[DataFrame, Any] = None
        self.df2: Union[DataFrame, Any] = None
        self.type: str = None
        self.condition: str = ''
        # Pandas Arguments:
        self.pd_args = kwargs.pop("pd_args", {})
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data: DataFrame = self.input

            if hasattr(self, "_multi") and self._multi:
                self.df1: DataFrame = self.previous[0].output()
                try:
                    self.df2: DataFrame = self.previous[1].output()
                except IndexError:
                    self.df2 = None
            else:
                if not isinstance(self.data, DataFrame):
                    raise ComponentError("Incompatible Pandas Dataframe", status=404)
        else:
            raise DataNotFound("Data Not Found", status=404)

        await super().start(**kwargs)
        return True

    async def close(self):
        pass

    async def run(self):
        self._result = self.data
        try:
            df = await self._run()
            if df.empty:
                raise DataNotFound(
                    f"Data not Found over {self.__name__}"
                )
            self._result = df
            self.add_metric("NUM_ROWS", self._result.shape[0])
            self.add_metric("NUM_COLUMNS", self._result.shape[1])
            if self._debug:
                print(f"Debugging: {self.__name__} ===")
                print(self._result)
                columns = list(self._result.columns)
                for column in columns:
                    t = self._result[column].dtype
                    print(
                        column, "->", t, "->", self._result[column].iloc[0]
                    )
            return self._result
        except DataNotFound:
            raise
        except (ValueError, KeyError) as err:
            raise ComponentError(
                f"{self.__name__} Error: {err!s}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"{self.__name__} Exception {err!s}"
            ) from err
