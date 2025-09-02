import json
import logging
import os
import tempfile
from typing import Optional, Literal, Any, Union
from urllib.parse import urlparse

import httpx
from httpx import Response, HTTPError
from pydantic import BaseModel, Field

from ipfabric.tools.shared import raise_for_status
from ipfabric.models.users import User

logger = logging.getLogger("ipfabric")


class Resources(BaseModel):
    cpu: int
    memory: int


class Extension(BaseModel):
    client: Optional[Any] = Field(None, exclude=True)
    id: str
    name: str
    description: Optional[str] = None
    slug: str
    status: str
    type: Optional[Literal["docker-zip", "docker-image"]] = None
    environment_variables: Optional[list[dict[str, str]]] = Field(alias="environmentVariables")
    access_permission: str = Field(alias="accessPermission")
    accessible_by_users: list[str] = Field(alias="accessibleByUsers")
    resources: Resources

    @property
    def users(self) -> list[User]:
        """
        Fetch users with access to the extension.

        Returns:
            List[User]: List of users with access to the extension
        """
        try:
            return [self.client.settings.local_users.users_by_id[user] for user in self.accessible_by_users]
        except:  # noqa: E722
            return []


class Extensions(BaseModel):
    client: Any = Field(exclude=True)

    @property
    def extensions(self) -> list[Extension]:
        """
        Fetch all extensions.

        Returns:
            List[Extension]: List of all available extensions
        """
        response = raise_for_status(self.client.get("extensions")).json()["extensions"]
        return [Extension(client=self.client, **ext) for ext in response]

    def extension_by_id(self, extension_id: str) -> Extension:
        """
        Fetch a specific extension by ID.

        Args:
            extension_id (str): The ID of the extension to fetch

        Returns:
            Extension: The requested extension
        """
        return Extension(client=self.client, **raise_for_status(self.client.get(f"extensions/{extension_id}")).json())

    def logs_by_extension_id(self, extension_id: str) -> dict:
        """
        Fetch paginated logs for a specific extension.

        Args:
            extension_id (str): The ID of the extension to fetch logs for

        Returns:
            Dict: The paginated logs response
        """
        return raise_for_status(self.client.get(f"extensions/{extension_id}/logs")).json()

    def extension_by_name(self, name: str) -> Extension:
        """
        Fetch a specific extension by name.
        """
        extension = next((ext for ext in self.extensions if ext.name == name), None)
        if extension is None:
            raise ValueError(f"Extension with name '{name}' not found")
        return extension

    def extension_by_slug(self, slug: str) -> Extension:
        """
        Fetch a specific extension by slug.
        """
        extension = next((ext for ext in self.extensions if ext.slug == slug), None)
        if extension is None:
            raise ValueError(f"Extension with slug '{slug}' not found")
        return extension

    @staticmethod
    def _users_permissions(
        access_permission: Literal["anyone", "only-me", "selected-users"] = "anyone",
        accessible_by_users: Optional[list[str]] = None,
    ):
        if access_permission != "selected-users":
            if accessible_by_users:
                logger.warning("Accessible by Users is only allowed with selected-users permission")
            return {"accessPermission": access_permission, "accessibleByUsers": []}
        return {"accessPermission": access_permission, "accessibleByUsers": accessible_by_users}

    def _register_extension(
        self,
        docker_type: Literal["docker-zip", "docker-image"],
        file: bytes,
        name: str,
        slug: str,
        description: str,
        cpu: int = 1,
        memory: int = 512,
        environment_variables: Optional[dict[str, str]] = None,
        access_permission: Literal["anyone", "only-me", "selected-users"] = "anyone",
        accessible_by_users: Optional[list[str]] = None,
    ) -> Response:
        files = (
            {"file": ("extension.zip", file, "application/zip")}
            if docker_type == "docker-zip"
            else {"file": ("image.tar", file, "application/x-tar")}
        )

        data = {
            "name": name,
            "slug": slug,
            "description": description,
            "resources": json.dumps({"cpu": cpu, "memory": memory}),
            **self._users_permissions(access_permission, accessible_by_users),
        }

        if environment_variables:
            data["environmentVariables"] = [
                {"name": key, "value": value} for key, value in environment_variables.items()
            ]

        return raise_for_status(self.client.post(f"extensions/{docker_type}", files=files, data=data, timeout=300))

    def register_docker_zip(
        self,
        file: bytes,
        name: str,
        slug: str,
        description: str,
        cpu: int = 1,
        memory: int = 512,
        environment_variables: Optional[dict[str, str]] = None,
        access_permission: Literal["anyone", "only-me", "selected-users"] = "anyone",
        accessible_by_users: Optional[list[str]] = None,
    ) -> Response:
        """
        Register a new extension using zipped source code. Raises an exception if the extension is not registered successfully.

        Args:
            file (bytes): The zipped source code file
            name (str): Name of the extension
            slug (str): Slug for the extension
            description (str): Description of the extension
            cpu (int): Number of CPU cores for the extension
            memory (int): Memory size in MB for the extension
            environment_variables (Optional[Dict[str, str]]): Environment variables for the extension
            access_permission (Literal["anyone", "only-me", "selected-users"]): Access permission for the extension
            accessible_by_users (Optional[List[str]]): List of User IDs with access to the extension
        """
        return self._register_extension(
            "docker-zip",
            file=file,
            name=name,
            slug=slug,
            description=description,
            cpu=cpu,
            memory=memory,
            environment_variables=environment_variables,
            access_permission=access_permission,
            accessible_by_users=accessible_by_users,
        )

    def register_docker_image(
        self,
        file: bytes,
        name: str,
        slug: str,
        description: str,
        cpu: int = 1,
        memory: int = 512,
        environment_variables: Optional[dict[str, str]] = None,
        access_permission: Literal["anyone", "only-me", "selected-users"] = "anyone",
        accessible_by_users: Optional[list[str]] = None,
    ) -> Response:
        """
        Register a new extension using a docker image. Raises an exception if the extension is not registered successfully.

        Args:
            file (bytes): The tar file of the docker image
            name (str): Name of the extension
            slug (str): Slug for the extension
            description (str): Description of the extension
            cpu (int): Number of CPU cores for the extension
            memory (int): Memory size in MB for the extension
            environment_variables (Optional[Dict[str, str]]): Environment variables for the extension
            access_permission (Literal["anyone", "only-me", "selected-users"]): Access permission for the extension
            accessible_by_users (Optional[List[str]]): List of User IDs with access to the extension
        """
        self._register_extension(
            "docker-zip",
            file=file,
            name=name,
            slug=slug,
            description=description,
            cpu=cpu,
            memory=memory,
            environment_variables=environment_variables,
            access_permission=access_permission,
            accessible_by_users=accessible_by_users,
        )

    def start_extension(self, extension_id: str) -> Response:
        """
        Start an extension by its ID. Raises an exception if the extension fails to start.

        Args:
            extension_id (str): The ID of the extension to start
        """
        return raise_for_status(self.client.post(f"extensions/{extension_id}/start"))

    def stop_extension(self, extension_id: str) -> Response:
        """
        Stop an extension by its ID. Raises an exception if the extension fails to stop.

        Args:
            extension_id (str): The ID of the extension to stop
        """
        return raise_for_status(self.client.post(f"extensions/{extension_id}/stop"))

    def unregister_extension(self, extension_id: str) -> Response:
        """
        Unregister an extension by its ID. Raises an exception if the extension fails to unregister.

        Args:
            extension_id (str): The ID of the extension to unregister
        """
        return raise_for_status(self.client.delete(f"extensions/{extension_id}"))

    def register_from_git_url(
        self,
        git_url: str,
        name: str,
        slug: str,
        description: str,
        branch: str = "main",
        cpu: int = 1,
        memory: int = 512,
        environment_variables: Optional[dict[str, str]] = None,
        access_permission: Literal["anyone", "only-me", "selected-users"] = "anyone",
        accessible_by_users: Optional[list[str]] = None,
    ) -> Union[Response, None]:
        """
        Register an extension from a Git repository URL. Supports GitHub and GitLab repositories.
        Downloads the repository, creates a ZIP file, and registers it as a docker-zip extension.

        Args:
            git_url (str): URL to the Git repository (GitHub or GitLab)
            name (str): Name of the extension
            slug (str): Slug for the extension
            description (str): Description of the extension
            branch (str): Branch to download (default: "main")
            cpu (int): Number of CPU cores for the extension
            memory (int): Memory size in MB for the extension
            environment_variables (Optional[Dict[str, str]]): Environment variables for the extension
            access_permission (Literal["anyone", "only-me", "selected-users"]): Access permission for the extension
            accessible_by_users (Optional[List[str]]): List of User IDs with access to the extension

        Example:
            client.extensions.register_from_git_url(
                "https://github.com/username/repo",
                "My Extension",
                "my-extension",
                "Description",
                branch="main"
            )
        """
        parsed_url = urlparse(git_url)

        path_parts = parsed_url.path.rstrip(".git").strip("/").split("/")

        if "github.com" in parsed_url.netloc:
            if len(path_parts) != 2:
                raise ValueError("Invalid GitHub URL format")
            user, repo = path_parts
            download_url = f"https://github.com/{user}/{repo}/archive/{branch}.zip"

        elif "gitlab.com" in parsed_url.netloc:
            if len(path_parts) < 2:
                raise ValueError("Invalid GitLab URL format")
            project = path_parts[-1]  # Last part is the project name
            group = "/".join(path_parts[:-1])  # Everything else is the group path
            download_url = f"https://gitlab.com/{group}/{project}/-/archive/{branch}/{project}-{branch}.zip"

        else:
            raise ValueError("Only GitHub and GitLab repositories are supported")

        response = httpx.get(download_url)
        if response.status_code != 200:
            raise HTTPError(f"Failed to download repository: {response.status_code}")

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)

        try:
            with open(tmp_file.name, "rb") as f:
                resp = self._register_extension(
                    "docker-zip",
                    file=f.read(),
                    name=name,
                    slug=slug,
                    description=description,
                    cpu=cpu,
                    memory=memory,
                    environment_variables=environment_variables,
                    access_permission=access_permission,
                    accessible_by_users=accessible_by_users,
                )
        finally:
            os.unlink(tmp_file.name)
        return resp
