"""the updater's saved state: last check, pending cycle, the installed version, when the next check is due."""

from __future__ import annotations
import contextlib
import json
import os
import time

from ...foundation.service_api import paths
from ...foundation.service_api.vocabularies import (
    AppResult,
    StepState,
    CHECK_TRIGGERS,
    UpdateStep)
from probe.service.updater.quiet.quiet import behind
from probe.service.updater.settings import CHECK_EVERY_S, FAILED_RETRY_S, STATE_VERSION


class StateMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    # -- state -----------------------------------------------------------------

    def _load(self) -> dict:
        try:
            data = json.loads(paths.update_state_path().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = None
        if data is None:
            # The first start in this machine's folder (plan D8): what the
            # service before the machine key recorded, so the schedule goes on
            # instead of starting a cycle at once.
            try:
                data = json.loads((paths.root_dir() / paths.UPDATE_STATE_NAME).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                data = None
        if not isinstance(data, dict) or data.get("v") != STATE_VERSION:
            data = {"v": STATE_VERSION}
        return data

    def _migrate_app_check(self) -> None:
        """A `last_app_check` the service before this one recorded (no `app`
        record beside it) counts only when that check found the app current
        or updated it: it was also written for an app it never checked
        (quarantined, not installed, not capable, a failed launch, no result
        in time), and read as a recent check those would hold the app's next
        launch check off for 6 h. The outcome is the last cycle's `app` step;
        anything else (or unknown) drops it, so the next launch is due."""
        if "app" in self.state or self._number("last_app_check") is None:
            return
        last = self.state.get("last_result")
        steps = last.get("steps") if isinstance(last, dict) else None
        step = steps.get(UpdateStep.APP) if isinstance(steps, dict) else None
        outcome = step.get("outcome") if isinstance(step, dict) else None
        if outcome not in (AppResult.UPDATED, AppResult.CURRENT):
            self.state.pop("last_app_check", None)
            return
        at = self._number("last_app_check")
        self.state["app"] = {
            "state": StepState.DONE,
            "delegated_at": None,
            "cycle_id": None,
            "trigger": None,
            "via": "background_update",  # the older service's hidden launch
            "version": step.get("version_before"),
            "at": at,
            "reported_at": at,
            "result": outcome,
            "version_before": step.get("version_before"),
            "version_after": step.get("version_after"),
            "error": None,
        }

    def _save(self) -> None:
        target = paths.update_state_path()
        tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
        try:
            with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
                json.dump(self.state, handle)
            os.replace(tmp, target)
        except OSError:
            pass
        finally:
            with contextlib.suppress(OSError):
                os.unlink(tmp)

    def _pending_on_disk(self) -> str | None:
        deferred = self.state.get("last_deferred")
        if not isinstance(deferred, dict):
            return None
        at, last = deferred.get("at"), self._number("last_check")
        if not isinstance(at, (int, float)) or (last is not None and at <= last):
            return None
        trigger = deferred.get("trigger")
        return trigger if trigger in CHECK_TRIGGERS else None

    def _number(self, key: str) -> float | None:
        value = self.state.get(key)
        return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None

    @property
    def last_check(self) -> float | None:
        return self._number("last_check")

    def interval(self) -> float:
        """From the last check to the next: CHECK_EVERY_S, or after cycles that
        ended not ok, FAILED_RETRY_S doubling with each one in a row."""
        streak = self.state.get("failed_in_a_row")
        if isinstance(streak, int) and not isinstance(streak, bool) and streak > 0:
            return float(min(CHECK_EVERY_S, FAILED_RETRY_S * 2 ** min(streak - 1, 16)))
        return float(CHECK_EVERY_S)

    def next_check(self) -> float | None:
        if self.in_progress():
            return None
        last = self.last_check
        return time.time() if last is None else last + self.interval()

    def due(self, now: float | None = None) -> bool:
        last = self.last_check
        now = time.time() if now is None else now
        return last is None or now - last >= self.interval() or now < last or self.moved_back()

    def installed_now(self) -> str | None:
        """The CLI version installed now: the one the CLI last recorded at its
        start (`runtime.json`'s `cli_version`, which a person's own `uv tool
        install` changes too), else this service's."""
        try:
            data = json.loads(paths.runtime_path().read_text(encoding="utf-8"))
            found = data.get("cli_version") if isinstance(data, dict) else None
        except (OSError, ValueError):
            found = None
        return found if isinstance(found, str) and found else self.version

    def moved_back(self) -> bool:
        """Did the CLI go BACK since the last check (`checked_cli`, the version
        installed when it ended)? A person's `uv tool uninstall` then an older
        `uv tool install` (plan R3): the last check is no answer for this
        install, so a check is due now and no ask waits out the cooldown. It
        took up to CHECK_EVERY_S (6 h) to reach the newest again."""
        checked = self.state.get("checked_cli")
        return isinstance(checked, str) and behind(self.installed_now(), checked) is True
