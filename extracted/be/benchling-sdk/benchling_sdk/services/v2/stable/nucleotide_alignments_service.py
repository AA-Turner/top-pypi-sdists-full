from typing import List, Optional, Union

from benchling_api_client.v2.stable.api.nucleotide_alignments import (
    create_consensus_nucleotide_alignment,
    create_template_nucleotide_alignment,
    delete_nucleotide_alignment,
    get_nucleotide_alignment,
    list_nucleotide_alignments,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import (
    ListNucleotideAlignmentsSort,
    NucleotideAlignment,
    NucleotideAlignmentsPaginatedList,
    NucleotideAlignmentSummary,
    NucleotideConsensusAlignmentCreate,
    NucleotideTemplateAlignmentCreate,
)
from benchling_sdk.services.v2.base_service import BaseService


class NucleotideAlignmentsService(BaseService):
    """
    Nucleotide Alignments.

    A Nucleotide Alignment is a Benchling object representing an alignment of multiple DNA and/or RNA sequences.

    See https://benchling.com/api/reference#/Nucleotide%20Alignments
    """

    @api_method
    def get_by_id(self, alignment_id: str) -> NucleotideAlignment:
        """
        Get a Nucleotide Alignment.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments/getNucleotideAlignment
        """
        response = get_nucleotide_alignment.sync_detailed(client=self.client, alignment_id=alignment_id)
        return model_from_detailed(response)

    @api_method
    def _nucleotide_alignments_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ids: Optional[List[str]] = None,
        names_any_of: Optional[List[str]] = None,
        names_any_of_case_sensitive: Optional[List[str]] = None,
        sequence_ids: Optional[List[str]] = None,
        sort: Optional[ListNucleotideAlignmentsSort] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
    ) -> Response[NucleotideAlignmentsPaginatedList]:
        response = list_nucleotide_alignments.sync_detailed(
            client=self.client,
            modified_at=none_as_unset(modified_at),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            ids=none_as_unset(optional_array_query_param(ids)),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            namesany_ofcase_sensitive=none_as_unset(optional_array_query_param(names_any_of_case_sensitive)),
            sequence_ids=none_as_unset(optional_array_query_param(sequence_ids)),
            sort=none_as_unset(sort),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ids: Optional[List[str]] = None,
        names_any_of: Optional[List[str]] = None,
        names_any_of_case_sensitive: Optional[List[str]] = None,
        sequence_ids: Optional[List[str]] = None,
        sort: Optional[Union[str, ListNucleotideAlignmentsSort]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[NucleotideAlignmentSummary]:
        """
        List Nucleotide Alignments.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments/listNucleotideAlignments
        """

        def api_call(next_token: NextToken) -> Response[NucleotideAlignmentsPaginatedList]:
            return self._nucleotide_alignments_page(
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                ids=ids,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                sequence_ids=sequence_ids,
                sort=_translate_to_string_enum(ListNucleotideAlignmentsSort, sort),
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(
            body: NucleotideAlignmentsPaginatedList,
        ) -> Optional[List[NucleotideAlignmentSummary]]:
            return body.alignments

        return PageIterator(api_call, results_extractor)

    @api_method
    def create_template_alignment(
        self, template_alignment: NucleotideTemplateAlignmentCreate
    ) -> TaskHelper[NucleotideAlignment]:
        """
        Create a template Nucleotide alignment.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments/createTemplateNucleotideAlignment
        """
        response = create_template_nucleotide_alignment.sync_detailed(
            client=self.client, json_body=template_alignment
        )
        return self._task_helper_from_response(response, NucleotideAlignment)

    @api_method
    def create_consensus_alignment(
        self, consensus_alignment: NucleotideConsensusAlignmentCreate
    ) -> TaskHelper[NucleotideAlignment]:
        """
        Create a consensus Nucleotide alignment.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments/createConsensusNucleotideAlignment
        """
        response = create_consensus_nucleotide_alignment.sync_detailed(
            client=self.client, json_body=consensus_alignment
        )
        return self._task_helper_from_response(response, NucleotideAlignment)

    @api_method
    def delete_alignment(self, alignment_id: str) -> None:
        """
        Delete a Nucleotide alignment.

        See https://benchling.com/api/reference#/Nucleotide%20Alignments/deleteNucleotideAlignment
        """
        response = delete_nucleotide_alignment.sync_detailed(client=self.client, alignment_id=alignment_id)
        raise_for_status(response)
