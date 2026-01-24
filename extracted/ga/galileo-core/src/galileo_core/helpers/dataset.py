from functools import partial
from typing import Dict, List, Optional
from uuid import UUID

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.helpers.pagination import paginated_request
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.dataset import Dataset, UploadDatasetRequest
from galileo_core.utils.dataset import DatasetType


def create_dataset(dataset: DatasetType, config: Optional[GalileoConfig] = None) -> Dataset:
    """
    Create a dataset.

    Parameters
    ----------
    dataset : DatasetType
        A dataset file path, dictionary, or list of dictionaries.

    Returns
    -------
    Dataset
        Response object for the created dataset.
    """
    config = config or GalileoConfig.get()
    request = UploadDatasetRequest(file_path=dataset)
    logger.debug(f"Creating dataset from {request.file_path}...")
    content_headers = {
        "Accept": "application/json",
    }

    response_dict = config.api_client.request(
        RequestMethod.POST,
        Routes.datasets,
        content_headers=content_headers,
        params=request.params,
        files=request.files,
    )
    dataset_response = Dataset.model_validate(response_dict)
    logger.debug(f"Created dataset with name {dataset_response.name}, ID {dataset_response.id}.")
    return dataset_response


def list_datasets(config: Optional[GalileoConfig] = None) -> List[Dataset]:
    """
    List all datasets for the user.

    Returns
    -------
    List[Dataset]
        List of all datasets.
    """
    config = config or GalileoConfig.get()
    logger.debug("Listing datasets...")
    all_datasets = paginated_request(partial(config.api_client.request, RequestMethod.GET, Routes.datasets), "datasets")
    datasets = [Dataset.model_validate(dataset) for dataset in all_datasets]
    logger.debug(f"Listed all datasets, found {len(datasets)} datasets.")
    return datasets


def get_dataset_content(dataset_id: UUID, config: Optional[GalileoConfig] = None) -> List[Dict]:
    """
    Get the content of a dataset.

    Returns
    -------
    List[Dict]
        The content of the dataset as a list of dictionaries.
        Each dictionary represents a row in the dataset, with an index and a list of values.
        For example (for a dataset with 2 columns):
        [
            {"index": 0, "values": ["value1", "value2"]},
            {"index": 1, "values": ["value3", "value4"]},
            ...
        ]
    """
    config = config or GalileoConfig.get()
    logger.debug("Getting dataset content...")
    all_rows = paginated_request(
        partial(config.api_client.request, RequestMethod.GET, Routes.dataset_content.format(dataset_id=dataset_id)),
        "rows",
    )
    logger.debug("Got dataset content.")
    return all_rows
