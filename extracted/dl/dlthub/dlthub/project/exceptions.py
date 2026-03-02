import os
from typing import Iterable

from dlt.common.runtime.exceptions import RunContextNotAvailable

from dlthub.common.exceptions import DltPlusException


class ProjectException(DltPlusException):
    def __init__(self, project_dir: str, msg: str):
        self.project_dir = project_dir
        super().__init__(msg)


class ProjectRunContextNotAvailable(RunContextNotAvailable, ProjectException):
    def __init__(self, project_dir: str):
        msg = (
            f"Path {os.path.abspath(project_dir)} does not belong to dlt project.\n"
            "* it does not contain dlt.yml\n"
            "* none of parent folders contains dlt.yml\n"
            "* it does not contain pyproject.toml which defines a python module with dlt.yml "
            "in the root folder\n"
            "* it does not contain pyproject.toml which explicitly defines dlt project with "
            "`dlt_project` entry point\n"
            "Please refer to dlthub documentation for details."
        )
        super().__init__(project_dir, msg)


class ProjectDocValidationError(ProjectException):
    def __init__(self, project_dir: str, validation_err: str):
        super().__init__(
            project_dir,
            f"Project file {project_dir} contains unknown or invalid entities: {validation_err}",
        )


class ProfileNotFound(ProjectException, KeyError):
    def __init__(self, project_dir: str, profile_name: str, available_profiles: Iterable[str]):
        super().__init__(
            project_dir,
            f"Project {project_dir} does not declare profile {profile_name}"
            f" and {profile_name} is not one of implicit profiles. "
            f"Available profiles: {available_profiles}",
        )


class ProjectExplicitEntityNotFound(ProjectException, KeyError):
    """Explicitly defined `entity` with `name` not found in project."""

    def __init__(self, project_dir: str, entity: str, name: str):
        self.entity = entity
        self.name = name
        super().__init__(
            project_dir,
            f"{entity} with name '{name}' is not explicitly declared in project {project_dir} and "
            f"project settings (allow_undefined_entities) prevent undefined {entity} "
            "to be used.",
        )


class InvalidDestinationException(ProjectException):
    def __init__(
        self,
        project_dir: str,
        dataset_name: str,
        destination_name: str,
        available_destinations: Iterable[str],
    ):
        self.dataset_name = dataset_name
        self.destination_name = destination_name
        self.available_destinations = available_destinations

        msg = f"Dataset {dataset_name} is not available on destination {destination_name}. "
        if available_destinations:
            msg += f"Available destinations: {available_destinations}. "
        else:
            msg += "No destinations are configured for this dataset. "
            msg += (
                "You can use the destination property to specify a "
                + "list of allowed destinations for a dataset."
            )

        super().__init__(project_dir, msg)
