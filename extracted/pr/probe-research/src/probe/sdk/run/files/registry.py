"""ArtifactRegistryMixin, Run's methods: find, promote and cite what the run knows: artifacts by
name or hash, sandbox base state, datasets and checkpoints used or made."""

from __future__ import annotations
from collections.abc import Iterable, Mapping
import os
from typing import TYPE_CHECKING, Any
from ...artifact.filetype import file_extension

if TYPE_CHECKING:

    from ...catalog.refs import DatasetRef


class ArtifactRegistryMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def list_artifacts(self, *, scope: str = "all", **filters: Any) -> list[dict]:
        """Artifacts visible to this run. Defaults to ``scope="all"`` -- the run's own
        artifacts PLUS the ones promoted to its experiment and project, each tagged
        ``source_level`` -- because during a run that inherited context is usually what
        you want. Pass ``scope="own"`` to see only this run's, ``scope="inherited"`` for
        just the parent levels. Extra kwargs (``kind``, ``step_from``, ``step_to``) filter
        server-side."""
        return self._client.list_run_artifacts(self.id, scope=scope, **filters)

    def reconcile_artifact(self, name: str, content_hash: str) -> dict | None:
        """This run's already-recorded artifact with ``name`` AND ``content_hash``.

        OPT-IN helper: the SDK's own ``log_artifact`` does NOT call this yet, so a
        caller that retries artifact creation must invoke it explicitly.

        A proxy in front of the API can return 502 AFTER the write has landed, so
        the response is lost while the artifact exists. A blind retry then records
        the same bytes twice, and later selection
        (``next(a for a in arts if a["kind"] == "checkpoint")``) silently chooses
        between duplicates.

        Matching on the content hash makes this exact rather than a guess:
        artifacts are content-addressed, so identical hash under the same name on
        the same run IS the same artifact.
        """
        if not content_hash:
            return None
        for row in self._client.list_run_artifacts(self.id, name=name, scope="own") or []:
            if row.get("content_hash") == content_hash:
                return row
        # The server is not the only place a record can be. Under async the
        # original `log_artifact` may have journaled, so the artifact exists as
        # a queued op and the listing above sees nothing -- the caller then
        # re-logs, and BOTH land when the queue drains, producing exactly the
        # duplicate this method exists to prevent. A queued match is reported
        # with `state: "queued"` rather than a server row, because it has no id
        # yet and pretending otherwise would be a different lie.
        try:
            queued = self._queued_ops(self._client.journal.pending())
        except Exception:  # noqa: BLE001 -- no journal, or unreadable; the
            queued = []  # server listing above is still a valid answer
        for op in queued:
            if op.get("method") != "POST" or not str(op.get("path", "")).endswith("/artifacts"):
                continue
            body = op.get("body") or {}
            if body.get("name") == name and body.get("content_hash") == content_hash:
                return {**body, "state": "queued"}
        return None

    def resolve_artifact(self, name: str, *, scope: str = "all") -> dict | None:
        """The nearest artifact named ``name`` visible to this run, or ``None``. The
        backend returns nearest-wins order (run before experiment before project), so a
        run-level artifact shadows a same-named one promoted higher.

        An exact miss falls back to ``name`` plus ONE extension, because uploads keep
        the file's extension now (:mod:`probe.sdk.artifact.filetype`): a script that logged
        ``log_artifact("ckpt", path="ckpt-4000.pt")`` stored ``ckpt.pt`` and would
        otherwise stop finding its own artifact. The fallback costs one extra listing
        and only on a miss, so the hit path is unchanged.

        Nearest-wins still decides, and among equals at the same level the FIRST match
        wins -- with both ``ckpt.pt`` and ``ckpt.tar`` present, ``"ckpt"`` is genuinely
        ambiguous and this picks one. Pass the full name to say which.
        """
        rows = self._client.list_run_artifacts(self.id, name=name, scope=scope)
        if rows:
            return rows[0]
        stem = f"{name}."
        for row in self._client.list_run_artifacts(self.id, scope=scope):
            candidate = row.get("name") or ""
            if candidate.startswith(stem) and file_extension(candidate) == candidate[len(stem) :]:
                return row
        return None

    def claim_sandbox_base_state(
        self,
        ref: str,
        owner_key: str,
        *,
        strict: bool | None = None,
    ) -> dict[str, Any]:
        """Elect one worker to archive a shared sandbox begin state.

        Under fail-open operation an unavailable/older server returns
        ``capture_here=True`` and ``coordinated=False``: duplicate work is
        preferable to losing the only recoverable begin state.
        """
        if not ref.strip():
            raise ValueError("base-state ref must not be blank")
        if not owner_key.strip():
            raise ValueError("base-state owner_key must not be blank")
        strict_resolved = (not self._client.fail_open) if strict is None else strict
        try:
            return self._client.claim_sandbox_base_state(self.id, ref, owner_key)
        except Exception:  # noqa: BLE001 -- fail-open capture survives API drift/outage
            if strict_resolved:
                raise
            return {
                "ref": ref,
                "owner_key": owner_key,
                "capture_here": True,
                "coordinated": False,
            }

    def promote_artifact(self, artifact_id: str, *, to: str) -> dict:
        """Promote one of this run's artifacts up to its experiment or project so every
        run under that scope can see it (``to="experiment"`` or ``"project"``). Sugar over
        ``Client.move_artifact``; the target scope is derived from this run's chain."""
        return self._client.move_artifact(artifact_id, level=to)

    # -- the data catalog (plan data-catalog C5; `probe.sdk.catalog`) --------
    # What this run used and made, as the team's datasets, sources and
    # checkpoints. Each warns once and returns quietly on an old server, a
    # network error or a refusal: none raises into the job.

    def use_dataset(self, ref: Any, *, role: str = "train", share: float | None = None) -> None:
        """Record that this run used a dataset version or a source (``ref``: a
        ``str`` such as ``"dataset:c4-clean@3"``, or what ``probe.source`` /
        :meth:`log_dataset` returned) for ``role``: ``train``, ``validation``,
        ``test``, ``eval``, ``init``, ``tokenizer`` or ``other``. A bare
        ``dataset:<name>`` is pinned to the version that is current now.
        ``share``: its weight in a training mix (see :meth:`use_mixture`)."""
        from ... import catalog

        catalog.use(self, ref, role=role, share=share, what="use_dataset")

    def use_mixture(self, parts: Mapping[Any, float], *, role: str = "train") -> None:
        """Record what this run trained on as a mixture, ``{ref: share}`` with
        shares summing to 1: one request that replaces the run's shares for
        ``role``, so separate calls cannot drift past 1."""
        from ... import catalog

        catalog.use_mixture(self, parts, role=role)

    def use_checkpoint(self, ref: str, *, role: str = "init") -> None:
        """Record a checkpoint this run used: ``checkpoint:<id>`` or
        ``checkpoint:<run>@best|latest|step<N>``. The weights it started from
        are role ``init`` (the default); a run that evaluates the checkpoint
        passes ``role="eval"``."""
        from ... import catalog

        catalog.use(self, ref, role=role, what="use_checkpoint")

    def log_dataset(
        self,
        path_or_uri: str | os.PathLike,
        name: str,
        *,
        register: bool = True,
        publish: bool = False,
        upload: bool = False,
        sources: Iterable[Any] = (),
        note: str | None = None,
        stats: Mapping[str, Any] | None = None,
        hash: str = "budget",  # noqa: A002 - the plan's name
        composition: Mapping[Any, Any] | None = None,
        preview: bool = True,
        description: str | None = None,
    ) -> DatasetRef:
        """Record a dataset this run produced -- a file, a folder or a remote
        uri -- as the next version of the team dataset ``name`` (``register``),
        and return a :class:`~probe.sdk.catalog.refs.DatasetRef` (``.ref`` is
        ``dataset:<name>@<n>``).

        Bytes stay where they are by default: a folder is identified by its
        manifest (each file's path, size and sha256, hashed within the run's I/O
        budget; past it a file is fingerprinted and the version is ``partial``;
        ``hash="full"`` hashes everything), a remote uri by itself
        (``pointer``). ``upload=True`` stores the file or folder in Probe
        instead (uploads before it returns). ``sources``: what it was derived
        from; ``note``: what changed and why; ``stats``: counts from the closed
        list ``files``, ``bytes``, ``rows``, ``tokens``, ``removed`` (whole
        numbers >= 0; any other key is dropped with a warning, so put other
        numbers in ``note``); ``composition``: ``{ref: rows}`` (shares
        computed) or ``{ref: share}`` for a dataset built from others, each ref
        a dataset (``dataset:<name>@<n>``) or a source (``probe.source(...)``,
        e.g. 80% a Hub dataset and 20% an HTTPS CSV). ``publish=True`` is needed from a
        read-restricted project. ``register=False`` records the run's file only
        and returns its ``artifact:<id>``. A dataset kept outside Probe gets a
        100-record preview sample uploaded (``preview=False`` turns it off).

        Waits at most 10 s for Probe; past that the ref comes back
        ``pending=True`` and fills in when the registration lands
        (``DatasetRef.wait()``). Never raises."""
        from ... import catalog

        return catalog.log_dataset(
            self, path_or_uri, name, register=register, publish=publish, upload=upload, sources=sources,
            note=note, stats=stats, hash=hash, composition=composition, preview=preview,
            description=description,
        )
