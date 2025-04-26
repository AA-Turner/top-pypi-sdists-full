# fmt: off
import json
import warnings
from copy import deepcopy

import pytest

from streamsets.sdk.models import Configuration
from streamsets.sdk.sch_models import Connection, Pipeline, SchSdcStage

from .resources.configuration_data import DUMMY_CONNECTION_JSON, DUMMY_DESTINATION_STAGE_JSON

# fmt: on


class DummyPipelineBuilder:
    """
    A Dummy Pipeline Class Builder
    """

    def __init__(self):
        self._config_key = 'pipelineBuilder'
        self._pipeline = {self._config_key: {'stages': []}}


@pytest.fixture(scope="function")
def dummy_connection(mocker):
    connection_json = deepcopy(DUMMY_CONNECTION_JSON)
    return Connection(connection_json, mocker.Mock())


@pytest.fixture(scope="function")
def dummy_pipeline(mocker):
    pipeline_json = {'pipelineId': 1, 'commitId': None, 'name': 'Test Pipeline', 'version': 1}

    configuration = [
        {'name': 'transformerEmrConnection.retryPolicyConfig.baseDelay', 'value': 100},
        {'name': 'emrServerlessConnection.retryPolicyConfig.maxBackoff', 'value': 20000},
        {'name': 'googleCloudConfig.workerCount', 'value': 2},
    ]
    pipeline_definition_json = {'configuration': configuration}

    rules_definition_json = {}

    config_definitions = [
        {
            'label': 'Retry Base Delay',
            'fieldName': 'baseDelay',
            'name': 'transformerEmrConnection.retryPolicyConfig.baseDelay',
        },
        {
            'label': 'Max Backoff',
            'fieldName': 'maxBackoff',
            'name': 'emrServerlessConnection.retryPolicyConfig.maxBackoff',
        },
        {'label': 'Worker Count', 'fieldName': 'workerCount', 'name': 'googleCloudConfig.workerCount'},
    ]
    library_definitions_json = json.dumps({'pipeline': [{'configDefinitions': config_definitions}]})

    builder = DummyPipelineBuilder()

    pipeline = Pipeline(
        pipeline=pipeline_json,
        builder=builder,
        pipeline_definition=pipeline_definition_json,
        rules_definition=rules_definition_json,
        library_definitions=library_definitions_json,
        control_hub=mocker.Mock(),
    )
    pipeline.fragment = False

    return pipeline


@pytest.fixture(scope='function')
def dummy_destination_stage():
    stage_json = deepcopy(DUMMY_DESTINATION_STAGE_JSON)
    stage = SchSdcStage(stage=stage_json)
    return stage


def test_configuration_sanity(dummy_pipeline):
    assert isinstance(dummy_pipeline.configuration, Configuration)


def test_get_configuration_value(dummy_pipeline):
    # test against attribute.python_name, attribute['python_name'] & attribute['camelcase_name']
    assert dummy_pipeline.configuration.retry_base_delay == 100
    assert dummy_pipeline.configuration['retry_base_delay'] == 100
    assert dummy_pipeline.configuration['transformerEmrConnection.retryPolicyConfig.baseDelay'] == 100

    # make sure the first element in underlying data is what is being tested
    assert (
        dummy_pipeline._pipeline_definition['configuration'][0]['name']
        == 'transformerEmrConnection.retryPolicyConfig.baseDelay'
    )
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 100


def test_set_configuration_value_setattr_pythonic_name(dummy_pipeline):
    # make sure the first element in underlying data is transformerEmrConnection.retryPolicyConfig.baseDelay
    assert (
        dummy_pipeline._pipeline_definition['configuration'][0]['name']
        == 'transformerEmrConnection.retryPolicyConfig.baseDelay'
    )

    # test base case where the value is 100
    assert dummy_pipeline.configuration.retry_base_delay == 100
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 100

    # test against attribute.python_name and that the change is reflected in the underlying data
    dummy_pipeline.configuration.retry_base_delay = 1
    assert dummy_pipeline.configuration.retry_base_delay == 1
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 1


def test_set_configuration_value_setitem_pythonic_name(dummy_pipeline):
    # make sure the first element in underlying data is transformerEmrConnection.retryPolicyConfig.baseDelay
    assert (
        dummy_pipeline._pipeline_definition['configuration'][0]['name']
        == 'transformerEmrConnection.retryPolicyConfig.baseDelay'
    )

    # test base case where the value is 100
    assert dummy_pipeline.configuration.retry_base_delay == 100
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 100

    # test against attribute['python_name'] and that the change is reflected in the underlying data
    dummy_pipeline.configuration['retry_base_delay'] = 5
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 5


def test_set_configuration_value_setattr_camelcase_name(dummy_pipeline):
    # make sure the first element in underlying data is transformerEmrConnection.retryPolicyConfig.baseDelay
    assert (
        dummy_pipeline._pipeline_definition['configuration'][0]['name']
        == 'transformerEmrConnection.retryPolicyConfig.baseDelay'
    )

    # test base case where the value is 100
    assert dummy_pipeline.configuration.retry_base_delay == 100
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 100

    # test against attribute['camelcase_name'] and that the change is reflected in the underlying data
    dummy_pipeline.configuration['transformerEmrConnection.retryPolicyConfig.baseDelay'] = 400
    assert dummy_pipeline._pipeline_definition['configuration'][0]['value'] == 400


def test_configuration_contains(dummy_pipeline):
    # Make sure data returned from the configuration attribute is same as the underlying data
    assert dummy_pipeline.configuration.__contains__('retry_base_delay') is True
    # test the control_hub backend name as well
    assert dummy_pipeline.configuration.__contains__('transformerEmrConnection.retryPolicyConfig.baseDelay') is True
    assert dummy_pipeline.configuration.__contains__('random_value_that_does_not_exist') is False


def test_configuration_items(dummy_pipeline):
    excepted_items = {'retry_base_delay': 100, 'max_backoff': 20000, 'worker_count': 2}

    items = dummy_pipeline.configuration.items()

    assert items is not None
    assert len(items) == len(excepted_items)

    for name, value in items:
        assert name in excepted_items.keys()
        assert value == excepted_items[name]


def test_configuration_get(dummy_pipeline):
    item_python = dummy_pipeline.configuration.get('retry_base_delay')
    assert item_python == 100

    item_backend_name = dummy_pipeline.configuration.get('transformerEmrConnection.retryPolicyConfig.baseDelay')
    assert item_backend_name == 100


def test_configuration_update_pythonic_name(dummy_pipeline):
    # test with pythonic name
    dummy_pipeline.configuration.update({'retry_base_delay': 55, 'max_backoff': 90})
    assert dummy_pipeline.configuration.retry_base_delay == 55
    assert dummy_pipeline.configuration.max_backoff == 90


def test_configuration_update_camelcase_name(dummy_pipeline):
    # test with camelcase backend name
    dummy_pipeline.configuration.update(
        {
            'transformerEmrConnection.retryPolicyConfig.baseDelay': 1,
            'emrServerlessConnection.retryPolicyConfig.maxBackoff': 5,
        }
    )
    assert dummy_pipeline.configuration.retry_base_delay == 1
    assert dummy_pipeline.configuration.max_backoff == 5


@pytest.mark.parametrize(
    "test_config, expected_value",
    [
        ({'name': 'dummy_value', 'value': 'false', 'type': 'boolean'}, False),
        ({'name': 'dummy_value', 'value': '123', 'type': 'integer'}, 123),
        ({'name': 'dummy_value', 'value': 'random value as string', 'type': 'dummy_type'}, "random value as string"),
    ],
)
def test_configuration_convert_value(dummy_pipeline, test_config, expected_value):
    value = dummy_pipeline.configuration._convert_value(test_config)
    assert value == expected_value


def test_service_configuration_under_configuration_attribute(dummy_destination_stage):
    # assert that data dataFormat exists in underlying stage data
    assert dummy_destination_stage._data['services'][0]['configuration'][0]['name'] == 'dataFormat'
    assert dummy_destination_stage._data['services'][0]['configuration'][0]['value'] == 'BINARY'

    # assert dataFormat shows up in service configuration
    assert 'dataFormat' in (
        dummy_destination_stage.services[
            'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatGeneratorService'
        ]
    )

    # assert that service config shows up in stage configuration getter
    assert dummy_destination_stage.configuration['dataFormat'] == 'BINARY'

    dummy_destination_stage.configuration['dataFormat'] = 'JSON'

    # assert value has been changed
    assert (
        dummy_destination_stage.services[
            'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatGeneratorService'
        ]['dataFormat']
        == 'JSON'
    )
    assert dummy_destination_stage._data['services'][0]['configuration'][0]['value'] == 'JSON'
    assert dummy_destination_stage.configuration['dataFormat'] == 'JSON'


def test_connection_configuration_sanity(dummy_connection):
    assert dummy_connection._connection_definition_internal.configuration


def test_connection_configuration_python_name_as_attribute(dummy_connection):
    configuration = dummy_connection._connection_definition_internal.configuration
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is False
    assert configuration.use_snowflake_role is False

    dummy_connection._connection_definition_internal.configuration.use_snowflake_role = True

    # Validate
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is True
    assert configuration.use_snowflake_role is True


def test_connection_configuration_python_name_as_key(dummy_connection):
    configuration = dummy_connection._connection_definition_internal.configuration
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is False
    assert configuration['use_snowflake_role'] is False

    dummy_connection._connection_definition_internal.configuration['use_snowflake_role'] = True

    # Validate
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is True
    assert configuration['use_snowflake_role'] is True


def test_connection_configuration_camel_case_name(dummy_connection):
    configuration = dummy_connection._connection_definition_internal.configuration
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is False
    assert configuration['useSnowflakeRole'] is False

    configuration['useSnowflakeRole'] = True

    # Validate
    assert configuration._data[0][2]['name'] == 'useSnowflakeRole'
    assert configuration._data[0][2]['value'] is True
    assert configuration['useSnowflakeRole'] is True


@pytest.mark.parametrize(
    "value, flag",
    [
        ([{}], False),
        ([[{}], [{}]], True),
    ],
)
def test_configuration_list_with_empty_dictionary(value, flag):
    with pytest.raises(TypeError):
        Configuration(value)


@pytest.mark.parametrize(
    "value, flag",
    [
        ("value", False),
        (['DUMMY VALUE', 1, 1.4, False], False),
        ("value", True),
        ([['dummy', 'dummy2'], [1, 3], [1.4, 7.8], [False, True]], True),
    ],
)
def test_configuration_with_invalid_configurations(value, flag):
    with pytest.raises(TypeError):
        Configuration(value)


@pytest.mark.parametrize(
    "value",
    [
        [
            {'name': 'name1', 'value': 'value2'},
            {'name': 'name1', 'value': 'value2'},
            {'dummy_key': 'name3', 'value': 'value3'},
        ],
        [
            {'name': 'name1', 'value': 'value2'},
            {'name': 'name1', 'value': 'value2'},
            {'name': 'name1', 'dummy_value': 'value2'},
        ],
    ],
)
def test_configuration_with_incorrect_property_keys_values(value):
    with pytest.raises(TypeError):
        Configuration(value)


def test_configuration_compatibility_map():
    configuration = [{'name': 'config1', 'value': 'value1'}, {'name': 'config2', 'value': 'value1'}]
    compatibility_map = {
        'config1': {'name': 'new_config1', 'values': {'value1': 'new_value1', 'value2': 'new_value2'}},
        'config2': {'name': 'new_config2', 'values': {'value1': 'new_value1'}},
    }

    config = Configuration(
        configuration=configuration,
        property_key='name',
        property_value='value',
        compatibility_map=compatibility_map,
    )

    assert config['new_config1'] == 'new_value1'
    assert config['new_config2'] == 'new_value1'

    config['config1'] = 'value2'
    assert config['new_config1'] == 'new_value2'

    with pytest.raises(AttributeError):
        assert config['config1']
        assert config['config2']


def test_configuration_transformer_pipeline_aliases():
    configuration = [{'name': 'config1', 'value': 'value1'}, {'name': 'config2', 'value': 'value2'}]
    compatibility_map = {
        'config1': {'name': 'new_config1'},
        'config2': {'name': 'new_config2'},
    }

    config = Configuration(
        configuration=configuration,
        property_key='name',
        property_value='value',
        compatibility_map=compatibility_map,
    )

    assert config['new_config1'] == 'value1'
    assert config['new_config2'] == 'value2'

    config['config1'] = 'new_value2'
    assert config['new_config1'] == 'new_value2'

    with pytest.raises(AttributeError):
        assert config['config1']
        assert config['config2']


def test_transformer_backwards_compatibility_on_pipeline(mocker):
    # Test using values from constants.py
    pipeline_json = {
        'executorType': 'TRANSFORMER',
        'sdcVersion': '5.7.0',
        'pipelineId': 1,
        'commitId': None,
        'name': 'Test Pipeline',
        'version': 1,
    }

    configuration = [
        {'name': 'transformerEmrConnection.provisionNewCluster', 'value': True},
    ]
    pipeline_definition_json = {'configuration': configuration}

    library_definitions_json = json.dumps(
        {
            'pipeline': [
                {
                    'configDefinitions': [
                        {
                            'label': 'EMR Cluster',
                            'fieldName': 'emrClusterOption',
                            'name': 'transformerEmrConnection.emrClusterOption',
                        },
                    ]
                }
            ]
        }
    )

    builder = DummyPipelineBuilder()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        pipeline = Pipeline(
            pipeline=pipeline_json,
            builder=builder,
            pipeline_definition=pipeline_definition_json,
            rules_definition={},
            library_definitions=library_definitions_json,
            control_hub=mocker.Mock(),
        )
        pipeline.fragment = False

        assert pipeline.configuration['transformerEmrConnection.emrClusterOption'] == 'PROVISION_CLUSTER'
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)

        pipeline.configuration['transformerEmrConnection.provisionNewCluster'] = False
        assert len(w) == 2
        assert issubclass(w[-1].category, DeprecationWarning)
        assert pipeline.configuration['transformerEmrConnection.emrClusterOption'] == 'EXISTING_CLUSTER'
