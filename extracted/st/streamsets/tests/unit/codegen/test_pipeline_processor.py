#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2026
import textwrap

from streamsets.sdk.codegen.processors import PipelineProcessor
from streamsets.sdk.codegen.sources.source import PipelineDto


def test_processor_stages_connection_as_str_method(test_data_json_jdbc):
    processor = PipelineProcessor(
        source_data=PipelineDto(
            pipeline_config=test_data_json_jdbc["pipelineConfig"],
            pipeline_rules={},
            library_definitions=test_data_json_jdbc["libraryDefinitions"],
        ),
        sch_credential_id="",
        sch_token="",
    )

    assert processor.stages_connection_as_str() == textwrap.dedent(
        """\
    jdbc_query_consumer_1.connect_outputs(stages=[stream_selector_1])
    stream_selector_1.connect_outputs(stages=[trash_1], output_lane_index=0)
    stream_selector_1.connect_outputs(stages=[trash_2], output_lane_index=1)
    stream_selector_1.connect_outputs(stages=[trash_3], output_lane_index=2)"""
    )


def test_processor_stages_connection_as_str_method_with_event_stage(test_data_json_with_event_stage):
    processor = PipelineProcessor(
        source_data=PipelineDto(
            pipeline_config=test_data_json_with_event_stage["pipelineConfig"],
            pipeline_rules={},
            library_definitions=test_data_json_with_event_stage["libraryDefinitions"],
        ),
        sch_credential_id="",
        sch_token="",
    )

    assert processor.stages_connection_as_str() == textwrap.dedent(
        """\
    dev_raw_data_source_1.connect_outputs(stages=[trash_1])
    dev_raw_data_source_1.connect_outputs(stages=[pipeline_finisher_executor_1], event_lane=True)"""
    )


def test_processor_stages_as_str_method(test_data_json_jdbc):
    processor = PipelineProcessor(
        source_data=PipelineDto(
            pipeline_config=test_data_json_jdbc["pipelineConfig"],
            pipeline_rules={},
            library_definitions=test_data_json_jdbc["libraryDefinitions"],
        ),
        sch_credential_id="",
        sch_token="",
    )
    assert processor.stages_as_str() == textwrap.dedent(
        """\
    jdbc_query_consumer_1 = pipeline_builder.add_stage("JDBC Query Consumer", type="origin")
    jdbc_query_consumer_1.sql_query = \"\"\"select * from users where id > ${OFFSET} order by id\"\"\"
    jdbc_query_consumer_1.offset_column = "id"
    jdbc_query_consumer_1.jdbc_connection_string = "jdbc:postgresql://postgres-cdc-15.0.cluster:5432/default"
    stream_selector_1 = pipeline_builder.add_stage("Stream Selector", type="processor")
    stream_selector_1.condition = [{'outputLane': 'StreamSelector_1OutputLane1682014212086', 'predicate': '${1 == 1}'}, {'outputLane': 'StreamSelector_1OutputLane1682014211502', 'predicate': '${2 == 2}'}, {'outputLane': 'StreamSelector_1OutputLane1682014206436', 'predicate': 'default'}]
    stream_selector_1.required_fields = []
    trash_1 = pipeline_builder.add_stage("Trash", type="destination")
    trash_2 = pipeline_builder.add_stage("Trash", type="destination")
    trash_3 = pipeline_builder.add_stage("Trash", type="destination")"""
    )


def test_pipeline_processor_happy_path(test_data_json_jdbc):
    processor = PipelineProcessor(
        source_data=PipelineDto(
            pipeline_config=test_data_json_jdbc["pipelineConfig"],
            pipeline_rules={},
            library_definitions=test_data_json_jdbc["libraryDefinitions"],
        ),
        sch_credential_id="SCH_CREDENTIAL_ID",
        sch_token="SCH_TOKEN",
    )
    assert str(processor.run()) == textwrap.dedent(
        f"""\
    import os
    from streamsets.sdk import ControlHub


    sch = ControlHub(
        os.getenv("SCH_CREDENTIAL_ID"),
        os.getenv("SCH_TOKEN")
    )

    engine = sch.engines.get(id="{test_data_json_jdbc["pipelineConfig"]["info"]["sdcId"]}")
    pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)

    jdbc_query_consumer_1 = pipeline_builder.add_stage("JDBC Query Consumer", type="origin")
    jdbc_query_consumer_1.sql_query = \"\"\"select * from users where id > ${{OFFSET}} order by id\"\"\"
    jdbc_query_consumer_1.offset_column = "id"
    jdbc_query_consumer_1.jdbc_connection_string = "jdbc:postgresql://postgres-cdc-15.0.cluster:5432/default"
    stream_selector_1 = pipeline_builder.add_stage("Stream Selector", type="processor")
    stream_selector_1.condition = [{{'outputLane': 'StreamSelector_1OutputLane1682014212086', 'predicate': '${{1 == 1}}'}}, {{'outputLane': 'StreamSelector_1OutputLane1682014211502', 'predicate': '${{2 == 2}}'}}, {{'outputLane': 'StreamSelector_1OutputLane1682014206436', 'predicate': 'default'}}]
    stream_selector_1.required_fields = []
    trash_1 = pipeline_builder.add_stage("Trash", type="destination")
    trash_2 = pipeline_builder.add_stage("Trash", type="destination")
    trash_3 = pipeline_builder.add_stage("Trash", type="destination")

    jdbc_query_consumer_1.connect_outputs(stages=[stream_selector_1])
    stream_selector_1.connect_outputs(stages=[trash_1], output_lane_index=0)
    stream_selector_1.connect_outputs(stages=[trash_2], output_lane_index=1)
    stream_selector_1.connect_outputs(stages=[trash_3], output_lane_index=2)

    pipeline = pipeline_builder.build("{test_data_json_jdbc["pipelineConfig"]["title"]}")
    sch.publish_pipeline(pipeline)
    """
    )
