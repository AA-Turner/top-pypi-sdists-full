"""Common model base."""

import abc
import dataclasses
import functools
import uuid
from typing import Generic, TypeVar

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from typing_extensions import Self, deprecated

from corvic import orm, system
from corvic.model._proto_orm_convert import orm_to_proto, proto_to_orm
from corvic.proto_wrapper import ProtoWrapper
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic_generated.model.v1alpha import models_pb2

_ID = TypeVar(
    "_ID",
    orm.ResourceID,
    orm.SourceID,
    orm.FeatureViewID,
    orm.SpaceID,
    orm.FeatureViewSourceID,
    orm.AgentID,
)
_ProtoObj = TypeVar(
    "_ProtoObj",
    models_pb2.Resource,
    models_pb2.Source,
    models_pb2.FeatureView,
    models_pb2.Space,
    models_pb2.FeatureViewSource,
    models_pb2.Agent,
)

_UNCOMMITTED_ID_PREFIX = "__uncommitted_object-"


def _generate_uncommitted_id_str():
    return f"{_UNCOMMITTED_ID_PREFIX}{uuid.uuid4()}"


@dataclasses.dataclass(frozen=True)
class WrappedProto(Generic[_ID, _ProtoObj], ProtoWrapper[_ProtoObj], abc.ABC):
    """Base for orm wrappers providing a unified update mechanism."""

    client: system.Client
    proto_self: _ProtoObj
    uncommitted_id: _ID

    def __post_init__(self):
        if not self.uncommitted_id:
            # set for new ids and transparently carried forward by
            # dataclasses.replace to track providance of in-memory objects
            object.__setattr__(
                self,
                "uncommitted_id",
                self.uncommitted_id.from_str(_generate_uncommitted_id_str()),
            )

    @functools.cached_property
    def id(self) -> _ID:
        # If this orm object has a non-empty id, it's based on an object
        # from the orm layer; return that instance's id. Else, return
        # an id unique to this ephemeral object.
        return self.uncommitted_id.from_str(self.proto_self.id) or self.uncommitted_id

    @deprecated("use commit instead")
    def register(self) -> Self:
        """Assign this object a new ID by committing it to the database."""
        return self.commit().unwrap_or_raise()

    def commit(self) -> Ok[Self] | InvalidArgumentError:
        """Store this object in the database at its id or a newly allocated id.

        This overwrites the entry at id in the database so that future readers will see
        this object. One of `id` or `derived_from_id` cannot be empty or None.
        """
        with sa_orm.Session(self.client.sa_engine, expire_on_commit=False) as session:
            new_orm_self = proto_to_orm(self.proto_self).unwrap_or_raise()
            if new_orm_self.id is None:
                session.add(new_orm_self)
            else:
                session.merge(new_orm_self)
            try:
                session.commit()
            except sa.exc.IntegrityError as err:
                return InvalidArgumentError.from_(err)
            return Ok(
                dataclasses.replace(
                    self,
                    proto_self=orm_to_proto(new_orm_self),
                )
            )

    def delete(self) -> Ok[Self] | NotFoundError:
        with sa_orm.Session(self.client.sa_engine, expire_on_commit=False) as session:
            new_orm_self = proto_to_orm(self.proto_self).unwrap_or_raise()
            val = session.query(new_orm_self.__class__).get(new_orm_self.id)
            if val is None:
                return NotFoundError("could not find object with that id")
            session.delete(val)
            session.commit()
            new_orm_self.id = None

            return Ok(
                dataclasses.replace(
                    self,
                    proto_self=orm_to_proto(new_orm_self),
                )
            )
