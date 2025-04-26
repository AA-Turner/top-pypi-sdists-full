# Copyright 2022 StreamSets Inc.

# fmt: off
import uuid

import pytest

from streamsets.sdk.sch_models import PipelineLabel
from streamsets.sdk.utils import SeekableList

# fmt: on


@pytest.mark.snowflake
def test_create_pipeline_with_labels_logic(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline_name = 'create_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label = str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name, labels=[label])
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)
    try:
        pipeline_labels = pipeline.labels
        assert len(pipeline_labels) == 1
        assert isinstance(pipeline_labels, SeekableList)
        assert isinstance(pipeline_labels[0], PipelineLabel)
        assert pipeline_labels[0].label == label
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
def test_update_pipeline_with_labels_logic(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline_name = 'update_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label = str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name)
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)
    pipeline.add_label(label)
    sch.publish_pipeline(pipeline)
    try:
        pipeline_labels = pipeline.labels
        assert len(pipeline_labels) == 1
        assert isinstance(pipeline_labels, SeekableList)
        assert isinstance(pipeline_labels[0], PipelineLabel)
        assert pipeline_labels[0].label == label
    finally:
        sch.delete_pipeline(pipeline)


@pytest.mark.snowflake
def test_remove_labels(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
    snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
    trash = pipeline_builder.add_stage('Trash')
    snowflake_table >> trash
    pipeline_name = 'create_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label1, label2 = str(uuid.uuid4()), str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name, labels=[label1, label2])
    pipeline.configuration['connectionString'] = snowflake_config['connectionString']
    pipeline.configuration['db'] = snowflake_config['db']
    pipeline.configuration['warehouse'] = snowflake_config['warehouse']
    pipeline.configuration['schema'] = snowflake_config['schema']
    sch.publish_pipeline(pipeline)
    try:
        pipeline_labels = pipeline.labels
        assert len(pipeline_labels) == 2
        assert isinstance(pipeline_labels, SeekableList)
        assert isinstance(pipeline_labels[0], PipelineLabel)

        pipeline.remove_label(label1)
        sch.publish_pipeline(pipeline)

        pipeline_labels = pipeline.labels
        assert len(pipeline_labels) == 1
        assert isinstance(pipeline_labels, SeekableList)
        assert isinstance(pipeline_labels[0], PipelineLabel)
        assert pipeline_labels[0].label == label2
    finally:
        sch.delete_pipeline(pipeline)
