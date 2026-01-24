from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.project import CreateProjectRequest, ProjectResponse, ProjectType


def create_project(request: CreateProjectRequest, config: Optional[GalileoConfig] = None) -> ProjectResponse:
    """
    Create a project.

    Parameters
    ----------
    request : CreateProjectRequest
        Request object for creating a project.

    Returns
    -------
    ProjectResponse
        Response object for the created project.
    """
    config = config or GalileoConfig.get()
    existing_project = get_project_from_name(project_name=request.name, raise_if_missing=False, config=config)
    if existing_project:
        logger.debug(f"Project {request.name} already exists, using it.")
        project_response = existing_project
    else:
        logger.debug(f"Creating project {request.name}...")
        response_dict = config.api_client.request(
            RequestMethod.POST, Routes.projects, json=request.model_dump(mode="json")
        )
        project_response = ProjectResponse.model_validate(response_dict)
        logger.debug(f"Created project with name {project_response.name}, ID {project_response.id}.")
    return project_response


def get_project(
    project_id: Optional[UUID4] = None,
    project_name: Optional[str] = None,
    project_type: Optional[ProjectType] = None,
    raise_if_missing: bool = True,
    config: Optional[GalileoConfig] = None,
) -> Optional[ProjectResponse]:
    """
    Get a project by either ID or name.

    If both project_id and project_name are provided, project_id will take precedence.

    For cases when the project name is if the project_type is provided, it will be used
    to filter the projects by type if the project_name is provided. If raise_if_missing
    is True, a ValueError will be raised if the project is not found. This is useful
    when the project is expected to exist, and the absence of the project would be an error.

    Parameters
    ----------
    project_id : Optional[UUID4], optional
        Project ID, by default None.
    project_name : Optional[str], optional
        Project name, by default None.
    project_type : Optional[ProjectType], optional
        Project type, by default None.
    raise_if_missing : bool, optional
        Raise an error if the project is not found, by default True.

    Returns
    -------
    Optional[ProjectResponse]
        Project response object if the project is found, None otherwise.

    Raises
    ------
    ValueError
        If neither project_id nor project_name is provided.
    """
    if project_id:
        return get_project_from_id(project_id=project_id, config=config)
    elif project_name:
        return get_project_from_name(
            project_name=project_name,
            project_type=project_type,
            raise_if_missing=raise_if_missing,
            config=config,
        )
    else:
        raise ValueError("Either project_id or project_name must be provided.")


def get_project_from_id(project_id: UUID4, config: Optional[GalileoConfig] = None) -> ProjectResponse:
    """
    Given a project ID, get the project.

    Parameters
    ----------
    project_id : UUID4
        Project ID.

    Returns
    -------
    ProjectResponse
        Project response object.
    """
    config = config or GalileoConfig.get()
    response_dict = config.api_client.request(RequestMethod.GET, Routes.project.format(project_id=project_id))
    project = ProjectResponse.model_validate(response_dict)
    logger.debug(f"Got project with name {project.name}, ID {project.id}.")
    return project


def get_projects(
    project_type: Optional[ProjectType] = None, config: Optional[GalileoConfig] = None
) -> List[ProjectResponse]:
    """
    Given a project type, returns all projects of that type that the user has access to.

    Parameters
    ----------
    project_type : ProjectType
        The type of projects to get.

    Returns
    -------
    List[ProjectResponse]
        A list of projects of the given type.
    """
    config = config or GalileoConfig.get()
    params = dict(type=project_type.value) if project_type else {}
    projects = [
        ProjectResponse.model_validate(proj)
        for proj in config.api_client.request(RequestMethod.GET, Routes.projects, params=params)
    ]
    logger.debug(f"Got {len(projects)} projects of type {project_type}.")
    return projects


def get_project_from_name(
    project_name: str,
    project_type: Optional[ProjectType] = None,
    raise_if_missing: bool = True,
    config: Optional[GalileoConfig] = None,
) -> Optional[ProjectResponse]:
    """
    Get a project by name.

    Parameters
    ----------
    project_name : str
        Name of the project.
    project_type : Optional[ProjectType], optional
        Type of the project to filter by, by default None.
    raise_if_missing : bool, optional
        Raise an error if the proejct is not found, by default True.

    Returns
    -------
    Optional[ProjectResponse]
        Project response object if the project is found, None otherwise.

    Raises
    ------
    ValueError
        If the project is not found and raise_if_missing is True.
    """
    config = config or GalileoConfig.get()
    params = dict(project_name=project_name)
    if project_type:
        params["project_type"] = project_type
    projects = [
        ProjectResponse.model_validate(proj)
        for proj in config.api_client.request(RequestMethod.GET, Routes.projects, params=params)
    ]
    if raise_if_missing and len(projects) == 0:
        raise ValueError(f"Project {project_name} does not exist.")
    elif len(projects) > 0:
        project_response = projects[0]
        logger.debug(f"Got project with name {project_response.name}, with ID {project_response.id}.")
        return project_response
    else:
        return None


def update_project(
    project_id: UUID4,
    project_name: str,
    config: Optional[GalileoConfig] = None,
) -> ProjectResponse:
    """
    Update the name of a project.

    Args:
        project_id : UUID4
            Project ID
        project_name : str
            New project name

    Returns:
        ProjectResponse
        Project response object.

    """
    config = config or GalileoConfig.get()

    response_dict = config.api_client.request(
        RequestMethod.PUT,
        Routes.project.format(project_id=project_id),
        json={"name": project_name},
    )
    project = ProjectResponse.model_validate(response_dict)
    logger.debug(f"Updated project with ID {project.id}. New project name: {project.name}")
    return project
