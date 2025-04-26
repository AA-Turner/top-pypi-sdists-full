# Copyright 2023 StreamSets Inc.

# fmt: off
import datetime
import time

import pytest

from streamsets.sdk.sch_models import ScheduledTask, ScheduledTaskAudit, ScheduledTaskRun
from streamsets.sdk.utils import SeekableList, get_random_string

# fmt: on


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
def sample_job(sch, simple_pipeline, sch_executor_sdc_label):
    """A set of simple jobs based on simple pipeline."""
    job_builder = sch.get_job_builder()

    job = job_builder.build('test_simple_job', pipeline=simple_pipeline)
    job.data_collector_labels = sch_executor_sdc_label
    sch.add_job(job)

    try:
        yield job
    finally:
        if job.status == 'ACTIVE':
            sch.stop_job(job, force=True)
            time.sleep(10)
        sch.delete_job(job)


def test_scheduler_operations(sample_job, sch):
    if len(sch.data_collectors) < 1:
        pytest.skip('This test requires atleast one data collector')
    # Create
    task_name = 'Task for job {}'.format(sample_job.job_name)
    task = sch.get_scheduled_task_builder().build(
        task_object=sample_job,
        action='START',
        name=task_name,
        description='Scheduled task for job {}'.format(sample_job.job_name),
        cron_expression='0/1 * 1/1 * ? *',
        time_zone='UTC',
        status='RUNNING',
        start_time=None,
        end_time=None,
        missed_execution_handling='IGNORE',
    )
    sch.add_scheduled_task(task)

    # Get
    assert isinstance(task, ScheduledTask)
    assert task.status == 'RUNNING'
    assert task.name == task_name

    # Runs
    # Wait for 1+ minutes for the run to execute
    time.sleep(65)
    runs = task.runs
    assert len(runs) >= 1
    assert isinstance(runs, SeekableList)
    assert isinstance(runs[0], ScheduledTaskRun)
    task_run_time = datetime.datetime.utcfromtimestamp(runs[0].scheduled_time / 1000)
    current_time = datetime.datetime.utcnow()
    # Assert that the task started running before current_time.
    assert (current_time - task_run_time).total_seconds() > 0
    sample_job = sch.jobs.get(job_id=sample_job.job_id)
    assert sample_job.status == 'ACTIVE' or sample_job.status == 'ACTIVATING'

    # Actions
    sch.pause_scheduled_tasks(task)
    assert task.status == 'PAUSED'
    sch.resume_scheduled_tasks(task)
    assert task.status == 'RUNNING'

    # Audits
    audits = task.audits
    assert len(audits) >= 3
    assert isinstance(audits, SeekableList)
    assert isinstance(audits[0], ScheduledTaskAudit)
    # current_time variable is being used from above Runs section.
    # Assert that the task was created before current_time.
    assert (
        current_time - datetime.datetime.utcfromtimestamp(audits.get(action='CREATE').time / 1000)
    ).total_seconds() > 0
    # Assert that the task was paused after current_time.
    assert (
        current_time - datetime.datetime.utcfromtimestamp(audits.get(action='PAUSE').time / 1000)
    ).total_seconds() < 0
    # Assert that the task was resumed after current_time.
    assert (
        current_time - datetime.datetime.utcfromtimestamp(audits.get(action='RESUME').time / 1000)
    ).total_seconds() < 0

    # More actions
    sch.kill_scheduled_tasks(task)
    assert task.status == 'KILLED'
    sch.delete_scheduled_tasks(task)
    assert task.status == 'DELETED'


def test_scheduler_stop_job(sample_job, sch):
    if len(sch.data_collectors) < 1:
        pytest.skip('This test requires at least one data collector')

    sample_job = sch.jobs.get(job_id=sample_job.job_id)
    if sample_job.status != 'ACTIVE':
        sch.start_job(sample_job)

    task_name = 'Stop task for job {}'.format(sample_job.job_name)
    task = sch.get_scheduled_task_builder().build(
        task_object=sample_job,
        action='STOP',
        name=task_name,
        description='Scheduled task for job {}'.format(sample_job.job_name),
        cron_expression='0/1 * 1/1 * ? *',
        time_zone='UTC',
        status='RUNNING',
        start_time=None,
        end_time=None,
        missed_execution_handling='IGNORE',
    )
    sch.add_scheduled_task(task)
    time.sleep(65)
    runs = task.runs
    assert len(runs) >= 1
    sample_job = sch.jobs.get(job_id=sample_job.job_id)
    assert sample_job.status == 'INACTIVE' or sample_job.status == 'DEACTIVATING'
    sch.kill_scheduled_tasks(task)
    assert task.status == 'KILLED'
    sch.delete_scheduled_tasks(task)
    assert task.status == 'DELETED'
