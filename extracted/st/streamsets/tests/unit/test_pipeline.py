# fmt: off
import json
import warnings

import pytest
from tests.mocks.mock_api import MockResponse

from streamsets.sdk.constants import SNOWFLAKE_EXECUTOR_TYPE, STATUS_ERRORS
from streamsets.sdk.exceptions import InvalidError
from streamsets.sdk.sch_api import Command
from streamsets.sdk.sch_models import Pipeline
from streamsets.sdk.utils import get_random_string

# fmt: on


class DummyPipelineBuilder:
    """
    A Dummy Pipeline Class Builder
    """

    def __init__(self):
        self._config_key = 'pipelineBuilder'
        self._pipeline = {self._config_key: {'stages': []}}


class MockControlHub:
    def __init__(self):
        self.api_client = MockApiClient()


class MockApiClient:
    def get_pipelines_definitions(self, val):
        return Command(self, MockResponse({"foo": "bar"}, 200))


@pytest.fixture(scope="function")
def dummy_pipeline():
    pipeline_json = {
        'pipelineId': 1,
        'commitId': None,
        'name': 'Test Pipeline',
        'version': 1,
        'sdcId': 'a738b839-bac3-4118-b0f4-eb6509f0b7cf',
    }
    pipeline_definition_json = json.dumps({'title': 'dummy_value'})
    rules_definition_json = {}
    library_definitions_json = json.dumps({'schemaVersion': 1})
    builder = DummyPipelineBuilder()

    return Pipeline(
        pipeline=pipeline_json,
        builder=builder,
        pipeline_definition=pipeline_definition_json,
        rules_definition=rules_definition_json,
        library_definitions=library_definitions_json,
        control_hub=MockControlHub(),
    )


def test_library_definitions_in_data_str_sanity(dummy_pipeline):
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)


def test_library_definitions_in_data_str_after_calling_property_sanity(dummy_pipeline):
    assert isinstance(dummy_pipeline._library_definitions, dict)
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)  # Check data didn't change


def test_library_definitions_lazy_loading_data_collector(dummy_pipeline, mocker):
    def get_defs_dict():
        return {"foo": "bar"}

    def get_defs_str(val):
        return '{"foo": "bar"}'

    mocker.patch('json.dumps', side_effect=get_defs_str)

    # Use mocker.Mock() here so that _control_hub.engines.get(id=self.sdc_id) in sch_models passes, MockControlHub does
    # not have an engines attribute as of writing this test.
    dummy_pipeline._control_hub = mocker.Mock()

    dummy_pipeline.executor_type = "foo"
    dummy_pipeline.sdc_id = "bar"
    dummy_pipeline._data['libraryDefinitions'] = None  # We want to trigger lazy loading in the next call

    # Lazy loading will be triggered, and we mock the json.dumps to return a string
    # We expect the property to return dict, but the underlying data to return str
    assert isinstance(dummy_pipeline._library_definitions, dict)
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)
    assert dummy_pipeline._library_definitions == get_defs_dict()
    assert dummy_pipeline._data['libraryDefinitions'] == get_defs_str(None)


def test_library_definitions_lazy_loading_snowflake(dummy_pipeline):
    dummy_pipeline.executor_type = SNOWFLAKE_EXECUTOR_TYPE
    dummy_pipeline._data['libraryDefinitions'] = None  # We want to trigger lazy loading in the next call

    # Lazy loading will be triggered, and we mock the json.dumps to return a string
    # We expect the property to return dict, but the underlying data to return str
    assert isinstance(dummy_pipeline._library_definitions, dict)
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)


def test_pipeline_get_stages():
    supported_connection_type = 'FOO_BAR_CONNECTION_TYPE'
    stage = {
        'instanceName': 'foo',
        'stageName': 'com_streamsets_foo_stage',
        'stageVersion': '1',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'uiInfo': {
            'stageType': 'SOURCE',
        },
    }
    stage_definitions = {
        'instanceName': 'foo',
        'name': 'com_streamsets_foo_stage',
        'fieldName': 'connectionSelection',
        'stageVersion': '1',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'configDefinitions': [
            {
                'fieldName': 'connectionSelection',
                'connectionType': supported_connection_type,
                'name': 'conf.connectionSelection',
            }
        ],
        'connectionType': 'STREAMSETS_FOO_CLIENT',
    }
    pipeline = {'pipelineId': 1, 'executorType': 'COLLECLTOR', 'name': 'foo_pipeline', 'version': 1}
    pipeline_definition = {'title': 'foo_pipeline', 'stages': [stage]}
    library_definitions = {'schemaVersion': 1, 'stages': [stage_definitions]}
    rules_definition = {}

    p = Pipeline(
        pipeline=pipeline,
        builder=None,
        pipeline_definition=pipeline_definition,
        rules_definition=rules_definition,
        library_definitions=library_definitions,
        control_hub=MockControlHub(),
    )

    stages = p.stages
    assert len(stages) == 1  # We expect one stage - see definitions above
    assert stages[0].supported_connection_types == [supported_connection_type]


def test_property_stages_not_exist_in_pipeline_definition():
    supported_connection_type = 'FOO_BAR_CONNECTION_TYPE'
    stage = {
        'instanceName': 'foo',
        'stageName': 'com_streamsets_foo_stage',
        'stageVersion': '1',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'uiInfo': {
            'stageType': 'SOURCE',
        },
    }
    stage_definitions = {
        'instanceName': 'foo',
        'name': 'com_streamsets_foo_stage',
        'fieldName': 'connectionSelection',
        'stageVersion': '1',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'configDefinitions': [
            {
                'fieldName': 'connectionSelection',
                'connectionType': supported_connection_type,
                'name': 'conf.connectionSelection',
            }
        ],
        'connectionType': 'STREAMSETS_FOO_CLIENT',
    }
    pipeline = {'pipelineId': 1, 'executorType': 'COLLECTOR', 'name': 'foo_pipeline', 'version': 1}
    pipeline_definition = {'title': 'foo_pipeline', 'stages': [stage]}
    library_definitions = {'schemaVersion': 1, 'stages': [stage_definitions]}
    rules_definition = {}

    p = Pipeline(
        pipeline=pipeline,
        builder=None,
        pipeline_definition=pipeline_definition,
        rules_definition=rules_definition,
        library_definitions=library_definitions,
        control_hub=MockControlHub(),
    )

    assert not p.error_stage
    assert not p.stats_aggregator_stage


def test_invalid_status_pipeline():
    def run_pipeline_preview():
        invalid_pipeline_preview_response = {
            'previewerId': '45e1ff73-8bd1-41be-995d-668147f1e1e2',
            'status': 'INVALID',
            'pipelineId': get_random_string,
            'attributes': {},
        }

        response = MockResponse(invalid_pipeline_preview_response, 200)
        current_status = response.json()['status']
        if current_status in STATUS_ERRORS:
            raise STATUS_ERRORS.get(current_status)(response.json())

    with pytest.raises(InvalidError) as e:
        run_pipeline_preview()

    assert e.type is InvalidError


def test_pipeline_engine_id(dummy_pipeline):
    fake_engine_id = 'abcd1234'
    assert dummy_pipeline.engine_id
    dummy_pipeline.engine_id = fake_engine_id
    assert dummy_pipeline._data['sdcId'] == fake_engine_id


def test_pipeline_sdc_id(dummy_pipeline):
    fake_engine_id = 'wxyz0987'
    assert dummy_pipeline.sdc_id
    dummy_pipeline.sdc_id = fake_engine_id
    assert dummy_pipeline._data['sdcId'] == fake_engine_id


def test_pipeline_sdc_id_is_deprecated(dummy_pipeline):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        assert dummy_pipeline.sdc_id
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
