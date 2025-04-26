# fmt: off
import pytest

from streamsets.sdk.sch_models import TopologyNode

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
    pipeline = pipeline_builder.build('simple_pipeline')
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.api_client.delete_pipeline(pipeline.pipeline_id)


@pytest.fixture(scope="module")
def sample_job(sch, simple_pipeline, sch_executor_sdc_label):
    """A simple jobs based on a simple pipeline."""
    job_builder = sch.get_job_builder()
    job = job_builder.build('test_simple_job_fetch', pipeline=simple_pipeline)
    job.data_collector_labels = sch_executor_sdc_label
    sch.add_job(job)

    try:
        yield job
    finally:
        sch.delete_job(job)


def test_topology_publish_ability(sch, sample_job):
    topology_builder = sch.get_topology_builder()
    topology_builder.add_job(sample_job)
    assert topology_builder._topology['topologyDefinition']['topologyNodes'][0]['jobId'] == sample_job.job_id
    sample_topology = topology_builder.build("sample_topology")
    sch.publish_topology(sample_topology)
    try:
        assert sch.topologies.get(topology_name='sample_topology').topology_id == sample_topology.topology_id
    finally:
        sch.delete_topology(sample_topology)


def test_topology_builder_access_nodes_after_publish(sch, sample_job):
    topology_builder = sch.get_topology_builder()
    topology_builder.add_job(sample_job)
    assert isinstance(topology_builder.topology_nodes[0], TopologyNode)
    sample_topology = topology_builder.build("sample_topology")
    sch.publish_topology(sample_topology)
    try:
        assert isinstance(topology_builder.topology_nodes[0], TopologyNode)
    finally:
        sch.delete_topology(sample_topology)
