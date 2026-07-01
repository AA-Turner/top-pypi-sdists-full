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

from os.path import basename
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, cast

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.pipelines.enums import PipelineMode, PipelineVersionStatus
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject

TPipeline = TypeVar("TPipeline", bound="Pipeline")


class PipelineVersion:
    """A specific version of a pipeline.

    Attributes
    ----------
    version : int
        The version number.
    status : str
        The version status (PENDING, READY, FAILED).
    task_names : list or None
        The names of ``@task`` functions in the pipeline.
    python_version : str
        The Python version the pipeline was parsed with.
    resource_bundle : dict or None
        Resource configuration for the version.
    error_detail : str or None
        Error message if the version failed parsing.
    created_at : str
        When the version was created.
    """

    def __init__(
        self,
        version: int,
        status: PipelineVersionStatus,
        python_version: Optional[str] = None,
        task_names: Optional[List[str]] = None,
        resource_bundle: Optional[Dict[str, Any]] = None,
        error_detail: Optional[str] = None,
        created_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.version = version
        self.status = status
        self.python_version = python_version
        self.task_names = task_names
        self.resource_bundle = resource_bundle
        self.error_detail = error_detail
        self.created_at = created_at

    def __repr__(self) -> str:
        return f"PipelineVersion(version={self.version}, status={self.status!r})"


class TaskParameter:
    """A single parameter from a ``@task`` function signature.

    Attributes
    ----------
    name : str
        The parameter name.
    annotation : str or None
        The type annotation as written in source, or None if unannotated.
    """

    def __init__(self, name: str, annotation: Optional[str] = None, **kwargs: Any) -> None:
        self.name = name
        self.annotation = annotation

    def __repr__(self) -> str:
        return f"TaskParameter(name={self.name!r}, annotation={self.annotation!r})"


class PipelineTask:
    """Per-task detail for a node in a pipeline DAG.

    The numeric ``task_id`` is a 1-based integer scoped per pipeline (the
    same shape as version numbers). Discover task IDs from the ``taskId``
    field on each node of a graph response (see :meth:`Pipeline.get_graph`).

    Attributes
    ----------
    task_id : int
        The 1-based numeric task ID, scoped per pipeline.
    pipeline_id : str
        The ID of the pipeline this task belongs to.
    version_id : int or None
        The version number for a locked-version task, or None for a draft task.
    name : str
        The ``@task`` function name.
    parameters : list of TaskParameter
        The function signature parameters.
    inputs : dict or None
        The pipeline inputs payload from the latest VALID input for the version.
        Always None for draft tasks -- inputs only exist once a version is locked.
    source : str
        The source code of the ``@task`` function.
    resource_bundle : dict or None
        Resource configuration for the task (None until executor AST extraction lands).
    task_group_id : int or None
        The task group ID (None until task-grouping lands).
    """

    def __init__(
        self,
        task_id: int,
        pipeline_id: str,
        name: str,
        source: str,
        version_id: Optional[int] = None,
        parameters: Optional[List[TaskParameter]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        resource_bundle: Optional[Dict[str, Any]] = None,
        task_group_id: Optional[int] = None,
    ) -> None:
        self.task_id = task_id
        self.pipeline_id = pipeline_id
        self.version_id = version_id
        self.name = name
        self.parameters = parameters or []
        self.inputs = inputs
        self.source = source
        self.resource_bundle = resource_bundle
        self.task_group_id = task_group_id

    @classmethod
    def from_server_data(cls, data: Dict[str, Any]) -> "PipelineTask":
        """Build a PipelineTask from a raw (camelCase) task detail response.

        ``inputs`` is preserved verbatim rather than running through the
        SDK's camelCase-to-snake_case conversion, since its keys are
        user-supplied pipeline input names.
        """
        parameters = [
            TaskParameter(name=p["name"], annotation=p.get("annotation")) for p in (data.get("parameters") or [])
        ]
        return cls(
            task_id=data["id"],
            pipeline_id=data["pipelineId"],
            version_id=data.get("versionId"),
            name=data["name"],
            parameters=parameters,
            inputs=data.get("inputs"),
            source=data["source"],
            resource_bundle=data.get("resourceBundle"),
            task_group_id=data.get("taskGroupId"),
        )

    def __repr__(self) -> str:
        return f"PipelineTask(task_id={self.task_id}, name={self.name!r})"


class Pipeline(APIObject):
    """A pipeline created from an uploaded workflow file.

    Attributes
    ----------
    pipeline_id : str
        The ID of the pipeline.
    name : str
        Human-readable display name of the pipeline.
    description : str or None
        The pipeline description.
    mode : str
        The pipeline mode (draft or locked).
    is_active : bool
        Whether the pipeline is active (not deleted).
    latest_version : int or None
        The latest version number (in list responses).
    task_names : list or None
        The names of ``@task`` functions in the pipeline (in detail responses).
    python_version : str or None
        The Python version the workflow was parsed with (in detail responses).
    resource_bundle : dict or None
        Resource configuration for the draft pipeline (in detail responses).
    versions : list
        List of PipelineVersion objects (in detail responses).
    created_at : str
        When the pipeline was created.
    updated_at : str
        When the pipeline was last updated.
    """

    _path = "pipelines/"

    _converter = t.Dict({
        t.Key("id", to_name="pipeline_id"): String(),
        t.Key("name"): String(),
        t.Key("description", optional=True, default=None): t.Or(String(allow_blank=True), t.Null()),
        t.Key("mode", optional=True, default=None): t.Or(t.Enum(*enum_to_list(PipelineMode)), t.Null()),
        t.Key("is_active", optional=True, default=None): t.Or(t.Bool(), t.Null()),
        t.Key("version", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("status", optional=True, default=None): t.Or(t.Enum(*enum_to_list(PipelineVersionStatus)), t.Null()),
        t.Key("latest_version", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("task_names", optional=True, default=None): t.Or(t.List(String()), t.Null()),
        t.Key("python_version", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("resource_bundle", optional=True, default=None): t.Or(t.Dict().allow_extra("*"), t.Null()),
        t.Key("versions", optional=True, default=None): t.Or(t.List(t.Dict().allow_extra("*")), t.Null()),
        t.Key("created_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("updated_at", optional=True, default=None): t.Or(String(), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        pipeline_id: str,
        name: str,
        description: Optional[str] = None,
        mode: Optional[PipelineMode] = None,
        is_active: Optional[bool] = None,
        version: Optional[int] = None,
        status: Optional[PipelineVersionStatus] = None,
        latest_version: Optional[int] = None,
        task_names: Optional[List[str]] = None,
        python_version: Optional[str] = None,
        resource_bundle: Optional[Dict[str, Any]] = None,
        versions: Optional[List[Dict[str, Any]]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.pipeline_id = pipeline_id
        self.name = name
        self.description = description
        self.mode = mode
        self.is_active = is_active
        self.version = version
        self.status = status
        self.latest_version = latest_version
        self.task_names = task_names
        self.python_version = python_version
        self.resource_bundle = resource_bundle
        self.versions = [PipelineVersion(**v) for v in versions] if versions else []
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"Pipeline({self.name!r}, id={self.pipeline_id!r})"

    @classmethod
    def create(
        cls: Type[TPipeline],
        file_path: str,
        description: Optional[str] = None,
    ) -> TPipeline:
        """Upload a .py workflow file to create a pipeline.

        Pipelines are always created in draft mode. Call :meth:`promote`
        to lock the pipeline and cut a version.

        Parameters
        ----------
        file_path : str
            Path to the .py file containing @task and @pipeline decorated functions.
        description : str, optional
            Description of the pipeline.

        Returns
        -------
        pipeline : Pipeline
            The created pipeline.

        Raises
        ------
        FileNotFoundError
            If ``file_path`` does not exist.
        IsADirectoryError
            If ``file_path`` refers to a directory rather than a file.
        PermissionError
            If the process lacks permission to read ``file_path``.
        OSError
            For any other I/O error opening or reading ``file_path``.
        """
        with open(file_path, "rb") as f:
            files = {"file": (basename(file_path), f, "application/octet-stream")}
            data: Dict[str, str] = {}
            if description is not None:
                data["description"] = description
            response = cls._client.request(
                method="POST",
                url=cls._path,
                files=files,
                data=data,
            )
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls: Type[TPipeline],
        mode: Optional[PipelineMode] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[TPipeline]:
        """List all pipelines.

        Parameters
        ----------
        mode : str, optional
            Filter by mode ('draft' or 'locked').
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        pipelines : list of Pipeline
        """
        params: Dict[str, Union[int, str]] = {"offset": offset, "limit": limit}
        if mode is not None:
            params["mode"] = mode
        response = cls._client.get(cls._path, params=params)
        data = response.json()
        return [cls.from_server_data(item) for item in data.get("data", [])]

    @classmethod
    def get(cls: Type[TPipeline], pipeline_id: str) -> TPipeline:
        """Get a pipeline by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        pipeline : Pipeline
        """
        response = cls._client.get(f"{cls._path}{pipeline_id}/")
        return cls.from_server_data(response.json())

    def update(self: TPipeline, file_path: str) -> TPipeline:
        """Update a draft pipeline by re-uploading the .py file.

        Parameters
        ----------
        file_path : str
            Path to the updated .py file.

        Returns
        -------
        pipeline : Pipeline
            The updated pipeline.

        Raises
        ------
        FileNotFoundError
            If ``file_path`` does not exist.
        IsADirectoryError
            If ``file_path`` refers to a directory rather than a file.
        PermissionError
            If the process lacks permission to read ``file_path``.
        OSError
            For any other I/O error opening or reading ``file_path``.
        """
        with open(file_path, "rb") as f:
            files = {"file": (basename(file_path), f, "application/octet-stream")}
            response = self._client.request(
                method="PATCH",
                url=f"{self._path}{self.pipeline_id}/",
                files=files,
            )
        updated = self.from_server_data(response.json())
        self.__dict__.update(updated.__dict__)
        return self

    def delete(self) -> None:
        """Soft-delete this pipeline."""
        self._client.delete(f"{self._path}{self.pipeline_id}/")

    def promote(self: TPipeline) -> TPipeline:
        """Promote this pipeline from draft to locked.

        Returns
        -------
        pipeline : Pipeline
            The promoted pipeline.
        """
        response = self._client.patch(f"{self._path}{self.pipeline_id}/mode/")
        updated = self.from_server_data(response.json())
        self.__dict__.update(updated.__dict__)
        return self

    def list_versions(
        self,
        offset: int = 0,
        limit: int = 50,
    ) -> List[PipelineVersion]:
        """List all versions of this pipeline.

        Parameters
        ----------
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        versions : list of PipelineVersion
        """
        params: Dict[str, int] = {"offset": offset, "limit": limit}
        response = self._client.get(f"{self._path}{self.pipeline_id}/versions/", params=params)
        return [PipelineVersion(**v) for v in response.json().get("data", [])]

    def get_version(self, version_id: int) -> PipelineVersion:
        """Get a specific version of this pipeline.

        Parameters
        ----------
        version_id : int
            The version number.

        Returns
        -------
        version : PipelineVersion
        """
        response = self._client.get(f"{self._path}{self.pipeline_id}/versions/{version_id}/")
        return PipelineVersion(**response.json())

    def get_graph(self) -> Dict[str, Any]:
        """Get the DAG of the draft pipeline.

        Returns
        -------
        graph : dict
            JSON representation of the pipeline DAG.
        """
        response = self._client.get(f"{self._path}{self.pipeline_id}/graph/")
        return cast(Dict[str, Any], response.json())

    def get_version_graph(self, version_id: int) -> Dict[str, Any]:
        """Get the DAG of a specific pipeline version.

        Parameters
        ----------
        version_id : int
            The version number.

        Returns
        -------
        graph : dict
            JSON representation of the pipeline DAG.
        """
        response = self._client.get(f"{self._path}{self.pipeline_id}/versions/{version_id}/graph/")
        return cast(Dict[str, Any], response.json())

    def get_task(self, task_id: int) -> PipelineTask:
        """Get per-task detail for a task in the draft pipeline.

        Parameters
        ----------
        task_id : int
            The 1-based numeric task ID. Discover IDs from the ``taskId``
            field on each node of :meth:`get_graph`.

        Returns
        -------
        task : PipelineTask
            Task detail including source, function signature, and parameters.
            ``inputs`` is always None for draft tasks.
        """
        response = self._client.get(f"{self._path}{self.pipeline_id}/tasks/{task_id}/")
        return PipelineTask.from_server_data(response.json())

    def get_version_task(self, version_id: int, task_id: int) -> PipelineTask:
        """Get per-task detail for a task in a specific locked pipeline version.

        Parameters
        ----------
        version_id : int
            The version number.
        task_id : int
            The 1-based numeric task ID. Discover IDs from the ``taskId``
            field on each node of :meth:`get_version_graph`.

        Returns
        -------
        task : PipelineTask
            Task detail including source, function signature, parameters, and
            the latest VALID pipeline inputs payload for that version.
        """
        response = self._client.get(f"{self._path}{self.pipeline_id}/versions/{version_id}/tasks/{task_id}/")
        return PipelineTask.from_server_data(response.json())
