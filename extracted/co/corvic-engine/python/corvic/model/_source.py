"""Sources."""

from __future__ import annotations

import copy
import dataclasses
import enum
import functools
from collections.abc import Iterable, Mapping, Sequence
from typing import Final, TypeAlias

import polars as pl
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
import structlog
from typing_extensions import Self

from corvic import op_graph, orm, system
from corvic.model._defaults import get_default_client
from corvic.model._proto_orm_convert import orm_to_proto
from corvic.model._resource import Resource
from corvic.model._wrapped_proto import WrappedProto
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic.table import Table
from corvic_generated.model.v1alpha import models_pb2

_logger = structlog.get_logger()

ResourceID: TypeAlias = orm.ResourceID
SourceID: TypeAlias = orm.SourceID
RoomID: TypeAlias = orm.RoomID


@enum.unique
class SourceType(enum.Enum):
    """Hints about how a source should be treated."""

    UNKNOWN = 1
    DIMENSION_TABLE = 2
    FACT_TABLE = 3
    PDF_DOCUMENT = 4

    # Work-around missing StrEnum in python 3.10

    @classmethod
    def from_str(cls, value: str):
        match value:
            case "unknown":
                return cls.UNKNOWN
            case "dimension_table":
                return cls.DIMENSION_TABLE
            case "fact_table":
                return cls.FACT_TABLE
            case "pdf_document":
                return cls.PDF_DOCUMENT
            case _:
                raise InvalidArgumentError(
                    "could not parse value into SourceType", value=value
                )

    def __str__(self):
        """Convert SourceType to readable value."""
        match self:
            case SourceType.UNKNOWN:
                return "unknown"
            case SourceType.DIMENSION_TABLE:
                return "dimension_table"
            case SourceType.FACT_TABLE:
                return "fact_table"
            case SourceType.PDF_DOCUMENT:
                return "pdf_document"


def foreign_key(
    referenced_source: SourceID | Source, *, is_excluded: bool = False
) -> op_graph.feature_type.ForeignKey:
    match referenced_source:
        case SourceID():
            return op_graph.feature_type.foreign_key(
                referenced_source, is_excluded=is_excluded
            )
        case Source():
            return op_graph.feature_type.foreign_key(
                referenced_source.id, is_excluded=is_excluded
            )


@dataclasses.dataclass(frozen=True)
class Source(WrappedProto[SourceID, models_pb2.Source]):
    """Sources describe how resources should be treated.

    Example:
    >>> Source.from_polars(order_data)
    >>>    .as_dimension_table()
    >>> )
    """

    _SOURCE_TYPE_METADATA_KEY: Final = "source_type"

    @classmethod
    def from_id(
        cls, source_id: SourceID, client: system.Client | None = None
    ) -> Ok[Self] | NotFoundError | InvalidArgumentError:
        client = client or get_default_client()
        with sa_orm.Session(client.sa_engine, expire_on_commit=False) as session:
            orm_self = session.get(orm.Source, source_id)

            if orm_self is None:
                return NotFoundError(
                    "source with given id does not exists", id=source_id
                )
            proto_self = orm_to_proto(orm_self)
        return Ok(
            cls(
                client,
                proto_self,
                SourceID(),
            )
        )

    @classmethod
    def from_resource(
        cls,
        resource: Resource,
        name: str | None = None,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | system.DataMisplacedError | InvalidArgumentError:
        return cls.from_non_tabular_resource(resource, name, client, room_id).and_then(
            lambda new_source: Table.from_parquet_file(
                new_source.client, resource.url
            ).map(lambda table: new_source.with_table(table))
        )

    @classmethod
    def from_non_tabular_resource(
        cls,
        resource: Resource,
        name: str | None = None,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Ok[Self] | InvalidArgumentError:
        """Construct a source for a resource that requires some preprocessing.

        This flavor populates all of the metadata that comes from the resource
        but does not populate table. Callers are expected to populate table later.
        """
        client = client or resource.client
        room_id = room_id or resource.room_id

        proto_source = models_pb2.Source(
            name=name or resource.name,
            resource_id=str(resource.id),
            room_id=str(room_id),
        )

        return Ok(
            cls(
                client,
                proto_source,
                SourceID(),
            )
        )

    @classmethod
    def from_polars(
        cls,
        name: str,
        data_frame: pl.DataFrame,
        client: system.Client | None = None,
        room_id: RoomID | None = None,
    ) -> Self:
        """Create a source from a pl.DataFrame.

        Args:
            name: a unique name for this source
            data_frame: a polars DataFrame
            client: use a particular system.Client instead of the default
            room_id: room to associate this source with. Use the default room if None.
        """
        client = client or get_default_client()
        resource = Resource.from_polars(data_frame, client).commit().unwrap_or_raise()
        return cls.from_resource(
            resource, name=name, client=client, room_id=room_id
        ).unwrap_or_raise()

    def with_table(self, table: Table) -> Self:
        proto_self = copy.copy(self.proto_self)
        proto_self.table_op_graph.CopyFrom(table.op_graph.to_proto())
        return dataclasses.replace(
            self,
            proto_self=proto_self,
        )

    @staticmethod
    def _to_orm_if_exists(
        id_val: RoomID | ResourceID, client: system.Client
    ) -> Ok[RoomID | ResourceID] | NotFoundError:
        match id_val:
            case RoomID():
                orm_class = orm.Room
            case ResourceID():
                orm_class = orm.Resource

        with orm.Session(client.sa_engine) as session:
            if session.get(orm_class, id_val) is not None:
                return Ok(id_val)
        return NotFoundError("entity not found")

    @classmethod
    def _generate_sources(
        cls, query: sa.Select[tuple[orm.Source]], client: system.Client
    ):
        with orm.Session(client.sa_engine) as session:
            it = iter(session.scalars(query))
            while True:
                try:
                    for val in it:
                        yield cls(
                            client,
                            orm_to_proto(val),
                            val.id or SourceID(),
                        )
                except Exception:  # noqa: PERF203
                    _logger.exception(
                        "omitting source from list: "
                        + "failed to parse source from database entry",
                    )
                else:
                    break

    @classmethod
    def list(
        cls,
        room_id: RoomID | None = None,
        resource_id: ResourceID | None = None,
        client: system.Client | None = None,
    ) -> Ok[Iterable[Source]] | NotFoundError:
        """List sources that exist in storage."""
        client = client or get_default_client()
        query = sa.select(orm.Source)
        if room_id is not None:
            match cls._to_orm_if_exists(room_id, client):
                case NotFoundError():
                    return NotFoundError("room not found", room_id=room_id)
                case Ok(orm_id):
                    query = query.filter_by(room_id=orm_id)

        if resource_id is not None:
            match cls._to_orm_if_exists(resource_id, client):
                case NotFoundError():
                    return NotFoundError("resource not found", resource_id=resource_id)
                case Ok(orm_id):
                    query = query.filter(
                        orm.Source.resource_associations.any(resource_id=orm_id)
                    )
        query = query.order_by(sa.desc("created_at"))

        return Ok(list(cls._generate_sources(query, client)))

    def with_feature_types(
        self, feature_types: Mapping[str, op_graph.FeatureType]
    ) -> Self:
        """Assign a Feature Type to each column in source.

        Args:
            feature_types: Mapping between column name and feature type

        Example:
        >>> with_feature_types(
        >>>        {
        >>>            "id": corvic.model.feature_type.primary_key(),
        >>>            "customer_id": corvic.model.feature_type.foreign_key(
        >>>                customer_source.id
        >>>            ),
        >>>        },
        >>>    )
        """
        return self.with_table(self.table.update_feature_types(feature_types))

    @functools.cached_property
    def table(self):
        return Table.from_ops(
            self.client, op_graph.op.from_proto(self.proto_self.table_op_graph)
        )

    @property
    def source_type(self) -> SourceType:
        value: str = self.table.metadata.get(
            self._SOURCE_TYPE_METADATA_KEY, str(SourceType.UNKNOWN)
        )
        try:
            return SourceType.from_str(value)
        except (InvalidArgumentError, ValueError) as exc:
            _logger.exception(
                "returning default source type: failed to parse from table metadata",
                source_id=self.id,
                exc_info=exc,
            )

        return SourceType.UNKNOWN

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def room_id(self) -> RoomID:
        return RoomID(self.proto_self.room_id)

    @property
    def resource_ids(self) -> Sequence[ResourceID]:
        return [ResourceID(self.proto_self.resource_id)]

    def as_dimension_table(self) -> Self:
        """Return Source as a Dimension Table."""
        new_table = self.table.update_metadata(
            {self._SOURCE_TYPE_METADATA_KEY: str(SourceType.DIMENSION_TABLE)}
        )
        return self.with_table(new_table)

    def as_fact_table(self) -> Self:
        """Return Source as a Fact Table."""
        new_table = self.table.update_metadata(
            {self._SOURCE_TYPE_METADATA_KEY: str(SourceType.FACT_TABLE)}
        )
        return self.with_table(new_table)

    def as_pdf_document(self) -> Self:
        """Return Source as a PDF Document (unstructured)."""
        new_table = self.table.update_metadata(
            {self._SOURCE_TYPE_METADATA_KEY: str(SourceType.PDF_DOCUMENT)}
        )
        return self.with_table(new_table)
