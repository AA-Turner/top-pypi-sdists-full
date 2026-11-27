from collections.abc import Callable, Iterator

import pytest

from mistralai.workflows.core.config.config import AppConfig, use_config
from mistralai.workflows.core.rate_limiting.rate_limit import (
    RateLimit,
    clear_rate_limit,
    get_rate_limit,
    set_rate_limit,
)
from mistralai.workflows.plugins.mistralai import _LLM_ACTIVITIES, configure_for_worker


def _llm_activities() -> list[Callable]:
    return list(_LLM_ACTIVITIES)


@pytest.fixture
def restore_llm_rate_limits() -> Iterator[None]:
    activities = _llm_activities()
    previous = {activity: get_rate_limit(activity) for activity in activities}
    yield
    for activity, rate_limit in previous.items():
        if rate_limit is None:
            clear_rate_limit(activity)
        else:
            set_rate_limit(activity, rate_limit)


def test_code_config_applies_rate_limit_after_plugin_import(restore_llm_rate_limits: None) -> None:
    activities = _llm_activities()
    runtime_config = AppConfig(
        worker={
            "agent": {
                "llm_rate_limit": {
                    "time_window_in_sec": 17,
                    "max_execution": 23,
                    "key": "runtime-llm-limit",
                }
            }
        }
    )

    with use_config(runtime_config):
        configure_for_worker([])

    for activity in activities:
        rate_limit = get_rate_limit(activity)
        assert rate_limit is not None
        assert rate_limit.time_window_in_sec == 17
        assert rate_limit.max_execution == 23
        assert rate_limit.key == "runtime-llm-limit"


def test_code_config_can_clear_import_time_rate_limit(restore_llm_rate_limits: None) -> None:
    activities = _llm_activities()
    import_time_limit = RateLimit(time_window_in_sec=29, max_execution=31, key="import-time-limit")
    for activity in activities:
        set_rate_limit(activity, import_time_limit)

    with use_config(AppConfig()):
        configure_for_worker([])

    assert all(get_rate_limit(activity) is None for activity in activities)
