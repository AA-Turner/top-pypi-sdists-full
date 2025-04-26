# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.sch_models import ScheduledTaskStatus
from streamsets.sdk.utils import get_random_string

# fmt: on


@pytest.fixture(scope="module")
def sample_job(sch, sch_authoring_sdc_id, sch_executor_sdc_label):
    """A trivial job

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline)

    job_builder = sch.get_job_builder()
    job = job_builder.build(
        'Job Template SDK Tests {}'.format(get_random_string()),
        pipeline=pipeline,
        runtime_parameters={'x': 'y', 'a': 'b'},
    )
    sch.add_job(job)

    try:
        yield job
    finally:
        sch.delete_job(job)
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture
def sample_running_scheduled_task(sch, sample_job):
    scheduled_task_builder = sch.get_scheduled_task_builder()
    scheduled_task = scheduled_task_builder.build(sample_job)
    sch.add_scheduled_task(scheduled_task)

    try:
        yield scheduled_task
    finally:
        if ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.DELETED:
            return
        if ScheduledTaskStatus(scheduled_task.status) != ScheduledTaskStatus.KILLED:
            sch.kill_scheduled_tasks(scheduled_task)
        sch.delete_scheduled_tasks(scheduled_task)


@pytest.fixture
def sample_paused_scheduled_task(sch, sample_job):
    scheduled_task_builder = sch.get_scheduled_task_builder()
    scheduled_task = scheduled_task_builder.build(sample_job)
    sch.add_scheduled_task(scheduled_task)
    sch.pause_scheduled_tasks(scheduled_task)

    try:
        yield scheduled_task
    finally:
        if ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.DELETED:
            return
        if ScheduledTaskStatus(scheduled_task.status) != ScheduledTaskStatus.KILLED:
            sch.kill_scheduled_tasks(scheduled_task)
        sch.delete_scheduled_tasks(scheduled_task)


@pytest.fixture
def sample_killed_scheduled_task(sch, sample_job):
    scheduled_task_builder = sch.get_scheduled_task_builder()
    scheduled_task = scheduled_task_builder.build(sample_job)
    sch.add_scheduled_task(scheduled_task)
    sch.kill_scheduled_tasks(scheduled_task)

    try:
        yield scheduled_task
    finally:
        if ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.DELETED:
            return
        if ScheduledTaskStatus(scheduled_task.status) != ScheduledTaskStatus.KILLED:
            sch.kill_scheduled_tasks(scheduled_task)
        sch.delete_scheduled_tasks(scheduled_task)


@pytest.fixture
def sample_deleted_scheduled_task(sch, sample_job):
    scheduled_task_builder = sch.get_scheduled_task_builder()
    scheduled_task = scheduled_task_builder.build(sample_job)
    sch.add_scheduled_task(scheduled_task)
    sch.kill_scheduled_tasks(scheduled_task)
    sch.delete_scheduled_tasks(scheduled_task)

    try:
        yield scheduled_task
    finally:
        if ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.DELETED:
            return
        if ScheduledTaskStatus(scheduled_task.status) != ScheduledTaskStatus.KILLED:
            sch.kill_scheduled_tasks(scheduled_task)
        sch.delete_scheduled_tasks(scheduled_task)


def test_scheduled_task_in_sch(sch, sample_running_scheduled_task):
    assert sample_running_scheduled_task in sch.scheduled_tasks


def test_scheduled_task_removed_from_sch(sch, sample_deleted_scheduled_task):
    assert sample_deleted_scheduled_task not in sch.scheduled_tasks


def test_overriden_contains_function(sch, sample_running_scheduled_task):
    task_id = sample_running_scheduled_task.id
    task_name = sample_running_scheduled_task.name
    # should be present
    assert sch.scheduled_tasks.contains(id=task_id)
    assert sch.scheduled_tasks.contains(name=task_name)
    # should not be present
    assert not sch.scheduled_tasks.contains(id=get_random_string())
    assert not sch.scheduled_tasks.contains(name=get_random_string())


@pytest.mark.parametrize(
    "scheduled_task",
    [
        'sample_running_scheduled_task',
        'sample_paused_scheduled_task',
        'sample_killed_scheduled_task',
        'sample_deleted_scheduled_task',
    ],
)
def test_resume_action(sch, scheduled_task, request):
    scheduled_task = request.getfixturevalue(scheduled_task)
    initial_status = ScheduledTaskStatus(scheduled_task.status)
    sch.resume_scheduled_tasks(scheduled_task)
    if initial_status == ScheduledTaskStatus.PAUSED:
        assert ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.RUNNING
    else:
        assert ScheduledTaskStatus(scheduled_task.status) == initial_status


@pytest.mark.parametrize(
    "scheduled_task",
    [
        'sample_running_scheduled_task',
        'sample_paused_scheduled_task',
        'sample_killed_scheduled_task',
        'sample_deleted_scheduled_task',
    ],
)
def test_pause_action(sch, scheduled_task, request):
    scheduled_task = request.getfixturevalue(scheduled_task)
    initial_status = ScheduledTaskStatus(scheduled_task.status)
    sch.pause_scheduled_tasks(scheduled_task)

    if initial_status == ScheduledTaskStatus.RUNNING:
        assert ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.PAUSED
    else:
        assert ScheduledTaskStatus(scheduled_task.status) == initial_status


@pytest.mark.parametrize(
    "scheduled_task",
    [
        'sample_running_scheduled_task',
        'sample_paused_scheduled_task',
        'sample_killed_scheduled_task',
        'sample_deleted_scheduled_task',
    ],
)
def test_kill_action(sch, scheduled_task, request):
    scheduled_task = request.getfixturevalue(scheduled_task)
    initial_status = ScheduledTaskStatus(scheduled_task.status)
    sch.kill_scheduled_tasks(scheduled_task)
    if initial_status in [ScheduledTaskStatus.RUNNING, ScheduledTaskStatus.PAUSED]:
        assert ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.KILLED
    else:
        assert ScheduledTaskStatus(scheduled_task.status) == initial_status


@pytest.mark.parametrize(
    "scheduled_task",
    [
        'sample_running_scheduled_task',
        'sample_paused_scheduled_task',
        'sample_killed_scheduled_task',
        'sample_deleted_scheduled_task',
    ],
)
def test_delete_action(sch, scheduled_task, request):
    scheduled_task = request.getfixturevalue(scheduled_task)
    initial_status = ScheduledTaskStatus(scheduled_task.status)
    sch.delete_scheduled_tasks(scheduled_task)
    if initial_status == ScheduledTaskStatus.KILLED:
        assert ScheduledTaskStatus(scheduled_task.status) == ScheduledTaskStatus.DELETED
    else:
        assert ScheduledTaskStatus(scheduled_task.status) == initial_status


@pytest.mark.parametrize(
    "function_name, result_status, first_task, second_task",
    [
        (
            'resume_scheduled_tasks',
            ScheduledTaskStatus.RUNNING,
            'sample_paused_scheduled_task',
            'sample_paused_scheduled_task',
        ),
        (
            'pause_scheduled_tasks',
            ScheduledTaskStatus.PAUSED,
            'sample_running_scheduled_task',
            'sample_running_scheduled_task',
        ),
        (
            'kill_scheduled_tasks',
            ScheduledTaskStatus.KILLED,
            'sample_running_scheduled_task',
            'sample_paused_scheduled_task',
        ),
        (
            'delete_scheduled_tasks',
            ScheduledTaskStatus.DELETED,
            'sample_killed_scheduled_task',
            'sample_killed_scheduled_task',
        ),
    ],
)
def test_action_on_multiple_scheduled_tasks(sch, function_name, result_status, first_task, second_task, request):
    first_task = request.getfixturevalue(first_task)
    second_task = request.getfixturevalue(second_task)
    function_to_test = getattr(sch, function_name)
    function_to_test(first_task, second_task)
    assert ScheduledTaskStatus(first_task.status) == result_status
    assert ScheduledTaskStatus(second_task.status) == result_status


@pytest.mark.parametrize(
    "function_name, first_task, first_task_result_status, second_task, second_task_result_status",
    [
        (
            'resume_scheduled_tasks',
            'sample_killed_scheduled_task',
            ScheduledTaskStatus.KILLED,
            'sample_paused_scheduled_task',
            ScheduledTaskStatus.RUNNING,
        ),
        (
            'pause_scheduled_tasks',
            'sample_killed_scheduled_task',
            ScheduledTaskStatus.KILLED,
            'sample_running_scheduled_task',
            ScheduledTaskStatus.PAUSED,
        ),
        (
            'kill_scheduled_tasks',
            'sample_deleted_scheduled_task',
            ScheduledTaskStatus.DELETED,
            'sample_running_scheduled_task',
            ScheduledTaskStatus.KILLED,
        ),
        (
            'delete_scheduled_tasks',
            'sample_paused_scheduled_task',
            ScheduledTaskStatus.PAUSED,
            'sample_killed_scheduled_task',
            ScheduledTaskStatus.DELETED,
        ),
    ],
)
def test_skip_tasks_not_permissible_state(
    sch, function_name, first_task, first_task_result_status, second_task, second_task_result_status, request
):
    # only one of the tasks is in the correct state, the first task should be skipped by the function
    first_task = request.getfixturevalue(first_task)
    second_task = request.getfixturevalue(second_task)
    function_to_test = getattr(sch, function_name)
    function_to_test(first_task, second_task)
    assert ScheduledTaskStatus(first_task.status) == first_task_result_status
    assert ScheduledTaskStatus(second_task.status) == second_task_result_status


@pytest.mark.parametrize(
    "function_name",
    ['resume_scheduled_tasks', 'pause_scheduled_tasks', 'kill_scheduled_tasks', 'delete_scheduled_tasks'],
)
def test_call_function_without_parameters(sch, function_name):
    function_to_test = getattr(sch, function_name)
    with pytest.raises(ValueError):
        function_to_test()


@pytest.mark.parametrize(
    "function_name",
    ['resume_scheduled_tasks', 'pause_scheduled_tasks', 'kill_scheduled_tasks', 'delete_scheduled_tasks'],
)
@pytest.mark.parametrize("parameters", [(1, 2, 3), ('hello world', "this shouldn't work", get_random_string()), 'wow'])
def test_passing_random_variables_parameters(sch, function_name, parameters):
    function_to_test = getattr(sch, function_name)
    with pytest.raises(ValueError):
        function_to_test(*parameters)


@pytest.mark.parametrize("random_object", ['hello world', 4, ScheduledTaskStatus.DELETED])
def test_passing_random_variables_in_action(sch, sample_running_scheduled_task, random_object):
    with pytest.raises(ValueError):
        sch._validate_and_execute_scheduled_tasks_action(random_object, sample_running_scheduled_task)


def test_update_scheduled_task(sch, sample_running_scheduled_task):
    new_name = 'Switched Name'
    task_id = sample_running_scheduled_task.id
    task = sch.scheduled_tasks.get(id=task_id)
    task.name = new_name
    sch.update_scheduled_task(task)
    task = sch.scheduled_tasks.get(id=task_id)
    assert task.name == new_name


def test_filter_by(sch, sample_running_scheduled_task):
    results = sch.scheduled_tasks.get_all(filter_by=sample_running_scheduled_task.name)
    assert len(results) == 1

    results = sch.scheduled_tasks.get_all(filter_by='NAME THAT CLEARLY DOESNT EXIST')
    assert len(results) == 0
