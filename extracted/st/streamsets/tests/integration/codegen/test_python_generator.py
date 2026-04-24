#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import textwrap
from pathlib import Path

import pytest

from streamsets.sdk.codegen import PythonGenerator
from streamsets.sdk.utils import get_random_string


@pytest.fixture(scope="module")
def sample_dev_to_trash_pipeline(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Raw Data Source')
    dev_data_generator.stop_after_first_batch = True

    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash

    pipeline = pipeline_builder.build(f'pipeline_sdc_test_{get_random_string()}')
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


def test_python_generator_on_pipeline_object_happy_path(
    tmp_path, args, sch_authoring_sdc_id, sample_dev_to_trash_pipeline
):
    destination_file = tmp_path / "result.py"
    generator = PythonGenerator(
        source=sample_dev_to_trash_pipeline, destination=destination_file, aster_url=args.aster_url
    )

    assert not destination_file.exists()

    generator.save()

    assert destination_file.exists()
    assert destination_file.is_file()

    assert destination_file.read_text() == textwrap.dedent(
        f"""\
    import os
    from streamsets.sdk import ControlHub


    sch = ControlHub(
        os.getenv("SCH_CREDENTIAL_ID"),
        os.getenv("SCH_TOKEN"),
        aster_url="{args.aster_url}"
    )

    engine = sch.engines.get(id="{sch_authoring_sdc_id}")
    pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)

    dev_raw_data_source_1 = pipeline_builder.add_stage("Dev Raw Data Source", type="origin")
    dev_raw_data_source_1.stop_after_first_batch = True
    trash_1 = pipeline_builder.add_stage("Trash", type="destination")

    dev_raw_data_source_1.connect_outputs(stages=[trash_1])

    pipeline = pipeline_builder.build("{sample_dev_to_trash_pipeline.name}")
    sch.publish_pipeline(pipeline)
    """
    )


def test_python_generator_on_zip_archive_pipeline_happy_path(tmpdir):
    destination_file = Path(tmpdir / "result.py")
    generator = PythonGenerator(
        source=Path(__file__).parent.parent.parent / "unit" / "resources" / "codegen" / "jdbc_pipeline_test.zip",
        destination=destination_file,
    )

    assert not destination_file.exists()

    generator.save()

    assert destination_file.exists()
    assert destination_file.is_file()

    assert destination_file.read_text() == textwrap.dedent(
        """\
    import os
    from streamsets.sdk import ControlHub


    sch = ControlHub(
        os.getenv("SCH_CREDENTIAL_ID"),
        os.getenv("SCH_TOKEN")
    )

    engine = sch.engines.get(id="942cb24c-c2d5-4619-8b8d-1adaaff412b5")
    pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)

    jdbc_query_consumer_1 = pipeline_builder.add_stage("JDBC Query Consumer", type="origin")
    jdbc_query_consumer_1.sql_query = \"\"\"select * from users where id > ${OFFSET} order by id\"\"\"
    jdbc_query_consumer_1.offset_column = "id"
    jdbc_query_consumer_1.jdbc_connection_string = "jdbc:postgresql://postgres-cdc-15.0.cluster:5432/default"
    stream_selector_1 = pipeline_builder.add_stage("Stream Selector", type="processor")
    stream_selector_1.condition = [{'outputLane': 'StreamSelector_1OutputLane1682014212086', 'predicate': '${1 == 1}'}, {'outputLane': 'StreamSelector_1OutputLane1682014211502', 'predicate': '${2 == 2}'}, {'outputLane': 'StreamSelector_1OutputLane1682014206436', 'predicate': 'default'}]
    stream_selector_1.required_fields = []
    trash_1 = pipeline_builder.add_stage("Trash", type="destination")
    trash_2 = pipeline_builder.add_stage("Trash", type="destination")
    trash_3 = pipeline_builder.add_stage("Trash", type="destination")

    jdbc_query_consumer_1.connect_outputs(stages=[stream_selector_1])
    stream_selector_1.connect_outputs(stages=[trash_1], output_lane_index=0)
    stream_selector_1.connect_outputs(stages=[trash_2], output_lane_index=1)
    stream_selector_1.connect_outputs(stages=[trash_3], output_lane_index=2)

    pipeline = pipeline_builder.build("JDBC pipeline created using SDK with stream selector")
    sch.publish_pipeline(pipeline)
    """
    )
