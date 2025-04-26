from os import PathLike
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterable,
    Callable,
    ClassVar,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)

import pyarrow as pa

if TYPE_CHECKING:
    import sqlalchemy.ext.asyncio
    from sqlalchemy.engine import Connection

from chalk.features import Feature
from chalk.sql._internal.chalk_query import ChalkQuery
from chalk.sql._internal.query_execution_parameters import QueryExecutionParameters
from chalk.sql._internal.sql_source import BaseSQLSource
from chalk.sql._internal.string_chalk_query import StringChalkQuery
from chalk.sql.finalized_query import FinalizedChalkQuery
from chalk.sql.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, StringChalkQueryProtocol
from chalk.utils.datasource_tags import tag_matches
from chalk.utils.missing_dependency import missing_dependency_exception


class SQLSourceGroup(BaseSQLSourceProtocol):
    registry: ClassVar[List["SQLSourceGroup"]] = []

    def __init__(self, name: str, default: BaseSQLSource, tagged_sources: Mapping[str, BaseSQLSource]):
        super().__init__()

        if hasattr(default, "kind"):
            self.kind = default.kind

        self.name = name
        self._default = default
        self._tagged_sources = tagged_sources
        self.registry.append(self)

        try:
            import sqlalchemy
        except ImportError:
            raise missing_dependency_exception("chalkpy[sql]")
        del sqlalchemy  # unused

    def to_json(self) -> Dict[str, str]:
        return self._default.to_json()

    def get_sqlglot_dialect(self) -> Optional[str]:
        return self._default.get_sqlglot_dialect()

    def query_string(
        self,
        query: str,
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:

        default_response = self._default.query_string(query, fields, args)

        if isinstance(default_response, StringChalkQuery):
            default_response._source = self  # pyright: ignore[reportPrivateUsage]

        return default_response

    def query_sql_file(
        self,
        path: Union[str, bytes, PathLike],
        fields: Optional[Mapping[str, Union[Feature, str, Any]]] = None,
        args: Optional[Mapping[str, object]] = None,
    ) -> StringChalkQueryProtocol:
        default_response = self._default.query_sql_file(path, fields, args)

        if isinstance(default_response, StringChalkQuery):
            default_response._source = self  # pyright: ignore[reportPrivateUsage]

        return default_response

    def query(self, *entities: Any) -> ChalkQueryProtocol:
        default_response = self._default.query(*entities)

        if isinstance(default_response, ChalkQuery):
            default_response._source = self  # pyright: ignore[reportPrivateUsage]

        return default_response

    def execute_query(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: "Optional[Connection]" = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> Iterable[pa.RecordBatch]:
        source = self.select_matching_source(query_execution_parameters=query_execution_parameters)
        return source.execute_query(
            finalized_query=finalized_query,
            columns_to_features=columns_to_features,
            connection=connection,
            query_execution_parameters=query_execution_parameters,
        )

    async def async_execute_query(
        self,
        finalized_query: FinalizedChalkQuery,
        columns_to_features: Callable[[Sequence[str]], Mapping[str, Feature]],
        connection: "Optional[sqlalchemy.ext.asyncio.AsyncConnection]" = None,
        query_execution_parameters: Optional[QueryExecutionParameters] = None,
    ) -> AsyncIterable[pa.RecordBatch]:
        source = self.select_matching_source(query_execution_parameters=query_execution_parameters)
        return source.async_execute_query(
            finalized_query=finalized_query,
            columns_to_features=columns_to_features,
            connection=connection,
            query_execution_parameters=query_execution_parameters,
        )

    def get_engine(self) -> "sqlalchemy.engine.Engine":
        raise NotImplementedError("SQLSourceGroup does not support get_engine")

    def select_matching_source(self, query_execution_parameters: Optional[QueryExecutionParameters]) -> BaseSQLSource:
        if query_execution_parameters is None:
            return self._default

        candidate = None

        for tag, source in self._tagged_sources.items():
            if tag_matches(datasource_tag=tag, context_tags=query_execution_parameters.tags):
                if candidate is not None:
                    raise ValueError(
                        f"Ambiguous tags in datasource selection; multiple sources match: {source} and {candidate}. Provided tags were: {query_execution_parameters.tags}."
                    )
                candidate = source

        return candidate or self._default
