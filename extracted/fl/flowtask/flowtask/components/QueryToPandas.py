import logging
import asyncio
from pathlib import Path, PurePath
from collections.abc import Callable
from pprint import pprint
import aiofiles
import urllib3
import pandas as pd
from asyncdb.exceptions import NoDataFound
from querysource.types.validators import Entity
from ..exceptions import (
    ComponentError,
    DataNotFound,
    NotSupported,
    FileError
)
from ..interfaces.qs import QSSupport
from ..utils import cPrint, is_empty, SafeDict
from ..conf import (
    TASK_PATH,
    FILE_STORAGES,
    TASK_STORAGES
)
from ..interfaces.flow import FlowComponent
from ..interfaces import TemplateSupport


urllib3.disable_warnings()
logging.getLogger("urllib3").setLevel(logging.WARNING)


class QueryToPandas(TemplateSupport, FlowComponent, QSSupport):
    """
    QueryToPandas.

    Overview

        This component fetches data using QuerySource and transforms it into a Pandas DataFrame.

    :widths: auto

    | query        |   Yes    | Represents an SQL query                                           |
    | query_slug   |   Yes    | Named queries that are saved in Navigator (QuerySource)           |
    | as_dict      |   Yes    | True | False. if true, it returns the data in JSON format         |
    |              |          | instead of a dataframe                                            |
    | raw_result   |   Yes    | Returns the data in the NATIVE FORMAT of the database for         |
    |              |          | example ( pg RECORDSET)                                           |
    | file_sql     |   Yes    | SQL comes from a sql file                                         |
    | use_template |   Yes    | The component is passed to the SQL file through a  template       |
    |              |          | replacement system                                                |
    | infer_types  |   Yes    | Type inference, give the component the power to decide the data   |
    |              |          | types of each column                                              |
    | drop_empty   |   Yes    | False | True  delete (drop) any column that is empty              |
    | dropna       |   Yes    | False | True  delete all NA (Not a Number)                        |
    | fillna       |   Yes    | False | True  fills with an EMPTY SPACE all the NAs of the        |
    |              |          | dataframe                                                         |
    | clean_strings|   Yes    | Fills with an empty space the NA,but ONLY of the fields of        |
    |              |          | type string                                                       |
    | clean_dates  |   Yes    | Declares NONE any date field that has a NAT (Not a Time)          |
    | conditions   |   Yes    | This attribute allows me to apply conditions to filter the data   |
    | formit       |   Yes    | Form id   (i have doubts about this)                              |
    | orgid        |   Yes    | Organization id     (i have doubts about this)                    |
    | refresh      |   Yes    | Refreshes the data in the QueryToPandas                           |
    | to_string    |   No     | Whether to convert all data to string type. Default is True.      |
    | as_objects   |   No     | Whether to return the result as objects. Default is True.         |
    | datatypes    |   No     | A dictionary specifying data types for columns.                   |
    | datasource   |   No     | The datasource to fetch the data from. Default is "db".           |
    Returns

    This component returns a Pandas DataFrame if the query is successfully executed and data is fetched,
    otherwise raises a ComponentError.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          QueryToPandas:
          query: SELECT formid, orgid FROM banco.forms WHERE enabled = true
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
        self.data = None
        self.infer_types: bool = True
        self.to_string: bool = True
        self._query: dict = {}
        self.as_dict: bool = False
        self.as_objects: bool = True
        self._dtypes: dict = {}
        self.datatypes: dict = {}
        self.use_template: bool = kwargs.get('use_template', False)
        self._driver = kwargs.get("driver", "pg")
        self.use_qs_parser: bool = kwargs.get("use_qs_parser", True)
        # Define if SQL files comes from taskstorage or filestore
        self._use_taskstorage = kwargs.get('use_taskstorage', True)
        # Accept `sql` as an alias for `query` (common in BigQuery-style configs)
        if 'sql' in kwargs and 'query' not in kwargs:
            kwargs['query'] = kwargs.pop('sql')
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        if file.exists() and file.is_file():
            self._logger.debug(f"Opening SQL File: {file}")
            content = None
            # open SQL File:
            async with aiofiles.open(file, "r+") as afp:
                content = await afp.read()
                # check if we need to replace masks
            if hasattr(self, "masks"):
                if "{" in content:
                    content = self.mask_replacement(content)
            if self.use_template is True:
                content = self._templateparser.from_string(content, kwargs)
            elif hasattr(self, "conditions"):
                content = self.conditions_replacement(content)
            return content
        else:
            raise FileError(f"{self.__name__}: Missing SQL File: {file}")

    async def start(self, **kwargs):
        if not self._filestore:
            # we need to calculate which is the filestore
            self._filestore = FILE_STORAGES.get('default')
        if not self._taskstorage:
            self._taskstorage = TASK_STORAGES.get('default')
        if hasattr(self, 'directory'):
            directory = Path(self.directory).resolve()
        if self._use_taskstorage:
            directory = self._taskstorage.get_path().joinpath(self._program, 'sql')
        else:
            directory = self._filestore.get_directory('sql', program=self._program)
        if not directory.exists():
            directory = Path(TASK_PATH).joinpath(self._program, "sql")
        await super(QueryToPandas, self).start(**kwargs)
        # compute conditions:
        self.set_conditions()
        # check if sql comes from a filename:
        if hasattr(self, "file_sql") or hasattr(self, "query_file"):
            # based on a list/dict of queries
            if hasattr(self, "file_sql"):
                query = self.file_sql
            else:
                query = self.query_file
            if isinstance(query, PurePath):
                self._query = []
                if query.exists() and query.is_file():
                    sql = await self.open_sqlfile(query)
                    self._query.append(sql)
            elif isinstance(query, str):
                self._query = []
                try:
                    file_path = directory.joinpath(query)
                    if file_path.exists() and file_path.is_file():
                        sql = await self.open_sqlfile(file_path)
                        self._query.append(sql)
                except Exception as ex:
                    raise FileError(
                        f"File SQL doesn't exists: {query!s}: {ex}"
                    ) from ex
            elif isinstance(query, list):  # list of queries
                self._query = []
                for file_sql in query:
                    file_path = directory.joinpath(file_sql)
                    if file_path.exists() and file_path.is_file():
                        sql = await self.open_sqlfile(file_path)
                        self._query.append(sql)
            elif isinstance(query, dict):  # named queries
                self._query = {}
                for key, file_sql in query.items():
                    file_path = directory.joinpath(file_sql)
                    if file_path.exists() and file_path.is_file():
                        sql = await self.open_sqlfile(file_path)
                        self._query[key] = sql
        elif hasattr(self, "query_slug"):
            if isinstance(self.query_slug, str):  # pylint: disable=E0203
                if "{" in self.query_slug:  # pylint: disable=E0203 # noqa
                    self.query_slug = self.mask_replacement(self.query_slug)
                self._query[self.query_slug] = self.query_slug
            elif isinstance(self.query_slug, list):
                for slug in self.query_slug:
                    self._query[slug] = slug
            elif isinstance(self.query_slug, dict):
                # iterate over all conditions and search in masks:
                for key, data in self.query_slug.items():
                    slug = data["slug"]
                    for mask, replace in self._mask.items():
                        if mask in data["conditions"]:
                            self.query_slug[key]["conditions"][mask] = replace
                    self._query[key] = slug
        elif hasattr(self, "query"):
            if isinstance(self.query, str):  # pylint: disable=E0203
                self._query = []
                if hasattr(self, "masks"):
                    self.query = self.mask_replacement(self.query)
                elif "{" in self.query and hasattr(self, "conditions"):
                    try:
                        self.query = self.query.format(**self.conditions)
                    except Exception as err:
                        self._logger.warning(f"Error replacing Vars in Query: {err}")
                try:
                    self.query = self.query.format(**self._variables)
                except Exception as err:
                    self._logger.warning(f"Error replacing Vars in Query: {err}")
                self._query.append(self.query)
            elif isinstance(self.query, dict):  # named queries
                self._query = {}
                for key, query in self.query.items():
                    query = self.mask_replacement(query)
                    try:
                        query = query.format(**self._variables)
                    except Exception:
                        pass
                    self._query[key] = query
            elif isinstance(self.query, list):  # need to be concatenated
                self._query = []
                for query in self.query:
                    query = self.mask_replacement(query)
                    try:
                        for val in self._variables:
                            if isinstance(self._variables[val], list):
                                result = ", ".join(self._variables[val])
                            else:
                                result = ", ".join(
                                    "'{}'".format(v) for v in self._variables[val]
                                )
                        query = query.format(**self._variables)
                    except Exception:
                        pass
                    self._query.append(query)
        if hasattr(self, "conditions"):
            self.set_conditions("conditions")
            cPrint("NEW CONDITIONS ARE> ", level="WARN")
            pprint(self.conditions)

        # Replace variables
        if isinstance(self._query, list):
            queries = []
            for query in self._query:
                values = {}
                for key, val in self._variables.items():
                    if isinstance(val, list):
                        value = ", ".join(
                            "'{}'".format(Entity.quoteString(v)) for v in val
                        )
                    else:
                        value = val
                    query = query.replace("{{{}}}".format(str(key)), str(value))
                    values[key] = value
                # using safeDict
                query.format_map(SafeDict(**values))
                queries.append(query)
            self._query = queries
        return True

    async def close(self):
        """Method."""

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
        res, error = await conn.query(query)
        if error:
            raise DataNotFound(error)
        return self._normalize_rows(res)

    async def _query_with_qs(self, query: str):
        """Query path through QuerySource parser/provider pipeline."""
        from querysource.queries.qs import QS as QuerySourceQS

        conditions = {}
        if hasattr(self, "conditions") and isinstance(self.conditions, dict):
            conditions = {**self.conditions}

        qry = QuerySourceQS(
            query=query,
            driver=self._driver,
            conditions=conditions,
            loop=self._loop,
            lazy=True,
        )
        try:
            res, error = await qry.query()
            if error:
                raise DataNotFound(error)
            return self._normalize_rows(res)
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
                    "QueryToPandas: QS parser path failed, using legacy fallback: %s",
                    err,
                )
        return await self._query_with_connection(conn, query)

    async def run(self):
        # TODO: support for datasources
        # TODO: using maps to transform data types
        if not self._query:
            raise ComponentError(
                "QueryToPandas: Empty Query/Slug or File"
            )
        if hasattr(self, "query") or hasattr(self, "file_sql"):
            try:
                connection = await self.create_connection()
            except Exception as err:
                self._logger.exception(err, stack_info=True)
                raise
            if isinstance(self._query, list):  # list of queries
                results = []
                async with await connection.connection() as conn:
                    for query in self._query:
                        self._logger.debug(
                            f"Query: {query}"
                        )
                        try:
                            result = await self._query_with_fallback(conn, query)
                        except NoDataFound:
                            result = []
                        except Exception as err:
                            self._logger.error(err)
                            raise
                        ln = len(result)
                        st = {
                            "result": ln
                        }
                        self.add_metric("Query", st)
                        if ln == 1 and self.as_dict is True:
                            # saving only one row
                            result = dict(result[0])
                            results.append(result)
                        else:
                            results.extend(result)
                if hasattr(self, "raw_result"):
                    self._result = results
                    self._variables[f"{self.StepName}_NUMROWS"] = len(results)
                else:
                    self._result = await self.get_dataframe(
                        results, infer_types=self.infer_types
                    )
                    numrows = len(self._result.index)
                    self._variables[f"{self.StepName}_NUMROWS"] = numrows
            elif isinstance(self._query, dict):  # Named queries
                self._result = {}
                results = []
                async with await connection.connection() as conn:
                    for key, query in self._query.items():
                        try:
                            result = await self._query_with_fallback(conn, query)
                        except NoDataFound:
                            result = []
                        except Exception as err:
                            self._logger.error(err)
                            raise
                        ln = len(result)
                        st = {"query": key, "result": ln}
                        self.add_metric("Query", st)
                        if ln == 1:
                            # saving only one row
                            result = dict(result[0])
                        if hasattr(self, "raw_result"):
                            self._result[key] = result
                            self._variables[f"{self.StepName}_{key}_NUMROWS"] = len(
                                result
                            )
                        else:
                            df = await self.get_dataframe(
                                result, infer_types=self.infer_types
                            )
                            self._result[key] = df
                            self._variables[f"{self.StepName}_{key}_NUMROWS"] = len(
                                df.index
                            )
            else:
                raise NotSupported(f"{self.__name__}: Incompatible Query Method.")
        elif hasattr(self, "query_slug"):
            # TODO: assign the datasource to QuerySource connection
            self.add_metric("SLUG", self.query_slug)
            if isinstance(self.query_slug, dict):
                # return a list of queries
                self._result = {}
                for key, data in self.query_slug.items():
                    slug = data["slug"]
                    conditions = data["conditions"]
                    try:
                        result = await self.get_qs(slug, conditions)
                        ln = len(result)
                        st = {"query": key, "result": ln}
                        if ln == 1 and self.as_dict is True:
                            # saving only one row
                            result = dict(result[0])
                    except (DataNotFound, NoDataFound) as ex:
                        raise DataNotFound(str(ex)) from ex
                    if hasattr(self, "raw_result"):
                        self._result[key] = result
                        self._variables[f"{self.StepName}_{key}_NUMROWS"] = len(result)
                        self.add_metric("NUMROWS", len(result))
                    else:
                        df = await self.get_dataframe(
                            result, infer_types=self.infer_types
                        )
                        self._result[key] = df
                        self._variables[f"{self.StepName}_{key}_NUMROWS"] = len(
                            df.index
                        )
                        self.add_metric("NUMROWS", len(df.index))
            else:
                results = []
                for key, slug in self._query.items():
                    conditions = {}
                    if hasattr(self, "conditions"):
                        conditions = self.conditions
                    try:
                        result = await self.get_qs(slug, conditions)
                        ln = len(result)
                        self._logger.debug(f"QS {key}: length: {ln}")
                        st = {"query": key, "result": ln}
                        if ln == 1 and self.as_dict is True:
                            # saving only one row
                            result = dict(result[0])
                    except (DataNotFound, NoDataFound):
                        result = {}
                    except Exception as err:
                        self._logger.exception(err, stack_info=False)
                        raise
                    results.extend(result)
                if hasattr(self, "raw_result"):
                    self._result = results
                    self._variables[f"{self.StepName}_NUMROWS"] = len(results)
                    self.add_metric("NUMROWS", len(result))
                else:
                    self._result = await self.get_dataframe(
                        results, infer_types=self.infer_types
                    )
                    numrows = len(self._result.index)
                    self._variables[f"{self.StepName}_NUMROWS"] = numrows
                    self.add_metric("NUMROWS", numrows)
        else:
            raise NotSupported(f"{self.__name__}: Method not allowed")
        if is_empty(self._result):
            raise DataNotFound(f"{self.__name__}: Data Not Found")
        else:
            ### making traspose of data:
            if hasattr(self, "transpose"):
                # transpose rows to columns:
                # self._result = self._result.transpose()
                self._result = pd.melt(self._result, id_vars=self.transpose["columns"])
                if "variable" in self.transpose:
                    # rename variable to a new name:
                    self._result.rename(
                        columns={"variable": self.transpose["variable"]}, inplace=True
                    )
                if "value" in self.transpose:
                    self._result.rename(
                        columns={"value": self.transpose["value"]}, inplace=True
                    )
            if hasattr(self, 'limit'):
                # limit the number of rows:
                if isinstance(self._result, pd.DataFrame):
                    self._result = self._result.head(self.limit)
                elif isinstance(self._result, dict):
                    for key, df in self._result.items():
                        if isinstance(df, pd.DataFrame):
                            self._result[key] = df.head(self.limit)
                elif isinstance(self._result, list):
                    new_results = []
                    for df in self._result:
                        if isinstance(df, pd.DataFrame):
                            df = df.head(self.limit)
                        new_results.append(df)
                    self._result = new_results
            if self._debug is True:
                print("== DATA PREVIEW ==")
                print(self._result)
                print()
            return self._result
