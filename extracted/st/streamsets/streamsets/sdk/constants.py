# Copyright 2020 StreamSets Inc.

"""
This module contains project-wide constants.
"""

# fmt: off
import collections

from .exceptions import ConnectError, InvalidError, RunError, RunningError, StartError, StartingError, ValidationError

# fmt: on


ENGINE_AUTHENTICATION_METHOD_FORM = 'form'
ENGINE_AUTHENTICATION_METHOD_ASTER = 'aster'

SDC_EXECUTOR_TYPE = 'COLLECTOR'
SNOWFLAKE_EXECUTOR_TYPE = 'SNOWPARK'
SNOWFLAKE_ENGINE_ID = 'SYSTEM_SNOWPARK_ENGINE_ID'
TRANSFORMER_EXECUTOR_TYPE = 'TRANSFORMER'

SDC_DEPLOYMENT_TYPE = 'DC'
TRANSFORMER_DEPLOYMENT_TYPE = 'TF'

EXECUTOR_TO_DEPLOYMENT_MAP = {
    SDC_EXECUTOR_TYPE: SDC_DEPLOYMENT_TYPE,
    TRANSFORMER_EXECUTOR_TYPE: TRANSFORMER_DEPLOYMENT_TYPE,
}

ENGINELESS_ENGINE_ID = 'SYSTEM_DESIGNER'
ENGINELESS_CONNECTION_ID = 'ENGINELESS_ID'

StageConfigurationProperty = collections.namedtuple('StageConfigurationProperty', ['config_name'])
ServiceConfigurationProperty = collections.namedtuple('ServiceConfigurationProperty', ['service_name', 'config_name'])

# Default values for Deployment Engine Configurations
DEFAULT_MAX_CPU_LOAD_VALUE = 80.0
DEFAULT_MAX_MEMORY_USED_VALUE = 100.0
DEFAULT_MAX_PIPELINES_RUNNING_VALUE = 1000000


# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent SDC release, the older attribute name should be mapped
# to the newer one.
SDC_STAGE_ATTRIBUTE_RENAME_ALIASES = {
    'com_streamsets_pipeline_stage_destination_couchbase_CouchbaseConnectorDTarget': {
        # https://git.io/fABEc
        'generate_unique_document_key': 'generate_document_key',
        'unique_document_key_field': 'document_key_field',
    },
    'com_streamsets_pipeline_stage_destination_hdfs_HdfsDTarget': {
        # https://git.io/fjCZ1, https://git.io/fjCZD
        'hadoop_fs_configuration': 'additional_configuration',
        'hadoop_fs_configuration_directory': 'configuration_files_directory',
        'hadoop_fs_uri': 'file_system_uri',
        'hdfs_user': 'impersonation_user',
        'validate_hdfs_permissions': 'validate_permissions',
    },
    'com_streamsets_pipeline_stage_destination_s3_AmazonS3DTarget': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_s3_S3ConnectionTargetConfig': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_s3_ToErrorAmazonS3DTarget': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_destination_snowflake_SnowflakeDTarget': {
        # https://git.io/Jednw, https://git.io/JJ61u, https://git.io/JJ61w
        'cdc_data': 'processing_cdc_data',
        'stage_location': 'external_stage_location',
        'external_stage_name': 'snowflake_stage_name',
    },
    'com_streamsets_pipeline_stage_executor_s3_AmazonS3DExecutor': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_stage_origin_hdfs_HdfsDSource': {
        # https://git.io/fjCZ1, https://git.io/fjCZD
        'hadoop_fs_configuration': 'additional_configuration',
        'hadoop_fs_configuration_directory': 'configuration_files_directory',
        'hadoop_fs_uri': 'file_system_uri',
        'hdfs_user': 'impersonation_user',
    },
    'com_streamsets_pipeline_stage_origin_httpserver_HttpServerDPushSource': {
        # https://git.io/JvBgX
        'application_id': 'list_of_application_ids',
    },
    'com_streamsets_pipeline_stage_origin_jdbc_cdc_oracle_OracleCDCDSource': {
        # https://git.io/Jt6CY
        'use_peg_parser_in_beta': 'use_peg_parser',
    },
    'com_streamsets_pipeline_stage_origin_spooldir_SpoolDirDSource': {
        # https://git.io/vpJ8w
        'max_files_in_directory': 'max_files_soft_limit',
    },
    'com_streamsets_pipeline_stage_origin_startJob_StartJobDSource': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'unique_task_name': 'task_name',
        'url_of_control_hub_that_runs_the_specified_jobs': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_origin_startPipeline_StartPipelineDSource': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'control_hub_base_url': 'control_hub_url',
        'unique_task_name': 'task_name',
    },
    'com_streamsets_pipeline_stage_processor_kudulookup_KuduLookupDProcessor': {
        # https://git.io/vpJZF
        'ignore_missing_value': 'ignore_missing_value_in_matching_record',
    },
    'com_streamsets_pipeline_stage_processor_startJob_StartJobDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'unique_task_name': 'task_name',
        'url_of_control_hub_that_runs_the_specified_jobs': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_startPipeline_StartPipelineDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'control_hub_base_url': 'control_hub_url',
        'unique_task_name': 'task_name',
    },
    'com_streamsets_pipeline_stage_processor_waitForJobCompletion_WaitForJobCompletionDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
        'url_of_control_hub': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_waitForPipelineCompletion_WaitForPipelineCompletionDProcessor': {
        # https://git.io/JJsTN
        'delay_between_state_checks': 'status_check_interval',
    },
    'com_streamsets_pipeline_stage_processor_controlHub_ControlHubApiDProcessor': {
        # https://git.io/JOcVh
        'control_hub_api_url': 'control_hub_url',
    },
    'com_streamsets_pipeline_stage_processor_http_HttpDProcessor': {
        'pass_record': 'pass_records',
    },
    'com_streamsets_pipeline_stage_origin_jdbc_cdc_postgres_PostgresCDCDSource': {
        # https://git.io/J1O0w
        'database_time_zone': 'db_time_zone',
    },
}

# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent TfS release, the older attribute name should be mapped
# to the newer one.
SNOWFLAKE_STAGE_ATTRIBUTE_RENAME_ALIASES = {
    'com_streamsets_transformer_snowpark_processor_join_JoinDProcessor': {
        'input_1': 'input_1_in_left',
        'input_2': 'input_2_in_right',
        'join_using_condition': 'join_condition',
    },
}

# This dictionary maps the stage labels from old labeling to the new ones.
# When calling SDCPipelineBuilder.add_stage('Snowflake SQL Evaluator') it should return the stage with
# label Column Transformer.
SNOWFLAKE_STAGE_RENAME_ALIASES = {'Snowflake SQL Evaluator': 'Column Transformer'}

# This is a dictionary mapping stage names to attribute aliases. As an example, if a particular
# stage had a label updated in a more recent ST release, the older attribute name should be mapped
# to the newer one.
ST_STAGE_ATTRIBUTE_RENAME_ALIASES = {
    'com_streamsets_pipeline_spark_destination_redshift_RedshiftDDestination': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_destination_s3_AmazonS3DDestination': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_mysql_MySQLJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_oracle_OracleJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_postgresql_PostgreJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_jdbc_table_branded_sqlserver_SqlServerJdbcTableDOrigin': {
        'max_number_of_partitions': 'number_of_partitions',
    },
    'com_streamsets_pipeline_spark_origin_redshift_RedshiftDOrigin': {
        'bucket': 'bucket_and_path',
    },
    'com_streamsets_pipeline_spark_origin_s3_AmazonS3DOrigin': {
        'bucket': 'bucket_and_path',
    },
}

# For various reasons, a few configurations don't lend themselves to easy conversion
# from their labels; the overrides handle those edge cases.
STAGE_CONFIG_OVERRIDES = {
    'com_streamsets_datacollector_pipeline_executor_spark_SparkDExecutor': {
        'maximum_time_to_wait_in_ms': StageConfigurationProperty('conf.yarnConfigBean.waitTimeout'),
    },
    'com_streamsets_pipeline_stage_bigquery_origin_BigQueryDSource': {
        'use_cached_query_results': StageConfigurationProperty('conf.useQueryCache'),
    },
    'com_streamsets_pipeline_stage_destination_elasticsearch_ElasticSearchDTarget': {
        'security_username_and_password': StageConfigurationProperty('elasticSearchConfig.securityConfig.securityUser'),
    },
    'com_streamsets_pipeline_stage_destination_elasticsearch_ToErrorElasticSearchDTarget': {
        'security_username_and_password': StageConfigurationProperty('elasticSearchConfig.securityConfig.securityUser'),
    },
    'com_streamsets_pipeline_stage_destination_snowflake_SnowflakeDTarget': {
        'processing_cdc_data': StageConfigurationProperty('config.data.cdcData'),
    },
    'com_streamsets_pipeline_stage_devtest_rawdata_RawDataDSource': {
        'data_format': [
            StageConfigurationProperty('dataFormat'),
            ServiceConfigurationProperty(
                'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatParserService', 'dataFormat'
            ),
        ],
        'datagram_data_format': [
            StageConfigurationProperty('dataFormatConfig.datagramMode'),
            ServiceConfigurationProperty(
                'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatParserService',
                'dataFormatConfig.datagramMode',
            ),
        ],
    },
    'com_streamsets_pipeline_stage_origin_coapserver_CoapServerDPushSource': {
        'data_format': StageConfigurationProperty('dataFormat'),
        'datagram_data_format': StageConfigurationProperty('dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_elasticsearch_ElasticsearchDSource': {
        'security_username_and_password': StageConfigurationProperty('elasticSearchConfig.securityConfig.securityUser'),
    },
    'com_streamsets_pipeline_stage_origin_hdfs_cluster_ClusterHdfsDSource': {
        'data_format': StageConfigurationProperty('clusterHDFSConfigBean.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('clusterHDFSConfigBean.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_http_HttpClientDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
        'initial_page_or_offset': StageConfigurationProperty('conf.pagination.startAt'),
    },
    'com_streamsets_pipeline_stage_origin_httpserver_HttpServerDPushSource': {
        'data_format': StageConfigurationProperty('dataFormat'),
        'datagram_data_format': StageConfigurationProperty('dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_jms_JmsDSource': {
        'data_format': [
            StageConfigurationProperty('dataFormat'),
            ServiceConfigurationProperty(
                'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatParserService', 'dataFormat'
            ),
        ],
        'datagram_data_format': [
            StageConfigurationProperty('dataFormatConfig.datagramMode'),
            ServiceConfigurationProperty(
                'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatParserService',
                'dataFormatConfig.datagramMode',
            ),
        ],
    },
    'com_streamsets_pipeline_stage_origin_kafka_KafkaDSource': {
        'data_format': StageConfigurationProperty('kafkaConfigBean.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('kafkaConfigBean.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_kinesis_KinesisDSource': {
        'data_format': StageConfigurationProperty('kinesisConfig.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('kinesisConfig.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_logtail_FileTailDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_maprfs_ClusterMapRFSDSource': {
        'data_format': StageConfigurationProperty('clusterHDFSConfigBean.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('clusterHDFSConfigBean.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_maprstreams_MapRStreamsDSource': {
        'data_format': StageConfigurationProperty('maprstreamsSourceConfigBean.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('maprstreamsSourceConfigBean.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_mqtt_MqttClientDSource': {
        'data_format': StageConfigurationProperty('subscriberConf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('subscriberConf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_rabbitmq_RabbitDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_redis_RedisDSource': {
        'data_format': StageConfigurationProperty('redisOriginConfigBean.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('redisOriginConfigBean.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_remote_RemoteDownloadDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_s3_AmazonS3DSource': {
        'data_format': [
            StageConfigurationProperty('s3ConfigBean.dataFormat'),
            ServiceConfigurationProperty(
                'com.streamsets.pipeline.api.service.' 'dataformats.DataFormatParserService', 'dataFormat'
            ),
        ],
    },
    'com_streamsets_pipeline_stage_origin_spooldir_SpoolDirDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_tcp_TCPServerDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_origin_websocketserver_WebSocketServerDPushSource': {
        'data_format': StageConfigurationProperty('dataFormat'),
        'datagram_data_format': StageConfigurationProperty('dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_processor_http_HttpDProcessor': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
    'com_streamsets_pipeline_stage_pubsub_origin_PubSubDSource': {
        'data_format': StageConfigurationProperty('conf.dataFormat'),
        'datagram_data_format': StageConfigurationProperty('conf.dataFormatConfig.datagramMode'),
    },
}

STATUS_ERRORS = {
    'CONNECT_ERROR': ConnectError,
    'RUN_ERROR': RunError,
    'RUNNING_ERROR': RunningError,
    'START_ERROR': StartError,
    'STARTING_ERROR': StartingError,
    'INVALID': InvalidError,
    'VALIDATION_ERROR': ValidationError,
}


"""
 The following dictionary keeps backward compatibility for renamed pipeline configurations in Transformer engines.
 The way this dictionary should be formatted is as following:

    {
        'version1': {
            'old name 1' {
                'name': 'new name 1',
                'values': {
                    'old value 1': 'new value 1',
                    'old value 2': 'new value 2'
                }
            },
            'old value 2': {
                'name': 'new name 2',
                'values': {
                    'old value 3': 'new value 3',
                    'old value 4': 'new value 4'
                }
            }
        },
        'more versions': {
            ...
        }
    }

 The versions should be sorted in ascending order.
"""

ST_PIPELINE_BW_COMPATIBILITY = {
    '5.7.0': {
        'transformerEmrConnection.provisionNewCluster': {
            'name': 'transformerEmrConnection.emrClusterOption',
            'values': {True: 'PROVISION_CLUSTER', False: 'EXISTING_CLUSTER'},
        },
        'transformerEmrConnection.createNewApplication': {
            'name': 'transformerEmrConnection.emrClusterOption',
            'values': {True: 'PROVISION_CLUSTER', False: 'EXISTING_CLUSTER'},
        },
    },
    '6.0.0': {
        # Transformer
        'transformerEmrConnection.masterInstanceType': {'name': 'transformerEmrConnection.primaryInstanceType'},
        'transformerEmrConnection.masterInstanceTypeCustom': {
            'name': 'transformerEmrConnection.primaryInstanceTypeCustom'
        },
        'transformerEmrConnection.masterSecurityGroup': {'name': 'transformerEmrConnection.primarySecurityGroup'},
        'transformerEmrConnection.slaveInstanceType': {'name': 'transformerEmrConnection.secondaryInstanceType'},
        'transformerEmrConnection.slaveInstanceTypeCustom': {
            'name': 'transformerEmrConnection.secondaryInstanceTypeCustom'
        },
        'transformerEmrConnection.slaveSecurityGroup': {'name': 'transformerEmrConnection.secondarySecurityGroup'},
        # Data Collector
        'sdcEmrConnection.masterInstanceType': {'name': 'sdcEmrConnection.primaryInstanceType'},
        'sdcEmrConnection.masterInstanceTypeCustom': {'name': 'sdcEmrConnection.primaryInstanceTypeCustom'},
        'sdcEmrConnection.masterSecurityGroup': {'name': 'sdcEmrConnection.primarySecurityGroup'},
        'sdcEmrConnection.slaveInstanceType': {'name': 'sdcEmrConnection.secondaryInstanceType'},
        'sdcEmrConnection.slaveInstanceTypeCustom': {'name': 'sdcEmrConnection.secondaryInstanceTypeCustom'},
        'sdcEmrConnection.slaveSecurityGroup': {'name': 'sdcEmrConnection.secondarySecurityGroup'},
    },
}


"""
 The following dictionary keeps backward compatibility for renamed pipeline configurations in Transformer engines.
 This dictionary should be formatted is the same as the pipeline compatibility map,
 with the connection type as a top level condition.
 The versions should be sorted inside each connection type in ascending order.
"""


SDC_CONNECTIONS_BW_COMPATIBILITY = {
    'STREAMSETS_AWS_EMR_CLUSTER': {
        '5.10.0': {
            'provisionNewCluster': {
                'name': 'emrClusterOption',
                'values': {True: 'PROVISION_CLUSTER', False: 'EXISTING_CLUSTER'},
            },
            'createNewApplication': {
                'name': 'emrClusterOption',
                'values': {True: 'PROVISION_CLUSTER', False: 'EXISTING_CLUSTER'},
            },
        }
    },
}
