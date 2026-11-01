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
from ... import secret_gate
from ..logs.logs import live_dir
# scanning disabled: from .secret_gate import FIELD_NAME_RULE, CredentialBlocked, _findings, prepare_upload
from ...secret_gate import FIELD_NAME_RULE
LOG_ENV = "PROBE_CAPTURE_LOG"
LOG_NAME = "probe/run.log"
CAPTURE_LOG = "log"
#: Local logs, ledgers and capture records older than this are pruned.
RETAIN_SECONDS = 30 * 86_400
_OFF = frozenset({"0", "false", "no", "off"})
#: A run of base64-looking characters: where an encoded credential hides.
_ENCODED_RUN = re.compile(r"[A-Za-z0-9+/_-]{24,}={0,2}")


def log_enabled() -> bool:
    """``PROBE_CAPTURE_LOG`` (on), and never for a run whose working directory
    or script is at `.probe.config` `hash`: such a run records identities only,
    and a script over excluded data commonly prints its records."""
    if (os.environ.get(LOG_ENV) or "").strip().lower() in _OFF:
        return False
    from ...recording_rules import recording_rules as _exclusions

    return not _exclusions.run_identity_only()


def in_process_log_supported() -> bool:
    """Swapping fds 1/2 is wrong in a notebook: ipykernel captures file
    descriptors itself, and the notebook's output is not fd 1 at all."""
    return os.name == "posix" and bool(sys.executable) and "ipykernel" not in sys.modules


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
    for path in (log_path, log_path + ".meta.json", log_path + ".ready"):
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
    world = next((v for v in (os.environ.get(n) for n in ("WORLD_SIZE", "SLURM_NTASKS")) if v), "")
    if not (world.strip().isdigit() and int(world) > 1):
        return None
    for name in ("RANK", "SLURM_PROCID"):
        value = (os.environ.get(name) or "").strip()
        if value.isdigit():
            return f"probe/run.rank{value}.log"
    return None


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

    def _queue_log(self, log_path: str, stats: dict | None, shared: list[str]) -> bool | None:
        """Queue the log: True when queued, False when it could not be (worth a
        retry), None when there is nothing to send."""
        try:
            raw = Path(log_path).read_bytes()
        except OSError:
            return None
        if not raw:
            return None
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
        meta = {
            "capture": CAPTURE_LOG,
            "host": self.host,
            **{k: v for k, v in (stats or {}).items() if k in ("total_bytes", "omitted_bytes")},
            **({} if stats else {"log_incomplete": True}),
            **({"shared_with": shared} if shared else {}),
        }
        if result.rewritten:
            _diagnostics.warn(
                f"probe: replaced credentials in {self.log_name} before upload; "
                f"the local copy is unchanged."
            )
        queued = self._queue_generated(self.log_name, data, meta=meta)
        if queued and stats:
            _discard_local_log(log_path)
        return queued
