# Copyright 2024 StreamSets Inc.

# fmt: off
from copy import deepcopy

import pytest

from streamsets.sdk.sch import ControlHub
from streamsets.sdk.sch_models import JobSequence, JobSequenceBuilder

from .resources.conftest_data import JOB_SEQUENCE_BUILDER_JSON, JOB_SEQUENCE_EMPTY_JSON

# fmt: on

START_TIME_2099 = 4200268800
END_TIME_2099 = 4200268800
START_TIME_2100 = 4237401600
END_TIME_2100 = 4237996800
UTC_TIME_Z0NE = 'UTC'
BASIC_CRON_TAB_MASK = '0/1 * 1/1 * ? *'
NUM_OF_STEPS = 4
NUM_OF_JOBS = 3


class MockControlHub:
    def __init__(self):
        self.organization = 'DUMMY ORG'

    @property
    def _sequencing_api(self):
        return {'definitions': {'USequence': deepcopy(JOB_SEQUENCE_BUILDER_JSON)}}


def test_get_job_sequence_builder_build():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())
    assert isinstance(job_sequence_builder, JobSequenceBuilder)
    assert isinstance(job_sequence_builder._control_hub, MockControlHub)

    assert job_sequence_builder._job_sequence == deepcopy(JOB_SEQUENCE_EMPTY_JSON)

    name, description = 'TEST NAME', 'TEST DESC'
    job_sequence = job_sequence_builder.build(name=name, description=description)
    assert isinstance(job_sequence, JobSequence)
    assert isinstance(job_sequence._control_hub, MockControlHub)
    assert job_sequence.name == name
    assert job_sequence.description == description


def test_get_job_sequence_builder_build_with_incorrect_types():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())

    name, description = 'TEST NAME', 'TEST DESC'

    with pytest.raises(TypeError):
        job_sequence_builder.build(name=123, description=description)

    with pytest.raises(TypeError):
        job_sequence_builder.build(name=name, description=123)


def test_get_job_sequence_builder_build_with_default_values():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())
    job_sequence = job_sequence_builder.build()
    assert job_sequence.name == 'Job Sequence'
    assert job_sequence.description is None


def test_get_job_sequence_builder_add_start_condition():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())
    assert job_sequence_builder._job_sequence == deepcopy(JOB_SEQUENCE_EMPTY_JSON)

    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    assert job_sequence_builder._job_sequence['startTime'] == START_TIME_2099
    assert job_sequence_builder._job_sequence['endTime'] == END_TIME_2099
    assert job_sequence_builder._job_sequence['timezone'] == UTC_TIME_Z0NE
    assert job_sequence_builder._job_sequence['crontabMask'] == BASIC_CRON_TAB_MASK


def test_get_job_sequence_builder_add_start_condition_incorrect_types():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())

    with pytest.raises(TypeError):
        job_sequence_builder.add_start_condition('STRING', END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)

    with pytest.raises(TypeError):
        job_sequence_builder.add_start_condition(START_TIME_2099, 'STRING', UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)

    with pytest.raises(TypeError):
        job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, 123, BASIC_CRON_TAB_MASK)

    with pytest.raises(TypeError):
        job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, 123)


def test_get_job_sequence_builder_add_start_condition_with_default_values():
    job_sequence_builder = ControlHub.get_job_sequence_builder(MockControlHub())

    job_sequence_builder.add_start_condition()
    assert job_sequence_builder._job_sequence['startTime'] == 0
    assert job_sequence_builder._job_sequence['endTime'] == 0
    assert job_sequence_builder._job_sequence['timezone'] == UTC_TIME_Z0NE
    assert job_sequence_builder._job_sequence['crontabMask'] == BASIC_CRON_TAB_MASK
