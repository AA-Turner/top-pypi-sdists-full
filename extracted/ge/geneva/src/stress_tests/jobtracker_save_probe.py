# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Ray actor for the JobTracker save-path stress test.

Defined in its own importable module (not the test file) so Ray workers can
load the actor class by reference. A class defined in the pytest test module
pickles under a bare, non-importable module name and fails to import on workers.
"""

import asyncio

import ray

from geneva.runners.ray.jobtracker import _JobTracker


@ray.remote
class InjectedSaveJobTracker(_JobTracker):
    """JobTracker whose DB write is replaced with an injected delay/failure.

    Exercises the real ``enable_saves=True`` machinery (throttle -> schedule ->
    background save -> lock/backoff) without a system DB by overriding only the
    innermost write.
    """

    def configure_injected_save(self, delay_s: float, fail: bool) -> None:
        """Set the injected per-save delay and whether the save raises."""
        self._inj_delay = delay_s
        self._inj_fail = fail
        self._inj_attempts = 0

    async def _write_metrics(self, _metrics: dict[str, dict]) -> None:  # type: ignore[override]
        self._inj_attempts = getattr(self, "_inj_attempts", 0) + 1
        delay = getattr(self, "_inj_delay", 0.0)
        if delay:
            await asyncio.sleep(delay)
        if getattr(self, "_inj_fail", False):
            raise RuntimeError("injected save failure")

    def injected_save_attempts(self) -> int:
        """Number of times the (injected) write was attempted."""
        return getattr(self, "_inj_attempts", 0)
