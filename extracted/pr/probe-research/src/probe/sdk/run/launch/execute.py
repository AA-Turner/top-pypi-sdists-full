"""ExecuteMixin, Run's methods: run.execute: run a local command with run/process correlation, then
send what the child read and wrote."""

from __future__ import annotations
import os
import shutil
import socket
import subprocess
import tempfile
import time
import warnings
from ...recording_rules import recording_rules as _ignore
from . import launch as _launch
from . import preempt as _preempt
from . import program as _program
from .oom import OomCounter
from ...capture.logs import stream as _logstream
from ...capture import outputs as _outputs


#: The id of the run whose launcher will close it, set in a child that
#: `execute(finalize=True)` runs: the launcher holds the child's real exit code
#: and closes the run from it. A `probe.init()` attached to THAT run sends no
#: terminal status at exit unless its own hooks saw how it ended --
#: `sys.exit(main())` looks `sys.exit` up before main() runs, so no wrapper sees
#: that exit, and the child's guess of `completed` used to land first and win
#: against the launcher's `only_if_running`. The id, not "1": a sweep driver
#: under `probe exec` that opens run B and hands PROBE_RUN_ID=B to a job passes
#: this variable on too, and B has no launcher to close it.
EXEC_FINALIZES_ENV = "PROBE_EXEC_FINALIZES"


class ExecuteMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def execute(
        self,
        argv: list[str],
        *,
        cwd: str | None = None,
        env: dict[str, str] | None = None,
        finalize: bool = True,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
    ) -> subprocess.CompletedProcess:
        """Run a local command with deterministic run/process correlation.

        This is normal experiment execution capture, not the hook-only session
        API. Output streams pass through to the caller; a process span records
        argv, cwd, timestamps, and exit state.

        D17: the child's stdout/stderr are TEED -- to this process's own streams
        (a pty when those are a terminal, so the child still sees one) and to
        ``probe/run.log`` -- and the folder it works in (``cwd``, or ``outputs``) is
        swept when it exits. ``capture_outputs=False`` (or
        ``PROBE_CAPTURE_OUTPUTS=0``) turns both off. A handle whose own window
        is already open (``Client.run``) closes it here too, and tees nothing
        twice: the child inherits its streams. A submit-and-return launcher
        (``finalize=False``) captures nothing: the job's own ``probe.init()``
        does, wherever it runs. The child is told what this host captures
        (``PROBE_CAPTURE_OWNER``/``_ROOT`` for the folder,
        ``PROBE_CAPTURE_LOG_OWNER`` for its output) so a ``probe.init()`` inside
        it does not capture the same thing twice.
        """
        if not argv:
            raise ValueError("argv must not be empty")
        # Span attributes are persisted telemetry, not the launch mechanism --
        # they must carry the SAME scrubbed argv the launch block ships, never
        # the raw one. The raw argv is kept only for the actual subprocess
        # invocation and for `snapshot(argv=argv)` below, which scrubs
        # internally and needs the raw form for entrypoint detection.
        scrubbed_argv, _ = _launch.scrub_argv(list(argv))
        # Every executed run snapshots by default (design D3). detect_venv=True
        # because THIS interpreter is the launcher, not the environment being
        # recorded -- see Run.snapshot's docstring. Failure never blocks the
        # child: capture is never a gate, opt-in or otherwise (maintainer
        # decision 2026-08-06) -- it only ever warns.
        if os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0":
            try:
                self.snapshot(cwd=cwd, detect_venv=True, argv=argv)
            except Exception as exc:
                warnings.warn(
                    f"auto-snapshot failed; run continues uncaptured: {exc}",
                    stacklevel=2,
                )
        started_at = _now()
        span_id = self.span(
            "process",
            name=os.path.basename(argv[0]),
            status="running",
            started_at=started_at,
            attributes={"argv": scrubbed_argv, "cwd": os.path.abspath(cwd or os.getcwd())},
        )
        # 0205. The EPOCH travels with the id. A run id names a row, not an
        # execution attempt: a stale process that still has the id would
        # otherwise attach to a row a newer attempt already reopened and inherit
        # its write authority. With the epoch in hand the server's 0185 fencing
        # (ensure_writer_epoch) refuses the old attempt at the door. Anything
        # forwarding these across a machine boundary -- Modal secrets, Ray
        # runtime_env, sbatch --export -- must carry BOTH.
        #
        # The agent session travels the same way (audit E2): a job that leaves
        # this machine has none of the agent's own variables, and without the
        # session its runs lose the tag the daemon finds them by. Locally it
        # changes nothing -- the agent's variables win wherever they exist.
        from ... import agent_session

        # `existing`: a window this handle opened in-process (Client.run). It
        # closes with this command. `capture`: one for the command's own folder
        # when `existing` does not already sweep it. The log is teed here
        # unless `existing` already tees this process -- the child inherits it.
        existing = self._capture if finalize else None
        capture = None
        log_path = None
        if finalize and _outputs.enabled(capture_outputs):
            try:
                target = _outputs.target_root(outputs=outputs, cwd=cwd)
                if existing is None or not (existing.sweeps and _outputs._within(target, existing.root)):
                    capture = _outputs.OutputCapture.start(
                        self._client,
                        self.id,
                        outputs=outputs,
                        cwd=cwd,
                        tee=False,
                        launcher=True,
                        ignore=self._ignore_rules(cwd),
                        # The launcher's chunks name this handle's attempt.
                        epoch=_logstream.handle_epoch(self),
                    )
                    if self._capture is None:
                        self._capture = capture
                holder = capture or existing
                teed = existing is not None and existing._tee is not None
                if holder is not None and not teed and _outputs.log_enabled() and os.name == "posix":
                    log_path = _outputs.reserve_log_path(self.id)
                    holder.adopt_log(log_path)
            except Exception:  # noqa: BLE001 -- capture never stops the command
                pass
        process_env = {
            **os.environ,
            **agent_session.forwarding_env(),
            **(env or {}),
            "PROBE_RUN_ID": self.id,
            # Explicit either way: a submitted job (finalize=False) must not
            # inherit an outer `probe exec`'s value.
            EXEC_FINALIZES_ENV: self.id if finalize else "",
        }
        # Only an epoch this handle KNOWS travels. An inherited value names
        # some other run's generation, so it is removed rather than passed on.
        if self.write_epoch is not None:
            process_env["PROBE_RUN_EPOCH"] = str(self.write_epoch)
        else:
            process_env.pop("PROBE_RUN_EPOCH", None)
        # What the child reads (lineage). This process cannot see a child's
        # opens, so a Python child gets a small stdlib hook through an injected
        # `sitecustomize` and spools them; this launcher hashes and sends them
        # once the child exits. Only for a child it RUNS: a submitted job
        # (finalize=False) reads on another machine, where its own
        # `probe.init()` records. Never a gate.
        reads_child = False
        # `.probeignore` (plan (n)) for the directory the child runs in: its
        # reads are filtered with these after it exits (`_finalize_child_reads`),
        # or by a recovery if this launcher never collects them.
        self._child_ignore = self._ignore_rules(cwd)
        if finalize:
            try:
                from ...capture import lineage as _inputs

                reads_child = _inputs.prepare_child(
                    self.id,
                    process_env,
                    client=self._client,
                    ignore=self._child_ignore,
                    capture_outputs=capture_outputs,
                )
            except Exception:  # noqa: BLE001
                reads_child = False
        # Tell the child what this host already captures, so its own
        # probe.init() does not capture it twice (R12).
        # Only a window that really sweeps may claim the folder: a log-only one
        # (`/`, a workspace too big to list) must leave a narrower
        # `probe.init(outputs=...)` in the child to sweep its own.
        sweeper = next((w for w in (capture, existing) if w is not None and w.sweeps), None)
        if sweeper is not None:
            process_env[_outputs.OWNER_ENV] = socket.gethostname()
            process_env[_outputs.ROOT_ENV] = sweeper.root
        if existing is not None and existing._tee is not None:
            process_env[_outputs.LOG_OWNER_ENV] = socket.gethostname()
        if capture_outputs is False:
            process_env[_outputs.CAPTURE_ENV] = "0"
        # `.probeignore` (plan (n)): the child uses THIS run's file even if it
        # changes directory, and sees the `ignore=` patterns too.
        if self._child_ignore is not None:
            if self._child_ignore.source_file:
                process_env[_ignore.ENV_FILE] = self._child_ignore.source_file
            if self._ignore_patterns:
                # In their own variable, one per line: through PROBE_IGNORE a
                # comma inside a pattern would split it in two. PROBE_IGNORE
                # itself is inherited as it is.
                process_env[_ignore.ENV_EXPORTED] = _ignore.join_lines(
                    [*_ignore.split_lines(process_env.get(_ignore.ENV_EXPORTED)), *self._ignore_patterns]
                )
        # How the child ends, as only it can tell (a SIGTERM's sender) and as this machine counts it
        # (OOM kills): `_read_exit_verdict`. An outer launcher's note folder is never passed on.
        note_folder = None
        oom = None
        process_env.pop(_preempt.EXIT_NOTE_ENV, None)
        if finalize:
            oom = OomCounter()
            try:
                note_folder = tempfile.mkdtemp(prefix="probe-exit-")
                process_env[_preempt.EXIT_NOTE_ENV] = note_folder
            except OSError:
                note_folder = None
        log_stats = None
        try:
            if log_path is not None:
                from ...capture.logs.tee import run_teed

                result, log_stats = run_teed(
                    argv,
                    cwd=cwd,
                    env=process_env,
                    log_path=log_path,
                    # If this process dies first, the helper -- which outlives
                    # it -- recovers the log and the folder once the child ends.
                    recovery_entry=str(capture._entry) if capture is not None and capture._entry else None,
                    on_helper=capture.note_helper if capture is not None else None,
                    # Only once the tee is live: a child told its output is
                    # logged, when it is not, would keep no log at all.
                    teed_env={_outputs.LOG_OWNER_ENV: socket.gethostname()},
                )
            else:
                # Here, or by the `probe` shim when this runs in the service (T42).
                result = _program.run_program(argv, cwd=cwd, env=process_env)
        except BaseException as exc:
            _remove_folder(note_folder)
            if reads_child:
                self._finalize_child_reads(interrupted=True)
            if capture is not None:
                # Ctrl-C, or a launch failure: what the child wrote so far is
                # still this run's. Queued, then left to the detached drainer.
                try:
                    capture.finalize(log_path=log_path)
                    self._client._kick_drainer(force=True)
                except Exception:  # noqa: BLE001
                    pass
            self.span(
                "process",
                id=span_id,
                name=os.path.basename(argv[0]),
                status="failed",
                started_at=started_at,
                ended_at=_now(),
                attributes={"argv": scrubbed_argv, "cwd": os.path.abspath(cwd or os.getcwd())},
            )
            # Ctrl-C reaches the whole foreground process group, so the LAUNCHER
            # takes it too and lands here. The run was never closed: it sat
            # `running` until the reaper called it `crashed`, and a crash notice
            # went to the person who had just pressed Ctrl-C. KeyboardInterrupt
            # only -- a launcher that broke for its own reasons (a fork failure,
            # a bad argv) has no standing to call the run stopped on purpose.
            # `only_if_running`, like the finalize below: a job that closed
            # itself from inside already wrote the honest verdict.
            if finalize and isinstance(exc, KeyboardInterrupt):
                try:
                    self.set_status("canceled", only_if_running=True)
                except Exception:  # noqa: BLE001 -- the interrupt must still propagate
                    pass
            raise
        verdict = _read_exit_verdict(result.returncode, note_folder, oom)
        _remove_folder(note_folder)
        stopped = verdict == "canceled" and result.returncode < 0
        if finalize and stopped:
            # Before the sweep: a killed SDK child's own lease, reported gone by the watcher,
            # would count `crashed` over this verdict (`_release_dead_writer`).
            self._release_dead_writer(verdict)
        attributes = {
            "argv": scrubbed_argv,
            "cwd": os.path.abspath(cwd or os.getcwd()),
            "exit_code": result.returncode,
        }
        if stopped:
            attributes["reason"] = _preempt.STOPPED_REASON
        self.span(
            "process",
            id=span_id,
            name=os.path.basename(argv[0]),
            status="completed" if result.returncode == 0 else "failed",
            started_at=started_at,
            ended_at=_now(),
            attributes=attributes,
        )
        # 0205. The launcher is the DESIGNATED FINALIZER for a wrapped run: it
        # is the only party holding the child's exit code. Before this, execute()
        # recorded the span and returned, so a wrapped run was never closed by
        # anyone -- it sat 'running' until the reaper, and with no beats the
        # reaper called it 'untracked'. A real exit code became a guess.
        #
        # GUARDED, because the child may have finished the run itself: a script
        # calling probe.init() ... finish() has already written the authoritative
        # verdict from inside the work, and the launcher must not overwrite it
        # with its own view. `only_if_running` makes this a no-op against any
        # row already terminal, so the child's verdict wins on arrival ORDER
        # being irrelevant -- whoever spoke first and meant it, stands.
        # finalize=False when this process SUBMITTED the work rather than running
        # it: a scheduler accepting a job says nothing about how the job ends,
        # and recording the submitter's exit code as the run's is exactly the
        # lie the hand-off path exists to avoid. The job's own probe.init()
        # owns the verdict there.
        if reads_child:
            self._finalize_child_reads()
        try:
            enqueued = False
            holder = capture or existing
            # ONE deadline for the whole close -- every window and the delivery.
            timeout = self._resolve_finish_timeout(None, default=None)
            deadline = None if timeout is None else time.monotonic() + max(timeout, 0.0)
            for window in (capture, existing):
                if window is None:
                    continue
                budget = None if deadline is None else min(
                    _outputs.close_budget(), max(0.0, deadline - time.monotonic())
                )
                try:
                    if window is holder:
                        window.finalize(log_path=log_path, log_stats=log_stats, budget=budget)
                    else:
                        window.finalize(budget=budget)
                except Exception:  # noqa: BLE001 -- the child's verdict is recorded regardless
                    pass
                enqueued = enqueued or bool(window.enqueued)
            if enqueued:
                self._deliver_captured(deadline)
        finally:
            # In a `finally`: a Ctrl-C during the sweep must not cost the run
            # the child's exit code.
            if finalize:
                self.set_status(verdict, only_if_running=True)
        return result

    def _finalize_child_reads(self, *, interrupted: bool = False) -> None:
        """Send what the executed child read. Never raises. Interrupted, the
        launcher does not stop to hash: the child's spools stay, and the next
        run on this host sends them. A Ctrl-C during that hashing only skips
        it, as it always has here: the child has exited, and its exit code is
        what closes the run next."""
        try:
            from ...capture import lineage as _inputs

            if interrupted:
                _inputs.abandon(self.id)
            else:
                _inputs.finalize(self._client, self.id, ignore=self._child_ignore)
        except (Exception, KeyboardInterrupt):  # noqa: BLE001
            pass

    def _deliver_captured(self, deadline: float | None) -> None:
        """Try to deliver captured outputs before the terminal status, like
        finish(), within what is left of the close's deadline. They are
        non-blocking: whatever does not land is left to the detached drainer."""
        if getattr(self._client, "_drains_by_hand", False):
            return  # an offline run: only `probe sync` delivers its queue, nothing here can
        while deadline is None or time.monotonic() < deadline:
            try:
                self._client.flush(run_ref=self.id)
            except Exception:  # noqa: BLE001 -- drain records last_error itself
                pass
            if deadline is None or not self._queued_ops_any(self._client.journal.pending()):
                break
            time.sleep(min(0.25, max(deadline - time.monotonic(), 0.0)))
        try:
            if self._queued_ops_any(self._client.journal.pending()):
                self._client.hand_off_delivery()
        except Exception:  # noqa: BLE001
            pass


def _read_exit_verdict(returncode: int, note_folder: str | None, oom: OomCounter | None) -> str:
    """The run's status from the child's exit (`_status_for_exit`): its own note for a SIGTERM,
    the OOM counter for a SIGKILL -- unless this launcher is itself being stopped."""
    if _preempt.ending() is not None:
        return _status_for_exit(returncode)
    note = _preempt.read_exit_note(note_folder) if note_folder else None
    unchanged = oom is not None and oom.is_unchanged()
    return _status_for_exit(returncode, note=note, is_oom_unchanged=unchanged)


def _remove_folder(folder: str | None) -> None:
    if folder:
        shutil.rmtree(folder, ignore_errors=True)


from probe.sdk.run.closing.status import _status_for_exit  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.values import _now  # noqa: E402 -- pieces need each other; the front door loads this one first
