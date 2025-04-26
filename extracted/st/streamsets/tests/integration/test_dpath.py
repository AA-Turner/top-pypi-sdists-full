# Copyright 2022 StreamSets Inc.

# fmt: off
from streamsets.sdk.sdc import DataCollector

# fmt: on


def test_get_field_data(sch, sch_authoring_sdc):
    # Test Record.get_field_data where dpath is used
    # Since we only support snapshot, where dpath is used, on only non SCH DataCollector, we construct it here
    sdc_executor = DataCollector(server_url=sch_authoring_sdc.engine_url, control_hub=sch, sdc_id=sch_authoring_sdc.id)

    pipeline_builder = sdc_executor.get_pipeline_builder()
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    # we add a bit of a delay so as we do not overwhelm the SDC instance
    dev_data_generator.set_attributes(
        fields_to_generate=[{'type': 'STRING', 'field': 'stringField'}], batch_size=1, delay_between_batches=10
    )
    # SDK does not yet support header attributes via get_field_* but if it were, we would add header attributes as:
    # dev_data_generator.header_attributes = [
    #     {'key': 'header_name', 'value': 'header value'}
    # ]
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline = pipeline_builder.build('testing get_field_data')

    sdc_executor.add_pipeline(pipeline)
    try:
        snapshot = sdc_executor.capture_snapshot(pipeline, start_pipeline=True).snapshot
        assert isinstance(snapshot[pipeline.origin_stage].output[0].get_field_data('/stringField').value, str)
    finally:
        sdc_executor.stop_pipeline(pipeline)
