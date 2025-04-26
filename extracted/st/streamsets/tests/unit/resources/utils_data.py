TEST_VALIDATE_PIPELINE_STAGES_PASSES_FOR_VALID_PIPELINE_WITH_VALID_STAGES_JSON = {
    'instanceName': 'DevDataGenerator_1',
    'library': 'streamsets-datacollector-dev-lib',
    'stageName': 'com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource',
    'stageVersion': '6',
    'configuration': [
        {'name': 'delay', 'value': 1000},
        {'name': 'numberOfRecords', 'value': 0},
        {'name': 'eventName', 'value': 'generated-event'},
        {'name': 'batchSize', 'value': 1000},
        {'name': 'headerAttributes', 'value': []},
        {
            'name': 'dataGenConfigs',
            'value': [{'type': 'STRING', 'precision': 10, 'scale': 2, 'fieldAttributes': []}],
        },
        {'name': 'numThreads', 'value': 1},
        {'name': 'rootFieldType', 'value': 'MAP'},
        {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
    ],
    'uiInfo': {
        'colorIcon': 'Origin_Dev_Data_Generator.png',
        'outputStreamLabels': None,
        'yPos': 50,
        'stageType': 'SOURCE',
        'rawSource': None,
        'icon': 'dev.png',
        'description': '',
        'inputStreamLabels': None,
        'label': 'Dev Data Generator 1',
        'xPos': 60,
        'displayMode': 'BASIC',
    },
    'inputLanes': [],
    'outputLanes': ['DevDataGenerator_1OutputLane17048194517380'],
    'eventLanes': [],
    'services': [],
}

TEST_VALIDATE_PIPELINE_STAGES_FAILS_FOR_INVALID_PIPELINE_WITH_INVALID_STAGES_JSON = {
    'instanceName': 'AmazonS3_01',
    'library': 'streamsets-datacollector-aws-lib',
    'stageName': 'com_streamsets_pipeline_stage_destination_s3_AmazonS3DTarget',
    'stageVersion': '15',
    'configuration': [
        {'name': 's3TargetConfigBean.s3Config.connection.awsConfig.awsSecretAccessKey', 'value': None},
        {'name': 's3TargetConfigBean.tmConfig.threadPoolSize', 'value': 10},
    ],
    'uiInfo': {
        'colorIcon': 'Destination_Amazon_S3.png',
        'description': '',
        'label': 'Amazon S3 1',
        'xPos': 280,
        'yPos': 50,
        'stageType': 'TARGET',
    },
    'inputLanes': [],
    'outputLanes': [],
    'eventLanes': [],
    'services': [
        {
            'service': 'com.streamsets.pipeline.api.service.dataformats.DataFormatGeneratorService',
            'serviceVersion': '3',
            'configuration': [
                {'name': 'displayFormats', 'value': 'AVRO,BINARY,DELIMITED,JSON,PROTOBUF,SDC_JSON,TEXT,WHOLE_FILE'},
            ],
        }
    ],
}
