#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, List, Optional

import trafaret as t
from typing_extensions import TypedDict

from datarobot.models.api_object import APIObject
from datarobot.models.custom_application import CustomApplication
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class CustomApplicationSourceResources(TypedDict):
    """Resource configuration for a Custom Application Source."""

    replicas: int
    resource_label: str
    service_web_requests_on_root_path: Optional[bool]
    session_affinity: Optional[bool]


class CustomApplicationSourceVersion(TypedDict):
    """Version information for a Custom Application Source."""

    id: str
    label: Optional[str]
    created_at: str
    updated_at: str
    is_frozen: bool


# Trafaret validator for resources field (can be dict or null)
_resources_validator = t.Or(
    t.Dict({
        t.Key("replicas"): t.Int,
        t.Key("resource_label"): t.String,
        t.Key("service_web_requests_on_root_path", optional=True): t.Bool,
        t.Key("session_affinity", optional=True): t.Bool,
    }).ignore_extra("*"),
    t.Null,
)

# Trafaret validator for latest_version field
# The latest_version can contain resources nested within it
_latest_version_validator = t.Dict({
    t.Key("id"): t.String,
    t.Key("label", optional=True): t.Or(t.String, t.Null),
    t.Key("created_at"): t.String,
    t.Key("updated_at"): t.String,
    t.Key("is_frozen"): t.Bool,
    t.Key("resources", optional=True): _resources_validator,
}).ignore_extra("*")


class CustomApplicationSource(APIObject):
    """
    A DataRobot custom application source that serves as a template for creating custom applications.

    Custom application sources define the code, configuration, and resource requirements
    used when creating custom applications. They can have resource configurations
    that determine the default resource allocation for applications created from this source.

    Attributes
    ----------
    id : str
        The ID of the custom application source.
    name : str
        The name of the custom application source.
    latest_version : CustomApplicationSourceVersion
        Information about the latest version of this source.
    user_id : str
        The ID of the user who created the source.
    org_id : str
        The organization ID.
    permissions : List[str]
        List of permissions for the current user.
    created_at : str
        Timestamp when the source was created.
    updated_at : str
        Timestamp when the source was last updated.
    created_by : str
        Email of the user who created the source.
    creator_first_name : str
        First name of the creator.
    creator_last_name : str
        Last name of the creator.
    creator_userhash : str
        Userhash of the creator.

    Notes
    -----
    Resource configuration is stored in the latest_version field and can be accessed
    via the get_resources() method.
    """

    _path = "customApplicationSources/"

    _converter = t.Dict({
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("latest_version"): _latest_version_validator,
        t.Key("user_id"): t.String,
        t.Key("org_id"): t.String,
        t.Key("permissions"): t.List(t.String),
        t.Key("created_at"): t.String,
        t.Key("updated_at"): t.String,
        t.Key("created_by"): t.String,
        t.Key("creator_first_name"): t.String,
        t.Key("creator_last_name"): t.String,
        t.Key("creator_userhash"): t.String,
    }).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        latest_version: Dict[str, Any],
        user_id: str,
        org_id: str,
        permissions: List[str],
        created_at: str,
        updated_at: str,
        created_by: str,
        creator_first_name: str,
        creator_last_name: str,
        creator_userhash: str,
    ):
        self.id = id
        self.name = name
        self.latest_version = latest_version
        self.user_id = user_id
        self.org_id = org_id
        self.permissions = permissions
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_userhash = creator_userhash

    def __repr__(self) -> str:
        return f"CustomApplicationSource({self.name!r}, id={self.id!r})"

    @classmethod
    def list(
        cls,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[CustomApplicationSource]:
        """
        Retrieve a list of custom application sources.

        Parameters
        ----------
        offset : Optional[int]
            Optional. Retrieve sources in a list after this number.
        limit : Optional[int]
            Optional. Retrieve only this number of sources.

        Returns
        -------
        sources : List[CustomApplicationSource]
            The requested list of custom application sources.
        """
        query = {"offset": offset, "limit": limit}
        sources = unpaginate(initial_url=cls._path, initial_params=query, client=cls._client)
        return [cls.from_server_data(source) for source in sources]

    @classmethod
    def get(cls, source_id: str) -> CustomApplicationSource:
        """
        Retrieve a single custom application source with full details.

        Parameters
        ----------
        source_id : str
            The ID of the custom application source to retrieve.

        Returns
        -------
        source : CustomApplicationSource
            The requested custom application source.
        """
        r_data = cls._client.get(f"{cls._path}{source_id}/")
        return cls.from_server_data(r_data.json())

    @classmethod
    def create(cls, name: str) -> CustomApplicationSource:
        """
        Create a new custom application source.

        Parameters
        ----------
        name : str
            The name for the new custom application source.

        Returns
        -------
        source : CustomApplicationSource
            The newly created custom application source.
        """
        payload = {"name": name}
        r_data = cls._client.post(cls._path, data=payload)
        return cls.from_server_data(r_data.json())

    def update(self, name: Optional[str] = None) -> CustomApplicationSource:
        """
        Update this custom application source.

        Parameters
        ----------
        name : Optional[str]
            New name for the source. If None, name will not be changed.

        Returns
        -------
        source : CustomApplicationSource
            The updated custom application source.
        """
        payload = {}
        if name is not None:
            payload["name"] = name

        if not payload:
            return self  # No changes to make

        r_data = self._client.patch(f"{self._path}{self.id}/", data=payload)
        return self.from_server_data(r_data.json())

    def delete(self, hard_delete: bool = False) -> None:
        """
        Delete this custom application source.

        Parameters
        ----------
        hard_delete : bool, optional
            If True, permanently delete the source and all its data.
            If False (default), soft delete the source (can be recovered).

        Note
        ----
        Deleting a source will affect all its versions. Applications created from this
        source will continue to run but cannot be recreated from the source.

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomApplicationSource

            source = CustomApplicationSource.get("source_id")
            source.delete()  # Soft delete
            source.delete(hard_delete=True)  # Permanent delete
        """
        params = {"hardDelete": hard_delete} if hard_delete else {}
        self._client.delete(f"{self._path}{self.id}/", params=params)

    def get_resources(self) -> Optional[Dict[str, Any]]:
        """
        Get resource configuration for applications created from this source.

        Returns
        -------
        resources : Optional[Dict[str, Any]]
            Resource configuration including replicas, resource bundle, and other settings.
            Returns None if no resources are configured.
        """
        # Resources are in the latest_version object
        if (
            self.latest_version is None
            or not isinstance(self.latest_version, dict)
            or "resources" not in self.latest_version
            or self.latest_version["resources"] is None
        ):
            return None

        resources = self.latest_version["resources"]

        # Resources are already in snake_case format from the API client conversion
        return {
            "replicas": resources.get("replicas"),
            "resource_label": resources.get("resource_label"),
            "service_web_requests_on_root_path": resources.get("service_web_requests_on_root_path"),
            "session_affinity": resources.get("session_affinity"),
        }

    def get_resource_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get a human-readable summary of resource configuration.

        Returns
        -------
        summary : Optional[Dict[str, Any]]
            A summary of resource configuration with readable descriptions.
            Returns None if no resources are configured.
        """
        # Resources are in the latest_version object
        if (
            self.latest_version is None
            or not isinstance(self.latest_version, dict)
            or "resources" not in self.latest_version
            or self.latest_version["resources"] is None
        ):
            return None

        resources = self.latest_version["resources"]

        return {
            "resource_bundle": resources.get("resource_label"),
            "scaling": {
                "replicas": resources.get("replicas"),
                "session_affinity": resources.get("session_affinity"),
            },
            "networking": {
                "service_web_requests_on_root_path": resources.get("service_web_requests_on_root_path"),
            },
        }

    @property
    def has_resources_configured(self) -> bool:
        """
        Check if this source has resource configuration.

        Returns
        -------
        bool
            True if resources are configured, False otherwise.
        """
        return (
            self.latest_version is not None
            and isinstance(self.latest_version, dict)
            and "resources" in self.latest_version
            and self.latest_version["resources"] is not None
        )

    def get_details(self) -> Dict[str, Any]:
        """
        Get comprehensive details about this custom application source.

        Returns
        -------
        details : Dict[str, Any]
            Comprehensive source details including metadata, version info, and resources.
        """
        return {
            "basic_info": {
                "id": self.id,
                "name": self.name,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
            },
            "creator_info": {
                "created_by": self.created_by,
                "creator_name": f"{self.creator_first_name} {self.creator_last_name}",
                "creator_userhash": self.creator_userhash,
            },
            "latest_version": {
                "id": self.latest_version.get("id"),
                "label": self.latest_version.get("label"),
                "created_at": self.latest_version.get("created_at"),
                "updated_at": self.latest_version.get("updated_at"),
                "is_frozen": self.latest_version.get("is_frozen"),
            },
            "resources": self.get_resource_summary(),
            "permissions": self.permissions,
            "has_resources": self.has_resources_configured,
        }

    @classmethod
    def get_by_name(cls, name: str) -> Optional[CustomApplicationSource]:
        """
        Find a custom application source by name.

        Parameters
        ----------
        name : str
            The name of the custom application source to find.

        Returns
        -------
        source : Optional[CustomApplicationSource]
            The custom application source if found, None otherwise.
        """
        sources = cls.list()
        for source in sources:
            if source.name == name:
                return source
        return None

    def create_application(
        self,
        name: str,
        resources: Optional[Dict[str, Any]] = None,
        environment_id: Optional[str] = None,
    ) -> CustomApplication:
        """
        Create a Custom Application from this source.

        Parameters
        ----------
        name : str
            Name for the new application.
        resources : Optional[Dict[str, Any]]
            Resource configuration for the application. If None, uses source defaults.
        environment_id : Optional[str]
            The ID of the execution environment to use. If None, uses source default.
        external_access_enabled : bool
            Whether to enable external access. Default is False.
        external_access_recipients : Optional[List[str]]
            List of email addresses for external access recipients.

        Returns
        -------
        application : CustomApplication
            The newly created Custom Application.

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomApplicationSource

            source = CustomApplicationSource.get("source_id")

            # Create with default settings
            app1 = source.create_application("My App")

            # Create with custom resources and environment
            app2 = source.create_application(
                "My App",
                resources={"replicas": 2, "resourceLabel": "cpu.large"},
                environment_id="env_id_123"
            )
        """
        # Build the payload - use applicationSourceId to create from source
        # The API requires ONLY ONE of: baseEnvironmentId, applicationSourceId, or applicationSourceVersionId
        payload: Dict[str, Any] = {
            "name": name,
            "applicationSourceId": self.id,
        }

        # Add optional environment ID
        if environment_id:
            payload["envVersionId"] = environment_id

        # Add optional resources
        if resources:
            payload["resources"] = {
                "replicas": resources.get("replicas"),
                "resourceLabel": resources.get("resourceLabel") or resources.get("resource_label"),
                "sessionAffinity": resources.get("sessionAffinity") or resources.get("session_affinity"),
                "serviceWebRequestsOnRootPath": resources.get("serviceWebRequestsOnRootPath")
                or resources.get("service_web_requests_on_root_path"),
            }

        r_data = self._client.post("customApplications/", data=payload)

        # Handle async creation - the API returns 202 with Location header
        if r_data.status_code == 202:
            location = wait_for_async_resolution(self._client, r_data.headers["Location"])
            return CustomApplication.from_location(location)
        else:
            return CustomApplication.from_server_data(r_data.json())

    def get_versions(self) -> List[Dict[str, Any]]:
        """
        Get all versions of this custom application source.

        Returns
        -------
        versions : List[Dict[str, Any]]
            List of version information for this source.
        """
        r_data = self._client.get(f"{self._path}{self.id}/versions/")
        data = r_data.json().get("data", [])
        return data  # type: ignore[no-any-return]

    def get_version(self, version_id: str) -> Dict[str, Any]:
        """
        Get details of a specific version of this source.

        Parameters
        ----------
        version_id : str
            The ID of the version to retrieve.

        Returns
        -------
        version : Dict[str, Any]
            Version details including files, environment, and configuration.
        """
        r_data = self._client.get(f"{self._path}{self.id}/versions/{version_id}/")
        data = r_data.json()
        return data  # type: ignore[no-any-return]

    def update_resources(
        self,
        resource_label: Optional[str] = None,
        replicas: Optional[int] = None,
        session_affinity: Optional[bool] = None,
        service_web_requests_on_root_path: Optional[bool] = None,
    ) -> CustomApplicationSource:
        """
        Update resource configuration for this source.

        Parameters
        ----------
        resource_label : Optional[str]
            Resource bundle ID (e.g., 'cpu.small', 'cpu.large').
        replicas : Optional[int]
            Number of replicas (1-4).
        session_affinity : Optional[bool]
            Whether to enable session affinity.
        service_web_requests_on_root_path : Optional[bool]
            Whether to serve requests on root path.

        Returns
        -------
        source : CustomApplicationSource
            The updated custom application source.
        """
        resources_payload: Dict[str, Any] = {}

        if resource_label is not None:
            resources_payload["resourceLabel"] = resource_label
        if replicas is not None:
            resources_payload["replicas"] = replicas
        if session_affinity is not None:
            resources_payload["sessionAffinity"] = session_affinity
        if service_web_requests_on_root_path is not None:
            resources_payload["serviceWebRequestsOnRootPath"] = service_web_requests_on_root_path

        if not resources_payload:
            return self  # No changes to make

        payload = {"resources": resources_payload}
        r_data = self._client.patch(f"{self._path}{self.id}/", data=payload)
        return self.from_server_data(r_data.json())

    def get_file(self, version_id: str, item_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific file from a version of this custom application source.

        Parameters
        ----------
        version_id : str
            The ID of the source version containing the file.
        item_id : str
            The ID of the file to download.

        Returns
        -------
        file_data : Dict[str, Any]
            The file information and content as a JSON object.

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomApplicationSource

            source = CustomApplicationSource.get("source_id")

            # Get the latest version
            versions = source.get_versions()
            version_id = versions[0]["id"]

            # Get a file from that version
            version_info = source.get_version(version_id)
            item_id = version_info["items"][0]["id"]
            file_data = source.get_file(version_id, item_id)

            print(f"File name: {file_data.get('fileName', 'Unknown')}")
            if 'content' in file_data:
                print(f"Content: {file_data['content']}")
        """
        url = f"{self._path}{self.id}/versions/{version_id}/items/{item_id}/"
        r_data = self._client.get(url)
        return r_data.json()  # type: ignore[no-any-return]
