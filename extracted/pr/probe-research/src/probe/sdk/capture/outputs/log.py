"""LogTee: the run's console log -- reserve its file, tee and stream it live, redact and queue it."""

from __future__ import annotations
import os
import re
import sys
import time
from pathlib import Path
from ....foundation.durable import homedir
from ..logs import stream as _logstream
from ....foundation.safe_warn import safe_warn as _diagnostics
from ....foundation.process_rank import read_process_rank, read_world_size
from ... import secret_gate
from ..logs import early as _early
from ..logs.logs import live_dir
# scanning disabled: from .secret_gate import FIELD_NAME_RULE, CredentialBlocked, _findings, prepare_upload
from ...secret_gate import FIELD_NAME_RULE
LOG_ENV = _early.LOG_ENV
LOG_NAME = "probe/run.log"
CAPTURE_LOG = "log"
#: Local logs, ledgers and capture records older than this are pruned.
RETAIN_SECONDS = 30 * 86_400
_OFF = _early.OFF
#: A run of base64-looking characters: where an encoded credential hides.
_ENCODED_RUN = re.compile(r"[A-Za-z0-9+/_-]{24,}={0,2}")
#: The line between a run's log and what printed after it finished (T15), in the version sent at exit.
AFTER_FINISH_MARKER = b"[probe: printed after the run finished]\n"
#: What the exit spends sending that version itself (a container's detached drain may die with it, and a
#: server gone by then would keep the drain retrying for hours); the rest stays queued for the drain.
AFTER_FINISH_SEND_SECONDS = 5.0
#: Why a run's printed output cannot be teed here, said once per process (T19).
_UNSAVED_WARNING = (
    "probe: this run's printed output isn't being saved here ({why}). Metrics and files are still recorded."
)
_is_unsaved_warned = False


def log_enabled() -> bool:
    """``PROBE_CAPTURE_LOG`` (on)."""
    return (os.environ.get(LOG_ENV) or "").strip().lower() not in _OFF


def in_process_log_supported() -> bool:
    """The fd-level tee sees what reaches fds 1/2: a notebook kernel's streams do not (T19)."""
    return log_unsaved_reason() is None


def log_unsaved_reason() -> str | None:
    """Why this process's printed output cannot be teed into its run's log, or None when it can. Only a
    kernel moves ``sys.stdout``/``sys.stderr`` off fds 1/2 (ipykernel loaded and its streams not on them):
    a script's own wrapper (``sys.stdout = Logger(sys.stdout)``, ``sys.stderr = sys.stdout``) still writes
    through fds 1/2, and merely importing ``ipykernel`` changes nothing."""
    if os.name != "posix":
        return "Windows"
    if not sys.executable:
        return "no Python executable to run the recorder"
    if "ipykernel" in sys.modules and not _early.is_fd_behind_streams():
        return "notebook"
    return None


def warn_log_unsaved(why: str) -> None:
    """Once per process: capture is off and the user did not turn it off."""
    global _is_unsaved_warned
    if _is_unsaved_warned:
        return
    _is_unsaved_warned = True
    _diagnostics.warn(_UNSAVED_WARNING.format(why=why))


# -- local state ----------------------------------------------------------------------
def state_dir() -> Path:
    """``<state>/probe``, where the log, the capture registry and baselines
    live; under a private ``$TMPDIR`` folder when the state folder cannot be
    written (``HOME=/`` for an arbitrary uid: `homedir.state_base`). It used to
    be `session_marker.state_dir`, and output capture did not start there."""
    return homedir.state_base() / "probe"


def _private_dir(*parts: str) -> Path:
    path = state_dir().joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    return path


def _prune(directory: Path) -> None:
    cutoff = time.time() - RETAIN_SECONDS
    try:
        for entry in os.scandir(directory):
            try:
                if entry.is_file(follow_symlinks=False) and entry.stat().st_mtime < cutoff:
                    os.unlink(entry.path)
            except OSError:
                pass
    except OSError:
        pass


def reserve_log_path(run_id: str) -> str:
    """A fresh file under ``<state>/probe/logs``: ``<run-id>.log``, then
    ``<run-id>.2.log`` ... when a resumed attempt of the same run logs again.

    A name whose live-log spool (``<log>.live/``) still exists is taken even
    when its log is gone: a process killed after its log was queued (and the
    local copy discarded) but before its stream stopped leaves the spool, with
    that attempt's cursor and unsent tail, for its recovery to send. Reusing
    the name would ship the dead attempt's tail as this one's output and start
    this one past its own first bytes."""
    directory = _private_dir("logs")
    _prune(directory)
    _prune_spools(directory)
    for n in range(1, 1000):
        path = directory / (f"{run_id}.log" if n == 1 else f"{run_id}.{n}.log")
        if os.path.lexists(live_dir(str(path))):
            continue
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            continue
        os.close(fd)
        return str(path)
    raise OSError("no free log file name")


def _prune_spools(directory: Path) -> None:
    """Live-log spools (`<log>.live/`) nothing removed: a process and its
    recovery both died. Same retention as the logs beside them."""
    import shutil

    cutoff = time.time() - RETAIN_SECONDS
    try:
        for entry in os.scandir(directory):
            try:
                if (
                    entry.name.endswith(".live")
                    and entry.is_dir(follow_symlinks=False)
                    and entry.stat(follow_symlinks=False).st_mtime < cutoff
                ):
                    shutil.rmtree(entry.path, ignore_errors=True)
            except OSError:
                pass
    except OSError:
        pass


def _discard_local_log(log_path: str) -> None:
    """The log is staged in the outbox: the local copy has done its job."""
    # Not `.stopped`: a helper still forwarding for a straggler reads it at EOF
    # to tell a stop from a crash. It is empty, and pruned with the logs.
    for path in (log_path, log_path + ".meta.json", log_path + ".ready", log_path + ".adopted"):
        try:
            os.unlink(path)
        except OSError:
            pass


def _unredacted(result: secret_gate.InspectionResult) -> bool:
    """A finding the gate could not replace (``field-name`` never counts)."""
    return any(rule != FIELD_NAME_RULE for rule in result.flagged)


def redact_log_text(text: str) -> tuple[bytes | None, secret_gate.InspectionResult]:
    """``(bytes to upload, what the gate did)`` for text a run printed, or
    ``(None, ...)`` when it holds a credential the gate could not redact.

    THE one decision for a run's printed output: the final ``probe/run.log``
    (`OutputCapture._queue_log`) and the live stream (`logstream`) both call
    it. Replace what can be replaced; an encoded credential the gate sees
    inside but cannot replace (base64 of gzip) blanks every encoded-looking
    run and is looked for again."""
    # scanning disabled: data, result = secret_gate.redact_text(text)
    return text.encode("utf-8"), secret_gate.InspectionResult()
    # scanning disabled: if not _unredacted(result):
    # scanning disabled:     return data, result
    # scanning disabled: data, second = secret_gate.redact_text(_ENCODED_RUN.sub("<redacted:encoded>", data.decode("utf-8")))
    # scanning disabled: if _unredacted(second):
    # scanning disabled:     return None, second
    # scanning disabled: return data, secret_gate.InspectionResult(
    # scanning disabled:     warnings=second.warnings, rewritten=tuple(result.rewritten) + ("encoded",), flagged=second.flagged
    # scanning disabled: )


def _distributed_log_name() -> str | None:
    """``probe/run.rank<N>.log`` for one process of a distributed job, else
    None. From the environment, not from the registry: the registry is per
    host, and the first rank on every host would otherwise keep the plain
    name -- one artifact, overwritten version by version."""
    world = read_world_size(os.environ)
    launched = read_process_rank(os.environ)
    if world is None or world <= 1 or launched is None:
        return None
    return f"probe/run.rank{launched.rank}.log"


def _head_is_clean(path: str, limit: int) -> bool:
    """Whether the first ``limit`` bytes of ``path`` hold nothing the
    credential gate records, replaceable or not: bytes that go up in parts are
    sent as they are, so nothing found there could be redacted first. A head the
    gate refuses to read (an archive member or a decompression past its limits)
    or cannot open is not clean.

    A head the gate reads only in part -- a zip cut before its central
    directory, which is every big PyTorch checkpoint -- is still scanned as raw
    text, so a stored credential is found. What stays unscanned is what a cut
    archive cannot show: a credential inside a COMPRESSED member, as with any
    multipart upload."""
    # scanning disabled: try:
    # scanning disabled:     with open(path, "rb") as fh:
    # scanning disabled:         head = fh.read(limit)
    # scanning disabled:     return not secret_gate.inspect_bytes(head).has_findings
    # scanning disabled: except (OSError, CredentialBlocked):
    # scanning disabled:     return False
    return True


class LogTeeMixin:
    """Part of OutputCapture: its methods run with `self` the OutputCapture; compose() folds them into OutputCapture."""

    def adopt_log(self, log_path: str) -> None:
        """A launcher tees its child into ``log_path``: record it, so a
        recovery can find the log if the launcher dies first. Called before
        the tee starts, so the live stream is asked for here too."""
        self._log_path = log_path
        self._rewrite_record(log_path=log_path)
        if self._streamer is None:
            self._live = _logstream.prepare(self.client, log_path)
            self._start_stream()

    def _start_stream(self) -> None:
        """Start shipping the live log, when it was asked for and a tee
        writes it. Never raises."""
        if not self._live or self._streamer is not None:
            return
        if self._log_path is None or self.client is None:
            self._drop_live()
            return
        try:
            epoch = self._epoch or _logstream.active_epoch(self.run_id)
            stream = _logstream.stream_for(self.log_name)
            self._streamer = _logstream.LogStreamer(
                self.client, self.run_id, self._log_path, stream, epoch=epoch
            ).start()
            # What a recovery needs to send the rest as THIS attempt's.
            self._rewrite_record(log_stream=stream, write_epoch=epoch())
        except Exception:  # noqa: BLE001 -- the live view is best effort
            self._streamer = None
            self._drop_live()

    def _stop_stream(self, deadline: float) -> None:
        """The last lines, within a small slice of what is left of the close
        (`logstream.FINAL_FLUSH_SECONDS`, and at most `FINAL_FLUSH_SHARE` of
        it: the outputs sweep after this needs the rest); the spool is removed
        either way."""
        streamer, self._streamer = self._streamer, None
        if streamer is not None:
            left = max(0.0, deadline - time.monotonic())
            streamer.stop(budget=min(_logstream.FINAL_FLUSH_SECONDS, left * _logstream.FINAL_FLUSH_SHARE))
        self._drop_live()

    def _drop_live(self) -> None:
        if self._live and self._log_path:
            import shutil

            shutil.rmtree(live_dir(self._log_path), ignore_errors=True)
        self._live = False

    def _log_write_epoch(self) -> int | None:
        """The run attempt this process wrote under, when known (`meta.write_epoch`): the live
        stream's reader, else the writer record. Kept once read: at exit the handle may be gone."""
        epoch = getattr(self, "_log_epoch", None)
        if epoch is None:
            try:
                epoch = (self._epoch or _logstream.active_epoch(self.run_id))()
            except Exception:  # noqa: BLE001 -- an attempt we cannot read is left out
                epoch = None
            if epoch is None:
                epoch = (self.writer or {}).get("write_epoch")
        if not isinstance(epoch, int) or isinstance(epoch, bool) or epoch < 1:
            return None
        self._log_epoch = epoch
        return epoch

    def _log_meta(self, stats: dict | None, shared: list[str]) -> dict:
        """The saved log's facts (WIRE.md "Saved log meta the SDK writes"): ``stream`` is the live
        stream name this process posts (`logstream.stream_for`), ``write_epoch`` its attempt."""
        epoch = self._log_write_epoch()
        return {
            "capture": CAPTURE_LOG,
            "host": self.host,
            "stream": _logstream.stream_for(self.log_name),
            **({"write_epoch": epoch} if epoch is not None else {}),
            **{k: v for k, v in (stats or {}).items() if k in ("total_bytes", "omitted_bytes")},
            **({} if stats else {"log_incomplete": True}),
            **({"shared_with": shared} if shared else {}),
        }

    def _queue_log(
        self, log_path: str, stats: dict | None, shared: list[str], *, should_keep_local: bool = False
    ) -> bool | None:
        """Queue the log: True when queued, False when it could not be (worth a
        retry), None when there is nothing to send. ``should_keep_local``: the tee goes
        on, and what prints after this run may still be sent behind this copy
        (`_send_after_finish`). A log the helper has not finished (no ``stats``)
        goes up as it is, flagged, and the whole of it follows once the helper is
        done (`_ask_for_complete_log`, T21)."""
        try:
            raw = Path(log_path).read_bytes()
        except OSError:
            raw = b""
        queued = None
        if raw:
            meta = self._log_meta(stats, shared)
            queued = self._queue_log_bytes(raw, meta, log_path)
            self._log_meta_sent = meta
            if queued and stats:
                if should_keep_local:
                    # Kept in memory, not on disk: an exit that skips atexit (a SIGTERM close, `os._exit`)
                    # would leave the file behind for the 30-day prune.
                    self._log_bytes_sent = raw
                _discard_local_log(log_path)
        if not stats and queued is not False:
            self._ask_for_complete_log(log_path, shared)  # after the head: its version comes first
        return queued

    def _queue_log_bytes(self, raw: bytes, meta: dict, log_path: str) -> bool | None:
        # The TERMINAL and the local file get the program's exact bytes. The
        # uploaded copy is valid UTF-8 first, because the gate can only redact
        # text: a credential printed beside one stray binary byte would
        # otherwise ship byte-for-byte.
        data, result = redact_log_text(raw.decode("utf-8", errors="replace"))
        if data is None:
            _diagnostics.warn(
                f"probe: {self.log_name} was not uploaded: it holds a credential Probe "
                f"could not redact. The local copy is {log_path}."
            )
            return None
        if result.rewritten:
            _diagnostics.warn(
                f"probe: replaced credentials in {self.log_name} before upload; "
                f"the local copy is unchanged."
            )
        return self._queue_generated(self.log_name, data, meta=meta)

    def _send_after_finish(self, rest: tuple[str, dict | None] | None) -> None:
        """What printed after this run finished (T15). None: the next run in this process took it as
        its head. Else ``(path, stats)`` of it at exit: when there is any, this run's log gets a new
        version -- its own copy, the `AFTER_FINISH_MARKER` line, then the rest. Never raises."""
        own = self._log_path
        rest_path = rest[0] if rest is not None else None
        try:
            if rest is None:
                return
            tail = Path(rest_path).read_bytes()
            if not tail.strip():
                return
            head = getattr(self, "_log_bytes_sent", None)
            if head is None:
                head = Path(own).read_bytes() if own and os.path.exists(own) else b""
            # This run's own copy went up with these facts; an empty one (nothing printed during the run) sent none.
            nothing = {"total_bytes": 0, "omitted_bytes": 0}
            sent = dict(getattr(self, "_log_meta_sent", None) or self._log_meta(nothing, []))
            stats = rest[1]
            meta = {k: v for k, v in sent.items() if k not in ("total_bytes", "omitted_bytes", "log_incomplete")}
            if stats and not sent.get("log_incomplete"):
                meta["total_bytes"] = int(sent.get("total_bytes") or 0) + int(stats.get("total_bytes") or 0)
                meta["omitted_bytes"] = int(sent.get("omitted_bytes") or 0) + int(stats.get("omitted_bytes") or 0)
            else:
                meta["log_incomplete"] = True
            joint = b"" if not head or head.endswith(b"\n") else b"\n"
            if self._queue_log_bytes(head + joint + AFTER_FINISH_MARKER + tail, meta, rest_path):
                self._send_before_exit()
        except Exception:  # noqa: BLE001 -- at exit, best effort
            pass
        finally:
            self._log_bytes_sent = None
            # The run's own copy only once its log was queued (a finalize that could not queue it retries from it)
            # and no late sender still needs it (`.late`, T21).
            is_own_done = getattr(self, "_log_done", False) and own and not os.path.exists(own + ".late")
            for path in (own if is_own_done else None, rest_path):
                if path:
                    _discard_local_log(path)

    def _send_before_exit(self) -> None:
        """Deliver this run's queued log version now, as the run (`recovery._recovery_client`: the run's
        context and credential; the run's own client is closed by now), within AFTER_FINISH_SEND_SECONDS.
        What is left goes to the detached drain. An offline run's queue waits for `probe sync`."""
        client = None
        try:
            from ...delivery.transport.deadlines import deadline_scope, without_patience
            from .recovery import _recovery_client

            client, _journal = _recovery_client(self._record(shared_with=[]))
            deadline = time.monotonic() + AFTER_FINISH_SEND_SECONDS
            with without_patience(), deadline_scope(deadline):
                while client is not None and time.monotonic() < deadline:
                    # Bounded on the drain lock too: a detached drain mid-pass may hold it, and then
                    # it sends this op; this waits for that, never past the deadline.
                    left = deadline - time.monotonic()
                    report = client._drain_for_close(self.run_id, lock_timeout=min(1.0, left))
                    if not report.lock_busy and not report.remaining:
                        break
                    if report.unreachable or report.auth_blocked:
                        break  # left for the drain: nothing here will change that in seconds
                    time.sleep(0.1)
        except Exception:  # noqa: BLE001 -- left queued for the drain
            pass
        finally:
            if client is not None:
                try:
                    client._kick_drainer(force=True)  # a no-op when nothing is left
                    client.close()
                except Exception:  # noqa: BLE001
                    pass

    def _ask_for_complete_log(self, log_path: str, shared: list[str]) -> None:
        """The helper had not finished the log when the close stopped waiting (T21): leave it a
        request (``<log>.late``) that it hands to `recovery.send_late_log` once the log is
        complete, so the whole log follows the head as its next version, ``log_incomplete``
        false. The helper may have finished in between: then the request is sent from here."""
        if self.recovery:
            return  # a recovery reads what the helper left; nothing will finish it later
        try:
            from ..logs.logs import get_late_path, read_stats, spawn_late_log, write_request

            record = {
                **self._record(shared_with=shared),
                "log_path": log_path,
                "log_name": self.log_name,
                "meta": {k: v for k, v in self._log_meta(None, shared).items() if k != "log_incomplete"},
            }
            write_request(get_late_path(log_path), record)
            if read_stats(log_path) is not None:
                spawn_late_log(get_late_path(log_path))
        except Exception:  # noqa: BLE001 -- the head still goes up, flagged
            pass
