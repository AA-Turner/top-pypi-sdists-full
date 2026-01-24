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
from datarobot.utils.pagination import unpaginate


class CustomApplicationResources(TypedDict):
    """Resource allocation for a Custom Application."""

    resource_label: str
    memory_request: int
    memory_limit: int
    cpu_request: float
    cpu_limit: int
    replicas: int
    session_affinity: bool
    service_web_requests_on_root_path: bool


# Trafaret validator for resources field (can be dict with all fields, or null)
# When resources are allocated, all fields are present. When not allocated, it's null.
_resources_validator = t.Or(
    t.Dict({
        t.Key("resource_label"): t.String,
        t.Key("memory_request"): t.Int,
        t.Key("memory_limit"): t.Int,
        t.Key("cpu_request"): t.Float,
        t.Key("cpu_limit"): t.Or(t.Int, t.Float),  # API sometimes returns float
        t.Key("replicas"): t.Int,
        t.Key("session_affinity"): t.Bool,
        t.Key("service_web_requests_on_root_path"): t.Bool,
    }).ignore_extra("*"),
    t.Null,
)


class CustomApplication(APIObject):
    """
    A DataRobot Custom Application with detailed resource information.

    This class provides access to the customApplications/ API endpoint which contains
    more detailed information than the basic applications/ endpoint, including
    resource allocation, status, and configuration details.

    Attributes
    ----------
    id : str
        The ID of the custom application.
    name : str
        The name of the custom application.
    env_version_id : str
        The environment version ID used by the application.
    custom_application_source_id : str
        The ID of the custom application source.
    custom_application_source_version_id : str
        The version ID of the custom application source.
    lrs_id : str
        The LRS (Lifecycle Resource Service) ID.
    status : str
        Current status of the application (e.g., 'running', 'stopped').
    user_id : str
        The ID of the user who created the application.
    org_id : str
        The organization ID.
    created_by : str
        Email of the user who created the application.
    creator_first_name : str
        First name of the creator.
    creator_last_name : str
        Last name of the creator.
    creator_userhash : str
        Userhash of the creator.
    permissions : List[str]
        List of permissions for the current user.
    created_at : str
        Timestamp when the application was created.
    updated_at : str
        Timestamp when the application was last updated.
    expires_at : Optional[str]
        Expiration timestamp, if any.
    application_url : str
        URL to access the application.
    external_access_enabled : bool
        Whether external access is enabled.
    allow_auto_stopping : bool
        Whether the application can be automatically stopped.
    external_access_recipients : List[str]
        List of external access recipients.
    resources : Optional[Dict[str, Any]]
        Resource allocation details including CPU, memory, and replicas. May be None if not allocated.
    required_key_scope_level : Optional[str]
        Required key scope level, if any.
    """

    _path = "customApplications/"

    _converter = t.Dict({
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("env_version_id"): t.String,
        t.Key("custom_application_source_id", optional=True): t.Or(t.String, t.Null),
        t.Key("custom_application_source_version_id", optional=True): t.Or(t.String, t.Null),
        t.Key("lrs_id"): t.String,
        t.Key("status"): t.String,
        t.Key("user_id"): t.String,
        t.Key("org_id"): t.String,
        t.Key("created_by"): t.String,
        t.Key("creator_first_name"): t.String,
        t.Key("creator_last_name"): t.String,
        t.Key("creator_userhash"): t.String,
        t.Key("permissions"): t.List(t.String),
        t.Key("created_at"): t.String,
        t.Key("updated_at"): t.String,
        t.Key("expires_at", optional=True): t.Or(t.String, t.Null),
        t.Key("application_url"): t.String,
        t.Key("external_access_enabled"): t.Bool,
        t.Key("allow_auto_stopping"): t.Bool,
        t.Key("external_access_recipients"): t.List(t.String),
        t.Key("resources", optional=True): _resources_validator,
        t.Key("required_key_scope_level", optional=True): t.Or(t.String, t.Null),
    }).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        env_version_id: str,
        lrs_id: str,
        status: str,
        user_id: str,
        org_id: str,
        created_by: str,
        creator_first_name: str,
        creator_last_name: str,
        creator_userhash: str,
        permissions: List[str],
        created_at: str,
        updated_at: str,
        application_url: str,
        external_access_enabled: bool,
        allow_auto_stopping: bool,
        external_access_recipients: List[str],
        custom_application_source_id: Optional[str] = None,
        custom_application_source_version_id: Optional[str] = None,
        expires_at: Optional[str] = None,
        resources: Optional[Dict[str, Any]] = None,
        required_key_scope_level: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.env_version_id = env_version_id
        self.custom_application_source_id = custom_application_source_id
        self.custom_application_source_version_id = custom_application_source_version_id
        self.lrs_id = lrs_id
        self.status = status
        self.user_id = user_id
        self.org_id = org_id
        self.created_by = created_by
        self.creator_first_name = creator_first_name
        self.creator_last_name = creator_last_name
        self.creator_userhash = creator_userhash
        self.permissions = permissions
        self.created_at = created_at
        self.updated_at = updated_at
        self.expires_at = expires_at
        self.application_url = application_url
        self.external_access_enabled = external_access_enabled
        self.allow_auto_stopping = allow_auto_stopping
        self.external_access_recipients = external_access_recipients
        self.resources = resources
        self.required_key_scope_level = required_key_scope_level

    def __repr__(self) -> str:
        return f"CustomApplication({self.name!r}, id={self.id!r})"

    @classmethod
    def list(
        cls,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[CustomApplication]:
        """
        Retrieve a list of custom applications.

        Parameters
        ----------
        offset : Optional[int]
            Optional. Retrieve applications in a list after this number.
        limit : Optional[int]
            Optional. Retrieve only this number of applications.

        Returns
        -------
        applications : List[CustomApplication]
            The requested list of custom applications.
        """
        query = {"offset": offset, "limit": limit}
        applications = unpaginate(initial_url=cls._path, initial_params=query, client=cls._client)
        return [cls.from_server_data(application) for application in applications]

    @classmethod
    def get(cls, application_id: str) -> CustomApplication:
        """
        Retrieve a single custom application with full details including resources.

        Parameters
        ----------
        application_id : str
            The ID of the custom application to retrieve.

        Returns
        -------
        application : CustomApplication
            The requested custom application with resource details.
        """
        r_data = cls._client.get(f"{cls._path}{application_id}/")
        return cls.from_server_data(r_data.json())

    def get_resources(self) -> Optional[Dict[str, Any]]:
        """
        Get resource allocation details for this custom application.

        Returns
        -------
        resources : Optional[Dict[str, Any]]
            Resource allocation including CPU, memory, replicas, and other settings.
            Returns None if no resources are allocated.
        """
        if self.resources is None or not isinstance(self.resources, dict):
            return None

        # Resources are already in snake_case format from the API client conversion
        return {
            "resource_label": self.resources.get("resource_label"),
            "memory_request": self.resources.get("memory_request"),
            "memory_limit": self.resources.get("memory_limit"),
            "cpu_request": self.resources.get("cpu_request"),
            "cpu_limit": self.resources.get("cpu_limit"),
            "replicas": self.resources.get("replicas"),
            "session_affinity": self.resources.get("session_affinity"),
            "service_web_requests_on_root_path": self.resources.get("service_web_requests_on_root_path"),
        }

    def get_resource_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get a human-readable summary of resource allocation.

        Returns
        -------
        summary : Optional[Dict[str, Any]]
            A summary of resource allocation with readable units.
            Returns None if no resources are allocated.
        """
        if self.resources is None or not isinstance(self.resources, dict):
            return None

        resources = self.resources

        # Convert bytes to more readable units
        memory_request_mb = resources.get("memory_request", 0) / (1024 * 1024)
        memory_limit_mb = resources.get("memory_limit", 0) / (1024 * 1024)

        return {
            "resource_bundle": resources.get("resource_label"),
            "cpu_allocation": {
                "request": resources.get("cpu_request"),
                "limit": resources.get("cpu_limit"),
            },
            "memory_allocation": {
                "request_mb": round(memory_request_mb, 2),
                "limit_mb": round(memory_limit_mb, 2),
                "request_gb": round(memory_request_mb / 1024, 2),
                "limit_gb": round(memory_limit_mb / 1024, 2),
            },
            "scaling": {
                "replicas": resources.get("replicas"),
                "session_affinity": resources.get("session_affinity"),
            },
            "networking": {
                "service_web_requests_on_root_path": resources.get("service_web_requests_on_root_path"),
            },
        }

    @property
    def is_running(self) -> bool:
        """
        Check if the custom application is currently running.

        Returns
        -------
        bool
            True if the application status is 'running', False otherwise.
        """
        return self.status.lower() == "running"

    def get_details(self) -> Dict[str, Any]:
        """
        Get comprehensive details about this custom application.

        Returns
        -------
        details : Dict[str, Any]
            Comprehensive application details including metadata and resources.
        """
        return {
            "basic_info": {
                "id": self.id,
                "name": self.name,
                "status": self.status,
                "application_url": self.application_url,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "expires_at": self.expires_at,
            },
            "creator_info": {
                "created_by": self.created_by,
                "creator_name": f"{self.creator_first_name} {self.creator_last_name}",
                "creator_userhash": self.creator_userhash,
            },
            "configuration": {
                "env_version_id": self.env_version_id,
                "custom_application_source_id": self.custom_application_source_id,
                "custom_application_source_version_id": self.custom_application_source_version_id,
                "external_access_enabled": self.external_access_enabled,
                "allow_auto_stopping": self.allow_auto_stopping,
                "external_access_recipients": self.external_access_recipients,
            },
            "resources": self.get_resource_summary(),
            "permissions": self.permissions,
        }

    @classmethod
    def get_by_name(cls, name: str) -> Optional[CustomApplication]:
        """
        Find a custom application by name.

        Parameters
        ----------
        name : str
            The name of the custom application to find.

        Returns
        -------
        application : Optional[CustomApplication]
            The custom application if found, None otherwise.
        """
        applications = cls.list()
        for app in applications:
            if app.name == name:
                return app
        return None

    def delete(self, hard_delete: bool = False) -> None:
        """
        Delete this custom application.

        Parameters
        ----------
        hard_delete : bool, optional
            If True, permanently delete the application and all its data.
            If False (default), soft delete the application (can be recovered).

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomApplication

            app = CustomApplication.get("app_id")
            app.delete()  # Soft delete
            app.delete(hard_delete=True)  # Permanent delete
        """
        params = {"hardDelete": hard_delete} if hard_delete else {}
        self._client.delete(f"{self._path}{self.id}/", params=params)

    def get_logs(self) -> Dict[str, Any]:
        """
        Retrieve logs and build information for this custom application.

        Returns
        -------
        logs_info : Dict[str, Any]
            Dictionary containing:
            - logs: List[str] - Application runtime logs (up to 1000 entries)
            - build_log: str - Build log of the custom application (optional)
            - build_status: str - Build status of the custom application (optional)
            - build_error: str - Build error message if build failed (optional)

        Examples
        --------
        .. code-block:: python

            from datarobot import CustomApplication

            app = CustomApplication.get("app_id")
            logs_info = app.get_logs()

            # Print runtime logs
            for log_line in logs_info['logs']:
                print(log_line)

            # Check build status
            if 'build_status' in logs_info:
                print(f"Build status: {logs_info['build_status']}")

            # Check for build errors
            if 'build_error' in logs_info:
                print(f"Build error: {logs_info['build_error']}")
        """
        r_data = self._client.get(f"{self._path}{self.id}/logs/")
        return r_data.json()  # type: ignore[no-any-return]
