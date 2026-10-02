"""LambdaTest mobile-session reporter.

Emits lambda hooks through ``driver.execute_script``. On an Appium session the hub
intercepts the script STRING (there is no JS engine on a native session to evaluate
it), so every hook is sent in the ``<hook-name>=<payload>`` body form — the same form
``lambda-status=passed`` uses.

Hooks emitted:
  - lambda-status=<passed|failed>        overall verdict
  - lambda-testCase-start=<json>         per-step start
  - lambda-testCase-end=<json>           per-step end, carrying is_autohealed /
                                         autoheal_source / interacted_element

Every event is ALSO logged to stdout: the hook calls alone are invisible in
HyperExecute logs.

Reporting must never mask a test result — a hook that raises is logged and dropped.
"""
import json
import logging

_log = logging.getLogger("testmu_appium")


class LTReporter:
    def __init__(self):
        self._driver = None
        self._step_num = 0

    def set_driver(self, driver) -> None:
        self._driver = driver

    def begin_test(self, name: str) -> None:
        self._step_num = 0
        _log.info("[TEST START] %s", name)

    def pass_test(self) -> None:
        _log.info("[TEST PASS] (%d steps)", self._step_num)
        self._hook("lambda-status", "passed")

    def fail_test(self, error) -> None:
        _log.error("[TEST FAIL] at step %d — %s", self._step_num, error)
        self._hook("lambda-status", "failed")

    def begin_step(self, description, instruction_id=None) -> None:
        self._step_num += 1
        _log.info("  [STEP %d] %s", self._step_num, description)
        args = {"name": description}
        if instruction_id:
            args["instructionId"] = instruction_id
        self._hook("lambda-testCase-start", json.dumps(args))

    def end_step(self, description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None) -> None:
        if not ok:
            _log.error("  [STEP %d FAIL] %s", self._step_num, error)
        args = {"name": description, "status": "passed" if ok else "failed"}
        if instruction_id:
            args["instructionId"] = instruction_id
        # Heal fields are omitted rather than sent false/empty: the dashboard reads
        # their presence as "this step was healed", and a blanket false on every step
        # would make the healed ones indistinguishable in aggregate queries.
        if is_autohealed:
            args["is_autohealed"] = True
            args["autoheal_source"] = autoheal_source
        if interacted_element:
            args["interacted_element"] = interacted_element
        self._hook("lambda-testCase-end", json.dumps(args))

    def warn_step(self, description, error) -> None:
        # Local log only — the WARN verdict is read from the authoring source.
        _log.warning("  [STEP %d WARN] %s — %s", self._step_num, description, error)

    def attach_screenshot(self, data: bytes) -> None:
        _log.info("  [STEP %d] screenshot (%d bytes)", self._step_num, len(data or b""))

    def _hook(self, name: str, payload: str) -> None:
        if self._driver is None:
            return
        try:
            self._driver.execute_script(f"{name}={payload}")
        except Exception as e:  # noqa: BLE001 — never propagate reporter errors
            _log.warning("[testmu] lambda hook %s failed: %s", name, e)
