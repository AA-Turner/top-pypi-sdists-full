from typing import Optional

from anyscale._private.models.model_base import ListResponse
from anyscale._private.sdk import sdk_command_v2
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.llm.dataset._private import docs
from anyscale.llm.dataset._private.models import Dataset


@sdk_command_v2(
    doc_py_example=docs.GET_PY_EXAMPLE, arg_docstrings=docs.GET_PY_ARG_DOCSTRINGS,
)
def get(
    name: str, version: Optional[int] = None, project: Optional[str] = None
) -> Dataset:
    """Retrieves metadata about a dataset.

    :param name: Name of the dataset.
    :param version: Version of the dataset. If a negative integer is provided, the dataset returned is this many versions back of the latest version. Default: Latest version.
    :param project: Name of the Anyscale project that the dataset belongs to. If not provided, all projects will be searched.

    Example usage:
    ```python
    dataset = anyscale.llm.dataset.get("my_first_dataset")
    print(f"Dataset name: '{dataset.name}'")  # Dataset name: 'my_first_dataset'

    # Get the second latest version of the dataset
    prev_dataset = anyscale.llm.dataset.get("my_first_dataset", version=-1)
    ```

    Return:
        Dataset: The `Dataset` object.
    """
    _sdk = BaseSDK()
    dataset = _sdk.client.get_dataset(name, version, project)
    return dataset


@sdk_command_v2(
    doc_py_example=docs.UPLOAD_PY_EXAMPLE, arg_docstrings=docs.UPLOAD_PY_ARG_DOCSTRINGS,
)
def upload(
    dataset_file: str,
    name: str,
    *,
    description: Optional[str] = None,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
) -> Dataset:
    """Uploads a dataset, or a new version of a dataset, to your Anyscale cloud.

    :param dataset_file: Path to the dataset file to upload.
    :param name: Name of a new dataset, or an existing dataset, to upload a new version of.
    :param description: Description of the dataset version.
    :param cloud: Name of the Anyscale cloud to upload a new dataset to. If not provided, the default cloud will be used.
    :param project: Name of the Anyscale project to upload a new dataset to. If not provided, the default project of the cloud will be used.

    Example usage:
    ```python
    anyscale.llm.dataset.upload("path/to/my_first_dataset.jsonl", name="my_first_dataset")
    anyscale.llm.dataset.upload("my_dataset.jsonl", "second_dataset")
    anyscale.llm.dataset.upload("my_dataset2.jsonl", "second_dataset", description="added 3 lines")
    ```
    Return:
        Dataset: The `Dataset` object representing the uploaded dataset.

    NOTE:
    If you are uploading a new version, have run this from within an Anyscale workspace,
    and neither `cloud` nor `project` are provided, the cloud and project of the workspace will be used.
    """
    _sdk = BaseSDK()
    dataset = _sdk.client.upload_dataset(
        dataset_file, name, description, cloud, project,
    )
    return dataset


@sdk_command_v2(
    doc_py_example=docs.DOWNLOAD_PY_EXAMPLE,
    arg_docstrings=docs.DOWNLOAD_PY_ARG_DOCSTRINGS,
)
def download(
    name: str, version: Optional[int] = None, project: Optional[str] = None
) -> bytes:
    """Downloads a dataset from your Anyscale cloud.

    :param name: Name of the dataset to download.
    :param version: Version of the dataset to download. If a negative integer is provided, the dataset returned is this many versions back of the latest version. Default: Latest version.
    :param project: Name of the Anyscale project to download the dataset from. If not provided, all projects will be searched.

    Example usage:
    ```python
    dataset_contents: bytes = anyscale.llm.dataset.download("my_first_dataset.jsonl")
    jsonl_obj = [json.loads(line) for line in dataset_contents.decode().splitlines()]

    prev_dataset_contents = anyscale.llm.dataset.download("my_first_dataset.jsonl", version=-1)
    ```

    Returns:
        bytes: The contents of the dataset file.
    """
    _sdk = BaseSDK()
    dataset_bytes = _sdk.client.download_dataset(name, version, project)
    return dataset_bytes


@sdk_command_v2(
    doc_py_example=docs.LIST_PY_EXAMPLE, arg_docstrings=docs.LIST_PY_ARG_DOCSTRINGS
)
def list(  # noqa: A001
    *,
    # Pagination
    limit: Optional[int] = None,
    after: Optional[str] = None,  # Unique ID to start listing after
    # Filtering
    name_contains: Optional[str] = None,  # Substring in name, case insensitive
    cloud: Optional[str] = None,
    project: Optional[str] = None,
) -> ListResponse[Dataset]:
    """
    Lists datasets.

    :param limit: Maximum number of datasets to return. Default: 1000.
    :param after: ID of the dataset to start the listing from. If provided, the list will start from the dataset after this ID.
    :param name_contains: Filter datasets by name. If provided, only datasets with name containing this string will be returned.
    :param cloud: Name of the Anyscale cloud to search in. If not provided, all clouds will be searched.
    :param project: Name of the Anyscale project to search in. If not provided, all projects will be searched.

    Example usage:
    ```
    datasets = anyscale.llm.dataset.list(limit=10)
    for d in datasets:
        print(f"Dataset name: '{d.name}'")  # Prints 10 dataset names
    ```

    Returns:
        ListResponse[Dataset]: List of `Dataset` objects.
    """
    _sdk = BaseSDK()
    list_response = _sdk.client.list_datasets(
        limit=limit,
        after=after,
        name_contains=name_contains,
        cloud=cloud,
        project=project,
    )
    return list_response
