from dataclasses import dataclass
from typing import Any, cast, Generic, List, Optional, Type, TypeVar, Union

from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.serialization_helpers import unset_as_none
from benchling_sdk.models import AsyncTaskErrors, AsyncTaskErrorsItem, AsyncTaskLink, AsyncTaskStatus

ResponseT = TypeVar("ResponseT")


@dataclass
class TaskCompletion(Generic[ResponseT]):
    """Return type for TaskHelper.wait_for_task, same as AsyncTask but with a typed response."""

    success: bool
    errors: Optional[Union[AsyncTaskErrors, List[AsyncTaskErrorsItem]]] = None
    message: Optional[str] = None
    response: Optional[ResponseT] = None


@dataclass
class TaskFailureException(Exception):
    """Exception type used by :py:class:`.TaskHelper` methods."""

    errors: Union[AsyncTaskErrors, List[AsyncTaskErrorsItem]]
    message: Optional[str]


class EmptyTaskResponse:
    """A sentinel object used for tasks that do not return any response data on completion."""

    pass


EMPTY_TASK_RESPONSE = EmptyTaskResponse()


class TaskHelper(AsyncTaskLink, Generic[ResponseT]):
    """
    Used by Benchling async task endpoints to provide the task response in an appropriate type.

    In the API spec, endpoints that create a long-running task are defined as returning an
    :py:class:`benchling_sdk.models.AsyncTaskLink`, which can be used with
    :py:class:`benchling_sdk.services.v2.stable.TaskService` to query the task status and
    response. But AsyncTaskLink and the task query endpoint do not define a specific schema
    for the task response.

    To work around that limitation, those SDK endpoints now return a TaskHelper instead. This is
    subclassed from AsyncTaskLink for backward compatibility, but unlike AsyncTaskLink, TaskHelper
    knows what the type of the task response should be. It also retains an association with the API
    client, so rather than calling a separate service method, you can simply call
    :py:meth:`.TaskHelper.wait_for_completion` or :py:meth:`.TaskHelper.wait_for_response`.

    You can access a task for up to 30 minutes after its completion, after which its data will no
    longer be available.
    """

    _client: Client
    _response_class: Type[ResponseT]
    _response_decoder: Any
    # _response_decoder is really a Callable, but adding that type hint would cause problems because
    # mypy would treat it as an instance method and assume it should have a self parameter.

    def __init__(self, from_task_link: AsyncTaskLink, client: Client, response_class: Type[ResponseT]):
        """Initialize the instance. This should only be used internally by Benchling API methods."""
        self.task_id = from_task_link.task_id
        self.additional_properties = from_task_link.additional_properties
        self._client = client
        self._response_class = response_class

        if response_class is not EmptyTaskResponse:
            assert hasattr(response_class, "from_dict")
            self._response_decoder = getattr(response_class, "from_dict")  # noqa: B009

    def wait_for_completion(
        self, interval_wait_seconds: int = 1, max_wait_seconds: int = 600
    ) -> TaskCompletion[ResponseT]:
        """
        Wait for the task to succeed or fail.

        This is equivalent to the :py:meth:`benchling_sdk.services.v2.stable.task_service.TaskService.wait_for_task`
        method in :py:class:`benchling_sdk.services.v2.stable.task_service.TaskService`, except that
        instead of returning an :py:class:`benchling_sdk.models.AsyncTask` whose `response` property is
        a dict, it returns a :py:class:`TaskCompletion` whose `response` property is the appropriate type
        for the API method you called. For instance, if the method was `AaSequenceService.bulk_create`,
        the response type will be :py:class:`benchling_sdk.models.BulkCreateAaSequencesAsyncTaskResponse`.

        :param interval_wait_seconds: time to wait between API calls in seconds
        :param max_wait_seconds: maximum wait time in seconds before raising an error
        :return: The task completion status. Check `status` for success or failure
        :rtype: TaskCompletion
        :raises benchling_sdk.errors.WaitForTaskExpiredError: if the maximum wait time has elapsed
        """
        from benchling_sdk.helpers.client_helpers import v2_stable_client
        from benchling_sdk.services.v2.stable.task_service import TaskService

        # The "get task" polling endpoint is part of the v2 stable API; it doesn't exist in alpha or beta.
        task_service = TaskService(v2_stable_client(self._client))

        task = task_service.wait_for_task(
            self.task_id, interval_wait_seconds=interval_wait_seconds, max_wait_seconds=max_wait_seconds
        )
        response: Optional[ResponseT]
        if task.status != AsyncTaskStatus.SUCCEEDED:
            response = None
        elif self._response_class is EmptyTaskResponse:
            response = cast(ResponseT, EMPTY_TASK_RESPONSE)
        else:
            response = self._response_decoder(task.response.to_dict())
        errors = None if task.status != AsyncTaskStatus.FAILED else unset_as_none(lambda: task.errors)
        message = None if task.status != AsyncTaskStatus.FAILED else unset_as_none(lambda:task.message)
        return TaskCompletion(
            success=task.status == AsyncTaskStatus.SUCCEEDED,
            errors=errors,  # type: ignore
            message=message,
            response=response,
        )

    def wait_for_response(self, interval_wait_seconds: int = 1, max_wait_seconds: int = 600) -> ResponseT:
        """
        Wait for the task and return the response object on success, or raise an exception on failure.

        This is a convenience method for calling :py:meth:`wait_for_completion` and then getting the
        `response` property of the returned object if the task succeeded, in cases where you're not
        interested in any :py:class:`.TaskCompletion` properties except the response.

        The type of the returned object is depends on the API method you called. For instance, if the
        method was `AaSequenceService.bulk_create`, the response type will be
        :py:class:`benchling_sdk.models.BulkCreateAaSequencesAsyncTaskResponse`.

        :param interval_wait_seconds: time to wait between API calls in seconds
        :param max_wait_seconds: maximum wait time in seconds before raising an error
        :return: The response object, if the task succeeded.
        :rtype: ResponseT
        :raises benchling_sdk.errors.WaitForTaskExpiredError: if the maximum wait time has elapsed
        :raises .TaskFailureException: if the task failed
        """
        task_completion = self.wait_for_completion(interval_wait_seconds, max_wait_seconds)
        if not task_completion.success:
            raise TaskFailureException(task_completion.errors or AsyncTaskErrors(), task_completion.message)
        assert task_completion.response, "completed task should have contained a response"
        # This assertion matches the behavior of TaskHelper.wait_for_completion(): response is only set
        # to None if the task failed, otherwise it should always be an object even if that object is an
        # EmptyTaskResponse. This also matches how we define async task models in the API spec, where
        # if we don't care about the response field, it's an empty object rather than null.

        return task_completion.response
