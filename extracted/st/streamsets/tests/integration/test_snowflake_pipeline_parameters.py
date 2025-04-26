# Copyright 2022 StreamSets Inc.

# fmt: off
import pytest

# fmt: on


@pytest.mark.snowflake
def test_pipeline_parameters(sch, snowflake_config):
    try:
        pipeline_builder = sch.get_pipeline_builder(engine_type='snowflake')

        snowflake_table_name = 'com_streamsets_transformer_snowpark_origin_snowflake_table_TableDOrigin'
        snowflake_table = pipeline_builder.add_stage(name=snowflake_table_name).set_attributes(table='dinos')
        trash = pipeline_builder.add_stage('Trash')
        snowflake_table >> trash
        pipeline = pipeline_builder.build('pipeline_parameters_test_pipeline')
        pipeline.configuration['connectionString'] = snowflake_config['connectionString']
        pipeline.configuration['db'] = snowflake_config['db']
        pipeline.configuration['warehouse'] = snowflake_config['warehouse']
        pipeline.configuration['schema'] = snowflake_config['schema']
        sch.publish_pipeline(pipeline)

        # Set
        params = {'abc': '456', 'def': '123'}
        pipeline.parameters = params
        sch.publish_pipeline(pipeline)
        pipeline_new = sch.pipelines.get(pipeline_id=pipeline.pipeline_id)
        assert dict(pipeline_new.parameters) == params

        # Update
        params_to_be_updated = {'abc': '123', 'ghi': '123'}
        pipeline_new.parameters.update(params_to_be_updated)
        sch.publish_pipeline(pipeline_new)
        pipeline_new = sch.pipelines.get(pipeline_id=pipeline_new.pipeline_id)
        params.update(params_to_be_updated)
        assert dict(pipeline_new.parameters) == params
    finally:
        if pipeline:
            sch.delete_pipeline(pipeline)
