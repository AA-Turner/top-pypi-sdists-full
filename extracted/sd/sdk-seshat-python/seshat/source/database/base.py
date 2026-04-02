from typing import Optional, List

from sqlalchemy import Engine, text

from seshat.data_class import SFrame, DFrame
from seshat.general.exceptions import InvalidArgumentsError
from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.source import Source
from seshat.source.mixins import SQLMixin
from seshat.transformer.schema import Schema


class SQLDBSource(SQLMixin, Source):
    """
    This class is responsible for fetching data from SQL databases using filters and queries.
    Supports querying by table name with filters, raw SQL queries, or dynamic query generation functions.

    Parameters
    ----------
    url : str
        Database connection URL (SQLAlchemy format).
    filters : dict, optional
        Key-value pairs for filtering table data (only used with table_name).
    table_name : str, optional
        Name of the database table to query.
    limit : int, optional
        Maximum number of rows to fetch.
    query : str, optional
        Raw SQL query string to execute.
    query_fn : callable, optional
        Function that generates SQL query dynamically. Receives filters and other kwargs.
    schema : Schema, optional
        Schema for data transformation after fetching.
    mode : str, optional
        SFrame mode for data conversion.
    group_keys : dict, optional
        Group keys for SFrame grouping.
    """

    _engine: Engine = None
    filters: Optional[dict]
    table_name: str
    schema: Optional[Schema]
    limit: int
    query: str

    def __init__(
        self,
        url,
        filters=None,
        table_name=None,
        limit=None,
        query=None,
        query_fn=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not any([table_name, query, query_fn]):
            raise InvalidArgumentsError(
                "At least one of the query, table_name and query_fn must be specified"
            )

        self.url = url
        self.table_name = table_name
        self.filters = filters or {}
        self.limit = limit
        self.query = query
        self.query_fn = query_fn

    def fetch(self, *args, **kwargs) -> SFrame:
        query_result = self.get_from_db(
            text(self.get_query(self.filters, *args, **kwargs))
        )
        return self.convert_data_type(query_result)

    def convert_data_type(self, data) -> SFrame:
        return super().convert_data_type(DFrame.from_raw(data).to_raw())

    def calculate_complexity(self):
        return 30


class SQLDBSourceStory(BaseTransformerStory):
    transformer = SQLDBSource

    use_cases = [
        "Fetch data from SQL databases (currently only postgresql) using SQL queries",
        "Query tables with dynamic filters and limits",
        "Integrate database data into SFrame pipelines with optional schema transformation",
    ]

    logic_overview = (
        "SQLDBSource fetches data from SQL databases by executing queries (either from table_name with filters, "
        "raw SQL query strings, or dynamically generated via query_fn). It inherits from Source, "
        "using the standard Source.__call__() method for integration with SFrame pipelines."
    )

    steps = [
        "Build SQL query using get_query() with filters or use provided query/query_fn",
        "Execute query against database using get_from_db() with SQLAlchemy",
        "Convert query results to DFrame then to the appropriate SFrame format",
        "Follow standard Source logic: apply schema if provided, merge or add to GroupSFrame as needed",
    ]

    tags = ["source", "database", "sql", "data-fetching"]

    def get_scenarios(self) -> List[TransformerScenario]:
        from test.transformer.source.test_sqldb_source import SQLDBSourceTestCase

        return TransformerScenario.from_testcase(
            SQLDBSourceTestCase, transformer=self.transformer
        )
