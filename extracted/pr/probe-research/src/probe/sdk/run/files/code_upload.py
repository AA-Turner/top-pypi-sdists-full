"""CodeUploadMixin, Run's methods: store the code files git cannot supply as one archive, within
the capture deadline, and say what was left out."""

from __future__ import annotations

import contextvars
import os
import re
import tempfile

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...capture import code as _snapshot


#: How a snapshot stores the files git cannot supply. ``archive`` is one
#: deterministic tar.gz per run (the original design); ``artifacts`` is one
#: ``kind='code'`` artifact row per file, content-addressed so an unchanged
#: file across runs is stored once and every captured file is visible in the
#: run's artifact explorer. ``artifacts`` is the default since the CLI release
#: after 0.140.0 (the server's batch doors landed in 0.352.0.0);
#: ``PROBE_CODE_STORAGE=archive`` keeps the one-tarball-per-run behaviour.
CODE_STORAGE_ENV = "PROBE_CODE_STORAGE"
CODE_STORAGE_ARCHIVE = "archive"
CODE_STORAGE_ARTIFACTS = "artifacts"
DEFAULT_CODE_STORAGE = CODE_STORAGE_ARTIFACTS
#: The whole per-file capture gets this long, presign to last confirm. A tree of
#: thousands of files on a flaky network must not park `run.snapshot()` (which
#: runs before the training loop) for hours: past the deadline the remaining
#: files are named as unstored and the run goes on (under ``strict=True`` the
#: deadline raises, like any other storage failure). `PROBE_CODE_CAPTURE_DEADLINE`
#: (seconds) overrides it.
CAPTURE_DEADLINE_SECONDS = 600.0
_SIGNED_QUERY = re.compile(r"\?[^\s'\"]*")


def _code_storage() -> str:
    raw = (os.environ.get(CODE_STORAGE_ENV) or "").strip().lower()
    if raw in (CODE_STORAGE_ARCHIVE, CODE_STORAGE_ARTIFACTS):
        return raw
    if raw:
        _diagnostics.warn(
            f"{CODE_STORAGE_ENV}={raw!r} is not one of "
            f"{CODE_STORAGE_ARCHIVE!r}/{CODE_STORAGE_ARTIFACTS!r}; using {DEFAULT_CODE_STORAGE!r} "
            "(to store no code at all, pass upload=False / --no-upload)",
            stacklevel=2,
        )
    return DEFAULT_CODE_STORAGE


def _capture_deadline() -> float:
    raw = (os.environ.get("PROBE_CODE_CAPTURE_DEADLINE") or "").strip()
    try:
        return float(raw) if raw else float(CAPTURE_DEADLINE_SECONDS)
    except ValueError:
        return float(CAPTURE_DEADLINE_SECONDS)


def _redact_signed(message: str) -> str:
    """A presigned URL's query string IS its credential (an hour of access to
    that object); an error message that quotes one must not reach a warning, a
    transcript or the run's metadata."""
    return _SIGNED_QUERY.sub("?<signed>", message)


def _warn_credential_skips(manifest: dict) -> None:
    """Say, once, what code capture left out that the person would not expect:
    a file WITHHELD because its content looks like a credential, and any TRACKED
    file stopped by name or content (a committed file missing from a capture
    breaks its restore). An untracked `.env` skipped by name is expected and
    stays in the record only. Rule names only, never a value."""
    skipped = [s for s in manifest.get("skipped") or [] if isinstance(s, dict)]
    hits = [s for s in skipped if s.get("found_in") == "content"]
    slow = [s for s in skipped if s.get("found_in") == "scan_time"]
    tracked = [s for s in skipped if s.get("tracked") and s.get("found_in") not in ("content", "scan_time")]
    if not hits and not tracked and not slow:
        return

    def _names(items: list) -> str:
        shown = ", ".join(str(s.get("path")) for s in items[:10])
        return shown + (f" (+{len(items) - 10} more)" if len(items) > 10 else "")

    parts = []
    if hits:
        rules = sorted({str(r) for s in hits for r in s.get("rules") or ()})
        marked = [dict(s, path=f"{s.get('path')} (tracked)") if s.get("tracked") else s for s in hits]
        parts.append(
            f"withheld {len(hits)} file(s) whose contents look like a credential "
            f"({', '.join(rules)}): {_names(marked)}. A snapshot stores exact bytes and "
            "never redacts, so these were not uploaded; move the key to an environment "
            "variable or a gitignored file to capture the rest of the file"
        )
    if tracked:
        parts.append(
            f"left out {len(tracked)} tracked file(s) whose NAME marks a credential: "
            f"{_names(tracked)}; restoring this run will not rebuild them"
        )
    if slow:
        parts.append(
            f"withheld {len(slow)} file(s) whose credential scan could not finish in "
            f"time: {_names(slow)}. Unscanned bytes are never uploaded; raise "
            f"{_snapshot.FILE_SCAN_BUDGET_ENV} / {_snapshot.SNAPSHOT_SCAN_BUDGET_ENV} "
            "(seconds, 0 = no limit) to scan them"
        )
    _diagnostics.warn(
        "probe: code capture " + "; and ".join(parts) + ". All are listed as skipped "
        "(reason 'secret' or 'scan_budget') on the run's code snapshot.",
        stacklevel=3,
    )

#: Set by a caller that reports a failed upload in its OWN words (the
#: code-bytes archive), so `Run._warn_not_uploaded` stays quiet for that call
#: instead of telling the user to pass `strict=True` to a `log_artifact` they
#: never made. A ContextVar, not an attribute: a sampler thread logging its own
#: artifacts at the same moment must still hear about its failures.
_OWN_UPLOAD_WARNING: contextvars.ContextVar[bool] = contextvars.ContextVar(
    "probe_own_upload_warning", default=False
)


class CodeUploadMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- snapshot (execution record) ----------------------------------------
    def _upload_pending_code(
        self,
        manifest: dict,
        cwd: str | None,
        *,
        upload: bool,
        max_upload_bytes: int,
        strict: bool | None,
    ) -> dict:
        """Store the files git cannot supply. Returns what to record in meta.

        The returned ``pending_upload`` is the count that SURVIVES this call, so
        a reader can trust it: it is 0 only when the bytes are actually stored.
        `Client.check_run` gates `pending_code_bytes` on it.
        """
        pending = _snapshot.pending_entries(manifest)
        # Stamped before the branch: a run with nothing to store, or one that
        # opted out of uploads, is still recorded under the storage it would
        # have used, not under the archive by default.
        if not pending:
            return {
                "uploaded": False,
                "pending_upload": 0,
                "reason": "nothing pending",
                "storage": _code_storage(),
            }
        if not upload:
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "upload disabled",
                "storage": _code_storage(),
            }

        root = os.path.abspath(cwd or os.getcwd())
        if _code_storage() == CODE_STORAGE_ARTIFACTS:
            result = self._upload_pending_files(
                root, pending, strict=strict, max_upload_bytes=max_upload_bytes
            )
            if result.get("fallback") != CODE_STORAGE_ARCHIVE:
                return result
            # A server that predates the batch doors (404/405 on the first
            # presign) still takes the archive; a lagging deploy must not turn
            # every run into an unreproducible one.
            _diagnostics.warn(
                "this server has no per-file capture doors yet; storing the "
                "code-bytes archive instead",
                stacklevel=3,
            )
        tmp = tempfile.NamedTemporaryFile(prefix="probe-code-", suffix=".tar.gz", delete=False)
        tmp.close()
        try:
            summary = _snapshot.build_pending_archive(
                root, manifest, tmp.name, max_bytes=max_upload_bytes
            )
            drifted = list(summary["missing"]) + list(summary["changed"])
            drift_meta = {"drifted": drifted[: _snapshot.DRIFTED_META_LIMIT]} if drifted else {}
            drift_warning = (
                f"code capture stored {summary['n_files']} of {len(pending)} files; "
                f"{summary['drift_message']}"
            )
            if summary["n_files"] == 0:
                # Every pending file moved between manifest and archive; an
                # empty archive would claim a capture that did not happen.
                _diagnostics.warn(drift_warning, stacklevel=3)
                return {
                    "uploaded": False,
                    "pending_upload": len(pending),
                    "reason": "tree drifted during capture",
                    **drift_meta,
                }
            drifted_set = set(drifted)
            # This method says what happened to the archive, once, below: the
            # generic "pass strict=True" line would name a call the user never
            # made, on top of that.
            own_warning = _OWN_UPLOAD_WARNING.set(True)
            try:
                rec = self.log_artifact(
                    _snapshot.CODE_BYTES_ARTIFACT,
                    # sync=True: the `finally` below unlinks this tmp archive, so a
                    # queued op would reference a file guaranteed to be gone by the
                    # time the drainer read it -- a dead letter with 100% hit rate.
                    sync=True,
                    path=tmp.name,
                    kind="code_bytes",
                    content_type="application/gzip",
                    meta={
                        "n_files": summary["n_files"],
                        "uncompressed_bytes": summary["uncompressed_bytes"],
                        "tree_sha256": manifest.get("tree_sha256"),
                        # Only the members whose bytes VERIFIED against the manifest.
                        # A path listed here that the archive does not hold is the
                        # lie this whole path removes.
                        "paths": [e["path"] for e in pending if e["path"] not in drifted_set],
                        **drift_meta,
                    },
                    strict=strict,
                )
            finally:
                _OWN_UPLOAD_WARNING.reset(own_warning)
        except _snapshot.SnapshotTooLarge:
            raise
        except errors.RosError as exc:
            # Fail-open like every other write: the training run continues, but
            # the count stays non-zero so nothing reads this as captured. Drift
            # never raises (it is recorded, below); what does is a malformed
            # manifest entry, a file that shrank or changed under the stream,
            # or an upload error -- and the cause rides in the warning.
            if strict is True or (strict is None and not self._client.fail_open):
                raise
            _diagnostics.warn(
                f"code-bytes upload failed ({exc}); {len(pending)} files remain unstored "
                "and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {"uploaded": False, "pending_upload": len(pending), "reason": "upload failed"}
        finally:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass

        if drifted:
            _diagnostics.warn(drift_warning, stacklevel=3)
        # A fail-open spooled write returns None -- unverifiable until flush, so
        # it cannot be claimed as stored.
        if not rec:
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "spooled",
                **drift_meta,
            }
        # A storage failure under fail-open makes `log_artifact` record a
        # REFERENCE to the tmp archive (a pointer the `finally` above deletes).
        # That is not stored bytes: it used to read as a complete capture with
        # `n_pending_upload` 0, the same lie as the short archive.
        if rec.get("is_reference") or (rec.get("meta") or {}).get("upload") == "failed":
            # The gate's own reason when it was the gate (an archive over the
            # inspection limit never reached storage at all).
            refusal = (rec.get("meta") or {}).get("upload_error")
            cause = (
                f"refused by the credential gate: {_gate_reason(refusal)}"
                if refusal
                else "storage refused the archive"
            )
            _diagnostics.warn(
                f"code-bytes upload failed ({cause}); {len(pending)} "
                "files remain unstored and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "upload failed",
                **drift_meta,
            }
        return {
            "uploaded": True,
            # The files whose bytes did NOT land: drifted ones are unstored
            # exactly like a failed upload, and named so a reader knows which.
            "pending_upload": len(drifted),
            "artifact_id": rec.get("id"),
            "archive_sha256": summary["sha256"],
            "size_bytes": summary["size_bytes"],
            "n_files": summary["n_files"],
            **drift_meta,
        }
    def _archive_pending_code(
        self, manifest: dict, cwd: str | None, *, max_upload_bytes: int
    ) -> tuple[dict, str | None, dict | None]:
        """Run open's code bytes: one deterministic archive, built now.

        Per-file capture needs the batch presign/confirm doors, which no queued op kind can
        drive, so the open stores the `code-bytes` archive. Its code-snapshot row names it by
        ``code_bytes.archive_sha256`` (the archive's id is the server's, minted when the queued
        upload lands); readers match the run's `code_bytes` row on that hash. The archive pass
        re-hashes every member against the manifest as it streams, so its bytes are the
        open-time bytes whatever happens to the files later. Returns ``(code_bytes meta,
        archive path, its row meta)``; the caller hands the archive to `_stage_open_archive`,
        which owns the file from then on. A build that fails (other than over the size cap) is
        a capture gap and one warning, as the upload path's is: the run still opens.
        """
        pending = _snapshot.pending_entries(manifest)
        if not pending:
            return {
                "uploaded": False,
                "pending_upload": 0,
                "reason": "nothing pending",
                "storage": CODE_STORAGE_ARCHIVE,
            }, None, None
        root = os.path.abspath(cwd or os.getcwd())
        tmp = tempfile.NamedTemporaryFile(prefix="probe-code-", suffix=".tar.gz", delete=False)
        tmp.close()
        try:
            summary = _snapshot.build_pending_archive(
                root, manifest, tmp.name, max_bytes=max_upload_bytes
            )
        except _snapshot.SnapshotTooLarge:
            _unlink_quietly(tmp.name)
            raise
        except (errors.RosError, OSError) as exc:
            # A file that shrank or changed under the stream twice, a malformed entry, a full
            # temp disk: the bytes are not stored, the run opens anyway, and the count says so.
            _unlink_quietly(tmp.name)
            _diagnostics.warn(
                f"code-bytes archive not built ({exc}); {len(pending)} files remain unstored "
                "and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "archive failed",
                "storage": CODE_STORAGE_ARCHIVE,
            }, None, None
        except BaseException:
            _unlink_quietly(tmp.name)
            raise
        drifted = list(summary["missing"]) + list(summary["changed"])
        drift_meta = {"drifted": drifted[: _snapshot.DRIFTED_META_LIMIT]} if drifted else {}
        if drifted or summary["n_files"] == 0:
            _diagnostics.warn(
                f"code capture stored {summary['n_files']} of {len(pending)} files; "
                f"{summary['drift_message']}",
                stacklevel=3,
            )
        if summary["n_files"] == 0:
            _unlink_quietly(tmp.name)
            return {
                "uploaded": False,
                "pending_upload": len(pending),
                "reason": "tree drifted during capture",
                "storage": CODE_STORAGE_ARCHIVE,
                **drift_meta,
            }, None, None
        drifted_set = set(drifted)
        meta = {
            "n_files": summary["n_files"],
            "uncompressed_bytes": summary["uncompressed_bytes"],
            "tree_sha256": manifest.get("tree_sha256"),
            "paths": [e["path"] for e in pending if e["path"] not in drifted_set],
            **drift_meta,
        }
        return {
            "uploaded": False,
            "queued": True,
            "pending_upload": len(drifted),
            "storage": CODE_STORAGE_ARCHIVE,
            "archive_sha256": summary["sha256"],
            "size_bytes": summary["size_bytes"],
            "n_files": summary["n_files"],
            **drift_meta,
        }, tmp.name, meta

    def _stage_open_archive(self, path: str, meta: dict, code_bytes: dict) -> dict:
        """Queue the open's archive as a NON-blocking upload with its bytes copied into the
        outbox now, then delete the temp file; returns the code_bytes meta to record.

        Never an upload from the caller's thread: an archive the outbox has no room to stage
        is not stored (one warning; the row says so), and one over the inspection limit is
        staged in parts for the outbox when a features answer already in hand says the server
        takes multipart uploads, else not stored (the open asks the server nothing).
        Non-blocking: a storage outage never holds the run's close; `finish()` still drains
        it, after the run's own writes."""
        from ...artifact.filetype import kind_to_send, name_with_extension
        from ...artifact.storage_handlers import multipart as _multipart
        from ...delivery.journal.headroom import INLINE_HASH_MAX_BYTES

        try:
            size_bytes = os.path.getsize(path)
            name = name_with_extension(_snapshot.CODE_BYTES_ARTIFACT, path)
            try:
                queued = self._client.journal.append_upload(
                    anchor="run",
                    anchor_id=self.id,
                    name=name,
                    src_path=path,
                    inline_hash=size_bytes <= INLINE_HASH_MAX_BYTES,
                    content_type="application/gzip",
                    kind=kind_to_send("code_bytes"),
                    meta=meta,
                    run_ref=self.id,
                    require_staged=True,
                    blocking=False,
                    # Its own lane: the record's PATCH and row rewrite queue after it, and a
                    # storage outage parking it must not hold them (final review of #3792).
                    lane=f"code-bytes:{self.id}",
                )
            except Exception:  # noqa: BLE001 -- over the inspection limit, or no journal
                queued = {}
            if queued.get("staged"):
                self._client._after_enqueue()
                return code_bytes
            why = queued.get("unstaged_reason") or "the outbox could not take it"
            if _multipart.over_threshold(path):
                # Only a verdict in hand: asking `/v1/server/features` here would put a network
                # wait back on the open's thread (final review of #3792).
                known = getattr(self._client, "_server_features_cache", None)
                if known is None:
                    why = "over the inspection limit; multipart uploads not yet known at open"
                elif _multipart.FEATURE not in known:
                    why = "over the inspection limit, and no multipart door"
                else:
                    refusals: list[str] = []
                    handled = self._maybe_multipart(
                        name, path, kind="code_bytes", content_type="application/gzip",
                        span_id=None, step_index=None, meta=meta, strict=False, sync=False,
                        refused=refusals.append,
                    )
                    if handled is None and not refusals:
                        return code_bytes  # staged in parts, queued
                    why = refusals[0] if refusals else "over the inspection limit, and no multipart door"
            _diagnostics.warn(
                f"code-bytes archive not stored ({why}); {meta.get('n_files')} files remain "
                "unstored and this run is not reproducible from the record alone.",
                stacklevel=3,
            )
            return {
                **{k: v for k, v in code_bytes.items() if k != "queued"},
                "pending_upload": int(meta.get("n_files") or 0)
                + int(code_bytes.get("pending_upload") or 0),
                "reason": "archive not stored",
            }
        finally:
            _unlink_quietly(path)

def _unlink_quietly(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass


from probe.sdk.run.files.files import _gate_reason  # noqa: E402 -- pieces need each other; the front door loads this one first
