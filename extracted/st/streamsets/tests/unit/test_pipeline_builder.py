#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024


from contextlib import nullcontext
from unittest.mock import ANY

# fmt: off
import pytest

from streamsets.sdk.sdc_models import PipelineBuilder as SdcPipelineBuilder
from streamsets.sdk.st_models import PipelineBuilder as StPipelineBuilder

from .resources.pipeline_builder_data import CONFIG_TYPE_TEST_CASES_JSON as CONFIG_TYPE_TEST_CASES

# fmt: on


@pytest.mark.parametrize(
    'pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_snowflake_pipeline_builder', 'sch_st_pipeline_builder']
)
def test_pipeline_builder_add_stage_stage_exist(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    stage_to_add = "Trash"
    pipeline_builder.add_stage(stage_to_add)
    dummy_pipeline_stage = pipeline_builder._pipeline[pipeline_builder._config_key]['stages'][0]
    assert stage_to_add in dummy_pipeline_stage["instanceName"]


def test_pipeline_builder_add_stage_stage_with_shorthand_library_name(sch_sdc_pipeline_builder):
    stage_to_add = "Trash"
    sch_sdc_pipeline_builder.add_stage(stage_to_add, library='basic')
    dummy_pipeline_stage = sch_sdc_pipeline_builder._pipeline[sch_sdc_pipeline_builder._config_key]['stages'][0]
    assert stage_to_add in dummy_pipeline_stage["instanceName"]


@pytest.mark.parametrize(
    'pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_snowflake_pipeline_builder', 'sch_st_pipeline_builder']
)
def test_pipeline_builder_add_stage_stage_does_not_exist(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    fake_stage_name = "Cannot Exist"
    with pytest.raises(Exception) as e:
        pipeline_builder.add_stage(fake_stage_name)
    assert str(e.value) == "Could not find stage ({}).".format(fake_stage_name)


@pytest.mark.parametrize(
    'pipeline_builder', ['sch_sdc_pipeline_builder', 'sch_snowflake_pipeline_builder', 'sch_st_pipeline_builder']
)
def test_add_stage_supported_types(pipeline_builder, request):
    pipeline_builder = request.getfixturevalue(pipeline_builder)
    snowflake_destination = pipeline_builder.add_stage('Snowflake', type='destination')

    assert 'STREAMSETS_SNOWFLAKE' in snowflake_destination.supported_connection_types


@pytest.mark.parametrize('builder_type', ['sdc', 'st'])
@pytest.mark.parametrize('test_case', CONFIG_TYPE_TEST_CASES)
def test_configuration_default_values(builder_type, pipeline_builder_definitions, pipeline_builder_json, test_case):
    config_definition, expected_value = test_case

    if builder_type == 'sdc':
        builder_class = SdcPipelineBuilder
    elif builder_type == 'st':
        builder_class = StPipelineBuilder

    # Assert that the default value for each model type returns the expected value when there is no default set in
    # the root level of the configuration definition.
    pipeline_builder_definitions['stages'][0]['configDefinitions'] = [config_definition.copy()]
    builder = builder_class(pipeline=pipeline_builder_json, definitions=pipeline_builder_definitions)
    stage_instance = builder.add_stage(pipeline_builder_definitions['stages'][0]['label'])
    assert stage_instance.configuration[config_definition['name']] == expected_value

    # Assert that the default value in the root level of the configuration definition will take precedence over
    # all others.
    pipeline_builder_definitions['stages'][0]['configDefinitions'][0]['defaultValue'] = "OVERRIDE"
    builder = builder_class(pipeline=pipeline_builder_json, definitions=pipeline_builder_definitions)
    stage_instance = builder.add_stage(pipeline_builder_definitions['stages'][0]['label'])
    assert stage_instance.configuration[config_definition['name']] == "OVERRIDE"


@pytest.mark.parametrize(
    'name,config_name_type,expected,err',
    [
        (
            'JSON Content',
            'label',
            [('JSON array of objects', 'ARRAY_OBJECTS'), ('Multiple JSON objects', 'MULTIPLE_OBJECTS')],
            None,
        ),
        (
            'dataFormatConfig.jsonContent',
            'full_name',
            [('JSON array of objects', 'ARRAY_OBJECTS'), ('Multiple JSON objects', 'MULTIPLE_OBJECTS')],
            None,
        ),
        (
            'jsonContent',
            'field_name',
            [('JSON array of objects', 'ARRAY_OBJECTS'), ('Multiple JSON objects', 'MULTIPLE_OBJECTS')],
            None,
        ),
        (
            'json_content',
            'sdk',
            [('JSON array of objects', 'ARRAY_OBJECTS'), ('Multiple JSON objects', 'MULTIPLE_OBJECTS')],
            None,
        ),
        (
            'On Record Error',
            'label',
            [('Discard', 'DISCARD'), ('Send to Error', 'TO_ERROR'), ('Stop Pipeline', 'STOP_PIPELINE')],
            None,
        ),
        (
            'stageOnRecordError',
            'full_name',
            [('Discard', 'DISCARD'), ('Send to Error', 'TO_ERROR'), ('Stop Pipeline', 'STOP_PIPELINE')],
            None,
        ),
        (
            'stageOnRecordError',
            'field_name',
            [('Discard', 'DISCARD'), ('Send to Error', 'TO_ERROR'), ('Stop Pipeline', 'STOP_PIPELINE')],
            None,
        ),
        (
            'on_record_error',
            'sdk',
            [('Discard', 'DISCARD'), ('Send to Error', 'TO_ERROR'), ('Stop Pipeline', 'STOP_PIPELINE')],
            None,
        ),
        ('Max Object Length (chars)', 'label', None, None),
        ('dataFormatConfig.jsonMaxObjectLen', 'full_name', None, None),
        ('jsonMaxObjectLen', 'field_name', None, None),
        ('max_object_length_in_chars', 'sdk', None, None),
        ('Number of Threads', 'label', None, None),
        ('numberOfThreads', 'full_name', None, None),
        ('numberOfThreads', 'field_name', None, None),
        ('number_of_threads', 'sdk', None, None),
        ('unknown', 'label', None, ValueError),
        ('unknown', 'full_name', None, ValueError),
        ('unknown', 'field_name', None, ValueError),
        ('unknown', 'sdk', None, ValueError),
    ],
)
def test_get_stage_configuration_options(name, config_name_type, expected, err, request):
    pipeline_builder = request.getfixturevalue('sch_sdc_pipeline_builder_with_definitions')

    exception_context = pytest.raises(err) if err else nullcontext()

    with exception_context:
        output = pipeline_builder.get_stage_configuration_options(
            config_name=name, stage_name=ANY, config_name_type=config_name_type, stage_name_type=ANY
        )

    if expected:
        assert len(output) == len(expected)
        assert output == expected
    elif err is None:
        assert output == expected
