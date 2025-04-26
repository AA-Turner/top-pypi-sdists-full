#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

# fmt: off
import pytest

from streamsets.sdk.analytics import (
    FUNCTION_CALLS_HEADERS_KEY, INTERACTIVE_MODE_HEADERS_KEY, MAX_THRESHOLD, AnalyticsHeaders,
)

# fmt: on
DUMMY_VALUE = 'dummy value'


@pytest.fixture(scope="function")
def analytics_headers():
    headers = {FUNCTION_CALLS_HEADERS_KEY: None, INTERACTIVE_MODE_HEADERS_KEY: 'False'}
    return headers


def test_analytics_attribute_added_to_headers(sch_sdc_pipeline_builder, analytics_headers):
    pipeline_builder = sch_sdc_pipeline_builder
    analytics_instance = AnalyticsHeaders.get_instance()

    pipeline_builder.dummy_attribute1 = DUMMY_VALUE
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'PipelineBuilder.dummy_attribute1'
    assert analytics_instance.headers == analytics_headers

    # FUNCTION_CALLS_HEADERS_KEY is flushed after the function has been called.
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = None

    # Set another attribute to assert that dummy_attribute1 was flushed out
    pipeline_builder.dummy_attribute2 = DUMMY_VALUE
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'PipelineBuilder.dummy_attribute2'
    assert analytics_instance.headers == analytics_headers


def test_analytics_method_added_to_headers(sch_sdc_pipeline_builder, analytics_headers):
    pipeline_builder = sch_sdc_pipeline_builder
    analytics_instance = AnalyticsHeaders.get_instance()

    pipeline_builder.add_stage('Snowflake', type='destination')
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'PipelineBuilder.add_stage'
    assert analytics_instance.headers == analytics_headers


def test_analytics_property_added_to_headers(sch_sdc_pipeline, analytics_headers):
    pipeline = sch_sdc_pipeline
    analytics_instance = AnalyticsHeaders.get_instance()

    pipeline.name = DUMMY_VALUE
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'Pipeline.name'
    assert analytics_instance.headers == analytics_headers

    # FUNCTION_CALLS_HEADERS_KEY is flushed after the function has been called.
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = None

    pipeline.name
    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'Pipeline.name'
    assert analytics_instance.headers == analytics_headers


def test_analytics_resets_headers_if_called_more_than_threshold(sch_sdc_pipeline, analytics_headers):
    pipeline = sch_sdc_pipeline
    analytics_instance = AnalyticsHeaders.get_instance()

    for i in range(0, MAX_THRESHOLD + 1):
        pipeline.name

    analytics_headers[FUNCTION_CALLS_HEADERS_KEY] = 'Pipeline.name'
    assert analytics_instance.headers == analytics_headers
