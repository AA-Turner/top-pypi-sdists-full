import uuid

import grpc
from _qwak_proto.qwak.feature_store.entities.entity_pb2 import (
    Entity,
    EntityDefinition,
    EntityMetadata,
    FeatureSetBrief,
)
from _qwak_proto.qwak.feature_store.entities.entity_service_pb2 import (
    CreateEntityResponse,
    DeleteEntityRequest,
    DeleteEntityResponse,
    GetEntityByIdResponse,
    GetEntityByNameResponse,
    ListEntitiesResponse,
)
from _qwak_proto.qwak.feature_store.entities.entity_service_pb2_grpc import (
    EntityServiceServicer,
)


class EntityServiceMock(EntityServiceServicer):
    def __init__(self):
        self._entities_spec = {}
        self._entity_id_name = {}

    def reset_entities(self):
        self._entities_spec.clear()

    def CreateEntity(self, request, context):
        entity_id = str(uuid.uuid4())
        self._entities_spec[request.entity_spec.name] = request.entity_spec
        self._entity_id_name[entity_id] = request.entity_spec.name
        return CreateEntityResponse()

    def DeleteEntity(self, request: DeleteEntityRequest, context):
        entity_id: str = request.entity_id

        if entity_id not in self._entity_id_name.keys():
            context.set_details(f"Entity ID {request.entity_id} doesn't exist'")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return

        entity_name: str = self._entity_id_name[entity_id]
        del self._entity_id_name[entity_id]
        del self._entities_spec[entity_name]

        return DeleteEntityResponse()

    def GetEntityByName(self, request, context):
        if request.entity_name not in self._entities_spec:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return GetEntityByNameResponse()

        entity_key: str = list(self._entity_id_name.keys())[
            list(self._entity_id_name.values()).index(request.entity_name)
        ]
        return GetEntityByNameResponse(
            entity=Entity(
                entity_definition=EntityDefinition(
                    entity_id=entity_key,
                    entity_spec=self._entities_spec[request.entity_name],
                ),
                metadata=None,
                feature_sets=[],
            )
        )

    def GetEntityById(self, request, context):
        if request.entity_id not in self._entity_id_name:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return GetEntityByIdResponse()

        entity_name: str = self._entity_id_name[request.entity_id]
        return GetEntityByIdResponse(
            entity=Entity(
                entity_definition=EntityDefinition(
                    entity_id=request.entity_id,
                    entity_spec=self._entities_spec[entity_name],
                ),
                metadata=None,
                feature_sets=[],
            )
        )

    def ListEntities(self, request, context):
        return ListEntitiesResponse(
            entities=[
                Entity(
                    entity_definition=EntityDefinition(
                        entity_spec=self._entities_spec[entity_name],
                        entity_id=entity_id,
                    ),
                    metadata=EntityMetadata(),
                    feature_sets=[FeatureSetBrief()],
                )
                for entity_id, entity_name in self._entity_id_name.items()
            ]
        )
