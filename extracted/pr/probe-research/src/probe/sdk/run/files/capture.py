"""CaptureMixin, Run's methods: the run's automatic output capture window in this process, its
.probeignore rules, and the forked-writer marker."""

from __future__ import annotations
import os
import warnings
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...recording_rules import ignore as _ignore
from ...capture.logs import stream as _logstream
from ...capture import outputs as _outputs


class CaptureMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- output capture (D17) -------------------------------------------------
    def _ignore_rules(self, cwd: str | os.PathLike | None = None) -> Any:
        """This run's ``.probeignore`` rules for ``cwd`` (plan (n)), or None when
        nothing is configured. Loaded once per directory; never raises."""
        cache = self.__dict__.setdefault("_ignore_cache", {})
        try:
            key = os.path.abspath(os.fspath(cwd) if cwd is not None else os.getcwd())
        except OSError:  # the working directory was deleted under the run
            return None
        if key not in cache:
            try:
                cache[key] = _ignore.load(key, extra=getattr(self, "_ignore_patterns", ()))
            except Exception:  # noqa: BLE001 -- an ignore file may never cost a capture
                cache[key] = None
        return cache[key]

    def _set_ignore(self, patterns: Any) -> None:
        """Record ``ignore=`` patterns (a string is one pattern)."""
        if patterns is None:
            return
        try:
            self._ignore_patterns = _ignore.normalize(patterns)
        except ValueError as exc:
            raise errors.ValidationError(str(exc)) from None
        self.__dict__.pop("_ignore_cache", None)

    def _hand_ignore_to_launcher(self) -> None:
        """A JOINED run's own ``ignore=`` patterns (plan (n), #2045 review).

        Under ``probe exec`` the launcher on this host collects this
        process's reads and sweeps its folder after it exits, with the rules
        the LAUNCHER loaded, which never saw these. They travel through the
        channels those captures already read: the read spool
        (:func:`inputs.hand_to_launcher`) and the output window's registry
        record (:func:`outputs.share_ignore`); with no launcher on this host
        both are no-ops. The code snapshot is the one capture they cannot
        reach -- a launcher takes it before this process starts -- so a
        pattern the launcher never loaded is named in a warning. Never raises.
        """
        patterns = getattr(self, "_ignore_patterns", ())
        if not patterns:
            return
        try:
            rules = self._ignore_rules()
            if rules is None:
                return
            from ...capture import lineage as _inputs

            _inputs.hand_to_launcher(self.id, rules)
            _outputs.share_ignore(self.id, rules)
            unseen = _ignore.unseen_by_launcher(patterns, rules)
            if unseen and os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0":
                from ....foundation.safe_warn import safe_warn

                safe_warn.warn(
                    f"probe: ignore={unseen!r} cannot keep files out of this run's code snapshot: "
                    "the launcher that opened the run (`probe exec`) took it before this script "
                    "started. They still keep matching files out of what this script reads and "
                    "writes. To keep them out of code capture too, put them in .probeignore (at "
                    "the git toplevel) or PROBE_IGNORE where you launch.",
                    stacklevel=3,
                )
        except Exception:  # noqa: BLE001 -- filtering is never a reason to fail init
            pass

    def _start_capture(
        self,
        *,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
    ) -> None:
        """Open this run's capture window IN THIS PROCESS: the folder's
        baseline now, fds 1/2 teed to ``probe/run.log``, the sweep at close. A
        no-op when opted out, or when a launcher on this host (``probe
        exec``) already captures for this process."""
        if self._capture is not None or not _outputs.enabled(capture_outputs):
            return
        try:
            root = _outputs.target_root(outputs=outputs)
            if _outputs.outputs_owned_here(root) and _outputs.log_owned_here():
                # `probe exec` on this host already sweeps this folder and tees
                # this process (PROBE_CAPTURE_OWNER/_ROOT/_LOG_OWNER).
                return
            # When exec sweeps the folder but does not tee (it could not), this
            # window keeps the log only.
            self._capture = _outputs.OutputCapture.start(
                self._client,
                self.id,
                outputs=outputs,
                sweep=not _outputs.outputs_owned_here(root),
                ignore=self._ignore_rules(),
                epoch=_logstream.handle_epoch(self),
                writer=self._writer_record(),
            )
        except Exception as exc:  # noqa: BLE001 -- capture never stops a run from opening
            warnings.warn(f"probe: output capture could not start ({type(exc).__name__}): {exc}", stacklevel=2)

    def _note_forked_writer(self) -> None:
        """This handle is writing from a forked child (2.2): leave a marker
        beside the capture record, once per child, so the output helper's
        reporter does not call the run's writer dead when the process that
        opened it exits (`fork()` then `os._exit()` in the parent is how a
        script daemonizes). A child that never writes (a DataLoader worker)
        leaves none, and the opener's death is still reported."""
        pid = os.getpid()
        if self._forked_writer_marked == pid:
            return
        self._forked_writer_marked = pid
        try:
            capture = self._capture
            entry = getattr(capture, "_entry", None) if capture is not None else None
            if entry is not None:
                _outputs.mark_forked_writer(entry, pid)
        except Exception:  # noqa: BLE001 -- bookkeeping never touches a write
            pass

    def _writer_record(self) -> dict:
        """What the output helper needs to report this process's death (2.2).

        ``sole_writer`` is this process's own belief: a handle attached through
        PROBE_RUN_ID (a rank, a job under a launcher) is one of several writers
        by construction, and the server additionally refuses when anything
        attached (`attached_at`) or the run is not in-process."""
        attached = bool(getattr(self, "attached", False))
        return {
            "session_id": self.session_id,
            "write_epoch": self.write_epoch,
            "role": "attached" if attached else "owner",
            "sole_writer": not attached,
        }

    def _note_logged(self, path: str, digest: str | None = None) -> None:
        capture = self._capture
        if capture is not None:
            try:
                capture.note_logged(path, digest)
            except Exception:  # noqa: BLE001 -- bookkeeping never touches a write
                pass

    def _finalize_capture(self, budget: float | None = None) -> dict | None:
        """Queue this run's log, then sweep and queue its outputs, within
        ``budget`` seconds. Before the barrier drain, so the close makes one
        attempt at delivering them -- but they are non-blocking ops, and an
        undeliverable one never holds the close: it stays queued for the
        detached drainer."""
        capture = self._capture
        if capture is None:
            return None
        try:
            return capture.finalize(budget=budget)
        except Exception:  # noqa: BLE001 -- finalize warns itself; never block a close
            return None

    def _warn_if_capture_incomplete(self) -> None:
        """Completion warning, never a gate (maintainer decision 2026-08-06):
        an incomplete capture makes the record honest about itself at the one
        moment someone claims success -- but nothing, opt-in or otherwise, may
        block a run. PROBE_AUTO_SNAPSHOT=0 means capture was declined; a
        warning would be nagging about a choice, so it is silent too.
        Placed after the journal drain so it never fires on writes this very
        finish() is about to deliver (the async_writes false-positive)."""
        try:
            result = self._client.check_run(self.id)
        except BaseException:  # noqa: BLE001
            return  # a completeness probe must never break a close-out
        # Everything below is diagnostics, and all of it used to be able to kill
        # the run it was describing. The warn raised under `-W error`, and the
        # `", ".join(...)` sat OUTSIDE the guard above, so a backend answering
        # `missing` with objects or nulls raised TypeError -- either one turning
        # a SUCCESSFUL twelve-hour run into a failure at its closing brace, on
        # the clean path, against the explicit rule two lines up that nothing
        # may block a run.
        try:
            state = result.get("state")
        except BaseException:  # noqa: BLE001
            return
        if state == "incomplete":
            missing = _diagnostics.join(result.get("missing"))
            _diagnostics.warn(
                "run may not be reproducible -- capture incomplete: "
                f"{missing}. See `probe run check {self.id}` for the full audit.",
                stacklevel=3,
            )
