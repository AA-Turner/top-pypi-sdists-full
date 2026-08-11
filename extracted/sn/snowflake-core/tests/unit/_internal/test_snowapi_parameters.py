import pytest

from snowflake.core._internal.snowapi_parameters import SnowApiParameter, SnowApiParameters


VALUES = [
    ("true", True),
    ("TRUE", True),
    ("True", True),
    ("t", True),
    ("yes", True),
    ("y", True),
    ("on", True),
    ("any-other-value", False),
]


def test_max_threads():
    parameters = SnowApiParameters({SnowApiParameter.MAX_THREADS: "30"})
    assert parameters.max_threads == 30


def test_default_max_threads():
    parameters = SnowApiParameters({SnowApiParameter.MAX_THREADS: None})
    assert parameters.max_threads is None


@pytest.mark.parametrize(
    "flag",
    ("should_retry_request", "should_print_verbose_stack_trace", "fix_hostname", "should_skip_async_exec_polling"),
)
@pytest.mark.parametrize("value, expected", VALUES)
def test_flags(flag, value, expected):
    parameters = SnowApiParameters(
        {
            SnowApiParameter.USE_CLIENT_RETRY: value,
            SnowApiParameter.PRINT_VERBOSE_STACK_TRACE: value,
            SnowApiParameter.FIX_HOSTNAME: value,
            SnowApiParameter.SKIP_ASYNC_EXEC_POLLING: value,
        }
    )
    assert getattr(parameters, flag) is expected


def test_default_flags():
    parameters = SnowApiParameters({})
    assert parameters.should_retry_request is True
    assert parameters.should_print_verbose_stack_trace is True
    assert parameters.fix_hostname is True
    assert parameters.should_skip_async_exec_polling is True

    parameters = SnowApiParameters(
        {
            SnowApiParameter.USE_CLIENT_RETRY: None,
            SnowApiParameter.PRINT_VERBOSE_STACK_TRACE: None,
            SnowApiParameter.FIX_HOSTNAME: None,
            SnowApiParameter.SKIP_ASYNC_EXEC_POLLING: None,
        }
    )
    assert parameters.should_retry_request is True
    assert parameters.should_print_verbose_stack_trace is True
    assert parameters.fix_hostname is True
    assert parameters.should_skip_async_exec_polling is True
