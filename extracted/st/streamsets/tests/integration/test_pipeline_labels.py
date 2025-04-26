# Copyright 2022 StreamSets Inc.

# fmt: off
import uuid

from streamsets.sdk.sch_models import PipelineLabel
from streamsets.sdk.utils import SeekableList

# fmt: on


def test_create_pipeline_with_labels_logic(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline_name = 'create_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label = str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name, labels=[label])
    sch.publish_pipeline(pipeline)
    try:
        pipeline_labels = pipeline.labels
        assert len(pipeline_labels) == 1
        assert isinstance(pipeline_labels, SeekableList)
        assert isinstance(pipeline_labels[0], PipelineLabel)
        assert pipeline_labels[0].label == label
    finally:
        sch.delete_pipeline(pipeline)


def test_update_pipeline_with_labels_logic(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline_name = 'update_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label = str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name)
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


def test_remove_labels(sch, sch_authoring_sdc_id):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    dev_data_generator = pipeline_builder.add_stage('Dev Data Generator')
    trash = pipeline_builder.add_stage('Trash')
    dev_data_generator >> trash
    pipeline_name = 'create_pipeline_with_label_{}'.format(str(uuid.uuid4()))
    label1, label2 = str(uuid.uuid4()), str(uuid.uuid4())
    pipeline = pipeline_builder.build(title=pipeline_name, labels=[label1, label2])
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
