from typing import Any, Dict, Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.custom_entities import (
    archive_custom_entities,
    bulk_create_custom_entities,
    bulk_get_custom_entities,
    bulk_update_custom_entities,
    bulk_upsert_custom_entities,
    create_custom_entity,
    get_custom_entity,
    list_custom_entities,
    unarchive_custom_entities,
    update_custom_entity,
    upsert_custom_entity,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.logging_helpers import check_for_csv_bug_fix
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import (
    none_as_unset,
    optional_array_query_param,
    schema_fields_query_param,
)
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import (
    BulkCreateCustomEntitiesAsyncTaskResponse,
    BulkUpdateCustomEntitiesAsyncTaskResponse,
    CustomEntitiesArchivalChange,
    CustomEntitiesArchive,
    CustomEntitiesBulkCreateRequest,
    CustomEntitiesBulkUpdateRequest,
    CustomEntitiesBulkUpsertRequest,
    CustomEntitiesPaginatedList,
    CustomEntitiesUnarchive,
    CustomEntity,
    CustomEntityBulkCreate,
    CustomEntityBulkUpdate,
    CustomEntityCreate,
    CustomEntityUpdate,
    CustomEntityUpsertRequest,
    EntityArchiveReason,
    ListCustomEntitiesSort,
)
from benchling_sdk.services.v2.base_service import BaseService


class CustomEntityService(BaseService):
    """
    Service for managing custom entities in Benchling.

    Custom entities are flexible biological entities that allow you to model 
    lab-specific objects like cell lines, reagents, samples, or any other 
    biological entity that doesn't fit standard sequence types.

    All custom entities must have an entity schema that defines their structure, 
    validation rules, and field types. They support both schema fields (defined 
    by the schema) and custom fields (user-defined metadata).

    See https://benchling.com/api/reference#/Custom%20Entities
    """

    @api_method
    def get_by_id(self, entity_id: str, returning: Optional[Iterable[str]] = None) -> CustomEntity:
        """
        Get a custom entity.

        Args:
            entity_id (str): The ID of the custom entity to get.
            returning (Optional[Iterable[str]]): The fields to return.
                See https://benchling.com/api/reference#/Custom%20Entities/getCustomEntity
                for available fields. If not specified, returns all fields. Examples:
                - ["id", "name", "fields"] for basic info only
                - ["customEntities.fields.Status"] for specific field

        Returns:
            CustomEntity: The custom entity.

        Example:
            Get a custom entity with all fields:

            .. code-block:: python

                entity = custom_entities.get_by_id("bfi_abc123")
                print(f"Entity: {entity.name} (Schema: {entity.schema_id})")
                
                # Get only specific fields for performance
                entity = custom_entities.get_by_id(
                    "bfi_abc123", 
                    returning=["id", "name", "fields.Vendor"]
                )

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/getCustomEntity

        """
        returning_string = optional_array_query_param(returning)
        response = get_custom_entity.sync_detailed(
            client=self.client, custom_entity_id=entity_id, returning=none_as_unset(returning_string)
        )
        return model_from_detailed(response)

    @api_method
    def _custom_entities_page(
        self,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        created_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[ListCustomEntitiesSort] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
    ) -> Response[CustomEntitiesPaginatedList]:
        response = list_custom_entities.sync_detailed(
            client=self.client,
            schema_id=none_as_unset(schema_id),
            modified_at=none_as_unset(modified_at),
            created_at=none_as_unset(created_at),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            folder_id=none_as_unset(folder_id),
            mentioned_in=none_as_unset(optional_array_query_param(mentioned_in)),
            project_id=none_as_unset(project_id),
            registry_id=none_as_unset(registry_id),
            archive_reason=none_as_unset(archive_reason),
            mentions=none_as_unset(optional_array_query_param(mentions)),
            sort=none_as_unset(sort),
            ids=none_as_unset(optional_array_query_param(ids)),
            entity_registry_idsany_of=none_as_unset(optional_array_query_param(entity_registry_ids_any_of)),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
            creator_ids=none_as_unset(optional_array_query_param(creator_ids)),
            schema_fields=none_as_unset(schema_fields_query_param(schema_fields)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            author_idsany_of=none_as_unset(optional_array_query_param(author_idsany_of)),
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        schema_id: Optional[str] = None,
        modified_at: Optional[str] = None,
        created_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[Union[str, ListCustomEntitiesSort]] = None,
        page_size: Optional[int] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
    ) -> PageIterator[CustomEntity]:
        """
        List custom entities with flexible filtering and pagination.

        This method supports comprehensive filtering options to find specific entities.
        For performance on large datasets, always specify schema_id when possible.

        Args:
            schema_id (Optional[str]): Filter to entities of this schema type. Recommended
                for performance on tenants with many entities.
            modified_at (Optional[str]): Filter to entities modified after this date/time.
                Format: ISO 8601 (e.g., "2024-01-15" or "2024-01-15T10:30:00Z").
            created_at (Optional[str]): Filter to entities created after this date/time.
                Same format as modified_at.
            name (Optional[str]): Filter to entities with this exact name (case-sensitive).
            name_includes (Optional[str]): Filter to entities whose name contains this substring
                (case-insensitive).
            folder_id (Optional[str]): Filter to entities in this folder.
            mentioned_in (Optional[List[str]]): Filter to entities mentioned in these entries.
            project_id (Optional[str]): Filter to entities in this project.
            registry_id (Optional[str]): Filter to entities in this registry.
            archive_reason (Optional[str]): Filter to entities archived for this reason.
            mentions (Optional[List[str]]): Filter to entities that mention these items.
            ids (Optional[Iterable[str]]): Filter to entities with these specific IDs.
            entity_registry_ids_any_of (Optional[Iterable[str]]): Filter to entities with
                any of these registry IDs.
            names_any_of (Optional[Iterable[str]]): Filter to entities with any of these
                names (case-insensitive).
            names_any_of_case_sensitive (Optional[Iterable[str]]): Filter to entities with
                any of these names (case-sensitive).
            creator_ids (Optional[Iterable[str]]): Filter to entities created by these users.
            schema_fields (Optional[Dict[str, Any]]): Filter by schema field values.
                Example: {"Status": "Active", "Priority": "High"}.
            sort (Optional[Union[str, ListCustomEntitiesSort]]): Sort order.
                Examples: "name:asc", "modifiedAt:desc".
            page_size (Optional[int]): Number of results per page (max 100).
            author_idsany_of (Optional[Iterable[str]]): Filter to entities authored by these users.
            returning (Optional[Iterable[str]]): Specify which fields to return for performance.
                Examples: ["id", "name"], ["customEntities.fields.Status"].

        Returns:
            PageIterator[CustomEntity]: An iterator over pages of custom entities.

        Example:
            List entities with filtering and pagination:

            .. code-block:: python

                entities = custom_entities.list(
                    schema_id="ts_cellline_schema",
                    name_includes="HEK",
                    folder_id="lib_abc123",
                    modified_at="2024-01-01",
                    page_size=50,
                    sort="name:asc",
                    returning=["id", "name", "fields.Status"]
                )
                
                for page in entities:
                    for entity in page:
                        print(f"Entity: {entity.name} (ID: {entity.id})")

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/listCustomEntities

        """
        check_for_csv_bug_fix("mentioned_in", mentioned_in)
        check_for_csv_bug_fix("mentions", mentions)

        if returning and "nextToken" not in returning:
            returning = list(returning) + ["nextToken"]

        def api_call(next_token: NextToken) -> Response[CustomEntitiesPaginatedList]:
            return self._custom_entities_page(
                schema_id=schema_id,
                modified_at=modified_at,
                created_at=created_at,
                name=name,
                name_includes=name_includes,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                archive_reason=archive_reason,
                mentions=mentions,
                ids=ids,
                entity_registry_ids_any_of=entity_registry_ids_any_of,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                creator_ids=creator_ids,
                schema_fields=schema_fields,
                sort=_translate_to_string_enum(ListCustomEntitiesSort, sort),
                page_size=page_size,
                next_token=next_token,
                author_idsany_of=author_idsany_of,
                returning=returning,
            )

        def results_extractor(body: CustomEntitiesPaginatedList) -> Optional[List[CustomEntity]]:
            return body.custom_entities

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, entity: CustomEntityCreate) -> CustomEntity:
        """
        Create a new custom entity.

        Creates a single custom entity with the specified properties. The entity
        must be associated with a valid schema and folder.

        Args:
            entity (CustomEntityCreate): 
                The custom entity to create. Contains the following fields:
                
                **Required Fields:**
                
                * **name** (str): The display name for the entity
                * **schema_id** (str): The ID of the schema that defines this entity type  
                * **folder_id** (str): The ID of the folder where the entity will be stored
                
                **Optional Fields:**
                
                * **fields** (Optional[Fields]): Schema-defined field values created using the 
                  fields() helper. Structure: ``{"field_name": {"value": field_value}}``
                * **custom_fields** (Optional[CustomFields]): User-defined field values created 
                  using custom_fields() helper
                * **registry_id** (Optional[str]): The ID of the registry if the entity should 
                  be registered
                * **entity_registry_id** (Optional[str]): Custom identifier for the entity in 
                  the registry
                * **naming_strategy** (Optional[NamingStrategy]): Strategy for naming registered 
                  entities (e.g., ``NamingStrategy.KEEP_NAMES``)
                * **author_ids** (Optional[List[str]]): List of user IDs to set as authors
                * **custom_notation_ids** (Optional[List[str]]): List of custom notation IDs

        Returns:
            CustomEntity: The newly created custom entity with generated ID and server-populated fields.

        Note:
            For registry entities, provide either:
            
            * ``registry_id`` + ``entity_registry_id`` OR
            * ``registry_id`` + ``naming_strategy``
            
            You cannot specify both ``entity_registry_id`` and ``naming_strategy``.

        Example:
            Create a custom entity with schema and custom fields:

            .. code-block:: python

                from benchling_sdk.models import CustomEntityCreate, NamingStrategy
                from benchling_sdk.helpers.serialization_helpers import fields, custom_fields

                entity = CustomEntityCreate(
                    name="Cell Line HEK293",
                    schema_id="ts_rbQWr8Pf",
                    folder_id="lib_TL5mqoz9",
                    registry_id="src_LbZzJIke", 
                    naming_strategy=NamingStrategy.NEW_IDS,
                    fields=fields({
                        "Vendor": {"value": "Vendor Name"},
                        "Passage Number": {"value": 15}
                    }),
                    custom_fields=custom_fields({
                        "Notes": {"value": "Created via API"}
                    })
                )
                created_entity = custom_entities.create(entity)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/createCustomEntity

        """
        response = create_custom_entity.sync_detailed(client=self.client, json_body=entity)
        return model_from_detailed(response)

    @api_method
    def update(self, entity_id: str, entity: CustomEntityUpdate) -> CustomEntity:
        """
        Update an existing custom entity.

        Updates the specified fields of a custom entity. Only provided fields will be
        updated; omitted fields remain unchanged.

        Args:
            entity_id (str): 
                The ID of the custom entity to update.
                
            entity (CustomEntityUpdate): 
                The update data containing:
                
                * **fields** (Optional[Fields]): Schema-defined field values to update using 
                  fields() helper. Only specified fields will be updated.
                * **custom_fields** (Optional[CustomFields]): User-defined field values to 
                  update using custom_fields() helper.
                * **author_ids** (Optional[List[str]]): List of user IDs to set as authors.
                * **custom_notation_ids** (Optional[List[str]]): List of custom notation IDs.

        Returns:
            CustomEntity: The updated custom entity with new field values.

        Example:
            Update custom fields on an entity:

            .. code-block:: python

                from benchling_sdk.models import CustomEntityUpdate
                from benchling_sdk.helpers.serialization_helpers import custom_fields

                update = CustomEntityUpdate(
                    custom_fields=custom_fields({
                        "Notes": {"value": "Updated via API"},
                        "Priority": {"value": "High"}
                    })
                )
                updated_entity = custom_entities.update("ent_abc123", update)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/updateCustomEntity

        """
        response = update_custom_entity.sync_detailed(
            client=self.client, custom_entity_id=entity_id, json_body=entity
        )
        return model_from_detailed(response)

    @api_method
    def archive(self, entity_ids: Iterable[str], reason: EntityArchiveReason) -> CustomEntitiesArchivalChange:
        """
        Archive custom entities.

        Archives multiple custom entities with a specified reason. Archived entities
        are hidden from normal views but can be restored using unarchive().

        Args:
            entity_ids (Iterable[str]): 
                The IDs of custom entities to archive. Can be a list, tuple, or any iterable of string IDs.
                
            reason (EntityArchiveReason): 
                The reason for archiving. Valid values:
                
                * **EntityArchiveReason.MADE_IN_ERROR**: Entity was created by mistake
                * **EntityArchiveReason.RETIRED**: Entity is no longer in use  
                * **EntityArchiveReason.SHIPPED_TO_COLLABORATOR**: Entity sent externally
                * **EntityArchiveReason.OTHER**: Other reason not listed

        Returns:
            CustomEntitiesArchivalChange: Archive operation result containing the list of successfully archived entity IDs 
            and any errors that occurred during archival.

        Example:
            Archive entities with a specific reason:

            .. code-block:: python

                from benchling_sdk.models import EntityArchiveReason

                entity_ids = ["ent_abc123", "ent_def456", "ent_ghi789"]
                result = custom_entities.archive(
                    entity_ids, 
                    reason=EntityArchiveReason.MADE_IN_ERROR
                )
                print(f"Archived {len(result.custom_entity_ids)} entities")

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/archiveCustomEntities

        """
        archive_request = CustomEntitiesArchive(reason=reason, custom_entity_ids=list(entity_ids))
        response = archive_custom_entities.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, entity_ids: Iterable[str]) -> CustomEntitiesArchivalChange:
        """
        Unarchive (restore) previously archived custom entities.

        Restores archived custom entities, making them visible in normal views again.

        Args:
            entity_ids (Iterable[str]): The IDs of archived custom entities to restore.
                Can be a list, tuple, or any iterable of string IDs.

        Returns:
            CustomEntitiesArchivalChange: Unarchive operation result containing the list of successfully unarchived entity IDs 
            and any errors that occurred during unarchival.

        Example:
            Unarchive multiple entities:

            .. code-block:: python

                entity_ids = ["ent_abc123", "ent_def456"] 
                result = custom_entities.unarchive(entity_ids)
                print(f"Unarchived {len(result.custom_entity_ids)} entities")

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/unarchiveCustomEntities

        """
        unarchive_request = CustomEntitiesUnarchive(custom_entity_ids=list(entity_ids))
        response = unarchive_custom_entities.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(
        self, entity_ids: Iterable[str], returning: Optional[Iterable[str]] = None
    ) -> Optional[List[CustomEntity]]:
        """
        Retrieve multiple custom entities by ID in a single request.

        Efficiently fetches multiple custom entities by their IDs. More performant
        than calling get_by_id() multiple times.

        Args:
            entity_ids (Iterable[str]): The IDs of custom entities to retrieve.
                Can be a list, tuple, or any iterable of string IDs.
            returning (Optional[Iterable[str]]): Fields to return for performance
                optimization. If not specified, returns all fields. Examples:
                - ["id", "name", "fields"] for basic info only
                - ["customEntities.fields.Status"] for specific fields

        Returns:
            Optional[List[CustomEntity]]: List of retrieved custom entities, or None if no entities found. 
            Order may not match input order.

        Example:
            Get multiple entities with specific fields:

            .. code-block:: python

                entity_ids = ["ent_abc123", "ent_def456", "ent_ghi789"]
                entities = custom_entities.bulk_get(
                    entity_ids,
                    returning=["id", "name", "fields.Status"]
                )
                
                for entity in entities:
                    print(f"Entity: {entity.name} (Status: {entity.fields.get('Status')})")

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/bulkGetCustomEntities

        """
        entity_id_string = ",".join(entity_ids)
        returning_string = optional_array_query_param(returning)
        response = bulk_get_custom_entities.sync_detailed(
            client=self.client,
            custom_entity_ids=entity_id_string,
            returning=none_as_unset(returning_string),
        )
        custom_entities = model_from_detailed(response)
        return custom_entities.custom_entities

    @api_method
    def bulk_create(
        self, entities: Iterable[CustomEntityBulkCreate]
    ) -> TaskHelper[BulkCreateCustomEntitiesAsyncTaskResponse]:
        """
        Create multiple custom entities in a single asynchronous operation.

        Efficiently creates many custom entities at once. Returns a task that runs
        asynchronously - use the TaskHelper to monitor progress and get results.

        Args:
            entities (Iterable[CustomEntityBulkCreate]): 
                The custom entities to create. Each entity should have the same structure as 
                CustomEntityCreate with name, schema_id, folder_id, fields, and optional custom_fields.

        Returns:
            TaskHelper[BulkCreateCustomEntitiesAsyncTaskResponse]: Async task helper for monitoring the bulk creation operation. Use ``wait_for_completion()``
            or check task status to get results.

        Example:
            Create multiple entities and wait for completion:

            .. code-block:: python

                from benchling_sdk.models import CustomEntityBulkCreate
                from benchling_sdk.helpers.serialization_helpers import fields

                entities = [
                    CustomEntityBulkCreate(
                        name=f"Sample {i}",
                        schema_id="ts_sample_schema",
                        folder_id="lib_samples",
                        fields=fields({"Index": {"value": i}})
                    ) for i in range(10)
                ]

                task_helper = custom_entities.bulk_create(entities)
                task = benchling.tasks.wait_for_task(task_helper.task_id)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/bulkCreateCustomEntities

        """
        body = CustomEntitiesBulkCreateRequest(list(entities))
        response = bulk_create_custom_entities.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkCreateCustomEntitiesAsyncTaskResponse)

    @api_method
    def bulk_update(
        self, entities: Iterable[CustomEntityBulkUpdate]
    ) -> TaskHelper[BulkUpdateCustomEntitiesAsyncTaskResponse]:
        """
        Update multiple custom entities in a single asynchronous operation.

        Efficiently updates many custom entities at once. Returns a task that runs
        asynchronously - use the TaskHelper to monitor progress and get results.

        Args:
            entities (Iterable[CustomEntityBulkUpdate]): The entity updates to apply.
                Each update should contain the entity ID and the fields to update.

        Returns:
            TaskHelper[BulkUpdateCustomEntitiesAsyncTaskResponse]: Async task helper for monitoring the bulk update operation. Use ``wait_for_completion()``
            or check task status to get results.

        Example:
            Update multiple entities with new field values:

            .. code-block:: python

                from benchling_sdk.models import CustomEntityBulkUpdate
                from benchling_sdk.helpers.serialization_helpers import fields

                updates = [
                    CustomEntityBulkUpdate(
                        id="ent_abc123",
                        fields=fields({"Status": {"value": "Complete"}})
                    ),
                    CustomEntityBulkUpdate(
                        id="ent_def456", 
                        fields=fields({"Status": {"value": "In Progress"}})
                    )
                ]

                task_helper = custom_entities.bulk_update(updates)
                task = benchling.tasks.wait_for_task(task_helper.task_id)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/bulkUpdateCustomEntities

        """
        body = CustomEntitiesBulkUpdateRequest(list(entities))
        response = bulk_update_custom_entities.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkUpdateCustomEntitiesAsyncTaskResponse)

    @api_method
    def upsert(self, entity_registry_id: str, entity: CustomEntityUpsertRequest) -> CustomEntity:
        """
        Create or update a custom entity based on registry ID.

        Creates a new entity if none exists with the given registry ID, or updates
        the existing entity if found. Useful for synchronizing with external systems.

        Args:
            entity_registry_id (str): The registry ID to use for lookup/creation.
                This should be a unique identifier from your external system.
            entity (CustomEntityUpsertRequest): The entity data containing name,
                schema_id, folder_id, registry_id, fields, and optional custom_fields.

        Returns:
            CustomEntity: The created or updated custom entity.

        Example:
            Upsert entity from external system:

            .. code-block:: python

                from benchling_sdk.models import CustomEntityUpsertRequest
                from benchling_sdk.helpers.serialization_helpers import fields

                external_id = "EXT_SAMPLE_001"
                upsert_request = CustomEntityUpsertRequest(
                    name="External Sample 001",
                    schema_id="ts_sample_schema",
                    folder_id="lib_external_samples",
                    registry_id="sample_registry",
                    fields=fields({
                        "External ID": {"value": external_id},
                        "Status": {"value": "Active"}
                    })
                )

                entity = custom_entities.upsert(external_id, upsert_request)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/upsertCustomEntity

        """
        response = upsert_custom_entity.sync_detailed(
            client=self.client, entity_registry_id=entity_registry_id, json_body=entity
        )
        return model_from_detailed(response)

    @api_method
    def bulk_upsert(
        self, body: CustomEntitiesBulkUpsertRequest
    ) -> TaskHelper[BulkUpdateCustomEntitiesAsyncTaskResponse]:
        """
        Create or update multiple custom entities based on registry IDs.

        Efficiently performs upsert operations on many entities at once. Each entity
        is created if its registry ID doesn't exist, or updated if found.

        Args:
            body (CustomEntitiesBulkUpsertRequest): Bulk upsert request containing
                the list of entities to upsert, each with registry ID and entity data.

        Returns:
            TaskHelper[BulkUpdateCustomEntitiesAsyncTaskResponse]: Async task helper for monitoring the bulk upsert operation. Use ``wait_for_completion()`` 
            to get the final results.

        Example:
            Bulk upsert multiple entities:

            .. code-block:: python

                from benchling_sdk.models import CustomEntitiesBulkUpsertRequest
                
                upsert_request = CustomEntitiesBulkUpsertRequest(
                    custom_entities=[
                        {"registry_id": "REG_001", "name": "Entity 1", "schema_id": "ts_abc123"},
                        {"registry_id": "REG_002", "name": "Entity 2", "schema_id": "ts_abc123"}
                    ]
                )
                
                task_helper = custom_entities.bulk_upsert(upsert_request)
                task = benchling.tasks.wait_for_task(task_helper.task_id)

        See Also:
            https://benchling.com/api/reference#/Custom%20Entities/bulkUpsertCustomEntities

        """
        response = bulk_upsert_custom_entities.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkUpdateCustomEntitiesAsyncTaskResponse)
