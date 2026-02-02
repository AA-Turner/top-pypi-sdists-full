import dataclasses
from typing import Generic, TypeVar

from google.protobuf import json_format, struct_pb2
from typing_extensions import overload

from corvic import orm
from corvic.result import InvalidArgumentError, Ok
from corvic_generated.model.v1alpha import models_pb2
from corvic_generated.orm.v1 import common_pb2

_Proto = (
    models_pb2.Resource
    | models_pb2.Source
    | models_pb2.FeatureView
    | models_pb2.Space
    | models_pb2.FeatureViewSource
    | models_pb2.Agent
)
_Orm = (
    orm.Resource
    | orm.Source
    | orm.FeatureView
    | orm.Space
    | orm.FeatureViewSource
    | orm.Agent
)

_ID = TypeVar(
    "_ID",
    orm.ResourceID,
    orm.SourceID,
    orm.FeatureViewID,
    orm.SpaceID,
    orm.FeatureViewSourceID,
    orm.AgentID,
)


@dataclasses.dataclass
class _OrmIDs(Generic[_ID]):
    obj_id: _ID | None
    room_id: orm.RoomID | None


def _translate_orm_ids(
    proto_obj: _Proto, obj_id_class: type[_ID]
) -> Ok[_OrmIDs[_ID]] | orm.InvalidORMIdentifierError:
    if not proto_obj.id:
        obj_id = None
    else:
        obj_id = obj_id_class(proto_obj.id)
        match obj_id.to_db():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok():
                pass

    match proto_obj:
        case (
            models_pb2.Resource()
            | models_pb2.Source()
            | models_pb2.FeatureView()
            | models_pb2.Space()
            | models_pb2.Agent()
        ):
            room_id = orm.RoomID(proto_obj.room_id)
            match room_id.to_db():
                case orm.InvalidORMIdentifierError() as err:
                    return err
                case Ok():
                    pass
        case models_pb2.FeatureViewSource():
            room_id = None

    return Ok(_OrmIDs(obj_id, room_id))


@overload
def orm_to_proto(orm_obj: orm.Resource) -> models_pb2.Resource: ...


@overload
def orm_to_proto(orm_obj: orm.Source) -> models_pb2.Source: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureView) -> models_pb2.FeatureView: ...


@overload
def orm_to_proto(orm_obj: orm.Space) -> models_pb2.Space: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureViewSource) -> models_pb2.FeatureViewSource: ...


@overload
def orm_to_proto(orm_obj: orm.Agent) -> models_pb2.Agent: ...


def _agent_orm_to_proto(orm_obj: orm.Agent):
    messages: list[models_pb2.MessageEntry] = []
    for raw_message in orm_obj.messages.values():
        agent_message = None
        user_message = None
        if (
            raw_message.agent_message is not None
            and raw_message.user_message is not None
        ):
            raise ValueError("both agent message and user message are not None")
        if raw_message.agent_message is not None:
            match raw_message.agent_message.message_metadata:
                case common_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED
                case common_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_DOWN:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_DOWN
                case common_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_UP:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_THUMBS_UP
                case _:
                    reaction = models_pb2.MessageReaction.MESSAGE_REACTION_UNSPECIFIED

            struct = struct_pb2.Struct()
            json_format.Parse(
                raw_message.agent_message.policy
                if raw_message.agent_message.policy is not None
                else "{}",
                struct,
            )
            agent_message = models_pb2.AgentMessage(
                id=str(raw_message.agent_message_id),
                message=raw_message.agent_message.message,
                policy=struct,
                context=raw_message.agent_message.context,
                message_reaction=reaction,
                user_message_id=str(raw_message.agent_message.user_message_id),
                retrieved_entities=raw_message.agent_message.retrieved_entities,
            )
        elif raw_message.user_message is not None:
            user_message = models_pb2.UserMessage(
                id=str(raw_message.user_message_id),
                message=raw_message.user_message.message,
            )
        else:
            raise ValueError("no user message nor agent message retrieved")

        message = models_pb2.MessageEntry(
            id=str(raw_message.id),
            user_message=user_message,
            agent_message=agent_message,
        )
        messages.append(message)

    return models_pb2.Agent(
        id=str(orm_obj.id),
        name=orm_obj.name,
        room_id=str(orm_obj.room_id),
        agent_parameters=orm_obj.parameters,
        org_id=str(orm_obj.org_id),
        messages=messages,
    )


def orm_to_proto(orm_obj: _Orm) -> _Proto:
    match orm_obj:
        case orm.Resource():
            return models_pb2.Resource(
                id=str(orm_obj.id),
                name=orm_obj.name,
                description=orm_obj.description,
                mime_type=orm_obj.mime_type,
                url=orm_obj.url,
                md5=orm_obj.md5,
                size=orm_obj.size,
                original_path=orm_obj.original_path,
                room_id=str(orm_obj.room_id),
                source_ids=[str(val.source_id) for val in orm_obj.source_associations],
                org_id=str(orm_obj.org_id),
            )
        case orm.Source():
            return models_pb2.Source(
                id=str(orm_obj.id),
                name=orm_obj.name,
                table_op_graph=orm_obj.table_op_graph,
                room_id=str(orm_obj.room_id),
                resource_id=str(orm_obj.resource_associations[0].resource_id)
                if orm_obj.resource_associations
                else "",
                org_id=str(orm_obj.org_id),
            )
        case orm.FeatureView():
            return models_pb2.FeatureView(
                id=str(orm_obj.id),
                name=orm_obj.name,
                description=orm_obj.description,
                room_id=str(orm_obj.room_id),
                feature_view_output=orm_obj.feature_view_output,
                org_id=str(orm_obj.org_id),
            )
        case orm.Space():
            raise NotImplementedError()
        case orm.FeatureViewSource():
            raise NotImplementedError()
        case orm.Agent():
            return _agent_orm_to_proto(orm_obj=orm_obj)


@overload
def proto_to_orm(
    proto_obj: models_pb2.Resource,
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Source,
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureView,
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Space,
) -> Ok[orm.Space] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureViewSource,
) -> Ok[orm.FeatureViewSource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Agent,
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError: ...


def _resource_proto_to_orm(
    proto_obj: models_pb2.Resource,
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.ResourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    source_ids = list[orm.SourceID]()
    for source_id in proto_obj.source_ids:
        orm_id = orm.SourceID(source_id)
        match orm_id.to_db():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok():
                source_ids.append(orm_id)
    orm_obj = orm.Resource(
        id=ids.obj_id,
        name=proto_obj.name,
        description=proto_obj.description,
        mime_type=proto_obj.mime_type,
        md5=proto_obj.md5,
        url=proto_obj.url,
        size=proto_obj.size,
        original_path=proto_obj.original_path,
        room_id=ids.room_id,
        source_associations=[
            orm.SourceResourceAssociation(source_id=src_id, resource_id=ids.obj_id)
            for src_id in source_ids
        ],
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
        for assn in orm_obj.source_associations:
            assn.org_id = orm_obj.org_id
    return Ok(orm_obj)


def _source_proto_to_orm(
    proto_obj: models_pb2.Source,
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.SourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")
    resource_id = orm.ResourceID(proto_obj.resource_id)
    match resource_id.to_db():
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok():
            pass

    orm_obj = orm.Source(
        id=ids.obj_id,
        name=proto_obj.name,
        table_op_graph=proto_obj.table_op_graph,
        room_id=ids.room_id,
        resource_associations=[
            orm.SourceResourceAssociation(source_id=ids.obj_id, resource_id=resource_id)
        ],
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
        for assn in orm_obj.resource_associations:
            assn.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _agent_proto_to_orm(
    proto_obj: models_pb2.Agent,
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.AgentID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    orm_obj = orm.Agent(
        id=ids.obj_id,
        name=proto_obj.name,
        parameters=proto_obj.agent_parameters,
        room_id=ids.room_id,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def _feature_view_proto_to_orm(
    proto_obj: models_pb2.FeatureView,
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match _translate_orm_ids(proto_obj, orm.FeatureViewID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return InvalidArgumentError("room id required to commit resource")

    orm_obj = orm.FeatureView(
        id=ids.obj_id,
        name=proto_obj.name,
        description=proto_obj.description,
        room_id=ids.room_id,
        feature_view_output=proto_obj.feature_view_output,
    )
    if proto_obj.org_id:
        orm_obj.org_id = orm.OrgID(proto_obj.org_id)
    return Ok(orm_obj)


def proto_to_orm(
    proto_obj: _Proto,
) -> Ok[_Orm] | orm.InvalidORMIdentifierError | InvalidArgumentError:
    match proto_obj:
        case models_pb2.Resource():
            return _resource_proto_to_orm(proto_obj)
        case models_pb2.Source():
            return _source_proto_to_orm(proto_obj)
        case models_pb2.FeatureView():
            return _feature_view_proto_to_orm(proto_obj)
        case models_pb2.Space():
            raise NotImplementedError()
        case models_pb2.FeatureViewSource():
            raise NotImplementedError()
        case models_pb2.Agent():
            return _agent_proto_to_orm(proto_obj)
