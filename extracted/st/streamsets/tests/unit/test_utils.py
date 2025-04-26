# Copyright 2023 StreamSets Inc.

# fmt: off
import logging
import random
import string
from copy import deepcopy

import pytest

from streamsets.sdk.constants import SDC_DEPLOYMENT_TYPE, TRANSFORMER_DEPLOYMENT_TYPE
from streamsets.sdk.exceptions import InvalidVersionError
from streamsets.sdk.sdc_models import PipelineBuilder as SdcPipelineBuilder
from streamsets.sdk.st_models import PipelineBuilder as StPipelineBuilder
from streamsets.sdk.utils import (
    get_attribute, get_color_icon_from_stage_definition, get_decoded_jwt, get_random_string,
    get_stage_library_display_name_from_library, get_stage_library_name_from_display_name, reversed_dict,
    validate_pipeline_stages,
)

from .resources.utils_data import (
    TEST_VALIDATE_PIPELINE_STAGES_FAILS_FOR_INVALID_PIPELINE_WITH_INVALID_STAGES_JSON,
    TEST_VALIDATE_PIPELINE_STAGES_PASSES_FOR_VALID_PIPELINE_WITH_VALID_STAGES_JSON,
)

# fmt: on


class DummyPipeline:
    """
    A Dummy Pipeline Class
    """

    def __init__(self):
        self._config_key = 'pipelineBuilder'
        self._pipeline = {self._config_key: {'stages': []}}
        self.stages = []

    def _get_builder(self):
        return DummyPipelineBuilder()


class DummyPipelineBuilder:
    """
    A Dummy Pipeline Class Builder
    """

    def __init__(self):
        self._config_key = 'pipelineBuilder'
        self._pipeline = {self._config_key: {'stages': []}}
        self._definitions = {
            'stages': [
                {
                    'services': [],
                    'description': 'Generates error records and silently discards records as specified.',
                    'label': 'Dev Random Error',
                    'name': 'com_streamsets_pipeline_stage_devtest_RandomErrorProcessor',
                    'type': 'PROCESSOR',
                    'className': 'com.streamsets.pipeline.stage.devtest.RandomErrorProcessor',
                    'version': '2',
                    'eventDefs': [],
                    'library': 'streamsets-datacollector-dev-lib',
                },
            ]
        }

    def _update_stages_definition(self):
        return


class DummyStage:
    """
    A Dummy Pipeline Class
    """

    def __init__(self):
        self._data = None
        self.instance_name = 'dummy stage'


@pytest.fixture(scope="function")
def dummy_pipeline():
    return DummyPipeline()


@pytest.fixture(
    params=[
        {
            "label": "Max Backoff",
            "name": "emrServerlessConnection.retryPolicyConfig.maxBackoff",
            "expected_output": ("max_backoff", "emrServerlessConnection.retryPolicyConfig.maxBackoff"),
        },
        {
            "label": "Cluster Name",
            "name": "sdcEmrConnection.clusterName",
            "expected_output": ("cluster_name", "sdcEmrConnection.clusterName"),
        },
        {
            "label": "Set Session Tags",
            "name": "emrServerlessConnection.awsConfig.setSessionTags",
            "expected_output": ("set_session_tags", "emrServerlessConnection.awsConfig.setSessionTags"),
        },
        {
            "label": "Session Timeout (secs)",
            "name": "emrServerlessConnection.awsConfig.sessionDuration",
            "expected_output": ("session_timeout_in_secs", "emrServerlessConnection.awsConfig.sessionDuration"),
        },
    ]
)
def config_definition(request):
    return request.param


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(42)  # Set a fixed seed for predictable random values


def test_get_random_string_default_length():
    result = get_random_string()
    assert len(result) == 8
    assert all(char in string.ascii_letters for char in result)


def test_get_random_string_custom_length():
    length = 12
    result = get_random_string(length=length)
    assert len(result) == length
    assert all(char in string.ascii_letters for char in result)


def test_get_random_string_custom_characters():
    characters = "abc123"
    result = get_random_string(characters=characters)
    assert len(result) == 8
    assert all(char in characters for char in result)


def test_get_decoded_jwt_token():
    token = (
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZ'
        'SI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.YW55IGNhcm5hbCBwbGVhc3VyZS4='
    )
    expected_payload = {'sub': '1234567890', 'name': 'John Doe', 'iat': 1516239022}
    assert get_decoded_jwt(token) == expected_payload


def test_get_decoded_jwt_invalid_token_type():
    invalid_token = 4
    with pytest.raises(TypeError):
        get_decoded_jwt(invalid_token)


def test_get_decoded_jwt_invalid_token():
    invalid_token = 'invalid_token'
    with pytest.raises(ValueError):
        get_decoded_jwt(invalid_token)


def test_get_decoded_jwt_invalid_malformed_token():
    malformed_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid_token'
    with pytest.raises(ValueError):
        get_decoded_jwt(malformed_token)


def test_reversed_dict(caplog):
    forward_dict = {'a': 1, 'b': 2, 'c': 3}
    expected_result = {1: 'a', 2: 'b', 3: 'c'}

    with caplog.at_level(logging.WARNING):
        result = reversed_dict(forward_dict)

    assert result == expected_result
    assert len(caplog.records) == 0


def test_reversed_dict_invalid_duplicate_value(caplog):
    forward_dict = {'a': 1, 'b': 2, 'c': 1}
    expected_result = {1: 'c', 2: 'b'}

    with caplog.at_level(logging.WARNING):
        result = reversed_dict(forward_dict)

    assert result == expected_result
    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "WARNING"
    assert "The dictionary provided, is not one-one mapping." in caplog.text


@pytest.mark.parametrize(
    'stage_definition, expected_output',
    [
        ({'label': 'Trash', 'type': 'TARGET'}, 'Destination_Trash.png'),
        ({'label': 'Delay', 'type': 'PROCESSOR'}, 'Processor_Delay.png'),
        ({'label': 'Dev Data Generator', 'type': 'SOURCE'}, 'Origin_Dev_Data_Generator.png'),
        ({'label': 'SFTP/FTP/FTPS Client', 'type': 'TARGET'}, 'Destination_SFTP_FTP_FTPS_Client.png'),
    ],
)
@pytest.mark.parametrize('stage_types', [SdcPipelineBuilder.STAGE_TYPES, StPipelineBuilder.STAGE_TYPES])
def test_get_color(stage_definition, expected_output, stage_types):
    result = get_color_icon_from_stage_definition(stage_definition, stage_types)
    assert result == expected_output


@pytest.mark.parametrize('stage_definition, stage_types', [({'type': ''}, {}), ({'type': ':)'}, {'key': ':('})])
def test_get_color_icon_returns_empty_when_error_out(stage_definition, stage_types):
    result = get_color_icon_from_stage_definition(stage_definition, stage_types)
    assert result == ''


def test_get_attribute(config_definition):
    expected_attribute_name, expected_config_name = config_definition["expected_output"]
    attribute_name, config_name = get_attribute(config_definition)

    assert attribute_name == expected_attribute_name
    assert config_name == expected_config_name


@pytest.mark.parametrize(
    "library_name, deployment_type, result",
    [
        (
            "streamsets-spark-snowflake-with-no-dependency-lib:4.1.0",
            TRANSFORMER_DEPLOYMENT_TYPE,
            "snowflake-with-no-dependency",
        ),
        ("streamsets-datacollector-amazing-lib:4.2.2", SDC_DEPLOYMENT_TYPE, "amazing"),
        ("streamsets-transformer-noooooo-lib:0.0.1", TRANSFORMER_DEPLOYMENT_TYPE, "noooooo"),
    ],
)
def test_get_stage_library_display_name_from_library(library_name, deployment_type, result):
    output = get_stage_library_display_name_from_library(
        stage_library_name=library_name, deployment_type=deployment_type
    )
    assert output == result


@pytest.mark.parametrize("invalid_library_name", [None, 3])
def test_get_stage_library_display_name_from_library_raises_type_error_with_invalid_library_name(invalid_library_name):
    with pytest.raises(TypeError):
        get_stage_library_display_name_from_library(
            stage_library_name=invalid_library_name, deployment_type=SDC_DEPLOYMENT_TYPE
        )


@pytest.mark.parametrize("invalid_deployment_type", [None, 3])
def test_get_stage_library_display_name_from_library_raises_type_error_with_invalid_deployment_type(
    invalid_deployment_type,
):
    with pytest.raises(TypeError):
        get_stage_library_display_name_from_library(
            stage_library_name='streamsets-datacollector-aws-lib:3.2.0', deployment_type=invalid_deployment_type
        )


def test_get_stage_library_display_name_from_library_raises_value_error_with_invalid_deployment_type():
    with pytest.raises(ValueError):
        get_stage_library_display_name_from_library(
            stage_library_name='streamsets-datacollector-aws-lib:3.2.0', deployment_type='Obama'
        )


@pytest.mark.parametrize(
    "library_name, deployment_type",
    [
        ("streamsets-datacollector-snowflake-with-no-dependency-lib:4.1.0", TRANSFORMER_DEPLOYMENT_TYPE),
        ("this isn't valid", TRANSFORMER_DEPLOYMENT_TYPE),
    ],
)
def test_get_stage_library_display_name_from_library_raises_value_error_with_invalid_library_name(
    library_name, deployment_type
):
    # value error can be raised either because the library name does not match regex string, or because an incorrect
    # combination of library name and deployment type was passed. We check for both conditions
    with pytest.raises(ValueError):
        get_stage_library_display_name_from_library(stage_library_name=library_name, deployment_type=deployment_type)


@pytest.mark.parametrize(
    "display_name, deployment_type, deployment_engine_version, result",
    [
        ('test:1.1.1', SDC_DEPLOYMENT_TYPE, '5.7.2', 'streamsets-datacollector-test-lib:1.1.1'),
        ('test', SDC_DEPLOYMENT_TYPE, '5.7.2', 'streamsets-datacollector-test-lib:5.7.2'),
        ('credentialstore', TRANSFORMER_DEPLOYMENT_TYPE, '3.0.0', 'streamsets-transformer-credentialstore-lib:3.0.0'),
        ('random', TRANSFORMER_DEPLOYMENT_TYPE, '1.2.3', 'streamsets-spark-random-lib:1.2.3'),
    ],
)
def test_get_stage_library_name_from_display_name(display_name, deployment_type, deployment_engine_version, result):
    output = get_stage_library_name_from_display_name(
        stage_library_display_name=display_name,
        deployment_type=deployment_type,
        deployment_engine_version=deployment_engine_version,
    )
    assert output == result


@pytest.mark.parametrize("invalid_library_name", [None, 3])
def test_get_stage_library_name_from_display_name_raises_type_error_with_invalid_library_name(invalid_library_name):
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(
            stage_library_display_name=invalid_library_name,
            deployment_type=SDC_DEPLOYMENT_TYPE,
        )


@pytest.mark.parametrize("invalid_deployment_type", [None, 3])
def test_get_stage_library_name_from_display_name_raises_type_error_with_invalid_deployment_type(
    invalid_deployment_type,
):
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(
            stage_library_display_name='aws', deployment_type=invalid_deployment_type
        )


def test_get_stage_library_name_from_display_name_raises_value_error_with_invalid_deployment_type():
    with pytest.raises(ValueError):
        get_stage_library_name_from_display_name(stage_library_display_name='aws', deployment_type='Obama')


def test_get_stage_library_name_from_display_name_raises_type_error_when_no_version_is_passed():
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(stage_library_display_name='aws', deployment_type=SDC_DEPLOYMENT_TYPE)


@pytest.mark.parametrize(
    "library_name, deployment_type, deployment_engine_version",
    [('aws:not-a-version', SDC_DEPLOYMENT_TYPE, None), ('aws', SDC_DEPLOYMENT_TYPE, 'again, not a version')],
)
def test_get_stage_library_name_from_display_name_raises_invalid_version_error(
    library_name, deployment_type, deployment_engine_version
):
    with pytest.raises(InvalidVersionError):
        get_stage_library_name_from_display_name(
            stage_library_display_name=library_name,
            deployment_type=deployment_type,
            deployment_engine_version=deployment_engine_version,
        )


def test_validate_pipeline_stages_passes_for_valid_pipeline_with_valid_stages(dummy_pipeline):
    stage = DummyStage()
    stage._data = deepcopy(TEST_VALIDATE_PIPELINE_STAGES_PASSES_FOR_VALID_PIPELINE_WITH_VALID_STAGES_JSON)
    dummy_pipeline.stages = [stage]
    validate_pipeline_stages(dummy_pipeline)


def test_validate_pipeline_stages_fails_for_invalid_pipeline_with_invalid_stages(dummy_pipeline):
    stage = DummyStage()
    stage._data = deepcopy(TEST_VALIDATE_PIPELINE_STAGES_FAILS_FOR_INVALID_PIPELINE_WITH_INVALID_STAGES_JSON)
    dummy_pipeline.stages = [stage]
    with pytest.raises(ValueError):
        validate_pipeline_stages(dummy_pipeline)
