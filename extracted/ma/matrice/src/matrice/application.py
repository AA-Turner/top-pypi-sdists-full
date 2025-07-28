"""Module to handle applications."""

from matrice.utils import handle_response


class Application:
    """
    A class for handling application operations using the backend API.

    Attributes
    ----------
    session : Session
        The session object used for API interactions.


    Examples
    --------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> application = Application(session)
    >>> response = application.delete_application(session, applicationID="664b5df23abcf1c331234561")
    """

    def __init__(self, session):
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    def create_application(self, name, projectID, coverImage, notebookLink, blogLink):
        """
        Create an application with the given parameters

        This function create an application

        Parameters
        ----------
        name : str
            The page you want to see. default = 0
        projectID : str
            The number of applications in each page. default = 10
        coverImage: str
            The
        notebookLink: str
            the
        blogLink: str
            the

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the status of the application.
            - str or None: Error message if an error occurred, `None` otherwise.
            - str: Status message indicating success or failure.
        """

        path = f"/v1/applications/"
        headers = {"Content-Type": "application/json"}
        payload = {
            "name": name,
            "_idProject": projectID,
            "accountNumber": self.account_number,
            "coverImage": coverImage,
            "notebookLink": notebookLink,
            "blogLink": blogLink,
        }

        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )

        return handle_response(
            resp,
            "Successfully created Application",
            f"Error creating applications: {resp}",
        )

    def delete_application(self, applicationID):
        """
        Delete an application by its ID

        In that function only Team member and user can delete that particular Application

        Parameters
        ----------
        applicationID : str

        Returns
        -------
        tuple
            A tuple containing:
            - dict: API response indicating the deletion status
            - str or None: Error message
            - str: Status message of success or failure
        """
        path = f"/v1/applications/{applicationID}"
        headers = {"Content-Type": "application/json"}

        resp = self.rpc.delete(path=path, headers=headers)

        return handle_response(
            resp,
            "Successfully deleted application",
            f"Error deleting application: {resp}",
        )

    def add_model_version(
        self, application_id, model_name, model_id, project_id, model_type, blog_link
    ):
        """
        Add a new model version to an existing application.

        Parameters
        ----------
        application_id : str
            The ID of the application to which the model belongs.
        model_name : str
            Name of the model version (e.g., "my_model_v2").
        cloud_path : str
            Cloud storage path (e.g., S3 URI) where the model file is located.
        model_key : str
            Logical key or type of the model
        model_family : str
            Family or framework the model belongs to

        Returns
        -------
        tuple
            - dict: The API response with model version details.
            - str or None: Error message if any, else None.
            - str: Status message.
        """
        path = f"/v1/applications/{application_id}/models"
        headers = {"Content-Type": "application/json"}
        payload = {
            "projectId": project_id,
            "modelId": model_id,
            "modelType": model_type,
            "modelName": model_name,
            "blogLink": blog_link,
        }

        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=payload,
        )

        return handle_response(
            resp, "Model Added Successfully", f"Error adding model version: {resp}"
        )

    def delete_model(self, model_id):
        """
        Delete a model by its ID.

        Only publishers or authorized team members can perform this action.

        Parameters
        ----------
        model_id : str
            The unique identifier of the model to be deleted.

        Returns
        -------
        tuple
            - dict: The API response indicating the deletion status.
            - str or None: Error message if any, else None.
            - str: Status message (e.g., "Model deleted successfully").
        """
        path = f"/v1/models/{model_id}"
        headers = {"Content-Type": "application/json"}

        resp = self.rpc.delete(path=path, headers=headers, session=self.session)

        return handle_response(
            resp, "Model deleted successfully", f"Error deleting model: {resp}"
        )
