import asyncio
from collections.abc import Callable
from pathlib import Path
import numpy as np
import pandas as pd
import orjson
import ast
from asyncdb.exceptions import NoDataFound
from ..exceptions import ComponentError, DataNotFound, TaskError
from ..utils import cPrint
from .flow import FlowComponent
from ..conf import TASK_PATH
from ..interfaces import DBSupport, TemplateSupport
from ..interfaces.qs import QSSupport


class AddDataset(QSSupport, DBSupport, TemplateSupport, FlowComponent):
    """
    AddDataset Component

        Overview

        This component joins two pandas DataFrames based on specified criteria.
        It supports various join types and handles cases where one of the DataFrames might be empty.

        :widths: auto

    |  fields                   |   Yes    | List of field names to retrieve from the second dataset                                              |
    |  dataset                  |   Yes    | Name of the second dataset to retrieve                                                               |
    |  datasource               |   No     | Source of the second dataset ("datasets" or "vision") (default: "datasets")                          |
    |  join                     |   No     | List of columns to use for joining the DataFrames                                                    |
    |  type                     |   No     | Type of join to perform (left, inner) (default: left)                                                |
    |  no_copy                  |   No     | If True, modifies original DataFrames instead of creating a copy (default: False)                    |
    |  distinct                 |   No     | If True, retrieves distinct rows based on join columns (default: False)                              |
    |  operator                 |   No     | Operator to use for joining rows (currently only "and" supported)                                    |
    |  join_with                |   No     | List of columns for a series of left joins (if main DataFrame has unmatched rows)                    |
    |  datatypes                |   No     | Dictionary specifying data types for columns in the second dataset                                   |
    |  infer_types              |   No     | If True, attempts to infer better data types for object columns (default: False)                     |
    |  to_string                |   No     | If True, attempts to convert object columns to strings during data type conversion (default: True)   |
    |  as_objects               |   No     | If True, creates resulting DataFrame with all columns as objects (default: False)                    |
    |  drop_empty               |   No     | If True, drops columns with only missing values after join (default: False)                          |
    |  dropna                   |   No     | List of columns to remove rows with missing values after join                                        |
    |  clean_strings            |   No     | If True, replaces missing values in object/string columns with empty strings (default: False)        |
    |  Group                    |   No     | usually used FormData                                                                                |
    |  skipError                |   No     | spected = skip - Log Errors - Enforce                                                                |
    |  driver                   |   No     | Database driver to use (e.g., "pg", "bigquery", "mysql") (default: "pg")                    |

            Returns the joined DataFrame and a metric ("JOINED_ROWS")
            representing the number of rows in the result.



        Example:


        Example with BigQuery:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          AddDataset:
          datasource: banco_chile
          dataset: vw_form_metadata
          distinct: true
          type: left
          fields:
          - formid
          - form_name
          - column_name
          - description as question
          join:
          - formid
          - column_name
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
        self.df1: pd.DataFrame = None
        self.df2: pd.DataFrame = None
        self.type: str = "left"
        self._dtypes: dict = {}
        self.infer_types: bool = False
        self.to_string: bool = True
        self.as_objects: bool = False
        self.use_dataframe: bool = kwargs.pop("use_dataframe", False)
        self.datasource: str = kwargs.pop("datasource", "datasets")
        self.driver: str = kwargs.pop("driver", "pg")  # Default to PostgreSQL
        self._driver = self.driver  # Set _driver like QueryToPandas
        self.use_qs_parser: bool = kwargs.pop("use_qs_parser", True)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self._no_warnings = True

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        try:
            if self._multi:
                self.df1 = self.previous[0].output()
            else:
                self.df1 = self.previous.output()
        except IndexError as ex:
            raise ComponentError("Missing LEFT Dataframe") from ex
        ### check info for creating the second dataset:
        self.df2 = None
        # check if "file_sql" exists:
        if hasattr(self, "file_sql"):
            file_path = Path(TASK_PATH).joinpath(self._program, "sql", self.file_sql)
            if file_path.exists() and file_path.is_file():
                self.query = await self.open_tmpfile(file_path)
            else:
                raise TaskError(
                    f"Missing SQL File: {file_path}"
                )
        elif hasattr(self, "query") and self.query:
            # Check-in if query:
            self.query = self.mask_replacement(
                self.query
            )
        else:
            if not hasattr(self, "fields"):
                raise TaskError("Wrong Task configuration: AddDataset needs *fields* declaration.")
            if not hasattr(self, "dataset"):
                raise TaskError(
                    "Wrong Task configuration: need *dataset* name declaration."
                )
            if not hasattr(self, "datasource"):
                self.datasource = "datasets"
        await super().start(**kwargs)
        self.processing_credentials()
        return True

    def _normalize_rows(self, rows):
        """Normalize provider/query results to a list of dictionaries."""
        if rows is None:
            return []
        if isinstance(rows, pd.DataFrame):
            return rows.to_dict(orient="records")
        if isinstance(rows, dict):
            return [rows]
        if isinstance(rows, (list, tuple)):
            normalized = []
            for row in rows:
                if isinstance(row, dict):
                    normalized.append(row)
                else:
                    normalized.append(dict(row))
            return normalized
        return list(rows)

    async def _query_with_connection(self, conn, query: str):
        """Legacy query path using direct driver connection."""
        result, error = await conn.query(query)
        if error:
            raise DataNotFound(error)
        return self._normalize_rows(result)

    async def _query_with_qs(self, query: str):
        """Query path through QuerySource parser/provider pipeline."""
        from querysource.queries.qs import QS as QuerySourceQS

        qry = QuerySourceQS(
            query=query,
            driver=self._driver,
            conditions={},
            loop=self._loop,
            lazy=True,
        )
        try:
            result, error = await qry.query()
            if error:
                raise DataNotFound(error)
            return self._normalize_rows(result)
        finally:
            try:
                await qry.close()
            except Exception as ex:  # pylint: disable=W0703
                self._logger.warning(ex)

    async def _query_with_fallback(self, conn, query: str):
        """Try QuerySource parser path first, fallback to legacy direct query path."""
        if self.use_qs_parser:
            try:
                return await self._query_with_qs(query)
            except NoDataFound:
                return []
            except Exception as err:  # pylint: disable=W0703
                self._logger.warning(
                    "AddDataset: QS parser path failed, using legacy fallback: %s",
                    err,
                )
        return await self._query_with_connection(conn, query)

    async def run(self):
        args = {}
        if self.df1.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1")
        self._logger.debug(f"AddDataset: datasource={self.datasource}, driver={getattr(self, 'driver', 'not set')}")
        
        # Use the same logic as QueryToPandas
        if self.datasource in ("datasets", "vision"):
            # using current datasets on pg database
            self._logger.debug("AddDataset: Using PostgreSQL for datasets/vision")
            connection = self.pg_connection()
        else:
            # Use create_connection() like QueryToPandas
            self._logger.debug(f"AddDataset: Using create_connection() with driver: {self._driver}")
            connection = await self.create_connection()
        try:
            ### TODO: instrumentation for getting dataset from different sources
            async with await connection.connection() as conn:
                if self.use_dataframe is True:
                    # from list self.join (list of columns), extract the unique list from self.data
                    # extract a list of unique from self.data:
                    result = []
                    _filter = self.data[self.join].drop_duplicates().to_dict(orient="records")
                    for element in _filter:
                        query = self.query.format(**element)
                        r = await self._query_with_fallback(conn, query)
                        result.extend(r)
                    if not result:
                        raise DataNotFound(
                            "Empty Dataset: No data was found on query"
                        )
                else:
                    fields = ", ".join(self.fields)
                    if hasattr(self, 'query'):
                        query = self.query
                    elif hasattr(self, "distinct"):
                        join = ", ".join(self.join)
                        if self.driver == "bigquery":
                            query = f"SELECT DISTINCT {fields} FROM {self.datasource}.{self.dataset}"
                        else:
                            query = f"SELECT DISTINCT ON ({join}) {fields} FROM {self.datasource}.{self.dataset}"
                    else:
                        query = f"SELECT {fields} FROM {self.datasource}.{self.dataset}"
                    self._logger.info(
                        f"DATASET QUERY: {query}"
                    )
                    result = await self._query_with_fallback(conn, query)
                    if not result:
                        raise DataNotFound(
                            "Empty Dataset: No data was found on query"
                        )
                ## converting on Dataframe:
                self.df2 = await self.get_dataframe(result, infer_types=True)
        except (DataNotFound, NoDataFound) as exc:
            self._result = self.data
            raise DataNotFound(str(exc)) from exc
        if self.type == "left" and (self.df2 is None or self.df2.empty):
            self._logger.warning(
                "No data was found on right Dataframe, returned first dataframe."
            )
            self._result = self.df1
            return self._result
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound("Data Was Not Found on Dataset")
        if hasattr(self, "no_copy"):
            args["copy"] = self.no_copy
        if not self.type:
            self.type = "left"
        if self.type == "inner":
            args["left_index"] = True
        if hasattr(self, "args") and isinstance(self.args, dict):
            args = {**args, **self.args}
        if hasattr(self, "operator"):
            operator = self.operator
        else:
            operator = "and"
            if hasattr(self, "join"):
                args["on"] = self.join
            else:
                args["left_index"] = True
        # making a Join between 2 dataframes
        try:
            if operator == "and":
                df = pd.merge(
                    self.df1,
                    self.df2,
                    how=self.type,
                    suffixes=("_left", "_right"),
                    **args,
                )
            else:
                if hasattr(self, "join"):
                    args["left_on"] = self.join
                else:
                    args["left_index"] = True
                ndf = self.df1
                sdf = self.df2.copy()
                merge = []
                for key in self.join_with:
                    d = pd.merge(
                        ndf,
                        sdf,
                        right_on=key,
                        how=self.type,
                        suffixes=("_left", None),
                        **args,
                    )
                    ndf = d[d[key].isnull()]
                    ndf.drop(
                        ndf.columns[ndf.columns.str.contains("_left")],
                        axis=1,
                        inplace=True,
                    )
                    ddf = d[d[key].notnull()]
                    ddf.drop(
                        ddf.columns[ddf.columns.str.contains("_left")],
                        axis=1,
                        inplace=True,
                    )
                    merge.append(ddf)
                # merge the last (not matched) rows
                merge.append(ndf)
                df = pd.concat(merge, axis=0)
                df.reset_index(drop=True)
                df.is_copy = None
        except (ValueError, KeyError) as err:
            raise ComponentError(f"Cannot Join with missing Column: {err!s}") from err
        except Exception as err:
            raise ComponentError(f"Unknown JOIN error {err!s}") from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound("Cannot make any JOIN, returns zero coincidences")
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        print("ON END> ", numrows)
        self.add_metric("JOINED_ROWS", numrows)
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        # helping some transformations
        df.is_copy = None
        self._result = df
        return self._result

    async def close(self):
        pass

    async def get_dataframe(self, result, infer_types: bool = False):
        self.set_datatypes()
        print(self._dtypes)
        ### TODO: using QS iterables instead
        result = self._normalize_rows(result)
        try:
            if self.as_objects is True:
                df = pd.DataFrame(result, dtype=object)
            else:
                df = pd.DataFrame(result, **self._dtypes)
        except Exception as err:  # pylint: disable=W0718
            self._logger.exception(
                err,
                stack_info=True
            )
        # Attempt to infer better dtypes for object columns.
        if hasattr(self, "infer_types") or infer_types is True:
            df.infer_objects()
            df = df.convert_dtypes(convert_string=self.to_string)
        if self._debug is True:
            cPrint("Data Types:")
            print(df.dtypes)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if getattr(self, "clean_strings", False) is True:
            u = df.select_dtypes(include=["object", "string"])
            df[u.columns] = u.fillna("")

        for col in df.columns:
            if df[col].dtype == 'object':
                first_val = df[col].dropna().astype(str).head(1)
                if not first_val.empty and first_val.iloc[0].strip().startswith(('{', '[')):
                    def _try_parse(v):
                        if not isinstance(v, str):
                            return v
                        s = v.strip()
                        if not s or s.lower() in ('none', 'null', 'nan'):
                            return None
                        try:
                            return orjson.loads(s)
                        except Exception:
                            try:
                                return ast.literal_eval(s)
                            except Exception:
                                return v 
                    df[col] = df[col].apply(_try_parse)
                    self._logger.debug(f"Auto-parsed JSON column: {col}")
        return df

    def set_datatypes(self):
        if hasattr(self, "datatypes"):
            dtypes = {}
            for field, dtype in self.datatypes.items():
                if dtype == "uint8":
                    dtypes[field] = np.uint8
                elif dtype == "uint16":
                    dtypes[field] = np.uint16
                elif dtype == "uint32":
                    dtypes[field] = np.uint32
                elif dtype == "int8":
                    dtypes[field] = np.int8
                elif dtype == "int16":
                    dtypes[field] = np.int16
                elif dtype == "int32":
                    dtypes[field] = np.int32
                elif dtype == "float":
                    dtypes[field] = float
                elif dtype == "float32":
                    dtypes[field] = float
                elif dtype in ("string", "varchar", "str"):
                    dtypes[field] = str
                else:
                    # invalid datatype
                    self._logger.warning(
                        f"Invalid DataType value: {field} for field {dtype}"
                    )
                    continue
            if dtypes:
                self._dtypes["dtype"] = dtypes
