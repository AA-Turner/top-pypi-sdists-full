"""Module to handle applications store."""

from matrice.utils import handle_response

class AppStore:
    """
    A class handling to App store operations using backend API.

    Attributes
    ----------

    session : Session
        The session object used for API interactions
    
        Examples
    --------
    >>> session = Session(account_number="account_number", access_key="access_key", secret_key="secret_key")
    >>> application = Application(session)
    >>> application_by_page = application.get_all_applications_public(page=1, limit=10)
    """
    def __init__(self, session):
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    def get_all_applications(self, page = 0, limit = 10):
        """
        Get all the applications on the platform

        This function returns all the applications details that are present on the platform

        Parameters
        ----------
        page : str
            The page you want to see. default = 0
        limit : str
            The number of applications in each page. default = 10

        Returns
        -------
        dict - 
            Dictonary of the applications with the given page number
        """

        path = f"/v1/public/applications?page={page}&limit={limit}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.get(
            path=path,
        )

        return handle_response(
            resp,
            "Successfully created Application",
            f"Error creating applications: {resp}"
        )
    
    def get_public_application_by_id(self, application_id):
        """
        Retrieve a specific public application by its ID.

        This endpoint fetches detailed information about a single public application,
        including its models, current version, and related demo information.

        Parameters
        ----------
        application_id : str
            The unique identifier of the public application.

        Returns
        -------
        tuple
            - dict: The application details including ID, name, cover image, current version, models, and demos.
            - str or None: Error message if any, else None.
            - str: Status message (e.g., "Successfully fetched application details").
        """
        path = f"/v1/public/applications/{application_id}"
        headers = {"Content-Type": "application/json"}

        resp = self.rpc.get(
            path=path,
        )

        return handle_response(
            resp,
            "Successfully fetched application details",
            f"Error fetching application details: {resp}"
        )



