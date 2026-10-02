"""Public testmu_appium.configure(**kwargs) — set test-time configuration."""
from typing import Any

from testmu_appium import _config as _config_mod
from testmu_appium._errors import TestmuConfigError

# Whitelist: unknown keys raise rather than warn-and-ignore, so a generator
# emitting a key this binding version does not understand fails at module import
# instead of silently dropping configuration.
_ALLOWED_KWARGS = {
    # Session identity / app under test
    "app_id", "platform", "udid", "target_kind",
    "device_name", "platform_version", "no_reset", "app",
    "appium_version",
    # Run metadata
    "build", "name", "capability", "custom_capabilities", "lt_options",
    "lt_options_fixed", "driver_settings", "test_metadata",
    # Version gates
    "kane_version", "kane_run_v4",
    # Timeouts
    "default_action_timeout_ms", "settle_timeout_ms", "heal_timeout_ms",
    "new_command_timeout_s",
    # Identity
    "username", "accesskey", "test_id", "commit_id", "org_id",
    "appium_url", "lt_hub_url", "ai_api_host", "automind_url",
    # Test-manager identity
    "tc_id", "environment_id", "uploaded_files",
    # Feature flags + recorded data bags
    "smart", "heal", "test_params", "variables", "global_variables",
    # Perception screenshot path
    "screenshot_source", "mjpeg_port",
    # iOS web surface: path to ios_webkit_debug_proxy when it is not on PATH
    # (a host agent knows its canonical location; a dev laptop rarely needs it).
    "iwdp_binary",
}


def configure(**kwargs: Any) -> None:
    """Set test-time configuration. Called at module-top of the generated test.py.

    Validates allowed kwargs; raises TestmuConfigError on unknown, conflicting or
    out-of-range values.
    """
    for key in kwargs:
        if key not in _ALLOWED_KWARGS:
            raise TestmuConfigError(
                f"unknown kwarg {key!r}; allowed: {sorted(_ALLOWED_KWARGS)}"
            )

    if "capability" in kwargs and "custom_capabilities" in kwargs:
        raise TestmuConfigError(
            "conflicting capability spec — use either capability= dict or "
            "custom_capabilities=, not both"
        )

    for dict_key in ("lt_options", "lt_options_fixed", "driver_settings"):
        if dict_key in kwargs and not isinstance(kwargs[dict_key], (dict, type(None))):
            raise TestmuConfigError(
                f"{dict_key} must be a dict; got {type(kwargs[dict_key]).__name__}"
            )

    if "platform" in kwargs:
        value = str(kwargs["platform"] or "").lower()
        if value not in _config_mod.KNOWN_PLATFORMS:
            raise TestmuConfigError(
                f"unknown platform {kwargs['platform']!r}; "
                f"allowed: {list(_config_mod.KNOWN_PLATFORMS)}"
            )
        kwargs["platform"] = value

    if "target_kind" in kwargs:
        value = str(kwargs["target_kind"] or "").lower()
        if value and value not in _config_mod.KNOWN_TARGET_KINDS:
            raise TestmuConfigError(
                f"unknown target_kind {kwargs['target_kind']!r}; "
                f"allowed: {list(_config_mod.KNOWN_TARGET_KINDS)} (or omit it)"
            )
        kwargs["target_kind"] = value

    if "screenshot_source" in kwargs:
        value = str(kwargs["screenshot_source"] or "").lower()
        if value not in _config_mod.SCREENSHOT_SOURCES:
            raise TestmuConfigError(
                f"unknown screenshot_source {kwargs['screenshot_source']!r}; "
                f"allowed: {list(_config_mod.SCREENSHOT_SOURCES)}"
            )
        kwargs["screenshot_source"] = value

    if "mjpeg_port" in kwargs:
        try:
            port = int(kwargs["mjpeg_port"])
        except (TypeError, ValueError) as exc:
            raise TestmuConfigError(
                f"mjpeg_port must be a port number; got {kwargs['mjpeg_port']!r}"
            ) from exc
        if not 1 <= port <= 65535:
            raise TestmuConfigError(f"mjpeg_port {port} is outside the port range")
        kwargs["mjpeg_port"] = port

    if "kane_version" in kwargs and str(kwargs["kane_version"]).lower() != "v4":
        raise TestmuConfigError(
            f"mobile export is v4-only; got kane_version={kwargs['kane_version']!r}"
        )

    # These three populate the _vars namespaces rather than the _config dict:
    # test_params backs ${name}, variables backs {{name}}, and global_variables is
    # the list the {{global.*}} resolver consults.
    from testmu_appium._vars import _global_variables, _test_params, _variable_store
    _test_params.update(kwargs.pop("test_params", {}) or {})
    _variable_store.update(kwargs.pop("variables", {}) or {})
    globals_value = kwargs.pop("global_variables", None)
    if globals_value:
        _global_variables.clear()
        _global_variables.extend(globals_value)

    for key, value in kwargs.items():
        _config_mod.set_value(key, value)

    # `smart` also lives as a module attribute, because that is what every gate in
    # the package reads through _config.smart_enabled(). `heal` rides the same
    # path for the same reason.
    if "smart" in kwargs:
        _config_mod.smart = bool(kwargs["smart"])
    if "heal" in kwargs:
        _config_mod.heal = bool(kwargs["heal"])
