from typing import Any, Dict, Iterable, List, Optional, Union

from benchling_api_client.v2.stable.api.rna_sequences import (
    archive_rna_sequences,
    auto_annotate_rna_sequences,
    autofill_rna_sequence_parts,
    autofill_rna_sequence_translations,
    bulk_create_rna_sequences,
    bulk_get_rna_sequences,
    bulk_update_rna_sequences,
    create_rna_sequence,
    get_rna_sequence,
    list_rna_sequences,
    match_bases_rna_sequences,
    search_rna_sequences,
    unarchive_rna_sequences,
    update_rna_sequence,
)
from benchling_api_client.v2.stable.models.autofill_rna_sequences import AutofillRnaSequences
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import (
    none_as_unset,
    optional_array_query_param,
    schema_fields_query_param,
)
from benchling_sdk.helpers.task_helpers import EmptyTaskResponse, TaskHelper
from benchling_sdk.models import (
    AutoAnnotateRnaSequences,
    BulkCreateRnaSequencesAsyncTaskResponse,
    BulkUpdateRnaSequencesAsyncTaskResponse,
    EntityArchiveReason,
    ListRNASequencesSort,
    MatchBasesRequest,
    RnaSequence,
    RnaSequenceBulkCreate,
    RnaSequenceBulkUpdate,
    RnaSequenceCreate,
    RnaSequencesArchivalChange,
    RnaSequencesArchive,
    RnaSequencesBulkCreateRequest,
    RnaSequencesBulkUpdateRequest,
    RnaSequencesPaginatedList,
    RnaSequencesUnarchive,
    RnaSequenceUpdate,
    SearchBasesRequest,
)
from benchling_sdk.services.v2.base_service import BaseService


class RnaSequenceService(BaseService):
    """
    RNA Sequences.

    Chains of linear, single stranded RNA that support most capabilities and attributes of DNA Sequences.

    See https://benchling.com/api/reference?stability=not-available#/RNA%20Sequences
    """

    @api_method
    def get_by_id(
        self,
        rna_sequence_id: str,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> RnaSequence:
        """
        Get a RNA sequence.

        See https://benchling.com/api/reference#/RNA%20Sequences/getRNASequence
        """
        returning_string = optional_array_query_param(returning)
        response = get_rna_sequence.sync_detailed(
            client=self.client,
            rna_sequence_id=rna_sequence_id,
            returning=none_as_unset(returning_string),
            custom_notation_id=none_as_unset(custom_notation_id),
        )
        return model_from_detailed(response)

    @api_method
    def _rna_sequences_page(
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
        sort: Optional[ListRNASequencesSort] = None,
        ids: Optional[Iterable[str]] = None,
        entity_registry_ids_any_of: Optional[Iterable[str]] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        names_any_of_case_sensitive: Optional[Iterable[str]] = None,
        creator_ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> Response[RnaSequencesPaginatedList]:
        response = list_rna_sequences.sync_detailed(
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
            schema_fields=none_as_unset(schema_fields_query_param(schema_fields)),
            entity_registry_idsany_of=none_as_unset(optional_array_query_param(entity_registry_ids_any_of)),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
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
        creator_ids: Optional[Iterable[str]] = None,
        schema_fields: Optional[Dict[str, Any]] = None,
        sort: Optional[Union[ListRNASequencesSort]] = None,
        page_size: Optional[int] = None,
        author_idsany_of: Optional[Iterable[str]] = None,
        returning: Optional[Iterable[str]] = None,
        custom_notation_id: Optional[str] = None,
    ) -> PageIterator[RnaSequence]:
        """
        List RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/listRNASequences
        """
        if sort:
            sort = ListRNASequencesSort(sort)

        def api_call(next_token: NextToken) -> Response[RnaSequencesPaginatedList]:
            return self._rna_sequences_page(
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
                creator_ids=creator_ids,
                schema_fields=schema_fields,
                sort=sort,
                page_size=page_size,
                next_token=next_token,
                author_idsany_of=author_idsany_of,
                returning=returning,
                custom_notation_id=custom_notation_id,
            )

        def results_extractor(body: RnaSequencesPaginatedList) -> Optional[List[RnaSequence]]:
            return body.rna_sequences

        return PageIterator(api_call, results_extractor)

    @api_method
    def create(self, rna_sequence: RnaSequenceCreate) -> RnaSequence:
        """
        Create a RNA sequence.

        See https://benchling.com/api/reference#/RNA%20Sequences/createRNASequence
        """
        response = create_rna_sequence.sync_detailed(client=self.client, json_body=rna_sequence)
        return model_from_detailed(response)

    @api_method
    def update(self, rna_sequence_id: str, rna_sequence: RnaSequenceUpdate) -> RnaSequence:
        """
        Update a RNA sequence.

        See https://benchling.com/api/reference#/RNA%20Sequences/updateRNASequence
        """
        response = update_rna_sequence.sync_detailed(
            client=self.client, rna_sequence_id=rna_sequence_id, json_body=rna_sequence
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self, rna_sequence_ids: Iterable[str], reason: EntityArchiveReason
    ) -> RnaSequencesArchivalChange:
        """
        Archive RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/archiveRNASequences
        """
        archive_request = RnaSequencesArchive(reason=reason, rna_sequence_ids=list(rna_sequence_ids))
        response = archive_rna_sequences.sync_detailed(client=self.client, json_body=archive_request)
        return model_from_detailed(response)

    @api_method
    def unarchive(self, rna_sequence_ids: Iterable[str]) -> RnaSequencesArchivalChange:
        """
        Unarchive RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/unarchiveRNASequences
        """
        unarchive_request = RnaSequencesUnarchive(rna_sequence_ids=list(rna_sequence_ids))
        response = unarchive_rna_sequences.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def bulk_get(
        self, rna_sequence_ids: Iterable[str], returning: Optional[Iterable[str]] = None
    ) -> Optional[List[RnaSequence]]:
        """
        Bulk get RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/bulkGetRNASequences
        """
        rna_sequence_id_string = ",".join(rna_sequence_ids)
        returning_string = optional_array_query_param(returning)
        response = bulk_get_rna_sequences.sync_detailed(
            client=self.client,
            rna_sequence_ids=rna_sequence_id_string,
            returning=none_as_unset(returning_string),
        )
        rna_sequences_results = model_from_detailed(response)
        return rna_sequences_results.rna_sequences

    @api_method
    def bulk_create(
        self, rna_sequences: Iterable[RnaSequenceBulkCreate]
    ) -> TaskHelper[BulkCreateRnaSequencesAsyncTaskResponse]:
        """
        Bulk create RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/bulkCreateRNASequences
        """
        body = RnaSequencesBulkCreateRequest(list(rna_sequences))
        response = bulk_create_rna_sequences.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkCreateRnaSequencesAsyncTaskResponse)

    @api_method
    def bulk_update(
        self, rna_sequences: Iterable[RnaSequenceBulkUpdate]
    ) -> TaskHelper[BulkUpdateRnaSequencesAsyncTaskResponse]:
        """
        Bulk update RNA sequences.

        See https://benchling.com/api/reference#/RNA%20Sequences/bulkUpdateRNASequences
        """
        body = RnaSequencesBulkUpdateRequest(list(rna_sequences))
        response = bulk_update_rna_sequences.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, BulkUpdateRnaSequencesAsyncTaskResponse)

    @api_method
    def autofill_parts(self, rna_sequence_ids: Iterable[str]) -> TaskHelper[EmptyTaskResponse]:
        """
        Autofill RNA sequence parts.

        See https://benchling.com/api/reference#/RNA%20Sequences/autofillRNASequenceParts
        """
        body = AutofillRnaSequences(rna_sequence_ids=list(rna_sequence_ids))
        response = autofill_rna_sequence_parts.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, EmptyTaskResponse)

    @api_method
    def autofill_translations(self, rna_sequence_ids: Iterable[str]) -> TaskHelper[EmptyTaskResponse]:
        """
        Autofill RNA sequence translations.

        See https://benchling.com/api/reference#/RNA%20Sequences/autofillRNASequenceTranslations
        """
        body = AutofillRnaSequences(rna_sequence_ids=list(rna_sequence_ids))
        response = autofill_rna_sequence_translations.sync_detailed(client=self.client, json_body=body)
        return self._task_helper_from_response(response, EmptyTaskResponse)

    @api_method
    def auto_annotate(self, auto_annotate: AutoAnnotateRnaSequences) -> TaskHelper[EmptyTaskResponse]:
        """
        Auto-annotate RNA sequences with matching features from specified Feature Libraries.

        See https://benchling.com/api/reference#/RNA%20Sequences/autoAnnotateRnaSequences
        """
        response = auto_annotate_rna_sequences.sync_detailed(client=self.client, json_body=auto_annotate)
        return self._task_helper_from_response(response, EmptyTaskResponse)

    @api_method
    def match_bases(self, match_bases_request: MatchBasesRequest) -> RnaSequencesPaginatedList:
        """
        Match bases.

        Returns RNA Sequences that exactly match the provided bases.

        See https://benchling.com/api/reference#/RNA%20Sequences/matchBasesRnaSequences
        """
        response = match_bases_rna_sequences.sync_detailed(
            client=self.client,
            json_body=match_bases_request,
        )
        return model_from_detailed(response)

    @api_method
    def search_bases(self, search_bases_request: SearchBasesRequest) -> RnaSequencesPaginatedList:
        """
        Search bases.

        Returns RNA Sequences that contain the provided bases.
        Search indexing is asynchronous, so results may be not be available immediately after creation.

        See https://benchling.com/api/reference#/RNA%20Sequences/searchRnaSequences
        """
        response = search_rna_sequences.sync_detailed(
            client=self.client,
            json_body=search_bases_request,
        )
        return model_from_detailed(response)
