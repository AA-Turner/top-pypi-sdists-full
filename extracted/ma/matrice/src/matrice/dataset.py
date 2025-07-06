"""Module to handle dataset-related operations within a project."""

import os
import sys
import requests
from matrice.utils import handle_response
from datetime import datetime, timedelta


def get_dataset_size_in_mb_from_url(session, url, project_id):
    """
    Fetch the size of a dataset from the specified URL.

    This function sends a request to retrieve the dataset size, measured in megabytes,
    for a given project.

    Parameters
    ----------
    session : Session
        The active session used to communicate with the API.
    url : str
        The URL of the dataset to fetch the size for.
    project_id : str
        The ID of the project associated with the dataset.

    Returns
    -------
    tuple
        A tuple containing three elements:
        - dict: API response with dataset size information (e.g., size in MB).
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.

    Example
    -------
    >>> size_info, err, msg = get_dataset_size(session=session,
    url="https://example.com/dataset.zip", project_id="12345")
    >>> if err:
    >>>     print(f"Error: {err}")
    >>> else:
    >>>     print(f"Dataset size: {size_info.get('size', 'N/A')} MB")
    """
    path = f"/v1/dataset/get_dataset_size_in_mb_from_url?projectId={project_id}"
    requested_payload = {"datasetUrl": url}
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(
        path=path,
        headers=headers,
        payload=requested_payload,
    )
    return handle_response(
        resp,
        "Dataset size fetched successfully",
        "Could not fetch dataset size",
    )


def upload_file(session, file_path):
    """
    Upload a file to the dataset. Only ZIP files are supported.

    This function uploads a ZIP file to the dataset server for the specified session. It generates an upload URL,
    then uses it to transfer the file.

    Parameters
    ----------
    session : Session
        The active session used to communicate with the API.
    file_path : str
        The local path of the file to upload.

    Returns
    -------
    dict
        A dictionary containing:
        - `success` (bool): Indicates if the upload was successful.
        - `data` (str): URL of the uploaded file if successful, empty string otherwise.
        - `message` (str): A status message indicating success or detailing any error.

    Example
    -------
    >>> result = upload_file(session=session, file_path="path/to/data.zip")
    >>> if result['success']:
    >>>     print(f"File uploaded successfully: {result['data']}")
    >>> else:
    >>>     print(f"Error: {result['message']}")
    """
    file_name = os.path.basename(file_path)
    upload_url, error, message = _get_upload_path(session, file_name)
    if error is not None:
        return {
            "success": False,
            "data": "",
            "message": message,
        }
    with open(file_path, "rb") as file:
        response = requests.put(upload_url, data=file, timeout=30)
    if response.status_code == 200:
        return {
            "success": True,
            "data": upload_url.split("?")[0],
            "message": "File uploaded successfully",
        }
    else:
        return {
            "success": False,
            "data": "",
            "message": response.json().get("message", "Network Error"),
        }


def _get_upload_path(session, file_name):
    """
    Get the upload path for a specified file name.

    This function generates an API request to retrieve the URL for uploading a specific file.

    Parameters
    ----------
    session : Session
        The active session used to communicate with the API.
    file_name : str
        The name of the file for which the upload path is required.

    Returns
    -------
    tuple
        A tuple containing:
        - dict: API response with the upload URL.
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.

    Example
    -------
    >>> resp, err, msg = _get_upload_path(session=session, file_name="data.zip")
    >>> if err:
    >>>     print(f"Error: {err}")
    >>> else:
    >>>     print(f"Upload Path: {resp.get('upload_url', 'N/A')}")
    """
    path = f"/v1/dataset/upload-path?fileName={file_name}"
    resp = session.rpc.get(path=path)
    return handle_response(
        resp,
        "Upload Path fetched successfully",
        "Could not fetch upload path",
    )


class Dataset:
    """
    Class to handle dataset-related operations within a project.

    This class manages operations on a dataset within a specified project. During initialization,
    either `dataset_name` or `dataset_id` must be provided to locate the dataset.

    Parameters
    ----------
    session : Session
        The session object that manages the connection to the server.
    dataset_id : str, optional
        The ID of the dataset (default is None). Used to directly locate the dataset.
    dataset_name : str, optional
        The name of the dataset (default is None). If `dataset_id` is not provided,
        `dataset_name` will be used to find the dataset.

    Attributes
    ----------
    dataset_id : str
        The unique identifier for the dataset.
    dataset_name : str
        The name of the dataset.
    version_status : str
        The processing status of the latest dataset version.
    latest_version : str
        The identifier of the latest version of the dataset.
    no_of_samples : int
        The total number of samples in the dataset.
    no_of_classes : int
        The total number of classes in the dataset.
    no_of_versions : int
        The total number of versions for this dataset.
    last_updated_at : str
        The timestamp of the dataset's most recent update.
    summary : dict
        Summary of the dataset's latest version, providing metrics like item count and class
            distribution.

    Raises
    ------
    ValueError
        If neither `dataset_id` nor `dataset_name` is provided, or if there is a mismatch between
            `dataset_id` and `dataset_name`.

    Example
    -------
    >>> session = Session(account_number=account_number, access_key=access_key, secret_key=secret_key)
    >>> dataset = Dataset(session=session, dataset_id="12345",dataset_name="Sample")
    >>> print(f"Dataset Name: {dataset.dataset_name}")
    >>> print(f"Number of Samples: {dataset.no_of_samples}")
    >>> print(f"Latest Version: {dataset.latest_version}")
    """

    def __init__(
        self,
        session,
        dataset_id=None,
        dataset_name=None,
    ):
        self.session = session
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.rpc = session.rpc
        assert dataset_id or dataset_name, "Either dataset_id or dataset_name must be provided"
        if dataset_name is not None:
            dataset_by_name, err, msg = self._get_dataset_by_name()
            if self.dataset_id is None:
                if dataset_by_name is None:
                    raise ValueError(f"Dataset with name '{self.dataset_name}' not found.")
                self.dataset_id = dataset_by_name["_id"]
            elif self.dataset_id is not None and self.dataset_name is not None:
                fetched_dataset_id = dataset_by_name["_id"]
                if fetched_dataset_id != self.dataset_id:
                    raise ValueError(
                        "Provided dataset_id does not match the dataset id of the provided dataset_name."
                    )
        self.dataset_details, error, message = self._get_details()
        self.dataset_id = self.dataset_details["_id"]
        self.dataset_name = self.dataset_details["name"]
        self.version_status = self.dataset_details.get("stats", [{}])[0].get("versionStatus")
        self.latest_version = self.dataset_details["latestVersion"]
        self.no_of_samples = sum(
            version["versionStats"]["total"] for version in self.dataset_details.get("stats", [])
        )
        self.no_of_classes = len(self.dataset_details.get("stats", [{}])[0].get("classStat", {}))
        self.no_of_versions = len(self.dataset_details.get("allVersions", []))
        self.last_updated_at = self.dataset_details.get("updatedAt")

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        self.__dict__.copy()
        init_params = {
            "session": self.session,
            "dataset_id": self.dataset_id,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def _get_details(self):
        """
        Retrieve dataset details based on the dataset ID or dataset name set during class
            initialization.

        This method attempts to fetch the dataset details using the dataset ID, if available.
        If the dataset ID is not provided, it will attempt to retrieve details by the dataset name.
        If neither is available, a ValueError is raised.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict
                A dictionary containing important dataset information, including:
                    - `_id` (str): Unique identifier for the dataset.
                    - `_idAction` (str): Action identifier related to the dataset.
                    - `_idDatasetVersion` (str): Identifier for the dataset version.
                    - `_idProject` (str): Project ID associated with the dataset.
                    - `_idUser` (str): User ID associated with the dataset.
                    - `allVersions` (list of str): List of all dataset versions.
                    - `createdAt` (str): Timestamp when the dataset was created.
                    - `datasetDesc` (str): Description of the dataset.
                    - `latestVersion` (str): Identifier of the latest dataset version.
                    - `name` (str): Name of the dataset.
                    - `stats` (list of dict): Version-specific statistics, including sample counts
                        and splits.
                    - `type` (str): Type of dataset (e.g., `classification`, `detection`).
                    - `updatedAt` (str): Last update timestamp of the dataset.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        ValueError
            If neither `dataset_id` nor `dataset_name` is provided.

        Examples
        --------
        >>> dataset_details, err, msg = dataset._get_details()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(dataset_details)
        >>>
        >>> # Sample output
        >>> {
        >>>     '_id': '671636dd5cffa65a7510a52b',
        >>>     'name': 'MSCOCO',
        >>>     'allVersions': ['v1.0', 'v1.1'],
        >>>     'latestVersion': 'v1.1',
        >>>     ...
        >>> }

        Notes
        -----
        - `_get_dataset()` is called if `dataset_id` is set to retrieve the dataset by its ID.
        - `_get_dataset_by_name()` is used if `dataset_name` is set to fetch the dataset by its
            name.
        """
        id = self.dataset_id
        name = self.dataset_name
        if id:
            try:
                return self._get_dataset()
            except Exception as e:
                print(f"Error retrieving dataset by id: {e}")
        elif name:
            try:
                return self._get_dataset_by_name()
            except Exception as e:
                print(f"Error retrieving dataset by name: {e}")
        else:
            raise ValueError("At least one of 'dataset_id' or 'dataset_name' must be provided.")

    def _get_summary(self, dataset_version):
        """
        Retrieve a summary for a specific dataset version.

        This method provides essential metrics for a specified version of the dataset.
        Only the `dataset_version` is required, as `dataset_id` and `project_id` are already set
            during initialization.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to fetch the summary for (e.g., "v1.0").

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: Key summary details of the dataset, including:
                - `categoryCount` (int): The number of unique categories in the dataset.
                - `dataItemCount` (int): Total number of data items in the dataset.
                - `histogram` (list of dict): Distribution of items per category,
                with each dictionary containing:
                    - `_id` (str): Unique identifier for each category.
                    - `count` (int): Total count of items in this category.
                    - `label` (str): Name of the category.
                    - `train` (int): Number of items in the training set.
                    - `val` (int): Number of items in the validation set.
                    - `test` (int): Number of items in the test set.
                    - `unassigned` (int): Number of unassigned items.
                - `testDataItemCount` (int): Number of items in the test set.
                - `trainDataItemCount` (int): Number of items in the training set.
                - `valDataItemCount` (int): Number of items in the validation set.
                - `unassignedDataItemCount` (int): Number of unassigned items.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> summary, err, msg = dataset._get_summary(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(summary)
        >>>
        >>> # Sample output
        >>> {
        >>>     'categoryCount': 2,
        >>>     'dataItemCount': 2877,
        >>>     'histogram': [{'_id': '671638ef0f4507663b8ca2b7', 'count': 81524, 'label': 'Window',
        'train': 70643, 'val': 7302, 'test': 3579, 'unassigned': 0}],
        >>>     'testDataItemCount': 120,
        >>>     'trainDataItemCount': 2517,
        >>>     'unassignedDataItemCount': 0,
        >>>     'valDataItemCount': 240
        >>> }
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Dataset summary fetched successfully",
            "Could not fetch dataset summary",
        )

    def _get_dataset(self):
        """
        Fetch dataset details using the dataset ID.

        This function retrieves detailed information about the dataset by its ID. The dataset ID
            must be set during
        initialization for this function to work.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response with detailed dataset information, including:
                - `_id` (str): Unique identifier for the dataset.
                - `_idAction` (str): Action identifier related to the dataset.
                - `_idDatasetVersion` (str): Identifier for the dataset version.
                - `_idProject` (str): Project ID associated with the dataset.
                - `_idUser` (str): User ID associated with the dataset.
                - `allVersions` (list of str): List of all dataset versions.
                - `createdAt` (str): Timestamp when the dataset was created.
                - `datasetDesc` (str): Description of the dataset.
                - `latestVersion` (str): Identifier of the latest dataset version.
                - `name` (str): Name of the dataset.
                - `stats` (list of dict): Version-specific statistics, including sample counts and
                    splits.
                - `type` (str): Type of dataset (e.g., `classification`, `detection`).
                - `updatedAt` (str): Last update timestamp of the dataset.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> resp, err, msg = dataset._get_dataset()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(resp)
        >>>
        >>> # Sample output
        >>> {
        >>>     '_id': '671636dd5cffa65a7510a52b',
        >>>     'name': 'MSCOCO',
        >>>     'allVersions': ['v1.0', 'v1.1'],
        >>>     'latestVersion': 'v1.1',
        >>>     ...
        >>> }
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Dataset fetched successfully",
            "Could not fetch dataset",
        )

    def get_categories(self, dataset_version):
        """
        Get category details for a specific dataset version.

        This function retrieves the categories available in a specified version of the dataset,
        including category IDs, names, and associated metadata.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to fetch categories (e.g., "v1.0").

        Returns
        -------
        tuple
            A tuple containing:
            - list of dict: Each dictionary contains dataset category details, including:
                - `_id` (str): Unique identifier for the category.
                - `_idDataset` (str): ID of the dataset to which this category belongs.
                - `_idSuperCategory` (str): Identifier for the super-category, if applicable.
                - `datasetVersion` (str): Version of the dataset for this category.
                - `name` (str): Name of the category.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> categories, err, msg = dataset.get_categories(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(categories[:3])
        >>>
        >>> # Sample output
        >>> [
        >>>     {'_id': '671638ef0f4507663b8ca2b7', '_idDataset': '671636dd6cffa65a7510a52b',
        '_idSuperCategory': '000000000000000000000000', 'datasetVersion': 'v1.0', 'name': 'Dog'},
        >>>     {'_id': '671638ef0f4507663b8ca2b6', '_idDataset': '671636dd6cffa65a7510a52b',
        '_idSuperCategory': '000000000000000000000000', 'datasetVersion': 'v1.0', 'name': 'Cat'},
        >>>     ...
        >>> ]
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/categories?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            f"Dataset categories for version - {dataset_version} fetched successfully",
            "Could not fetch dataset categories",
        )

    def _list_items_V2(
        self,
        dataset_version,
        page_size=10,
        page_number=0,
    ):
        """
        List items for a specific version of the dataset.

        This function retrieves a paginated list of items for the specified dataset version,
        allowing control over the number of items per page and the page number.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to retrieve items from (e.g., "v1.0").
        page_size : int, optional
            The number of items to return per page (default is 10).
        page_number : int, optional
            The page number to retrieve (default is 0).

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response with a list of dataset items, where each item contains:
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> items, err, msg = dataset.list_items(dataset_version="v1.0", page_size=10,
        page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(items)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"v1/dataset/{self.dataset_id}/version/{dataset_version}/v2/item?Size={page_size}&pageNumber={page_number}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            f"Dataset items for version - {dataset_version} fetched successfully",
            "Could not fetch dataset items",
        )

    def list_items(
        self,
        dataset_version,
        page_size=10,
        page_number=0,
    ):
        """
        List items for a specific version of the dataset.

        This function retrieves a paginated list of items for the specified dataset version,
        allowing control over the number of items per page and the page number.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to retrieve items from (e.g., "v1.0").
        page_size : int, optional
            The number of items to return per page (default is 10).
        page_number : int, optional
            The page number to retrieve (default is 0).

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response with a list of dataset items, where each item contains:
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> items, err, msg = dataset.list_items(dataset_version="v1.0", page_size=10,
        page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(items)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"v1/dataset/{self.dataset_id}/version/{dataset_version}/v2/item?Size={page_size}&pageNumber={page_number}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            f"Dataset items for version - {dataset_version} fetched successfully",
            "Could not fetch dataset items",
        )

    def get_processed_versions(self):
        """
        Get all processed versions of the dataset.

        This function retrieves a list of all versions of the dataset that have completed
            processing.

        Returns
        -------
        tuple
            A tuple containing:
            - list of dict: Each dictionary contains processed dataset version details, including:
                - `_id` (str): Unique identifier for the dataset.
                - `_idProject` (str): Project ID associated with the dataset.
                - `allVersions` (list of str): List of all versions of the dataset.
                - `createdAt` (str): Timestamp of when the dataset was created.
                - `latestVersion` (str): Identifier of the latest version of the dataset.
                - `name` (str): Name of the dataset.
                - `processedVersions` (list of str): List of processed versions.
                - `stats` (list of dict): Version-specific statistics, including:
                    - `classStat` (dict): Contains category-specific counts for `test`, `train`,
                    `unassigned`, and `val`.
                    - `version` (str): Version identifier.
                    - `versionDescription` (str): Description of the version.
                    - `versionStats` (dict): Overall statistics, including `total`, `train`, `test`,
                    and `val` counts.
                    - `versionStatus` (str): Status of the version, usually "processed".
                - `updatedAt` (str): Timestamp of the last dataset update.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> processed_versions, err, msg = dataset.get_processed_versions()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(processed_versions[:3])
        >>>
        >>> # Sample output
        >>> [
        >>>     {'_id': '6703af894ddeac5b596b267b', '_idProject': '67036673ccb244bee86d1939',
        'allVersions': ['v1.0', 'v1.1'], 'createdAt': '2024-10-07T09:53:13.223Z',
        'name': 'Microcontroller', 'processedVersions': ['v1.1'], 'latestVersion': 'v1.1', ...},
        >>>     ...
        >>> ]
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/get_processed_versions?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Processed versions fetched successfully",
            "Could not fetch processed versions",
        )

    def check_valid_spilts(self, dataset_version):
        """
        Check if the specified dataset version contains valid splits.

        Valid splits include training, validation, and test sets. This function verifies that the
        specified dataset version has these splits properly configured.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to check for valid splits (e.g., "v1.0").

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating split validity, which includes:
                - `isValid` (str): Indicates if the splits are valid.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> split_status, err, msg = dataset.check_valid_splits(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(split_status)
        >>>
        >>> # Sample output
        >>>     'Valid Spilts'
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/check_valid_spilts/{self.dataset_id}/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Splits are valid",
            "Splits are invalid",
        )

    def _get_dataset_by_name(self):
        """
        Fetch dataset details using the dataset name.

        This function retrieves detailed information about the dataset by its name. The dataset name
        must be provided during initialization for this function to work.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response with dataset details, including:
                - `_id` (str): Unique identifier for the dataset.
                - `_idProject` (str): Project ID associated with the dataset.
                - `name` (str): Name of the dataset.
                - `type` (str): Type of dataset (e.g., `classification`, `detection`).
                - `createdAt` (str): Timestamp of when the dataset was created.
                - `updatedAt` (str): Last update timestamp of the dataset.
                - `latestVersion` (str): Identifier of the latest dataset version.
                - `allVersions` (list of str): List of all versions available for the dataset.
                - `description` (str): Brief description of the dataset.
                - `stats` (list of dict): Version-specific statistics and counts.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If `dataset_name` is not set.

        Example
        -------
        >>> dataset_details, err, msg = dataset._get_dataset_by_name()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(dataset_details)
        >>>
        >>> # Sample output
        >>> {
        >>>     '_id': '671636dd5cffa65a7510a52b',
        >>>     'name': 'Sample Dataset',
        >>>     'latestVersion': 'v1.2',
        >>>     'allVersions': ['v1.0', 'v1.1', 'v1.2'],
        >>>     ...
        >>> }
        """
        if self.dataset_name == "":
            print(
                "Dataset name not set for this dataset. Cannot perform the operation for dataset without dataset name"
            )
            sys.exit(0)
        path = f"/v1/dataset/get_dataset_by_name?datasetName={self.dataset_name}&projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Dataset Details Fetched successfully",
            "Could not fetch dataset details",
        )

    def rename(self, updated_name):
        """
        Update the name of the dataset.

        This function updates the dataset name to a specified value. The dataset ID must
        be set during initialization for this function to work.

        Parameters
        ----------
        updated_name : str
            The new name for the dataset.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the dataset name update, including:
                - `MatchedCount` (int): Number of records matched for the update.
                - `ModifiedCount` (int): Number of records modified.
                - `UpsertedCount` (int): Number of records upserted (inserted if not existing).
                - `UpsertedID` (str or None): ID of the upserted record if applicable,
                otherwise `None`.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset.rename(updated_name="Updated Dataset Name")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        >>>
        >>> # Sample output
        >>> {
        >>>     'MatchedCount': 1,
        >>>     'ModifiedCount': 1,
        >>>     'UpsertedCount': 0,
        >>>     'UpsertedID': None
        >>> }
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"name": updated_name}
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            f"Successfully updated dataset name to {updated_name}",
            "Could not update datename",
        )

    def update_item_label(self, dataset_version, item_id, label_id):
        """
        Update the label of a specific dataset item.

        This function assigns a new label to a specific item in a specified dataset version.
        The dataset ID must be set during initialization for this function to work.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset where the item resides (e.g., "v1.0").
        item_id : str
            The unique identifier of the dataset item to update.
        label_id : str
            The unique identifier of the new label to assign to the dataset item.

        Returns
        -------
        tuple
        A tuple containing:
        - dict: API response confirming the label update.
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset.update_item_label(dataset_version="v1.0", item_id="12345",
        label_id="67890")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/item/{item_id}/label?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"labelId": label_id}
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Update data item label in progress",
            "Could not update the date item label",
        )

    def add_data(
        self,
        source,
        source_url,
        new_dataset_version,
        old_dataset_version,
        dataset_description="",
        version_description="",
        compute_alias="",
    ):
        """
        Import a new version of the dataset from an external source. Only ZIP files are supported
            for upload.

        This function creates a new dataset version or updates an existing version with data from a
            specified
        external source URL. The dataset ID must be set during initialization for this function to
            work.

        Parameters
        ----------
        source : str
            The source of the dataset, indicating where the dataset originates (e.g., "url").
        source_url : str
            The URL of the dataset to be imported.
        new_dataset_version : str
            The version identifier for the new dataset (e.g., "v2.0").
        old_dataset_version : str
            The version identifier of the existing dataset to be updated.
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description for the new dataset version (default is an empty string).
        compute_alias : str, optional
            Alias for the compute instance to be used (default is an empty string).

        Returns
        -------
        tuple
        A tuple containing:
        - dict: API response indicating the status of the dataset import.
        - str or None: Error message if an error occurred, `None` otherwise.
        - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set or if the old dataset version is incomplete.

        Example
        -------
        >>> response, err, msg = dataset.add_data(
        >>>     source="url",
        >>>     source_url="https://example.com/dataset.zip",
        >>>     new_dataset_version="v2.0",
        >>>     old_dataset_version="v1.0"
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        dataset_resp, err, message = self._get_dataset()
        if err is not None:
            return dataset_resp, err, message
        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]
        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated. Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message
            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break
        is_created_new = new_dataset_version == old_dataset_version
        path = f"v1/dataset/{self.dataset_id}/import?project={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "source": source,
            "sourceUrl": source_url,
            "isCreateNew": is_created_new,
            "isUnlabeled": False,
            "newDatasetVersion": new_dataset_version,
            "oldDatasetVersion": old_dataset_version,
            "newVersionDescription": version_description,
            "datasetDesc": dataset_description,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "New data item addition in progress",
            "An error occured while trying to add new data item.",
        )

    def split_data(
        self,
        old_dataset_version,
        new_dataset_version,
        is_random_split,
        train_num=0,
        val_num=0,
        test_num=0,
        transfers=[
            {
                "source": "",
                "destination": "",
                "transferAmount": 1,
            }
        ],
        dataset_description="",
        version_description="",
        new_version_description="",
        compute_alias="",
    ):
        """
        Split or transfer images between training, validation, and test sets in the dataset.

        This function enables the creation of a new dataset version by transferring or splitting
            images from an existing
        version into training, validation, and test sets, with options for random or manual split
            distribution.

        Parameters
        ----------
        old_dataset_version : str
            The version identifier of the existing dataset.
        new_dataset_version : str
            The version identifier of the new dataset.
        is_random_split : bool
            Indicates whether to perform a random split.
        train_num : int, optional
            Number of training samples (default is 0).
        val_num : int, optional
            Number of validation samples (default is 0).
        test_num : int, optional
            Number of test samples (default is 0).
        transfers : list of dict, optional
            List specifying transfers between dataset sets. Each dictionary should contain:
                - `source` (str): The source set (e.g., "train").
                - `destination` (str): The target set (e.g., "test").
                - `transferAmount` (int): Number of items to transfer (default is 1).
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description of the dataset version (default is an empty string).
        new_version_description : str, optional
            Description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            Alias for the compute instance (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the status of the dataset split or transfer.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set or if the `old_dataset_version` is not processed.

        Example
        -------
        >>> response, err, msg = dataset.split_data(
        >>>     old_dataset_version="v1.0",
        >>>     new_dataset_version="v2.0",
        >>>     is_random_split=True,
        >>>     train_num=100,
        >>>     val_num=20,
        >>>     test_num=30,
        >>>     transfers=[{"source": "train", "destination": "test", "transferAmount": 100}]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        dataset_resp, err, message = self._get_dataset()
        if err is not None:
            return dataset_resp, err, message
        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]
        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated. Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message
            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break
        path = f"/v2/dataset/split_data/{self.dataset_id}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "trainNum": train_num,
            "testNum": test_num,
            "valNum": val_num,
            "unassignedNum": 0,
            "oldDatasetVersion": old_dataset_version,
            "newDatasetVersion": new_dataset_version,
            "isRandomSplit": is_random_split,
            "datasetDesc": dataset_description,
            "newVersionDescription": new_version_description,
            "transfers": transfers,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Dataset spliting in progress",
            "An error occured while trying to split the data.",
        )

    def delete_item(self, dataset_version, dataset_item_ids):
        """
        Delete items from a specific version of the dataset based on dataset type.

        This function deletes items from a specified version of the dataset. The deletion method is
            selected
        automatically based on the dataset type (e.g., classification, detection)
        . The dataset ID must be set
        during initialization for this function to work.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list of str
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        ValueError
            If the dataset type is unsupported.

        Example
        -------
        >>> response, err, msg = dataset.delete_item(
        >>>     dataset_version="v1.0", dataset_item_ids=["123", "456"]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        resp, error, message = self._get_details()
        if error:
            return resp, error, message
        dataset_type = resp.get("type")
        if dataset_type == "classification":
            return self._delete_item_classification(
                dataset_version,
                dataset_item_ids,
            )
        elif dataset_type == "detection":
            return self._delete_item_detection(dataset_version, dataset_item_ids)
        else:
            return (
                {},
                f"Unsupported dataset type: {dataset_type}.",
                "Failed to delete dataset items",
            )

    def _delete_item_classification(self, dataset_version, dataset_item_ids):
        """
        Delete items from a classification dataset version.

        This function deletes specific items from a given version of a classification dataset.
        The dataset ID must be set during initialization for this function to work.

        Parameters
        ----------
        dataset_version : str
            The version of the classification dataset from which to delete items.
        dataset_item_ids : list of str
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset._delete_item_classification(
        >>>     dataset_version="v1.0", dataset_item_ids=["123", "456"]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/version/{dataset_version}/dataset_item_classification?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(
            path=path,
            headers=headers,
            payload=requested_payload,
        )
        return handle_response(
            resp,
            "Given dataset items deleted successfully",
            "Could not delete the given dataset items",
        )

    def _delete_item_detection(self, dataset_version, dataset_item_ids):
        """
        Delete items from a detection dataset version.

        This function deletes specified items from a given version of a detection dataset.
        The dataset ID must be set during initialization for this function to work.

        Parameters
        ----------
        dataset_version : str
            The version of the detection dataset from which to delete items.
        dataset_item_ids : list of str
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset._delete_item_detection(
        >>>     dataset_version="v1.0", dataset_item_ids=["123", "456"]
        >>> )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/version/{dataset_version}/dataset_item_detection?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(
            path=path,
            headers=headers,
            payload=requested_payload,
        )
        return handle_response(
            resp,
            "Given dataset items deleted successfully",
            "Could not delete the given dataset items",
        )

    def delete_version(self, dataset_version):
        """
        Delete a specific version of the dataset.

        This function removes a specified version of the dataset. The dataset ID must be set
        during initialization for this function to work.

        Parameters
        ----------
        dataset_version : str
            The version identifier of the dataset to delete (e.g., "v1.0").

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset.delete_version(dataset_version="v1.0")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = (
            f"/v1/dataset/{self.dataset_id}/version/{dataset_version}?projectId={self.project_id}"
        )
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            f"Successfully deleted version - {dataset_version}",
            "Could not delete the said version",
        )

    def delete(self):
        """
        Delete the entire dataset.

        This function deletes the entire dataset associated with the given dataset ID. The dataset
            ID
        must be set during initialization for this function to work.

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response confirming the dataset deletion status.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `dataset_id` is not set.

        Example
        -------
        >>> response, err, msg = dataset.delete()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(response)
        """
        if self.dataset_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Successfully deleted the dataset",
            "Could not delete the dataset",
        )
