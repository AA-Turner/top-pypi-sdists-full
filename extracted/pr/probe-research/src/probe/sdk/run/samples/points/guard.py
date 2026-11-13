"""Fail open inside a framework's training loop: a per-sample metrics hook body that raises warns once per hook, is
counted, and never reaches training. What it costs is said truthfully: that update's per-sample metrics are missing
(the capture reads partial or not recorded); sample capture is untouched."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .....foundation.safe_warn import safe_warn as _diagnostics


class TrainingGuard:
    def __init__(self, framework: str) -> None:
        self.framework = framework
        self.failures = 0
        self._warned: set[str] = set()

    def call(self, what: str, function: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 -- fail open: a Probe error never stops training
            self.record_failure(what, exc)
            return None

    def record_failure(self, what: str, exc: BaseException) -> None:
        self.failures += 1
        if what in self._warned:
            return
        self._warned.add(what)
        _diagnostics.warn(
            f"probe: the {self.framework} adapter could not record {what} ({type(exc).__name__}: {exc}); training "
            "continues, and the per-sample training metrics of the updates it hit read as partial or not recorded. "
            "Later failures here are counted, not shown."
        )
