#
# Copyright 2026 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, List, Optional, Type, TypeVar, cast

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.pipelines.enums import PipelineImageStatus
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict
from datarobot.utils.pagination import unpaginate

TPipelineImage = TypeVar("TPipelineImage", bound="PipelineImage")

_BASE_PATH = "pipelines/images/"


class PipelineImageVersion:
    """A single immutable version of a pipeline image.

    Attributes
    ----------
    version : int
        Monotonically increasing version number.
    definition : dict
        The canonical image definition (``name``, ``packages``,
        ``python_base_image``, ...) round-tripped from create/update.
    status : str
        Build status (CREATING, READY, ERROR).
    error_detail : str or None
        Build error message when status is ERROR.
    image_uri : str or None
        The built image URI, populated once the build completes successfully.
    created_at : str
        When the version was created.
    updated_at : str
        When the version was last updated.
    """

    def __init__(
        self,
        version: int,
        status: PipelineImageStatus,
        definition: Optional[Dict[str, Any]] = None,
        error_detail: Optional[str] = None,
        image_uri: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.version = version
        self.definition = definition or {}
        self.status = status
        self.error_detail = error_detail
        self.image_uri = image_uri
        self.created_at = created_at
        self.updated_at = updated_at

    @property
    def packages(self) -> List[str]:
        """Pip package specifiers from the image definition."""
        return list(self.definition.get("packages") or [])

    def __repr__(self) -> str:
        return f"PipelineImageVersion(version={self.version}, status={self.status!r})"


class PipelineImage(APIObject):
    """A named execution image for pipeline dispatches.

    Attributes
    ----------
    image_id : str
        The image ID.
    name : str
        User-provided image name (unique per user).
    description : str or None
        Optional description.
    latest_version : int
        Highest version number currently registered.
    latest_status : str or None
        Build status of the latest version (in list responses).
    versions : list of PipelineImageVersion
        All versions (in detail responses).
    created_at : str
        When the image was created.
    updated_at : str
        When the image was last updated.
    """

    _path = _BASE_PATH

    _converter = t.Dict({
        t.Key("id", to_name="image_id"): String(),
        t.Key("name"): String(),
        t.Key("description", optional=True, default=None): t.Or(String(allow_blank=True), t.Null()),
        t.Key("latest_version"): t.Int(),
        t.Key("latest_status", optional=True, default=None): t.Or(
            t.Enum(*enum_to_list(PipelineImageStatus)),
            t.Null(),
        ),
        t.Key("versions", optional=True, default=None): t.Or(t.List(t.Dict().allow_extra("*")), t.Null()),
        t.Key("created_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("updated_at", optional=True, default=None): t.Or(String(), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        image_id: str,
        name: str,
        latest_version: int,
        description: Optional[str] = None,
        latest_status: Optional[PipelineImageStatus] = None,
        versions: Optional[List[Dict[str, Any]]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.image_id = image_id
        self.name = name
        self.description = description
        self.latest_version = latest_version
        self.latest_status = latest_status
        self.versions = [PipelineImageVersion(**v) for v in versions] if versions else []
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"PipelineImage({self.name!r}, id={self.image_id!r})"

    @classmethod
    def create(
        cls: Type[TPipelineImage],
        name: str,
        packages: List[str],
        python_base_image: Optional[str] = None,
        description: Optional[str] = None,
    ) -> TPipelineImage:
        """Create a named execution image with an initial build.

        Parameters
        ----------
        name : str
            Image name (unique per user).
        packages : list of str
            Pip package specifiers (e.g., ['numpy>=1.24', 'pandas']).
        python_base_image : str, optional
            Base Docker image to build on top of.
        description : str, optional
            Human-readable description.

        Returns
        -------
        image : PipelineImage
        """
        data: Dict[str, Any] = {"name": name, "packages": packages}
        if python_base_image is not None:
            data["python_base_image"] = python_base_image
        if description is not None:
            data["description"] = description
        response = cls._client.post(cls._path, data=rawdict(data))
        return cls.from_server_data(response.json())

    @classmethod
    def get(
        cls: Type[TPipelineImage],
        image_id: str,
    ) -> TPipelineImage:
        """Get an image by ID.

        Parameters
        ----------
        image_id : str
            The image ID.

        Returns
        -------
        image : PipelineImage
        """
        response = cls._client.get(f"{cls._path}{image_id}/")
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls: Type[TPipelineImage],
    ) -> List[TPipelineImage]:
        """List the caller's active images.

        Transparently follows pagination and returns the complete result set.

        Returns
        -------
        images : list of PipelineImage
        """
        return [cls.from_server_data(item) for item in unpaginate(cls._path, None, cls._client)]

    def update(
        self: TPipelineImage,
        packages: List[str],
        name: Optional[str] = None,
        python_base_image: Optional[str] = None,
    ) -> TPipelineImage:
        """Create a new immutable version of this image.

        The PATCH body is a complete redefinition (not a merge): the new
        version carries exactly the definition supplied here. Because the
        server requires ``name``, it defaults to this image's current name
        when not provided.

        Parameters
        ----------
        packages : list of str
            Pip package specifiers for the new version.
        name : str, optional
            Image name. Defaults to this image's current name.
        python_base_image : str, optional
            Base Docker image to build on top of.

        Returns
        -------
        image : PipelineImage
            The updated image with the new version.
        """
        data: Dict[str, Any] = {"name": name or self.name, "packages": packages}
        if python_base_image is not None:
            data["python_base_image"] = python_base_image
        response = self._client.patch(
            f"{self._path}{self.image_id}/",
            data=rawdict(data),
        )
        updated = self.from_server_data(response.json())
        self.__dict__.update(updated.__dict__)
        return self

    def delete(self) -> None:
        """Soft-delete the most recent active version of this image.

        If no active versions remain, the image is deleted as well.
        """
        self._client.delete(f"{self._path}{self.image_id}/")

    def delete_version(self, version_id: int) -> None:
        """Soft-delete a specific version of this image.

        Parameters
        ----------
        version_id : int
            The version number to delete.
        """
        self._client.delete(f"{self._path}{self.image_id}/versions/{version_id}/")

    def get_version_logs(self, version_id: int) -> str:
        """Get the raw build logs for a specific version of this image.

        Parameters
        ----------
        version_id : int
            The version number.

        Returns
        -------
        logs : str
            The raw build output.
        """
        response = self._client.get(f"{self._path}{self.image_id}/versions/{version_id}/logs/")
        return cast(str, response.json().get("logs") or "")
