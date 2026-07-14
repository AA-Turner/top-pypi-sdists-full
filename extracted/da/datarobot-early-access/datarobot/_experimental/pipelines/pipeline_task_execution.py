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
from datarobot._experimental.pipelines.enums import TaskExecutionStatus
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict

TPipelineTaskExecution = TypeVar("TPipelineTaskExecution", bound="PipelineTaskExecution")

_BASE_PATH = "pipelines/"


class TaskExecutionResult:
    """A completed task's result, as a presigned S3 URL plus a JSON preview.

    Attributes
    ----------
    url : str
        Presigned ``https://`` URL granting one-shot access to the cloudpickled
        ``result.tobj`` blob. Decode the downloaded bytes with
        ``cloudpickle.loads(response.content)``.
    expires_in : int
        Validity window in seconds from the moment the URL was signed.
    content_type : str
        MIME type the URL serves (``application/octet-stream``).
    value : Any or None
        JSON-decoded preview of the task's return value, when available.
        ``None`` both when no preview exists and when the task legitimately
        returned ``None`` -- use ``value_available`` to disambiguate.
    value_available : bool
        True iff ``value`` reflects an actual preview.
    value_unavailable_reason : str or None
        When ``value_available`` is False, one of ``not_json_serializable``,
        ``too_large``, or ``unavailable``.
    """

    def __init__(
        self,
        url: str,
        expires_in: int,
        content_type: str = "application/octet-stream",
        value: Any = None,
        value_available: bool = False,
        value_unavailable_reason: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.url = url
        self.expires_in = expires_in
        self.content_type = content_type
        self.value = value
        self.value_available = value_available
        self.value_unavailable_reason = value_unavailable_reason

    def __repr__(self) -> str:
        return f"TaskExecutionResult(value_available={self.value_available!r})"


class TaskExecutionLogs:
    """Live K8s pod logs for a task execution.

    Attributes
    ----------
    logs : str
        Pod stdout+stderr, subject to the ``verbosity`` filter.
    filtered_line_count : int
        Number of lines removed by the verbosity filter (0 when ``verbosity='all'``).
    """

    def __init__(self, logs: str, filtered_line_count: int = 0, **kwargs: Any) -> None:
        self.logs = logs
        self.filtered_line_count = filtered_line_count

    def __repr__(self) -> str:
        return f"TaskExecutionLogs(len={len(self.logs)}, filtered={self.filtered_line_count})"


class TaskExecutionDurableLog:
    """Inline content of a task's durable (S3-uploaded) stdout/stderr log.

    Attributes
    ----------
    content : str
        UTF-8 decoded log content, subject to the ``verbosity`` filter. A
        head+tail excerpt when ``truncated`` is True.
    content_type : str
        MIME type of the payload (``text/plain``).
    total_bytes : int
        Size in bytes of the full S3 object (independent of truncation/verbosity).
    truncated : bool
        True iff ``content`` is an excerpt because the filtered content exceeded
        the inline response cap.
    filtered_line_count : int
        Number of lines removed by the verbosity filter (0 when ``verbosity='all'``).
    """

    def __init__(
        self,
        content: str,
        total_bytes: int,
        content_type: str = "text/plain",
        truncated: bool = False,
        filtered_line_count: int = 0,
        **kwargs: Any,
    ) -> None:
        self.content = content
        self.content_type = content_type
        self.total_bytes = total_bytes
        self.truncated = truncated
        self.filtered_line_count = filtered_line_count

    def __repr__(self) -> str:
        return f"TaskExecutionDurableLog(total_bytes={self.total_bytes}, truncated={self.truncated!r})"


class PipelineTaskExecution(APIObject):
    """The execution record of a single ``@task`` within a dispatch.

    Task-execution endpoints are keyed by dispatch ID (not version); ``task_id``
    is the public sequential task number (1, 2, 3, ...) from the pipeline tasks
    endpoint.

    Attributes
    ----------
    task_id : int or None
        The public sequential task number, or None for utility electrons not
        backed by a task row.
    name : str
        The ``@task`` function name.
    status : str
        Current task-execution status (PENDING, RUNNING, RETRYING, COMPLETED,
        FAILED, CANCELLED, ERRORED).
    started_at : str or None
        When execution began, or None if not yet started.
    completed_at : str or None
        When execution finished, or None if still running.
    error_detail : str or None
        Failure message when the task failed.
    """

    _converter = t.Dict({
        t.Key("task_id", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("name"): String(),
        t.Key("status"): t.Enum(*enum_to_list(TaskExecutionStatus)),
        t.Key("started_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("completed_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("error_detail", optional=True, default=None): t.Or(String(allow_blank=True), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        name: str,
        status: TaskExecutionStatus,
        task_id: Optional[int] = None,
        started_at: Optional[str] = None,
        completed_at: Optional[str] = None,
        error_detail: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.task_id = task_id
        self.name = name
        self.status = status
        self.started_at = started_at
        self.completed_at = completed_at
        self.error_detail = error_detail

    def __repr__(self) -> str:
        return f"PipelineTaskExecution(task_id={self.task_id!r}, name={self.name!r}, status={self.status!r})"

    @classmethod
    def _tasks_path(cls, pipeline_id: str, dispatch_id: str) -> str:
        return f"{_BASE_PATH}{pipeline_id}/dispatches/{dispatch_id}/tasks/"

    @classmethod
    def list(
        cls: Type[TPipelineTaskExecution],
        pipeline_id: str,
        dispatch_id: str,
    ) -> List[TPipelineTaskExecution]:
        """List all task-execution records for a dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.

        Returns
        -------
        tasks : list of PipelineTaskExecution
        """
        path = cls._tasks_path(pipeline_id, dispatch_id)
        response = cls._client.get(path)
        # This endpoint returns a bare JSON array, not a paginated envelope.
        return [cls.from_server_data(item) for item in response.json()]

    @classmethod
    def get(
        cls: Type[TPipelineTaskExecution],
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
    ) -> TPipelineTaskExecution:
        """Get the execution record for a single task in a dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.

        Returns
        -------
        task : PipelineTaskExecution
        """
        path = cls._tasks_path(pipeline_id, dispatch_id)
        response = cls._client.get(f"{path}{task_id}/")
        return cls.from_server_data(response.json())

    @classmethod
    def get_result(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
    ) -> TaskExecutionResult:
        """Get a completed task's result (presigned URL + JSON preview).

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.

        Returns
        -------
        result : TaskExecutionResult
        """
        path = cls._tasks_path(pipeline_id, dispatch_id)
        response = cls._client.get(f"{path}{task_id}/result/")
        data = response.json()
        return TaskExecutionResult(
            url=data["url"],
            expires_in=data.get("expires_in") or data.get("expiresIn"),
            content_type=data.get("content_type") or data.get("contentType") or "application/octet-stream",
            value=data.get("value"),
            value_available=bool(data.get("value_available") or data.get("valueAvailable")),
            value_unavailable_reason=data.get("value_unavailable_reason") or data.get("valueUnavailableReason"),
        )

    @classmethod
    def get_logs(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        tail_lines: Optional[int] = None,
        verbosity: str = "user",
    ) -> TaskExecutionLogs:
        """Read the live K8s pod logs for a task execution.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        tail_lines : int, optional
            Cap on the number of trailing log lines returned.
        verbosity : str, optional
            'user' (default) hides the electron runner's own structured JSON log
            lines; 'all' returns every line unfiltered.

        Returns
        -------
        logs : TaskExecutionLogs
        """
        path = cls._tasks_path(pipeline_id, dispatch_id)
        # rawdict keeps query keys snake_case; the server expects ``tail_lines``,
        # not the camelCased ``tailLines`` that to_api would otherwise produce.
        params: Dict[str, Any] = {"verbosity": verbosity}
        if tail_lines is not None:
            params["tail_lines"] = tail_lines
        response = cls._client.get(f"{path}{task_id}/logs/", params=rawdict(params))
        data = response.json()
        return TaskExecutionLogs(
            logs=data.get("logs") or "",
            filtered_line_count=data.get("filtered_line_count") or data.get("filteredLineCount") or 0,
        )

    @classmethod
    def get_durable_log(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        stream: str,
        verbosity: str = "user",
    ) -> TaskExecutionDurableLog:
        """Read a task's durable (S3-uploaded) stdout/stderr log content.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        stream : str
            Which stream to read: ``'stdout'`` or ``'stderr'``.
        verbosity : str, optional
            'user' (default) hides the electron runner's own structured JSON log
            lines; 'all' returns every line unfiltered.

        Returns
        -------
        log : TaskExecutionDurableLog
        """
        path = cls._tasks_path(pipeline_id, dispatch_id)
        response = cls._client.get(
            f"{path}{task_id}/logs/{stream}/",
            params=rawdict({"verbosity": verbosity}),
        )
        data = response.json()
        return TaskExecutionDurableLog(
            content=data.get("content") or "",
            total_bytes=data.get("total_bytes") or data.get("totalBytes") or 0,
            content_type=data.get("content_type") or data.get("contentType") or "text/plain",
            truncated=bool(data.get("truncated")),
            filtered_line_count=data.get("filtered_line_count") or data.get("filteredLineCount") or 0,
        )
