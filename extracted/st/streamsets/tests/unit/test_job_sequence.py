# Copyright 2024 StreamSets Inc.

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk.sch import ControlHub
from streamsets.sdk.sch_models import FinishCondition, Job, JobSequence, JobSequenceBuilder, Step
from streamsets.sdk.utils import SeekableList

from .resources.conftest_data import JOB_SEQUENCE_BUILDER_JSON, JOB_SEQUENCE_EMPTY_JSON
from .resources.job_sequence_data import (
    DUMMY_JOB_JSON_1, DUMMY_JOB_JSON_2, DUMMY_STEP_JSON, FINISH_CONDITION_JSON, JOB_SEQUENCE_HISTORY_LOG_JSON,
    JOB_SEQUENCE_JSON,
)

# fmt: on
START_TIME_2099 = 4200268800
END_TIME_2099 = 4200268800
START_TIME_2100 = 4237401600
END_TIME_2100 = 4237996800
UTC_TIME_Z0NE = ' UTC'
BASIC_CRON_TAB_MASK = '0/1 * 1/1 * ? *'
NUM_OF_STEPS = 4
NUM_OF_JOBS = 3


class MockControlHub(ControlHub):
    def __init__(self):
        self.api_client = MockApiClient()
        self.organization = 'DUMMY ORG'

    @property
    def _sequencing_api(self):
        return {'definitions': {'USequence': JOB_SEQUENCE_BUILDER_JSON}}


class MockApiClient:
    def __init__(self):
        self.value = 'value'

    def mark_job_as_finished(self, value):
        return MockReturn(value)

    def get_job_sequence_log_history(
        self, sequence_id, offset, len, log_type, log_level, last_run_only, run_id, from_date, to_date
    ):
        json_copy = dict(JOB_SEQUENCE_HISTORY_LOG_JSON)
        json_copy['offset'] = offset
        json_copy['len'] = -1

        for json in json_copy['data']:
            json['sequenceId'] = sequence_id
            json['logType'] = log_type
            json['logLevel'] = log_level
        return MockReturn(json_copy)

    def add_step_jobs_to_job_sequence(self, value1, value2):
        return MockReturn([value1, value2])

    def update_steps_of_job_sequence(self, value1, value2):
        return MockReturn([value1, value2])

    def run_job_sequence(self, sequence_id, step_number, single_step):
        return sequence_id, step_number, single_step


class MockReturn:
    def __init__(self, value):
        self.response = MockResponse(value)


class MockResponse:
    def __init__(self, value):
        self.value = value

    def json(self):
        return self.value


@pytest.fixture(scope="function")
def job_sequence():
    json = deepcopy(JOB_SEQUENCE_JSON)
    return JobSequence(json, MockControlHub())


@pytest.fixture(scope="function")
def dummy_job():
    json = deepcopy(DUMMY_JOB_JSON_1)
    return Job(json, MockControlHub())


@pytest.fixture(scope="function")
def dummy_jobs():
    jobs = []
    json = deepcopy(DUMMY_JOB_JSON_2)
    for i in range(NUM_OF_JOBS):
        json_copy = dict(json)
        json_copy['id'] = i
        jobs.append(Job(json_copy, MockControlHub()))

    return jobs


@pytest.fixture(scope="function")
def dummy_step():
    json = deepcopy(DUMMY_STEP_JSON)
    return Step(json, MockControlHub())


@pytest.fixture(scope="function")
def dummy_finish_condition(dummy_step, dummy_job):
    finish_condition_json = dict(FINISH_CONDITION_JSON)
    return FinishCondition(
        finish_condition=finish_condition_json, job_id=dummy_job.job_id, step=dummy_step, control_hub=MockControlHub()
    )


def test_get_job_sequence_builder():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())
    assert isinstance(job_sequence_builder, JobSequenceBuilder)
    assert isinstance(job_sequence_builder._control_hub, MockControlHub)

    assert job_sequence_builder._job_sequence == JOB_SEQUENCE_EMPTY_JSON

    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    assert job_sequence_builder._job_sequence['startTime'] == START_TIME_2099
    assert job_sequence_builder._job_sequence['endTime'] == END_TIME_2099
    assert job_sequence_builder._job_sequence['timezone'] == UTC_TIME_Z0NE
    assert job_sequence_builder._job_sequence['crontabMask'] == BASIC_CRON_TAB_MASK

    name, description = 'TEST NAME', 'TEST DESC'
    job_sequence = job_sequence_builder.build(name=name, description=description)
    assert isinstance(job_sequence, JobSequence)
    assert job_sequence.name == name
    assert job_sequence.description == description


def test_steps_getter(job_sequence):
    assert isinstance(job_sequence.steps, SeekableList)
    assert len(job_sequence.steps) == NUM_OF_STEPS

    for idx, step in enumerate(job_sequence.steps):
        assert isinstance(step, Step)
        assert step.step_number == idx + 1


@pytest.mark.parametrize(
    "step_to_move_index, target_step_number, id_to_correct_position_map, swap",
    [
        (3, 1, {'1': 2, '2': 3, '3': 4, '4': 1}, False),
        (0, 3, {'1': 3, '2': 1, '3': 2, '4': 4}, False),
        (-1, 1, {'1': 4, '2': 2, '3': 3, '4': 1}, True),
        (1, 3, {'1': 1, '2': 3, '3': 2, '4': 4}, True),
    ],
)
def test_move_step(job_sequence, step_to_move_index, target_step_number, id_to_correct_position_map, swap):
    step_to_move = job_sequence.steps[step_to_move_index]
    index_to_move = target_step_number
    id = job_sequence.id

    job_sequence.move_step(step_to_move, index_to_move, swap)

    # _data will now have [job_sequence.id, payload_data], assert that is accurate
    assert job_sequence._data[0] == id

    for step_payload in job_sequence._data[1]:
        assert step_payload['id'] in id_to_correct_position_map
        assert id_to_correct_position_map[step_payload['id']] == step_payload['stepNumber']


@pytest.mark.parametrize(
    "swap",
    [False, True],
)
def test_move_step_with_index_same_as_step_number_of_step(job_sequence, swap):
    step_to_move = job_sequence.steps[-1]

    with pytest.raises(ValueError):
        job_sequence.move_step(step_to_move, step_to_move.step_number, swap)


@pytest.mark.parametrize(
    "swap",
    [False, True],
)
def test_move_step_with_target_step_number_greater_than_number_of_steps(job_sequence, swap):
    with pytest.raises(ValueError):
        job_sequence.move_step(job_sequence.steps[0], 5, swap)


@pytest.mark.parametrize(
    "swap",
    [False, True],
)
def test_move_step_with_incorrect_step_type(job_sequence, swap):
    with pytest.raises(TypeError):
        job_sequence.move_step('ABC', 2, swap)


@pytest.mark.parametrize(
    "swap",
    [False, True],
)
def test_move_step_with_incorrect_target_step_number_type(job_sequence, swap):
    with pytest.raises(TypeError):
        job_sequence.move_step(job_sequence.steps[0], 'ABC', swap)


def test_move_step_with_incorrect_swap_type(job_sequence):
    with pytest.raises(TypeError):
        job_sequence.move_step(job_sequence.steps[0], 2, 'ABC')


@pytest.mark.parametrize(
    "job",
    ['1', ['1'], 1, [2]],
)
def test_mark_job_as_finished_with_incorrect_type(job_sequence, job):
    # trigger setter
    with pytest.raises(TypeError):
        job_sequence.mark_job_as_finished(job)


def test_mark_job_as_finished(job_sequence, dummy_job):
    dummy_job.job_sequence = True
    assert job_sequence.mark_job_as_finished(dummy_job).response.json() == dummy_job.job_id


def test_get_history_log_incorrect_value(job_sequence):
    with pytest.raises(ValueError):
        job_sequence.get_history_log('1', '2')


@pytest.mark.parametrize(
    "step",
    ['1', ['1'], 1, [2]],
)
def test_remove_step_incorrect_type(job_sequence, step):
    with pytest.raises(TypeError):
        job_sequence.remove_step(step)


def test_remove_step_with_step_not_in_sequence(job_sequence, dummy_step):
    with pytest.raises(ValueError):
        job_sequence.remove_step(dummy_step)


def test_remove_step(job_sequence):
    step = job_sequence.steps[0]
    id = job_sequence.id
    step_ids_after_removal = {'2': 1, '3': 2, '4': 3}

    job_sequence.remove_step(step)

    assert job_sequence._data[0] == id
    for step_data in job_sequence._data[1]:
        assert step_data['id'] != step.id
        assert step_data['id'] in step_ids_after_removal
        assert step_ids_after_removal[step_data['id']] == step_data['stepNumber']


@pytest.mark.parametrize(
    "job",
    ['1', ['1'], 1, [2]],
)
def test_add_step_incorrect_jobs_type(job_sequence, job):
    with pytest.raises(TypeError):
        job_sequence.add_step_with_jobs(job)


@pytest.mark.parametrize(
    "parallel_jobs, ignore_error",
    [("0", True), (True, "1"), ("0", False), (False, "1")],
)
def test_add_step_incorrect_parallel_jobs_ignore_error_type(job_sequence, dummy_job, parallel_jobs, ignore_error):
    with pytest.raises(TypeError):
        job_sequence.add_step_with_jobs([dummy_job], parallel_jobs, ignore_error)


def test_add_step_with_job_that_is_in_a_job_sequence(job_sequence, dummy_job):
    dummy_job.job_sequence = True

    with pytest.raises(ValueError):
        job_sequence.add_step_with_jobs([dummy_job])


@pytest.mark.parametrize(
    "ignore_error",
    [True, False],
)
def test_add_step_parallel_jobs_true(job_sequence, dummy_jobs, ignore_error):
    id = job_sequence.id

    job_sequence.add_step_with_jobs(dummy_jobs, True, ignore_error)

    assert job_sequence._data[0] == id
    job_ids = [job.job_id for job in dummy_jobs]
    assert job_sequence._data[1] == [{"stepNumber": NUM_OF_STEPS + 1, "ignoreError": ignore_error, "jobIds": job_ids}]


@pytest.mark.parametrize(
    "ignore_error",
    [True, False],
)
def test_add_step_parallel_jobs_false(job_sequence, dummy_jobs, ignore_error):
    job_sequence_id = job_sequence.id

    job_sequence.add_step_with_jobs(dummy_jobs, False, ignore_error)

    assert job_sequence._data[0] == job_sequence_id
    for idx, job in enumerate(dummy_jobs):
        assert job_sequence._data[1][idx] == {
            "stepNumber": NUM_OF_STEPS + idx + 1,
            "ignoreError": ignore_error,
            "jobIds": [job.job_id],
        }


def test_create_steps_payload(job_sequence):
    job_sequence_payload = job_sequence._create_steps_payload()
    job_sequence_ids_to_step_payload_map = {step_payload['id']: step_payload for step_payload in job_sequence_payload}

    for step in job_sequence.steps:
        assert step.id in job_sequence_ids_to_step_payload_map

        job_ids = [job['jobId'] for job in step.jobs]
        assert job_ids == job_sequence_ids_to_step_payload_map[step.id]['jobIds']

        assert step.step_number == job_sequence_ids_to_step_payload_map[step.id]['stepNumber']

        assert step.ignore_error == job_sequence_ids_to_step_payload_map[step.id]['ignoreError']


@pytest.mark.parametrize(
    "condition_type",
    ['CRON', 'END_TIME'],
)
def test_setting_condition_type(condition_type, dummy_finish_condition):
    dummy_finish_condition.condition_type = condition_type


def test_setting_crontab_mask(dummy_finish_condition):
    dummy_finish_condition.condition_type = 'CRON'
    dummy_finish_condition.crontab_mask = BASIC_CRON_TAB_MASK

    assert dummy_finish_condition.crontab_mask == BASIC_CRON_TAB_MASK


def test_setting_end_time(dummy_finish_condition):
    dummy_finish_condition.condition_type = 'END_TIME'
    dummy_finish_condition.end_time = END_TIME_2100

    assert dummy_finish_condition.end_time == END_TIME_2100


def test_setting_timezone(dummy_finish_condition):
    dummy_finish_condition.condition_type = 'END_TIME'
    dummy_finish_condition.timezone = UTC_TIME_Z0NE

    assert dummy_finish_condition.timezone == UTC_TIME_Z0NE


@pytest.mark.parametrize("condition_type", ['abc', '123', 123, [], {}])
def test_condition_type_with_incorrect_values(condition_type, dummy_finish_condition):
    if isinstance(condition_type, str):
        with pytest.raises(ValueError):
            dummy_finish_condition.condition_type = condition_type
    else:
        with pytest.raises(TypeError):
            dummy_finish_condition.condition_type = condition_type


@pytest.mark.parametrize("crontab", [123, [], {}])
def test_crontab_with_incorrect_values(crontab, dummy_finish_condition):
    dummy_finish_condition.condition_type = 'CRON'
    with pytest.raises(TypeError):
        dummy_finish_condition.crontab_mask = crontab

    dummy_finish_condition.condition_type = 'END_TIME'
    with pytest.raises(TypeError):
        dummy_finish_condition.crontab_mask = BASIC_CRON_TAB_MASK


@pytest.mark.parametrize("end_time", ['123', [], {}])
def test_end_time_with_incorrect_values(end_time, dummy_finish_condition):
    dummy_finish_condition.condition_type = 'END_TIME'
    with pytest.raises(TypeError):
        dummy_finish_condition.end_time = end_time

    dummy_finish_condition.condition_type = 'CRON'
    with pytest.raises(TypeError):
        dummy_finish_condition.end_time = END_TIME_2100


@pytest.mark.parametrize("timezone", [123, [], {}])
def test_timezone_with_incorrect_values(timezone, dummy_finish_condition):
    dummy_finish_condition.condition_type = 'END_TIME'
    with pytest.raises(TypeError):
        dummy_finish_condition.timezone = timezone

    dummy_finish_condition.condition_type = 'CRON'
    with pytest.raises(TypeError):
        dummy_finish_condition.timezone = UTC_TIME_Z0NE


def test_finish_conditions_attribute(dummy_step):
    assert isinstance(dummy_step.finish_conditions, SeekableList)
    assert isinstance(dummy_step.finish_conditions[0], FinishCondition)


def test_run_job_sequence_with_wrong_sequence_type(job_sequence):
    sch = MockControlHub()
    with pytest.raises(TypeError):
        sch.run_job_sequence(job_sequence=1)

    with pytest.raises(TypeError):
        sch.run_job_sequence(job_sequence=job_sequence, start_from_step_number='hello')

    with pytest.raises(ValueError):
        sch.run_job_sequence(job_sequence=job_sequence, start_from_step_number=-1)

    with pytest.raises(ValueError):
        steps = len(job_sequence.steps)
        sch.run_job_sequence(job_sequence=job_sequence, start_from_step_number=steps + 5)


def test_run_job_sequence(job_sequence):
    sch = MockControlHub()

    job_sequence.status = 'INACTIVE'

    sequence_id, step_number, single_step = sch.run_job_sequence(job_sequence=job_sequence, start_from_step_number=2)
    assert sequence_id == job_sequence.id
    assert step_number == 2
    assert single_step is False

    sequence_id, step_number, single_step = sch.run_job_sequence(
        job_sequence=job_sequence, start_from_step_number=2, single_step=True
    )
    assert sequence_id == job_sequence.id
    assert step_number == 2
    assert single_step is True

    sequence_id, step_number, single_step = sch.run_job_sequence(job_sequence=job_sequence)
    assert sequence_id == job_sequence.id
    assert step_number is None
    assert single_step is False
