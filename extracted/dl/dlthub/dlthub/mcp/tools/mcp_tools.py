import re
from typing import Any, Callable, List, Dict, NamedTuple, Optional, cast

import sqlglot
import pyarrow as pa
from pydantic.networks import AnyUrl

from fastmcp import FastMCP
from fastmcp.resources import FunctionResource
from fastmcp.resources.template import ResourceTemplate
from fastmcp.tools import Tool

from dlt import Dataset
from dlt.common.libs.pandas import pandas_to_arrow
from dlt.common.schema.utils import is_valid_schema_name

from dlthub.mcp.tools.helpers import format_csv
from dlthub.project import Catalog, ProjectRunContext

# NOTE: those imports are needed only for Python scripting feature in mcp server
import unicodedata

import pandas as pd  # type: ignore[import-untyped]
import numpy as np


class CacheEntry(NamedTuple):
    result: pa.Table
    query: str
    input_cache_entry: Optional[str]


class ProjectMCPTools:
    RECENT_CACHE_KEY = "_recent"

    def __init__(self, run_context: ProjectRunContext):
        self.result_cache: Dict[str, CacheEntry] = {}
        self._recent_count = 0
        self.run_context = run_context
        self.catalog = Catalog(run_context)

    def register_resource(
        self,
        mcp_server: FastMCP,
        fn: Callable[[], Any],
        uri: str,
        name: str,
        description: str,
        mime_type: str,
    ) -> None:
        resource = FunctionResource(
            uri=AnyUrl(uri),
            name=name,
            description=description,
            mime_type=mime_type,
            fn=fn,
        )
        mcp_server.add_resource(resource)

    def register_resource_template(
        self,
        mcp_server: FastMCP,
        fn: Callable[..., Any],
        uri_template: str,
        name: str,
        description: str,
        mime_type: str,
    ) -> None:
        template = ResourceTemplate.from_function(
            fn,
            uri_template=uri_template,
            name=name,
            description=description,
            mime_type=mime_type,
        )
        mcp_server.add_template(template)

    def recent_result_resource(self) -> str:
        return self._return_from_cache(self.RECENT_CACHE_KEY)

    def bookmark_resource(self, bookmark: str) -> str:
        return self._return_from_cache(bookmark)

    def register_with(self, mcp_server: FastMCP) -> None:
        mcp_server.add_tool(
            Tool.from_function(
                self.get_profile,
                name="get_profile",
                description="Get the current profile",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.available_datasets,
                name="available_datasets",
                description="List all available datasets in the project",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.available_tables,
                name="available_tables",
                description="List all available tables in the dataset",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.table_head,
                name="table_head",
                description="Print first 10 rows in the table",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.table_schema,
                name="table_schema",
                description="Get the schema of the table",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.query_sql,
                name="query_sql",
                description=(
                    "Executes sql statement on a given dataset as returns the result as | "
                    "delimited csv. Use this tool for simple analysis where the number of rows is "
                    "small i.e. below 100. SQL dialect: Use table and column names discovered in "
                    "`available_tables` and `table_schema` tools. Use SQL dialect as indicated in "
                    "`table_schema`. Do not qualify table names with schema names. "
                ),
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.bookmark_sql,
                name="bookmark_sql",
                description=(
                    "Executes sql statement on a given dataset and bookmarks it under given "
                    "bookmark for further processing. Use this tool when you need to select and "
                    "transform a large result or when you want to reuse results of the query. "
                    "To obtain full result use `read_result_from_bookmark` or `recent_result` "
                    "tools. You transform the result using `transform_bookmark_and_return` tool. "
                    "SQL dialect: Use table and column names discovered in `available_tables` and "
                    "`table_schema` tools. Use SQL dialect as indicated in `table_schema`. Do not "
                    "qualify table names with schema names. "
                ),
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.read_result_from_bookmark,
                name="read_result_from_bookmark",
                description="Read the result of the bookmark and return it as '|' delimited CSV",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.recent_result,
                name="recent_result",
                description="Read the most recent result and return it as '|' delimited CSV",
            )
        )
        mcp_server.add_tool(
            Tool.from_function(
                self.transform_bookmark_and_return,
                name="transform_bookmark_and_return",
                description=(
                    "READ THIS VERY CAREFULLY OTHERWISE YOU WILL NOT BE ABLE TO USE THIS TOOL.\n\n"
                    "Transforms result under bookmark `bookmark` with Python script "
                    "`python_script` which is compiled and evaluated. If bookmark is not "
                    "specified, the most recent result is used. This script receives bookmark as "
                    "DataFrame, transforms it and returns modified DataFrame which we return "
                    "from the functions as CSV.\n\n"
                    "In script in `python_script`, `df` is a Pandas DataFrame created from "
                    "bookmark. You can directly manipulate `df` using Pandas operations. "
                    "Examples:\n\n"
                    "Filter rows where 'age' is greater than 30:\n"
                    "```\n"
                    "df = df[df['age'] > 30]\n"
                    "```\n\n"
                    "# Add a new column 'age_group' classifying rows based on the 'age':\n"
                    "```\n"
                    "df['age_group'] = df['age'].apply("
                    "lambda x: 'Senior' if x > 60 else 'Adult')\n"
                    "```\n\n"
                    "# Rename columns:\n"
                    "```\n"
                    "df = df.rename(columns={'first_name': 'fname', 'last_name': 'lname'})\n"
                    "```\n\n"
                    "After the script finishes, `df` will be returned with these transformations "
                    "applied as | delimited CSV. NEVER use return at the end of your script. "
                    "Assign results back to df! Do not use print statements. Avoid defining "
                    "functions. Do not save any files - they won't be visible."
                ),
            )
        )
        self.register_resource(
            mcp_server,
            fn=self.recent_result_resource,
            uri="bookmark://" + self.RECENT_CACHE_KEY,
            name="recent_result",
            description="Result returned by most recently used tool",
            mime_type="text/csv",
        )

        self.register_resource_template(
            mcp_server,
            fn=self.bookmark_resource,
            uri_template="bookmark://{bookmark}",
            name="bookmark",
            description="Result stored under bookmark as | delimited csv",
            mime_type="text/csv",
        )

    def get_profile(self) -> str:
        return "Current profile is: " + self.run_context.profile

    def available_datasets(self) -> List[str]:
        return list(self.catalog.datasets)

    def available_tables(self, dataset: str) -> List[str]:
        return self.catalog[dataset].schema.data_table_names()

    def table_head(self, dataset: str, table: str) -> Any:
        return self.catalog[dataset][table].head(10).df()

    def table_schema(self, dataset_name: str, table_name: str) -> Dict[str, Any]:
        dataset = self.catalog[dataset_name]
        return self._make_table_schema(dataset, table_name)

    def query_sql(self, dataset_name: str, sql: str) -> str:
        dataset = self.catalog[dataset_name]
        return self._execute_sql(dataset, sql)

    def bookmark_sql(self, dataset_name: str, sql: str, bookmark: str) -> str:
        dataset = self.catalog[dataset_name]
        return self._execute_sql(dataset, sql, bookmark)

    def transform_bookmark_and_return(
        self, python_script: str, bookmark: Optional[str] = None
    ) -> str:
        if not (cache_entry := self.result_cache.get(bookmark or self.RECENT_CACHE_KEY)):
            raise ValueError(f"{bookmark} bookmark not found")
        df = cache_entry.result.to_pandas()

        # TODO: parse AST and use visitor
        if "return df" in python_script:
            raise ValueError(
                "Do not return anything from the script. Read the tool description again."
            )
        if "print(" in python_script:
            raise ValueError("Do not print in the script. It is executed remotely.")

        # Create isolated namespaces for execution
        # NOTE: if script contains import that import a module that is not yet imported
        #    server unfortunately disconnects
        local_dict = {"df": df}
        global_dict = {
            "__builtins__": __builtins__,  # consider restricting builtins if necessary
            "pd": pd,
            "np": np,
            "re": re,
            "unicodedata": unicodedata,
            "result_cache": self.result_cache,
            "pa": pa,
        }

        # Compile and execute the script
        code = compile(python_script, "<string>", "exec")
        exec(code, global_dict, local_dict)

        # After execution, `df` should now be transformed
        if "df" not in local_dict:
            raise ValueError("The script did not produce a transformed DataFrame named df.")

        df = local_dict["df"]
        # NOTE: removed from function arguments, was too complicated for LLMs
        save_bookmark: Optional[str] = None
        return self._return_or_cache(
            pandas_to_arrow(df, preserve_index=True), python_script, save_bookmark, bookmark
        )

    def read_result_from_bookmark(self, bookmark: str) -> str:
        return self._return_from_cache(bookmark)

    def recent_result(self) -> str:
        return self._return_from_cache(self.RECENT_CACHE_KEY)

    def _make_table_schema(self, dataset: Dataset, table_name: str) -> Dict[str, Any]:
        """Construct a normalized table schema dictionary for the specified table."""
        from dlt.common.libs.pyarrow import get_py_arrow_datatype
        from dlt.destinations.impl.duckdb.sql_client import DuckDbSqlClient

        schema = dataset.schema
        table_schema = cast(Dict[str, Any], schema.get_table(table_name))
        if isinstance(dataset.sql_client, DuckDbSqlClient):
            dialect = "duckdb"
        else:
            assert dataset._destination is not None
            dialect = dataset._destination.destination_type
        table_schema["sql_dialect"] = dialect
        table_schema["normalized_name"] = dataset.sql_client.escape_column_name(
            schema.naming.normalize_tables_path(table_schema["name"])
        )
        for col_schema in table_schema["columns"].values():
            col_schema["normalized_name"] = dataset.sql_client.escape_column_name(
                schema.naming.normalize_tables_path(col_schema["name"])
            )
            if "data_type" in col_schema:
                col_schema["arrow_data_type"] = str(
                    get_py_arrow_datatype(col_schema, dataset.sql_client.capabilities, "UTC")
                )
        stored_schema = schema.to_dict(remove_defaults=True, bump_version=False)
        return cast(Dict[str, Any], stored_schema["tables"][table_name])

    def _execute_sql(
        self,
        dataset: Dataset,
        sql: str,
        bookmark: Optional[str] = None,
    ) -> str:
        parsed = sqlglot.parse(sql)
        if any(
            isinstance(expr, (sqlglot.exp.Insert, sqlglot.exp.Update, sqlglot.exp.Delete))
            for expr in parsed
        ):
            raise ValueError("Data modification statements are not allowed")

        table = dataset(sql).arrow()
        return self._return_or_cache(table, sql, bookmark)

    def _return_or_cache(
        self,
        table: pa.Table,
        query: Optional[str] = None,
        save_bookmark: Optional[str] = None,
        input_bookmark: Optional[str] = None,
    ) -> str:
        info = self._cache_arrow(table, query, self.RECENT_CACHE_KEY, input_bookmark)
        if save_bookmark:
            return self._cache_arrow(table, query, save_bookmark, input_bookmark)
        else:
            return format_csv(table, info)

    def _cache_arrow(
        self,
        table: pa.Table,
        query: Optional[str] = None,
        save_bookmark: Optional[str] = None,
        input_bookmark: Optional[str] = None,
    ) -> str:
        if not is_valid_schema_name(save_bookmark):
            raise ValueError(
                f"Invalid bookmark name: {save_bookmark}. Only strings that are valid Python "
                "identifiers are accepted."
            )
        info = f"Result with {len(table)} row(s) bookmarked under {save_bookmark}\n"
        self.result_cache[save_bookmark] = CacheEntry(table, query, input_bookmark)
        if save_bookmark == self.RECENT_CACHE_KEY:
            self._recent_count += 1
            save_bookmark = save_bookmark + f".{self._recent_count}"

        return info

    def _return_from_cache(self, cache_url: str) -> str:
        if not (cache_entry := self.result_cache.get(cache_url)):
            raise ValueError(f"{cache_url} bookmark not found")
        return format_csv(cache_entry.result)
