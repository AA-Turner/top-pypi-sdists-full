from typing import Iterable, List, Optional

from benchling_api_client.v2.beta.api.datasets import (
    archive_datasets as api_client_archive_datasets,
    create_dataset,
    get_dataset,
    list_datasets,
    unarchive_datasets,
    update_dataset,
)
from benchling_api_client.v2.beta.models.dataset import Dataset
from benchling_api_client.v2.beta.models.dataset_create import DatasetCreate
from benchling_api_client.v2.beta.models.dataset_update import DatasetUpdate
from benchling_api_client.v2.beta.models.datasets_archival_change import DatasetsArchivalChange
from benchling_api_client.v2.beta.models.datasets_archive import DatasetsArchive
from benchling_api_client.v2.beta.models.datasets_archive_reason import DatasetsArchiveReason
from benchling_api_client.v2.beta.models.datasets_paginated_list import DatasetsPaginatedList
from benchling_api_client.v2.beta.models.datasets_unarchive import DatasetsUnarchive
from benchling_api_client.v2.beta.models.list_datasets_sort import ListDatasetsSort
from benchling_api_client.v2.types import Response

from benchling_sdk.errors import raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.pagination_helpers import NextToken, PageIterator
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.serialization_helpers import none_as_unset
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaDatasetService(BaseService):
    """
    V2-Beta Datasets.

    Similar to Data frames, datasets in Benchling represent tabular data that is not schematized. Datasets are
    saved to folders within Benchling with additional metadata, making them accessible and searchable within
    Benchling. Each dataset actually contains a data frame, and a data frame is required to create a dataset.

    See https://benchling.com/api/v2-beta/reference#/Datasets
    """

    @api_method
    def get_by_id(self, dataset_id: str) -> Dataset:
        """
        Get a dataset.

        See https://benchling.com/api/v2-beta/reference#/Datasets/getDataset
        """
        response = get_dataset.sync_detailed(client=self.client, dataset_id=dataset_id)
        return model_from_detailed(response)

    @api_method
    def archive_datasets(
        self, dataset_ids: Iterable[str], reason: DatasetsArchiveReason
    ) -> DatasetsArchivalChange:
        """
        Archive Datasets.

        See https://benchling.com/api/reference#/Datasets/archiveDatasets
        """
        archive_request = DatasetsArchive(reason=reason, dataset_ids=list(dataset_ids))
        response = api_client_archive_datasets.sync_detailed(
            client=self.client,
            json_body=archive_request,
        )
        return model_from_detailed(response)

    @api_method
    def create(self, dataset: DatasetCreate) -> Dataset:
        """
        Create a dataset.

        See https://benchling.com/api/v2-beta/reference#/Datasets/createDataset
        """
        response = create_dataset.sync_detailed(client=self.client, json_body=dataset)
        return model_from_detailed(response)

    @api_method
    def _datasets_page(
        self,
        page_size: Optional[int] = 50,
        next_token: Optional[str] = None,
        sort: Optional[ListDatasetsSort] = ListDatasetsSort.MODIFIEDAT,
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
    ) -> Response[DatasetsPaginatedList]:
        response = list_datasets.sync_detailed(
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
        sort: Optional[ListDatasetsSort] = ListDatasetsSort.MODIFIEDAT,
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
    ) -> PageIterator[Dataset]:
        """
        List Datasets.

        See https://benchling.com/api/v2-beta/reference#/Datasets/listDatasets
        """

        def api_call(next_token: NextToken) -> Response[DatasetsPaginatedList]:
            return self._datasets_page(
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

        def results_extractor(body: DatasetsPaginatedList) -> Optional[List[Dataset]]:
            return body.datasets

        return PageIterator(api_call, results_extractor)

    @api_method
    def unarchive_datasets(self, dataset_ids: Iterable[str]) -> DatasetsArchivalChange:
        """
        Unarchive one or more Datasets.

        See https://benchling.com/api/reference#/Datasets/unarchiveDatasets
        """
        unarchive_request = DatasetsUnarchive(dataset_ids=list(dataset_ids))
        response = unarchive_datasets.sync_detailed(client=self.client, json_body=unarchive_request)
        return model_from_detailed(response)

    @api_method
    def update(self, dataset_id: str, dataset: DatasetUpdate) -> Dataset:
        """
        Update a Dataset.

        See https://benchling.com/api/reference#/Datasets/updateDataset
        """
        response = update_dataset.sync_detailed(client=self.client, dataset_id=dataset_id, json_body=dataset)
        return model_from_detailed(response)
