import logging
import typing
import warnings
from typing import Any, AsyncIterator, Dict, Iterator, Optional

from .._api import BaseAPI, BaseAsyncAPI
from .types import (
    TaskCallResponse,
    TaskRoster,
    TaskStreamData,
    TaskStreamExecutionMetadata,
    TaskStreamFinishMetadata,
    TaskStreamFunctionCallMetadata,
    TaskStreamQuotaMetaData,
    TaskStreamText,
    TaskStreamUnknownMetadata,
)

logger = logging.getLogger(__name__)


class TasksAPI(BaseAPI):
    """TaskAPI client."""

    def execute_stream(self, id: str, parameters: dict) -> Iterator[TaskStreamData]:
        """Executes the task in TaskAPI.

        Args:
            id: task id from the roster
            parameters: task parameters from Swagger
        Returns:
            Stream of `TaskStreamData` objects in a form of iterator.
        """

        kwargs: typing.Dict[str, Any] = {}
        id, tag = split_id(id)
        if tag:
            kwargs["headers"] = {"Grazie-Task-Tag": tag}

        logger.debug(
            "Executing request to TaskAPI with task id %s and parameters: %r",
            f"{id}:{tag}" if tag else id,
            parameters,
        )
        for sse_event in self.client.stream(
            method="POST",
            path=f"task/stream/v4/{id}",
            json={"parameters": parameters},
            **kwargs,
        ):
            if event := _convert_sse_event(sse_event):
                yield event

    def execute(self, id: str, parameters: dict) -> TaskCallResponse:
        """Executes the task in TaskAPI.

        Args:
            id: task id from the roster
            parameters: task parameters from Swagger
        Returns:
            `TaskCallResponse` object that aggregates the streamed response from TaskAPI.
        """

        content = []
        quota_metadata = None
        execution_metadata = []
        finish_metadata = None
        unknown_metadata = None
        function_call_metadata = None

        for task_stream_data in self.execute_stream(id=id, parameters=parameters):
            if isinstance(task_stream_data, TaskStreamText):
                content.append(task_stream_data.content)
            elif isinstance(task_stream_data, TaskStreamQuotaMetaData):
                quota_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamExecutionMetadata):
                execution_metadata.append(task_stream_data)
            elif isinstance(task_stream_data, TaskStreamFinishMetadata):
                finish_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamUnknownMetadata):
                unknown_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamFunctionCallMetadata):
                function_call_metadata = task_stream_data

        return TaskCallResponse(
            content="".join(content),
            quota_metadata=quota_metadata,
            execution_metadata=execution_metadata,
            finish_metadata=finish_metadata,
            unknown_metadata=unknown_metadata,
            function_call_metadata=function_call_metadata,
        )

    def roster(self) -> TaskRoster:
        """
        Returns all available task ids.

        For the list of task parameters, see the Swagger documentation:
        https://api.app.stgn.grazie.aws.intellij.net/swagger-ui/index.html?urls.primaryName=Tasks#/
        """
        resp = self.client.request(
            method="GET",
            path="task/roster",
        )
        return TaskRoster.parse_raw(resp.read())


class AsyncTasksAPI(BaseAsyncAPI):
    """TaskAPI async client."""

    async def execute_stream(self, id: str, parameters: dict) -> AsyncIterator[TaskStreamData]:
        """Executes the task in TaskAPI.

        Args:
            id: task id from the roster
            parameters: task parameters from Swagger
        Returns:
            Stream of `TaskStreamData` objects in a form of async iterator.
        """

        kwargs: typing.Dict[str, Any] = {}
        id, tag = split_id(id)
        if tag:
            kwargs["headers"] = {"Grazie-Task-Tag": tag}

        logger.debug(
            "Executing request to TaskAPI with task id %s and parameters: %r",
            f"{id}:{tag}" if tag else id,
            parameters,
        )
        async for sse_event in self.client.stream(
            method="POST",
            path=f"task/stream/v4/{id}",
            json={"parameters": parameters},
            **kwargs,
        ):
            if event := _convert_sse_event(sse_event):
                yield event

    async def execute(self, id: str, parameters: dict) -> TaskCallResponse:
        """Executes the task in TaskAPI.

        Args:
            id: task id from the roster
            parameters: task parameters from Swagger
        Returns:
            `TaskCallResponse` object that aggregates the streamed response from TaskAPI.
        """

        content = []
        quota_metadata = None
        execution_metadata = []
        finish_metadata = None
        unknown_metadata = None
        function_call_metadata = None

        async for task_stream_data in self.execute_stream(id=id, parameters=parameters):
            if isinstance(task_stream_data, TaskStreamText):
                content.append(task_stream_data.content)
            elif isinstance(task_stream_data, TaskStreamQuotaMetaData):
                quota_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamExecutionMetadata):
                execution_metadata.append(task_stream_data)
            elif isinstance(task_stream_data, TaskStreamFinishMetadata):
                finish_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamUnknownMetadata):
                unknown_metadata = task_stream_data
            elif isinstance(task_stream_data, TaskStreamFunctionCallMetadata):
                function_call_metadata = task_stream_data

        return TaskCallResponse(
            content="".join(content),
            quota_metadata=quota_metadata,
            execution_metadata=execution_metadata,
            finish_metadata=finish_metadata,
            unknown_metadata=unknown_metadata,
            function_call_metadata=function_call_metadata,
        )

    async def roster(self) -> TaskRoster:
        """
        Returns all available task ids.

        For the list of task parameters, see the Swagger documentation:
        https://api.app.stgn.grazie.aws.intellij.net/swagger-ui/index.html?urls.primaryName=Tasks#/
        """
        resp = await self.client.request(
            method="GET",
            path="task/roster",
        )
        return TaskRoster.parse_raw(await resp.aread())


def _convert_sse_event(sse_event: Dict[str, Any]) -> Optional[TaskStreamData]:
    logger.debug("Received SSE from TaskAPI: %r", sse_event)

    event_type = sse_event.pop("type")

    if event_type == "Content":
        return TaskStreamText.parse_obj(sse_event)
    elif event_type == "QuotaMetadata":
        return TaskStreamQuotaMetaData.parse_obj(sse_event)
    elif event_type == "ExecutionMetadata":
        return TaskStreamExecutionMetadata.parse_obj(sse_event)
    elif event_type == "FinishMetadata":
        return TaskStreamFinishMetadata.parse_obj(sse_event)
    elif event_type == "UnknownMetadata":
        return TaskStreamUnknownMetadata.parse_obj(sse_event)
    elif event_type == "FunctionCallMetadata":
        return TaskStreamFunctionCallMetadata.parse_obj(sse_event)

    warnings.warn(f"Can't convert unknown task stream event type {event_type!r}")
    return None


def split_id(id: str) -> typing.Tuple[str, str]:
    if ":" in id:
        id, tag = id.split(":", 1)
        return id, tag
    return id, ""
