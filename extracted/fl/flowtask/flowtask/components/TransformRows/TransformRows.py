import asyncio
import copy
from typing import Any, Union
from collections.abc import Callable
import pandas
import numpy as np
from datamodel.typedefs.types import AttrDict
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from querysource.types import strtobool
from querysource.types.dt import transforms as qsdfunctions
from . import functions as dffunctions
from ...exceptions import (
    ComponentError,
    DataNotFound,
    ConfigError
)
from ...utils.executor import getFunction
from ...utils.functions import check_empty
from ..flow import FlowComponent


class TransformRows(FlowComponent):
    """
    TransformRows

    Overview

        The TransformRows class is a component for transforming, adding, or modifying rows in a Pandas DataFrame based on
        specified criteria. It supports single and multiple DataFrame transformations, and various operations on columns.

    :widths: auto

        | fields             |   No     | A dictionary defining the fields and corresponding transformations to be applied.                     |
        | filter_conditions  |   No     | A dictionary defining the filter conditions for transformations.                                      |
        | clean_notnull      |   No     | Boolean flag indicating if non-null values should be cleaned, defaults to True.                       |
        | replace_columns    |   No     | Boolean flag indicating if columns should be replaced, defaults to False.                             |
        | multi              |   No     | Boolean flag indicating if multiple DataFrame transformations should be supported, defaults to False. |
        | function           |   No     | View the list of function in the functions.py file on this directory                                  |
        | _applied           |   No     | List to store the applied transformations.                                                            |

    Return

        The methods in this class manage the transformation of DataFrames, including initialization, execution, and result handling.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TransformRows:
          fields:
          display_name:
          value:
          - concat
          - columns:
          - first_name
          - last_name
          legal_address:
          value:
          - concat
          - columns:
          - legal_street_address_1
          - legal_street_address_2
          work_address:
          value:
          - concat
          - columns:
          - work_location_address_1
          - work_location_address_2
          first_name:
          value:
          - capitalize
          last_name:
          value:
          - capitalize
          warp_id:
          value:
          - nullif
          - chars:
          - '*'
          old_warp_id:
          value:
          - nullif
          - chars:
          - '*'
          worker_category_description:
          value:
          - case
          - column: benefits_eligibility_class_code
          condition: PART-TIME
          match: Part Time
          notmatch: Full Time
          file_number:
          value:
          - ereplace
          - columns:
          - position_id
          - payroll_group
          newvalue: ''
          original_hire_date:
          value:
          - convert_to_datetime
          hire_date:
          value:
          - convert_to_datetime
          start_date:
          value:
          - convert_to_datetime
          updated:
          value:
          - convert_to_datetime
          gender_code:
          value:
          - convert_to_string
          payroll_id:
          value:
          - convert_to_string
          reports_to_payroll_id:
          value:
          - convert_to_string
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
        self.fields: dict = {}
        self.filter_conditions: dict = {}
        self.clean_notnull: bool = True
        self.replace_columns: bool = False
        self._applied: list = []
        replace_cols = kwargs.pop("replace_columns", False)
        if isinstance(replace_cols, str):
            self.replace_columns = strtobool(replace_cols)
        else:
            self.replace_columns = bool(replace_cols)
        # support for multiple dataframe transformations
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        if self.multi is False:
            if "fields" in kwargs:
                self.fields = kwargs["fields"]
                del kwargs["fields"]
        else:
            self.fields = {}
        super(TransformRows, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._logger.debug(f"Using Replace Columns: {self.replace_columns}")

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("a Previous Component was not found.")
        if check_empty(self.data):
            raise DataNotFound("No data was found")

    async def run(self):
        if self.data is None:
            return False
        if isinstance(self.data, pandas.DataFrame):
            self.add_metric("started_rows", self.data.shape[0])
            self.add_metric("started_columns", self.data.shape[1])
            df = await self.transform(self, self.data)
            self._result = df
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            return self._result
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    f"TransformRows: Invalid Result type for Multiple: {err}"
                ) from err
            self._result = {}
            for name, rs in result:
                try:
                    el = getattr(self, name)
                except AttributeError:
                    self._result[name] = rs
                    continue
                df = await self.transform(AttrDict(el), rs)
                self._result[name] = df
            return self._result
        else:
            raise NoDataFound(
                "TransformRows: Pandas Dataframe Empty or is not a Dataframe"
            )

    async def _scalar_column(
        self,
        it: pandas.DataFrame,
        field: str,
        val: Any
    ) -> None:
        """_scalar_column.

        Operating the Dataframe Function Column as an Scalar Value.
        """
        try:
            if val.startswith('{'):
                it[field] = self.mask_replacement(val)
            else:
                it[field] = it[val]
                if self.replace_columns is True:
                    it.drop(val, axis="columns", inplace=True)
        except KeyError:
            self._logger.error(
                f"Column doesn't exists: {val}"
            )
        except Exception as e:
            self._logger.error(
                f"Error dropping Column: {val}, {e}"
            )

    def _get_df_function(self, fn: str) -> Union[Callable, None]:
        func = getattr(dffunctions, fn, None)
        if func is None:
            func = getattr(qsdfunctions, fn)
        return func

    async def _check_condition(self, df, field: str, fname: str, conditions: dict):
        """Check if a field meets the specified condition."""
        # Check column existence
        if conditions.get("exists") and field not in df.columns:
            return False

        # Check for specific criteria (e.g., column must have non-null values)
        if "not_null" in conditions and conditions["not_null"]:
            try:
                if df[field].notnull().all():
                    return False
            except KeyError:
                return False

        # TODO: add more conditions to check
        return True

    async def _apply_one(
        self,
        it: pandas.DataFrame,
        field: str,
        val: Any
    ) -> None:
        """_apply_one.

        Processing "fields" attributes as a Dictionary.
        Apply to one column only.
        """
        conditions = {}
        if "conditions" in val:
            conditions = val.get('conditions')
            if not isinstance(conditions, dict):
                self._logger.warning(
                    f"TranformRows conditions need to be a dictionary, got {type(conditions)}"
                )
        args = {}
        if isinstance(val, dict):
            args = {k: v for k, v in val.items() if k not in ("value", "conditions")}

        if "value" in val:
            operation = val.get('value')
            if isinstance(operation, list):
                operation = operation.copy()
        else:
            operation = val
        
        try:
            fname = operation.pop(0)
        except AttributeError:
            fname = operation
            operation = []
        self._applied.append(f"Function: {fname!s} args: {operation}")
        if not await self._check_condition(it, field, fname, conditions):
            self._logger.warning(
                f"Column {field} not met conditions {conditions}"
            )
            return it  # Skip transformation if condition fails
        # fname is a field and len > 1
        if fname in it.columns and len(operation) == 0 and not args:
            # simple field replacement
            it[field] = it[fname]
            it = it.copy()
            return it

        # only calls functions on TransformRows scope:
        # first, check if is a Pandas-based Function
        if not args:
            try:
                args = operation[0]
            except IndexError:
                args = {}
        try:
            func = self._get_df_function(fname)
            self._logger.notice(
                f"Calling Function: {fname!s} with args: {operation}"
            )
            if fname == "fill_column":
                args["variables"] = self._variables
            if args:
                it = func(df=it, field=field, **args)
            else:
                it = func(df=it, field=field)
            it = it.copy()
            return it
        except AttributeError:
            pass
        # try to apply an scalar function:
        func = getFunction(fname)
        if callable(func):
            # SCALAR FUNCTION
            try:
                tmp = operation[0]
                for a, b in tmp.items():
                    if isinstance(b, list):
                        for idx, el in enumerate(b):
                            if el in self._variables:
                                b[idx] = el.replace(
                                    str(el),
                                    str(self._variables[str(el)]),
                                )
                    if b in self._variables:
                        args[a] = b.replace(
                            str(b), str(self._variables[str(b)])
                        )
                result = func(**args)
            except (KeyError, IndexError, ValueError):
                result = func()
            except Exception as err:
                self._logger.warning(
                    f"Error or missing DF Function: {err!s}"
                )
                # using scalar functions to set value in columns
                func = getFunction(fname)
                if not callable(func):
                    return it
                self._logger.debug(
                    f"Calling Scalar: {fname!s}: {func}"
                )
                try:
                    args = operation[0]
                    tmp = operation[0]
                except IndexError:
                    args = {}
                try:
                    for a, b in tmp.items():
                        if b in self._variables:
                            args[a] = b.replace(
                                str(b), str(self._variables[str(b)])
                            )
                    result = func(**args)
                except (TypeError, KeyError, IndexError, ValueError):
                    # result doesn't need keyword arguments
                    result = func()
                except Exception as e:
                    print(func, fname, field, val)
                    self._logger.exception(
                        f"Error Running an Scalar Function {fname!s} \
                        to set Dataframe: {e}"
                    )
                    return it
            r = {field: result}
            it = it.assign(**r)
            it = it.copy()
            return it
        else:
            self._logger.warning(
                f"Function {func} is not callable."
            )
        return it

    async def _apply_multiple(
        self,
        it: pandas.DataFrame,
        field: str,
        val: Any
    ) -> None:
        """_apply_multiple.

        Apply Multiples functions to a single column.
        """
        if isinstance(val, dict):
            for fn, args in val.items():
                try:
                    func = self._get_df_function(fn)
                    self._logger.notice(
                        f"Calling Function: {fn!s} with args: {args}"
                    )
                    if not args:
                        args = {}
                    it = func(df=it, field=field, **args)
                    it = it.copy()
                except AttributeError:
                    pass
            return it
        for value in val:
            # iterate over a list of possible functions:
            if isinstance(value, str):
                # create the column based on value
                await self._scalar_column(it, field, value)
                continue
            if isinstance(value, dict):
                # function dictionary: {'split': {'separator': ','}}
                # TODO: for now, only work with dataframe functions:
                for fn, args in value.items():
                    try:
                        func = self._get_df_function(fn)
                        self._logger.notice(
                            f"Calling Function: {fn!s} with args: {args}"
                        )
                        if not args:
                            args = {}
                        it = func(df=it, field=field, **args)
                        it = it.copy()
                    except AttributeError:
                        pass
            elif isinstance(value, list):
                # list of functions to be applied:
                # split the list element in fn and arguments
                fn, args = value if len(value) == 2 else (value[0], {})
                func = self._get_df_function(fn)
                if func is not None:
                    it = func(df=it, field=field, **args)
                    it = it.copy()
                else:
                    self._logger.warning(
                        f"Function {fn} is not callable."
                    )
            else:
                raise ConfigError(
                    f"Unable to work with this Function {value}: {type(value)}"
                )
        return it

    async def transform(self, elem, df):
        try:
            fields = copy.deepcopy(elem.fields)
        except KeyError:
            fields = {}
        if not isinstance(df, pandas.DataFrame):
            raise NoDataFound("Pandas Dataframe Empty or is not a Dataframe")
        if hasattr(elem, "clean_dates"):
            u = df.select_dtypes(include=["datetime64[ns]"])
            df[u.columns] = df[u.columns].replace({np.nan: None})
        it = df.copy()
        for field, val in fields.items():
            if isinstance(val, str):
                await self._scalar_column(it, field, val)
                continue
            elif isinstance(val, (int, float, bool)):
                it[field] = val
                continue
            elif isinstance(val, dict) and 'value' in val:
                # Function to be applied:
                it = await self._apply_one(it, field, val)
                continue
            elif isinstance(val, (dict, list)):
                # Applying multiple functions to same column:
                it = await self._apply_multiple(it, field, val)
                continue
        # at the end
        df = it
        # starting changes:
        if hasattr(elem, "clean_str"):
            df.is_copy = None
            u = df.select_dtypes(include=["object", "string"])
            u = u.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df[u.columns] = df[u.columns].fillna("")
        if hasattr(elem, "drop_empty"):
            # First filter out those rows which
            # does not contain any data
            df.dropna(how="all")
            # removing empty cols
            df.is_copy = None
            df.dropna(axis=1, how="all")
            df.dropna(axis=0, how="all")
        if self._debug is True:
            print("TRANSFORM ===")
            print(df)
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        # avoid threat the Dataframe as a Copy
        df.is_copy = None
        self._result = df
        try:
            self.add_metric("ended_rows", df.shape[0])
            self.add_metric("ended_columns", df.shape[1])
            self.add_metric("Transformations", self._applied)
        except Exception as err:
            logging.error(f"TransformRows: Error setting Metrics: {err}")
        return self._result

    def close(self):
        pass
