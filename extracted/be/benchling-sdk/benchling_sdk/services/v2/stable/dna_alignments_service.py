from typing import List, Optional, Union

from benchling_api_client.v2.stable.api.dna_alignments import (
    create_dna_consensus_alignment,
    create_dna_template_alignment,
    delete_dna_alignment,
    get_dna_alignment,
    list_dna_alignments,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.logging_helpers import log_deprecation
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.models import (
    DnaAlignment,
    DnaAlignmentsPaginatedList,
    DnaAlignmentSummary,
    DnaConsensusAlignmentCreate,
    DnaTemplateAlignmentCreate,
    ListDNAAlignmentsSort,
)
from benchling_sdk.services.v2.base_service import BaseService


class DnaAlignmentsService(BaseService):
    """
    DNA Alignments (Deprecated).

    A DNA alignment is a Benchling object representing an alignment of multiple DNA sequences.

    Please migrate to the corresponding Nucleotide Alignment endpoints.

    See https://benchling.com/api/reference#/DNA%20Alignments
    See https://benchling.com/api/reference#/Nucleotide%20Alignments
    """

    @api_method
    def get_by_id(self, dna_alignment_id: str) -> DnaAlignment:
        """
        Get a DNA alignment (Deprecated).

        Please migrate to the corresponding Nucleotide Alignment endpoints.

        See https://benchling.com/api/reference#/DNA%20Alignments/getDNAAlignment
        See https://benchling.com/api/reference#/Nucleotide%20Alignments/getNucleotideAlignment
        """
        log_deprecation("dna_alignments.get_by_id", "nucleotide_alignments.get_by_id")
        response = get_dna_alignment.sync_detailed(client=self.client, dna_alignment_id=dna_alignment_id)
        return model_from_detailed(response)

    @api_method
    def _dna_alignments_page(
        self,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        ids: Optional[List[str]] = None,
        names_any_of: Optional[List[str]] = None,
        names_any_of_case_sensitive: Optional[List[str]] = None,
        sequence_ids: Optional[List[str]] = None,
        sort: Optional[ListDNAAlignmentsSort] = None,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
    ) -> Response[DnaAlignmentsPaginatedList]:
        response = list_dna_alignments.sync_detailed(
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
        sort: Optional[Union[str, ListDNAAlignmentsSort]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[DnaAlignmentSummary]:
        """
        List DNA Alignments (Deprecated).

        Please migrate to the corresponding Nucleotide Alignment endpoints.

        See https://benchling.com/api/reference#/DNA%20Alignments/listDNAAlignments
        See https://benchling.com/api/reference#/Nucleotide%20Alignments/listNucleotideAlignments
        """
        log_deprecation("dna_alignments.list", "nucleotide_alignments.list")

        def api_call(next_token: NextToken) -> Response[DnaAlignmentsPaginatedList]:
            return self._dna_alignments_page(
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                ids=ids,
                names_any_of=names_any_of,
                names_any_of_case_sensitive=names_any_of_case_sensitive,
                sequence_ids=sequence_ids,
                sort=_translate_to_string_enum(ListDNAAlignmentsSort, sort),
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(body: DnaAlignmentsPaginatedList) -> Optional[List[DnaAlignmentSummary]]:
            return body.dna_alignments

        return PageIterator(api_call, results_extractor)

    @api_method
    def create_template_alignment(
        self, template_alignment: DnaTemplateAlignmentCreate
    ) -> TaskHelper[DnaAlignment]:
        """
        Create a template DNA alignment (Deprecated).

        Please migrate to the corresponding Nucleotide Alignment endpoints.

        See https://benchling.com/api/reference#/DNA%20Alignments/createTemplateAlignment
        See https://benchling.com/api/reference#/Nucleotide%20Alignments/createTemplateNucleotideAlignment
        """
        log_deprecation(
            "dna_alignments.create_template_alignment", "nucleotide_alignments.create_template_alignment"
        )
        response = create_dna_template_alignment.sync_detailed(
            client=self.client, json_body=template_alignment
        )
        return self._task_helper_from_response(response, DnaAlignment)

    @api_method
    def create_consensus_alignment(
        self, consensus_alignment: DnaConsensusAlignmentCreate
    ) -> TaskHelper[DnaAlignment]:
        """
        Create a consensus DNA alignment (Deprecated).

        Please migrate to the corresponding Nucleotide Alignment endpoints.

        See https://benchling.com/api/reference#/DNA%20Alignments/createConsensusAlignment
        See https://benchling.com/api/reference#/Nucleotide%20Alignments/createConsensusNucleotideAlignment
        """
        log_deprecation(
            "dna_alignments.create_consensus_alignment", "nucleotide_alignments.create_consensus_alignment"
        )
        response = create_dna_consensus_alignment.sync_detailed(
            client=self.client, json_body=consensus_alignment
        )
        return self._task_helper_from_response(response, DnaAlignment)

    @api_method
    def delete_alignment(self, dna_alignment_id: str) -> None:
        """
        Delete a DNA alignment (Deprecated).

        Please migrate to the corresponding Nucleotide Alignment endpoints.

        See https://benchling.com/api/reference#/DNA%20Alignments/deleteDNAAlignment
        See https://benchling.com/api/reference#/Nucleotide%20Alignments/deleteNucleotideAlignment
        """
        log_deprecation("dna_alignments.delete_alignment", "nucleotide_alignments.delete_alignment")
        response = delete_dna_alignment.sync_detailed(client=self.client, dna_alignment_id=dna_alignment_id)
        raise_for_status(response)
