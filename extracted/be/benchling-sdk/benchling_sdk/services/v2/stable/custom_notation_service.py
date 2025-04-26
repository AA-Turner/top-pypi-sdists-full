from typing import List, Optional

from benchling_api_client.v2.stable.api.custom_notations import list_custom_notations
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.models import CustomNotation, CustomNotationsPaginatedList
from benchling_sdk.services.v2.base_service import BaseService


class CustomNotationService(BaseService):
    """
    Custom Notations.

    Benchling allows users to configure their own fully-custom string representation formats for import/export
    of nucleotide sequences (including chemical modifications).

    See https://benchling.com/api/reference#/Custom%20Notations
    """

    @api_method
    def _custom_notations_page(
        self,
        *,
        page_size: Optional[int] = None,
        next_token: Optional[str] = None,
    ) -> Response[CustomNotationsPaginatedList]:
        response = list_custom_notations.sync_detailed(
            client=self.client,
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(self, *, page_size: Optional[int] = None) -> PageIterator[CustomNotation]:
        """
        List custom notations.

        List all available custom notations for specifying modified nucleotide sequences.

        See https://benchling.com/api/reference#/Custom%20Notations/listCustomNotations
        """

        def api_call(next_token: NextToken) -> Response[CustomNotationsPaginatedList]:
            return self._custom_notations_page(
                page_size=page_size,
                next_token=next_token,
            )

        def results_extractor(
            body: CustomNotationsPaginatedList,
        ) -> Optional[List[CustomNotation]]:
            return body.custom_notations

        return PageIterator(api_call, results_extractor)
