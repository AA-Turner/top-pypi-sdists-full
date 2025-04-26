import json

# Referenced Data for function dummy_connection(mocker)
dummy_connection_connection_definition_json = json.dumps(
    {
        'type': 'STREAMSETS_SNOWFLAKE',
        'version': '7',
        'configuration': [
            {'name': 'connectionProperties', 'value': [{}]},
            {'name': 'privateKeyPemPath', 'value': None},
            {'name': 'useSnowflakeRole', 'value': False},
            {'name': 'user', 'value': 'Test User'},
            {'name': 'account', 'value': 'Test Account'},
        ],
    }
)
dummy_connection_library_definitions_json = json.dumps(
    {
        'configDefinitions': [
            {
                'name': 'connectionProperties',
                'label': 'Connection Properties',
                'fieldName': 'connectionProperties',
            },
            {
                'name': 'privateKeyPemPath',
                'label': 'Private Key Path',
                'fieldName': 'privateKeyPemPath',
            },
            {
                'name': 'useSnowflakeRole',
                'label': 'Use Snowflake Role',
                'fieldName': 'useSnowflakeRole',
            },
            {
                'name': 'account',
                'label': 'Account',
                'fieldName': 'account',
            },
            {
                'name': 'User',
                'label': 'user',
                'fieldName': 'user',
            },
        ]
    }
)

DUMMY_CONNECTION_JSON = {
    'id': '011c7781-48a1-4d4c-93c8-1ad42a5505cb:1a1b7cf4-862e-11ed-94d5-41a005fd7967',
    'name': 'Snowflake Demo Connection',
    'connectionType': 'STREAMSETS_SNOWFLAKE',
    'connectionDefinition': dummy_connection_connection_definition_json,
    'libraryDefinition': dummy_connection_library_definitions_json,
}

DUMMY_DESTINATION_STAGE_JSON = {
    'instanceName': 'AmazonS3_1',
    'library': 'streamsets-datacollector-aws-lib',
    'stageName': 'com_streamsets_pipeline_stage_destination_s3_AmazonS3DTarget',
    'stageVersion': '15',
    'configuration': [
        {'name': 's3TargetConfigBean.s3Config.connection.awsConfig.awsSecretAccessKey', 'value': '1212'},
        {'name': 's3TargetConfigBean.tmConfig.threadPoolSize', 'value': 10},
        {'name': 's3TargetConfigBean.tmConfig.multipartUploadThreshold', 'value': 26843545},
        {'name': 's3TargetConfigBean.s3Config.connection.proxyConfig.proxyWorkstation', 'value': None},
        {'name': 's3TargetConfigBean.s3Config.connection.proxyConfig.socketTimeout', 'value': 50},
        {'name': 's3TargetConfigBean.s3Config.connection.endpoint', 'value': None},
        {'name': 's3TargetConfigBean.s3Config.connectionSelection', 'value': 'MANUAL'},
        {'name': 's3TargetConfigBean.s3Config.connection.awsConfig.sessionDuration', 'value': 3600},
        {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
        {'name': 'stageRequiredFields', 'value': []},
        {'name': 'stageRecordPreconditions', 'value': []},
    ],
    'uiInfo': {
        'colorIcon': 'Destination_Amazon_S3.png',
        'outputStreamLabels': None,
        'yPos': 50,
        'stageType': 'TARGET',
        'rawSource': None,
        'icon': 's3.png',
        'description': '',
        'inputStreamLabels': None,
        'label': 'Amazon S3 1',
        'xPos': 280,
        'displayMode': 'BASIC',
    },
    'inputLanes': [],
    'outputLanes': [],
    'eventLanes': ['AmazonS3_1_EventLane'],
    'services': [
        {
            'service': 'com.streamsets.pipeline.api.service.dataformats.DataFormatGeneratorService',
            'serviceVersion': 3,
            'configuration': [
                {'name': 'dataFormat', 'value': 'BINARY'},
                {'name': 'dataGeneratorFormatConfig.charset', 'value': 'UTF-8'},
                {'name': 'dataGeneratorFormatConfig.csvHeader', 'value': 'NO'},
                {'name': 'dataGeneratorFormatConfig.csvFileFormat', 'value': 'CSV'},
                {'name': 'dataGeneratorFormatConfig.csvCustomDelimiter', 'value': '|'},
                {'name': 'dataGeneratorFormatConfig.avroSchema', 'value': None},
                {'name': 'dataGeneratorFormatConfig.xmlPrettyPrint', 'value': True},
                {'name': 'dataGeneratorFormatConfig.xmlValidateSchema', 'value': False},
                {'name': 'dataGeneratorFormatConfig.xmlSchema', 'value': None},
            ],
        }
    ],
}
