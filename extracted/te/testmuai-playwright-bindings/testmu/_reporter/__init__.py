"""Reporter protocol and factory.

Two implementations:
- LocalReporter: logs to stdout (used for local runs)
- LTReporter:    TestMu dashboard reporter via the lambdatest_action CDP channel (cloud only)

Picking rule: LTReporter only when run_target == "cloud". The cloud reporter
talks via the lambdatest_action CDP channel which is intercepted by the
LambdaTest grid server-side, so a local browser always uses LocalReporter
even when credentials are present.

Per-step extensions:
  - begin_step / end_step accept an optional ``instruction_id`` so the
    dashboard can group commands per step.
  - ``send_element_bounds`` ships the element rect from the binding via
    the ``lambda-element-bounds`` action verb so the per-step record
    picks up coordinates on the Playwright wire path that doesn't
    otherwise expose element rects.
"""

from typing import Optional, Protocol

from testmu import _config


class Reporter(Protocol):
    async def begin_test(self, name: str) -> None: ...
    async def pass_test(self) -> None: ...
    async def fail_test(self, error: Exception) -> None: ...
    async def begin_step(
        self, description: str, instruction_id: Optional[str] = None
    ) -> None: ...
    async def end_step(
        self,
        description: str,
        ok: bool,
        error: Optional[Exception] = None,
        instruction_id: Optional[str] = None,
    ) -> None: ...
    async def warn_step(self, description: str, error: BaseException) -> None: ...
    async def send_element_bounds(
        self, bbox: dict, instruction_id: Optional[str] = None
    ) -> None: ...
    async def attach_screenshot(self, data: bytes) -> None: ...


def get_reporter() -> Reporter:
    """Factory: pick reporter based on run target."""
    if _config.run_target == "cloud":
        from testmu._reporter.lt import LTReporter

        return LTReporter()
    from testmu._reporter.local import LocalReporter

    return LocalReporter()


_reporter: Optional[Reporter] = None


def reporter() -> Reporter:
    global _reporter
    if _reporter is None:
        _reporter = get_reporter()
    return _reporter


def _reset_reporter():
    """Reset reporter singleton (for testing)."""
    global _reporter
    _reporter = None
