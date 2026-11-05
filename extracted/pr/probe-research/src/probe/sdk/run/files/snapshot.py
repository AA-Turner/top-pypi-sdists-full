"""SnapshotMixin, Run's methods: run.snapshot: the content-addressed execution record of code,
dependencies and GPUs; at run open, the same capture with its network off the caller's thread."""

from __future__ import annotations
import os
import time
import warnings
from types import SimpleNamespace

from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ..launch import launch as _launch
from ...capture import code as _snapshot
from ....models import ExecutionRecordCreate
from probe.sdk.routes import WriteOp, path_for
#: The snapshot row's newline-joined path list is what /v1/search matches a
#: captured tree on; it also rides every list response that carries the row,
#: so it is bounded. 512 KB covers the largest tree seen so far (7,942 paths).
PATHS_TEXT_MAX_BYTES = 512 * 1024


class SnapshotMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def snapshot(
        self,
        *,
        cwd: str | None = None,
        include_env: bool = True,
        include_gpu: bool = True,
        venv: str | None = None,
        detect_venv: bool = False,
        upload: bool = True,
        max_upload_bytes: int = _snapshot.DEFAULT_MAX_UPLOAD_BYTES,
        include: list[str] | None = None,
        reference_over_bytes: int = _snapshot.DEFAULT_REFERENCE_OVER_BYTES,
        strict: bool | None = None,
        argv: list[str] | None = None,
    ) -> dict:
        """Capture code + deps + GPUs as a content-addressed execution record
        (fold #7), with git provenance (HEAD, branch, dirty -- read, never
        written) on the code-snapshot artifact. Non-disruptive.

        ``argv`` — the command this run executes, when a caller launches a
        child process; defaults to this process's argv.

        ``venv`` / ``detect_venv`` choose WHICH environment is recorded. The
        default records this interpreter's, which is correct here and only here:
        an in-process caller is running in the environment being snapshotted.
        A caller that launches the code as a subprocess -- the CLI, or any
        launcher script outside the training venv -- must pass ``detect_venv=True``
        (or an explicit ``venv``), otherwise it records its OWN packages with
        full confidence. See :func:`probe.sdk.capture.code.environment.capture_env`.

        The execution record pins ``run.env_ref`` to its content hash via RunPatch
        (fold #7 + the RunPatch env_ref parity), the same column the ingest path sets.

        Git is provenance, NOT the code record -- neither the retired shadow ref
        (it lived in the object database of whatever machine ran the job, so on an
        ephemeral box it stopped resolving the moment that box was destroyed) nor the pushed
        remote (a force-push, a deleted fork or a private repo an auditor cannot
        read all break it silently). So ``capture_manifest`` no longer classifies
        anything as retrievable-from-git: THE BYTES ARE THE RECORD.

        ``upload`` (default ON) STORES them. Every file classified
        ``source="blob"`` -- which is now every file that fits under
        ``reference_over_bytes`` -- is stored as its own ``kind='code'`` artifact
        row, content-addressed (presign in windows of ``CAPTURE_WINDOW``, the
        server's ``have`` answer dedupes unchanged files across runs and users);
        ``PROBE_CODE_STORAGE=archive`` tars them into a single deterministic
        ``code-bytes`` artifact instead. Without either the record holds a
        sha256, and a sha256 verifies a file you already have rather than
        producing one you do not: the run is identified and unreproducible.

        The one thing still recorded rather than copied is a file ABOVE
        ``reference_over_bytes`` -- a base checkpoint or a dataset shard, whose
        path, host and sha256 are recorded as a file-path reference. That is a
        deliberate size decision, not a bet on a remote still existing.

        Manifests of 200+ entries are ordinary; the per-file path batches them
        (one presign and one confirm per window, 16 PUTs in flight) so the cost
        is a few round-trips, not hundreds, and a sweep of N runs over unchanged
        code uploads each changed file once. The archive path keeps the older
        single-object shape for servers without the batch doors."""
        # The open's own snapshot queues first, so this one's env_ref and launch block are
        # the ones the run ends with (`run.execute()` records the child's this way).
        self._settle_open_snapshot()
        cap = self._capture_snapshot(
            cwd=cwd, include_env=include_env, include_gpu=include_gpu, venv=venv,
            detect_venv=detect_venv, upload=upload, max_upload_bytes=max_upload_bytes,
            include=include, reference_over_bytes=reference_over_bytes, strict=strict,
            probe_remote=True,
        )
        manifest = cap.manifest
        exec_rec = self._client.transport.post("/v1/execution-records", cap.body)
        content_hash = exec_rec.get("content_hash") if exec_rec else None

        # Store the bytes git cannot supply. Runs BEFORE the code-snapshot
        # artifact is written, so its meta records the real outcome rather than
        # a promise: `pending_upload` in that meta means those bytes are gone,
        # and it must never say 0 because an upload was merely attempted.
        code_bytes = self._upload_pending_code(
            manifest, cwd, upload=upload, max_upload_bytes=max_upload_bytes, strict=strict
        )

        launch_block = self._pin_env_ref(content_hash, argv=argv, cwd=cwd, strict=strict)
        self.log_artifact(
            "code-snapshot",
            **self._snapshot_row(cap, content_hash, code_bytes, launch_block),
            strict=strict,
        )
        return {
            "git": cap.git,
            "git_error": cap.git_error,
            "manifest": manifest,
            "code_bytes": code_bytes,
            "deps": cap.deps,
            "env_provenance": cap.env_provenance,
            "execution_record": exec_rec,
            "content_hash": content_hash,
            "launch": launch_block,
        }

    def _capture_snapshot(
        self,
        *,
        cwd: str | None,
        include_env: bool,
        include_gpu: bool,
        venv: str | None,
        detect_venv: bool,
        upload: bool,
        max_upload_bytes: int,
        include: list[str] | None,
        reference_over_bytes: int,
        strict: bool | None,
        probe_remote: bool,
    ) -> SimpleNamespace:
        """The local half of a snapshot: git provenance, manifest, environment, and the
        execution record's body. No network unless ``probe_remote`` (`ls-remote`)."""
        # Git is PROVENANCE, read-only, and never a gate (plan 2.6): no author
        # identity, an unborn HEAD, a read-only `.git` or no git binary used to
        # abort the whole capture (no code, deps or argv). Now the tree is
        # captured regardless -- as a plain directory when git cannot read it --
        # and why git failed rides in `meta.git_error`.
        # A fenced caller's command (D25): no git at all (it runs what the repository's config names,
        # outside the fence). The rest is recorded: the files, dependencies, launch, env_ref.
        is_fenced = is_caller_fenced()
        if is_fenced:
            git, git_error = None, FENCED_GIT_SKIPPED
        else:
            git, git_error = _snapshot.git_provenance(cwd or os.getcwd())
        manifest = _snapshot.capture_manifest(
            cwd,
            include=include,
            reference_over_bytes=reference_over_bytes,
            # Every file that could be uploaded is content-scanned and withheld
            # when it holds a credential (snapshot._ContentGate) -- whether or not
            # this capture uploads, so the tree's identity never depends on the
            # flag. Bounded by the upload cap only when uploading.
            scan=True,
            scan_budget_bytes=max_upload_bytes if upload else None,
            # `.probeignore` (plan (n)): excluded after the safety stops, and
            # never over an explicit `include=`.
            ignore=self._ignore_rules(cwd),
            probe_remote=probe_remote and not is_fenced,
            should_use_git=not is_fenced,
        )
        _warn_credential_skips(manifest)
        # Identity is hashed into the execution record; provenance is NOT --
        # a venv path in `deps` would make two identical environments at
        # different paths produce different env_refs. See split_env_provenance.
        deps, env_provenance = _snapshot.split_env_provenance(
            _snapshot.capture_env(
                cwd,
                venv=venv,
                detect_venv=detect_venv,
                strict=strict if strict is not None else not self._client.fail_open,
            )
            if include_env
            else {}
        )
        # Warn HERE rather than in the CLI's display code, because `probe exec`
        # reaches this same `detect_venv=True` path (see `execute`) and has no
        # display layer to carry the notice. Without this the exec path records
        # no environment and says nothing -- and absence that prints nothing is
        # how a run reaches the record looking captured. The `probe snapshot`
        # command prints its own fuller message, so that one path says it twice;
        # a duplicated warning is the cheap side of never losing it.
        if env_provenance.get("resolved_via") == _snapshot.UNRESOLVED_FALLBACK:
            warnings.warn(
                "environment NOT captured: no virtualenv could be attributed to "
                f"{os.path.abspath(cwd or os.getcwd())}, and the interpreter "
                f"({env_provenance.get('python_executable')}) is outside it. "
                "Recording its packages would describe the launcher, not the "
                "run. Pass venv=... (CLI: --venv PATH), or activate the "
                "environment the code runs in.",
                stacklevel=3,
            )
        lockfiles = sorted(
            (
                {"path": e["path"], "sha256": e["sha256"]}
                for e in manifest["entries"]
                if e.get("lockfile") and e.get("source") != "withheld"
            ),
            key=lambda item: item["path"],
        )
        if lockfiles:
            deps = {**deps, "lockfiles": lockfiles}
        record = ExecutionRecordCreate(
            # `git` is deliberately NOT hashed into the execution record (design
            # doc D1): the identity table names the code MANIFEST as identity.
            # Git is provenance, not identity -- HEAD, branch and dirty ride the
            # code-snapshot artifact's meta below.
            code={"manifest": manifest},
            deps=deps,
            hardware=(
                {"gpu": _snapshot.capture_gpu(), **_snapshot.capture_system()}
                if include_gpu
                else {}
            ),
        )
        return SimpleNamespace(
            git=git, git_error=git_error, manifest=manifest, deps=deps,
            env_provenance=env_provenance, lockfiles=lockfiles,
            body=record.model_dump(mode="json", exclude_none=True),
        )

    def _pin_env_ref(
        self, content_hash: str | None, *, argv: list[str] | None, cwd: str | None, strict: bool | None
    ) -> dict:
        """PATCH the run's env_ref (when known) and launch block; returns the launch block."""
        # Pin the real runs.env_ref column (FK to the execution record just
        # created). Launch ephemera ride the SAME patch as env_ref: one write, and
        # the metadata merge is client-side (read-modify-write) because RunPatch
        # REPLACES metadata. Single-writer per run is the operating assumption
        # (probe exec holds the run lock; SDK runs are process-bound).
        launch_block = _launch.build_launch_block(
            argv=argv,
            cwd=cwd,
            config=(self._data or {}).get("config"),
        )
        current_meta = dict((self._data or {}).get("metadata") or {})
        patch_body: dict = {"metadata": {**current_meta, "launch": launch_block}}
        if content_hash is not None:
            patch_body["env_ref"] = content_hash
            # Before the write, so no reader sees the PATCH queued and the pin
            # missing (the hardware rail's never-clobber check).
            self._pinned_env_ref = content_hash
        # Deliberately NOT sync. `finish()` orders its completeness check after
        # the drain precisely so this PATCH and the code-snapshot artifact are
        # observed together; forcing this one to land early would break that
        # ordering (tests/test_run_check_launch.py pins it) and put a round trip
        # on run open.
        #
        # The cost is that the env_ref persistence probe below -- which catches a
        # backend that accepts the field, ignores it and answers 200 -- only runs
        # when a row comes back. That is now SAID rather than silently skipped:
        # a guard nobody knows was skipped is worse than no guard.
        data = self._client.write("PATCH", path_for(WriteOp.RUN_PATCH, self.id), patch_body, strict=strict)
        if data is None and content_hash is not None:
            _diagnostics.warn(
                "probe: env_ref was queued, not confirmed — the backend-capability "
                "check is unavailable for this write. `probe run check` after the "
                "outbox drains verifies it."
            )
        if data:
            self._data = data
            if content_hash is not None and data.get("env_ref") != content_hash:
                message = (
                    "Probe Research API did not persist run.env_ref after snapshot "
                    f"(expected {content_hash}, got {data.get('env_ref')!r})"
                )
                if strict is True or (strict is None and not self._client.fail_open):
                    raise errors.CapabilityUnavailable("run.env_ref", message)
                warnings.warn(message, stacklevel=3)
        return launch_block

    def _snapshot_row(
        self,
        cap: SimpleNamespace,
        content_hash: str | None,
        code_bytes: dict,
        launch_block: dict,
        *,
        pushed: tuple[str | None, str | None] | None = None,
        code_uri: str | None = None,
    ) -> dict:
        """The code-snapshot row's `log_artifact` arguments. ``pushed`` (run open) is the
        thread's `(base_commit, remote)`, which the open's manifest leaves out; ``code_uri``
        (run open) pins the row's uri, so its later rewrite updates the same row."""
        git, git_error, manifest = cap.git, cap.git_error, cap.manifest
        lockfiles, env_provenance = cap.lockfiles, cap.env_provenance
        base_commit, remote = pushed if pushed is not None else (
            manifest["base_commit"], manifest["remote"]
        )
        # The code-snapshot row points at what was STORED, git repo or not: the
        # `git:refs/probe/snapshots/...` uri named a shadow commit that is no
        # longer written (plan 2.6). The manifest travels with it so a reader can
        # tell, without fetching anything, which files the capture holds.
        # `check_run` requires a code_snapshot row to exist at all.
        if code_uri is not None:
            pass  # run open: one uri across the row's rewrite, so the server updates it in place
        elif code_bytes.get("storage") == CODE_STORAGE_ARTIFACTS and content_hash:
            # Per-file storage has no single archive to point at; the execution
            # record (keyed by env_ref) IS the record of what was captured, and
            # its rows sit on this run.
            code_uri = f"probe-manifest:{content_hash}"
        elif code_bytes.get("artifact_id"):
            code_uri = f"probe-artifact:{code_bytes.get('artifact_id')}"
        elif content_hash:
            # Nothing stored (upload off or failed; `n_pending_upload` says so),
            # but the manifest still identifies the tree -- and a reference row
            # must name something (the server 422s one that names nothing).
            code_uri = f"probe-manifest:{content_hash}"
        paths_text = "\n".join(
            sorted(e["path"] for e in (manifest.get("entries") or []) if e.get("path"))
        )
        paths_truncated = False
        if len(paths_text.encode("utf-8")) > PATHS_TEXT_MAX_BYTES:
            cut = paths_text.encode("utf-8")[:PATHS_TEXT_MAX_BYTES].decode("utf-8", "ignore")
            paths_text = cut.rsplit("\n", 1)[0]
            paths_truncated = True
        if code_uri is None:
            # A reference row must name something (the server 422s one that names
            # nothing); with no record and no stored archive, the tree's own digest.
            code_uri = f"probe-tree:{manifest['tree_sha256']}"
        return dict(
            uri=code_uri,
            kind="code_snapshot",
            is_reference=True,
            allow_missing=True,
            meta={
                "vcs": "git" if git else None,
                "branch": git.get("branch") if git else None,
                "dirty": git.get("dirty") if git else None,
                # The commit the tree sat on (None on an unborn branch). The uri
                # used to carry a shadow commit; this is the real one.
                "head": git.get("head") if git else None,
                **({"git_error": git_error} if git_error else {}),
                "skipped": manifest.get("skipped") or None,
                # `skipped` lists at most PROBEIGNORE_REPORT_LIMIT of these.
                **({"n_probeignore": manifest["n_probeignore"]} if manifest.get("n_probeignore") else {}),
                "env_ref": content_hash,
                "tree_sha256": manifest["tree_sha256"],
                "base_commit": base_commit,
                "remote": remote,
                "n_git_referenced": manifest["n_git_referenced"],
                # What SURVIVES, not what was classified. `check_run` gates
                # `pending_code_bytes` on this, so it must mean "these bytes are
                # gone" -- never "an upload was attempted". `n_classified_pending`
                # keeps the pre-upload count for diagnostics.
                "n_pending_upload": code_bytes["pending_upload"],
                "n_classified_pending": manifest["n_pending_upload"],
                "n_referenced_offsite": manifest.get("n_referenced_offsite", 0),
                # Files left out whole because their content holds a credential
                # (`source: "withheld"` in the manifest; the paths are in `skipped`).
                "n_withheld": manifest.get("n_withheld", 0),
                # Which storage the captured bytes live in (0193): "artifacts"
                # means one code row per file on this run; "archive" means the
                # code-bytes tarball. A label for readers and search; restore
                # does NOT branch on it -- it looks for complete capture rows
                # on the run and falls back to the archive.
                "storage": code_bytes.get("storage", CODE_STORAGE_ARCHIVE),
                # Every path this run ran with, newline-joined, so /v1/search
                # can answer "which run captured results.jsonl" from THIS row
                # instead of from thousands of per-file rows. Bounded (see
                # PATHS_TEXT_MAX_BYTES); a cut list says so.
                "paths_text": paths_text,
                **({"paths_text_truncated": True} if paths_truncated else {}),
                "code_bytes": code_bytes,
                # WHICH environment the deps came from. Deliberately here and
                # not in the hashed execution record (split_env_provenance).
                **({"env": env_provenance} if env_provenance else {}),
                "n_lockfiles": len(lockfiles),
                **({"launch_errors": launch_block["errors"]} if launch_block.get("errors") else {}),
            },
        )

    def _snapshot_at_open(self) -> None:
        """The snapshot `client.run()` / `probe.init()` takes: no network on this thread.

        Only under async writes with fail-open (the default): a sync-write or strict client
        asked for its writes in hand, so it keeps `snapshot()`. Everything local happens HERE
        and is queued before this returns, so a process killed a moment later still has it on
        disk: the launch PATCH, the code-bytes archive (built and staged now, the open-time
        bytes) and the code-snapshot row. The execution record (its hash is the server's) is
        POSTed by `PendingSnapshot`'s thread, with the pushed base in it; its answer queues
        the env_ref PATCH and the row again with its env_ref and pushed base (same uri, so
        the server updates the row). Any close, terminal status or explicit `snapshot()`
        settles it first (`_settle_open_snapshot`).
        """
        client = self._client
        if is_caller_fenced() or not getattr(client, "async_writes", False) or not client.fail_open:
            # (A fenced caller's: the synchronous snapshot, which runs no git; the open's
            # thread would ask the remote with git.)
            self.snapshot()
            return
        cap = self._capture_snapshot(
            cwd=None, include_env=True, include_gpu=True, venv=None, detect_venv=False,
            upload=True, max_upload_bytes=_snapshot.DEFAULT_MAX_UPLOAD_BYTES, include=None,
            reference_over_bytes=_snapshot.DEFAULT_REFERENCE_OVER_BYTES, strict=None,
            probe_remote=False,
        )
        code_bytes, archive, archive_meta = self._archive_pending_code(
            cap.manifest, None, max_upload_bytes=_snapshot.DEFAULT_MAX_UPLOAD_BYTES
        )
        try:
            launch_block = self._pin_env_ref(None, argv=None, cwd=None, strict=None)
            code_uri = f"probe-tree:{cap.manifest['tree_sha256']}"
            opened_row = self._snapshot_row(
                cap, None, code_bytes, launch_block, pushed=(None, None), code_uri=code_uri
            )
            # The row before the archive: the archive rides its own lane, but an older drainer
            # puts it on the run's, where a storage outage holding its upload must not hold the
            # row too.
            self.log_artifact("code-snapshot", **opened_row)
            if archive is not None:
                staged = self._stage_open_archive(archive, archive_meta, code_bytes)
                archive = None  # `_stage_open_archive` owns (and deleted) the file
                if staged is not code_bytes:  # not stored: the row says so (same uri: updated)
                    code_bytes = staged
                    opened_row = self._snapshot_row(
                        cap, None, code_bytes, launch_block, pushed=(None, None),
                        code_uri=code_uri,
                    )
                    self.log_artifact("code-snapshot", **opened_row)
        finally:
            if archive is not None:  # an interrupt before the handoff: no temp archive left
                try:
                    os.unlink(archive)
                except OSError:
                    pass

        def pin(content_hash: str | None) -> str | None:
            if content_hash is None:
                return None
            # Before the write, so no reader sees the PATCH queued and the pin missing.
            self._pinned_env_ref = content_hash
            if self._client.write("PATCH", path_for(WriteOp.RUN_PATCH, self.id), {"env_ref": content_hash}):
                return None
            return (
                "probe: env_ref was queued, not confirmed — the backend-capability check is "
                "unavailable for this write. `probe run check` after the outbox drains "
                "verifies it."
            )

        def rewrite_row(content_hash: str | None, base: str | None, remote: str | None) -> None:
            row = self._snapshot_row(
                cap, content_hash, code_bytes, launch_block, pushed=(base, remote),
                code_uri=code_uri,
            )
            if row != opened_row:
                self.log_artifact("code-snapshot", **row)

        pending = PendingSnapshot(
            client, cap.body, pin=pin, rewrite_row=rewrite_row,
            should_wait_for_pushed=bool(cap.git),
        )
        if cap.git:
            try:
                _snapshot.start_pushed_base(os.getcwd(), pending.answer_pushed)
            except RuntimeError:
                # No thread for `ls-remote` (a thread limit): the record goes without a pushed
                # base rather than not at all (final review of #3792).
                pending.answer_pushed(None, None)
        pending.start()
        self._pending_snapshot = pending

    def _settle_open_snapshot(self, wait_until: float | None = None) -> None:
        """Before a terminal status or another snapshot: wait for the open's execution record
        (at most until its own deadline, ``wait_until`` and this thread's `deadline_scope`),
        then queue what it has not queued, here. After this, nothing of the open's snapshot
        can be queued (`PendingSnapshot.settle`)."""
        pending = getattr(self, "_pending_snapshot", None)
        if pending is None:
            return
        from ...delivery.transport.deadlines import deadline_remaining

        scope_end = time.monotonic() + deadline_remaining(float("inf"))
        pending.settle(scope_end if wait_until is None else min(wait_until, scope_end))

    def _wait_for_open_record(self) -> bool:
        """Until the open's execution record is pinned or given up (bounded by its deadline):
        `env_ref` read before that would miss the pin still in flight. False once the open's
        snapshot is settled (a close, a terminal status or another snapshot took over): no
        other writer may pin env_ref after that."""
        pending = getattr(self, "_pending_snapshot", None)
        if pending is None:
            return True
        pending.wait_for_record()
        return not pending.is_settled


from probe.sdk.run.files.snapshot_queue import PendingSnapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.files.code_upload import CODE_STORAGE_ARCHIVE, CODE_STORAGE_ARTIFACTS, _warn_credential_skips  # noqa: E402 -- pieces need each other; the front door loads this one first


#: The code snapshot's `git_error` for a fenced caller's run: git was not run, on purpose.
FENCED_GIT_SKIPPED = "skipped: fenced"


def is_caller_fenced() -> bool:
    """Does this command run for a fenced caller (`env.CALLER_FENCED_ENV`, set by the service)?"""
    from ....foundation.service_api.env import CALLER_FENCED_ENV

    return os.environ.get(CALLER_FENCED_ENV) == "1"
