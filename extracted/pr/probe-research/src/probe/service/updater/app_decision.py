"""the desktop app's own check: the service decides when, hands it to one app connection, and settles its result."""

from __future__ import annotations
import os
import time
from ...foundation.service_api.vocabularies import (
    AppCheckReason,
    AppReportIgnored,
    AppResult,
    AppStepOutcome,
    CheckOutcome,
    StepState,
    CheckTrigger,
    UpdateStep)
from ...foundation.service_api.wire import Method
from probe.service.updater.quiet.quiet import auto_update_enabled
from probe.service.updater.settings import CHECK_EVERY_S, log


class AppDecisionMixin:
    """Part of Updater: its methods run with `self` the Updater; compose() folds them into Updater."""

    # -- the desktop app's check (the service decides, the app's updater acts) --

    def _app_record(self, now: float | None = None) -> dict | None:
        """The last app check handed to the app (or reported by it), as it
        reads now: a delegation with no report past the timeout is failed."""
        record = self.state.get("app")
        if not isinstance(record, dict):
            return None
        out = dict(record)
        if out.get("state") == StepState.DELEGATED:
            at = out.get("delegated_at")
            now = time.time() if now is None else now
            if not isinstance(at, (int, float)) or not 0 <= now - at < self.app_result_timeout_s:
                out.update(self._timed_out(at))
        return out

    def _timed_out(self, delegated_at: object) -> dict:
        at = delegated_at if isinstance(delegated_at, (int, float)) else time.time()
        return {
            "state": StepState.FAILED,
            "result": AppResult.FAILED,
            "error": f"no result from the app within {int(self.app_result_timeout_s)} s",
            "timed_out": True,
            "at": at + self.app_result_timeout_s,
        }

    def app_decision(self, *, force: bool = False, now: float | None = None) -> dict:
        """`{due, reason}` (AppCheckReason): should the app check for its
        update now? Due when none was handed over within CHECK_EVERY_S, the
        last one failed (or never reported), or the app forces it."""
        now = time.time() if now is None else now
        record = self._app_record(now)
        if record is not None and record.get("state") in (StepState.DELEGATED, StepState.READY):
            # One check at a time, forced or not: this one has not reported
            # yet, or its downloaded update waits for the app to quit.
            return {"due": False, "reason": AppCheckReason.IN_PROGRESS}
        if force:
            return {"due": True, "reason": AppCheckReason.FORCED}
        if not auto_update_enabled(self.session_state_dirs()):
            return {"due": False, "reason": AppCheckReason.AUTO_UPDATE_OFF}
        last = self._number("last_app_check")
        if last is None:
            return {"due": True, "reason": AppCheckReason.NEVER_CHECKED}
        if record is not None and record.get("state") == StepState.FAILED:
            return {"due": True, "reason": AppCheckReason.LAST_FAILED}
        if not 0 <= now - last < CHECK_EVERY_S:
            return {"due": True, "reason": AppCheckReason.INTERVAL_PASSED}
        return {"due": False, "reason": AppCheckReason.CHECKED_RECENTLY}

    def app_public(self) -> dict:
        """`update.status`'s `app`: the decision as it stands, when a check was
        last handed over, how many open apps take `app.check`, and the last
        check's record (`last`: a delegation, or the app's report)."""
        now = time.time()
        return {
            **self.app_decision(now=now),
            "last_check": self._number("last_app_check"),
            "listening": self.app_listeners(),
            "last": self._app_record(now),
        }

    def _delegate(
        self, *, cycle_id: str | None, trigger: str, via: str, version: str | None = None, owner: int | None = None
    ) -> dict:
        """Hand the app its check: recorded (`last_app_check` too) before the
        app is told, so a check is never handed over unrecorded. `owner`: the
        app connection `app.check` goes to (None: the app's launch check,
        asked on a connection of its own; only the timeout bounds it)."""
        now = time.time()
        record = {
            "state": StepState.DELEGATED,
            "delegated_at": now,
            "cycle_id": cycle_id,
            "trigger": trigger,
            "via": via,
            "version": version,
            "owner": owner,
            #: Connections are numbered per service process: the owner is this one's.
            "owner_pid": os.getpid() if owner is not None else None,
        }
        self.state["app"] = record
        self.state["last_app_check"] = now
        self._save()
        self._arm_app_timeout(now)
        log(f"app check handed to the app ({via}, cycle {cycle_id})")
        return record

    def _arm_app_timeout(self, delegated_at: float) -> None:
        if self._loop is None:
            return
        if self._app_timer is not None:
            self._app_timer.cancel()
        delay = max(0.0, delegated_at + self.app_result_timeout_s - time.time())
        self._app_timer = self._loop.call_later(delay, self._app_timed_out, delegated_at)

    def app_gone(self, serial: int) -> None:
        """An app connection closed: the check it owned and never reported is
        failed (due again at the next ask; a late report still counts)."""
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.DELEGATED:
            return  # a `ready` check stays ready: the app quit to install it
        if record.get("owner") is None or record.get("owner") != serial or record.get("owner_pid") != os.getpid():
            return
        log("the app connection that had the update check closed before it reported")
        self._settle_app({**record, **self._owner_gone()})

    def _owner_left_with_the_old_service(self) -> None:
        """At start: a check sent to a connection of the service before this
        one, still unreported, lost that connection with it."""
        record = self.state.get("app")
        if (
            isinstance(record, dict)
            and record.get("state") == StepState.DELEGATED
            and record.get("owner") is not None
            and record.get("owner_pid") != os.getpid()
        ):
            self._settle_app({**record, **self._owner_gone()})

    def _owner_alive(self, record: dict) -> bool:
        owner = record.get("owner")
        return owner is not None and record.get("owner_pid") == os.getpid() and self.app_alive(owner)

    def _settle_ready_at_launch(self, version: str | None) -> None:
        """The app's launch check, with a downloaded update waiting (`ready`)
        and the app that downloaded it gone (it quit to install it): running
        the downloaded version, it was updated; anything else, the install did
        not happen, and the check is failed (due again). While that app is
        still open, nothing changes: it installs when it quits."""
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.READY or self._owner_alive(record):
            return
        now = time.time()
        ready = record.get("version_after")
        settled = {**record, "at": now, "reported_at": now, "settled_at_launch": True}
        if version is not None and version == ready:
            settled.update(state=StepState.DONE, result=AppResult.UPDATED, version_after=version, error=None)
            log(f"the app runs the downloaded {version}: updated")
        else:
            settled.update(
                state=StepState.FAILED,
                result=AppResult.FAILED,
                error=f"the app started at {version}, not the downloaded {ready}",
            )
            log(f"the app started at {version}, not the downloaded {ready}: due again")
        self._settle_app(settled)

    @staticmethod
    def _owner_gone() -> dict:
        return {
            "state": StepState.FAILED,
            "result": AppResult.FAILED,
            "error": "the app connection it was sent to closed before it reported",
            "owner_gone": True,
            "at": time.time(),
        }

    def _app_timed_out(self, delegated_at: float) -> None:
        """No report for this delegation: recorded as failed (due again)."""
        self._app_timer = None
        record = self.state.get("app")
        if not isinstance(record, dict) or record.get("state") != StepState.DELEGATED:
            return
        if record.get("delegated_at") != delegated_at:
            return
        record = {**record, **self._timed_out(delegated_at)}
        log(f"the app did not report its update check within {int(self.app_result_timeout_s)} s")
        self._settle_app(record)

    @staticmethod
    def _app_step(record: dict, outcome: str = AppStepOutcome.ALREADY_DELEGATED) -> dict:
        """A cycle's `app` step from the record: `{state, outcome, ...}`."""
        state = record.get("state")
        out: dict = {"state": state, "delegated_at": record.get("delegated_at")}
        if state == StepState.DELEGATED:
            out["outcome"] = outcome
            return out
        out["outcome"] = record.get("result")
        for key in ("version_before", "version_after", "error", "timed_out", "owner_gone"):
            if record.get(key) is not None:
                out[key] = record[key]
        return out

    def _settle_app(self, record: dict) -> None:
        """The app check's result (reported, or timed out): into the state
        file, the last cycle's `app` step when that was this delegation, and
        an `update.step` like every other step's. The check is over: its
        timeout no longer runs."""
        if self._app_timer is not None:
            self._app_timer.cancel()
            self._app_timer = None
        self.state["app"] = record
        last = self.state.get("last_result")
        steps = last.get("steps") if isinstance(last, dict) else None
        app = steps.get(UpdateStep.APP) if isinstance(steps, dict) else None
        delegated_at = record.get("delegated_at")
        if isinstance(app, dict) and delegated_at is not None and app.get("delegated_at") == delegated_at:
            steps[UpdateStep.APP] = self._app_step(record)
            last["ok"] = "error" not in steps and all(
                isinstance(s, dict) and s.get("state") != StepState.FAILED for s in steps.values()
            )
        self._save()
        step = self._app_step(record)
        self._step(record.get("cycle_id"), UpdateStep.APP, step.pop("state"), **step)

    def app_result(self, report: dict) -> dict:
        """`update.app_result` (`protocol.need_app_result`): what the app's
        own updater did, for the check its `cycle_id` names (none: the check
        in the app's hands now, as an older build reports). It answers that
        check while it has no report of its own: in the app's hands, timed
        out, or lost with its connection (a late report still counts). A
        `cycle_id` of an earlier check, or a second report of one, changes
        nothing (`recorded: false`, AppReportIgnored). `ready` (downloaded,
        installs at quit) stops the check's timeout and keeps it open for one
        final `updated` or `failed`. A report with no check at all (none was
        ever handed over here) is recorded as one made now."""
        now = time.time()
        record = self.state.get("app")
        record = record if isinstance(record, dict) else None
        cycle_id = report.get("cycle_id")
        ignored = None
        if record is not None and cycle_id is not None and cycle_id != record.get("cycle_id"):
            ignored = AppReportIgnored.STALE
        elif record is not None and record.get("reported_at") is not None:
            ignored = AppReportIgnored.DUPLICATE
        elif (
            record is not None
            and record.get("state") == StepState.READY
            and report["result"] not in (AppResult.UPDATED, AppResult.FAILED)
        ):
            ignored = AppReportIgnored.DUPLICATE  # after `ready`: one final updated or failed
        if ignored is not None:
            log(f"the app reported {report['result']}, not recorded ({ignored})")
            return {"recorded": False, "reason": ignored, "app": self.app_public()}
        if record is not None and (record.get("delegated_at") is not None or record.get("state") == StepState.READY):
            record = {k: v for k, v in record.items() if k not in ("timed_out", "owner_gone")}
        else:
            record = {
                "delegated_at": None,
                "cycle_id": cycle_id,
                "trigger": None,
                "via": None,
                "version": report.get("version_before"),
                "owner": None,
            }
            self.state["last_app_check"] = now
        result = report["result"]
        versions = {
            key: report[key] if report.get(key) is not None else record.get(key)
            for key in ("version_before", "version_after")
        }
        if result == AppResult.READY:
            # Downloaded and verified: no timeout now, and the check stays open
            # for one final report (no `reported_at` yet).
            record.update(state=StepState.READY, at=now, ready_at=now, result=result, error=None, **versions)
        else:
            failed = result == AppResult.FAILED
            record.update(
                state=StepState.FAILED if failed else StepState.DONE,
                at=now,
                reported_at=now,
                result=result,
                error=report.get("error"),
                **versions,
            )
        log(f"the app reported its update check: {result}")
        self._settle_app(record)
        return {"recorded": True, "app": self.app_public()}

    def _launch_check(self, app: dict, answer: dict) -> dict:
        """`update.check_now`'s `app` answer (the app's launch check):
        `{due, reason, cycle_id}`. Due: the check is the app's now, recorded
        as handed over (with the cycle this ask started or joined)."""
        self._settle_ready_at_launch(app.get("version"))
        decision = self.app_decision(force=bool(app.get("force")))
        cycle_id = answer.get("cycle_id") if answer.get("outcome") in (CheckOutcome.STARTED, CheckOutcome.RUNNING) else None
        if not decision["due"]:
            return {**decision, "cycle_id": None}
        self._delegate(cycle_id=cycle_id, trigger=CheckTrigger.APP, via=Method.UPDATE_CHECK_NOW, version=app.get("version"))
        return {**decision, "cycle_id": cycle_id}
