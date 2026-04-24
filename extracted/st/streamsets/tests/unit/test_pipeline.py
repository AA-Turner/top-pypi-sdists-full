#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

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
