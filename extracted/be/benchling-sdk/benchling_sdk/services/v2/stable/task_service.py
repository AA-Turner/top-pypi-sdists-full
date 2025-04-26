from time import sleep, time

from benchling_api_client.types import UNSET
from benchling_api_client.v2.alpha.extensions import (
    NotPresentError as NotPresentErrorAlpha,
    UnknownType as UnknownTypeAlpha,
)
from benchling_api_client.v2.beta.extensions import (
    NotPresentError as NotPresentErrorBeta,
    UnknownType as UnknownTypeBeta,
)
from benchling_api_client.v2.stable.api.tasks import get_task
from benchling_api_client.v2.stable.extensions import NotPresentError, UnknownType

from benchling_sdk.errors import WaitForTaskExpiredError
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.models import AsyncTask, AsyncTaskStatus
from benchling_sdk.services.v2.base_service import BaseService


class TaskService(BaseService):
    """
    Tasks.

    Endpoints that perform expensive computations launch long-running tasks. These endpoints return the task ID (a
    UUID) in the response body.

    After launching a task, periodically invoke the Get a task endpoint with the task UUID (e.g., every 10
    seconds), until the status is no longer RUNNING.

    You can access a task for up to 30 minutes after its completion, after which its data will no longer be
    available.

    Note that as of SDK version 1.19.0, most endpoint methods that create long-running tasks now return
    a :py:class:`benchling_sdk.helpers.task_helpers.TaskHelper`, which allows you to get the task result
    more conveniently as a specific model type.

    See https://benchling.com/api/reference#/Tasks
    """

    @api_method
    def get_by_id(self, task_id: str) -> AsyncTask:
        """
        Get a Task by ID.

        See https://benchling.com/api/reference#/Tasks/getTask
        """
        response = get_task.sync_detailed(client=self.client, task_id=task_id)

        # TODO BNCH-50360 - AsyncTask is deserializing as UnknownType due to partial discriminator support
        # Undo this workaround once full discriminator support for tasks is available
        task_model = model_from_detailed(response)
        if isinstance(task_model, (UnknownTypeAlpha, UnknownTypeBeta, UnknownType)):
            return AsyncTask.from_dict(task_model.value)
        # Convert to a generic AsyncTask if a more specific type is returned
        return _deserialize_task_from_instance(task_model)

    @api_method
    def wait_for_task(
        self, task_id: str, interval_wait_seconds: int = 1, max_wait_seconds: int = 600
    ) -> AsyncTask:
        """
        Wait for a task until completion or timeout.

        A blocking method which polls the Benchling API and will return an AsyncTask as
        soon as its status is not RUNNING (in progress). This does not guarantee that the
        task was successful, only that Benchling has finished executing it.

        If max_wait_seconds is exceeded, will raise
        :py:class:`benchling_sdk.errors.WaitForTaskExpiredError`

        :param task_id: The ID of the task to poll
        :param interval_wait_seconds: time to wait between API calls in seconds
        :param max_wait_seconds: maximum wait time in seconds before raising WaitForTaskExpiredError
        :return: The completed AsyncTask. Check `status` for success or failure
        :rtype: AsyncTask
        """
        start_time = time()
        response = self.get_by_id(task_id)
        while response.status == AsyncTaskStatus.RUNNING and time() - start_time <= max_wait_seconds:
            sleep(interval_wait_seconds)
            response = self.get_by_id(task_id)
        if response.status != AsyncTaskStatus.RUNNING:
            return response
        raise WaitForTaskExpiredError(
            message=f"Timed out waiting for task ID {task_id} " f"after {max_wait_seconds} seconds",
            task=response,
        )


def _deserialize_task_from_instance(task_instance) -> AsyncTask:
    # TODO BNCH-50360 - AsyncTask is deserializing as UnknownType due to partial discriminator support
    # However, in some cases it will deserialize to a concrete type, often an incorrect type
    # Manually serialize to Async Task. Calling .from_dict() on its own results in an error:
    # AttributeError: 'NoneType' object has no attribute 'copy' from response being None

    # Successful task seem to deserialize to UnknownType but code defensively just in case
    try:
        if hasattr(task_instance, "response") and task_instance.response is not None:
            serialized = task_instance.to_dict()
            serialized["errors"] = UNSET
            return AsyncTask.from_dict(serialized)
    except (NotPresentErrorAlpha, NotPresentErrorBeta, NotPresentError):
        pass
    serialized = task_instance.to_dict()
    # AsyncErrors data is always in additional_properties,
    # It has no modeled properties of its own. They don't copy over properly so manually move them
    try:
        if hasattr(task_instance, "errors") and task_instance.errors is not None:
            serialized["errors"] = task_instance.errors.additional_properties
    except (NotPresentErrorAlpha, NotPresentErrorBeta, NotPresentError):
        pass
    serialized["response"] = UNSET
    return AsyncTask.from_dict(serialized)
