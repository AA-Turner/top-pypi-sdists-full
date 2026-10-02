"""Stdout reporter for local Appium runs.

Log shapes mirror the selenium and playwright siblings so HyperExecute worker logs
read the same across drivers:

    [TEST START] <name>
      [STEP 1] <description>
      [STEP 1] end name='<description>' status=passed auto_heal=False
    [TEST PASS] (N steps)
"""
import logging

_log = logging.getLogger("testmu_appium")


class LocalReporter:
    def __init__(self):
        self._driver = None
        self._step_num = 0

    def set_driver(self, driver) -> None:
        # Held for symmetry with LTReporter; the local reporter never drives it.
        self._driver = driver

    def begin_test(self, name: str) -> None:
        self._step_num = 0
        _log.info("[TEST START] %s", name)

    def pass_test(self) -> None:
        _log.info("[TEST PASS] (%d steps)", self._step_num)

    def fail_test(self, error) -> None:
        _log.error("[TEST FAIL] at step %d — %s", self._step_num, error)

    def begin_step(self, description, instruction_id=None) -> None:
        self._step_num += 1
        _log.info("  [STEP %d] %s", self._step_num, description)

    def end_step(self, description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None) -> None:
        if not ok:
            _log.error("  [STEP %d FAIL] %s", self._step_num, error)
        _log.info(
            "  [STEP %d] end name=%r status=%s auto_heal=%s%s",
            self._step_num, description, "passed" if ok else "failed", is_autohealed,
            f" autoheal_source={autoheal_source}" if autoheal_source else "",
        )

    def warn_step(self, description, error) -> None:
        _log.warning("  [STEP %d WARN] %s — %s", self._step_num, description, error)

    def attach_screenshot(self, data: bytes) -> None:
        _log.info("  [STEP %d] screenshot (%d bytes)", self._step_num, len(data or b""))
