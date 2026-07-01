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

"""Client models for Custom Scoring Metrics (registry containers and versions)."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union

from requests_toolbelt import MultipartEncoder
import trafaret as t

from datarobot.models.api_object import APIObject

METRICS_URL = "customScoringMetrics/"
VERSIONS_URL = "customScoringMetrics/{metric_id}/versions/"
VERSION_FILES_URL = "customScoringMetrics/{registry_id}/versions/{registry_version_id}/files/"

_custom_scoring_metric_tag = t.Dict({
    t.Key("name"): t.String(),
    t.Key("value"): t.String(),
}).allow_extra("*")

_metric_dict = t.Dict({
    t.Key("label"): t.String(),
    t.Key("lower_is_better", optional=True): t.Bool(),
    t.Key("description", optional=True): t.String(),
    t.Key("entry_point"): t.String(),
    t.Key("primary_metric"): t.Bool(),
    t.Key("use_weights", optional=True): t.Bool(),
}).allow_extra("*")


def _initialize_custom_scoring_metric_attributes(
    metric: "CustomScoringMetric",
    **fields: Union[str, int, bool, List[Dict[str, str]], None],
) -> None:
    """Populate ``CustomScoringMetric`` instance attributes from constructor arguments."""
    for attr, value in fields.items():
        setattr(metric, attr, value)


class CustomScoringMetric(APIObject):
    """A versioned custom scoring metric container.

    Attributes
    ----------
    id : str
        Unique identifier.
    name : str
        Display name of the metric.
    target_type : str
        The target type this metric applies to (e.g. Binary, Regression, Multiclass).
    user_id : str or None
        ID of the user who created the metric.
    organization_id : str or None
        ID of the owning organization.
    description : str or None
        Optional description.
    latest_version_num : int
        The highest version number that has been created.
    is_archived : bool
        Whether the metric has been soft-deleted.
    created_at : str or None
        ISO-8601 creation timestamp.
    updated_at : str or None
        ISO-8601 last-updated timestamp.
    tags : list of dict
        Tag entries, each ``{"name": str, "value": str}`` (additional keys allowed).
    """

    id: str  # pylint: disable=invalid-name
    name: str
    target_type: str
    user_id: str
    organization_id: Optional[str]
    description: Optional[str]
    latest_version_num: int
    is_archived: bool
    created_at: Optional[str]
    updated_at: Optional[str]
    tags: List[Dict[str, str]]

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("name"): t.String(),
        t.Key("target_type"): t.String(),
        t.Key("user_id", optional=True): t.String(),
        t.Key("organization_id", optional=True): t.String(),
        t.Key("description", optional=True): t.String(),
        t.Key("latest_version_num", optional=True): t.Int(),
        t.Key("is_archived", optional=True): t.Bool(),
        t.Key("created_at", optional=True): t.String(),
        t.Key("updated_at", optional=True): t.String(),
        t.Key("tags", optional=True): t.Or(t.List(_custom_scoring_metric_tag), t.Null()),
    }).ignore_extra("*")

    def __init__(  # pylint: disable=too-many-arguments,redefined-builtin,invalid-name
        self,
        id: str,
        name: str,
        target_type: str,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        description: Optional[str] = None,
        latest_version_num: int = 0,
        is_archived: bool = False,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        _initialize_custom_scoring_metric_attributes(
            self,
            id=id,
            name=name,
            target_type=target_type,
            user_id=user_id or "",
            organization_id=organization_id,
            description=description,
            latest_version_num=latest_version_num,
            is_archived=is_archived,
            created_at=created_at,
            updated_at=updated_at,
            tags=tags or [],
        )

    def __repr__(self) -> str:
        return f"CustomScoringMetric(name={self.name!r}, target_type={self.target_type!r})"

    @classmethod
    def list(  # pylint: disable=too-many-arguments
        cls,
        offset: int = 0,
        limit: int = 20,
        target_type: Optional[str] = None,
        search: Optional[str] = None,
        is_archived: bool = False,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> List["CustomScoringMetric"]:
        """List custom scoring metrics.

        Parameters
        ----------
        offset : int
            Number of records to skip.
        limit : int
            Maximum number of records to return.
        target_type : str, optional
            Filter by target type (e.g. "Binary", "Regression", "Multiclass").
        search : str, optional
            Filter by name sub-string.
        is_archived : bool
            When True, return only archived metrics. When False (default), non-archived
            metrics are returned and ``isArchived`` is omitted from the list request.
        tags : list of dict, optional
            Tag entries shaped as ``{"name": ..., "value": ...}``.

        Returns
        -------
        list[CustomScoringMetric]
        """
        params: Dict[str, Union[int, str, bool, List[Dict[str, str]]]] = {
            "offset": offset,
            "limit": limit,
        }
        if is_archived:
            params["isArchived"] = True
        if target_type is not None:
            params["targetType"] = target_type
        if search is not None:
            params["search"] = search
        if tags is not None:
            params["tags"] = tags
        response = cls._client.get(METRICS_URL, params=params)
        return [cls.from_server_data(item) for item in response.json()["data"]]

    @classmethod
    def create(
        cls,
        name: str,
        target_type: str,
        description: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> "CustomScoringMetric":
        """Create a new custom scoring metric container.

        Parameters
        ----------
        name : str
            Display name for the metric.
        target_type : str
            Target type this metric applies to.
        description : str, optional
            Optional description.
        tags : list of dict, optional
            Tag entries shaped as ``{"name": ..., "value": ...}``.

        Returns
        -------
        CustomScoringMetric
        """
        payload: Dict[str, Union[str, List[Dict[str, str]]]] = {
            "name": name,
            "targetType": target_type,
        }
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags
        response = cls._client.post(METRICS_URL, data=payload)
        return cls.from_server_data(response.json())

    @classmethod
    def get(cls, metric_id: str) -> "CustomScoringMetric":
        """Retrieve a custom scoring metric by ID.

        Parameters
        ----------
        metric_id : str
            The ID of the metric to retrieve.

        Returns
        -------
        CustomScoringMetric
        """
        response = cls._client.get(f"{METRICS_URL}{metric_id}/")
        return cls.from_server_data(response.json())

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> "CustomScoringMetric":
        """Update the name, description, or tags of this metric.

        Parameters
        ----------
        name : str, optional
            New display name.
        description : str, optional
            New description.
        tags : list of dict, optional
            Replacement tags, each ``{"name": ..., "value": ...}``.

        Returns
        -------
        CustomScoringMetric
            This instance, updated in place.
        """
        payload: Dict[str, Union[str, List[Dict[str, str]]]] = {}
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if tags is not None:
            payload["tags"] = tags
        response = self._client.patch(f"{METRICS_URL}{self.id}/", data=payload)
        self.__dict__.update(self.from_server_data(response.json()).__dict__)
        return self

    def delete(self) -> None:
        """Archive (soft-delete) this metric."""
        self._client.delete(f"{METRICS_URL}{self.id}/")


class CustomScoringMetricVersionFileContents(APIObject):
    """Raw file contents (metadata + code) backing a custom scoring metric version.

    Attributes
    ----------
    metadata_file_name : str
        Stored name of the metadata file (e.g. ``metadata.yml`` or ``metadata.yaml``).
    metadata_file_contents : str
        Raw UTF-8 contents of the metadata file.
    code_file_name : str
        Stored name of the Python file (e.g. ``custom_metrics.py``).
    code_file_contents : str
        Raw UTF-8 contents of the custom metrics Python file.
    """

    metadata_file_name: str
    metadata_file_contents: str
    code_file_name: str
    code_file_contents: str

    _converter = t.Dict({
        t.Key("metadata_file_name"): t.String(),
        t.Key("metadata_file_contents"): t.String(allow_blank=True),
        t.Key("code_file_name"): t.String(),
        t.Key("code_file_contents"): t.String(allow_blank=True),
    }).ignore_extra("*")

    def __init__(
        self,
        metadata_file_name: str,
        metadata_file_contents: str,
        code_file_name: str,
        code_file_contents: str,
    ) -> None:
        self.metadata_file_name = metadata_file_name
        self.metadata_file_contents = metadata_file_contents
        self.code_file_name = code_file_name
        self.code_file_contents = code_file_contents

    def __repr__(self) -> str:
        return (
            f"CustomScoringMetricVersionFileContents("
            f"metadata_file_name={self.metadata_file_name!r}, "
            f"code_file_name={self.code_file_name!r})"
        )


class CustomScoringMetricVersion(APIObject):  # pylint: disable=too-many-instance-attributes
    """A single version of a custom scoring metric.

    Versions are created by uploading a ``metadata.yml`` and ``custom_metrics.py``
    file pair. Each new version receives the next sequential version number.

    Attributes
    ----------
    id : str
        Unique identifier of this version.
    custom_scoring_metric_registry_id : str
        ID of the parent metric container.
    version_num : int or None
        Sequential version number assigned on creation.
    files_catalog_id : str or None
        ID of the files catalog entry storing the uploaded files.
    files_catalog_version_id : str or None
        ID of the specific catalog version.
    metrics : list
        Metric definitions parsed from the uploaded metadata.
    stage : str or None
        Lifecycle stage of this version.
    description : str or None
        Optional description provided at upload time.
    validation_status : str or None
        Status of server-side validation of the uploaded files.
    user_id : str or None
        ID of the user who created this version.
    """

    _converter = t.Dict({
        t.Key("id"): t.String(),
        t.Key("custom_scoring_metric_registry_id"): t.String(),
        t.Key("version_num", optional=True): t.Int(),
        t.Key("files_catalog_id", optional=True): t.String(),
        t.Key("files_catalog_version_id", optional=True): t.String(),
        t.Key("metrics", optional=True): t.List(_metric_dict),
        t.Key("stage", optional=True): t.String(),
        t.Key("description", optional=True): t.String(),
        t.Key("validation_status", optional=True): t.String(),
        t.Key("user_id", optional=True): t.String(),
    }).ignore_extra("*")

    def __init__(  # pylint: disable=too-many-arguments,redefined-builtin,invalid-name
        self,
        id: str,
        custom_scoring_metric_registry_id: str,
        version_num: Optional[int] = None,
        files_catalog_id: Optional[str] = None,
        files_catalog_version_id: Optional[str] = None,
        metrics: Optional[List[Dict[str, Union[str, bool]]]] = None,
        stage: Optional[str] = None,
        description: Optional[str] = None,
        validation_status: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        self.id = id  # pylint: disable=invalid-name
        self.custom_scoring_metric_registry_id = custom_scoring_metric_registry_id
        self.version_num = version_num
        self.files_catalog_id = files_catalog_id
        self.files_catalog_version_id = files_catalog_version_id
        self.metrics = metrics or []
        self.stage = stage
        self.description = description
        self.validation_status = validation_status
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"CustomScoringMetricVersion(id={self.id!r}, version_num={self.version_num!r})"

    @classmethod
    def list(
        cls,
        metric_id: str,
        offset: int = 0,
        limit: int = 20,
    ) -> List["CustomScoringMetricVersion"]:
        """List all versions for a given custom scoring metric.

        Parameters
        ----------
        metric_id : str
            ID of the parent metric container.
        offset : int
            Number of records to skip.
        limit : int
            Maximum number of records to return.

        Returns
        -------
        list[CustomScoringMetricVersion]
        """
        url = VERSIONS_URL.format(metric_id=metric_id)
        response = cls._client.get(url, params={"offset": offset, "limit": limit})
        return [cls.from_server_data(item) for item in response.json()["data"]]

    @classmethod
    def create(
        cls,
        metric_id: str,
        metadata_file_path: str,
        code_file_path: str,
        description: Optional[str] = None,
    ) -> "CustomScoringMetricVersion":
        """Upload a new version of a custom scoring metric.

        Sends ``metadata.yml`` and ``custom_metrics.py`` as multipart form data.

        Parameters
        ----------
        metric_id : str
            ID of the parent metric container.
        metadata_file_path : str
            Local path to the ``metadata.yml`` file.
        code_file_path : str
            Local path to the ``custom_metrics.py`` file.
        description : str, optional
            Optional description for this version.

        Returns
        -------
        CustomScoringMetricVersion
        """
        url = VERSIONS_URL.format(metric_id=metric_id)

        with open(metadata_file_path, "rb") as meta_f:
            metadata_content = meta_f.read()

        with open(code_file_path, "rb") as code_f:
            code_content = code_f.read()

        fields: Dict[str, Union[str, Tuple[str, bytes]]] = {
            "metadataFile": ("metadata.yml", metadata_content),
            "codeFile": ("custom_metrics.py", code_content),
        }
        if description is not None:
            fields["description"] = description
        encoder = MultipartEncoder(fields=fields)
        response = cls._client.request(
            "post",
            url,
            headers={"Content-Type": encoder.content_type},
            data=encoder,
        )
        return cls.from_server_data(response.json())

    @classmethod
    def get(cls, metric_id: str, version_id: str) -> "CustomScoringMetricVersion":
        """Retrieve a specific version of a custom scoring metric.

        Parameters
        ----------
        metric_id : str
            ID of the parent metric container.
        version_id : str
            ID of the version to retrieve.

        Returns
        -------
        CustomScoringMetricVersion
        """
        url = f"{VERSIONS_URL.format(metric_id=metric_id)}{version_id}/"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())

    def delete(self) -> None:
        """Delete this version."""
        url = f"{VERSIONS_URL.format(metric_id=self.custom_scoring_metric_registry_id)}{self.id}/"
        self._client.delete(url)

    @classmethod
    def get_file_contents(cls, registry_id: str, registry_version_id: str) -> "CustomScoringMetricVersionFileContents":
        """Retrieve the raw metadata and code file contents for a version.

        Parameters
        ----------
        registry_id : str
            ID of the parent custom scoring metric registry.
        registry_version_id : str
            ID of the registry version whose files should be retrieved.

        Returns
        -------
        CustomScoringMetricVersionFileContents
        """
        url = VERSION_FILES_URL.format(registry_id=registry_id, registry_version_id=registry_version_id)
        response = cls._client.get(url)
        return CustomScoringMetricVersionFileContents.from_server_data(response.json())

    def get_files(self) -> "CustomScoringMetricVersionFileContents":
        """Retrieve the raw metadata and code file contents for this version.

        Returns
        -------
        CustomScoringMetricVersionFileContents
        """
        return self.get_file_contents(self.custom_scoring_metric_registry_id, self.id)
