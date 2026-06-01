from uuid import UUID

from orjson import orjson

from picsellia import exceptions
from picsellia.sdk.connection import Connection
from picsellia.sdk.datasource import DataSource
from picsellia.utils import filter_payload


class DataSourceService:
    @classmethod
    def create_datasource(
        cls, connection: Connection, organization_id: UUID, name: str
    ) -> DataSource:
        params = {"name": name}
        r = connection.post(
            f"/api/organization/{organization_id}/datasources",
            data=orjson.dumps(params),
        ).json()
        return DataSource(connection, r)

    @classmethod
    def get_datasource(
        cls, connection: Connection, organization_id: UUID, name: str
    ) -> DataSource:
        params = {"name": name}
        r = connection.get(
            f"/api/organization/{organization_id}/datasources/find",
            params=params,
        ).json()
        return DataSource(connection, r)

    @classmethod
    def get_or_create_datasource(
        cls, connection: Connection, organization_id: UUID, name: str
    ) -> DataSource:
        try:
            return cls.get_datasource(connection, organization_id, name)
        except exceptions.ResourceNotFoundError:
            return cls.create_datasource(connection, organization_id, name)

    @classmethod
    def list_datasources(
        cls,
        connection: Connection,
        organization_id: UUID,
        limit: int | None = None,
        offset: int | None = None,
        order_by: list[str] | None = None,
    ) -> list[DataSource]:
        params = {"limit": limit, "offset": offset, "order_by": order_by}
        params = filter_payload(params)
        r = connection.get(
            f"/api/organization/{organization_id}/datasources",
            params=params,
        ).json()
        return [DataSource(connection, item) for item in r["items"]]
