from typing import Iterable, Optional

from benchling_api_client.v2.stable.api.monomers import (
    archive_monomers,
    create_monomer,
    list_monomers,
    unarchive_monomers,
    update_monomer,
)
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.models import (
    Monomer,
    MonomerCreate,
    MonomersArchivalChange,
    MonomersArchive,
    MonomersArchiveReason,
    MonomersPaginatedList,
    MonomersUnarchive,
    MonomerUpdate,
)
from benchling_sdk.services.v2.base_service import BaseService


class MonomerService(BaseService):
    """
    Monomers.

    Monomers are chemical building blocks with specified structures used to compose modified
    nucleotides. Note that monomer write endpoints require tenant admin permissions.

    See https://benchling.com/api/reference#/Monomers
    """

    @api_method
    def _list_page(
        self,
        page_size: Optional[int] = None,
        next_token: Optional[NextToken] = None,
        returning: Optional[Iterable[str]] = None,
    ) -> Response[MonomersPaginatedList]:
        response = list_monomers.sync_detailed(
            client=self.client,
            next_token=none_as_unset(next_token),
            page_size=none_as_unset(page_size),
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return raise_for_status(response)

    def list(
        self,
        page_size: Optional[int] = None,
        returning: Optional[Iterable[str]] = None,
    ) -> PageIterator[Monomer]:
        """
        List monomers.

        See https://benchling.com/api/reference#/Monomers/listMonomers
        """

        def api_call(next_token: NextToken) -> Response[MonomersPaginatedList]:
            return self._list_page(
                page_size=page_size,
                next_token=next_token,
                returning=returning,
            )

        return PageIterator(api_call, lambda result: result.monomers)

    @api_method
    def create(
        self,
        monomer: MonomerCreate,
        returning: Optional[Iterable[str]] = None,
    ) -> Monomer:
        """
        Create a monomer.

        See https://benchling.com/api/reference#/Monomers/createMonomer
        """
        response = create_monomer.sync_detailed(
            client=self.client,
            json_body=monomer,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)

    @api_method
    def update(
        self,
        monomer_id: str,
        monomer: MonomerUpdate,
        returning: Optional[Iterable[str]] = None,
    ) -> Monomer:
        """
        Update a Monomer.

        See https://benchling.com/api/reference#/Monomers/updateMonomer
        """
        response = update_monomer.sync_detailed(
            client=self.client,
            monomer_id=monomer_id,
            json_body=monomer,
            returning=none_as_unset(optional_array_query_param(returning)),
        )
        return model_from_detailed(response)

    @api_method
    def archive(
        self,
        monomer_ids: Iterable[str],
        reason: MonomersArchiveReason,
    ) -> MonomersArchivalChange:
        """
        Archive Monomers.

        See https://benchling.com/api/reference#/Monomers/archiveMonomers
        """
        response = archive_monomers.sync_detailed(
            client=self.client,
            json_body=MonomersArchive(monomer_ids=list(monomer_ids), reason=reason),
        )
        return model_from_detailed(response)

    @api_method
    def unarchive(
        self,
        monomer_ids: Iterable[str],
    ) -> MonomersArchivalChange:
        """
        Unarchive Monomers.

        See https://benchling.com/api/reference#/Monomers/unarchiveMonomers
        """
        response = unarchive_monomers.sync_detailed(
            client=self.client,
            json_body=MonomersUnarchive(monomer_ids=list(monomer_ids)),
        )
        return model_from_detailed(response)
