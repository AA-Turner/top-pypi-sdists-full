"""Module providing action functionality."""


class Action:
    """
    Represents an action within the system.

    This class provides an interface to interact with a specific action identified by its
    action_id. It retrieves the action's details such as type, project, user, status,
    creation time, and associated service from the API.

    Attributes
    ----------
    action_id : str
        The unique identifier for this action.
    action_type : str
        The type of action (retrieved from the API response).
    project_id : str
        The unique ID of the project associated with this action.
    user_id : str
        The unique ID of the user who triggered the action.
    step_code : str
        A code representing the current step of the action process.
    status : str
        The current status of the action (e.g., "pending", "completed").
    created_at : str
        The timestamp when the action was initiated.
    service_name : str
        The name of the service handling this action.

    Methods
    -------
    __init__(session, action_id)
        Initializes the Action object and fetches the action details from the API.

    refresh()
        Refreshes the action instance, updating its details by calling the API again.

    Examples
    --------
    >>> session = RPCSession()  # Assuming `RPCSession` is an existing session class
    >>> action = Action(session, "action_id_1234")
    >>> print(action.action_type)  # Output the type of action
    """

    def __init__(self, session, action_id):
        """
        Initializes the Action object and fetches the action details from the API.

        Parameters
        ----------
        session : RPCSession
            An active session object that is used to make API calls.
        action_id : str
            The unique identifier for the action whose details need to be fetched.

        Notes
        -----
        This constructor calls the `get_action_details` function to retrieve the action details,
        which are then set as attributes of the Action object.

        If an error occurs while fetching the action details, an error message will be printed.
        """
        self.action_id = action_id
        self.session = session
        self.action_type = None
        self.project_id = None
        self.user_id = None
        self.step_code = None
        self.status = None
        self.created_at = None
        self.service_name = None
        self.action_details = None
        self.job_params = {}
        data, error = get_action_details(session, action_id)
        if error is not None:
            print(f"An error occurred while fetching action details: \n {error}")
        else:
            self.action_type = data["action"]
            self.project_id = data["_idProject"]
            self.user_id = data["_idUser"]
            self.step_code = data["stepCode"]
            self.status = data["status"]
            self.created_at = data["createdAt"]
            self.service_name = data["serviceName"]
            self.action_details = data["actionDetails"]
            self.job_params = data.get("jobParams", {})

    def refresh(self):
        """Refresh the instance by reinstantiating it with the previous values."""
        init_params = {
            "session": self.session,
            "action_id": self.action_id,
        }
        self.__init__(**init_params)

def get_project_id_by_service_id(session, service_id):
    """
    Get the Project Id by the service ID.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    service_id: str
        A unique identifier of a particular service associated with a project

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_project_id_by_service_id(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/list_all_account_action_details"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def list_all_account_action_details(session):
    """
    List all account with there action details.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = list_all_account_action_details(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/list_all_account_action_details"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_recent_actions(session):
    """
    Fetches recent actions performed on the platform.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_recent_actions(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/recent_actions"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_record_for_account_number(session):
    """
    Fetches action details of the account number.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action records if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_record_for_account_number(session)
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/action_records"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_logs_from_record_id(session, action_record_id):
    """
    Fetches action details from action record ID.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the action logs whose details are being fetched.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_logs_from_record_id(session, "action_record_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/action_logs_from_record_id/{action_record_id}"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_service_action_logs(session, service_id):
    """
    Fetches action details from service ID.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    service_id : str
        The unique identifier of the service whose details are being fetched.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_details(session, "service_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/{service_id}/logs"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_logs_from_action_record_id(session, action_record_id):
    """
    Fetches action details from action record ID.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the service whose details are being fetched.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action logs if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_logs_from_action_record_id(session, "action_record_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/action_logs_from_record_id/{action_record_id}"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_details(session, action_id):
    """
    Fetches action details from the API.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_id : str
        The unique identifier of the action whose details are being fetched.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_details(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/action/{action_id}/details"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_docker_logs(session, action_record_id):
    """
    Get the docker logs associated with a particular action record.

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    action_record_id : str
        The unique identifier of the action record whose docker logs are being fetched.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_docker_logs(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/get_action_docker_logs/{action_record_id}"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.get("data"), resp.get("message")

def get_action_graph(session, granularity, start_date, end_date):
    """
    Get the action graph

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    granularity : str
        Unit for the created by time
    start_date: str
        Date and tiem 

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = get_action_graph(session, "action_id_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/get_actions_graph"
    payload = {
        "accountNumber": session.account_number,
        "granularity": granularity,
        "startDate": start_date,
        "endDate": end_date
    }

    resp = session.rpc.get(path=path, payload=payload)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.post("data"), resp.get("message")

def clone_project(session, source_project_id, new_project_name):
    """
    Clone the project with the project ID

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    source_project_id : str
        ID of the project you want to copy.
    new_project_name: str
        Name of the new project.

    Returns
    -------
    tuple
        A tuple containing two elements:
        - A dictionary with the action details if the request is successful.
        - An error message (str) if the request fails, otherwise `None`.

    Raises
    ------
    ConnectionError
        Raised when there's a failure in communication with the API.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = clone_project(session, "ProjectID_1234", "New_Project_name")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/clone_project"
    payload = {
        "sourceProjectId": source_project_id,
        "newProjectName": new_project_name
    }

    resp = session.rpc.get(path=path, payload=payload)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.post("data"), resp.get("message")

def enable_disable_project(session, type, project_id):
    """
    Enable or disable a project

    Parameters
    ----------
    session : RPCSession
        An active session object used to perform API requests.
    type : str
        Action you want to perform i.e either enable or disable
    project_id: str
        Id of the project you want to enable or disable

    Returns
    -------

    Raises
    ------
    ConnectionError
        Raised when there's a failure in enabling or disabling the project.

    Examples
    --------
    >>> session = RPCSession()
    >>> data, error = enable_disable_project(session, "enable", "ProjectID_1234")
    >>> if error is None:
    >>>     pprint(data)
    >>> else:
    >>>     print(f"Error: {error}")
    """
    path = f"/v1/actions/enable-disable-project/{type}/{project_id}"


    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    return resp.put("data"), resp.get("message")