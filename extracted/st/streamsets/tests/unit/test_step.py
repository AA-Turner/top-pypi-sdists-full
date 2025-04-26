# Copyright 2024 StreamSets Inc.

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk.sch_models import Job, JobSequence
from streamsets.sdk.utils import SeekableList

from .resources.job_sequence_step_data import JOB_JSON, JOB_SEQUENCE_WITH_STEPS_JSON, JOB_WITHIN_JOB_SEQUENCE_JSON

# fmt: on
START_TIME_2099 = 4200268800
END_TIME_2099 = 4200268800
START_TIME_2100 = 4237401600
END_TIME_2100 = 4237996800
UTC_TIME_Z0NE = ' UTC'
BASIC_CRON_TAB_MASK = '0/1 * 1/1 * ? *'
NUM_OF_STEPS = 4
NUM_OF_JOBS = 3


class MockControlHub:
    def __init__(self):
        self.api_client = MockApiClient()
        self.organization = 'DUMMY ORG'

    @property
    def jobs(self):
        return MockResponse('dummy')


class MockApiClient:
    def __init__(self):
        self.value = 'value'

    def mark_job_as_finished(self, value):
        return MockReturn(value)

    def get_job_sequence_log_history(self, value1, value2, value3):
        return MockReturn([value1, value2, value3])

    def add_step_jobs_to_job_sequence(self, value1, value2):
        return MockReturn({value1: value2})

    def update_job_sequence_steps(self, value):
        pass

    def update_steps_of_job_sequence(self, value1, value2):
        return MockReturn({'steps': value2})

    def get_jobs(self, job_ids):
        result = []
        for job_id in job_ids:
            json_copy = dict(JOB_JSON)
            json_copy['id'] = job_id
            result.append(json_copy)
        return MockReturn(result)


class MockReturn:
    def __init__(self, value):
        self.response = MockResponse(value)


class MockResponse:
    def __init__(self, value):
        self.value = value

    def json(self):
        return self.value

    def get(self, job_id):
        json_copy = dict(JOB_JSON)
        json_copy['id'] = job_id
        job = Job(json_copy, MockControlHub())
        return job


@pytest.fixture(scope="function")
def job_sequence_with_steps():
    json = deepcopy(JOB_SEQUENCE_WITH_STEPS_JSON)
    return JobSequence(json, MockControlHub())


@pytest.fixture(scope="function")
def job_within_job_sequence():
    json = deepcopy(JOB_WITHIN_JOB_SEQUENCE_JSON)
    return Job(json, MockControlHub())


@pytest.fixture(scope="function")
def dummy_jobs():
    jobs = []
    for i in range(NUM_OF_JOBS):
        json_copy = dict(JOB_JSON)
        json_copy['id'] = i
        jobs.append(Job(json_copy, MockControlHub()))

    return jobs


def test_step_jobs(job_sequence_with_steps):
    step = job_sequence_with_steps.steps[0]

    assert isinstance(step.step_jobs, SeekableList)
    assert len(step.step_jobs) == 1
    assert isinstance(step.step_jobs[0], Job)
    assert step._data['jobs'][0]['jobId'] == step.step_jobs[0].job_id


def test_remove_jobs(job_sequence_with_steps):
    step = job_sequence_with_steps.steps[0]
    step_jobs = step.step_jobs

    assert len(step_jobs) == 1
    id = step.id
    job_to_remove = step_jobs[0]

    step.remove_jobs(job_to_remove)

    assert step._data['id'] == id
    assert len(step._data['jobIds']) == 0


def test_remove_jobs_invalid_type(job_sequence_with_steps):
    step = job_sequence_with_steps.steps[0]

    with pytest.raises(TypeError):
        step.remove_jobs('invalid string')


def test_remove_jobs_with_job_that_isnt_in_step(job_sequence_with_steps):
    step1, step2 = job_sequence_with_steps.steps[0], job_sequence_with_steps.steps[1]

    with pytest.raises(ValueError):
        step1.remove_jobs(step2.step_jobs[0])


def test_add_job_incorrect_jobs_type(job_sequence_with_steps):
    step = job_sequence_with_steps.steps[0]

    with pytest.raises(TypeError):
        step.add_jobs('1')

    with pytest.raises(TypeError):
        step.add_jobs(['1'])


def test_add_job_incorrect_ignore_error_type(job_sequence_with_steps, dummy_jobs):
    step = job_sequence_with_steps.steps[0]
    job = dummy_jobs[0]
    job._data['jobSequence'] = None

    with pytest.raises(TypeError):
        step.add_jobs([job], ignore_error='1')


def test_add_job_with_job_that_is_in_another_job_sequence(job_sequence_with_steps, dummy_jobs):
    step = job_sequence_with_steps.steps[0]
    job = dummy_jobs[0]
    job._data['jobSequence'] = job_sequence_with_steps

    with pytest.raises(ValueError):
        step.add_jobs([job])


def test_change_step_name(job_sequence_with_steps):
    step = job_sequence_with_steps.steps[0]
    assert step.name == 'Step 1'

    step.name = 'My new step'
    assert step.name == 'My new step'
