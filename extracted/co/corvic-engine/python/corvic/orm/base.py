"""Base models for corvic RDBMS backed orm tables."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, ClassVar, Protocol, runtime_checkable

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from google.protobuf import timestamp_pb2
from sqlalchemy.ext import hybrid
from typing_extensions import Self

from corvic.orm._proto_columns import ProtoMessageDecorator
from corvic.orm.func import utc_now
from corvic.orm.ids import (
    AgentID,
    AgentMessageID,
    FeatureViewID,
    FeatureViewSourceID,
    IntIDDecorator,
    MessageEntryID,
    OrgID,
    ResourceID,
    RoomID,
    SourceID,
    SpaceID,
    SpaceParametersID,
    SpaceRunID,
    StrIDDecorator,
    UserMessageID,
)
from corvic.orm.keys import (
    INT_PK_TYPE,
    ForeignKey,
    primary_key_identity_column,
    primary_key_uuid_column,
)
from corvic_generated.orm.v1 import (
    agent_pb2,
    common_pb2,
    feature_view_pb2,
    space_pb2,
    table_pb2,
)
from corvic_generated.status.v1 import event_pb2

# A quick primer on SQLAlchemy (sa) hybrid methods:
#
# Hybrid just means functionality that is different at the class-level versus
# the instance-level, and in the sa documentation, the authors really
# want to stress that class-versus-instance (decorators) is orthgonal to an
# ORM.
#
# However, this distinction is not particularly helpful for users of sa.
# It is best to have a working model of instance-level means Python-world and
# class-level means SQL-world. So, a hybrid method is something that has
# a different Python representation from its SQL representation.
#
# Since sa already handles conversions like "Python str" to "SQL text",
# certain representation differences between Python and SQL are already handled
# (not considered differences at all).
#
# Hybrid methods are for cases where we want to do non-trivial transformations
# between SQL and Python representations.
#
# The recipe is:
#
# 1. Define a hybrid_method / hybrid_property (wlog property) that produces the Python
#    object you want.
# 2. If the property doesn't need to be used in any sa query again, you are done.
# 3. If the property is simple enough for sa to also use it to produce the SQL
#    representation, you are also done. E.g., comparisons and bitwise operations
#    on columns.
# 4. Otherwise, you need to define a class-level function, hybrid_property.expression,
#    which gives the SQL representation of your property when it is passed to
#    a sa query.
# 5. Because of how redefining decorators is supposed to work in Python [1], you
#    should use @<property_method_name>.inplace.expression to define your
#    class-level function that describes how the property should be represented
#    in SQL.
#
# [1] https://docs.sqlalchemy.org/en/20/orm/extensions/hybrid.html#using-inplace-to-create-pep-484-compliant-hybrid-properties


class Base(sa_orm.MappedAsDataclass, sa_orm.DeclarativeBase):
    """Base class for all DB mapped classes."""

    type_annotation_map: ClassVar = {
        # proto  message column types
        common_pb2.BlobUrlList: ProtoMessageDecorator(common_pb2.BlobUrlList()),
        feature_view_pb2.FeatureViewOutput: ProtoMessageDecorator(
            feature_view_pb2.FeatureViewOutput()
        ),
        common_pb2.EmbeddingMetrics: ProtoMessageDecorator(
            common_pb2.EmbeddingMetrics()
        ),
        common_pb2.AgentMessageMetadata: ProtoMessageDecorator(
            common_pb2.AgentMessageMetadata()
        ),
        space_pb2.SpaceParameters: ProtoMessageDecorator(space_pb2.SpaceParameters()),
        table_pb2.TableComputeOp: ProtoMessageDecorator(table_pb2.TableComputeOp()),
        agent_pb2.AgentParameters: ProtoMessageDecorator(agent_pb2.AgentParameters()),
        table_pb2.NamedTables: ProtoMessageDecorator(table_pb2.NamedTables()),
        common_pb2.RetrievedEntities: ProtoMessageDecorator(
            common_pb2.RetrievedEntities()
        ),
        # ID types
        OrgID: StrIDDecorator(OrgID()),
        RoomID: IntIDDecorator(RoomID()),
        ResourceID: IntIDDecorator(ResourceID()),
        SourceID: IntIDDecorator(SourceID()),
        FeatureViewID: IntIDDecorator(FeatureViewID()),
        FeatureViewSourceID: IntIDDecorator(FeatureViewSourceID()),
        SpaceID: IntIDDecorator(SpaceID()),
        SpaceRunID: IntIDDecorator(SpaceRunID()),
        SpaceParametersID: IntIDDecorator(SpaceParametersID()),
        AgentID: IntIDDecorator(AgentID()),
        AgentMessageID: IntIDDecorator(AgentMessageID()),
        UserMessageID: IntIDDecorator(UserMessageID()),
        MessageEntryID: IntIDDecorator(MessageEntryID()),
    }

    _created_at: sa_orm.Mapped[datetime] = sa_orm.mapped_column(
        "created_at", sa.DateTime(timezone=True), server_default=utc_now(), init=False
    )

    _updated_at: sa_orm.Mapped[datetime] = sa_orm.mapped_column(
        "updated_at",
        sa.DateTime(timezone=True),
        onupdate=utc_now(),
        server_default=utc_now(),
        init=False,
        nullable=True,
    )

    @hybrid.hybrid_property
    def created_at(self) -> datetime:
        if not self._created_at:
            # If not committed in the database the output should be None.
            # Align the typing to other fields without the None included.
            return None  # pyright: ignore[reportReturnType]
        return self._created_at.replace(tzinfo=timezone.utc)

    @created_at.inplace.expression
    @classmethod
    def _created_at_expression(cls):
        return cls._created_at

    @hybrid.hybrid_property
    def updated_at(self) -> datetime:
        if not self._updated_at:
            # If not committed in the database the output should be None.
            # Align the typing to other fields without the None included.
            return None  # pyright: ignore[reportReturnType]
        return self._updated_at.replace(tzinfo=timezone.utc)

    @updated_at.inplace.expression
    @classmethod
    def _updated_at_expression(cls):
        return cls._created_at

    @classmethod
    def foreign_key(cls):
        return ForeignKey(cls=cls)


class OrgBase(Base):
    """An organization it a top level grouping of resources."""

    __tablename__ = "org"

    # overriding table_args is the recommending way of defining these base model types
    __table_args__: ClassVar[Any] = ({"extend_existing": True},)

    id: sa_orm.Mapped[OrgID] = primary_key_uuid_column()

    @property
    def name(self) -> str:
        return str(self.id)


class EventKey:
    """An event key."""

    @runtime_checkable
    class Provider(Protocol):
        """Type which can provide an event key."""

        @property
        def event_key(self) -> EventKey: ...

    def __init__(self, id: str):
        self._id = id

    def __str__(self):
        return self._id

    @classmethod
    def from_str(cls, id: str) -> Self:
        return cls(id=id)

    @classmethod
    def from_uuid(cls, uuid: uuid.UUID) -> Self:
        return cls(id=str(uuid))

    @property
    def event_key(self):
        return self


class EventBase(Base):
    """Events from corvic orm objects."""

    __tablename__ = "event"

    # overriding table_args is the recommending way of defining these base model types
    __table_args__: ClassVar[Any] = {"extend_existing": True}

    event: sa_orm.Mapped[int] = sa_orm.mapped_column(sa.Integer)
    reason: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    regarding: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    event_key: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    timestamp: sa_orm.Mapped[datetime] = sa_orm.mapped_column(
        sa.DateTime(timezone=True)
    )
    id: sa_orm.Mapped[int | None] = primary_key_identity_column(type_=INT_PK_TYPE)

    @classmethod
    def select_latest_by_event_key(cls, event_key: EventKey, limit: int | None = None):
        query = (
            sa.select(cls)
            .where(cls.event_key == str(event_key))
            .order_by(cls.timestamp.desc())
        )
        if limit:
            query = query.limit(limit)
        return query

    def as_event(self) -> event_pb2.Event:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(dt=self.timestamp)
        return event_pb2.Event(
            reason=self.reason,
            regarding=self.regarding,
            event_type=event_pb2.EventType.Name(self.event),
            timestamp=timestamp,
        )
