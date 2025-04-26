import typing as t
from abc import abstractmethod
from pathlib import Path

from gql import Client
from gql.client import AsyncClientSession
from gql.dsl import DSLSchema
from graphql import GraphQLSchema, build_schema
from typing_extensions import Self

from connector.generated import ErrorCode
from connector.httpx_rewrite import AsyncClient
from connector.oai.capability import Request
from connector.oai.errors import ConnectorError


class BaseIntegrationClient:
    @classmethod
    @abstractmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        pass

    @classmethod
    def build_client(cls, args: Request) -> AsyncClient:
        return AsyncClient(**cls.prepare_client_args(args))

    def __init__(self, args: Request) -> None:
        self._http_client = self.build_client(args)

    async def __aenter__(self):
        await self._http_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._http_client.__aexit__()
        if exc_type is not None:
            raise exc_val


class BaseGraphQLSession(AsyncClientSession):
    def __init__(self, args: Request):
        super().__init__(client=self.build_client(args))

    async def __aenter__(self) -> Self:
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type=exc_type, exc=exc, tb=tb)

        if exc_type is not None:
            raise exc

    @classmethod
    @abstractmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        pass

    @classmethod
    def build_client(cls, args: Request) -> Client:
        return Client(**cls.prepare_client_args(args))

    @classmethod
    def load_schema(cls, schema_file_path: str | Path) -> GraphQLSchema:
        """Load the GraphQL schema from a file."""
        with open(schema_file_path) as f:
            return build_schema(f.read())

    @property
    def schema(self) -> DSLSchema:
        if self.client.schema is None:
            raise ConnectorError(
                message="Failed to fetch schema",
                error_code=ErrorCode.API_ERROR,
            )

        return DSLSchema(self.client.schema)
