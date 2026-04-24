#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import uuid

import pytest

from streamsets.sdk.constants import SNOWFLAKE_STAGE_RENAME_ALIASES
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


@pytest.mark.snowflake
def test_stage_label_alias_logic(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    stage_name = 'Snowflake Table'
    stage_alias = 'Copo de Nieve'

    # Add a new alias for the stage
    SNOWFLAKE_STAGE_RENAME_ALIASES.update({stage_alias: stage_name})
    try:
        # Creating a stage using the new alias
        stage = pipeline_builder.add_stage(stage_alias, type='origin')
        # Assert the stage created corresponds to Snowflake Table stage.
        assert stage.stage_name == 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'

    finally:
        # Remove the new alias
        SNOWFLAKE_STAGE_RENAME_ALIASES.pop(stage_alias)

    # Test that calling the stage without the alias defined fails
    with pytest.raises(Exception):
        pipeline_builder.add_stage(stage_alias)


@pytest.mark.snowflake
def test_stage_label_alias(sch, snowflake_config):
    pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

    for alias, name in SNOWFLAKE_STAGE_RENAME_ALIASES.items():
        alias_stage = pipeline_builder.add_stage(alias)
        stage = pipeline_builder.add_stage(name)
        assert stage.stage_name == alias_stage.stage_name
