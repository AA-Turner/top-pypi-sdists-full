"""Auto-generated stub for module: session."""
from typing import Any, Dict, List, Optional, Tuple

from .rpc import RPC
from .utils import handle_response

# Constants
logger: Any

# Functions
def create_session(account_number: str, access_key: str, secret_key: str) -> Session:
    """
    Create and initialize a new session with specified credentials.
    
    Parameters
    ----------
    account_number : str
        The account number to associate with the new session.
    access_key : str
        The access key for authentication.
    secret_key : str
        The secret key for authentication.
    
    Returns
    -------
    Session
        An instance of the Session class initialized with the given credentials.
    
    Example
    -------
    >>> session = create_session("9625383462734064921642156", "HREDGFXB6KI0TWH6UZEYR",
    "UY8LP0GQRKLSFPZAW1AUF")
    >>> print(session)
    <Session object at 0x...>
    """
    ...

# Classes
class Session:
    # Class to manage sessions.
    #
    #     Initialize a new session instance.
    #
    #     Parameters
    #     ----------
    #     account_number : str
    #         The account number associated with the session.
    #     project_id : str, optional
    #         The ID of the project for this session.
    #     Example
    #     -------
    #     >>> session = Session(account_number="9625383462734064921642156")

    def __init__(self: Any, account_number: str, access_key: Optional[str] = None, secret_key: Optional[str] = None, project_id: Optional[str] = None, project_name: Optional[str] = None) -> None: ...

    def close(self: Any) -> None:
        """
        Close the current session by resetting the RPC and project details.
        
        Example
        -------
        >>> session.close()
        """
        ...

    def create_classification_project(self: Any, project_name: str, industries: Optional[List[str]] = None, tags: Optional[List[str]] = None, computeType: str = 'matrice', storageType: str = 'matrice', supportedDevices: str = 'nvidia_gpu', deploymentSupportedDevices: str = 'nvidia_gpu') -> Optional[Dict[str, Any]]:
        """
        Create a classification project.
        
        Parameters
        ----------
        project_name : str
            The name of the classification project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_classification_project("Image Classification Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def create_detection_project(self: Any, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Create a detection project.
        
        Parameters
        ----------
        project_name : str
            The name of the detection project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_detection_project("Object Detection Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def create_segmentation_project(self: Any, project_name: str) -> Optional[Dict[str, Any]]:
        """
        Create a segmentation project.
        
        Parameters
        ----------
        project_name : str
            The name of the segmentation project to be created.
        
        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.
        
        Example
        -------
        >>> project = session.create_segmentation_project("Instance Segmentation Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        ...

    def get_project_type_summary(self: Any) -> Tuple[Dict[str, Any], Optional[str]]:
        """
        Get the count of different types of projects.
        
        Returns
        -------
        tuple
            A tuple containing:
            - A dictionary with project types as keys and their counts as values if the request is
                successful.
            - An error message if the request fails.
        
        Example
        -------
        >>> project_summary, error = session.get_project_type_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Project type summary: {project_summary}")
        """
        ...

    def list_projects(self: Any, project_type: str = '', page_size: int = 10, page_number: int = 0) -> Tuple[List[Any], str]:
        """
        List projects based on the specified type.
        
        Parameters
        ----------
        project_type : str, optional
            The type of projects to list (e.g., 'classification', 'detection'). If empty,
            all projects are listed.
        
        Returns
        -------
        tuple
            A tuple containing the dictionary of projects and a message indicating the result of
                the fetch operation.
        
        Example
        -------
        >>> projects, message = session.list_projects("classification")
        >>> print(message)
        Projects fetched successfully
        >>> for project_name, project_instance in projects.items():
        >>>     print(project_name, project_instance)
        """
        ...

    def refresh(self: Any) -> None:
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        ...

    def update(self: Any, project_id: Optional[str]) -> None:
        """
        Update the session with new project details.
        
        Parameters
        ----------
        project_id : str, optional
            The new ID of the project.
        
        
        Example
        -------
        >>> session.update(project_id="660b96fc019dd5321fd4f8c7")
        """
        ...

