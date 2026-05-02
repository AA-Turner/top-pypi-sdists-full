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
from . import getComponent


class FilterIf(FlowComponent):
    """
    FilterIf.

        Overview

            The FilterIf is a component that applies specified filters to a Pandas DataFrame.
            if the condition is met, the row is kept, otherwise it is discarded.
            at result set (if any) will be executed a subset of components.

        :widths: auto

            | operator     |   Yes    | Logical operator (e.g., `and`, `or`) used to combine filter conditions.   |
            | conditions   |   Yes    | List of conditions with columns, values, and expressions for filtering.   |
            |              |          | Format: `{ "column": <col_name>, "value": <val>, "expression": <expr> }`  |
            | filter       |   Yes    | List of conditions with columns, values, and expressions for filtering.   |
            |              |          | Format: `{ "column": <col_name>, "value": <val>, "expression": <expr> }`  |
            | true_condition|  Yes    | List of components to execute if the condition is met.                   |
            | false_condition| Yes    | List of components to execute if the condition is not met.               |
            | passthrough |   No     | If True, the component will pass through the data without filtering.      |
        Returns

            This component returns a filtered Pandas DataFrame based on the provided conditions.
            The component tracks metrics such as the initial and filtered row counts,
            and optionally limits the returned columns if specified.
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
          - FilterIf:
          operator: "&"
          filter:
          - column: previous_form_id
          expression: not_null
          true_condition:
          - TransformRows:
          replace_columns: true
          fields:
          form_id: previous_form_id
          - ExecuteSQL:
          file_sql: delete_previous_form.sql
          use_template: true
          use_dataframe: true
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
        self.true_condition = kwargs.pop('true_condition', [])
        self.false_condition = kwargs.pop('false_condition', [])
        self.filter_conditions: dict = {}
        self._passthrough = kwargs.pop('passthrough', False)
        super(FilterIf, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "Data Not Found"
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe"
            )
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

    def _define_step(self, cpobj: FlowComponent, params: dict) -> Callable:
        params["ENV"] = self._environment
        if hasattr(self, "_program"):
            params["_program"] = self._program
        # params
        params["params"] = self._params
        # parameters
        params["parameters"] = self._parameters
        # useful to change variables in set var components
        params["_vars"] = self._vars
        # variables dictionary
        params["variables"] = self._variables
        params["_args"] = self._args
        # argument list for components (or tasks) that need argument lists
        params["arguments"] = self._arguments
        params["debug"] = self._debug
        params["argparser"] = self._argparser
        # the current in-memory connector
        params["memory"] = self._memory
        try:
            job = cpobj(
                job=self,
                loop=self._loop,
                # stat=self.stat,
                **params
            )
            return job
        except TypeError as err:
            raise ComponentError(
                f"Component {cpobj} is not callable: {err}"
            ) from err
        except AttributeError as err:
            raise ComponentError(
                f"Component {cpobj} not found: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"Generic Component Error on {cpobj}, error: {err}"
            ) from err

    async def _execute_components(
        self,
        components: list,
        df: pd.DataFrame
    ) -> None:
        """
        Execute a list of components with the given DataFrame.
        Args:
            components (list): List of components to execute.
            df (pd.DataFrame): DataFrame to pass to the components.
        """
        inner_result = df
        for component in components:
            try:
                # component is a dict, split into key and values:
                component_name = list(component.keys())[0]
                args = component[component_name]
                cpobj = getComponent(component_name)
                # check if component is callable:
                if not callable(cpobj):
                    raise ComponentError(
                        f"Component {component_name} is not callable."
                    )
                step = self._define_step(cpobj, args)
                step.input = inner_result
                async with step as comp:
                    try:
                        result = await comp.run()
                        if isinstance(result, bool):
                            result = step.input
                        if result is None or result.empty:
                            self._logger.warning(
                                f"No Data was Found after Executing {component_name}."
                            )
                        self._logger.notice(
                            f"Component {component_name} executed successfully."
                        )
                        inner_result = result
                    except Exception as e:
                        self._logger.error(
                            f"Error executing component {component_name}: {e}"
                        )
            except ComponentError as exc:
                raise ComponentError(
                    f"Component {component_name} not found: {exc}"
                ) from exc

    async def run(self):
        self.add_metric("STARTED_ROWS", len(self.data.index))
        if not self.filter:
            raise ConfigError(
                "No Filter Conditions were Found."
            )
        if not self.operator:
            self.operator = '&'
        df = self.data.copy()
        # iterate over all filtering conditions:
        df = self._filter_conditions(df)
        # Applying filter expressions by Column:
        if self.fields:
            df = self._filter_fields()
        if self.filter:
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
            self._logger.warning(
                "No Data was Found after Filtering."
            )
            self._result = self.data
            return self._result
        # if the condition is met, execute true_condition
        if self.true_condition:
            await self._execute_components(
                self.true_condition,
                df
            )
        # if the condition is not met, execute false_condition
        # if self.false_condition:
        #     await self._execute_components(
        #         self.false_condition,
        #         df
        #     )
        self.add_metric(
            "FILTERED_ROWS", len(df.index)
        )
        if hasattr(self, "columns"):
            # returning only a subset of data
            df = df[self.columns]
        self.add_metric(
            "FILTERED_COLS", len(df.columns)
        )
        # if passthrough is True, return the original data
        if self._passthrough:
            # data passthrough
            self._result = self.data
        else:
            # filtered data
            self._result = df
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in self._result.dtypes.items():
                print(column, "->", t, "->", self._result[column].iloc[0])
        return self._result
