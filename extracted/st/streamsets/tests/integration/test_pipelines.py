# Copyright 2022 StreamSets Inc.

# fmt: off
import json
import os
import re
import time
from datetime import datetime

import pytest

from streamsets.sdk.sch_models import ACL, Configuration, Pipeline
from streamsets.sdk.utils import SeekableList, get_random_string

# fmt: on

NUM_PIPELINES = 12
PIPELINE_NAME_PREFIX = '{}_pipeline_sdc_test'.format(str(datetime.now()))


@pytest.fixture(scope="module")
def sample_pipelines(resources_label, sch, sch_authoring_sdc_id):
    """A set of trivial pipelines:

    dev_data_generator >> trash
    """
    pipelines = []

    for i in range(NUM_PIPELINES):
        pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

        dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
        trash = pipeline_builder.add_stage('Trash')
        dev_data_generator >> trash

        pipeline_name = PIPELINE_NAME_PREFIX + '_{}_{}'.format(i, get_random_string())
        pipeline = pipeline_builder.build(pipeline_name)
        sch.publish_pipeline(pipeline)

        pipelines.append(pipeline)

    try:
        yield pipelines
    finally:
        for pipeline in pipelines:
            sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def sample_pipeline(resources_label, sch, sch_authoring_sdc_id):
    """A trivial pipelines:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build(
        'pipeline_sdc_test_{}_{}_{}'.format(resources_label, NUM_PIPELINES + 1, get_random_string())
    )
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


def test_iter(sch, sample_pipelines):
    iter_results = []
    for pipeline in sch.pipelines:
        iter_results.append(pipeline.pipeline_id)
    assert len(iter_results) >= len(sample_pipelines)
    assert not ({pipeline.pipeline_id for pipeline in sample_pipelines} - set(iter_results))


def test_pipelines_get_returns_pipeline_object(sch, sample_pipelines):
    assert sample_pipelines[0] in sch.pipelines
    assert isinstance(sch.pipelines.get(organization=sch.organization), Pipeline)


def test_pipeline_in_returns_true(sch, sample_pipelines):
    assert sample_pipelines[0] in sch.pipelines


def test_pipeline_contains(sch, sample_pipelines):
    pipeline = sample_pipelines[0]
    assert sch.pipelines.contains(pipeline_id=pipeline.pipeline_id)
    assert sch.pipelines.contains(name=pipeline.name)
    assert not sch.pipelines.contains(pipeline_id='impossible_to_clash_with_this_zbsdudcugeqwgui')


def test_pipelines_len_works(sch, sample_pipelines):
    assert len(sch.pipelines) >= len(sample_pipelines)


# Tests for __getitem__
def test_pipelines_getitem_int_pos_invalid_index(sch):
    total_number_of_pipelines = len(sch.pipelines)
    with pytest.raises(IndexError):
        sch.pipelines[total_number_of_pipelines]


def test_pipelines_getitem_int_neg_invalid_index(sch):
    total_number_of_pipelines = len(sch.pipelines)
    with pytest.raises(IndexError):
        sch.pipelines[-total_number_of_pipelines - 1]


def test_pipelines_getitem_int_instance_type(sch, sample_pipelines):
    total_number_of_pipelines = len(sch.pipelines)
    assert isinstance(sch.pipelines[total_number_of_pipelines - 1], Pipeline)


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_all(sch):
    total_number_of_pipelines = len(sch.pipelines)
    assert len(sch.pipelines[:]) == total_number_of_pipelines


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_stop(sch):
    assert len(sch.pipelines[:NUM_PIPELINES]) == NUM_PIPELINES


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_start_stop(sch):
    assert len(sch.pipelines[0:NUM_PIPELINES]) == NUM_PIPELINES


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_neg_start(sch):
    total_number_of_pipelines = len(sch.pipelines)
    assert len(sch.pipelines[-total_number_of_pipelines:]) == total_number_of_pipelines


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_neg_start_0_stop(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # stop is 0 so, it should always return empty list
    assert len(sch.pipelines[-total_number_of_pipelines:0]) == 0


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_extra_neg_start(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # eg. [1,2,3,4][-9:] = [1,2,3,4]
    assert len(sch.pipelines[-total_number_of_pipelines - 5 :]) == total_number_of_pipelines


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_step_size(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # verify with step size for both the cases of total_number_of_pipelines being an odd or even number
    assert len(sch.pipelines[::2]) == total_number_of_pipelines // 2 + total_number_of_pipelines % 2


@pytest.mark.skip("This test is flakey and will be skipped until TLKT-1052 is resolved")
def test_pipelines_getitem_slice_neg_step_size(sch):
    # verify negative step size
    assert len(sch.pipelines[-1:-2:-1]) == 1


# Tests for get_all
def test_get_all_returns_seekable_list(sch, sample_pipeline):
    assert isinstance(sch.pipelines.get_all(), SeekableList)


def test_get_all_filter_by_organization_and_version(sch, sample_pipeline):
    assert sch.pipelines.get_all(organization=sch.organization, version='1')


def test_get_all_filter_by_text(sch, sample_pipelines):
    pipelines = sch.pipelines.get_all(filter_text=PIPELINE_NAME_PREFIX)
    assert len(pipelines) == NUM_PIPELINES


# ACL tests
def test_pipeline_acl_get(sch):
    pipeline = sch.pipelines[0]
    acl = pipeline.acl
    assert isinstance(acl, ACL)
    assert acl.resource_type == 'PIPELINE'


def test_import_export_pipelines(sch, sch_authoring_sdc_id):
    # Create a pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('import_export_pipeline')
    sch.publish_pipeline(pipeline)

    pipelines_zip_data = sch.export_pipelines([pipeline])
    assert isinstance(pipelines_zip_data, bytes)

    path = '/tmp'
    filename = 'import_export_pipelines_{}.zip'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    with open('{}/{}'.format(path, filename), 'wb') as pipelines_zip_file:
        pipelines_zip_file.write(pipelines_zip_data)
    pipelines_zip_file_name = '{}/{}'.format(path, filename)

    try:
        pipelines_before = [pipeline]
        sch.delete_pipeline(pipeline)
        with open(pipelines_zip_file_name, 'rb') as input_file:
            pipelines_after = sch.import_pipelines_from_archive(input_file, 'Test Import Pipelines')
        assert len(pipelines_before) == len(pipelines_after)
    except Exception as ex:
        raise ex
    finally:
        os.remove(pipelines_zip_file_name)
        if pipeline:
            sch.delete_pipeline(pipeline)


def test_import_pipelines_v2(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('import_pipelines_v2')
    try:
        sch.publish_pipeline(pipeline)

        pipeline_id = pipeline.pipeline_id
        assert len(sch.pipelines.get_all(pipeline_id=pipeline_id)) == 1

        pipelines_zip_data = sch.export_pipelines([pipeline])
        sch.delete_pipeline(pipeline)
        assert len(sch.pipelines.get_all(pipeline_id=pipeline_id)) == 0

        pipelines = sch.api_client.verify_import_pipelines(
            "Test Import Pipelines V2", pipelines_zip_data
        ).response.json()
        sch.api_client.import_pipelines_v2(pipelines)

        assert len(sch.pipelines.get_all(pipeline_id=pipeline_id)) == 1
    except Exception as ex:
        raise ex
    finally:
        if pipeline.pipeline_id:
            sch.delete_pipeline(pipeline)


def test_verify_import_pipelines(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('verify_import_pipeline')
    sch.publish_pipeline(pipeline)

    pipelines_zip_data = sch.export_pipelines([pipeline])
    sch.delete_pipeline(pipeline)
    import_pipeline_json = sch.api_client.verify_import_pipelines(
        'Test Verify Import Pipelines',
        pipelines_zip_data,
    ).response.json()
    import_pipeline_json_keys = ['commitPipelineJsons', 'importConnectionJsons', 'availableConnections']
    for key in import_pipeline_json_keys:
        assert key in import_pipeline_json.keys()


def test_get_pipeline_templates(sch):
    templates = sch.pipelines.get_all(template=True)
    assert isinstance(templates, SeekableList)
    if templates:
        assert isinstance(templates[0], Pipeline)


def test_update_pipeline(sch, sch_authoring_sdc_id):
    # Build and publish pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('pipeline_to_be_updated')
    sch.publish_pipeline(pipeline)

    try:
        # Update batch size
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource':
                assert stage.batch_size != 999
                stage.batch_size = 999
        sch.publish_pipeline(pipeline)

        # Confirm pipeline.stages is updated
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource':
                assert stage.batch_size == 999

        # Confirm it is updated in json data
        for stage in json.loads(pipeline._data['pipelineDefinition'])['stages']:
            if stage['stageName'] == 'com_streamsets_pipeline_stage_devtest_RandomDataGeneratorSource':
                for config in stage['configuration']:
                    if config['name'] == 'batchSize':
                        assert config['value'] == 999
    finally:
        sch.delete_pipeline(pipeline)


def test_update_pipeline_with_transformer(sch, sch_authoring_transformer_id):
    # Build and publish pipeline
    if len(sch.transformers) < 1:
        pytest.skip("Need at least one transformer instance to run this test")
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    dev_random = pipeline_builder.add_stage('Dev Random')
    trash = pipeline_builder.add_stage('Trash')
    dev_random >> trash
    pipeline = pipeline_builder.build('pipeline_to_be_updated')
    sch.publish_pipeline(pipeline)

    try:
        # Update batch size
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_pipeline_spark_origin_dev_DevRandomDOrigin':
                assert stage.batch_size != 999
                stage.batch_size = 999
        sch.publish_pipeline(pipeline)

        # Confirm pipeline.stages is updated
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_pipeline_spark_origin_dev_DevRandomDOrigin':
                assert stage.batch_size == 999

        # Confirm it is updated in json data
        for stage in json.loads(pipeline._data['pipelineDefinition'])['stages']:
            if stage['stageName'] == 'com_streamsets_pipeline_spark_origin_dev_DevRandomDOrigin':
                for config in stage['configuration']:
                    if config['name'] == 'batchSize':
                        assert config['value'] == 999
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.parametrize('executor_type', ('TRANSFORMER', 'DATACOLLECTOR'))
def test_execution_mode_config(sch, executor_type, sch_authoring_sdc_id, sch_authoring_transformer_id):
    if executor_type == 'TRANSFORMER':
        if len(sch.transformers) < 1:
            pytest.skip("Need at least one transformer instance to run this test")
        pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
        dev = pipeline_builder.add_stage('Dev Random')
    elif executor_type == 'DATACOLLECTOR':
        if len(sch.data_collectors) < 1:
            pytest.skip("Need at least one registered DataCollector instance to run this test")
        pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
        dev = pipeline_builder.add_stage('Dev Data Generator')

    trash = pipeline_builder.add_stage('Trash')
    dev >> trash
    pipeline = pipeline_builder.build('execution_mode_config')
    sch.publish_pipeline(pipeline)

    try:
        pipeline_definition = json.loads(pipeline._data['pipelineDefinition'])
        assert 'executionMode' not in pipeline_definition
        configuration = Configuration(configuration=pipeline_definition['configuration'])
        assert configuration.get('executionMode', None) is not None
    finally:
        sch.delete_pipeline(pipeline)


def test_duplicate_pipeline(sch, sample_pipeline):
    duplicated_pipelines = sch.duplicate_pipeline(sample_pipeline)
    try:
        assert isinstance(duplicated_pipelines, SeekableList)
        assert len(duplicated_pipelines) == 1
        assert (
            sch.pipelines.get(name='{} copy'.format(sample_pipeline.name), only_published=False).pipeline_id
            == duplicated_pipelines[0].pipeline_id
        )
    finally:
        for pipeline in duplicated_pipelines:
            sch.delete_pipeline(pipeline)


def test_duplicate_pipelines(sch, sample_pipeline):
    name = 'test_duplicate_pipeline_{}_'.format(get_random_string())
    duplicated_pipelines = sch.duplicate_pipeline(
        sample_pipeline, name=name, description='Testing Duplication', number_of_copies=3
    )

    pipeline_id_to_object = {}
    for pipeline in duplicated_pipelines:
        pipeline_id_to_object[pipeline.pipeline_id] = pipeline

    try:
        assert isinstance(duplicated_pipelines, SeekableList)
        assert len(duplicated_pipelines) == 3

        for duplicate_pipeline in duplicated_pipelines:
            pipeline = sch.pipelines.get(name=duplicate_pipeline.name, only_published=False)

            assert pipeline.pipeline_id in pipeline_id_to_object
            assert pipeline.name == pipeline_id_to_object[pipeline.pipeline_id].name

    finally:
        for pipeline in duplicated_pipelines:
            sch.delete_pipeline(pipeline)


def test_create_and_publish_draft(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple pipeline draft')
    sch.publish_pipeline(pipeline, draft=True)
    try:
        assert pipeline.draft is True
        assert pipeline.name == 'simple pipeline draft'
        assert pipeline.version == '1-DRAFT'
        sch.publish_pipeline(pipeline)
        assert getattr(pipeline, 'draft', False) is False
        assert pipeline.name == 'simple pipeline draft'
    finally:
        sch.delete_pipeline(pipeline)


def test_publishing_duplicate_of_pipeline_draft(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple pipeline draft')
    sch.publish_pipeline(pipeline, draft=True)
    try:
        duplicated_pipeline = sch.duplicate_pipeline(pipeline)[0]
        assert duplicated_pipeline.draft is True
        assert duplicated_pipeline.version == '1-DRAFT'
        duplicated_pipeline_name = duplicated_pipeline.name
        sch.publish_pipeline(duplicated_pipeline)
        assert getattr(duplicated_pipeline, 'draft', False) is False
        assert duplicated_pipeline.name == duplicated_pipeline_name
    finally:
        sch.delete_pipeline(duplicated_pipeline)
        sch.delete_pipeline(pipeline)


def test_should_fail_to_add_empty_collection_of_downstream_stages_to_collector(sch, sch_authoring_sdc_id):
    if len(sch.data_collectors) < 1:
        pytest.skip("Need at least one registered DataCollector instance to run this test")

    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')

    with pytest.raises(ValueError) as exc_info:
        dev_data_generator >> []

    assert exc_info.match(re.escape("Attempted to add an empty collection of downstream stages."))


def test_should_fail_to_add_empty_collection_of_downstream_stages_to_spark_transformer(
    sch, sch_authoring_transformer_id
):
    if len(sch.transformers) < 1:
        pytest.skip("Need at least one transformer instance to run this test")

    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    dev_random = pipeline_builder.add_stage('Dev Random')

    with pytest.raises(ValueError) as exc_info:
        dev_random >> []

    assert exc_info.match(re.escape("Attempted to add an empty collection of downstream stages."))


def test_should_fail_to_add_empty_collection_of_downstream_stages_to_snowflake_transformer(sch):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake', fragment=True)
    dev_data_generator = pipeline_builder.add_stage('Snowflake Table', type='origin')

    with pytest.raises(ValueError) as exc_info:
        dev_data_generator >> []

    assert exc_info.match(re.escape("Attempted to add an empty collection of downstream stages."))


def test_retrieve_draft_pipeline_via_pipeline_id(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('simple pipeline draft')
    sch.publish_pipeline(pipeline, draft=True)
    try:
        draft_pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id, draft=True)
        assert pipeline.draft is True
        assert draft_pipeline.draft is True
        assert draft_pipeline.pipeline_id == pipeline.pipeline_id
        assert draft_pipeline.commit_id == pipeline.commit_id
    finally:
        sch.delete_pipeline(pipeline)


def test_pipeline_add_stage(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    sample_pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(sample_pipeline)

    try:
        # Assert that the inital stages are present
        assert len(sample_pipeline.stages) == 2
        sample_pipeline.stages[0].instance_name = 'DevDataGenerator_01'
        sample_pipeline.stages[1].instance_name = 'Trash_01'

        # Assert that the stage has been added in memory
        sample_pipeline.add_stage('Dev Data Generator')
        assert len(sample_pipeline.stages) == 3
        sample_pipeline.stages[-1].instance_name = 'DevDataGenerator_02'

        # Assert that the stage exists in Platform
        sch.publish_pipeline(sample_pipeline)
        sample_pipeline = sch.pipelines.get(pipeline_id=sample_pipeline.pipeline_id)
        assert len(sample_pipeline.stages) == 3
        sample_pipeline.stages[-1].instance_name = 'DevDataGenerator_02'

        # Add another stage to make sure pipelines pulled in from SCH are editable
        sample_pipeline.add_stage('Dev Data Generator')
        assert len(sample_pipeline.stages) == 4
        sample_pipeline.stages[-1].instance_name = 'DevDataGenerator_03'

    except Exception as e:
        raise e
    finally:
        sch.delete_pipeline(sample_pipeline)


def test_add_and_connect_stage_to_linear_pipeline(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')
    data_parser >> trash
    sample_pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(sample_pipeline)

    try:
        # Assert that the inital stages are present
        assert len(sample_pipeline.stages) == 2
        sample_pipeline.stages[0].instance_name = 'DataParser_01'
        assert len(sample_pipeline.stages[0]._data['inputLanes']) == 0
        sample_pipeline.stages[1].instance_name = 'Trash_01'

        # Assert that the stage has been added in memory
        dev_data_generator = sample_pipeline.add_stage('Dev Data Generator')
        dev_data_generator >> sample_pipeline.stages[0]

        assert len(sample_pipeline.stages) == 3
        sample_pipeline.stages[-1].instance_name = 'DevDataGenerator_01'

        data_parser, dev_data_generator = sample_pipeline.stages[0], sample_pipeline.stages[-1]
        assert dev_data_generator._data['outputLanes'][0].split('OutputLane')[0] == dev_data_generator.instance_name
        assert data_parser._data['inputLanes'][0] == dev_data_generator._data['outputLanes'][0]

        # Assert that the stage exists in Platform
        sch.publish_pipeline(sample_pipeline)
        sample_pipeline = sch.pipelines.get(pipeline_id=sample_pipeline.pipeline_id)

        assert len(sample_pipeline.stages) == 3
        sample_pipeline.stages[-1].instance_name = 'DevDataGenerator_01'

        data_parser, dev_data_generator = sample_pipeline.stages[1], sample_pipeline.stages[0]
        print(data_parser)
        print(dev_data_generator)
        assert dev_data_generator._data['outputLanes'][0].split('OutputLane')[0] == dev_data_generator.instance_name
        assert data_parser._data['inputLanes'][0] == dev_data_generator._data['outputLanes'][0]

    except Exception as e:
        raise e
    finally:
        sch.delete_pipeline(sample_pipeline)


def test_add_multiple_destinations_to_linear_pipeline(sch, sch_authoring_sdc_id):
    # Build pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)

    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    data_parser = pipeline_builder.add_stage('Data Parser')
    trash = pipeline_builder.add_stage('Trash')

    dev_data_generator >> data_parser
    data_parser >> trash
    sample_pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(sample_pipeline)

    try:
        # Assert that the initial stages are present
        assert len(sample_pipeline.stages) == 3

        # Assert that the stage has been added in memory
        trash_2 = sample_pipeline.add_stage('Trash')
        assert trash_2.instance_name == 'Trash_02'
        sample_pipeline.stages[-3] >> trash_2

        assert len(sample_pipeline.stages) == 4
        data_parser, trash_1, trash_2 = (
            sample_pipeline.stages[-3],
            sample_pipeline.stages[-2],
            sample_pipeline.stages[-1],
        )

        assert len(data_parser._data['outputLanes']) == 1
        assert len(trash_1._data['inputLanes']) == 1
        assert len(trash_2._data['inputLanes']) == 1
        assert data_parser._data['outputLanes'][0] == trash_1._data['inputLanes'][0]
        assert data_parser._data['outputLanes'][0] == trash_2._data['inputLanes'][0]

        # Assert that the stage exists in Platform
        sch.publish_pipeline(sample_pipeline)
        sample_pipeline = sch.pipelines.get(pipeline_id=sample_pipeline.pipeline_id)

        data_parser, trash_1, trash_2 = (
            sample_pipeline.stages[-3],
            sample_pipeline.stages[-2],
            sample_pipeline.stages[-1],
        )

        assert len(data_parser._data['outputLanes']) == 1
        assert len(trash_1._data['inputLanes']) == 1
        assert len(trash_2._data['inputLanes']) == 1
        assert data_parser._data['outputLanes'][0] == trash_1._data['inputLanes'][0]
        assert data_parser._data['outputLanes'][0] == trash_2._data['inputLanes'][0]

    except Exception as e:
        raise e
    finally:
        sch.delete_pipeline(sample_pipeline)


def test_pipeline_add_stage_with_stage_that_doesnt_exist(sch, sample_pipeline):
    # Assert that the inital stages are present
    assert len(sample_pipeline.stages) == 2
    sample_pipeline.stages[0].instance_name = 'DevDataGenerator_01'
    sample_pipeline.stages[1].instance_name = 'Trash_01'

    # Assert that adding a stage that doesn't exist throws an exception
    with pytest.raises(Exception):
        sample_pipeline.add_stage('Stage that doesnt exist')


def test_add_stage_to_pipeline_in_v1_draft_mode(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline = pipeline_builder.build('simple pipeline draft')

    # publish as v1-draft
    sch.publish_pipeline(pipeline, draft=True)
    try:
        # pull draft pipeline and add stages
        pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id, draft=True)
        dev_data_generator = pipeline.add_stage('Dev Data Generator')
        trash = pipeline.add_stage('Trash')
        dev_data_generator >> trash

        # publish pipeline as v1
        sch.publish_pipeline(pipeline)

        # assert that the changes carried over to control hub
        pipeline = sch.pipelines.get(pipeline_id=pipeline.pipeline_id)
        assert len(pipeline.stages) == 2
        assert pipeline.stages[0].instance_name == 'DevDataGenerator_01'
        assert pipeline.stages[1].instance_name == 'Trash_01'

    except Exception as e:
        raise e
    finally:
        sch.delete_pipeline(pipeline)


def test_library_definitions_lazy_loading(sch, sch_authoring_sdc_id):
    # Creating a new pipeline to ensure it hasn't been loaded in-memory yet
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    sch.publish_pipeline(pipeline)

    assert pipeline.library_definitions is not None
    assert pipeline.library_definitions == json.loads(pipeline._data['libraryDefinitions'])
    assert pipeline._library_definitions == json.loads(pipeline._data['libraryDefinitions'])
    assert pipeline._data_internal['libraryDefinitions'] == pipeline._data['libraryDefinitions']


def test_pipeline_configuration_property(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline = pipeline_builder.build('TEST {}'.format(get_random_string()))

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)

        # Picking three arbitrary configuration fields that should exist and checking those values
        assert pipeline.configuration.get('shouldRetry') == pipeline.configuration.retry_pipeline_on_error
        assert (
            pipeline.configuration.get('shouldCreateFailureSnapshot') == pipeline.configuration.create_failure_snapshot
        )
        assert pipeline.configuration.get('triggerInterval') == pipeline.configuration.trigger_interval_in_millis

        # Store old values
        retry_pipeline_on_error = pipeline.configuration.retry_pipeline_on_error
        create_failure_snapshot = pipeline.configuration.create_failure_snapshot
        trigger_interval_in_millis = pipeline.configuration.trigger_interval_in_millis

        # Changing values via the property names
        pipeline.configuration.retry_pipeline_on_error = not pipeline.configuration.retry_pipeline_on_error
        pipeline.configuration.create_failure_snapshot = not pipeline.configuration.create_failure_snapshot
        pipeline.configuration.trigger_interval_in_millis = pipeline.configuration.trigger_interval_in_millis + 1

        # Assert value has been changed in property
        assert pipeline.configuration.retry_pipeline_on_error == (not retry_pipeline_on_error)
        assert pipeline.configuration.create_failure_snapshot == (not create_failure_snapshot)
        assert pipeline.configuration.trigger_interval_in_millis == trigger_interval_in_millis + 1

        # assert that the change has been made in the underlying json
        assert pipeline.configuration.get('shouldRetry') == pipeline.configuration.retry_pipeline_on_error
        assert (
            pipeline.configuration.get('shouldCreateFailureSnapshot') == pipeline.configuration.create_failure_snapshot
        )
        assert pipeline.configuration.get('triggerInterval') == pipeline.configuration.trigger_interval_in_millis

        # Publish pipeline and make sure these changes have been added to Platform
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)

        # assert that the change has been made in the underlying json
        assert pipeline.configuration.get('shouldRetry') == (not retry_pipeline_on_error)
        assert pipeline.configuration.get('shouldCreateFailureSnapshot') == (not create_failure_snapshot)
        assert pipeline.configuration.get('triggerInterval') == trigger_interval_in_millis + 1

    except Exception as e:
        raise e

    finally:
        sch.delete_pipeline(pipeline)


def test_stage_configuration_property(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.add_stage('Dev Data Generator')
    pipeline_builder.add_stage('Data Parser')
    pipeline_builder.add_stage('JDBC Multitable Consumer')
    pipeline = pipeline_builder.build('TEST {}'.format(get_random_string()))

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)
        stages = pipeline.stages
        dev_data_gen, data_parser, jdbc_multitable_consumer = stages[0], stages[1], stages[2]

        # Picking three arbitrary configuration fields that should exist and checking those values
        assert dev_data_gen.configuration.get('batchSize') == dev_data_gen.configuration.batch_size
        assert (
            jdbc_multitable_consumer.configuration.get('commonSourceConfigBean.noMoreDataEventDelay')
            == jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds
        )
        assert data_parser.configuration.get('stageOnRecordError') == data_parser.configuration.on_record_error

        # Store older value
        batch_size = dev_data_gen.configuration.batch_size
        no_more_data_event_generation_delay_in_seconds = (
            jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds
        )

        # Changing values via the property names
        dev_data_gen.configuration.batch_size = dev_data_gen.configuration.batch_size + 1
        jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds = (
            jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds + 1
        )
        data_parser.configuration.on_record_error = 'RANDOM VALUE'

        # assert value has been changed
        assert batch_size + 1 == dev_data_gen.configuration.batch_size
        assert no_more_data_event_generation_delay_in_seconds + 1 == (
            jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds
        )
        assert 'RANDOM VALUE' == data_parser.configuration.on_record_error

        # assert that the change has been made in the underlying json
        assert dev_data_gen.configuration.get('batchSize') == dev_data_gen.configuration.batch_size
        assert jdbc_multitable_consumer.configuration.get('commonSourceConfigBean.noMoreDataEventDelay') == (
            jdbc_multitable_consumer.configuration.no_more_data_event_generation_delay_in_seconds
        )
        assert data_parser.configuration.get('stageOnRecordError') == data_parser.configuration.on_record_error

        # Publish pipeline and make sure these changes have been added to Platform
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)

        # assert that the change has been made in the underlying json
        assert dev_data_gen.configuration.get('batchSize') == batch_size + 1
        assert jdbc_multitable_consumer.configuration.get('commonSourceConfigBean.noMoreDataEventDelay') == (
            no_more_data_event_generation_delay_in_seconds + 1
        )
        assert data_parser.configuration.get('stageOnRecordError') == 'RANDOM VALUE'

    except Exception as e:
        raise e

    finally:
        sch.delete_pipeline(pipeline)


def test_invalid_pipeline_configuration_property(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline = pipeline_builder.build('TEST {}'.format(get_random_string()))

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)

        # Assert that invoking an attribute that does not exist raises an error
        with pytest.raises(AttributeError):
            pipeline.configuration.property_that_clearly_does_not_exist

    except Exception as e:
        raise e

    finally:
        sch.delete_pipeline(pipeline)


def test_invalid_stage_configuration_property(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.add_stage('Dev Data Generator')
    pipeline = pipeline_builder.build('TEST {}'.format(get_random_string()))

    try:
        sch.publish_pipeline(pipeline)
        pipeline = sch.pipelines.get(name=pipeline.name)
        stages = pipeline.stages
        dev_data_gen = stages[0]

        # Assert that invoking an attribute that does not exist raises an error
        with pytest.raises(AttributeError):
            dev_data_gen.configuration.property_that_clearly_does_not_exist

    except Exception as e:
        raise e

    finally:
        sch.delete_pipeline(pipeline)


def test_import_pipeline_and_build_basic_sdc(sch, sch_authoring_sdc_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.import_pipeline(sample_pipeline)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name


def test_import_pipeline_and_build_basic_transformer(sch, sch_authoring_transformer_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    pipeline_builder.import_pipeline(sample_pipeline)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name


def test_import_pipeline_with_new_title(sch, sch_authoring_sdc_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.import_pipeline(sample_pipeline)
    pipeline = pipeline_builder.build('TEST IMPORT NAME', build_from_imported=True)

    assert pipeline.name == 'TEST IMPORT NAME'


def test_import_pipeline_with_new_title_transformer(sch, sch_authoring_transformer_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    pipeline_builder.import_pipeline(sample_pipeline)
    pipeline = pipeline_builder.build('TEST IMPORT NAME', build_from_imported=True)

    assert pipeline.name == 'TEST IMPORT NAME'


def test_import_pipeline_and_build_with_commit_id_regeneration_false_sdc(sch, sch_authoring_sdc_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.import_pipeline(sample_pipeline, commit_id_regeneration=False)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name

    assert pipeline.commit_id == sample_pipeline.commit_id
    assert pipeline.commit_message == sample_pipeline.commit_message
    assert pipeline.commit_time == sample_pipeline.commit_time


def test_import_pipeline_and_build_with_commit_id_regeneration_false_transformer(
    sch, sch_authoring_transformer_id, sample_pipeline
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    pipeline_builder.import_pipeline(sample_pipeline, commit_id_regeneration=False)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name

    assert pipeline.commit_id == sample_pipeline.commit_id
    assert pipeline.commit_message == sample_pipeline.commit_message
    assert pipeline.commit_time == sample_pipeline.commit_time


def test_import_pipeline_and_build_with_regenerate_id_false_sdc(sch, sch_authoring_sdc_id, sample_pipeline):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    pipeline_builder.import_pipeline(sample_pipeline, regenerate_id=False)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name

    assert pipeline.pipeline_id == sample_pipeline.pipeline_id


def test_import_pipeline_and_build_with_regenerate_id_false_transformer(
    sch, sch_authoring_transformer_id, sample_pipeline
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='transformer', engine_id=sch_authoring_transformer_id)
    pipeline_builder.import_pipeline(sample_pipeline, regenerate_id=False)
    pipeline = pipeline_builder.build(build_from_imported=True)

    assert pipeline.name == 'Pipeline'
    assert pipeline.version == sample_pipeline.version
    assert pipeline.description == sample_pipeline.description
    assert pipeline.draft == sample_pipeline.draft
    assert pipeline.execution_mode == sample_pipeline.execution_mode

    pipeline_stages, sample_pipeline_stages = pipeline.stages, sample_pipeline.stages
    assert len(pipeline_stages) == len(sample_pipeline_stages)

    for index, stage in enumerate(pipeline_stages):
        assert stage.stage_name == sample_pipeline_stages[index].stage_name

    assert pipeline.pipeline_id == sample_pipeline.pipeline_id


def test_import_pipeline_with_invalid_pipeline_type(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    with pytest.raises(ValueError):
        pipeline_builder.import_pipeline('sample_pipeline')


def test_pipeline_uses_same_builder(sample_pipeline):
    sample_pipeline.add_stage("Trash")
    sample_pipeline_builder_1 = sample_pipeline._builder
    sample_pipeline.add_stage("Trash")
    assert sample_pipeline_builder_1 is sample_pipeline._builder


def test_pipeline_uses_same_builder_with_engine_changes(sch, sdc_deployment):
    pipeline = None
    try:
        deployment = sdc_deployment
        pipeline_name = 'sample_pipeline_{}'.format(get_random_string())
        engine = deployment.registered_engines[0]
        engine_id = engine.id
        engine_type = "data_collector"
        stage_to_add = "Cassandra"
        library_to_add = "cassandra_3"

        # Create a pipeline
        pipeline_builder = sch.get_pipeline_builder(engine_type=engine_type, engine_id=engine_id)
        pipeline = pipeline_builder.build(pipeline_name)
        sch.publish_pipeline(pipeline)

        # Retrieve a pipeline and check it has no builder
        pipeline = sch.pipelines.get(name=pipeline_name)
        assert pipeline._builder is None

        # Check a pipelineBuilder is made
        pipeline.add_stage("Trash")
        assert pipeline._builder is not None
        pipeline_builder_1 = pipeline._builder

        # Check pipeline can't add stage that does not exist
        with pytest.raises(Exception) as e:
            pipeline.add_stage(stage_to_add)
        assert str(e.value) == "Could not find stage ({}).".format(stage_to_add)

        # Update the deployment and engine with a new library
        deployment.engine_configuration.stage_libs.extend([library_to_add])
        sch.update_deployment(deployment)
        sch.restart_engines(engine)
        # Wait for engine to restart
        time.sleep(300)

        # Check ability to add new stage with the same builder object
        pipeline_stage_len = len(pipeline.stages)
        pipeline.add_stage(stage_to_add)
        assert len(pipeline.stages) == pipeline_stage_len + 1
        assert pipeline._builder is pipeline_builder_1
    finally:
        if pipeline:
            sch.delete_pipeline(pipeline)


@pytest.mark.parametrize(
    "sch_authoring_id, engine_type",
    [("sch_authoring_sdc_id", "transformer"), ("sch_authoring_transformer_id", "data_collector")],
)
def test_call_get_pipeline_builder_with_disparate_engine_type_and_engine(sch, sch_authoring_id, engine_type, request):
    sch_authoring_id = request.getfixturevalue(sch_authoring_id)
    with pytest.raises(TypeError):
        sch.get_pipeline_builder(engine_type, sch_authoring_id)
