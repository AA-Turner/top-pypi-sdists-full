# Copyright 2022 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.utils import get_random_string

# fmt: on

NUM_PIPELINES = 12
NUM_JOBS = 5


@pytest.fixture(scope="module")
def sample_pipelines(resources_label, sch, sch_authoring_sdc_id):
    """A set of trivial pipelines:

    dev_data_generator >> trash
    """
    pipelines = []
    try:
        for i in range(NUM_PIPELINES):
            pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
            dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
            trash = pipeline_builder.add_stage('Trash')
            dev_data_generator >> trash
            pipeline_name = 'simple_saql_pipeline_{}_{}_{}_{}'.format(
                'even' if i % 2 == 0 else 'odd', resources_label, i, get_random_string()
            )
            pipeline = pipeline_builder.build(pipeline_name)
            sch.publish_pipeline(pipeline)

            pipelines.append(pipeline)

        yield pipelines
    finally:
        for pipeline in pipelines:
            sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def sample_fragments(resources_label, sch, sch_authoring_sdc_id):
    """A set of trivial pipelines:

    dev_data_generator >> trash
    """
    pipelines = []
    try:
        for i in range(NUM_PIPELINES):
            pipeline_builder = sch.get_pipeline_builder(
                engine_type='data_collector', engine_id=sch_authoring_sdc_id, fragment=True
            )
            dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
            trash = pipeline_builder.add_stage('Trash')
            dev_data_generator >> trash
            pipeline_name = 'simple_saql_fragments_{}_{}_{}_{}'.format(
                'even' if i % 2 == 0 else 'odd', resources_label, i, get_random_string()
            )
            pipeline = pipeline_builder.build(pipeline_name)
            sch.publish_pipeline(pipeline)

            pipelines.append(pipeline)

        yield pipelines
    finally:
        for pipeline in pipelines:
            sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def simple_pipeline(resources_label, sch, sch_authoring_sdc_id):
    """A trivial pipeline:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple_saql_draft_{}_{}'.format(resources_label, get_random_string()))
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def sample_jobs(resources_label, sch, simple_pipeline, sch_executor_sdc_label):
    """A set of simple jobs based on simple pipeline."""
    job_builder = sch.get_job_builder()

    jobs = []
    for i in range(NUM_JOBS):
        job = job_builder.build(
            'test_simple_saql_job_fetch_{}_{}_{}'.format(resources_label, i, get_random_string()),
            pipeline=simple_pipeline,
        )
        job.data_collector_labels = sch_executor_sdc_label
        sch.add_job(job)
        jobs.append(job)

    try:
        yield jobs
    finally:
        for job in jobs:
            sch.delete_job(job)


@pytest.fixture(scope="module")
def sample_job_templates(resources_label, sch, simple_pipeline, sch_executor_sdc_label):
    job_builder = sch.get_job_builder()

    jobs = []
    for i in range(NUM_JOBS):
        job = job_builder.build(
            'test_simple_saql_job_fetch_{}_{}_{}'.format(resources_label, i, get_random_string()),
            pipeline=simple_pipeline,
            job_template=True,
            runtime_parameters={'x': 'y', 'a': 'b'},
        )
        job.data_collector_labels = sch_executor_sdc_label
        sch.add_job(job)
        jobs.append(job)

    try:
        yield jobs
    finally:
        for job in jobs:
            sch.delete_job(job)


def test_saql_search_on_pipelines(resources_label, sch, sample_pipelines):
    even_pipelines = sch.pipelines.get_all(search="name==simple_saql_pipeline_even_{}*".format(resources_label))
    assert len(even_pipelines) == (NUM_PIPELINES / 2)
    odd_pipelines = sch.pipelines.get_all(search="name==simple_saql_pipeline_odd_{}*".format(resources_label))
    assert len(odd_pipelines) == (NUM_PIPELINES / 2)
    null_pipelines = sch.pipelines.get_all(search="name==DOES_NOT_EXIST")
    assert len(null_pipelines) == 0


def test_saql_search_on_fragments(resources_label, sch, sample_fragments):
    even_fragments = sch.pipelines.get_all(
        fragment=True, search="name==simple_saql_fragments_even_{}*".format(resources_label)
    )
    assert len(even_fragments) == (NUM_PIPELINES / 2)
    odd_fragments = sch.pipelines.get_all(
        fragment=True, search="name==simple_saql_fragments_odd_{}*".format(resources_label)
    )
    assert len(odd_fragments) == (NUM_PIPELINES / 2)
    null_fragments = sch.pipelines.get_all(fragment=True, search="name==DOES_NOT_EXIST")
    assert len(null_fragments) == 0


def test_saql_search_on_jobs(resources_label, sch, sample_jobs):
    simple_jobs = sch.jobs.get_all(search="name=='test_simple_saql_job_fetch_{}*'".format(resources_label))
    assert len(simple_jobs) == NUM_JOBS
    null_jobs = sch.jobs.get_all(search="name==DOES_NOT_EXIST")
    assert len(null_jobs) == 0


def test_saql_search_on_job_templates(resources_label, sch, sample_job_templates):
    simple_job_templates = sch.jobs.get_all(
        search="name=='test_simple_saql_job_fetch_{}*'".format(resources_label), job_template=True
    )
    assert len(simple_job_templates) == NUM_JOBS
    null_job_templates = sch.jobs.get_all(search="name==DOES_NOT_EXIST", job_template=True)
    assert len(null_job_templates) == 0
