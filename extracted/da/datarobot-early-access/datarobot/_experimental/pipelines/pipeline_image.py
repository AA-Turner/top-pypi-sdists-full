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

from typing import Any, Dict, List, Optional, Type, TypeVar

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.pipelines.enums import PipelineImageStatus
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict

TPipelineImage = TypeVar("TPipelineImage", bound="PipelineImage")

_BASE_PATH = "pipelines/images/"


class PipelineImageVersion:
    """A single immutable version of a pipeline image.

    Attributes
    ----------
    version : int
        Monotonically increasing version number.
    packages : list of str
        Pip package specifiers for this version.
    status : str
        Build status (CREATING, READY, ERROR).
    error_detail : str or None
        Build error message when status is ERROR.
    created_at : str
        When the version was created.
    updated_at : str
        When the version was last updated.
    """

    def __init__(
        self,
        version: int,
        packages: List[str],
        status: PipelineImageStatus,
        error_detail: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.version = version
        self.packages = packages
        self.status = status
        self.error_detail = error_detail
        self.created_at = created_at
        self.updated_at = updated_at

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
        description: Optional[str] = None,
    ) -> TPipelineImage:
        """Create a named execution image with an initial build.

        Parameters
        ----------
        name : str
            Image name (unique per user).
        packages : list of str
            Pip package specifiers (e.g., ['numpy>=1.24', 'pandas']).
        description : str, optional
            Human-readable description.

        Returns
        -------
        image : PipelineImage
        """
        data: Dict[str, Any] = {"name": name, "packages": packages}
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
        offset: int = 0,
        limit: int = 50,
    ) -> List[TPipelineImage]:
        """List the caller's active images.

        Parameters
        ----------
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        images : list of PipelineImage
        """
        params: Dict[str, int] = {"offset": offset, "limit": limit}
        response = cls._client.get(cls._path, params=params)
        return [cls.from_server_data(item) for item in response.json().get("data", [])]

    def update(
        self: TPipelineImage,
        packages: List[str],
    ) -> TPipelineImage:
        """Add packages to this image, creating a new immutable version.

        Parameters
        ----------
        packages : list of str
            Pip package specifiers to merge into the latest version.

        Returns
        -------
        image : PipelineImage
            The updated image with the new version.
        """
        response = self._client.patch(
            f"{self._path}{self.image_id}/",
            data=rawdict({"packages": packages}),
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
