# Copyright 2024 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.exceptions import EnginelessError
from streamsets.sdk.utils import get_random_string

# fmt: on


def test_default_engineless_pipeline(sch):
    pipeline_builder = sch.get_pipeline_builder()
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    trash = pipeline_builder.add_stage('Trash')
    dev_raw_data_source >> trash
    pipeline = pipeline_builder.build("Engineless_Pipeline_{}".format(get_random_string()))
    with pytest.raises(EnginelessError):
        sch.publish_pipeline(pipeline)
    sch.delete_pipeline(pipeline)


def test_versioned_engineless_pipeline(sch):
    pipeline_builder = sch.get_pipeline_builder(engine_version_id="DC:5.6.2::Released")
    dev_raw_data_source = pipeline_builder.add_stage('Dev Raw Data Source')
    trash = pipeline_builder.add_stage('Trash')
    dev_raw_data_source >> trash
    pipeline = pipeline_builder.build("Engineless_Pipeline_{}".format(get_random_string()))
    with pytest.raises(EnginelessError):
        sch.publish_pipeline(pipeline)
    sch.delete_pipeline(pipeline)
