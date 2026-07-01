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

    async def end_step(self, description, ok, error=None, instruction_id=None):
        if not ok:
            _log.error("  [STEP %d FAIL] %s", self._step_num, error)
        args = {"name": description, "status": "passed" if ok else "failed"}
        if instruction_id:
            args["instructionId"] = instruction_id
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
