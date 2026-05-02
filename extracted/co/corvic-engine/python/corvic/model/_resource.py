"""Resources."""

from __future__ import annotations

import dataclasses
import uuid
from collections.abc import Iterable
from typing import TypeAlias

import polars as pl
import sqlalchemy as sa
from typing_extensions import Self

from corvic import orm, result, system
from corvic.model._defaults import get_default_client, get_default_room_id
from corvic.model._proto_orm_convert import orm_to_proto
from corvic.model._wrapped_proto import WrappedProto
from corvic_generated.model.v1alpha import models_pb2

SourceID: TypeAlias = orm.SourceID
ResourceID: TypeAlias = orm.ResourceID
RoomID: TypeAlias = orm.RoomID


@dataclasses.dataclass(frozen=True)
class Resource(WrappedProto[ResourceID, models_pb2.Resource]):
    """Resources represent import data."""

    @property
    def url(self) -> str:
        return self.proto_self.url

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def room_id(self) -> RoomID:
        return RoomID(self.proto_self.room_id)

    @property
    def mime_type(self) -> str:
        return self.proto_self.mime_type

    @property
    def md5(self) -> str:
        return self.proto_self.md5

    @property
    def size(self) -> int:
        return self.proto_self.size

    @property
    def original_path(self) -> str:
        return self.proto_self.original_path

    @property
    def description(self) -> str:
        return self.proto_self.description

    @property
    def source_ids(self) -> list[SourceID]:
        return [SourceID(val) for val in self.proto_self.source_ids]

    @classmethod
    def list(
        cls, room_id: RoomID | None, client: system.Client | None = None
    ) -> result.Ok[Iterable[Resource]] | result.NotFoundError:
        """List resources."""
        client = client or get_default_client()
        query = sa.select(orm.Resource)

        if room_id:
            with orm.Session(client.sa_engine) as session:
                orm_room = session.get(orm.Room, room_id)
                if not orm_room:
                    return result.NotFoundError("room not found", id=room_id)
                query = query.filter_by(room_id=room_id)
        query = query.order_by(sa.desc("created_at"))

        def generate_resources():
            with orm.Session(client.sa_engine) as session:
                for entry in session.scalars(query):
                    yield Resource(client, orm_to_proto(entry), ResourceID())

        return result.Ok(list(generate_resources()))

    @classmethod
    def from_id(
        cls, id: ResourceID, client: system.Client | None = None
    ) -> result.Ok[Resource] | result.NotFoundError:
        client = client or get_default_client()
        with orm.Session(client.sa_engine) as session:
            resource = session.get(orm.Resource, id)
            if not resource:
                return result.NotFoundError("resource not found", id=id)
            return result.Ok(cls(client, orm_to_proto(resource), id))

    @classmethod
    def from_blob(
        cls,
        name: str,
        blob: system.Blob,
        client: system.Client | None,
        original_path: str = "",
        description: str = "",
        room_id: orm.RoomID | None = None,
    ) -> Self:
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        blob.reload()
        md5 = blob.md5_hash
        size = blob.size

        if not md5 or not size:
            raise result.Error("failed to get metadata from blob store")

        proto_resource = models_pb2.Resource(
            name=name,
            mime_type=blob.content_type,
            url=blob.url,
            md5=md5,
            size=size,
            original_path=original_path,
            description=description,
            room_id=str(room_id),
        )
        return cls(client, proto_resource, ResourceID())

    @classmethod
    def from_polars(
        cls,
        data_frame: pl.DataFrame,
        client: system.Client | None = None,
        room_id: orm.RoomID | None = None,
    ) -> Self:
        client = client or get_default_client()
        room_id = room_id or get_default_room_id(client)
        blob = client.storage_manager.tabular.blob(f"polars_dataframe/{uuid.uuid4()}")

        with blob.open(mode="wb") as stream:
            data_frame.write_parquet(stream)

        blob.content_type = "application/octet-stream"
        blob.patch()
        return cls.from_blob(blob.url, blob, client, room_id=room_id)
