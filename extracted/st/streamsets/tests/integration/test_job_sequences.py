# Copyright 2024 StreamSets Inc.

# fmt: off
import pytest
import requests

from streamsets.sdk.sch_models import (
    FinishCondition, Job, JobSequence, JobSequenceBuilder, JobSequenceHistoryLog, JobSequenceHistoryLogs, Step,
)
from streamsets.sdk.utils import SeekableList, get_random_string

# fmt: on
START_TIME_2099 = 4200268800
END_TIME_2099 = 4200854400
START_TIME_2100 = 4237401600
END_TIME_2100 = 4237996800
UTC_TIME_Z0NE = 'UTC'
BASIC_CRON_TAB_MASK = '0/1 * 1/1 * ? *'


@pytest.fixture(scope="module")
def simple_pipeline(sch, sch_authoring_sdc_id):
    """A trivial pipeline:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def sample_jobs(sch, simple_pipeline, sch_executor_sdc_label):
    """A set of simple jobs based on simple pipeline."""
    job_builder = sch.get_job_builder()

    jobs = []
    for i in range(5):
        job = job_builder.build('test_simple_job_fetch_{}'.format(i), pipeline=simple_pipeline)
        job.data_collector_labels = sch_executor_sdc_label
        sch.add_job(job)
        jobs.append(job)

    try:
        yield jobs
    finally:
        for job in jobs:
            sch.delete_job(job)


def test_publish_job_sequence(sch):
    job_sequence_builder = sch.get_job_sequence_builder()
    assert isinstance(job_sequence_builder, JobSequenceBuilder)

    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)

    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    assert isinstance(job_sequence, JobSequence)
    assert not job_sequence.id
    try:
        sch.publish_job_sequence(job_sequence=job_sequence)
        assert job_sequence.id
        assert job_sequence.start_time == START_TIME_2099
        assert job_sequence.end_time == END_TIME_2099
        assert job_sequence.timezone == UTC_TIME_Z0NE
        assert job_sequence.crontab_mask == BASIC_CRON_TAB_MASK

        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence_from_sch.id == job_sequence.id
        assert job_sequence_from_sch.name == job_sequence.name
        assert job_sequence_from_sch.description == job_sequence.description
    except Exception as e:
        raise e
    finally:
        if job_sequence.id:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_delete_job_sequence(sch):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    try:
        deleted = False
        sch.publish_job_sequence(job_sequence=job_sequence)
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        sch.delete_job_sequences(job_sequence_from_sch)

        with pytest.raises(requests.exceptions.HTTPError):
            sch.job_sequences.get(id=job_sequence_from_sch.id)

        deleted = True
    except Exception as e:
        raise e
    finally:
        if job_sequence.id and not deleted:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_update_job_sequence_metadata(sch):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    try:
        sch.publish_job_sequence(job_sequence=job_sequence)
        assert job_sequence.start_time == START_TIME_2099
        assert job_sequence.end_time == END_TIME_2099
        assert job_sequence.timezone == UTC_TIME_Z0NE
        assert job_sequence.crontab_mask == BASIC_CRON_TAB_MASK

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        job_sequence.start_time = START_TIME_2100
        job_sequence.end_time = END_TIME_2100
        new_desc = get_random_string()
        job_sequence.description = new_desc
        assert job_sequence.start_time == START_TIME_2100
        assert job_sequence.end_time == END_TIME_2100
        assert job_sequence.description == new_desc

        sch.update_job_sequence_metadata(job_sequence=job_sequence)

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence.start_time == START_TIME_2100
        assert job_sequence.end_time == END_TIME_2100
        assert job_sequence.description == new_desc

    except Exception as e:
        raise e
    finally:
        sch.api_client.delete_job_sequence(job_sequence.id)


def test_job_sequences_property(sch):
    try:
        job_sequence_list = []
        number_of_job_sequences = 3
        for i in range(number_of_job_sequences):
            job_sequence_builder = sch.get_job_sequence_builder()
            job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
            job_sequence = job_sequence_builder.build(
                name='TEST Sequence {}'.format(get_random_string()),
                description='description {}'.format(get_random_string()),
            )
            sch.publish_job_sequence(job_sequence=job_sequence)
            job_sequence_list.append(job_sequence.id)
        job_sequences_from_sch = sch.job_sequences

        counter = 0
        for job_sequence in job_sequences_from_sch:
            if job_sequence.id in job_sequence_list:
                counter += 1

        assert counter == number_of_job_sequences

    except Exception as e:
        raise e
    finally:
        if job_sequence_list:
            sch.api_client.delete_job_sequences(job_sequence_list)


def test_get_and_delete_history_log_and_history_logs(sch, sample_jobs):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    try:
        sch.publish_job_sequence(job_sequence=job_sequence)
        job_sequence = sch.job_sequences.get(id=job_sequence.id)

        job1 = sample_jobs[0]
        job_sequence.add_step_with_jobs([job1])
        sch.enable_job_sequence(job_sequence)

        # Start and Stop the job sequence
        job_sequence.refresh()
        sch.run_job_sequence(job_sequence)
        sch.wait_for_job_sequence_status(job_sequence, 'ACTIVE')
        sch.wait_for_job_status(job1, 'ACTIVE')
        sch.stop_job(job1)
        job1.refresh()
        sch.wait_for_job_sequence_status(job_sequence, 'INACTIVE')
        job_sequence.refresh()

        logs = job_sequence.get_history_log()
        assert isinstance(logs, SeekableList)

        logs = job_sequence.history_logs
        assert isinstance(logs, JobSequenceHistoryLogs)
        assert isinstance(logs[0], JobSequenceHistoryLog)

        logs = job_sequence.history_logs.get_all()
        assert isinstance(logs, SeekableList)
        assert isinstance(logs[0], JobSequenceHistoryLog)

        with pytest.raises(TypeError):
            job_sequence.delete_history_logs(['dummy_value'])

        assert len(logs) != 0
        job_sequence.delete_history_logs(logs)
        assert len(job_sequence.history_logs) == 0

    except Exception as e:
        raise e
    finally:
        if job_sequence.id:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_add_steps_and_jobs_to_job_sequence(sch, sample_jobs):
    job_sequence_builder = sch.get_job_sequence_builder()

    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)

    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    job1, job2 = sample_jobs[0], sample_jobs[1]
    try:
        sch.publish_job_sequence(job_sequence=job_sequence)

        # Add step and pull from SCH
        job_sequence.add_step_with_jobs([job1])
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)

        # Make sure step has been added
        assert len(job_sequence_from_sch.steps) == 1
        step = job_sequence_from_sch.steps[0]
        assert isinstance(step, Step)

        # Add job to step and pull again
        step.add_jobs([job2])
        job_sequence_again_from_sch = sch.job_sequences.get(id=job_sequence.id)

        # Make sure extra job has been added to step and only one step exists within the Job Sequence
        assert len(job_sequence_again_from_sch.steps) == 1
        step = job_sequence_again_from_sch.steps[0]
        assert len(step.step_jobs) == 2
        assert isinstance(step.step_jobs[0], Job) and isinstance(step.step_jobs[1], Job)
        job_ids = [job.job_id for job in step.step_jobs]
        assert job1.job_id in job_ids and job2.job_id in job_ids

        # test changing step names
        job_sequence_again_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_again_from_sch.steps[0]
        assert step.name == 'Step 1'
        step.name = 'My new step'

        job_sequence_again_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_again_from_sch.steps[0]
        assert step.name == 'My new step'

    except Exception as e:
        raise e
    finally:
        if job_sequence.id:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_reorder_and_remove_jobs_from_sequence(sch, sample_jobs):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    try:
        sch.publish_job_sequence(job_sequence=job_sequence)
        job_sequence.add_step_with_jobs(sample_jobs)

        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        assert len(job_sequence_from_sch.steps) == 5

        steps = job_sequence_from_sch.steps

        # base case: make sure that our step_1_id & step_3_id are in index 0,2
        step_1_id, step_3_id = steps[0].id, steps[2].id
        assert steps[0].id == step_1_id
        assert steps[0].step_number == 1
        assert steps[2].id == step_3_id
        assert steps[2].step_number == 3

        # trigger move_step & assert it has changed in SCH
        job_sequence_from_sch.move_step(steps[0], steps[2].step_number, swap=True)
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        new_steps = job_sequence_from_sch.steps
        assert new_steps[0].id == step_3_id
        assert new_steps[2].id == step_1_id

        # Remove and assert it has change in local memory and assert it's changed in SCH
        job_sequence_from_sch.remove_step(job_sequence_from_sch.steps[2])
        assert len(job_sequence_from_sch.steps) == 4
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        assert len(job_sequence_from_sch.steps) == 4

    except Exception as e:
        raise e
    finally:
        sch.api_client.delete_job_sequence(job_sequence.id)


def test_change_status_of_job_sequence(sch, sample_jobs):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    job1 = sample_jobs[0]

    try:
        sch.publish_job_sequence(job_sequence=job_sequence)
        job_sequence.add_step_with_jobs([job1])

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence.status == 'DISABLED'

        sch.enable_job_sequence(job_sequence)
        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence.status == 'INACTIVE'

        sch.run_job_sequence(job_sequence)
        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence.status == 'ACTIVE'

        sch.stop_job(job1)
        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        assert job_sequence.status == 'INACTIVE'

    except Exception as e:
        raise e
    finally:
        if job_sequence.id:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_job_sequence_finish_conditions(sch, sample_jobs):
    # Set up Job Sequence and Jobs
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )
    job = sample_jobs[0]
    try:
        # Publish and create relevant Step with Job
        sch.publish_job_sequence(job_sequence=job_sequence)
        job_sequence.add_step_with_jobs([job])
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_from_sch.steps[0]

        # Assert finish condition has been properly created
        finish_condition = step.create_finish_condition(
            condition_type='CRON', job=job, crontab_mask=BASIC_CRON_TAB_MASK
        )
        assert isinstance(finish_condition, FinishCondition)
        assert step.finish_conditions[0].id == finish_condition.id

        # Assert changes have been made in Platform
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_from_sch.steps[0]
        assert step.finish_conditions[0].id == finish_condition.id

        # Make in-memory changes to Finish Condition
        finish_condition = step.finish_conditions[0]
        finish_condition.condition_type = 'END_TIME'
        finish_condition.end_time = END_TIME_2100
        finish_condition.timezone = UTC_TIME_Z0NE

        # Assert changes reflect in-memory
        assert finish_condition.condition_type == 'END_TIME'
        assert finish_condition.end_time == END_TIME_2100
        assert finish_condition.timezone == UTC_TIME_Z0NE

        # Reflect in Platform
        step.update_finish_condition(finish_condition)

        # Assert changes have been made in Platform
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_from_sch.steps[0]
        finish_condition = step.finish_conditions[0]
        assert finish_condition.condition_type == 'END_TIME'
        assert finish_condition.end_time == END_TIME_2100
        assert finish_condition.timezone == UTC_TIME_Z0NE

        # Make sure the appropriate job is returned
        returned_job = finish_condition.job
        assert returned_job.job_id == job.job_id

        # Delete Finish Condition
        step.delete_finish_condition(finish_condition)
        assert len(step.finish_conditions) == 0

        # Assert changes have been made in Platform
        job_sequence_from_sch = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence_from_sch.steps[0]
        assert len(step.finish_conditions) == 0

    except Exception as e:
        raise e

    finally:
        # Cleanup Job Sequence
        if job_sequence.id:
            sch.api_client.delete_job_sequence(job_sequence.id)


def test_running_a_job_sequence(sch, sample_jobs):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )

    try:
        sch.publish_job_sequence(job_sequence=job_sequence)

        job_sequence.add_step_with_jobs(sample_jobs)
        step = job_sequence.steps[2]
        assert all(step.status != 'RUNNING' for step in job_sequence.steps)
        sch.enable_job_sequence(job_sequence)

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        sch.run_job_sequence(job_sequence, start_from_step_number=step.step_number, single_step=True)

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence.steps[2]
        assert step.status == 'RUNNING'
        assert all(step.status != 'RUNNING' for step in job_sequence.steps if step.step_number != 3)
        sch.stop_job(step.step_jobs[0])
        job_sequence = sch.job_sequences.get(id=job_sequence.id)

        sch.run_job_sequence(job_sequence, start_from_step_number=4, single_step=False)
        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence.steps[3]
        assert step.status == 'RUNNING'
        assert all(step.status != 'RUNNING' for step in job_sequence.steps if step.step_number != 4)
        sch.stop_job(step.step_jobs[0])

        step = job_sequence.steps[4]
        sch.wait_for_job_status(step.step_jobs[0], 'ACTIVE')

        job_sequence = sch.job_sequences.get(id=job_sequence.id)
        step = job_sequence.steps[4]
        assert step.status == 'RUNNING'
        assert all(step.status != 'RUNNING' for step in job_sequence.steps if step.step_number != 5)
        sch.stop_job(step.step_jobs[0])

    except Exception as e:
        raise e

    finally:
        if job_sequence.id:
            job_sequence = sch.job_sequences.get(id=job_sequence.id)
            if job_sequence.status == 'ACTIVE':
                sch.disable_job_sequence(job_sequence)

            sch.api_client.delete_job_sequence(job_sequence.id)
