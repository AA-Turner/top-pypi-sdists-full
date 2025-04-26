# Copyright 2022 StreamSets Inc.
# fmt: off
import pytest

from streamsets.sdk.utils import get_random_string

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
    pipeline = pipeline_builder.build('simple_draft_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline, draft=True)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def simple_draft_run(sch, sch_authoring_sdc_id, simple_pipeline):
    """A trivial draft run:"""
    start_draft_command = sch.start_draft_run(simple_pipeline)
    start_draft_command.wait_for_job_status('ACTIVE')
    draft_run_obj = sch.draft_runs.get(search="id=='{}'".format(start_draft_command.response.json()['jobId']))

    try:
        yield draft_run_obj
    finally:
        sch.stop_draft_run(draft_run_obj)
        sch.delete_draft_run(draft_run_obj)


def test_draft_run_snapshot(sch, simple_draft_run):
    simple_draft_run.capture_snapshot()
    simple_draft_run.wait_for_finished_snapshot()
    snapshots = simple_draft_run.snapshots
    assert snapshots[0].name == "Snapshot1"
    assert snapshots[-1].batches is not None

    simple_draft_run.capture_snapshot()
    simple_draft_run.wait_for_finished_snapshot()
    snapshots = simple_draft_run.snapshots
    assert len(snapshots) == 2
    assert snapshots[-1].id is not None
    assert snapshots[1].time_stamp > snapshots[0].time_stamp

    simple_draft_run.remove_snapshot(snapshots[0])
    snapshots = simple_draft_run.snapshots
    assert len(snapshots) == 1

    simple_draft_run.remove_snapshot(snapshots[0])
    assert len(simple_draft_run.snapshots) == 0


def test_draft_run_logs(sch, simple_draft_run):
    logs = simple_draft_run.get_logs()
    assert logs is not None
