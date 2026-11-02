"""UpdateStep for the desktop app: check at most once per interval, install over a closed app, sweep and recover swaps."""

from __future__ import annotations

import asyncio
import contextlib
import time
from pathlib import Path

from ..app import locate as appupdate
from ....foundation.service_api import paths
from ....foundation.service_api.vocabularies import (
    AppCheckReason,
    AppResult,
    AppStepOutcome,
    StepState,
    Topic,
    UpdateStep)
from probe.service.updater.settings import VIA_SERVICE_INSTALL, _installs_closed_app, log


class AppStepMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    async def _app(self, cycle_id: str, trigger: str) -> dict:
        """Step 2: the desktop app's update check, at most once per
        CHECK_EVERY_S, handed to the open app (`app.check`). Never launches
        the app: closed, on macOS the service installs its update itself
        (`_install_closed`); elsewhere there is no app."""
        step = UpdateStep.APP
        await self._sweep_closed()
        record = self._app_record()
        if record is not None and record.get("delegated_at") is not None and record.get("cycle_id") == cycle_id:
            # The app's launch check started this cycle and has its check already.
            out = self._app_step(record)
        else:
            decision = self.app_decision()
            if (
                record is not None
                and record.get("state") == StepState.READY
                and _installs_closed_app()
                and self.app_connected() == 0
                and not self._owner_alive(record)
                and (found := await asyncio.to_thread(appupdate.installed))
            ):
                # The app that downloaded an update quit without installing it (killed,
                # crashed): the service installs it now. The install looks for the app's
                # processes and lock itself; a skip leaves the `ready` record as it is.
                out = await self._install_closed(cycle_id, trigger, found)
            elif record is not None and record.get("state") == StepState.READY:
                # A downloaded update waits for the app to quit: no second check.
                out = {
                    "state": StepState.SKIPPED,
                    "outcome": AppStepOutcome.READY_WAITING,
                    **({"version_after": record["version_after"]} if record.get("version_after") else {}),
                }
            elif decision["reason"] == AppCheckReason.IN_PROGRESS and record is not None:
                out = self._app_step(record)
            elif not decision["due"]:
                out = {"state": StepState.SKIPPED, "outcome": decision["reason"]}
            elif (target := self.app_target()) is not None:
                # One app connection gets it (the newest) and owns it.
                record = self._delegate(cycle_id=cycle_id, trigger=trigger, via=Topic.APP_CHECK, owner=target)
                if self.send_app_check(target, {"cycle_id": cycle_id}):
                    out = self._app_step(record, AppStepOutcome.APP_CHECK_SENT)
                else:
                    self.app_gone(target)
                    out = self._app_step(self.state["app"])
            elif self.app_connected() > 0:
                # An older app build: it checks for its own update at its launch.
                out = {"state": StepState.SKIPPED, "outcome": AppStepOutcome.APP_NOT_LISTENING}
            else:
                found = await asyncio.to_thread(appupdate.installed)
                if found and _installs_closed_app():
                    out = await self._install_closed(cycle_id, trigger, found)
                else:
                    out = {
                        "state": StepState.SKIPPED,
                        "outcome": AppStepOutcome.APP_CLOSED if found else AppStepOutcome.NOT_INSTALLED,
                        **({"version": found["version"]} if found and found.get("version") else {}),
                    }
        detail = {k: v for k, v in out.items() if k != "state"}
        self._step(cycle_id, step, out["state"], **detail)
        return out

    async def _install_closed(self, cycle_id: str, trigger: str, found: dict) -> dict:
        """The app is installed and closed (no app connection; the install
        looks again for its processes and its instance lock): the service
        installs its update itself (`appinstall.install_closed`), starting no
        app process. Installed, current or failed is recorded as the app's
        check (`last_app_check` too: the next launch is not due, and a launch
        reports the version that is now in place); a skip records nothing, so
        the app's own updater checks at its next launch. A launch check that
        took the app's check while this ran keeps it: its record is not
        replaced."""
        from .. import app as appinstall

        now = time.time()
        refused = self._number("app_install_refused_at")
        if refused is not None and 0 <= now - refused < appinstall.REFUSED_BACKOFF_S:
            # Each refused try can show a macOS notification: not again for a while.
            return {"state": StepState.SKIPPED, "outcome": appinstall.Outcome.NOT_PERMITTED, "version": found.get("version")}
        self._step(cycle_id, UpdateStep.APP, StepState.STARTED, installing=True, version=found.get("version"))
        before = self.state.get("app")
        # Releases not downloaded again: one without the helper, and one whose helper
        # refused it for a reason that stays (for REFUSED_BACKOFF_S at most).
        no_helper = self.state.get("app_install_no_helper")
        if not isinstance(no_helper, dict):
            no_helper = None
        refused_release = self.state.get("app_install_refused_release")
        if not isinstance(refused_release, dict) or not (
            isinstance(refused_release.get("at"), (int, float))
            and 0 <= now - refused_release["at"] < appinstall.REFUSED_BACKOFF_S
        ):
            refused_release = None
        # An earlier install left an app that may not verify (its undo failed): sticky
        # until an install or a verified `current` clears it.
        broken = self.state.get("app_install_broken")
        result = await asyncio.to_thread(
            appinstall.install_closed,
            Path(found["app"]),
            home=paths.home(),
            skip_version=no_helper.get("version") if no_helper is not None else None,
            refused_version=refused_release.get("version") if refused_release is not None else None,
            repair=isinstance(broken, dict),
            log=log,
        )
        outcome = result.get("outcome")
        versions = {k: result[k] for k in ("version_before", "version_after") if result.get(k) is not None}
        latest = result.get("latest")
        for key in ("app_install_no_helper", "app_install_refused_release"):
            skipped = self.state.get(key)
            if isinstance(skipped, dict) and (
                outcome in (appinstall.Outcome.INSTALLED, appinstall.Outcome.CURRENT)
                or (isinstance(latest, str) and not appinstall.same_version(latest, str(skipped.get("version"))))
            ):
                # That release is in place or no longer the latest; a failure (the
                # manifest unread, say) says neither.
                self.state.pop(key, None)
                self._save()
        helper = result.get("helper") if isinstance(result.get("helper"), dict) else None
        if (
            outcome == appinstall.Outcome.FAILED
            and helper is not None
            and helper.get("result") == appinstall.HELPER_REFUSED
            and helper.get("reason") in appinstall.PERMANENT_REFUSALS
            and isinstance(latest, str)
        ):
            # The same release would be refused again: not downloaded every cycle.
            self.state["app_install_refused_release"] = {"version": latest, "reason": helper["reason"], "at": time.time()}
            self._save()
        if outcome in (appinstall.Outcome.INSTALLED, appinstall.Outcome.CURRENT):
            if self.state.pop("app_install_broken", None) is not None:
                self._save()
        elif (
            helper is not None
            and helper.get("undo_failed") is True
            and helper.get("reason") in appinstall.UNTRUSTED_AFTER_SWAP
        ):
            # The new app failed its checks after the swap and could not be swapped back:
            # it may be the app now. Never `current` while it fails codesign; repaired by
            # the next install, or by a reinstall.
            self.state["app_install_broken"] = {
                "reason": helper["reason"], "version": latest, "old": result.get("old_app"), "at": time.time(),
            }
            self._save()
        reinstall = isinstance(self.state.get("app_install_broken"), dict)
        if outcome in appinstall.SKIPS:
            if outcome == appinstall.Outcome.NOT_PERMITTED:
                self.state["app_install_refused_at"] = time.time()
                self._save()
            elif outcome == appinstall.Outcome.NO_HELPER and isinstance(result.get("latest"), str):
                # Not downloaded again for the same release; a newer one is looked at.
                self.state["app_install_no_helper"] = {"version": result["latest"], "at": time.time()}
                self._save()
            out = {"state": StepState.SKIPPED, "outcome": outcome, "version": found.get("version")}
            if result.get("detail"):
                out["detail"] = result["detail"]
            if helper is not None:
                out["helper"] = helper
            if reinstall:
                out["reinstall"] = True
            return out
        failed = outcome != appinstall.Outcome.INSTALLED and outcome != appinstall.Outcome.CURRENT
        out = {"state": StepState.FAILED if failed else StepState.DONE, "outcome": outcome, **versions}
        if result.get("error"):
            out["error"] = result["error"]
        if helper is not None:
            out["helper"] = helper  # the step event's too
        if reinstall:
            out["reinstall"] = True  # `probe doctor`: reinstall Probe
        if self.state.get("app") is not before:
            log("the app's launch check took its update check while the service installed: its record stays")
            return out
        at = time.time()
        self.state["app"] = {
            "state": out["state"],
            "delegated_at": None,
            "cycle_id": cycle_id,
            "trigger": trigger,
            "via": VIA_SERVICE_INSTALL,
            "version": result.get("version_before"),
            "owner": None,
            "at": at,
            "reported_at": at,
            # The app's own words for what happened (`AppResult`).
            "result": AppResult.FAILED if failed else (
                AppResult.UPDATED if outcome == appinstall.Outcome.INSTALLED else AppResult.CURRENT
            ),
            "version_before": result.get("version_before"),
            "version_after": result.get("version_after"),
            "error": result.get("error"),
            # What the release's helper answered (`result`, `reason`, `undo_failed`), when it ran.
            **({"helper": helper} if helper is not None else {}),
            **({"reinstall": True} if reinstall else {}),
        }
        self.state["last_app_check"] = at
        self.state.pop("app_install_refused_at", None)
        self._save()
        return out

    async def _sweep_closed(self) -> None:
        """Every cycle on macOS, before the app is looked for: a swap the
        release's helper left halfway is finished by that helper (`recover`:
        until then there is no app to find), then, with no app connected, what
        earlier installs left beside the bundle is removed (an old bundle by
        the installed app's own helper, once nothing runs from it)."""
        if not _installs_closed_app():
            return
        from .. import app as appinstall

        recovering = self._recovering
        if recovering is not None and not recovering.done():
            # The start-time recover first: a second helper run beside it finds the
            # app's instance lock held, and the app is looked for only after it.
            with contextlib.suppress(Exception):
                await asyncio.shield(recovering)
        connected = self.app_connected() > 0  # read on the loop, which owns it
        keep_old = isinstance(self.state.get("app_install_broken"), dict)

        def sweep() -> list:
            appinstall.recover(paths.home(), log=log)
            found = appupdate.installed()
            if not found or connected:
                return []
            return appinstall.sweep(Path(found["app"]), paths.home(), keep_old=keep_old)

        with contextlib.suppress(Exception):
            removed = await asyncio.to_thread(sweep)
            if removed:
                log(f"removed {', '.join(removed)} left beside the app by an earlier install")

    async def _recover_closed(self) -> None:
        """At service start (macOS): a swap the release's helper left halfway
        is finished before anything looks for the app."""
        from .. import app as appinstall

        with contextlib.suppress(Exception):
            await asyncio.to_thread(appinstall.recover, paths.home(), log=log)
