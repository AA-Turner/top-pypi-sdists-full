# Copyright 2022 StreamSets Inc.

# fmt: off
import json
import os
from datetime import datetime

import pytest

from streamsets.sdk.sch_models import ACL, Configuration, Pipeline
from streamsets.sdk.st_models import Preview as StPreview
from streamsets.sdk.utils import SeekableList, get_random_string

# fmt: on

NUM_PIPELINES = 12


@pytest.fixture(scope="module")
def sample_pipelines(sch, snowflake_config):
    """A set of trivial pipelines:

    dev_data_generator >> trash
    """
    pipelines = []

    for i in range(NUM_PIPELINES):
        pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

        snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
        snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
        trash = pipeline_builder.add_stage('Trash')
        snowflake_table >> trash

        pipeline_name = 'pipeline_snowflake_test_{}_{}'.format(i, get_random_string())
        pipeline = pipeline_builder.build(pipeline_name)
        pipeline.configuration['connectionString'] = snowflake_config['connectionString']
        pipeline.configuration['db'] = snowflake_config['db']
        pipeline.configuration['warehouse'] = snowflake_config['warehouse']
        pipeline.configuration['schema'] = snowflake_config['schema']
        sch.publish_pipeline(pipeline)

        pipelines.append(pipeline)

    try:
        yield pipelines
    finally:
        for pipeline in pipelines:
            sch.delete_pipeline(pipeline)


@pytest.fixture(scope="module")
def sample_pipeline(sch, snowflake_config):
    """A trivial pipelines:

    dev_data_generator >> trash
    """
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
def test_iter(sch, sample_pipelines):
    iter_results = []
    for pipeline in sch.pipelines:
        iter_results.append(pipeline.pipeline_id)
    assert len(iter_results) >= len(sample_pipelines)
    assert not ({pipeline.pipeline_id for pipeline in sample_pipelines} - set(iter_results))


@pytest.mark.snowflake
def test_pipelines_get_returns_pipeline_object(sch, sample_pipelines):
    assert sample_pipelines[0] in sch.pipelines
    assert isinstance(sch.pipelines.get(organization=sch.organization), Pipeline)


@pytest.mark.snowflake
def test_pipeline_in_returns_true(sch, sample_pipelines):
    assert sample_pipelines[0] in sch.pipelines


@pytest.mark.snowflake
def test_pipeline_contains(sch, sample_pipelines):
    pipeline = sample_pipelines[0]
    assert sch.pipelines.contains(pipeline_id=pipeline.pipeline_id)
    assert sch.pipelines.contains(name=pipeline.name)
    assert not sch.pipelines.contains(pipeline_id='impossible_to_clash_with_this_zbsdudcugeqwgui')


@pytest.mark.snowflake
def test_pipelines_len_works(sch, sample_pipelines):
    assert len(sch.pipelines) >= len(sample_pipelines)


# Tests for __getitem__
@pytest.mark.snowflake
def test_pipelines_getitem_int_pos_invalid_index(sch):
    total_number_of_pipelines = len(sch.pipelines)
    with pytest.raises(IndexError):
        sch.pipelines[total_number_of_pipelines]


@pytest.mark.snowflake
def test_pipelines_getitem_int_neg_invalid_index(sch):
    total_number_of_pipelines = len(sch.pipelines)
    with pytest.raises(IndexError):
        sch.pipelines[-total_number_of_pipelines - 1]


@pytest.mark.snowflake
def test_pipelines_getitem_int_instance_type(sch, sample_pipelines):
    total_number_of_pipelines = len(sch.pipelines)
    assert isinstance(sch.pipelines[total_number_of_pipelines - 1], Pipeline)


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_all(sch):
    total_number_of_pipelines = len(sch.pipelines)
    assert len(sch.pipelines[:]) == total_number_of_pipelines


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_stop(sch):
    assert len(sch.pipelines[:NUM_PIPELINES]) == NUM_PIPELINES


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_start_stop(sch):
    assert len(sch.pipelines[0:NUM_PIPELINES]) == NUM_PIPELINES


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_neg_start(sch):
    total_number_of_pipelines = len(sch.pipelines)
    assert len(sch.pipelines[-total_number_of_pipelines:]) == total_number_of_pipelines


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_neg_start_0_stop(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # stop is 0 so, it should always return empty list
    assert len(sch.pipelines[-total_number_of_pipelines:0]) == 0


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_extra_neg_start(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # eg. [1,2,3,4][-9:] = [1,2,3,4]
    assert len(sch.pipelines[-total_number_of_pipelines - 5 :]) == total_number_of_pipelines


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_step_size(sch):
    total_number_of_pipelines = len(sch.pipelines)
    # verify with step size for both the cases of total_number_of_pipelines being an odd or even number
    assert len(sch.pipelines[::2]) == total_number_of_pipelines // 2 + total_number_of_pipelines % 2


@pytest.mark.snowflake
@pytest.mark.skip('This test will fail until TLKT-1052 is resolved')
def test_pipelines_getitem_slice_neg_step_size(sch):
    # verify negative step size
    assert len(sch.pipelines[-1:-2:-1]) == 1


# Tests for get_all
@pytest.mark.snowflake
def test_get_all_returns_seekable_list(sch):
    assert isinstance(sch.pipelines.get_all(), SeekableList)


@pytest.mark.snowflake
def test_get_all_filter_by_organization_and_version(sch):
    assert sch.pipelines.get_all(organization=sch.organization, version='1')


@pytest.mark.snowflake
def test_get_all_filter_by_text(sch, sample_pipelines):
    pipelines = sch.pipelines.get_all(filter_text='pipeline_snowflake_test_')
    assert len(pipelines) == NUM_PIPELINES


# ACL tests
@pytest.mark.snowflake
def test_pipeline_acl_get(sch):
    pipeline = sch.pipelines[0]
    acl = pipeline.acl
    assert isinstance(acl, ACL)
    assert acl.resource_type == 'PIPELINE'


@pytest.mark.snowflake
def test_import_export_pipelines(sch, snowflake_config):
    # Create a pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('import_export_pipeline')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
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


@pytest.mark.snowflake
def test_get_pipeline_templates(sch):
    templates = sch.pipelines.get_all(template=True)
    assert isinstance(templates, SeekableList)
    if templates:
        assert isinstance(templates[0], Pipeline)


@pytest.mark.snowflake
def test_update_pipeline(sch, snowflake_config):
    # Build and publish pipeline
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('pipeline_to_be_updated')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)

    try:
        # Update batch size
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin':
                assert stage.label != 'Updated stage name'
                stage.label = 'Updated stage name'
        sch.publish_pipeline(pipeline)

        # Confirm pipeline.stages is updated
        for stage in pipeline.stages:
            if stage.stage_name == 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin':
                assert stage.label == 'Updated stage name'

        # Confirm it is updated in json data
        for stage in json.loads(pipeline._data['pipelineDefinition'])['stages']:
            if stage['stageName'] == 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin':
                for config in stage['configuration']:
                    if config['name'] == 'label':
                        assert config['value'] == 'Updated stage name'
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
def test_execution_mode_config(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('execution_mode_config')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)
    try:
        pipeline_definition = json.loads(pipeline._data['pipelineDefinition'])
        assert 'executionMode' not in pipeline_definition
        configuration = Configuration(configuration=pipeline_definition['configuration'])
        assert configuration.get('executionMode', None) is not None
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
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


@pytest.mark.snowflake
def test_duplicate_pipelines(sch, sample_pipeline):
    name = 'test_duplicate_pipeline_snowflake_{}_'.format(get_random_string())
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


@pytest.mark.snowflake
def test_create_and_publish_draft(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('simple pipeline draft')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
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


@pytest.mark.snowflake
def test_create_and_publish_validate(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    pipeline = pipeline_builder.build('simple pipeline validate true')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline, validate=True)
    try:
        # The published pipeline is not valid since it doesn't have a destination. Checking that it was marked as such
        # when validate is True
        pipeline_definition = json.loads(pipeline.pipeline_definition)
        assert not pipeline_definition['valid']
        # Publishing the pipeline again with validate equals False, to see if now it always shows as valid
        sch.publish_pipeline(pipeline)
        pipeline_definition = json.loads(pipeline.pipeline_definition)
        assert pipeline_definition['valid']
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
def test_publishing_duplicate_of_pipeline_draft(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline = pipeline_builder.build('simple pipeline draft')
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
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


@pytest.fixture(scope="module")
def preview_pipeline(sch, snowflake_config):
    """A spcific pipeline to test preview end point"""
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    query = "select COLUMN1 as col1, COLUMN2 as col2 from values (1, 'one'), (2, 'two'), (3, 'three')"
    query_origin = pipeline_builder.add_stage('Snowflake Query', type='origin')
    query_origin.query = query

    filter_processor = pipeline_builder.add_stage('Filter')
    filter_processor.filter_by = "BY_SQL"
    filter_processor.where_clause = "col1 >= 3"

    trash = pipeline_builder.add_stage('Trash')
    query_origin >> filter_processor >> trash

    pipeline = pipeline_builder.build('sample_pipeline_{}'.format(get_random_string()))
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)

    try:
        yield pipeline
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
@pytest.mark.parametrize('push_limit_down', [True, False])
def test_get_pipeline_preview_end_limit(sch, preview_pipeline, push_limit_down):
    sch.publish_pipeline(preview_pipeline)
    preview = sch.run_pipeline_preview(preview_pipeline, batch_size=1, push_limit_down=push_limit_down).preview
    assert preview is not None
    assert preview.issues.issues_count == 0
    assert isinstance(preview, StPreview)
