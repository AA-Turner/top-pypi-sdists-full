"""StatusHoldsMixin, Client's methods: hold the incumbent's queued status writes during a takeover,
and release or restore them (twin: app/runs)."""

from __future__ import annotations
import json
import os
import socket
import time
from pathlib import Path
#: A wait budget that allows any wait covers at least one threshold plus this,
#: so a relaunch seconds after the death is not refused at its first 409.
_TAKEOVER_BUDGET_SLACK_SECONDS = 30
#: The key marking a status op the takeover barrier set aside, and how long
#: past the barrier's own bounds a hold is honoured before the next drain or
#: relaunch treats its holder as dead and puts the op back (on the holder's own
#: host, a dead holder pid ends the hold at once: `journal.hold_abandoned`).
#: Short: both barrier phases are deadline-bounded, and a hold outliving the
#: reaper's 900 s cost a finished run its verdict (review of #2019). A hold
#: restored under a barrier still finishing is harmless -- 1.10's fence refuses
#: the old close once the takeover's epoch moves.
_TAKEOVER_HOLD_KEY = "takeover_hold"
_TAKEOVER_HOLD_MARGIN_SECONDS = 120.0


class StatusHoldsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _hold_status_writes(self, old: dict, ops: dict[str, dict]) -> list[str]:
        """Set the incumbent's queued STATUS PATCHes aside for the barrier (see
        `_drain_before_takeover`); returns the names held.

        Aside means the dead-letter folder, marked as a hold: no drain delivers
        from there, and if this process dies mid-barrier the op is still
        VISIBLE (`probe outbox status`, `probe outbox retry`) and the next
        relaunch's barrier puts an expired hold back. Under the drain lock, so a
        worker can never be delivering one of them at the same moment; if a
        worker holds the lock for more than a few seconds, nothing is held and
        the barrier may deliver them, as before 2.3."""
        from ......_shared import oscompat

        # A `completed` close is NOT held: the incumbent finished, so the
        # barrier delivers it with the data and the relaunch must not continue
        # a finished run (review of #2019; `_resume_run` then refuses, as a
        # resume of a completed run does). Every other verdict is the dead
        # attempt's, which a requeue continues.
        doomed = [
            name
            for name, op in ops.items()
            if (
                op.get("method") == "PATCH"
                and "status" in (op.get("body") or {})
                and (op.get("body") or {}).get("status") != "completed"
            )
            # 2.8: on a `leases` run the incumbent's verdict is its queued
            # lease release, held and retired exactly like a status write (a
            # `completed` one is delivered, like a `completed` close).
            or (
                op.get("method") == "POST"
                and str(op.get("path") or "").endswith("/release")
                and (op.get("body") or {}).get("exit_status") != "completed"
            )
        ]
        if not doomed:
            return []
        try:
            handle = self.journal.drain_lock.open("a+")
        except OSError:
            return []
        held: list[str] = []
        try:
            give_up = time.monotonic() + 5.0
            while True:
                try:
                    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= give_up:
                        return []
                    time.sleep(0.05)
            until = (
                time.time()
                + _env_seconds("PROBE_TAKEOVER_DRAIN_SEC", _TAKEOVER_DRAIN_SECONDS)
                + max(
                    _takeover_wait_budget(),
                    _takeover_threshold() + _TAKEOVER_BUDGET_SLACK_SECONDS,
                )
                + _TAKEOVER_HOLD_MARGIN_SECONDS
            )
            hold = {"pid": os.getpid(), "host": socket.gethostname(), "until": until}
            # The marker first: whatever happens next, a drain or a new client
            # knows to look for a hold this process may not live to release.
            self.journal.holds_marker.touch()
            for name in doomed:
                path = self.journal.ops_dir / name
                try:
                    op = json.loads(path.read_text())
                except (OSError, ValueError):
                    continue
                op[_TAKEOVER_HOLD_KEY] = {
                    **hold,
                    "last_error": op.get("last_error"),
                    "blocking": op.get("blocking"),
                }
                op["last_error"] = (
                    "held by a relaunch taking over run "
                    f"{old.get('slug') or old.get('id')}: retired if it takes over, "
                    "put back if it does not"
                )
                op["blocking"] = False
                self._move_op(path, self.journal.failed_dir / name, op)
                held.append(name)
        except Exception:  # noqa: BLE001 -- a close left queued is the old behaviour
            pass
        finally:
            handle.close()
        self._recount_outbox()
        return held

    def _release_status_writes(self, names: list[str], *, retire: bool) -> None:
        """End the barrier's hold on ``names``: RETIRED (the reopen succeeded,
        the relaunch owns the verdict) or PUT BACK at their original queue
        positions (anything else), with the drainer woken to deliver them."""
        if not names:
            return
        moved = False
        for name in names:
            path = self.journal.failed_dir / name
            try:
                op = json.loads(path.read_text())
            except (OSError, ValueError):
                continue  # retried by hand meanwhile, or gone: nothing to undo
            hold = op.pop(_TAKEOVER_HOLD_KEY, None)
            if not isinstance(hold, dict):
                continue
            try:
                if retire:
                    op["last_error"] = (
                        "retired by a takeover: the relaunch of this run owns its verdict now"
                    )
                    self._move_op(path, path, op)
                else:
                    op["last_error"] = hold.get("last_error")
                    if hold.get("blocking") is None:
                        op.pop("blocking", None)
                    else:
                        op["blocking"] = hold["blocking"]
                    self._move_op(path, self.journal.ops_dir / name, op)
                    moved = True
            except Exception:  # noqa: BLE001 -- the next barrier restores an expired hold
                continue
        self._recount_outbox()
        if moved:
            self._kick_drainer(force=True)

    def _restore_expired_holds(self) -> None:
        """Put back holds whose relaunch died before releasing them: expired,
        or held by a process of this host that no longer exists. A full scan
        (a hold an older client left carries no marker); the barrier runs it."""
        from .....delivery.outbox.drain.holds import hold_abandoned

        try:
            stale = [
                path.name
                for path, op in self.journal.failed()
                if isinstance(op.get(_TAKEOVER_HOLD_KEY), dict)
                and hold_abandoned(op[_TAKEOVER_HOLD_KEY])
            ]
        except Exception:  # noqa: BLE001 -- an unreadable folder has nothing to restore
            return
        self._release_status_writes(stale, retire=False)

    def _restore_abandoned_holds(self) -> list[str]:
        """The cheap check every new client makes (`journal.restore_abandoned_holds`),
        with the outbox's counts kept right. Returns what went back."""
        from .....delivery.outbox.drain.holds import restore_abandoned_holds

        restored = restore_abandoned_holds(self.journal)
        if restored:
            self._recount_outbox()
        return restored

    def _move_op(self, src: Path, dst: Path, op: dict) -> None:
        """Rewrite ``op`` at ``src`` and move it to ``dst`` atomically: written
        in place first, so a crash never leaves it in both folders."""
        from ......foundation.durable.durable import fsync_directory, write_text_atomic

        write_text_atomic(src, json.dumps(op, indent=2) + "\n", mode=0o600)
        if src != dst:
            os.replace(src, dst)
            fsync_directory(dst.parent)
        fsync_directory(src.parent)

    def _recount_outbox(self) -> None:
        """status.json follows ops moved between the queue and dead letters."""
        try:
            from ......foundation.durable.durable import file_lock

            with file_lock(self.journal.append_lock):
                self.journal._write_status_locked()
        except Exception:  # noqa: BLE001 -- the next append recounts
            pass

    def _clear_draining_tag(self, old: dict, receipt: dict) -> None:
        """A retired close was also what took the incumbent's "draining" tag
        back off (its deferred finish restores the tags). The run is running
        again under this relaunch, so the tag is wrong: drop it (review of
        #2019, LOW-D)."""
        row = receipt.get("run") if isinstance(receipt.get("run"), dict) else receipt
        tags = row.get("tags") if isinstance(row, dict) else None
        if not isinstance(tags, list) or "draining" not in tags:
            return
        try:
            self.write(
                "PATCH",
                f"/v1/runs/{old['id']}",
                {"tags": [t for t in tags if t != "draining"]},
                sync=True,
            )
        except Exception:  # noqa: BLE001 -- a stale hint, never a reason to fail init
            pass
from probe.sdk.client.resources.runs.reopen.reopen import _TAKEOVER_DRAIN_SECONDS  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.client.resources.runs.reopen.takeover import _env_seconds, _takeover_threshold, _takeover_wait_budget  # noqa: E402 -- pieces need each other; the front door loads this one first
