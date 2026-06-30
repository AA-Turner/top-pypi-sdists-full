#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

import copy

# fmt: off
import json
from contextlib import nullcontext

import pytest
from tests.mocks.mock_api import MockResponse

from streamsets.sdk.constants import COLLECTOR, SNOWPARK, STATUS_ERRORS, EngineType
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


class MockEngine:
    def __init__(self, version):
        self.version = version


class MockEngines:
    def __init__(self):
        self._engines_data = {'abcd1234': {"version": "6.1.1"}, 'wxyz0987': {"version": "5.6.1"}}

    def get(self, id):
        version = self._engines_data.get(id)["version"]
        return MockEngine(version)


class MockControlHub:
    def __init__(self):
        self.api_client = MockApiClient()

    @property
    def engines(self):
        return MockEngines()


class MockApiClient:
    def get_pipelines_definitions(self, val):
        return Command(self, MockResponse({"foo": "bar"}, 200))

    def get_pipeline_commit(self, commit_id):
        mock_data = {
            'libraryDefinitions': json.dumps({'schemaVersion': 1}),
            'pipelineDefinition': json.dumps({'title': 'dummy_value'}),
            'currentRules': {
                'rulesDefinition': json.dumps(
                    {'metricsRuleDefinitions': [], 'driftRuleDefinitions': [], 'dataRuleDefinitions': []}
                )
            },
        }
        return Command(self, MockResponse(mock_data, 200))


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
    rules_definition_json = {'metricsRuleDefinitions': [], 'driftRuleDefinitions': [], 'dataRuleDefinitions': []}
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


@pytest.fixture(scope="function")
def dummy_collector_pipeline(dummy_pipeline):
    dummy_pipeline._data['executorType'] = "COLLECTOR"
    return dummy_pipeline


def test_library_definitions_in_data_str_sanity(dummy_pipeline):
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)


def test_library_definitions_in_data_str_after_calling_property_sanity(dummy_pipeline):
    assert isinstance(dummy_pipeline._library_definitions, dict)
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)  # Check data didn't change


@pytest.mark.parametrize(
    "engine_type",
    [engine_type for engine_type in EngineType],
)
def test_engine_types(dummy_pipeline, engine_type):
    dummy_pipeline._data['executorType'] = engine_type.value
    assert dummy_pipeline._data['executorType'] == engine_type.value
    assert dummy_pipeline.engine_type == engine_type
    dummy_pipeline.engine_type = engine_type
    assert dummy_pipeline._data['executorType'] == engine_type.value
    assert dummy_pipeline.engine_type == engine_type
    assert isinstance(dummy_pipeline.engine_type, EngineType)


def test_library_definitions_lazy_loading_data_collector(dummy_pipeline, mocker):
    def get_defs_dict():
        return {"COLLECTOR": "bar"}

    def get_defs_str(val):
        return '{"COLLECTOR": "bar"}'

    mocker.patch('json.dumps', side_effect=get_defs_str)

    # Use mocker.Mock() here so that _control_hub.engines.get(id=self.engine_id) in sch_models passes, MockControlHub does
    # not have an engines attribute as of writing this test.
    dummy_pipeline._control_hub = mocker.Mock()

    dummy_pipeline._data['executorType'] = COLLECTOR.value
    dummy_pipeline.engine_id = "bar"
    dummy_pipeline._data['libraryDefinitions'] = None  # We want to trigger lazy loading in the next call

    # Lazy loading will be triggered, and we mock the json.dumps to return a string
    # We expect the property to return dict, but the underlying data to return str
    assert isinstance(dummy_pipeline._library_definitions, dict)
    assert isinstance(dummy_pipeline._data['libraryDefinitions'], str)
    assert dummy_pipeline._library_definitions == get_defs_dict()
    assert dummy_pipeline._data['libraryDefinitions'] == get_defs_str(None)


def test_library_definitions_lazy_loading_snowflake(dummy_pipeline):
    dummy_pipeline._data['executorType'] = SNOWPARK.value
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
    assert dummy_pipeline.sdc_version == '6.1.1'


@pytest.mark.parametrize(
    'engine_type, exception',
    [
        ('COLLECTOR', nullcontext()),
        ('TRANSFORMER', pytest.raises(TypeError)),
        ('SNOWPARK', pytest.raises(TypeError)),
        ('EDGE', pytest.raises(TypeError)),
        (None, pytest.raises(TypeError)),
    ],
)
def test_pipeline_add_rules_works_only_for_collector(engine_type, exception, dummy_pipeline):
    dummy_pipeline._data['executorType'] = engine_type

    with exception:
        dummy_pipeline.add_data_rule(stream="Dev Raw Data Source 1 output Stream 1", label="data_rule_label")

    with exception:
        dummy_pipeline.add_datadrift_rule(stream="Dev Raw Data Source 1 output Stream 1", label="drift_rule_label")

    with exception:
        dummy_pipeline.add_metric_rule(alert_text="dummy metric rule")


@pytest.mark.parametrize(
    'rule_args, rule_kwargs, exception',
    [
        (["Dev Raw Data Source 1 output Stream 1", "data_rule_label"], {}, nullcontext()),
        (["Dev Raw Data Source 1 output Stream 1"], {"label": "data_rule_label"}, nullcontext()),
        ([], {"stream": "Dev Raw Data Source 1 output Stream 1", "label": "data_rule_label"}, nullcontext()),
    ],
)
def test_pipeline_add_data_rule(rule_args, rule_kwargs, exception, dummy_collector_pipeline):
    with exception:
        dummy_collector_pipeline.add_data_rule(*rule_args, **rule_kwargs)

        assert 1 == len(dummy_collector_pipeline._rules_definition['dataRuleDefinitions'])
        assert (
            "Dev Raw Data Source 1 output Stream 1"
            == dummy_collector_pipeline._rules_definition['dataRuleDefinitions'][0]["lane"]
        )
        assert "data_rule_label" == dummy_collector_pipeline._rules_definition['dataRuleDefinitions'][0]["label"]


@pytest.mark.parametrize(
    'rule_args, rule_kwargs, exception',
    [
        (["Dev Raw Data Source 1 output Stream 1", "drift_rule_label"], {}, nullcontext()),
        (["Dev Raw Data Source 1 output Stream 1"], {"label": "drift_rule_label"}, nullcontext()),
        ([], {"stream": "Dev Raw Data Source 1 output Stream 1", "label": "drift_rule_label"}, nullcontext()),
    ],
)
def test_pipeline_add_datadrift_rule(rule_args, rule_kwargs, exception, dummy_collector_pipeline):
    with exception:
        dummy_collector_pipeline.add_datadrift_rule(*rule_args, **rule_kwargs)

        assert 1 == len(dummy_collector_pipeline._rules_definition['driftRuleDefinitions'])
        assert (
            "Dev Raw Data Source 1 output Stream 1"
            == dummy_collector_pipeline._rules_definition['driftRuleDefinitions'][0]["lane"]
        )
        assert "drift_rule_label" == dummy_collector_pipeline._rules_definition['driftRuleDefinitions'][0]["label"]


@pytest.mark.parametrize(
    'rule_args, rule_kwargs, exception',
    [
        (["dummy metric rule"], {}, nullcontext()),
        ([], {"alert_text": "dummy metric rule"}, nullcontext()),
    ],
)
def test_pipeline_add_metric_rule(rule_args, rule_kwargs, exception, dummy_collector_pipeline):
    with exception:
        dummy_collector_pipeline.add_metric_rule(*rule_args, **rule_kwargs)

        assert 1 == len(dummy_collector_pipeline._rules_definition['metricsRuleDefinitions'])
        assert (
            "dummy metric rule" == dummy_collector_pipeline._rules_definition['metricsRuleDefinitions'][0]["alertText"]
        )


def test_pipeline_shallow_copy__library_definitions_not_called(dummy_pipeline):
    pipeline_copy = copy.copy(dummy_pipeline)

    assert id(pipeline_copy._pipeline_definition_internal) == id(dummy_pipeline._pipeline_definition_internal)
    assert id(pipeline_copy._rules_definition) == id(dummy_pipeline._rules_definition)
    assert id(pipeline_copy._library_definitions_internal) == id(dummy_pipeline._library_definitions_internal)
    # library_definitions wasn't called before so each access will return different value
    assert id(pipeline_copy.library_definitions) != id(dummy_pipeline.library_definitions)
    # _library_definitions returns differnet objects on each access
    assert id(pipeline_copy._library_definitions) != id(dummy_pipeline._library_definitions)

    # after direct change it is no longer same value
    pipeline_copy.library_definitions = {"dummy": "dummy"}
    assert id(pipeline_copy._library_definitions_internal) != id(dummy_pipeline._library_definitions_internal)
    assert id(pipeline_copy.library_definitions) != id(dummy_pipeline.library_definitions)


def test_pipeline_shallow_copy__library_definitions_called(dummy_pipeline):
    dummy_pipeline.library_definitions
    pipeline_copy = copy.copy(dummy_pipeline)

    assert id(pipeline_copy._pipeline_definition_internal) == id(dummy_pipeline._pipeline_definition_internal)
    assert id(pipeline_copy._rules_definition) == id(dummy_pipeline._rules_definition)
    assert id(pipeline_copy._library_definitions_internal) == id(dummy_pipeline._library_definitions_internal)
    # library_definitions was called before so it should be the same object
    assert id(pipeline_copy.library_definitions) == id(dummy_pipeline.library_definitions)
    # _library_definitions returns differnet objects on each access
    assert id(pipeline_copy._library_definitions) != id(dummy_pipeline._library_definitions)

    # after direct change it is no longer same value
    pipeline_copy.library_definitions = {"dummy": "dummy"}
    assert id(pipeline_copy._library_definitions_internal) != id(dummy_pipeline._library_definitions_internal)
    assert id(pipeline_copy.library_definitions) != id(dummy_pipeline.library_definitions)


def test_no_recursion_error_when_accessing_name_with_null_library_definitions(dummy_pipeline, monkeypatch):
    """
    Test that accessing the name property of a Pipeline object with null libraryDefinitions
    does NOT cause a RecursionError.

    This test verifies the fix for the recursion issue that occurred when:
    1. Pipeline has commit_id set
    2. _data_internal['libraryDefinitions'] is None
    3. Accessing the name property triggers _data property
    4. _data property calls _load_data()
    5. _load_data() accesses library_definitions property
    6. library_definitions accesses _library_definitions property
    7. _library_definitions should NOT call _load_data() again (preventing infinite loop)

    The test ensures that the name can be accessed without recursion.
    """
    from unittest.mock import Mock

    # Set up commit_id to trigger the potential recursion path
    dummy_pipeline._data_internal['commitId'] = 'test-commit-id'

    # Set up the internal state that previously triggered the recursion
    # The key is setting libraryDefinitions to None and _pipeline_definition_internal to None
    dummy_pipeline._data_internal['libraryDefinitions'] = None
    dummy_pipeline._pipeline_definition_internal = None
    dummy_pipeline._library_definitions_internal = None

    # Add the engine ID to MockEngines so it can be found
    dummy_pipeline._control_hub.engines._engines_data[dummy_pipeline.engine_id] = {"version": "6.1.1"}

    # Mock the API response for get_pipeline_commit to return None for libraryDefinitions
    # This reproduces the actual bug scenario
    mock_response = Mock()
    mock_response.json.return_value = {
        'libraryDefinitions': None,  # Return None to trigger the recursion bug
        'pipelineDefinition': '{}',
        'currentRules': {'rulesDefinition': '{}'},
    }
    mock_command = Mock(response=mock_response)
    monkeypatch.setattr(dummy_pipeline._control_hub.api_client, 'get_pipeline_commit', lambda commit_id: mock_command)

    # Accessing the name property should NOT trigger RecursionError
    name = dummy_pipeline.name
    assert name == 'Test Pipeline'


def test_no_recursion_error_during_fragment_filtering(dummy_pipeline, monkeypatch):
    """
    Test that filtering fragments by name does NOT cause a RecursionError.

    This test verifies the fix for the recursion issue that occurred when:
    sch.pipelines.get(fragment=True, name=fragment_name)
    triggered recursion when filtering by name attribute.

    The test ensures that fragments can be filtered by name without recursion.
    """
    from unittest.mock import Mock

    from streamsets.sdk.utils import SeekableList

    # Set up commit_id to trigger the potential recursion path
    dummy_pipeline._data_internal['commitId'] = 'test-commit-id'

    # Set up the state that previously caused recursion
    dummy_pipeline._data_internal['libraryDefinitions'] = None
    dummy_pipeline._pipeline_definition_internal = None
    dummy_pipeline._library_definitions_internal = None

    # Add the engine ID to MockEngines so it can be found
    dummy_pipeline._control_hub.engines._engines_data[dummy_pipeline.engine_id] = {"version": "6.1.1"}

    # Mock API response to return None for libraryDefinitions
    # This reproduces the actual bug scenario
    mock_response = Mock()
    mock_response.json.return_value = {
        'libraryDefinitions': None,  # Return None to trigger the recursion bug
        'pipelineDefinition': '{}',
        'currentRules': {'rulesDefinition': '{}'},
    }
    mock_command = Mock(response=mock_response)
    monkeypatch.setattr(dummy_pipeline._control_hub.api_client, 'get_pipeline_commit', lambda commit_id: mock_command)

    # Create a SeekableList with the fragment
    fragments = SeekableList([dummy_pipeline])

    # Filtering by name should NOT trigger recursion
    # This mimics: fragments.get_all(name='Test Pipeline')
    result = SeekableList(i for i in fragments if all(getattr(i, k) == v for k, v in {'name': 'Test Pipeline'}.items()))
    # Force evaluation of the generator - should succeed without RecursionError
    result_list = list(result)
    assert len(result_list) == 1
    assert result_list[0].name == 'Test Pipeline'
