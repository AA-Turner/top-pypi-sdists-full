# Copyright 2024 StreamSets Inc.

# fmt: off
from streamsets.sdk.analytics import FUNCTION_CALLS_HEADERS_KEY, INTERACTIVE_MODE_HEADERS_KEY
from streamsets.sdk.utils import get_random_string

# fmt: on
START_TIME_2099 = 4200268800
END_TIME_2099 = 4200854400
UTC_TIME_Z0NE = 'UTC'
BASIC_CRON_TAB_MASK = '0/1 * 1/1 * ? *'


def test_analytics_headers_sent(sch):
    job_sequence_builder = sch.get_job_sequence_builder()
    job_sequence_builder.add_start_condition(START_TIME_2099, END_TIME_2099, UTC_TIME_Z0NE, BASIC_CRON_TAB_MASK)
    job_sequence = job_sequence_builder.build(
        name='Sequence {}'.format(get_random_string()), description='description {}'.format(get_random_string())
    )

    response = sch.publish_job_sequence(job_sequence)
    assert response.response.request.headers[FUNCTION_CALLS_HEADERS_KEY] == "ControlHub.publish_job_sequence"
    assert response.response.request.headers[INTERACTIVE_MODE_HEADERS_KEY] == 'False'

    # Assert that the old value aka 'ControlHub.publish_job_sequence' has been flushed and we only send the most
    # recent recorded value
    response = sch.check_snowflake_account_validation('dummy_value')
    assert (
        response.response.request.headers[FUNCTION_CALLS_HEADERS_KEY] == "ControlHub.check_snowflake_account_validation"
    )
    assert response.response.request.headers[INTERACTIVE_MODE_HEADERS_KEY] == 'False'
