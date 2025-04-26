# Copyright 2023 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.utils import get_random_string

# fmt: on

NUM_PIPELINES = 12


@pytest.fixture(scope="module")
def sample_pipelines(sch, sch_authoring_sdc_id):
    """A set of trivial pipelines:

    dev_data_generator >> trash
    """
    pipelines = []

    for i in range(NUM_PIPELINES):
        pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

        dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
        trash = pipeline_builder.add_stage('Trash')
        dev_data_generator >> trash

        pipeline_name = 'pipeline_stage_test_{}_{}'.format(i, get_random_string())
        pipeline = pipeline_builder.build(pipeline_name)
        sch.publish_pipeline(pipeline)

        pipelines.append(pipeline)

    try:
        yield pipelines
    finally:
        for pipeline in pipelines:
            sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def sample_pipeline(sch, sch_authoring_sdc_id):
    """A trivial pipelines:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def sample_fragment(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(
        engine_type='data_collector', engine_id=sch_authoring_sdc_id, fragment=True
    )
    dev = pipeline_builder.add_stage('Dev Data Generator')
    evaluator = pipeline_builder.add_stage('Expression Evaluator')

    dev >> evaluator
    fragment = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))

    sch.publish_pipeline(fragment)

    try:
        yield fragment
    finally:
        sch.delete_pipeline(fragment)


@pytest.fixture(scope='module', params=['data_collector', 'transformer', 'snowflake'])
def engine_type(request):
    yield request.param


@pytest.fixture(scope='function')
def pipeline_builder(request, sch, engine_type):
    engine_args = {
        'data_collector': 'sch_authoring_sdc_id',
        'transformer': 'sch_authoring_transformer_id',
        'snowflake': None,
    }
    engine_id_arg = engine_args[engine_type]
    if engine_id_arg:
        extra_args = {'engine_id': request.getfixturevalue(engine_id_arg)}
    else:
        extra_args = {}

    pipeline_builder = sch.get_pipeline_builder(engine_type, **extra_args)

    yield pipeline_builder


# SDC Tests for stage lanes
def test_output_lanes_created_on_instantiation(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')

    assert len(dev_data_generator.output_lanes) == dev_data_generator.output_streams
    assert len(data_parser.output_lanes) == data_parser.output_streams


def test_output_lanes_not_created_for_0_output_stream_stages(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    trash = pipeline_builder.add_stage('Trash')

    assert len(trash.output_lanes) == 0


def test_output_lanes_not_created_on_stage_connection(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    assert len(dev_data_generator.output_lanes) == dev_data_generator.output_streams
    assert len(data_parser.output_lanes) == data_parser.output_streams
    assert len(data_parser.input_lanes) == 0
    assert len(trash.input_lanes) == 0

    dev_data_generator_output_lanes = len(dev_data_generator.output_lanes)
    data_parser_output_lanes = len(data_parser.output_lanes)

    dev_data_generator >> data_parser
    data_parser >> trash

    assert len(dev_data_generator.output_lanes) == dev_data_generator_output_lanes
    assert len(data_parser.output_lanes) == data_parser_output_lanes
    assert len(data_parser.input_lanes) == 1
    assert len(trash.input_lanes) == 1


def test_add_event_lane_to_stage_with_no_output_lanes(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    s3 = pipeline_builder.add_stage('Amazon S3', type='destination')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> s3
    s3 >= trash

    # asset that s3 has no output_lanes
    assert len(s3.output_lanes) == 0

    # assert that added input_lane was an event lane
    assert len(trash.input_lanes) == 1
    assert s3.instance_name + '_EventLane' == trash.input_lanes[0]

    # publish and make sure the connection still exists
    pipeline = pipeline_builder.build('TEST {}'.format(get_random_string()))

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)
        stages = pipeline.stages

        s3, trash = stages[1], stages[2]

        # assert that event lane still exists
        assert len(s3.output_lanes) == 0
        assert len(trash.input_lanes) == 1
        assert s3.instance_name + '_EventLane' == trash.input_lanes[0]

    except Exception as e:
        raise e

    finally:
        sch.delete_pipeline(pipeline)


def test_input_output_lanes_names_match_appropriate_instance_names(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash
    pipeline = pipeline_builder.build('simple pipeline')

    dev_data_generator, data_parser, trash = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]

    assert len(dev_data_generator.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    assert dev_data_generator.output_lanes[0].split('OutputLane')[0] == dev_data_generator.instance_name
    assert data_parser.input_lanes[0].split('OutputLane')[0] == dev_data_generator.instance_name
    assert data_parser.output_lanes[0].split('OutputLane')[0] == data_parser.instance_name
    assert trash.input_lanes[0].split('OutputLane')[0] == data_parser.instance_name


def test_connect_stages_with_multiple_output_streams(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    tail = pipeline_builder.add_stage('File Tail')
    t1 = pipeline_builder.add_stage('Trash')
    t2 = pipeline_builder.add_stage('Trash')
    t3 = pipeline_builder.add_stage('Trash')
    t4 = pipeline_builder.add_stage('Trash')

    tail >> t1
    tail >> t2
    tail >> t3
    tail >> t4
    pipeline = pipeline_builder.build('simple pipeline')

    tail, t1, t2, t3, t4 = (
        pipeline.stages[0],
        pipeline.stages[1],
        pipeline.stages[2],
        pipeline.stages[3],
        pipeline.stages[4],
    )

    # Assert input/output lanes are as expected
    assert len(tail.output_lanes) == 2
    assert len(t1.input_lanes) == 1
    assert len(t2.input_lanes) == 1
    assert len(t3.input_lanes) == 1
    assert len(t4.input_lanes) == 1

    # Assert that the first trash stage was given the first output lane, and all other trash stages were given the
    # second
    assert tail.output_lanes[0] == t1.input_lanes[0]
    assert tail.output_lanes[1] == t2.input_lanes[0]
    assert tail.output_lanes[1] == t3.input_lanes[0]
    assert tail.output_lanes[1] == t4.input_lanes[0]
    assert (
        tail.output_lanes[1] not in t1.input_lanes
        and tail.output_lanes[0] not in t2.input_lanes
        and tail.output_lanes[0] not in t3.input_lanes
        and tail.output_lanes[0] not in t4.input_lanes
    )


def test_connect_multiple_stages_at_once_with_stage_with_multiple_output_streams(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    tail = pipeline_builder.add_stage('File Tail')
    t1 = pipeline_builder.add_stage('Trash')
    t2 = pipeline_builder.add_stage('Trash')
    t3 = pipeline_builder.add_stage('Trash')
    t4 = pipeline_builder.add_stage('Trash')

    tail >> [t1, t2, t3, t4]
    pipeline = pipeline_builder.build('simple pipeline')

    tail, t1, t2, t3, t4 = (
        pipeline.stages[0],
        pipeline.stages[1],
        pipeline.stages[2],
        pipeline.stages[3],
        pipeline.stages[4],
    )

    # Assert input/output lanes are as expected
    assert len(tail.output_lanes) == 2
    assert len(t1.input_lanes) == 1
    assert len(t2.input_lanes) == 1
    assert len(t3.input_lanes) == 1
    assert len(t4.input_lanes) == 1

    # Assert that the all trash stages were assigned the same output lane
    assert tail.output_lanes[0] == t1.input_lanes[0]
    assert tail.output_lanes[0] == t2.input_lanes[0]
    assert tail.output_lanes[0] == t3.input_lanes[0]
    assert tail.output_lanes[0] == t4.input_lanes[0]
    assert (
        tail.output_lanes[1] not in t1.input_lanes
        and tail.output_lanes[1] not in t2.input_lanes
        and tail.output_lanes[1] not in t3.input_lanes
        and tail.output_lanes[1] not in t4.input_lanes
    )


def test_manipulate_output_streams(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    tail = pipeline_builder.add_stage('File Tail')

    tail_output_lanes = tail.output_lanes
    tail.output_lanes = ['DUMMY_OUTPUT_LANE']

    # assert that output_lanes have not been changed
    assert tail.output_lanes != ['DUMMY_OUTPUT_LANE']
    assert tail.output_lanes == tail_output_lanes


def test_disconnect_inputs(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> trash
    data_parser >> trash
    jdbc_multitable_consumer >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    dev_data_gen, data_parser, jdbc_multitable_consumer = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(jdbc_multitable_consumer.output_lanes) == 1

    # assert that only input lanes have been changed appropriately after disconnect_inputs is called
    trash.disconnect_input_lanes([dev_data_gen, data_parser])
    assert len(trash.input_lanes) == 1
    assert len(jdbc_multitable_consumer.output_lanes) == 1
    assert trash.input_lanes[0] == jdbc_multitable_consumer.output_lanes[0]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.output_lanes) == 1


def test_disconnect_all_inputs_in_pipeline_builder(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> trash
    data_parser >> trash
    jdbc_multitable_consumer >> trash

    # assert that the input/output lanes of all stages are accurate
    assert len(trash._data['inputLanes']) == 3

    assert len(dev_data_generator._data['outputLanes']) == 1
    assert len(data_parser._data['outputLanes']) == 1
    assert len(jdbc_multitable_consumer._data['outputLanes']) == 1

    # assert that only input lanes have been changed after disconnect_inputs is called with all_stages set to True
    trash.disconnect_input_lanes(all_stages=True)
    assert len(trash._data['inputLanes']) == 0
    assert len(dev_data_generator._data['outputLanes']) == 1
    assert len(data_parser._data['outputLanes']) == 1
    assert len(jdbc_multitable_consumer._data['outputLanes']) == 1


def test_disconnect_all_inputs(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> trash
    data_parser >> trash
    jdbc_multitable_consumer >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    dev_data_gen, data_parser, jdbc_multitable_consumer = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(jdbc_multitable_consumer.output_lanes) == 1

    # assert that only input lanes have been changed after disconnect_inputs is called with all_stages set to True
    trash.disconnect_input_lanes(all_stages=True)
    assert len(trash.input_lanes) == 0
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(jdbc_multitable_consumer.output_lanes) == 1


def test_disconnect_inputs_with_incorrect_stage_type(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> trash
    data_parser >> trash
    jdbc_multitable_consumer >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    dev_data_gen, data_parser, jdbc_multitable_consumer = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(jdbc_multitable_consumer.output_lanes) == 1

    # assert that error is raised
    with pytest.raises(AttributeError):
        trash.disconnect_input_lanes(['STRING TYPE THAT IS CLEARLY AN INVALID TYPE'])


def test_disconnect_inputs_with_stage_that_doesnt_exist(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    data_parser >> trash

    pipeline1 = pipeline_builder.build('simple pipeline')

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    pipeline_builder.build('simple pipeline 2')

    # assert that the input/output lanes of all stages are accurate
    dev_data_gen, data_parser, trash = pipeline1.stages[0], pipeline1.stages[1], pipeline1.stages[2]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that nothing has changed
    dev_data_gen.disconnect_input_lanes([data_parser])
    data_parser.disconnect_input_lanes([trash])
    trash.disconnect_input_lanes([jdbc_multitable_consumer])
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1


def test_disconnect_outputs_in_pipeline_builder(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    dev_data_gen >> jdbc_multitable_consumer
    dev_data_gen >> trash

    assert len(dev_data_gen._data['outputLanes']) == 1
    assert len(data_parser._data['inputLanes']) == 1
    assert len(jdbc_multitable_consumer._data['inputLanes']) == 1
    assert len(trash._data['inputLanes']) == 1

    # assert that only input lanes have been changed appropriately after disconnect_outputs is called
    dev_data_gen.disconnect_output_lanes([data_parser, jdbc_multitable_consumer])

    assert len(dev_data_gen._data['outputLanes']) == 1
    assert len(trash._data['inputLanes']) == 1

    assert len(data_parser._data['inputLanes']) == 0
    assert len(jdbc_multitable_consumer._data['inputLanes']) == 0


def test_disconnect_outputs(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    dev_data_gen >> jdbc_multitable_consumer
    dev_data_gen >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    dev_data_gen = pipeline.stages[0]
    assert dev_data_gen.instance_name == 'DevDataGenerator_01'
    assert len(dev_data_gen.output_lanes) == 1

    data_parser, jdbc_multitable_consumer, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(data_parser.input_lanes) == 1
    assert len(jdbc_multitable_consumer.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that only input lanes have been changed appropriately after disconnect_outputs is called
    dev_data_gen.disconnect_output_lanes([data_parser, jdbc_multitable_consumer])

    assert len(dev_data_gen.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    assert len(data_parser.input_lanes) == 0
    assert len(jdbc_multitable_consumer.input_lanes) == 0


def test_disconnect_all_outputs(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    dev_data_gen >> jdbc_multitable_consumer
    dev_data_gen >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    dev_data_gen = pipeline.stages[0]
    assert dev_data_gen.instance_name == 'DevDataGenerator_01'
    assert len(dev_data_gen.output_lanes) == 1

    data_parser, jdbc_multitable_consumer, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(data_parser.input_lanes) == 1
    assert len(jdbc_multitable_consumer.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    dev_data_gen.disconnect_output_lanes(all_stages=True)

    # assert that only input lanes have been changed appropriately after disconnect_outputs is called
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.input_lanes) == 0
    assert len(jdbc_multitable_consumer.input_lanes) == 0
    assert len(trash.input_lanes) == 0


def test_disconnect_outputs_with_incorrect_stage_type(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    dev_data_gen >> jdbc_multitable_consumer
    dev_data_gen >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    dev_data_gen = pipeline.stages[0]
    assert dev_data_gen.instance_name == 'DevDataGenerator_01'
    assert len(dev_data_gen.output_lanes) == 1

    data_parser, jdbc_multitable_consumer, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(data_parser.input_lanes) == 1
    assert len(jdbc_multitable_consumer.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that error is raised
    with pytest.raises(AttributeError):
        trash.disconnect_output_lanes(['STRING TYPE THAT IS CLEARLY AN INVALID TYPE'])


def test_disconnect_outputs_with_stage_that_doesnt_exist(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_gen = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_gen >> data_parser
    data_parser >> trash

    pipeline1 = pipeline_builder.build('simple pipeline')

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    jdbc_multitable_consumer = pipeline_builder.add_stage('JDBC Multitable Consumer')
    pipeline_builder.build('simple pipeline 2')

    # assert that the input/output lanes of all stages are accurate
    dev_data_gen, data_parser, trash = pipeline1.stages[0], pipeline1.stages[1], pipeline1.stages[2]
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that nothing has changed
    dev_data_gen.disconnect_output_lanes([trash])
    data_parser.disconnect_output_lanes([jdbc_multitable_consumer])
    trash.disconnect_output_lanes([dev_data_gen])
    assert len(dev_data_gen.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1


# SDC Tests for removing stage from Pipeline
def test_remove_stage_from_pipeline_object(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    stage_names = {stage.stage_name for stage in pipeline.stages}
    assert len(stage_names) == 3
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name in stage_names
    assert trash.stage_name in stage_names

    assert len(dev_data_generator.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # remove stage
    pipeline.remove_stages(pipeline.stages[1])

    # assert stage has been removed
    stage_names = {stage.stage_name for stage in pipeline.stages}
    assert len(stage_names) == 2
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name not in stage_names

    assert trash.stage_name in stage_names

    # assert only input_lanes have been removed
    assert len(pipeline.stages[0].output_lanes) == 1
    assert len(pipeline.stages[1].input_lanes) == 0


def test_pass_incorrect_type_into_remove_stages(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    with pytest.raises(AttributeError):
        pipeline.remove_stages('STRING THAT SHOULD RESULT IN ERROR')


def test_pass_stage_that_doesnt_exist_into_remove_stages(sch, sch_authoring_sdc_id):
    # Build pipeline1
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash

    pipeline1 = pipeline_builder.build('simple pipeline 1')

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.add_stage('JDBC Multitable Consumer')
    pipeline_builder.add_stage('Dev Data Generator')
    pipeline2 = pipeline_builder.build('simple pipeline 2')

    with pytest.raises(ValueError):
        pipeline1.remove_stages(pipeline2.stages[0])

    with pytest.raises(ValueError):
        pipeline1.remove_stages(pipeline2.stages[1])

    # Nothing should change within pipeline1
    stage_names = {stage.stage_name for stage in pipeline1.stages}
    assert len(stage_names) == 3
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name in stage_names
    assert trash.stage_name in stage_names


def test_remove_stage_from_pipeline_builder(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 3
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name in stage_names
    assert trash.stage_name in stage_names

    # remove stage
    pipeline_builder.remove_stage(data_parser)

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 2
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name not in stage_names
    assert trash.stage_name in stage_names


def test_remove_connected_stages_from_pipeline_builder(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    # connect stages
    dev_data_generator >> data_parser
    data_parser >> trash

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 3
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name in stage_names
    assert trash.stage_name in stage_names
    assert len(dev_data_generator.output_lanes) == 1
    assert len(data_parser.input_lanes) == 1
    assert len(data_parser.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # remove stage
    pipeline_builder.remove_stage(data_parser)

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 2
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name not in stage_names
    assert trash.stage_name in stage_names

    # assert only input_lanes have been removed
    assert len(dev_data_generator.output_lanes) == 1
    assert len(trash.input_lanes) == 0


def test_remove_stage_from_pipeline_builder_that_doesnt_exist(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 3
    assert dev_data_generator.stage_name in stage_names
    assert data_parser.stage_name in stage_names
    assert trash.stage_name in stage_names

    # remove stage
    with pytest.raises(Exception):
        pipeline_builder.remove_stages('STAGE THAT SHOULD RESULT IN ERROR')


# Transformer Tests for stage lanes
def test_input_output_lanes_property_values_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    aggregate, join, trash = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]

    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    assert aggregate.output_lanes[0].split('OutputLane')[0] == aggregate.instance_name
    assert join.input_lanes[0].split('OutputLane')[0] == aggregate.instance_name
    assert join.output_lanes[0].split('OutputLane')[0] == join.instance_name
    assert trash.input_lanes[0].split('OutputLane')[0] == join.instance_name


def test_disconnect_inputs_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> trash
    join >> trash
    dev_random >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    aggregate, join, dev_random = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(aggregate.output_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(dev_random.output_lanes) == 1

    # assert that the input/output lanes have been changed appropriately after disconnect_inputs is called
    trash.disconnect_input_lanes([aggregate, join])
    assert len(trash.input_lanes) == 1
    assert len(dev_random.output_lanes) == 1
    assert trash.input_lanes[0] == dev_random.output_lanes[0]
    assert len(aggregate.output_lanes) == 1
    assert len(join.output_lanes) == 1


def test_disconnect_all_inputs_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> trash
    join >> trash
    dev_random >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    aggregate, join, dev_random = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(aggregate.output_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(dev_random.output_lanes) == 1

    # assert that the input/output lanes have been changed after disconnect_inputs is called with all_stages set to True
    trash.disconnect_input_lanes(all_stages=True)
    assert len(trash.input_lanes) == 0
    assert len(aggregate.output_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(dev_random.output_lanes) == 1


def test_disconnect_inputs_with_incorrect_stage_type_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> trash
    join >> trash
    dev_random >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    trash = pipeline.stages[-1]
    assert trash.instance_name == 'Trash_01'
    assert len(trash.input_lanes) == 3

    aggregate, join, dev_random = pipeline.stages[0], pipeline.stages[1], pipeline.stages[2]
    assert len(aggregate.output_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(dev_random.output_lanes) == 1

    # assert that error is raised
    with pytest.raises(AttributeError):
        trash.disconnect_input_lanes(['STRING TYPE THAT IS CLEARLY AN INVALID TYPE'])


def test_disconnect_inputs_with_stage_that_doesnt_exist_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline1 = pipeline_builder.build('simple pipeline')

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    dev_random = pipeline_builder.add_stage('Dev Random')
    pipeline_builder.build('simple pipeline 2')

    # assert that the input/output lanes of all stages are accurate
    aggregate, join, trash = pipeline1.stages[0], pipeline1.stages[1], pipeline1.stages[2]
    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that nothing has changed
    aggregate.disconnect_input_lanes([join])
    join.disconnect_input_lanes([trash])
    trash.disconnect_input_lanes([dev_random])
    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1


def test_disconnect_outputs_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    aggregate >> dev_random
    aggregate >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    aggregate = pipeline.stages[0]
    assert len(aggregate.output_lanes) == 1

    join, dev_random, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(join.input_lanes) == 1
    assert len(dev_random.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that the input lanes have been changed appropriately after disconnect_outputs is called
    aggregate.disconnect_output_lanes([join, dev_random])

    assert len(aggregate.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    assert len(join.input_lanes) == 0
    assert len(dev_random.input_lanes) == 0


def test_disconnect_all_outputs_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    aggregate >> dev_random
    aggregate >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    aggregate = pipeline.stages[0]
    assert len(aggregate.output_lanes) == 1

    join, dev_random, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(join.input_lanes) == 1
    assert len(dev_random.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    aggregate.disconnect_output_lanes(all_stages=True)
    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 0
    assert len(dev_random.input_lanes) == 0
    assert len(trash.input_lanes) == 0


def test_disconnect_outputs_with_incorrect_stage_type_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    aggregate >> dev_random
    aggregate >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    # assert that the input/output lanes of all stages are accurate
    aggregate = pipeline.stages[0]
    assert len(aggregate.output_lanes) == 1

    join, dev_random, trash = pipeline.stages[1], pipeline.stages[2], pipeline.stages[3]
    assert len(join.input_lanes) == 1
    assert len(dev_random.input_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that error is raised
    with pytest.raises(AttributeError):
        trash.disconnect_output_lanes(['STRING TYPE THAT IS CLEARLY AN INVALID TYPE'])


def test_disconnect_outputs_with_stage_that_doesnt_exist_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline1 = pipeline_builder.build('simple pipeline')

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    dev_random = pipeline_builder.add_stage('Dev Random')
    pipeline_builder.build('simple pipeline 2')

    # assert that the input/output lanes of all stages are accurate
    aggregate, join, trash = pipeline1.stages[0], pipeline1.stages[1], pipeline1.stages[2]
    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # assert that nothing has changed
    aggregate.disconnect_output_lanes([trash])
    join.disconnect_output_lanes([dev_random])
    trash.disconnect_output_lanes([aggregate])
    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1


# Transformer Tests for removing stage from Pipeline
def test_remove_stage_from_pipeline_object_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    stage_names = {stage.stage_name for stage in pipeline.stages}
    assert len(stage_names) == 3
    assert aggregate.stage_name in stage_names
    assert join.stage_name in stage_names
    assert trash.stage_name in stage_names

    assert len(aggregate.output_lanes) == 1
    assert len(join.input_lanes) == 1
    assert len(join.output_lanes) == 1
    assert len(trash.input_lanes) == 1

    # remove stage
    pipeline.remove_stages(pipeline.stages[1])

    # assert stage has been removed
    stage_names = {stage.stage_name for stage in pipeline.stages}
    assert len(stage_names) == 2
    assert aggregate.stage_name in stage_names
    assert join.stage_name not in stage_names
    assert trash.stage_name in stage_names

    # assert lanes have been removed
    assert len(pipeline.stages[0].output_lanes) == 1
    assert len(pipeline.stages[1].input_lanes) == 0


def test_pass_incorrect_type_into_remove_stages_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline = pipeline_builder.build('simple pipeline')

    with pytest.raises(AttributeError):
        pipeline.remove_stages('STRING THAT SHOULD RESULT IN ERROR')


def test_pass_stage_that_doesnt_exist_into_remove_stages_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline1
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    aggregate >> join
    join >> trash

    pipeline1 = pipeline_builder.build('simple pipeline 1')

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    pipeline_builder.add_stage('Dev Random')
    pipeline_builder.add_stage('Join')
    pipeline2 = pipeline_builder.build('simple pipeline 2')

    with pytest.raises(ValueError):
        pipeline1.remove_stages(pipeline2.stages[0])

    with pytest.raises(ValueError):
        pipeline1.remove_stages(pipeline2.stages[1])

    # Nothing should change within pipeline1
    stage_names = {stage.stage_name for stage in pipeline1.stages}
    assert len(stage_names) == 3
    assert aggregate.stage_name in stage_names
    assert join.stage_name in stage_names
    assert trash.stage_name in stage_names


def test_remove_stage_from_pipeline_builder_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 3
    assert aggregate.stage_name in stage_names
    assert join.stage_name in stage_names
    assert trash.stage_name in stage_names

    # remove stage
    pipeline_builder.remove_stage(join)

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 2
    assert aggregate.stage_name in stage_names
    assert join.stage_name not in stage_names
    assert trash.stage_name in stage_names


def test_remove_stage_from_pipeline_builder_that_doesnt_exist_transformer(sch, sch_authoring_transformer_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)

    aggregate = pipeline_builder.add_stage('Aggregate')
    join = pipeline_builder.add_stage('Join')
    trash = pipeline_builder.add_stage('Trash')

    stage_names = {stage['stageName'] for stage in pipeline_builder._pipeline[pipeline_builder._config_key]['stages']}
    assert len(stage_names) == 3
    assert aggregate.stage_name in stage_names
    assert join.stage_name in stage_names
    assert trash.stage_name in stage_names

    # remove stage
    with pytest.raises(Exception):
        pipeline_builder.remove_stages('STAGE THAT SHOULD RESULT IN ERROR')


def test_connect_outputs_to_multi_lane_fixed_stage(sch, sch_authoring_sdc_id):
    # Building a new pipeline since we need to test the construction of one as part of this test case
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source').set_attributes(
        data_format='JSON', raw_data='12345', stop_after_first_batch=True
    )
    deduplicator = pipeline_builder.add_stage('Record Deduplicator')
    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')
    trash3 = pipeline_builder.add_stage('Trash')
    publish_response = None
    try:
        # Intentionally avoid specifying an index value to make sure the default case works as expected
        dev_raw_data_source.connect_outputs([deduplicator])
        deduplicator.connect_outputs(stages=[trash1, trash2], output_lane_index=0)
        deduplicator.connect_outputs(stages=[trash3], output_lane_index=1)
        assert dev_raw_data_source.output_lanes == deduplicator.input_lanes
        assert trash1.input_lanes == trash2.input_lanes
        assert not (trash1.input_lanes == trash3.input_lanes or trash2.input_lanes == trash3.input_lanes)
        assert (
            trash1.input_lanes[0] in deduplicator.output_lanes
            and trash2.input_lanes[0] in deduplicator.output_lanes
            and trash3.input_lanes[0] in deduplicator.output_lanes
        )
        pipeline = pipeline_builder.build(title='connect-outputs-multi-lane-test{}'.format(get_random_string()))
        publish_response = sch.publish_pipeline(pipeline)

        # Retrieve the pipeline again and validate the same changes are seen after pushing to SCH
        pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id)
        dev_raw_data_source = pipeline.stages.get(instance_name='DevRawDataSource_01')
        deduplicator = pipeline.stages.get(instance_name='RecordDeduplicator_01')
        trash1 = pipeline.stages.get(instance_name='Trash_01')
        trash2 = pipeline.stages.get(instance_name='Trash_02')
        trash3 = pipeline.stages.get(instance_name='Trash_03')
        assert dev_raw_data_source.output_lanes == deduplicator.input_lanes
        assert trash1.input_lanes == trash2.input_lanes
        assert not (trash1.input_lanes == trash3.input_lanes or trash2.input_lanes == trash3.input_lanes)
        assert (
            trash1.input_lanes[0] in deduplicator.output_lanes
            and trash2.input_lanes[0] in deduplicator.output_lanes
            and trash3.input_lanes[0] in deduplicator.output_lanes
        )
    finally:
        if publish_response:
            sch.delete_pipeline(pipeline)


def test_connect_inputs_to_multi_lane_fixed_stage(sch, sch_authoring_sdc_id):
    # Building a new pipeline since we need to test the construction of one as part of this test case
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source').set_attributes(
        data_format='JSON', raw_data='12345', stop_after_first_batch=True
    )
    deduplicator = pipeline_builder.add_stage('Record Deduplicator')
    field_flattener = pipeline_builder.add_stage('Field Flattener')
    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')
    trash3 = pipeline_builder.add_stage('Trash')
    publish_response = None
    try:
        # Intentionally avoid specifying an index value to make sure the default case works as expected
        deduplicator.connect_inputs([dev_raw_data_source])
        field_flattener.connect_inputs([dev_raw_data_source], target_stage_output_lane_index=0)
        trash1.connect_inputs(stages=[deduplicator, field_flattener], target_stage_output_lane_index=0)
        trash2.connect_inputs(stages=[deduplicator])
        trash3.connect_inputs(stages=[deduplicator], target_stage_output_lane_index=1)
        assert (
            dev_raw_data_source.output_lanes == deduplicator.input_lanes
            and dev_raw_data_source.output_lanes == field_flattener.input_lanes
        )
        assert trash2.input_lanes[0] in trash1.input_lanes
        assert (
            field_flattener.output_lanes[0] in trash1.input_lanes and deduplicator.output_lanes[0] in trash1.input_lanes
        )
        assert not (trash3.input_lanes[0] in trash1.input_lanes or trash2.input_lanes == trash3.input_lanes)
        assert trash2.input_lanes[0] in deduplicator.output_lanes and trash3.input_lanes[0] in deduplicator.output_lanes
        assert field_flattener.input_lanes == dev_raw_data_source.output_lanes
        pipeline = pipeline_builder.build(title='connect-inputs-multi-lane-test{}'.format(get_random_string()))
        publish_response = sch.publish_pipeline(pipeline)

        # Retrieve the pipeline again and validate the same changes are seen after pushing to SCH
        pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id)
        dev_raw_data_source = pipeline.stages.get(instance_name='DevRawDataSource_01')
        deduplicator = pipeline.stages.get(instance_name='RecordDeduplicator_01')
        field_flattener = pipeline.stages.get(instance_name='FieldFlattener_01')
        trash1 = pipeline.stages.get(instance_name='Trash_01')
        trash2 = pipeline.stages.get(instance_name='Trash_02')
        trash3 = pipeline.stages.get(instance_name='Trash_03')
        assert (
            dev_raw_data_source.output_lanes == deduplicator.input_lanes
            and dev_raw_data_source.output_lanes == field_flattener.input_lanes
        )
        assert trash2.input_lanes[0] in trash1.input_lanes
        assert (
            field_flattener.output_lanes[0] in trash1.input_lanes and deduplicator.output_lanes[0] in trash1.input_lanes
        )
        assert not (trash3.input_lanes[0] in trash1.input_lanes or trash2.input_lanes == trash3.input_lanes)
        assert trash2.input_lanes[0] in deduplicator.output_lanes and trash3.input_lanes[0] in deduplicator.output_lanes
        assert field_flattener.input_lanes == dev_raw_data_source.output_lanes
    finally:
        if publish_response:
            sch.delete_pipeline(pipeline)


def test_connect_via_legacy_rshift_operator(sch, sch_authoring_sdc_id):
    # Building a new pipeline since we need to test the construction of one as part of this test case
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source').set_attributes(
        data_format='JSON', raw_data='12345', stop_after_first_batch=True
    )
    deduplicator = pipeline_builder.add_stage('Record Deduplicator')
    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')
    trash3 = pipeline_builder.add_stage('Trash')
    publish_response = None
    try:
        dev_raw_data_source >> deduplicator >> [trash1, trash2]
        deduplicator >> trash3
        assert dev_raw_data_source.output_lanes == deduplicator.input_lanes
        assert trash1.input_lanes[0] == trash2.input_lanes[0] == deduplicator.output_lanes[0]
        assert trash3.input_lanes[0] == deduplicator.output_lanes[1]
        pipeline = pipeline_builder.build(title='connect-legacy-multi-lane-test{}'.format(get_random_string()))
        publish_response = sch.publish_pipeline(pipeline)

        # Retrieve the pipeline again and validate the same changes are seen after pushing to SCH
        pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id)
        dev_raw_data_source = pipeline.stages.get(instance_name='DevRawDataSource_01')
        deduplicator = pipeline.stages.get(instance_name='RecordDeduplicator_01')
        trash1 = pipeline.stages.get(instance_name='Trash_01')
        trash2 = pipeline.stages.get(instance_name='Trash_02')
        trash3 = pipeline.stages.get(instance_name='Trash_03')
        assert dev_raw_data_source.output_lanes == deduplicator.input_lanes
        assert trash1.input_lanes[0] == trash2.input_lanes[0] == deduplicator.output_lanes[0]
        assert trash3.input_lanes[0] == deduplicator.output_lanes[1]
    finally:
        if publish_response:
            sch.delete_pipeline(pipeline)


@pytest.mark.selector
def test_stream_selector_with_different_initial_value_format(pipeline_builder):
    selector = pipeline_builder.add_stage('Stream Selector')

    assert len(selector.output_lanes) == 1
    assert selector.condition[0].get('predicate', None) == 'default'
    assert all([s.get('outputLane', False) for s in selector.condition])

    predicate = '>=0'
    selector.condition = [predicate]
    assert len(selector.output_lanes) == 2
    assert selector.condition[0].get('predicate', None) == predicate
    assert selector.condition[1].get('predicate', None) == 'default'
    assert all([s.get('outputLane', False) for s in selector.condition])
    assert selector.output_streams == len(selector.output_lanes)

    selector.condition = [{'predicate': predicate}]
    assert len(selector.output_lanes) == 2
    assert selector.condition[0].get('predicate', None) == predicate
    assert selector.condition[1].get('predicate', None) == 'default'
    assert all([s.get('outputLane', False) for s in selector.condition])
    assert selector.output_streams == len(selector.output_lanes)

    selector.condition = [{'predicate': predicate, 'outputLane': 'this'}, {'predicate': 'default'}]
    assert len(selector.output_lanes) == 2
    assert selector.condition[0].get('predicate', None) == predicate
    assert selector.condition[1].get('predicate', None) == 'default'
    assert all([s.get('outputLane', False) for s in selector.condition])
    assert selector.output_streams == len(selector.output_lanes)

    selector.condition = [{'predicate': predicate}, 'default']
    assert len(selector.output_lanes) == 2
    assert selector.condition[0].get('predicate', None) == predicate
    assert selector.condition[1].get('predicate', None) == 'default'
    assert all([s.get('outputLane', False) for s in selector.condition])
    assert selector.output_streams == len(selector.output_lanes)


@pytest.mark.selector
def test_invalid_predicate_format(pipeline_builder):
    selector = pipeline_builder.add_stage('Stream Selector')

    with pytest.raises(ValueError):
        selector.condition = ['default', '>0']

    with pytest.raises(ValueError):
        selector.condition = [{'predicate': 'default'}, {'predicate': '>0'}]

    with pytest.raises(ValueError):
        selector.add_predicates('single predicate')

    with pytest.raises(ValueError):
        selector.add_predicates([{'invalidkey': 'invalid'}])


@pytest.mark.selector
def test_output_lanes_are_different_for_stream_selector(pipeline_builder):
    num_conditions = 10
    selector_stage = pipeline_builder.add_stage('Stream Selector')
    selector_stage.condition = ['>0' for i in range(num_conditions)]

    for i in range(num_conditions):
        for j in range(num_conditions):
            if i != j:
                assert selector_stage.output_lanes[i] != selector_stage.output_lanes[j]


@pytest.mark.selector
def test_stream_selector_connections(pipeline_builder):
    selector_stage = pipeline_builder.add_stage('Stream Selector')
    trash = pipeline_builder.add_stage('Trash')

    selector_stage >> trash

    assert selector_stage.output_lanes[0] == selector_stage.condition[0]['outputLane']
    assert selector_stage.output_lanes[0] == trash.input_lanes[0]

    selector_stage.condition = ['>=0']
    # Assert that the trash was disconnected.
    assert len(trash.input_lanes) == 0
    assert len(selector_stage.output_lanes) == 2

    trash2 = pipeline_builder.add_stage('Trash')
    selector_stage >> trash
    selector_stage >> trash2

    # Assert the proper order for connections
    assert selector_stage.output_lanes[0] == selector_stage.condition[0]['outputLane']
    assert selector_stage.output_lanes[0] == trash.input_lanes[0]
    assert selector_stage.output_lanes[1] == selector_stage.condition[1]['outputLane']
    assert selector_stage.output_lanes[1] == trash2.input_lanes[0]

    # Assert both trashes get disconnected
    selector_stage.condition = []
    assert len(trash.input_lanes) == 0
    assert len(trash2.input_lanes) == 0


@pytest.mark.selector
def test_publish_pipeline_with_stream_selector(engine_type, pipeline_builder, sch):
    if engine_type == 'snowflake':
        src_stage = pipeline_builder.add_stage('Snowflake Table', type='origin')
    else:
        src_stage = pipeline_builder.add_stage('Dev Raw Data Source')

    stream_selector = pipeline_builder.add_stage('Stream Selector')

    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')

    stage_names = [stage.instance_name for stage in [src_stage, stream_selector, trash1, trash2]]

    stream_selector.condition = ['>=0', 'default']

    src_stage >> stream_selector
    stream_selector >> trash1
    stream_selector >> trash2

    pipeline_name = 'simple_pipeline_with_stream_selector_{}'.format(get_random_string())
    pipeline = pipeline_builder.build(pipeline_name)
    try:
        sch.publish_pipeline(pipeline)
        published_pipeline = sch.pipelines.get(name=pipeline_name)
        src_stage, stream_selector, trash1, trash2 = [
            published_pipeline.stages.get(instance_name=name) for name in stage_names
        ]
        assert published_pipeline is not None
        assert stream_selector.output_lanes[0] == trash1.input_lanes[0]
        assert stream_selector.output_lanes[1] == trash2.input_lanes[0]
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.selector
def test_edit_pipeline_with_stream_selector(engine_type, pipeline_builder, sch):
    if engine_type == 'snowflake':
        src_stage = pipeline_builder.add_stage('Snowflake Table', type='origin')
    else:
        src_stage = pipeline_builder.add_stage('Dev Raw Data Source')

    stream_selector = pipeline_builder.add_stage('Stream Selector')

    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')

    stage_names = [stage.instance_name for stage in [src_stage, stream_selector, trash1, trash2]]

    stream_selector.condition = ['>=0', 'default']

    src_stage >> stream_selector
    stream_selector >> trash1
    stream_selector >> trash2

    pipeline_name = 'simple_pipeline_with_stream_selector_{}'.format(get_random_string())
    pipeline = pipeline_builder.build(pipeline_name)

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline_name)
        src_stage, stream_selector, trash1, trash2 = [pipeline.stages.get(instance_name=name) for name in stage_names]
        stream_selector.condition = ['=0']
        assert stream_selector.condition[0]['predicate'] == '=0'
        assert stream_selector.condition[1]['predicate'] == 'default'
        assert not trash1.input_lanes
        assert not trash2.input_lanes
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.selector
def test_stream_selector_has_output_lanes_with_different_id(pipeline_builder):
    stream_selector = pipeline_builder.add_stage('Stream Selector')

    stream_selector.predicates = ['0']
    lanes = stream_selector.output_lanes
    assert len(lanes) == 2
    # Check that no lane repeats
    assert len(lanes) == len(set(lanes))
    assert all(isinstance(predicate, dict) for predicate in stream_selector.predicates)

    stream_selector.add_predicates(['1'])
    stream_selector.add_predicates(['2'])

    lanes = stream_selector.output_lanes
    assert len(lanes) == 4
    # Check that no lane repeats
    assert len(lanes) == len(set(lanes))


@pytest.mark.selector
def test_remove_predicate_from_stream_selector(engine_type, pipeline_builder):
    if engine_type == 'snowflake':
        src_stage = pipeline_builder.add_stage('Snowflake Table', type='origin')
    else:
        src_stage = pipeline_builder.add_stage('Dev Raw Data Source')

    stream_selector = pipeline_builder.add_stage('Stream Selector')

    trash1 = pipeline_builder.add_stage('Trash')
    trash2 = pipeline_builder.add_stage('Trash')

    stream_selector.condition = ['>=0', 'default']

    src_stage >> stream_selector
    stream_selector >> trash1
    stream_selector >> trash2

    assert stream_selector.output_lanes[0] == trash1.input_lanes[0]
    assert len(stream_selector.output_lanes) == stream_selector.output_streams

    stream_selector.remove_predicate(stream_selector.condition[0])

    assert len(trash1.input_lanes) == 0
    assert len(stream_selector.output_lanes) == 1
    assert stream_selector.output_lanes[0] == trash2.input_lanes[0]
    assert len(stream_selector.output_lanes) == stream_selector.output_streams


@pytest.mark.selector
def test_add_predicates_to_stream_selector(engine_type, pipeline_builder):
    stream_selector = pipeline_builder.add_stage('Stream Selector')

    stream_selector.condition = ['default']
    assert len(stream_selector.predicates) == 1
    assert len(stream_selector.output_lanes) == len(stream_selector.predicates)

    stream_selector.add_predicates(['>=0'])

    assert len(stream_selector.predicates) == 2
    assert stream_selector.predicates[0]['predicate'] == '>=0'
    assert stream_selector.predicates[1]['predicate'] == 'default'
    assert len(stream_selector.output_lanes) == len(stream_selector.predicates)
    assert len(stream_selector.output_lanes) == stream_selector.output_streams


def test_add_and_remove_fragment_from_pipeline(sch, sch_authoring_sdc_id, sample_fragment):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    trash = pipeline_builder.add_stage('Trash')
    pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    number_of_stages = 2
    number_of_fragments = 1

    fragment_stage = pipeline.add_fragment(sample_fragment)
    fragment_stage >> trash

    # check that fragment has been added to stages and the internal fragments list
    assert len(pipeline.stages) == number_of_stages
    assert len(pipeline._pipeline_definition['fragments']) == number_of_fragments

    # test that the fragment metadata has been added to pipeline._builder
    assert len(pipeline._builder._fragment_commit_ids) == number_of_fragments
    assert pipeline._builder._fragment_commit_ids[0] == sample_fragment.commit_id
    assert pipeline._builder._fragment_instance_count[fragment_stage._data['uiInfo']['fragmentName']] == 1

    sch.publish_pipeline(pipeline)

    try:
        pipeline = sch.pipelines.get(name=pipeline.name)
        fragment_stage = pipeline.stages.get(instance_name=fragment_stage.instance_name)

        # after pulling from platform, check that fragment has been added to stages and the internal fragments list
        assert len(pipeline.stages) == number_of_stages
        assert len(pipeline._pipeline_definition['fragments']) == number_of_fragments

        # test that the remove functionality works
        pipeline.remove_stages(fragment_stage)

        # check that fragment has been removed from stages and the internal fragments list
        assert len(pipeline.stages) == number_of_stages - number_of_fragments
        assert len(pipeline._pipeline_definition['fragments']) == number_of_fragments - 1
        assert pipeline.stages[0].instance_name == trash.instance_name

        # test that the fragment metadata has been removed from pipeline._builder
        pipeline._get_builder()
        assert len(pipeline._builder._fragment_commit_ids) == number_of_fragments - 1
        assert pipeline._builder._fragment_instance_count[fragment_stage._data['uiInfo']['fragmentName']] == 0

    finally:
        sch.delete_pipeline(pipeline)


def test_copy_inputs_and_copy_outputs(sch, sample_pipeline):
    dev, trash = sample_pipeline.stages[0], sample_pipeline.stages[-1]
    field_renamer = sample_pipeline.add_stage('Field Renamer')

    field_renamer.copy_inputs(trash)
    assert field_renamer.input_lanes[0] == trash.input_lanes[0]

    field_renamer.copy_outputs(dev)
    assert field_renamer._data['outputLanes'][0] in trash._data['inputLanes']
    assert dev._data['outputLanes'][0] in trash._data['inputLanes']

    sch.publish_pipeline(sample_pipeline)
    sample_pipeline = sch.pipelines.get(pipeline_id=sample_pipeline.pipeline_id)
    dev = sample_pipeline.stages.get(instance_name='DevDataGenerator_01')
    trash = sample_pipeline.stages.get(instance_name='Trash_01')
    field_renamer = sample_pipeline.stages.get(instance_name='FieldRenamer_01')

    assert field_renamer.input_lanes[0] == trash.input_lanes[0]
    assert field_renamer._data['outputLanes'][0] in trash._data['inputLanes']
    assert dev._data['outputLanes'][0] in trash._data['inputLanes']
