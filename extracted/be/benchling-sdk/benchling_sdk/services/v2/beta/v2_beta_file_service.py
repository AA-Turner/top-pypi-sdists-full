from typing import List, Optional

from benchling_api_client.v2.beta.api.files import (
    create_file,
    get_file,
    list_files,
    patch_file,
)
from benchling_api_client.v2.beta.models.file import File
from benchling_api_client.v2.beta.models.file_create import FileCreate
from benchling_api_client.v2.beta.models.file_update import FileUpdate
from benchling_api_client.v2.beta.models.files_paginated_list import FilesPaginatedList
from benchling_api_client.v2.beta.models.list_files_sort import ListFilesSort
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaFileService(BaseService):
    """
    V2-Beta Files.

    Files are Benchling objects that represent files and their metadata. Compared to Blobs, which are used by
    most Benchling products for attachments, Files are primarily used in the Analysis and Connect product.

    See https://benchling.com/api/v2-beta/reference#/Files
    """

    @api_method
    def create(self, file: FileCreate) -> File:
        """
        Create a file.

        See https://benchling.com/api/v2-beta/reference#/Files/createFile
        """
        response = create_file.sync_detailed(client=self.client, json_body=file)
        return model_from_detailed(response)

    @api_method
    def get_by_id(self, file_id: str) -> File:
        """
        Get a file.

        See https://benchling.com/api/v2-beta/reference#/Files/getFile
        """
        response = get_file.sync_detailed(client=self.client, file_id=file_id)
        return model_from_detailed(response)

    @api_method
    def _files_page(
        self,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListFilesSort] = ListFilesSort.MODIFIEDAT,
        archive_reason: Optional[str] = None,
        created_at: Optional[str] = None,
        creator_ids: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        namesany_ofcase_sensitive: Optional[str] = None,
        namesany_of: Optional[str] = None,
        origin_ids: Optional[str] = None,
        ids: Optional[str] = None,
        display_ids: Optional[str] = None,
        returning: Optional[str] = None,
    ) -> Response[FilesPaginatedList]:
        response = list_files.sync_detailed(
            client=self.client,
            page_size=none_as_unset(page_size),
            next_token=none_as_unset(next_token),
            sort=none_as_unset(sort),
            archive_reason=none_as_unset(archive_reason),
            created_at=none_as_unset(created_at),
            creator_ids=none_as_unset(creator_ids),
            folder_id=none_as_unset(folder_id),
            mentioned_in=none_as_unset(mentioned_in),
            modified_at=none_as_unset(modified_at),
            name=none_as_unset(name),
            name_includes=none_as_unset(name_includes),
            namesany_ofcase_sensitive=none_as_unset(namesany_ofcase_sensitive),
            namesany_of=none_as_unset(namesany_of),
            origin_ids=none_as_unset(origin_ids),
            ids=none_as_unset(ids),
            display_ids=none_as_unset(display_ids),
            returning=none_as_unset(returning),
        )
        raise_for_status(response)
        return response  # type: ignore

    def list(
        self,
        *,
        page_size: Optional[int] = 50,
        sort: Optional[ListFilesSort] = ListFilesSort.MODIFIEDAT,
        archive_reason: Optional[str] = None,
        created_at: Optional[str] = None,
        creator_ids: Optional[str] = None,
        folder_id: Optional[str] = None,
        mentioned_in: Optional[str] = None,
        modified_at: Optional[str] = None,
        name: Optional[str] = None,
        name_includes: Optional[str] = None,
        namesany_ofcase_sensitive: Optional[str] = None,
        namesany_of: Optional[str] = None,
        origin_ids: Optional[str] = None,
        ids: Optional[str] = None,
        display_ids: Optional[str] = None,
        returning: Optional[str] = None,
    ) -> PageIterator[File]:
        """
        List Files.

        See https://benchling.com/api/v2-beta/reference#/Files/listFiles
        """

        def api_call(next_token: NextToken) -> Response[FilesPaginatedList]:
            return self._files_page(
                page_size=page_size,
                next_token=next_token,
                sort=sort,
                archive_reason=archive_reason,
                created_at=created_at,
                creator_ids=creator_ids,
                folder_id=folder_id,
                mentioned_in=mentioned_in,
                modified_at=modified_at,
                name=name,
                name_includes=name_includes,
                namesany_ofcase_sensitive=namesany_ofcase_sensitive,
                namesany_of=namesany_of,
                origin_ids=origin_ids,
                ids=ids,
                display_ids=display_ids,
                returning=returning,
            )

        def results_extractor(body: FilesPaginatedList) -> Optional[List[File]]:
            return body.files

        return PageIterator(api_call, results_extractor)

    @api_method
    def update(self, file_id: str, file: FileUpdate) -> File:
        """
        Update a File.

        See https://benchling.com/api/reference#/Files/updateFile
        """
        response = patch_file.sync_detailed(client=self.client, file_id=file_id, json_body=file)
        return model_from_detailed(response)
