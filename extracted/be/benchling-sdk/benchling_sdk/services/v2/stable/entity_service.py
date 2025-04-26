from typing import Iterable, Optional

from benchling_api_client.v2.stable.api.entities import bulk_upsert_entities

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import AsyncTaskLink, EntitiesBulkUpsertRequest
from benchling_sdk.services.v2.base_service import BaseService


class EntityService(BaseService):
    """
    Entities.

    Entities include DNA and AA sequences, oligos, molecules, custom entities, and
    other biological objects in Benchling. Entities support schemas, tags, and aliases,
    and can be registered.

    See https://benchling.com/api/reference#/Entities
    """

    @api_method
    def bulk_upsert(
        self, bulk_upsert: EntitiesBulkUpsertRequest, returning: Optional[Iterable[str]] = None
    ) -> AsyncTaskLink:
        """
        Upsert many entities at once.

        All entities and their schemas must be within the same registry.

        This operation performs the following actions:

        1. Any existing objects are looked up in Benchling by the provided entity registry ID.
        2. Then, all objects are either created or updated accordingly, temporarily skipping any schema field links between objects.
        3. Schema field links between objects are populated according to the provided identifier. In the `value` field of the `Field` resource, the entity registry ID may be provided instead of the API ID if desired. You may link to objects being created in the same operation.
        4. Entities are registered, using the provided name and entity registry ID.

        If any action fails, the whole operation is canceled and no objects are created or updated.
        See https://benchling.com/api/reference#/Entities/bulkUpsertEntities
        """
        returning_string = optional_array_query_param(returning)
        response = bulk_upsert_entities.sync_detailed(
            client=self.client, json_body=bulk_upsert, returning=none_as_unset(returning_string)
        )
        return model_from_detailed(response)
