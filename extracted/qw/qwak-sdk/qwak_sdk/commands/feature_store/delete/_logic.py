from _qwak_proto.qwak.feature_store.entities.entity_pb2 import Entity, EntityDefinition
from _qwak_proto.qwak.feature_store.entities.entity_service_pb2 import (
    GetEntityByNameResponse,
)
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import FeatureSet
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2 import (
    GetFeatureSetByNameResponse,
)
from qwak.clients.feature_store import FeatureRegistryClient
from qwak.exceptions import QwakException
from qwak.feature_store._common.feature_set_utils import _INTERNAL_KEY_PREFIX

from qwak_sdk.tools.colors import Color

FEATURE_SET = "feature_set"
ENTITY = "entity"
DATA_SOURCE = "data_source"
All = "all"


def _handle_featureset_key_deletion(
    entity_definition: EntityDefinition, registry_client: FeatureRegistryClient
):
    # If entity name start with the fs name
    if entity_definition.entity_spec.name.startswith(_INTERNAL_KEY_PREFIX):
        get_entity_resp: GetEntityByNameResponse = registry_client.get_entity_by_name(
            entity_definition.entity_spec.name
        )

        # the entity exists
        if get_entity_resp:
            entity_id: str = entity_definition.entity_id
            registered_entity: Entity = get_entity_resp.entity

            # it has a no registered fs for it
            if (
                not registered_entity.feature_sets
                or len(registered_entity.feature_sets) == 0
            ):
                try:
                    # delete since it's a key and not an entity
                    registry_client.delete_entity(entity_id=entity_id)
                # we fail this silently
                except QwakException:
                    pass


def _inner_delete(name, object, registry_client):
    if object == ENTITY:
        feature_store_entity = registry_client.get_entity_by_name(name)
        _delete_object(
            lambda e: registry_client.delete_entity(
                e.entity.entity_definition.entity_id
            ),
            feature_store_entity,
            "entity",
            name,
        )
    if object == FEATURE_SET:
        feature_set_response: GetFeatureSetByNameResponse = (
            registry_client.get_feature_set_by_name(name)
        )
        if feature_set_response:
            feature_set: FeatureSet = feature_set_response.feature_set

            # Delete fs regardless
            registry_client.delete_feature_set(
                feature_set.feature_set_definition.feature_set_id
            )
            print(
                f"{Color.GREEN}Feature Set '{name}' deletion request is being handled by the service"
            )

            entity: EntityDefinition = (
                feature_set.feature_set_definition.feature_set_spec.entity
            )

            _handle_featureset_key_deletion(
                entity_definition=entity, registry_client=registry_client
            )
        else:
            print(
                f"{Color.RED}Could not find specified feature set named '{name}' to delete{Color.END}"
            )
    if object == DATA_SOURCE:
        feature_store_ds = registry_client.get_data_source_by_name(name)
        _delete_object(
            lambda e: registry_client.delete_data_source(
                e.data_source.data_source_definition.data_source_id
            ),
            feature_store_ds,
            "data source",
            name,
        )


def _delete_object(delete_func, _object, _type, name):
    if _object:
        delete_func(_object)
        print(f"{Color.GREEN}Successfully deleted the {_type} named '{name}'")
    else:
        print(
            f"{Color.RED}Could not find specified {_type} named '{name}' to delete{Color.END}"
        )
