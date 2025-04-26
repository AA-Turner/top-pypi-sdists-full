# Copyright 2022 StreamSets Inc.


def test_pipeline_parameters(sch, sch_authoring_sdc_id):
    try:
        pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
        dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
        trash = pipeline_builder.add_stage('Trash')
        dev_data_generator >> trash
        pipeline = pipeline_builder.build('pipeline_parameters_test_pipeline')

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
