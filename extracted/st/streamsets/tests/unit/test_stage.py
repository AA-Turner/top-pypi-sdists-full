# fmt: off
import pytest

from streamsets.sdk.constants import StageConfigurationProperty
from streamsets.sdk.sch_models import Connection, SchSdcStage, SchStStage

# fmt: on

NUM_OF_STAGES = 5


class DummyPipeline:
    """
    A Dummy Pipeline Class
    """

    def __init__(self):
        self.stages = []

    def add_stage(self, *stages):
        for stage in stages:
            stage._pipeline = self
            self.stages.append(stage)


class DummyPipelineBuilder:
    """
    A Dummy Pipeline Class Builder
    """

    def __init__(self):
        self._config_key = 'pipelineBuilder'
        self._pipeline = {self._config_key: {'stages': []}}

    def add_stage(self, *stages):
        for stage in stages:
            stage._pipeline = self
            self._pipeline[self._config_key]['stages'].append(stage._data)


@pytest.fixture(scope="function")
def dummy_pipeline():
    return DummyPipeline()


@pytest.fixture(scope="function")
def dummy_pipeline_builder():
    return DummyPipelineBuilder()


@pytest.fixture(scope="function")
def dev_data_generator_sdc_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'DevDataGenerator_{}'.format(i),
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
                'label': 'Dev Data Generator {}'.format(i),
                'xPos': 60,
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['DevDataGenerator_1OutputLane1694131201219{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchSdcStage(stage=stage_json))

    return stages


@pytest.fixture(scope="function")
def dev_data_generator_st_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'DevDataGenerator_{}'.format(i),
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
                'label': 'Dev Data Generator {}'.format(i),
                'xPos': 60,
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['DevDataGenerator_1OutputLane1694131201219{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchStStage(stage=stage_json))

    return stages


@pytest.fixture(scope="function")
def trash_sdc_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'Trash_{}'.format(i),
            'library': 'streamsets-datacollector-basic-lib',
            'stageName': 'com_streamsets_pipeline_stage_destination_devnull_NullDTarget',
            'stageVersion': '1',
            'configuration': [],
            'uiInfo': {
                'colorIcon': 'Destination_Trash.png',
                'outputStreamLabels': None,
                'yPos': 180,
                'stageType': 'TARGET',
                'rawSource': None,
                'icon': 'trash.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Trash {}'.format(i),
                'xPos': 940,
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': [],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchSdcStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def trash_st_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'Trash_{}'.format(i),
            'library': 'streamsets-datacollector-basic-lib',
            'stageName': 'com_streamsets_pipeline_stage_destination_devnull_NullDTarget',
            'stageVersion': '1',
            'configuration': [],
            'uiInfo': {
                'colorIcon': 'Destination_Trash.png',
                'outputStreamLabels': None,
                'yPos': 180,
                'stageType': 'TARGET',
                'rawSource': None,
                'icon': 'trash.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Trash {}'.format(i),
                'xPos': 940,
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': [],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchStStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def delay_sdc_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'Delay_{}'.format(i),
            'library': 'streamsets-datacollector-basic-lib',
            'stageName': 'com_streamsets_pipeline_stage_processor_delay_DelayProcessor',
            'stageVersion': '2',
            'configuration': [
                {'name': 'delay', 'value': 1000},
                {'name': 'skipDelayOnEmptyBatch', 'value': False},
                {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
                {'name': 'stageRequiredFields', 'value': []},
                {'name': 'stageRecordPreconditions', 'value': []},
            ],
            'uiInfo': {
                'colorIcon': 'Processor_Delay.png',
                'outputStreamLabels': None,
                'yPos': '233.043875',
                'stageType': 'PROCESSOR',
                'rawSource': None,
                'icon': 'delay.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Delay {}'.format(i),
                'xPos': '1072.1999999999998',
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['Delay_1OutputLane1694191364195{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchSdcStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def delay_st_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'Delay_{}'.format(i),
            'library': 'streamsets-datacollector-basic-lib',
            'stageName': 'com_streamsets_pipeline_stage_processor_delay_DelayProcessor',
            'stageVersion': '2',
            'configuration': [
                {'name': 'delay', 'value': 1000},
                {'name': 'skipDelayOnEmptyBatch', 'value': False},
                {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
                {'name': 'stageRequiredFields', 'value': []},
                {'name': 'stageRecordPreconditions', 'value': []},
            ],
            'uiInfo': {
                'colorIcon': 'Processor_Delay.png',
                'outputStreamLabels': None,
                'yPos': '233.043875',
                'stageType': 'PROCESSOR',
                'rawSource': None,
                'icon': 'delay.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Delay {}'.format(i),
                'xPos': '1072.1999999999998',
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['Delay_1OutputLane1694191364195{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchStStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def dev_identity_sdc_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'DevIdentity_{}'.format(i),
            'library': 'streamsets-datacollector-dev-lib',
            'stageName': 'com_streamsets_pipeline_stage_processor_identity_IdentityProcessor',
            'stageVersion': '1',
            'configuration': [
                {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
                {'name': 'stageRequiredFields', 'value': []},
                {'name': 'stageRecordPreconditions', 'value': []},
            ],
            'uiInfo': {
                'colorIcon': 'Processor_Dev_Identity.png',
                'outputStreamLabels': None,
                'yPos': '387.065875',
                'stageType': 'PROCESSOR',
                'rawSource': None,
                'icon': 'dev.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Dev Identity {}'.format(i),
                'xPos': '1083.1999999999998',
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['DevIdentity_1OutputLane1694195672155{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchSdcStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def dev_identity_st_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'DevIdentity_{}'.format(i),
            'library': 'streamsets-datacollector-dev-lib',
            'stageName': 'com_streamsets_pipeline_stage_processor_identity_IdentityProcessor',
            'stageVersion': '1',
            'configuration': [
                {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
                {'name': 'stageRequiredFields', 'value': []},
                {'name': 'stageRecordPreconditions', 'value': []},
            ],
            'uiInfo': {
                'colorIcon': 'Processor_Dev_Identity.png',
                'outputStreamLabels': None,
                'yPos': '387.065875',
                'stageType': 'PROCESSOR',
                'rawSource': None,
                'icon': 'dev.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Dev Identity {}'.format(i),
                'xPos': '1083.1999999999998',
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': ['DevIdentity_1OutputLane1694195672155{}'.format(i)],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchStStage(stage=stage_json))
    return stages


@pytest.fixture(scope="function")
def record_dedup_sdc_stage():
    stages = []
    for i in range(1, NUM_OF_STAGES + 1):
        stage_json = {
            'instanceName': 'RecordDeduplicator_{}'.format(i),
            'library': 'streamsets-datacollector-basic-lib',
            'stageName': 'com_streamsets_pipeline_stage_processor_dedup_DeDupDProcessor',
            'stageVersion': '1',
            'configuration': [
                {'name': 'fieldsToCompare', 'value': []},
                {'name': 'compareFields', 'value': 'ALL_FIELDS'},
                {'name': 'timeWindowSecs', 'value': 0},
                {'name': 'recordCountWindow', 'value': 1000000},
                {'name': 'stageOnRecordError', 'value': 'TO_ERROR'},
                {'name': 'stageRequiredFields', 'value': []},
                {'name': 'stageRecordPreconditions', 'value': []},
            ],
            'uiInfo': {
                'colorIcon': 'Processor_Record_Deduplicator.png',
                'outputStreamLabels': ['Unique Records', 'Duplicate Records'],
                'yPos': '253.065875',
                'stageType': 'PROCESSOR',
                'rawSource': None,
                'icon': 'dedup.png',
                'description': '',
                'inputStreamLabels': None,
                'label': 'Record Deduplicator {}'.format(i),
                'xPos': '1196.1999999999998',
                'displayMode': 'BASIC',
            },
            'inputLanes': [],
            'outputLanes': [
                'RecordDeduplicator_1OutputLane169419698035{}0'.format(i),
                'RecordDeduplicator_1OutputLane169419698035{}1'.format(i),
            ],
            'eventLanes': [],
            'services': [],
        }
        stages.append(SchSdcStage(stage=stage_json))
    return stages


@pytest.mark.parametrize(
    "origin_stage, destination_stage, processor_stage_one, processor_stage_two",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage", "dev_identity_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage", "dev_identity_st_stage"),
    ],
)
def test_copy_inputs_sanity(origin_stage, destination_stage, processor_stage_one, processor_stage_two, request):
    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage_one = request.getfixturevalue(processor_stage_one)[0]
    processor_stage_two = request.getfixturevalue(processor_stage_two)[0]

    origin_stage >> processor_stage_one >> destination_stage
    origin_stage >> processor_stage_two

    destination_stage_input_lanes = destination_stage._data['inputLanes'][:]
    processor_stage_two_input_lanes = processor_stage_two._data['inputLanes'][:]
    assert destination_stage._data['inputLanes'] == destination_stage_input_lanes
    assert processor_stage_two._data['inputLanes'] == processor_stage_two_input_lanes

    processor_stage_two.copy_inputs(destination_stage)
    assert processor_stage_two._data['inputLanes'] == processor_stage_two_input_lanes + destination_stage_input_lanes


@pytest.mark.parametrize(
    "origin_stage,destination_stage,processor_stage_one,processor_stage_two",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage", "dev_identity_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage", "dev_identity_st_stage"),
    ],
)
def test_copy_inputs_override_true(origin_stage, destination_stage, processor_stage_one, processor_stage_two, request):
    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage_one = request.getfixturevalue(processor_stage_one)[0]
    processor_stage_two = request.getfixturevalue(processor_stage_two)[0]

    origin_stage >> processor_stage_one >> destination_stage
    origin_stage >> processor_stage_two

    destination_stage_input_lanes = destination_stage._data['inputLanes'][:]
    processor_stage_two_input_lanes = processor_stage_two._data['inputLanes'][:]
    assert destination_stage._data['inputLanes'] == destination_stage_input_lanes
    assert processor_stage_two._data['inputLanes'] == processor_stage_two_input_lanes

    processor_stage_two.copy_inputs(destination_stage, override=True)
    assert processor_stage_two._data['inputLanes'] == destination_stage_input_lanes


@pytest.mark.parametrize(
    "origin_stage, destination_stage, processor_stage",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage"),
    ],
)
def test_copy_outputs_from_pipeline_stages_sanity(origin_stage, destination_stage, processor_stage, request):
    pipeline = DummyPipeline()

    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage = request.getfixturevalue(processor_stage)[0]

    pipeline.add_stage(origin_stage, destination_stage, processor_stage)

    origin_stage >> destination_stage

    assert origin_stage._data['outputLanes'][0] in destination_stage._data['inputLanes']
    assert processor_stage._data['outputLanes'][0] not in destination_stage._data['inputLanes']

    processor_stage.copy_outputs(origin_stage)
    assert processor_stage._data['outputLanes'][0] in destination_stage._data['inputLanes']
    assert origin_stage._data['outputLanes'][0] in destination_stage._data['inputLanes']


def test_copy_outputs_from_pipeline_stages_invalid_num_output_lanes(
    dev_data_generator_sdc_stage, trash_sdc_stage, delay_sdc_stage, record_dedup_sdc_stage
):
    pipeline = DummyPipeline()

    origin_sdc_stage = dev_data_generator_sdc_stage[0]
    destination_sdc_stage = trash_sdc_stage[0]
    processor_sdc_stage = delay_sdc_stage[0]
    multi_output_lane_processor_sdc_stage = record_dedup_sdc_stage[0]

    pipeline.add_stage(
        origin_sdc_stage, destination_sdc_stage, processor_sdc_stage, multi_output_lane_processor_sdc_stage
    )
    origin_sdc_stage >> processor_sdc_stage >> destination_sdc_stage

    with pytest.raises(ValueError):
        multi_output_lane_processor_sdc_stage.copy_outputs(processor_sdc_stage)


def test_copy_outputs_from_pipeline_stages_multiple_output_lane_stage(
    dev_data_generator_sdc_stage, trash_sdc_stage, delay_sdc_stage, record_dedup_sdc_stage, dummy_pipeline
):
    dev = dev_data_generator_sdc_stage[0]
    trash1 = trash_sdc_stage[0]
    trash2 = trash_sdc_stage[1]
    dedup1 = record_dedup_sdc_stage[0]
    dedup2 = record_dedup_sdc_stage[1]

    dummy_pipeline.add_stage(dev, trash1, trash2, dedup1, dedup2)

    dev >> dedup1 >> trash1
    dedup1 >> trash2

    assert dedup1._data['outputLanes'][0] == trash1._data['inputLanes'][0]
    assert dedup1._data['outputLanes'][1] == trash2._data['inputLanes'][0]

    dedup2.copy_outputs(dedup1)

    assert dedup1._data['outputLanes'][0] == trash1._data['inputLanes'][0]
    assert dedup1._data['outputLanes'][1] == trash2._data['inputLanes'][0]
    assert dedup2._data['outputLanes'][0] == trash1._data['inputLanes'][1]
    assert dedup2._data['outputLanes'][1] == trash2._data['inputLanes'][1]


@pytest.mark.parametrize(
    "origin_stage,destination_stage,processor_stage",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage"),
    ],
)
def test_copy_outputs_from_stages_in_pipeline_builder_sanity(
    origin_stage, destination_stage, processor_stage, dummy_pipeline_builder, request
):
    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage = request.getfixturevalue(processor_stage)[0]

    dummy_pipeline_builder.add_stage(origin_stage, destination_stage, processor_stage)
    origin_stage >> destination_stage

    assert processor_stage._data['outputLanes'][0] not in destination_stage._data['inputLanes']
    processor_stage.copy_outputs(origin_stage)
    assert processor_stage._data['outputLanes'][0] in destination_stage._data['inputLanes']
    assert origin_stage._data['outputLanes'][0] in destination_stage._data['inputLanes']


@pytest.mark.parametrize(
    "origin_stage, destination_stage, processor_stage_one, processor_stage_two",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage", "dev_identity_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage", "dev_identity_st_stage"),
    ],
)
def test_copy_inputs_from_different_stage(
    origin_stage, destination_stage, processor_stage_one, processor_stage_two, request
):
    pipeline = DummyPipeline()
    pipeline2 = DummyPipeline()

    origin_stages = request.getfixturevalue(origin_stage)
    origin_stage, origin_stage_two = origin_stages[0], origin_stages[1]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage_one = request.getfixturevalue(processor_stage_one)[0]
    processor_stage_two = request.getfixturevalue(processor_stage_two)[0]

    pipeline.add_stage(origin_stage, destination_stage, processor_stage_one)
    pipeline2.add_stage(origin_stage_two, processor_stage_two)

    origin_stage >> processor_stage_one >> destination_stage
    origin_stage_two >> processor_stage_two

    with pytest.raises(ValueError):
        processor_stage_two.copy_inputs(destination_stage)


@pytest.mark.parametrize(
    "origin_stage, destination_stage, processor_stage",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage", "delay_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage", "delay_st_stage"),
    ],
)
def test_copy_outputs_from_different_stage(origin_stage, destination_stage, processor_stage, request):
    pipeline = DummyPipeline()
    pipeline2 = DummyPipeline()

    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]
    processor_stage = request.getfixturevalue(processor_stage)[0]

    pipeline.add_stage(origin_stage, destination_stage)
    pipeline2.add_stage(processor_stage)

    origin_stage >> destination_stage

    with pytest.raises(ValueError):
        processor_stage.copy_outputs(origin_stage)


@pytest.mark.parametrize("origin_stage", ["dev_data_generator_sdc_stage", "dev_data_generator_st_stage"])
def test_set_output_lanes(origin_stage, request):
    origin_stage = request.getfixturevalue(origin_stage)[0]

    assert origin_stage.output_lanes
    origin_stage_output_lanes = origin_stage.output_lanes

    # assert that origin_stage.output_lanes did not change
    origin_stage.output_lanes = ['dummy_value']
    assert origin_stage.output_lanes == origin_stage_output_lanes


@pytest.mark.parametrize(
    "origin_stage, destination_stage",
    [
        ("dev_data_generator_sdc_stage", "trash_sdc_stage"),
        ("dev_data_generator_st_stage", "trash_st_stage"),
    ],
)
def test_set_input_lanes(origin_stage, destination_stage, request):
    origin_stage = request.getfixturevalue(origin_stage)[0]
    destination_stage = request.getfixturevalue(destination_stage)[0]

    origin_stage.connect_outputs([destination_stage])

    assert destination_stage.input_lanes
    destination_stage_input_lanes = destination_stage.input_lanes

    # assert that destination_stage.input_lanes did not change
    destination_stage.input_lanes = ['dummy_value']
    assert destination_stage.input_lanes == destination_stage_input_lanes


@pytest.mark.parametrize(
    "dev_data_gen, trash",
    [("dev_data_generator_sdc_stage", "trash_sdc_stage"), ("dev_data_generator_st_stage", "trash_st_stage")],
)
def test_event_lane_sanity(dev_data_gen, trash, request):
    dev_data_gen = request.getfixturevalue(dev_data_gen)[0]
    trashes = request.getfixturevalue(trash)
    trash1, trash2 = trashes[0], trashes[1]

    # assert base case, no event_lanes exist
    assert len(dev_data_gen.event_lanes) == 0
    assert len(trash2.input_lanes) == 0

    dev_data_gen.connect_outputs(stages=[trash1], event_lane=False)
    dev_data_gen.connect_outputs(stages=[trash2], event_lane=True)

    # assert that event lane have been created
    assert len(dev_data_gen.event_lanes) == 1
    assert '_EventLane' in trash2.input_lanes[0]
    assert dev_data_gen.event_lanes == trash2.input_lanes


@pytest.mark.parametrize(
    "dev_data_gen, trash",
    [("dev_data_generator_sdc_stage", "trash_sdc_stage"), ("dev_data_generator_st_stage", "trash_st_stage")],
)
def test_only_one_event_lane_created_for_stage(dev_data_gen, trash, request):
    dev_data_gen = request.getfixturevalue(dev_data_gen)[0]
    trashes = request.getfixturevalue(trash)
    trash1, trash2, trash3 = trashes[0], trashes[1], trashes[2]

    # assert base case, no event_lanes exist
    assert len(dev_data_gen.event_lanes) == 0
    assert len(trash2.input_lanes) == 0
    assert len(trash3.input_lanes) == 0

    dev_data_gen.connect_outputs(stages=[trash1], event_lane=False)
    dev_data_gen.connect_outputs(stages=[trash2], event_lane=True)
    dev_data_gen.connect_outputs(stages=[trash3], event_lane=True)

    # assert that only one event lanes has been created
    assert len(dev_data_gen.event_lanes) == 1
    assert '_EventLane' in dev_data_gen.event_lanes[0]
    assert dev_data_gen.event_lanes == trash2.input_lanes
    assert dev_data_gen.event_lanes == trash3.input_lanes


def test_use_connection_sanity(mocker):
    mock_control_hub = mocker.Mock()
    stage_json = {
        'instanceName': 'foo',
        'library': 'streamsets-datacollector-foo-lib',
        'stageName': 'com_streamsets_foo_stage',
        'stageVersion': '2',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'eventLanes': [],
        'services': [],
        'uiInfo': {
            'colorIcon': 'Origin_Foo_Generator.png',
            'stageType': 'SOURCE',
        },
    }

    connection = Connection(
        connection={
            'connection': 'foo',
            'connectionType': 'bar',
            'id': 1,
            'connectionDefinition': '{"configuration": [{"name": "foo", "value": "bar"}]}',
        },
        control_hub=mock_control_hub,
    )
    stage_instance = type(
        "DummyStage",
        (SchSdcStage,),
        {'_attributes': {'connection': [StageConfigurationProperty(config_name='connection')]}},
    )

    stage = stage_instance(stage=stage_json, supported_connection_types=['bar'])

    assert stage.configuration['connection'] == 'MANUAL'
    assert stage.connection == 'MANUAL'

    stage.use_connection(connection)
    assert stage.connection == 1


def test_use_connection_unsupported_stage_type(mocker):
    mock_control_hub = mocker.Mock()
    stage_json = {
        'instanceName': 'foo',
        'library': 'streamsets-datacollector-foo-lib',
        'stageName': 'com_streamsets_foo_stage',
        'stageVersion': '2',
        'configuration': [],
        'inputLanes': [],
        'outputLanes': [],
        'eventLanes': [],
        'services': [],
        'uiInfo': {
            'colorIcon': 'Origin_Foo_Generator.png',
            'stageType': 'SOURCE',
        },
    }

    connection = Connection(
        connection={
            'connection': 'foo',
            'connectionType': 'bar',
            'id': 1,
            'connectionDefinition': '{"configuration": [{"name": "foo", "value": "bar"}]}',
        },
        control_hub=mock_control_hub,
    )
    stage = SchSdcStage(stage=stage_json)

    assert 'connection' not in stage.configuration
    assert not hasattr(stage, 'connection')

    with pytest.raises(ValueError):
        stage.use_connection(connection)


def test_use_connection_unsupported_connection_type(mocker):
    mock_control_hub = mocker.Mock()
    stage_json = {
        'instanceName': 'foo',
        'library': 'streamsets-datacollector-foo-lib',
        'stageName': 'com_streamsets_foo_stage',
        'stageVersion': '2',
        'configuration': [{'name': 'connection', 'value': 'MANUAL'}],
        'inputLanes': [],
        'outputLanes': [],
        'eventLanes': [],
        'services': [],
        'uiInfo': {
            'colorIcon': 'Origin_Foo_Generator.png',
            'stageType': 'SOURCE',
        },
    }

    connection = Connection(
        connection={
            'connection': 'foo',
            'connectionType': 'foo',
            'id': 1,
            'connectionDefinition': '{"configuration": [{"name": "foo", "value": "bar"}]}',
        },
        control_hub=mock_control_hub,
    )
    stage_instance = type(
        "DummyStage",
        (SchSdcStage,),
        {'_attributes': {'connection': [StageConfigurationProperty(config_name='connection')]}},
    )

    stage = stage_instance(stage=stage_json, supported_connection_types=['bar'])

    assert stage.configuration['connection'] == 'MANUAL'
    assert stage.connection == 'MANUAL'
    assert connection.connection_type not in stage.supported_connection_types

    with pytest.raises(ValueError):
        stage.use_connection(connection)
