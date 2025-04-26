from typing import Iterable, Optional

from benchling_api_client.v2.stable.api.codon_usage_tables import list_codon_usage_tables
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import CodonUsageTable, CodonUsageTablesPaginatedList, ListCodonUsageTablesSort
from benchling_sdk.services.v2.base_service import BaseService


class CodonUsageTableService(BaseService):
    """
    Codon Usage Tables.

    Benchling curates codon usage data for a variety of organisms to support operations such as Codon
    Optimization and Back Translation.

    See https://benchling.com/api/reference#/Codon%20Usage%20Tables
    """

    @api_method
    def _list_page(
        self,
        sort: Optional[ListCodonUsageTablesSort] = None,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = [],
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
    ) -> Response[CodonUsageTablesPaginatedList]:
        response = list_codon_usage_tables.sync_detailed(
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
        sort: Optional[ListCodonUsageTablesSort] = None,
        ids: Optional[Iterable[str]] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        names_any_of: Optional[Iterable[str]] = None,
        page_size: Optional[int] = None,
    ) -> PageIterator[CodonUsageTable]:
        """
        List codon usage tables.

        See https://benchling.com/api/reference#/Codon%20Usage%20Tables/listCodonUsageTables
        """

        def api_call(next_token: NextToken) -> Response[CodonUsageTablesPaginatedList]:
            return self._list_page(
                sort=sort,
                ids=ids,
                name=name,
                name_includes=name_includes,
                names_any_of=names_any_of,
                page_size=page_size,
                next_token=next_token,
            )

        return PageIterator(api_call, lambda result: result.codon_usage_tables)
