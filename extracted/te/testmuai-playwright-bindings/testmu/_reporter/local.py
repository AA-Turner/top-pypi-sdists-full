"""Local stdout reporter."""
import logging

_log = logging.getLogger("testmu")


class LocalReporter:
    def __init__(self):
        self._step_num = 0

    async def begin_test(self, name):
        self._step_num = 0
        _log.info("[TEST START] %s", name)

    async def pass_test(self):
        _log.info("[TEST PASS] (%d steps)", self._step_num)

    async def fail_test(self, error):
        _log.error("[TEST FAIL] at step %d — %s", self._step_num, error)

    async def begin_step(self, description, instruction_id=None):
        self._step_num += 1
        iid_part = f" [iid={instruction_id}]" if instruction_id else ""
        _log.info("  [STEP %d]%s %s", self._step_num, iid_part, description)

    async def end_step(self, description, ok, error=None, instruction_id=None):
        if not ok:
            _log.error("  [STEP %d FAIL] %s", self._step_num, error)

    async def warn_step(self, description, error):
        _log.warning("  [STEP %d WARN] %s — %s", self._step_num, description, error)

    async def send_element_bounds(self, bbox, instruction_id=None):
        if bbox:
            _log.debug(
                "  [BOUNDS] x=%s y=%s w=%s h=%s iid=%s",
                bbox.get("x"), bbox.get("y"), bbox.get("width"), bbox.get("height"),
                instruction_id,
            )

    # async def attach_screenshot(self, data):
    #     # Stub — screenshot bytes aren't uploaded anywhere.
    #     _log.info("  [SCREENSHOT] %d bytes", len(data))
