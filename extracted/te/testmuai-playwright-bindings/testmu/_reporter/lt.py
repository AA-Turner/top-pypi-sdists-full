"""TestMu dashboard reporter (LambdaTest grid).

Uses page.evaluate('lambdatest_action: ...') for:
  - setTestStatus (overall test verdict)
  - lambda-testCase-start / lambda-testCase-end (per-step annotations on LT timeline)
  - lambda-element-bounds (ships element rect before an action so the
    per-step record gets coordinates)

All events are ALSO logged to stdout so HyperExecute console
shows progress — the CDP calls alone are invisible in HE logs.

The page reference is set by testmu.run() at session start.
"""

import json
import logging

from testmu import _configure

_log = logging.getLogger("testmu")


class LTReporter:
    def __init__(self):
        self._page = None
        self._step_num = 0

    def set_page(self, page):
        self._page = page

    async def begin_test(self, name):
        self._step_num = 0
        # A step-variable buffer left over from a previous test would be
        # attributed to this test's first step.
        from testmu._step_variables import reset_step_variables
        reset_step_variables()
        _log.info("[TEST START] %s", name)

    async def pass_test(self):
        _log.info("[TEST PASS] (%d steps)", self._step_num)
        await self._evaluate_action(
            "setTestStatus",
            {
                "status": "passed",
                "remark": "Test completed successfully",
            },
        )

    async def fail_test(self, error):
        _log.error("[TEST FAIL] at step %d — %s", self._step_num, error)
        await self._evaluate_action(
            "setTestStatus",
            {
                "status": "failed",
                "remark": str(error),
            },
        )

    async def begin_step(self, description, instruction_id=None):
        self._step_num += 1
        _log.info("  [STEP %d] %s", self._step_num, description)
        args = {"name": description}
        if instruction_id:
            args["instructionId"] = instruction_id
        # V4 pre-step URL: page.url here is the URL just before the step's
        # action runs (begin_step fires on step __aenter__). Read must never
        # fail the hook — a closed/navigating page just skips the field.
        # Key matches the host runtime's per-operation pre_action_url in test_summary.
        if _configure.get("kane_run_v4") and self._page is not None:
            try:
                args["pre_action_url"] = self._page.url
            except Exception:
                pass
        await self._evaluate_action("lambda-testCase-start", args)

    async def end_step(self, description, ok, error=None, instruction_id=None,
                       on_failure=None):
        if not ok:
            _log.error("  [STEP %d FAIL] %s", self._step_num, error)
        args = {"name": description, "status": "passed" if ok else "failed"}
        if instruction_id:
            args["instructionId"] = instruction_id
        # auto_heal: whether any action in this step fell to the heal cascade.
        from testmu._step import get_step_autoheal
        args["auto_heal"] = get_step_autoheal()
        # Report the values this step ran with, not just the names. The
        # buffer is DRAINED unconditionally (even when the hook itself is a no-op)
        # so one step's reads cannot leak into the next step's payload.
        from testmu._step_variables import pop_step_variables
        step_variables = pop_step_variables()
        if step_variables:
            args["variables"] = step_variables
            _log.info("  [STEP %d] variables=%s", self._step_num, sorted(step_variables))
        # Carry WHY a failed step failed so HPS can show the per-step
        # disposition. Only on a failure — meaningless for a passing step, and
        # the source omits it there too.
        if not ok:
            from testmu._step import wire_failure_condition
            wire_condition = wire_failure_condition(on_failure)
            if wire_condition:
                args["failure_condition"] = wire_condition
        await self._evaluate_action("lambda-testCase-end", args)

    async def warn_step(self, description, error):
        # Local log only — WARN verdict is read by FE from the authoring source.
        _log.warning("  [STEP %d WARN] %s — %s", self._step_num, description, error)

    async def send_element_bounds(self, bbox, instruction_id=None):
        """Ship element bounding rect for the next command's coordinates."""
        if not bbox:
            return
        args = {
            "x": bbox.get("x", 0),
            "y": bbox.get("y", 0),
            "width": bbox.get("width", 0),
            "height": bbox.get("height", 0),
        }
        if instruction_id:
            args["instructionId"] = instruction_id
        await self._evaluate_action("lambda-element-bounds", args)

    async def _evaluate_action(self, action, arguments):
        if self._page is None:
            return
        try:
            payload = json.dumps({"action": action, "arguments": arguments})
            await self._page.evaluate("_ => {}", f"lambdatest_action: {payload}")
        except Exception as e:
            _log.warning("lambdatest_action failed: %s", e)
