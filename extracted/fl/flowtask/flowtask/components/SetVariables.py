import asyncio
from typing import Callable
from dateutil import parser
import pandas as pd
from ..exceptions import ComponentError
from .flow import FlowComponent
from ..utils.executor import getFunction


class SetVariables(FlowComponent):
    """
    SetVariables

        Overview

            The SetVariables class is a component for extracting values from data and setting them as variables
            for use in other components. This component can set variables based on specific column values in
            a DataFrame or by executing functions, with support for date formatting and value aggregation.

        :widths: auto

            | vars           |   Yes    | Dictionary defining variables to set with options for format,             |
            |                |          | row selection, and data sources.                                          |

        Returns

            This component returns the original data after setting variables based on the `vars` dictionary.
            Each variable is created from a specified column or function, and supports formatting options
            such as date, timestamp, epoch, or custom string formatting. Metrics are recorded for each variable
            set, and any issues with variable definitions or data retrieval raise a descriptive `ComponentError`.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SetVariables:
          vars:
          max_date:
          - order_date
          - row: max
          min_date:
          - order_date
          - row: min
        ```
    """
    _version = "1.0.0"

    data = None

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        super(SetVariables, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input

    def close(self):
        pass

    async def run(self):
        if hasattr(self, "vars"):
            for var, params in self.vars.items():
                variable = ""
                fname = ""
                try:
                    fname = params[0]
                except (KeyError, IndexError, ValueError) as err:
                    raise ComponentError(
                        f"Error Getting the variable definition: {err}"
                    ) from err
                try:
                    fmt = params[1]["format"]
                except (KeyError, IndexError, ValueError):
                    fmt = None
                # Si existe una columna llamada fname en el dataframe se saca de ahí
                if isinstance(self.data, pd.DataFrame) and fname in self.data.columns:
                    try:
                        try:
                            row = params[1]["row"]
                        except Exception:
                            row = 0
                        if isinstance(row, int):
                            variable = self.data.iloc[row][fname]
                        elif row == "min":
                            variable = self.data[fname].min()
                        elif row == "max":
                            variable = self.data[fname].max()
                        elif row == "array":
                            variable = self.data[fname].unique().tolist()
                        if fmt is not None:
                            # apply Format
                            if fmt == "date":
                                # convert to a date:
                                _var = parser.parse(str(variable))
                                variable = _var.strftime("%Y-%m-%d")
                            elif fmt == "timestamp":
                                _var = parser.parse(str(variable))
                                variable = _var.strftime("%Y-%m-%d %H:%M:%S")
                            elif fmt == "epoch":
                                _var = parser.parse(str(variable))
                                variable = _var.strftime("%s")
                            else:
                                try:
                                    _var = parser.parse(variable)
                                    variable = _var.strftime(fmt)
                                except (parser.ParserError, Exception):
                                    # f-string formatting:
                                    variable = f"{variable:fmt}"
                    except Exception as err:
                        print('E ', err)
                        raise ComponentError(
                            f"Error Getting the variable definition: {err}"
                        ) from err
                # Si no existe se saca de una función
                else:
                    try:
                        func = getFunction(fname)
                        if callable(func):
                            try:
                                args = params[1]
                                variable = func(**args)
                            except (KeyError, IndexError, ValueError):
                                variable = func()
                            if fmt is not None:
                                print("VAR ", variable)
                    except Exception as err:
                        raise ComponentError(
                            f"Error Getting the variable definition: {err}"
                        ) from err
                self.add_metric(
                    f"{self.StepName}_{var!s}", variable
                )
                self._variables[f"{self.StepName}_{var}"] = variable
                self._logger.debug(
                    f"Set Variable: {self.StepName}_{var} to {variable!s}"
                )
                print("VAR: ", f"{self.StepName}_{var}", variable)
        self._result = self.data
        return self._result
