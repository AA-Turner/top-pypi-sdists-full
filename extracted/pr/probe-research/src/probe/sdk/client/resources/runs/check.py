"""RunCheckMixin, Client's methods: check_run: assess a run's capture completeness (twin:
app/runs)."""

from __future__ import annotations
from ....artifact.kinds import KIND_LABEL_KEY


class RunCheckMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def check_run(self, run_id: str, *, verify: bool = False) -> dict:
        """Assess capture completeness from the bounded run bundle.

        Three verdicts, and the distinction is the point:

        * ``incomplete`` -- something is absent or provably unrecoverable.
        * ``unverified`` -- nothing is obviously absent. The default. It does NOT
          mean the run can be rebuilt.
        * ``complete`` -- earned only under ``verify=True``, either because the
          code record is self-contained (``n_git_referenced == 0``: every byte is
          on Probe, so there is nothing to resolve) or by resolving a legacy git
          reference against its remote.

        This used to answer ``complete`` for the first case's near-miss: a run
        whose code_snapshot artifact existed and pointed at a commit that lived
        nowhere. Seventeen runs read as captured for a week on the strength of a
        row being present. Counting rows is not the same as proving retrieval, so
        the cheap path no longer claims a word it has not earned.

        Runs captured since git referencing was retired cannot land in that hole
        at all -- their bytes are stored, not pointed at -- so ``verify`` on them
        costs nothing and never reports ``unresolvable_code_reference``. The
        network probe remains for the runs captured while it was live: one
        depth-1 fetch per DISTINCT (remote, commit), memoized, so auditing a
        project's runs is a few calls rather than one per run. Never called
        during a run: it cannot slow training or upload.

        ``advisories`` reports gaps that are surfaced but never flip the verdict:
        judgment calls a human makes on purpose (no ``notes``, no recorded
        ``inputs_decision``) and legacy gaps (a run captured before capture-core
        has no ``launch`` block at all; a launch block that recorded its own
        capture errors). ``missing`` remains the only input to ``state`` -- a
        launch block that EXISTS but is missing a slot (process/runtime/
        determinism) is a genuine capture failure and lands in ``missing``, not
        ``advisories``.
        """
        bundle = self.run_bundle(run_id)
        run = bundle.get("run", bundle)
        artifacts = bundle.get("artifacts", [])
        metadata = run.get("metadata") or {}
        missing: list[str] = []
        # env_ref (execution record) is the launch-capture signal (fold #7). On the
        # ingest path it is run.env_ref; on the interactive path it is metadata.env_ref.
        if not (run.get("env_ref") or metadata.get("env_ref")):
            missing.append("execution_record")
        # The bundle holds the newest `BUNDLE_ARTIFACT_LIMIT` artifacts: the open's code rows are a
        # run's oldest, so past a cut bundle they are asked for by kind (final review of #3792).
        is_cut = isinstance(bundle.get("artifact_total"), int) and bundle["artifact_total"] > len(artifacts)
        snapshot_rows: list[dict] | None = [item for item in artifacts if item.get("kind") == "code_snapshot"]
        if not snapshot_rows and is_cut:
            snapshot_rows = self._list_kind(run_id, "code_snapshot")  # None: the read failed
        # A read that failed proves nothing either way: never missing, never verified complete.
        is_unread = snapshot_rows is None
        if snapshot_rows == []:
            missing.append("code_snapshot_artifact")  # absent, not merely unread
        failed_uploads = _failed_uploads(artifacts)
        if verify and is_cut:
            # `complete` must see every failed upload, not only the bundle's newest
            # (convergence review of #3804): the whole inventory, or the verdict stays open.
            inventory = self._list_kind(run_id, None)
            if inventory is None:
                is_unread = True
            else:
                failed_uploads = _failed_uploads(inventory)
        if failed_uploads:
            missing.append("portable_artifact_bytes")

        # Free (the manifest summary rides on the meta): bytes nobody stored are as lost as a dead reference.
        snapshot_meta: dict = next(((item.get("meta") or {}) for item in snapshot_rows or []), {})
        pending = snapshot_meta.get("n_pending_upload")
        if isinstance(pending, int) and pending > 0:
            missing.append("pending_code_bytes")
        elif _is_archive_still_queued(snapshot_meta, artifacts):
            # Run open queues its code-bytes archive (non-blocking): until that upload lands as
            # a `code_bytes` row the bytes exist only in one machine's outbox.
            landed_rows = self._list_kind(run_id, "code_bytes") if is_cut else artifacts
            if landed_rows is None:
                is_unread = True
            elif _is_archive_still_queued(snapshot_meta, landed_rows):
                missing.append("pending_code_bytes")

        advisories: list[str] = []
        launch = metadata.get("launch") or {}
        if not launch:
            # Pre-capture-core run: an advisory, not a verdict flip (else every old run reads incomplete).
            advisories.append("launch_context")
        else:
            for slot in ("process", "runtime", "determinism"):
                if not launch.get(slot):
                    missing.append(f"launch_{slot}")
            if launch.get("errors"):
                advisories.append("launch_errors")
        n_lockfiles = snapshot_meta.get("n_lockfiles")
        if isinstance(n_lockfiles, int) and n_lockfiles == 0:
            advisories.append("no_lockfiles")
        if not any(a.get("kind") == "inputs_decision" for a in artifacts):
            advisories.append("inputs_decision")
        # A note FILE is stored as `other` with `meta.kind_label`; an unbackfilled row still says `note`.
        if not run.get("notes") and not any(
            a.get("kind") == "note" or (a.get("meta") or {}).get(KIND_LABEL_KEY) == "note"
            for a in artifacts
        ):
            advisories.append("notes")

        verified = None
        if verify and not missing:
            from ....capture import code as _snapshot

            base_commit = snapshot_meta.get("base_commit")
            remote = snapshot_meta.get("remote")
            n_git_referenced = snapshot_meta.get("n_git_referenced")
            # Typed and PRESENT, never defaulted: an absent key is a pre-0.26.3 run, unknown, never zero. An
            # OFFSITE (size) reference does not disqualify a run: it is part of a complete capture (DESIGN.md).
            self_contained = (
                isinstance(n_git_referenced, int)
                and not isinstance(n_git_referenced, bool)
                and n_git_referenced == 0
            )
            if self_contained:
                # Self-contained manifest: complete WITHOUT a network probe; a stale `base_commit` must not fail it.
                verified = True
            elif base_commit and remote:
                # Captured while git referencing was live: only the probe tells a live reference from a dead one.
                verified = _snapshot.commit_on_remote(str(remote), str(base_commit))
                if not verified:
                    missing.append("unresolvable_code_reference")
            else:
                # Pre-0.26.3: no manifest to resolve against; say so rather than invent a pass or a failure.
                verified = False

        if missing:
            state = "incomplete"
        elif verify and verified and not is_unread:
            state = "complete"
        else:
            state = "unverified"
        return {
            "run_id": run_id,
            "state": state,
            "missing": missing,
            "local_only_artifacts": failed_uploads,
            "verified_code_reference": verified,
            "advisories": advisories,
        }

    def _list_kind(self, run_id: str, kind: str | None) -> list[dict] | None:
        """This run's own artifacts of ``kind``, asked of the server; for None all of them but the
        per-file code captures (never a failed upload, and thousands on a converted snapshot).
        None when the read failed, which says nothing about them (never "missing")."""
        from ....artifact.listing import read_artifact_rows

        try:
            if kind is None:
                rows = read_artifact_rows(
                    lambda query: self.transport.request(
                        "GET", f"/v1/runs/{run_id}/artifacts", params=query, idempotent=True
                    ),
                    {"include_captured": "false"},
                )
            else:
                rows = self.list_run_artifacts(run_id, kind=kind)
        except Exception:  # noqa: BLE001 -- unread is not absent
            return None
        return [item for item in rows if kind is None or item.get("kind") == kind]


def _failed_uploads(artifacts: list[dict]) -> list:
    """References from a FAILED managed upload: a capture gap (an intentional one is not: meta.upload)."""
    return [
        item.get("id") or item.get("name")
        for item in artifacts
        if item.get("is_reference") and (item.get("meta") or {}).get("upload") == "failed"
    ]


def _is_archive_still_queued(snapshot_meta: dict, artifacts: list[dict]) -> bool:
    """The code-snapshot row says its archive was queued (run open), and no landed upload of
    THAT archive (its hash; a failed upload's reference row does not count) is in ``artifacts``.
    A row the capture backfill converted to per-file storage holds its bytes elsewhere.
    Twin: `app/runs/reads/reproduce.py` `_has_code_archive`."""
    from ....run.files.code_upload import CODE_STORAGE_ARTIFACTS

    code_bytes = snapshot_meta.get("code_bytes")
    if not isinstance(code_bytes, dict) or not code_bytes.get("queued"):
        return False
    if CODE_STORAGE_ARTIFACTS in (snapshot_meta.get("storage"), code_bytes.get("storage")):
        return False
    archive_sha256 = code_bytes.get("archive_sha256")
    if not isinstance(archive_sha256, str):
        return True  # no usable hash: no landed row can be shown to be it
    return not any(
        item.get("kind") == "code_bytes"
        and not item.get("is_reference")
        and item.get("status", "complete") == "complete"
        and item.get("content_hash") == archive_sha256
        for item in artifacts
    )
