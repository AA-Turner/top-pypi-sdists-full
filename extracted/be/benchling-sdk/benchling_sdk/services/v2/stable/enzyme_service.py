from typing import Iterable, Optional

from benchling_api_client.v2.stable.api.enzymes import list_enzymes
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import Enzyme, EnzymesPaginatedList, ListEnzymesSort
from benchling_sdk.services.v2.base_service import BaseService


class EnzymeService(BaseService):
    """
    Enzymes.

    Restriction enzymes are curated by Benchling for operations such as Digests and Codon Optimization.

    See https://benchling.com/api/reference#/Enzymes
    """

    @api_method
    def _list_page(
        self,
        sort: Optional[ListEnzymesSort] = None,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = [],
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
    ) -> Response[EnzymesPaginatedList]:
        response = list_enzymes.sync_detailed(
            client=self.client,
            ids=none_as_unset(optional_array_query_param(ids)),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            namesany_of=none_as_unset(optional_array_query_param(names_any_of)),
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
            sort=none_as_unset(sort),
        )
        return raise_for_status(response)

    def list(
        self,
        sort: Optional[ListEnzymesSort] = None,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[Enzyme]:
        """
        List enzymes.

        See https://benchling.com/api/reference#/Enzymes/listEnzymes
        """

        def api_call(next_token: NextToken) -> Response[EnzymesPaginatedList]:
            return self._list_page(
                sort=sort,
                ids=ids,
                name=name,
                name_includes=name_includes,
                names_any_of=names_any_of,
                page_size=page_size,
                next_token=next_token,
            )

        return PageIterator(api_call, lambda result: result.enzymes)
