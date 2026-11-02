"""TakeoverMixin, Client's methods: reopen a run and take over from an incumbent that went silent,
within the takeover budget (twin: app/runs)."""

from __future__ import annotations
import os
import sys
import time
import uuid
from ..... import agent_session
from ......foundation.safe_warn import safe_warn as _diagnostics

from ..... import errors

from ......foundation.request_identity.surface import Surface
from probe.sdk.routes import WriteOp, path_for


#: SDK reliability 2.3, requeue takeover. How long a relaunch waits for a
#: `running` incumbent to go silent before taking it over, and how long it spends
#: first delivering what the incumbent left queued in this outbox.
_TAKEOVER_WAIT_SECONDS = 300.0
#: The server's bounds on `takeover_stale_after_seconds`.
_TAKEOVER_MIN_SILENCE = 180
_TAKEOVER_MAX_SILENCE = 3600


def _env_seconds(name: str, default: float) -> float:
    """A non-negative seconds budget from the environment; malformed warns."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return max(0.0, float(raw))
    except ValueError:
        _diagnostics.warn(f"ignoring malformed {name}={raw!r}; expected seconds as a number")
        return default


def _takeover_wait_budget() -> float:
    """``PROBE_TAKEOVER_WAIT_SEC`` (300). A notebook cell never blocks for
    minutes on its own: under ipykernel the default is 0, so a live incumbent
    conflicts at once unless the variable asks for a wait."""
    default = 0.0 if "ipykernel" in sys.modules else _TAKEOVER_WAIT_SECONDS
    return _env_seconds("PROBE_TAKEOVER_WAIT_SEC", default)


def _takeover_threshold() -> int:
    """Silence that proves an incumbent dead: three of OUR beat intervals (a
    live one beats at least that often), never under the server's floor."""
    from .....run.closing.heartbeat import _heartbeat_interval

    import math

    interval = _heartbeat_interval()
    wanted = math.ceil(3 * interval) if interval > 0 else 0
    return int(min(_TAKEOVER_MAX_SILENCE, max(_TAKEOVER_MIN_SILENCE, wanted)))


def _takeover_sleep(seconds: float) -> None:
    """The wait between takeover attempts, by a name tests can replace."""
    time.sleep(seconds)


class TakeoverMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _reopen_taking_over(
        self,
        old: dict,
        session_id: str,
        rewind_to_step: int | None,
        *,
        heartbeat: bool | None = None,
        launcher: bool = False,
        writer: dict | None = None,
    ) -> dict:
        """Reopen a `running` incumbent once the server judges it silent.

        The server answers a not-yet-silent incumbent with 409 +
        ``retry_after_seconds``. Wait that long while it fits the remaining
        budget, one stderr line in all, and retry with the SAME session (the
        reopen is idempotent by session). The budget is ``PROBE_TAKEOVER_WAIT_SEC``
        (300; 0 in a notebook), and whenever it allows any wait it covers at
        least one full threshold plus slack, or a relaunch seconds after the
        death could never succeed. A live duplicate therefore waits out the
        budget and then conflicts: at the first 409 a pod dead for seconds and
        a live one look exactly alike."""
        threshold = _takeover_threshold()
        budget = _takeover_wait_budget()
        if budget > 0:
            budget = max(budget, threshold + _TAKEOVER_BUDGET_SLACK_SECONDS)
        started = time.monotonic()
        waited = 0.0  # what the budget has paid in waits, whatever the clock says
        announced = False
        name = old.get("slug") or old.get("id")
        while True:
            try:
                return self.reopen_run(
                    old["id"],
                    session_id=session_id,
                    rewind_to_step=rewind_to_step,
                    takeover_stale_after_seconds=threshold,
                    heartbeat=heartbeat,
                    launcher=launcher,
                    writer=writer,
                )
            except errors.ConflictError as exc:
                detail = exc.detail if isinstance(exc.detail, dict) else {}
                retry_after = detail.get("retry_after_seconds")
                if not isinstance(retry_after, (int, float)) or isinstance(retry_after, bool):
                    raise
                spent = max(time.monotonic() - started, waited)
                if retry_after > budget - spent:
                    raise errors.ConflictError(
                        f"run {name} is running and its writer may still be alive: "
                        f"the server can hand it over in {int(retry_after)}s, past "
                        f"this relaunch's wait budget ({budget:g}s, "
                        "PROBE_TAKEOVER_WAIT_SEC). If it is a live duplicate, stop "
                        'it; otherwise relaunch later, or use on_conflict="supersede".',
                        detail=exc.detail,
                    ) from exc
                if not announced:
                    announced = True
                    _diagnostics.warn(
                        f"probe: run {name} still reads running. Taking it over once "
                        "its writer has been silent long enough: waiting up to "
                        f"{budget:g}s (PROBE_TAKEOVER_WAIT_SEC)."
                    )
                _takeover_sleep(float(retry_after))
                waited += float(retry_after)

    def reopen_run(
        self,
        run_id: str,
        *,
        session_id: str,
        rewind_to_step: int | None = None,
        keep_epoch: bool = False,
        expected_write_epoch: int | None = None,
        takeover_stale_after_seconds: int | None = None,
        heartbeat: bool | None = None,
        launcher: bool = False,
        writer: dict | None = None,
    ) -> dict:
        """``POST /v1/runs/{id}/reopen`` — flip a dead run back to running.

        Returns the reopen receipt: the updated row plus ``write_epoch`` and
        ``last_step``. The caller just resolved the run, so a 404 here is the
        ROUTE missing, not the run — a backend that predates reopen
        (research-os#364) — and is translated into the actionable message
        rather than passed through as \"run not found\".

        ``keep_epoch`` + ``expected_write_epoch`` (SDK reliability 1.1) are
        SELF-recovery: the same attempt coming back after the reaper crashed
        it during an outage. The server keeps the epoch instead of bumping it,
        and only for a ``crashed`` row still on ``expected_write_epoch``;
        anything else is a 409. A server predating it silently ignores both
        fields and bumps, so check ``supports_feature("run_reopen_keep_epoch")``
        first."""
        try:
            body: dict = {"session_id": session_id}
            if rewind_to_step is not None:
                body["rewind_to_step"] = rewind_to_step
            if keep_epoch:
                body["keep_epoch"] = True
                body["expected_write_epoch"] = expected_write_epoch
            if takeover_stale_after_seconds is not None:
                # 2.3: only after `supports_feature("run_reopen_takeover")`; an
                # older server drops it and refuses the running run as before.
                body["takeover_stale_after_seconds"] = int(takeover_stale_after_seconds)
                if heartbeat is not None:
                    # How THIS attempt will be alive, so the server re-derives
                    # the run's liveness mode the takeover resets (2.2's
                    # writer-gone needs `in-process`). Ignored by older servers.
                    body["heartbeat"] = bool(heartbeat)
                    body["launcher"] = bool(launcher)
            if writer is not None:
                # 2.8: the reopening process's lease, written in the reopen's
                # transaction under the receipt's epoch (ignored on a run that
                # is not `leases`). Only after `run_writer_leases`.
                body["writer"] = writer
            # A large rewind legitimately outlasts the 30s default (measured:
            # ~34s for 2.5M points), and the route is idempotent by session_id
            # so even a timeout here is safely retryable — but not needing the
            # retry is better than surviving it.
            resp = self.transport.request(
                "POST",
                f"/v1/runs/{run_id}/reopen",
                json_body=body,
                # The route is idempotent BY SESSION (a replay returns the
                # committed receipt, no second epoch bump or delete), and this
                # body carries a fixed session_id — so the transport may
                # safely retry a lost response. Without this, a timeout after
                # the server committed left the run running-but-unowned, and
                # every later relaunch 409'd: the wedge the replay exists for.
                idempotent=True,
                timeout=180.0 if rewind_to_step is not None else None,
            )
            return resp.json() if resp.content else None
        except errors.NotFoundError as exc:
            raise errors.NotFoundError(
                "this backend predates run reopen (research-os#364): upgrade "
                'the server, or relaunch with on_conflict="supersede"'
            ) from exc

    def _reopen_for_attach(self, data: dict, *, session_id: str | None) -> dict:
        """Make `data` a row this process can actually write to, or raise.

        Four cases, and the distinctions are the whole point:

        * already 'running' -- nothing to do. This is also the MULTI-RANK case:
          eight DDP workers read the same PROBE_RUN_ID, the first reopens, and
          the other seven arrive here to find it live. That is success, not a
          race to lose; treating it as an error would kill every rank but one
          at import and leave a run that looks tracked because rank 0 attached.
        * 'created', 'untracked' or 'crashed' inside the age window -- reopen.
          A queued job reaching its run after the sweep rejoins instead of
          beating into a silent no-op forever, and a requeued one continues the
          run its killed attempt left `crashed`. So is a 'failed' that the
          SIGTERM close wrote (`probe_finish.reason` 'preempted', #2119): a
          scheduler's stop, which is how `scontrol requeue` ends the attempt
          it is about to start again with the same PROBE_RUN_ID.
        * any other 'failed' / 'canceled' / anything past the window -- raise,
          naming the run and when it ended. Somebody chose that ending.
        * reopen refused because a concurrent attach won -- re-read and accept
          the live row, same reasoning as the first case.
        """
        status = data.get("status")
        if status == "running":
            return data
        run_id = data["id"]
        if status not in self._REOPENABLE_ON_ATTACH and not self._ended_by_preemption(data):
            raise errors.ConflictError(
                f"run {data.get('slug') or run_id} is {status!r} and will not be "
                f"reopened by attach (ended {data.get('ended_at')!r}). Something "
                "chose that ending. If PROBE_RUN_ID is left over from an earlier "
                "job, clear it; to deliberately continue this run, reopen it "
                "explicitly with `probe run reopen`."
            )
        ended_at = data.get("ended_at")
        if ended_at and self._older_than_reopen_window(ended_at):
            raise errors.ConflictError(
                f"run {data.get('slug') or run_id} ended at {ended_at}, past the "
                f"{self._REOPEN_MAX_AGE_SECONDS // 3600}h window attach will adopt. "
                "A run id this old in the environment is far more likely to be "
                "stale than intended; clear PROBE_RUN_ID or reopen explicitly."
            )
        if status == "created":
            # 'created' is not a DEAD run, so /reopen refuses it (its reopenable
            # set is the four terminal verdicts). It was never started -- the
            # honest transition is a plain status PATCH, and it needs no epoch
            # bump because no earlier attempt wrote anything to supersede.
            self.transport.request("PATCH", path_for(WriteOp.RUN_PATCH, run_id), json_body={"status": "running"})
            return self.get_run(run_id)
        try:
            receipt = self.reopen_run(run_id, session_id=session_id or str(uuid.uuid4()))
        except errors.ConflictError:
            # Lost the race to a sibling rank. Whatever it did, the row is live
            # now -- re-read and use it rather than dying on a door someone else
            # already opened.
            fresh = self.get_run(run_id)
            if fresh.get("status") == "running":
                return fresh
            raise
        row = receipt.get("run") or receipt
        if receipt.get("write_epoch") is not None:
            row = {**row, "write_epoch": receipt["write_epoch"]}
            _repin_bracket_lease(run_id, receipt["write_epoch"])
        if receipt.get("last_step") is not None:
            # Plan 2.4: the step the dead attempt reached arms the resume
            # guard (attach_run pops this; it is not a row field).
            row = {**row, "_resume_last_step": receipt["last_step"]}
        return row

    @staticmethod
    def _ended_by_preemption(row: dict) -> bool:
        """A `failed` this SDK's SIGTERM close wrote (#2119): the run's own
        `probe_finish` says `preempted`. Nobody chose it -- a scheduler (or a
        person's `scancel`, which SIGTERM cannot tell apart) stopped the job."""
        from .....run.launch.preempt import REASON

        if row.get("status") != "failed":
            return False
        summary = row.get("summary_metrics") or row.get("summary")
        finish = summary.get("probe_finish") if isinstance(summary, dict) else None
        return isinstance(finish, dict) and finish.get("reason") == REASON

    @classmethod
    def _older_than_reopen_window(cls, ended_at: str) -> bool:
        """True when `ended_at` is outside the adopt window. Unparseable ⇒ False:
        a timestamp we cannot read is not evidence the run is stale, and refusing
        on it would break attach against any server whose format drifts."""
        from datetime import datetime
        from probe.foundation.compat.compat import UTC

        try:
            parsed = datetime.fromisoformat(str(ended_at).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return False
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return (datetime.now(UTC) - parsed).total_seconds() > cls._REOPEN_MAX_AGE_SECONDS

    def _mark_run_process(self) -> None:
        """A script opening or joining a run is that run's process from now on
        (`agent_session.mark_run_process`, R41): its writes are the run's, not
        its agent being active. A `probe` command's run is one write its agent
        made, so the CLI's client marks nothing (`probe exec` marks itself)."""
        if getattr(self.transport, "surface", None) == Surface.SDK.value:
            agent_session.mark_run_process()
from probe.sdk.client.resources.runs.reopen.conflict import _repin_bracket_lease  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.runs.reopen.status_holds import _TAKEOVER_BUDGET_SLACK_SECONDS  # noqa: E402 -- pieces need each other; the front door loads this one first
