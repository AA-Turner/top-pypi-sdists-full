#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import logging
import random
import string
from contextlib import nullcontext
from copy import deepcopy

import pytest
from requests.exceptions import HTTPError

from streamsets.sdk.exceptions import InvalidVersionError, ValidationError
from streamsets.sdk.sch import Job
from streamsets.sdk.sdc_models import PipelineBuilder as SdcPipelineBuilder
from streamsets.sdk.st_models import PipelineBuilder as StPipelineBuilder
from streamsets.sdk.utils import (
    EngineType, get_accepted_labels_libraries_and_names, get_attribute, get_color_icon_from_stage_definition,
    get_decoded_jwt, get_random_string, get_stage_library_display_name_from_library,
    get_stage_library_name_from_display_name, join_url_parts, reversed_dict, validate_job, validate_pipeline_stages,
)

from .resources.utils_data import (
    DUMMY_VALID_JOB_CONFIGURATION, TEST_VALIDATE_PIPELINE_STAGES_FAILS_FOR_INVALID_PIPELINE_WITH_INVALID_STAGES_JSON,
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
            ],
            'pipeline': [
                {
                    'configDefinitions': [
                        {
                            'max': 9223372036854775807,
                            'fieldName': 'startEventStage',
                            'label': 'Start Event',
                            'description': 'Stage that should handle pipeline start event.',
                            'name': 'startEventStage',
                            'type': 'MODEL',
                            'model': {
                                'labels': [
                                    'Amazon S3 (Library: Amazon Web Services 1.11.999)',
                                    'Databricks Job Launcher (Library: Basic)',
                                    'Discard (Library: Basic)',
                                    'Email (Library: Basic)',
                                    'JDBC Query (Library: JDBC)',
                                    'Shell (Library: Basic)',
                                    'Snowflake (Library: Snowflake Enterprise Library)',
                                    'Write to Another Pipeline (Library: Basic)',
                                ],
                                'values': [
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor::3',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_databricks_DatabricksJobLauncherDExecutor::2',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_devnull_ToErrorNullDTarget::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_emailexecutor_EmailDExecutor::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_executor_jdbc_JdbcQueryDExecutor::5',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_shell_ShellDExecutor::1',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_stage_executor_snowflake_SnowflakeDExecutor::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_sdcipc_ToErrorSdcIpcDTarget::3',
                                ],
                                'configDefinitions': None,
                                'modelType': 'VALUE_CHOOSER',
                                'valuesProviderClass': 'com.streamsets.datacollector.config.PipelineLifecycleStageChooserValues',
                                'filteringConfig': '',
                            },
                        },
                        {
                            'max': 9223372036854775807,
                            'fieldName': 'testOriginStage',
                            'label': 'Test Origin',
                            'description': 'Stage used for testing in preview mode.',
                            'name': 'testOriginStage',
                            'type': 'MODEL',
                            'model': {
                                'labels': [
                                    'Amazon Redshift Connection Verifier (Library: Amazon Web Services 1.11.999)',
                                    'Amazon S3 (Library: Amazon Web Services 1.11.999)',
                                    'Amazon S3 Connection Verifier (Library: Amazon Web Services 1.11.999)',
                                    'Amazon SQS Connection Verifier (Library: Amazon Web Services 1.11.999)',
                                    'Amazon SQS Consumer (Library: Amazon Web Services 1.11.999)',
                                    'CoAP Client Connection Verifier (Library: Basic)',
                                    'CoAP Server (Library: Basic)',
                                    'Dev Data Generator (Library: Dev (for development only))',
                                    'Dev Random Record Source (Library: Dev (for development only))',
                                    'Dev Raw Data Source (Library: Dev (for development only))',
                                    'Dev SDC RPC with Buffering (Library: Basic)',
                                    'Dev Snapshot Replaying (Library: Dev (for development only))',
                                    'Directory (Library: Basic)',
                                    'File Tail (Library: Basic)',
                                    'Fragment Origin (Library: Basic)',
                                    'gRPC Client (Library: Basic)',
                                    'HTTP Client (Library: Basic)',
                                    'HTTP Server (Library: Basic)',
                                    'JavaScript Scripting (Library: Basic)',
                                    'JDBC Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'JDBC Connection Verifier (Library: JDBC)',
                                    'JDBC Multitable Consumer (Library: JDBC)',
                                    'JDBC Query Consumer (Library: JDBC)',
                                    'MQTT Connection Verifier (Library: Basic)',
                                    'MQTT Subscriber (Library: Basic)',
                                    'MySQL Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'MySQL Connection Verifier (Library: JDBC)',
                                    'NiFi HTTP Server (Library: Basic)',
                                    'OPC UA Client (Library: Basic)',
                                    'OPC UA Client Connection Verifier (Library: Basic)',
                                    'Oracle CDC Client (Library: JDBC)',
                                    'Oracle Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'Oracle Connection Verifier (Library: JDBC)',
                                    'Postgres Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'Postgres Connection Verifier (Library: JDBC)',
                                    'PostgreSQL CDC Client (Library: JDBC)',
                                    'REST Service (Library: Basic)',
                                    'SDC RPC (Library: Basic)',
                                    'Sensor Reader (Library: Dev (for development only))',
                                    'SFTP/FTP/FTPS Client (Library: Basic)',
                                    'SFTP/FTP/FTPS Connection Verifier (Library: Basic)',
                                    'Snowflake Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'Snowpipe Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'SQL Server CDC Client (Library: JDBC)',
                                    'SQL Server Change Tracking Client (Library: JDBC)',
                                    'SQLServer Connection Verifier (Library: Snowflake Enterprise Library)',
                                    'SQLServer Connection Verifier (Library: JDBC)',
                                    'System Metrics (Library: Basic)',
                                    'TCP Server (Library: Basic)',
                                    'UDP Multithreaded Source (Library: Basic)',
                                    'UDP Source (Library: Basic)',
                                    'WebSocket Client (Library: Basic)',
                                    'WebSocket Server (Library: Basic)',
                                ],
                                'values': [
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_common_redshift_AwsRedshiftConnectionVerifier::1',
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_s3_AmazonS3DSource::13',
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_common_s3_AwsS3ConnectionVerifier::1',
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_sqs_AwsSqsConnectionVerifier::1',
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_sqs_SqsDSource::6',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_common_coap_CoapClientConnectionVerifier::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_coapserver_CoapServerDPushSource::3',
                                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource::6',
                                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_RandomSource::1',
                                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_rawdata_RawDataDSource::3',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_sdcipcwithbuffer_SdcIpcWithDiskBufferDSource::4',
                                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_replaying_SnapshotReplayDSource::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_spooldir_SpoolDirDSource::13',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_logtail_FileTailDSource::6',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_fragment_FragmentSource::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_grpcclient_GrpcClientDSource::4',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_http_HttpClientDSource::23',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_httpserver_HttpServerDPushSource::16',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_javascript_JavascriptDSource::1',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_JdbcConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_JdbcConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_table_TableJdbcDSource::10',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_JdbcDSource::13',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_mqtt_connection_MqttConnectionVerifier::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_mqtt_MqttClientDSource::8',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_MySQLConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_MySQLConnectionVerifier::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_httpserver_nifi_NiFiHttpServerDPushSource::5',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_opcua_OpcUaClientDSource::5',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_opcua_OpcUaClientConnectionVerifier::2',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_oracle_OracleCDCDSource::18',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_OracleConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_OracleConnectionVerifier::1',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_PostgresConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_PostgresConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_postgres_PostgresCDCDSource::8',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_restservice_RestServiceDPushSource::8',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_sdcipc_SdcIpcDSource::3',
                                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_origin_sensorreader_SensorReaderDSource::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_remote_RemoteDownloadDSource::10',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_lib_remote_RemoteConnectionVerifier::2',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_connection_snowflake_connection_SnowflakeConnectionVerifier::1',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_connection_snowflake_connection_SnowpipeConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_sqlserver_SQLServerCDCDSource::7',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_CT_sqlserver_SQLServerCTDSource::3',
                                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_SQLServerConnectionVerifier::1',
                                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_SQLServerConnectionVerifier::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_systemmetrics_SystemMetricsDSource::2',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_tcp_TCPServerDSource::7',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_udp_MultithreadedUDPDSource::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_udp_UDPDSource::4',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_websocket_WebSocketClientDSource::8',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_websocketserver_WebSocketServerDPushSource::16',
                                ],
                                'configDefinitions': None,
                                'modelType': 'VALUE_CHOOSER',
                                'valuesProviderClass': 'com.streamsets.datacollector.config.PipelineTestStageChooserValues',
                                'filteringConfig': '',
                            },
                        },
                        {
                            'description': 'Stage that should handle pipeline stop event.',
                            'max': 9223372036854775807,
                            'fieldName': 'stopEventStage',
                            'name': 'stopEventStage',
                            'type': 'MODEL',
                            'model': {
                                'labels': [
                                    'Amazon S3 (Library: Amazon Web Services)',
                                    'Databricks Job Launcher (Library: Basic)',
                                    'Discard (Library: Basic)',
                                    'Email (Library: Basic)',
                                    'Shell (Library: Basic)',
                                    'Snowflake (Library: Snowflake Library)',
                                    'Write to Another Pipeline (Library: Basic)',
                                ],
                                'values': [
                                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor::3',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_databricks_DatabricksJobLauncherDExecutor::2',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_devnull_ToErrorNullDTarget::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_emailexecutor_EmailDExecutor::1',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_shell_ShellDExecutor::1',
                                    'streamsets-datacollector-sdc-snowflake-lib::com_streamsets_pipeline_stage_executor_snowflake_SnowflakeDExecutor::5',
                                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_sdcipc_ToErrorSdcIpcDTarget::3',
                                ],
                                'configDefinitions': None,
                                'modelType': 'VALUE_CHOOSER',
                                'compositeConfigDefinitions': None,
                                'valuesProviderClass': 'com.streamsets.datacollector.config.PipelineLifecycleStageChooserValues',
                                'filteringConfig': '',
                            },
                        },
                    ]
                }
            ],
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


class DummyJob(Job):
    """
    A dummy Job Class
    """

    def __init__(self, job):
        super().__init__(job)

    @property
    def pipeline(self):
        if self._data['pipelineCommitId'] == 'pipelineCommitId:valid':
            _pipeline = DummyPipeline()
            _pipeline.version = self._pipeline_version
            _pipeline.engine_type = EngineType('COLLECTOR')
            return _pipeline
        raise HTTPError(400)


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
        {
            "label": "Storage Container / File System",
            "name": "dataLakeStorageGen2DSource.config.storage_container_filesystem",
            "expected_output": (
                "storage_container_or_file_system",
                "dataLakeStorageGen2DSource.config.storage_container_filesystem",
            ),
        },
        {
            "label": "List of formats that should be displayed to the user.",
            "name": "dataLakeStorageGen2DSource.list_of_formats_displayed",
            "expected_output": (
                "list_of_formats_that_should_be_displayed_to_the_user",
                "dataLakeStorageGen2DSource.list_of_formats_displayed",
            ),
        },
    ]
)
def config_definition(request):
    return request.param


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(42)  # Set a fixed seed for predictable random values


@pytest.fixture(scope="function")
def dummy_job():
    json = deepcopy(DUMMY_VALID_JOB_CONFIGURATION)
    return DummyJob(json)


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
    "library_name, engine_type, result",
    [
        (
            "streamsets-spark-snowflake-with-no-dependency-lib:4.1.0",
            EngineType.TRANSFORMER,
            "snowflake-with-no-dependency",
        ),
        ("streamsets-datacollector-amazing-lib:4.2.2", EngineType.COLLECTOR, "amazing"),
        ("streamsets-transformer-noooooo-lib:0.0.1", EngineType.TRANSFORMER, "noooooo"),
    ],
)
def test_get_stage_library_display_name_from_library(library_name, engine_type, result):
    output = get_stage_library_display_name_from_library(stage_library_name=library_name, engine_type=engine_type)
    assert output == result


@pytest.mark.parametrize("invalid_library_name", [None, 3])
def test_get_stage_library_display_name_from_library_raises_type_error_with_invalid_library_name(invalid_library_name):
    with pytest.raises(TypeError):
        get_stage_library_display_name_from_library(
            stage_library_name=invalid_library_name, engine_type=EngineType.COLLECTOR
        )


@pytest.mark.parametrize("invalid_engine_type", [None, 3])
def test_get_stage_library_display_name_from_library_raises_type_error_with_invalid_deployment_type(
    invalid_engine_type,
):
    with pytest.raises(TypeError):
        get_stage_library_display_name_from_library(
            stage_library_name='streamsets-datacollector-aws-lib:3.2.0', engine_type=invalid_engine_type
        )


def test_get_stage_library_display_name_from_library_raises_value_error_with_invalid_deployment_type():
    with pytest.raises(ValueError):
        get_stage_library_display_name_from_library(
            stage_library_name='streamsets-datacollector-aws-lib:3.2.0', engine_type=EngineType.NULL
        )


@pytest.mark.parametrize(
    "library_name, engine_type",
    [
        ("streamsets-datacollector-snowflake-with-no-dependency-lib:4.1.0", EngineType.TRANSFORMER),
        ("this isn't valid", EngineType.TRANSFORMER),
    ],
)
def test_get_stage_library_display_name_from_library_raises_value_error_with_invalid_library_name(
    library_name, engine_type
):
    # value error can be raised either because the library name does not match regex string, or because an incorrect
    # combination of library name and deployment type was passed. We check for both conditions
    with pytest.raises(ValueError):
        get_stage_library_display_name_from_library(stage_library_name=library_name, engine_type=engine_type)


@pytest.mark.parametrize(
    "display_name, engine_type, deployment_engine_version, result",
    [
        ('test:1.1.1', EngineType.COLLECTOR, '5.7.2', 'streamsets-datacollector-test-lib:1.1.1'),
        ('test', EngineType.COLLECTOR, '5.7.2', 'streamsets-datacollector-test-lib:5.7.2'),
        ('credentialstore', EngineType.TRANSFORMER, '3.0.0', 'streamsets-transformer-credentialstore-lib:3.0.0'),
        ('random', EngineType.TRANSFORMER, '1.2.3', 'streamsets-spark-random-lib:1.2.3'),
    ],
)
def test_get_stage_library_name_from_display_name(display_name, engine_type, deployment_engine_version, result):
    output = get_stage_library_name_from_display_name(
        stage_library_display_name=display_name,
        engine_type=engine_type,
        deployment_engine_version=deployment_engine_version,
    )
    assert output == result


@pytest.mark.parametrize("invalid_library_name", [None, 3])
def test_get_stage_library_name_from_display_name_raises_type_error_with_invalid_library_name(invalid_library_name):
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(
            stage_library_display_name=invalid_library_name,
            engine_type=EngineType.COLLECTOR,
        )


@pytest.mark.parametrize("invalid_engine_type", [None, 3])
def test_get_stage_library_name_from_display_name_raises_type_error_with_invalid_deployment_type(
    invalid_engine_type,
):
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(stage_library_display_name='aws', engine_type=invalid_engine_type)


def test_get_stage_library_name_from_display_name_raises_value_error_with_invalid_deployment_type():
    with pytest.raises(ValueError):
        get_stage_library_name_from_display_name(stage_library_display_name='aws', engine_type=EngineType.NULL)


def test_get_stage_library_name_from_display_name_raises_type_error_when_no_version_is_passed():
    with pytest.raises(TypeError):
        get_stage_library_name_from_display_name(stage_library_display_name='aws', engine_type=EngineType.COLLECTOR)


@pytest.mark.parametrize(
    "library_name, engine_type, deployment_engine_version",
    [('aws:not-a-version', EngineType.COLLECTOR, None), ('aws', EngineType.COLLECTOR, 'again, not a version')],
)
def test_get_stage_library_name_from_display_name_raises_invalid_version_error(
    library_name, engine_type, deployment_engine_version
):
    with pytest.raises(InvalidVersionError):
        get_stage_library_name_from_display_name(
            stage_library_display_name=library_name,
            engine_type=engine_type,
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


@pytest.mark.parametrize(
    "parts, expected, result",
    [
        (["part1", "part2", "part3"], nullcontext(), "part1/part2/part3"),
        (["part1", 2, "part3"], pytest.raises(TypeError), None),
        (["part1", "/part2", "part3/"], nullcontext(), "part1/part2/part3"),
        (["part1", None, "part3"], nullcontext(), "part1/part3"),
    ],
)
def test_join_url_parts_typing_value_check(parts, expected, result):
    output = None
    with expected:
        output = join_url_parts(*parts)
    assert output == result


@pytest.mark.parametrize(
    "field_name, field_value",
    [
        (['pipeline_id', None]),
        (['pipeline_id', ""]),
        (['pipeline_id', 5]),
        (['commit_id', True]),
        (['commit_id', ""]),
        (['commit_id', 'not_valid']),
        (['commit_label', 'v1-DRAFT']),
    ],
)
def test_validate_job_fails_for_invalid_job_configuration(field_name, field_value, dummy_job):
    dummy_job.__setattr__(field_name, field_value)
    with pytest.raises(ValidationError):
        validate_job(dummy_job)


def test_validate_job_fails_for_different_type_of_engines(dummy_job):
    dummy_job._data['executorType'] = "TRANSFORMER"  # pipeline engine is set to COLLECTOR
    with pytest.raises(ValidationError):
        validate_job(dummy_job)


def test_validate_job_passes_for_valid_job_configuration(dummy_job):
    result = validate_job(dummy_job)
    assert result is None


@pytest.mark.parametrize(
    "field_name, correct_response",
    [
        (
            'startEventStage',
            (
                [
                    'Amazon S3',
                    'Databricks Job Launcher',
                    'Discard',
                    'Email',
                    'JDBC Query',
                    'Shell',
                    'Snowflake',
                    'Write to Another Pipeline',
                ],
                [
                    'Amazon Web Services 1.11.999',
                    'Basic',
                    'Basic',
                    'Basic',
                    'JDBC',
                    'Basic',
                    'Snowflake Enterprise Library',
                    'Basic',
                ],
                [
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor::3',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_databricks_DatabricksJobLauncherDExecutor::2',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_devnull_ToErrorNullDTarget::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_emailexecutor_EmailDExecutor::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_executor_jdbc_JdbcQueryDExecutor::5',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_shell_ShellDExecutor::1',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_stage_executor_snowflake_SnowflakeDExecutor::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_sdcipc_ToErrorSdcIpcDTarget::3',
                ],
            ),
        ),
        (
            'testOriginStage',
            (
                [
                    'Amazon Redshift Connection Verifier',
                    'Amazon S3',
                    'Amazon S3 Connection Verifier',
                    'Amazon SQS Connection Verifier',
                    'Amazon SQS Consumer',
                    'CoAP Client Connection Verifier',
                    'CoAP Server',
                    'Dev Data Generator',
                    'Dev Random Record Source',
                    'Dev Raw Data Source',
                    'Dev SDC RPC with Buffering',
                    'Dev Snapshot Replaying',
                    'Directory',
                    'File Tail',
                    'Fragment Origin',
                    'gRPC Client',
                    'HTTP Client',
                    'HTTP Server',
                    'JavaScript Scripting',
                    'JDBC Connection Verifier',
                    'JDBC Connection Verifier',
                    'JDBC Multitable Consumer',
                    'JDBC Query Consumer',
                    'MQTT Connection Verifier',
                    'MQTT Subscriber',
                    'MySQL Connection Verifier',
                    'MySQL Connection Verifier',
                    'NiFi HTTP Server',
                    'OPC UA Client',
                    'OPC UA Client Connection Verifier',
                    'Oracle CDC Client',
                    'Oracle Connection Verifier',
                    'Oracle Connection Verifier',
                    'Postgres Connection Verifier',
                    'Postgres Connection Verifier',
                    'PostgreSQL CDC Client',
                    'REST Service',
                    'SDC RPC',
                    'Sensor Reader',
                    'SFTP/FTP/FTPS Client',
                    'SFTP/FTP/FTPS Connection Verifier',
                    'Snowflake Connection Verifier',
                    'Snowpipe Connection Verifier',
                    'SQL Server CDC Client',
                    'SQL Server Change Tracking Client',
                    'SQLServer Connection Verifier',
                    'SQLServer Connection Verifier',
                    'System Metrics',
                    'TCP Server',
                    'UDP Multithreaded Source',
                    'UDP Source',
                    'WebSocket Client',
                    'WebSocket Server',
                ],
                [
                    'Amazon Web Services 1.11.999',
                    'Amazon Web Services 1.11.999',
                    'Amazon Web Services 1.11.999',
                    'Amazon Web Services 1.11.999',
                    'Amazon Web Services 1.11.999',
                    'Basic',
                    'Basic',
                    'Dev (for development only',
                    'Dev (for development only',
                    'Dev (for development only',
                    'Basic',
                    'Dev (for development only',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'JDBC',
                    'JDBC',
                    'Basic',
                    'Basic',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'Basic',
                    'Basic',
                    'Basic',
                    'JDBC',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'JDBC',
                    'Basic',
                    'Basic',
                    'Dev (for development only',
                    'Basic',
                    'Basic',
                    'Snowflake Enterprise Library',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'JDBC',
                    'Snowflake Enterprise Library',
                    'JDBC',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                    'Basic',
                ],
                [
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_common_redshift_AwsRedshiftConnectionVerifier::1',
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_s3_AmazonS3DSource::13',
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_common_s3_AwsS3ConnectionVerifier::1',
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_sqs_AwsSqsConnectionVerifier::1',
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_origin_sqs_SqsDSource::6',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_common_coap_CoapClientConnectionVerifier::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_coapserver_CoapServerDPushSource::3',
                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource::6',
                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_RandomSource::1',
                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_rawdata_RawDataDSource::3',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_sdcipcwithbuffer_SdcIpcWithDiskBufferDSource::4',
                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_devtest_replaying_SnapshotReplayDSource::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_spooldir_SpoolDirDSource::13',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_logtail_FileTailDSource::6',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_fragment_FragmentSource::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_grpcclient_GrpcClientDSource::4',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_http_HttpClientDSource::23',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_httpserver_HttpServerDPushSource::16',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_javascript_JavascriptDSource::1',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_JdbcConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_JdbcConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_table_TableJdbcDSource::10',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_JdbcDSource::13',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_mqtt_connection_MqttConnectionVerifier::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_mqtt_MqttClientDSource::8',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_MySQLConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_MySQLConnectionVerifier::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_httpserver_nifi_NiFiHttpServerDPushSource::5',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_opcua_OpcUaClientDSource::5',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_opcua_OpcUaClientConnectionVerifier::2',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_oracle_OracleCDCDSource::18',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_OracleConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_OracleConnectionVerifier::1',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_PostgresConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_PostgresConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_postgres_PostgresCDCDSource::8',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_restservice_RestServiceDPushSource::8',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_sdcipc_SdcIpcDSource::3',
                    'streamsets-datacollector-dev-lib::com_streamsets_pipeline_stage_origin_sensorreader_SensorReaderDSource::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_remote_RemoteDownloadDSource::10',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_lib_remote_RemoteConnectionVerifier::2',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_connection_snowflake_connection_SnowflakeConnectionVerifier::1',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_connection_snowflake_connection_SnowpipeConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_cdc_sqlserver_SQLServerCDCDSource::7',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_stage_origin_jdbc_CT_sqlserver_SQLServerCTDSource::3',
                    'streamsets-datacollector-snowflake-lib::com_streamsets_pipeline_lib_jdbc_connection_SQLServerConnectionVerifier::1',
                    'streamsets-datacollector-jdbc-lib::com_streamsets_pipeline_lib_jdbc_connection_SQLServerConnectionVerifier::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_systemmetrics_SystemMetricsDSource::2',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_tcp_TCPServerDSource::7',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_udp_MultithreadedUDPDSource::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_udp_UDPDSource::4',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_websocket_WebSocketClientDSource::8',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_origin_websocketserver_WebSocketServerDPushSource::16',
                ],
            ),
        ),
        (
            'stopEventStage',
            (
                [
                    'Amazon S3',
                    'Databricks Job Launcher',
                    'Discard',
                    'Email',
                    'Shell',
                    'Snowflake',
                    'Write to Another Pipeline',
                ],
                ['Amazon Web Services', 'Basic', 'Basic', 'Basic', 'Basic', 'Snowflake Library', 'Basic'],
                [
                    'streamsets-datacollector-aws-lib::com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor::3',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_databricks_DatabricksJobLauncherDExecutor::2',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_devnull_ToErrorNullDTarget::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_emailexecutor_EmailDExecutor::1',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_executor_shell_ShellDExecutor::1',
                    'streamsets-datacollector-sdc-snowflake-lib::com_streamsets_pipeline_stage_executor_snowflake_SnowflakeDExecutor::5',
                    'streamsets-datacollector-basic-lib::com_streamsets_pipeline_stage_destination_sdcipc_ToErrorSdcIpcDTarget::3',
                ],
            ),
        ),
    ],
)
def test_get_accepted_labels_libraries_and_names_start_event_stage(field_name, correct_response):
    pipeline_builder = DummyPipelineBuilder()
    assert get_accepted_labels_libraries_and_names(pipeline_builder, field_name) == correct_response
