"""Mid-test network throttling — replay of an authored throttle step.

Cloud-only grid hook (V2 parity: auteur-utils appium_uiActions
.execute_network_throttle): non-custom profiles ride
`updateNetworkProfile=<profile>`; profile "custom" sends the V2
`customNetworkProfile:{...}` body (colon separator — the hub parses the
script STRING; there is no JS engine on a native session). A 2s settle
matches V2. Session-level throttle is separate (test-config env)."""

import logging
import time

from testmu_appium import _config
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")


def network_throttle(driver, *, profile: str, download_kbps: int = 0,
                     upload_kbps: int = 0, latency_ms: int = 0,
                     description: str = "") -> None:
    suffix = f" — {description}" if description else ""
    resolved = str(var(profile))
    if not resolved:
        raise ValueError("network_throttle: profile resolved empty")
    if _config.run_target != "cloud":
        raise RuntimeError(
            "network_throttle runs through the LambdaTest grid hook and "
            "needs run_target='cloud'"
        )
    if resolved != "custom":
        driver.execute_script(f"updateNetworkProfile={resolved}")
    else:
        driver.execute_script(
            'customNetworkProfile:{ \\"downloadSpeed\\": %d,\\"uploadSpeed\\" : %d, \\"latency\\": %d }'
            % (int(download_kbps), int(upload_kbps), int(latency_ms))
        )
    time.sleep(2)  # V2 parity: settle before the next step observes the profile
    _log.info("network_throttle: %s%s", resolved, suffix)
