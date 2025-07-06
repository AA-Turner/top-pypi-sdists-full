"""Module providing drift_monitor functionality."""

from matrice.utils import handle_response
from datetime import datetime, timedelta

"""Module for interacting with backend API to manage drift monitoring."""


class DriftMonitoring:
    """
    Class for managing drift monitoring operations within a project.

    Parameters
    ----------
    session : object
        The session object that provides access to the RPC interface and project ID.

    Attributes
    ----------
    session : object
        Session object for facilitating RPC communication.
    project_id : str
        ID of the project associated with this drift monitoring instance.
    rpc : object
        RPC interface for making backend API calls.

    Example
    -------
    >>> session = Session(account_number="account_number")
    >>> drift_monitoring = DriftMonitoring(session=session)
    """

    def __init__(self, session):
        self.session = session
        self.project_id = session.project_id
        self.rpc = session.rpc
        self.last_refresh_time = datetime.now()

    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        self.__dict__.copy()
        init_params = {"session": self.session}
        self.__init__(**init_params)
        self.last_refresh_time = datetime.now()

    def add_params(
        self,
        _idDeployment,
        deploymentName,
        imageStoreConfidenceThreshold,
        imageStoreCountThreshold,
    ):
        """
        Add drift monitoring parameters for a specified deployment.

        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response indicating the success or failure of adding parameters.
            - str or None:
                Error message if an error occurred, otherwise None.
            - str:
                Message indicating success or error status.

        Example
        -------
        >>> from pprint import pprint
        >>> add_params, err, msg = drift_monitoring.add_params(
        ...     _idDeployment="deployment123",
        ...     deploymentName="MyDeployment",
        ...     imageStoreConfidenceThreshold=0.85,
        ...     imageStoreCountThreshold=100
        ... )
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     pprint(add_params)
        """
        path = "/v1/deployment/drift_monitoring"
        headers = {"Content-Type": "application/json"}
        monitoring_params = {
            "_idDeployment": _idDeployment,
            "deploymentName": deploymentName,
            "imageStoreConfidenceThreshold": imageStoreConfidenceThreshold,
            "imageStoreCountThreshold": imageStoreCountThreshold,
        }
        resp = self.rpc.post(
            path=path,
            headers=headers,
            payload=monitoring_params,
        )
        return handle_response(
            resp,
            "Drift monitoring parameters added successfully",
            "An error occurred while trying to add drift monitoring parameters",
        )

    def update(
        self,
        _idDeployment,
        deploymentName,
        imageStoreConfidenceThreshold,
        imageStoreCountThreshold,
    ):
        """
        Update existing drift monitoring parameters for a specified deployment.

        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - dict:
                The API response indicating the success or failure of the update.
            - str or None:
                Error message if an error occurred, otherwise None.
            - str:
                Message indicating success or error status.

        Example
        -------
        >>> from pprint import pprint
        >>> update, err, msg = drift_monitoring.update(
        ...     _idDeployment="deployment123",
        ...     deploymentName="MyDeployment",
        ...     imageStoreConfidenceThreshold=0.9,
        ...     imageStoreCountThreshold=150
        ... )
        >>> if err:
        ...     pprint(err)
        >>> else:
        ...     pprint(update)
        """
        path = "/v1/deployment/update_drift_monitoring"
        headers = {"Content-Type": "application/json"}
        monitoring_params = {
            "_idDeployment": _idDeployment,
            "deploymentName": deploymentName,
            "imageStoreConfidenceThreshold": imageStoreConfidenceThreshold,
            "imageStoreCountThreshold": imageStoreCountThreshold,
        }
        resp = self.rpc.put(
            path=path,
            headers=headers,
            payload=monitoring_params,
        )
        return handle_response(
            resp,
            "Drift monitoring parameters updated successfully",
            "An error occurred while trying to update drift monitoring parameters",
        )
