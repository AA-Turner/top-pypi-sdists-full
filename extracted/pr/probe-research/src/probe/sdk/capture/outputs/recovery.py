"""finish a dead run's capture from another process (`--recover`), report a writer that is gone (`--writer-gone`),
and send a log its helper finished after the close (`--late-log`)."""

from __future__ import annotations
import json
import os
import time
from pathlib import Path
from typing import Any

from ....foundation.os_backend import os_backend as oscompat
from ...recording_rules import recording_rules as _ignore
from ..logs import stream as _logstream
from ..logs.logs import _spawn_recovery, read_stats
#: A recovery claim older than this belongs to a recoverer that died.
CLAIM_STALE_SECONDS = 600


# -- recovery ------------------------------------------------------------------------------
def _claim_path(entry: Path) -> Path:
    return Path(str(entry) + ".recovering")


def _claim_fresh(entry: Path) -> bool:
    try:
        return time.time() - _claim_path(entry).stat().st_mtime < CLAIM_STALE_SECONDS
    except OSError:
        return False


def _claim(entry: Path) -> bool:
    """One recoverer per record, across processes. A claim left by a recoverer
    that died goes stale and is taken over."""
    claim = _claim_path(entry)
    for _ in range(2):
        try:
            fd = os.open(str(claim), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if _claim_fresh(entry):
                return False
            claim.unlink(missing_ok=True)
            continue
        except OSError:
            return False
        os.close(fd)
        return True
    return False


def _is_offline_queue(journal_dir: str | None) -> bool:
    """Whether ``journal_dir`` is an offline run's queue (it holds the offline manifest)."""
    if not journal_dir:
        return False
    from ...delivery.offline.offline import MANIFEST_NAME

    return (Path(journal_dir) / MANIFEST_NAME).is_file()


def _is_offline_record(record: dict) -> bool:
    """Whether the dead process recorded an offline run: its queue, or its `local:` id."""
    from ...delivery.offline.offline import LOCAL_PREFIX

    return _is_offline_queue(record.get("journal_dir")) or str(record.get("run_id") or "").startswith(LOCAL_PREFIX)


def _recovery_client(record: dict) -> tuple[Any, Any]:
    """``(client, journal)`` for the context the run was opened under -- never
    whatever context is current where recovery happens to run. When that
    context no longer resolves to the same server, only the journal: the ops
    wait there for a drain under the right credentials."""
    context = record.get("context") or {}
    if _is_offline_record(record):
        # An offline run's own queue: only `probe sync` delivers it, after its server and team
        # checks. Recovery queues into it and never sends; a queue deleted since gets nothing.
        if not _is_offline_queue(record.get("journal_dir")):
            return None, None
        from ...delivery.journal.journal import Journal

        journal = Journal(record.get("journal_dir"), context=context)
        journal.op_ceiling = 0  # as the live offline client: nothing drains it before `probe sync`
        return None, journal
    try:
        from ...client.client import Client
        from ...settings.settings import resolve

        if context.get("principal"):
            # The run recorded which credential it wrote with (#2035): the
            # recovery lists and uploads with THAT one, or with none -- never
            # with whatever this process resolves (#2041 review). The same
            # rule the drain applies to the run's queued writes.
            from ...delivery.outbox.drain.credentials import _settings_for_op

            settings = _settings_for_op(context)
        else:
            settings = resolve(context=context.get("name") or None)
        recorded = (context.get("base_url") or "").rstrip("/")
        if recorded and settings.base_url != recorded:
            raise RuntimeError("the run's context now points elsewhere")
        from ...delivery.journal.journal import Journal

        journal = Journal(record.get("journal_dir") or None, context=context)
        client = Client(settings=settings, journal=journal)
        return client, journal
    except Exception:  # noqa: BLE001 -- no credentials here: queue for a later drain
        from ...delivery.journal.journal import Journal

        return None, Journal(record.get("journal_dir") or None, context=context)


def recover(entry_path: str) -> dict | None:
    """Finish the capture of a run whose process died: sweep its folder against
    the baseline it recorded, queue its log, deliver what can be delivered.

    Started by the log helper the moment it sees the run's process gone. Runs
    in a fresh interpreter with the run's own environment."""
    entry = Path(entry_path)
    try:
        record = json.loads(entry.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _claim(entry):
        return None
    client, journal = _recovery_client(record)
    try:
        if client is None and journal is None:
            return None  # an offline run whose queue was deleted: nothing to queue into
        capture = OutputCapture(
            client,
            record["run_id"],
            record["root"],
            tee=False,
            launcher=bool(record.get("launcher")),
            journal=journal,
            recovery=True,
            ignore=_ignore.from_record(record.get("ignore")),
            # The attempt the dead process wrote under: the recovered log's `meta.write_epoch`.
            writer=record.get("writer") or ({"write_epoch": record["write_epoch"]} if record.get("write_epoch") else None),
        )
        capture._entry = entry
        capture.log_name = str(record.get("log_name") or LOG_NAME)
        capture._baseline_file = Path(record["baseline"]) if record.get("baseline") else None
        if capture._baseline_file is None:
            capture._sweep_done = True  # a log-only recovery (see _recover_stale_logs)
        else:
            try:
                raw = json.loads(capture._baseline_file.read_text())
                capture.baseline = {k: (int(v[0]), int(v[1])) for k, v in raw.items()}
            except (OSError, ValueError, TypeError, IndexError, AttributeError):
                # Without its baseline every file would look new: never guess.
                capture._sweep_done = True
        log_path = record.get("log_path")
        summary = capture.finalize(log_path=log_path, log_stats=read_stats(log_path) if log_path else None)
        if log_path:
            # The live stream's last lines -- often the crash itself -- from
            # where the dead process's shipper stopped.
            _logstream.drain_spool(
                client,
                record["run_id"],
                log_path,
                capture.log_name,
                budget=_logstream.FINAL_FLUSH_SECONDS,
                stream=record.get("log_stream") or None,
                write_epoch=record.get("write_epoch"),
            )
        if client is not None:
            try:
                client.flush(run_ref=record["run_id"])
            except Exception:  # noqa: BLE001 -- left queued for the drainer
                client._kick_drainer(force=True)
        return summary
    finally:
        for path in (entry, _claim_path(entry), *entry.parent.glob(f"{entry.name}.writer-*")):
            path.unlink(missing_ok=True)


def send_late_log(request_path: str) -> dict | None:
    """The whole log a close sent only the head of (T21): its helper finished it late and hands
    over the close's request (``<log>.late``). Sent once, as the log's next version with
    ``log_incomplete`` false, through the run's journal; the local copy is then removed."""
    request = Path(request_path)
    try:
        record = json.loads(request.read_text())
    except (OSError, ValueError):
        return None
    if not isinstance(record, dict) or not _claim(request):
        return None
    log_path = str(record.get("log_path") or "")
    try:
        stats = read_stats(log_path) if log_path else None
        if stats is None:
            return None  # never finished: the head stays the run's log
        client, journal = _recovery_client(record)
        if client is None and journal is None:
            return None
        capture = OutputCapture(
            client,
            record["run_id"],
            str(record.get("root") or os.path.dirname(log_path)),
            tee=False,
            launcher=bool(record.get("launcher")),
            journal=journal,
            recovery=True,
        )
        capture.log_name = str(record.get("log_name") or LOG_NAME)
        meta = {
            **dict(record.get("meta") or {}),
            **{k: v for k, v in stats.items() if k in ("total_bytes", "omitted_bytes")},
            "log_incomplete": False,
        }
        raw = Path(log_path).read_bytes()
        queued = bool(raw) and bool(capture._queue_log_bytes(raw, meta, log_path))
        if queued:
            _discard_local_log(log_path)
            if client is not None:
                from ...delivery.transport.deadlines import deadline_scope

                try:
                    with deadline_scope(time.monotonic() + AFTER_FINISH_SEND_SECONDS):
                        client._drain_for_close(record["run_id"], lock_timeout=AFTER_FINISH_SEND_SECONDS)
                except Exception:  # noqa: BLE001 -- left queued for the drainer
                    pass
                client._kick_drainer(force=True)  # a no-op when nothing is left
        return {"queued": queued}
    except OSError:
        return None
    finally:
        for path in (request, _claim_path(request)):
            path.unlink(missing_ok=True)


def _gone_path(entry: Path) -> Path:
    return Path(str(entry) + ".gone")


def _process_start(pid: int) -> str | None:
    """The kernel's start time of ``pid`` (/proc/<pid>/stat field 22, in clock
    ticks since boot), or None where /proc cannot say. With the pid, it names
    ONE process: a pid the kernel reused for another process has another."""
    try:
        stat = Path(f"/proc/{int(pid)}/stat").read_text()
    except (OSError, ValueError):
        return None
    # The command name (field 2) may hold spaces and parentheses: split after
    # its LAST ")".
    fields = stat.rsplit(")", 1)[-1].split()
    return fields[19] if len(fields) > 19 else None


def mark_forked_writer(entry: Path | str, pid: int) -> None:
    """A forked child of the run's process is writing the run (see
    `Run._note_forked_writer`): ``ENTRY.writer-<pid>``, holding the child's
    start time so a later check cannot mistake a reused pid for it."""
    marker = Path(f"{entry}.writer-{int(pid)}")
    marker.touch(mode=0o600, exist_ok=True)
    start = _process_start(pid)
    if start is not None:
        try:
            marker.write_text(start)
        except OSError:
            pass


def _forked_writer_alive(entry: Path) -> int | None:
    """The pid of a forked child still writing this record's run, or None.
    Same host by construction: the registry is per host. A marker whose pid
    now names ANOTHER process (a different start time: the pid was reused)
    counts as gone (review of #2049)."""
    for marker in entry.parent.glob(f"{entry.name}.writer-*"):
        try:
            pid = int(marker.name.rsplit("-", 1)[1])
            oscompat.probe_pid(pid)
        except (ValueError, ProcessLookupError):
            marker.unlink(missing_ok=True)
            continue
        except PermissionError:
            continue  # another user's process: never this run's forked writer
        except OSError:
            continue
        try:
            recorded = marker.read_text().strip()
        except OSError:
            recorded = ""
        if recorded and _process_start(pid) not in (None, recorded):
            marker.unlink(missing_ok=True)  # the pid now names another process
            continue
        return pid
    return None


def writer_gone(entry_path: str) -> dict | None:
    """Report that this record's writer process is gone (SDK reliability 2.2).

    Started by the log helper the moment the run's process is reparented away
    from it -- a SIGKILL, the OOM killer, a segfault -- so the server can end a
    sole-writer run within seconds instead of after the reaper's 900 s. One
    report per record (``ENTRY.gone``, created exclusively, then holding the
    outcome). Only to a server that declares ``run_writer_gone``; one retry on
    a transient failure, then the op is queued for the drainer. The server
    decides whether the report is the whole story (sole writer, same epoch),
    so a report is never a verdict on its own.
    """
    entry = Path(entry_path)
    gone = _gone_path(entry)
    try:
        fd = os.open(str(gone), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        os.close(fd)
    except OSError:
        return None  # already reported (or cannot be claimed): once is enough
    outcome: dict = {"sent": False}
    try:
        try:
            record = json.loads(entry.read_text())
        except (OSError, ValueError):
            outcome["reason"] = "no_record"
            return outcome
        writer = (record.get("writer") if isinstance(record, dict) else None) or {}
        run_id = record.get("run_id") if isinstance(record, dict) else None
        if not run_id or not writer.get("session_id") or writer.get("write_epoch") is None:
            outcome["reason"] = "no_writer"
            return outcome
        body = {
            "session_id": str(writer["session_id"]),
            "write_epoch": int(writer["write_epoch"]),
            "observed_by": "output_helper",
            "host": record.get("host"),
            "pid": record.get("pid"),
            "sole_writer": bool(writer.get("sole_writer")),
        }
        survivor = _forked_writer_alive(entry)
        if survivor is not None:
            # A daemonizing script: the process that opened the run forked and
            # exited, and its child carries the run on (review of #2049).
            outcome["reason"] = "writer_continues"
            outcome["pid"] = survivor
            return outcome
        client, journal = _recovery_client(record)

        def queue() -> dict:
            # Queued for the drainer: a partition must not lose the report
            # (review of #2049). Non-blocking, so a server that turns out to
            # lack the route dead-letters it without holding anything, and the
            # server still judges it when it lands (a late report on a run a
            # relaunch reopened is `stale_epoch`, a no-op).
            try:
                journal.append_http(
                    "POST",
                    f"/v1/runs/{run_id}/writer-gone",
                    body,
                    run_ref=str(run_id),
                    blocking=False,
                )
                if client is not None:
                    client._kick_drainer(force=True)
                outcome["queued"] = True
            except Exception:  # noqa: BLE001 -- the reaper still ends the run
                pass
            return outcome

        if client is None:
            outcome["reason"] = "no_client"
            return queue()
        try:
            if not client.supports_feature("run_writer_gone"):
                outcome["reason"] = "unsupported"
                return outcome
        except Exception:  # noqa: BLE001 -- unreachable now; the drainer retries
            outcome["reason"] = "unreachable"
            return queue()
        from ... import errors as _errors

        for attempt in range(2):
            try:
                outcome.update(client.report_writer_gone(str(run_id), body) or {})
                outcome["sent"] = True
                return outcome
            except _errors.TransportError as exc:
                outcome["error"] = type(exc).__name__
                if attempt == 0:
                    time.sleep(1.0)
            except _errors.ServerError as exc:
                outcome["error"] = type(exc).__name__
                if attempt == 0:
                    time.sleep(1.0)
            except Exception as exc:  # noqa: BLE001 -- a refusal is final
                outcome["error"] = type(exc).__name__
                return outcome
        return queue()
    finally:
        try:
            _write_json(gone, outcome)
        except OSError:
            pass


def _recover_stale_logs() -> None:
    """Records whose process died and whose helper could not recover them (the
    whole process group was killed, or log capture was off). Only the LOG is
    sent: sweeping a folder long after the run would attribute other runs'
    files to it. A record whose helper still runs is its helper's to recover."""
    try:
        registry = _registry()
        entries = _entries()
    except OSError:
        return
    for path, record in entries:
        if _record_alive(record) or _helper_alive(record) or _claim_fresh(path):
            continue
        try:
            baseline = record.get("baseline")
            if baseline:
                Path(str(baseline)).unlink(missing_ok=True)
            record["baseline"] = None  # log only
            _write_json(path, record)
        except (OSError, TypeError, ValueError):
            continue
        _spawn_recovery(str(path))
    _prune(registry)


def _default_signals() -> None:
    """The log helper that starts a recovery ignores nearly every signal, and
    ignored signals survive exec: a recovery (and the drainer it starts) that
    inherited them could be stopped by nothing short of SIGKILL."""
    import signal

    from ..logs.logs import _IGNORED_SIGNALS

    for name in _IGNORED_SIGNALS:
        signum = getattr(signal, name, None)
        if signum is None or name == "SIGPIPE":
            continue  # Python keeps SIGPIPE ignored; so does this
        try:
            signal.signal(signum, signal.default_int_handler if name == "SIGINT" else signal.SIG_DFL)
        except (OSError, ValueError, RuntimeError):
            pass
from probe.sdk.capture.outputs.host_registry import _entries, _helper_alive, _record_alive, _registry, _write_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.log import AFTER_FINISH_SEND_SECONDS, LOG_NAME, _discard_local_log, _prune  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.outputs import OutputCapture  # noqa: E402 -- pieces need each other; the front door loads this one first


def run_command(argv: list[str]) -> None:
    """`python -m probe.sdk.outputs --recover|--writer-gone <entry>`: the log helper's call after a hard kill."""
    if len(argv) == 2 and argv[0] == "--recover":
        _default_signals()
        recover(argv[1])
    elif len(argv) == 2 and argv[0] == "--writer-gone":
        _default_signals()
        writer_gone(argv[1])
    elif len(argv) == 2 and argv[0] == "--late-log":
        _default_signals()
        send_late_log(argv[1])
