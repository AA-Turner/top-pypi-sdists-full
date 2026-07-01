"""Module-level config dictionary populated from env vars + configure() kwargs.

Public surface: testmu_selenium.configure(**kwargs) writes here; runtime modules read.

Two orthogonal flags drive the run() lifecycle (mirrors the playwright sibling):
- run_target: "local" (default) or "cloud". Only "cloud" connects to the LT hub
              via webdriver.Remote; "local" launches a direct webdriver.Chrome /
              webdriver.Firefox for dev iteration.
- lt_auth:    LT credentials present. Enables ATMS variable lookups, automind,
              file downloads, and other LT-backed features regardless of run target.
"""
import os
from typing import Any

# Run-target / auth flags — mirror the playwright sibling's env-var pattern.
# Read at module import; tests patch via `patch("testmu_selenium._config.run_target", ...)`.
run_target = os.getenv("TESTMU_RUN_TARGET", "local").lower()
lt_auth = bool(os.getenv("LT_USERNAME")) and bool(os.getenv("LT_ACCESS_KEY"))
smart = os.getenv("TESTMU_SMART", "1") == "1"

_PROD_AUTOMIND_URL = "https://kaneai-api.lambdatest.com"
_PROD_LT_HUB_URL = "https://hub.lambdatest.com/wd/hub"


def _resolve_automind_url() -> str:
    """Resolve automind_url with priority: AUTEUR_AUTOMIND > AUTOMIND_URL > prod default.

    Pure: reads env vars only and never writes os.environ. This is the single
    source of truth — _heal.Heal, _action_scroll_until_element and execute_db all
    call it so every automind request honors the same precedence without the
    binding mutating the host process environment.
    """
    resolved = (
        os.getenv("AUTEUR_AUTOMIND")
        or os.getenv("AUTOMIND_URL")
        or _PROD_AUTOMIND_URL
    )
    return resolved


def _resolve_lt_hub_url() -> str:
    """Resolve lt_hub_url with priority:

    1. Explicit LT_HUB_URL env var (wins unconditionally).
    2. Derived from HYE_HUB + LT_USERNAME + LT_ACCESS_KEY (only when all three
       are non-empty — avoids emitting malformed http://:@hub/wd/hub URLs).
    3. Prod default.
    """
    explicit = os.getenv("LT_HUB_URL")
    if explicit:
        return explicit

    hye_hub = os.getenv("HYE_HUB", "")
    username = os.getenv("LT_USERNAME", "")
    accesskey = os.getenv("LT_ACCESS_KEY", "")
    if hye_hub and username and accesskey:
        return f"http://{username}:{accesskey}@{hye_hub}/wd/hub"

    return _PROD_LT_HUB_URL


# Module-level config dict — populated by configure() at module-import time of generated test.py
_config: dict[str, Any] = {
    # Public (set by configure(**kwargs))
    "build": None,
    "name": None,
    "capability": None,
    "custom_capabilities": {},
    "test_metadata": {},

    # V2/V4 capability-parity metadata (set by configure(**kwargs))
    "tc_id": "",
    "network": False,
    "timezone": "",
    "chrome_options": [],
    "multiple_profiles": False,
    "custom_headers": {},

    # Heal timeouts — tunable
    "heal_timeout_per_tier_ms": int(os.getenv("HEAL_TIMEOUT_PER_TIER_MS", "30000")),
    "heal_timeout_total_ms": int(os.getenv("HEAL_TIMEOUT_TOTAL_MS", "90000")),

    # Identity (env-driven; host runtime can override at run() time)
    "username": os.getenv("LT_USERNAME", ""),
    "accesskey": os.getenv("LT_ACCESS_KEY", ""),
    "test_id": os.getenv("TEST_ID", ""),
    "commit_id": os.getenv("COMMIT_ID", ""),
    "org_id": int(os.getenv("ORG_ID", "0") or "0"),
    "automind_url": _resolve_automind_url(),
    "lt_hub_url": _resolve_lt_hub_url(),

    # Feature flags
    "smart": os.getenv("TESTMU_SMART", "1") == "1",
}


# Keys explicitly set via configure()/set_value() — distinguishes
# "configured to a falsy value" from "left at default" (needed for bool caps).
_configured_keys: set = set()


def get(key: str, default=None):
    """Read a config value. Used by other modules; not in __all__."""
    return _config.get(key, default)


def set_value(key: str, value):
    """Write a config value. Used by configure(); not public."""
    _config[key] = value
    _configured_keys.add(key)


def was_set(key: str) -> bool:
    """Return True if key was explicitly written via set_value()/configure()."""
    return key in _configured_keys
