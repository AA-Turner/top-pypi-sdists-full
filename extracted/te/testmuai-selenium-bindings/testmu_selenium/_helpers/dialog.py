"""Driver-level JavaScript dialog handlers — accept / dismiss alerts, confirms, prompts.

Maps to V3 codegen handler:
- the js-dialog handler — testmu_selenium.handle_alert(driver, ...)

Dialogs are driver-scoped (no element resolution), so this follows the
_helpers/navigation.py pattern, not the _action_*.py + _ActionSpec pattern.
"""
from __future__ import annotations

import time

from selenium.common.exceptions import NoAlertPresentException


def handle_alert(driver, *, action: str = "accept", value: str = "",
                 max_attempts: int = 4, retry_delay: float = 0.5) -> None:
    """Respond to the currently-open JS dialog.

    Retries briefly on NoAlertPresentException — useful for dialogs that
    open a tick after the trigger event. Sleeps only BETWEEN attempts,
    not after the final failure. Total worst-case budget is
    (max_attempts - 1) * retry_delay.
    """
    for attempt in range(max_attempts):
        try:
            alert = driver.switch_to.alert
            if action == "accept":
                if value:
                    alert.send_keys(value)
                alert.accept()
            else:
                alert.dismiss()
            return
        except NoAlertPresentException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(retry_delay)


__all__ = ["handle_alert"]
