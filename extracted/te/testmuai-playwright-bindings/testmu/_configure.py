"""Generation-time configuration for testmu.

testmu.configure() is called at the top of generated test files to
pass values that were known when the test was generated (test name, build ID,
variables, chrome options, etc.) into the binding runtime.

This replaces the old pattern of baking values into capability.py
and test.py as string literals.
"""
import logging

_log = logging.getLogger("testmu")

# All config fields with defaults
_config_data = {
    "build": "",
    "name": "",
    "tc_id": "",
    "network": False,
    "devtools": {},
    "timezone": "",
    "chrome_options": [],
    "custom_headers": {},
    "multiple_profiles": False,
    "variables": {},
    "test_params": {},
    "global_variables": [],
    "uploaded_files": [],
    "environment_id": 0,
    "default_action_timeout_ms": 10000,
    "default_navigation_timeout_ms": 30000,
    # Opt-in marker — generated tests set this to True to enable kaneRunV4 +
    # preCmdVisual cap emission in _capability.py.
    "kane_run_v4": False,
    # Version selector for the heal cascade. Default "v4" preserves the existing autoheal path;
    # generated tests override via configure(kane_version="v3").
    "kane_version": "v4",
    # Locator auto-heal version gate. Default "" keeps the flat autoheal path;
    # generated tests set configure(auto_heal_version="AH2") to route failed
    # actions through the AX-tree locator heal. Read by _default_heal (mirrors
    # kane_version's global gate — set once, read via _configure.get).
    "auto_heal_version": "",
    # Instance-view cap opt-in: generated V3 tests set this so _capability.py emits
    # the kaneRunV3 LT:Options marker (parallel to V4's kane_run_v4).
    "kane_run_v3": False,
    # Vision/heal endpoint config — consumed by the vision payload
    # builders. Empty defaults are inert when kane_version != "v3".
    "automind_url": "",
    "code_export_id": "",
    "commit_id": "",
    "test_id": "",
    "org_id": "",
    "username": "",
    "accesskey": "",
    "session_id": "",
    "clipboard": False,
}

# Keys explicitly set via configure() — used to distinguish "not configured"
# from "configured to the default value" (important for bool fields).
_configured_keys: set = set()


def configure(**kwargs):
    """Set generation-time configuration values.

    Called once at the top of generated test files before @testmu.test.
    Values are consumed by _capability.py, _vars.py, and _session.py.
    """
    for key, value in kwargs.items():
        if key not in _config_data:
            _log.warning(f"testmu.configure: unknown key '{key}', ignoring")
            continue
        _config_data[key] = value
        _configured_keys.add(key)

    # Populate variable stores immediately
    from testmu._vars import set_var, _test_params, _global_variables
    for var_name, var_value in _config_data.get("variables", {}).items():
        set_var(var_name, var_value)
    _test_params.update(_config_data.get("test_params", {}))
    _global_variables.clear()
    _global_variables.extend(_config_data.get("global_variables", []))


def get(key, default=None):
    """Read a config value."""
    return _config_data.get(key, default)


def was_set(key) -> bool:
    """Return True if key was explicitly passed to configure()."""
    return key in _configured_keys


_DEFAULTS = {
    "build": "", "name": "", "tc_id": "", "network": False,
    "devtools": {},
    "timezone": "", "chrome_options": [], "custom_headers": {},
    "multiple_profiles": False, "variables": {}, "test_params": {},
    "global_variables": [], "uploaded_files": [], "environment_id": 0,
    "default_action_timeout_ms": 10000,
    "default_navigation_timeout_ms": 30000,
    "kane_run_v4": False,
    "kane_version": "v4",
    "auto_heal_version": "",
    "kane_run_v3": False,
    "automind_url": "", "code_export_id": "", "commit_id": "", "test_id": "",
    "org_id": "", "username": "", "accesskey": "", "session_id": "",
}


def _reset():
    """Reset all config and variable stores (for testing)."""
    for key in list(_config_data.keys()):
        default = _DEFAULTS.get(key)
        if isinstance(default, dict):
            _config_data[key] = {}
        elif isinstance(default, list):
            _config_data[key] = []
        else:
            _config_data[key] = default if default is not None else ""
    _configured_keys.clear()
    # Also reset variable stores populated by configure()
    from testmu._vars import _reset_store
    _reset_store()
