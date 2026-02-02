"""Corvic Agents."""

from __future__ import annotations

import copy
import dataclasses
from typing import TypeAlias

import sqlalchemy.orm as sa_orm
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from corvic import orm, system
from corvic.model._defaults import get_default_client, get_default_room_id
from corvic.model._proto_orm_convert import orm_to_proto
from corvic.model._wrapped_proto import WrappedProto
from corvic.result import InvalidArgumentError, NotFoundError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1.agent_pb2 import AgentParameters

OrgID: TypeAlias = orm.OrgID
RoomID: TypeAlias = orm.RoomID
FeatureViewID: TypeAlias = orm.FeatureViewID
AgentID: TypeAlias = orm.AgentID


@dataclasses.dataclass(frozen=True)
class Agent(WrappedProto[AgentID, models_pb2.Agent]):
    """A corvic agent represents a named agent that can produce embeddings."""

    @classmethod
    def from_id(
        cls, agent_id: AgentID, client: system.Client | None = None
    ) -> Ok[Agent] | NotFoundError | InvalidArgumentError:
        client = client or get_default_client()
        with sa_orm.Session(client.sa_engine, expire_on_commit=False) as session:
            orm_self = session.get(orm.Agent, agent_id)

            if orm_self is None:
                return NotFoundError("agent with given id does not exists", id=agent_id)
            proto_self = orm_to_proto(orm_self)
        return Ok(
            cls(
                client,
                proto_self,
                AgentID(),
            )
        )

    @classmethod
    def from_orm(
        cls,
        agent: orm.Agent,
        client: system.Client | None = None,
    ):
        client = client or get_default_client()
        return cls(
            client,
            orm_to_proto(agent),
            AgentID(),
        )

    @classmethod
    def create(
        cls,
        name: str,
        parameters: AgentParameters,
        room_id: RoomID | None = None,
        client: system.Client | None = None,
    ):
        client = client or get_default_client()
        return cls(
            client,
            models_pb2.Agent(
                name=name,
                agent_parameters=parameters,
                room_id=str(room_id or get_default_room_id(client)),
            ),
            AgentID(),
        )

    @property
    def name(self) -> str:
        return self.proto_self.name

    @property
    def room_id(self) -> RoomID:
        return RoomID(self.proto_self.room_id)

    @property
    def parameters(self) -> AgentParameters:
        return self.proto_self.agent_parameters

    @property
    def messages(self) -> RepeatedCompositeFieldContainer[models_pb2.MessageEntry]:
        return self.proto_self.messages

    def with_name(self, name: str) -> Agent:
        proto_self = copy.copy(self.proto_self)
        proto_self.name = name
        return dataclasses.replace(
            self,
            proto_self=proto_self,
        )

    def with_parameters(self, parameters: AgentParameters) -> Agent:
        proto_self = copy.copy(self.proto_self)
        proto_self.agent_parameters.CopyFrom(parameters)
        return dataclasses.replace(
            self,
            proto_self=proto_self,
        )
