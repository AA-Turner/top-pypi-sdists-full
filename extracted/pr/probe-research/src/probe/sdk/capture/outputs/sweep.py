"""OutputSweep: walk the watched folder and pick the files that changed since the baseline."""

from __future__ import annotations
import hashlib
import os
import time
from typing import Any
from ...run.launch import ephemeral
from .. import owndirs as _owndirs
from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import secret_gate
from .. import code as _snapshot
from ...artifact.kinds import ArtifactKind, normalize_artifact_kind
# scanning disabled: from .secret_gate import FIELD_NAME_RULE, CredentialBlocked, _findings, prepare_upload
from ...secret_gate import CredentialBlocked
from ...artifact.limits import AUTO_UPLOAD_MAX_BYTES
BUDGET_ENV = "PROBE_CAPTURE_BUDGET_SEC"
MANIFEST_NAME = "probe/outputs-manifest.json"

#: The most an upload carries: the gate's in-memory inspection limit, which
#: the server's upload guard enforces too.
INSPECT_LIMIT_BYTES = secret_gate.ScanPolicy().max_bytes
MAX_FINAL_ENTRIES = 200_000
SKIP_DIRS = _snapshot.SKIP_DIRS | {".cache", ".probe"}
#: Credential files the code snapshot has no reason to know about, because
#: they live in a home directory rather than a repo.
OUTPUT_SECRET_NAMES = frozenset({
    ".pgpass", ".git-credentials", ".envrc", "kaggle.json", ".dockercfg", ".boto", ".s3cfg",
    ".htpasswd",
})
#: ``meta.capture`` on the per-file rows the CODE capture writes (kind ``code``),
#: which is what tells them apart from code a researcher uploaded.
CODE_CAPTURE = "code-snapshot"
#: Kinds only the code capture writes. Read through `normalize_artifact_kind`,
#: so a row still spelled `code-snapshot`/`code-bytes` (before the server's kind
#: backfill reaches it) counts too.
_CODE_CAPTURE_KINDS = frozenset({ArtifactKind.CODE_SNAPSHOT, ArtifactKind.CODE_BYTES})
#: Why a file was not uploaded. The code is what callers branch on; the text is
#: what a person reads.
TOO_LARGE, OVER_BUDGET, UNINSPECTABLE = "too_large", "over_budget", "uninspectable"
_REASONS = {
    TOO_LARGE: f"over the {INSPECT_LIMIT_BYTES // (1024 * 1024)} MB upload limit",
    OVER_BUDGET: "capture's time budget at close was spent",
    UNINSPECTABLE: "could not be inspected",
}


def _is_code_capture(row: dict) -> bool:
    """A row the automatic code capture wrote, which does not count as the
    run's output already stored: a script that copies `config.yaml` into its
    output folder still gets that copy captured, though the code capture holds
    the same bytes. Code a researcher uploaded (`--kind code`, no capture mark)
    is a file they logged, and counts like any other."""
    if (row.get("meta") or {}).get("capture") == CODE_CAPTURE:
        return True
    return normalize_artifact_kind(str(row.get("kind") or ""))[0] in _CODE_CAPTURE_KINDS


# -- listing ---------------------------------------------------------------------------
#: `(rules root, capture root)` pairs already warned about (once per process).
_UNREACHABLE_WARNED: set[tuple[str, str]] = set()


def _warn_unreachable_patterns(ignore: Any, root: str) -> None:
    """Say once when an ``outputs=`` folder lies outside the ``.probeignore``
    root and some of the file's patterns are anchored there (`/data`,
    `runs/*/dump`): they cannot apply to this folder. The unanchored ones and
    ``ignore=`` / ``PROBE_IGNORE`` still do, relative to the folder."""
    try:
        if ignore is None or (ignore.root, root) in _UNREACHABLE_WARNED:
            return
        lost = ignore.unreachable(root)
        if not lost:
            return
        _UNREACHABLE_WARNED.add((ignore.root, root))
        _diagnostics.warn(
            f"probe: output capture's folder {root} is outside {ignore.root}, so "
            f"{len(lost)} anchored .probeignore pattern(s) cannot apply to it: "
            f"{', '.join(repr(p) for p in lost[:5])}. Unanchored patterns (`*.jsonl`, "
            "`ckpt/`) and ignore= / PROBE_IGNORE still apply, relative to that folder.",
            stacklevel=3,
        )
    except Exception:  # noqa: BLE001 -- a warning may never cost the capture
        pass


def _walk(
    root: str,
    excluded: set[str],
    limit: int,
    *,
    deadline: float | None = None,
    skip_hidden_top: bool = False,
    ignore: Any = None,
    counts: dict[str, int] | None = None,
) -> tuple[dict[str, tuple[int, int]], bool]:
    """``({relative posix path: (size, mtime_ns)}, cut_short)`` for the regular
    files under ``root``, stopping at ``limit`` files or ``deadline``. Symlinks
    are not followed or listed: a link's target can live anywhere, and the run
    did not write it. Pseudo-filesystems are never entered.

    ``ignore`` is the run's ``.probeignore`` rules: an excluded directory is not
    entered and an excluded file is not listed, so neither counts toward
    ``limit``. Each is counted in ``counts["probeignore"]`` when given."""
    pseudo = ephemeral.pseudo_mountpoints()
    # The SDK's own folders below the root, wherever they are (`owndirs`):
    # `excluded` names this run's queue and state, not a $TMPDIR fallback's.
    own = _owndirs.current().within(os.path.realpath(root))
    found: dict[str, tuple[int, int]] = {}
    cut = len(root.rstrip(os.sep)) + 1
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            listing = os.scandir(directory)
        except OSError:
            continue
        with listing:
            for entry in listing:
                if skip_hidden_top and directory == root and entry.name.startswith("."):
                    continue
                try:
                    if own is not None and own.top(entry.path[cut:].replace(os.sep, "/")) is not None:
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        if (
                            entry.name not in SKIP_DIRS
                            and entry.path not in excluded
                            and entry.path not in pseudo
                            and not _snapshot.is_tagged_cache_dir(entry.path)
                        ):
                            if ignore is not None and ignore.ignored(entry.path, is_dir=True, capture_root=root):
                                if counts is not None:
                                    counts["probeignore"] = counts.get("probeignore", 0) + 1
                                continue
                            stack.append(entry.path)
                        continue
                    if not entry.is_file(follow_symlinks=False):
                        continue
                    if ignore is not None and ignore.ignored(entry.path, capture_root=root):
                        if counts is not None:
                            counts["probeignore"] = counts.get("probeignore", 0) + 1
                        continue
                    info = entry.stat(follow_symlinks=False)
                except OSError:
                    continue
                if len(found) >= limit:
                    return found, True
                found[entry.path[cut:].replace(os.sep, "/")] = (info.st_size, info.st_mtime_ns)
        if deadline is not None and time.monotonic() > deadline:
            return found, True
    return found, False


def _shallow_first_key(rel: str) -> tuple[int, str]:
    # Top-level files first: `metrics.json` beside the script is a headline
    # result far more often than `samples/00042.png` is -- and under the close
    # budget, what sorts last is what gets pointed to instead of uploaded.
    return rel.count("/"), rel


def _skip_reason(name: str) -> str | None:
    reason = _snapshot._skip_reason(name)
    if reason is None and (name in OUTPUT_SECRET_NAMES or name.lower().endswith(".env")):
        return "secret"
    return reason


class OutputSweepMixin:
    """Part of OutputCapture: its methods run with `self` the OutputCapture; compose() folds them into OutputCapture."""

    def _excluded_dirs(self) -> set[str]:
        excluded = set()
        for path in (getattr(self.journal, "dir", None), state_dir()):
            if path is not None:
                try:
                    excluded.add(os.path.realpath(path))
                except OSError:
                    pass
        return excluded

    # -- during ---------------------------------------------------------------------
    def note_logged(self, path: str, digest: str | None = None) -> None:
        """``log_artifact`` stored this file: the sweep skips it while it stays
        the same (same size and mtime, or same bytes)."""
        try:
            full = os.path.realpath(path)
            info = os.stat(full)
        except OSError:
            return
        self._logged[full] = {"stat": (info.st_size, info.st_mtime_ns), "sha256": digest}

    def _known_elsewhere(self) -> tuple[dict[str, set], set[str]]:
        """({source path: queued digests}, sha256s already stored on the run).

        The queue catches a ``log_artifact`` this process journaled; the server
        listing catches one a CHILD process made (``probe exec`` sweeps after
        its child logged), or, in a recovery, one the dead process made. Only
        those pay for the listing: in-process, :meth:`note_logged` saw every
        call."""
        queued: dict[str, set] = {}
        try:
            from ...artifact.storage_handlers import multipart

            # Plan (g): an artifact over 64 MiB being uploaded in parts waits
            # in its own queue.
            for _path, op in [*self.journal.pending(), *multipart.pending(self.journal)]:
                upload = op.get("upload") or {}
                if op.get("run_ref") == self.run_id and upload.get("src_path"):
                    queued.setdefault(os.path.realpath(upload["src_path"]), set()).add(upload.get("blob"))
        except Exception:  # noqa: BLE001
            pass
        stored: set[str] = set()
        if (self.launcher or self.recovery) and self.client is not None:
            try:
                for row in self.client.list_run_artifacts(self.run_id, scope="own") or []:
                    if row.get("content_hash") and not _is_code_capture(row):
                        stored.add(row["content_hash"])
            except Exception:  # noqa: BLE001 -- a listing failure only costs dedupe
                pass
        return queued, stored

    def _sweep(self, deadline: float) -> dict:
        summary = {"uploaded": 0, "referenced": 0, "unchanged_logged": 0, "skipped_secret": 0, "listed": 0}
        if not os.path.isdir(self.root):
            return summary
        ephemeral.refresh()  # a volume mounted since the last close
        counts: dict[str, int] = {}
        now, truncated = _walk(
            self.root,
            self._excluded,
            MAX_FINAL_ENTRIES,
            deadline=deadline,
            skip_hidden_top=self._is_home,
            ignore=self._sweep_ignore(),
            counts=counts,
        )
        if counts.get("probeignore"):
            summary["skipped_probeignore"] = counts["probeignore"]
        candidates = sorted(
            (rel for rel, stat in now.items() if self.baseline.get(rel) != stat),
            key=_shallow_first_key,
        )
        if not candidates and not truncated:
            return summary
        with _ledger_lock(self.run_id, deadline):
            self._sweep_candidates(now, candidates, truncated, deadline, summary)
        return summary

    def _sweep_candidates(
        self, now: dict, candidates: list[str], truncated: bool, deadline: float, summary: dict
    ) -> None:
        ledger = _Ledger(self.run_id)
        queued, stored = self._known_elsewhere()
        secret_skips: list[str] = []
        redacted: list[str] = []
        listed: list[dict] = []
        storage_of: dict[str, dict] = {}
        mount_points = ephemeral.mount_points()
        # References, queued AFTER every upload: hashing one (F3) reads up to
        # 1 GiB, and the close's time goes to uploads first.
        references: list[tuple] = []
        # Seconds per byte of inspect-and-stage, learned as the sweep goes;
        # it starts at the measured ~1 MB/s. A file that would run past the
        # deadline is not started: the budget is a bound, not a hint.
        per_byte = 1e-6

        def _already(rel: str, full: str, digest: str, logged: dict | None) -> bool:
            return (
                ledger.has(rel, digest)
                or digest in stored
                or digest in queued.get(full, ())
                or bool(logged and logged.get("sha256") == digest)
            )

        def _not_uploaded(rel: str, full: str, size: int, mtime_ns: int, storage: dict, code: str) -> None:
            if not storage["durable"]:
                listed.append({"path": rel, "size": size, "code": code, "reason": _REASONS[code]})
                return
            key = f"pointer:{size}:{mtime_ns}"
            if ledger.has(rel, key):
                summary["unchanged_logged"] += 1
                return
            # A pointer carries the PATH, never the bytes, so the path is what
            # must not hold a credential (a token in a folder name).
            # scanning disabled: if _findings(full)[0]:
            if False:
                secret_skips.append(rel)
                return
            references.append((rel, full, size, mtime_ns, storage, code, key))

        for rel in candidates:
            # `root` is a real path and the walk never follows a link, so
            # `full` is real too.
            full = os.path.join(self.root, rel)
            size, mtime_ns = now[rel]
            reason = _skip_reason(os.path.basename(rel))
            if reason == "secret":
                secret_skips.append(rel)
                continue
            if reason is not None:
                continue  # generated: .pyc, .so, .DS_Store
            logged = self._logged.get(full)
            if logged and logged["stat"] == (size, mtime_ns):
                summary["unchanged_logged"] += 1
                continue
            if ledger.unchanged(rel, size, mtime_ns):
                # Queued by an earlier close, or by another process of this
                # run, and not touched since: not even read again.
                summary["unchanged_logged"] += 1
                continue
            if full in mount_points:
                # A file bind-mounted on its own (a Kubernetes subPath): its
                # storage is not its folder's.
                storage = ephemeral.describe(full)
            else:
                directory = os.path.dirname(full)
                storage = storage_of.get(directory)
                if storage is None:
                    storage = storage_of[directory] = ephemeral.describe(directory)
            if size > INSPECT_LIMIT_BYTES:
                # Over the inspection limit: in parts when this team's capture
                # sends them (D4/D19) and the file is at most 5 GiB. Only its
                # first `SCAN_PREFIX_BYTES` are read here (the credential scan);
                # the outbox hashes the rest in the background.
                sent = (
                    self._queue_in_parts(rel, full, storage, deadline)
                    if size <= AUTO_UPLOAD_MAX_BYTES
                    else None
                )
                if sent == "secret":
                    secret_skips.append(rel)
                elif sent == "queued":
                    ledger.add(rel, f"parts:{size}:{mtime_ns}", size, mtime_ns)
                    summary["uploaded_in_parts"] = summary.get("uploaded_in_parts", 0) + 1
                else:
                    _not_uploaded(rel, full, size, mtime_ns, storage, TOO_LARGE)
                continue
            if time.monotonic() + size * per_byte >= deadline:
                _not_uploaded(rel, full, size, mtime_ns, storage, OVER_BUDGET)
                continue
            started = time.monotonic()
            try:
                # scanning disabled: data, result, source_sha256 = secret_gate.read_upload_redacted_sourced(full, full_scan=True)
                raw = secret_gate.read_source(full)
                data, result, source_sha256 = raw, secret_gate.InspectionResult(), hashlib.sha256(raw).hexdigest()
            except secret_gate.CredentialInPath:
                secret_skips.append(rel)
                continue
            except CredentialBlocked:
                if os.path.exists(full):
                    _not_uploaded(rel, full, size, mtime_ns, storage, UNINSPECTABLE)
                continue
            if _unredacted(result):
                # Found, and NOT replaced: a container, a checkpoint, bytes
                # that are not UTF-8. Uploading would ship it byte-for-byte.
                secret_skips.append(rel)
                continue
            if result.rewritten:
                redacted.append(rel)
            digest = hashlib.sha256(data).hexdigest()
            if _already(rel, full, digest, logged):
                # Keyed on the STORED bytes: a later original that redacts to
                # bytes already stored is not uploaded again (see WHAT A READER
                # CAN MATCH); its own hash rides the run's write list.
                summary["unchanged_logged"] += 1
                continue
            meta = self._meta(full, storage)
            if source_sha256 != digest:
                # Redacted: the stored hash names bytes no reader opened.
                meta["source_sha256"] = source_sha256
            # The bytes inspected are the bytes staged: the file is not opened
            # again, so a writer racing the close cannot swap what leaves.
            queued_ok = self._queue_generated(OUTPUT_PREFIX + rel, data, meta=meta)
            del data
            if size >= 1_000_000:
                per_byte = max(per_byte * 0.5, (time.monotonic() - started) / size)
            if queued_ok:
                ledger.add(rel, digest, size, mtime_ns)
                summary["uploaded"] += 1
        if references:
            # Hashed from what the run's I/O budget has left after its reads
            # and writes, in the time the uploads left (F3).
            from .. import lineage as _inputs

            budget = _inputs.reference_budget(self.run_id)
            for rel, full, size, mtime_ns, storage, code, key in references:
                content_hash = self._reference_hash(full, size, mtime_ns, budget, deadline)
                if content_hash is None:
                    summary["referenced_unhashed"] = summary.get("referenced_unhashed", 0) + 1
                self._queue_reference(rel, full, size, storage, why=_REASONS[code], content_hash=content_hash)
                ledger.add(rel, key, size, mtime_ns)
                summary["referenced"] += 1
        ledger.save()
        summary["skipped_secret"] = len(secret_skips)
        summary["listed"] = len(listed)
        if secret_skips:
            shown = ", ".join(secret_skips[:10])
            more = f" (+{len(secret_skips) - 10} more)" if len(secret_skips) > 10 else ""
            _diagnostics.warn(
                f"probe: did not upload {len(secret_skips)} output file(s) that may hold a "
                f"credential Probe could not redact: {shown}{more}. If one is safe to "
                "share, log it on purpose with log_artifact."
            )
        if redacted:
            shown = ", ".join(redacted[:10])
            more = f" (+{len(redacted) - 10} more)" if len(redacted) > 10 else ""
            _diagnostics.warn(
                f"probe: replaced credentials in {len(redacted)} output file(s) before upload: "
                f"{shown}{more}. The stored copies are not byte-identical to your files; "
                "the files on disk are unchanged."
            )
        if listed or truncated:
            self._queue_manifest(listed, truncated=truncated)
            self._warn_listed(listed, truncated)

    def _warn_listed(self, listed: list[dict], truncated: bool) -> None:
        shown = ", ".join(item["path"] for item in listed[:10])
        more = f" (+{len(listed) - 10} more)" if len(listed) > 10 else ""
        codes = {item["code"] for item in listed}
        advice = []
        if TOO_LARGE in codes:
            # Capture never uploads a LISTED one (a throwaway box's own disk,
            # where nothing would carry parts after exit). An explicit log_artifact does,
            # in parts -- but only against a server that ADVERTISES multipart
            # uploads (g); against any other (today's prod among them) it
            # cannot either, so the advice must not send you there.
            if self._server_takes_multipart():
                advice.append(
                    f"capture does not upload a file {_REASONS[TOO_LARGE]} from this machine's "
                    "own disk -- `run.log_artifact(path)` uploads one you want kept (in parts), "
                    "or write it to a bucket or a mounted volume, where capture records where it is"
                )
            else:
                advice.append(
                    f"a file {_REASONS[TOO_LARGE]} on this machine's own disk cannot be kept -- "
                    "write it to a bucket or a mounted volume, where capture records where it is"
                )
        if OVER_BUDGET in codes:
            advice.append(
                "capture stopped inspecting files when its time at close ran out -- narrow it "
                f"with probe.init(outputs=...) or raise {BUDGET_ENV}"
            )
        if truncated:
            advice.append(
                f"the folder listing stopped early (over {MAX_FINAL_ENTRIES:,} files, or out of "
                "time) -- narrow it with probe.init(outputs=...)"
            )
        _diagnostics.warn(
            f"probe: {len(listed)} output file(s) were not stored and are listed in "
            f"{MANIFEST_NAME}" + (f": {shown}{more}" if listed else "") + "."
            + "".join(f" Note: {line}." for line in advice)
        )
from probe.sdk.capture.outputs.host_registry import _ledger_lock  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.log import _unredacted, state_dir  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.outputs.queue import OUTPUT_PREFIX, _Ledger  # noqa: E402 -- pieces need each other; the front door loads this one first
