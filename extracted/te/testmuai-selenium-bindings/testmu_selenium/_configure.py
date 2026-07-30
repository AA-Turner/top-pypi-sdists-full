"""Public testmu_selenium.configure(**kwargs) — set test-time configuration."""
from typing import Any
from testmu_selenium._config import _config, set_value
from testmu_selenium._errors import TestmuConfigError


_ALLOWED_KWARGS = {
    "build", "name", "capability", "custom_capabilities", "test_metadata",
    "heal_timeout_per_tier_ms", "heal_timeout_total_ms",
    "username", "accesskey", "test_id", "commit_id", "org_id",
    "automind_url", "lt_hub_url", "smart", "test_params",
    # V2/V4 capability-parity metadata
    "tc_id", "network", "timezone", "chrome_options",
    "multiple_profiles", "custom_headers",
    # V3 instance-view opt-in: the generator sets kane_run_v3=True so build_capability emits kaneRunV3 + preCmdVisual.
    "kane_run_v3",
}


def configure(**kwargs: Any) -> None:
    """Set test-time configuration. Called at module-top of generated test.py.

    Validates allowed kwargs; raises TestmuConfigError on unknown or conflicting.
    """
    for key in kwargs:
        if key not in _ALLOWED_KWARGS:
            raise TestmuConfigError(
                f"unknown kwarg {key!r}; allowed: {sorted(_ALLOWED_KWARGS)}"
            )

    if "capability" in kwargs and "custom_capabilities" in kwargs:
        raise TestmuConfigError(
            "conflicting capability spec — use either capability= dict or custom_capabilities=, not both"
        )

    # test_params populates the _vars._test_params namespace (for ${name}
    # resolution), not the _config dict consumed by set_value.
    from testmu_selenium._vars import _test_params
    _test_params.update(kwargs.pop("test_params", {}) or {})

    for key, value in kwargs.items():
        set_value(key, value)
