from typing import Any, Dict, Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.rna_oligos import (
    archive_rna_oligos,
    bulk_create_rna_oligos,
    bulk_update_rna_oligos,
    bulk_upsert_rna_oligos,
    create_rna_oligo,
    get_rna_oligo,
    list_rna_oligos,
    unarchive_rna_oligos,
    update_rna_oligo,
    upsert_rna_oligo,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import (
    none_as_unset,
    optional_array_query_param,
    schema_fields_query_param,
)
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import (
    BulkCreateRnaOligosAsyncTaskResponse,
    BulkUpdateRnaOligosAsyncTaskResponse,
    EntityArchiveReason,
    ListRNAOligosSort,
    OligoUpsertRequest,
    RnaOligo,
    RnaOligoBulkUpdate,
    RnaOligoCreate,
    RnaOligosArchivalChange,
    RnaOligosArchive,
    RnaOligosBulkCreateRequest,
    RnaOligosBulkUpdateRequest,
    RnaOligosBulkUpsertRequest,
    RnaOligosPaginatedList,
    RnaOligosUnarchive,
    RnaOligoUpdate,
)
from benchling_sdk.services.v2.base_service import BaseService


class RnaOligoService(BaseService):
    """
    RNA Oligos.

    RNA Oligos are short linear RNA sequences that can be attached as primers to full DNA sequences. Just like other
    entities, they support schemas, tags, and aliases.
    See https://benchling.com/api/reference#/RNA%20Oligos
    """

    @api_method
    def get_by_id(
        self,
        oligo_id: str,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> RnaOligo:
        """
        Get an RNA Oligo by ID.

        See https://benchling.com/api/reference#/RNA%20Oligos/getRNAOligo
        """
        returning_string = optional_array_query_param(returning)
        response = get_rna_oligo.sync_detailed(
            client=self.client,
            oligo_id=oligo_id,
            returning=none_as_unset(returning_string),
            custom_notation_id=none_as_unset(custom_notation_id),
        )
        return model_from_detailed(response)

    @api_method
    def _rna_oligos_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        sort: Optional[ListRNAOligosSort] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> Response[RnaOligosPaginatedList]:
        response = list_rna_oligos.sync_detailed(
            client=self.client,
            modified_at=none_as_unset(modified_at),
            name=none_as_unset(name),
            bases=none_as_unset(bases),
            folder_id=none_as_unset(folder_id),
            mentioned_in=none_as_unset(optional_array_query_param(mentioned_in)),
            project_id=none_as_unset(project_id),
            registry_id=none_as_unset(registry_id),
            schema_id=none_as_unset(schema_id),
            archive_reason=none_as_unset(archive_reason),
            mentions=none_as_unset(optional_array_query_param(mentions)),
            sort=none_as_unset(sort),
            ids=none_as_unset(optional_array_query_param(ids)),
            entity_registry_idsany_of=none_as_unset(optional_array_query_param(entity_registry_ids_any_of)),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
            schema_fields=none_as_unset(schema_fields_query_param(schema_fields)),
            creator_ids=none_as_unset(optional_array_query_param(creator_ids)),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            author_idsany_of=none_as_unset(optional_array_query_param(author_idsany_of)),
            returning=none_as_unset(optional_array_query_param(returning)),
            custom_notation_id=none_as_unset(custom_notation_id),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        bases: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        registry_id: Optional[str] = None,
        schema_id: Optional[str] = None,
        archive_reason: Optional[str] = None,
        mentions: Optional[List[str]] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        sort: Optional[Union[str, ListRNAOligosSort]] = None,
        page_size: Optional[int] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> PageIterator[RnaOligo]:
        """
        List RNA Oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/listRNAOligos
        """

        def api_call(next_token: NextToken) -> Response[RnaOligosPaginatedList]:
            return self._rna_oligos_page(
                modified_at=modified_at,
                name=name,
                bases=bases,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                project_id=project_id,
                registry_id=registry_id,
                schema_id=schema_id,
                archive_reason=archive_reason,
                mentions=mentions,
                ids=ids,
                entity_registry_ids_any_of=entity_registry_ids_any_of,
                name_includes=name_includes,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                schema_fields=schema_fields,
                creator_ids=creator_ids,
                sort=_translate_to_string_enum(ListRNAOligosSort, sort),
                page_size=page_size,
                next_token=next_token,
                author_idsany_of=author_idsany_of,
                returning=returning,
                custom_notation_id=custom_notation_id,
            )

        def results_extractor(body: RnaOligosPaginatedList) -> Optional[List[RnaOligo]]:
            return body.rna_oligos

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, rna_oligo: RnaOligoCreate) -> RnaOligo:
        """
        Create an RNA Oligo.

        See https://benchling.com/api/reference#/RNA%20Oligos/createRNAOligo
        """
        response = create_rna_oligo.sync_detailed(client=self.client, json_body=rna_oligo)
        return model_from_detailed(response)

    @api_method
    def update(self, oligo_id: str, rna_oligo: RnaOligoUpdate) -> RnaOligo:
        """
        Update an RNA Oligo.

        See https://benchling.com/api/reference#/RNA%20Oligos/updateRNAOligo
        """
        response = update_rna_oligo.sync_detailed(client=self.client, oligo_id=oligo_id, json_body=rna_oligo)
        return model_from_detailed(response)

    @api_method
    def archive(self, rna_oligo_ids: Iterable[str], reason: EntityArchiveReason) -> RnaOligosArchivalChange:
        """
        Archive RNA Oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/archiveRNAOligos
        """
        archive_request = RnaOligosArchive(reason=reason, rna_oligo_ids=list(rna_oligo_ids))
        response = archive_rna_oligos.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, rna_oligo_ids: Iterable[str]) -> RnaOligosArchivalChange:
        """
        Unarchive RNA Oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/unarchiveRNAOligos
        """
        unarchive_request = RnaOligosUnarchive(rna_oligo_ids=list(rna_oligo_ids))
        response = unarchive_rna_oligos.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_create(
        self, rna_oligos: Iterable[RnaOligoCreate]
    ) -> TaskHelper[BulkCreateRnaOligosAsyncTaskResponse]:
        """
        Bulk create RNA Oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/bulkCreateRNAOligos
        """
        body = RnaOligosBulkCreateRequest(list(rna_oligos))
        response = bulk_create_rna_oligos.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkCreateRnaOligosAsyncTaskResponse)

    @api_method
    def bulk_update(
        self, rna_oligos: Iterable[RnaOligoBulkUpdate]
    ) -> TaskHelper[BulkUpdateRnaOligosAsyncTaskResponse]:
        """
        Bulk update RNA oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/bulkUpdateRNAOligos
        """
        body = RnaOligosBulkUpdateRequest(list(rna_oligos))
        response = bulk_update_rna_oligos.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkUpdateRnaOligosAsyncTaskResponse)

    @api_method
    def upsert(self, entity_registry_id: str, rna_oligo: OligoUpsertRequest) -> RnaOligo:
        """
        Create or modify a RNA Oligo.

        See https://benchling.com/api/reference#/RNA%20Oligos/upsertRNAOligo
        """
        response = upsert_rna_oligo.sync_detailed(
            client=self.client, entity_registry_id=entity_registry_id, json_body=rna_oligo
        )
        return model_from_detailed(response)

    @api_method
    def bulk_upsert(
        self, body: RnaOligosBulkUpsertRequest, returning: Optional[Iterable[str]] = None
    ) -> TaskHelper[BulkUpdateRnaOligosAsyncTaskResponse]:
        """
        Bulk create or update RNA Oligos.

        See https://benchling.com/api/reference#/RNA%20Oligos/bulkUpsertRnaOligos
        """
        returning_string = optional_array_query_param(returning)
        response = bulk_upsert_rna_oligos.sync_detailed(
            client=self.client, json_body=body, returning=none_as_unset(returning_string)
        )
        return self._task_helper_from_response(response, BulkUpdateRnaOligosAsyncTaskResponse)
