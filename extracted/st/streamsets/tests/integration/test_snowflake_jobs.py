# Copyright 2022 StreamSets Inc.

# fmt: off
import json
import uuid

import pytest

from streamsets.sdk.exceptions import RunError
from streamsets.sdk.sch_models import (
    ACL, Job, JobRunEvent, JobStatus, JobTimeSeriesMetric, JobTimeSeriesMetrics, Permission,
)
from streamsets.sdk.utils import SeekableList, get_random_file_path, get_random_string

# fmt: on


@pytest.fixture(scope="module")
def simple_pipeline(sch, snowflake_config):
    """A trivial pipeline:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('simple_pipeline_{}'.format(get_random_string()))
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def simple_job_template(sch, simple_pipeline):
    job_builder = sch.get_job_builder()
    job_template = job_builder.build(
        'Job Template SDK Tests {}'.format(get_random_string()),
        pipeline=simple_pipeline,
        job_template=True,
        runtime_parameters={'x': 'y', 'a': 'b'},
    )
    sch.add_job(job_template)

    try:
        yield job_template
    finally:
        sch.delete_job(job_template)


@pytest.fixture(scope="module")
def sample_jobs(sch, simple_pipeline):
    """A set of simple jobs based on simple pipeline."""
    job_builder = sch.get_job_builder()

    jobs = []
    for i in range(5):
        job = job_builder.build('test_simple_job_fetch_{}_{}'.format(i, get_random_string()), pipeline=simple_pipeline)
        sch.add_job(job)
        jobs.append(job)

    try:
        yield jobs
    finally:
        for job in jobs:
            sch.delete_job(job)


@pytest.fixture(scope="module")
def sample_user(sch):
    user_id = str(uuid.uuid4())
    user_builder = sch.get_user_builder()
    user = user_builder.build('{}@{}'.format(user_id, sch.organization), user_id, sch.default_user_email)
    sch.add_user(user)

    try:
        yield user
    finally:
        sch.delete_user(user, deactivate=True)


@pytest.mark.snowflake
def test_job_in_returns_true(sch, sample_jobs):
    assert sample_jobs[0] in sch.jobs


@pytest.mark.snowflake
def test_job_contains(sch, sample_jobs):
    job = sample_jobs[0]
    assert sch.jobs.contains(id=job.job_id)
    assert sch.jobs.contains(job_name=job.job_name)
    assert not sch.jobs.contains(id='impossible_to_clash_with_this_^%@@!$!%^!!%#RWQ')


@pytest.mark.snowflake
def test_jobs_len_works(sch, sample_jobs):
    assert len(sch.jobs) >= len(sample_jobs)


@pytest.mark.snowflake
def test_jobs_getitem_works(sample_jobs):
    job = sample_jobs[0]
    assert isinstance(job, Job)
    assert job.job_id
    # Assuming 5 to be a safe number of attributes to say that the job is populated.
    assert len(job._data) > 5


@pytest.mark.snowflake
def test_jobs_get_all_returns_seekable_list(sch):
    assert isinstance(sch.jobs.get_all(), SeekableList)


@pytest.mark.snowflake
def test_jobs_get_by_id(sch, sample_jobs):
    sample_job_id = sample_jobs[0].job_id
    job = sch.jobs.get(id=sample_job_id)
    assert isinstance(job, Job)
    assert job.job_id == sample_job_id


@pytest.mark.snowflake
def test_jobs_get_by_id_raises_value_error(sch, sample_jobs):
    job_id = sample_jobs[0].job_id
    fake_job_id = '{}zxyf'.format(job_id)
    with pytest.raises(ValueError):
        sch.jobs.get(id=fake_job_id)


@pytest.mark.snowflake
def test_jobs_cast_to_list(sch, sample_jobs):
    jobs = list(sch.jobs)
    assert isinstance(jobs, list)
    assert isinstance(jobs[0], Job)
    assert not ({job.job_id for job in sample_jobs} - {job.job_id for job in jobs})


@pytest.mark.snowflake
def test_jobs_with_filters(sch, sample_jobs):
    assert sample_jobs
    assert len(sch.jobs.get_all(organization=sch.organization, len=3)) == 3


# ACL tests
@pytest.mark.snowflake
def test_job_acl_get(sample_jobs):
    job = sample_jobs[0]
    acl = job.acl
    assert isinstance(acl, ACL)
    assert acl.resource_type == 'JOB'


@pytest.mark.snowflake
@pytest.mark.skip('Currently not testing ACL as user creation is different in StreamSets Platform.')
def test_job_acl_permissions(sch, sample_user):
    job = sch.jobs[0]
    acl = job.acl
    actions = ['READ', 'WRITE', 'EXECUTE']
    permission = acl.permission_builder.build(subject_id=sample_user.id, subject_type='USER', actions=actions)

    # Add
    acl.add_permission(permission)
    assert set(sch.jobs.get(job_id=job.job_id).acl.permissions.get(subject_id=sample_user.id).actions) == set(actions)

    # Get
    permissions = sch.jobs.get(job_id=job.job_id).acl.permissions
    assert isinstance(permissions, SeekableList)
    sample_permission = permissions[0]
    assert isinstance(sample_permission, Permission)
    actions = sample_permission.actions
    assert isinstance(actions, list)
    assert not set(actions) - {'READ', 'WRITE', 'EXECUTE'}

    # Update
    updated_actions = ['READ']
    permission.actions = updated_actions
    new_permission = sch.jobs[0].acl.permissions.get(subject_id=permission.subject_id)
    assert set(new_permission.actions) == set(updated_actions)

    # Remove
    acl.remove_permission(permission)
    with pytest.raises(ValueError):
        sch.jobs.get(job_id=job.job_id).acl.permissions.get(subject_id=sample_user.id)


@pytest.mark.snowflake
def test_job_templates_simple_instance(sch, simple_job_template):
    jobs = sch.start_job_template(simple_job_template)
    try:
        assert len(jobs) == 1
        assert jobs[0].status == 'ACTIVE'
        assert jobs[0].job_name == '{} - 1'.format(simple_job_template.job_name)
    finally:
        for job in jobs:
            sch.wait_for_job_status(job, 'INACTIVE')
            sch.delete_job(job)


@pytest.mark.snowflake
def test_job_templates_multiple_instances_counter(sch, simple_job_template):
    jobs = sch.start_job_template(simple_job_template, number_of_instances=3)
    try:
        assert len(jobs) == 3
        assert all(job.status == 'ACTIVE' for job in jobs)
        assert {job.job_name for job in jobs} == {
            '{} - {}'.format(simple_job_template.job_name, i + 1) for i in range(3)
        }
    finally:
        for job in jobs:
            sch.wait_for_job_status(job, 'INACTIVE')
            sch.delete_job(job)


@pytest.mark.snowflake
def test_job_templates_different_params_param_value(sch, simple_job_template):
    runtime_parameters = [{'x': '1', 'a': 'b'}, {'x': '2', 'a': 'b'}]
    jobs = sch.start_job_template(
        simple_job_template,
        instance_name_suffix='PARAM_VALUE',
        parameter_name='x',
        runtime_parameters=runtime_parameters,
    )
    try:
        assert len(jobs) == 2
        assert all(job.status == 'ACTIVE' for job in jobs)
        assert {job.job_name for job in jobs} == {
            '{} - {}'.format(simple_job_template.job_name, param['x']) for param in runtime_parameters
        }
    finally:
        for job in jobs:
            sch.wait_for_job_status(job, 'INACTIVE')
            sch.delete_job(job)


@pytest.mark.snowflake
@pytest.mark.skip("Will fail with JOBRUNNER_97: Action 'Upload Offset' is not supported in 'SNOWPARK' Cloud Engine.")
def test_offset(sch, simple_pipeline):
    job_builder = sch.get_job_builder()

    job = job_builder.build('test_job_offset', pipeline=simple_pipeline)
    job.enable_failover = True
    sch.add_job(job)

    try:
        # Upload offset file
        file_path = get_random_file_path(extension='json')
        with open(file_path, 'w') as offset_file:
            json.dump(
                {"version": 2, "offsets": {"$com.streamsets.datacollector.pollsource.offset$": None}}, offset_file
            )

        with open(file_path) as dummy_offset_file:
            job_with_offset = sch.upload_offset(job, offset_file=dummy_offset_file)

        assert len(job_with_offset.current_status.offsets) == 1
        assert hasattr(job_with_offset.current_status.offsets[0], 'offset')

        # Reset offset
        job_without_offset = sch.reset_origin(job_with_offset)[0]

        assert job_without_offset.current_status.offsets is None

        # Upload offset json
        with open(file_path) as dummy_offset_file:
            job_with_offset = sch.upload_offset(job, offset_json=json.load(dummy_offset_file))

        assert len(job_with_offset.current_status.offsets) == 1
        assert hasattr(job_with_offset.current_status.offsets[0], 'offset')

        # Reset offset
        job_without_offset = sch.reset_origin(job_with_offset)[0]

        assert job_without_offset.current_status.offsets is None
    finally:
        sch.delete_job(job)


@pytest.mark.xfail(reason="This test will fail until TLKT- is resolved", strict=True)
@pytest.mark.snowflake
def test_metrics(sch, sample_jobs):
    job = sample_jobs[0]

    sch.start_job(job)
    try:
        for stage in job.pipeline.stages:
            assert stage.instance_name in job.metrics().output_count
            assert stage.instance_name in job.metrics(include_error_count=True).error_count
            assert stage.instance_name in job.metrics(metric_type='RECORD_THROUGHPUT').output_count
    finally:
        sch.wait_for_job_status(job, 'INACTIVE')


@pytest.mark.snowflake
def test_history(sch, sample_jobs):
    job = sample_jobs[0]

    sch.start_job(job)

    sch.wait_for_job_status(job, 'INACTIVE')

    assert len(job.history) >= 1
    assert isinstance(job.history[0], JobStatus)

    assert len(job.history[-1].run_history) >= 2
    assert isinstance(job.history[-1].run_history[0], JobRunEvent)


@pytest.mark.snowflake
def test_import_export(sch, simple_pipeline):
    job_builder = sch.get_job_builder()
    job = job_builder.build('test_import_export_job', pipeline=simple_pipeline)
    sch.add_job(job)

    with open('/tmp/jobs_exported.zip', 'wb') as jobs_file:
        jobs_file.write(sch.export_jobs([job]))

    sch.delete_job(job)

    with open('/tmp/jobs_exported.zip', 'rb') as jobs_file:
        imported_jobs = sch.import_jobs(jobs_file)

    assert len(imported_jobs) == 1
    sch.delete_job(imported_jobs[0])


@pytest.mark.snowflake
@pytest.mark.skip('Currently skipping as it is failing and need to debug this')
def test_time_series_metrics(sch, simple_pipeline):
    job_builder = sch.get_job_builder()
    job = job_builder.build('test_job_time_series_metrics', pipeline=simple_pipeline)
    job.enable_time_series_analysis = True
    sch.add_job(job)

    sch.start_job(job)
    try:
        job_time_series_metrics = job.time_series_metrics('Record Count Time Series')
        assert isinstance(job_time_series_metrics, JobTimeSeriesMetrics)
        assert isinstance(job_time_series_metrics.input_records, JobTimeSeriesMetric)
        assert job_time_series_metrics.input_records._data['columns'] == ['time', 'count']
        assert len(job_time_series_metrics.input_records.time_series) > 0
        assert isinstance(job_time_series_metrics.input_records.time_series, dict)

        job_time_series_metrics = job.time_series_metrics('Record Throughput Time Series')
        assert isinstance(job_time_series_metrics, JobTimeSeriesMetrics)
        assert isinstance(job_time_series_metrics.input_records, JobTimeSeriesMetric)
        assert job_time_series_metrics.input_records._data['columns'] == ['time', 'm1_rate']
        assert len(job_time_series_metrics.input_records.time_series) > 0
        assert isinstance(job_time_series_metrics.input_records.time_series, dict)

        job_time_series_metrics = job.time_series_metrics('Batch Throughput Time Series')
        assert isinstance(job_time_series_metrics, JobTimeSeriesMetrics)
        assert isinstance(job_time_series_metrics.batch_counter, JobTimeSeriesMetric)
        assert job_time_series_metrics.batch_counter._data['columns'] == ['time', 'm1_rate']
        assert len(job_time_series_metrics.batch_counter.time_series) > 0
        assert isinstance(job_time_series_metrics.batch_counter.time_series, dict)

        job_time_series_metrics = job.time_series_metrics('Stage Batch Processing Timer seconds')
        assert isinstance(job_time_series_metrics, JobTimeSeriesMetrics)
        assert (
            isinstance(job_time_series_metrics.batch_processing_timer, JobTimeSeriesMetric)
            or job_time_series_metrics.batch_processing_timer is None
        )
        if job_time_series_metrics.batch_processing_timer:
            assert job_time_series_metrics.batch_processing_timer._data['columns'] == ['time', 'mean']
            assert len(job_time_series_metrics.batch_processing_timer.time_series) > 0
            assert isinstance(job_time_series_metrics.batch_processing_timer.time_series, dict)
    finally:
        sch.wait_for_job_status(job, 'INACTIVE')
        sch.delete_job(job)


@pytest.mark.snowflake
def test_update_job(sch, simple_pipeline):
    job_builder = sch.get_job_builder()
    job = job_builder.build('test_update_job', pipeline=simple_pipeline)
    sch.add_job(job)

    try:
        simple_pipeline.stages[0].label = 'Updated stage name'
        sch.publish_pipeline(simple_pipeline)

        sch.upgrade_job(job)
        job = sch.jobs.get(job_id=job.job_id)

        assert job.pipeline_commit_label == 'v2'

        pipeline_commit = simple_pipeline.commits.get(version='1')
        job.commit = pipeline_commit
        sch.update_job(job)

        assert job.pipeline_commit_label == 'v1'
        assert job.commit == pipeline_commit
    finally:
        sch.delete_job(job)


@pytest.mark.snowflake
def test_duplicate_job(sch, simple_pipeline):
    job_builder = sch.get_job_builder()
    job = job_builder.build('original job', pipeline=simple_pipeline)
    sch.add_job(job)
    try:
        duplicated_jobs = sch.duplicate_job(job)
        assert isinstance(duplicated_jobs, SeekableList)
        assert len(duplicated_jobs) == 1
        assert sch.jobs.get(job_name='{} copy'.format(job.job_name)).job_id == duplicated_jobs[0].job_id
    finally:
        try:
            for duplicated_job in duplicated_jobs:
                sch.delete_job(duplicated_job)
        finally:
            sch.delete_job(job)


@pytest.mark.snowflake
def test_duplicate_jobs(sch, simple_pipeline):
    name = str(uuid.uuid4())
    job_builder = sch.get_job_builder()
    job = job_builder.build('original job', pipeline=simple_pipeline)
    sch.add_job(job)
    try:
        duplicated_jobs = sch.duplicate_job(job, name=name, description='Testing Duplication', number_of_copies=3)
        assert isinstance(duplicated_jobs, SeekableList)
        assert len(duplicated_jobs) == 3
        for i in range(3):
            assert sch.jobs.get(job_name='{}{}'.format(name, i + 1)).job_id == duplicated_jobs[i].job_id
    finally:
        try:
            for duplicated_job in duplicated_jobs:
                sch.delete_job(duplicated_job)
        finally:
            sch.delete_job(job)


@pytest.mark.snowflake
def test_run_error(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='null-table')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('test_snowflake_run_error')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)

    job_builder = sch.get_job_builder()
    job = job_builder.build('test_run_error', pipeline=pipeline)
    sch.add_job(job)
    try:
        with pytest.raises(RunError) as e:
            sch.start_job(job)
            sch.wait_for_job_status(job, 'INACTIVE', check_failures=True)

        assert e.type is RunError
        sch.wait_for_job_status(job, 'INACTIVE')
    finally:
        sch.delete_job(job)
        sch.api_client.delete_pipeline(pipeline.pipeline_id)
