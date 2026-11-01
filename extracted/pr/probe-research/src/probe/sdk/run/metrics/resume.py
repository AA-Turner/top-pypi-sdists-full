"""ResumeGuardMixin, Run's methods: after a reopen, drop writes at or below the resume point and
keep the resume span's counts."""

from __future__ import annotations

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ..context import context as unit_context


class ResumeGuardMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def arm_resume_guard(self, last_step: int) -> None:
        """Called on attach after a reopen: refuse explicit steps the first
        execution already wrote, and start auto-steps above them — a resumed
        process must continue the curve, never re-log it."""
        self._resume_from_step = last_step
        with self._steps_lock:
            self._auto_step_floor = last_step + 1

    def _resume_exits(self, step: int) -> tuple[str, str, str]:
        """(overwrite, start over, keep both): what each intent does from HERE.

        A job that rejoined its run through ``PROBE_RUN_ID`` cannot use
        ``on_conflict`` (`probe.init()` joining a run takes none, and ignores
        ``"supersede"``), and `probe run start --rewind-to-step` is deprecated
        (#1551) and refuses a run with no external id. So its exits are the
        ones that work there (#2044 review)."""
        if not self._resume_via_attach:
            return (
                f"relaunch with on_conflict=probe.Rewind(step={step})",
                'on_conflict="supersede" (a fresh retry run)',
                "client.fork_run(...) from the checkpoint step",
            )
        ref = self._data.get("slug") or self.id
        # `probe exec` files a new run in the ACTIVE project unless told: the
        # retry belongs beside the run it retries (#2044 verify).
        project = f" --project id:{self.project_id}" if self.project_id else ""
        external = self._data.get("external_id")
        overwrite = (
            f"relaunch the job WITHOUT PROBE_RUN_ID, with probe.init(external_id={external!r}, "
            f"on_conflict=probe.Rewind(step={step}))"
            if external
            else "not possible for this run (it has no external id, and a rewind needs one)"
        )
        return (
            overwrite,
            f"a new run: `probe exec{project} --parent {ref} --relation retry -- <command>`",
            f"`probe run fork {ref} --step {step}` (or client.fork_run(...)), then run the job "
            "under the fork",
        )

    def _drop_below_resume(self, step, *, strict: bool | None) -> None:
        """A write at or below the resume point: dropped, with one warning (D6).

        The first execution already wrote these steps. A relaunch that restarted
        from an OLDER checkpoint re-logs them, and appending would splice two
        executions into one curve; raising (what this did) killed the relaunch
        at its first step instead. W&B drops the call and warns once; so does
        this. Nothing is sent or queued. ``strict`` still raises: a caller who
        asked for loud failure gets it.

        Counted in a keyed `diagnostic` span (`resume_guard`), not in run
        metadata, which a PATCH replaces whole. The span is written on the 1st,
        10th, 100th... drop and when logging climbs past the resume point, so
        its counts stay current in O(log n) writes."""
        resume_point = self._resume_from_step
        overwrite, start_over, keep_both = self._resume_exits(step)
        if strict or (strict is None and not self._client.fail_open):
            raise errors.ValidationError(
                f"step {step} <= resume point {resume_point} on a "
                "resumed run — the first execution already wrote this step. "
                "Three exits, by intent: restarted from an EARLIER checkpoint "
                f"and want the old range overwritten -> {overwrite}; "
                f"repeating from scratch -> {start_over}; "
                f"keeping both curves -> {keep_both}."
            )
        # NOT counted on client.dropped_writes: that counts writes the OUTBOX
        # lost, and finish() reports any rise as data loss (#2014). A resume
        # drop is the design working; the run's own `_resume_drops` counts it.
        with self._steps_lock:
            self._resume_drops += 1
            drops = self._resume_drops
            if drops == 1:
                self._resume_first_dropped = step
                self._resume_first_drop_at = _now()
            self._resume_last_dropped = step
        if drops == 1:
            _diagnostics.warn(
                f"probe: step {step} is at or below this resumed run's resume point "
                f"({resume_point}): the first execution already logged it, so this call "
                f"and every later one at or below step {resume_point} is DROPPED, not "
                f"sent. Logging continues above step {resume_point}. To overwrite that "
                f"range instead: {overwrite}; to keep both curves: {keep_both}."
            )
        if 10 ** (len(str(drops)) - 1) == drops:  # 1, 10, 100, ...
            self._write_resume_span()
        return None

    def _note_resumed(self, step: int) -> None:
        """The first write past the resume point after drops: one line, and the
        span's final counts."""
        with self._steps_lock:
            if self._resume_announced or step <= (self._resume_from_step or 0):
                return
            self._resume_announced = True
            self._resume_resumed_at = step
            drops = self._resume_drops
        _diagnostics.warn(
            f"probe: logging resumed at step {step} after dropping {drops} call(s) at "
            f"or below resume point {self._resume_from_step}."
        )
        self._write_resume_span()

    def _write_resume_span(self, *, closing: bool = False) -> None:
        """Upsert the keyed counter span. Never raises, never holds the close.

        One span per RANK (ranks resuming together would otherwise overwrite
        each other's counts), never under the caller's open span or unit: it
        belongs to the run, and the server sets a span's coordinate once."""
        rank = _global_rank()
        with self._steps_lock:
            # One consistent snapshot: log() on another thread may be adding a
            # drop while this writes (#2044 review).
            resumed = self._resume_resumed_at
            drops = self._resume_drops
            first_dropped = self._resume_first_dropped
            last_dropped = self._resume_last_dropped
            first_drop_at = self._resume_first_drop_at
        done = closing or resumed is not None
        try:
            with unit_context.detached():
                self.span(
                    "diagnostic",
                    external_key="resume_guard" if rank is None else f"resume_guard/rank-{rank}",
                    name="resume_guard",
                    parent_span_id=None,
                    status="completed" if done else "running",
                    started_at=first_drop_at,
                    ended_at=_now() if done else None,
                    attributes={
                        "resume_point": self._resume_from_step,
                        "dropped_calls": drops,
                        "first_dropped_step": first_dropped,
                        "last_dropped_step": last_dropped,
                        "resumed_at_step": resumed,
                        **({"rank": rank} if rank is not None else {}),
                    },
                    strict=False,
                    blocking=False,
                )
        except Exception:  # noqa: BLE001 -- a counter must never break a log() call
            pass

    def _close_resume_span(self) -> None:
        """At finish, whenever there were drops: the final counts and a closed
        status. The span is written only on the 1st, 10th, 100th... drop and
        on the resume, so a run that finishes inside its dropped range left it
        `running`, often with a stale count. Always written (one keyed,
        non-blocking upsert) rather than only when "something is missing": that
        bookkeeping raced with log() on other threads (#2044 review)."""
        with self._steps_lock:
            drops = self._resume_drops
        if drops:
            self._write_resume_span(closing=True)
from probe.sdk.run.launch.host_claims import _global_rank  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.values import _now  # noqa: E402 -- pieces need each other; the front door loads this one first
