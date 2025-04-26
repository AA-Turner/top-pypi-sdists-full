from typing import List, Optional

from benchling_api_client.v2.beta.api.folders import list_folder_collaborations
from benchling_api_client.v2.beta.models.collaboration import Collaboration
from benchling_api_client.v2.beta.models.collaborations_paginated_list import CollaborationsPaginatedList
from benchling_api_client.v2.beta.models.list_folder_collaborations_role import ListFolderCollaborationsRole
from benchling_api_client.v2.beta.models.list_folder_collaborations_sort import ListFolderCollaborationsSort
from benchling_api_client.v2.beta.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.constants import _translate_to_string_enum
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.serialization_helpers import none_as_unset, optional_array_query_param
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaFolderService(BaseService):
    """
    V2-Beta Folders.

    Folders are nested within projects to provide additional organization.

    See https://benchling.com/api/v2-beta/reference?showLa=true#/Folders
    """

    @api_method
    def _list_folder_collaborations_page(
        self,
        folder_id: str,
        user_id: Optional[str] = None,
        app_id: Optional[str] = None,
        team_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        role: Optional[ListFolderCollaborationsRole] = None,
        ids: Optional[str] = None,
        modified_atlt: Optional[str] = None,
        modified_atgt: Optional[str] = None,
        modified_atlte: Optional[str] = None,
        modified_atgte: Optional[str] = None,
        created_atlt: Optional[str] = None,
        created_atgt: Optional[str] = None,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListFolderCollaborationsSort] = None,
    ) -> Response[CollaborationsPaginatedList]:
        response = list_folder_collaborations.sync_detailed(
            client=self.client,
            folder_id=folder_id,
            user_id=none_as_unset(user_id),
            app_id=none_as_unset(app_id),
            team_id=none_as_unset(team_id),
            organization_id=none_as_unset(organization_id),
            role=none_as_unset(role),
            ids=none_as_unset(optional_array_query_param(ids)),
            modified_atlt=none_as_unset(modified_atlt),
            modified_atlte=none_as_unset(modified_atlte),
            modified_atgt=none_as_unset(modified_atgt),
            modified_atgte=none_as_unset(modified_atgte),
            created_atlt=none_as_unset(created_atlt),
            created_atgt=none_as_unset(created_atgt),
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            sort=none_as_unset(sort),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list_collaborations(
        self,
        *,
        folder_id: str,
        user_id: Optional[str] = None,
        app_id: Optional[str] = None,
        team_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        role: Optional[ListFolderCollaborationsRole] = None,
        ids: Optional[str] = None,
        modified_atlt: Optional[str] = None,
        modified_atgt: Optional[str] = None,
        modified_atlte: Optional[str] = None,
        modified_atgte: Optional[str] = None,
        created_atlt: Optional[str] = None,
        created_atgt: Optional[str] = None,
        page_size: Optional[int] = 50,
        sort: Optional[ListFolderCollaborationsSort] = None,
    ) -> PageIterator[Collaboration]:
        """
        List information about collaborations on the specified folder.

        See https://benchling.com/api/v2-beta/reference#/Folders/listFolderCollaborations
        """

        def api_call(next_token: NextToken) -> Response[CollaborationsPaginatedList]:
            return self._list_folder_collaborations_page(
                folder_id=folder_id,
                user_id=user_id,
                app_id=app_id,
                team_id=team_id,
                organization_id=organization_id,
                role=role,
                ids=ids,
                modified_atlt=modified_atlt,
                modified_atgt=modified_atgt,
                modified_atlte=modified_atlte,
                modified_atgte=modified_atgte,
                created_atlt=created_atlt,
                created_atgt=created_atgt,
                page_size=page_size,
                sort=_translate_to_string_enum(ListFolderCollaborationsSort, sort),
                next_token=next_token,
            )

        def results_extractor(body: CollaborationsPaginatedList) -> Optional[List[Collaboration]]:
            return body.collaborations

        return PageIterator(api_call, results_extractor)
