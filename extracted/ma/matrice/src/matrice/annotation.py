"""Module to handle annotation-related operations within a project."""

import sys
from matrice.utils import handle_response
from datetime import datetime


class Annotation:
    """
    Initialize an Annotation instance for managing annotation-related operations.

    This constructor sets up the `Annotation` instance using the provided session, and either
    the `annotation_id` or `annotation_name`. If only `annotation_name` is provided, the
    class attempts to retrieve the `annotation_id` based on the name. Similarly, if both
    `annotation_id` and `annotation_name` are given, the method checks for consistency.

    Parameters
    ----------
    session : Session
        The session object that manages the connection to the API.
    annotation_id : str, optional
        The unique identifier for the annotation (default is None).
    annotation_name : str, optional
        The name of the annotation to fetch if `annotation_id` is not provided (default is "").

    Raises
    ------
    ValueError
        If neither `annotation_id` nor `annotation_name` is provided, or if there is a mismatch between
        `annotation_id` and `annotation_name`.

    Attributes
    ----------
    project_id : str
        Identifier for the project to which the annotation belongs.
    annotation_id : str
        Identifier for the annotation, retrieved based on the provided `annotation_name` if not specified.
    annotation_name : str
        Name of the annotation.
    rpc : RPC
        The RPC interface from the session for communicating with the API.
    annotation_details : dict
        Detailed information about the annotation, retrieved during initialization.
    version_status : str
        The processing status of the latest annotation version.
    latest_version : str
        Identifier of the latest version of the annotation dataset.
    last_updated_at : str
        Timestamp indicating when the annotation was last updated.
    project_type : str
        The type of project associated with the annotation.

    Example
    -------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> annotation = Annotation(session, annotation_id="5678",annotation_name="annotation_name")
    >>> print(annotation.annotation_name)
    >>> print(annotation.version_status)
    """

    def __init__(
        self,
        session,
        annotation_id=None,
        annotation_name=None,
    ):
        self.session = session
        self.project_id = session.project_id
        self.annotation_id = annotation_id
        self.annotation_name = annotation_name
        self.rpc = session.rpc
        assert (
            annotation_id or annotation_name
        ), "Either annotation_id or annotation_name must be provided"
        annotation_by_name, err, msg = self._get_annotation_by_name()
        if self.annotation_id is None:
            if annotation_by_name is None:
                raise ValueError(f"Annotation with name '{self.annotation_name}' not found.")
            self.annotation_id = annotation_by_name["_id"]
        elif self.annotation_id is not None and self.annotation_name is not None:
            fetched_annotation_id = annotation_by_name["_id"]
            if fetched_annotation_id != self.annotation_id:
                raise ValueError(
                    "Provided annotation_id does not match the annotation id of the provided annotation_name."
                )
        (
            self.annotation_details,
            error,
            message,
        ) = self._get_details()
        print(self.annotation_details)
        self.version_status = self.annotation_details.get("status")
        self.latest_version = self.annotation_details.get("datasetVersion")
        self.last_updated_at = self.annotation_details.get("updatedAt")
        self.project_type = self.annotation_details.get("projectType")

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        init_params = {
            "session": self.session,
            "annotation_id": self.annotation_id,
        }
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def _get_details(self):
        """
        Retrieve detailed information for an annotation based on the provided annotation ID or name.

        This method attempts to fetch annotation details by `annotation_id` if available;
        if not, it uses `annotation_name`. If neither identifier is set, it raises a `ValueError`.
        Internally, it calls `_get_annotation_by_id()` or `_get_annotation_by_name()` to perform
        the actual retrieval.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict
                A dictionary containing important dataset information, including:
                - `_id` (str): Unique identifier for the annotation.
                - `status` (str): Processing status of the annotation.
                - `datasetVersion` (str): Dataset version associated with the annotation.
                - `updatedAt` (str): Last update timestamp for the annotation.
                - `projectType` (str): Type of project associated with the annotation.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        ValueError
            If neither `annotation_id` nor `annotation_name` is provided, raising an error due to
            lack of identifiers for the retrieval.

        Examples
        --------
        >>> annotation_details,err,msg = annotation._get_details()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(annotation_details)

        Notes
        -----
        - `_get_annotation_by_id()` is called if `annotation_id` is set, retrieving details by ID.
        - `_get_annotation_by_name()` is used if `annotation_name` is set, fetching details by name.
        """
        id = self.annotation_id
        name = self.annotation_name
        if id:
            try:
                return self._get_annotation_by_id()
            except Exception as e:
                print(f"Error retrieving annotation by id: {e}")
        elif name:
            try:
                return self._get_annotation_by_name()
            except Exception as e:
                print(f"Error retrieving annotation by name: {e}")
        else:
            raise ValueError(
                "At least one of 'annotation_id' or 'annotation_name' must be provided."
            )

    def _get_annotation_by_id(self):
        """
        Fetch details of a specific annotation by its ID.

        This method retrieves annotation details using the `annotation_id` set during initialization.
        It returns the raw response from the API along with status and error messages.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with detailed annotation information, including fields such as:
                - `_id` (str): Unique identifier for the annotation.
                - `datasetVersion` (str): Dataset version associated with the annotation.
                - `updatedAt` (str): Timestamp of the last update for the annotation.
                - `projectType` (str): Type of project associated with the annotation.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> annotation_details, err, msg = annotation._get_annotation_by_id()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(annotation_details)
        """
        path = f"/v1/annotations/{self.annotation_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Annotation fetched successfully",
            "Could not fetch annotation",
        )

    def _get_annotation_by_name(self):
        """
        Fetch details of a specific annotation by its name.

        This method retrieves annotation details using the `annotation_name` set during initialization.
        If `annotation_name` is not provided, the method will terminate execution.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response with detailed annotation information, including fields such as:
                - `_id` (str): Unique identifier for the annotation.
                - `datasetVersion` (str): Dataset version associated with the annotation.
                - `updatedAt` (str): Timestamp of the last update for the annotation.
                - `projectType` (str): Type of project associated with the annotation.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> annotation_details, err, msg = annotation._get_annotation_by_name()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(annotation_details)
        """
        if self.annotation_name == "":
            print(
                "Annotation name not set for this annotation. Cannot perform the operation for annotation without Annotation name"
            )
            sys.exit(0)
        path = f"/v1/annotations/get_annotation_by_name?annotationName={self.annotation_name}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Annotation by name fetched successfully",
            "Could not fetch annotation by name",
        )

    def rename(self, annotation_title):
        """
        Rename the annotation with the specified title. The annotation ID must be set in the class instance.

        Parameters
        ----------
        annotation_title : str
            The new title for the annotation.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the annotation title update.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.

        Example
        -------
        >>> from pprint import pprint
        >>> rename, err, msg = annotation.rename(annotation_title="New Title")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(rename)
        """
        if self.annotation_id is None:
            print(
                "Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id"
            )
            sys.exit(0)
        path = f"/v1/annotations/{self.annotation_id}"
        headers = {"Content-Type": "application/json"}
        body = {"title": annotation_title}
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

    def delete(self):
        """
        Delete the entire annotation task. The `annotation_id` and `project_id` must be set in the class instance.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the annotation deletion.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.

        Example
        -------
        >>> from pprint import pprint
        >>> delete, err, msg = annotation.delete()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete)
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the deletion for annotation without annotation id"
            )
            sys.exit(0)
        path = f"/v1/annotations/{self.annotation_id}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Annotation deleted successfully",
            "An error occured while deleting annotation",
        )

    def get_annotation_files(self, page_size=10, page_number=0):
        """
        Fetch the files associated with a specific annotation. The `annotation_id` and `project_id`
        must be set in the class instance.

        Parameters
        ----------
        page_size : int, optional
            Number of files to retrieve per page (default is 10).
        page_number : int, optional
            Page number to retrieve (default is 0).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with a list of files associated with the annotation.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> files, err, msg = annotation.get_annotation_files(page_size=10, page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(files)
        """
        path = f"/v1/annotations/{self.annotation_id}/files?projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Annotation files fetched successfully",
            "Could not fetch annotation files",
        )

    def get_item_history(self, annotation_item_id):
        """
        Fetch the annotation history for a specific item. The `annotation_id` and `project_id`
        must be set in the class instance.

        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item for which history is being fetched.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with the annotation history details.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> history, err, msg = annotation.get_annotation_history(annotation_item_id="12345")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(history)
        """
        path = f"/v1/annotations/{self.annotation_id}/{annotation_item_id}/annotation_history?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Annotation history fetched successfully",
            "Could not fetch annotation history",
        )

    def list_items(self, page_size=10, page_number=0):
        """
        Retrieve a paginated list of items associated with the annotation. The `annotation_id` and
        `project_id` must be set in the class instance.

        Parameters
        ----------
        page_size : int, optional
            The number of items to retrieve per page (default is 10).
        page_number : int, optional
            The page number to retrieve (default is 0).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with the annotation items.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.

        Example
        -------
        >>> from pprint import pprint
        >>> items, err, msg = annotation.list_items(page_size=10, page_number=0)
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(items)
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the operation for annotation without annotation id"
            )
            sys.exit(0)
        path = f"/v1/annotations/{self.annotation_id}/files?/v2/projectId={self.project_id}&pageSize={page_size}&pageNumber={page_number}"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Annotation items fetched successfully",
            "Could not fetch annotation items",
        )

    def update_classification_item(
        self,
        file_id,
        annotation_item_id,
        updated_classification_label,
        labeller,
        reviewer,
        status,
        issues,
        label_time,
        review_time,
    ):
        """
        Update annotation data for a specific file. The `annotation_id` and `project_id` must
        be set in the class instance.

        Parameters
        ----------
        file_id : str
            The ID of the file being annotated.
        annotation_item_id : str
            The ID of the annotation item.
        updated_classification_label : dict
            The updated classification label for the item, structured as:
                - `_idCategory` (str): The ID of the category.
                - `categoryName` (str): The name of the category.
        labeller : dict
            Information about the labeller, including:
                - `_idUser` (str): The user ID of the labeller.
                - `name` (str): Name of the labeller.
        reviewer : dict
            Information about the reviewer, including:
                - `_idUser` (str): The user ID of the reviewer.
                - `name` (str): Name of the reviewer.
        status : str
            The status of the annotation (e.g., "Completed").
        issues : str
            Any issues identified during the annotation process.
        label_time : int
            The time taken to label the item, in seconds.
        review_time : int
            The time taken to review the item, in seconds.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the update of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> update_resp, err, msg = annotation.update_classification_item(
        ...     file_id="file123", annotation_item_id="item456",
        ...     updated_classification_label={"_idCategory": "cat1", "categoryName": "Dog"},
        ...     labeller={"_idUser": "user123", "name": "John Doe"},
        ...     reviewer={"_idUser": "user456", "name": "Jane Doe"},
        ...     status="Completed", issues="", label_time=120, review_time=30
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(update_resp)
        """
        path = f"/v1/annotations/{self.annotation_id}/files/{file_id}/annotate?projectId={self.project_id}"
        payload = {
            "annotationId": self.annotation_id,
            "annotationItemId": annotation_item_id,
            "labeller": labeller,
            "reviewer": reviewer,
            "updatedClassificationLabel": updated_classification_label,
            "status": status,
            "issues": issues,
            "labelTime": label_time,
            "reviewTime": review_time,
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=payload,
        )
        return handle_response(
            resp,
            "Annotation updated successfully",
            "An error occured while updating annotation",
        )

    def get_categories(self):
        """
        Fetch categories for a specific annotation by its ID. The `annotation_id` must be set in
        the class instance.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response with details about the categories.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> categories, err, msg = annotation.get_categories()
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(categories)
        """
        path = f"/v1/annotations/{self.annotation_id}/categories"
        resp = self.rpc.get(path=path)
        return handle_response(
            resp,
            "Categories fetched successfully",
            "Could not fetch categories",
        )

    def annotate_classification_item(
        self,
        file_id,
        annotation_item_id,
        classification_label,
        labeller,
        reviewer,
        status,
        issues,
        label_time,
        review_time,
    ):
        """
        Add annotation data to a specific file. The `annotation_id` and `project_id`
        must be set in the class instance.

        Parameters
        ----------
        file_id : str
            The ID of the file being annotated.
        annotation_item_id : str
            The ID of the annotation item.
        classification_label : dict
            The classification label for the item, structured as:
                - `_idCategory` (str): The ID of the category.
                - `categoryName` (str): The name of the category.
        labeller : dict
            Information about the labeller, including:
                - `_idUser` (str): The user ID of the labeller.
                - `name` (str): Name of the labeller.
        reviewer : dict
            Information about the reviewer, including:
                - `_idUser` (str): The user ID of the reviewer.
                - `name` (str): Name of the reviewer.
        status : str
            The status of the annotation (e.g., "Completed").
        issues : str
            Any issues identified during the annotation process.
        label_time : int
            The time taken to label the item, in seconds.
        review_time : int
            The time taken to review the item, in seconds.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the addition of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> annotation_resp, err, msg = annotation.annotate_classification_item(
        ...     file_id="file123", annotation_item_id="item456",
        ...     classification_label={"_idCategory": "cat1", "categoryName": "Dog"},
        ...     labeller={"_idUser": "user123", "name": "John Doe"},
        ...     reviewer={"_idUser": "user456", "name": "Jane Doe"},
        ...     status="Completed", issues="", label_time=120, review_time=30
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(annotation_resp)
        """
        path = f"/v1/annotations/{self.annotation_id}/files/{file_id}/annotate?projectId={self.project_id}"
        payload = {
            "annotationId": self.annotation_id,
            "annotationItemId": annotation_item_id,
            "labeller": labeller,
            "reviewer": reviewer,
            "updatedClassificationLabel": classification_label,
            "status": status,
            "issues": issues,
            "labelTime": label_time,
            "reviewTime": review_time,
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        return handle_response(
            resp,
            "Annotation added successfully",
            "An error occured while adding annotation",
        )

    def create_dataset(
        self,
        is_create_new,
        old_dataset_version,
        new_dataset_version,
        new_version_description,
    ):
        """
        Create or update a dataset based on annotation data. The `annotation_id` and `project_id`
        must be set in the class instance.

        Parameters
        ----------
        is_create_new : bool
            Whether to create a new dataset version (`True`) or update an existing one (`False`).
        old_dataset_version : str
            The version identifier of the old dataset.
        new_dataset_version : str
            The version identifier of the new dataset.
        new_version_description : str
            The description for the new dataset version.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response confirming the creation or update of the dataset.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Example
        -------
        >>> from pprint import pprint
        >>> dataset_resp, err, msg = annotation.create_dataset(
        ...     is_create_new=True, old_dataset_version="v1.0",
        ...     new_dataset_version="v2.0", new_version_description="Updated Version"
        ... )
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(dataset_resp)
        """
        path = f"/v1/annotations/{self.annotation_id}/create_dataset?projectId={self.project_id}"
        payload = {
            "annotationId": self.annotation_id,
            "isCreateNew": is_create_new,
            "oldDatasetVersion": old_dataset_version,
            "newDatasetVersion": new_dataset_version,
            "newVersionDescription": new_version_description,
            "datasetDesc": "",
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )
        return handle_response(
            resp,
            "Annotation added successfully",
            "An error occured while adding annotation",
        )

    def add_label(self, labelname):
        """
        Adds a new label for the annotation. The `annotation_id` and `project_id`
        must be set in the class instance.

        Parameters
        ----------
        labelname : str
            The name of the new label.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the addition of the label, including:
                - `_id` (str): Unique identifier for the new label.
                - `name` (str): Name of the label.
                - `createdAt` (str): Timestamp when the label was created.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.

        Example
        -------
        >>> from pprint import pprint
        >>> label_resp, err, msg = annotation.add_label(labelname="Animal")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(label_resp)
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this annotation. Cannot download without annotation id"
            )
            sys.exit(0)
        body = {
            "_idAnnotation": self.annotation_id,
            "name": labelname,
        }
        headers = {"Content-Type": "application/json"}
        path = f"/v1/annotations/{self.annotation_id}/categories?projectId={self.project_id}"
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=body,
        )
        return handle_response(
            resp,
            "Category added successfully",
            "An error occured while adding Category",
        )

    def delete_item(self, annotation_item_id):
        """
        Delete a specific annotation item. The `annotation_id` and `project_id` must be set
        in the class instance.

        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict: The API response confirming the deletion of the annotation item.
            - str or None:
                Error message if an error occurred, `None` otherwise.
            - str:
                Status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the `annotation_id` is not set.

        Example
        -------
        >>> from pprint import pprint
        >>> delete_resp, err, msg = annotation.delete_item(annotation_item_id="item123")
        >>> if err:
        >>>     pprint(err)
        >>> else:
        >>>     pprint(delete_resp)
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the deletion for annotation without annotation id"
            )
            sys.exit(0)
        path = f"/v1/annotations/{self.annotation_id}/files/{annotation_item_id}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)
        return handle_response(
            resp,
            "Annotation Item deleted successfully",
            "An error occured while deleting annotation item",
        )
