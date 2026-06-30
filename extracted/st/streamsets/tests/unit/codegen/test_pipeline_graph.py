#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2026
import textwrap

import pytest

from streamsets.sdk.codegen.processors.pipeline_processor.pipeline_graph import StageVertex
from streamsets.sdk.codegen.processors.pipeline_processor.pipeline_processor import DefaultStageDefinition

from .test_utils import find_default_stage_definition, find_stage_definition


@pytest.fixture(scope="function")
def multiple_output_stage_data(test_data_json_jdbc) -> dict:
    return find_stage_definition(
        test_data_json_jdbc, "com_streamsets_pipeline_stage_processor_selector_SelectorDProcessor"
    )


@pytest.fixture(scope="function")
def multiple_output_stage_default_definition(test_data_json_jdbc) -> DefaultStageDefinition:
    stream_selector_definition = find_default_stage_definition(
        test_data_json_jdbc, "com_streamsets_pipeline_stage_processor_selector_SelectorDProcessor"
    )

    return DefaultStageDefinition(
        label=stream_selector_definition["label"],
        type=stream_selector_definition["type"],
        config_definitions=stream_selector_definition["configDefinitions"],
    )


@pytest.fixture(scope="function")
def jdbc_query_consumer_source_stage_data(test_data_json_jdbc) -> dict:
    return find_stage_definition(test_data_json_jdbc, "com_streamsets_pipeline_stage_origin_jdbc_JdbcDSource")


@pytest.fixture(scope="function")
def jdbc_query_consumer_source_stage_data_default_definition(test_data_json_jdbc) -> DefaultStageDefinition:
    stage_definition = find_default_stage_definition(
        test_data_json_jdbc, "com_streamsets_pipeline_stage_origin_jdbc_JdbcDSource"
    )

    return DefaultStageDefinition(
        label=stage_definition["label"],
        type=stage_definition["type"],
        config_definitions=stage_definition["configDefinitions"],
    )


def test_multiple_output_stage_str_representation(multiple_output_stage_data, multiple_output_stage_default_definition):
    stage = StageVertex(
        instance_name="A",
        stage_data=multiple_output_stage_data,
        default_stage_definition=multiple_output_stage_default_definition,
    )
    assert str(stage) == textwrap.dedent("""\
    stream_selector = pipeline_builder.add_stage("Stream Selector", type="processor")
    stream_selector.condition = [{'outputLane': 'StreamSelector_1OutputLane1682014212086', 'predicate': '${1 == 1}'}, {'outputLane': 'StreamSelector_1OutputLane1682014211502', 'predicate': '${2 == 2}'}, {'outputLane': 'StreamSelector_1OutputLane1682014206436', 'predicate': 'default'}]
    stream_selector.required_fields = []""")


def test_dev_raw_data_source_stage_str_representation(
    jdbc_query_consumer_source_stage_data, jdbc_query_consumer_source_stage_data_default_definition
):
    stage = StageVertex(
        instance_name="A",
        stage_data=jdbc_query_consumer_source_stage_data,
        default_stage_definition=jdbc_query_consumer_source_stage_data_default_definition,
    )
    assert str(stage) == textwrap.dedent("""\
    jdbc_query_consumer = pipeline_builder.add_stage("JDBC Query Consumer", type="origin")
    jdbc_query_consumer.sql_query = \"\"\"select * from users where id > ${OFFSET} order by id\"\"\"
    jdbc_query_consumer.offset_column = "id"
    jdbc_query_consumer.jdbc_connection_string = "jdbc:postgresql://postgres-cdc-15.0.cluster:5432/default\"""")


def test_stage_vertex_stage_configuration_skips_none_missing_and_defaults():
    default_stage_def = DefaultStageDefinition(
        label="Dummy",
        type="PROCESSOR",
        config_definitions=[
            {"name": "x", "fieldName": "x", "type": "int", "defaultValue": 0},
            {"name": "y", "fieldName": "y", "type": "string", "defaultValue": ""},
            {"name": "z", "fieldName": "z", "type": "boolean", "defaultValue": False},
        ],
    )

    stage_data = {
        "configuration": [
            {"name": "x"},  # no "value" -> skipped
            {"name": "y", "value": None},  # None -> skipped
            {"name": "x", "value": 0},  # defaultValue -> skipped
            {"name": "z", "value": False},  # defaultValue -> skipped
            {"name": "x", "value": 5},  # kept
        ],
        "outputLanes": ["lane1"],
    }

    v = StageVertex(instance_name="A", stage_data=stage_data, default_stage_definition=default_stage_def)
    assert v.stage_configuration() == "dummy.x = 5"


def test_stage_vertex_format_config_value():
    default_stage_def = DefaultStageDefinition(
        label="Dummy",
        type="PROCESSOR",
        config_definitions=[
            {"name": "delay", "fieldName": "delay", "type": "int", "defaultValue": 0},
            {"name": "ratio", "fieldName": "ratio", "type": "double", "defaultValue": 0.0},
            {"name": "enabled", "fieldName": "enabled", "type": "boolean", "defaultValue": False},
            {"name": "note", "fieldName": "note", "type": "string", "defaultValue": ""},
        ],
    )

    stage_data = {
        "configuration": [
            {"name": "delay", "value": 1000},
            {"name": "ratio", "value": "1.25"},
            {"name": "enabled", "value": "true"},
            {"name": "note", "value": 'a"b'},
        ],
        "outputLanes": ["lane1"],
    }

    v = StageVertex(instance_name="A", stage_data=stage_data, default_stage_definition=default_stage_def)

    assert v.stage_configuration() == textwrap.dedent("""\
        dummy.delay = 1000
        dummy.ratio = 1.25
        dummy.enabled = True
        dummy.note = "a\\"b\"""").strip()


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("true", "True"),
        ("True", "True"),
        ("1", "True"),
        ("yes", "True"),
        ("y", "True"),
        ("on", "True"),
        ("false", "False"),
        ("False", "False"),
        ("0", "False"),
        ("no", "False"),
        ("n", "False"),
        ("off", "False"),
        (True, "True"),
        (False, "False"),
        (1, "True"),
        (0, "False"),
    ],
)
def test_format_boolean_values(raw, expected):
    default_stage_def = DefaultStageDefinition(
        label="Dummy",
        type="PROCESSOR",
        config_definitions=[{"name": "enabled", "fieldName": "enabled", "type": "boolean", "defaultValue": None}],
    )
    stage_data = {"configuration": [{"name": "enabled", "value": raw}], "outputLanes": ["lane1"]}
    v = StageVertex(instance_name="A", stage_data=stage_data, default_stage_definition=default_stage_def)

    assert v.stage_configuration() == f"dummy.enabled = {expected}"


def test_float_fallback_to_repr_on_parse_error():
    default_stage_def = DefaultStageDefinition(
        label="Dummy",
        type="PROCESSOR",
        config_definitions=[{"name": "ratio", "fieldName": "ratio", "type": "double", "defaultValue": 0.0}],
    )
    stage_data = {"configuration": [{"name": "ratio", "value": "not-a-number"}], "outputLanes": ["lane1"]}
    v = StageVertex(instance_name="A", stage_data=stage_data, default_stage_definition=default_stage_def)

    assert v.stage_configuration() == "dummy.ratio = 'not-a-number'"
