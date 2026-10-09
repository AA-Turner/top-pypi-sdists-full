"""HyperExecute test-run configuration loader.

On HyperExecute, parameterized tests get per-row values from a test-run
JSON file written by the HE runner. This module reads that file and
provides per-instance overrides for test_params and capabilities.

Ported from: capability.py load_config() template.
"""
import json
import logging
import os
import sys

_log = logging.getLogger("testmu")

_test_instance = None


def load_test_config() -> dict | None:
    """Load test instance config from HE test-run JSON.

    Returns the test instance dict if found, None otherwise.
    """
    global _test_instance

    # Already loaded
    if _test_instance is not None:
        return _test_instance

    file_path = None

    # Direct path from command line (sys.argv[7])
    if len(sys.argv) > 7:
        file_path = sys.argv[7]
    else:
        test_run_id = os.getenv("TEST_RUN_ID")
        if not test_run_id:
            _log.debug("No TEST_RUN_ID env var — skipping test config load")
            return None

        # Platform from sys.argv[4] or env or default
        platform = sys.argv[4] if len(sys.argv) > 4 else os.getenv("LT_PLATFORM", "linux")

        if "linux" in platform:
            file_path = f"/home/ltuser/foreman/ltuser/{test_run_id}.json"
        elif "mac" in platform:
            file_path = f"/Users/ltuser/foreman/ltuser/{test_run_id}.json"
        elif "win" in platform:
            file_path = f"D:/foreman/ltuser/{test_run_id}.json"
        else:
            _log.warning(f"Unsupported platform for test config: {platform}")
            return None

    if not file_path or not os.path.exists(file_path):
        _log.debug(f"Test config file not found: {file_path}")
        return None

    _log.info(f"Loading test config from {file_path}")

    try:
        test_instance_id = sys.argv[6] if len(sys.argv) > 6 else "1"
        platform = sys.argv[4] if len(sys.argv) > 4 else os.getenv("LT_PLATFORM", "linux")

        with open(file_path) as f:
            test_configs = json.load(f)

        test_instances = test_configs.get(platform, [])
        for instance in test_instances:
            if instance.get("test_instance_id") == test_instance_id:
                _log.info(f"Test instance found: {test_instance_id}")
                _test_instance = instance
                return _test_instance

        _log.warning(f"Test instance {test_instance_id} not found in config")
        return None

    except Exception as e:
        _log.warning(f"Failed to load test config: {e}")
        return None


def get_cap_value(cap_name: str, default=None):
    """Get capability value: test_config > env var > default.

    Matches the old get_cap_value(test_config, cap_name, default_value) pattern.
    """
    config = load_test_config()
    if config:
        val = config.get(cap_name.lower())
        if val is not None:
            return val
    env_val = os.getenv(cap_name)
    if env_val is not None:
        return env_val
    return default


def get_test_params_override() -> dict:
    """Get per-row test_params from the test-run JSON.

    Returns dict of param overrides, or empty dict if no config.
    """
    config = load_test_config()
    if config and config.get("test_params"):
        return {k: v for k, v in config["test_params"].items() if k != "_id"}
    return {}


def _reset():
    """Reset cached config (for testing)."""
    global _test_instance
    _test_instance = None
