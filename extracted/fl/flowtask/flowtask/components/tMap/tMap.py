import asyncio
import copy
import re
from typing import Dict, List, Union
from collections.abc import Callable
import pandas as pd
import numpy as np
from navconfig.logging import logging
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from querysource.conf import asyncpg_url
from querysource.types.dt import transforms as qsdfunctions
from ...exceptions import ComponentError
from ...parsers.maps import open_map, open_model
from ..TransformRows import functions as tfunctions
from ...utils.executor import getFunction
from ..flow import FlowComponent
from . import functions as tmapfn


def is_snakecase(value):
    ## already in snake case:
    return re.match(r"^[a-zA-Z][a-zA-Z0-9_]+_[a-zA-Z0-9]*$", value.strip()) is not None


def is_camelcase(value):
    return re.match(r"^[A-Za-z][a-z0-9]*([A-Z][a-z0-9]*)*$", value.strip()) is not None


def is_titlecase(value):
    return re.match(r"^([A-Z][a-z]*\s?)*$", value.strip()) is not None


def camelCase_split(value):
    if bool(re.match(r"[A-Z]+$", value)):
        return re.findall(r"[A-Z]+$", value)
    elif bool(re.search(r"\d", value)):
        return re.findall(r"[A-Z](?:[a-z]+[1-9]?|[A-Z]*(?=[A-Z])|$)", value)
    elif value[0].isupper():
        return re.findall(r"[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", value)
    else:
        # value = value.capitalize()
        return re.findall(r"^[a-z]+|[A-Z][^A-Z]*", value)


class tMap(FlowComponent):
    """
    tMap

    Overview

        The tMap class is a component for transforming and mapping data in a Pandas DataFrame. It supports various column name
        transformations, data type conversions, and function applications to columns. It extends the FlowComponent class and
        provides methods for column information retrieval, data transformation, and function execution.

    :widths: auto

        | tablename        |   No     | The name of the table to retrieve column information from.                                       |
        | schema           |   No     | The schema of the table to retrieve column information from.                                     |
        | model            |   No     | The model to use for data transformation.                                                        |
        | _modelinfo       |   No     | A dictionary containing the model information.                                                   |
        | map              |   No     | The map file to use for column transformations.                                                  |
        | _mapping         |   No     | A dictionary containing the column mappings.                                                     |
        | force_map        |   No     | A flag indicating if the map file should be forced, defaults to False.                           |
        | replace_columns  |   No     | A flag indicating if columns should be replaced, defaults to True.                               |
        | drop_missing     |   No     | A flag indicating if missing columns should be dropped, defaults to False.                       |
        |  column_info     |   Yes    | I access the information of the column through a statement in sql to extract the data            |
        |  clean_names     |   Yes    | Remove duplicate names from data                                                                 |

        Return

        The methods in this class manage the transformation and mapping of data in a Pandas DataFrame, including initialization,
        column information retrieval, data transformation, and function execution.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tMap:
          schema: bose
          map: products_by_store
          drop_missing: false
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
        self.tablename: str = None
        self.schema: str = None
        self.model: str = None
        self._modelinfo: dict = None
        self.map: str = None
        self._mapping: dict = None
        self.force_map: bool = False
        self.replace_columns: bool = True
        self.drop_missing: bool = False
        # use it for getting column information
        self._flavor = kwargs.pop('flavor', 'postgres')
        super(tMap, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        if not self.schema:
            self.schema = self._program

    def _get_df_function(self, fn: str) -> Union[Callable, None]:
        func = getattr(tfunctions, fn, None)
        if func is None:
            func = getattr(qsdfunctions, fn, None)
        return func

    async def column_info(
        self, table: str, schema: str = "public", flavor: str = "postgres"
    ) -> list:
        if not self.force_map:
            result = None
            if flavor == "postgres":
                tablename = f"{schema}.{table}"
                discover = f"""SELECT attname AS column_name, atttypid::regtype
                AS data_type, attnotnull::boolean as notnull
                  FROM pg_attribute WHERE attrelid = '{tablename}'::regclass
                  AND attnum > 0 AND NOT attisdropped ORDER  BY attnum;
                """
                try:
                    try:
                        event_loop = asyncio.get_running_loop()
                    except RuntimeError:
                        event_loop = asyncio.get_event_loop()
                    db = AsyncDB("pg", dsn=asyncpg_url, loop=event_loop)
                    async with await db.connection() as conn:
                        result, error = await conn.query(discover)
                        if error:
                            raise ComponentError(f"Column Info Error {error}")
                except NoDataFound:
                    pass
                finally:
                    db = None
            else:
                raise ValueError(f"Column Info: Flavor not supported yet: {flavor}")
            if result:
                return {item["column_name"]: item["data_type"] for item in result}
        # getting model from file:
        model = await open_model(table, schema)
        if model:
            fields = model["fields"]
            return {field: fields[field]["data_type"] for field in fields}
        else:
            if self.force_map:
                self._logger.debug(
                    f"Open Map: Forcing using of Map File {schema}.{table}"
                )
            else:
                self._logger.error(f"Open Map: Table {schema}.{table} doesn't exist")
            return None

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        # getting model from model or from tablename
        if self.tablename:
            try:
                self._modelinfo = await self.column_info(
                    table=self.tablename, schema=self.schema, flavor=self._flavor
                )
            except Exception as exc:
                self._logger.warning(
                    f"Error getting Table Model for {self.tablename}.{self.schema} : {exc}"
                )
        if hasattr(self, "automap"):
            # Create a Mapping converting columns:
            mapping = {}
            columns = self.data.columns.tolist()
            for col in columns:
                if is_snakecase(col):
                    new_name = col.strip().lower()
                elif is_camelcase(col):
                    new_name = "_".join(
                        [x.lower().strip() for x in camelCase_split(col)]
                    )
                else:
                    new_col = col.replace("(", "").replace(')', '').replace('-', '_').strip()
                    if is_camelcase(new_col):
                        new_name = "_".join(
                            [x.lower().strip() for x in camelCase_split(new_col)]
                        )
                    elif is_titlecase(new_col):
                        new_name = "_".join(
                            [x.lower().strip() for x in new_col.split(" ")]
                        )
                    else:
                        new_name = col.strip()
                mapping[new_name] = col
            self._mapping = mapping
        else:
            try:
                # open a map file:
                self._mapping = await open_map(
                    filename=str(self.map), program=self._program
                )
            except Exception as err:
                raise ComponentError(f"TableMap: Error open Map File: {err}") from err

    async def close(self):
        """
        close.

            close method
        """

    def is_dataframe(self, df) -> bool:
        return isinstance(df, pd.DataFrame)

    async def run(self):
        """
        run.

            Iteration over all dataframes.
        """
        if isinstance(self.data, list):  # a list of dataframes
            pass
        elif isinstance(self.data, dict):  # named queries
            pass
        else:
            # one single dataframe
            if not self.is_dataframe(self.data):
                raise ComponentError(
                    "tMap Error: we're expecting a Pandas Dataframe as source."
                )
            # adding first metrics:
            self.add_metric("started_rows", self.data.shape[0])
            self.add_metric("started_columns", self.data.shape[1])
            df = await self.transform(self.data, copy.deepcopy(self._mapping))
            # check if a column is missing:
            if self.drop_missing is True:
                for column in df.columns:
                    if column not in self._mapping:  # Dropping unused columns
                        df.drop(column, axis="columns", inplace=True)
            self._result = df
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            return self._result

    async def transform(self, df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
        it = {}
        for column, field in mapping.items():
            logging.debug(f"tMap: CALLING {column} for {field}:{type(field)}")
            if isinstance(field, str):  # making a column replacement
                try:
                    if column != field:
                        it[column] = pd.Series(df[field])
                        df.drop(field, axis="columns", inplace=True)
                    else:
                        it[column] = pd.Series(df[column])
                        df.drop(field, axis="columns", inplace=True)
                    continue
                except KeyError:
                    self._logger.error(f"Column doesn't exists: {field}")
                    continue
            elif isinstance(field, list):
                col = field.pop(0)
                if isinstance(col, list):
                    ### combine several columns into one
                    df[column] = df[col].apply("|".join, axis=1)
                    # is a list of columns:
                    try:
                        fname = field.pop(0)
                        try:
                            kwargs = field[0]
                        except IndexError:
                            kwargs = {}
                        try:
                            result = await self.call_function(
                                fname, df, df, column, args=kwargs
                            )
                            it[column] = df[column]
                            if self.replace_columns is True:
                                df.drop(column, axis="columns", inplace=True)
                            continue
                        except Exception:
                            pass
                    except IndexError:
                        # No other changes to made:
                        it[column] = df[column]
                        if self.replace_columns is True:
                            for c in col:
                                df.drop(c, axis="columns", inplace=True)
                            df.drop(column, axis="columns", inplace=True)
                        continue
                if len(field) == 0:
                    if col in df.columns:
                        # there is no change to made:
                        # simple field replacement
                        it[column] = it[col]
                    else:
                        # calling an scalar function:
                        it[column] = await self.call_function(col, None, df, col)
                    continue
                if len(field) > 0:
                    ### Calling a Function with(out) parameters
                    fname = field.pop(0)
                    try:
                        kwargs = field[0]
                    except IndexError:
                        kwargs = {}
                    # Call a Transformation Function on Dataframe:
                    self._logger.debug(
                        f"Calling {fname} with parameters: {kwargs}"
                    )
                    if col in df:
                        result = await self.call_function(fname, df, df, col, args=kwargs)
                        if col in result:
                            it[column] = result[col]
                            if self.replace_columns is True:
                                df.drop(col, axis="columns", inplace=True)
            elif isinstance(field, dict):
                # direct calling of Transform Function
                val = list(field.keys())[0]
                operation = field[val]
                if val != "value":
                    fname = val
                    args = {}
                    if isinstance(operation[0], dict):
                        ## Operation doesn't have a column involved:
                        ## Or columns comes in arguments:
                        args = operation[0]
                        result = await self.call_function(
                            fname, df, df, column, args=args
                        )
                        it[column] = result[column]
                        df.drop(column, axis="columns", inplace=True)
                        continue
                    elif isinstance(operation[-1], dict):
                        args = operation.pop()
                    # all operation are arguments to fname:
                    # print('CALLING > ', fname, operation, args)
                    it[column] = await self.call_function(
                        fname, operation, df, column, args=args
                    )
                else:
                    col = operation.pop(0)  # name of column
                    try:
                        fname = operation.pop(0)
                    except IndexError:
                        ### there is not function to apply:
                        it[column] = result[col]
                        continue
                    try:
                        kwargs = operation[0]
                    except IndexError:
                        kwargs = {}
                    result = await self.call_function(fname, df, df, col, args=kwargs)
                    it[column] = result[col]
                    if self.replace_columns is True:
                        df.drop(col, axis="columns", inplace=True)
        # Join the original DataFrame with the new columns
        df = pd.concat([df, pd.DataFrame(it)], axis=1)
        # Set the index of the new DataFrame
        df.set_index(df.index, inplace=True)
        if self._debug is True:
            columns = list(df.columns)
            print("=== tMap Columns ===")
            for column in columns:
                try:
                    t = df[column].dtype
                except AttributeError:
                    raise ComponentError(f"Error Parsing Column {column}")
                print(column, "->", t, "->", df[column].iloc[0])
            print("===")
            print(df)
        # avoid threat the Dataframe as a Copy
        df.is_copy = None
        try:
            self.add_metric("mapped_rows", df.shape[0])
            self.add_metric("mapped_columns", df.shape[1])
        except Exception as err:  # pylint: disable=W0703
            logging.error(f"TransformRows: Error setting Metrics: {err}")
        return df

    async def call_function(
        self,
        fname: str,
        df: Union[pd.DataFrame, pd.Series, List[str]],
        old_df: pd.DataFrame,
        column: str,
        args: Dict = None,
        **kwargs,
    ) -> Union[pd.DataFrame, pd.Series, None]:
        logging.debug(
            f"tMap: Calling {fname!s} for {column} with args: {args}/{kwargs}"
        )
        if isinstance(df, pd.Series):
            try:
                func = getattr(tmapfn, fname)
            except AttributeError:
                func = getFunction(fname)
        elif isinstance(df, pd.DataFrame):
            try:
                func = self._get_df_function(fname)
            except TypeError as exc:
                raise ComponentError(f"Error on Function name: {fname}, {exc}") from exc
            except AttributeError:
                func = getFunction(fname)
        elif isinstance(df, list):
            try:
                func = getattr(tmapfn, fname)
            except AttributeError:
                func = getFunction(fname)
        else:
            func = getFunction(fname)
        if fname == "fill_column":
            args["variables"] = self._variables
        elif args is None:
            args = {}
        new_args = {**args, **kwargs}
        if callable(func):
            try:
                if isinstance(df, pd.Series):
                    it = func(series=df, field=column, **new_args)
                elif isinstance(df, pd.DataFrame):
                    it = func(df=df, field=column, **new_args)
                elif isinstance(df, list):
                    it = func(old_df, df, **new_args)
                else:
                    it = func(**new_args)
                if np.isscalar(it):
                    it = pd.Series(it, index=old_df.index)
                return it
            except (ValueError, TypeError) as exc:
                logging.warning(f"tMap: Error Calling function {func}: {exc}")
        else:
            logging.warning(f"tMap: Function {func} is not callable.")
            return df
