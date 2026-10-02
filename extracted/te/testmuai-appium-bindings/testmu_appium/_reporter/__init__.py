"""Sync Reporter protocol and factory.

Three implementations:
- LTReporter:    LambdaTest mobile session reporter; emits lambda hooks through
                 driver.execute_script and mirrors every event to stdout.
- LocalReporter: stdout only (local Appium runs — there is no cloud session to annotate).
- NullReporter:  available for embedding the binding without any reporting.

Picking rule: LTReporter only when run_target == "cloud". The hooks are intercepted
grid-side, so a local Appium session always uses LocalReporter even with credentials
present.

The surface is sync throughout. Two fields this Protocol carries that no web binding
emits — `is_autohealed`/`autoheal_source` on end_step, and the interacted-element
payload — are the mobile telemetry contract that replay-diff reads.
"""
from typing import Optional, Protocol

from testmu_appium import _config


class Reporter(Protocol):
    def set_driver(self, driver) -> None: ...
    def begin_test(self, name: str) -> None: ...
    def pass_test(self) -> None: ...
    def fail_test(self, error: BaseException) -> None: ...
    def begin_step(self, description: str, instruction_id: Optional[str] = None) -> None: ...
    def end_step(
        self,
        description: str,
        ok: bool,
        error: Optional[BaseException] = None,
        instruction_id: Optional[str] = None,
        is_autohealed: bool = False,
        autoheal_source: str = "",
        interacted_element: Optional[dict] = None,
    ) -> None: ...
    def warn_step(self, description: str, error: BaseException) -> None: ...
    def attach_screenshot(self, data: bytes) -> None: ...


class NullReporter:
    """No-op reporter. Every method is a sink."""

    def set_driver(self, driver) -> None: pass
    def begin_test(self, name: str) -> None: pass
    def pass_test(self) -> None: pass
    def fail_test(self, error: BaseException) -> None: pass
    def begin_step(self, description: str, instruction_id: Optional[str] = None) -> None: pass

    def end_step(self, description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None) -> None:
        pass

    def warn_step(self, description: str, error: BaseException) -> None: pass
    def attach_screenshot(self, data: bytes) -> None: pass


def get_reporter() -> Reporter:
    """Factory: pick the reporter based on run target."""
    if _config.run_target == "cloud":
        from testmu_appium._reporter.lt import LTReporter

        return LTReporter()
    from testmu_appium._reporter.local import LocalReporter

    return LocalReporter()


_reporter: Optional[Reporter] = None


def reporter() -> Reporter:
    global _reporter
    if _reporter is None:
        _reporter = get_reporter()
    return _reporter


def _reset_reporter() -> None:
    """Reset the reporter singleton (session start; tests)."""
    global _reporter
    _reporter = None


from testmu_appium._reporter.local import LocalReporter  # noqa: E402
from testmu_appium._reporter.lt import LTReporter  # noqa: E402

__all__ = [
    "Reporter", "NullReporter", "LocalReporter", "LTReporter",
    "get_reporter", "reporter", "_reset_reporter",
]
