"""`RolloutCapture`: one rollout's messages as sent, its tool runs, and the files its own code attaches, hung on one
`environment` span and exported into the adapter's own generator part (D1). Fail-open: nothing here raises into the
rollout. Why: DESIGN.md "Rollout capture"."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import tempfile
import threading
from collections.abc import Iterable, Mapping
from contextvars import ContextVar, Token
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .....foundation.safe_warn import safe_warn as _diagnostics
from .messages import build_turns
from .uploads import UPLOAD_TIMEOUT_S, Attachment, get_upload_pool

if TYPE_CHECKING:
    from ...run import Run

#: The span every attaching rollout hangs its files on. Never `rollout`: that span type becomes a Trial (0135/0136)
#: and turns on the Trials view (D9).
ENVIRONMENT_SPAN = "environment"
#: The fields an export carries into a generator part (`update_part`); `extras` is merged, never replaced.
PART_FIELDS = ("turns", "turns_blob", "turn_count", "turns_source", "environment")
#: Files one sample names in `environment.logs` / `.outputs` (the contract's `MAX_TRIAL_FILES`).
MAX_FILES = 256
#: One segment of an artifact name, in bytes (the server's per-component cap; names here are ASCII).
MAX_NAME_SEGMENT = 255
#: A tool call's id and name (`TurnToolCall`), in characters.
MAX_CALL_CHARS = 256
_SAFE = re.compile(r"[^A-Za-z0-9_.:=@+-]+")
_CURRENT: ContextVar[RolloutCapture | None] = ContextVar("probe_rollout_capture", default=None)
#: This context's (capture, token) per open ``with capture:``: a task or thread restores only its own value.
_ENTERED: ContextVar[tuple[tuple[RolloutCapture, Token], ...]] = ContextVar("probe_rollout_entered", default=())
_WARNED: set[str] = set()
_WARNED_LOCK = threading.Lock()


def warn_once(key: str, message: str, *, stacklevel: int = 2) -> None:
    """One warning per ``key`` per process; ``stacklevel`` counts from this function's caller."""
    with _WARNED_LOCK:
        if key in _WARNED:
            return
        _WARNED.add(key)
    _diagnostics.warn(message, stacklevel=stacklevel + 1)


def get_current_rollout() -> RolloutCapture | None:
    """The rollout this code runs in (an adapter opened it), else None. Rides `asyncio` tasks the rollout starts;
    not threads or other processes (those get a handle: `RolloutCapture.from_handle`)."""
    return _CURRENT.get()


def attach_file(path: str | os.PathLike, *, role: str, as_log: bool = False) -> Attachment | None:
    """Attach the file at ``path`` to the rollout this code runs in (`RolloutCapture.attach_file`). Outside a
    rollout: None, and one warning. Never raises."""
    capture = _find_rollout("attach_file")
    return None if capture is None else capture.attach_file(path, role=role, as_log=as_log)


def attach_text(name: str, text: str, *, role: str, as_log: bool = False) -> Attachment | None:
    """Attach ``text`` as the file ``name`` to the rollout this code runs in. Outside a rollout: None, and one
    warning. Never raises."""
    capture = _find_rollout("attach_text")
    return None if capture is None else capture.attach_text(name, text, role=role, as_log=as_log)


def _find_rollout(what: str) -> RolloutCapture | None:
    capture = _CURRENT.get()
    if capture is None:
        warn_once("outside", f"probe: samples.{what} ran outside a rollout Probe captures (no adapter opened one "
                  "here, or this thread or process does not carry it), so nothing was attached. Later calls are not "
                  "shown.", stacklevel=4)  # fmt: skip
    return capture


class RolloutCapture:
    """One rollout's capture. An adapter opens it as ambient context (``with RolloutCapture(run, key):``), the
    rollout's tools call `probe.samples.attach_file` / `attach_text`, the adapter records the messages and tool runs,
    and `export()` gives the fields its generator part carries (`update_part`)."""

    def __init__(self, run: Run, attempt_key: str, *, epoch: int | None = None, span_id: str | None = None,
                 upload_timeout: float = UPLOAD_TIMEOUT_S) -> None:  # fmt: skip
        self._run = run
        self.attempt_key = str(attempt_key)
        self.epoch = int(epoch or getattr(run, "write_epoch", None) or 1)
        self.upload_timeout = upload_timeout
        self._span_id = span_id
        #: Whether this capture wrote the span (its first attach), and when that write was queued (uploads wait for it).
        self._is_span_open = False
        self._span_sent = threading.Event()
        self._span_started_at: str | None = None
        #: The owner closes the span at export (`_close_span`); every write is final (`_send_span`).
        self._is_span_owner = True
        self._lock = threading.Lock()
        self._attachments: list[Attachment] = []
        self._files: list[dict] = []
        self._turns: list[dict] | None = None
        self._turns_source: str | None = None
        self._tool_runs: dict[str, dict] = {}
        #: Runs recorded with no call id, in order: each fills the first call of its name no run filled yet.
        self._unnamed_runs: list[dict] = []
        self._failed = 0
        #: Everything this capture could not record (attaches, a turns blob, an export), counted.
        self.failures = 0
        self._is_sealed = False

    # -- ambient context ---------------------------------------------------------------------------
    def __enter__(self) -> RolloutCapture:
        token = _CURRENT.set(self)
        _ENTERED.set((*_ENTERED.get(), (self, token)))
        return self

    def __exit__(self, *_exc: object) -> None:
        """Restores THIS context's value from before its own enter: N tasks entering one capture each get theirs."""
        entered = _ENTERED.get()
        index = next((index for index in range(len(entered) - 1, -1, -1) if entered[index][0] is self), None)
        if index is None:  # entered in another context only (a task's parent): that context keeps its own value
            return
        _ENTERED.set(entered[:index] + entered[index + 1:])
        try:
            _CURRENT.reset(entered[index][1])
        except (ValueError, RuntimeError):  # a token copied in from a parent context: never ours to reset
            pass

    # -- across processes --------------------------------------------------------------------------
    @property
    def span_id(self) -> str:
        """The `environment` span's id, derived from the run and the attempt (the same in every process)."""
        if self._span_id is None:
            from ...metrics.spans import _span_id_for

            raw_key = hashlib.sha256(self.attempt_key.encode("utf-8")).hexdigest()
            self._span_id = _span_id_for(str(self._run.id), ENVIRONMENT_SPAN, f"samples/e{self.epoch}/{raw_key}")
        return self._span_id

    def to_handle(self) -> dict:
        """What another process needs to attach to this rollout (verl's reward worker, D11): plain JSON."""
        return {"run_id": str(self._run.id), "attempt_key": self.attempt_key, "epoch": self.epoch,
                "span_id": self.span_id}  # fmt: skip

    @classmethod
    def from_handle(cls, run: Run, handle: Mapping[str, Any]) -> RolloutCapture | None:
        """A capture in another process for the rollout ``handle`` names (`to_handle`): its attachments go back to the
        rollout's own capture through `collect_files` -> `add_files`. None (warned once) for a handle of another run,
        or one that is not a handle: its files would hang on a span of a run this one cannot see."""
        try:
            if str(handle.get("run_id")) != str(run.id):
                warn_once("handle-run", f"probe: a rollout handle for run {handle.get('run_id')!r} was opened in run "
                          f"{run.id!r}, so nothing is attached through it. Later ones are not shown.", stacklevel=3)
                return None
            capture = cls(run, str(handle["attempt_key"]), epoch=handle.get("epoch"), span_id=handle.get("span_id"))
        except Exception as exc:  # noqa: BLE001 -- fail open: never raises into the reward worker
            warn_once("handle-bad", f"probe: a rollout handle could not be opened ({type(exc).__name__}: {exc}), so "
                      "nothing is attached through it. Later ones are not shown.", stacklevel=3)  # fmt: skip
            return None
        capture._is_span_owner = False
        return capture

    # -- what the rollout's code attaches ----------------------------------------------------------
    def attach_file(self, path: str | os.PathLike, *, role: str, as_log: bool = False,
                    name: str | None = None) -> Attachment | None:  # fmt: skip
        """Upload the file at ``path`` (named ``name``, default its file name) onto this rollout: a log of the sample
        (``as_log``) or one of its outputs. Returns at once; the upload runs in a worker thread. None when it could
        not be taken (warned once)."""
        try:
            source = Path(path)
            return self._attach(name or source.name, str(source), role=role, is_log=as_log)
        except Exception as exc:  # noqa: BLE001 -- fail open: an attach never fails the rollout
            self._record_failure("attach_file", exc)
            return None

    def attach_text(self, name: str, text: str, *, role: str, as_log: bool = False) -> Attachment | None:
        """`attach_file` for text in hand (a test run's output, a diff): written to a temp file, uploaded, deleted."""
        temp: str | None = None
        try:
            handle, temp = tempfile.mkstemp(prefix="probe-rollout-", suffix=Path(name).suffix or ".txt")
            with os.fdopen(handle, "w", encoding="utf-8") as out:
                out.write(str(text))
            return self._attach(name, temp, role=role, is_log=as_log, temp_path=temp)
        except Exception as exc:  # noqa: BLE001 -- fail open
            if temp is not None:
                Path(temp).unlink(missing_ok=True)
            self._record_failure("attach_text", exc)
            return None

    def add_files(self, files: Iterable[Mapping[str, Any]], *, failed: int = 0) -> None:
        """Files another process attached to this rollout (`collect_files` there, e.g. verl's reward worker), and how
        many it could not (`failed_count` there)."""
        with self._lock:
            self._files.extend(dict(found) for found in files if isinstance(found, Mapping) and found.get("artifact_id"))
            self._failed += max(0, int(failed))

    @property
    def failed_count(self) -> int:
        """Attaches that were taken but left nothing on the sample (failed, refused or late uploads)."""
        return self._failed

    def collect_files(self) -> list[dict]:
        """Every attached file that landed (each a `TrialFile` plus `is_log`), waiting for the uploads still running
        (each up to `upload_timeout` after its upload STARTED; one still queued, up to the queue timeout after its
        attach, `uploads.get_upload_queue_timeout`). A file that failed or is late is left out and counted."""
        with self._lock:
            pending, self._attachments = self._attachments, []
        for attachment in pending:
            found = attachment.wait(self.upload_timeout)
            if found is None:
                with self._lock:
                    self._failed += 1
                continue
            with self._lock:
                self._files.append(found)
        with self._lock:
            return list(self._files)

    # -- what the adapter records ------------------------------------------------------------------
    def set_turns(self, turns: list[Mapping[str, Any]], *, source: str | None = None) -> None:
        """The sample's turns in the contract's shape (`Turn`), and where they came from (`TurnsSource`; default
        `as_sent`, `decoded` for text Probe rebuilt from tokens)."""
        from .....generated.samples import TurnsSource

        with self._lock:
            self._turns = [dict(turn) for turn in turns]
            self._turns_source = TurnsSource(source or TurnsSource.AS_SENT).value

    def set_messages(self, messages: Iterable[Any], *, should_number_ids: bool = False) -> None:
        """The messages as the framework built them (OpenAI-shaped), as turns (`build_turns`)."""
        self.set_turns(build_turns(messages, should_number_ids=should_number_ids))

    def record_tool_run(self, call_id: str | None, name: str, *, is_ok: bool | None, duration_s: float | None = None,
                        error: str | None = None) -> None:  # fmt: skip
        """One tool call's run: whether it worked (None when unknown, never True by default), how long, its error.
        Joined at export to the turn whose reply asked for ``call_id`` (`TurnToolCall.id`)."""
        found = {"id": call_id[:MAX_CALL_CHARS] if call_id else None, "name": str(name)[:MAX_CALL_CHARS],
                 "is_ok": is_ok, "duration_s": duration_s,
                 "error": " ".join(str(error).split())[:1024] if error else None}  # fmt: skip
        run = {key: value for key, value in found.items() if value is not None}
        with self._lock:
            if call_id:
                self._tool_runs[run["id"]] = run
            else:
                self._unnamed_runs.append(run)

    # -- the export --------------------------------------------------------------------------------
    def export(self) -> dict:
        """The capture as plain JSON for the adapter's own generator part (`update_part`): the turns scrubbed by value
        (inline up to 64 KiB, else a `turns_blob` ref; inline at any size when the blob was not stored), `turns_source`,
        and `environment` (span + files). Closes the span when this capture opened it or the sample names it. Seals the
        capture: a later attach warns and is not linked (A2). Never raises; what failed is left out and counted in
        `extras.attach_failed`."""
        with self._lock:
            self._is_sealed = True
        payload: dict[str, Any] = {}
        try:
            files = self.collect_files()
            if self._turns:
                payload.update(self._export_turns())
                if self._turns_source:  # only with turns: alone it would relabel the part's own (A6)
                    payload["turns_source"] = self._turns_source
            if files:
                payload["environment"] = self._to_environment(files)
            self._close_span(is_named=bool(files))
        except Exception as exc:  # noqa: BLE001 -- fail open: the part goes without what failed
            self._record_failure("export", exc)
        if self._failed:
            payload["extras"] = {"attach_failed": self._failed}
        return payload

    async def export_async(self) -> dict:
        """`export` from a coroutine (verl's agent loop): it waits for uploads, so it runs in a thread, never on the
        event loop."""
        return await asyncio.to_thread(self.export)

    @staticmethod
    def update_part(part: dict, payload: Mapping[str, Any] | None) -> dict:
        """``part`` (a generator part) with an export's fields: the turns (with their `turns_source`) and `environment`
        replace the part's own; `extras` is merged. A payload without turns never touches the part's turns or their
        label (an adapter's `decoded` turns stay `decoded`). The one reader of `export`'s shape."""
        if not isinstance(payload, Mapping):
            return part
        has_turns = payload.get("turns") not in (None, [], {}) or payload.get("turns_blob") not in (None, {})
        for name in PART_FIELDS:
            if name == "turns_source" and not has_turns:
                continue
            if payload.get(name) not in (None, [], {}):
                part[name] = payload[name]
        if has_turns and payload.get("turns_source") is None:
            part.pop("turns_source", None)
        if "turns_blob" in payload:
            part.pop("turns", None)
        extras = payload.get("extras")
        if isinstance(extras, Mapping) and extras:
            part["extras"] = {**(part.get("extras") or {}), **extras}
        return part

    # -- inside -----------------------------------------------------------------------------------
    def _get_span_key(self) -> str:
        """`samples/e<epoch>/<attempt key>`: the key as is when it is a safe name segment, else made one plus a hash
        of the raw key, so two keys that read alike never share a name."""
        safe = _SAFE.sub("_", self.attempt_key)
        if safe != self.attempt_key or len(safe) > MAX_NAME_SEGMENT or safe in ("", ".", ".."):
            digest = hashlib.sha256(self.attempt_key.encode("utf-8")).hexdigest()[:12]
            safe = f"{safe[:MAX_NAME_SEGMENT - 13]}~{digest}"
        return f"samples/e{self.epoch}/{safe}"

    def _attach(self, name: str, path: str, *, role: str, is_log: bool, temp_path: str | None = None) -> Attachment:
        # Checked and the upload queued under ONE hold of the lock: an export between them would miss this file without
        # counting it. The span is SENT after the lock (a low-disk send does network I/O); the upload waits for it.
        should_send_span = False
        try:
            with self._lock:
                is_late = self._is_sealed
                if is_late:
                    self._failed += 1
                else:
                    if not self._is_span_open:
                        self._is_span_open = should_send_span = True
                        self._span_started_at = _get_now()
                    attachment = Attachment(name=str(name), role=str(role), is_log=bool(is_log), temp_path=temp_path)
                    segment = _SAFE.sub("_", str(name))[:MAX_NAME_SEGMENT]
                    segment = "file" if segment in ("", ".", "..") else segment  # never an empty or dot path segment
                    attachment.future = get_upload_pool().submit(self._upload, attachment, path,
                                                                 f"{self._get_span_key()}/{segment}")  # fmt: skip
                    self._attachments.append(attachment)
        finally:
            if should_send_span:  # even when the submit failed: later uploads and the close wait for this write
                self._send_span()
        if is_late:
            warn_once(f"late:{self.attempt_key}", f"probe: {name!r} was attached to rollout {self.attempt_key!r} after "
                      "its sample was written, so the sample does not name it (counted as a failed attach).")  # fmt: skip
            raise _AttachRefused("attached after the rollout's sample was written")
        return attachment

    def _upload(self, attachment: Attachment, path: str, published: str) -> Any:
        """One upload (`log_artifact`, sync): named under the rollout (`samples/e<epoch>/<attempt>/<name>`) so two
        rollouts' identical bytes stay two rows, each on its own span (O2)."""
        attachment.mark_started()
        try:
            # The file cites the span: its write must be queued first (`log_artifact` flushes queued spans, else 422).
            self._span_sent.wait(self.upload_timeout)
            return self._run.log_artifact(
                published, sync=True, path=path, kind="file", span_id=self.span_id, strict=False,
                meta={"sample_file": {"attempt_key": self.attempt_key, "epoch": self.epoch, "role": attachment.role,
                                      "path": attachment.name}},
            )  # fmt: skip
        finally:
            attachment.delete_temp()

    def _send_span(self) -> None:
        """This capture's one write of the rollout's `environment` span, on its first attach (a rollout attaching
        nothing has none), outside the lock. Every write is final (`completed`, started and ended at its first
        attach), the owner's open included: a queued open can reach the server after a direct close (sync mode, or
        the low-disk switch), and a final write landing last can only move `ended_at`, never reopen the span
        (DESIGN.md "Rollout capture"). Never raises; the uploads waiting on it go on either way."""
        try:
            self._write_span("completed", started_at=self._span_started_at, ended_at=self._span_started_at)
        except Exception as exc:  # noqa: BLE001 -- fail open: the uploads still go (a missing span fails them, counted)
            self._record_failure("span", exc)
        finally:
            self._span_sent.set()

    def _close_span(self, *, is_named: bool) -> None:
        """The owner's close (`completed`, now), after its own open: when it opened the span, or the sample names it
        (``is_named``: files a handle attached came back through `add_files`). The span's start stays the first one
        stored (an upsert keeps `started_at`)."""
        if not self._is_span_owner or not (self._is_span_open or is_named):
            return
        if self._is_span_open:
            self._span_sent.wait(self.upload_timeout)  # queued after the open, never before it
        self._write_span("completed", started_at=self._span_started_at, ended_at=_get_now())

    def _write_span(self, status: str, *, started_at: str | None, ended_at: str | None = None) -> None:
        """One upsert of the span by its derived id (the same row from every process). A queued write."""
        self._run.span(ENVIRONMENT_SPAN, id=self.span_id, external_key=self._get_span_key(), name=self.attempt_key,
                       parent_span_id=None, status=status, started_at=started_at, ended_at=ended_at, blocking=False,
                       strict=False)  # fmt: skip

    def _export_turns(self) -> dict:
        from ..wire import MAX_INLINE_TEXT_BYTES, fit_turns, measure_bytes, scrub_part

        turns = _join_tool_runs(fit_turns(self._turns or []), self._tool_runs, self._unnamed_runs)
        turns = scrub_part({"turns": turns}, _scrub_text)["turns"]
        if measure_bytes(turns) <= MAX_INLINE_TEXT_BYTES:
            return {"turns": turns}
        ref = self._store_blob(json.dumps(turns, default=str))
        # Not stored: the turns stay inline and `run.samples.log` spills them as it spills any long turns.
        return {"turns": turns} if ref is None else {"turns_blob": ref, "turn_count": len(turns)}

    def _store_blob(self, text: str) -> dict | None:
        """Turns past 64 KiB, scrubbed, as their own text object through the SDK's one spill (`prepare.write_spill` +
        `upload_spill`): `{sha256, size_bytes}`, or None (counted, warned once) when the bytes were not stored."""
        from ..prepare import upload_spill, write_spill

        blob = write_spill(text)
        try:
            row = upload_spill(self._run, blob, should_wait=True)
        except Exception as exc:  # noqa: BLE001 -- fail open: the turns stay inline
            self._record_failure("turns_blob", exc)
            return None
        finally:
            blob[0].unlink(missing_ok=True)
        if not isinstance(row, dict) or not row.get("id") or row.get("is_reference"):
            self._record_failure("turns_blob", RuntimeError("the upload stored no bytes"))
            return None
        return {"sha256": blob[1], "size_bytes": blob[2]}

    def _to_environment(self, files: list[dict]) -> dict:
        logs = [_to_trial_file(found) for found in files if found.get("is_log")][:MAX_FILES]
        outputs = [_to_trial_file(found) for found in files if not found.get("is_log")][:MAX_FILES]
        environment: dict[str, Any] = {"span_id": self.span_id,
                                       "artifact_ids": [found["artifact_id"] for found in files][:64]}  # fmt: skip
        if logs:
            environment["logs"] = logs
        if outputs:
            environment["outputs"] = outputs
        return environment

    def _record_failure(self, what: str, exc: Exception) -> None:
        if isinstance(exc, _AttachRefused):
            return
        with self._lock:
            self._failed += what.startswith("attach")
            self.failures += 1
        effect = ("its turns stay on the sample inline and `run.samples.log` stores them" if what == "turns_blob"
                  else "its sample leaves that out")  # fmt: skip
        warn_once(f"failed:{what}", f"probe: a rollout's {what} could not record ({type(exc).__name__}: {exc}); the "
                  f"rollout continues, and {effect}. Later failures are counted, not shown.")  # fmt: skip


class _AttachRefused(Exception):
    """An attach after the export: already warned by name, never counted as a failed upload."""


def _join_tool_runs(turns: list[dict], runs: Mapping[str, dict], unnamed: list[dict] = ()) -> list[dict]:
    """Each turn's `tool_calls` with the runs recorded for its calls: a run with an id fills the call with that id; a
    run without one fills the first call of its name, in turn order, no run filled yet. The entry `build_turns` made
    is filled, never repeated; only a run no call matches goes on the last turn as its own entry."""
    if not runs and not unnamed:
        return turns
    left = dict(runs)
    joined = [{**turn, "tool_calls": [dict(call) if isinstance(call, Mapping) else call
                                      for call in turn.get("tool_calls") or ()]} for turn in turns]  # fmt: skip
    filled: set[tuple[int, int]] = set()
    for turn_index, turn in enumerate(joined):
        for call_index, call in enumerate(turn["tool_calls"]):
            found = left.pop(call.get("id"), None) if isinstance(call, Mapping) and call.get("id") else None
            if found:
                call.update(found)
                filled.add((turn_index, call_index))
    extra = list(left.values())
    for run in unnamed:
        spot = next(((turn_index, call_index) for turn_index, turn in enumerate(joined)
                     for call_index, call in enumerate(turn["tool_calls"])
                     if isinstance(call, Mapping) and call.get("name") == run["name"]
                     and (turn_index, call_index) not in filled), None)  # fmt: skip
        if spot is None:
            extra.append(run)
            continue
        filled.add(spot)
        joined[spot[0]]["tool_calls"][spot[1]].update(run)
    if extra and joined:
        joined[-1]["tool_calls"].extend(extra)
    return [turn if turn["tool_calls"] else {key: value for key, value in turn.items() if key != "tool_calls"}
            for turn in joined]  # fmt: skip


def _to_trial_file(found: Mapping[str, Any]) -> dict:
    from ..wire import fit_trial_file

    return fit_trial_file({key: value for key, value in found.items() if key != "is_log"})


def _scrub_text(text: str) -> str:
    from ....redaction import scrub_string

    return scrub_string(text)


def _get_now() -> str:
    return datetime.now(timezone.utc).isoformat()
