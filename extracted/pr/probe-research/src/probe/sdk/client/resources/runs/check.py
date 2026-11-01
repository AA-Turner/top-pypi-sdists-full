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
        if not any(item.get("kind") == "code_snapshot" for item in artifacts):
            missing.append("code_snapshot_artifact")
        # A reference recorded because a managed upload FAILED (fold #16 fail-open) is a
        # real capture gap: its bytes never reached R2. An INTENTIONAL path reference (a
        # shared-volume checkpoint the agent resolves locally) is NOT -- it names bytes
        # that exist, just off-platform. Distinguish by meta.upload, not uri presence:
        # both now carry a file:// uri, so the old `not uri` test would both miss the
        # failure and false-flag every intentional reference.
        failed_uploads = [
            item.get("id") or item.get("name")
            for item in artifacts
            if item.get("is_reference") and (item.get("meta") or {}).get("upload") == "failed"
        ]
        if failed_uploads:
            missing.append("portable_artifact_bytes")

        # Free: the manifest summary already rode in on the artifact's meta, so
        # this costs a dict lookup. A file classified as needing upload whose
        # bytes nobody stored is unrecoverable exactly like a dead reference --
        # and this is the failure mode per-file capture INTRODUCED, so leaving it
        # unchecked would repeat the original mistake in a new place.
        snapshot_meta: dict = next(
            ((item.get("meta") or {}) for item in artifacts if item.get("kind") == "code_snapshot"),
            {},
        )
        pending = snapshot_meta.get("n_pending_upload")
        if isinstance(pending, int) and pending > 0:
            missing.append("pending_code_bytes")

        advisories: list[str] = []
        launch = metadata.get("launch") or {}
        if not launch:
            # Pre-capture-core run: honest advisory, not a verdict flip --
            # otherwise every historical run reads incomplete and the exit-2
            # gate becomes noise during migration.
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
        # A note FILE: `note` is not a kind, so the server stores one as `other`
        # with the word in `meta.kind_label`; a row the backfill has not reached
        # yet still says `note` itself.
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
            # Typed like `n_pending_upload` above, and for the same reasons.
            # `isinstance` rather than `== 0`, because this is server-supplied
            # JSON and Python's `False == 0` would let a malformed meta collect
            # `complete`. PRESENT rather than defaulted, because an absent key
            # is a pre-0.26.3 run that recorded no manifest at all -- unknown,
            # never zero, or the no-manifest case below collects the verdict on
            # a missing key. A test pins both.
            #
            # An OFFSITE reference (a file over the size threshold) deliberately
            # does NOT disqualify a run here. Its bytes are off-platform, so
            # this is not a claim that the run rebuilds from Probe alone -- it
            # is the same judgment `capture-run-inputs` states to agents: a
            # deliberate size reference is part of a complete capture, not a gap
            # in one. A rebuild needs that volume mounted, and `snapshot-restore`
            # reports it as OFF-PLATFORM rather than as a failure.
            self_contained = (
                isinstance(n_git_referenced, int)
                and not isinstance(n_git_referenced, bool)
                and n_git_referenced == 0
            )
            if self_contained:
                # Nothing in this manifest depends on anything but Probe for its
                # bytes, and `missing` already proved no upload is outstanding.
                # The code record is self-contained, so it is complete WITHOUT a
                # network probe -- and a stale `base_commit`, which is now
                # provenance rather than a retrieval path, must not fail a run
                # whose bytes are in R2.
                verified = True
            elif base_commit and remote:
                # A run captured while git referencing was live: some of its
                # bytes exist only on that remote, so the probe is still the
                # only thing that can tell a live reference from a dead one.
                verified = _snapshot.commit_on_remote(str(remote), str(base_commit))
                if not verified:
                    missing.append("unresolvable_code_reference")
            else:
                # Pre-0.26.3 runs recorded no manifest, so there is nothing to
                # resolve against. Absence of evidence; say so rather than
                # inventing a pass or a failure.
                verified = False

        if missing:
            state = "incomplete"
        elif verify and verified:
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
