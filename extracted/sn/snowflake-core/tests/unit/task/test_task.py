import itertools

from datetime import timedelta
from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.tag import TagValue
from snowflake.core.task import OverlapPolicy, Task, TaskResource
from snowflake.core.task._generated import TagAssignment, TagReference
from snowflake.core.task._generated.models import CronSchedule, MinutesSchedule
from snowflake.core.task._task import (
    Cron,
    _from_model_schedule,
    _from_model_target_completion_interval,
    _to_model_schedule,
    _to_model_target_completion_interval,
)

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


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
        **extra_params(body={"name": "my_task", "definition": "select 1"}),
    )


def test_drop_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root, "DELETE", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task", **extra_params()
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
        fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task", **extra_params()
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
        **extra_params(query_params=[("retryLast", False)]),
    )


def test_resume_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.resume_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:resume", **extra_params()
    )


def test_suspend_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.suspend_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:suspend", **extra_params()
    )


def test_fetch_task_dependents_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = task.fetch_task_dependents_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task/dependents", **extra_params()
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
        **extra_params(query_params=[("errorOnly", True)]),
    )


def test_get_current_graphs_async(fake_root, task):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.get_current_graphs_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(
        fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task/current-graphs", **extra_params()
    )


def test_create_async(fake_root, tasks):
    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = tasks.create_async(Task("my_task", "select 1"))
        assert isinstance(op, PollingOperation)
        task_res = op.result()
        assert isinstance(task_res, TaskResource)
        assert task_res.name == "my_task"
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        BASE_URL + "/databases/my_db/schemas/my_schema/tasks?createMode=errorIfExists",
        **extra_params(
            query_params=[("createMode", "errorIfExists")], body={"name": "my_task", "definition": "select 1"}
        ),
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
        **extra_params(query_params=[("rootOnly", False)]),
    )


def test_set_tags(fake_root, task, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:set-tags")
    tags = {tag: TagValue(value="value")}
    kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tags.items()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        task.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, task, tag):
    args = (fake_root, "POST", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:unset-tags")
    tag_resources = {tag}
    kwargs = extra_params(
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        task.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = task.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, task):
    args = (fake_root, "GET", BASE_URL + "/databases/my_db/schemas/my_schema/tasks/my_task:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert task.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = task.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)


class TestTaskOverlapPolicyBehavior:
    @pytest.mark.parametrize("overlap_policy", itertools.chain(OverlapPolicy, (None,)))
    def test_valid_constructions_with_overlap_policy(self, overlap_policy: OverlapPolicy | None):
        task = Task("test_task", "select 0", overlap_policy=overlap_policy)
        assert task.overlap_policy is overlap_policy
        assert task.allow_overlapping_execution is (
            overlap_policy._equivalent_allow_overlapping_execution_value() if overlap_policy is not None else None
        )
        rest_model = task._to_rest_model()
        assert rest_model.overlap_policy == (str(overlap_policy) if overlap_policy is not None else None)
        assert rest_model.allow_overlapping_execution is None

    @pytest.mark.parametrize("allow_overlapping_execution", (None, False, True))
    def test_valid_constructions_with_allow_overlapping_execution(self, allow_overlapping_execution: bool | None):
        task = Task("test_task", "select 0", allow_overlapping_execution=allow_overlapping_execution)
        assert task.overlap_policy is OverlapPolicy._from_allow_overlapping_execution(allow_overlapping_execution)
        assert task.allow_overlapping_execution is allow_overlapping_execution
        rest_model = task._to_rest_model()
        assert rest_model.overlap_policy is None
        assert rest_model.allow_overlapping_execution is allow_overlapping_execution

    def test_changing_values_after_construction(self):
        """Checks the behavior of changing the overlap policy and allow_overlapping_execution property values after construction."""
        task = Task("test_task", "select 0", overlap_policy=OverlapPolicy.NO_OVERLAP)
        assert task.overlap_policy is OverlapPolicy.NO_OVERLAP
        assert task.allow_overlapping_execution is False
        rest_model = task._to_rest_model()
        assert (rest_model.overlap_policy, rest_model.allow_overlapping_execution) == (
            str(OverlapPolicy.NO_OVERLAP),
            None,
        )

        task.overlap_policy = OverlapPolicy.ALLOW_CHILD_OVERLAP
        assert task.overlap_policy is OverlapPolicy.ALLOW_CHILD_OVERLAP
        assert task.allow_overlapping_execution is True
        rest_model = task._to_rest_model()
        assert (rest_model.overlap_policy, rest_model.allow_overlapping_execution) == (
            str(OverlapPolicy.ALLOW_CHILD_OVERLAP),
            None,
        )

        task.overlap_policy = OverlapPolicy.ALLOW_ALL_OVERLAP
        assert task.overlap_policy is OverlapPolicy.ALLOW_ALL_OVERLAP
        assert task.allow_overlapping_execution is None
        rest_model = task._to_rest_model()
        assert (rest_model.overlap_policy, rest_model.allow_overlapping_execution) == (
            str(OverlapPolicy.ALLOW_ALL_OVERLAP),
            None,
        )

        task.allow_overlapping_execution = True
        assert task.overlap_policy is OverlapPolicy.ALLOW_CHILD_OVERLAP
        assert task.allow_overlapping_execution is True
        rest_model = task._to_rest_model()
        assert (rest_model.overlap_policy, rest_model.allow_overlapping_execution) == (None, True)

        task.allow_overlapping_execution = False
        assert task.overlap_policy is OverlapPolicy.NO_OVERLAP
        assert task.allow_overlapping_execution is False
        rest_model = task._to_rest_model()
        assert (rest_model.overlap_policy, rest_model.allow_overlapping_execution) == (None, False)

    @pytest.mark.parametrize(
        "overlap_policy,allow_overlapping_execution",
        (
            (OverlapPolicy.NO_OVERLAP, True),
            (OverlapPolicy.ALLOW_CHILD_OVERLAP, False),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, False),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, True),
        ),
    )
    def test_invalid_constructions(
        self, overlap_policy: OverlapPolicy | None, allow_overlapping_execution: bool | None
    ):
        with pytest.raises(ValueError):
            Task(
                "test_task",
                "select 0",
                overlap_policy=overlap_policy,
                allow_overlapping_execution=allow_overlapping_execution,
            )

    @pytest.mark.parametrize(
        "overlap_policy,allow_overlapping_execution",
        (
            (OverlapPolicy.NO_OVERLAP, False),
            (OverlapPolicy.ALLOW_CHILD_OVERLAP, True),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, False),
            (OverlapPolicy.ALLOW_ALL_OVERLAP, True),
        ),
    )
    def test_from_rest_model_to_rest_model_round_trip(
        self, overlap_policy: OverlapPolicy, allow_overlapping_execution: bool
    ):
        """Checks Task._from_rest_model and Task._to_rest_model functionality.

        Specifically, checks that Task._from_rest_model functions when both properties are set,
        and the resulting task omits allow_overlapping_execution when converting back to the REST model.
        """
        rest_model = Task(
            "test_task", "select 0"
        )._to_rest_model()  # Using Task._to_rest_model() as an easy way to construct a valid REST model.
        rest_model.overlap_policy = str(overlap_policy)
        rest_model.allow_overlapping_execution = allow_overlapping_execution

        task = Task._from_rest_model(rest_model)
        assert task.overlap_policy is overlap_policy
        assert task.allow_overlapping_execution is overlap_policy._equivalent_allow_overlapping_execution_value()

        rest_model = task._to_rest_model()
        assert rest_model.overlap_policy == str(overlap_policy)
        # The task prioritizes the overlap policy when converting from the REST model to the task object,
        # revealed by this round trip.
        assert rest_model.allow_overlapping_execution is None


class TestScheduleConversion:
    @pytest.mark.parametrize(
        "value,expected_minutes,expected_seconds",
        (
            (timedelta(seconds=30), 0, 30),
            (timedelta(minutes=11), 11, 0),
            (timedelta(minutes=2, seconds=15), 2, 15),
            (timedelta(hours=2), 120, 0),
            (timedelta(hours=1, seconds=1), 60, 1),
            (timedelta(weeks=2), 20160, 0),
        ),
    )
    def test_to_model_schedule_timedelta(self, value: timedelta, expected_minutes: int, expected_seconds: int) -> None:
        result = _to_model_schedule(value)
        assert isinstance(result, MinutesSchedule)
        assert result.minutes == expected_minutes
        assert result.seconds == expected_seconds

    def test_to_model_schedule_cron(self) -> None:
        result = _to_model_schedule(Cron("0 9 * * *", "UTC"))
        assert isinstance(result, CronSchedule)
        assert result.cron_expr == "0 9 * * *"
        assert result.timezone == "UTC"

    def test_to_model_schedule_none(self) -> None:
        assert _to_model_schedule(None) is None

    @pytest.mark.parametrize(
        "value",
        (
            timedelta(microseconds=1),
            timedelta(seconds=3, microseconds=1),
            timedelta(milliseconds=500),
        ),
    )
    def test_to_model_schedule_rejects_sub_second_precision(self, value: timedelta) -> None:
        with pytest.raises(ValueError, match="whole number of seconds"):
            _to_model_schedule(value)

    @pytest.mark.parametrize(
        "value",
        (
            timedelta(seconds=30),
            timedelta(minutes=11),
            timedelta(minutes=2, seconds=15),
            timedelta(hours=25),
        ),
    )
    def test_to_model_target_completion_interval_pass_through(self, value: timedelta) -> None:
        """Sub-minute and beyond-24h intervals are no longer rejected client-side."""
        result = _to_model_target_completion_interval(value)
        assert isinstance(result, MinutesSchedule)
        assert _from_model_target_completion_interval(result) == value

    def test_to_model_target_completion_interval_rejects_sub_second_precision(self) -> None:
        with pytest.raises(ValueError, match="whole number of seconds"):
            _to_model_target_completion_interval(timedelta(microseconds=1))

    @pytest.mark.parametrize(
        "model,expected",
        (
            (MinutesSchedule(minutes=0, seconds=30), timedelta(seconds=30)),
            (MinutesSchedule(minutes=11), timedelta(minutes=11)),
            (MinutesSchedule(minutes=2, seconds=15), timedelta(minutes=2, seconds=15)),
        ),
    )
    def test_from_model_schedule_minutes(self, model: MinutesSchedule, expected: timedelta) -> None:
        assert _from_model_schedule(model) == expected

    def test_from_model_schedule_cron(self) -> None:
        cron_model = CronSchedule(cron_expr="0 9 * * *", timezone="UTC")
        result = _from_model_schedule(cron_model)
        assert result == Cron("0 9 * * *", "UTC")

    def test_round_trip_schedule(self) -> None:
        original = timedelta(minutes=5, seconds=42)
        assert _from_model_schedule(_to_model_schedule(original)) == original
