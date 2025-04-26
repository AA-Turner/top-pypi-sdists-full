from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.task import Task

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.task._generated.api_client.ApiClient.request"


@pytest.fixture
def tasks(schema):
    return schema.tasks


@pytest.fixture
def task(tasks):
    return tasks["my_task"]


def test_create_or_alter_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.create_or_alter_async(Task("my_task", "select 1"))
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "PUT",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task",
        **extra_params(body={"name": "my_task", "definition": "select 1"})
    )


def test_drop_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "DELETE",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task",
        **extra_params()
    )


def test_fetch_async(fake_root, task):
    from snowflake.core.task._generated.models import Task as TaskModel

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(TaskModel(name="my_task", definition="select 1").to_json())
        op = task.fetch_async()
        assert isinstance(op, PollingOperation)
        task = op.result()
        assert task.to_dict() == Task(name="my_task", definition="select 1").to_dict()
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task",
        **extra_params()
    )


def test_execute_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.execute_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:execute?retryLast=False",
        **extra_params(query_params=[("retryLast", False)])
    )


def test_resume_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:resume",
        **extra_params()
    )

def test_suspend_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:suspend",
        **extra_params()
    )


def test_fetch_task_dependents_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = task.fetch_task_dependents_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task/dependents",
        **extra_params()
    )


def test_get_complete_graphs_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.get_complete_graphs_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task/complete-graphs?errorOnly=True",
        **extra_params(query_params=[("errorOnly", True)])
    )


def test_get_current_graphs_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.get_current_graphs_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task/current-graphs",
        **extra_params()
    )


def test_create_async(fake_root, tasks):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tasks.create_async(Task("my_task", "select 1"))
        assert isinstance(op, PollingOperation)
        task_res = op.result()
        assert task_res.name == "my_task"
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks?createMode=errorIfExists",
        **extra_params(
            query_params=[("createMode", "errorIfExists")],
            body={"name": "my_task", "definition": "select 1"},
        )
    )


def test_iter_async(fake_root, tasks):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = tasks.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks?rootOnly=False",
        **extra_params(query_params=[("rootOnly", False)])
    )
