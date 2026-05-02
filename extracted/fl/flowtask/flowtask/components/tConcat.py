import asyncio
from typing import Any
from collections.abc import Callable
import pandas
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent


class tConcat(FlowComponent):
    """
    tConcat

        Overview

            The tConcat class is a component for merging (concatenating) two DataFrames along a specified axis.
            It supports handling multiple DataFrames and configurable options for the concatenation, with metrics
            tracking for input and output row counts.

        :widths: auto

            | df1            |   Yes    | The first DataFrame to concatenate.                                       |
            | df2            |   Yes    | The second DataFrame to concatenate.                                      |
            | args           |   No     | Dictionary of arguments to pass to `pandas.concat`, such as `axis`.       |

        Returns

            This component returns a concatenated DataFrame based on the specified axis and additional arguments.
            Metrics are recorded for the row counts of both input DataFrames and the final concatenated DataFrame.
            If either DataFrame is missing or empty, an error is raised with a descriptive message.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tConcat:
          depends:
          - TransformRows_8
          - TransformRows_15
          args:
          axis: 0
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
        super(tConcat, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe.
        TODO: iterate over all dataframes.
        """
        if self._multi:
            self.df1 = self.previous[0].output()
            self.df2 = self.previous[1].output()
        return True

    async def run(self):
        args = {}
        if self.df1.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1")
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 2")
        if hasattr(self, "args") and isinstance(self.args, dict):
            args = {**args, **self.args}
        if "axis" not in args:
            args["axis"] = 1
        # Adding Metrics:
        _left = len(self.df1.index)
        self.add_metric("LEFT: ", _left)
        _right = len(self.df2.index)
        self.add_metric("RIGHT: ", _right)
        # Concat two dataframes
        try:
            df = pandas.concat([self.df1, self.df2], **args)
        except Exception as err:
            raise ComponentError(
                f"Error Merging Dataframes: {err}"
            ) from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound(
                "Concat: Cannot make any Merge"
            )
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        self.add_metric("JOINED: ", numrows)
        df.is_copy = None
        print(df)
        self._result = df
        return self._result

    async def close(self):
        pass
